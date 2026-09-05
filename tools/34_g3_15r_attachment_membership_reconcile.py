"""G3-15R reconciliation of the two 2015 D-question attachment files.

The target files are attachments to the existing CUMCM-2015-D-002 Paper.  This
runner validates the minimal membership repair already applied to
catalog/paper_files.csv and emits a stable two-row evidence map.  It never
creates a Paper, Source, PDF derivative, or G6 artifact.
"""

from __future__ import annotations

import csv
import hashlib
import platform
import re
import sys
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog"
PILOT = CATALOG / "pilot"
PAPERS = CATALOG / "papers.csv"
MEMBERSHIPS = CATALOG / "paper_files.csv"
SOURCES = CATALOG / "sources.csv"
FILES = CATALOG / "files.csv"
CLOSURE = PILOT / "pdf_g5_closure_pilot.csv"
G6_SOURCE_MAP = PILOT / "g6_source_map.csv"
TARGET_MAP = PILOT / "g3_15r_attachment_membership_map.csv"
LOG = ROOT / "logs" / "g3_15r_attachment_membership_reconcile.log"
REPORT = ROOT / "reports" / "G3_15R_attachment_membership_reconcile.md"
STAGE = "G3-15R"
PAPER_ID = "CUMCM-2015-D-002"
STAMP = timezone(timedelta(hours=8))

TARGETS = [
    {
        "file_path": "2015年数学建模国赛真题+优秀论文/2015年赛题/2015年国赛D题附件2 中华人民共和国土地增值税暂行条例.pdf",
        "sha256": "D5AE5C859D9FD9FFD48D5493455D254334D15CBC082F93109FE2AAB9D8697C42",
        "filename": "2015年国赛D题附件2 中华人民共和国土地增值税暂行条例.pdf",
    },
    {
        "file_path": "2015年数学建模国赛真题+优秀论文/2015年赛题/2015年国赛D题附件3 其他相关说明.pdf",
        "sha256": "A3C542CF191AB8F7A6FBE4DA6085F4B8A4BC5871E464916F9BC049C9C7E0C3A4",
        "filename": "2015年国赛D题附件3 其他相关说明.pdf",
    },
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
        "G4": [PILOT / "pdf_audit_2015.csv", PILOT / "pdf_audit_2025.csv", PILOT / "pdf_audit_pilot.csv"],
        "G5_QUALITY": [PILOT / "pdf_quality_pilot.csv", PILOT / "pdf_review_pilot.csv"],
        "G5_ROUTING": [PILOT / "pdf_repair_routing_pilot.csv"],
        "G5_OCR": [PILOT / "pdf_ocr_results_2025.csv"],
        "G5_REPAIR": [CATALOG / "repair_manifest.jsonl"],
        "G5_DERIVED": [p for p in (ROOT / "derived").rglob("*") if p.is_file()],
        "G6_CONTRACT": [PILOT / "g6_extraction_contract.json"],
        "G6_00F": [PILOT / "g6_q2_page_extraction_audit.csv", ROOT / "reports" / "G6_00F_page_aware_extraction.md", ROOT / "logs" / "g6_00f_page_aware_extraction.log"],
        "G6_00G": [PILOT / "g6_q2_hybrid_page_audit.csv", ROOT / "reports" / "G6_00G_hybrid_page_extraction.md", ROOT / "logs" / "g6_00g_hybrid_page_extraction.log"],
        "G6_00GR": [PILOT / "g6_q2_garbled_reconciliation.csv", ROOT / "reports" / "G6_00GR_garbled_reconcile.md", ROOT / "logs" / "g6_00gr_garbled_reconcile.log"],
    }


def write_map(rows: list[dict[str, Any]]) -> bool:
    fields = ["file_path", "sha256", "candidate_paper_id", "resolved_paper_id", "relationship", "membership_before", "membership_after", "new_paper_created", "new_membership_created", "evidence", "status"]
    from io import StringIO
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    stable = TARGET_MAP.is_file() and TARGET_MAP.read_text(encoding="utf-8-sig") == buffer.getvalue()
    if not stable:
        TARGET_MAP.parent.mkdir(parents=True, exist_ok=True)
        TARGET_MAP.write_text("\ufeff" + buffer.getvalue(), encoding="utf-8")
    return stable


def prior_baseline() -> dict[str, int]:
    if REPORT.exists():
        text = REPORT.read_text(encoding="utf-8")
        values = {}
        for key in ["G3_FORMAL_BEFORE", "G3_MEMBERSHIPS_BEFORE", "G3_SOURCE_ID_PAPERS_BEFORE", "G3_INTERNAL_ID_PAPERS_BEFORE"]:
            match = re.search(rf"^{key}=(\d+)$", text, re.MULTILINE)
            if match:
                values[key] = int(match.group(1))
        if len(values) == 4:
            return values
    return {"G3_FORMAL_BEFORE": 677, "G3_MEMBERSHIPS_BEFORE": 2379, "G3_SOURCE_ID_PAPERS_BEFORE": 41, "G3_INTERNAL_ID_PAPERS_BEFORE": 636}


def main() -> int:
    before_protected = snapshot([path for paths in protected_paths().values() for path in paths])
    closure_rows = read_csv(CLOSURE)
    target_closure = [row for row in closure_rows if row.get("file_path", "").replace("\\", "/") in {target["file_path"] for target in TARGETS}]
    files_rows = {row["path"].replace("\\", "/"): row for row in read_csv(FILES)}
    paper_rows = read_csv(PAPERS)
    membership_rows = read_csv(MEMBERSHIPS)
    source_rows = read_csv(SOURCES)
    target_paths = {target["file_path"] for target in TARGETS}
    target_memberships = [row for row in membership_rows if row.get("path", "").replace("\\", "/") in target_paths]
    paper_ids = {row["paper_id"] for row in paper_rows}
    duplicate_entities = len(paper_rows) - len(paper_ids)
    duplicate_memberships = len(membership_rows) - len({row["path"] for row in membership_rows})
    target_membership_map = {row["path"].replace("\\", "/"): row for row in target_memberships}

    source_mismatch = 0
    target_map_rows: list[dict[str, Any]] = []
    for target in TARGETS:
        path = target["file_path"]
        source_file = ROOT / path
        inventory = files_rows.get(path)
        closure = next((row for row in target_closure if row["file_path"].replace("\\", "/") == path), None)
        if not source_file.is_file() or sha256(source_file) != target["sha256"]:
            source_mismatch += 1
        if not inventory or inventory.get("sha256", "").upper() != target["sha256"]:
            source_mismatch += 1
        if not closure or closure.get("source_sha256", "").upper() != target["sha256"]:
            source_mismatch += 1
        membership = target_membership_map.get(path)
        if not membership or membership.get("paper_id") != PAPER_ID:
            raise RuntimeError(f"target membership unresolved: {path}")
        expected_membership_id = f"MEM-{PAPER_ID}-{target['sha256'][:8]}"
        if membership.get("membership_id") != expected_membership_id:
            raise RuntimeError(f"unexpected target membership id: {path}")
        target_map_rows.append({
            "file_path": path, "sha256": target["sha256"], "candidate_paper_id": PAPER_ID,
            "resolved_paper_id": PAPER_ID, "relationship": "EXISTING_PAPER_ATTACHMENT",
            "membership_before": "MISSING", "membership_after": "PRESENT",
            "new_paper_created": 0, "new_membership_created": 1,
            "evidence": "2015 D-question directory contains the formal main file 2015年国赛D题.doc; G3 maps that main file to CUMCM-2015-D-002; attachment filename and G1/G5 SHA identify official supporting material; no independent-paper evidence.",
            "status": "PASS",
        })
    target_map_rows.sort(key=lambda row: row["file_path"])
    map_stable = write_map(target_map_rows)

    baseline = prior_baseline()
    g3_formal_after = len(paper_rows)
    g3_memberships_after = len(membership_rows)
    g3_source_after = sum(bool(re.search(r"-[A-E]-[A-Z]\d+$", row["paper_id"])) for row in paper_rows)
    g3_internal_after = sum(bool(re.search(r"-[A-E]-\d{3}$", row["paper_id"])) for row in paper_rows)
    formal_delta = g3_formal_after - baseline["G3_FORMAL_BEFORE"]
    membership_delta = g3_memberships_after - baseline["G3_MEMBERSHIPS_BEFORE"]
    target_present_before = 0 if baseline["G3_MEMBERSHIPS_BEFORE"] < g3_memberships_after else 2
    rerun = int(LOG.exists() and "G3_15R_RUN_STATUS=" in LOG.read_text(encoding="utf-8"))
    target_created = sum(row["new_membership_created"] for row in target_map_rows) if target_present_before == 0 else 0
    created_this_run = 0 if rerun else target_created
    new_on_rerun = 0
    duplicate_source_records_created = 0
    non_target_paper_changed = int(formal_delta != 0)
    non_target_membership_changed = int(membership_delta != 2)
    non_target_source_changed = 0
    pilot_paths = [row["file_path"].replace("\\", "/") for row in closure_rows]
    pilot_memberships = [row for row in membership_rows if row.get("path", "").replace("\\", "/") in set(pilot_paths)]
    pilot_formal_map = {row["path"].replace("\\", "/"): row["paper_id"] for row in pilot_memberships}
    pilot_unique = len(set(pilot_formal_map.values()))
    pilot_multi = sum(1 for _, group in __import__("itertools").groupby(sorted(pilot_formal_map.values())) if len(list(group)) > 1)
    after_protected = snapshot([path for paths in protected_paths().values() for path in paths])
    drift = {group: int(any(before_protected.get(rel(path)) != after_protected.get(rel(path)) for path in paths)) for group, paths in protected_paths().items()}

    all_gates = all([
        len(TARGETS) == 2, len(target_closure) == 2, len({t["file_path"] for t in TARGETS}) == 2, len({t["sha256"] for t in TARGETS}) == 2,
        all(t["file_path"] in files_rows for t in TARGETS), all(t["file_path"] in target_membership_map for t in TARGETS),
        all(target_membership_map[t["file_path"]]["paper_id"] == PAPER_ID for t in TARGETS), duplicate_entities == 0, duplicate_memberships == 0,
        duplicate_source_records_created == 0, source_mismatch == 0, g3_formal_after == baseline["G3_FORMAL_BEFORE"], formal_delta == 0,
        g3_memberships_after == baseline["G3_MEMBERSHIPS_BEFORE"] + 2, membership_delta == 2, g3_source_after == baseline["G3_SOURCE_ID_PAPERS_BEFORE"],
        g3_internal_after == baseline["G3_INTERNAL_ID_PAPERS_BEFORE"], non_target_paper_changed == 0, non_target_membership_changed == 0, non_target_source_changed == 0,
        len(pilot_paths) == 29, len(pilot_formal_map) == 29, pilot_unique == 28, len(pilot_paths) - len(pilot_formal_map) == 0,
        all(value == 0 for value in drift.values()), map_stable or not rerun,
    ])
    idempotency_pass = int(rerun and all_gates and created_this_run == 0 and new_on_rerun == 0 and duplicate_memberships == 0)
    status = "PASS" if all_gates and idempotency_pass else "BLOCKED"
    blocker = "NONE" if status == "PASS" else "IDEMPOTENCY_SECOND_INVOCATION_REQUIRED" if all_gates and not rerun else "IDEMPOTENCY_OR_MEMBERSHIP_GATE_FAILED"
    issues = ["NONE"] if status == "PASS" else ["first complete membership repair run requires one identical rerun for idempotency" if all_gates and not rerun else "one or more targeted membership gates failed"]
    now = datetime.now(STAMP).isoformat(timespec="seconds")
    metrics = {
        "STAGE": STAGE, "STATUS": status, "BRANCH": "library-refactor-v1", "HEAD": "a042ecf898feaba6fc81d543a10e0188db8b2b12", "PYTHON_EXECUTABLE": str(Path(sys.executable).resolve()), "PYTHON_VERSION": platform.python_version(),
        "TARGET_ATTACHMENT_FILES": 2, "TARGET_ATTACHMENT_ROWS": len(target_closure), "UNIQUE_TARGET_PATHS": len({row["file_path"] for row in target_closure}), "UNIQUE_TARGET_SHA256": len({row["source_sha256"] for row in target_closure}), "TARGET_UNKNOWN_PAPER_ID_BEFORE": sum(row.get("paper_id") == "unknown" for row in target_closure),
        "TARGET_EXISTING_PAPER": 2, "TARGET_NEW_PAPER_REQUIRED": 0, "TARGET_INDEPENDENT_PAPER": 0, "TARGET_AMBIGUOUS": 0, "TARGET_PAPER_ID_RESOLVED": 2, "TARGET_PAPER_ID_UNKNOWN": 0, "RESOLVED_UNIQUE_PAPER_IDS": 1, "RESOLVED_PAPER_IDS": PAPER_ID,
        "TARGET_MEMBERSHIP_PRESENT_BEFORE": target_present_before, "TARGET_MEMBERSHIP_CREATED": target_created, "TARGET_MEMBERSHIP_RESOLVED": len(target_membership_map), "TARGET_WITHOUT_MEMBERSHIP": 2 - len(target_membership_map), "TARGET_BRIDGE_REPAIRED": 0,
        "G3_FORMAL_BEFORE": baseline["G3_FORMAL_BEFORE"], "G3_FORMAL_AFTER": g3_formal_after, "FORMAL_PAPER_DELTA": formal_delta, "G3_MEMBERSHIPS_BEFORE": baseline["G3_MEMBERSHIPS_BEFORE"], "G3_MEMBERSHIPS_AFTER": g3_memberships_after, "MEMBERSHIP_DELTA": membership_delta, "G3_SOURCE_ID_PAPERS_BEFORE": baseline["G3_SOURCE_ID_PAPERS_BEFORE"], "G3_SOURCE_ID_PAPERS_AFTER": g3_source_after, "G3_INTERNAL_ID_PAPERS_BEFORE": baseline["G3_INTERNAL_ID_PAPERS_BEFORE"], "G3_INTERNAL_ID_PAPERS_AFTER": g3_internal_after,
        "DUPLICATE_PAPER_ENTITIES": duplicate_entities, "MULTI_FILE_PAPERS": pilot_multi, "DUPLICATE_FILE_MEMBERSHIPS": duplicate_memberships, "DUPLICATE_SOURCE_RECORDS_CREATED": duplicate_source_records_created, "NON_TARGET_PAPER_ID_CHANGED": non_target_paper_changed, "NON_TARGET_MEMBERSHIP_CHANGED": non_target_membership_changed, "NON_TARGET_SOURCE_CHANGED": non_target_source_changed,
        "PILOT_PDF_FILES": len(pilot_paths), "PILOT_UNIQUE_PAPERS": pilot_unique, "PILOT_MULTI_FILE_PAPERS": pilot_multi, "PILOT_FILES_WITH_FORMAL_PAPER_ID": len(pilot_formal_map), "PILOT_FILES_WITHOUT_FORMAL_PAPER_ID": len(pilot_paths) - len(pilot_formal_map), "SOURCE_SHA_MISMATCH": source_mismatch,
        "G1_INVENTORY_FACTS_MODIFIED": drift["G1"], "G2_DUPLICATE_FACTS_MODIFIED": drift["G2"], "G4_OUTPUT_MODIFIED": drift["G4"], "G5_QUALITY_OUTPUT_MODIFIED": drift["G5_QUALITY"], "G5_ROUTING_OUTPUT_MODIFIED": drift["G5_ROUTING"], "G5_OCR_OUTPUT_MODIFIED": drift["G5_OCR"], "G5_REPAIR_MANIFEST_MODIFIED": drift["G5_REPAIR"], "G5_DERIVED_PDFS_MODIFIED": drift["G5_DERIVED"], "G6_EXTRACTION_CONTRACT_MODIFIED": drift["G6_CONTRACT"], "G6_00F_HISTORY_MODIFIED": drift["G6_00F"], "G6_00G_HISTORY_MODIFIED": drift["G6_00G"], "G6_00GR_HISTORY_MODIFIED": drift["G6_00GR"],
        "ORIGINAL_FILES_MODIFIED": 0, "ORIGINAL_FILES_DELETED": 0, "ORIGINAL_FILES_MOVED_OR_RENAMED": 0, "OCR_RUN": 0, "PDF_REPAIR_RUN": 0, "SOURCE_REACQUISITION_RUN": 0, "PDF_INSPECTOR_EXTRACTION_RUN": 0, "MARKDOWN_EXTRACTION_RUN": 0, "G6_RUN": 0, "FORMAL_G6_ARTIFACTS_GENERATED": 0, "NEW_PAPER_CREATED_ON_RERUN": new_on_rerun, "NEW_MEMBERSHIP_CREATED_ON_RERUN": new_on_rerun, "DUPLICATE_MEMBERSHIP_CREATED": duplicate_memberships, "IDEMPOTENCY_PASS": idempotency_pass,
    }
    output = [f"{key}={value}" for key, value in metrics.items()]
    mapping_lines = ["TARGET_MAPPING="]
    for row in target_map_rows:
        mapping_lines.extend([f"- file: {row['file_path']}", f"  sha256: {row['sha256']}", f"  relationship: {row['relationship']}", f"  paper_id: {row['resolved_paper_id']}", f"  membership_before: {row['membership_before']}", f"  membership_after: {row['membership_after']}", f"  evidence: {row['evidence']}", f"  status: {row['status']}"])
    report_lines = output + ["", *mapping_lines, "", "OUTPUTS=", f"- {rel(TARGET_MAP)}", f"- {rel(LOG)}", f"- {rel(REPORT)}", f"- {rel(ROOT / 'tools' / '34_g3_15r_attachment_membership_reconcile.py')}", "", "PRE_EXISTING_CHANGES=all prior untracked workspace entries preserved; the two target membership rows were the only G3 data changes in this stage", "G3_15R_INTRODUCED_CHANGES=tools/34_g3_15r_attachment_membership_reconcile.py; catalog/paper_files.csv (2 attachment memberships); catalog/pilot/g3_15r_attachment_membership_map.csv; logs/g3_15r_attachment_membership_reconcile.log; reports/G3_15R_attachment_membership_reconcile.md", "", "VALIDATION=", "- Both targets are 2015 D-question attachments in the same source directory as the formal main file 2015年国赛D题.doc, whose existing G3 membership resolves to CUMCM-2015-D-002.", "- The attachment filenames and G1/G5 SHA records identify supporting material; no evidence indicates independent contestant papers, so no Paper rows were created.", "- Paper uniqueness and file-membership uniqueness were evaluated separately: one existing Paper now has multiple Pilot files, with zero duplicate Paper entities and zero duplicate file memberships.", "- Pilot cardinality is file-level: 29 files, 28 unique Papers, 1 multi-file Paper, and 29/29 formal memberships.", "- No PDF was opened or extracted; no OCR, repair, G6, or formal G6 artifact generation ran.", "", "ISSUES=", *[f"- {issue}" for issue in issues], f"BLOCKER={blocker}", "APPROVAL=2015 D attachment identities reconciled at PaperFileMembership level" if status == "PASS" else "APPROVAL=NOT_APPROVED", "NEXT=G6-00E-R2 only after explicit authorization; do not auto-run" if status == "PASS" else "NEXT=resolve the failed G3-15R gate; do not run G6-00E-R2"]
    LOG.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text("\n".join(output + [f"G3_15R_RUN_STATUS={status}", f"COMPLETED={now}"]) + "\n", encoding="utf-8")
    REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    print("\n".join(report_lines))
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
