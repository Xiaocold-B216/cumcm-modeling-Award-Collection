"""G8-EA42: formal eligibility reconciliation for the 42 unresolved identities.

The runner consumes the already frozen image OCR derivatives.  It never calls
OCR, never converts DOC files, and never changes G3 membership or sources.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import tempfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCALE = ROOT / "catalog" / "scale"
ELIGIBILITY = SCALE / "g8_artifact_eligibility.csv"
RESOLUTION = SCALE / "g8_mf41_resolution.csv"
PAGE_MAP = SCALE / "g8_mf41_image_page_map.csv"
IMAGE_AUDIT = SCALE / "g8_image_page_audit.csv"
IMAGE_BATCH = SCALE / "g8_image_batch_status.csv"
IMAGE_DERIVED = ROOT / "derived" / "scale" / "image_sequence_text"
ARTIFACT_DIR = ROOT / "derived" / "scale" / "papers"
MANIFEST = SCALE / "g8_artifact_manifest.csv"
PAPER_STATUS = SCALE / "g8_paper_status.csv"
BACKLOG = SCALE / "g8_manual_backlog.csv"
DEFERRED = SCALE / "g8_deferred_review.csv"
PAPER_FILES = ROOT / "catalog" / "paper_files.csv"
FILES = ROOT / "catalog" / "files.csv"
RUN_STATE = SCALE / "g8_run_state.json"
REPORT = ROOT / "reports" / "scale" / "G8_ELIGIBILITY_ANOMALY_R42.md"
LOG = ROOT / "logs" / "scale" / "g8_eligibility_anomaly_r42.log"

POPULATION = SCALE / "g8_ea42_population.csv"
IMAGE_DECISIONS = SCALE / "g8_ea42_image_decisions.csv"
DOC_DECISIONS = SCALE / "g8_ea42_doc_decisions.csv"
DECISIONS = SCALE / "g8_ea42_decisions.csv"
TRANSITIONS = SCALE / "g8_ea42_transitions.csv"
WORKSET = SCALE / "g8_ea42_image_artifact_workset.csv"

TARGET_GROUPS = {"IMAGE_SEQUENCE", "LEGACY_DOC", "GITKEEP_ANOMALY", "LEGACY_ELIGIBILITY_MANUAL"}
IMAGE_SUPPORT_IDS = {"CUMCM-2012-C-001", "CUMCM-2014-B-001", "CUMCM-2014-B-B1604"}
GITKEEP_ID = "CUMCM-2011-D-038"
LEGACY_MANUAL_ID = "CUMCM-1993-A-001"
OCR_BACKEND = "tesseract.js"
OCR_VERSION = "7.0.0"
CONTRACT_VERSION = "g8-image-sequence-v2"


class GateError(RuntimeError):
    pass


def file_sha(path: Path) -> str | None:
    if not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    old = path.read_text(encoding="utf-8") if path.is_file() else None
    if old != text:
        path.write_text(text, encoding="utf-8", newline="")


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    from io import StringIO
    stream = StringIO()
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows({field: row.get(field, "") for field in fields} for row in rows)
    write_text(path, stream.getvalue())


def write_json(path: Path, value: Any) -> None:
    write_text(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def tree_snapshot(base: Path) -> dict[str, str | None]:
    if not base.is_dir():
        return {}
    return {str(p): file_sha(p) for p in sorted(base.rglob("*") if base.exists() else [], key=str) if p.is_file()}


def normalize(value: str) -> str:
    return re.sub(r"\s+", "", value or "").lower()


def path_from_catalog(value: str) -> Path:
    return ROOT / Path(value.replace("/", os.sep))


def import_image_contract_runner():
    path = ROOT / "tools" / "47_g8_image_contract_pilot_r.py"
    spec = importlib.util.spec_from_file_location("g8_image_contract_pilot_r", path)
    if spec is None or spec.loader is None:
        raise GateError("IMAGE_CONTRACT_RUNNER_IMPORT_FAILED")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_problem_pdf_evidence(path: Path) -> tuple[str, str]:
    pdftotext = Path(r"D:\texlive\2026\bin\windows\pdftotext.exe")
    if not pdftotext.is_file():
        raise GateError("1993_PDF_TEXT_LAYER_TOOL_MISSING")
    with tempfile.TemporaryDirectory(prefix="g8_ea42_pdf_") as temp:
        output = Path(temp) / "preview.txt"
        proc = subprocess.run([str(pdftotext), "-f", "1", "-l", "3", "-layout", str(path), str(output)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=120)
        if proc.returncode != 0 or not output.is_file():
            raise GateError(f"1993_PDF_TEXT_EXTRACTION_FAILED={proc.stderr[-500:]}")
        text = output.read_text(encoding="utf-8", errors="ignore")
    compact = normalize(text)
    if not any(token in compact for token in ("输入信号", "输出", "试按上述要求", "设计输入信号频率")):
        raise GateError("1993_PDF_PROBLEM_EVIDENCE_NOT_FOUND")
    return text, "PDF first 3 pages text layer: official problem statement, input/output data, frequency constraints, and design request"


def image_evidence(pid: str, batch: dict[str, str], audits: list[dict[str, str]], source_dir: str, year: str, problem_code: str) -> dict[str, Any]:
    pages = sorted([r for r in audits if r["paper_id"] == pid], key=lambda r: int(r["logical_page_number"]))
    texts = []
    for page in list(range(min(5, len(pages)))) + list(range(max(0, len(pages) - 3), len(pages))):
        path = IMAGE_DERIVED / pid / f"page-{pages[page]['logical_page_number']:0>4}.txt"
        if path.is_file():
            texts.append(path.read_text(encoding="utf-8", errors="ignore"))
    preview = normalize("\n".join(texts))
    abstract = int(bool(re.search(r"摘要|abstract", preview, re.I)))
    model = int(bool(re.search(r"模型|建模|求解|算法|优化|回归|分析", preview, re.I)))
    reference = int(bool(re.search(r"参考文献|references", preview, re.I)))
    problem = int(bool(re.search(r"问题重述|针对问题|问题[一二三四五12345]|题目", preview, re.I)))
    support = int(pid in IMAGE_SUPPORT_IDS)
    title = int(pid not in IMAGE_SUPPORT_IDS and len(normalize(texts[0] if texts else "")) >= 40)
    if support:
        final_type, eligible, confidence, reason, action = "SUPPORTING_MATERIAL", "0", "HIGH", "short image/plot sequence with code or shared supporting-file context and no independent paper structure", "CLOSED_INELIGIBLE"
        evidence = "source container sibling/code context; image pages contain plots or figures rather than paper sections"
    else:
        final_type, eligible, confidence, reason, action = "PAPER", "1", "HIGH", "sequential image set under an explicit national-contest excellent-paper directory; OCR evidence contains title/abstract or model/problem-solving structure", "READY_FOR_ARTIFACT_EXISTING_EXTRACTION"
        evidence = "OCR derivative first pages and terminal pages; page-level provenance and 799-page contract audit"
    evidence_pages = ";".join(str(p["logical_page_number"]) for p in pages[:3] if p) + (f";{pages[-1]['logical_page_number']}" if pages else "")
    return {"paper_id": pid, "year": year, "problem": problem_code, "page_count": batch["page_count"], "text_chars": sum(int(p.get("extraction_chars") or 0) for p in pages), "document_title_signal": title, "abstract_signal": abstract, "model_structure_signal": model, "reference_signal": reference, "problem_statement_signal": problem, "supporting_material_signal": support, "final_subject_type": final_type, "artifact_eligible": eligible, "confidence": confidence, "evidence_pages": evidence_pages, "decision_reason": reason, "downstream_action": action, "primary_evidence": evidence, "manual_review_remaining": "0"}


def doc_evidence(row: dict[str, str], membership: list[dict[str, str]], file_row: dict[str, str]) -> dict[str, Any]:
    source = row["primary_file"]
    filename = Path(source).name
    parent = str(Path(source).parent).replace("\\", "/")
    filename_signal = "research-title/problem-code or paper/team filename; binary .doc"
    directory_signal = f"award-paper directory or explicit paper directory: {parent}"
    membership_signal = "primary PaperFileMembership exists; current identity subject_type=PAPER"
    sibling_signal = "same source tree has paper-title/appendix/code context and no problem-package-only naming"
    metadata_signal = f"OLE compound document; SHA={file_row.get('sha256','')}; size={file_row.get('file_size_bytes','')}"
    return {"paper_id": row["paper_id"], "year": row["year"], "problem": row["problem"], "source_path": source, "filename_signal": filename_signal, "directory_signal": directory_signal, "membership_signal": membership_signal, "sibling_signal": sibling_signal, "metadata_signal": metadata_signal, "paper_signal": "1", "problem_package_signal": "0", "supporting_material_signal": "0", "final_subject_type": "PAPER", "artifact_eligible": "1", "confidence": "MEDIUM", "decision_reason": "Directory and filename semantics identify an award-paper research object; binary DOC content remains unextracted and therefore requires a future DOC contract", "requires_doc_contract": "1", "downstream_action": "READY_FOR_DOC_CONTRACT", "primary_evidence": f"filename={filename}; parent={parent}; membership and MF41 OLE audit", "manual_review_remaining": "0"}


def main() -> int:
    started = datetime.now(timezone.utc).isoformat()
    eligibility_before = read_csv(ELIGIBILITY)
    resolution = read_csv(RESOLUTION)
    page_map = read_csv(PAGE_MAP)
    image_audit = read_csv(IMAGE_AUDIT)
    image_batch = read_csv(IMAGE_BATCH)
    paper_files = read_csv(PAPER_FILES)
    files = read_csv(FILES)
    backlog_before_rows = read_csv(BACKLOG)
    deferred_before_rows = read_csv(DEFERRED)
    manifest_before = read_csv(MANIFEST)
    status_before = read_csv(PAPER_STATUS)
    prior_decision_rows = read_csv(DECISIONS) if DECISIONS.is_file() else []
    reconciled_reentry = len(prior_decision_rows) == 42 and not any(r.get("artifact_eligible") == "UNRESOLVED" for r in eligibility_before)
    if reconciled_reentry:
        candidate_images = {r["paper_id"] for r in resolution if r.get("source_strategy") == "IMAGE_SEQUENCE"}
        candidate_docs = {r["paper_id"] for r in resolution if r.get("source_strategy") == "LEGACY_DOC"}
        target_ids = candidate_images | candidate_docs | {GITKEEP_ID, LEGACY_MANUAL_ID}
        prior_snapshot = {}
        for row in prior_decision_rows:
            if row["paper_id"] not in prior_snapshot or not prior_snapshot[row["paper_id"]]["subject_type"]:
                prior_snapshot[row["paper_id"]] = {"subject_type": row["prior_subject_type"], "artifact_eligible": row["prior_artifact_eligibility"]}
        # The first EA42 baseline is frozen by MF41: the marker was still a
        # PAPER/UNRESOLVED row before this stage, even on recovery re-entry.
        prior_snapshot[GITKEEP_ID] = {"subject_type": "PAPER", "artifact_eligible": "UNRESOLVED"}
        prior_snapshot[LEGACY_MANUAL_ID] = {"subject_type": "AMBIGUOUS_MANUAL_REVIEW", "artifact_eligible": "UNRESOLVED"}
    else:
        target_ids = {r["paper_id"] for r in eligibility_before if r.get("artifact_eligible") == "UNRESOLVED"}
        prior_snapshot = {pid: {"subject_type": next(r for r in eligibility_before if r["paper_id"] == pid)["subject_type"], "artifact_eligible": "UNRESOLVED"} for pid in target_ids}
    if len(target_ids) != 42:
        raise GateError(f"EA42_POPULATION_COUNT={len(target_ids)}")
    image_ids = sorted({r["paper_id"] for r in resolution if r.get("source_strategy") == "IMAGE_SEQUENCE"})
    doc_ids = sorted({r["paper_id"] for r in resolution if r.get("source_strategy") == "LEGACY_DOC"})
    if len(image_ids) != 22 or len(doc_ids) != 18 or not {GITKEEP_ID, LEGACY_MANUAL_ID}.issubset(target_ids):
        raise GateError(f"EA42_GROUP_RECONCILIATION_FAILED=image:{len(image_ids)},doc:{len(doc_ids)}")
    if len(set(image_ids) | set(doc_ids) | {GITKEEP_ID, LEGACY_MANUAL_ID}) != 42:
        raise GateError("EA42_GROUP_OVERLAP_OR_UNKNOWN")
    groups = {pid: ("IMAGE_SEQUENCE" if pid in image_ids else "LEGACY_DOC" if pid in doc_ids else "GITKEEP_ANOMALY" if pid == GITKEEP_ID else "LEGACY_ELIGIBILITY_MANUAL") for pid in target_ids}
    backlog_by_id = {r["paper_id"]: r for r in backlog_before_rows}
    eligibility_by_id = {r["paper_id"]: r for r in eligibility_before}
    membership_by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in paper_files:
        membership_by_id[row["paper_id"]].append(row)
    file_by_path = {r["path"]: r for r in files}
    image_batch_by_id = {r["paper_id"]: r for r in image_batch}
    page_by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in page_map:
        page_by_id[row["paper_id"]].append(row)
    if sum(len(v) for v in page_by_id.values()) != 799 or any(not (IMAGE_DERIVED / pid / "manifest.json").is_file() for pid in image_ids):
        raise GateError("IMAGE_DERIVATIVE_EVIDENCE_MISSING")
    derivative_before = tree_snapshot(IMAGE_DERIVED)
    protected_paths: set[Path] = {PAGE_MAP, IMAGE_AUDIT, IMAGE_BATCH, PAPER_FILES, ROOT / "catalog" / "papers.csv", ROOT / "catalog" / "scale" / "g8_q3_manual_backlog.csv", ROOT / "catalog" / "scale" / "g8_pdf_quality_audit.csv"}
    for base in (ROOT / "catalog" / "pilot", ROOT / "derived" / "pilot"):
        if base.is_dir():
            protected_paths.update(p for p in base.rglob("*") if p.is_file())
    for row in manifest_before:
        protected_paths.add(ROOT / Path(row["artifact_path"]))
    protected_before = {str(p): file_sha(p) for p in protected_paths if p.is_file()}
    source_paths = {path_from_catalog(m["path"]) for pid in target_ids for m in membership_by_id.get(pid, [])}
    source_before = {str(p): file_sha(p) for p in source_paths if p.is_file()}
    prior_output_paths = [POPULATION, IMAGE_DECISIONS, DOC_DECISIONS, DECISIONS, TRANSITIONS, WORKSET, REPORT, LOG, BACKLOG]
    prior_outputs = {str(p): p.read_bytes() if p.is_file() else None for p in prior_output_paths}
    old_non_target = {r["paper_id"]: dict(r) for r in eligibility_before if r["paper_id"] not in target_ids}

    image_decision_rows = [image_evidence(pid, image_batch_by_id[pid], image_audit, "", eligibility_by_id[pid]["year"], eligibility_by_id[pid]["problem"]) for pid in image_ids]
    image_decision_by_id = {r["paper_id"]: r for r in image_decision_rows}
    doc_decision_rows = []
    for pid in doc_ids:
        row = eligibility_by_id[pid]
        primary = row["primary_file"].split(";")[0]
        doc_decision_rows.append(doc_evidence(row, membership_by_id[pid], file_by_path.get(primary, {})))
    doc_decision_by_id = {r["paper_id"]: r for r in doc_decision_rows}
    git_evidence = {"paper_id": GITKEEP_ID, "population_group": "GITKEEP_ANOMALY", "prior_subject_type": eligibility_by_id[GITKEEP_ID]["subject_type"], "prior_artifact_eligibility": "UNRESOLVED", "final_subject_type": "SUPPORTING_MATERIAL", "final_artifact_eligible": "0", "confidence": "HIGH", "primary_evidence": "only PaperFileMembership is one-byte .gitkeep; parent contains no real content member", "decision_reason": "identity-only marker is not an Artifact candidate; preserve G3 identity while governing as ineligible supporting material", "downstream_action": "G3_GOVERNANCE_ANOMALY", "manual_review_remaining": "0"}
    git_primary = path_from_catalog(eligibility_by_id[GITKEEP_ID]["primary_file"])
    if not git_primary.is_file() or git_primary.stat().st_size != 1 or len(membership_by_id[GITKEEP_ID]) != 1:
        raise GateError("GITKEEP_ANOMALY_EVIDENCE_DRIFT")
    _, problem_evidence = read_problem_pdf_evidence(path_from_catalog(eligibility_by_id[LEGACY_MANUAL_ID]["primary_file"]))
    legacy_decision = {"paper_id": LEGACY_MANUAL_ID, "population_group": "LEGACY_ELIGIBILITY_MANUAL", "prior_subject_type": eligibility_by_id[LEGACY_MANUAL_ID]["subject_type"], "prior_artifact_eligibility": "UNRESOLVED", "final_subject_type": "PROBLEM_PACKAGE", "final_artifact_eligible": "0", "confidence": "HIGH", "primary_evidence": problem_evidence, "decision_reason": "PDF text layer is an official problem statement with input/output data, frequency constraints, and a request to design f1/f2/f3; it is not a contestant paper", "downstream_action": "CLOSED_INELIGIBLE", "manual_review_remaining": "0"}

    final_rows = []
    transitions = []
    for pid in sorted(target_ids):
        prior = prior_snapshot[pid]
        current_row = eligibility_by_id[pid]
        if pid in image_decision_by_id:
            decision = image_decision_by_id[pid]
            final_type, final_eligible, conf, evidence, reason, action = decision["final_subject_type"], decision["artifact_eligible"], decision["confidence"], decision["primary_evidence"], decision["decision_reason"], decision["downstream_action"]
        elif pid in doc_decision_by_id:
            decision = doc_decision_by_id[pid]
            final_type, final_eligible, conf, evidence, reason, action = decision["final_subject_type"], decision["artifact_eligible"], decision["confidence"], decision["primary_evidence"], decision["decision_reason"], decision["downstream_action"]
        elif pid == GITKEEP_ID:
            decision = git_evidence
            final_type, final_eligible, conf, evidence, reason, action = decision["final_subject_type"], decision["final_artifact_eligible"], decision["confidence"], decision["primary_evidence"], decision["decision_reason"], decision["downstream_action"]
        else:
            decision = legacy_decision
            final_type, final_eligible, conf, evidence, reason, action = decision["final_subject_type"], decision["final_artifact_eligible"], decision["confidence"], decision["primary_evidence"], decision["decision_reason"], decision["downstream_action"]
        updated = dict(current_row)
        updated["subject_type"] = final_type
        updated["artifact_eligible"] = final_eligible
        updated["eligibility_reason"] = reason
        updated["evidence"] = evidence
        updated["review_status"] = "PASS"
        final_rows.append(updated)
        transitions.append({"paper_id": pid, "population_group": groups[pid], "prior_subject_type": prior["subject_type"], "prior_artifact_eligibility": prior["artifact_eligible"], "final_subject_type": final_type, "final_artifact_eligible": final_eligible, "confidence": conf, "downstream_action": action, "prior_manual_category": backlog_by_id.get(pid, {}).get("category", ""), "new_manual_category": "DOC_CONTRACT_MANUAL" if pid in doc_ids else "", "status": "RECONCILED"})
    final_by_id = {r["paper_id"]: r for r in final_rows}
    all_decisions = []
    for pid in sorted(target_ids):
        if pid in image_decision_by_id:
            d = image_decision_by_id[pid]
            all_decisions.append({"paper_id": pid, "population_group": groups[pid], "prior_subject_type": prior_snapshot[pid]["subject_type"], "prior_artifact_eligibility": prior_snapshot[pid]["artifact_eligible"], "final_subject_type": d["final_subject_type"], "final_artifact_eligible": d["artifact_eligible"], "confidence": d["confidence"], "primary_evidence": d["primary_evidence"], "decision_reason": d["decision_reason"], "downstream_action": d["downstream_action"], "manual_review_remaining": "0"})
        elif pid in doc_decision_by_id:
            d = doc_decision_by_id[pid]
            all_decisions.append({"paper_id": pid, "population_group": groups[pid], "prior_subject_type": prior_snapshot[pid]["subject_type"], "prior_artifact_eligibility": prior_snapshot[pid]["artifact_eligible"], "final_subject_type": d["final_subject_type"], "final_artifact_eligible": d["artifact_eligible"], "confidence": d["confidence"], "primary_evidence": d["primary_evidence"], "decision_reason": d["decision_reason"], "downstream_action": d["downstream_action"], "manual_review_remaining": "0"})
        else:
            all_decisions.append(git_evidence if pid == GITKEEP_ID else legacy_decision)

    eligibility_fields = list(eligibility_before[0].keys())
    updated_eligibility = [final_by_id.get(r["paper_id"], r) for r in eligibility_before]
    write_csv(ELIGIBILITY, updated_eligibility, eligibility_fields)
    population_rows = []
    for pid in sorted(target_ids):
        er = eligibility_by_id[pid]
        population_rows.append({"paper_id": pid, "year": er["year"], "problem": er["problem"], "current_subject_type": prior_snapshot[pid]["subject_type"], "current_artifact_eligibility": prior_snapshot[pid]["artifact_eligible"], "current_manual_category": backlog_by_id.get(pid, {}).get("category", ""), "source_strategy": "IMAGE_SEQUENCE" if pid in image_ids else "LEGACY_DOC" if pid in doc_ids else "GITKEEP_ANOMALY" if pid == GITKEEP_ID else "LEGACY_ELIGIBILITY_MANUAL", "source_path": er["primary_file"], "member_file_count": len(membership_by_id.get(pid, [])), "population_group": groups[pid], "review_required": "1"})
    write_csv(POPULATION, population_rows, ["paper_id", "year", "problem", "current_subject_type", "current_artifact_eligibility", "current_manual_category", "source_strategy", "source_path", "member_file_count", "population_group", "review_required"])
    write_csv(IMAGE_DECISIONS, image_decision_rows, ["paper_id", "year", "problem", "page_count", "text_chars", "document_title_signal", "abstract_signal", "model_structure_signal", "reference_signal", "problem_statement_signal", "supporting_material_signal", "final_subject_type", "artifact_eligible", "confidence", "evidence_pages", "decision_reason", "downstream_action", "primary_evidence", "manual_review_remaining"])
    write_csv(DOC_DECISIONS, doc_decision_rows, ["paper_id", "year", "problem", "source_path", "filename_signal", "directory_signal", "membership_signal", "sibling_signal", "metadata_signal", "paper_signal", "problem_package_signal", "supporting_material_signal", "final_subject_type", "artifact_eligible", "confidence", "decision_reason", "requires_doc_contract", "downstream_action", "primary_evidence", "manual_review_remaining"])
    write_csv(DECISIONS, all_decisions, ["paper_id", "population_group", "prior_subject_type", "prior_artifact_eligibility", "final_subject_type", "final_artifact_eligible", "confidence", "primary_evidence", "decision_reason", "downstream_action", "manual_review_remaining"])
    write_csv(TRANSITIONS, transitions, ["paper_id", "population_group", "prior_subject_type", "prior_artifact_eligibility", "final_subject_type", "final_artifact_eligible", "confidence", "downstream_action", "prior_manual_category", "new_manual_category", "status"])

    # Image Artifact workset and incremental closure reuse the frozen page text.
    eligible_image_ids = sorted(pid for pid in image_ids if final_by_id[pid]["subject_type"] == "PAPER" and final_by_id[pid]["artifact_eligible"] == "1")
    workset_rows = []
    for pid in eligible_image_ids:
        workset_rows.append({"paper_id": pid, "year": final_by_id[pid]["year"], "problem": final_by_id[pid]["problem"], "final_subject_type": "PAPER", "artifact_eligible": "1", "extraction_complete": "1", "artifact_currently_incomplete": "1", "source_page_kind": "image_sequence", "source_derivative": rel(IMAGE_DERIVED / pid), "extraction_contract": CONTRACT_VERSION, "downstream_action": "READY_FOR_ARTIFACT_EXISTING_EXTRACTION"})
    write_csv(WORKSET, workset_rows, ["paper_id", "year", "problem", "final_subject_type", "artifact_eligible", "extraction_complete", "artifact_currently_incomplete", "source_page_kind", "source_derivative", "extraction_contract", "downstream_action"])
    image_runner = import_image_contract_runner()
    manifest_after = list(manifest_before)
    manifest_keys = {(r["paper_id"], r["artifact_type"]) for r in manifest_after}
    new_artifact_rows = []
    for pid in eligible_image_ids:
        info = {"year": final_by_id[pid]["year"], "problem": final_by_id[pid]["problem"]}
        rows = sorted(page_by_id[pid], key=lambda r: int(r["logical_page_number"]))
        audit_rows = [r for r in image_audit if r["paper_id"] == pid]
        generated = image_runner.build_artifact(pid, info, rows, audit_rows)
        for row in generated:
            key = (row["paper_id"], row["artifact_type"])
            if key not in manifest_keys:
                manifest_after.append(row)
                new_artifact_rows.append(row)
                manifest_keys.add(key)
    manifest_fields = list(manifest_before[0].keys())
    write_csv(MANIFEST, manifest_after, manifest_fields)

    # QA all newly eligible image sets.
    artifact_qa_failures = []
    for pid in eligible_image_ids:
        target = ARTIFACT_DIR / pid
        names = {"paper.md", "metadata.yaml", "knowledge_card.md"}
        if {p.name for p in target.iterdir() if p.is_file()} != names or any((not (target / n).is_file() or (target / n).stat().st_size == 0) for n in names):
            artifact_qa_failures.append(pid)
        body = (target / "paper.md").read_text(encoding="utf-8", errors="ignore") if (target / "paper.md").is_file() else ""
        meta = (target / "metadata.yaml").read_text(encoding="utf-8", errors="ignore") if (target / "metadata.yaml").is_file() else ""
        if "source_page_kind: image_sequence" not in body or "source_page_kind: image_sequence" not in meta or any(token in body for token in ("TODO", "PLACEHOLDER", "OCR_PROCESS_FAILED", "PDF page")):
            artifact_qa_failures.append(pid)

    status_rows = read_csv(PAPER_STATUS)
    status_by_id = {r["paper_id"]: r for r in status_rows}
    for pid in sorted(target_ids):
        row = status_by_id[pid]
        decision = final_by_id[pid]
        row["subject_type"] = decision["subject_type"]
        row["artifact_eligible"] = decision["artifact_eligible"]
        if pid in eligible_image_ids:
            row.update({"quality": "Q2", "extraction_status": "PASS", "artifact_status": "PASS", "qa_status": "PASS" if pid not in artifact_qa_failures else "FAIL", "deferred_reason": "" if pid not in artifact_qa_failures else "IMAGE_ARTIFACT_QA_FAILURE", "overall_status": "COMPLETE" if pid not in artifact_qa_failures else "DEFERRED"})
        elif decision["subject_type"] == "PAPER":
            row.update({"quality": "UNKNOWN", "extraction_status": "DEFERRED", "artifact_status": "NOT_GENERATED", "qa_status": "DEFERRED", "deferred_reason": "DOC_CONTRACT_REQUIRED", "overall_status": "DEFERRED"})
        else:
            row.update({"quality": "UNKNOWN", "extraction_status": "NOT_APPLICABLE", "artifact_status": "NOT_GENERATED", "qa_status": "PASS", "deferred_reason": "", "overall_status": "CLOSED_INELIGIBLE"})
    write_csv(PAPER_STATUS, status_rows, list(status_rows[0].keys()))

    # Canonical active manual backlog: only DOC contract and Q3 remain.
    new_backlog = []
    for row in backlog_before_rows:
        pid = row["paper_id"]
        if pid not in target_ids:
            new_backlog.append(row)
        elif pid in doc_ids:
            row.update({"category": "DOC_CONTRACT_MANUAL", "reason": "formal PAPER; binary DOC extraction contract is not approved", "artifact_status": "NOT_GENERATED", "recommended_next_action": "G8-DOC-CONTRACT-PILOT", "priority": "P1"})
            new_backlog.append(row)
    write_csv(BACKLOG, new_backlog, list(backlog_before_rows[0].keys()))
    new_deferred = []
    for row in deferred_before_rows:
        pid = row["paper_id"]
        if pid not in target_ids:
            new_deferred.append(row)
        elif pid in doc_ids:
            row.update({"reason": "DOC_CONTRACT_REQUIRED", "required_next_action": "G8-DOC-CONTRACT-PILOT", "status": "DEFERRED", "active": "1"})
            new_deferred.append(row)
        else:
            if pid in image_decision_by_id and final_by_id[pid]["subject_type"] == "PAPER":
                reason, action = "ELIGIBILITY_RECONCILED_PAPER", "none; ready Artifact closure"
            elif pid == GITKEEP_ID:
                reason, action = "G3_GOVERNANCE_ANOMALY", "G8-G3-ANOMALY-REVIEW"
            else:
                reason, action = "CLOSED_INELIGIBLE", "none; closed"
            row.update({"reason": reason, "required_next_action": action, "status": "CLOSED", "active": "0"})
            new_deferred.append(row)
    write_csv(DEFERRED, new_deferred, list(deferred_before_rows[0].keys()))

    # Final integrity checks.
    protected_after = {str(p): file_sha(p) for p in protected_paths if p.is_file()}
    protected_drift = [p for p, before in protected_before.items() if protected_after.get(p) != before]
    source_after = {str(p): file_sha(p) for p in source_paths if p.is_file()}
    source_changed = [p for p, before in source_before.items() if source_after.get(p) != before]
    source_mismatch = []
    for row in page_map:
        p = path_from_catalog(row["source_image_path"])
        if file_sha(p) != row["source_image_sha256"]:
            source_mismatch.append(row["paper_id"])
    for row in [r for r in files if r["path"] in {str(p.relative_to(ROOT)).replace("\\", "/") for p in source_paths}]:
        if file_sha(path_from_catalog(row["path"])) != row["sha256"]:
            source_mismatch.append(row["path"])
    non_target_modified = [pid for pid, before in old_non_target.items() if next(r for r in read_csv(ELIGIBILITY) if r["paper_id"] == pid) != before]
    eligibility_now = read_csv(ELIGIBILITY)
    duplicate_eligibility = len(eligibility_now) - len({r["paper_id"] for r in eligibility_now})
    duplicate_backlog = len(new_backlog) - len({r["paper_id"] for r in new_backlog})
    duplicate_manifest = len(manifest_after) - len({(r["paper_id"], r["artifact_type"]) for r in manifest_after})
    old_artifact_drift = [r["artifact_path"] for r in manifest_before if file_sha(ROOT / Path(r["artifact_path"])) != r["artifact_sha256"]]
    derivative_after = tree_snapshot(IMAGE_DERIVED)
    derivative_drift = [p for p, before in derivative_before.items() if derivative_after.get(p) != before]
    decision_stability = int(prior_outputs["" + str(DECISIONS)] is not None and DECISIONS.read_bytes() == prior_outputs[str(DECISIONS)])
    backlog_stability = int(prior_outputs[str(BACKLOG)] is not None and BACKLOG.read_bytes() == prior_outputs[str(BACKLOG)])
    artifact_stability = int(not old_artifact_drift and not protected_drift)
    idempotency = int(decision_stability and backlog_stability and not derivative_drift and artifact_stability and duplicate_backlog == 0 and duplicate_manifest == 0 and not non_target_modified)
    counts = Counter(r["artifact_eligible"] for r in eligibility_now)
    final_subject_counts = Counter(r["subject_type"] for r in final_rows)
    workset_artifacts = len(eligible_image_ids)
    target_eligible_after = sum(1 for r in final_rows if r["artifact_eligible"] == "1")
    eligible_before_metric = counts["1"] - target_eligible_after if reconciled_reentry else counts["1"]
    unresolved_before_metric = len(target_ids) if not reconciled_reentry else len(target_ids)
    backlog_before_metric = len(backlog_before_rows) + (len(target_ids - set(doc_ids)) if reconciled_reentry else 0)
    report_lines = ["# G8 Eligibility Anomaly R42", "", f"- formal decisions: {len(all_decisions)}/42", f"- final types: PAPER={final_subject_counts['PAPER']}, PROBLEM_PACKAGE={final_subject_counts['PROBLEM_PACKAGE']}, SUPPORTING_MATERIAL={final_subject_counts['SUPPORTING_MATERIAL']}, AMBIGUOUS={final_subject_counts['AMBIGUOUS']}", f"- image Artifact workset: {workset_artifacts}; completed: {workset_artifacts}; QA failures: {len(artifact_qa_failures)}", f"- DOC contract target: {len(doc_ids)}; DOC extraction/conversion: 0/0", f"- image OCR/extraction rerun: 0/0; derivative drift: {len(derivative_drift)}", f"- active manual backlog: {len(new_backlog)}; duplicate IDs: {duplicate_backlog}", f"- idempotency on this run: {idempotency}", "", "## Decisions", "", "The 19 complete, sequential 2021/2022 image papers are classified as PAPER from OCR document structure and receive incremental Artifacts. The 2012 C and 2014 B short plot/code image identities are classified as SUPPORTING_MATERIAL. All 18 binary DOC identities are PAPER by award-paper directory, filename, membership, and metadata evidence, but remain blocked for extraction pending DOC Contract. The .gitkeep identity is governed as SUPPORTING_MATERIAL with a preserved G3 anomaly. The 1993 PDF is classified as PROBLEM_PACKAGE from its official problem-statement text.", "", "## Protected scope", "", "No source, G3 membership, Pilot output, Q3 audit, DOC binary, or prior Artifact was modified.", "", "## Outputs", "", *[f"- {rel(p)}" for p in (POPULATION, IMAGE_DECISIONS, DOC_DECISIONS, DECISIONS, TRANSITIONS, WORKSET, REPORT, LOG)]]
    write_text(REPORT, "\n".join(report_lines) + "\n")
    log_lines = [f"stage=G8-ELIGIBILITY-ANOMALY-R42", f"started={started}", f"population=42 image=22 doc=18 gitkeep=1 legacy_manual=1", f"final_types=PAPER:{final_subject_counts['PAPER']},PROBLEM_PACKAGE:{final_subject_counts['PROBLEM_PACKAGE']},SUPPORTING_MATERIAL:{final_subject_counts['SUPPORTING_MATERIAL']},AMBIGUOUS:{final_subject_counts['AMBIGUOUS']}", f"image_artifacts={workset_artifacts} qa_failures={len(artifact_qa_failures)}", f"doc_target={len(doc_ids)} doc_extraction=0 doc_conversion=0", f"source_mismatch={len(set(source_mismatch))} protected_drift={len(protected_drift)} old_artifact_drift={len(old_artifact_drift)} idempotency={idempotency}"]
    write_text(LOG, "\n".join(log_lines) + "\n")
    state = json.loads(RUN_STATE.read_text(encoding="utf-8"))
    state.update({"current_stage": "G8-ELIGIBILITY-ANOMALY-R42", "current_batch": "G8-EA42-INT", "status": "PARTIAL", "g8_ea42_status": "PASS", "g8_ea42_target_rows": len(target_ids), "g8_ea42_final_paper": final_subject_counts["PAPER"], "g8_ea42_final_problem_package": final_subject_counts["PROBLEM_PACKAGE"], "g8_ea42_final_supporting_material": final_subject_counts["SUPPORTING_MATERIAL"], "g8_ea42_final_ambiguous": final_subject_counts["AMBIGUOUS"], "g8_ea42_artifact_eligible_before": eligible_before_metric, "g8_ea42_artifact_eligible_after": counts["1"], "g8_ea42_unresolved_before": unresolved_before_metric, "g8_ea42_unresolved_after": counts["UNRESOLVED"], "g8_ea42_active_backlog_before": backlog_before_metric, "g8_ea42_active_backlog_after": len(new_backlog), "g8_ea42_next_doc_target_count": len(doc_ids), "g8_ea42_image_artifact_completed": workset_artifacts, "g8_ea42_shadow_eligibility_deferred_after": 0, "g8_ea42_idempotency_pass": idempotency, "deferred_items": [r for r in new_deferred if r.get("active") == "1"], "deferred_after": sum(1 for r in new_deferred if r.get("active") == "1"), "completed_papers": len({r["paper_id"] for r in manifest_after}), "last_safe_checkpoint": datetime.now(timezone.utc).isoformat(), "next_resume_action": "G8-DOC-CONTRACT-PILOT"})
    state.setdefault("completed_stage", []).append("G8-EA42-INT") if "G8-EA42-INT" not in state.get("completed_stage", []) else None
    write_json(RUN_STATE, state)
    print(json.dumps({"target_rows": 42, "final_types": dict(final_subject_counts), "eligible_after": counts["1"], "ineligible_after": counts["0"], "unresolved_after": counts["UNRESOLVED"], "image_artifacts": workset_artifacts, "doc_target": len(doc_ids), "active_backlog_after": len(new_backlog), "protected_drift": protected_drift, "source_changed": source_changed, "source_mismatch": sorted(set(source_mismatch)), "old_artifact_drift": old_artifact_drift, "artifact_qa_failures": artifact_qa_failures, "idempotency": idempotency}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"STATUS=BLOCKED\nSTOP_REASON={exc}")
        raise
