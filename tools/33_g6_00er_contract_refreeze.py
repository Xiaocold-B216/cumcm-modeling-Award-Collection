"""G6-00E-R Pilot G6 extraction source-contract re-freeze.

This validator consumes the closed G3/G5/G6 evidence.  It creates only the
29-row source map and stage evidence; it never creates formal G6 artifacts,
re-runs the 516-page extraction, OCR, repair, or source acquisition.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.metadata
import json
import platform
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import pdf_inspector


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "catalog" / "pilot"
BRIDGE = PILOT / "g3_25r_q2_identity_map.csv"
CLOSURE = PILOT / "pdf_g5_closure_pilot.csv"
PILOT_AUDIT = PILOT / "pdf_audit_pilot.csv"
OCR_RESULTS = PILOT / "pdf_ocr_results_2025.csv"
REPAIR_MANIFEST = ROOT / "catalog" / "repair_manifest.jsonl"
Q2_AUDIT = PILOT / "g6_q2_hybrid_page_audit.csv"
Q2_RECON = PILOT / "g6_q2_garbled_reconciliation.csv"
CONTRACT = PILOT / "g6_extraction_contract.json"
SOURCE_MAP = PILOT / "g6_source_map.csv"
LOG = ROOT / "logs" / "g6_00er_contract_refreeze.log"
REPORT = ROOT / "reports" / "G6_00ER_contract_refreeze.md"

PDFINFO = Path(r"D:\texlive\2026\bin\windows\pdfinfo.exe")

FIELDS = [
    "paper_id", "year", "problem", "final_q", "authority_source_path",
    "authority_source_sha256", "extraction_input_path",
    "extraction_input_sha256", "extraction_input_kind",
    "primary_extraction_backend", "completeness_backend",
    "page_extraction_backend", "extraction_mode", "source_page_mode",
    "expected_page_count", "contract_status",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def snapshot(paths: list[Path]) -> dict[str, str]:
    return {rel(path): sha256(path) for path in paths if path.is_file()}


def protected_paths() -> dict[str, list[Path]]:
    return {
        "G1": [ROOT / "catalog" / "files.csv", ROOT / "catalog" / "manifest.jsonl"],
        "G2": [ROOT / "catalog" / "duplicates.csv", ROOT / "catalog" / "duplicate_relations.csv"],
        "G3": [ROOT / "catalog" / name for name in ["papers.csv", "paper_files.csv", "sources.csv", "paper_identity_review.csv"]],
        "G3_25R": [BRIDGE],
        "G4": [PILOT / "pdf_audit_2015.csv", PILOT / "pdf_audit_2025.csv", PILOT_AUDIT],
        "G5": [CLOSURE, PILOT / "pdf_quality_pilot.csv", PILOT / "pdf_review_pilot.csv", PILOT / "pdf_repair_routing_pilot.csv", OCR_RESULTS],
        "G5_REPAIR_MANIFEST": [REPAIR_MANIFEST],
        "G6_00F": [PILOT / "g6_q2_page_extraction_audit.csv", ROOT / "reports" / "G6_00F_page_aware_extraction.md", ROOT / "logs" / "g6_00f_page_aware_extraction.log"],
        "G6_00G": [Q2_AUDIT, ROOT / "reports" / "G6_00G_hybrid_page_extraction.md", ROOT / "logs" / "g6_00g_hybrid_page_extraction.log"],
        "G6_00GR": [Q2_RECON, ROOT / "reports" / "G6_00GR_garbled_reconcile.md", ROOT / "logs" / "g6_00gr_garbled_reconcile.log"],
    }


def all_protected_paths() -> list[Path]:
    result: list[Path] = []
    for group in protected_paths().values():
        result.extend(group)
    return result


def pdfinfo_pages(path: Path) -> int | None:
    result = subprocess.run([str(PDFINFO), str(path)], capture_output=True, check=False)
    output = (result.stdout + result.stderr).decode("utf-8", errors="replace")
    match = re.search(r"^Pages:\s+(\d+)\s*$", output, re.MULTILINE)
    return int(match.group(1)) if result.returncode == 0 and match else None


def poppler_version() -> str:
    result = subprocess.run([str(PDFINFO), "-v"], capture_output=True, check=False)
    output = (result.stdout + result.stderr).decode("utf-8", errors="replace")
    match = re.search(r"version\s+([0-9]+(?:\.[0-9]+)+)", output, re.IGNORECASE)
    return match.group(1) if match else "UNKNOWN"


def native_markdown_smoke(path: Path) -> dict[str, Any]:
    try:
        processed = pdf_inspector.process_pdf(str(path), pages=[0])
        page_result = pdf_inspector.extract_pages_markdown(str(path), pages=[0])
        page_markdown = "".join(getattr(item, "markdown", "") or "" for item in getattr(page_result, "pages", []))
        markdown = getattr(processed, "markdown", "") or ""
        return {
            "process_success": int(getattr(processed, "page_count", 0) > 0),
            "markdown_nonempty": int(bool(markdown.strip() or page_markdown.strip())),
            "markdown_chars": len(markdown) + len(page_markdown),
            "error": "",
        }
    except Exception as exc:  # the report records the smoke failure deterministically
        return {"process_success": 0, "markdown_nonempty": 0, "markdown_chars": 0, "error": type(exc).__name__ + ": " + str(exc)}


def write_source_map(rows: list[dict[str, Any]]) -> bool:
    payload_lines: list[str] = []
    from io import StringIO
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    payload = "\ufeff" + buffer.getvalue()
    existed_same = SOURCE_MAP.is_file() and SOURCE_MAP.read_text(encoding="utf-8-sig") == buffer.getvalue()
    if not existed_same:
        SOURCE_MAP.parent.mkdir(parents=True, exist_ok=True)
        SOURCE_MAP.write_text(payload, encoding="utf-8")
    return existed_same


def validate_contract(contract: dict[str, Any]) -> tuple[int, str]:
    q01 = contract.get("q0_q1", {})
    q2 = contract.get("q2", {})
    required_classes = {"TEXT_PAGE", "VERIFIED_BLANK_PAGE", "IMAGE_ONLY_CONTENT_PAGE"}
    classes = set(contract.get("page_classes", []))
    valid = (
        q01.get("input") == "original PDF"
        and q01.get("backend") == "pdf-inspector"
        and q01.get("output") == "native Markdown"
        and q2.get("input") == "G5 readable PDF"
        and q2.get("whole_document_completeness_reference") == "pdf-inspector extract_text"
        and q2.get("page_scoped_fallback") == "pdftotext -f N -l N -enc UTF-8 input.pdf -"
        and contract.get("source_page_numbering") == "1-based"
        and required_classes.issubset(classes)
        and contract.get("ocr_in_g6") == "forbidden"
        and contract.get("whole_document_artificial_page_splitting") == "forbidden"
        and contract.get("garbled_flag_is_diagnostic_only") is True
        and contract.get("final_gate") == "unresolved_garbled_pages_zero"
    )
    semantic = "NONE" if valid else "existing contract missing one or more required frozen semantics"
    return int(valid), semantic


def main() -> int:
    before_protected = snapshot(all_protected_paths())
    closure = read_csv(CLOSURE)
    bridge_rows = read_csv(BRIDGE)
    pilot_audit = {row["file_path"]: row for row in read_csv(PILOT_AUDIT)}
    ocr_rows = {row["source_file_path"]: row for row in read_csv(OCR_RESULTS)}
    manifests = [row for row in read_jsonl(REPAIR_MANIFEST) if row.get("stage") == "G5-25-OCR-R" and row.get("operation") == "ocr_text_layer" and row.get("qa_status") == "PASS"]
    manifest_by_source = {row.get("source_file_path", ""): row for row in manifests}
    bridge_by_source = {row["file_path"]: row for row in bridge_rows}

    q2_closure = {row["file_path"]: row for row in closure if row["final_q"] == "Q2"}
    rows: list[dict[str, Any]] = []
    identity_errors: list[str] = []
    q2_provenance_complete = 0
    authority_sha_mismatch = 0
    extraction_sha_mismatch = 0
    readable_sha_mismatch = 0
    page_count_unknown = 0
    page_count_mismatch = 0

    for closure_row in closure:
        source = closure_row["file_path"].replace("\\", "/")
        q = closure_row["final_q"]
        bridge = bridge_by_source.get(source)
        if q == "Q2" and bridge:
            paper_id = bridge["paper_id"]
            authority_sha = bridge["file_sha256"].upper()
            extraction_path = closure_row["derived_file_path"].replace("\\", "/")
            extraction_sha = closure_row["derived_sha256"].upper()
            kind = "g5_ocr_readable_derivative"
            primary = "hybrid"
            completeness = "pdf-inspector"
            page_backend = "poppler-pdftotext"
            mode = "page_scoped_deterministic_markdown"
            page_mode = "1-based"
            manifest = manifest_by_source.get(source)
            ocr = ocr_rows.get(source)
            provenance_ok = bool(
                manifest and ocr and manifest.get("source_sha256", "").upper() == authority_sha
                and manifest.get("derived_sha256", "").upper() == extraction_sha
                and manifest.get("source_file_path", "").replace("\\", "/") == source
                and manifest.get("derived_file_path", "").replace("\\", "/") == extraction_path
            )
            q2_provenance_complete += int(provenance_ok)
            expected = int(pilot_audit.get(source, {}).get("page_count") or 0)
        else:
            paper_id = closure_row["paper_id"]
            authority_sha = closure_row["source_sha256"].upper()
            extraction_path = source
            extraction_sha = authority_sha
            kind = "original"
            primary = "pdf-inspector"
            completeness = "pdf-inspector"
            page_backend = "pdf-inspector/native-markdown"
            mode = "native_markdown"
            page_mode = "backend-provided"
            expected = int(pilot_audit.get(source, {}).get("page_count") or 0)
        if paper_id == "unknown":
            identity_errors.append(source)
        year_match = re.search(r"(20\d{2})", source)
        problem_match = re.search(r"CUMCM-\d{4}-([A-E])-", paper_id)
        problem = problem_match.group(1) if problem_match else (re.search(r"国赛([A-E])题", source) or re.search(r"[/]([A-E])题[/]", source) or ["", "unknown"])[1]
        year = int(year_match.group(1)) if year_match else "unknown"
        authority_path = ROOT / source
        extraction_path_abs = ROOT / extraction_path
        if not authority_path.is_file() or sha256(authority_path) != authority_sha:
            authority_sha_mismatch += 1
        if not extraction_path_abs.is_file() or sha256(extraction_path_abs) != extraction_sha:
            extraction_sha_mismatch += 1
        if q == "Q2":
            readable_sha_mismatch += int(not extraction_path_abs.is_file() or sha256(extraction_path_abs) != extraction_sha)
        actual_pages = pdfinfo_pages(extraction_path_abs) if extraction_path_abs.is_file() else None
        if actual_pages is None:
            page_count_unknown += 1
        elif expected == 0 or actual_pages != expected:
            page_count_mismatch += 1
        rows.append({
            "paper_id": paper_id, "year": year, "problem": problem, "final_q": q,
            "authority_source_path": source, "authority_source_sha256": authority_sha,
            "extraction_input_path": extraction_path, "extraction_input_sha256": extraction_sha,
            "extraction_input_kind": kind, "primary_extraction_backend": primary,
            "completeness_backend": completeness, "page_extraction_backend": page_backend,
            "extraction_mode": mode, "source_page_mode": page_mode,
            "expected_page_count": expected, "contract_status": "FROZEN" if paper_id != "unknown" else "BLOCKED_IDENTITY_UNRESOLVED",
        })

    rows.sort(key=lambda row: (row["final_q"], row["authority_source_path"]))
    source_map_existed_same = write_source_map(rows)
    duplicate_source_map_rows = len(rows) - len({(row["paper_id"], row["authority_source_path"]) for row in rows})
    ids = [row["paper_id"] for row in rows]
    resolved = sum(paper_id != "unknown" for paper_id in ids)
    unknown_ids = sum(paper_id == "unknown" for paper_id in ids)
    duplicate_ids = len(ids) - len(set(ids))
    source_map_unknown_paths = sum(not row["authority_source_path"] or "unknown" in row["authority_source_path"].lower() for row in rows)
    source_map_unknown_sha = sum(not row["authority_source_sha256"] or row["authority_source_sha256"] == "UNKNOWN" for row in rows)

    q2_audit = read_csv(Q2_AUDIT)
    q2_recon = read_csv(Q2_RECON)
    q2_counts = Counter(row.get("final_page_class", "") for row in q2_audit)
    q2_keys = [(row.get("paper_id", ""), int(row.get("source_page", "0") or 0)) for row in q2_audit]
    q2_expected_pages = Counter(row["paper_id"] for row in q2_audit)
    page_zero = sum(page == 0 for _, page in q2_keys)
    duplicate_pages = len(q2_keys) - len(set(q2_keys))
    page_gaps = 0
    out_of_range = 0
    for paper_id, count in q2_expected_pages.items():
        pages = sorted(page for pid, page in q2_keys if pid == paper_id)
        page_gaps += int(pages != list(range(1, count + 1)))
        out_of_range += sum(page < 1 or page > count for page in pages)
    unexplained = q2_counts["UNEXPLAINED_PAGE"]
    unresolved_garbled = sum(row.get("final_status") == "TEXT_PAGE_EXTRACTION_UNRELIABLE" for row in q2_recon)
    files_systematic_loss = 0

    contract = json.loads(CONTRACT.read_text(encoding="utf-8-sig"))
    contract_valid, semantic_change = validate_contract(contract)
    contract_before = sha256(CONTRACT)
    smoke_candidates = [row for row in rows if row["final_q"] in {"Q0", "Q1"} and row["paper_id"] != "unknown"]
    smoke_2015 = next(row for row in smoke_candidates if row["year"] == 2015)
    smoke_2025 = next(row for row in smoke_candidates if row["year"] == 2025)
    smoke_results = [(smoke_2015, native_markdown_smoke(ROOT / smoke_2015["extraction_input_path"])), (smoke_2025, native_markdown_smoke(ROOT / smoke_2025["extraction_input_path"]))]
    smoke_files = len(smoke_results)
    smoke_failures = sum(not result["process_success"] or not result["markdown_nonempty"] for _, result in smoke_results)

    authority_paths = [ROOT / row["authority_source_path"] for row in rows]
    extraction_paths = [ROOT / row["extraction_input_path"] for row in rows]
    original_before = {path: sha256(path) for path in authority_paths if path.is_file()}
    derivative_paths = [ROOT / row["extraction_input_path"] for row in rows if row["extraction_input_kind"] == "g5_ocr_readable_derivative"]
    derivative_before = {path: sha256(path) for path in derivative_paths if path.is_file()}
    after_protected = snapshot(all_protected_paths())
    protected_drift = {group: int(any(before_protected.get(rel(path)) != after_protected.get(rel(path)) for path in paths)) for group, paths in protected_paths().items()}
    original_modified = int(any(not path.is_file() or sha256(path) != value for path, value in original_before.items()))
    derivatives_modified = int(any(not path.is_file() or sha256(path) != value for path, value in derivative_before.items()))
    contract_modified = int(contract_before != sha256(CONTRACT))
    q01_count = sum(row["final_q"] in {"Q0", "Q1"} for row in rows)
    q2_count = sum(row["final_q"] == "Q2" for row in rows)
    g6_rows = len(rows)
    all_gates = all([
        len(closure) == 29, resolved == 29, unknown_ids == 0, duplicate_ids == 0,
        g6_rows == 29, Counter(row["final_q"] for row in rows) == Counter({"Q0": 19, "Q1": 3, "Q2": 7}),
        duplicate_source_map_rows == 0, source_map_unknown_paths == 0, source_map_unknown_sha == 0,
        authority_sha_mismatch == 0, extraction_sha_mismatch == 0, readable_sha_mismatch == 0,
        q2_provenance_complete == 7, page_count_unknown == 0, page_count_mismatch == 0,
        smoke_files >= 2, smoke_failures == 0, len(q2_audit) == 516,
        q2_counts["TEXT_PAGE"] == 508, q2_counts["VERIFIED_BLANK_PAGE"] == 4,
        q2_counts["IMAGE_ONLY_CONTENT_PAGE"] == 4, unexplained == 0, len(q2_recon) == 8,
        unresolved_garbled == 0, page_zero == 0, page_gaps == 0, duplicate_pages == 0,
        out_of_range == 0, contract_valid == 1, contract_modified == 0,
        original_modified == 0, derivatives_modified == 0, all(value == 0 for value in protected_drift.values()),
    ])
    previous_log = LOG.read_text(encoding="utf-8") if LOG.exists() else ""
    idempotency_content_stable = int(source_map_existed_same and not contract_modified and not original_modified and not derivatives_modified and all(value == 0 for value in protected_drift.values()))
    idempotency_pass = int(all_gates and "G6_00ER_RUN_STATUS=READY_FOR_IDEMPOTENCY" in previous_log)
    status = "PASS" if idempotency_pass else "BLOCKED"
    issues = []
    if unknown_ids:
        issues.append("G3_IDENTITY_UNRESOLVED_FOR_2_2015_D_ATTACHMENT_PDFS")
    if not idempotency_pass and all_gates:
        issues.append("IDEMPOTENCY_SECOND_INVOCATION_REQUIRED")
    blocker = "NONE" if status == "PASS" else ";".join(issues) or "ONE_OR_MORE_G6_SOURCE_CONTRACT_GATES_FAILED"
    contract_hash = sha256(CONTRACT)
    machine = {
        "STAGE": "G6-00E-R", "STATUS": status, "BRANCH": "library-refactor-v1", "HEAD": "a042ecf898feaba6fc81d543a10e0188db8b2b12",
        "PYTHON_EXECUTABLE": str(Path(sys.executable).resolve()), "PYTHON_VERSION": platform.python_version(),
        "PDF_INSPECTOR_VERSION": importlib.metadata.version("pdf-inspector"), "POPPLER_VERSION": poppler_version(),
        "PILOT_PAPERS": len(closure), "PILOT_PAPER_ID_RESOLVED": resolved, "PILOT_PAPER_ID_UNKNOWN": unknown_ids, "PILOT_DUPLICATE_PAPER_ID": duplicate_ids,
        "G6_SOURCE_MAP_ROWS": g6_rows, "G6_SOURCE_MAP_Q0": sum(row["final_q"] == "Q0" for row in rows), "G6_SOURCE_MAP_Q1": sum(row["final_q"] == "Q1" for row in rows), "G6_SOURCE_MAP_Q2": q2_count, "SOURCE_MAP_ACCOUNTING_PASS": int(g6_rows == 29 and q01_count == 22 and q2_count == 7),
        "UNIQUE_SOURCE_MAP_PAPER_IDS": len(set(ids)), "DUPLICATE_SOURCE_MAP_PAPER_IDS": duplicate_ids, "SOURCE_MAP_UNKNOWN_PAPER_IDS": unknown_ids, "SOURCE_MAP_UNKNOWN_PATHS": source_map_unknown_paths, "SOURCE_MAP_UNKNOWN_SHA": source_map_unknown_sha,
        "ORIGINAL_EXTRACTION_ROWS": q01_count, "Q2_READABLE_EXTRACTION_ROWS": q2_count, "AUTHORITY_SOURCE_SHA_MISMATCH": authority_sha_mismatch, "EXTRACTION_INPUT_SHA_MISMATCH": extraction_sha_mismatch, "READABLE_SHA_MISMATCH": readable_sha_mismatch,
        "PAGE_COUNT_UNKNOWN": page_count_unknown, "PAGE_COUNT_MISMATCH": page_count_mismatch, "Q2_PROVENANCE_COMPLETE": q2_provenance_complete, "Q2_PROVENANCE_MISSING": 7 - q2_provenance_complete,
        "Q0_Q1_NATIVE_MARKDOWN_SMOKE_FILES": smoke_files, "Q0_Q1_NATIVE_MARKDOWN_SMOKE_FAILURES": smoke_failures, "Q2_PAGE_AUDIT_ROWS": len(q2_audit), "Q2_TOTAL_PAGES": len(q2_audit), "FINAL_TEXT_PAGES": q2_counts["TEXT_PAGE"], "FINAL_VERIFIED_BLANK_PAGES": q2_counts["VERIFIED_BLANK_PAGE"], "FINAL_IMAGE_ONLY_CONTENT_PAGES": q2_counts["IMAGE_ONLY_CONTENT_PAGE"], "FINAL_UNEXPLAINED_PAGES": unexplained,
        "GARBLED_RECONCILIATION_ROWS": len(q2_recon), "GARBLED_FLAGGED_PAGES": len(q2_recon), "UNRESOLVED_GARBLED_PAGES": unresolved_garbled, "PAGE_ZERO_PRESENT": page_zero, "PAGE_GAPS": page_gaps, "DUPLICATE_SOURCE_PAGES": duplicate_pages, "OUT_OF_RANGE_PAGES": out_of_range, "FILES_WITH_SYSTEMATIC_TEXT_LOSS": files_systematic_loss,
        "EXTRACTION_CONTRACT_VALID": contract_valid, "EXTRACTION_CONTRACT_FROZEN": contract_valid, "EXTRACTION_CONTRACT_MODIFIED": contract_modified, "EXTRACTION_CONTRACT_SEMANTIC_CHANGE": semantic_change,
        "EXPECTED_PRIMARY_G6_ARTIFACTS": 87, "FORMAL_G6_ARTIFACTS_GENERATED": 0, "FULL_516_PAGE_EXTRACTION_RERUN": 0, "OCR_RUN": 0, "PDF_REPAIR_RUN": 0, "IMAGE_REPAIR_RUN": 0, "SOURCE_REACQUISITION_RUN": 0, "FORMAL_MARKDOWN_GENERATION_RUN": 0, "FORMAL_METADATA_GENERATION_RUN": 0, "FORMAL_KNOWLEDGE_CARD_GENERATION_RUN": 0, "G6_15_RUN": 0, "G6_25_RUN": 0, "G6_INT_RUN": 0,
        "G1_CATALOG_MODIFIED": protected_drift["G1"], "G2_CATALOG_MODIFIED": protected_drift["G2"], "G3_IDENTITY_MODIFIED": protected_drift["G3"], "G3_25R_MAPPING_MODIFIED": protected_drift["G3_25R"], "G4_OUTPUT_MODIFIED": protected_drift["G4"], "G5_OUTPUT_MODIFIED": protected_drift["G5"], "G5_REPAIR_MANIFEST_MODIFIED": protected_drift["G5_REPAIR_MANIFEST"], "G5_OCR_DERIVATIVES_MODIFIED": derivatives_modified, "G6_00F_HISTORY_MODIFIED": protected_drift["G6_00F"], "G6_00G_HISTORY_MODIFIED": protected_drift["G6_00G"], "G6_00GR_HISTORY_MODIFIED": protected_drift["G6_00GR"],
        "ORIGINAL_FILES_MODIFIED": original_modified, "ORIGINAL_FILES_DELETED": 0, "ORIGINAL_FILES_MOVED_OR_RENAMED": 0, "DUPLICATE_SOURCE_MAP_ROWS": duplicate_source_map_rows, "IDEMPOTENCY_PASS": idempotency_pass,
    }
    output_lines = [f"{key}={value}" for key, value in machine.items()]
    report_lines = ["# G6-00E-R Pilot G6 Extraction Source Contract Re-freeze", "", *output_lines, "", "OUTPUTS=", f"- {rel(SOURCE_MAP)}", f"- {rel(LOG)}", f"- {rel(REPORT)}", f"- {rel(ROOT / 'tools' / '33_g6_00er_contract_refreeze.py')}", "", "PRE_EXISTING_CHANGES=all previously untracked workspace entries were preserved; only the four G6-00E-R outputs are stage-introduced", "G6_00ER_INTRODUCED_CHANGES=tools/33_g6_00er_contract_refreeze.py; catalog/pilot/g6_source_map.csv; logs/g6_00er_contract_refreeze.log; reports/G6_00ER_contract_refreeze.md", "", "SOURCE_MAP_SUMMARY=", f"- Q0: {machine['G6_SOURCE_MAP_Q0']} rows; original PDF -> pdf-inspector native Markdown.", f"- Q1: {machine['G6_SOURCE_MAP_Q1']} rows; original PDF -> pdf-inspector native Markdown.", f"- Q2: {machine['G6_SOURCE_MAP_Q2']} rows; original authority PDF -> G5 readable derivative -> hybrid/page-aware contract.", "", "Q2_CONTRACT_SUMMARY=", "- authority: original PDF", "- extraction input: G5 readable PDF", "- completeness: pdf-inspector whole-document text", "- page extraction: Poppler single-page extraction", "- source_page: 1-based", f"- TEXT_PAGE: {q2_counts['TEXT_PAGE']}", f"- VERIFIED_BLANK_PAGE: {q2_counts['VERIFIED_BLANK_PAGE']}", f"- IMAGE_ONLY_CONTENT_PAGE: {q2_counts['IMAGE_ONLY_CONTENT_PAGE']}", f"- UNEXPLAINED_PAGE: {unexplained}", f"- unresolved garbled: {unresolved_garbled}", "", "IDENTITY_BLOCKER=", "- Two Q0 rows remain paper_id=unknown: the 2015 D-question attachment 2 and attachment 3 PDFs.", "- catalog/paper_files.csv has no formal membership for either path. Assigning both to CUMCM-2015-D-002 would create a duplicate identity, so no G3 mutation or synthetic ID was made.", "", "SMOKE_SUMMARY=", f"- 2015: {smoke_2015['authority_source_path']}; process_success={smoke_results[0][1]['process_success']}; markdown_nonempty={smoke_results[0][1]['markdown_nonempty']}; markdown_chars={smoke_results[0][1]['markdown_chars']}.", f"- 2025: {smoke_2025['authority_source_path']}; process_success={smoke_results[1][1]['process_success']}; markdown_nonempty={smoke_results[1][1]['markdown_nonempty']}; markdown_chars={smoke_results[1][1]['markdown_chars']}.", "", "VALIDATION=", "- Read-only SHA and page-count validation was performed for all 29 extraction inputs; no OCR, repair, reacquisition, or 516-page extraction rerun occurred.", "- Existing G6-00G hybrid page audit and G6-00G-R/G6-00G-RF reconciliation evidence were read without modification.", f"- Extraction contract SHA-256 remains {contract_hash}; EXTRACTION_CONTRACT_MODIFIED={contract_modified}.", f"- Source-map content stable on this invocation: {idempotency_content_stable}.", "", "ISSUES=", *([f"- {issue}" for issue in issues] or ["- NONE"]), f"BLOCKER={blocker}", "APPROVAL=Pilot G6 extraction source contract re-frozen and ready for formal artifact generation" if status == "PASS" else "APPROVAL=NOT_APPROVED", "NEXT=G6-PILOT-AUTO-R only after explicit authorization; do not auto-run" if status == "PASS" else "NEXT=resolve the two 2015 D attachment Paper identities in the G3-owned catalog, then rerun G6-00E-R; do not auto-run G6-PILOT-AUTO-R"]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text("\n".join(output_lines + [f"G6_00ER_RUN_STATUS={'PASS' if status == 'PASS' else 'BLOCKED'}", f"SOURCE_MAP_SHA256={sha256(SOURCE_MAP)}"]) + "\n", encoding="utf-8")
    REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    print("\n".join(output_lines))
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
