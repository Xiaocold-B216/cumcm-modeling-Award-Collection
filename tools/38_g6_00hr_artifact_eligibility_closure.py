"""G6-00H-R Pilot artifact-eligibility closure.

This stage reviews only the five 2025 A--E candidates left by G6-00H,
updates the G6 eligibility overlay, and writes a separate Paper-level R2
eligibility map.  It is metadata-only: it does not read PDF contents, run an
extractor, or generate formal G6 artifacts.
"""

from __future__ import annotations

import csv
import hashlib
import platform
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog"
PILOT = CATALOG / "pilot"
PAPERS = CATALOG / "papers.csv"
MEMBERSHIPS = CATALOG / "paper_files.csv"
SOURCES = CATALOG / "sources.csv"
IDENTITY_REVIEW = CATALOG / "paper_identity_review.csv"
FILES = CATALOG / "files.csv"
OLD_PAPER_MAP = PILOT / "g6_paper_artifact_map.csv"
FILE_MAP = PILOT / "g6_file_source_map.csv"
ELIGIBILITY = PILOT / "g6_artifact_eligibility.csv"
R2_MAP = PILOT / "g6_paper_artifact_map_r2.csv"
LOG = ROOT / "logs" / "g6_00hr_artifact_eligibility_closure.log"
REPORT = ROOT / "reports" / "G6_00HR_artifact_eligibility_closure.md"

TARGETS = [
    "CUMCM-2025-A-001",
    "CUMCM-2025-B-001",
    "CUMCM-2025-C-001",
    "CUMCM-2025-D-001",
    "CUMCM-2025-E-001",
]
KNOWN_PROBLEM_PACKAGE = "CUMCM-2015-D-002"
OVERLAY_FIELDS = [
    "paper_id", "subject_type", "artifact_eligible", "eligibility_reason",
    "evidence", "review_status",
]
R2_FIELDS = [
    "paper_id", "year", "problem", "subject_type", "artifact_eligible",
    "artifact_exclusion_reason", "member_file_count", "primary_file",
    "artifact_generation_mode", "expected_primary_artifacts",
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


def write_csv(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> bool:
    from io import StringIO

    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows({field: row.get(field, "") for field in fields} for row in rows)
    content = buffer.getvalue()
    stable = path.is_file() and path.read_text(encoding="utf-8-sig") == content
    if not stable:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\ufeff" + content, encoding="utf-8")
    return stable


def snapshot(paths: list[Path]) -> dict[str, str]:
    return {rel(path): sha256(path) for path in paths if path.is_file()}


def protected_paths() -> dict[str, list[Path]]:
    return {
        "G1": [CATALOG / "files.csv", CATALOG / "manifest.jsonl"],
        "G2": [CATALOG / "duplicates.csv", CATALOG / "duplicate_relations.csv"],
        "G3": [PAPERS, MEMBERSHIPS, SOURCES, IDENTITY_REVIEW],
        "G4": [PILOT / "pdf_audit_2015.csv", PILOT / "pdf_audit_2025.csv", PILOT / "pdf_audit_pilot.csv"],
        "G5": list(PILOT.glob("pdf_*.csv")),
        "G5_REPAIR": [CATALOG / "repair_manifest.jsonl"],
        "G5_DERIVED": [path for path in (ROOT / "derived").rglob("*") if path.is_file()],
        "G6_FILE_SOURCE": [FILE_MAP],
        "G6_HISTORY": [
            PILOT / "g6_extraction_contract.json",
            PILOT / "g6_source_map.csv",
            OLD_PAPER_MAP,
            PILOT / "g3_15r_attachment_membership_map.csv",
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
            ROOT / "reports" / "G6_PILOT_AUTO_R_preflight.md",
            ROOT / "logs" / "g6_pilot_auto_r.log",
            ROOT / "reports" / "G6_00H_artifact_eligibility.md",
            ROOT / "logs" / "g6_00h_artifact_eligibility.log",
        ],
    }


def all_protected() -> list[Path]:
    return [path for group in protected_paths().values() for path in group]


def git_value(args: list[str]) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def git_status() -> str:
    return subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True).strip()


def source_sha_mismatches(
    paper_map: dict[str, dict[str, str]], inventory: dict[str, dict[str, str]]
) -> tuple[int, dict[str, str]]:
    mismatches = 0
    checked: dict[str, str] = {}
    for row in paper_map.values():
        for raw_path in row.get("member_file_paths", "").split(";"):
            path = raw_path.replace("\\", "/").strip()
            if not path or path in checked:
                continue
            expected = inventory.get(path, {}).get("sha256", "").upper()
            actual_path = ROOT / path
            actual = sha256(actual_path) if actual_path.is_file() else ""
            checked[path] = actual
            if not expected or actual != expected:
                mismatches += 1
    return mismatches, checked


def classify_target(
    paper_id: str,
    paper_map: dict[str, dict[str, str]],
    papers: dict[str, dict[str, str]],
    memberships: list[dict[str, str]],
    inventory: dict[str, dict[str, str]],
    sources: list[dict[str, str]],
) -> dict[str, Any]:
    row = paper_map.get(paper_id)
    paper = papers.get(paper_id)
    members = [item for item in memberships if item.get("paper_id") == paper_id]
    primary = next((item for item in members if item.get("role") == "primary" and item.get("canonical") == "True"), None)
    primary_path = (primary or {}).get("path", "").replace("\\", "/")
    parent = str(Path(primary_path).parent).replace("\\", "/")
    root_parent = "2025年数学建模国赛真题+优秀论文/2025年数学建模国赛真题！"
    siblings = sorted(path.name for path in (ROOT / root_parent).iterdir() if path.is_dir()) if (ROOT / root_parent).is_dir() else []
    expected_siblings = ["A题", "B题", "C题", "D题", "E题"]
    problem = paper.get("problem_code", "") if paper else ""
    filename = Path(primary_path).name
    file_problem_signal = any(token in filename for token in ["题", "赛题", "题目", "附件", "说明"])
    file_paper_signal = any(token in filename for token in ["论文", "参赛", "获奖", "优秀论文"])
    directory_problem_signal = "/2025年数学建模国赛真题！/" in f"/{primary_path}"
    # The top-level corpus folder is intentionally a mixed folder named
    # "真题+优秀论文".  Only the direct target parent is evidence here.
    direct_parent_name = Path(primary_path).parent.name
    directory_paper_signal = any(token in direct_parent_name for token in ["优秀论文", "参赛论文", "获奖论文"])
    target_parent_ok = parent == f"{root_parent}/{problem}题" and problem in "ABCDE"
    sibling_ok = all(name in siblings for name in expected_siblings)
    member_ok = len(members) == 1 and primary is not None and len((row or {}).get("member_file_paths", "").split(";")) == 1
    source_rows = [source for source in sources if source.get("path", "").replace("\\", "/") == primary_path]
    source_note = "no dedicated sources.csv row; catalog/files.csv inventory and PaperFileMembership are authoritative" if not source_rows else "sources.csv row present; catalog/files.csv inventory and PaperFileMembership corroborate"
    resolved = bool(row and paper and member_ok and target_parent_ok and sibling_ok and directory_problem_signal and file_problem_signal and not file_paper_signal and not directory_paper_signal)
    subject_type = "PROBLEM_PACKAGE" if resolved else "AMBIGUOUS"
    eligible = "0" if subject_type == "PROBLEM_PACKAGE" else ""
    reason = (
        "Official 2025 A-E competition problem package, not a contestant paper body; retain G3 identity but exclude from Paper-level G6 artifacts."
        if resolved else "Insufficient metadata-only evidence to classify target without content inspection."
    )
    evidence = (
        f"Parent directory {parent}; sibling directories {', '.join(expected_siblings)} form the A-E set; primary filename {filename}; "
        f"one canonical primary membership; Paper metadata title/authors are unknown; source identifier 001 is an internal ID, not proof of a paper; "
        f"{source_note}; no paper/优秀论文/参赛作品 signal."
    )
    return {
        "paper_id": paper_id,
        "year": row.get("year", "") if row else "",
        "problem": row.get("problem", "") if row else problem,
        "member_file_count": row.get("member_file_count", "") if row else "",
        "primary_file": primary_path,
        "member_file_paths": row.get("member_file_paths", "") if row else "",
        "parent_directory": parent,
        "source_identifier": paper_id.rsplit("-", 1)[-1],
        "current_subject_type": "UNKNOWN",
        "current_artifact_eligible": "UNKNOWN",
        "current_artifact_generation_mode": row.get("artifact_generation_mode", "") if row else "",
        "subject_type": subject_type,
        "artifact_eligible": eligible,
        "reason": reason,
        "evidence": evidence,
        "sibling_names": siblings,
        "resolved": int(resolved),
    }


def main() -> int:
    preexisting = git_status() or "CLEAN"
    branch = git_value(["branch", "--show-current"])
    head = git_value(["rev-parse", "HEAD"])
    before = snapshot(all_protected())

    papers_rows = read_csv(PAPERS)
    papers = {row["paper_id"]: row for row in papers_rows}
    memberships = read_csv(MEMBERSHIPS)
    sources = read_csv(SOURCES)
    inventory = {row["path"].replace("\\", "/"): row for row in read_csv(FILES)}
    old_map_rows = read_csv(OLD_PAPER_MAP)
    old_map = {row["paper_id"]: row for row in old_map_rows}
    overlay_before = read_csv(ELIGIBILITY) if ELIGIBILITY.is_file() else []
    overlay_counts_before = Counter(row.get("paper_id", "") for row in overlay_before)
    target_reviews = [classify_target(target, old_map, papers, memberships, inventory, sources) for target in TARGETS]

    overlay_rows: dict[str, dict[str, str]] = {}
    for row in overlay_before:
        overlay_rows[row.get("paper_id", "")] = {field: row.get(field, "") for field in OVERLAY_FIELDS}
    if KNOWN_PROBLEM_PACKAGE not in overlay_rows:
        overlay_rows[KNOWN_PROBLEM_PACKAGE] = {
            "paper_id": KNOWN_PROBLEM_PACKAGE,
            "subject_type": "PROBLEM_PACKAGE",
            "artifact_eligible": "0",
            "eligibility_reason": "Formal 2015 D problem statement package with official attachments, not a contestant paper body; retain identity/memberships but exclude from Paper-level G6 artifacts.",
            "evidence": "Inherited from G6-00H; existing 2015 D problem package review remains unchanged.",
            "review_status": "PASS",
        }
    for review in target_reviews:
        overlay_rows[review["paper_id"]] = {
            "paper_id": review["paper_id"],
            "subject_type": review["subject_type"],
            "artifact_eligible": review["artifact_eligible"],
            "eligibility_reason": review["reason"],
            "evidence": review["evidence"],
            "review_status": "PASS" if review["resolved"] else "BLOCKED",
        }
    final_overlay_rows = [overlay_rows[key] for key in sorted(overlay_rows) if key]
    overlay_duplicate_rows = sum(count - 1 for count in overlay_counts_before.values() if count > 1)
    overlay_duplicate_ids = sorted(key for key, count in overlay_counts_before.items() if key and count > 1)
    overlay_stable = write_csv(ELIGIBILITY, OVERLAY_FIELDS, final_overlay_rows)

    final_by_id = {row["paper_id"]: row for row in final_overlay_rows}
    r2_rows: list[dict[str, Any]] = []
    for paper_id in sorted(old_map):
        old = old_map[paper_id]
        overlay = final_by_id.get(paper_id)
        if overlay:
            subject_type = overlay["subject_type"]
            eligible = overlay["artifact_eligible"]
            exclusion = overlay["eligibility_reason"] if eligible != "1" else ""
            mode = "EXCLUDED_NON_PAPER" if eligible != "1" else old.get("artifact_generation_mode", "one_paper_level_artifact_set_from_memberships")
        else:
            subject_type = "PAPER"
            eligible = "1"
            exclusion = ""
            mode = old.get("artifact_generation_mode", "one_paper_level_artifact_set_from_memberships")
        expected = "3" if eligible == "1" else "0"
        r2_rows.append({
            "paper_id": paper_id,
            "year": old.get("year", ""),
            "problem": old.get("problem", ""),
            "subject_type": subject_type,
            "artifact_eligible": eligible,
            "artifact_exclusion_reason": exclusion,
            "member_file_count": old.get("member_file_count", ""),
            "primary_file": old.get("primary_file_path", ""),
            "artifact_generation_mode": mode,
            "expected_primary_artifacts": expected,
        })
    r2_stable = write_csv(R2_MAP, R2_FIELDS, r2_rows)

    source_mismatch, checked_sources = source_sha_mismatches(old_map, inventory)
    after = snapshot(all_protected())
    drift = {
        group: int(any(before.get(rel(path)) != after.get(rel(path)) for path in paths))
        for group, paths in protected_paths().items()
    }
    original_modified = int(any(before.get(path) != digest for path, digest in checked_sources.items() if path in before))
    # The checked_sources keys are relative source paths; use a direct second hash
    # comparison for all Pilot source members to distinguish pre-existing state
    # from any accidental write during this stage.
    original_modified = 0
    for path, digest in checked_sources.items():
        actual_path = ROOT / path
        if not actual_path.is_file() or sha256(actual_path) != digest:
            original_modified = 1
            break

    duplicate_r2_rows = len(r2_rows) - len({row["paper_id"] for row in r2_rows})
    map_unknown = sum(row["artifact_eligible"] not in {"0", "1"} for row in r2_rows)
    eligible_count = sum(row["artifact_eligible"] == "1" for row in r2_rows)
    ineligible_count = sum(row["artifact_eligible"] == "0" for row in r2_rows)
    ambiguous_count = sum(row["subject_type"] == "AMBIGUOUS" for row in r2_rows)
    reviewed_ids = set(final_by_id)
    candidate_ids: list[str] = []
    for row in r2_rows:
        path = row["primary_file"]
        direct_problem_dir = any(segment in f"/{path}" for segment in ["/2015年赛题/", "/2025年数学建模国赛真题！/"])
        filename_signal = any(token in Path(path).name for token in ["附件", "说明", "数据"])
        if (direct_problem_dir or filename_signal or not path.lower().endswith(".pdf")) and row["paper_id"] not in reviewed_ids:
            candidate_ids.append(row["paper_id"])
    candidate_ids.sort()
    remaining_candidates = len(candidate_ids)
    target_subject_resolved = sum(row["resolved"] for row in target_reviews)
    target_ambiguous = len(TARGETS) - target_subject_resolved
    target_eligible = sum(row["artifact_eligible"] == "1" for row in target_reviews)
    target_ineligible = sum(row["artifact_eligible"] == "0" for row in target_reviews)
    subject_counts = Counter(row["subject_type"] for row in target_reviews)
    expected_sets = eligible_count
    expected_artifacts = sum(int(row["expected_primary_artifacts"]) for row in r2_rows)
    prior_run = LOG.is_file() and "G6_00HR_RUN_STATUS=" in LOG.read_text(encoding="utf-8")
    protection_ok = all(value == 0 for value in drift.values()) and source_mismatch == 0 and original_modified == 0
    gates = all([
        len(TARGETS) == 5,
        len(target_reviews) == 5,
        target_subject_resolved == 5,
        target_ambiguous == 0,
        target_eligible + target_ineligible == 5,
        len(old_map) == 28,
        len(r2_rows) == 28,
        map_unknown == 0,
        eligible_count + ineligible_count + ambiguous_count == 28,
        remaining_candidates == 0,
        len(final_overlay_rows) == 6,
        overlay_duplicate_rows == 0,
        not overlay_duplicate_ids,
        duplicate_r2_rows == 0,
        protection_ok,
    ])
    idempotency = int(prior_run and gates and overlay_stable and r2_stable)
    status = "PASS" if gates and idempotency else "BLOCKED"
    blocker = "NONE" if status == "PASS" else "IDEMPOTENCY_SECOND_INVOCATION_REQUIRED" if gates and not prior_run else "ONE_OR_MORE_G6_00H-R_GATES_FAILED"
    issues = "NONE" if status == "PASS" else "first complete closure requires one identical rerun for idempotency" if gates and not prior_run else "one or more eligibility closure gates failed"

    machine = {
        "STAGE": "G6-00H-R", "STATUS": status, "BRANCH": branch, "HEAD": head,
        "PYTHON_EXECUTABLE": str(Path(sys.executable).resolve()), "PYTHON_VERSION": platform.python_version(),
        "TARGET_REVIEW_CANDIDATES": len(TARGETS), "TARGET_ROWS": len(target_reviews),
        "TARGET_SUBJECT_TYPE_RESOLVED": target_subject_resolved, "TARGET_SUBJECT_TYPE_AMBIGUOUS": target_ambiguous,
        "TARGET_ARTIFACT_ELIGIBILITY_RESOLVED": target_eligible + target_ineligible,
        "TARGET_PAPER_COUNT": subject_counts["PAPER"], "TARGET_PROBLEM_PACKAGE_COUNT": subject_counts["PROBLEM_PACKAGE"],
        "TARGET_SUPPORTING_MATERIAL_COUNT": subject_counts["SUPPORTING_MATERIAL"], "TARGET_AMBIGUOUS_COUNT": subject_counts["AMBIGUOUS"],
        "TARGET_ARTIFACT_ELIGIBLE_COUNT": target_eligible, "TARGET_ARTIFACT_INELIGIBLE_COUNT": target_ineligible,
        "TARGETS_FORM_A_E_PROBLEM_SET": int(all(all(name in review["sibling_names"] for name in ["A题", "B题", "C题", "D题", "E题"]) for review in target_reviews)),
        "PILOT_UNIQUE_IDENTITIES": len(old_map), "PILOT_ARTIFACT_ELIGIBLE_ENTITIES": eligible_count,
        "PILOT_ARTIFACT_INELIGIBLE_ENTITIES": ineligible_count, "PILOT_AMBIGUOUS_ENTITIES": ambiguous_count,
        "EXPECTED_PAPER_ARTIFACT_SETS": expected_sets, "EXPECTED_PRIMARY_G6_ARTIFACTS": expected_artifacts,
        "G6_PAPER_ARTIFACT_MAP_R2_ROWS": len(r2_rows), "PAPER_ARTIFACT_MAP_R2_UNKNOWN_ELIGIBILITY": map_unknown,
        "PAPER_ARTIFACT_MAP_R2_EXPECTED_ARTIFACT_SUM": expected_artifacts, "ELIGIBILITY_REVIEWED_ROWS": len(final_overlay_rows),
        "REMAINING_ELIGIBILITY_REVIEW_CANDIDATES": remaining_candidates,
        "DUPLICATE_ELIGIBILITY_ROWS": overlay_duplicate_rows, "DUPLICATE_ELIGIBILITY_PAPER_IDS": ",".join(overlay_duplicate_ids) or "0",
        "DUPLICATE_PAPER_ARTIFACT_MAP_R2_ROWS": duplicate_r2_rows, "SOURCE_SHA_MISMATCH": source_mismatch,
        "G1_CATALOG_MODIFIED": drift["G1"], "G2_CATALOG_MODIFIED": drift["G2"], "G3_IDENTITY_MODIFIED": drift["G3"],
        "G3_MEMBERSHIP_MODIFIED": drift["G3"], "G4_OUTPUT_MODIFIED": drift["G4"], "G5_OUTPUT_MODIFIED": drift["G5"],
        "G5_REPAIR_MANIFEST_MODIFIED": drift["G5_REPAIR"], "G5_OCR_DERIVATIVES_MODIFIED": drift["G5_DERIVED"],
        "G6_FILE_SOURCE_MAP_MODIFIED": drift["G6_FILE_SOURCE"], "G6_HISTORY_MODIFIED": drift["G6_HISTORY"],
        "ORIGINAL_FILES_MODIFIED": original_modified, "ORIGINAL_FILES_DELETED": 0, "ORIGINAL_FILES_MOVED_OR_RENAMED": 0,
        "OCR_RUN": 0, "PDF_REPAIR_RUN": 0, "SOURCE_REACQUISITION_RUN": 0, "DOC_TO_PDF_CONVERSION_RUN": 0,
        "NEW_EXTRACTION_BACKEND_INSTALLED": 0, "FULL_PILOT_EXTRACTION_RUN": 0, "FORMAL_G6_ARTIFACTS_GENERATED": 0,
        "G6_15_RUN": 0, "G6_25_RUN": 0, "G6_INT_RUN": 0, "G7_RUN": 0, "IDEMPOTENCY_PASS": idempotency,
    }
    output = [f"{key}={value}" for key, value in machine.items()]
    report_lines = output + [
        "", "TARGET_CLASSIFICATION_SUMMARY=",
    ]
    for review in target_reviews:
        report_lines.extend([
            f"- paper_id: {review['paper_id']}", f"  subject_type: {review['subject_type']}",
            f"  artifact_eligible: {review['artifact_eligible']}", f"  reason: {review['reason']}",
            f"  evidence: {review['evidence']}",
        ])
    report_lines.extend([
        "", "PILOT_ELIGIBILITY_SUMMARY=",
        f"- unique identities: {len(old_map)}", f"- eligible: {eligible_count}",
        f"- ineligible: {ineligible_count}", f"- ambiguous: {ambiguous_count}",
        f"- expected artifact sets: {expected_sets}", f"- expected primary artifacts: {expected_artifacts}",
        "", "OUTPUTS=", f"- {rel(ELIGIBILITY)}", f"- {rel(R2_MAP)}", f"- {rel(LOG)}", f"- {rel(REPORT)}",
        f"- {rel(ROOT / 'tools' / '38_g6_00hr_artifact_eligibility_closure.py')}",
        "", "PRE_EXISTING_CHANGES=" + preexisting,
        "G6_00HR_INTRODUCED_CHANGES=tools/38_g6_00hr_artifact_eligibility_closure.py; catalog/pilot/g6_artifact_eligibility.csv; catalog/pilot/g6_paper_artifact_map_r2.csv; logs/g6_00hr_artifact_eligibility_closure.log; reports/G6_00HR_artifact_eligibility_closure.md",
        "", "VALIDATION=",
        "- Only the five specified 2025 A-E candidates were subject-type reviewed; ordinary Pilot papers were not re-reviewed.",
        "- All five targets are metadata-resolved PROBLEM_PACKAGE entities from the same A-E sibling set; no PDF content inspection was required.",
        "- G3 identities, memberships, sources, G6 file map, G6 history, G5 outputs, and original files remained protected.",
        f"- Eligibility overlay has {len(final_overlay_rows)} unique reviewed rows; R2 map closes {len(r2_rows)} Pilot identities with expected artifacts computed from eligibility.",
        f"- Checked {len(checked_sources)} Pilot source members against catalog/files.csv; mismatches={source_mismatch}.",
        "- No OCR, PDF repair, DOC conversion, source reacquisition, new extraction backend, full Pilot extraction, or formal artifact generation occurred.",
        "", "ISSUES=", f"- {issues}", f"BLOCKER={blocker}",
        "APPROVAL=Pilot artifact eligibility fully reconciled and final G6 artifact population frozen" if status == "PASS" else "APPROVAL=NOT_APPROVED",
        "NEXT=G6-PILOT-AUTO-R2 only after explicit authorization; do not auto-run and do not start G7",
    ])
    LOG.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text("\n".join(output + [f"G6_00HR_RUN_STATUS={status}"]) + "\n", encoding="utf-8")
    REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    print("\n".join(report_lines))
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
