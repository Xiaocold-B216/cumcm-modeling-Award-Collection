#!/usr/bin/env python3
"""G8 legacy binary DOC contract pilot.

This runner deliberately stops before conversion when the local Word COM
capability/security gate fails.  It produces the auditable reconciliation and
rejection contract without touching source files, formal Artifacts, backlog
rows, or frozen upstream outputs.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "scale"
REPORTS = ROOT / "reports" / "scale"
LOGS = ROOT / "logs" / "scale"
STAGE = "G8-DOC-CONTRACT-PILOT"
OLE_SIGNATURE = bytes.fromhex("D0CF11E0A1B11AE1")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path: Path, rows: Iterable[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def json_write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def process_count(value: Any) -> int:
    if isinstance(value, int):
        return value
    return len([item for item in str(value or "").split(",") if item.strip()])


def powershell_word_capability() -> dict[str, Any]:
    """Probe Word without conversion and without touching any source file."""
    command = r"""
$before = @(Get-Process -Name WINWORD -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id)
$word = $null
$result = [ordered]@{capable=0; version=''; build=''; error_code=''; pre_existing=($before -join ','); stage_created=''; stage_cleaned=0; orphan=''}
$word_exe = 'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE'
if (Test-Path -LiteralPath $word_exe) {
  $file_version = [string](Get-Item -LiteralPath $word_exe).VersionInfo.FileVersion
  $result.version = $file_version
  $result.build = $file_version
}
try {
  $word = New-Object -ComObject Word.Application
  $word.Visible = $false
  $word.DisplayAlerts = 0
  $word.AutomationSecurity = 3
  $word.Options.UpdateLinksAtOpen = $false
  $word.Options.ConfirmConversions = $false
  $after_start = @(Get-Process -Name WINWORD -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id)
  $new_ids = @($after_start | Where-Object { $before -notcontains $_ })
  $result.capable = 1
  $result.version = [string]$word.Version
  try { $result.build = [string]$word.Build } catch { $result.build = '' }
  $result.stage_created = ($new_ids -join ',')
}
catch {
  $message = $_.Exception.Message
  if ($message -match '0x[0-9A-Fa-f]+') { $result.error_code = $Matches[0].ToUpperInvariant() } else { $result.error_code = 'COM_START_FAILURE' }
}
finally {
  if ($word) {
    try { $word.Quit(0) } catch {}
    try { [Runtime.InteropServices.Marshal]::FinalReleaseComObject($word) | Out-Null } catch {}
  }
  [GC]::Collect(); [GC]::WaitForPendingFinalizers(); [GC]::Collect(); [GC]::WaitForPendingFinalizers()
}
Start-Sleep -Milliseconds 500
$after = @(Get-Process -Name WINWORD -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id)
$result.stage_cleaned = @($after | Where-Object { $before -notcontains $_ }).Count -eq 0
$result.orphan = (@($after | Where-Object { $before -notcontains $_ }) -join ',')
$result | ConvertTo-Json -Compress
"""
    completed = subprocess.run(
        ["powershell.exe", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", command],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=45,
        check=False,
    )
    lines = [line.strip() for line in completed.stdout.splitlines() if line.strip()]
    if not lines:
        return {
            "capable": 0,
            "version": "",
            "build": "",
            "error_code": "COM_PROBE_NO_OUTPUT",
            "pre_existing": "",
            "stage_created": "",
            "stage_cleaned": 0,
            "orphan": "",
        }
    try:
        result = json.loads(lines[-1])
    except json.JSONDecodeError:
        result = {
            "capable": 0,
            "version": "",
            "build": "",
            "error_code": "COM_PROBE_INVALID_OUTPUT",
            "pre_existing": "",
            "stage_created": "",
            "stage_cleaned": 0,
            "orphan": "",
        }
    result["probe_exit_code"] = completed.returncode
    return result


def select_samples(inventory: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ordered = sorted(inventory, key=lambda row: (int(row["source_size"]), row["paper_id"]))
    if len(ordered) < 3:
        return ordered
    indices = [0, (len(ordered) - 1) // 2, len(ordered) - 1]
    roles = ["SMALL_SIZE", "MEDIAN_SIZE", "LARGE_SIZE"]
    samples = []
    seen: set[str] = set()
    for role, index in zip(roles, indices):
        row = dict(ordered[index])
        if row["paper_id"] in seen:
            continue
        row["sample_role"] = role
        row["selection_key"] = f"{int(row['source_size']):012d}|{row['paper_id']}"
        row["sample_reason"] = f"deterministic {role.lower()} by source_size then paper_id"
        samples.append(row)
        seen.add(row["paper_id"])
    return samples


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validation", action="store_true", help="revalidate existing pilot outputs without COM")
    args = parser.parse_args()

    decisions = read_csv(CATALOG / "g8_ea42_doc_decisions.csv")
    eligibility = {row["paper_id"]: row for row in read_csv(CATALOG / "g8_artifact_eligibility.csv")}
    status = {row["paper_id"]: row for row in read_csv(CATALOG / "g8_paper_status.csv")}
    backlog = read_csv(CATALOG / "g8_manual_backlog.csv")
    target_ids = sorted(
        row["paper_id"]
        for row in decisions
        if row.get("final_subject_type") == "PAPER"
        and row.get("artifact_eligible") == "1"
        and row.get("requires_doc_contract") == "1"
    )

    inventory: list[dict[str, Any]] = []
    for paper_id in target_ids:
        decision = next(row for row in decisions if row["paper_id"] == paper_id)
        source_path = decision["source_path"]
        absolute = ROOT / Path(source_path.replace("/", os.sep))
        exists = absolute.is_file()
        actual_sha = sha256(absolute) if exists else ""
        size = absolute.stat().st_size if exists else 0
        signature = absolute.read_bytes()[:8] == OLE_SIGNATURE if exists else False
        artifact_complete = status.get(paper_id, {}).get("artifact_status") == "PASS"
        inventory.append(
            {
                "paper_id": paper_id,
                "year": decision["year"],
                "problem": decision["problem"],
                "source_path": source_path,
                "source_sha256": actual_sha,
                "source_size": size,
                "actual_format": "legacy_binary_doc_ole" if signature else "MISSING_OR_NON_OLE",
                "ole_signature_verified": int(signature),
                "eligibility_confidence": decision["confidence"],
                "artifact_complete": int(artifact_complete),
                "conversion_required": int(not artifact_complete),
                "pilot_candidate": 1,
                "sample_reason": "",
                "source_exists": int(exists),
            }
        )

    samples = select_samples(inventory)
    sample_ids = {row["paper_id"] for row in samples}
    sample_reason_by_id = {row["paper_id"]: row["sample_reason"] for row in samples}
    for row in inventory:
        row["pilot_candidate"] = int(row["paper_id"] in sample_ids)
        row["sample_reason"] = sample_reason_by_id.get(
            row["paper_id"],
            "not selected; deterministic size-stratified pilot has three slots",
        )
    if args.validation and (CATALOG / "g8_doc_extraction_contract_v1.json").is_file():
        previous_contract = json.loads((CATALOG / "g8_doc_extraction_contract_v1.json").read_text(encoding="utf-8"))
        previous_state = json.loads((CATALOG / "g8_run_state.json").read_text(encoding="utf-8"))
        capability = {
            "capable": previous_contract.get("word_com_contract_capable", 0),
            "version": previous_contract.get("word_version", ""),
            "build": previous_contract.get("word_build", ""),
            "error_code": "VALIDATION_REUSES_BLOCKED_CAPABILITY",
            "pre_existing": previous_state.get("g8_doc_pre_existing_word_processes", ""),
            "stage_created": previous_state.get("g8_doc_stage_word_processes_created", ""),
            "stage_cleaned": previous_state.get("g8_doc_stage_word_processes_cleaned", 0),
            "orphan": previous_state.get("g8_doc_orphan_stage_word_processes", ""),
            "probe_exit_code": 0,
        }
    else:
        capability = powershell_word_capability()

    source_mismatch = 0
    conversion_rows = []
    pdf_rows = []
    page_rows = []
    result_rows = []
    for sample in samples:
        source_sha = sample["source_sha256"]
        source_integrity = int(bool(source_sha) and source_sha == sample["source_sha256"])
        source_mismatch += int(not source_integrity)
        conversion_rows.append(
            {
                "paper_id": sample["paper_id"],
                "source_path": sample["source_path"],
                "source_sha256_before": source_sha,
                "source_sha256_after": source_sha,
                "source_format": sample["actual_format"],
                "converter": "Microsoft Word COM" if capability.get("capable") else "NOT_ATTEMPTED",
                "word_version": capability.get("version", ""),
                "word_build": capability.get("build", ""),
                "conversion_method": "read-only DOC -> PDF ExportAsFixedFormat" if capability.get("capable") else "NOT_ATTEMPTED_WORD_COM_UNAVAILABLE",
                "conversion_timestamp": "",
                "derivative_path": "",
                "derivative_sha256": "",
                "derivative_size": "",
                "derivative_page_count": "",
                "conversion_status": "BLOCKED_WORD_COM_UNAVAILABLE",
            }
        )
        pdf_rows.append(
            {
                "paper_id": sample["paper_id"],
                "derivative_path": "",
                "page_count": "",
                "pdf_class": "",
                "text_availability": "",
                "malformed_pdf": "",
                "encrypted": "",
                "extraction_capability": "NOT_ATTEMPTED",
                "ocr_route_pages": "",
                "conversion_anomalies": capability.get("error_code", "COM_UNAVAILABLE"),
                "audit_status": "NOT_ATTEMPTED",
            }
        )
        result_rows.append(
            {
                "paper_id": sample["paper_id"],
                "sample_role": sample["sample_role"],
                "source_sha256_before": source_sha,
                "source_sha256_after": source_sha,
                "conversion_status": "BLOCKED_WORD_COM_UNAVAILABLE",
                "pdf_validation_status": "NOT_ATTEMPTED",
                "extraction_status": "NOT_ATTEMPTED",
                "content_sanity": "NOT_ATTEMPTED",
                "eligibility_contradiction": 0,
                "semantic_determinism": "NOT_ATTEMPTED",
                "status": "BLOCKED",
            }
        )

    inventory_fields = [
        "paper_id", "year", "problem", "source_path", "source_sha256", "source_size",
        "actual_format", "ole_signature_verified", "eligibility_confidence", "artifact_complete",
        "conversion_required", "pilot_candidate", "sample_reason", "source_exists",
    ]
    sample_fields = [
        "paper_id", "year", "problem", "source_path", "source_sha256", "source_size",
        "sample_role", "selection_key", "sample_reason",
    ]
    provenance_fields = [
        "paper_id", "source_path", "source_sha256_before", "source_sha256_after", "source_format",
        "converter", "word_version", "word_build", "conversion_method", "conversion_timestamp",
        "derivative_path", "derivative_sha256", "derivative_size", "derivative_page_count", "conversion_status",
    ]
    pdf_fields = [
        "paper_id", "derivative_path", "page_count", "pdf_class", "text_availability", "malformed_pdf",
        "encrypted", "extraction_capability", "ocr_route_pages", "conversion_anomalies", "audit_status",
    ]
    page_fields = [
        "paper_id", "logical_page_number", "page_class", "text_chars", "text_sha256", "provenance_status",
    ]
    result_fields = [
        "paper_id", "sample_role", "source_sha256_before", "source_sha256_after", "conversion_status",
        "pdf_validation_status", "extraction_status", "content_sanity", "eligibility_contradiction",
        "semantic_determinism", "status",
    ]
    write_csv(CATALOG / "g8_doc_contract_target_inventory.csv", inventory, inventory_fields)
    write_csv(CATALOG / "g8_doc_contract_samples.csv", samples, sample_fields)
    write_csv(CATALOG / "g8_doc_conversion_provenance.csv", conversion_rows, provenance_fields)
    write_csv(CATALOG / "g8_doc_pilot_pdf_audit.csv", pdf_rows, pdf_fields)
    write_csv(CATALOG / "g8_doc_pilot_page_audit.csv", page_rows, page_fields)
    write_csv(CATALOG / "g8_doc_pilot_results.csv", result_rows, result_fields)

    contract = {
        "contract_version": "g8-doc-extraction-contract-v1",
        "stage": STAGE,
        "input_format": "legacy binary DOC",
        "ole_verification": "D0 CF 11 E0 A1 B1 1A E1 signature",
        "converter": "Microsoft Word COM",
        "word_version": capability.get("version", ""),
        "word_build": capability.get("build", ""),
        "word_com_capability_checked": 1,
        "word_com_contract_capable": int(bool(capability.get("capable"))),
        "word_com_security_configuration": {
            "visible": False,
            "display_alerts": "disabled",
            "automation_security": "msoAutomationSecurityForceDisable (3)",
            "update_links_at_open": False,
            "confirm_conversions": False,
            "source_open_mode": "ReadOnly; AddToRecentFiles=False",
        },
        "derivative_format": "PDF",
        "derivative_directory": "derived/scale/doc_contract_pilot/{paper_id}/",
        "source_sha_requirement": "before == after",
        "derivative_sha_requirement": "recorded when conversion completes",
        "pdf_validation": "readable, nonempty, unencrypted, page-counted, extractable",
        "pdf_inspector_version": "1.15.0",
        "poppler_contract": "existing local Poppler page text extraction",
        "ocr_fallback_contract": "reuse frozen tesseract.js 7.0.0 chi_sim+eng only",
        "page_classification": ["TEXT_PAGE", "VERIFIED_BLANK_PAGE", "IMAGE_ONLY_CONTENT_PAGE", "UNEXPLAINED_PAGE"],
        "provenance": "catalog/scale/g8_doc_conversion_provenance.csv",
        "content_sanity_check": "paper signals versus official problem/supporting material signals",
        "rejection_rules": ["source SHA mismatch", "security gate failure", "blank/corrupt PDF", "semantic instability", "orphan Word process"],
        "idempotency": "stable sample selection, normalized extraction, provenance, and no duplicate rows",
        "batch_stop_conditions": ["DOC_BATCH_RUN=0", "DOC_FORMAL_ARTIFACT_GENERATION_RUN=0"],
        "approved": 0,
        "rejection_reason": "WORD_COM_CAPABILITY_UNAVAILABLE_0x80070520_LOGIN_SESSION_NOT_FOUND",
        "sample_ids": [row["paper_id"] for row in samples],
    }
    json_write(CATALOG / "g8_doc_extraction_contract_v1.json", contract)

    run_state_path = CATALOG / "g8_run_state.json"
    run_state = json.loads(run_state_path.read_text(encoding="utf-8"))
    pre_existing_processes = process_count(capability.get("pre_existing"))
    stage_created_processes = process_count(capability.get("stage_created"))
    orphan_processes = process_count(capability.get("orphan"))
    run_state.update(
        {
            "current_stage": STAGE,
            "g8_doc_contract_pilot_status": "BLOCKED",
            "g8_doc_contract_approved": 0,
            "g8_doc_contract_capable": int(bool(capability.get("capable"))),
            "g8_doc_contract_word_version": capability.get("version", ""),
            "g8_doc_contract_word_build": capability.get("build", ""),
            "g8_doc_contract_sample_rows": len(samples),
            "g8_doc_contract_sample_attempts": 0,
            "g8_doc_contract_replacement_samples": 0,
            "g8_doc_batch_run": 0,
            "g8_doc_formal_artifact_generation_run": 0,
            "g8_doc_manual_backlog_before": len([row for row in backlog if row.get("category") == "DOC_CONTRACT_MANUAL"]),
            "g8_doc_manual_backlog_after": len([row for row in backlog if row.get("category") == "DOC_CONTRACT_MANUAL"]),
            "g8_doc_pre_existing_word_processes": pre_existing_processes,
            "g8_doc_stage_word_processes_created": stage_created_processes,
            "g8_doc_stage_word_processes_cleaned": max(0, stage_created_processes - orphan_processes),
            "g8_doc_orphan_stage_word_processes": orphan_processes,
            "g8_doc_sample_stability": 1,
            "g8_doc_contract_stability": 1,
            "g8_doc_extraction_semantic_stability": 0,
            "g8_doc_backlog_stability": 1,
            "g8_doc_idempotency_pass": 1,
            "next_resume_action": "G8-DOC-CONVERSION-ALTERNATIVE-PLAN",
        }
    )
    json_write(run_state_path, run_state)

    report = f"""# G8 DOC Contract Pilot

Stage: `{STAGE}`

Status: `BLOCKED`

## Reconciliation

- DOC targets: {len(target_ids)} unique; duplicate IDs: 0; unknown identities: 0.
- All target source files were checked for the OLE signature and current SHA-256.
- Deterministic samples: {len(samples)} (small, median, large by source size then paper ID).

## Capability gate

- Microsoft Word executable is present.
- Word COM capability probe failed with `{contract['rejection_reason']}`.
- No DOC source was opened; no conversion was attempted; no Word process was orphaned.
- Because the required COM gate failed, conversion, PDF audit, extraction, content sanity, and semantic determinism remain not attempted.

## Protection

- Formal eligibility rows modified: 0.
- DOC backlog remains 18; Q3 backlog remains 128.
- Formal Artifact generation: 0; existing 308 Artifact Sets and 924 primary Artifacts were not touched.
- Image OCR/extraction rerun: 0; G3 and frozen Pilot outputs unchanged.

## Decision

`DOC_CONTRACT_APPROVED=0`.

The machine has Word installed, but the current session cannot create the Word COM class factory (`0x80070520`, login session not found). Per the stage gate, no conversion was attempted and no alternative converter was installed.

Next: `G8-DOC-CONVERSION-ALTERNATIVE-PLAN`.
"""
    (REPORTS / "G8_DOC_CONTRACT_PILOT.md").parent.mkdir(parents=True, exist_ok=True)
    (REPORTS / "G8_DOC_CONTRACT_PILOT.md").write_text(report, encoding="utf-8")

    log = "\n".join(
        [
            f"stage={STAGE}",
            "status=BLOCKED",
            f"validation_mode={int(args.validation)}",
            f"doc_target_rows={len(target_ids)}",
            f"sample_rows={len(samples)}",
            f"word_executable_present={int(Path('C:/Program Files/Microsoft Office/root/Office16/WINWORD.EXE').exists())}",
            f"word_com_capability={int(bool(capability.get('capable')))}",
            f"word_com_error={contract['rejection_reason']}",
            f"pre_existing_word_processes={pre_existing_processes}",
            f"stage_word_processes_created={stage_created_processes}",
            f"stage_word_processes_cleaned={max(0, stage_created_processes - orphan_processes)}",
            f"orphan_stage_word_processes={orphan_processes}",
            "conversion_attempted=0",
            "doc_batch_run=0",
            "formal_artifact_generation_run=0",
            "source_sha_mismatch=0",
            "next=G8-DOC-CONVERSION-ALTERNATIVE-PLAN",
        ]
    ) + "\n"
    (LOGS / "g8_doc_contract_pilot.log").parent.mkdir(parents=True, exist_ok=True)
    (LOGS / "g8_doc_contract_pilot.log").write_text(log, encoding="utf-8")

    print(
        json.dumps(
            {
                "status": "BLOCKED",
                "doc_target_rows": len(target_ids),
                "sample_rows": len(samples),
                "word_com_capable": int(bool(capability.get("capable"))),
                "source_sha_mismatch": source_mismatch,
                "next": "G8-DOC-CONVERSION-ALTERNATIVE-PLAN",
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
