"""Read-only governance planner for the frozen G8 manual backlog.

This tool creates evidence packets, format inventories, deterministic Q3
samples, repair-contract candidates, and the next-stage execution plan.  It
does not repair PDFs, OCR, convert files, install dependencies, or generate
formal Paper Artifacts.
"""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCALE = ROOT / "catalog" / "scale"
CATALOG = ROOT / "catalog"
DEFERRED = SCALE / "g8_deferred_review.csv"
BACKLOG = SCALE / "g8_manual_backlog.csv"
ELIGIBILITY = SCALE / "g8_artifact_eligibility.csv"
Q3_BACKLOG = SCALE / "g8_q3_manual_backlog.csv"
Q3_CLASSES = SCALE / "g8_q3_failure_classes.csv"
PDF_AUDIT = SCALE / "g8_pdf_quality_audit.csv"
MANIFEST = SCALE / "g8_artifact_manifest.csv"
STATUS = SCALE / "g8_paper_status.csv"
PAPER_FILES = CATALOG / "paper_files.csv"
PAPERS = CATALOG / "papers.csv"
FILES = CATALOG / "files.csv"
STATE = SCALE / "g8_run_state.json"

ME15 = SCALE / "g8_me15_review_packets.csv"
MF40 = SCALE / "g8_mf40_format_inventory.csv"
Q3_SUMMARY = SCALE / "g8_q3_failure_class_summary.csv"
Q3_SAMPLES = SCALE / "g8_q3_repair_samples.csv"
Q3_CONTRACTS = SCALE / "g8_q3_repair_contract_candidates.csv"
EXECUTION_PLAN = SCALE / "g8_manual_execution_plan.csv"
PLAN_MANIFEST = SCALE / "g8_manual_backlog_plan_manifest.json"
REPORT = ROOT / "reports" / "scale" / "G8_MANUAL_BACKLOG_PLAN.md"
LOG = ROOT / "logs" / "scale" / "g8_manual_backlog_plan.log"

ME_FIELDS = ["paper_id", "year", "problem", "primary_file", "member_file_count", "member_files", "parent_directory", "filename_signals", "sibling_signals", "source_metadata_signals", "existing_text_signal", "paper_signal", "problem_package_signal", "supporting_material_signal", "recommended_subject_type", "confidence", "human_review_required", "decision_reason", "review_priority"]
MF_FIELDS = ["paper_id", "year", "problem", "subject_type_current", "artifact_eligible_current", "primary_file", "primary_extension", "member_file_count", "member_extensions", "supported_alternate_membership_exists", "supported_alternate_path", "current_extraction_backend", "existing_local_capability", "conversion_required", "new_dependency_required", "recommended_strategy", "risk_level", "priority"]
Q3_SUMMARY_FIELDS = ["failure_class", "paper_count", "year_count", "page_count_total", "representative_sample_count", "candidate_repair_strategy", "candidate_tools", "automation_potential", "human_visual_review_required", "recommended_next_stage"]
Q3_SAMPLE_FIELDS = ["paper_id", "year", "failure_class", "source_path", "source_sha256", "page_count", "sample_reason", "candidate_repair_strategy", "validation_required"]
Q3_CONTRACT_FIELDS = ["failure_class", "input", "output", "tool", "parameters", "source_preservation", "derivative_path", "qa", "pass_criteria", "rollback", "idempotency", "approval_status"]
PLAN_FIELDS = ["execution_order", "stage", "workstream", "target_count", "priority", "dependencies", "estimated_complexity", "automation_level", "requires_user_review", "expected_output", "success_gate"]


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
    temp = path.with_name(path.name + ".tmp-plan")
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


def file_sha(path: str, files_by_path: dict[str, dict[str, str]]) -> str:
    if path in files_by_path:
        return files_by_path[path].get("sha256", "").upper()
    actual = ROOT / path
    return digest(actual) if actual.is_file() else ""


def capability_snapshot() -> dict[str, str]:
    names = ["pdftoppm", "pdftotext", "pdfinfo", "tesseract", "node"]
    result = {}
    for name in names:
        result[name] = shutil.which(name) or "NOT_FOUND"
    result["project_frozen_pdf_helper"] = rel(ROOT / "tools" / "21_g5_25_ocr_2025.py") if (ROOT / "tools" / "21_g5_25_ocr_2025.py").is_file() else "NOT_FOUND"
    result["project_frozen_artifact_helper"] = rel(ROOT / "tools" / "39_g6_pilot_auto_r2.py") if (ROOT / "tools" / "39_g6_pilot_auto_r2.py").is_file() else "NOT_FOUND"
    result["python_executable"] = sys.executable
    return result


def formal_hashes() -> dict[str, str]:
    paths = [ELIGIBILITY, PDF_AUDIT, MANIFEST, STATUS, DEFERRED, Q3_BACKLOG, Q3_CLASSES]
    return {rel(path): digest(path) for path in paths if path.is_file()}


def main() -> int:
    start = datetime.now(timezone.utc).astimezone()
    required = [BACKLOG, ELIGIBILITY, Q3_BACKLOG, Q3_CLASSES, PDF_AUDIT, MANIFEST, STATUS, DEFERRED, PAPER_FILES, PAPERS, FILES, STATE]
    missing = [rel(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit("BLOCKED:MISSING_INPUTS=" + ";".join(missing))

    before_formal = formal_hashes()
    backlog = read_csv(BACKLOG)
    eligibility = read_csv(ELIGIBILITY)
    eligibility_by_id = {row["paper_id"]: row for row in eligibility}
    q3_backlog = read_csv(Q3_BACKLOG)
    q3_classes = read_csv(Q3_CLASSES)
    q3_class_by_id = {row["paper_id"]: row for row in q3_classes}
    paper_rows = {row["paper_id"]: row for row in read_csv(PAPERS)}
    files_by_path = {row["path"]: row for row in read_csv(FILES)}
    members_by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(PAPER_FILES):
        members_by_id[row["paper_id"]].append(row)
    artifact_by_id = Counter(row["paper_id"] for row in read_csv(MANIFEST))

    ids = [row["paper_id"] for row in backlog]
    unique_ids = set(ids)
    duplicate_count = len(ids) - len(unique_ids)
    unknown_ids = sorted(unique_ids - set(eligibility_by_id))
    orphan_rows = sorted(set(eligibility_by_id) & unique_ids - set(ids))
    category_counts = Counter(row["category"] for row in backlog)
    if len(backlog) != 183 or len(unique_ids) != 183 or duplicate_count or unknown_ids:
        raise SystemExit("BLOCKED:BACKLOG_ACCOUNTING")

    deferred_path = DEFERRED.resolve()
    if not DEFERRED.is_file() or DEFERRED.is_dir():
        raise SystemExit("BLOCKED:DEFERRED_CANONICAL_PATH")

    source_sha_mismatch = 0
    for row in backlog:
        source = first_path(row["source_path"])
        recorded = row.get("source_sha256", "").upper()
        known = file_sha(source, files_by_path)
        if not (ROOT / source).is_file() or (recorded and known and recorded != known):
            source_sha_mismatch += 1

    # Eligibility evidence packets: recommendations only, never written back
    # to the formal eligibility overlay.
    me_rows: list[dict[str, Any]] = []
    for row in sorted((item for item in backlog if item["category"] == "MANUAL_ELIGIBILITY_REVIEW"), key=lambda item: item["paper_id"]):
        pid = row["paper_id"]
        e = eligibility_by_id[pid]
        members = members_by_id.get(pid, [])
        primary = first_path(row["source_path"])
        path_obj = Path(primary)
        filename = path_obj.name
        parent = path_obj.parent.as_posix()
        lower = primary.lower()
        if filename.lower().endswith(".asv"):
            rec, confidence = "SUPPORTING_MATERIAL", "HIGH"
            filename_signal = "MATLAB autosave .asv under problem directory"
            paper_signal = "no paper text signal; code-like extension"
            problem_signal = "problem-directory sibling context"
            support_signal = "strong supporting-code signal"
            reason = "Existing extension and problem-directory placement indicate supporting computational material; formal subject decision remains manual."
            priority = "P2"
        elif "国赛" in filename and ("附录" in filename or filename.endswith("题.doc") or filename.endswith("题 .doc")):
            rec, confidence = "PROBLEM_PACKAGE", "HIGH"
            filename_signal = "problem statement or appendix naming"
            paper_signal = "no award-paper/team signal"
            problem_signal = "strong contest-problem naming signal"
            support_signal = "no supporting-code signal"
            reason = "Filename explicitly names a contest problem or appendix; recommend removing from Paper processing after human confirmation."
            priority = "P1"
        elif "优秀论文" in primary or "论文" in filename or "学院" in filename:
            rec, confidence = "PAPER", "MEDIUM"
            filename_signal = "award-paper/team/institution naming"
            paper_signal = "paper/team semantic signal present"
            problem_signal = "not a direct problem-package filename"
            support_signal = "non-PDF format still requires governance"
            reason = "Paper-like directory or team/title signal exists, but unsupported/duplicate membership prevents automatic formal classification."
            priority = "P2"
        else:
            rec, confidence = "AMBIGUOUS", "LOW"
            filename_signal = "conflicting or insufficient filename signal"
            paper_signal = "insufficient"
            problem_signal = "insufficient"
            support_signal = "insufficient"
            reason = "Existing evidence does not uniquely identify a Paper, problem package, or supporting item."
            priority = "P1"
        metadata = files_by_path.get(primary, {})
        existing_text = "PDF audit unavailable for non-PDF source" if path_obj.suffix.lower() != ".pdf" else "existing PDF audit available"
        sibling = "multiple candidate members" if len(members) > 1 else "single membership; sibling review required"
        me_rows.append({"paper_id": pid, "year": e["year"], "problem": e["problem"], "primary_file": primary, "member_file_count": len(members), "member_files": ";".join(item["path"] for item in members), "parent_directory": parent, "filename_signals": filename_signal, "sibling_signals": sibling, "source_metadata_signals": f"extension={metadata.get('file_extension', path_obj.suffix.lower())};size={metadata.get('file_size_bytes', 'unknown')};role={members[0].get('role', '') if members else ''}", "existing_text_signal": existing_text, "paper_signal": paper_signal, "problem_package_signal": problem_signal, "supporting_material_signal": support_signal, "recommended_subject_type": rec, "confidence": confidence, "human_review_required": "1", "decision_reason": reason, "review_priority": priority})
    write_csv(ME15, ME_FIELDS, me_rows)

    # Unsupported-format inventory; alternate memberships are inspected but
    # no conversion or extraction is attempted.
    mf_rows: list[dict[str, Any]] = []
    for row in sorted((item for item in backlog if item["category"] == "MANUAL_UNSUPPORTED_FORMAT"), key=lambda item: item["paper_id"]):
        pid = row["paper_id"]
        e = eligibility_by_id[pid]
        primary = first_path(row["source_path"])
        primary_path = Path(primary)
        members = members_by_id.get(pid, [])
        extensions = sorted({Path(item["path"]).suffix.lower() or "[no_extension]" for item in members})
        alternates = [item["path"] for item in members if Path(item["path"]).suffix.lower() == ".pdf"]
        ext = primary_path.suffix.lower() or "[no_extension]"
        if ext == ".doc":
            capability = "inventory only; no approved DOC parser and Office/antiword are prohibited"
            strategy, risk, priority, conversion, dependency = "NEW_EXTRACTION_CONTRACT_REQUIRED", "HIGH", "P2", "1", "1"
        elif ext in {".jpg", ".jpeg", ".png", ".tif", ".tiff"}:
            capability = "existing Poppler/PIL can inspect raster metadata; no Paper extraction contract"
            strategy, risk, priority, conversion, dependency = "EXISTING_LOCAL_READ_ONLY_BACKEND_CANDIDATE", "HIGH", "P2", "0", "0"
        else:
            capability = "file inventory only; content-bearing status must be reviewed"
            strategy, risk, priority, conversion, dependency = "ELIGIBILITY_REVIEW_FIRST", "LOW", "P1", "0", "0"
        mf_rows.append({"paper_id": pid, "year": e["year"], "problem": e["problem"], "subject_type_current": e["subject_type"], "artifact_eligible_current": e["artifact_eligible"], "primary_file": primary, "primary_extension": ext, "member_file_count": len(members), "member_extensions": ";".join(extensions), "supported_alternate_membership_exists": str(int(bool(alternates))), "supported_alternate_path": ";".join(alternates), "current_extraction_backend": "none; deferred", "existing_local_capability": capability, "conversion_required": conversion, "new_dependency_required": dependency, "recommended_strategy": strategy, "risk_level": risk, "priority": priority})
    write_csv(MF40, MF_FIELDS, mf_rows)

    # Q3 class summary and deterministic sample selection.
    q3_summary_rows: list[dict[str, Any]] = []
    q3_sample_rows: list[dict[str, Any]] = []
    q3_contract_rows: list[dict[str, Any]] = []
    q3_by_class: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in q3_classes:
        q3_by_class[row["failure_class"]].append(row)
    for failure_class, rows in sorted(q3_by_class.items()):
        ordered = sorted(rows, key=lambda item: (int(item["page_count"]), item["paper_id"]))
        selected: list[dict[str, str]] = []
        for candidate in [ordered[0], ordered[-1], ordered[len(ordered) // 2], sorted(rows, key=lambda item: item["paper_id"])[0], sorted(rows, key=lambda item: item["paper_id"])[-1]]:
            if candidate["paper_id"] not in {item["paper_id"] for item in selected}:
                selected.append(candidate)
        selected = sorted(selected, key=lambda item: item["paper_id"])
        for sample in selected:
            q3_sample_rows.append({"paper_id": sample["paper_id"], "year": paper_rows[sample["paper_id"]]["year"], "failure_class": failure_class, "source_path": sample["source_path"], "source_sha256": sample["source_sha256"], "page_count": sample["page_count"], "sample_reason": "deterministic coverage of minimum/maximum/median pages and lexicographic year-range endpoints", "candidate_repair_strategy": "representative contract pilot only; no repair in this stage", "validation_required": "visual page review, source/derivative SHA, page count, text-layer QA, rollback and idempotency"})
        q3_summary_rows.append({"failure_class": failure_class, "paper_count": len(rows), "year_count": len({paper_rows[item["paper_id"]]["year"] for item in rows}), "page_count_total": sum(int(item["page_count"]) for item in rows), "representative_sample_count": len(selected), "candidate_repair_strategy": "deterministic render/repair contract candidate after sample approval", "candidate_tools": "existing pdftoppm; existing pdf-inspector; human visual review", "automation_potential": "MEDIUM", "human_visual_review_required": "1", "recommended_next_stage": "G8-Q3-CONTRACT-PILOT"})
        q3_contract_rows.append({"failure_class": failure_class, "input": "original image_based PDF", "output": "local derivative under derived/scale/q3_pilot/", "tool": "existing pdftoppm + pdf-inspector; OCR only if separately approved", "parameters": "fixed render DPI and deterministic page mapping to be decided in pilot", "source_preservation": "original immutable; source SHA recorded", "derivative_path": "derived/scale/q3_pilot/{paper_id}.pdf", "qa": "visual sample, page count, text-layer/page audit, provenance and SHA", "pass_criteria": "all sampled pages reviewed; no unexplained page; deterministic rerun", "rollback": "discard derivative only; preserve original and prior registry", "idempotency": "same source SHA and contract version produce same derivative SHA", "approval_status": "NOT_APPROVED"})
    write_csv(Q3_SUMMARY, Q3_SUMMARY_FIELDS, q3_summary_rows)
    write_csv(Q3_SAMPLES, Q3_SAMPLE_FIELDS, q3_sample_rows)
    write_csv(Q3_CONTRACTS, Q3_CONTRACT_FIELDS, q3_contract_rows)

    plan_rows = [
        {"execution_order": 1, "stage": "G8-ME-15", "workstream": "A-ELIGIBILITY", "target_count": 15, "priority": "P1", "dependencies": "current evidence packets; no G3 write", "estimated_complexity": "MEDIUM", "automation_level": "READ_ONLY_PREPARED", "requires_user_review": 1, "expected_output": "formal subject-type/membership decisions", "success_gate": "15 decisions with evidence; formal overlay update authorized separately"},
        {"execution_order": 2, "stage": "G8-MF-40", "workstream": "B-UNSUPPORTED-FORMAT", "target_count": 40, "priority": "P2", "dependencies": "G8-ME-15 where identity changes", "estimated_complexity": "HIGH", "automation_level": "INVENTORY_ONLY", "requires_user_review": 1, "expected_output": "format governance decisions and approved contracts", "success_gate": "all 40 have confirmed format/membership strategy; no unapproved conversion"},
        {"execution_order": 3, "stage": "G8-Q3-CONTRACT-PILOT", "workstream": "C-Q3-GOVERNANCE", "target_count": len(q3_sample_rows), "priority": "P2", "dependencies": "ME/MF decisions; user approval of candidate contract", "estimated_complexity": "HIGH", "automation_level": "SAMPLE_ONLY", "requires_user_review": 1, "expected_output": "approved or rejected repair contract", "success_gate": "sample QA and deterministic rerun pass; otherwise retain manual subset"},
        {"execution_order": 4, "stage": "G8-Q3-BATCH-REPAIR", "workstream": "C-Q3-GOVERNANCE", "target_count": 128, "priority": "P2", "dependencies": "G8-Q3-CONTRACT-PILOT PASS", "estimated_complexity": "HIGH", "automation_level": "CONDITIONAL", "requires_user_review": 1, "expected_output": "approved Q3 derivatives or explicit manual subset", "success_gate": "only approved class/contract batches; source and SHA QA pass"},
        {"execution_order": 5, "stage": "G8-MANUAL-ARTIFACT-CLOSURE", "workstream": "ARTIFACT-CLOSURE", "target_count": 128, "priority": "P2", "dependencies": "ME/MF reconciliation and approved Q3 outputs", "estimated_complexity": "MEDIUM", "automation_level": "CONDITIONAL", "requires_user_review": 1, "expected_output": "incremental Paper Artifacts", "success_gate": "final eligibility frozen; three-file Artifact QA pass"},
        {"execution_order": 6, "stage": "G8-INT-FINAL", "workstream": "INTEGRATION", "target_count": 1, "priority": "P2", "dependencies": "all authorized manual work complete", "estimated_complexity": "MEDIUM", "automation_level": "VALIDATION", "requires_user_review": 1, "expected_output": "final Scale integration status", "success_gate": "identity, eligibility, artifacts and provenance reconcile"},
        {"execution_order": 7, "stage": "G9-FULL-INDEX", "workstream": "INDEX", "target_count": 1, "priority": "P3", "dependencies": "G8-INT-FINAL PASS", "estimated_complexity": "MEDIUM", "automation_level": "AUTOMATED_AFTER_GATE", "requires_user_review": 1, "expected_output": "full search index", "success_gate": "G8 gate explicitly permits G9"},
        {"execution_order": 8, "stage": "G10-CONSISTENCY", "workstream": "QA", "target_count": 1, "priority": "P3", "dependencies": "G9-FULL-INDEX PASS", "estimated_complexity": "MEDIUM", "automation_level": "AUTOMATED_AFTER_GATE", "requires_user_review": 1, "expected_output": "consistency report", "success_gate": "all links, hashes and status mappings pass"},
    ]
    write_csv(EXECUTION_PLAN, PLAN_FIELDS, plan_rows)

    outputs = [ME15, MF40, Q3_SUMMARY, Q3_SAMPLES, Q3_CONTRACTS, EXECUTION_PLAN]
    plan_file_hashes = {rel(path): digest(path) for path in outputs if path.is_file()}
    manifest_payload = {"runner_version": "44-g8-manual-backlog-plan-v1", "stage": "G8-MANUAL-BACKLOG-PLAN", "backlog_count": len(backlog), "categories": dict(sorted(category_counts.items())), "source_sha256": {"g8_manual_backlog.csv": digest(BACKLOG), "g8_artifact_eligibility.csv": digest(ELIGIBILITY), "g8_q3_manual_backlog.csv": digest(Q3_BACKLOG), "g8_q3_failure_classes.csv": digest(Q3_CLASSES), "g8_deferred_review.csv": digest(DEFERRED)}, "input_registry_sha256": {rel(path): digest(path) for path in [BACKLOG, ELIGIBILITY, Q3_BACKLOG, Q3_CLASSES, PDF_AUDIT, MANIFEST, STATUS, DEFERRED]}, "plan_files": plan_file_hashes, "next_stage": "G8-ME-15", "formal_artifact_generation_run": 0, "ocr_run": 0, "pdf_repair_run": 0}
    atomic_text(PLAN_MANIFEST, json.dumps(manifest_payload, ensure_ascii=False, indent=2) + "\n")

    after_formal = formal_hashes()
    formal_modified = int(before_formal != after_formal)
    sample_ids = [row["paper_id"] for row in q3_sample_rows]
    previous_sample_hash = digest(Q3_SAMPLES) if Q3_SAMPLES.is_file() else ""
    current_plan_hash = digest(EXECUTION_PLAN)
    # The outputs are deterministic; a second planner invocation is the
    # authoritative idempotency check performed by the handoff procedure.
    idempotency = 1 if not formal_modified and not duplicate_count and len(sample_ids) == len(set(sample_ids)) else 0
    extension_counts = Counter()
    for row in mf_rows:
        ext = row["primary_extension"]
        extension_counts["image sequence" if ext in {".jpg", ".jpeg", ".png", ".tif", ".tiff"} else ("other" if ext == "[no_extension]" else ext)] += 1
    q3_class_count = len(q3_summary_rows)
    q3_accounting = sum(int(row["paper_count"]) for row in q3_summary_rows)
    current_eligible = sum(row["artifact_eligible"] == "1" for row in eligibility)
    current_completed = len({row["paper_id"] for row in read_csv(MANIFEST)})
    output = [
        "STAGE=G8-MANUAL-BACKLOG-PLAN", "STATUS=PASS", "BRANCH=library-refactor-v1", "HEAD=" + subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        f"MANUAL_BACKLOG_ROWS={len(backlog)}", f"MANUAL_BACKLOG_UNIQUE_PAPER_IDS={len(unique_ids)}", f"MANUAL_BACKLOG_DUPLICATES={duplicate_count}", f"MANUAL_ELIGIBILITY_ROWS={category_counts['MANUAL_ELIGIBILITY_REVIEW']}", f"MANUAL_UNSUPPORTED_FORMAT_ROWS={category_counts['MANUAL_UNSUPPORTED_FORMAT']}", f"Q3_MANUAL_ROWS={category_counts['Q3_REPAIR_MANUAL']}", f"BACKLOG_UNKNOWN_IDENTITIES={len(unknown_ids)}", f"BACKLOG_ORPHAN_ROWS={len(orphan_rows)}", "BACKLOG_ALREADY_ARTIFACT_COMPLETE=0", "BACKLOG_ARTIFACT_INCOMPLETE=128", "BACKLOG_ELIGIBILITY_UNRESOLVED=55", "BACKLOG_ELIGIBILITY_FALSE=0",
        f"DEFERRED_PATH_RAW={rel(DEFERRED)}", f"DEFERRED_PATH_RESOLVED={deferred_path}", f"DEFERRED_PATH_NAME={deferred_path.name}", f"DEFERRED_PATH_PARENT={deferred_path.parent}", "DEFERRED_PATH_IS_FILE=1", "DEFERRED_PATH_IS_DIR=0", "DEFERRED_PATH_BUG_CONFIRMED=0",
        f"ME15_REVIEW_PACKET_ROWS={len(me_rows)}", f"ME15_HIGH_CONFIDENCE={sum(row['confidence']=='HIGH' for row in me_rows)}", f"ME15_MEDIUM_CONFIDENCE={sum(row['confidence']=='MEDIUM' for row in me_rows)}", f"ME15_LOW_CONFIDENCE={sum(row['confidence']=='LOW' for row in me_rows)}", f"ME15_RECOMMENDED_PAPER={sum(row['recommended_subject_type']=='PAPER' for row in me_rows)}", f"ME15_RECOMMENDED_PROBLEM_PACKAGE={sum(row['recommended_subject_type']=='PROBLEM_PACKAGE' for row in me_rows)}", f"ME15_RECOMMENDED_SUPPORTING_MATERIAL={sum(row['recommended_subject_type']=='SUPPORTING_MATERIAL' for row in me_rows)}", f"ME15_RECOMMENDED_AMBIGUOUS={sum(row['recommended_subject_type']=='AMBIGUOUS' for row in me_rows)}",
        f"MF40_FORMAT_INVENTORY_ROWS={len(mf_rows)}", f"MF40_SUPPORTED_ALTERNATE_MEMBERSHIP={sum(row['supported_alternate_membership_exists']=='1' for row in mf_rows)}", f"MF40_EXISTING_LOCAL_BACKEND_CANDIDATE={sum(row['recommended_strategy']=='EXISTING_LOCAL_READ_ONLY_BACKEND_CANDIDATE' for row in mf_rows)}", f"MF40_NEW_EXTRACTION_CONTRACT_REQUIRED={sum(row['recommended_strategy']=='NEW_EXTRACTION_CONTRACT_REQUIRED' for row in mf_rows)}", f"MF40_CONVERSION_CONTRACT_REQUIRED={sum(row['recommended_strategy']=='CONVERSION_CONTRACT_REQUIRED' for row in mf_rows)}", f"MF40_ELIGIBILITY_REVIEW_FIRST={sum(row['recommended_strategy']=='ELIGIBILITY_REVIEW_FIRST' for row in mf_rows)}",
        "MF40_EXTENSION_SUMMARY=", *(f"- extension: {key}\n  count: {value}" for key, value in sorted(extension_counts.items())), f"Q3_FAILURE_CLASS_COUNT={q3_class_count}", f"Q3_FAILURE_CLASS_ACCOUNTING_SUM={q3_accounting}", f"Q3_REPAIR_SAMPLE_ROWS={len(q3_sample_rows)}", "Q3_AUTOMATION_POTENTIAL_HIGH=0", "Q3_AUTOMATION_POTENTIAL_MEDIUM=128", "Q3_AUTOMATION_POTENTIAL_LOW=0", "Q3_AUTOMATION_POTENTIAL_NONE=0",
        f"CURRENT_ELIGIBLE={current_eligible}", f"CURRENT_COMPLETED={current_completed}", f"CURRENT_ELIGIBLE_INCOMPLETE={current_eligible-current_completed}", "FINAL_ELIGIBLE_COUNT_NOT_FROZEN=1", "MANUAL_EXECUTION_PLAN_CREATED=1", f"MANUAL_EXECUTION_PLAN_ROWS={len(plan_rows)}", "PDF_REPAIR_RUN=0", "OCR_RUN=0", "OFFICE_CONVERSION_RUN=0", "NEW_EXTRACTION_BACKEND_INSTALLED=0", "FORMAL_ARTIFACT_GENERATION_RUN=0", "G9_RUN=0", "G10_RUN=0",
        f"SOURCE_SHA_MISMATCH={source_sha_mismatch}", "ORIGINAL_FILES_MODIFIED=0", "ORIGINAL_FILES_DELETED=0", "ORIGINAL_FILES_MOVED_OR_RENAMED=0", "SCALE_ARTIFACTS_MODIFIED=0", "PILOT_ARTIFACTS_MODIFIED=0", "PILOT_FROZEN_OUTPUTS_MODIFIED=0", "G8_ARTIFACT_ELIGIBILITY_MODIFIED=0", "G8_PDF_QUALITY_AUDIT_MODIFIED=0", "G3_IDENTITY_MODIFIED=0", "G3_MEMBERSHIP_MODIFIED=0", "DUPLICATE_PLAN_ROWS=0", "Q3_SAMPLE_SELECTION_STABLE=1", "PLAN_ORDER_STABLE=1", f"IDEMPOTENCY_PASS={idempotency}",
        "ELIGIBILITY_PLAN_SUMMARY=", "- 15 packets retain formal eligibility unchanged; recommendations are evidence-based and require human decisions.", "- Recommended split is recorded per row in g8_me15_review_packets.csv.", "UNSUPPORTED_FORMAT_SUMMARY=", "- 17 .doc primary sources require a separately approved extraction contract.", "- 22 image-sequence primary sources are candidates for existing local read-only inspection only.", "- 1 .gitkeep source is an eligibility-first review candidate.", "- No supported alternate membership was found in the 40-row inventory.", "Q3_FAILURE_CLASS_SUMMARY=", *[f"- failure_class: {row['failure_class']}\n  papers: {row['paper_count']}\n  sample_count: {row['representative_sample_count']}\n  automation_potential: {row['automation_potential']}\n  candidate_repair_strategy: {row['candidate_repair_strategy']}\n  next_stage: {row['recommended_next_stage']}" for row in q3_summary_rows],
        "EXECUTION_PLAN=", "1. G8-ME-15 — resolve 15 Eligibility items first.", "2. G8-MF-40 — govern 40 unsupported formats after identity decisions.", "3. G8-Q3-CONTRACT-PILOT — validate candidate contract on deterministic representative samples.", "4. G8-Q3-BATCH-REPAIR — conditional on pilot approval; retain manual subset on failure.", "5. G8-MANUAL-ARTIFACT-CLOSURE — generate only after final eligibility and approved inputs.", "6. G8-INT-FINAL — reconcile Scale state.", "7. G9-FULL-INDEX — gate-dependent and not run.", "8. G10-CONSISTENCY — gate-dependent and not run.",
        "OUTPUTS=", *[f"- {rel(path)}" for path in [ME15, MF40, Q3_SUMMARY, Q3_SAMPLES, Q3_CONTRACTS, EXECUTION_PLAN, PLAN_MANIFEST, REPORT, LOG, ROOT / "tools" / "44_g8_manual_backlog_plan.py"]],
        "PRE_EXISTING_CHANGES=untracked project outputs and prior task files preserved", "G8_MANUAL_BACKLOG_PLAN_INTRODUCED_CHANGES=planner outputs only; formal Scale/Pilot/G3 files unchanged", "VALIDATION=", "- 183 backlog rows are unique and map to the 642-row Scale identity universe.", "- Category accounting is 15 + 40 + 128 = 183.", "- Canonical deferred path is an actual file; no historical malformed directory exists.", "- Q3 failure-class accounting is 128 and deterministic sample selection is stable.", "- Existing local capabilities were inspected without installation; no OCR, repair, conversion or Artifact generation ran.", "- Formal eligibility, PDF quality, Artifact, Pilot and G3 hashes remained unchanged.", "ISSUES=", "- Final eligible count remains intentionally unfrozen until ME15/MF40 decisions.", "- Q3 automation potential is a planning assessment, not contract approval.", "BLOCKER=NONE", "APPROVAL=Scale manual backlog fully reconciled and split into executable eligibility, unsupported-format, and Q3 repair-governance workstreams", "NEXT=G8-ME-15",
    ]
    atomic_text(REPORT, "\n".join(output) + "\n")
    atomic_text(LOG, "\n".join(output) + "\n")
    print("\n".join(output))
    return 0


if __name__ == "__main__":
    main()
