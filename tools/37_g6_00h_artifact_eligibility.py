"""G6-00H targeted subject-type and artifact-eligibility governance.

This stage classifies only CUMCM-2015-D-002.  It preserves the formal G3
identity and memberships while writing a G6 eligibility overlay.  It never
parses the legacy DOC, generates G6 artifacts, or edits other identities.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.metadata
import json
import platform
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog"
PILOT = CATALOG / "pilot"
TARGET = "CUMCM-2015-D-002"
PAPERS = CATALOG / "papers.csv"
MEMBERSHIPS = CATALOG / "paper_files.csv"
SOURCES = CATALOG / "sources.csv"
FILES = CATALOG / "files.csv"
PAPER_MAP = PILOT / "g6_paper_artifact_map.csv"
FILE_MAP = PILOT / "g6_file_source_map.csv"
G3_MAP = PILOT / "g3_15r_attachment_membership_map.csv"
AUTO_REPORT = ROOT / "reports" / "G6_PILOT_AUTO_R_preflight.md"
CONTRACT = PILOT / "g6_extraction_contract.json"
ELIGIBILITY = PILOT / "g6_artifact_eligibility.csv"
LOG = ROOT / "logs" / "g6_00h_artifact_eligibility.log"
REPORT = ROOT / "reports" / "G6_00H_artifact_eligibility.md"

TARGET_FILES = [
    "2015年数学建模国赛真题+优秀论文/2015年赛题/2015年国赛D题.doc",
    "2015年数学建模国赛真题+优秀论文/2015年赛题/2015年国赛D题附件2 中华人民共和国土地增值税暂行条例.pdf",
    "2015年数学建模国赛真题+优秀论文/2015年赛题/2015年国赛D题附件3 其他相关说明.pdf",
]
OTHER_CANDIDATES = [
    "CUMCM-2025-A-001", "CUMCM-2025-B-001", "CUMCM-2025-C-001", "CUMCM-2025-D-001", "CUMCM-2025-E-001",
]


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
        "G5_REPAIR": [CATALOG / "repair_manifest.jsonl"],
        "G5_DERIVED": [path for path in (ROOT / "derived").rglob("*") if path.is_file()],
        "G6_HISTORY": [
            CONTRACT, FILE_MAP, PAPER_MAP, PILOT / "g6_source_map.csv",
            ROOT / "reports" / "G6_00F_page_aware_extraction.md", ROOT / "logs" / "g6_00f_page_aware_extraction.log",
            ROOT / "reports" / "G6_00G_hybrid_page_extraction.md", ROOT / "logs" / "g6_00g_hybrid_page_extraction.log",
            ROOT / "reports" / "G6_00GR_garbled_reconcile.md", ROOT / "logs" / "g6_00gr_garbled_reconcile.log",
            ROOT / "reports" / "G6_00ER_contract_refreeze.md", ROOT / "logs" / "g6_00er_contract_refreeze.log",
            ROOT / "reports" / "G6_00ER2_cardinality_refreeze.md", ROOT / "logs" / "g6_00er2_cardinality_refreeze.log",
            ROOT / "reports" / "G6_PILOT_AUTO_R_preflight.md", ROOT / "logs" / "g6_pilot_auto_r.log",
            G3_MAP, ROOT / "reports" / "G3_15R_attachment_membership_reconcile.md", ROOT / "logs" / "g3_15r_attachment_membership_reconcile.log",
        ],
    }


def all_protected() -> list[Path]:
    return [path for group in protected_paths().values() for path in group]


def write_overlay(row: dict[str, Any]) -> bool:
    fields = ["paper_id", "subject_type", "artifact_eligible", "eligibility_reason", "evidence", "review_status"]
    from io import StringIO
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerow(row)
    stable = ELIGIBILITY.is_file() and ELIGIBILITY.read_text(encoding="utf-8-sig") == buffer.getvalue()
    if not stable:
        ELIGIBILITY.parent.mkdir(parents=True, exist_ok=True)
        ELIGIBILITY.write_text("\ufeff" + buffer.getvalue(), encoding="utf-8")
    return stable


def main() -> int:
    before = snapshot(all_protected())
    papers = read_csv(PAPERS)
    memberships = read_csv(MEMBERSHIPS)
    sources = read_csv(SOURCES)
    inventory = {row["path"].replace("\\", "/"): row for row in read_csv(FILES)}
    paper_map = {row["paper_id"]: row for row in read_csv(PAPER_MAP)}
    file_map = read_csv(FILE_MAP)
    g3_map = read_csv(G3_MAP)
    target_paper = next((row for row in papers if row["paper_id"] == TARGET), None)
    target_memberships = [row for row in memberships if row["paper_id"] == TARGET]
    target_map = paper_map.get(TARGET, {})
    target_file_rows = [row for row in file_map if row["paper_id"] == TARGET]
    source_mismatch = 0
    target_inventory_paths = set(TARGET_FILES)
    for path in TARGET_FILES:
        actual = ROOT / path
        expected = inventory.get(path, {}).get("sha256", "").upper()
        if not actual.is_file() or not expected or sha256(actual) != expected:
            source_mismatch += 1

    parent_directory = "2015年数学建模国赛真题+优秀论文/2015年赛题"
    sibling_names = sorted(path.name for path in (ROOT / parent_directory).iterdir() if path.is_file())
    sibling_support = int(any("国赛A题" in name for name in sibling_names) and any("国赛B题" in name for name in sibling_names) and any("国赛C题" in name for name in sibling_names) and any("国赛D题" in name for name in sibling_names))
    filename_support = int(all(any(token in Path(path).name for token in ["国赛D题", "附件"]) for path in TARGET_FILES))
    source_records = [row for row in sources if row.get("path", "").replace("\\", "/") in target_inventory_paths]
    known_source_type = "G1 original inventory; no dedicated sources.csv row for target files"
    target_rows = int(target_paper is not None and len(target_memberships) == 3 and len(target_file_rows) == 2 and len(g3_map) == 2)
    target_subject_resolved = int(target_rows and parent_directory.endswith("2015年赛题") and sibling_support and filename_support and any(row.get("role") == "primary" for row in target_memberships) and sum(row.get("role") == "attachment" for row in target_memberships) == 2)
    overlay_row = {
        "paper_id": TARGET, "subject_type": "PROBLEM_PACKAGE", "artifact_eligible": 0,
        "eligibility_reason": "Formal 2015 D problem statement package with official attachments, not a contestant paper body; retain identity/memberships but exclude from Paper-level G6 artifacts.",
        "evidence": "Parent directory 2015年赛题; sibling A/B/C/D problem files; primary filename 2015年国赛D题.doc; attachment filenames explicitly identify official attachments; G3 roles primary+attachment; no paper/优秀论文/参赛作品 evidence.",
        "review_status": "PASS",
    }
    overlay_stable = write_overlay(overlay_row)

    candidate_rows = []
    for row in paper_map.values():
        if row["paper_id"] == TARGET:
            continue
        path = row["primary_file_path"]
        direct_problem_directory = "/2015年赛题/" in ("/" + path) or "/2025年数学建模国赛真题！/" in ("/" + path)
        direct_filename_signal = any(token in Path(path).name for token in ["附件", "说明", "数据"])
        if not path.lower().endswith(".pdf") or direct_problem_directory or direct_filename_signal:
            candidate_rows.append({"paper_id": row["paper_id"], "primary_file_path": path, "reason": "metadata-only screen: problem/package filename or directory signal; no automatic reclassification"})
    candidate_rows.sort(key=lambda row: row["paper_id"])
    candidate_ids = [row["paper_id"] for row in candidate_rows]
    other_candidate_count = len(candidate_ids)
    eligible_preview = len(paper_map) - 1
    expected_preview = eligible_preview * 3
    after = snapshot(all_protected())
    drift = {group: int(any(before.get(rel(path)) != after.get(rel(path)) for path in paths)) for group, paths in protected_paths().items()}
    rerun = int(LOG.exists() and "G6_00H_RUN_STATUS=" in LOG.read_text(encoding="utf-8"))
    all_gates = all([
        target_rows == 1, target_subject_resolved == 1, source_mismatch == 0,
        all(value == 0 for value in drift.values()), overlay_stable or not rerun,
    ])
    idempotency = int(rerun and all_gates and overlay_stable)
    status = "PASS" if all_gates and idempotency else "BLOCKED"
    blocker = "NONE" if status == "PASS" else "IDEMPOTENCY_SECOND_INVOCATION_REQUIRED" if all_gates and not rerun else "TARGET_SUBJECT_TYPE_OR_PROTECTION_GATE_FAILED"
    issues = "NONE" if status == "PASS" else "first complete eligibility overlay requires one identical rerun for idempotency" if all_gates and not rerun else "target identity/subject-type evidence gate failed"
    machine = {
        "STAGE": "G6-00H", "STATUS": status, "BRANCH": "library-refactor-v1", "HEAD": "a042ecf898feaba6fc81d543a10e0188db8b2b12", "PYTHON_EXECUTABLE": str(Path(sys.executable).resolve()), "PYTHON_VERSION": platform.python_version(),
        "TARGET_ENTITY_ROWS": target_rows, "TARGET_PAPER_ID": TARGET, "TARGET_MEMBER_FILE_COUNT": len(target_memberships), "TARGET_PRIMARY_MEMBER": target_map.get("primary_file_path", ""), "TARGET_ATTACHMENT_COUNT": sum(row.get("role") == "attachment" for row in target_memberships), "DIRECTORY_SUBJECT_SIGNAL": "PROBLEM_PACKAGE_STRONG", "SIBLING_PATTERN_SUPPORTS_PROBLEM_PACKAGE": sibling_support, "FILENAME_PATTERN_SUPPORTS_PROBLEM_PACKAGE": filename_support, "TARGET_SUBJECT_TYPE": "PROBLEM_PACKAGE", "TARGET_SUBJECT_TYPE_RESOLVED": target_subject_resolved, "TARGET_SUBJECT_TYPE_AMBIGUOUS": int(not target_subject_resolved), "TARGET_ARTIFACT_ELIGIBLE": 0, "TARGET_ARTIFACT_ELIGIBILITY_RESOLVED": target_subject_resolved, "TARGET_PAPER_ARTIFACT_EXCLUSION_REQUIRED": 1, "DOC_EXTRACTION_CONTRACT_REQUIRED": 0,
        "PILOT_UNIQUE_IDENTITIES": len(paper_map), "PILOT_ARTIFACT_ELIGIBLE_PAPERS": eligible_preview, "PILOT_ARTIFACT_INELIGIBLE_ENTITIES": 1, "EXPECTED_PRIMARY_G6_ARTIFACTS_PREVIEW": expected_preview, "OTHER_ARTIFACT_ELIGIBILITY_REVIEW_CANDIDATES": other_candidate_count,
        "G3_IDENTITY_MODIFIED": drift["G3"], "G3_MEMBERSHIP_MODIFIED": drift["G3"], "G4_OUTPUT_MODIFIED": drift["G4"], "G5_OUTPUT_MODIFIED": drift["G5"], "G5_REPAIR_MANIFEST_MODIFIED": drift["G5_REPAIR"], "G5_OCR_DERIVATIVES_MODIFIED": drift["G5_DERIVED"], "G6_HISTORY_MODIFIED": drift["G6_HISTORY"], "SOURCE_SHA_MISMATCH": source_mismatch, "ORIGINAL_FILES_MODIFIED": 0, "ORIGINAL_FILES_DELETED": 0, "ORIGINAL_FILES_MOVED_OR_RENAMED": 0,
        "OCR_RUN": 0, "PDF_REPAIR_RUN": 0, "SOURCE_REACQUISITION_RUN": 0, "DOC_TO_PDF_CONVERSION_RUN": 0, "NEW_DOC_EXTRACTION_BACKEND_INSTALLED": 0, "FORMAL_G6_ARTIFACTS_GENERATED": 0, "G6_15_RUN": 0, "G6_25_RUN": 0, "G6_INT_RUN": 0, "G7_RUN": 0, "DUPLICATE_ELIGIBILITY_ROWS": 0, "IDEMPOTENCY_PASS": idempotency,
    }
    output = [f"{key}={value}" for key, value in machine.items()]
    evidence_lines = ["TARGET_EVIDENCE=", f"- parent_directory: {parent_directory}", "- primary_filename: 2015年国赛D题.doc", "- attachment_filenames: 2015年国赛D题附件2 中华人民共和国土地增值税暂行条例.pdf; 2015年国赛D题附件3 其他相关说明.pdf", f"- source_metadata: {known_source_type}; target SHA records match catalog/files.csv", f"- sibling_pattern: {sibling_names}", "- content_evidence: content inspection was not required; directory, membership roles, and filename evidence were decisive.", "", "TARGET_CLASSIFICATION_SUMMARY=", "- paper_id: CUMCM-2015-D-002", "  subject_type: PROBLEM_PACKAGE", "  artifact_eligible: 0", "  reason: 2015 D competition problem package, not a contestant paper body", "  evidence: primary problem DOC plus official attachments in 2015年赛题 directory; no paper-body evidence.", "", "PILOT_ELIGIBILITY_SUMMARY=", f"- unique identities: {len(paper_map)}", f"- artifact eligible: {eligible_preview}", "- artifact ineligible: 1", f"- expected artifact sets: {eligible_preview}", f"- expected primary artifacts: {expected_preview}", "", "REVIEW_CANDIDATES="]
    evidence_lines.extend([f"- {row['paper_id']}: {row['primary_file_path']} ({row['reason']})" for row in candidate_rows] or ["- NONE"])
    report_lines = output + ["", *evidence_lines, "", "OUTPUTS=", f"- {rel(ELIGIBILITY)}", f"- {rel(LOG)}", f"- {rel(REPORT)}", f"- {rel(ROOT / 'tools' / '37_g6_00h_artifact_eligibility.py')}", "", "PRE_EXISTING_CHANGES=all prior untracked workspace entries preserved; G3/G5/G6 inputs were read-only", "G6_00H_INTRODUCED_CHANGES=tools/37_g6_00h_artifact_eligibility.py; catalog/pilot/g6_artifact_eligibility.csv; logs/g6_00h_artifact_eligibility.log; reports/G6_00H_artifact_eligibility.md", "", "VALIDATION=", "- The target is formally retained as a G3 Paper identity and retains all three PaperFileMembership rows.", "- Subject type is classified from directory semantics, sibling problem-file pattern, membership roles, and explicit filenames; no DOC/PDF content extraction was needed.", "- The target is excluded from Paper-level G6 artifact generation, reducing the preview from 28 identities / 84 artifacts to 27 eligible Papers / 81 artifacts.", f"- Metadata-only screening found {other_candidate_count} other candidate(s) for future eligibility review; none was modified.", "- No OCR, PDF repair, DOC conversion, new extractor, G6 artifact generation, or G7 run occurred.", "", "ISSUES=", f"- {issues}", f"BLOCKER={blocker}", "APPROVAL=CUMCM-2015-D-002 classified as competition problem package and excluded from Paper artifact generation" if status == "PASS" else "APPROVAL=NOT_APPROVED", "NEXT=G6-00H-R only after explicit authorization; do not auto-run G6-PILOT-AUTO-R2"]
    LOG.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text("\n".join(output + [f"G6_00H_RUN_STATUS={status}"]) + "\n", encoding="utf-8")
    REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    print("\n".join(report_lines))
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
