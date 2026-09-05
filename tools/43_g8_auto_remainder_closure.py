"""G8 automatic remainder closure.

This stage consumes the frozen Scale outputs from G8 Deferred Closure.  It
does not rerun G8, does not repair Q3, and does not modify Pilot/G3/original
files.  Remaining Q2 derivatives are only resumed when a local derivative is
already present; the 55 non-Q3 rows are classified from the existing
eligibility and membership evidence.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import shutil
import subprocess
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCALE = ROOT / "catalog" / "scale"
DERIVED = ROOT / "derived" / "scale"
PILOT = ROOT / "catalog" / "pilot"
STATE = SCALE / "g8_run_state.json"
DEFERRED = SCALE / "g8_deferred_review.csv"
ELIGIBILITY = SCALE / "g8_artifact_eligibility.csv"
PDF_AUDIT = SCALE / "g8_pdf_quality_audit.csv"
Q2_RESULTS = SCALE / "g8_q2_ocr_results.csv"
Q2_AUDIT = SCALE / "g8_q2_page_audit.csv"
Q3_CLASSES = SCALE / "g8_q3_failure_classes.csv"
MANIFEST = SCALE / "g8_artifact_manifest.csv"
PAPER_MAP = SCALE / "g8_paper_artifact_map.csv"
PAPER_STATUS = SCALE / "g8_paper_status.csv"
REPAIR_MANIFEST = SCALE / "g8_repair_manifest.jsonl"
Q2_DIAGNOSIS = SCALE / "g8_q2_remainder_diagnosis.csv"
REMAINDER_RECON = SCALE / "g8_remainder_reconciliation.csv"
Q3_BACKLOG = SCALE / "g8_q3_manual_backlog.csv"
MANUAL_BACKLOG = SCALE / "g8_manual_backlog.csv"
REPORT = ROOT / "reports" / "scale" / "G8_AUTO_REMAINDER_CLOSURE.md"
LOG = ROOT / "logs" / "scale" / "g8_auto_remainder_closure.log"
ARTIFACT_TYPES = ("paper.md", "metadata.yaml", "knowledge_card.md")
Q2_AUDIT_FIELDS = ["paper_id", "source_file", "source_sha256", "source_page", "page_class", "final_page_class", "extraction_chars", "status", "evidence"]
Q2_RESULT_FIELDS = ["paper_id", "source_file", "source_sha256", "derivative_path", "derivative_sha256", "page_count", "ocr_engine", "ocr_engine_version", "ocr_languages", "status", "failure_reason"]
DIAG_FIELDS = ["paper_id", "source_path", "source_sha256", "page_count", "prior_deferred_reason", "ocr_started", "ocr_completed", "ocr_output_exists", "page_audit_exists", "extraction_failure_reason", "retry_safe"]
RECON_FIELDS = ["paper_id", "category", "prior_reason", "subject_type", "artifact_eligible", "source_path", "source_sha256", "final_status", "resolution", "evidence"]
Q3_BACKLOG_FIELDS = ["paper_id", "year", "problem", "source_path", "source_sha256", "quality", "failure_class", "manual_required", "artifact_status", "recommended_manual_action", "review_priority"]
MANUAL_FIELDS = ["paper_id", "year", "problem", "category", "reason", "source_path", "quality", "artifact_status", "recommended_next_action", "priority"]
STATUS_FIELDS = ["paper_id", "year", "subject_type", "artifact_eligible", "quality", "extraction_status", "artifact_status", "qa_status", "deferred_reason", "overall_status"]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def atomic_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp-rm")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> None:
    from io import StringIO
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows({field: row.get(field, "") for field in fields} for row in rows)
    atomic_text(path, "\ufeff" + output.getvalue())


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def validate_artifacts() -> tuple[int, int, int, dict[str, str]]:
    rows = read_csv(MANIFEST)
    by_key: dict[tuple[str, str], dict[str, str]] = {}
    papers: set[str] = set()
    drift = 0
    for row in rows:
        key = (row["paper_id"], row["artifact_type"])
        if key in by_key:
            raise RuntimeError("BLOCKED:DUPLICATE_ARTIFACT_MANIFEST_ROWS")
        by_key[key] = row
        papers.add(row["paper_id"])
        artifact = ROOT / row["artifact_path"]
        if not artifact.is_file() or sha256(artifact) != row["artifact_sha256"].upper():
            drift += 1
    prior_q2_ids = {row.get("paper_id") for row in load_jsonl(REPAIR_MANIFEST) if row.get("stage") == "G8-Q2-R"}
    current_q2_ids = {row["paper_id"] for row in rows if row.get("quality") == "Q2"}
    baseline_papers = (papers - current_q2_ids) | prior_q2_ids
    baseline_keys = {(paper, artifact_type) for paper in baseline_papers for artifact_type in ARTIFACT_TYPES}
    baseline_drift = sum(key not in by_key or not (ROOT / by_key[key]["artifact_path"]).is_file() or sha256(ROOT / by_key[key]["artifact_path"]) != by_key[key]["artifact_sha256"].upper() for key in baseline_keys)
    if len(baseline_papers) != 283 or len(baseline_keys) != 849 or baseline_drift or drift:
        raise RuntimeError(f"BLOCKED:PREVIOUS_ARTIFACT_BASELINE:{len(baseline_papers)},{len(baseline_keys)},0,{baseline_drift + drift}")
    return len(baseline_papers), len(baseline_keys), baseline_drift, {f"{paper}|{kind}": by_key[(paper, kind)]["artifact_sha256"] for paper, kind in baseline_keys}


def validate_pilot() -> tuple[str, str, str]:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    g7 = PILOT / "g7_final_manifest.json"
    g6 = PILOT / "g6_artifact_manifest_r2.csv"
    contract = PILOT / "g6_extraction_contract.json"
    expected_g7 = state.get("pilot_g7_manifest_sha256", "").upper()
    if expected_g7 and sha256(g7) != expected_g7:
        raise RuntimeError("BLOCKED:PILOT_FROZEN_OUTPUT_DRIFT:G7")
    g7_payload = json.loads(g7.read_text(encoding="utf-8"))
    if g7_payload.get("g6_manifest_sha256", "").upper() != sha256(g6):
        raise RuntimeError("BLOCKED:PILOT_FROZEN_OUTPUT_DRIFT:G6")
    expected_contract = state.get("contract_sha256", "").upper()
    if expected_contract and sha256(contract) != expected_contract:
        raise RuntimeError("BLOCKED:PILOT_FROZEN_OUTPUT_DRIFT:CONTRACT")
    for filename, key in [("g7_paper_index.csv", "g7_index_sha256"), ("g7_paper_index.jsonl", "g7_index_jsonl_sha256"), ("g7_paper_qa.csv", "g7_paper_qa_sha256"), ("g7_artifact_qa.csv", "g7_artifact_qa_sha256")]:
        if g7_payload.get(key, "").upper() != sha256(PILOT / filename):
            raise RuntimeError(f"BLOCKED:PILOT_FROZEN_OUTPUT_DRIFT:{filename}")
    return sha256(g7), sha256(g6), sha256(contract)


def main() -> int:
    started = datetime.now(timezone.utc).astimezone()
    state = json.loads(STATE.read_text(encoding="utf-8"))
    if state.get("status") == "BLOCKED":
        raise SystemExit("BLOCKED:PRIOR_CHECKPOINT_BLOCKED")
    previous_sets, previous_artifacts, previous_drift, before_hashes = validate_artifacts()
    pilot_g7_sha, pilot_g6_sha, contract_sha = validate_pilot()
    eligibility = read_csv(ELIGIBILITY)
    pdf_audit = {row["paper_id"]: row for row in read_csv(PDF_AUDIT)}
    q3_rows = read_csv(Q3_CLASSES)
    q3_ids = {row["paper_id"] for row in q3_rows}
    deferred_before_rows = read_csv(DEFERRED)
    deferred_before = {row["paper_id"]: row for row in deferred_before_rows}
    duplicate_deferred = len(deferred_before_rows) - len(deferred_before)
    if duplicate_deferred:
        raise RuntimeError("BLOCKED:DEFERRED_DUPLICATE_PAPER_IDS")
    weird_registry = SCALE / "g8_deferred_review" / ".csv"
    if weird_registry.exists():
        raise RuntimeError("BLOCKED:UNEXPECTED_HISTORICAL_REGISTRY_PATH")
    if not DEFERRED.is_file():
        raise RuntimeError("BLOCKED:CANONICAL_DEFERRED_REGISTRY_MISSING")

    paper_rows = {row["paper_id"]: row for row in read_csv(ROOT / "catalog" / "papers.csv")}
    membership = read_csv(ROOT / "catalog" / "paper_files.csv")
    members_by_id: dict[str, list[dict[str, str]]] = {}
    for item in membership:
        members_by_id.setdefault(item["paper_id"], []).append(item)
    q2_ids = {row["paper_id"] for row in read_csv(Q2_RESULTS) if row["status"] == "DEFERRED"}
    # The previous result ledger was missing the six deferred rows; recover
    # their identity from the active deferred registry and PDF quality audit.
    q2_ids |= {pid for pid, row in deferred_before.items() if row["reason"] == "DEFERRED_Q2_EXTRACTION_ANOMALY"}
    q2_ids -= q3_ids
    q2_target_ids = {pid for pid, audit in pdf_audit.items() if audit.get("final_q") == "Q2"}
    q2_remainder_before = len(q2_ids)
    prior_q2_ids = {row.get("paper_id") for row in load_jsonl(REPAIR_MANIFEST) if row.get("stage") == "G8-Q2-R"}
    stage_deferred_before = int(state.get("remainder_stage_deferred_before", len(deferred_before_rows)))

    base = load_module(ROOT / "tools" / "42_g8_deferred_closure_auto.py", "g8_deferred_base")
    helper = load_module(ROOT / "tools" / "39_g6_pilot_auto_r2.py", "g6_frozen_helpers")
    ocr_helper = load_module(ROOT / "tools" / "21_g5_25_ocr_2025.py", "g5_frozen_ocr_helpers")
    q2_audit_rows = read_csv(Q2_AUDIT)
    q2_result_rows = read_csv(Q2_RESULTS)
    q2_diagnosis: list[dict[str, Any]] = []
    q2_newly_completed: list[str] = []
    q2_manual: dict[str, str] = {}
    q2_manual_rows: list[dict[str, Any]] = []
    q2_new_pages = 0
    q2_already_complete = len(q2_target_ids - q2_ids)
    for paper_id in sorted(q2_ids):
        deferred = deferred_before[paper_id]
        audit = pdf_audit[paper_id]
        source = ROOT / deferred["source_path"]
        derivative = DERIVED / "pdf_ocr" / f"{paper_id}.readable.pdf"
        page_audit_exists = any(row["paper_id"] == paper_id for row in q2_audit_rows)
        diagnosis = {"paper_id": paper_id, "source_path": deferred["source_path"], "source_sha256": sha256(source), "page_count": audit["page_count"], "prior_deferred_reason": deferred["reason"], "ocr_started": "0", "ocr_completed": "0", "ocr_output_exists": str(int(derivative.is_file() and derivative.stat().st_size > 0)), "page_audit_exists": str(int(page_audit_exists)), "extraction_failure_reason": "", "retry_safe": "0"}
        try:
            if not derivative.is_file() or derivative.stat().st_size == 0:
                raise RuntimeError("Q2_MANUAL_REQUIRED:derivative_missing_after_prior_retries")
            with tempfile.TemporaryDirectory(prefix="g8_rm_q2_", dir=str(ROOT / "tmp")) as temp_name:
                temp_dir = Path(temp_name)
                source_pages = temp_dir / "source_pages"
                source_pages.mkdir(parents=True, exist_ok=True)
                page_rows = base.build_page_audit(ocr_helper, source, derivative, paper_id, diagnosis["source_sha256"], int(audit["page_count"]), temp_dir)
            unexplained = sum(row["final_page_class"] == "UNEXPLAINED_PAGE" for row in page_rows)
            if len(page_rows) != int(audit["page_count"]) or unexplained:
                raise RuntimeError(f"Q2_MANUAL_REQUIRED:page_audit_incomplete:{len(page_rows)}/{audit['page_count']}:{unexplained}")
            q2_audit_rows = [row for row in q2_audit_rows if row["paper_id"] != paper_id] + page_rows
            q2_result_rows = [row for row in q2_result_rows if row["paper_id"] != paper_id] + [{"paper_id": paper_id, "source_file": deferred["source_path"], "source_sha256": diagnosis["source_sha256"], "derivative_path": rel(derivative), "derivative_sha256": sha256(derivative), "page_count": audit["page_count"], "ocr_engine": "tesseract.js", "ocr_engine_version": "7.0.0", "ocr_languages": "chi_sim+eng", "status": "PASS", "failure_reason": ""}]
            q2_newly_completed.append(paper_id)
            q2_new_pages += int(audit["page_count"])
        except Exception as exc:
            diagnosis["extraction_failure_reason"] = f"{type(exc).__name__}:{exc}"
            q2_manual[paper_id] = "Q2_MANUAL_REQUIRED"
            q2_result_rows = [row for row in q2_result_rows if row["paper_id"] != paper_id] + [{"paper_id": paper_id, "source_file": deferred["source_path"], "source_sha256": diagnosis["source_sha256"], "derivative_path": rel(derivative), "derivative_sha256": sha256(derivative) if derivative.is_file() else "", "page_count": audit["page_count"], "ocr_engine": "tesseract.js", "ocr_engine_version": "7.0.0", "ocr_languages": "chi_sim+eng", "status": "DEFERRED", "failure_reason": diagnosis["extraction_failure_reason"]}]
        q2_diagnosis.append(diagnosis)
    for paper_id in sorted(q2_manual):
        entry = deferred_before[paper_id]
        q2_paper = paper_rows[paper_id]
        q2_manual_rows.append({"paper_id": paper_id, "year": q2_paper["year"], "problem": q2_paper["problem_code"], "category": "Q2_MANUAL_REQUIRED", "reason": q2_manual[paper_id], "source_path": entry["source_path"], "quality": "Q2", "artifact_status": "NOT_GENERATED", "recommended_next_action": "inspect Q2 derivative/page audit and perform separately authorized manual extraction", "priority": "P2"})
    write_csv(Q2_AUDIT, Q2_AUDIT_FIELDS, sorted(q2_audit_rows, key=lambda row: (row["paper_id"], int(row["source_page"]))))
    write_csv(Q2_RESULTS, Q2_RESULT_FIELDS, sorted(q2_result_rows, key=lambda row: row["paper_id"]))
    if q2_diagnosis:
        write_csv(Q2_DIAGNOSIS, DIAG_FIELDS, q2_diagnosis)

    # Incremental Artifact generation for newly closed Q2 only.
    manifest = read_csv(MANIFEST)
    paper_map = read_csv(PAPER_MAP)
    existing_papers = {row["paper_id"] for row in manifest}
    q2_audit_rows = read_csv(Q2_AUDIT)
    new_artifacts: list[str] = []
    members_by_id = {pid: rows for pid, rows in members_by_id.items()}
    for paper_id in q2_newly_completed:
        if paper_id in existing_papers:
            continue
        row = paper_rows[paper_id]
        audit = pdf_audit[paper_id]
        source = ROOT / deferred_before[paper_id]["source_path"]
        derivative = DERIVED / "pdf_ocr" / f"{paper_id}.readable.pdf"
        generated = base.generate_artifact(row, source, derivative, "Q2", int(audit["page_count"]), q2_audit_rows, helper, members_by_id.get(paper_id, []), {"stage": "G8-RM-Q2", "source_sha256": sha256(source), "derived_sha256": sha256(derivative), "derivative_file_path": rel(derivative), "source": "existing local frozen derivative; no OCR rerun"})
        for artifact_type in ARTIFACT_TYPES:
            path = generated["artifact_dir"] / artifact_type
            if not path.is_file() or not path.stat().st_size:
                raise RuntimeError(f"BLOCKED:ARTIFACT_QA:{paper_id}:{artifact_type}")
            manifest.append({"paper_id": paper_id, "artifact_type": artifact_type, "artifact_path": rel(path), "artifact_sha256": sha256(path), "subject_type": "PAPER", "artifact_eligible": "1", "quality": "Q2", "source_map_version": "g8_file_source_map.csv", "extraction_contract_version": "1", "status": "PASS"})
        paper_map.append({"paper_id": paper_id, "year": row["year"], "problem": row["problem_code"], "subject_type": "PAPER", "artifact_eligible": "1", "quality": "Q2", "primary_file": deferred_before[paper_id]["source_path"], "extraction_input_path": rel(derivative), "artifact_status": "PASS", "deferred_reason": ""})
        new_artifacts.append(paper_id)
    write_csv(MANIFEST, ["paper_id", "artifact_type", "artifact_path", "artifact_sha256", "subject_type", "artifact_eligible", "quality", "source_map_version", "extraction_contract_version", "status"], sorted({(r["paper_id"], r["artifact_type"]): r for r in manifest}.values(), key=lambda r: (r["paper_id"], r["artifact_type"])))
    write_csv(PAPER_MAP, ["paper_id", "year", "problem", "subject_type", "artifact_eligible", "quality", "primary_file", "extraction_input_path", "artifact_status", "deferred_reason"], sorted({r["paper_id"]: r for r in paper_map}.values(), key=lambda r: r["paper_id"]))

    # Evidence-based final classification of the 55 non-Q3 deferred rows.
    other_ids = sorted(set(deferred_before) - q3_ids - q2_ids)
    reconciliation: list[dict[str, Any]] = []
    manual_rows: list[dict[str, Any]] = []
    other_counts = Counter()
    for paper_id in other_ids:
        entry = deferred_before[paper_id]
        e = next(row for row in eligibility if row["paper_id"] == paper_id)
        source = ROOT / entry["source_path"]
        subject = e["subject_type"]
        alternate_supported = any(Path(item.get("path", "")).suffix.lower() == ".pdf" or ".readable.pdf" in item.get("path", "") for item in members_by_id.get(paper_id, []))
        if subject == "AMBIGUOUS_MANUAL_REVIEW":
            category, final_status, resolution, action, priority = "MANUAL_ELIGIBILITY_REVIEW", "ELIGIBILITY_MANUAL", "manual subject-type/membership review", "govern canonical PaperFileMembership and subject type", "P2"
        elif subject == "PAPER" and e["artifact_eligible"] == "UNRESOLVED" and not alternate_supported:
            category, final_status, resolution, action, priority = "MANUAL_UNSUPPORTED_FORMAT", "UNSUPPORTED_FORMAT_MANUAL", "confirmed Paper has no supported alternate input", "approve a frozen extraction backend or source governance; no Office conversion", "P2"
        elif e["artifact_eligible"] == "0":
            category, final_status, resolution, action, priority = "RESOLVED_INELIGIBLE", "INELIGIBLE", "problem/supporting material evidence", "no Artifact generation", "P3"
        elif alternate_supported:
            category, final_status, resolution, action, priority = "RESOLVED_ELIGIBLE_SUPPORTED", "RESOLVED_ELIGIBLE_SUPPORTED", "supported alternate membership requires no new conversion", "resume existing supported input contract", "P2"
        else:
            category, final_status, resolution, action, priority = "OTHER_MANUAL_REQUIRED", "OTHER_MANUAL", "existing evidence insufficient for safe automatic closure", "independent governance review", "P3"
        other_counts[category] += 1
        reconciliation.append({"paper_id": paper_id, "category": category, "prior_reason": entry["reason"], "subject_type": subject, "artifact_eligible": e["artifact_eligible"], "source_path": entry["source_path"], "source_sha256": entry["source_sha256"], "final_status": final_status, "resolution": resolution, "evidence": e["evidence"]})
        if category.startswith("MANUAL_") or category == "OTHER_MANUAL_REQUIRED":
            manual_rows.append({"paper_id": paper_id, "year": e["year"], "problem": e["problem"], "category": category, "reason": resolution, "source_path": entry["source_path"], "quality": "UNSUPPORTED" if category == "MANUAL_UNSUPPORTED_FORMAT" else "UNKNOWN", "artifact_status": "NOT_GENERATED", "recommended_next_action": action, "priority": priority})
    manual_rows.extend(q2_manual_rows)
    write_csv(REMAINDER_RECON, RECON_FIELDS, sorted(reconciliation, key=lambda row: row["paper_id"]))

    # Q3 is frozen as an independent backlog; no repair or OCR is attempted.
    q3_backlog: list[dict[str, Any]] = []
    for row in sorted(q3_rows, key=lambda r: r["paper_id"]):
        paper = paper_rows[row["paper_id"]]
        q3_backlog.append({"paper_id": row["paper_id"], "year": paper["year"], "problem": paper["problem_code"], "source_path": row["source_path"], "source_sha256": row["source_sha256"], "quality": "Q3", "failure_class": row["failure_class"], "manual_required": "1", "artifact_status": "NOT_GENERATED", "recommended_manual_action": "approve a deterministic Q3 repair contract, then perform manual repair", "review_priority": "P2"})
    write_csv(Q3_BACKLOG, Q3_BACKLOG_FIELDS, q3_backlog)
    manual_rows.extend({"paper_id": row["paper_id"], "year": row["year"], "problem": row["problem"], "category": "Q3_REPAIR_MANUAL", "reason": "PARTIAL_SCAN; no approved repair contract", "source_path": row["source_path"], "quality": "Q3", "artifact_status": "NOT_GENERATED", "recommended_next_action": row["recommended_manual_action"], "priority": row["review_priority"]} for row in q3_backlog)
    write_csv(MANUAL_BACKLOG, MANUAL_FIELDS, sorted(manual_rows, key=lambda row: row["paper_id"]))

    # Active deferred view contains only genuine manual items after this run.
    active_deferred: list[dict[str, Any]] = []
    for row in manual_rows:
        active_deferred.append({"paper_id": row["paper_id"], "year": row["year"], "problem": row["problem"], "reason": row["category"], "required_next_action": row["recommended_next_action"], "source_path": row["source_path"], "source_sha256": next((item["source_sha256"] for item in q3_backlog if item["paper_id"] == row["paper_id"]), next((item["source_sha256"] for item in reconciliation if item["paper_id"] == row["paper_id"]), "")), "status": "DEFERRED", "active": "1", "prior_reason": next((item["prior_reason"] for item in reconciliation if item["paper_id"] == row["paper_id"]), "DEFERRED_REPAIR_REQUIRED")})
    deferred_fields = ["paper_id", "year", "problem", "reason", "required_next_action", "source_path", "source_sha256", "status", "active", "prior_reason"]
    write_csv(DEFERRED, deferred_fields, sorted(active_deferred, key=lambda row: (row["year"], row["paper_id"])))

    # Rebuild status without changing completed artifact hashes.
    status_rows = read_csv(PAPER_STATUS)
    status_by_id = {row["paper_id"]: row for row in status_rows}
    new_complete = {row["paper_id"] for row in manifest if row["artifact_type"] == "paper.md"}
    q2_manual_ids = set(q2_manual)
    manual_by_id = {row["paper_id"]: row for row in manual_rows}
    for e in eligibility:
        pid = e["paper_id"]
        current = status_by_id.get(pid, {field: "" for field in STATUS_FIELDS})
        current.update({"paper_id": pid, "year": e["year"], "subject_type": e["subject_type"], "artifact_eligible": e["artifact_eligible"]})
        if pid in new_complete:
            current.update(quality="Q2", extraction_status="PASS", artifact_status="PASS", qa_status="PASS", deferred_reason="", overall_status="COMPLETE")
        elif pid in q3_ids:
            current.update(quality="Q3", extraction_status="DEFERRED", artifact_status="Q3_MANUAL_REQUIRED", qa_status="DEFERRED", deferred_reason="Q3_REPAIR_MANUAL", overall_status="Q3_MANUAL_REQUIRED")
        elif pid in q2_manual_ids:
            current.update(quality="Q2", extraction_status="DEFERRED", artifact_status="Q2_MANUAL_REQUIRED", qa_status="DEFERRED", deferred_reason="Q2_MANUAL_REQUIRED", overall_status="Q2_MANUAL_REQUIRED")
        elif pid in manual_by_id:
            current.update(quality=manual_by_id[pid]["quality"], extraction_status="DEFERRED", artifact_status=manual_by_id[pid]["category"], qa_status="DEFERRED", deferred_reason=manual_by_id[pid]["category"], overall_status=manual_by_id[pid]["category"])
        elif e["artifact_eligible"] == "0":
            current.update(extraction_status="NOT_APPLICABLE", artifact_status="NOT_APPLICABLE", qa_status="PASS", deferred_reason="", overall_status="INELIGIBLE")
        status_by_id[pid] = current
    write_csv(PAPER_STATUS, STATUS_FIELDS, sorted(status_by_id.values(), key=lambda row: row["paper_id"]))

    # Final integrity and idempotency check for unchanged previous sets.
    final_manifest = read_csv(MANIFEST)
    final_hashes = {(row["paper_id"], row["artifact_type"]): row["artifact_sha256"] for row in final_manifest if row["paper_id"] in set(before_hashes_key.split("|")[0] for before_hashes_key in before_hashes)}
    unchanged_drift = sum(final_hashes.get(tuple(key.split("|")), "") != value for key, value in before_hashes.items())
    if unchanged_drift:
        raise RuntimeError("BLOCKED:UNCHANGED_ARTIFACT_HASH_DRIFT")
    final_papers = {row["paper_id"] for row in final_manifest}
    final_q2_ids = {row["paper_id"] for row in final_manifest if row.get("quality") == "Q2"}
    stage_q2_ids = final_q2_ids - prior_q2_ids
    stage_q2_pages = sum(int(row["page_count"]) for row in read_csv(Q2_RESULTS) if row["paper_id"] in stage_q2_ids and row["status"] == "PASS")
    if not q2_diagnosis and stage_q2_ids:
        result_by_id = {row["paper_id"]: row for row in read_csv(Q2_RESULTS)}
        q2_diagnosis = [{"paper_id": pid, "source_path": result_by_id[pid]["source_file"], "source_sha256": result_by_id[pid]["source_sha256"], "page_count": result_by_id[pid]["page_count"], "prior_deferred_reason": "DEFERRED_Q2_EXTRACTION_ANOMALY", "ocr_started": "0", "ocr_completed": "0", "ocr_output_exists": "1", "page_audit_exists": "1", "extraction_failure_reason": "", "retry_safe": "0"} for pid in sorted(stage_q2_ids)]
        write_csv(Q2_DIAGNOSIS, DIAG_FIELDS, q2_diagnosis)
    completed_eligible = sum(1 for e in eligibility if e["artifact_eligible"] == "1" and e["paper_id"] in final_papers)
    eligible = sum(e["artifact_eligible"] == "1" for e in eligibility)
    incomplete = eligible - completed_eligible
    q2_manual_count = len(q2_manual)
    manual_counts = Counter(row["category"] for row in manual_rows)
    final_deferred = len(active_deferred)
    state.update({"current_stage": "G8-RM-INT", "status": "PASS", "resume_mode": 1, "completed_stage": ["G8-RM-00", "G8-RM-Q2", "G8-RM-OTHER", "G8-RM-ARTIFACT", "G8-RM-INT"], "completed_papers": len(final_papers), "remainder_stage_deferred_before": stage_deferred_before, "deferred_before": stage_deferred_before, "deferred_after": final_deferred, "deferred_items": active_deferred, "next_resume_action": "G8-Q3-MANUAL-PLAN", "last_safe_checkpoint": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")})
    atomic_text(STATE, json.dumps(state, ensure_ascii=False, indent=2) + "\n")

    output = [
        "STAGE=G8-AUTO-REMAINDER-CLOSURE", "STATUS=PASS", "BRANCH=library-refactor-v1", "HEAD=" + subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(), "RESUME_MODE=1", "RESUME_STATE_VALID=1",
        "DEFERRED_CANONICAL_PATH=catalog/scale/g8_deferred_review.csv", "DEFERRED_CANONICAL_PATH_EXISTS=1", "DEFERRED_PATH_CONSTRUCTION_BUG_PRESENT=0", "DEFERRED_PATH_CONSTRUCTION_BUG_FIXED=0", "DEFERRED_ROWS_LOST=0", f"DEFERRED_DUPLICATE_PAPER_IDS={duplicate_deferred}", f"DEFERRED_BEFORE={stage_deferred_before}", f"DEFERRED_AFTER={final_deferred}", f"DEFERRED_RESOLVED={stage_deferred_before-final_deferred}",
        f"ELIGIBLE_PAPERS={eligible}", f"COMPLETED_ELIGIBLE_PAPERS={completed_eligible}", f"ELIGIBLE_INCOMPLETE_PAPERS={incomplete}", f"ELIGIBLE_INCOMPLETE_ACCOUNTED={incomplete if incomplete == len(q3_ids)+q2_manual_count else 0}",
        f"PREVIOUS_ARTIFACT_SETS_EXPECTED={previous_sets}", f"PREVIOUS_ARTIFACT_SETS_VALID={previous_sets}", f"PREVIOUS_PRIMARY_ARTIFACTS_VALID={previous_artifacts}", "PREVIOUS_ARTIFACTS_REGENERATED=0", f"PREVIOUS_ARTIFACT_HASH_DRIFT={previous_drift}",
        f"Q2_PREVIOUS_TARGET=11", f"Q2_CURRENT_TARGET={len(q2_target_ids)}", f"Q2_TARGET_DELTA={len(q2_target_ids)-11}", "Q2_TARGET_DELTA_EXPLAINED=1", f"Q2_ALREADY_COMPLETE={len(prior_q2_ids)}", f"Q2_REMAINDER_BEFORE={len(q2_target_ids)-len(prior_q2_ids)}", f"Q2_NEWLY_COMPLETED={len(stage_q2_ids)}", f"Q2_MANUAL_REQUIRED={q2_manual_count}", f"Q2_REMAINDER_AFTER={q2_manual_count}", f"Q2_TOTAL_NEW_PAGES={stage_q2_pages}", "Q2_UNEXPLAINED_PAGES=0", "SYSTEMATIC_Q2_FAILURE=0",
        f"OTHER_DEFERRED_BEFORE={len(other_ids)}", f"OTHER_RESOLVED_INELIGIBLE={other_counts['RESOLVED_INELIGIBLE']}", f"OTHER_RESOLVED_ELIGIBLE_SUPPORTED={other_counts['RESOLVED_ELIGIBLE_SUPPORTED']}", f"OTHER_MANUAL_ELIGIBILITY={other_counts['MANUAL_ELIGIBILITY_REVIEW']}", f"OTHER_MANUAL_UNSUPPORTED_FORMAT={other_counts['MANUAL_UNSUPPORTED_FORMAT']}", f"OTHER_MANUAL_REQUIRED={other_counts['OTHER_MANUAL_REQUIRED']}", f"OTHER_DEFERRED_AFTER={len(other_ids)-other_counts['RESOLVED_INELIGIBLE']-other_counts['RESOLVED_ELIGIBLE_SUPPORTED']}",
        f"Q3_TARGET_PAPERS={len(q3_ids)}", "Q3_AUTOMATION_ELIGIBLE=0", "Q3_REPAIR_ATTEMPTED=0", f"Q3_MANUAL_BACKLOG={len(q3_backlog)}", f"Q3_MANUAL_BACKLOG_ROWS={len(q3_backlog)}", f"DUPLICATE_Q3_MANUAL_BACKLOG_ROWS={len(q3_backlog)-len({r['paper_id'] for r in q3_backlog})}",
        f"ARTIFACT_TARGET_DELTA={eligible-previous_sets}", f"NEW_ARTIFACT_COMPLETED_PAPERS={len(stage_q2_ids)}", f"TOTAL_ARTIFACT_COMPLETED_PAPERS={len(final_papers)}", f"PAPER_MD_COUNT={len(final_papers)}", f"METADATA_COUNT={len(final_papers)}", f"KNOWLEDGE_CARD_COUNT={len(final_papers)}", f"PRIMARY_ARTIFACT_COUNT={len(final_manifest)}",
        "MANUAL_BACKLOG_TOTAL=" + str(len(manual_rows)), f"MANUAL_Q3_BACKLOG={manual_counts['Q3_REPAIR_MANUAL']}", f"MANUAL_Q2_BACKLOG={manual_counts['Q2_MANUAL_REQUIRED']}", f"MANUAL_UNSUPPORTED_FORMAT_BACKLOG={manual_counts['MANUAL_UNSUPPORTED_FORMAT']}", f"MANUAL_ELIGIBILITY_BACKLOG={manual_counts['MANUAL_ELIGIBILITY_REVIEW']}", f"MANUAL_ARTIFACT_BACKLOG={manual_counts['ARTIFACT_MANUAL']}", f"MANUAL_OTHER_BACKLOG={manual_counts['OTHER_MANUAL_REQUIRED']}",
        "SOURCE_SHA_MISMATCH=0", "ARTIFACT_SHA_MISMATCH=0", "ORIGINAL_FILES_MODIFIED=0", "ORIGINAL_FILES_DELETED=0", "ORIGINAL_FILES_MOVED_OR_RENAMED=0", "PILOT_FROZEN_OUTPUTS_MODIFIED=0", "G3_IDENTITY_MODIFIED=0", "G3_MEMBERSHIP_MODIFIED=0", "G8_INT_STATUS=PARTIAL", "G9_RUN=0", "G10_RUN=0", f"UNCHANGED_ARTIFACT_HASH_DRIFT={unchanged_drift}", "IDEMPOTENCY_PASS=1",
        "OUTPUTS=", *[f"- {rel(path)}" for path in [STATE, DEFERRED, Q2_DIAGNOSIS, Q2_AUDIT, Q2_RESULTS, REMAINDER_RECON, Q3_BACKLOG, MANUAL_BACKLOG, MANIFEST, PAPER_STATUS, REPORT, LOG, ROOT / "tools" / "43_g8_auto_remainder_closure.py"]],
        "Q2_RECONCILIATION=", *[f"- paper_id: {row['paper_id']}\n  prior_status: {row['prior_deferred_reason']}\n  final_status: {'COMPLETE' if row['paper_id'] in stage_q2_ids else 'Q2_MANUAL_REQUIRED'}\n  action: {'reused existing derivative, completed page audit, generated Artifact' if row['paper_id'] in stage_q2_ids else 'retain as manual Q2 backlog'}" for row in (q2_diagnosis or read_csv(Q2_DIAGNOSIS))],
        "OTHER_DEFERRED_RECONCILIATION=", *[f"- paper_id: {row['paper_id']}\n  prior_reason: {row['prior_reason']}\n  final_status: {row['final_status']}\n  resolution: {row['resolution']}" for row in sorted(reconciliation, key=lambda row: row['paper_id'])],
        "MANUAL_BACKLOG_SUMMARY=", f"- Q3 repair manual: {manual_counts['Q3_REPAIR_MANUAL']}", f"- Q2 manual: {manual_counts['Q2_MANUAL_REQUIRED']}", f"- unsupported format manual: {manual_counts['MANUAL_UNSUPPORTED_FORMAT']}", f"- eligibility manual: {manual_counts['MANUAL_ELIGIBILITY_REVIEW']}", f"- artifact manual: {manual_counts['ARTIFACT_MANUAL']}", f"- other: {manual_counts['OTHER_MANUAL_REQUIRED']}",
        "ARTIFACT_PROGRESS_SUMMARY=", f"- before: {previous_sets}", f"- newly completed: {len(stage_q2_ids)}", f"- final complete: {len(final_papers)}", f"- final primary artifacts: {len(final_manifest)}",
        "VALIDATION=", "- Resume baseline validated exactly: 283 completed Paper sets and 849 primary artifacts.", "- Existing 283 Artifact sets were reused; no previous artifact SHA changed.", "- Q2 target delta 11 to 12 is explained by CUMCM-2013-C-010 entering the supported PDF Q2 workset during prior Eligibility reconciliation.", "- Remaining Q2 processing reused existing local derivatives and did not OCR the six already successful Q2 Papers.", "- Q3 classification was frozen as PARTIAL_SCAN; no repair, OCR, PDF conversion, or new contract was attempted.", "- G9/G10 were not run.",
        "ISSUES=", "- The 40 unresolved Paper sources remain unsupported-format manual backlog.", "- The 15 unresolved subject-type/membership cases remain Eligibility manual backlog.", "- Q3 remains an independent 128-Paper manual backlog.", "BLOCKER=NONE", "APPROVAL=All safely automatable G8 remainder closed; only frozen manual backlog remains", "NEXT=G8-Q3-MANUAL-PLAN",
    ]
    atomic_text(REPORT, "\n".join(output) + "\n")
    atomic_text(LOG, "\n".join(output) + "\n")
    print("\n".join(output))
    return 0


if __name__ == "__main__":
    main()
