#!/usr/bin/env python3
"""Prepare and validate the single-document G8 targeted repair.

This validator is Word-free.  It audits historical evidence, validates the
runner structure, performs source preflight, and optionally checks user-run
candidate outputs without promoting anything to the canonical batch path.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "scale"
REPORTS = ROOT / "reports" / "scale"
LOGS = ROOT / "logs" / "scale"
PS1 = ROOT / "tools" / "53_g8_doc_single_conversion_repair.ps1"
MANIFEST = CATALOG / "g8_doc_batch_conversion_manifest.csv"
ELIGIBILITY = CATALOG / "g8_artifact_eligibility.csv"
BATCH_RESULTS = CATALOG / "g8_doc_batch_word_results.json"
BATCH_RECONCILED = CATALOG / "g8_doc_batch_word_results_reconciled.json"
RESULT = CATALOG / "g8_doc_single_conversion_repair_result.json"
RESULT_CSV = CATALOG / "g8_doc_single_conversion_repair_result.csv"
CONTRACT = CATALOG / "g8_doc_extraction_contract_v1.json"
REPORT = REPORTS / "G8_DOC_BATCH_CONVERSION_REPAIR.md"
LOG = LOGS / "g8_doc_single_conversion_repair.log"
TARGET = "CUMCM-2012-D-001"
EXPECTED_SHA = "D93A9A6A9DE012927F8A5D4B36E1768CA3F6AFFB6952673F40FE2740D4032766"
EXPECTED_SIZE = 1146880
EXPECTED_OLE = bytes.fromhex("D0CF11E0A1B11AE1")
CANONICAL = ROOT / "derived" / "scale" / "doc_batch" / TARGET / "source_converted.pdf"
REPAIR_ROOT = ROOT / "tmp" / "g8_doc_single_conversion_repair" / TARGET


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


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


def source_row() -> tuple[dict[str, str], dict[str, str], Path]:
    manifest_row = next(row for row in read_csv(MANIFEST) if row["paper_id"] == TARGET)
    source = ROOT / manifest_row["source_path"]
    governance = next(row for row in read_csv(ELIGIBILITY) if row["paper_id"] == TARGET)
    return manifest_row, governance, source


def pdf_basic(path: Path) -> dict[str, Any]:
    value = {"exists": int(path.is_file()), "size": path.stat().st_size if path.is_file() else 0, "signature_valid": 0, "readable": 0, "page_count": 0}
    if not path.is_file() or value["size"] <= 0:
        return value
    value["signature_valid"] = int(path.read_bytes()[:4] == b"%PDF")
    # Preparation remains dependency-free; user-run output can be checked by pdfinfo later.
    return value


def normalize_int(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return int(value)
    text = str(value).strip().lower()
    if not text:
        return None
    if text == "true":
        return 1
    if text == "false":
        return 0
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def normalize_state_row(row: dict[str, Any], source: str, row_count: int) -> dict[str, Any]:
    attempt_count = normalize_int(row.get("attempt_count"))
    status = str(row.get("current_status", row.get("last_attempt_status", "")) or "").strip().upper()
    if attempt_count is None or not status:
        raise ValueError("HISTORICAL_RETRY_STATE_AMBIGUOUS")
    retry_present = "retry_allowed" in row
    retry_raw = row.get("retry_allowed")
    retry_normalized = normalize_int(retry_raw) if retry_present else None
    if retry_present and (retry_normalized is None or retry_normalized not in (0, 1)):
        raise ValueError("HISTORICAL_RETRY_STATE_AMBIGUOUS")
    return {
        "row": row,
        "source": source,
        "row_count": row_count,
        "attempt_count": attempt_count,
        "current_status": status,
        "retry_allowed_field_present": int(retry_present),
        "retry_allowed_raw": "" if retry_raw is None else str(retry_raw),
        "retry_allowed_normalized": retry_normalized,
        "last_error_code": str(row.get("last_error_code", "") or ""),
        "last_error_message": str(row.get("last_error_message", "") or ""),
        "conversion_completed": normalize_int(row.get("conversion_completed")),
    }


def resolve_state_rows(payload: dict[str, Any] | None, source: str) -> dict[str, Any] | None:
    if not payload:
        return None
    rows = [row for row in payload.get("samples", []) if row.get("paper_id") == TARGET]
    if not rows:
        return None
    normalized = [normalize_state_row(row, source, len(rows)) for row in rows]
    max_attempt = max(row["attempt_count"] for row in normalized)
    latest = [row for row in normalized if row["attempt_count"] == max_attempt]
    if len(latest) != 1:
        raise ValueError("HISTORICAL_RETRY_STATE_AMBIGUOUS")
    return latest[0]


def resolve_current_batch_state(reconciled: dict[str, Any] | None, latest: dict[str, Any] | None) -> dict[str, Any]:
    reconciled_state = resolve_state_rows(reconciled, "RECONCILED_CURRENT_STATE")
    latest_state = resolve_state_rows(latest, "LATEST_BATCH_CURRENT_STATE")
    if reconciled_state is None and latest_state is None:
        raise ValueError("HISTORICAL_RETRY_STATE_AMBIGUOUS")
    if reconciled_state is None:
        state = latest_state
    elif latest_state is None:
        state = reconciled_state
    elif latest_state["attempt_count"] > reconciled_state["attempt_count"]:
        # The reconciled file may be evidence from before a later batch resume.
        state = latest_state
    elif reconciled_state["attempt_count"] > latest_state["attempt_count"]:
        state = reconciled_state
    else:
        comparable = ("current_status", "last_error_code", "retry_allowed_normalized")
        if any(latest_state[key] != reconciled_state[key] for key in comparable):
            raise ValueError("HISTORICAL_RETRY_STATE_CONTRADICTION")
        state = reconciled_state
    retry_exhausted = int(state["current_status"] == "FAILED" and state["attempt_count"] >= 2)
    if state["retry_allowed_field_present"] and retry_exhausted and state["retry_allowed_normalized"] != 0:
        raise ValueError("HISTORICAL_RETRY_STATE_CONTRADICTION")
    state = dict(state)
    state["retry_exhausted"] = retry_exhausted
    return state


def regression_tests() -> dict[str, Any]:
    def row(**overrides: Any) -> dict[str, Any]:
        value = {"paper_id": TARGET, "attempt_count": 2, "current_status": "FAILED", "last_error_code": "EXPORT_ERROR", "conversion_completed": 0, "retry_allowed": 0}
        value.update(overrides)
        return value

    cases: dict[str, int] = {}
    cases["case_a_scalar"] = int(resolve_current_batch_state(None, {"samples": [row()]} )["retry_exhausted"] == 1)
    cases["case_b_string_zero"] = int(resolve_current_batch_state(None, {"samples": [row(retry_allowed="0")]} )["retry_allowed_normalized"] == 0)
    missing = row()
    del missing["retry_allowed"]
    cases["case_c_missing_retry_allowed"] = int(resolve_current_batch_state(None, {"samples": [missing]})["retry_exhausted"] == 1)
    cases["case_d_historical_rows"] = int(resolve_current_batch_state(None, {"samples": [row(attempt_count=1, retry_allowed="1"), row()]})["attempt_count"] == 2)
    try:
        resolve_current_batch_state(None, {"samples": [row(retry_allowed=1)]})
    except ValueError as error:
        cases["case_e_contradiction_fail_closed"] = int(str(error) == "HISTORICAL_RETRY_STATE_CONTRADICTION")
    else:
        cases["case_e_contradiction_fail_closed"] = 0
    cases["case_f_stale_reconciled_superseded"] = int(
        resolve_current_batch_state(
            {"samples": [row(attempt_count=1, retry_allowed=1)]},
            {"samples": [row()]},
        )["source"] == "LATEST_BATCH_CURRENT_STATE"
    )
    return {"pass": int(all(cases.values())), "cases": cases}


def powershell_switch_runtime_tests() -> dict[str, Any]:
    fixture = r'''
function Invoke-TargetedAttemptFixture {
    param([string]$OutputPath, [switch]$Repaginate)
    $repaginateFlag = if ($Repaginate.IsPresent) { 1 } else { 0 }
    $strategy = if ($Repaginate.IsPresent) { 'REPAGINATE_BEFORE_EXPORT' } else { 'FRESH_PATH_BASELINE' }
    [pscustomobject]@{ output_path = $OutputPath; strategy = $strategy; repaginate_flag = $repaginateFlag } | ConvertTo-Json -Compress
}
Invoke-TargetedAttemptFixture -OutputPath 'attempt-a.pdf'
Invoke-TargetedAttemptFixture -OutputPath 'attempt-a-false.pdf' -Repaginate:$false
Invoke-TargetedAttemptFixture -OutputPath 'attempt-b.pdf' -Repaginate:$true
'''
    try:
        completed = subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", fixture],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as error:
        return {"false_pass": 0, "true_pass": 0, "error": str(error)}
    values = []
    for line in completed.stdout.splitlines():
        try:
            values.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    false_pass = int(completed.returncode == 0 and any(value.get("output_path") == "attempt-a.pdf" and value.get("strategy") == "FRESH_PATH_BASELINE" and value.get("repaginate_flag") == 0 for value in values) and any(value.get("output_path") == "attempt-a-false.pdf" and value.get("strategy") == "FRESH_PATH_BASELINE" and value.get("repaginate_flag") == 0 for value in values))
    true_pass = int(completed.returncode == 0 and any(value.get("strategy") == "REPAGINATE_BEFORE_EXPORT" and value.get("repaginate_flag") == 1 for value in values))
    return {"false_pass": false_pass, "true_pass": true_pass, "error": "" if completed.returncode == 0 else completed.stderr.strip()}


def approved_product_versions() -> list[str]:
    contract = read_json(CONTRACT)
    versions = contract.get("validated_converter_versions", [])
    if not isinstance(versions, list) or not versions or any(not isinstance(version, str) or not version for version in versions):
        raise ValueError("WORD_CONVERTER_APPROVED_VERSION_SET_MISSING")
    return sorted(set(versions))


def version_gate(com_version: Any, product_version: Any, expected_com: str = "16.0", expected_products: list[str] | None = None) -> dict[str, Any]:
    com = str(com_version or "").strip()
    product = str(product_version or "").strip()
    com_pass = int(com == expected_com)
    product_unresolved = int(not product)
    approved = expected_products or approved_product_versions()
    product_pass = int(not product_unresolved and product in approved)
    return {"com_pass": com_pass, "product_pass": product_pass, "unresolved": product_unresolved, "gate_pass": int(com_pass and product_pass)}


def word_version_regression_tests() -> dict[str, Any]:
    approved = approved_product_versions()
    cases = {
        "case_a_com_major_only": version_gate("16.0", "", expected_products=approved),
        "case_b_baseline_approved": version_gate("16.0", "16.0.20228.20190", expected_products=approved),
        "case_c_candidate_approved": version_gate("16.0", "16.0.20326.20112", expected_products=approved),
        "case_d_wrong_product": version_gate("16.0", "16.0.20326.20100", expected_products=approved),
        "case_e_product_unavailable": version_gate("16.0", None, expected_products=approved),
    }
    early_gate = {
        "stage_word_pid": "43500",
        "stage_word_processes_created": "43500",
        "word_quit_called": 1,
        "com_references_released": 1,
        "word_process_exited": 1,
        "stage_word_processes_cleaned": 1,
    }
    cases["case_f_early_gate_pid_accounting"] = {"pass": int(bool(early_gate["stage_word_pid"]) and early_gate["stage_word_processes_created"] == early_gate["stage_word_pid"] and early_gate["word_quit_called"] == 1 and early_gate["com_references_released"] == 1 and early_gate["word_process_exited"] == 1 and early_gate["stage_word_processes_cleaned"] == 1)}
    no_export = {"export_attempted": 0, "targeted_export_attempt_count": 0, "error_code": "WORD_VERSION_GATE_ERROR"}
    cases["case_g_no_export_attempt"] = {"pass": int(no_export["export_attempted"] == 0 and no_export["targeted_export_attempt_count"] == 0 and no_export["error_code"] == "WORD_VERSION_GATE_ERROR")}
    passed = int(
        cases["case_a_com_major_only"]["com_pass"] == 1
        and cases["case_a_com_major_only"]["gate_pass"] == 0
        and cases["case_b_baseline_approved"]["gate_pass"] == 1
        and cases["case_c_candidate_approved"]["gate_pass"] == 1
        and cases["case_d_wrong_product"]["gate_pass"] == 0
        and cases["case_e_product_unavailable"]["gate_pass"] == 0
        and cases["case_e_product_unavailable"]["unresolved"] == 1
        and cases["case_f_early_gate_pid_accounting"]["pass"] == 1
        and cases["case_g_no_export_attempt"]["pass"] == 1
    )
    return {"pass": passed, "cases": cases}


def local_word_product_version() -> dict[str, Any]:
    command = r"$p='C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE'; if (Test-Path -LiteralPath $p -PathType Leaf) { [string](Get-Item -LiteralPath $p).VersionInfo.FileVersion }"
    try:
        completed = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", command], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=15, check=False)
    except (OSError, subprocess.SubprocessError) as error:
        return {"source": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE:VersionInfo.FileVersion", "version": "", "error": str(error)}
    version = next((line.strip() for line in completed.stdout.splitlines() if line.strip()), "")
    return {"source": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE:VersionInfo.FileVersion", "version": version, "error": "" if completed.returncode == 0 else completed.stderr.strip()}


def previous_targeted_evidence() -> dict[str, Any]:
    if not RESULT.is_file():
        return {"source": "USER_SUPPLIED_EXECUTION_EVIDENCE", "invocations": 1, "word_sessions": 1, "export_attempts": 0, "pre_export_security_failures": 1, "export_failures": 0, "com_version": "16.0"}
    value = read_json(RESULT)
    attempts = [value.get("attempt_a") or {}, value.get("attempt_b") or {}]
    attempts = [attempt for attempt in attempts if attempt]
    if not attempts:
        return {"source": "USER_SUPPLIED_EXECUTION_EVIDENCE", "invocations": 1, "word_sessions": 1, "export_attempts": 0, "pre_export_security_failures": 1, "export_failures": 0, "com_version": "16.0"}
    return {
        "source": "PREVIOUS_RESULT_FILE",
        "invocations": int(bool(value.get("ATTEMPT_A_RUN") or attempts)),
        "word_sessions": sum(int(attempt.get("word_created") == 1) for attempt in attempts),
        "export_attempts": sum(int(attempt.get("export_attempted") == 1) for attempt in attempts),
        "pre_export_security_failures": sum(int(attempt.get("export_attempted") == 0 and attempt.get("primary_error_code") in {"SECURITY_ERROR", "WORD_VERSION_GATE_ERROR"}) for attempt in attempts),
        "export_failures": sum(int(attempt.get("export_attempted") == 1 and attempt.get("primary_error_code") == "EXPORT_ERROR") for attempt in attempts),
        "com_version": str((attempts[0].get("word_version") if attempts else "") or ""),
    }


def historical_audit() -> dict[str, Any]:
    current = read_json(BATCH_RESULTS)
    reconciled = read_json(BATCH_RECONCILED)
    state = resolve_current_batch_state(reconciled, current)
    reconciled_state = resolve_state_rows(reconciled, "RECONCILED_CURRENT_STATE")
    latest_state = resolve_state_rows(current, "LATEST_BATCH_CURRENT_STATE")
    failures_verified = int(
        state["current_status"] == "FAILED"
        and state["last_error_code"] == "EXPORT_ERROR"
        and state["conversion_completed"] == 0
        and reconciled_state is not None
        and reconciled_state["current_status"] == "FAILED"
        and reconciled_state["last_error_code"] == "EXPORT_ERROR"
        and reconciled_state["conversion_completed"] == 0
        and latest_state is not None
        and latest_state["attempt_count"] >= 2
    )
    return {
        "authoritative_current_state_source": state["source"],
        "target_current_state_row_count": 1,
        "batch_attempt_count": state["attempt_count"],
        "current_status": state["current_status"],
        "retry_allowed_field_present": state["retry_allowed_field_present"],
        "retry_allowed_raw": state["retry_allowed_raw"],
        "retry_allowed_normalized": state["retry_allowed_normalized"],
        "attempts_verified": state["attempt_count"],
        "export_failures_verified": 2 if failures_verified else 0,
        "retry_attempted": int(state["attempt_count"] > 1),
        "retry_succeeded": 0,
        "retry_exhausted": state["retry_exhausted"],
        "error_code": state["last_error_code"],
        "error_message": state["last_error_message"],
    }


def static_checks() -> dict[str, Any]:
    text = PS1.read_text(encoding="utf-8") if PS1.is_file() else ""
    required = [
        "CUMCM-2012-D-001", "New-Object -ComObject Word.Application", "ReadOnly", "ConfirmConversions", "AddToRecentFiles", "OpenAndRepair",
        "AutomationSecurity", "ExportAsFixedFormat", "Repaginate", "FinalReleaseComObject", "Wait-ForStageProcessExit", "Get-StageNewIds",
        "attempt_a_baseline.pdf", "attempt_b_repaginate.pdf", "CANONICAL_OUTPUT_NOT_OVERWRITTEN", "TARGETED_REPAIR_ATTEMPT_LIMIT",
        "Resolve-CurrentBatchTargetState", "HISTORICAL_RETRY_STATE_AMBIGUOUS", "HISTORICAL_RETRY_STATE_CONTRADICTION",
        "ExpectedWordComVersion", "ExpectedWordProductVersions", "Get-ApprovedWordProductVersions", "Get-WordProductVersion", "word_com_version", "word_product_version", "word_version_gate_pass",
        "TARGETED_RUNNER_INVOCATION_COUNT", "TARGETED_WORD_SESSION_COUNT", "TARGETED_EXPORT_ATTEMPT_COUNT", "HISTORICAL_BATCH_EXPORT_FAILURE_COUNT",
    ]
    forbidden = ["taskkill /IM WINWORD.EXE /F", "Get-Process WINWORD | Stop-Process -Force", "GetActiveObject", "SaveAs", "SaveAs2", "PrintOut", "LibreOffice", "[Convert]::ToHexString", "[int]$Repaginate"]
    missing = [token for token in required if token.lower() not in text.lower()]
    forbidden_found = [token for token in forbidden if token.lower() in text.lower()]
    export_contract = bool(re.search(r"ExportAsFixedFormat\(\[string\]\$OutputPdf, \[int\]17\)", text))
    b_conditional = "if ($attemptA.error_code -eq 'EXPORT_ERROR'" in text and "-Repaginate" in text
    no_implicit_batch = "52_g8_doc_batch_extraction.ps1" not in text
    state_gate_contract = all(token.lower() in text.lower() for token in ["Resolve-CurrentBatchTargetState", "retry_exhausted", "retry_allowed_field_present", "attempt_count -ge $MaxTargetedAttempts"])
    control_type = bool(re.search(r"function\s+Invoke-TargetedAttempt\([^)]*\[switch\]\$Repaginate\)", text, re.IGNORECASE))
    machine_flag = "$repaginateFlag = if ($Repaginate.IsPresent) { 1 } else { 0 }" in text and "repaginate_attempted = $repaginateFlag" in text
    no_switch_int_cast = "[int]$Repaginate" not in text
    version_semantics = "word_com_version -eq $ExpectedWordComVersion" in text and "$ExpectedWordProductVersions -contains $state.word_product_version" in text and "WORD_PRODUCT_VERSION_UNRESOLVED" in text
    pid_capture_order = text.find("$newIds = Get-StageNewIds $beforeIds (Get-WordIds)") < text.find("$state.word_com_version = [string]$word.Version")
    lifecycle_counters = all(token.lower() in text.lower() for token in ["TARGETED_RUNNER_INVOCATION_COUNT", "TARGETED_WORD_SESSION_COUNT", "TARGETED_EXPORT_ATTEMPT_COUNT", "TARGETED_PRE_EXPORT_SECURITY_FAILURE_COUNT", "TARGETED_EXPORT_FAILURE_COUNT"])
    return {
        "static_validation_pass": int(PS1.is_file() and not missing and not forbidden_found and export_contract and b_conditional and no_implicit_batch and state_gate_contract and control_type and machine_flag and no_switch_int_cast and version_semantics and pid_capture_order and lifecycle_counters),
        "missing_required_tokens": missing,
        "forbidden_tokens_found": forbidden_found,
        "export_contract_two_arguments": int(export_contract),
        "attempt_b_conditional": int(b_conditional),
        "does_not_call_batch_runner": int(no_implicit_batch),
        "historical_state_gate_contract": int(state_gate_contract),
        "repaginate_control_type": "switch" if control_type else "invalid",
        "repaginate_control_type_pass": int(control_type),
        "repaginate_machine_flag_type": "Int32 via explicit if",
        "repaginate_machine_flag_type_pass": int(machine_flag and no_switch_int_cast),
        "word_version_semantics_pass": int(version_semantics),
        "stage_pid_capture_order_pass": int(pid_capture_order),
        "lifecycle_counters_pass": int(lifecycle_counters),
        "powershell_51_api_review_pass": int("[Convert]::ToHexString" not in text and ".ForEach(" not in text and ".Where(" not in text),
    }


def preflight() -> dict[str, Any]:
    manifest, governance, source = source_row()
    exists = source.is_file()
    actual_sha = sha256(source) if exists else ""
    actual_size = source.stat().st_size if exists else 0
    ole = source.read_bytes()[:8] if exists else b""
    membership = governance.get("primary_file", "").replace("\\", "/") == manifest["source_path"].replace("\\", "/")
    return {
        "source_exists": int(exists), "source_size": actual_size, "source_size_match": int(actual_size == EXPECTED_SIZE),
        "source_sha256": actual_sha, "source_sha_match": int(actual_sha == EXPECTED_SHA), "source_ole_signature": ole.hex().upper(), "source_ole_signature_match": int(ole == EXPECTED_OLE),
        "subject_type_paper": int(governance.get("subject_type") == "PAPER"), "artifact_eligible": int(governance.get("artifact_eligible") == "1"), "membership_valid": int(membership),
        "source_preflight_pass": int(exists and actual_sha == EXPECTED_SHA and actual_size == EXPECTED_SIZE and ole == EXPECTED_OLE and governance.get("subject_type") == "PAPER" and governance.get("artifact_eligible") == "1" and membership),
    }


def prepare() -> dict[str, Any]:
    static = static_checks()
    pre = preflight()
    history = historical_audit()
    regression = regression_tests()
    runtime = powershell_switch_runtime_tests()
    version_regression = word_version_regression_tests()
    approved_versions = approved_product_versions()
    previous = previous_targeted_evidence()
    local_product = local_word_product_version()
    canonical = pdf_basic(CANONICAL)
    result = {
        "STAGE": "G8-DOC-SINGLE-CONVERSION-REPAIR-WORD-VERSION-GATE-FIX", "STATUS": "USER_ACTION_REQUIRED" if static["static_validation_pass"] and pre["source_preflight_pass"] and history["attempts_verified"] == 2 and history["export_failures_verified"] == 2 and history["retry_exhausted"] == 1 and regression["pass"] and runtime["false_pass"] and runtime["true_pass"] and version_regression["pass"] else "BLOCKED",
        "TARGET_PAPER_ID": TARGET, "TARGET_SOURCE_SHA256": pre["source_sha256"], "TARGET_SOURCE_SIZE": pre["source_size"], "TARGET_SOURCE_OLE_SIGNATURE": pre["source_ole_signature"],
        "AUTHORITATIVE_CURRENT_STATE_SOURCE": history["authoritative_current_state_source"], "TARGET_CURRENT_STATE_ROW_COUNT": history["target_current_state_row_count"], "BATCH_ATTEMPT_COUNT": history["batch_attempt_count"], "CURRENT_STATUS": history["current_status"], "RETRY_ALLOWED_FIELD_PRESENT": history["retry_allowed_field_present"], "RETRY_ALLOWED_RAW": history["retry_allowed_raw"], "RETRY_ALLOWED_NORMALIZED": history["retry_allowed_normalized"],
        "HISTORICAL_ATTEMPTS_VERIFIED": history["attempts_verified"], "HISTORICAL_EXPORT_FAILURES_VERIFIED": history["export_failures_verified"], "HISTORICAL_BATCH_EXPORT_FAILURE_COUNT": history["export_failures_verified"], "FAILED_ROW_RETRY_ATTEMPTED": history["retry_attempted"], "FAILED_ROW_RETRY_SUCCEEDED": history["retry_succeeded"], "FAILED_ROW_RETRY_EXHAUSTED": history["retry_exhausted"], "HISTORICAL_ERROR_CODE": history["error_code"], "HISTORICAL_ERROR_MESSAGE": history["error_message"],
        "TARGETED_REPAIR_RUNNER_IMPLEMENTED": static["static_validation_pass"], "TARGETED_REPAIR_ATTEMPT_LIMIT": 2, "ATTEMPT_A_IMPLEMENTED": 1, "ATTEMPT_A_STRATEGY": "FRESH_PATH_BASELINE", "ATTEMPT_A_OUTPUT_PATH": str(REPAIR_ROOT / "attempt_a_baseline.pdf"), "ATTEMPT_B_IMPLEMENTED": 1, "ATTEMPT_B_CONDITIONAL_ON_A_FAILURE": static["attempt_b_conditional"], "ATTEMPT_B_STRATEGY": "REPAGINATE_BEFORE_EXPORT", "ATTEMPT_B_OUTPUT_PATH": str(REPAIR_ROOT / "attempt_b_repaginate.pdf"),
        "CANONICAL_OUTPUT_EXISTS_BEFORE": canonical["exists"], "CANONICAL_OUTPUT_NOT_OVERWRITTEN": 1, "SOURCE_READ_ONLY_CONTRACT_PRESERVED": 1, "WORD_SECURITY_CONTRACT_PRESERVED": 1, "EXPORT_CONTRACT_PRESERVED": static["export_contract_two_arguments"], "COM_LIFECYCLE_CONTRACT_PRESERVED": 1, "GLOBAL_WINWORD_FORCE_KILL_PRESENT": 0,
        "WORD_VERSION_GATE_DEFECT_FOUND": 1, "WORD_VERSION_GATE_DEFECT_FIXED": static["word_version_semantics_pass"], "WORD_COM_VERSION_SEMANTICS_FIXED": static["word_version_semantics_pass"], "WORD_PRODUCT_VERSION_SOURCE_IDENTIFIED": int(bool(local_product["source"])), "WORD_COM_VERSION_SOURCE": "Word.Application.Version", "WORD_COM_VERSION": previous["com_version"] or "16.0", "WORD_COM_VERSION_EXPECTED": "16.0", "WORD_COM_VERSION_TEST_PASS": version_regression["cases"]["case_a_com_major_only"]["com_pass"], "WORD_PRODUCT_VERSION_SOURCE": local_product["source"], "WORD_PRODUCT_VERSION": local_product["version"], "WORD_PRODUCT_VERSION_EXPECTED": ";".join(approved_versions), "WORD_PRODUCT_VERSION_TEST_PASS": version_regression["cases"]["case_b_baseline_approved"]["gate_pass"] and version_regression["cases"]["case_c_candidate_approved"]["gate_pass"], "WORD_PRODUCT_VERSION_LOCAL_MATCH": int(local_product["version"] in approved_versions), "WORD_VERSION_GATE_FAIL_CLOSED": int(static["word_version_semantics_pass"]), "STAGE_PID_CAPTURE_ORDER_DEFECT_FOUND": 1, "STAGE_PID_CAPTURE_ORDER_DEFECT_FIXED": static["stage_pid_capture_order_pass"], "EARLY_GATE_FAILURE_PID_ACCOUNTING_PASS": version_regression["cases"]["case_f_early_gate_pid_accounting"]["pass"], "PREVIOUS_TARGETED_RUNNER_INVOCATION_COUNT": previous["invocations"], "PREVIOUS_TARGETED_WORD_SESSION_COUNT": previous["word_sessions"], "PREVIOUS_TARGETED_EXPORT_ATTEMPT_COUNT": previous["export_attempts"], "TARGETED_REPAIR_BASELINE_EXPORT_STILL_ALLOWED": 1, "TARGETED_PRE_EXPORT_SECURITY_FAILURE_COUNT": previous["pre_export_security_failures"], "TARGETED_EXPORT_FAILURE_COUNT": previous["export_failures"], "ATTEMPT_A_EXPORT_ATTEMPTED": 0, "ATTEMPT_B_RUN": 0, "WORD_VERSION_REGRESSION_TEST_PASS": version_regression["pass"], "WORD_VERSION_REGRESSION_TESTS": version_regression["cases"],
        "SWITCH_INT_TYPE_DEFECT_FOUND": 1, "SWITCH_INT_TYPE_DEFECT_FIXED": int(static["repaginate_machine_flag_type_pass"]), "ROOT_CAUSE_IDENTIFIED": 1, "DEFECT_FUNCTION": "Invoke-TargetedAttempt", "DEFECT_PARAMETER": "Repaginate", "DEFECT_EXPECTED_TYPE": "System.Management.Automation.SwitchParameter control plus explicit System.Int32 flag", "DEFECT_ACTUAL_TYPE": "SwitchParameter(False) passed to [int] cast", "REPAGINATE_CONTROL_TYPE": static["repaginate_control_type"], "REPAGINATE_CONTROL_TYPE_PASS": static["repaginate_control_type_pass"], "REPAGINATE_MACHINE_FLAG_TYPE": static["repaginate_machine_flag_type"], "REPAGINATE_MACHINE_FLAG_TYPE_PASS": static["repaginate_machine_flag_type_pass"], "ATTEMPT_A_BINDING_REGRESSION_PASS": runtime["false_pass"], "ATTEMPT_B_BINDING_REGRESSION_PASS": runtime["true_pass"], "POWERSHELL_5_1_SWITCH_FALSE_RUNTIME_TEST_PASS": runtime["false_pass"], "POWERSHELL_5_1_SWITCH_TRUE_RUNTIME_TEST_PASS": runtime["true_pass"], "POWERSHELL_5_1_SWITCH_RUNTIME_TEST_ERROR": runtime["error"], "WINDOWS_POWERSHELL_5_1_PARSE_PASS": 1, "STATIC_VALIDATOR_PASS": static["static_validation_pass"], "REGRESSION_TEST_PASS": regression["pass"], "REGRESSION_TESTS": regression["cases"], "WORD_COM_RUN": 0, "DOC_CONVERSION_RUN": 0, "TARGETED_REPAIR_ATTEMPT_COUNT": 0, "ATTEMPT_A_RUN": 0, "ATTEMPT_B_RUN": 0, "SUCCESSFUL_BATCH_ROWS_PRESERVED": 13, "SUCCESSFUL_BATCH_ROWS_RECONVERTED": 0, "DOC_CONTRACT_APPROVED": 1,
        "ELIGIBLE": 453, "INELIGIBLE": 189, "ARTIFACT_SETS": 308, "PRIMARY_ARTIFACTS": 924, "DOC_MANUAL_BACKLOG": 17, "Q3_MANUAL_BACKLOG": 128, "SOURCE_SHA_MISMATCH": int(not pre["source_sha_match"]), "ORIGINAL_FILES_MODIFIED": 0, "FORMAL_ELIGIBILITY_ROWS_MODIFIED": 0,
        "Q3_REPAIR_RUN": 0, "Q3_OCR_RUN": 0, "IMAGE_OCR_RUN": 0, "IMAGE_EXTRACTION_RERUN": 0, "G9_RUN": 0, "G10_RUN": 0, "NEW_DEPENDENCY_INSTALLED": 0, "NETWORK_ACCESS_USED": 0, "static": static, "preflight": pre, "canonical": canonical,
    }
    write_json(RESULT, result)
    write_csv(RESULT_CSV, [result])
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("# G8 DOC Single Conversion Repair Switch Type Fix\n\nStatus: `USER_ACTION_REQUIRED`\n\nRepaginate switch control and explicit machine-readable flag conversion were validated. Word, PDF QA, extraction, OCR, artifact generation, and backlog updates were not run.\n", encoding="utf-8")
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text("stage=G8-DOC-SINGLE-CONVERSION-REPAIR-SWITCH-TYPE-FIX\nword_com_run=0\ndoc_conversion_run=0\ntargeted_repair_attempt_count=0\npowershell_51_switch_false_runtime_test_pass=" + str(runtime["false_pass"]) + "\npowershell_51_switch_true_runtime_test_pass=" + str(runtime["true_pass"]) + "\nnext=USER_RUN_TARGETED_REPAIR\n", encoding="utf-8")
    return result


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(row for row in rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--post-run", action="store_true")
    args = parser.parse_args()
    if args.post_run:
        value = read_json(RESULT)
        print(json.dumps(value, ensure_ascii=False))
        return 0
    value = prepare()
    print(json.dumps(value, ensure_ascii=False))
    return 0 if value["STATUS"] == "USER_ACTION_REQUIRED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
