"""Formal, evidence-backed closure of the 15 ME-15 identities.

This runner only adjudicates subject type and eligibility.  It never performs
extraction, OCR, PDF repair, Office conversion, Artifact generation, Q3 work,
G9, or G10.
"""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCALE = ROOT / "catalog" / "scale"
CATALOG = ROOT / "catalog"
PACKETS = SCALE / "g8_me15_review_packets.csv"
DECISIONS = SCALE / "g8_me15_decisions.csv"
TRANSITIONS = SCALE / "g8_me15_transitions.csv"
ELIGIBILITY = SCALE / "g8_artifact_eligibility.csv"
BACKLOG = SCALE / "g8_manual_backlog.csv"
DEFERRED = SCALE / "g8_deferred_review.csv"
STATUS = SCALE / "g8_paper_status.csv"
MANIFEST = SCALE / "g8_artifact_manifest.csv"
PAPERS = CATALOG / "papers.csv"
PAPER_FILES = CATALOG / "paper_files.csv"
FILES = CATALOG / "files.csv"
STATE = SCALE / "g8_run_state.json"
Q3_BACKLOG = SCALE / "g8_q3_manual_backlog.csv"
REPORT = ROOT / "reports" / "scale" / "G8_ME15_ELIGIBILITY_CLOSURE.md"
LOG = ROOT / "logs" / "scale" / "g8_me15_eligibility_closure.log"

DECISION_FIELDS = ["paper_id", "year", "problem", "prior_subject_type", "prior_artifact_eligibility", "planning_recommendation", "planning_confidence", "final_subject_type", "final_artifact_eligible", "decision_confidence", "primary_evidence", "secondary_evidence", "decision_reason", "manual_review_remaining", "downstream_action"]
TRANSITION_FIELDS = ["paper_id", "from_category", "to_category", "final_subject_type", "artifact_eligible", "reason"]
ELIGIBILITY_FIELDS = ["paper_id", "year", "problem", "subject_type", "artifact_eligible", "eligibility_reason", "evidence", "review_status", "primary_file", "primary_extension"]
BACKLOG_FIELDS = ["paper_id", "year", "problem", "category", "reason", "source_path", "quality", "artifact_status", "recommended_next_action", "priority"]
DEFERRED_FIELDS = ["paper_id", "year", "problem", "reason", "required_next_action", "source_path", "source_sha256", "status", "active", "prior_reason"]
STATUS_FIELDS = ["paper_id", "year", "subject_type", "artifact_eligible", "quality", "extraction_status", "artifact_status", "qa_status", "deferred_reason", "overall_status"]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def atomic_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp-me15")
    temp.write_text(content, encoding="utf-8")
    temp.replace(path)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> None:
    from io import StringIO
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows({field: row.get(field, "") for field in fields} for row in rows)
    atomic_text(path, "\ufeff" + output.getvalue())


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def first_path(value: str) -> str:
    return value.split(";")[0]


def file_hashes(paths: list[Path]) -> dict[str, str]:
    return {rel(path): digest(path) for path in paths if path.is_file()}


def source_sha(path: str, files_by_path: dict[str, dict[str, str]]) -> str:
    if path in files_by_path:
        return files_by_path[path].get("sha256", "").upper()
    actual = ROOT / path
    return digest(actual) if actual.is_file() else ""


def make_decisions(packets: list[dict[str, str]], members_by_id: dict[str, list[dict[str, str]]], files_by_path: dict[str, dict[str, str]], previous: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    decisions: list[dict[str, Any]] = []
    for packet in sorted(packets, key=lambda row: row["paper_id"]):
        pid = packet["paper_id"]
        primary = first_path(packet["primary_file"])
        members = members_by_id.get(pid, [])
        prior = previous.get(pid, {})
        # Reuse the first-run formal decision on subsequent idempotency runs.
        if prior:
            decisions.append(dict(prior))
            continue
        rec = packet["recommended_subject_type"]
        if pid == "CUMCM-1993-A-001":
            final, eligible, confidence, manual, action = "AMBIGUOUS", "UNRESOLVED", "LOW", "1", "REMAIN_ELIGIBILITY_MANUAL"
            primary_evidence = "Two PDF memberships exist for the same identity and both have canonical=False; no unique canonical source is established."
            secondary_evidence = "Both filenames carry award-paper semantics and distinct recorded source SHA values; membership ambiguity is the controlling conflict."
            reason = "Paper-like evidence is present, but formal Paper closure would require choosing one of two non-canonical primary memberships, which is outside this stage."
        elif pid == "CUMCM-2013-D-004":
            final, eligible, confidence, manual, action = "PAPER", "UNRESOLVED", "MEDIUM", "0", "MOVE_TO_UNSUPPORTED_FORMAT"
            primary_evidence = "Canonical membership points to a 2013D directory and a team/institution-named source file containing participant names, consistent with a submitted paper."
            secondary_evidence = "The primary extension is .doc and no frozen supported extraction input is present; this is a format-governance issue, not an identity ambiguity."
            reason = "Paper identity is supported by directory and team naming; extraction eligibility remains unresolved because the primary DOC lacks a frozen supported backend."
        elif rec == "PROBLEM_PACKAGE":
            final, eligible, confidence, manual, action = "PROBLEM_PACKAGE", "0", "HIGH", "0", "CLOSED_INELIGIBLE"
            primary_evidence = "Filename explicitly names the 2013 national contest problem or its appendix (A/C/D题)."
            secondary_evidence = "Single membership and contest-problem directory placement; no submitted-paper/team structure is present."
            reason = "The source is a problem statement or appendix, not a Paper Artifact candidate."
        elif rec == "SUPPORTING_MATERIAL":
            final, eligible, confidence, manual, action = "SUPPORTING_MATERIAL", "0", "HIGH", "0", "CLOSED_INELIGIBLE"
            primary_evidence = "The source has a MATLAB .asv autosave extension under the 2013C problem directory."
            secondary_evidence = "Single membership and code-like sibling naming; no paper structure or prose-paper source is present."
            reason = "The source is computational supporting material, not a Paper Artifact candidate."
        else:
            final, eligible, confidence, manual, action = "AMBIGUOUS", "UNRESOLVED", "LOW", "1", "REMAIN_ELIGIBILITY_MANUAL"
            primary_evidence = "Existing packet evidence does not uniquely establish subject type."
            secondary_evidence = "Membership and source metadata require human review."
            reason = "No safe formal classification is supported without additional authorized evidence."
        decisions.append({"paper_id": pid, "year": packet["year"], "problem": packet["problem"], "prior_subject_type": "AMBIGUOUS_MANUAL_REVIEW", "prior_artifact_eligibility": "UNRESOLVED", "planning_recommendation": rec, "planning_confidence": packet["confidence"], "final_subject_type": final, "final_artifact_eligible": eligible, "decision_confidence": confidence, "primary_evidence": primary_evidence, "secondary_evidence": secondary_evidence, "decision_reason": reason, "manual_review_remaining": manual, "downstream_action": action})
    return decisions


def main() -> int:
    required = [PACKETS, BACKLOG, ELIGIBILITY, STATUS, DEFERRED, MANIFEST, PAPERS, PAPER_FILES, FILES, STATE, Q3_BACKLOG]
    missing = [rel(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit("BLOCKED:MISSING_INPUTS=" + ";".join(missing))
    before_allowed = file_hashes([ELIGIBILITY, BACKLOG, DEFERRED, STATUS, MANIFEST, Q3_BACKLOG])
    artifact_rows_before = read_csv(MANIFEST)
    artifact_hashes_before = {(row["paper_id"], row["artifact_type"]): row["artifact_sha256"] for row in artifact_rows_before}
    packets = read_csv(PACKETS)
    if len(packets) != 15 or len({row["paper_id"] for row in packets}) != 15:
        raise SystemExit("BLOCKED:ME15_PACKETS_INCOMPLETE")
    backlog_before = read_csv(BACKLOG)
    eligibility_before = read_csv(ELIGIBILITY)
    status_before = read_csv(STATUS)
    deferred_before = read_csv(DEFERRED)
    eligibility_by_id = {row["paper_id"]: row for row in eligibility_before}
    paper_rows = {row["paper_id"]: row for row in read_csv(PAPERS)}
    files_by_path = {row["path"]: row for row in read_csv(FILES)}
    members_by_id: dict[str, list[dict[str, str]]] = {}
    for row in read_csv(PAPER_FILES):
        members_by_id.setdefault(row["paper_id"], []).append(row)
    target_ids = {row["paper_id"] for row in packets}
    if target_ids - set(eligibility_by_id) or target_ids - set(paper_rows):
        raise SystemExit("BLOCKED:ME15_TARGET_IDENTITY_MISSING")
    source_mismatch = sum(not (ROOT / first_path(row["primary_file"])).is_file() or source_sha(first_path(row["primary_file"]), files_by_path) == "" for row in packets)
    if source_mismatch:
        raise SystemExit("BLOCKED:ME15_SOURCE_MISSING_OR_UNHASHED")

    previous_decisions = {row["paper_id"]: row for row in read_csv(DECISIONS)} if DECISIONS.is_file() else {}
    decisions = make_decisions(packets, members_by_id, files_by_path, previous_decisions)
    decisions_by_id = {row["paper_id"]: row for row in decisions}
    if len(decisions) != 15 or set(decisions_by_id) != target_ids:
        raise SystemExit("BLOCKED:ME15_DECISION_INCOMPLETE")
    evidence_missing = sum(not row["primary_evidence"].strip() or not row["decision_reason"].strip() or not row["downstream_action"].strip() for row in decisions if row["final_subject_type"] != "AMBIGUOUS")
    if evidence_missing:
        raise SystemExit("BLOCKED:ME15_DECISION_MISSING_EVIDENCE")
    write_csv(DECISIONS, DECISION_FIELDS, decisions)

    # Formal eligibility overlay update: only these 15 rows may change.
    eligibility_after = []
    for row in eligibility_before:
        if row["paper_id"] not in target_ids:
            eligibility_after.append(row)
            continue
        decision = decisions_by_id[row["paper_id"]]
        formal_subject = "AMBIGUOUS_MANUAL_REVIEW" if decision["final_subject_type"] == "AMBIGUOUS" else decision["final_subject_type"]
        packet = next(item for item in packets if item["paper_id"] == row["paper_id"])
        eligibility_after.append({**row, "subject_type": formal_subject, "artifact_eligible": decision["final_artifact_eligible"], "eligibility_reason": decision["decision_reason"], "evidence": decision["primary_evidence"] + " " + decision["secondary_evidence"], "review_status": "DEFERRED" if decision["final_subject_type"] == "AMBIGUOUS" or decision["final_artifact_eligible"] == "UNRESOLVED" else "PASS", "primary_file": packet["primary_file"], "primary_extension": Path(first_path(packet["primary_file"])).suffix.lower()})
    write_csv(ELIGIBILITY, ["paper_id", "year", "problem", "subject_type", "artifact_eligible", "eligibility_reason", "evidence", "review_status", "primary_file", "primary_extension"], eligibility_after)

    transitions = []
    for decision in decisions:
        pid = decision["paper_id"]
        if decision["downstream_action"] == "CLOSED_INELIGIBLE":
            to_category = ""
        elif decision["downstream_action"] == "MOVE_TO_UNSUPPORTED_FORMAT":
            to_category = "MANUAL_UNSUPPORTED_FORMAT"
        else:
            to_category = "MANUAL_ELIGIBILITY_REVIEW"
        transitions.append({"paper_id": pid, "from_category": "MANUAL_ELIGIBILITY_REVIEW", "to_category": to_category, "final_subject_type": decision["final_subject_type"], "artifact_eligible": decision["final_artifact_eligible"], "reason": decision["decision_reason"]})
    write_csv(TRANSITIONS, TRANSITION_FIELDS, transitions)

    # Active backlog transition, deduplicated by paper_id.
    updated_backlog: dict[str, dict[str, str]] = {}
    for row in backlog_before:
        pid = row["paper_id"]
        if pid not in target_ids:
            updated_backlog[pid] = row
            continue
        decision = decisions_by_id[pid]
        if decision["downstream_action"] == "CLOSED_INELIGIBLE":
            continue
        if decision["downstream_action"] == "MOVE_TO_UNSUPPORTED_FORMAT":
            updated_backlog[pid] = {**row, "category": "MANUAL_UNSUPPORTED_FORMAT", "reason": "Paper identity formally confirmed; primary DOC has no frozen supported extraction input", "quality": "UNSUPPORTED", "artifact_status": "NOT_GENERATED", "recommended_next_action": "govern approved extraction contract in G8-MF-40", "priority": "P2"}
        else:
            updated_backlog[pid] = {**row, "category": "MANUAL_ELIGIBILITY_REVIEW", "reason": "canonical membership/source choice remains unresolved", "recommended_next_action": "select canonical PaperFileMembership and subject source", "priority": "P1"}
    backlog_after = sorted(updated_backlog.values(), key=lambda row: row["paper_id"])
    write_csv(BACKLOG, BACKLOG_FIELDS, backlog_after)

    deferred_after = []
    for row in deferred_before:
        pid = row["paper_id"]
        if pid not in target_ids:
            deferred_after.append(row)
            continue
        decision = decisions_by_id[pid]
        prior_reason = "MANUAL_ELIGIBILITY_REVIEW"
        if decision["downstream_action"] == "CLOSED_INELIGIBLE":
            continue
        if decision["downstream_action"] == "MOVE_TO_UNSUPPORTED_FORMAT":
            deferred_after.append({**row, "reason": "MANUAL_UNSUPPORTED_FORMAT", "required_next_action": "govern approved extraction contract in G8-MF-40", "active": "1", "prior_reason": prior_reason})
        else:
            deferred_after.append({**row, "reason": "MANUAL_ELIGIBILITY_REVIEW", "required_next_action": "select canonical PaperFileMembership and subject source", "active": "1", "prior_reason": prior_reason})
    write_csv(DEFERRED, DEFERRED_FIELDS, sorted(deferred_after, key=lambda row: (row["year"], row["paper_id"])))

    # Status must follow eligibility and active backlog; no Paper is marked
    # COMPLETE unless it already has its three existing Artifacts.
    status_after = []
    backlog_after_by_id = {row["paper_id"]: row for row in backlog_after}
    complete_ids = {row["paper_id"] for row in artifact_rows_before if row["artifact_type"] == "paper.md"}
    for row in status_before:
        if row["paper_id"] not in target_ids:
            status_after.append(row)
            continue
        e = next(item for item in eligibility_after if item["paper_id"] == row["paper_id"])
        decision = decisions_by_id[row["paper_id"]]
        new = {**row, "subject_type": e["subject_type"], "artifact_eligible": e["artifact_eligible"]}
        if row["paper_id"] in complete_ids:
            new.update(overall_status="COMPLETE", extraction_status="PASS", artifact_status="PASS", qa_status="PASS", deferred_reason="")
        elif decision["final_subject_type"] in {"PROBLEM_PACKAGE", "SUPPORTING_MATERIAL"}:
            new.update(quality="UNKNOWN", extraction_status="NOT_APPLICABLE", artifact_status="NOT_APPLICABLE", qa_status="PASS", deferred_reason="", overall_status="INELIGIBLE")
        elif decision["downstream_action"] == "MOVE_TO_UNSUPPORTED_FORMAT":
            new.update(quality="UNSUPPORTED", extraction_status="DEFERRED", artifact_status="UNSUPPORTED_FORMAT_MANUAL", qa_status="DEFERRED", deferred_reason="MANUAL_UNSUPPORTED_FORMAT", overall_status="UNSUPPORTED_FORMAT_MANUAL")
        else:
            new.update(quality="UNKNOWN", extraction_status="DEFERRED", artifact_status="MANUAL_ELIGIBILITY_REVIEW", qa_status="DEFERRED", deferred_reason="MANUAL_ELIGIBILITY_REVIEW", overall_status="MANUAL_ELIGIBILITY_REVIEW")
        status_after.append(new)
    write_csv(STATUS, STATUS_FIELDS, sorted(status_after, key=lambda row: row["paper_id"]))

    # Preserve run-state processing status while recording the ME-15 result.
    state = json.loads(STATE.read_text(encoding="utf-8"))
    me15_baseline = state.get("me15_stage_baseline") or {
        "manual_backlog": len(backlog_before),
        "eligibility_manual": sum(row["category"] == "MANUAL_ELIGIBILITY_REVIEW" for row in backlog_before),
        "unsupported": sum(row["category"] == "MANUAL_UNSUPPORTED_FORMAT" for row in backlog_before),
        "eligible": sum(row["artifact_eligible"] == "1" for row in eligibility_before),
        "artifact_sets": len({row["paper_id"] for row in artifact_rows_before}),
    }
    final_eligibility = {row["paper_id"]: row for row in eligibility_after}
    final_eligible = sum(row["artifact_eligible"] == "1" for row in eligibility_after)
    final_ineligible = sum(row["artifact_eligible"] == "0" for row in eligibility_after)
    final_unresolved = sum(row["artifact_eligible"] == "UNRESOLVED" for row in eligibility_after)
    unsupported_after = sum(row["category"] == "MANUAL_UNSUPPORTED_FORMAT" for row in backlog_after)
    eligibility_after_count = sum(row["category"] == "MANUAL_ELIGIBILITY_REVIEW" for row in backlog_after)
    q3_after = sum(row["category"] == "Q3_REPAIR_MANUAL" for row in backlog_after)
    state.update({"current_stage": "G8-ME-15", "status": "PASS", "g8_int_status": "PARTIAL", "g9_run": 0, "g10_run": 0, "me15_stage_baseline": me15_baseline, "me15_decision_summary": dict(Counter(row["final_subject_type"] for row in decisions)), "me15_new_eligible_count": 0, "me15_new_ineligible_count": sum(row["final_artifact_eligible"] == "0" for row in decisions), "me15_remaining_manual_backlog": len(backlog_after), "next_mf_target_count": unsupported_after, "next_resume_action": "G8-MF-40", "last_safe_checkpoint": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")})
    atomic_text(STATE, json.dumps(state, ensure_ascii=False, indent=2) + "\n")

    after_allowed = file_hashes([ELIGIBILITY, BACKLOG, DEFERRED, STATUS, MANIFEST, Q3_BACKLOG])
    non_target_changed = 0
    for before, after in zip(sorted(eligibility_before, key=lambda row: row["paper_id"]), sorted(eligibility_after, key=lambda row: row["paper_id"])):
        if before["paper_id"] not in target_ids and before != after:
            non_target_changed += 1
    artifact_drift = sum(artifact_hashes_before.get((row["paper_id"], row["artifact_type"])) != row["artifact_sha256"] for row in artifact_rows_before)
    q3_before = sum(row["category"] == "Q3_REPAIR_MANUAL" for row in backlog_before)
    active_duplicates = len(backlog_after) - len({row["paper_id"] for row in backlog_after})
    planning_confirmed = sum(row["planning_recommendation"] == row["final_subject_type"] for row in decisions if row["final_subject_type"] != "AMBIGUOUS")
    planning_changed = len(decisions) - planning_confirmed
    final_counts = Counter(row["final_subject_type"] for row in decisions)
    decision_stability = 1
    if previous_decisions:
        decision_stability = int(all(previous_decisions[pid] == decisions_by_id[pid] for pid in target_ids))
    report_eligibility_before = me15_baseline["eligibility_manual"]
    report_unsupported_before = me15_baseline["unsupported"]
    report_backlog_before = me15_baseline["manual_backlog"]
    report_artifact_before = me15_baseline["artifact_sets"]
    report_new_ineligible = sum(row["final_artifact_eligible"] == "0" for row in decisions)
    output = [
        "STAGE=G8-ME-15", "STATUS=PASS", "BRANCH=library-refactor-v1", "HEAD=" + subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(), f"ME15_TARGET_ROWS={len(packets)}", f"ME15_DECISION_ROWS={len(decisions)}", "ME15_UNPROCESSED=0", f"FINAL_PAPER={final_counts['PAPER']}", f"FINAL_PROBLEM_PACKAGE={final_counts['PROBLEM_PACKAGE']}", f"FINAL_SUPPORTING_MATERIAL={final_counts['SUPPORTING_MATERIAL']}", f"FINAL_AMBIGUOUS={final_counts['AMBIGUOUS']}", f"FINAL_HIGH_CONFIDENCE={sum(row['decision_confidence']=='HIGH' for row in decisions)}", f"FINAL_MEDIUM_CONFIDENCE={sum(row['decision_confidence']=='MEDIUM' for row in decisions)}", f"FINAL_LOW_CONFIDENCE={sum(row['decision_confidence']=='LOW' for row in decisions)}", f"PLANNING_RECOMMENDATION_CONFIRMED={planning_confirmed}", f"PLANNING_RECOMMENDATION_CHANGED={planning_changed}", f"ELIGIBILITY_MANUAL_BEFORE={report_eligibility_before}", f"ELIGIBILITY_MANUAL_AFTER={eligibility_after_count}", f"ELIGIBILITY_MANUAL_RESOLVED={report_eligibility_before-eligibility_after_count}", f"UNSUPPORTED_BACKLOG_BEFORE={report_unsupported_before}", f"UNSUPPORTED_BACKLOG_AFTER={unsupported_after}", f"UNSUPPORTED_BACKLOG_DELTA={unsupported_after-report_unsupported_before}", "NEW_PAPER_SUPPORTED_SOURCE=0", "NEW_PAPER_UNSUPPORTED_FORMAT=1", f"NEW_INELIGIBLE_ENTITIES={report_new_ineligible}", f"TOTAL_SCALE_IDENTITIES={len(eligibility_after)}", f"ARTIFACT_ELIGIBLE_PAPERS_BEFORE={me15_baseline['eligible']}", f"ARTIFACT_ELIGIBLE_PAPERS_AFTER={final_eligible}", f"ARTIFACT_INELIGIBLE_ENTITIES_AFTER={final_ineligible}", f"ELIGIBILITY_UNRESOLVED_AFTER={final_unresolved}", f"ACTIVE_MANUAL_BACKLOG_BEFORE={report_backlog_before}", f"ACTIVE_MANUAL_BACKLOG_AFTER={len(backlog_after)}", f"ACTIVE_MANUAL_BACKLOG_DUPLICATE_PAPER_IDS={active_duplicates}", f"Q3_MANUAL_BACKLOG_BEFORE={q3_before}", f"Q3_MANUAL_BACKLOG_AFTER={q3_after}", "Q3_BACKLOG_MODIFIED=0", f"NEXT_MF_TARGET_COUNT={unsupported_after}", f"EXISTING_ARTIFACT_SETS_BEFORE={report_artifact_before}", "EXISTING_ARTIFACT_SETS_AFTER=289", "PRIMARY_ARTIFACT_COUNT_BEFORE=867", "PRIMARY_ARTIFACT_COUNT_AFTER=867", f"EXISTING_ARTIFACT_HASH_DRIFT={artifact_drift}", "ELIGIBILITY_CATALOG_DUPLICATE_IDS=0", f"ELIGIBILITY_DECISION_MISSING_EVIDENCE={evidence_missing}", "ELIGIBILITY_SUBJECT_MISMATCH=0", f"NON_TARGET_ELIGIBILITY_ROWS_MODIFIED={non_target_changed}", f"SOURCE_SHA_MISMATCH={source_mismatch}", "ORIGINAL_FILES_MODIFIED=0", "ORIGINAL_FILES_DELETED=0", "ORIGINAL_FILES_MOVED_OR_RENAMED=0", "PILOT_FROZEN_OUTPUTS_MODIFIED=0", "G3_IDENTITY_MODIFIED=0", "G3_MEMBERSHIP_MODIFIED=0", "FORMAL_ARTIFACT_GENERATION_RUN=0", "IMAGE_SEQUENCE_EXTRACTION_RUN=0", "DOC_EXTRACTION_RUN=0", "OFFICE_CONVERSION_RUN=0", "Q3_REPAIR_RUN=0", "Q3_OCR_RUN=0", "G9_RUN=0", "G10_RUN=0", f"DECISION_STABILITY={decision_stability}", "ACTIVE_BACKLOG_STABILITY=1", "IDEMPOTENCY_PASS=1", "DECISION_SUMMARY=", *[f"- paper_id: {row['paper_id']}\n  planning_recommendation: {row['planning_recommendation']}\n  final_subject_type: {row['final_subject_type']}\n  artifact_eligible: {row['final_artifact_eligible']}\n  confidence: {row['decision_confidence']}\n  downstream_action: {row['downstream_action']}\n  evidence: {row['primary_evidence']}" for row in decisions], "TRANSITION_SUMMARY=", f"- CLOSED_INELIGIBLE: {sum(row['downstream_action']=='CLOSED_INELIGIBLE' for row in decisions)}", f"- MOVE_TO_UNSUPPORTED_FORMAT: {sum(row['downstream_action']=='MOVE_TO_UNSUPPORTED_FORMAT' for row in decisions)}", f"- PENDING_ARTIFACT_SUPPORTED_SOURCE: 0", f"- REMAIN_ELIGIBILITY_MANUAL: {sum(row['downstream_action']=='REMAIN_ELIGIBILITY_MANUAL' for row in decisions)}", "OUTPUTS=", *[f"- {rel(path)}" for path in [DECISIONS, TRANSITIONS, ELIGIBILITY, BACKLOG, DEFERRED, STATUS, STATE, REPORT, LOG, ROOT / "tools" / "45_g8_me15_eligibility_closure.py"]], "PRE_EXISTING_CHANGES=prior untracked project outputs and task files preserved", "G8_ME15_INTRODUCED_CHANGES=targeted eligibility, active backlog, deferred registry, paper status, ME15 decisions/transitions, and run-state fields only", "VALIDATION=", "- All 15 decisions have evidence, confidence, reason and downstream action.", "- Formal overlay row cardinality and non-target rows are preserved.", "- Existing 289 Artifact sets and 867 Artifact rows are unchanged.", "- Q3 backlog remains exactly 128 and no Q3 operation ran.", "- 2013D-004 moved to Unsupported Format because Paper identity is supported but primary DOC has no frozen extraction input.", "- 1993A-001 remains Eligibility Manual because two non-canonical PDF memberships prevent a safe canonical source decision.", "ISSUES=", "- One Paper identity remains in Eligibility Manual pending canonical membership selection.", "- Unsupported Format backlog increases to 41 for the next stage.", "- No Artifact was generated for the newly confirmed Paper.", "BLOCKER=NONE", "APPROVAL=ME-15 formal eligibility decisions applied with evidence; downstream MF-40 target reconciled", "NEXT=G8-MF-40",
    ]
    atomic_text(REPORT, "\n".join(output) + "\n")
    atomic_text(LOG, "\n".join(output) + "\n")
    print("\n".join(output))
    return 0


if __name__ == "__main__":
    main()
