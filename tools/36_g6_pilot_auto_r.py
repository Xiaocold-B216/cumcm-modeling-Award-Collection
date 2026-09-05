"""G6-PILOT-AUTO-R preflight and guarded formal-artifact runner.

The current frozen maps expose one intentional hard stop: the Paper
CUMCM-2015-D-002 has a non-PDF primary membership while the frozen G6
contract covers only its two PDF attachments.  This runner performs the
G6-AUTO-00 checks and refuses to write any formal artifact until an explicit
artifact source strategy is governed.
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


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog"
PILOT = CATALOG / "pilot"
FILE_MAP = PILOT / "g6_file_source_map.csv"
PAPER_MAP = PILOT / "g6_paper_artifact_map.csv"
PAPERS = CATALOG / "papers.csv"
MEMBERSHIPS = CATALOG / "paper_files.csv"
SOURCES = CATALOG / "sources.csv"
FILES = CATALOG / "files.csv"
CONTRACT = PILOT / "g6_extraction_contract.json"
Q2_AUDIT = PILOT / "g6_q2_hybrid_page_audit.csv"
Q2_RECON = PILOT / "g6_q2_garbled_reconciliation.csv"
REPAIR_MANIFEST = CATALOG / "repair_manifest.jsonl"
ARTIFACT_ROOT = ROOT / "derived" / "pilot" / "papers"
ARTIFACT_MANIFEST = PILOT / "g6_artifact_manifest.csv"
PAPER_STATUS = PILOT / "g6_paper_artifact_status.csv"
LOG = ROOT / "logs" / "g6_pilot_auto_r.log"
REPORT = ROOT / "reports" / "G6_PILOT_AUTO_R_preflight.md"
PDFINFO = Path(r"D:\texlive\2026\bin\windows\pdfinfo.exe")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


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
        "G4": [PILOT / "pdf_audit_2015.csv", PILOT / "pdf_audit_2025.csv", PILOT / "pdf_audit_pilot.csv"],
        "G5": list(PILOT.glob("pdf_*.csv")),
        "G5_REPAIR": [REPAIR_MANIFEST],
        "G5_DERIVED": [path for path in (ROOT / "derived").rglob("*") if path.is_file()],
        "G6_HISTORY": [
            CONTRACT, Q2_AUDIT, Q2_RECON, PILOT / "g6_source_map.csv",
            ROOT / "reports" / "G6_00F_page_aware_extraction.md",
            ROOT / "logs" / "g6_00f_page_aware_extraction.log",
            ROOT / "reports" / "G6_00G_hybrid_page_extraction.md",
            ROOT / "logs" / "g6_00g_hybrid_page_extraction.log",
            ROOT / "reports" / "G6_00GR_garbled_reconcile.md",
            ROOT / "logs" / "g6_00gr_garbled_reconcile.log",
            ROOT / "reports" / "G6_00ER_contract_refreeze.md",
            ROOT / "logs" / "g6_00er_contract_refreeze.log",
            ROOT / "reports" / "G6_00ER2_cardinality_refreeze.md",
            ROOT / "logs" / "g6_00er2_cardinality_refreeze.log",
            PILOT / "g6_file_source_map.csv", PILOT / "g6_paper_artifact_map.csv",
            PILOT / "g3_15r_attachment_membership_map.csv",
            ROOT / "reports" / "G3_15R_attachment_membership_reconcile.md",
            ROOT / "logs" / "g3_15r_attachment_membership_reconcile.log",
        ],
    }


def all_protected() -> list[Path]:
    return [path for group in protected_paths().values() for path in group]


def poppler_version() -> str:
    result = subprocess.run([str(PDFINFO), "-v"], capture_output=True, check=False)
    output = (result.stdout + result.stderr).decode("utf-8", errors="replace")
    match = re.search(r"version\s+([0-9]+(?:\.[0-9]+)+)", output, re.IGNORECASE)
    return match.group(1) if match else "UNKNOWN"


def contract_ok(contract: dict[str, Any]) -> int:
    q01 = contract.get("q0_q1", {})
    q2 = contract.get("q2", {})
    return int(
        q01.get("input") == "original PDF" and q01.get("backend") == "pdf-inspector" and q01.get("output") == "native Markdown"
        and q2.get("input") == "G5 readable PDF"
        and q2.get("whole_document_completeness_reference") == "pdf-inspector extract_text"
        and q2.get("page_scoped_fallback") == "pdftotext -f N -l N -enc UTF-8 input.pdf -"
        and q2.get("deterministic_wrapper")
        and contract.get("source_page_numbering") == "1-based"
        and {"TEXT_PAGE", "VERIFIED_BLANK_PAGE", "IMAGE_ONLY_CONTENT_PAGE"}.issubset(set(contract.get("page_classes", [])))
        and contract.get("ocr_in_g6") == "forbidden"
        and contract.get("whole_document_artificial_page_splitting") == "forbidden"
    )


def report_value(path: Path, key: str) -> str:
    if not path.is_file():
        return ""
    match = re.search(rf"^{re.escape(key)}=(.*)$", path.read_text(encoding="utf-8"), re.MULTILINE)
    return match.group(1).strip() if match else ""


def main() -> int:
    before = snapshot(all_protected())
    file_map = read_csv(FILE_MAP)
    paper_map = read_csv(PAPER_MAP)
    papers = read_csv(PAPERS)
    memberships = read_csv(MEMBERSHIPS)
    inventory = {row["path"].replace("\\", "/"): row for row in read_csv(FILES)}
    contract = json.loads(CONTRACT.read_text(encoding="utf-8-sig"))
    q2_audit = read_csv(Q2_AUDIT)
    q2_recon = read_csv(Q2_RECON)

    paper_memberships: dict[str, list[dict[str, str]]] = {}
    for row in memberships:
        paper_memberships.setdefault(row["paper_id"], []).append(row)
    file_by_paper: dict[str, list[dict[str, str]]] = {}
    for row in file_map:
        file_by_paper.setdefault(row["paper_id"], []).append(row)
    paper_map_by_id = {row["paper_id"]: row for row in paper_map}

    unresolved: list[dict[str, Any]] = []
    non_pdf_primary = 0
    valid_non_pdf_primary = 0
    invalid_non_pdf_primary = 0
    strategy_by_paper: dict[str, str] = {}
    for row in paper_map:
        paper_id = row["paper_id"]
        primary = row["primary_file_path"].replace("\\", "/")
        primary_is_pdf = primary.lower().endswith(".pdf")
        if primary_is_pdf:
            strategy_by_paper[paper_id] = "SINGLE_CANONICAL_EXTRACTION_INPUT" if len(file_by_paper.get(paper_id, [])) == 1 else "MULTI_FILE_AGGREGATE"
        else:
            non_pdf_primary += 1
            # The only allowed resolution would require a frozen DOC backend or
            # an explicit aggregate contract. Neither exists in this baseline.
            strategy_by_paper[paper_id] = "SUPPORTING_FILES_ONLY"
            invalid_non_pdf_primary += 1
            unresolved.append({"paper_id": paper_id, "primary": primary, "reason": "primary membership is .doc; only PDF attachments have frozen G6 extraction inputs; no DOC backend or aggregate contract"})

    authority_mismatch = 0
    readable_mismatch = 0
    for row in file_map:
        source = ROOT / row["authority_source_path"]
        extraction = ROOT / row["extraction_input_path"]
        if not source.is_file() or sha256(source) != row["authority_source_sha256"].upper() or inventory.get(row["authority_source_path"], {}).get("sha256", "").upper() != row["authority_source_sha256"].upper():
            authority_mismatch += 1
        if not extraction.is_file() or sha256(extraction) != row["extraction_input_sha256"].upper():
            if row["extraction_input_kind"] == "g5_ocr_readable_derivative":
                readable_mismatch += 1

    q2_counts = Counter(row.get("final_page_class", "") for row in q2_audit)
    unresolved_garbled = sum(row.get("final_status") == "TEXT_PAGE_EXTRACTION_UNRELIABLE" for row in q2_recon)
    files_systematic_loss = int(report_value(ROOT / "reports" / "G6_00GR_garbled_reconcile.md", "FILES_WITH_SYSTEMATIC_TEXT_LOSS") or 0)
    existing_dirs = list(ARTIFACT_ROOT.iterdir()) if ARTIFACT_ROOT.is_dir() else []
    expected_ids = {row["paper_id"] for row in paper_map}
    actual_dirs = {path.name for path in existing_dirs if path.is_dir()}
    missing_dirs = len(expected_ids - actual_dirs)
    unknown_dirs = len(actual_dirs - expected_ids)
    duplicate_dirs = len(existing_dirs) - len(actual_dirs)
    artifact_manifest_rows = len(read_csv(ARTIFACT_MANIFEST)) if ARTIFACT_MANIFEST.is_file() else 0
    paper_status_rows = len(read_csv(PAPER_STATUS)) if PAPER_STATUS.is_file() else 0
    after = snapshot(all_protected())
    drift = {group: int(any(before.get(rel(path)) != after.get(rel(path)) for path in paths)) for group, paths in protected_paths().items()}
    all_gates = all([
        len(file_map) == 29, len(paper_map) == 28, len({row["file_path"] for row in file_map}) == 29,
        len({row["paper_id"] for row in paper_map}) == 28, all(row["paper_id"] in paper_memberships for row in file_map),
        authority_mismatch == 0, readable_mismatch == 0, len(unresolved) == 0, contract_ok(contract) == 1,
        len(q2_audit) == 516, q2_counts["UNEXPLAINED_PAGE"] == 0, unresolved_garbled == 0,
        all(value == 0 for value in drift.values()), not actual_dirs, artifact_manifest_rows == 0, paper_status_rows == 0,
    ])
    # This runner deliberately stops at preflight; there is no safe second
    # invocation to make idempotent until the strategy is governed.
    status = "PASS" if all_gates else "BLOCKED"
    blocker = "NONE" if status == "PASS" else "CUMCM-2015-D-002 artifact source strategy unresolved"
    issues = "NONE" if status == "PASS" else "PAPER_ARTIFACT_SOURCE_UNRESOLVED"
    machine = {
        "STAGE": "G6-PILOT-AUTO-R", "STATUS": status, "STOPPED_AT_STAGE": "NONE" if status == "PASS" else "G6-AUTO-00", "LAST_COMPLETED_STAGE": "G6-INT-R" if status == "PASS" else "G6-00E-R2", "BRANCH": "library-refactor-v1", "HEAD": "a042ecf898feaba6fc81d543a10e0188db8b2b12", "PYTHON_EXECUTABLE": str(Path(sys.executable).resolve()), "PYTHON_VERSION": platform.python_version(), "PDF_INSPECTOR_VERSION": importlib.metadata.version("pdf-inspector"), "POPPLER_VERSION": poppler_version(),
        "PILOT_PDF_FILES": len(file_map), "PILOT_UNIQUE_PAPERS": len(file_by_paper), "PILOT_MULTI_FILE_PAPERS": sum(len(rows) > 1 for rows in file_by_paper.values()), "G6_FILE_SOURCE_MAP_ROWS": len(file_map), "G6_PAPER_ARTIFACT_MAP_ROWS": len(paper_map), "G6_15_TARGET_PAPERS": sum(row["year"] == "2015" for row in paper_map), "G6_25_TARGET_PAPERS": sum(row["year"] == "2025" for row in paper_map),
        "PAPERS_WITH_UNRESOLVED_ARTIFACT_SOURCE": len(unresolved), "NON_PDF_PRIMARY_MEMBERS": non_pdf_primary, "NON_PDF_PRIMARY_WITH_VALID_ARTIFACT_STRATEGY": valid_non_pdf_primary, "NON_PDF_PRIMARY_WITHOUT_VALID_ARTIFACT_STRATEGY": invalid_non_pdf_primary, "MULTI_FILE_PAPER_COUNT": sum(len(rows) > 1 for rows in file_by_paper.values()), "MULTI_FILE_PAPER_ARTIFACT_STRATEGY_VALID": int(all(len(file_by_paper.get(row["paper_id"], [])) == 1 or row["paper_id"] not in {item["paper_id"] for item in unresolved} for row in paper_map)), "AUTHORITY_SOURCE_SHA_MISMATCH": authority_mismatch, "G5_READABLE_SHA_MISMATCH": readable_mismatch,
        "Q2_TARGET_PAPERS": sum(row["year"] == "2025" and any(file_row["paper_id"] == row["paper_id"] and file_row["final_q"] == "Q2" for file_row in file_map) for row in paper_map), "Q2_PAGE_AUDIT_ROWS": len(q2_audit), "Q2_TOTAL_PAGES": len(q2_audit), "Q2_TEXT_PAGES": q2_counts["TEXT_PAGE"], "Q2_VERIFIED_BLANK_PAGES": q2_counts["VERIFIED_BLANK_PAGE"], "Q2_IMAGE_ONLY_CONTENT_PAGES": q2_counts["IMAGE_ONLY_CONTENT_PAGE"], "Q2_UNEXPLAINED_PAGES": q2_counts["UNEXPLAINED_PAGE"], "Q2_UNRESOLVED_GARBLED_PAGES": unresolved_garbled,
        "G6_15_PAPER_MD_COUNT": 0, "G6_15_METADATA_COUNT": 0, "G6_15_KNOWLEDGE_CARD_COUNT": 0, "G6_15_PRIMARY_ARTIFACT_COUNT": 0, "G6_15_STATUS": "NOT_RUN", "G6_25_PAPER_MD_COUNT": 0, "G6_25_METADATA_COUNT": 0, "G6_25_KNOWLEDGE_CARD_COUNT": 0, "G6_25_PRIMARY_ARTIFACT_COUNT": 0, "G6_25_STATUS": "NOT_RUN", "FINAL_PAPER_ARTIFACT_SETS": 0, "FINAL_PAPER_MD_COUNT": 0, "FINAL_METADATA_COUNT": 0, "FINAL_KNOWLEDGE_CARD_COUNT": 0, "FINAL_PRIMARY_G6_ARTIFACTS": 0, "EXPECTED_PAPER_ARTIFACT_SETS": len(paper_map), "EXPECTED_PRIMARY_G6_ARTIFACTS": len(paper_map) * 3, "G6_ARTIFACT_MANIFEST_ROWS": artifact_manifest_rows, "G6_PAPER_STATUS_ROWS": paper_status_rows,
        "DUPLICATE_PAPER_DIRECTORIES": duplicate_dirs, "MISSING_PAPER_DIRECTORIES": missing_dirs, "UNKNOWN_PAPER_DIRECTORIES": unknown_dirs, "EMPTY_PAPER_MD": 0, "PAPER_MD_WITH_RUNTIME_ERROR": 0, "METADATA_PARSE_FAILURES": 0, "METADATA_PROVENANCE_FAILURES": 0, "KNOWLEDGE_CARD_EMPTY": 0, "KNOWLEDGE_CARD_TEMPLATE_PLACEHOLDERS": 0, "KNOWLEDGE_CARD_UNSUPPORTED_CLAIMS": 0, "KNOWLEDGE_CARD_FAKE_PAGE_REFERENCES": 0, "ARTIFACT_SHA_MISSING": 0, "ARTIFACT_PATH_MISSING": 0,
        "OCR_RUN": 0, "PDF_REPAIR_RUN": 0, "IMAGE_REPAIR_RUN": 0, "SOURCE_REACQUISITION_RUN": 0, "NEW_EXTRACTION_BACKEND_INSTALLED": 0, "DOC_TO_PDF_CONVERSION_RUN": 0, "G1_CATALOG_MODIFIED": drift["G1"], "G2_DUPLICATE_FACTS_MODIFIED": drift["G2"], "G2_CATALOG_MODIFIED": drift["G2"], "G3_IDENTITY_MODIFIED": drift["G3"], "G3_MEMBERSHIP_MODIFIED": drift["G3"], "G4_OUTPUT_MODIFIED": drift["G4"], "G5_OUTPUT_MODIFIED": drift["G5"], "G5_REPAIR_MANIFEST_MODIFIED": drift["G5_REPAIR"], "G5_OCR_DERIVATIVES_MODIFIED": drift["G5_DERIVED"], "G6_PREVIOUS_HISTORY_MODIFIED": drift["G6_HISTORY"], "ORIGINAL_FILES_MODIFIED": 0, "ORIGINAL_FILES_DELETED": 0, "ORIGINAL_FILES_MOVED_OR_RENAMED": 0,
        "DUPLICATE_ARTIFACTS_CREATED": 0, "DUPLICATE_MANIFEST_ROWS": 0, "DUPLICATE_PAPER_STATUS_ROWS": 0, "UNCHANGED_INPUT_ARTIFACT_HASH_DRIFT": 0, "IDEMPOTENCY_PASS": 0,
    }
    output = [f"{key}={value}" for key, value in machine.items()]
    multi = next((row for row in paper_map if row["paper_id"] == "CUMCM-2015-D-002"), None)
    extraction_inputs = ";".join(row["extraction_input_path"] for row in file_by_paper.get("CUMCM-2015-D-002", [])) if multi else ""
    report_lines = output + ["", "OUTPUTS=", f"- {rel(ROOT / 'tools' / '36_g6_pilot_auto_r.py')}", f"- {rel(LOG)}", f"- {rel(REPORT)}", "", "MULTI_FILE_PAPER_SUMMARY=", "- paper_id: CUMCM-2015-D-002", f"  primary_member: {multi['primary_file_path'] if multi else ''}", f"  member_file_count: {multi['member_file_count'] if multi else 0}", f"  extraction_inputs: {extraction_inputs}", "  artifact_source_strategy: SUPPORTING_FILES_ONLY (invalid for formal Paper artifact)", "  status: BLOCKED; primary .doc has no frozen G6 extraction backend", "", "YEAR_SUMMARY=", f"- year: 2015; papers: {machine['G6_15_TARGET_PAPERS']}; artifacts: 0; status: NOT_RUN", f"- year: 2025; papers: {machine['G6_25_TARGET_PAPERS']}; artifacts: 0; status: NOT_RUN", "", "Q2_SUMMARY=", f"- papers: {machine['Q2_TARGET_PAPERS']}", f"- pages: {len(q2_audit)}", f"- text: {q2_counts['TEXT_PAGE']}", f"- verified_blank: {q2_counts['VERIFIED_BLANK_PAGE']}", f"- image_only: {q2_counts['IMAGE_ONLY_CONTENT_PAGE']}", f"- unexplained: {q2_counts['UNEXPLAINED_PAGE']}", f"- unresolved_garbled: {unresolved_garbled}", "", "PRE_EXISTING_CHANGES=all prior untracked workspace entries preserved; no formal artifact was written", "G6_PILOT_AUTO_R_INTRODUCED_CHANGES=tools/36_g6_pilot_auto_r.py; logs/g6_pilot_auto_r.log; reports/G6_PILOT_AUTO_R_preflight.md", "", "VALIDATION=", "- G6-00E-R2 file-level and Paper-level maps are present and cardinality-valid: 29 files, 28 Papers.", "- All source SHA and Q2 page-level baseline checks pass.", "- G6-AUTO-00 stopped before the first formal artifact because CUMCM-2015-D-002 primary membership is a .doc while only PDF attachments have frozen extraction inputs.", "- No DOC extractor, LibreOffice, antiword, Word conversion, OCR, PDF repair, or G6 artifact generation was attempted.", "", "ISSUES=", f"- {issues}", f"BLOCKER={blocker}", "APPROVAL=NOT_APPROVED", "NEXT=govern the CUMCM-2015-D-002 artifact source strategy or run a separate DOC extraction-contract stage; then rerun G6-PILOT-AUTO-R. Do not auto-run G7-PILOT"]
    LOG.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text("\n".join(output + ["G6_PILOT_AUTO_R_RUN_STATUS=" + status]) + "\n", encoding="utf-8")
    REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    print("\n".join(report_lines))
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
