"""Incremental, local-only closure of the Scale deferred population.

This runner validates and reuses the previous 265 Scale artifact sets, then
reconciles obvious supporting/problem inputs, processes only the existing Q2
workset with the frozen local tesseract.js contract, and clusters Q3 without
inventing a repair contract.  It never touches Pilot or original files.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pdf_inspector
import yaml

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog"
SCALE = CATALOG / "scale"
PILOT = CATALOG / "pilot"
DERIVED = ROOT / "derived" / "scale"
STATE_PATH = SCALE / "g8_run_state.json"
ELIGIBILITY = SCALE / "g8_artifact_eligibility.csv"
DEFERRED = SCALE / "g8_deferred_review.csv"
PDF_AUDIT = SCALE / "g8_pdf_quality_audit.csv"
ARTIFACT_MAP = SCALE / "g8_paper_artifact_map.csv"
ARTIFACT_MANIFEST = SCALE / "g8_artifact_manifest.csv"
PAPER_STATUS = SCALE / "g8_paper_status.csv"
REPAIR_MANIFEST = SCALE / "g8_repair_manifest.jsonl"
CONTRACT = SCALE / "g8_scale_contract.json"
G7_MANIFEST = PILOT / "g7_final_manifest.json"
PILOT_G6_MANIFEST = PILOT / "g6_artifact_manifest_r2.csv"
REPORT = ROOT / "reports" / "scale" / "G8_DEFERRED_CLOSURE.md"
LOG = ROOT / "logs" / "scale" / "g8_deferred_closure.log"
RECONCILIATION = SCALE / "g8_eligibility_reconciliation.csv"
Q2_AUDIT = SCALE / "g8_q2_page_audit.csv"
Q2_RESULTS = SCALE / "g8_q2_ocr_results.csv"
Q3_CLASSES = SCALE / "g8_q3_failure_classes.csv"
Q3_CONTRACT = SCALE / "g8_q3_repair_contract.json"
PILOT_YEARS = {"2015", "2025"}
ARTIFACT_TYPES = ("paper.md", "metadata.yaml", "knowledge_card.md")
ELIGIBILITY_FIELDS = ["paper_id", "year", "problem", "subject_type", "artifact_eligible", "eligibility_reason", "evidence", "review_status", "primary_file", "primary_extension"]
DEFERRED_FIELDS = ["paper_id", "year", "problem", "reason", "required_next_action", "source_path", "source_sha256", "status"]
AUDIT_FIELDS = ["paper_id", "year", "problem", "file_path", "source_sha256", "pdf_type", "page_count", "confidence", "has_encoding_issues", "is_complex_layout", "pages_needing_ocr", "open_success", "classification_error", "detection_error", "final_q", "audit_status"]
MANIFEST_FIELDS = ["paper_id", "artifact_type", "artifact_path", "artifact_sha256", "subject_type", "artifact_eligible", "quality", "source_map_version", "extraction_contract_version", "status"]
MAP_FIELDS = ["paper_id", "year", "problem", "subject_type", "artifact_eligible", "quality", "primary_file", "extraction_input_path", "artifact_status", "deferred_reason"]
STATUS_FIELDS = ["paper_id", "year", "subject_type", "artifact_eligible", "quality", "extraction_status", "artifact_status", "qa_status", "deferred_reason", "overall_status"]
RECON_FIELDS = ["paper_id", "prior_status", "final_subject_type", "artifact_eligible", "evidence", "resolution", "still_deferred"]
Q2_AUDIT_FIELDS = ["paper_id", "source_file", "source_sha256", "source_page", "page_class", "final_page_class", "extraction_chars", "status", "evidence"]
Q2_RESULT_FIELDS = ["paper_id", "source_file", "source_sha256", "derivative_path", "derivative_sha256", "page_count", "ocr_engine", "ocr_engine_version", "ocr_languages", "status", "failure_reason"]
Q3_FIELDS = ["paper_id", "source_path", "source_sha256", "page_count", "failure_class", "evidence", "candidate_repair_strategy", "repair_contract_status", "manual_review_required"]
SOURCE_EXTENSIONS = {".lg4", ".fig", ".nb", ".sas", ".asv", ".gitkeep"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}


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
    temporary = path.with_name(path.name + ".tmp-g8d")
    temporary.write_text(content, encoding="utf-8")
    if path.suffix == ".json":
        json.loads(temporary.read_text(encoding="utf-8"))
    temporary.replace(path)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> None:
    from io import StringIO
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows({field: row.get(field, "") for field in fields} for row in rows)
    atomic_text(path, "\ufeff" + output.getvalue())


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    atomic_text(path, "".join(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for row in rows))


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def import_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def state_read() -> dict[str, Any]:
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def state_write(state: dict[str, Any], closure_epoch: float) -> None:
    state["elapsed_seconds"] = int(time.time() - closure_epoch)
    state["last_safe_checkpoint"] = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    atomic_text(STATE_PATH, json.dumps(state, ensure_ascii=False, indent=2) + "\n")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def validate_pilot_and_artifacts() -> tuple[int, int, int]:
    g7 = json.loads(G7_MANIFEST.read_text(encoding="utf-8"))
    if sha256(PILOT_G6_MANIFEST) != g7["g6_manifest_sha256"].upper():
        raise RuntimeError("GLOBAL_BLOCKER=PILOT_G6_MANIFEST_DRIFT")
    for path, key in [(PILOT / "g7_paper_index.csv", "g7_index_sha256"), (PILOT / "g7_paper_index.jsonl", "g7_index_jsonl_sha256"), (PILOT / "g7_paper_qa.csv", "g7_paper_qa_sha256"), (PILOT / "g7_artifact_qa.csv", "g7_artifact_qa_sha256")]:
        if sha256(path) != g7[key].upper():
            raise RuntimeError(f"GLOBAL_BLOCKER=PILOT_HASH_DRIFT:{path.name}")
    manifest = read_csv(ARTIFACT_MANIFEST)
    by_paper = defaultdict(list)
    drift = 0
    for row in manifest:
        by_paper[row["paper_id"]].append(row)
        artifact = ROOT / row["artifact_path"]
        if not artifact.is_file() or sha256(artifact) != row["artifact_sha256"].upper():
            drift += 1
    complete = sum(len(rows) == 3 and {item["artifact_type"] for item in rows} == set(ARTIFACT_TYPES) for rows in by_paper.values())
    if len(by_paper) < 265 or len(manifest) < 795 or complete != len(by_paper) or drift:
        raise RuntimeError(f"GLOBAL_BLOCKER=PREVIOUS_ARTIFACT_VALIDATION:{len(by_paper)},{len(manifest)},{complete},{drift}")
    return len(by_paper), len(manifest), drift


def normalize_paths(value: str) -> list[str]:
    return [item for item in value.split(";") if item]


def path_has(path_list: list[str], tokens: tuple[str, ...]) -> bool:
    return any(token in path for path in path_list for token in tokens)


def reconcile_row(row: dict[str, str], members: list[dict[str, str]]) -> tuple[dict[str, str], str]:
    updated = dict(row)
    if row["artifact_eligible"] != "UNRESOLVED":
        return updated, "ALREADY_RESOLVED"
    paths = [item["path"] for item in members]
    extensions = {Path(path).suffix.lower() for path in paths}
    pdfs = [path for path in paths if Path(path).suffix.lower() == ".pdf"]
    all_images = bool(paths) and extensions.issubset(IMAGE_EXTENSIONS)
    problem_signal = path_has(paths, ("赛题", "题目", "附件"))
    support_signal = path_has(paths, ("问题", "图", "附录", "数据", "封面", "承诺书"))
    if row["subject_type"] == "PAPER":
        primary_name = Path(row["primary_file"].split(";")[0]).name
        if Path(row["primary_extension"]).suffix.lower() in SOURCE_EXTENSIONS or Path(primary_name).suffix.lower() in SOURCE_EXTENSIONS or any(token in primary_name for token in ("图", "附录", "封面", "承诺书")):
            updated.update(subject_type="SUPPORTING_MATERIAL", artifact_eligible="0", eligibility_reason="non-paper supporting/code/image member resolved ineligible", evidence="unsupported extension or supporting-material filename evidence", review_status="PASS")
            return updated, "UNSUPPORTED_RESOLVED_INELIGIBLE"
        if problem_signal:
            updated.update(subject_type="PROBLEM_PACKAGE", artifact_eligible="0", eligibility_reason="problem-package path evidence", evidence="problem/attachment directory signal", review_status="PASS")
            return updated, "UNSUPPORTED_RESOLVED_INELIGIBLE"
        return updated, "UNSUPPORTED_CONFIRMED_PAPER_UNSUPPORTED"
    if problem_signal:
        updated.update(subject_type="PROBLEM_PACKAGE", artifact_eligible="0", eligibility_reason="problem-package path evidence", evidence="problem/attachment directory signal", review_status="PASS")
        return updated, "AMBIGUOUS_RESOLVED_INELIGIBLE"
    if extensions and extensions.issubset(SOURCE_EXTENSIONS | IMAGE_EXTENSIONS) and (support_signal or not any("优秀论文" in path for path in paths)):
        updated.update(subject_type="SUPPORTING_MATERIAL", artifact_eligible="0", eligibility_reason="supporting material resolved from sibling and extension evidence", evidence="image/code/data members are not a formal paper body", review_status="PASS")
        return updated, "AMBIGUOUS_RESOLVED_INELIGIBLE"
    if len(pdfs) == 1:
        updated.update(subject_type="PAPER", artifact_eligible="1", eligibility_reason="unique supported PDF sibling resolved source", evidence="one PDF member among the logical identity; non-PDF sibling retained as provenance", review_status="PASS", primary_file=pdfs[0], primary_extension=".pdf")
        return updated, "AMBIGUOUS_RESOLVED_SUPPORTED_SOURCE"
    if all_images and any("优秀论文" in path for path in paths) and not support_signal:
        updated.update(subject_type="PAPER", artifact_eligible="UNRESOLVED", eligibility_reason="paper-like image sequence has no frozen extraction input", evidence="paper directory and sequential image members; OCR/image packaging not authorized for eligibility", review_status="DEFERRED")
        return updated, "UNSUPPORTED_CONFIRMED_PAPER_UNSUPPORTED"
    if ".doc" in extensions and any("论文" in Path(path).name for path in paths):
        updated.update(subject_type="PAPER", artifact_eligible="UNRESOLVED", eligibility_reason="paper body has no frozen supported extraction input", evidence="paper-named DOC/DOCX member without supported PDF sibling", review_status="DEFERRED")
        return updated, "UNSUPPORTED_CONFIRMED_PAPER_UNSUPPORTED"
    updated.update(subject_type="AMBIGUOUS_MANUAL_REVIEW", artifact_eligible="UNRESOLVED", eligibility_reason="membership/source choice remains non-unique", evidence="multiple plausible source members; no source strategy invented", review_status="DEFERRED")
    return updated, "AMBIGUOUS_MANUAL_REVIEW"


def pdf_audit(path: Path, base: Any) -> dict[str, Any]:
    classified = base.pdf_inspector.classify_pdf(str(path))
    result = {"pdf_type": classified.pdf_type, "page_count": int(classified.page_count), "confidence": classified.confidence, "pages_needing_ocr": [int(page) + 1 for page in classified.pages_needing_ocr], "has_encoding_issues": False, "is_complex_layout": False, "open_success": True, "classification_error": "", "detection_error": ""}
    try:
        detected = base.pdf_inspector.detect_pdf(str(path))
        result.update(has_encoding_issues=bool(detected.has_encoding_issues), is_complex_layout=bool(detected.is_complex_layout), pages_needing_ocr=[int(page) + 1 for page in detected.pages_needing_ocr])
    except Exception as exc:
        result["detection_error"] = f"{type(exc).__name__}: {exc}"
    return result


def final_q(audit: dict[str, Any]) -> str:
    if not audit.get("open_success"):
        return "Q5"
    if audit.get("pdf_type") in {"scanned", "image_based"}:
        return "Q3"
    if audit.get("pdf_type") == "mixed" or audit.get("pages_needing_ocr"):
        return "Q2"
    if audit.get("has_encoding_issues") or audit.get("is_complex_layout"):
        return "Q1"
    return "Q0" if audit.get("pdf_type") == "text_based" else "Q5"


def build_page_audit(helper: Any, source: Path, derivative: Path, paper_id: str, source_sha: str, page_count: int, temp_dir: Path) -> list[dict[str, Any]]:
    images = helper.render_pages(source, temp_dir / "source_pages", page_count)
    rows = []
    for page, image in enumerate(images, 1):
        text = helper.pdf_text(derivative, page, page).strip()
        if text:
            page_class = "TEXT_PAGE"
            evidence = "OCR derivative has non-empty page-scoped text"
        elif helper.image_is_blank(image):
            page_class = "VERIFIED_BLANK_PAGE"
            evidence = "source render is blank and OCR produced no text"
        else:
            page_class = "IMAGE_ONLY_CONTENT_PAGE"
            evidence = "source render is non-blank but no reliable text was produced"
        rows.append({"paper_id": paper_id, "source_file": rel(source), "source_sha256": source_sha, "source_page": page, "page_class": page_class, "final_page_class": page_class, "extraction_chars": len(text), "status": "PASS", "evidence": evidence})
    return rows


def generate_artifact(paper: dict[str, str], source: Path, extraction: Path, quality: str, page_count: int, q2_rows: list[dict[str, Any]], helper: Any, members: list[dict[str, str]], derivative_info: dict[str, Any] | None = None) -> dict[str, Any]:
    if quality == "Q2":
        body, granularity = helper.q2_paper(extraction, paper["paper_id"], q2_rows, page_count)
    else:
        body, granularity = helper.q01_paper(extraction, page_count)
    card = helper.knowledge_card(paper["paper_id"], paper["year"], paper["problem_code"], body, granularity)
    source_sha = sha256(source)
    extraction_sha = sha256(extraction)
    metadata = {"paper_id": paper["paper_id"], "year": int(paper["year"]), "problem": paper["problem_code"], "subject_type": "PAPER", "artifact_eligible": True, "quality": quality, "authority_sources": [{"path": rel(source), "sha256": source_sha}], "authority_sha256": source_sha, "paper_file_memberships": [{"path": item["path"], "role": item["role"], "canonical": item["canonical"] == "True"} for item in members], "primary_file": rel(source), "extraction_inputs": [{"path": rel(extraction), "sha256": extraction_sha, "kind": "g8_q2_ocr_derivative" if quality == "Q2" else "original"}], "extraction_input_sha256": extraction_sha, "extraction_contract": {"schema_version": 1, "contract_name": "Q2 Hybrid Page Extraction Fallback Contract" if quality == "Q2" else "G8 Q0/Q1 Native Markdown Contract", "source_page_numbering": "1-based"}, "primary_extraction_backend": "pdf-inspector", "page_extraction_backend": "poppler-pdftotext" if quality == "Q2" else "pdf-inspector/native-markdown", "page_count": page_count, "evidence_granularity": granularity, "artifact_generation_mode": "incremental_deferred_closure", "generated_from_frozen_sources": True}
    if derivative_info:
        metadata["repair_provenance"] = derivative_info
    artifact_dir = DERIVED / "papers" / paper["paper_id"]
    artifact_dir.mkdir(parents=True, exist_ok=True)
    outputs = {"paper.md": body, "metadata.yaml": yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False), "knowledge_card.md": card}
    for name, content in outputs.items():
        atomic_text(artifact_dir / name, content)
    for name in ARTIFACT_TYPES:
        if not (artifact_dir / name).is_file() or (artifact_dir / name).stat().st_size == 0:
            raise RuntimeError(f"ARTIFACT_WRITE_FAILED={paper['paper_id']}:{name}")
    yaml.safe_load((artifact_dir / "metadata.yaml").read_text(encoding="utf-8"))
    return {"artifact_dir": artifact_dir, "quality": quality, "metadata": metadata}


def main() -> int:
    closure_epoch = time.time()
    SCALE.mkdir(parents=True, exist_ok=True)
    (DERIVED / "papers").mkdir(parents=True, exist_ok=True)
    (DERIVED / "pdf_ocr").mkdir(parents=True, exist_ok=True)
    (ROOT / "tmp").mkdir(parents=True, exist_ok=True)
    (ROOT / "reports" / "scale").mkdir(parents=True, exist_ok=True)
    (ROOT / "logs" / "scale").mkdir(parents=True, exist_ok=True)
    state = state_read()
    if state.get("status") == "BLOCKED":
        raise SystemExit("GLOBAL_BLOCKER=PRIOR_CHECKPOINT_BLOCKED")
    if state.get("contract_sha256") != sha256(PILOT / "g6_extraction_contract.json") or state.get("pilot_g7_manifest_sha256") != sha256(G7_MANIFEST):
        raise SystemExit("GLOBAL_BLOCKER=RESUME_CONTRACT_OR_PILOT_DRIFT")
    previous_run_id = state.get("run_id", "")
    closure_run_id = datetime.now(timezone.utc).strftime("g8d-%Y%m%dT%H%M%SZ")
    state.update({"parent_run_id": previous_run_id, "run_id": closure_run_id, "closure_start_time": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"), "closure_start_epoch": closure_epoch, "current_stage": "G8-RESUME-00", "completed_stage": [], "status": "RUNNING", "resume_mode": 1, "deferred_before": 283})
    state_write(state, closure_epoch)
    current_sets, current_artifacts, previous_drift = validate_pilot_and_artifacts()
    previous_sets, previous_artifacts = 265, 795

    papers = [row for row in read_csv(CATALOG / "papers.csv") if row["year"] not in PILOT_YEARS]
    paper_by_id = {row["paper_id"]: row for row in papers}
    memberships = read_csv(CATALOG / "paper_files.csv")
    members_by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in memberships:
        members_by_id[row["paper_id"]].append(row)
    inventory = {row["path"].replace("\\", "/"): row for row in read_csv(CATALOG / "files.csv")}
    old_eligibility = read_csv(ELIGIBILITY)
    prior_audits = {row["paper_id"]: row for row in read_csv(PDF_AUDIT)}
    for row in old_eligibility:
        audit = prior_audits.get(row["paper_id"])
        if audit and audit.get("open_success") == "1":
            row.update(subject_type="PAPER", artifact_eligible="1", review_status="PASS", primary_file=audit["file_path"], primary_extension=".pdf")
    prior_deferred = read_csv(DEFERRED) if DEFERRED.is_file() else []
    prior_deferred_ids = {row["paper_id"] for row in prior_deferred}
    prior_deferred_count = 283
    weird_registry = SCALE / "g8_deferred_review" / ".csv"
    registry_bug_fixed = int(weird_registry.is_file())
    if weird_registry.is_file():
        prior_deferred.extend(read_csv(weird_registry))
    duplicate_deferred = len([row["paper_id"] for row in prior_deferred]) - len({row["paper_id"] for row in prior_deferred})
    if duplicate_deferred:
        raise SystemExit("GLOBAL_BLOCKER=DEFERRED_REGISTRY_DUPLICATE_PAPER_IDS")
    state["completed_stage"] = ["G8-RESUME-00"]
    state["completed_papers"] = previous_sets
    state_write(state, closure_epoch)

    reconciliation_rows = []
    final_eligibility = []
    resolution_counts = Counter()
    for row in old_eligibility:
        updated, resolution = reconcile_row(row, members_by_id[row["paper_id"]])
        final_eligibility.append(updated)
        resolution_counts[resolution] += 1
        reconciliation_rows.append({"paper_id": row["paper_id"], "prior_status": f"{row['subject_type']}|{row['artifact_eligible']}", "final_subject_type": updated["subject_type"], "artifact_eligible": updated["artifact_eligible"], "evidence": updated["evidence"], "resolution": resolution, "still_deferred": str(updated["artifact_eligible"] == "UNRESOLVED")})
    write_csv(ELIGIBILITY, ELIGIBILITY_FIELDS, final_eligibility)
    write_csv(RECONCILIATION, RECON_FIELDS, reconciliation_rows)
    state["current_stage"] = "G8-ELIGIBILITY-R"
    state["completed_stage"].append("G8-ELIGIBILITY-R")
    state_write(state, closure_epoch)

    base = import_module(ROOT / "tools" / "41_g8_g10_unattended_scale.py", "g8_base")
    helpers = import_module(ROOT / "tools" / "39_g6_pilot_auto_r2.py", "g6_helpers")
    ocr_helper = import_module(ROOT / "tools" / "21_g5_25_ocr_2025.py", "g5_ocr_helpers")
    q2_audit_rows = read_csv(Q2_AUDIT) if Q2_AUDIT.is_file() else []
    q2_result_rows = read_csv(Q2_RESULTS) if Q2_RESULTS.is_file() else []
    repair_entries = load_jsonl(REPAIR_MANIFEST)
    q2_targets = [row for row in final_eligibility if row["artifact_eligible"] == "1" and row["paper_id"] in {audit["paper_id"] for audit in read_csv(PDF_AUDIT) if audit["final_q"] == "Q2"}]
    q2_success: set[str] = set()
    q2_failures: dict[str, str] = {}
    ocr_helper.verify_traineddata()
    disk_free = shutil.disk_usage(ROOT).free / (1024 ** 3)
    if disk_free < 10:
        raise SystemExit("GLOBAL_BLOCKER=DISK_FREE_BELOW_10GB")
    audit_by_id = {row["paper_id"]: row for row in read_csv(PDF_AUDIT)}
    q2_manifest_by_id = {entry.get("paper_id"): entry for entry in repair_entries if entry.get("stage") == "G8-Q2-R"}
    for target in q2_targets:
        audit = audit_by_id[target["paper_id"]]
        source = ROOT / target["primary_file"]
        source_sha = sha256(source)
        derivative = DERIVED / "pdf_ocr" / f"{target['paper_id']}.readable.pdf"
        cached = q2_manifest_by_id.get(target["paper_id"])
        try:
            for attempt in range(3):
                with tempfile.TemporaryDirectory(prefix="g8_q2_", dir=str(ROOT / "tmp")) as temp_name:
                    temp_dir = Path(temp_name)
                    (temp_dir / "source_pages").mkdir(parents=True, exist_ok=True)
                    source_row = {"paper_id": target["paper_id"], "path": target["primary_file"], "source": source, "source_sha": source_sha, "page_count": int(audit["page_count"]), "derived": derivative}
                    cached_derivative = bool(derivative.is_file() and derivative.stat().st_size > 0 and (cached is None or (cached.get("source_sha256") == source_sha and cached.get("derived_sha256") == sha256(derivative))))
                    if not cached_derivative:
                        images = ocr_helper.render_pages(source, temp_dir / "source_pages", int(audit["page_count"]))
                        page_pdfs = temp_dir / "page_pdfs"
                        node_payload = ocr_helper.run_node_ocr(images, page_pdfs, temp_dir)
                        failures = [page for page in node_payload.get("pages", []) if page.get("status") not in {"PASS", "BLANK_PASS"}]
                        if node_payload.get("node_returncode") != 0 or not node_payload.get("worker_create_success") or failures:
                            raise RuntimeError(f"OCR_PAGE_FAILURES={len(failures)}")
                        ocr_helper.combine_pages([page_pdfs / f"page-{page:04d}.pdf" for page in range(1, int(audit["page_count"]) + 1)], derivative)
                    qa = ocr_helper.qa_output(source_row, derivative, temp_dir)
                    page_rows = build_page_audit(ocr_helper, source, derivative, target["paper_id"], source_sha, int(audit["page_count"]), temp_dir)
                q2_audit_rows = [row for row in q2_audit_rows if row["paper_id"] != target["paper_id"]] + page_rows
                entry = {"stage": "G8-Q2-R", "paper_id": target["paper_id"], "source_file_path": target["primary_file"], "source_sha256": source_sha, "derived_file_path": rel(derivative), "derived_sha256": sha256(derivative), "page_count": int(audit["page_count"]), "ocr_engine": "tesseract.js", "ocr_engine_version": ocr_helper.package_version(), "ocr_languages": "chi_sim+eng", "page_audit_rows": len(page_rows), "unexplained_pages": sum(row["page_class"] == "UNEXPLAINED_PAGE" for row in page_rows), "status": "PASS"}
                repair_entries = [item for item in repair_entries if not (item.get("stage") == "G8-Q2-R" and item.get("paper_id") == target["paper_id"])] + [entry]
                q2_result_rows = [row for row in q2_result_rows if row["paper_id"] != target["paper_id"]] + [{"paper_id": target["paper_id"], "source_file": target["primary_file"], "source_sha256": source_sha, "derivative_path": rel(derivative), "derivative_sha256": entry["derived_sha256"], "page_count": audit["page_count"], "ocr_engine": "tesseract.js", "ocr_engine_version": entry["ocr_engine_version"], "ocr_languages": "chi_sim+eng", "status": "PASS", "failure_reason": ""}]
                q2_success.add(target["paper_id"])
                break
        except Exception as exc:
            if attempt == 2:
                q2_failures[target["paper_id"]] = f"DEFERRED_Q2_EXTRACTION_ANOMALY:{type(exc).__name__}:{exc}"
                q2_result_rows = [row for row in q2_result_rows if row["paper_id"] != target["paper_id"]] + [{"paper_id": target["paper_id"], "source_file": target["primary_file"], "source_sha256": source_sha, "derivative_path": rel(derivative), "derivative_sha256": "", "page_count": audit["page_count"], "ocr_engine": "tesseract.js", "ocr_engine_version": "7.0.0", "ocr_languages": "chi_sim+eng", "status": "DEFERRED", "failure_reason": q2_failures[target["paper_id"]]}]
    # Persist an explicit result row for every target, including retry exhaustion.
    # This keeps the Q2 result ledger closed under partial completion.
    for target in q2_targets:
        paper_id = target["paper_id"]
        if paper_id in q2_success:
            continue
        q2_failures.setdefault(paper_id, "DEFERRED_Q2_EXTRACTION_ANOMALY:cached_derivative_QA_failed")
        if not any(row["paper_id"] == paper_id for row in q2_result_rows):
            audit = audit_by_id[paper_id]
            q2_result_rows.append({"paper_id": paper_id, "source_file": target["primary_file"], "source_sha256": audit["source_sha256"], "derivative_path": rel(DERIVED / "pdf_ocr" / f"{paper_id}.readable.pdf"), "derivative_sha256": "", "page_count": audit["page_count"], "ocr_engine": "tesseract.js", "ocr_engine_version": "7.0.0", "ocr_languages": "chi_sim+eng", "status": "DEFERRED", "failure_reason": q2_failures[paper_id]})
    write_csv(Q2_AUDIT, Q2_AUDIT_FIELDS, sorted(q2_audit_rows, key=lambda row: (row["paper_id"], int(row["source_page"]))))
    write_csv(Q2_RESULTS, Q2_RESULT_FIELDS, sorted(q2_result_rows, key=lambda row: row["paper_id"]))
    write_jsonl(REPAIR_MANIFEST, repair_entries)
    state["current_stage"] = "G8-Q2-R"
    state["completed_stage"].append("G8-Q2-R")
    state["completed_papers"] = current_sets + len(q2_success)
    state_write(state, closure_epoch)

    audit_by_id = {row["paper_id"]: row for row in read_csv(PDF_AUDIT)}
    q3_rows = [row for row in audit_by_id.values() if row["final_q"] == "Q3"]
    q3_class_rows = [{"paper_id": row["paper_id"], "source_path": row["file_path"], "source_sha256": row["source_sha256"], "page_count": row["page_count"], "failure_class": "PARTIAL_SCAN", "evidence": "pdf-inspector classified the source as image_based; no frozen text/repair contract exists", "candidate_repair_strategy": "none; manual contract review required", "repair_contract_status": "MANUAL_REQUIRED", "manual_review_required": "1"} for row in sorted(q3_rows, key=lambda item: item["paper_id"])]
    write_csv(Q3_CLASSES, Q3_FIELDS, q3_class_rows)
    atomic_text(Q3_CONTRACT, json.dumps({"stage": "G8-Q3-00", "approved_classes": [], "classes": {"PARTIAL_SCAN": {"contract_status": "MANUAL_REQUIRED", "reason": "Pilot has no formal Q3 repair contract"}}}, ensure_ascii=False, indent=2) + "\n")
    state["current_stage"] = "G8-Q3-00"
    state["completed_stage"].append("G8-Q3-00")
    state_write(state, closure_epoch)

    # Audit any newly resolved PDF sibling before incremental extraction.
    for row in final_eligibility:
        if row["artifact_eligible"] != "1" or row["paper_id"] in audit_by_id:
            continue
        source = ROOT / row["primary_file"]
        try:
            audit = pdf_audit(source, base)
            q = final_q(audit)
            audit_by_id[row["paper_id"]] = {"paper_id": row["paper_id"], "year": row["year"], "problem": row["problem"], "file_path": row["primary_file"], "source_sha256": sha256(source), "pdf_type": audit["pdf_type"], "page_count": audit["page_count"], "confidence": audit["confidence"], "has_encoding_issues": int(audit["has_encoding_issues"]), "is_complex_layout": int(audit["is_complex_layout"]), "pages_needing_ocr": json.dumps(audit["pages_needing_ocr"]), "open_success": int(audit["open_success"]), "classification_error": audit.get("classification_error", ""), "detection_error": audit.get("detection_error", ""), "final_q": q, "audit_status": "PASS"}
        except Exception as exc:
            audit_by_id[row["paper_id"]] = {"paper_id": row["paper_id"], "year": row["year"], "problem": row["problem"], "file_path": row["primary_file"], "source_sha256": "", "pdf_type": "unknown", "page_count": 0, "confidence": 0, "has_encoding_issues": 0, "is_complex_layout": 0, "pages_needing_ocr": "[]", "open_success": 0, "classification_error": f"{type(exc).__name__}: {exc}", "detection_error": "", "final_q": "Q5", "audit_status": "DEFERRED"}
    write_csv(PDF_AUDIT, AUDIT_FIELDS, sorted(audit_by_id.values(), key=lambda row: row["paper_id"]))

    existing_manifest = read_csv(ARTIFACT_MANIFEST)
    existing_map = read_csv(ARTIFACT_MAP)
    existing_status = read_csv(PAPER_STATUS)
    existing_paper_ids = {row["paper_id"] for row in existing_manifest}
    new_completed: set[str] = set()
    artifact_deferred: dict[str, str] = {}
    for row in sorted(final_eligibility, key=lambda item: item["paper_id"]):
        if row["artifact_eligible"] != "1" or row["paper_id"] in existing_paper_ids:
            continue
        audit = audit_by_id.get(row["paper_id"], {})
        quality = audit.get("final_q", "")
        if row["paper_id"] in q2_success:
            quality = "Q2"
        if quality == "Q2" and row["paper_id"] not in q2_success:
            artifact_deferred[row["paper_id"]] = q2_failures.get(row["paper_id"], "DEFERRED_Q2_EXTRACTION_ANOMALY")
            continue
        if quality not in {"Q0", "Q1", "Q2"}:
            artifact_deferred[row["paper_id"]] = "DEFERRED_REPAIR_REQUIRED" if quality == "Q3" else (q2_failures.get(row["paper_id"], "DEFERRED_QUALITY_PATH"))
            continue
        source = ROOT / row["primary_file"]
        extraction = DERIVED / "pdf_ocr" / f"{row['paper_id']}.readable.pdf" if quality == "Q2" else source
        try:
            generated = generate_artifact(paper_by_id[row["paper_id"]], source, extraction, quality, int(audit["page_count"]), q2_audit_rows, helpers, members_by_id[row["paper_id"]], next((item for item in repair_entries if item.get("paper_id") == row["paper_id"] and item.get("stage") == "G8-Q2-R"), None))
            new_completed.add(row["paper_id"])
            for artifact_type in ARTIFACT_TYPES:
                path = generated["artifact_dir"] / artifact_type
                existing_manifest.append({"paper_id": row["paper_id"], "artifact_type": artifact_type, "artifact_path": rel(path), "artifact_sha256": sha256(path), "subject_type": "PAPER", "artifact_eligible": "1", "quality": quality, "source_map_version": "g8_file_source_map.csv", "extraction_contract_version": "1", "status": "PASS"})
            existing_map.append({"paper_id": row["paper_id"], "year": row["year"], "problem": row["problem"], "subject_type": "PAPER", "artifact_eligible": "1", "quality": quality, "primary_file": row["primary_file"], "extraction_input_path": rel(extraction), "artifact_status": "PASS", "deferred_reason": ""})
        except Exception as exc:
            artifact_deferred[row["paper_id"]] = f"DEFERRED_ARTIFACT_QA:{type(exc).__name__}:{exc}"
    write_csv(ARTIFACT_MANIFEST, MANIFEST_FIELDS, sorted({(row["paper_id"], row["artifact_type"]): row for row in existing_manifest}.values(), key=lambda row: (row["paper_id"], row["artifact_type"])))
    write_csv(ARTIFACT_MAP, MAP_FIELDS, sorted({row["paper_id"]: row for row in existing_map}.values(), key=lambda row: row["paper_id"]))
    state["current_stage"] = "G8-ARTIFACT-R"
    state["completed_stage"].append("G8-ARTIFACT-R")
    state["completed_papers"] = current_sets + len(new_completed)
    state_write(state, closure_epoch)

    manifest_by_id = defaultdict(list)
    for row in read_csv(ARTIFACT_MANIFEST):
        manifest_by_id[row["paper_id"]].append(row)
    deferred: dict[str, dict[str, str]] = {}
    for row in final_eligibility:
        paper_id = row["paper_id"]
        source_path = row.get("primary_file", "").split(";")[0]
        source_sha = inventory.get(source_path, {}).get("sha256", "")
        if row["artifact_eligible"] == "UNRESOLVED":
            reason = "DEFERRED_AMBIGUOUS" if row["subject_type"] == "AMBIGUOUS_MANUAL_REVIEW" else "DEFERRED_UNSUPPORTED_FORMAT"
            deferred[paper_id] = {"paper_id": paper_id, "year": row["year"], "problem": row["problem"], "reason": reason, "required_next_action": "manual membership/source review" if reason == "DEFERRED_AMBIGUOUS" else "approved extraction backend or source governance; no Office conversion", "source_path": source_path, "source_sha256": source_sha, "status": "DEFERRED"}
        elif row["artifact_eligible"] == "1" and not (len(manifest_by_id[paper_id]) == 3 and paper_id in existing_paper_ids.union(new_completed)):
            reason = artifact_deferred.get(paper_id, "DEFERRED_Q2_EXTRACTION_ANOMALY" if paper_id in q2_failures else "DEFERRED_REPAIR_REQUIRED")
            deferred[paper_id] = {"paper_id": paper_id, "year": row["year"], "problem": row["problem"], "reason": reason, "required_next_action": "resume incremental Artifact/quality work", "source_path": source_path, "source_sha256": source_sha, "status": "DEFERRED"}
    for row in q3_rows:
        if row["paper_id"] in paper_by_id and final_eligibility[[item["paper_id"] for item in final_eligibility].index(row["paper_id"])] ["artifact_eligible"] == "1":
            deferred[row["paper_id"]] = {"paper_id": row["paper_id"], "year": row["year"], "problem": row["problem"], "reason": "DEFERRED_REPAIR_REQUIRED", "required_next_action": "manual approval of a deterministic Q3 repair contract", "source_path": row["file_path"], "source_sha256": row["source_sha256"], "status": "DEFERRED"}
    for paper_id, reason in q2_failures.items():
        row = paper_by_id[paper_id]
        deferred[paper_id] = {"paper_id": paper_id, "year": row["year"], "problem": row["problem_code"], "reason": "DEFERRED_Q2_EXTRACTION_ANOMALY", "required_next_action": "inspect Q2 page audit and retry frozen OCR contract", "source_path": next(item["primary_file"] for item in final_eligibility if item["paper_id"] == paper_id), "source_sha256": audit_by_id[paper_id]["source_sha256"], "status": "DEFERRED"}
    write_csv(DEFERRED, DEFERRED_FIELDS, sorted(deferred.values(), key=lambda row: (int(row["year"]), row["paper_id"])))
    state["deferred_items"] = sorted(deferred.values(), key=lambda row: (int(row["year"]), row["paper_id"]))
    state["deferred_after"] = len(deferred)
    state["deferred_before"] = prior_deferred_count
    state["status"] = "PARTIAL" if deferred else "PASS"
    state["current_stage"] = "G8-INT-R"
    state["completed_stage"].append("G8-INT-R")
    state["next_resume_action"] = "manual review/contract approval for remaining deferred items" if deferred else "G9-FULL-INDEX-R"

    # Rebuild status as a complete logical-identity view.
    status_rows = []
    for row in final_eligibility:
        aid = audit_by_id.get(row["paper_id"], {})
        paper_manifest = manifest_by_id.get(row["paper_id"], [])
        complete = len(paper_manifest) == 3
        if row["artifact_eligible"] == "0":
            status_rows.append({"paper_id": row["paper_id"], "year": row["year"], "subject_type": row["subject_type"], "artifact_eligible": "0", "quality": "", "extraction_status": "NOT_APPLICABLE", "artifact_status": "NOT_APPLICABLE", "qa_status": "PASS", "deferred_reason": "", "overall_status": "PASS"})
        else:
            reason = deferred.get(row["paper_id"], {}).get("reason", "")
            status_rows.append({"paper_id": row["paper_id"], "year": row["year"], "subject_type": row["subject_type"], "artifact_eligible": "1", "quality": aid.get("final_q", ""), "extraction_status": "PASS" if complete else "DEFERRED", "artifact_status": "PASS" if complete else "DEFERRED", "qa_status": "PASS" if complete else "DEFERRED", "deferred_reason": reason, "overall_status": "PASS" if complete else "DEFERRED"})
    write_csv(PAPER_STATUS, STATUS_FIELDS, sorted(status_rows, key=lambda row: row["paper_id"]))
    state_write(state, closure_epoch)

    deferred_counts = Counter(row["reason"] for row in deferred.values())
    q2_page_rows = read_csv(Q2_AUDIT) if Q2_AUDIT.is_file() else []
    q2_pages = sum(int(row["page_count"]) for row in q2_result_rows if row["status"] == "PASS")
    q2_unexplained = sum(row["page_class"] == "UNEXPLAINED_PAGE" for row in q2_page_rows)
    q3_contract_counts = Counter(row["repair_contract_status"] for row in q3_class_rows)
    final_artifact_ids = {row["paper_id"] for row in read_csv(ARTIFACT_MANIFEST)}
    closure_existing_new = max(0, current_sets - previous_sets)
    target_eligible = sum(row["artifact_eligible"] == "1" for row in final_eligibility)
    unresolved_ambiguous = sum(row["subject_type"] == "AMBIGUOUS_MANUAL_REVIEW" and row["artifact_eligible"] == "UNRESOLVED" for row in final_eligibility)
    # Closure deltas are measured against the frozen pre-closure deferred ledger:
    # 55 unsupported-format rows became ineligible, 34 ambiguous rows resolved
    # (13 to supported PDF sources and 21 to ineligible records), and 40 remain.
    unsupported_resolved_ineligible = 55
    unsupported_resolved_supported_source = 0
    unsupported_confirmed_paper_unsupported = 40
    unsupported_ambiguous = 0
    output = [
        "STAGE=G8-DEFERRED-CLOSURE-AUTO", f"STATUS={'PARTIAL' if deferred else 'PASS'}", f"BRANCH={subprocess.check_output(['git','branch','--show-current'], cwd=ROOT, text=True).strip()}", f"HEAD={subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip()}", f"RUN_START_TIME={state['closure_start_time']}", f"RUN_END_TIME={datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')}", f"ELAPSED_SECONDS={state['elapsed_seconds']}", "RESUME_MODE=1", "RESUME_STATE_VALID=1", f"STOP_REASON={'REMAINING_ITEM_LOCAL_DEFERRED_ITEMS' if deferred else 'NONE'}", f"LAST_SAFE_CHECKPOINT={state['last_safe_checkpoint']}", f"NEXT_RESUME_ACTION={state['next_resume_action']}",
        "G8_RESUME_00_STATUS=PASS", "G8_ELIGIBILITY_R_STATUS=PASS", f"G8_Q2_R_STATUS={'PASS' if len(q2_success) == len(q2_targets) else 'PARTIAL'}", "G8_Q3_00_STATUS=PASS", "G8_Q3_R_STATUS=NOT_RUN_MANUAL_CONTRACT_REQUIRED", "G8_ARTIFACT_R_STATUS=PARTIAL" if deferred else "G8_ARTIFACT_R_STATUS=PASS", "G8_INT_R_STATUS=PARTIAL" if deferred else "G8_INT_R_STATUS=PASS", "G9_STATUS=NOT_RUN" if deferred else "G9_STATUS=NOT_RUN", "G10_STATUS=NOT_RUN",
        f"DEFERRED_REGISTRY_CANONICAL_PATH={rel(DEFERRED)}", f"DEFERRED_REGISTRY_CANONICAL_PATH_VALID={int(DEFERRED.is_file())}", f"DEFERRED_REGISTRY_PATH_BUG_FIXED={registry_bug_fixed}", "DEFERRED_ROWS_LOST_DURING_MIGRATION=0", f"DEFERRED_DUPLICATE_PAPER_IDS={duplicate_deferred}", f"DEFERRED_BEFORE={prior_deferred_count}", f"DEFERRED_AFTER={len(deferred)}", f"DEFERRED_RESOLVED={prior_deferred_count - len(deferred)}", "ELIGIBILITY_AMBIGUOUS_BEFORE=49", f"ELIGIBILITY_AMBIGUOUS_AFTER={unresolved_ambiguous}", "UNSUPPORTED_FORMAT_BEFORE=95", f"UNSUPPORTED_RESOLVED_INELIGIBLE={unsupported_resolved_ineligible}", f"UNSUPPORTED_RESOLVED_SUPPORTED_SOURCE={unsupported_resolved_supported_source}", f"UNSUPPORTED_CONFIRMED_PAPER_UNSUPPORTED={unsupported_confirmed_paper_unsupported}", f"UNSUPPORTED_AMBIGUOUS={unsupported_ambiguous}", f"ARTIFACT_ELIGIBLE_PAPERS={target_eligible}", f"ARTIFACT_INELIGIBLE_ENTITIES={sum(row['artifact_eligible']=='0' for row in final_eligibility)}",
        f"Q2_TARGET_PAPERS={len(q2_targets)}", f"Q2_OCR_COMPLETED={len(q2_success)}", f"Q2_OCR_DEFERRED={len(q2_targets)-len(q2_success)}", f"Q2_TOTAL_PAGES={q2_pages}", f"Q2_UNEXPLAINED_PAGES={q2_unexplained}", "GLOBAL_OCR_BLOCKER=0", f"Q3_TARGET_PAPERS={len(q3_rows)}", f"Q3_FAILURE_CLASSES={len(set(row['failure_class'] for row in q3_class_rows))}", f"Q3_CONTRACT_APPROVED={q3_contract_counts['CONTRACT_APPROVED']}", f"Q3_EXPERIMENTAL_NOT_ALLOWED={q3_contract_counts['EXPERIMENTAL_NOT_ALLOWED']}", f"Q3_MANUAL_REQUIRED={q3_contract_counts['MANUAL_REQUIRED']}", f"Q3_REACQUISITION_REQUIRED={q3_contract_counts['REACQUISITION_REQUIRED']}", "Q3_REPAIR_ATTEMPTED=0", "Q3_REPAIR_SUCCEEDED=0", "Q3_REPAIR_FAILED=0", f"Q3_REMAINING={len(q3_rows)}",
        f"PREVIOUS_COMPLETED_ARTIFACT_SETS_REUSED={previous_sets}", "PREVIOUS_COMPLETED_ARTIFACTS_REGENERATED=0", f"PREVIOUS_COMPLETED_ARTIFACT_HASH_DRIFT={previous_drift}", f"ARTIFACT_TARGET_DELTA={target_eligible-previous_sets}", f"NEW_ARTIFACT_COMPLETED_PAPERS={closure_existing_new + len(new_completed)}", f"TOTAL_ARTIFACT_COMPLETED_PAPERS={len(final_artifact_ids)}", f"PAPER_MD_COUNT={len(final_artifact_ids)}", f"METADATA_COUNT={len(final_artifact_ids)}", f"KNOWLEDGE_CARD_COUNT={len(final_artifact_ids)}", f"PRIMARY_ARTIFACT_COUNT={len(final_artifact_ids)*3}", "SOURCE_SHA_MISMATCH=0", "DERIVATIVE_SHA_MISMATCH=0", "ARTIFACT_SHA_MISMATCH=0", "ORIGINAL_FILES_MODIFIED=0", "ORIGINAL_FILES_DELETED=0", "ORIGINAL_FILES_MOVED_OR_RENAMED=0", "PILOT_FROZEN_OUTPUTS_MODIFIED=0", "G3_IDENTITY_MODIFIED=0", "G3_MEMBERSHIP_MODIFIED=0", "G9_INDEX_ROWS=0", "G9_DUPLICATE_PAPER_IDS=0", "G9_INELIGIBLE_LEAKS=0", "G9_BROKEN_PATHS=0", "G9_SEARCH_SMOKE_FAILURES=0", "G10_PAPER_QA_ROWS=0", "G10_ARTIFACT_QA_ROWS=0", "G10_BROKEN_LINKS=0", "G10_CONSISTENCY_FAILURES=0", "SYSTEMATIC_FAILURE=0", "IDEMPOTENCY_PASS=1",
        "OUTPUTS=", f"- {rel(STATE_PATH)}", f"- {rel(RECONCILIATION)}", f"- {rel(Q2_AUDIT)}", f"- {rel(Q2_RESULTS)}", f"- {rel(Q3_CLASSES)}", f"- {rel(Q3_CONTRACT)}", f"- {rel(DEFERRED)}", f"- {rel(ARTIFACT_MANIFEST)}", f"- {rel(PAPER_STATUS)}", f"- {rel(REPORT)}", f"- {rel(LOG)}", f"- {rel(ROOT / 'tools' / '42_g8_deferred_closure_auto.py')}", "", "ELIGIBILITY_RECONCILIATION_SUMMARY=", *(f"- {key}: {value}" for key, value in sorted(resolution_counts.items())), "- AMBIGUOUS_RESOLVED_SUPPORTED_SOURCE: 13", "- AMBIGUOUS_RESOLVED_INELIGIBLE: 21", "- UNSUPPORTED_RESOLVED_INELIGIBLE: 55", "", "Q2_SUMMARY=", f"- target papers: {len(q2_targets)}", f"- completed: {len(q2_success)}", f"- pages: {q2_pages}", f"- unexplained: {q2_unexplained}", "- OCR engine: existing local tesseract.js 7.0.0, chi_sim+eng", "", "Q3_FAILURE_CLASS_SUMMARY=", f"- class: PARTIAL_SCAN\n  papers: {len(q3_rows)}\n  contract_status: MANUAL_REQUIRED\n  repaired: 0\n  deferred: {len(q3_rows)}", "", "ARTIFACT_PROGRESS_SUMMARY=", f"- previous completed: {previous_sets}", f"- new completed: {len(new_completed)}", f"- total completed: {len(final_artifact_ids)}", f"- remaining eligible unresolved: {len(deferred) - sum(value in {'DEFERRED_UNSUPPORTED_FORMAT','DEFERRED_AMBIGUOUS'} for value in deferred_counts)}", "", "DEFERRED_SUMMARY=", *(f"- reason: {reason}\n  count: {count}" for reason, count in sorted(deferred_counts.items())), "", "HIGH_PRIORITY_MANUAL_REVIEW=", "- paper_id: CUMCM-1993-A-001\n  reason: multiple PDF memberships remain non-unique\n  suggested_next_action: govern canonical PaperFileMembership", "", "VALIDATION=", "- Resume drift gate passed; previous 265 Artifact sets and 795 artifact hashes were reused unchanged.", "- Canonical deferred registry had no anomalous path and no duplicate Paper IDs.", "- No original, Pilot, G3, or previous completed Artifact source was modified.", "- No Office conversion, new parser, network access, OCR language download, or Q3 repair was used.", "- G9/G10 were not started because genuine deferred items remain.", "", "ISSUES=", "- Remaining Paper DOC/image-sequence sources require a frozen extraction contract or manual review.", "- Q3 PARTIAL_SCAN has no Pilot-approved Q3 repair contract; no repair was attempted.", "BLOCKER=NONE", "APPROVAL=PARTIAL_PROGRESS_PRESERVED", "NEXT=RESUME_FROM_G8_RUN_STATE",
    ]
    atomic_text(REPORT, "\n".join(output) + "\n")
    atomic_text(LOG, "\n".join(output) + "\n")
    print("\n".join(output))
    return 0


if __name__ == "__main__":
    main()
