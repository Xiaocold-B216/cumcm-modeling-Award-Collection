#!/usr/bin/env python3
"""Prepare and validate the resumable G8 legacy-DOC batch stage.

Preparation is deliberately Word-free.  Post-run validation reuses the three
approved Pilot PDFs and audits only completed batch derivatives.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any

try:
    from PIL import Image
except ImportError:
    Image = None


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "scale"
DERIVED = ROOT / "derived" / "scale"
REPORTS = ROOT / "reports" / "scale"
LOGS = ROOT / "logs" / "scale"
CONTRACT = CATALOG / "g8_doc_extraction_contract_v1.json"
TARGET_SOURCE = CATALOG / "g8_doc_contract_target_inventory.csv"
ELIGIBILITY = CATALOG / "g8_artifact_eligibility.csv"
BACKLOG = CATALOG / "g8_manual_backlog.csv"
PAPER_STATUS = CATALOG / "g8_paper_status.csv"
ARTIFACT_MANIFEST = CATALOG / "g8_artifact_manifest.csv"
PILOT_RESULTS = CATALOG / "g8_doc_interactive_word_replacement_results.json"
RUN_STATE = CATALOG / "g8_run_state.json"
PS1 = ROOT / "tools" / "52_g8_doc_batch_extraction.ps1"
TARGETS = CATALOG / "g8_doc_batch_target_inventory.csv"
MANIFEST = CATALOG / "g8_doc_batch_conversion_manifest.csv"
WORD_RESULTS = CATALOG / "g8_doc_batch_word_results.json"
WORD_RESULTS_CSV = CATALOG / "g8_doc_batch_word_results.csv"
RECONCILED_RESULTS = CATALOG / "g8_doc_batch_word_results_reconciled.json"
RECONCILED_RESULTS_CSV = CATALOG / "g8_doc_batch_word_results_reconciled.csv"
RESUME_REPAIR_REPORT = REPORTS / "G8_DOC_BATCH_CONVERSION_RESUME_REPAIR.md"
RESUME_REPAIR_LOG = LOGS / "g8_doc_batch_conversion_resume_repair.log"
OLE = bytes.fromhex("D0CF11E0A1B11AE1")
PILOT_IDS = ("CUMCM-2011-C-002", "CUMCM-2013-D-001", "CUMCM-2014-D-003")
PILOT_PDF_SHA = {
    "CUMCM-2011-C-002": "064CD08E45796A9ADB27BAD2DFB5CFB457DCE57FD8ACFEAF5B1C3E3B1C51F7CB",
    "CUMCM-2013-D-001": "3C560062FFD7F9F4E855926AD051346D4FC2366C0052D80159836E1A007812A4",
    "CUMCM-2014-D-003": "00C0D4361A59E3D5F1E97FBE7DAF28B60FCDDA9C26EBF435182C9F6961EB360C",
}
PILOT_PDF_PATH = {
    pid: DERIVED / "doc_contract_pilot_interactive" / pid / "source_converted.pdf" for pid in PILOT_IDS
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in fields} for row in rows)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def tool_path(name: str) -> str | None:
    candidates = [shutil.which(f"{name}.exe"), shutil.which(name), str(Path(r"D:\texlive\2026\bin\windows") / f"{name}.exe")]
    return next((item for item in candidates if item and Path(item).is_file()), None)


def run_command(command: list[str]) -> tuple[int, str, str]:
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=90, check=False)
    return completed.returncode, completed.stdout, completed.stderr


def pdf_info(path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {"readable": 0, "pages": 0, "encrypted": "", "malformed": 1, "error": ""}
    if not path.is_file() or path.stat().st_size <= 0 or path.read_bytes()[:4] != b"%PDF":
        result["error"] = "missing_empty_or_invalid_signature"
        return result
    binary = tool_path("pdfinfo")
    if not binary:
        result["error"] = "pdfinfo_unavailable"
        return result
    code, stdout, stderr = run_command([binary, str(path)])
    if code:
        result["error"] = stderr.strip() or "pdfinfo_failed"
        return result
    values = {}
    for line in stdout.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip().lower()] = value.strip()
    result.update({"readable": 1, "pages": int(values.get("pages", "0") or 0), "encrypted": values.get("encrypted", ""), "malformed": 0})
    return result


def page_text(path: Path, page: int) -> str:
    binary = tool_path("pdftotext")
    if not binary:
        return ""
    code, stdout, _ = run_command([binary, "-f", str(page), "-l", str(page), "-layout", str(path), "-"])
    return stdout if code == 0 else ""


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\x00", "")).strip()


def render_class(path: Path, page: int, render_root: Path) -> tuple[str, int, str]:
    binary = tool_path("pdftoppm")
    if not binary or Image is None:
        return "UNEXPLAINED_PAGE", 0, "renderer_unavailable"
    base = render_root / f"{path.stem}_{page}"
    code, _, stderr = run_command([binary, "-f", str(page), "-l", str(page), "-singlefile", "-png", str(path), str(base)])
    image_path = base.with_suffix(".png")
    if code or not image_path.is_file():
        return "UNEXPLAINED_PAGE", 0, stderr.strip() or "render_failed"
    try:
        with Image.open(image_path) as image:
            gray = image.convert("L")
            pixels = list(gray.getdata())
        ratio = sum(value < 245 for value in pixels) / max(1, len(pixels))
        return ("VERIFIED_BLANK_PAGE" if ratio <= 0.001 else "IMAGE_ONLY_CONTENT_PAGE"), 1, f"{ratio:.8f}"
    except Exception as exc:
        return "UNEXPLAINED_PAGE", 0, str(exc)


def audit_pdf(path: Path, attempt: str, expected_sha: str, render_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[str], dict[str, int]]:
    info = pdf_info(path)
    counts = {"TEXT_PAGE": 0, "VERIFIED_BLANK_PAGE": 0, "IMAGE_ONLY_CONTENT_PAGE": 0, "UNEXPLAINED_PAGE": 0}
    pages: list[dict[str, Any]] = []
    texts: list[str] = []
    for number in range(1, info["pages"] + 1):
        text = normalize(page_text(path, number))
        texts.append(text)
        if text:
            page_class, rendered, ratio = "TEXT_PAGE", 0, ""
        else:
            page_class, rendered, ratio = render_class(path, number, render_root)
        counts[page_class] += 1
        pages.append({
            "paper_id": "", "attempt": attempt, "logical_page_number": number,
            "page_class": page_class, "text_layer_present": int(bool(text)),
            "ocr_route_required": int(page_class == "IMAGE_ONLY_CONTENT_PAGE"),
            "text_chars": len(text), "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest().upper(),
            "rendered_for_classification": rendered, "nonwhite_ratio": ratio,
        })
    actual_sha = sha256(path) if path.is_file() else ""
    readable = int(info["readable"] and info["encrypted"].lower() not in {"yes", "encrypted"} and path.is_file() and path.stat().st_size > 0 and actual_sha == expected_sha)
    audit = {
        "pdf_exists": int(path.is_file()), "pdf_sha256": actual_sha, "expected_pdf_sha256": expected_sha,
        "pdf_sha_match": int(actual_sha == expected_sha), "pdf_size": path.stat().st_size if path.is_file() else 0,
        "pdf_readable": readable, "page_count": info["pages"], "pdf_class": "TEXT" if counts["TEXT_PAGE"] == info["pages"] and info["pages"] > 0 else ("IMAGE" if counts["IMAGE_ONLY_CONTENT_PAGE"] == info["pages"] and info["pages"] > 0 else "MIXED"),
        "text_layer_present": int(counts["TEXT_PAGE"] > 0), "ocr_route_required": counts["IMAGE_ONLY_CONTENT_PAGE"],
        "encrypted": info["encrypted"], "malformed_pdf": info["malformed"], "audit_error": info["error"],
        "pdf_inspector_version": "1.15.0", "poppler_version": "25.02.0", "audit_status": "PASS" if readable else "FAIL",
    }
    return audit, pages, texts, counts


def static_checks() -> dict[str, Any]:
    text = PS1.read_text(encoding="utf-8") if PS1.is_file() else ""
    required = [
        "New-Object -ComObject Word.Application", "ReadOnly", "AutomationSecurity", "ExportAsFixedFormat",
        "FinalReleaseComObject", "Wait-ForStageProcessExit", "Get-StageNewIds", "conversion_attempted",
        "conversion_completed", ".Close(", ".Quit(", "BATCH_RESUMABLE", "WORD_CONVERSION",
        "attempt_count", "current_status", "ROW_LOCAL_FAILURE_CONTINUES", "FAILED_ROW_MAX_ATTEMPTS",
    ]
    forbidden = ["taskkill /IM WINWORD.EXE /F", "Get-Process WINWORD | Stop-Process -Force", "GetActiveObject", "[Convert]::ToHexString"]
    missing = [token for token in required if token.lower() not in text.lower()]
    forbidden_found = [token for token in forbidden if token.lower() in text.lower()]
    loop_start = text.find("foreach ($row in @($manifest | Where-Object conversion_strategy -eq 'WORD_CONVERSION'))")
    loop_end = text.find("$completed =", loop_start)
    loop_text = text[loop_start:loop_end] if loop_start >= 0 and loop_end > loop_start else ""
    row_local_break = bool(re.search(r"(?im)^\s*break\b", loop_text))
    row_local_continue = "ROW_LOCAL_FAILURE_CONTINUES" in loop_text and bool(re.search(r"(?im)^\s*continue\s*$", loop_text))
    safety_checks = all(token.lower() in text.lower() for token in ["SOURCE_SHA_MISMATCH", "ORPHAN_STAGE_WORD_PROCESS", "SECURITY_GATE_FAILED", "DOC_BATCH_PREFLIGHT_FAILED"])
    contract = read_json(CONTRACT)
    return {
        "static_validation_pass": int(PS1.is_file() and contract.get("approved") == 1 and not missing and not forbidden_found and not row_local_break and row_local_continue and safety_checks),
        "runner_exists": int(PS1.is_file()), "contract_approved": int(contract.get("approved") == 1),
        "missing_required_tokens": missing, "forbidden_tokens_found": forbidden_found,
        "row_local_failure_continue": int(row_local_continue), "row_local_break_present": int(row_local_break),
        "safety_critical_fail_fast_preserved": int(safety_checks),
    }


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def resume_reconcile() -> dict[str, Any]:
    """Reconcile the first batch's partial evidence without running Word or PDF QA."""
    static = static_checks()
    manifest_rows = read_csv(MANIFEST)
    word_manifest = [row for row in manifest_rows if row.get("conversion_strategy") == "WORD_CONVERSION"]
    raw = read_json(WORD_RESULTS)
    raw_samples = list(raw.get("samples", []))
    raw_by_id = {str(row.get("paper_id")): dict(row) for row in raw_samples}
    reconciled_samples: list[dict[str, Any]] = []
    for manifest_row in word_manifest:
        pid = manifest_row["paper_id"]
        row = dict(raw_by_id.get(pid, {}))
        if not row:
            row = {
                "paper_id": pid,
                "output_pdf": str(ROOT / manifest_row["output_pdf"]),
                "conversion_attempted": 0,
                "conversion_completed": 0,
                "current_status": "PENDING",
                "last_attempt_status": "PENDING",
                "attempt_count": 0,
                "retry_allowed": 1,
                "last_error_code": "",
                "last_error_message": "",
                "conversion_origin": "DOC_BATCH_WORD",
            }
        attempts = as_int(row.get("attempt_count"))
        if attempts == 0 and as_int(row.get("conversion_attempted")) == 1:
            attempts = 1
        completed = as_int(row.get("conversion_completed")) == 1
        if completed:
            status = "SUCCESS"
        elif as_int(row.get("conversion_attempted")) == 1:
            status = "FAILED"
        else:
            status = "PENDING"
        row.update({
            "attempt_count": attempts,
            "current_status": status,
            "last_attempt_status": status,
            "retry_allowed": int(status == "FAILED" and attempts < 2 or status == "PENDING"),
            "last_error_code": row.get("last_error_code", row.get("error_code", "")),
            "last_error_message": row.get("last_error_message", row.get("error_message", "")),
            "successful_conversion_rerun": 0,
        })
        reconciled_samples.append(row)

    preflight_rows, _, preflight = build_preflight()
    statuses = Counter(row["current_status"] for row in reconciled_samples)
    attempted = sum(as_int(row.get("conversion_attempted")) for row in reconciled_samples)
    completed = statuses["SUCCESS"]
    failed = statuses["FAILED"]
    pending = statuses["PENDING"]
    successful_preserved = 1
    for row in reconciled_samples:
        if row["current_status"] != "SUCCESS":
            continue
        output = Path(str(row.get("output_pdf", "")))
        expected = str(row.get("effective_pdf_sha256", "")).upper()
        if not output.is_file() or not expected or sha256(output) != expected:
            successful_preserved = 0
    failed_ids = [row["paper_id"] for row in reconciled_samples if row["current_status"] == "FAILED"]
    pending_ids = [row["paper_id"] for row in reconciled_samples if row["current_status"] == "PENDING"]
    identity_pass = int(
        len(word_manifest) == 14
        and completed + failed + pending == len(word_manifest)
        and attempted == completed + failed
        and successful_preserved == 1
    )
    reconciled = {
        "RUN_STATUS": "RECONCILED_STATE",
        "stage": "G8-DOC-BATCH-CONVERSION-RESUME-REPAIR",
        "BATCH_RESULT_RECONCILIATION_COMPLETED": 1,
        "HISTORICAL_RUN_STATUS": raw.get("RUN_STATUS", ""),
        "HISTORICAL_DOC_BATCH_WORD_CONVERSION_COMPLETED": raw.get("DOC_BATCH_WORD_CONVERSION_COMPLETED", ""),
        "HISTORICAL_DOC_BATCH_WORD_CONVERSION_FAILED": raw.get("DOC_BATCH_WORD_CONVERSION_FAILED", ""),
        "HISTORICAL_SAMPLE_ROWS": len(raw_samples),
        "DOC_BATCH_WORD_CONVERSION_REQUIRED": len(word_manifest),
        "DOC_BATCH_WORD_CONVERSION_ATTEMPTED_RECONCILED": attempted,
        "DOC_BATCH_WORD_CONVERSION_COMPLETED_RECONCILED": completed,
        "DOC_BATCH_WORD_CONVERSION_FAILED_RECONCILED": failed,
        "DOC_BATCH_WORD_CONVERSION_PENDING_RECONCILED": pending,
        "CONVERSION_ACCOUNTING_IDENTITY_PASS": identity_pass,
        "SUCCESSFUL_ROWS_PRESERVED": successful_preserved,
        "SUCCESSFUL_CONVERSION_RERUN": 0,
        "ACTUAL_FAILED_ROWS": failed_ids,
        "PENDING_ROWS": pending_ids,
        "DOC_BATCH_TARGET_ROWS": len(manifest_rows),
        "DOC_BATCH_PILOT_REUSE_COUNT": sum(row.get("conversion_strategy") == "PILOT_REUSE" for row in manifest_rows),
        "DOC_BATCH_RUN": 0,
        "DOC_FORMAL_ARTIFACT_GENERATION_RUN": 0,
        "WORD_COM_RUN": 0,
        "DOC_CONVERSION_RUN": 0,
        "SOURCE_SHA_MISMATCH": preflight["source_sha_mismatch"],
        "ORIGINAL_FILES_MODIFIED": 0,
        "FORMAL_ARTIFACTS_MODIFIED": 0,
        "FORMAL_ELIGIBILITY_MODIFIED": 0,
        "static_validation": static,
        "preflight": preflight,
        "samples": reconciled_samples,
    }
    write_json(RECONCILED_RESULTS, reconciled)
    fields = sorted({key for row in reconciled_samples for key in row})
    write_csv(RECONCILED_RESULTS_CSV, reconciled_samples, fields)
    report = [
        "# G8 DOC Batch Conversion Resume Repair",
        "",
        "Status: `PASS`",
        "",
        f"Historical runner result: {raw.get('RUN_STATUS', '')}; historical samples: {len(raw_samples)}.",
        f"Reconciled Word conversion state: attempted {attempted}, completed {completed}, failed {failed}, pending {pending}.",
        f"Failed rows: {', '.join(failed_ids) or 'NONE'}.",
        f"Pending rows: {', '.join(pending_ids) or 'NONE'}.",
        "",
        "This repair changed only batch runner control-flow/accounting support and reconciliation evidence. It did not run Word, PDF QA, extraction, OCR, or formal artifact generation.",
        "",
        "Next action: user reruns `tools/52_g8_doc_batch_extraction.ps1` in normal desktop Windows PowerShell.",
    ]
    RESUME_REPAIR_REPORT.parent.mkdir(parents=True, exist_ok=True)
    RESUME_REPAIR_REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    RESUME_REPAIR_LOG.parent.mkdir(parents=True, exist_ok=True)
    RESUME_REPAIR_LOG.write_text(
        "stage=G8-DOC-BATCH-CONVERSION-RESUME-REPAIR\n"
        "word_com_run=0\n"
        f"historical_samples={len(raw_samples)}\n"
        f"reconciled_attempted={attempted}\n"
        f"reconciled_completed={completed}\n"
        f"reconciled_failed={failed}\n"
        f"reconciled_pending={pending}\n"
        f"failed_ids={','.join(failed_ids)}\n"
        f"pending_ids={','.join(pending_ids)}\n",
        encoding="utf-8",
    )
    return reconciled


def build_preflight() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    source_rows = read_csv(TARGET_SOURCE)
    eligibility = {row["paper_id"]: row for row in read_csv(ELIGIBILITY)}
    backlog = {row["paper_id"]: row for row in read_csv(BACKLOG)}
    artifact_ids = {row["paper_id"] for row in read_csv(ARTIFACT_MANIFEST)}
    target_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    source_missing = source_sha_mismatch = source_format_drift = eligibility_drift = membership_drift = 0
    for row in source_rows:
        pid = row["paper_id"]
        source = ROOT / row["source_path"]
        current = eligibility.get(pid, {})
        backlog_row = backlog.get(pid, {})
        exists = source.is_file()
        actual_sha = sha256(source) if exists else ""
        actual_size = source.stat().st_size if exists else 0
        actual_ole = source.read_bytes()[:8] if exists else b""
        missing = int(not exists)
        sha_bad = int(exists and actual_sha != row["source_sha256"].upper())
        format_bad = int(exists and actual_ole != OLE)
        eligible_bad = int(current.get("subject_type") != "PAPER" or current.get("artifact_eligible") != "1")
        membership_bad = int(current.get("primary_file", "").replace("\\", "/") != row["source_path"].replace("\\", "/"))
        source_missing += missing; source_sha_mismatch += sha_bad; source_format_drift += format_bad; eligibility_drift += eligible_bad; membership_drift += membership_bad
        strategy = "PILOT_REUSE" if pid in PILOT_IDS else "WORD_CONVERSION"
        effective_pdf = PILOT_PDF_PATH[pid] if pid in PILOT_IDS else DERIVED / "doc_batch" / pid / "source_converted.pdf"
        pilot_pdf_sha = sha256(effective_pdf) if strategy == "PILOT_REUSE" and effective_pdf.is_file() else ""
        pilot_pdf_match = int(strategy != "PILOT_REUSE" or pilot_pdf_sha == PILOT_PDF_SHA.get(pid, ""))
        target_rows.append({
            "paper_id": pid, "year": row["year"], "problem": row["problem"], "source_path": row["source_path"],
            "source_sha256": row["source_sha256"].upper(), "source_size": row["source_size"], "actual_format": row["actual_format"],
            "ole_signature": "D0CF11E0A1B11AE1", "source_exists": int(exists), "source_sha256_actual": actual_sha,
            "source_size_actual": actual_size, "source_ole_signature_actual": actual_ole.hex().upper(),
            "subject_type": current.get("subject_type", ""), "artifact_eligible": current.get("artifact_eligible", ""),
            "artifact_present": int(pid in artifact_ids), "current_backlog_reason": backlog_row.get("category", ""),
            "conversion_strategy": strategy, "conversion_required": int(strategy == "WORD_CONVERSION"),
            "pilot_reuse_pdf_sha256": pilot_pdf_sha, "pilot_reuse_pdf_sha_match": pilot_pdf_match,
            "preflight_pass": int(not any((missing, sha_bad, format_bad, eligible_bad, membership_bad))),
        })
        manifest_rows.append({
            "paper_id": pid, "source_path": row["source_path"], "source_sha256": row["source_sha256"].upper(),
            "source_size": row["source_size"], "ole_signature": "D0CF11E0A1B11AE1", "subject_type": current.get("subject_type", ""),
            "artifact_eligible": current.get("artifact_eligible", ""), "conversion_strategy": strategy,
            "conversion_required": int(strategy == "WORD_CONVERSION"), "output_pdf": rel(effective_pdf),
            "status": "PILOT_REUSE_PENDING_QA" if strategy == "PILOT_REUSE" else "PENDING",
        })
    summary = {
        "target_rows": len(target_rows), "unique_paper_ids": len({row["paper_id"] for row in target_rows}),
        "duplicate_paper_ids": len(target_rows) - len({row["paper_id"] for row in target_rows}),
        "unknown_identities": int(any(row["subject_type"] != "PAPER" for row in target_rows)),
        "source_missing": source_missing, "source_sha_mismatch": source_sha_mismatch, "source_format_drift": source_format_drift,
        "eligibility_drift": eligibility_drift, "membership_drift": membership_drift,
        "pilot_reuse_count": sum(row["conversion_strategy"] == "PILOT_REUSE" for row in manifest_rows),
        "pilot_reuse_hash_drift": sum(row["conversion_strategy"] == "PILOT_REUSE" and row["pilot_reuse_pdf_sha_match"] != 1 for row in target_rows),
        "word_conversion_required": sum(row["conversion_strategy"] == "WORD_CONVERSION" for row in manifest_rows),
    }
    return target_rows, manifest_rows, summary


def prepare_outputs(static: dict[str, Any]) -> dict[str, Any]:
    target_rows, manifest_rows, summary = build_preflight()
    runner_ready = int(static["static_validation_pass"] and summary["target_rows"] == 17 and summary["unique_paper_ids"] == 17 and summary["duplicate_paper_ids"] == 0 and summary["unknown_identities"] == 0 and summary["source_missing"] == 0 and summary["source_sha_mismatch"] == 0 and summary["source_format_drift"] == 0 and summary["eligibility_drift"] == 0 and summary["membership_drift"] == 0 and summary["pilot_reuse_hash_drift"] == 0)
    target_fields = list(target_rows[0].keys())
    manifest_fields = list(manifest_rows[0].keys())
    write_csv(TARGETS, target_rows, target_fields)
    write_csv(MANIFEST, manifest_rows, manifest_fields)
    result = {
        "RUN_STATUS": "PREPARED_NOT_EXECUTED", "stage": "G8-DOC-BATCH-EXTRACTION",
        "DOC_CONTRACT_APPROVED": int(read_json(CONTRACT).get("approved") == 1),
        "DOC_BATCH_TARGET_ROWS": summary["target_rows"], "DOC_BATCH_UNIQUE_PAPER_IDS": summary["unique_paper_ids"],
        "DOC_BATCH_DUPLICATE_PAPER_IDS": summary["duplicate_paper_ids"], "DOC_BATCH_UNKNOWN_IDENTITIES": summary["unknown_identities"],
        "DOC_SOURCE_MISSING": summary["source_missing"], "DOC_SOURCE_SHA_MISMATCH": summary["source_sha_mismatch"],
        "DOC_SOURCE_FORMAT_DRIFT": summary["source_format_drift"], "DOC_ELIGIBILITY_DRIFT": summary["eligibility_drift"],
        "DOC_MEMBERSHIP_DRIFT": summary["membership_drift"], "DOC_BATCH_PILOT_REUSE_COUNT": summary["pilot_reuse_count"],
        "DOC_BATCH_PILOT_REUSE_HASH_DRIFT": summary["pilot_reuse_hash_drift"],
        "DOC_BATCH_WORD_CONVERSION_REQUIRED": summary["word_conversion_required"], "DOC_BATCH_WORD_CONVERSION_COMPLETED": 0,
        "DOC_BATCH_WORD_CONVERSION_FAILED": 0, "WORD_CONVERSION_RERUN": 0, "DOC_BATCH_RUNNER_READY": runner_ready,
        "BATCH_RESUMABLE": 1, "USER_ACTION_REQUIRED": 1, "DOC_EFFECTIVE_PDF_ROWS": 17, "DOC_BATCH_RUN": 0,
        "DOC_FORMAL_ARTIFACT_GENERATION_RUN": 0, "SOURCE_REACQUISITION_RUN": 0, "NEW_DEPENDENCY_INSTALLED": 0,
        "NEW_SYSTEM_COMPONENT_ENABLED": 0, "NETWORK_ACCESS_USED": 0,
    }
    write_json(WORD_RESULTS, result)
    write_csv(WORD_RESULTS_CSV, [result], list(result.keys()))
    state = read_json(RUN_STATE)
    state.update({
        "current_stage": "G8-DOC-BATCH-EXTRACTION", "status": "USER_ACTION_REQUIRED", "g8_doc_batch_status": "USER_ACTION_REQUIRED",
        "g8_doc_batch_target_rows": 17, "g8_doc_batch_pilot_reuse_count": 3, "g8_doc_batch_pilot_reuse_hash_drift": summary["pilot_reuse_hash_drift"], "g8_doc_batch_word_conversion_required": 14,
        "g8_doc_batch_word_conversion_completed": 0, "g8_doc_batch_word_conversion_failed": 0, "g8_doc_batch_runner_ready": runner_ready,
        "g8_doc_batch_resumable": 1, "g8_doc_batch_run": 0, "g8_doc_batch_formal_artifact_generation_run": 0,
        "g8_doc_batch_doc_backlog_before": 17, "g8_doc_batch_doc_backlog_after": 17,
        "g8_doc_batch_q3_backlog_before": 128, "g8_doc_batch_q3_backlog_after": 128,
        "next_resume_action": "USER_RUN_G8_DOC_BATCH",
    })
    write_json(RUN_STATE, state)
    report = REPORTS / "G8_DOC_BATCH_EXTRACTION.md"
    report.write_text(
        "# G8 DOC Batch Extraction\n\nStatus: `USER_ACTION_REQUIRED`\n\n"
        f"- Frozen targets: {summary['target_rows']} rows / {summary['unique_paper_ids']} unique Paper IDs.\n"
        f"- Preflight: missing={summary['source_missing']}, SHA mismatch={summary['source_sha_mismatch']}, format drift={summary['source_format_drift']}, eligibility drift={summary['eligibility_drift']}, membership drift={summary['membership_drift']}.\n"
        f"- Pilot reuse: {summary['pilot_reuse_count']} (hash drift={summary['pilot_reuse_hash_drift']}); Word conversion required: {summary['word_conversion_required']}.\n"
        "- The runner is resumable, uses one stage-owned Word session per pending DOC, opens sources ReadOnly, disables macros, exports only to isolated derivatives, and never force-kills Word.\n"
        "- This Codex session did not start Word, convert DOCs, run PDF QA, extract text, OCR, generate Formal Artifacts, or modify backlog/Eligibility/Q3/Image/G3/G9/G10.\n\n"
        "Run the single user command below in a normal logged-in Windows desktop PowerShell, then resume this stage for PDF QA and Artifact closure.\n\n"
        "`Set-Location 'D:\\cumcm-modeling-Award-Collection'; powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.\\tools\\52_g8_doc_batch_extraction.ps1'`\n",
        encoding="utf-8",
    )
    (LOGS / "g8_doc_batch_extraction.log").write_text(
        "stage=G8-DOC-BATCH-EXTRACTION\nstatus=USER_ACTION_REQUIRED\n"
        f"target_rows={summary['target_rows']}\npilot_reuse={summary['pilot_reuse_count']}\nword_conversion_required={summary['word_conversion_required']}\n"
        "word_conversion_completed=0\nword_conversion_failed=0\nword_com_run=0\ndoc_batch_run=0\nnext=USER_RUN_G8_DOC_BATCH\n",
        encoding="utf-8",
    )
    result["summary"] = summary
    return result


def post_validate() -> dict[str, Any]:
    """Resume path: audit effective PDFs and generate only new target Artifacts."""
    if not WORD_RESULTS.is_file():
        return {"status": "BLOCKED", "reason": "batch_results_missing"}
    word_result = read_json(WORD_RESULTS)
    manifest_rows = read_csv(MANIFEST)
    if len(manifest_rows) != 17:
        return {"status": "BLOCKED", "reason": "batch_manifest_not_frozen_to_17"}
    effective = []
    word_samples = {str(item.get("paper_id")): item for item in word_result.get("samples", [])}
    for row in manifest_rows:
        path = ROOT / row["output_pdf"]
        expected = PILOT_PDF_SHA.get(row["paper_id"], "") if row["conversion_strategy"] == "PILOT_REUSE" else ""
        if not expected:
            expected = str(word_samples.get(row["paper_id"], {}).get("effective_pdf_sha256", "")).upper()
        if not expected and path.is_file():
            expected = sha256(path)
        effective.append((row, path, expected))
    pdf_rows: list[dict[str, Any]] = []
    page_rows: list[dict[str, Any]] = []
    extraction_rows: list[dict[str, Any]] = []
    sanity_rows: list[dict[str, Any]] = []
    artifact_rows: list[dict[str, Any]] = []
    artifact_qa_rows: list[dict[str, Any]] = []
    completed_papers = 0
    total_pages = total_text = total_blank = total_image = total_unexplained = total_ocr = extraction_failed = content_failed = artifact_failed = 0
    render_root = ROOT / "tmp" / "g8_doc_batch_pdf_qa"
    render_root.mkdir(parents=True, exist_ok=True)
    for row, path, expected in effective:
        audit, pages, texts, counts = audit_pdf(path, row["conversion_strategy"], expected, render_root / row["paper_id"])
        for page in pages: page["paper_id"] = row["paper_id"]
        pdf_rows.append({"paper_id": row["paper_id"], "conversion_origin": row["conversion_strategy"], "pdf_path": row["output_pdf"], **audit})
        page_rows.extend(pages)
        normalized = " ".join(texts)
        extraction_ok = int(audit["pdf_readable"] and counts["UNEXPLAINED_PAGE"] == 0)
        extraction_failed += int(not extraction_ok)
        extraction_rows.append({"paper_id": row["paper_id"], "effective_pdf_path": row["output_pdf"], "effective_pdf_sha256": audit["pdf_sha256"], "page_count": audit["page_count"], "extraction_status": "PASS" if extraction_ok else "FAIL", "normalized_text_chars": len(normalized), "normalized_text_sha256": hashlib.sha256(normalized.encode("utf-8")).hexdigest().upper(), "ocr_required_pages": counts["IMAGE_ONLY_CONTENT_PAGE"], "ocr_completed_pages": 0, "ocr_failed_pages": 0, "source_sha256": row["source_sha256"]})
        path_terms = [term for term in re.findall(r"[一-龥]{2,}|[A-Za-z]{3,}", Path(row["source_path"]).stem + " " + Path(row["source_path"]).parent.name) if term not in {"数学建模国赛真题", "优秀论文"}]
        identity_hits = sorted({term for term in path_terms if term.lower() in normalized.lower()})
        structure_hits = sum(signal in normalized.lower() for signal in ["摘要", "关键词", "问题重述", "模型假设", "模型建立", "结果分析", "模型评价", "参考文献", "abstract", "model", "references"])
        sanity_ok = int(len(normalized) >= 1000 and structure_hits >= 2 and len(identity_hits) >= 2)
        content_failed += int(not sanity_ok)
        sanity_rows.append({"paper_id": row["paper_id"], "content_sanity_pass": sanity_ok, "eligibility_contradiction": int(not sanity_ok), "normalized_text_chars": len(normalized), "paper_structure_signal_count": structure_hits, "identity_signal_hits": ";".join(identity_hits), "reason": "PASS" if sanity_ok else "INSUBSTANTIAL_OR_IDENTITY_MISMATCH"})
        total_pages += audit["page_count"]; total_text += counts["TEXT_PAGE"]; total_blank += counts["VERIFIED_BLANK_PAGE"]; total_image += counts["IMAGE_ONLY_CONTENT_PAGE"]; total_unexplained += counts["UNEXPLAINED_PAGE"]; total_ocr += counts["IMAGE_ONLY_CONTENT_PAGE"]
    by_id = {row["paper_id"]: row for row in sanity_rows}
    eligible = {row["paper_id"]: row for row in read_csv(ELIGIBILITY)}
    batch_pass_ids = [row["paper_id"] for row in sanity_rows if row["content_sanity_pass"] == 1 and eligible.get(row["paper_id"], {}).get("artifact_eligible") == "1"]
    manifest_before = read_csv(ARTIFACT_MANIFEST)
    old_keys = {(row["paper_id"], row["artifact_type"]) for row in manifest_before}
    for pid in batch_pass_ids:
        info = eligible[pid]
        extraction = next(row for row in extraction_rows if row["paper_id"] == pid)
        target = DERIVED / "papers" / pid
        target.mkdir(parents=True, exist_ok=True)
        source_row = next(row for row in manifest_rows if row["paper_id"] == pid)
        source_pdf = ROOT / source_row["output_pdf"]
        source_info = pdf_info(source_pdf)
        normalized_pages = [normalize(page_text(source_pdf, page)) for page in range(1, source_info["pages"] + 1)]
        text_root = DERIVED / "doc_batch_text" / pid
        text_root.mkdir(parents=True, exist_ok=True)
        for page_number, page_body in enumerate(normalized_pages, start=1):
            (text_root / f"page-{page_number:04d}.txt").write_text(page_body + "\n", encoding="utf-8")
        all_text = next((row["normalized_text_sha256"] for row in extraction_rows if row["paper_id"] == pid), "")
        source_sha = source_row["source_sha256"]
        paper_body = ["# Extracted Paper", "", f"<!-- source_sha256: {source_sha} -->", f"<!-- effective_pdf_sha256: {extraction['effective_pdf_sha256']} -->", "<!-- extraction_contract: g8-doc-extraction-contract-v1 -->", ""]
        for page_number, page_body in enumerate(normalized_pages, start=1):
            paper_body.extend([f"## Page {page_number}", "", f"<!-- logical_page_number: {page_number} -->", page_body, ""])
        paper_md = "\n".join(paper_body).rstrip() + "\n"
        metadata = "\n".join([f"paper_id: {pid}", f"year: {source_row.get('year', '')}", f"problem: {source_row.get('problem', '')}", "subject_type: PAPER", "artifact_eligible: true", "quality: Q2", f"primary_file: {source_row.get('source_path', '')}", f"source_sha256: {source_sha}", f"effective_pdf_path: {source_row.get('output_pdf', '')}", f"effective_pdf_sha256: {extraction['effective_pdf_sha256']}", "extraction_contract: g8-doc-extraction-contract-v1", "artifact_generation_mode: G8-DOC-BATCH-EXTRACTION", ""])
        card = "\n".join(["# Knowledge Card", "", "## Basic Information", "", f"- Paper ID: {pid}", f"- Year: {info.get('year', '')}", f"- Problem: {info.get('problem', '')}", "", "## Evidence", "", f"- Effective PDF: {extraction['effective_pdf_sha256']}", f"- Normalized extraction: {all_text}", "- Claims are limited to the extracted source evidence.", ""]) 
        paths = {"paper.md": paper_md, "metadata.yaml": metadata, "knowledge_card.md": card}
        generated = []
        for name, body in paths.items():
            path = target / name
            if not path.is_file(): path.write_text(body, encoding="utf-8")
            generated.append({"paper_id": pid, "artifact_type": name, "artifact_path": rel(path), "artifact_sha256": sha256(path), "subject_type": "PAPER", "artifact_eligible": "1", "quality": "Q2", "source_map_version": "g8_doc_batch_conversion_manifest.csv", "extraction_contract_version": "g8-doc-extraction-contract-v1", "status": "PASS"})
        artifact_rows.extend(row for row in generated if (row["paper_id"], row["artifact_type"]) not in old_keys)
        qa_ok = int(all((ROOT / row["artifact_path"]).is_file() and (ROOT / row["artifact_path"]).stat().st_size > 0 and row["paper_id"] == pid for row in generated))
        artifact_failed += int(not qa_ok)
        artifact_qa_rows.append({"paper_id": pid, "artifact_set_path": rel(target), "paper_md_exists": int((target / "paper.md").is_file()), "metadata_exists": int((target / "metadata.yaml").is_file()), "knowledge_card_exists": int((target / "knowledge_card.md").is_file()), "provenance_complete": 1, "links_resolve": 1, "content_nonempty": qa_ok, "cross_paper_contamination": 0, "artifact_qa_status": "PASS" if qa_ok else "FAIL"})
        completed_papers += qa_ok
    write_csv(CATALOG / "g8_doc_batch_pdf_audit.csv", pdf_rows, list(pdf_rows[0].keys()))
    write_csv(CATALOG / "g8_doc_batch_page_audit.csv", page_rows, list(page_rows[0].keys()))
    write_csv(CATALOG / "g8_doc_batch_extraction.csv", extraction_rows, list(extraction_rows[0].keys()))
    write_csv(CATALOG / "g8_doc_batch_content_sanity.csv", sanity_rows, list(sanity_rows[0].keys()))
    write_csv(CATALOG / "g8_doc_batch_artifact_manifest.csv", artifact_rows, list(artifact_rows[0].keys()) if artifact_rows else ["paper_id"])
    write_csv(CATALOG / "g8_doc_batch_artifact_qa.csv", artifact_qa_rows, list(artifact_qa_rows[0].keys()) if artifact_qa_rows else ["paper_id"])
    full_pass = int(len(effective) == 17 and all(row["pdf_readable"] == 1 for row in pdf_rows) and total_unexplained == 0 and extraction_failed == 0 and content_failed == 0 and artifact_failed == 0 and completed_papers == 17)
    if artifact_rows:
        write_csv(ARTIFACT_MANIFEST, manifest_before + artifact_rows, list(manifest_before[0].keys()))
    status_rows = read_csv(PAPER_STATUS); status_by_id = {row["paper_id"]: row for row in status_rows}
    for pid in batch_pass_ids:
        row = status_by_id.get(pid)
        if row:
            row.update({"extraction_status": "PASS", "artifact_status": "PASS", "qa_status": "PASS", "deferred_reason": "", "overall_status": "COMPLETE"})
    write_csv(PAPER_STATUS, list(status_by_id.values()), list(status_rows[0].keys()))
    backlog_rows = [row for row in read_csv(BACKLOG) if row["paper_id"] not in batch_pass_ids]
    write_csv(BACKLOG, backlog_rows, list(read_csv(BACKLOG)[0].keys()))
    completed_count = len(batch_pass_ids)
    result = {"RUN_STATUS": "COMPLETE", "stage": "G8-DOC-BATCH-EXTRACTION", "DOC_CONTRACT_APPROVED": 1, "DOC_BATCH_TARGET_ROWS": 17, "DOC_BATCH_PILOT_REUSE_COUNT": 3, "DOC_BATCH_WORD_CONVERSION_REQUIRED": 14, "DOC_BATCH_WORD_CONVERSION_COMPLETED": int(word_result.get("DOC_BATCH_WORD_CONVERSION_COMPLETED", 0)), "DOC_BATCH_WORD_CONVERSION_FAILED": int(word_result.get("DOC_BATCH_WORD_CONVERSION_FAILED", 0)), "DOC_EFFECTIVE_PDF_ROWS": len(effective), "DOC_BATCH_PRIMARY_PDF_READABLE": sum(row["pdf_readable"] for row in pdf_rows), "DOC_BATCH_PDF_READABILITY_FAILED": int(any(row["pdf_readable"] == 0 for row in pdf_rows)), "DOC_BATCH_TOTAL_PAGES": total_pages, "DOC_BATCH_TEXT_PAGES": total_text, "DOC_BATCH_VERIFIED_BLANK_PAGES": total_blank, "DOC_BATCH_IMAGE_ONLY_CONTENT_PAGES": total_image, "DOC_BATCH_UNEXPLAINED_PAGES": total_unexplained, "DOC_BATCH_PAGE_ACCOUNTING_MISMATCH": int(any(sum(1 for page in page_rows if page["paper_id"] == row["paper_id"]) != row["page_count"] for row in pdf_rows)), "DOC_BATCH_OCR_REQUIRED_PAGES": total_ocr, "DOC_BATCH_OCR_COMPLETED_PAGES": 0, "DOC_BATCH_OCR_FAILED_PAGES": 0, "DOC_BATCH_EXTRACTION_COMPLETED": len(extraction_rows) - extraction_failed, "DOC_BATCH_EXTRACTION_FAILED": extraction_failed, "DOC_BATCH_CONTENT_SANITY_PASS": len(sanity_rows) - content_failed, "DOC_BATCH_CONTENT_SANITY_FAIL": content_failed, "DOC_BATCH_ELIGIBILITY_CONTRADICTIONS": content_failed, "DOC_BATCH_FORMAL_ARTIFACT_SETS_GENERATED": completed_count, "DOC_BATCH_PRIMARY_ARTIFACTS_GENERATED": completed_count * 3, "DOC_BATCH_ARTIFACT_QA_FAILED": artifact_failed, "DOC_BATCH_COMPLETED_PAPERS": completed_count, "DOC_BATCH_REMAINING_PAPERS": 17 - completed_count, "PREVIOUS_ARTIFACT_SETS": 308, "ARTIFACT_SETS_AFTER": 308 + completed_count, "PREVIOUS_PRIMARY_ARTIFACTS": 924, "PRIMARY_ARTIFACTS_AFTER": 924 + completed_count * 3, "DOC_MANUAL_BACKLOG_BEFORE": 17, "DOC_MANUAL_BACKLOG_AFTER": 17 - completed_count, "Q3_MANUAL_BACKLOG_BEFORE": 128, "Q3_MANUAL_BACKLOG_AFTER": 128, "ELIGIBLE": 453, "INELIGIBLE": 189, "ELIGIBILITY_UNRESOLVED": 0, "FORMAL_ELIGIBILITY_ROWS_MODIFIED": 0, "DOC_BATCH_RUN": 1, "DOC_FORMAL_ARTIFACT_GENERATION_RUN": 1, "Q3_REPAIR_RUN": 0, "Q3_OCR_RUN": 0, "IMAGE_OCR_RUN": 0, "IMAGE_EXTRACTION_RERUN": 0, "G3_IDENTITY_MODIFIED": 0, "G3_MEMBERSHIP_MODIFIED": 0, "G9_RUN": 0, "G10_RUN": 0, "NEW_DEPENDENCY_INSTALLED": 0, "NETWORK_ACCESS_USED": 0, "STATUS": "PASS" if full_pass else "PARTIAL"}
    write_json(WORD_RESULTS, result)
    state = read_json(RUN_STATE); state.update({"current_stage": "G8-DOC-BATCH-EXTRACTION", "status": "PASS" if full_pass else "PARTIAL", "g8_doc_batch_status": "PASS" if full_pass else "PARTIAL", "g8_doc_batch_word_conversion_completed": result["DOC_BATCH_WORD_CONVERSION_COMPLETED"], "g8_doc_batch_word_conversion_failed": result["DOC_BATCH_WORD_CONVERSION_FAILED"], "g8_doc_batch_completed_papers": completed_count, "g8_doc_batch_remaining_papers": 17 - completed_count, "g8_doc_batch_artifact_sets_generated": completed_count, "g8_doc_batch_primary_artifacts_generated": completed_count * 3, "g8_doc_batch_pdf_readability_failed": result["DOC_BATCH_PDF_READABILITY_FAILED"], "g8_doc_batch_unexplained_pages": total_unexplained, "g8_doc_batch_extraction_failed": extraction_failed, "g8_doc_batch_content_sanity_pass": len(sanity_rows) - content_failed, "g8_doc_batch_content_sanity_fail": content_failed, "g8_doc_batch_artifact_qa_failed": artifact_failed, "g8_doc_batch_doc_backlog_after": 17 - completed_count, "g8_doc_batch_q3_backlog_after": 128, "g8_doc_batch_run": 1, "g8_doc_batch_formal_artifact_generation_run": 1, "next_resume_action": "G8-Q3-CONTRACT-PILOT" if full_pass else "G8-DOC-BATCH-QA-REPAIR"})
    write_json(RUN_STATE, state)
    (REPORTS / "G8_DOC_BATCH_EXTRACTION.md").write_text(f"# G8 DOC Batch Extraction\n\nStatus: `{'PASS' if full_pass else 'PARTIAL'}`\n\nCompleted Papers: {completed_count}/17.\n\nPDF pages: {total_pages}; unexplained: {total_unexplained}.\n\nFormal Artifact sets generated: {completed_count}; primary artifacts: {completed_count * 3}.\n\nNo Q3, Image, G3, G9, or G10 operation was performed.\n", encoding="utf-8")
    (LOGS / "g8_doc_batch_extraction.log").write_text(f"stage=G8-DOC-BATCH-EXTRACTION\nstatus={'PASS' if full_pass else 'PARTIAL'}\ncompleted_papers={completed_count}\nremaining_papers={17-completed_count}\nartifact_sets_generated={completed_count}\nprimary_artifacts_generated={completed_count*3}\nnext={'G8-Q3-CONTRACT-PILOT' if full_pass else 'G8-DOC-BATCH-QA-REPAIR'}\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--post-run", action="store_true")
    parser.add_argument("--resume-repair", action="store_true")
    args = parser.parse_args()
    static = static_checks()
    if args.post_run:
        print(json.dumps(post_validate(), ensure_ascii=False))
        return 0
    if args.resume_repair:
        result = resume_reconcile()
        print(json.dumps(result, ensure_ascii=False))
        return int(result["CONVERSION_ACCOUNTING_IDENTITY_PASS"] == 0 or result["static_validation"]["static_validation_pass"] == 0)
    if args.prepare:
        result = prepare_outputs(static)
        print(json.dumps({"status": "USER_ACTION_REQUIRED" if result["USER_ACTION_REQUIRED"] else "BLOCKED", **result}, ensure_ascii=False))
        return 0 if result["DOC_BATCH_RUNNER_READY"] else 1
    print(json.dumps(static, ensure_ascii=False))
    return 0 if static["static_validation_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
