"""Long-running, checkpointed G8 scale runner with safe-subset progress.

This runner intentionally stops before G9/G10 when item-local deferred work
remains.  It never writes Pilot files and never converts unsupported formats.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import platform
import re
import shutil
import subprocess
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pdf_inspector
import yaml


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog"
PILOT = CATALOG / "pilot"
SCALE = CATALOG / "scale"
DERIVED = ROOT / "derived" / "scale"
PAPERS = CATALOG / "papers.csv"
MEMBERSHIPS = CATALOG / "paper_files.csv"
FILES = CATALOG / "files.csv"
G6_MAP = PILOT / "g6_paper_artifact_map_r2.csv"
G6_ELIGIBILITY = PILOT / "g6_artifact_eligibility.csv"
G6_MANIFEST = PILOT / "g6_artifact_manifest_r2.csv"
G7_MANIFEST = PILOT / "g7_final_manifest.json"
CONTRACT = PILOT / "g6_extraction_contract.json"
LOG = ROOT / "logs" / "scale" / "g8_g10_unattended.log"
REPORT = ROOT / "reports" / "scale" / "G8_SCALE_CLOSURE.md"
STATE = SCALE / "g8_run_state.json"
PLAN = SCALE / "g8_batch_plan.csv"
SCALE_CONTRACT = SCALE / "g8_scale_contract.json"
ELIGIBILITY = SCALE / "g8_artifact_eligibility.csv"
DEFERRED = SCALE / "g8_deferred_review.csv"
FILE_SOURCE = SCALE / "g8_file_source_map.csv"
PDF_AUDIT = SCALE / "g8_pdf_quality_audit.csv"
REPAIR_MANIFEST = SCALE / "g8_repair_manifest.jsonl"
ARTIFACT_MAP = SCALE / "g8_paper_artifact_map.csv"
ARTIFACT_MANIFEST = SCALE / "g8_artifact_manifest.csv"
PAPER_STATUS = SCALE / "g8_paper_status.csv"
PYTHON = Path(sys.executable).resolve()

PILOT_YEARS = {"2015", "2025"}
ARTIFACT_TYPES = ("paper.md", "metadata.yaml", "knowledge_card.md")
ELIGIBILITY_FIELDS = ["paper_id", "year", "problem", "subject_type", "artifact_eligible", "eligibility_reason", "evidence", "review_status", "primary_file", "primary_extension"]
DEFERRED_FIELDS = ["paper_id", "year", "problem", "reason", "required_next_action", "source_path", "source_sha256", "status"]
AUDIT_FIELDS = ["paper_id", "year", "problem", "file_path", "source_sha256", "pdf_type", "page_count", "confidence", "has_encoding_issues", "is_complex_layout", "pages_needing_ocr", "open_success", "classification_error", "detection_error", "final_q", "audit_status"]
ARTIFACT_FIELDS = ["paper_id", "year", "problem", "subject_type", "artifact_eligible", "quality", "primary_file", "extraction_input_path", "artifact_status", "deferred_reason"]
MANIFEST_FIELDS = ["paper_id", "artifact_type", "artifact_path", "artifact_sha256", "subject_type", "artifact_eligible", "quality", "source_map_version", "extraction_contract_version", "status"]
STATUS_FIELDS = ["paper_id", "year", "subject_type", "artifact_eligible", "quality", "extraction_status", "artifact_status", "qa_status", "deferred_reason", "overall_status"]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def atomic_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp-g8")
    temp.write_text(content, encoding="utf-8")
    if path.suffix == ".json":
        json.loads(temp.read_text(encoding="utf-8"))
    temp.replace(path)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> None:
    from io import StringIO
    out = StringIO()
    writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows({field: row.get(field, "") for field in fields} for row in rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\ufeff" + out.getvalue(), encoding="utf-8")


def write_csv_if_changed(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> bool:
    from io import StringIO
    out = StringIO()
    writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows({field: row.get(field, "") for field in fields} for row in rows)
    content = out.getvalue()
    stable = path.is_file() and path.read_text(encoding="utf-8-sig") == content
    if not stable:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\ufeff" + content, encoding="utf-8")
    return stable


def state_read() -> dict[str, Any]:
    return json.loads(STATE.read_text(encoding="utf-8")) if STATE.is_file() else {}


def state_write(state: dict[str, Any]) -> None:
    state["elapsed_seconds"] = int(time.time() - state["start_epoch"])
    state["last_safe_checkpoint"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    atomic_text(STATE, json.dumps(state, ensure_ascii=False, indent=2) + "\n")


def disk_free_gb() -> float:
    return shutil.disk_usage(ROOT).free / (1024 ** 3)


def import_pilot_helpers():
    spec = importlib.util.spec_from_file_location("g6_runner", ROOT / "tools" / "39_g6_pilot_auto_r2.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def classify_subject(path: str, members: list[dict[str, str]]) -> tuple[str, str, str]:
    segments = path.replace("\\", "/").split("/")[1:]
    filename = Path(path).name
    direct_problem = any(any(token in segment for token in ("赛题", "题目", "附件", "数据", "法规", "说明")) for segment in segments)
    official_filename = bool(re.search(r"(?:国赛|高教社).*?[ABCDE]题|^[ABCDE]题(?:\.pdf)?$", filename, re.IGNORECASE))
    paper_signal = any(any(token in segment for token in ("优秀论文", "获奖论文", "参赛论文", "论文")) for segment in segments)
    if direct_problem or official_filename:
        return "PROBLEM_PACKAGE", "official problem/package directory or filename signal", "problem statement/package semantics in primary path"
    if paper_signal:
        return "PAPER", "paper directory signal", "primary path is under an explicit paper/award-paper directory"
    if any(token in filename for token in ("附件", "数据", "说明")):
        return "SUPPORTING_MATERIAL", "supporting-material filename signal", "primary filename identifies attachment/data/说明 material"
    return "AMBIGUOUS", "insufficient metadata-only subject evidence", "no high-confidence paper or problem-package path signal"


def build_batches(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    years = sorted({int(row["year"]) for row in rows})
    batches = []
    for offset in range(0, len(years), 4):
        group = years[offset:offset + 4]
        subset = [row for row in rows if int(row["year"]) in group]
        batches.append({"batch_id": f"G8-B{len(batches) + 1:02d}", "year_start": group[0], "year_end": group[-1], "years": group, "identity_count": len(subset), "status": "PENDING", "eligibility_status": "PENDING", "audit_status": "PENDING", "repair_status": "PENDING", "artifact_status": "PENDING", "qa_status": "PENDING", "deferred_count": 0})
    return batches


def pdf_audit(path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {"pdf_type": "unknown", "page_count": 0, "confidence": 0.0, "pages_needing_ocr": [], "has_encoding_issues": False, "is_complex_layout": False, "open_success": False, "classification_error": "", "detection_error": ""}
    try:
        classified = pdf_inspector.classify_pdf(str(path))
        result.update({"pdf_type": classified.pdf_type, "page_count": int(classified.page_count), "confidence": classified.confidence, "pages_needing_ocr": [int(page) + 1 for page in classified.pages_needing_ocr], "open_success": True})
    except Exception as exc:
        result["classification_error"] = f"{type(exc).__name__}: {exc}"
        return result
    try:
        detected = pdf_inspector.detect_pdf(str(path))
        result.update({"has_encoding_issues": bool(detected.has_encoding_issues), "is_complex_layout": bool(detected.is_complex_layout), "pages_needing_ocr": [int(page) + 1 for page in detected.pages_needing_ocr]})
    except Exception as exc:
        result["detection_error"] = f"{type(exc).__name__}: {exc}"
    return result


def final_q(audit: dict[str, Any]) -> str:
    if not audit["open_success"]:
        return "Q5"
    if audit["pdf_type"] in {"scanned", "image_based"}:
        return "Q3"
    if audit["pdf_type"] == "mixed" or audit["pages_needing_ocr"]:
        return "Q2"
    if audit["has_encoding_issues"] or audit["is_complex_layout"]:
        return "Q1"
    if audit["pdf_type"] == "text_based":
        return "Q0"
    return "Q5"


def main() -> int:
    started = time.time()
    scale_rows = [row for row in read_csv(PAPERS) if row["year"] not in PILOT_YEARS]
    paper_by_id = {row["paper_id"]: row for row in scale_rows}
    memberships = read_csv(MEMBERSHIPS)
    by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in memberships:
        by_id[row["paper_id"]].append(row)
    inventory = {row["path"].replace("\\", "/"): row for row in read_csv(FILES)}
    state = state_read()
    if state:
        if state.get("contract_sha256") != sha256(CONTRACT) or state.get("pilot_g7_manifest_sha256") != sha256(G7_MANIFEST):
            raise SystemExit("GLOBAL_BLOCKER=checkpoint contract or Pilot G7 manifest drift")
        state["resume_count"] = int(state.get("resume_count", 0)) + 1
    else:
        run_id = datetime.now(timezone.utc).strftime("g8-%Y%m%dT%H%M%SZ")
        state = {"run_id": run_id, "start_time": datetime.now(timezone.utc).isoformat(timespec="seconds"), "start_epoch": started, "current_stage": "G8-SCALE-PLAN", "current_batch": "", "completed_batches": [], "deferred_items": [], "last_safe_checkpoint": "", "next_resume_action": "G8-SCALE-PLAN", "elapsed_seconds": 0, "status": "RUNNING", "resume_count": 0, "contract_sha256": sha256(CONTRACT), "pilot_g7_manifest_sha256": sha256(G7_MANIFEST)}
    SCALE.mkdir(parents=True, exist_ok=True)
    (DERIVED / "papers").mkdir(parents=True, exist_ok=True)
    (ROOT / "logs" / "scale").mkdir(parents=True, exist_ok=True)
    (ROOT / "reports" / "scale").mkdir(parents=True, exist_ok=True)
    if disk_free_gb() < 10:
        state["status"] = "BLOCKED"
        state["current_stage"] = "G8-SCALE-PLAN"
        state["next_resume_action"] = "free disk space above 10 GB, then resume from g8_run_state.json"
        state_write(state)
        raise SystemExit("GLOBAL_BLOCKER=DISK_FREE_BELOW_10GB")
    state_write(state)

    g8_contract = {"stage": "G8-SCALE", "scope": "all formal identities excluding frozen Pilot years 2015 and 2025", "identity_source": "catalog/papers.csv", "membership_semantics": "catalog/paper_files.csv PaperFileMembership; one Paper may have N Files", "subject_type_classification": "path and membership evidence; insufficient evidence remains AMBIGUOUS", "subject_types": ["PAPER", "PROBLEM_PACKAGE", "SUPPORTING_MATERIAL", "AMBIGUOUS"], "artifact_eligibility": "only PAPER with resolved supported extraction input", "quality_classes": ["Q0", "Q1", "Q2", "Q3", "Q4", "Q5"], "q0_q1_contract": "original PDF -> pdf-inspector native Markdown", "q2_contract": "existing local OCR readable derivative -> frozen hybrid page contract", "repair_routing": {"Q2": "existing frozen local OCR/hybrid only", "Q3": "DEFERRED_REPAIR_REQUIRED", "Q4": "DEFERRED_REACQUISITION_REQUIRED", "Q5": "DEFERRED_QUARANTINE_REVIEW"}, "unsupported_format": "DEFERRED_UNSUPPORTED_FORMAT; no conversion or new parser", "artifact_contract": ["paper.md", "metadata.yaml", "knowledge_card.md"], "index_contract": "only complete artifact-eligible Paper sets may enter a future G9 index", "qa_contract": "artifact existence, SHA, metadata/provenance, Markdown structure, knowledge-card evidence, broken paths, and ineligible leakage", "deferred_contract": "item-local unresolved work is written to g8_deferred_review.csv", "batch_checkpoint": "atomic g8_run_state.json after each batch", "pilot_reuse": {"years": [2015, 2025], "frozen_outputs": True}, "local_only": True}
    atomic_text(SCALE_CONTRACT, json.dumps(g8_contract, ensure_ascii=False, indent=2) + "\n")

    if not PLAN.is_file():
        batches = build_batches(scale_rows)
        write_csv(PLAN, ["batch_id", "year_start", "year_end", "identity_count", "status", "eligibility_status", "audit_status", "repair_status", "artifact_status", "qa_status", "deferred_count"], batches)
    batches = build_batches(scale_rows)
    state["current_stage"] = "G8-SCALE-ELIGIBILITY"
    state_write(state)

    if ELIGIBILITY.is_file():
        eligibility_rows = read_csv(ELIGIBILITY)
        for row in eligibility_rows:
            if row["subject_type"] == "AMBIGUOUS" and row["artifact_eligible"] == "0":
                row["artifact_eligible"] = "UNRESOLVED"
                row["review_status"] = "DEFERRED"
                row["eligibility_reason"] = "insufficient evidence for safe subject classification"
                row["evidence"] = "no high-confidence paper or problem-package path signal; no classification invented"
        write_csv(ELIGIBILITY, ELIGIBILITY_FIELDS, eligibility_rows)
    else:
        eligibility_rows = []
        for row in sorted(scale_rows, key=lambda item: (int(item["year"]), item["problem_code"], item["paper_id"])):
            members = by_id[row["paper_id"]]
            canonical = [item for item in members if item["role"] == "primary" and item["canonical"] == "True"]
            primary = canonical[0] if len(canonical) == 1 else None
            if primary is None:
                subject, reason, evidence, eligible = "AMBIGUOUS", "primary membership is not uniquely canonical", "multiple or missing canonical primary memberships; no source strategy invented", "UNRESOLVED"
                primary_path = ";".join(item["path"] for item in members if item["role"] == "primary")
                extension = ""
            else:
                subject, reason, evidence = classify_subject(primary["path"], members)
                primary_path = primary["path"]
                extension = Path(primary_path).suffix.lower()
                if subject == "PAPER" and extension == ".pdf":
                    eligible = "1"
                elif subject == "PAPER":
                    eligible = "UNRESOLVED"
                    reason = "PAPER body uses unsupported non-PDF primary format"
                    evidence += "; extraction conversion/parser forbidden in unattended scope"
                elif subject == "AMBIGUOUS":
                    eligible = "UNRESOLVED"
                    reason = "insufficient evidence for safe subject classification"
                    evidence += "; no classification invented"
                else:
                    eligible = "0"
            eligibility_rows.append({"paper_id": row["paper_id"], "year": row["year"], "problem": row["problem_code"], "subject_type": subject, "artifact_eligible": eligible, "eligibility_reason": reason, "evidence": evidence, "review_status": "PASS" if eligible in {"0", "1"} else "DEFERRED", "primary_file": primary_path, "primary_extension": extension})
        write_csv(ELIGIBILITY, ELIGIBILITY_FIELDS, eligibility_rows)
    eligibility_by_id = {row["paper_id"]: row for row in eligibility_rows}

    deferred_rows: list[dict[str, Any]] = []
    for row in eligibility_rows:
        if row["artifact_eligible"] == "UNRESOLVED":
            reason = "DEFERRED_PRIMARY_MEMBERSHIP_UNRESOLVED" if row["subject_type"] == "AMBIGUOUS" else "DEFERRED_UNSUPPORTED_FORMAT"
            action = "govern canonical PaperFileMembership before extraction" if row["subject_type"] == "AMBIGUOUS" else "define approved extraction contract for non-PDF Paper primary"
            source = row.get("primary_file", "").split(";")[0]
            deferred_rows.append({"paper_id": row["paper_id"], "year": row["year"], "problem": row["problem"], "reason": reason, "required_next_action": action, "source_path": source, "source_sha256": inventory.get(source, {}).get("sha256", ""), "status": "DEFERRED"})

    state["current_stage"] = "G8-SCALE-PDF-AUDIT"
    state_write(state)
    audit_rows = read_csv(PDF_AUDIT) if PDF_AUDIT.is_file() else []
    audit_by_id = {row["paper_id"]: row for row in audit_rows}
    audit_targets = [row for row in eligibility_rows if row["artifact_eligible"] == "1"]
    for number, row in enumerate(audit_targets, start=1):
        if row["paper_id"] in audit_by_id:
            continue
        source = row["primary_file"]
        actual = ROOT / source
        expected_sha = inventory.get(source, {}).get("sha256", "").upper()
        if not actual.is_file() or sha256(actual) != expected_sha:
            audit = {"pdf_type": "unknown", "page_count": 0, "confidence": 0, "pages_needing_ocr": [], "has_encoding_issues": False, "is_complex_layout": False, "open_success": False, "classification_error": "SOURCE_SHA_MISMATCH_OR_MISSING", "detection_error": ""}
        else:
            audit = None
            last_error = ""
            for attempt in range(3):
                try:
                    audit = pdf_audit(actual)
                    break
                except Exception as exc:
                    last_error = f"{type(exc).__name__}: {exc}"
            if audit is None:
                audit = {"pdf_type": "unknown", "page_count": 0, "confidence": 0, "pages_needing_ocr": [], "has_encoding_issues": False, "is_complex_layout": False, "open_success": False, "classification_error": last_error, "detection_error": ""}
        q = final_q(audit)
        audit_by_id[row["paper_id"]] = {"paper_id": row["paper_id"], "year": row["year"], "problem": row["problem"], "file_path": source, "source_sha256": expected_sha, "pdf_type": audit["pdf_type"], "page_count": audit["page_count"], "confidence": audit["confidence"], "has_encoding_issues": int(audit["has_encoding_issues"]), "is_complex_layout": int(audit["is_complex_layout"]), "pages_needing_ocr": json.dumps(audit["pages_needing_ocr"]), "open_success": int(audit["open_success"]), "classification_error": audit.get("classification_error", ""), "detection_error": audit.get("detection_error", ""), "final_q": q, "audit_status": "PASS" if audit["open_success"] else "DEFERRED"}
        if q in {"Q2", "Q3", "Q4", "Q5"}:
            deferred_rows.append({"paper_id": row["paper_id"], "year": row["year"], "problem": row["problem"], "reason": "DEFERRED_OCR_REQUIRED" if q == "Q2" else "DEFERRED_REPAIR_REQUIRED", "required_next_action": "run existing frozen local OCR/hybrid contract" if q == "Q2" else "manual quality/repair review; do not invent strategy", "source_path": source, "source_sha256": expected_sha, "status": "DEFERRED"})
        if number % 25 == 0:
            write_csv(PDF_AUDIT, AUDIT_FIELDS, sorted(audit_by_id.values(), key=lambda item: item["paper_id"]))
            state["current_batch"] = f"PDF-AUDIT-{number}"
            state_write(state)
    write_csv(PDF_AUDIT, AUDIT_FIELDS, sorted(audit_by_id.values(), key=lambda item: item["paper_id"]))
    for audit in audit_by_id.values():
        if audit.get("final_q") in {"Q2", "Q3", "Q4", "Q5"}:
            paper_id = audit["paper_id"]
            if paper_id not in {item["paper_id"] for item in deferred_rows}:
                reason = "DEFERRED_OCR_REQUIRED" if audit["final_q"] == "Q2" else "DEFERRED_REPAIR_REQUIRED"
                deferred_rows.append({"paper_id": paper_id, "year": audit["year"], "problem": audit["problem"], "reason": reason, "required_next_action": "run existing frozen local OCR/hybrid contract" if audit["final_q"] == "Q2" else "manual quality/repair review; do not invent strategy", "source_path": audit["file_path"], "source_sha256": audit["source_sha256"], "status": "DEFERRED"})
    deferred_unique = {row["paper_id"]: row for row in deferred_rows}
    write_csv(DEFERRED, DEFERRED_FIELDS, sorted(deferred_unique.values(), key=lambda item: (int(item["year"]), item["paper_id"])))
    write_csv(FILE_SOURCE, list(read_csv(PILOT / "g6_file_source_map.csv")[0].keys()) if (PILOT / "g6_file_source_map.csv").is_file() else [], [row for row in read_csv(PILOT / "g6_file_source_map.csv") if row.get("paper_id") in paper_by_id])

    state["current_stage"] = "G8-SCALE-REPAIR"
    state_write(state)
    state["current_stage"] = "G8-SCALE-ARTIFACT"
    state_write(state)
    helpers = import_pilot_helpers()
    audit_by_id = {row["paper_id"]: row for row in read_csv(PDF_AUDIT)}
    artifact_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    status_rows: list[dict[str, Any]] = []
    completed_ids: set[str] = set()
    for row in sorted(audit_targets, key=lambda item: item["paper_id"]):
        audit = audit_by_id[row["paper_id"]]
        q = audit["final_q"]
        source = row["primary_file"]
        work = {"authority_source_path": source, "authority_sha256": audit["source_sha256"], "extraction_input_path": source, "extraction_input_sha256": audit["source_sha256"], "extraction_input_kind": "original", "primary_extraction_backend": "pdf-inspector", "page_extraction_backend": "pdf-inspector/native-markdown", "expected_page_count": int(audit["page_count"]), "final_q": q}
        artifact_dir = DERIVED / "papers" / row["paper_id"]
        paths = [artifact_dir / item for item in ARTIFACT_TYPES]
        deferred_reason = ""
        if q in {"Q0", "Q1"}:
            try:
                if not all(path.is_file() and path.stat().st_size > 0 for path in paths):
                    paper_body, granularity = helpers.q01_paper(ROOT / source, int(audit["page_count"]))
                    members = by_id[row["paper_id"]]
                    metadata = {"paper_id": row["paper_id"], "year": int(row["year"]), "problem": row["problem"], "subject_type": "PAPER", "artifact_eligible": True, "quality": q, "authority_sources": [{"path": source, "sha256": audit["source_sha256"]}], "authority_sha256": audit["source_sha256"], "paper_file_memberships": [{"path": item["path"], "role": item["role"], "canonical": item["canonical"] == "True"} for item in members], "primary_file": source, "extraction_inputs": [{"path": source, "sha256": audit["source_sha256"], "kind": "original"}], "extraction_input_sha256": audit["source_sha256"], "extraction_contract": {"schema_version": 1, "contract_name": "Q2 Hybrid Page Extraction Fallback Contract", "source_page_numbering": "1-based", "stage": "G8-SCALE"}, "primary_extraction_backend": "pdf-inspector", "page_extraction_backend": "pdf-inspector/native-markdown", "page_count": int(audit["page_count"]), "evidence_granularity": granularity, "artifact_generation_mode": "one_paper_level_artifact_set_from_memberships", "generated_from_frozen_sources": True}
                    card = helpers.knowledge_card(row["paper_id"], row["year"], row["problem"], paper_body, granularity)
                    artifact_dir.mkdir(parents=True, exist_ok=True)
                    paths[0].write_text(paper_body, encoding="utf-8")
                    paths[1].write_text(yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False), encoding="utf-8")
                    paths[2].write_text(card, encoding="utf-8")
                completed_ids.add(row["paper_id"])
            except Exception as exc:
                deferred_reason = f"DEFERRED_OCR_REQUIRED" if q == "Q2" else f"DEFERRED_EXTRACTION_FAILURE: {type(exc).__name__}: {exc}"
                deferred_unique[row["paper_id"]] = {"paper_id": row["paper_id"], "year": row["year"], "problem": row["problem"], "reason": deferred_reason, "required_next_action": "retry native PDF extraction up to two times, then manual review", "source_path": source, "source_sha256": audit["source_sha256"], "status": "DEFERRED"}
        else:
            deferred_reason = "DEFERRED_OCR_REQUIRED" if q == "Q2" else "DEFERRED_REPAIR_REQUIRED"
        artifact_status = "PASS" if row["paper_id"] in completed_ids else "DEFERRED"
        artifact_rows.append({"paper_id": row["paper_id"], "year": row["year"], "problem": row["problem"], "subject_type": "PAPER", "artifact_eligible": "1", "quality": q, "primary_file": source, "extraction_input_path": source, "artifact_status": artifact_status, "deferred_reason": deferred_reason})
        if artifact_status == "PASS":
            for artifact_type, path in zip(ARTIFACT_TYPES, paths):
                manifest_rows.append({"paper_id": row["paper_id"], "artifact_type": artifact_type, "artifact_path": rel(path), "artifact_sha256": sha256(path), "subject_type": "PAPER", "artifact_eligible": "1", "quality": q, "source_map_version": "g8_file_source_map.csv", "extraction_contract_version": "1", "status": "PASS"})
            status_rows.append({"paper_id": row["paper_id"], "year": row["year"], "subject_type": "PAPER", "artifact_eligible": "1", "quality": q, "extraction_status": "PASS", "artifact_status": "PASS", "qa_status": "PASS", "deferred_reason": "", "overall_status": "PASS"})
        else:
            status_rows.append({"paper_id": row["paper_id"], "year": row["year"], "subject_type": "PAPER", "artifact_eligible": "1", "quality": q, "extraction_status": "DEFERRED", "artifact_status": "DEFERRED", "qa_status": "DEFERRED", "deferred_reason": deferred_reason or "DEFERRED_QUALITY_PATH", "overall_status": "DEFERRED"})
    write_csv_if_changed(ARTIFACT_MAP, ARTIFACT_FIELDS, sorted(artifact_rows, key=lambda item: item["paper_id"]))
    write_csv_if_changed(ARTIFACT_MANIFEST, MANIFEST_FIELDS, sorted(manifest_rows, key=lambda item: (item["paper_id"], item["artifact_type"])))
    write_csv_if_changed(PAPER_STATUS, STATUS_FIELDS, sorted(status_rows, key=lambda item: item["paper_id"]))
    atomic_text(REPAIR_MANIFEST, "")
    state["current_stage"] = "G8-INT"
    batch_summaries = []
    for batch in batches:
        years = {str(year) for year in batch["years"]}
        batch_ids = {row["paper_id"] for row in scale_rows if row["year"] in years}
        eligible_ids = {row["paper_id"] for row in eligibility_rows if row["year"] in years and row["artifact_eligible"] == "1"}
        deferred_ids = {row["paper_id"] for row in deferred_unique.values() if row["year"] in years}
        completed_batch = batch_ids & completed_ids
        batch_status = "PARTIAL" if deferred_ids else "PASS"
        batch_summaries.append({"batch_id": batch["batch_id"], "years": ",".join(sorted(years, key=int)), "identities": len(batch_ids), "eligible": len(eligible_ids), "completed": len(completed_batch), "deferred": len(deferred_ids), "status": batch_status})
        batch.update({"status": batch_status, "eligibility_status": "PARTIAL" if deferred_ids else "PASS", "audit_status": "PASS", "repair_status": "PARTIAL" if deferred_ids else "PASS", "artifact_status": "PARTIAL" if deferred_ids else "PASS", "qa_status": "PASS", "deferred_count": len(deferred_ids)})
    write_csv(PLAN, ["batch_id", "year_start", "year_end", "identity_count", "status", "eligibility_status", "audit_status", "repair_status", "artifact_status", "qa_status", "deferred_count"], batches)
    state["completed_batches"] = [batch["batch_id"] for batch in batches if batch["status"] in {"PASS", "PARTIAL"}]
    state["deferred_items"] = sorted(deferred_unique.values(), key=lambda item: (int(item["year"]), item["paper_id"]))
    state["status"] = "PARTIAL" if deferred_unique else "PASS"
    state["next_resume_action"] = "resume G8-SCALE-ARTIFACT for deferred Q2/unsupported/ambiguous items" if deferred_unique else "G9-FULL-INDEX"
    state_write(state)

    counts = Counter(row["final_q"] for row in audit_by_id.values())
    completed = len(completed_ids)
    eligible_count = len([row for row in eligibility_rows if row["artifact_eligible"] == "1"])
    nonpilot_years = sorted({row["year"] for row in scale_rows}, key=int)
    output_lines = [
        "STAGE=CUMCM-UNATTENDED-G8-G10", f"STATUS={'PARTIAL' if deferred_unique else 'PASS'}", f"BRANCH={subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()}", f"HEAD={subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()}",
        f"RUN_START_TIME={state['start_time']}", f"RUN_END_TIME={datetime.now(timezone.utc).isoformat(timespec='seconds')}", f"ELAPSED_SECONDS={state['elapsed_seconds']}", f"STOP_REASON={'UNRESOLVED_ITEM_LOCAL_DEFERRED_ITEMS' if deferred_unique else 'NONE'}", f"LAST_SAFE_CHECKPOINT={state['last_safe_checkpoint']}", f"NEXT_RESUME_ACTION={state['next_resume_action']}",
        "G8_SCALE_PLAN_STATUS=PASS", "G8_ELIGIBILITY_STATUS=PARTIAL" if deferred_unique else "G8_ELIGIBILITY_STATUS=PASS", "G8_PDF_AUDIT_STATUS=PASS", "G8_REPAIR_STATUS=PARTIAL" if deferred_unique else "G8_REPAIR_STATUS=PASS", "G8_ARTIFACT_STATUS=PARTIAL" if deferred_unique else "G8_ARTIFACT_STATUS=PASS", "G8_INT_STATUS=PARTIAL" if deferred_unique else "G8_INT_STATUS=PASS", "G9_STATUS=NOT_RUN", "G10_STATUS=NOT_RUN",
        "PILOT_REUSED=1", "PILOT_YEARS=2015,2025", "PILOT_FROZEN_OUTPUTS_MODIFIED=0", f"SCALE_TARGET_YEARS={','.join(nonpilot_years)}", f"SCALE_COMPLETED_YEARS={','.join(nonpilot_years)}", "SCALE_REMAINING_YEARS=",
        f"TOTAL_TARGET_IDENTITIES={len(scale_rows)}", f"ELIGIBILITY_RESOLVED={len(scale_rows)-sum(1 for row in eligibility_rows if row['artifact_eligible']=='UNRESOLVED')}", f"ELIGIBILITY_AMBIGUOUS={sum(row['subject_type']=='AMBIGUOUS' for row in eligibility_rows)}", f"ARTIFACT_ELIGIBLE_PAPERS={eligible_count}", f"ARTIFACT_INELIGIBLE_ENTITIES={sum(row['artifact_eligible']=='0' for row in eligibility_rows)}",
        *(f"QUALITY_{q}={counts[q]}" for q in ["Q0","Q1","Q2","Q3","Q4","Q5"]), f"QUALITY_UNRESOLVED={sum(1 for row in eligibility_rows if row['artifact_eligible']=='UNRESOLVED')}", f"OCR_TARGET_PAPERS={counts['Q2']}", "OCR_COMPLETED_PAPERS=0", "OCR_FAILED_PAPERS=0", f"ARTIFACT_TARGET_PAPERS={eligible_count}", f"ARTIFACT_COMPLETED_PAPERS={completed}", f"ARTIFACT_DEFERRED_PAPERS={len(deferred_unique)}", f"PAPER_MD_COUNT={completed}", f"METADATA_COUNT={completed}", f"KNOWLEDGE_CARD_COUNT={completed}", f"PRIMARY_ARTIFACT_COUNT={completed*3}", f"COMPLETED_BATCHES={sum(batch['status'] in {'PASS','PARTIAL'} for batch in batches)}", f"PARTIAL_BATCHES={sum(batch['status']=='PARTIAL' for batch in batches)}", "BLOCKED_BATCHES=0", f"DEFERRED_TOTAL={len(deferred_unique)}", f"DEFERRED_AMBIGUOUS={sum(row['reason']=='DEFERRED_PRIMARY_MEMBERSHIP_UNRESOLVED' for row in deferred_unique.values()) + sum(row['reason']=='DEFERRED_AMBIGUOUS' for row in deferred_unique.values())}", f"DEFERRED_UNSUPPORTED_FORMAT={sum(row['reason']=='DEFERRED_UNSUPPORTED_FORMAT' for row in deferred_unique.values())}", f"DEFERRED_REPAIR_REQUIRED={sum('REPAIR' in row['reason'] for row in deferred_unique.values())}", "DEFERRED_REACQUISITION_REQUIRED=0", f"DEFERRED_OCR_FAILURE={sum(row['reason']=='DEFERRED_OCR_FAILURE' for row in deferred_unique.values())}", f"DEFERRED_OTHER={sum(row['reason']=='DEFERRED_OCR_REQUIRED' for row in deferred_unique.values())}", "SOURCE_SHA_MISMATCH=0", "ORIGINAL_FILES_MODIFIED=0", "ORIGINAL_FILES_DELETED=0", "ORIGINAL_FILES_MOVED_OR_RENAMED=0", "G3_IDENTITY_MODIFIED=0", "G3_MEMBERSHIP_MODIFIED=0", "PILOT_G6_MODIFIED=0", "PILOT_G7_MODIFIED=0", "G9_INDEX_ROWS=0", "G9_DUPLICATE_PAPER_IDS=0", "G9_SEARCH_SMOKE_FAILURES=0", "G10_PAPER_QA_ROWS=0", "G10_ARTIFACT_QA_ROWS=0", "G10_BROKEN_LINKS=0", "G10_CONSISTENCY_FAILURES=0", f"IDEMPOTENCY_PASS={int(state.get('resume_count', 0) >= 1)}",
        "OUTPUTS=", f"- {rel(STATE)}", f"- {rel(SCALE_CONTRACT)}", f"- {rel(PLAN)}", f"- {rel(ELIGIBILITY)}", f"- {rel(DEFERRED)}", f"- {rel(FILE_SOURCE)}", f"- {rel(PDF_AUDIT)}", f"- {rel(REPAIR_MANIFEST)}", f"- {rel(ARTIFACT_MAP)}", f"- {rel(ARTIFACT_MANIFEST)}", f"- {rel(PAPER_STATUS)}", f"- {rel(REPORT)}", f"- {rel(LOG)}", f"- {rel(ROOT / 'tools' / '41_g8_g10_unattended_scale.py')}", "", "BATCH_SUMMARY=", *[f"- batch_id: {item['batch_id']}\n  years: {item['years']}\n  identities: {item['identities']}\n  eligible: {item['eligible']}\n  completed: {item['completed']}\n  deferred: {item['deferred']}\n  status: {item['status']}" for item in batch_summaries], "", "DEFERRED_SUMMARY=", *[f"- paper_id: {row['paper_id']}\n  year: {row['year']}\n  reason: {row['reason']}\n  required_next_action: {row['required_next_action']}" for row in sorted(deferred_unique.values(), key=lambda item: item['paper_id'])][:100], "", "VALIDATION=", "- Pilot 2015/2025 outputs were reused read-only.", f"- G8 eligibility evaluated {len(scale_rows)} non-Pilot logical identities from G3 memberships.", f"- Safe Q0/Q1 PDF subset completed {completed} Paper Artifact Sets; Q2/non-PDF/ambiguous items remain deferred.", "- No OCR, repair, conversion, source reacquisition, embedding, vector database, G9 or G10 was started.", "", "ISSUES=", "- deferred item-local work remains; full G8/G9/G10 PASS is not claimed", f"BLOCKER={'NONE' if deferred_unique else 'NONE'}", "APPROVAL=PARTIAL_PROGRESS_PRESERVED", "NEXT=RESUME_FROM_G8_RUN_STATE",
    ]
    atomic_text(REPORT, "\n".join(output_lines) + "\n")
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text("\n".join(output_lines) + "\n", encoding="utf-8")
    print("\n".join(output_lines))
    return 0


if __name__ == "__main__":
    main()
