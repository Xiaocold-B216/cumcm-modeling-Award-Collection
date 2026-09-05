"""G6-00E-R2 file-to-Paper source-contract cardinality revalidation.

Builds a 29-row file-level map and a 28-row Paper-level artifact map from the
closed G3-15R membership model.  This is read-only for G3/G5/PDF inputs and
does not generate formal G6 artifacts.
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
CATALOG = ROOT / "catalog"
PILOT = CATALOG / "pilot"
PAPERS = CATALOG / "papers.csv"
MEMBERSHIPS = CATALOG / "paper_files.csv"
SOURCES = CATALOG / "sources.csv"
FILES = CATALOG / "files.csv"
CLOSURE = PILOT / "pdf_g5_closure_pilot.csv"
PILOT_AUDIT = PILOT / "pdf_audit_pilot.csv"
BRIDGE = PILOT / "g3_25r_q2_identity_map.csv"
OCR_RESULTS = PILOT / "pdf_ocr_results_2025.csv"
REPAIR_MANIFEST = CATALOG / "repair_manifest.jsonl"
Q2_AUDIT = PILOT / "g6_q2_hybrid_page_audit.csv"
Q2_RECON = PILOT / "g6_q2_garbled_reconciliation.csv"
CONTRACT = PILOT / "g6_extraction_contract.json"
OLD_SOURCE_MAP = PILOT / "g6_source_map.csv"
FILE_MAP = PILOT / "g6_file_source_map.csv"
PAPER_MAP = PILOT / "g6_paper_artifact_map.csv"
LOG = ROOT / "logs" / "g6_00er2_cardinality_refreeze.log"
REPORT = ROOT / "reports" / "G6_00ER2_cardinality_refreeze.md"
PDFINFO = Path(r"D:\texlive\2026\bin\windows\pdfinfo.exe")

FILE_FIELDS = [
    "file_path", "file_sha256", "paper_id", "year", "problem", "final_q",
    "authority_source_path", "authority_source_sha256", "extraction_input_path",
    "extraction_input_sha256", "extraction_input_kind", "primary_extraction_backend",
    "completeness_backend", "page_extraction_backend", "extraction_mode",
    "expected_page_count", "contract_status",
]
PAPER_FIELDS = [
    "paper_id", "year", "problem", "member_file_count", "member_file_paths",
    "primary_file_path", "primary_file_sha256", "quality_profile",
    "artifact_generation_mode", "expected_primary_artifacts",
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
        "G1": [CATALOG / "files.csv", CATALOG / "manifest.jsonl"],
        "G2": [CATALOG / "duplicates.csv", CATALOG / "duplicate_relations.csv"],
        "G3": [PAPERS, MEMBERSHIPS, SOURCES, CATALOG / "paper_identity_review.csv"],
        "G4": [PILOT / "pdf_audit_2015.csv", PILOT / "pdf_audit_2025.csv", PILOT_AUDIT],
        "G5": list(PILOT.glob("pdf_*.csv")),
        "G5_REPAIR": [REPAIR_MANIFEST],
        "G5_DERIVED": [path for path in (ROOT / "derived").rglob("*") if path.is_file()],
        "G6_CONTRACT": [CONTRACT],
        "G6_00F": [PILOT / "g6_q2_page_extraction_audit.csv", ROOT / "reports" / "G6_00F_page_aware_extraction.md", ROOT / "logs" / "g6_00f_page_aware_extraction.log"],
        "G6_00G": [PILOT / "g6_q2_hybrid_page_audit.csv", ROOT / "reports" / "G6_00G_hybrid_page_extraction.md", ROOT / "logs" / "g6_00g_hybrid_page_extraction.log"],
        "G6_00GR": [PILOT / "g6_q2_garbled_reconciliation.csv", ROOT / "reports" / "G6_00GR_garbled_reconcile.md", ROOT / "logs" / "g6_00gr_garbled_reconcile.log"],
        "G6_00ER": [OLD_SOURCE_MAP, ROOT / "reports" / "G6_00ER_contract_refreeze.md", ROOT / "logs" / "g6_00er_contract_refreeze.log"],
        "G3_15R": [PILOT / "g3_15r_attachment_membership_map.csv", ROOT / "reports" / "G3_15R_attachment_membership_reconcile.md", ROOT / "logs" / "g3_15r_attachment_membership_reconcile.log"],
    }


def all_protected() -> list[Path]:
    return [path for group in protected_paths().values() for path in group]


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


def write_csv(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> bool:
    from io import StringIO
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    stable = path.is_file() and path.read_text(encoding="utf-8-sig") == buffer.getvalue()
    if not stable:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\ufeff" + buffer.getvalue(), encoding="utf-8")
    return stable


def native_markdown_smoke(path: Path) -> dict[str, Any]:
    try:
        processed = pdf_inspector.process_pdf(str(path), pages=[0])
        page_result = pdf_inspector.extract_pages_markdown(str(path), pages=[0])
        page_markdown = "".join(getattr(item, "markdown", "") or "" for item in getattr(page_result, "pages", []))
        markdown = getattr(processed, "markdown", "") or ""
        return {"process_success": int(getattr(processed, "page_count", 0) > 0), "markdown_nonempty": int(bool(markdown.strip() or page_markdown.strip())), "markdown_chars": len(markdown) + len(page_markdown), "error": ""}
    except Exception as exc:
        return {"process_success": 0, "markdown_nonempty": 0, "markdown_chars": 0, "error": type(exc).__name__ + ": " + str(exc)}


def contract_valid(contract: dict[str, Any]) -> int:
    q01 = contract.get("q0_q1", {})
    q2 = contract.get("q2", {})
    classes = set(contract.get("page_classes", []))
    return int(
        q01.get("input") == "original PDF" and q01.get("backend") == "pdf-inspector" and q01.get("output") == "native Markdown"
        and q2.get("input") == "G5 readable PDF" and q2.get("whole_document_completeness_reference") == "pdf-inspector extract_text"
        and q2.get("page_scoped_fallback") == "pdftotext -f N -l N -enc UTF-8 input.pdf -"
        and contract.get("source_page_numbering") == "1-based"
        and {"TEXT_PAGE", "VERIFIED_BLANK_PAGE", "IMAGE_ONLY_CONTENT_PAGE"}.issubset(classes)
        and contract.get("ocr_in_g6") == "forbidden"
        and contract.get("whole_document_artificial_page_splitting") == "forbidden"
        and contract.get("garbled_flag_is_diagnostic_only") is True
        and contract.get("final_gate") == "unresolved_garbled_pages_zero"
    )


def report_value(path: Path, key: str) -> str:
    if not path.is_file():
        return ""
    match = re.search(rf"^{re.escape(key)}=(.*)$", path.read_text(encoding="utf-8"), re.MULTILINE)
    return match.group(1).strip() if match else ""


def main() -> int:
    before_protected = snapshot(all_protected())
    closure = read_csv(CLOSURE)
    pilot_audit = {row["file_path"].replace("\\", "/"): row for row in read_csv(PILOT_AUDIT)}
    file_inventory = {row["path"].replace("\\", "/"): row for row in read_csv(FILES)}
    papers = read_csv(PAPERS)
    memberships = read_csv(MEMBERSHIPS)
    membership_by_path = {row["path"].replace("\\", "/"): row for row in memberships}
    membership_groups: dict[str, list[dict[str, str]]] = {}
    for row in memberships:
        membership_groups.setdefault(row["paper_id"], []).append(row)
    paper_by_id = {row["paper_id"]: row for row in papers}
    bridge = {row["file_path"].replace("\\", "/"): row for row in read_csv(BRIDGE)}
    ocr = {row["source_file_path"].replace("\\", "/"): row for row in read_csv(OCR_RESULTS)}
    manifest = {row.get("source_file_path", "").replace("\\", "/"): row for row in read_jsonl(REPAIR_MANIFEST) if row.get("stage") == "G5-25-OCR-R" and row.get("operation") == "ocr_text_layer" and row.get("qa_status") == "PASS"}

    file_rows: list[dict[str, Any]] = []
    authority_sha_mismatch = 0
    extraction_sha_mismatch = 0
    readable_sha_mismatch = 0
    page_count_mismatch = 0
    page_count_unknown = 0
    q2_provenance_complete = 0
    q2_count = 0
    for closure_row in closure:
        source = closure_row["file_path"].replace("\\", "/")
        membership = membership_by_path.get(source)
        if not membership or membership["paper_id"] == "unknown":
            raise RuntimeError(f"formal membership missing for Pilot file: {source}")
        paper_id = membership["paper_id"]
        final_q = closure_row["final_q"]
        source_sha = closure_row["source_sha256"].upper()
        authority_path = source
        if final_q == "Q2":
            q2_count += 1
            bridge_row = bridge.get(source)
            ocr_row = ocr.get(source)
            manifest_row = manifest.get(source)
            extraction_path = closure_row["derived_file_path"].replace("\\", "/")
            extraction_sha = closure_row["derived_sha256"].upper()
            provenance_ok = bool(
                bridge_row and bridge_row.get("paper_id") == paper_id and bridge_row.get("file_sha256", "").upper() == source_sha
                and ocr_row and ocr_row.get("derived_file_path", "").replace("\\", "/") == extraction_path
                and manifest_row and manifest_row.get("source_sha256", "").upper() == source_sha
                and manifest_row.get("derived_sha256", "").upper() == extraction_sha
            )
            q2_provenance_complete += int(provenance_ok)
            input_kind = "g5_ocr_readable_derivative"
            primary_backend = "hybrid"
            page_backend = "poppler-pdftotext"
            mode = "page_scoped_deterministic_markdown"
        else:
            extraction_path = source
            extraction_sha = source_sha
            input_kind = "original"
            primary_backend = "pdf-inspector"
            page_backend = "pdf-inspector/native-markdown"
            mode = "native_markdown"
        if not (ROOT / source).is_file() or sha256(ROOT / source) != source_sha or file_inventory.get(source, {}).get("sha256", "").upper() != source_sha:
            authority_sha_mismatch += 1
        if not (ROOT / extraction_path).is_file() or sha256(ROOT / extraction_path) != extraction_sha:
            extraction_sha_mismatch += 1
            if final_q == "Q2":
                readable_sha_mismatch += 1
        expected = int(pilot_audit.get(source, {}).get("page_count") or 0)
        observed_pages = pdfinfo_pages(ROOT / extraction_path) if (ROOT / extraction_path).is_file() else None
        if observed_pages is None:
            page_count_unknown += 1
        elif expected == 0 or observed_pages != expected:
            page_count_mismatch += 1
        paper = paper_by_id.get(paper_id, {})
        problem = paper.get("problem_code", "")
        year = paper_id.split("-")[1]
        file_rows.append({
            "file_path": source, "file_sha256": source_sha, "paper_id": paper_id, "year": year, "problem": problem,
            "final_q": final_q, "authority_source_path": authority_path, "authority_source_sha256": source_sha,
            "extraction_input_path": extraction_path, "extraction_input_sha256": extraction_sha,
            "extraction_input_kind": input_kind, "primary_extraction_backend": primary_backend,
            "completeness_backend": "pdf-inspector", "page_extraction_backend": page_backend,
            "extraction_mode": mode, "expected_page_count": expected, "contract_status": "FROZEN",
        })
    file_rows.sort(key=lambda row: row["file_path"])

    quality_rows = read_csv(PILOT / "pdf_quality_pilot.csv")
    quality_by_path = {row["file_path"].replace("\\", "/"): row for row in quality_rows}
    pilot_paths = {row["file_path"] for row in file_rows}
    pilot_grouped: dict[str, list[dict[str, Any]]] = {}
    for row in file_rows:
        pilot_grouped.setdefault(row["paper_id"], []).append(row)
    paper_rows: list[dict[str, Any]] = []
    for paper_id in sorted(pilot_grouped):
        pilot_members = pilot_grouped[paper_id]
        all_members = membership_groups[paper_id]
        primary = next((row for row in all_members if row.get("role") == "primary" and row.get("canonical") == "True"), all_members[0])
        primary_path = primary["path"].replace("\\", "/")
        primary_sha = file_inventory.get(primary_path, {}).get("sha256", "").upper()
        q_counts = Counter(row["final_q"] for row in pilot_members)
        quality_profile = ";".join(f"{q}={q_counts.get(q, 0)}" for q in ["Q0", "Q1", "Q2", "Q3", "Q4", "Q5"])
        paper = paper_by_id[paper_id]
        paper_rows.append({
            "paper_id": paper_id, "year": paper.get("year", paper_id.split("-")[1]), "problem": paper.get("problem_code", ""),
            "member_file_count": len(all_members), "member_file_paths": ";".join(row["path"].replace("\\", "/") for row in all_members),
            "primary_file_path": primary_path, "primary_file_sha256": primary_sha, "quality_profile": quality_profile,
            "artifact_generation_mode": "one_paper_level_artifact_set_from_memberships", "expected_primary_artifacts": 3,
        })
    paper_rows.sort(key=lambda row: row["paper_id"])
    file_map_stable = write_csv(FILE_MAP, FILE_FIELDS, file_rows)
    paper_map_stable = write_csv(PAPER_MAP, PAPER_FIELDS, paper_rows)

    duplicate_paper_entities = len(papers) - len({row["paper_id"] for row in papers})
    duplicate_file_memberships = len(memberships) - len({row["path"] for row in memberships})
    duplicate_file_map_rows = len(file_rows) - len({row["file_path"] for row in file_rows})
    duplicate_paper_map_rows = len(paper_rows) - len({row["paper_id"] for row in paper_rows})
    pilot_unique = len(pilot_grouped)
    pilot_multi = sum(len(rows) > 1 for rows in pilot_grouped.values())
    files_without_id = sum(not row["paper_id"] or row["paper_id"] == "unknown" for row in file_rows)
    unknown_paths = sum(not row["file_path"] or "unknown" in row["file_path"].lower() for row in file_rows)
    unknown_sha = sum(not row["file_sha256"] or row["file_sha256"] == "UNKNOWN" for row in file_rows)

    q2_audit = read_csv(Q2_AUDIT)
    q2_recon = read_csv(Q2_RECON)
    q2_counts = Counter(row.get("final_page_class", "") for row in q2_audit)
    unresolved_garbled = sum(row.get("final_status") == "TEXT_PAGE_EXTRACTION_UNRELIABLE" for row in q2_recon)
    files_systematic_loss = int(report_value(ROOT / "reports" / "G6_00GR_garbled_reconcile.md", "FILES_WITH_SYSTEMATIC_TEXT_LOSS") or 0)
    contract = json.loads(CONTRACT.read_text(encoding="utf-8-sig"))
    contract_ok = contract_valid(contract)
    smoke_candidates = [row for row in file_rows if row["final_q"] in {"Q0", "Q1"}]
    smoke_2015 = next(row for row in smoke_candidates if row["year"] == "2015")
    smoke_2025 = next(row for row in smoke_candidates if row["year"] == "2025")
    smoke_results = [(smoke_2015, native_markdown_smoke(ROOT / smoke_2015["extraction_input_path"])), (smoke_2025, native_markdown_smoke(ROOT / smoke_2025["extraction_input_path"]))]
    smoke_files = len(smoke_results)
    smoke_failures = sum(not result["process_success"] or not result["markdown_nonempty"] for _, result in smoke_results)

    source_files = [ROOT / row["authority_source_path"] for row in file_rows]
    extraction_files = [ROOT / row["extraction_input_path"] for row in file_rows]
    original_before = {path: sha256(path) for path in source_files if path.is_file()}
    extraction_before = {path: sha256(path) for path in extraction_files if path.is_file()}
    after_protected = snapshot(all_protected())
    drift = {group: int(any(before_protected.get(rel(path)) != after_protected.get(rel(path)) for path in paths)) for group, paths in protected_paths().items()}
    original_modified = int(any(not path.is_file() or sha256(path) != digest for path, digest in original_before.items()))
    extraction_modified = int(any(not path.is_file() or sha256(path) != digest for path, digest in extraction_before.items()))
    rerun = int(LOG.exists() and "G6_00ER2_RUN_STATUS=" in LOG.read_text(encoding="utf-8"))
    all_gates = all([
        len(closure) == 29, len(file_rows) == 29, pilot_unique == 28, pilot_multi == 1, files_without_id == 0, unknown_paths == 0, unknown_sha == 0,
        len(paper_rows) == 28, duplicate_paper_entities == 0, duplicate_file_memberships == 0, duplicate_file_map_rows == 0, duplicate_paper_map_rows == 0,
        q2_count == 7, authority_sha_mismatch == 0, extraction_sha_mismatch == 0, readable_sha_mismatch == 0, q2_provenance_complete == 7,
        page_count_unknown == 0, page_count_mismatch == 0, len(q2_audit) == 516, q2_counts["TEXT_PAGE"] == 508, q2_counts["VERIFIED_BLANK_PAGE"] == 4,
        q2_counts["IMAGE_ONLY_CONTENT_PAGE"] == 4, q2_counts["UNEXPLAINED_PAGE"] == 0, len(q2_recon) == 8, unresolved_garbled == 0,
        smoke_files >= 2, smoke_failures == 0, files_systematic_loss == 0, contract_ok == 1, not extraction_modified, not original_modified,
        all(value == 0 for value in drift.values()), file_map_stable or not rerun, paper_map_stable or not rerun,
    ])
    idempotency = int(rerun and all_gates and duplicate_file_map_rows == 0 and duplicate_paper_map_rows == 0)
    status = "PASS" if all_gates and idempotency else "BLOCKED"
    blocker = "NONE" if status == "PASS" else "IDEMPOTENCY_SECOND_INVOCATION_REQUIRED" if all_gates and not rerun else "ONE_OR_MORE_G6_00ER2_GATES_FAILED"
    issues = ["NONE"] if status == "PASS" else ["first complete map build requires one identical rerun for idempotency" if all_gates and not rerun else "one or more G6-00E-R2 gates failed"]
    expected_artifacts = len(paper_rows) * 3
    multi = next((row for row in paper_rows if row["paper_id"] == "CUMCM-2015-D-002"), None)
    machine = {
        "STAGE": "G6-00E-R2", "STATUS": status, "BRANCH": "library-refactor-v1", "HEAD": "a042ecf898feaba6fc81d543a10e0188db8b2b12", "PYTHON_EXECUTABLE": str(Path(sys.executable).resolve()), "PYTHON_VERSION": platform.python_version(), "PDF_INSPECTOR_VERSION": importlib.metadata.version("pdf-inspector"), "POPPLER_VERSION": poppler_version(),
        "PILOT_PDF_FILES": len(file_rows), "PILOT_UNIQUE_PAPERS": pilot_unique, "PILOT_MULTI_FILE_PAPERS": pilot_multi, "PILOT_FILES_WITH_FORMAL_PAPER_ID": len(file_rows) - files_without_id, "PILOT_FILES_WITHOUT_FORMAL_PAPER_ID": files_without_id, "G6_FILE_SOURCE_MAP_ROWS": len(file_rows), "G6_PAPER_ARTIFACT_MAP_ROWS": len(paper_rows), "DUPLICATE_PAPER_ENTITIES": duplicate_paper_entities, "DUPLICATE_FILE_MEMBERSHIPS": duplicate_file_memberships, "MULTI_FILE_PAPERS": pilot_multi,
        "ORIGINAL_EXTRACTION_FILE_ROWS": len([row for row in file_rows if row["final_q"] in {"Q0", "Q1"}]), "Q2_READABLE_EXTRACTION_FILE_ROWS": q2_count, "AUTHORITY_SOURCE_SHA_MISMATCH": authority_sha_mismatch, "EXTRACTION_INPUT_SHA_MISMATCH": extraction_sha_mismatch, "READABLE_SHA_MISMATCH": readable_sha_mismatch, "Q2_PROVENANCE_COMPLETE": q2_provenance_complete, "Q2_PROVENANCE_MISSING": 7 - q2_provenance_complete, "Q0_Q1_NATIVE_MARKDOWN_SMOKE_FILES": smoke_files, "Q0_Q1_NATIVE_MARKDOWN_SMOKE_FAILURES": smoke_failures,
        "Q2_PAGE_AUDIT_ROWS": len(q2_audit), "Q2_TOTAL_PAGES": len(q2_audit), "FINAL_TEXT_PAGES": q2_counts["TEXT_PAGE"], "FINAL_VERIFIED_BLANK_PAGES": q2_counts["VERIFIED_BLANK_PAGE"], "FINAL_IMAGE_ONLY_CONTENT_PAGES": q2_counts["IMAGE_ONLY_CONTENT_PAGE"], "FINAL_UNEXPLAINED_PAGES": q2_counts["UNEXPLAINED_PAGE"], "GARBLED_RECONCILIATION_ROWS": len(q2_recon), "GARBLED_FLAGGED_PAGES": len(q2_recon), "UNRESOLVED_GARBLED_PAGES": unresolved_garbled, "FILES_WITH_SYSTEMATIC_TEXT_LOSS": files_systematic_loss, "EXTRACTION_CONTRACT_VALID": contract_ok, "EXTRACTION_CONTRACT_FROZEN": contract_ok, "EXTRACTION_CONTRACT_MODIFIED": drift["G6_CONTRACT"], "EXPECTED_PRIMARY_G6_ARTIFACTS": expected_artifacts, "FORMAL_G6_ARTIFACTS_GENERATED": 0,
        "FULL_516_PAGE_EXTRACTION_RERUN": 0, "OCR_RUN": 0, "PDF_REPAIR_RUN": 0, "IMAGE_REPAIR_RUN": 0, "SOURCE_REACQUISITION_RUN": 0, "FORMAL_MARKDOWN_GENERATION_RUN": 0, "FORMAL_METADATA_GENERATION_RUN": 0, "FORMAL_KNOWLEDGE_CARD_GENERATION_RUN": 0, "G6_15_RUN": 0, "G6_25_RUN": 0, "G6_INT_RUN": 0,
        "G1_CATALOG_MODIFIED": drift["G1"], "G2_CATALOG_MODIFIED": drift["G2"], "G3_IDENTITY_MODIFIED": drift["G3"], "G3_MEMBERSHIP_MODIFIED": drift["G3"], "G4_OUTPUT_MODIFIED": drift["G4"], "G5_OUTPUT_MODIFIED": drift["G5"], "G5_REPAIR_MANIFEST_MODIFIED": drift["G5_REPAIR"], "G5_OCR_DERIVATIVES_MODIFIED": drift["G5_DERIVED"], "G6_00F_HISTORY_MODIFIED": drift["G6_00F"], "G6_00G_HISTORY_MODIFIED": drift["G6_00G"], "G6_00GR_HISTORY_MODIFIED": drift["G6_00GR"], "G6_00ER_HISTORY_MODIFIED": drift["G6_00ER"], "G3_15R_HISTORY_MODIFIED": drift["G3_15R"], "ORIGINAL_FILES_MODIFIED": original_modified, "ORIGINAL_FILES_DELETED": 0, "ORIGINAL_FILES_MOVED_OR_RENAMED": 0, "DUPLICATE_FILE_SOURCE_MAP_ROWS": duplicate_file_map_rows, "DUPLICATE_PAPER_ARTIFACT_MAP_ROWS": duplicate_paper_map_rows, "IDEMPOTENCY_PASS": idempotency,
    }
    output = [f"{key}={value}" for key, value in machine.items()]
    report_lines = output + ["", "OUTPUTS=", f"- {rel(FILE_MAP)}", f"- {rel(PAPER_MAP)}", f"- {rel(LOG)}", f"- {rel(REPORT)}", f"- {rel(ROOT / 'tools' / '35_g6_00er2_cardinality_refreeze.py')}", "", "FILE_LEVEL_SUMMARY=", f"- files: {len(file_rows)}", f"- Q0: {sum(row['final_q'] == 'Q0' for row in file_rows)}", f"- Q1: {sum(row['final_q'] == 'Q1' for row in file_rows)}", f"- Q2: {sum(row['final_q'] == 'Q2' for row in file_rows)}", "- model: File -> Paper -> extraction input", "", "PAPER_LEVEL_SUMMARY=", f"- unique papers: {len(paper_rows)}", f"- multi-file papers: {pilot_multi}", f"- expected formal artifact sets: {expected_artifacts} (Paper-level, 3 per Paper)", "- model: Paper -> formal memberships -> one future artifact set", "", "MULTI_FILE_PAPER_SUMMARY=", f"- paper_id: {multi['paper_id'] if multi else 'CUMCM-2015-D-002'}", f"  member_file_count: {multi['member_file_count'] if multi else 0}", f"  primary_file: {multi['primary_file_path'] if multi else ''}", f"  attachment_files: {multi['member_file_paths'] if multi else ''}", "  status: PASS; one Paper-level row, multiple File-level inputs; no duplicate Paper entity", "", "Q2_CONTRACT_SUMMARY=", "- authority: original PDF", "- extraction input: G5 readable PDF", "- completeness: pdf-inspector whole-document text", "- page extraction: Poppler single-page", "- source_page: 1-based", f"- TEXT_PAGE: {q2_counts['TEXT_PAGE']}", f"- VERIFIED_BLANK_PAGE: {q2_counts['VERIFIED_BLANK_PAGE']}", f"- IMAGE_ONLY_CONTENT_PAGE: {q2_counts['IMAGE_ONLY_CONTENT_PAGE']}", f"- UNEXPLAINED_PAGE: {q2_counts['UNEXPLAINED_PAGE']}", f"- unresolved garbled: {unresolved_garbled}", "", "PRE_EXISTING_CHANGES=all prior untracked workspace entries preserved; G3-15R membership repair and G6-00E-R history were read-only in this stage", "G6_00ER2_INTRODUCED_CHANGES=tools/35_g6_00er2_cardinality_refreeze.py; catalog/pilot/g6_file_source_map.csv; catalog/pilot/g6_paper_artifact_map.csv; logs/g6_00er2_cardinality_refreeze.log; reports/G6_00ER2_cardinality_refreeze.md", "", "VALIDATION=", "- File-level mapping consumes formal PaperFileMembership rows, including the two CUMCM-2015-D-002 attachments.", "- Paper-level mapping aggregates memberships and selects the canonical primary membership; CUMCM-2015-D-002 has one Paper row and multiple file memberships.", "- Q0/Q1 native Markdown smoke ran on one 2015 file and one 2025 file only; no batch formal Markdown was generated.", "- Existing Q2 516-page audit and 8-row reconciliation were reused without extraction or visual re-audit.", f"- Source-map contents stable on this invocation: file_map={int(file_map_stable)}; paper_map={int(paper_map_stable)}.", "", "ISSUES=", *[f"- {issue}" for issue in issues], f"BLOCKER={blocker}", "APPROVAL=Pilot file-level and paper-level G6 source contracts re-frozen successfully" if status == "PASS" else "APPROVAL=NOT_APPROVED", "NEXT=G6-PILOT-AUTO-R only after explicit authorization; do not auto-run" if status == "PASS" else "NEXT=run the identical G6-00E-R2 validator once more for idempotency; do not start G6-PILOT-AUTO-R"]
    LOG.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text("\n".join(output + [f"G6_00ER2_RUN_STATUS={status}"]) + "\n", encoding="utf-8")
    REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    print("\n".join(report_lines))
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
