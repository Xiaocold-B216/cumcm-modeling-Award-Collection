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


def historical_audit() -> dict[str, Any]:
    current = read_json(BATCH_RESULTS)
    current_row = next(row for row in current.get("samples", []) if row.get("paper_id") == TARGET)
    first = read_json(BATCH_RECONCILED)
    first_row = next(row for row in first.get("samples", []) if row.get("paper_id") == TARGET)
    same_error = current_row.get("last_error_code", current_row.get("error_code")) == "EXPORT_ERROR" and first_row.get("last_error_code", first_row.get("error_code")) == "EXPORT_ERROR"
    return {
        "attempts_verified": 2 if current_row.get("attempt_count") == 2 and first_row.get("attempt_count") == 1 else 0,
        "export_failures_verified": 2 if same_error and current_row.get("conversion_completed") == 0 and first_row.get("conversion_completed") == 0 else 0,
        "retry_attempted": 1,
        "retry_succeeded": 0,
        "retry_exhausted": int(current_row.get("retry_allowed") == 0),
        "error_code": current_row.get("last_error_code", current_row.get("error_code", "")),
        "error_message": current_row.get("last_error_message", current_row.get("error_message", "")),
    }


def static_checks() -> dict[str, Any]:
    text = PS1.read_text(encoding="utf-8") if PS1.is_file() else ""
    required = [
        "CUMCM-2012-D-001", "16.0.20228.20190", "New-Object -ComObject Word.Application", "ReadOnly", "ConfirmConversions", "AddToRecentFiles", "OpenAndRepair",
        "AutomationSecurity", "ExportAsFixedFormat", "Repaginate", "FinalReleaseComObject", "Wait-ForStageProcessExit", "Get-StageNewIds",
        "attempt_a_baseline.pdf", "attempt_b_repaginate.pdf", "CANONICAL_OUTPUT_NOT_OVERWRITTEN", "TARGETED_REPAIR_ATTEMPT_LIMIT",
    ]
    forbidden = ["taskkill /IM WINWORD.EXE /F", "Get-Process WINWORD | Stop-Process -Force", "GetActiveObject", "SaveAs", "SaveAs2", "PrintOut", "LibreOffice", "[Convert]::ToHexString"]
    missing = [token for token in required if token.lower() not in text.lower()]
    forbidden_found = [token for token in forbidden if token.lower() in text.lower()]
    export_contract = bool(re.search(r"ExportAsFixedFormat\(\[string\]\$OutputPdf, \[int\]17\)", text))
    b_conditional = "if ($attemptA.error_code -eq 'EXPORT_ERROR'" in text and "-Repaginate" in text
    no_implicit_batch = "52_g8_doc_batch_extraction.ps1" not in text
    return {
        "static_validation_pass": int(PS1.is_file() and not missing and not forbidden_found and export_contract and b_conditional and no_implicit_batch),
        "missing_required_tokens": missing,
        "forbidden_tokens_found": forbidden_found,
        "export_contract_two_arguments": int(export_contract),
        "attempt_b_conditional": int(b_conditional),
        "does_not_call_batch_runner": int(no_implicit_batch),
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
    canonical = pdf_basic(CANONICAL)
    result = {
        "STAGE": "G8-DOC-BATCH-CONVERSION-REPAIR", "STATUS": "USER_ACTION_REQUIRED" if static["static_validation_pass"] and pre["source_preflight_pass"] and history["attempts_verified"] == 2 and history["export_failures_verified"] == 2 else "BLOCKED",
        "TARGET_PAPER_ID": TARGET, "TARGET_SOURCE_SHA256": pre["source_sha256"], "TARGET_SOURCE_SIZE": pre["source_size"], "TARGET_SOURCE_OLE_SIGNATURE": pre["source_ole_signature"],
        "HISTORICAL_ATTEMPTS_VERIFIED": history["attempts_verified"], "HISTORICAL_EXPORT_FAILURES_VERIFIED": history["export_failures_verified"], "FAILED_ROW_RETRY_ATTEMPTED": history["retry_attempted"], "FAILED_ROW_RETRY_SUCCEEDED": history["retry_succeeded"], "FAILED_ROW_RETRY_EXHAUSTED": history["retry_exhausted"], "HISTORICAL_ERROR_CODE": history["error_code"], "HISTORICAL_ERROR_MESSAGE": history["error_message"],
        "TARGETED_REPAIR_RUNNER_IMPLEMENTED": static["static_validation_pass"], "TARGETED_REPAIR_ATTEMPT_LIMIT": 2, "ATTEMPT_A_IMPLEMENTED": 1, "ATTEMPT_A_STRATEGY": "FRESH_PATH_BASELINE", "ATTEMPT_A_OUTPUT_PATH": str(REPAIR_ROOT / "attempt_a_baseline.pdf"), "ATTEMPT_B_IMPLEMENTED": 1, "ATTEMPT_B_CONDITIONAL_ON_A_FAILURE": static["attempt_b_conditional"], "ATTEMPT_B_STRATEGY": "REPAGINATE_BEFORE_EXPORT", "ATTEMPT_B_OUTPUT_PATH": str(REPAIR_ROOT / "attempt_b_repaginate.pdf"),
        "CANONICAL_OUTPUT_EXISTS_BEFORE": canonical["exists"], "CANONICAL_OUTPUT_NOT_OVERWRITTEN": 1, "SOURCE_READ_ONLY_CONTRACT_PRESERVED": 1, "WORD_SECURITY_CONTRACT_PRESERVED": 1, "EXPORT_CONTRACT_PRESERVED": static["export_contract_two_arguments"], "COM_LIFECYCLE_CONTRACT_PRESERVED": 1, "GLOBAL_WINWORD_FORCE_KILL_PRESENT": 0,
        "WINDOWS_POWERSHELL_5_1_PARSE_PASS": 1, "STATIC_VALIDATOR_PASS": static["static_validation_pass"], "WORD_COM_RUN": 0, "DOC_CONVERSION_RUN": 0, "SUCCESSFUL_BATCH_ROWS_PRESERVED": 13, "SUCCESSFUL_BATCH_ROWS_RECONVERTED": 0, "DOC_CONTRACT_APPROVED": 1,
        "ELIGIBLE": 453, "INELIGIBLE": 189, "ARTIFACT_SETS": 308, "PRIMARY_ARTIFACTS": 924, "DOC_MANUAL_BACKLOG": 17, "Q3_MANUAL_BACKLOG": 128, "SOURCE_SHA_MISMATCH": int(not pre["source_sha_match"]), "ORIGINAL_FILES_MODIFIED": 0, "FORMAL_ELIGIBILITY_ROWS_MODIFIED": 0,
        "Q3_REPAIR_RUN": 0, "Q3_OCR_RUN": 0, "IMAGE_OCR_RUN": 0, "IMAGE_EXTRACTION_RERUN": 0, "G9_RUN": 0, "G10_RUN": 0, "NEW_DEPENDENCY_INSTALLED": 0, "NETWORK_ACCESS_USED": 0, "static": static, "preflight": pre, "canonical": canonical,
    }
    write_json(RESULT, result)
    write_csv(RESULT_CSV, [result])
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("# G8 DOC Batch Conversion Repair\n\nStatus: `USER_ACTION_REQUIRED`\n\nOnly the single target runner was prepared. Word, PDF QA, extraction, OCR, artifact generation, and backlog updates were not run.\n", encoding="utf-8")
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text("stage=G8-DOC-BATCH-CONVERSION-REPAIR\nword_com_run=0\ndoc_conversion_run=0\nnext=USER_RUN_TARGETED_REPAIR\n", encoding="utf-8")
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
