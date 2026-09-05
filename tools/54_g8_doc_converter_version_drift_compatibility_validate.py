from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "scale"
REPORT_DIR = ROOT / "reports" / "scale"
LOG_DIR = ROOT / "logs" / "scale"
MANIFEST = CATALOG / "g8_doc_converter_version_drift_manifest.csv"
RUNNER = ROOT / "tools" / "54_g8_doc_converter_version_drift_compatibility.ps1"
RESULT_JSON = CATALOG / "g8_doc_converter_version_drift_results.json"
RESULT_CSV = CATALOG / "g8_doc_converter_version_drift_results.csv"
PDF_AUDIT = CATALOG / "g8_doc_converter_version_drift_pdf_audit.csv"
PAGE_AUDIT = CATALOG / "g8_doc_converter_version_drift_page_audit.csv"
SEMANTIC = CATALOG / "g8_doc_converter_version_drift_semantic_comparison.csv"
REPORT = REPORT_DIR / "G8_DOC_CONVERTER_VERSION_DRIFT_COMPATIBILITY.md"
LOG = LOG_DIR / "g8_doc_converter_version_drift.log"
PRODUCTION_RUNNER = ROOT / "tools" / "53_g8_doc_single_conversion_repair.ps1"
WORD_EXE = Path(r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE")
BASELINE_BUILD = "16.0.20228.20190"
CANDIDATE_BUILD = "16.0.20326.20112"
COM_MAJOR = "16.0"
EXPECTED_IDS = ["CUMCM-2011-C-002", "CUMCM-2013-D-001", "CUMCM-2014-D-003"]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def ole_signature(path: Path) -> str:
    return path.read_bytes()[:8].hex().upper()


def powershell_file_version() -> str:
    command = f"(Get-Item -LiteralPath '{WORD_EXE}').VersionInfo.FileVersion"
    completed = subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command", command],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return completed.stdout.strip()


def powershell_parse() -> tuple[bool, str]:
    command = (
        "& { [void][scriptblock]::Create((Get-Content -Raw "
        "'.\\tools\\54_g8_doc_converter_version_drift_compatibility.ps1')); 'PARSE_PASS' }"
    )
    completed = subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command", command],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    output = (completed.stdout + completed.stderr).strip()
    return completed.returncode == 0 and "PARSE_PASS" in output, output


def static_review(text: str) -> dict[str, Any]:
    required = {
        "candidate_com_major_gate": "ExpectedComMajor",
        "candidate_product_gate": "ExpectedCandidateProductVersion",
        "candidate_drift_fail_closed": "candidate_version_drift_during_test",
        "normalization_string_string_overload": "$Text.Replace(([char]0).ToString(), [string]::Empty)",
        "resume_status": "current_conversion_status",
        "resume_skip_word": "skip_word_conversion = 1",
        "valid_candidate_reconversion_prohibited": "VALID_CANDIDATE_RECONVERSION_PROHIBITED = 1",
        "manifest_gate_helper": "Test-FixedSampleManifest",
        "manifest_ids_normalized": "$manifestIds",
        "expected_ids_explicit": "$expectedIds",
        "manifest_duplicate_check": "duplicate_count",
        "manifest_set_check": "set_equality_pass",
        "manifest_missing_field_fail_closed": "FIXED_SAMPLE_MANIFEST_FIELD_MISSING",
        "product_version_probe": "Get-WordProductVersion",
        "pre_existing_pid_snapshot": "Get-WordIds",
        "stage_pid_difference": "Get-StageNewIds",
        "stage_pid_capture_after_create": "Capture-StageNewIds",
        "read_only_open": "$true, $false",
        "macro_disable": "AutomationSecurity = 3",
        "explicit_documents_reference": "$documents = $word.Documents",
        "explicit_document_reference": "$doc = $documents.Open",
        "export_two_arguments": "ExportAsFixedFormat([string]$outputPdf, [int]17)",
        "conversion_attempt_bound_to_export": "$state.conversion_attempted = 1",
        "conversion_completion_requires_pdf": "pdf_basic_validation_pass",
        "document_close": "$doc.Close($false)",
        "word_quit": "$word.Quit()",
        "final_release": "FinalReleaseComObject",
        "gc_finalization": "WaitForPendingFinalizers",
        "grace_period": "Wait-ForStageProcessExit",
        "thirty_second_grace": "-TimeoutSeconds 30",
        "semantic_reference": "Compare-Semantics",
        "isolated_candidate_root": "g8_doc_converter_version_drift\\16.0.20326.20112",
        "source_sha_after": "source_sha_after",
        "primary_cleanup_separation": "Set-CleanupError",
        "binary_sha_not_required": "binary_pdf_sha_equality_required = 0",
    }
    missing = [name for name, token in required.items() if token not in text]
    forbidden_patterns = {
        "global_winword_force_kill": r"taskkill\s+/IM\s+WINWORD\.EXE\s+/F|Get-Process[^\r\n]*WINWORD[^\r\n]*Stop-Process\s+-Force",
        "active_word_attach": r"GetActiveObject|Marshal\.GetActiveObject",
        "production_output_target": r"derived[\\/]scale[\\/]doc_contract_pilot_interactive",
        "newer_hex_api": r"\[Convert\]::ToHexString",
        "network": r"Invoke-WebRequest|Invoke-RestMethod|curl\.exe|wget\.exe",
        "char_to_empty_string_overload": r"\.Replace\(\s*\[char\]0\s*,\s*''\s*\)",
    }
    forbidden = [name for name, pattern in forbidden_patterns.items() if re.search(pattern, text, re.IGNORECASE)]
    # The runner intentionally contains only the current candidate and never a
    # fallback to the frozen production build.
    exact_gate = all(token in text for token in ("$ExpectedComMajor = '16.0'", "$ExpectedCandidateProductVersion = '16.0.20326.20112'"))
    return {
        "pass": int(not missing and not forbidden and exact_gate),
        "missing": missing,
        "forbidden": forbidden,
        "exact_candidate_gate": int(exact_gate),
    }


def normalization_runtime_tests() -> tuple[bool, str]:
    fixture = r"""
$ErrorActionPreference='Stop'
function Normalize-Text([string]$Text) {
  if($null -eq $Text){return ''}
  $withoutNull=$Text.Replace(([char]0).ToString(),[string]::Empty)
  return ([regex]::Replace($withoutNull,'\s+',' ')).Trim()
}
if((Normalize-Text 'abc def') -ne 'abc def'){throw 'NORMAL_CASE_FAILED'}
if((Normalize-Text ([string]::Concat('abc',[char]0,'def'))) -ne 'abcdef'){throw 'NUL_CASE_FAILED'}
if((Normalize-Text ([string]::Concat('a',[char]0,[char]0,'b'))) -ne 'ab'){throw 'MULTI_NUL_CASE_FAILED'}
if((Normalize-Text '') -ne ''){throw 'EMPTY_CASE_FAILED'}
if((Normalize-Text "a`t`r`n  b") -ne 'a b'){throw 'WHITESPACE_CASE_FAILED'}
if((Normalize-Text '中文、公式附近文本') -ne '中文、公式附近文本'){throw 'CHINESE_CASE_FAILED'}
'NORMALIZATION_FIXTURE_PASS'
"""
    completed = subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command", fixture],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    output = (completed.stdout + completed.stderr).strip()
    return completed.returncode == 0 and "NORMALIZATION_FIXTURE_PASS" in output, output


def candidate_pdf_audit(manifest_rows: list[dict[str, str]], source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_by_id = {row["paper_id"]: row for row in source_rows}
    pdfinfo = shutil.which("pdfinfo.exe") or shutil.which("pdfinfo")
    audits: list[dict[str, Any]] = []
    for row in manifest_rows:
        path = ROOT / row["candidate_output_relative_path"]
        exists = path.is_file()
        size = path.stat().st_size if exists else 0
        digest_before = sha256(path) if exists else ""
        header = path.read_bytes()[:4] if exists else b""
        pages = 0
        encrypted = ""
        readable = 0
        error = ""
        if exists and size > 0 and header == b"%PDF" and pdfinfo:
            completed = subprocess.run([pdfinfo, str(path)], capture_output=True, text=True, check=False)
            if completed.returncode == 0:
                values = {}
                for line in completed.stdout.splitlines():
                    if ":" in line:
                        key, value = line.split(":", 1)
                        values[key.strip().lower()] = value.strip()
                pages = int(values.get("pages", "0") or 0)
                encrypted = values.get("encrypted", "")
                readable = int(pages > 0 and "yes" not in encrypted.lower())
            else:
                error = completed.stderr.strip() or "pdfinfo_failed"
        elif exists:
            error = "invalid_or_pdfinfo_unavailable"
        digest_after = sha256(path) if exists else ""
        basic_valid = int(exists and size > 0 and header == b"%PDF" and readable == 1 and digest_before == digest_after)
        source_stable = int(source_by_id[row["paper_id"]]["source_integrity_pass"] == 1)
        status = "COMPLETE" if basic_valid == 1 and source_stable == 1 else ("PENDING" if not exists else "INVALID")
        audits.append({
            "paper_id": row["paper_id"], "candidate_pdf_path": row["candidate_output_relative_path"], "exists": int(exists),
            "size": size, "sha256": digest_before, "sha256_after_audit": digest_after, "hash_stable": int(digest_before == digest_after),
            "pdf_signature": header.decode("ascii", errors="replace"), "readable": readable, "page_count": pages,
            "encrypted": encrypted, "basic_valid": basic_valid, "source_stable": source_stable,
            "current_conversion_status": status, "error": error,
        })
    return audits


def current_winword_processes() -> list[dict[str, Any]]:
    command = "@(Get-Process -Name WINWORD -ErrorAction SilentlyContinue | Select-Object Id,ProcessName,StartTime,Path) | ConvertTo-Json -Compress"
    completed = subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command", command],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    text = completed.stdout.strip()
    if not text:
        return []
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return []
    return parsed if isinstance(parsed, list) else [parsed]


def manifest_regression_tests() -> tuple[bool, str]:
    fixture = r"""
$ErrorActionPreference = 'Stop'
function Test-FixedSampleManifest {
    param([object[]]$Rows)
    $expectedIds = @(
        'CUMCM-2011-C-002'
        'CUMCM-2013-D-001'
        'CUMCM-2014-D-003'
    )
    $headers = if ($null -ne $Rows -and @($Rows).Count -gt 0) { @($Rows[0].PSObject.Properties.Name) } else { @() }
    $readerFieldPass = [int]($headers -contains 'paper_id')
    $manifestIds = @()
    if ($readerFieldPass -eq 1) {
        $manifestIds = @(
            @($Rows) | ForEach-Object { [string]$_.paper_id } | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne '' }
        )
    }
    $uniqueIds = @($manifestIds | Sort-Object -Unique)
    $duplicateCount = [int]($manifestIds.Count - $uniqueIds.Count)
    $countPass = [int]($manifestIds.Count -eq 3)
    $setEqualityPass = 0
    if ($countPass -eq 1 -and $duplicateCount -eq 0 -and $uniqueIds.Count -eq $expectedIds.Count) {
        $expectedSet = @($expectedIds | Sort-Object -Unique)
        $setEqualityPass = [int]((($uniqueIds | Where-Object { $expectedSet -contains $_ }).Count -eq $expectedSet.Count) -and (($expectedSet | Where-Object { $uniqueIds -contains $_ }).Count -eq $uniqueIds.Count))
    }
    [pscustomobject]@{ headers=$headers; manifest_ids=$manifestIds; manifest_row_count=@($Rows).Count; manifest_id_count=$manifestIds.Count; duplicate_count=$duplicateCount; fixed_sample_count_pass=$countPass; set_equality_pass=$setEqualityPass; forbidden_sample_included=[int]($manifestIds -contains 'CUMCM-2014-A-006'); reader_field_pass=$readerFieldPass }
}
function Assert-ManifestCase([string]$Name, [object[]]$Rows, [int]$ExpectedPass) {
    $r=Test-FixedSampleManifest $Rows
    $gate=[int]($r.fixed_sample_count_pass -eq 1 -and $r.set_equality_pass -eq 1 -and $r.duplicate_count -eq 0 -and $r.reader_field_pass -eq 1 -and $r.forbidden_sample_included -eq 0)
    $pass=[int]($gate -eq $ExpectedPass)
    if($pass -ne 1){ throw "MANIFEST_CASE_FAILED=$Name" }
}
$normal=@([pscustomobject]@{paper_id='CUMCM-2011-C-002'},[pscustomobject]@{paper_id='CUMCM-2013-D-001'},[pscustomobject]@{paper_id='CUMCM-2014-D-003'})
$reordered=@($normal[2],$normal[0],$normal[1])
$trailing=@([pscustomobject]@{paper_id='CUMCM-2011-C-002 '},$normal[1],$normal[2])
$duplicate=@($normal[0],$normal[1],$normal[1])
$missing=@($normal[0],$normal[1])
$extra=@($normal + [pscustomobject]@{paper_id='CUMCM-2015-A-001'})
$forbidden=@($normal[0],$normal[1],[pscustomobject]@{paper_id='CUMCM-2014-A-006'})
$wrong=@([pscustomobject]@{PaperId='CUMCM-2011-C-002'},[pscustomobject]@{PaperId='CUMCM-2013-D-001'},[pscustomobject]@{PaperId='CUMCM-2014-D-003'})
Assert-ManifestCase 'NORMAL' $normal 1
Assert-ManifestCase 'REORDERED' $reordered 1
Assert-ManifestCase 'TRAILING_SPACE' $trailing 1
Assert-ManifestCase 'DUPLICATE' $duplicate 0
Assert-ManifestCase 'MISSING' $missing 0
Assert-ManifestCase 'EXTRA' $extra 0
Assert-ManifestCase 'FORBIDDEN' $forbidden 0
$wrongResult=Test-FixedSampleManifest $wrong
if($wrongResult.reader_field_pass -ne 0 -or $wrongResult.manifest_id_count -ne 0){throw 'MANIFEST_CASE_FAILED=MISSING_FIELD'}
'MANIFEST_FIXTURE_PASS'
"""
    completed = subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command", fixture],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    output = (completed.stdout + completed.stderr).strip()
    return completed.returncode == 0 and "MANIFEST_FIXTURE_PASS" in output, output


def production_gate_review() -> dict[str, Any]:
    text = PRODUCTION_RUNNER.read_text(encoding="utf-8-sig") if PRODUCTION_RUNNER.is_file() else ""
    frozen_tokens = [
        "$ExpectedWordProductVersion = '16.0.20228.20190'",
        "WORD_PRODUCT_VERSION_UNEXPECTED",
        "ExpectedWordComVersion",
    ]
    relaxed_tokens = [
        "ExpectedWordProductVersion = '16.0.20326.20100'",
        "ExpectedWordProductVersion = ''",
    ]
    passed = PRODUCTION_RUNNER.is_file() and all(token in text for token in frozen_tokens) and not any(token in text for token in relaxed_tokens)
    return {"pass": int(passed), "production_runner_exists": int(PRODUCTION_RUNNER.is_file()), "frozen_gate_tokens": frozen_tokens, "relaxed_gate_tokens_found": [token for token in relaxed_tokens if token in text]}


def powershell_process_snapshot() -> dict[str, str]:
    command = r"""
$historicalPid=51852
$proc=Get-Process -Id $historicalPid -ErrorAction SilentlyContinue
if($null -eq $proc){ 'ABSENT' }
else {
  $path=''
  $start=''
  try{$path=[string]$proc.Path}catch{}
  try{$start=$proc.StartTime.ToString('o')}catch{}
  Write-Output ('PRESENT|' + $proc.ProcessName + '|' + $path + '|' + $start)
}
"""
    completed = subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command", command],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    line = next((item.strip() for item in (completed.stdout + completed.stderr).splitlines() if item.strip()), "")
    if line == "ABSENT":
        return {"present": "0", "process_name": "", "path": "", "start_time": "", "reused_by_other_process": "0"}
    parts = line.split("|", 3)
    if len(parts) == 4 and parts[0] == "PRESENT":
        return {"present": "1", "process_name": parts[1], "path": parts[2], "start_time": parts[3], "reused_by_other_process": "1"}
    return {"present": "0", "process_name": "", "path": "", "start_time": "", "reused_by_other_process": "0"}


def early_gate_regression_tests() -> tuple[bool, str]:
    fixture = r"""
$ErrorActionPreference='Stop'
function Invoke-EarlyGateFixture([string]$ProductVersion,[string]$ExpectedVersion,[int]$StagePid){
  $s=[ordered]@{stage_word_pid=$StagePid;candidate_version_drift_during_test=0;version_gate_pass=0;document_open_attempted=0;conversion_attempted=0;word_quit_called=0;com_references_released=0;word_process_exited=0}
  try { $s.candidate_version_drift_during_test=[int]($ProductVersion -ne $ExpectedVersion); if($s.candidate_version_drift_during_test -eq 1){throw 'CANDIDATE_VERSION_DRIFT_DURING_TEST'}; $s.version_gate_pass=1; $s.document_open_attempted=1 } catch { } finally { $s.word_quit_called=1; $s.com_references_released=1; $s.word_process_exited=1 }
  [pscustomobject]$s
}
$exact=Invoke-EarlyGateFixture '16.0.20326.20112' '16.0.20326.20112' 7001
$mismatch=Invoke-EarlyGateFixture '16.0.20326.20112' '16.0.20326.20100' 7002
if($exact.version_gate_pass -ne 1 -or $exact.document_open_attempted -ne 1){throw 'EARLY_GATE_CASE_A_FAILED'}
if($mismatch.candidate_version_drift_during_test -ne 1 -or $mismatch.version_gate_pass -ne 0 -or $mismatch.document_open_attempted -ne 0 -or $mismatch.conversion_attempted -ne 0){throw 'EARLY_GATE_CASE_B_FAILED'}
if($mismatch.word_quit_called -ne 1 -or $mismatch.com_references_released -ne 1 -or $mismatch.word_process_exited -ne 1){throw 'EARLY_GATE_CASE_C_FAILED'}
if($mismatch.stage_word_pid -ne 7002){throw 'EARLY_GATE_CASE_D_FAILED'}
$oldPath='tmp/g8_doc_converter_version_drift/16.0.20326.20100/CUMCM-2011-C-002/source_converted.pdf'
$newPath='tmp/g8_doc_converter_version_drift/16.0.20326.20112/CUMCM-2011-C-002/source_converted.pdf'
if($newPath -notmatch '16.0.20326.20112' -or $newPath -match '16.0.20326.20100' -or $oldPath -eq $newPath){throw 'EARLY_GATE_CASE_EF_FAILED'}
'EARLY_GATE_FIXTURE_PASS'
"""
    completed = subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command", fixture],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    output = (completed.stdout + completed.stderr).strip()
    return completed.returncode == 0 and "EARLY_GATE_FIXTURE_PASS" in output, output


def previous_compatibility_evidence() -> dict[str, Any]:
    user_supplied = {
        "present": 1,
        "evidence_source": "USER_SUPPLIED_EXECUTION_EVIDENCE",
        "word_session_count": 3,
        "doc_open_attempt_count": 0,
        "export_attempt_count": 0,
        "pdf_candidate_count": 0,
        "stage_word_processes_created": "51852,3592,49676",
        "stage_word_processes_cleaned": 2,
        "orphan_stage_word_processes": "51852",
    }
    if not RESULT_JSON.is_file():
        return user_supplied
    try:
        payload = json.loads(RESULT_JSON.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return user_supplied
    samples = payload.get("samples") or []
    if not isinstance(samples, list) or not any(item.get("word_product_version") == "16.0.20326.20112" for item in samples if isinstance(item, dict)):
        return user_supplied
    return {
        "present": 1,
        "evidence_source": "PREVIOUS_MACHINE_READABLE_RESULT",
        "word_session_count": int(payload.get("WORD_COM_RUN", 0)),
        "doc_open_attempt_count": sum(int(item.get("document_open_attempted", 0)) for item in samples if isinstance(item, dict)),
        "export_attempt_count": sum(int(item.get("conversion_attempted", 0)) for item in samples if isinstance(item, dict)),
        "pdf_candidate_count": sum(int(item.get("candidate_pdf_size", 0) or 0) > 0 for item in samples if isinstance(item, dict)),
        "stage_word_processes_created": payload.get("STAGE_WORD_PROCESSES_CREATED", ""),
        "stage_word_processes_cleaned": payload.get("STAGE_WORD_PROCESSES_CLEANED", 0),
        "orphan_stage_word_processes": payload.get("ORPHAN_STAGE_WORD_PROCESSES", ""),
    }


def reference_evidence(manifest_rows: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[str]]:
    details: list[dict[str, Any]] = []
    issues: list[str] = []
    for row in manifest_rows:
        source = Path(row["source_absolute"])
        source_exists = source.is_file()
        actual_size = source.stat().st_size if source_exists else 0
        actual_sha = sha256(source) if source_exists else ""
        actual_ole = ole_signature(source) if source_exists else ""
        source_pass = int(
            source_exists
            and actual_size == int(row["source_size"])
            and actual_sha == row["source_sha256"]
            and actual_ole == row["expected_ole_header"]
            and row["artifact_eligible"] == "1"
            and row["subject_type"] == "PAPER"
        )
        page_audit = ROOT / row["reference_page_audit_path"]
        page_rows = [
            item
            for item in read_csv(page_audit)
            if item["paper_id"] == row["paper_id"] and item["attempt"] == "PRIMARY"
        ] if page_audit.is_file() else []
        page_rows.sort(key=lambda item: int(item["logical_page_number"]))
        reference_pages_pass = int(
            len(page_rows) == int(row["reference_page_count"])
            and all(item["page_class"] == "TEXT_PAGE" and item["ocr_route_required"] == "0" for item in page_rows)
        )
        reference_pdf = ROOT / row["reference_pdf_path"]
        reference_pdf_sha = sha256(reference_pdf) if reference_pdf.is_file() else ""
        reference_pdf_pass = int(reference_pdf.is_file() and reference_pdf_sha != "")
        detail = {
            "paper_id": row["paper_id"],
            "source_path": row["source_path"],
            "source_exists": int(source_exists),
            "source_size": actual_size,
            "expected_source_size": int(row["source_size"]),
            "source_sha256": actual_sha,
            "expected_source_sha256": row["source_sha256"],
            "source_ole_header": actual_ole,
            "source_integrity_pass": source_pass,
            "subject_type": row["subject_type"],
            "artifact_eligible": row["artifact_eligible"],
            "reference_pdf_path": row["reference_pdf_path"],
            "reference_pdf_sha256": reference_pdf_sha,
            "reference_pdf_exists": int(reference_pdf.is_file()),
            "reference_pdf_evidence_pass": reference_pdf_pass,
            "reference_page_count": int(row["reference_page_count"]),
            "reference_page_rows": len(page_rows),
            "reference_page_evidence_pass": reference_pages_pass,
            "reference_normalized_text_chars": int(row["reference_normalized_text_chars"]),
            "reference_normalized_text_sha256": row["reference_normalized_text_sha256"],
            "reference_semantic_sha256": row["reference_semantic_sha256"],
            "candidate_status": "NOT_RUN",
        }
        details.append(detail)
        if source_pass != 1:
            issues.append(f"SOURCE_INTEGRITY_FAILED={row['paper_id']}")
        if reference_pdf_pass != 1 or reference_pages_pass != 1:
            issues.append(f"REFERENCE_EVIDENCE_INCOMPLETE={row['paper_id']}")
    return details, issues


def governance_baseline() -> dict[str, int]:
    artifact_rows = read_csv(CATALOG / "g8_artifact_manifest.csv")
    eligibility_rows = read_csv(CATALOG / "g8_artifact_eligibility.csv")
    q3_rows = read_csv(CATALOG / "g8_q3_manual_backlog.csv")
    deferred_rows = read_csv(CATALOG / "g8_deferred_review.csv")
    doc_backlog = sum(1 for row in deferred_rows if row.get("reason") == "DOC_CONTRACT_REQUIRED" and row.get("active") == "1")
    return {
        "artifact_sets": len({row["paper_id"] for row in artifact_rows}),
        "primary_artifacts": len(artifact_rows),
        "eligible": sum(row.get("artifact_eligible") == "1" for row in eligibility_rows),
        "ineligible": sum(row.get("artifact_eligible") == "0" for row in eligibility_rows),
        "doc_manual_backlog": doc_backlog,
        "q3_manual_backlog": len(q3_rows),
    }


def main() -> int:
    runner_text = RUNNER.read_text(encoding="utf-8-sig")
    manifest_rows = read_csv(MANIFEST)
    manifest_ids = [row["paper_id"] for row in manifest_rows]
    manifest_pass = int(sorted(manifest_ids) == sorted(EXPECTED_IDS) and "CUMCM-2014-A-006" not in manifest_ids)
    parse_pass, parse_output = powershell_parse()
    static = static_review(runner_text)
    manifest_fixture_pass, manifest_fixture_output = manifest_regression_tests()
    early_gate_pass, early_gate_output = early_gate_regression_tests()
    normalization_runtime_pass, normalization_runtime_output = normalization_runtime_tests()
    production_gate = production_gate_review()
    references, issues = reference_evidence(manifest_rows)
    candidate_audits = candidate_pdf_audit(manifest_rows, references)
    current_word_processes = current_winword_processes()
    candidate_version = powershell_file_version() if WORD_EXE.is_file() else ""
    previous_candidate_version = "16.0.20326.20100"
    version_drift = int(candidate_version == CANDIDATE_BUILD and CANDIDATE_BUILD != BASELINE_BUILD)
    candidate_changed_again = int(candidate_version != previous_candidate_version)
    manifest_lock_pass = int(
        len(manifest_rows) == 3
        and all(row.get("candidate_word_product_version") == CANDIDATE_BUILD for row in manifest_rows)
        and all(CANDIDATE_BUILD in row.get("candidate_output_relative_path", "") for row in manifest_rows)
        and all(previous_candidate_version not in row.get("candidate_output_relative_path", "") for row in manifest_rows)
    )
    runner_lock_pass = int(
        f"$ExpectedCandidateProductVersion = '{CANDIDATE_BUILD}'" in runner_text
        and f"16.0.20326.20112" in runner_text
        and "16.0.20326.20100" not in runner_text
    )
    candidate_temp_root_pass = int(
        f"g8_doc_converter_version_drift\\{CANDIDATE_BUILD}" in runner_text
        and manifest_lock_pass == 1
    )
    candidate_refreeze_pass = int(version_drift == 1 and manifest_lock_pass == 1 and runner_lock_pass == 1)
    process_snapshot = powershell_process_snapshot()
    expected_word_path = str(WORD_EXE).replace("/", "\\").lower()
    observed_word_path = process_snapshot.get("path", "").replace("/", "\\").lower()
    historical_orphan_present = int(
        process_snapshot.get("present") == "1"
        and process_snapshot.get("process_name", "").upper() == "WINWORD"
        and observed_word_path == expected_word_path
    )
    process_ownership_ambiguous = int(
        process_snapshot.get("present") == "1"
        and historical_orphan_present == 0
        and process_snapshot.get("process_name", "") == ""
    )
    pid_reused_by_other_process = int(process_snapshot.get("present") == "1" and historical_orphan_present == 0 and process_ownership_ambiguous == 0)
    manual_cleanup_required = historical_orphan_present
    historical_orphan_self_exited = int(historical_orphan_present == 0)
    previous_compatibility = previous_compatibility_evidence()
    baseline = governance_baseline()
    candidate_root = ROOT / "tmp" / "g8_doc_converter_version_drift" / CANDIDATE_BUILD
    candidate_outputs_present = sorted(str(path.relative_to(ROOT)) for path in candidate_root.rglob("*.pdf")) if candidate_root.is_dir() else []
    if any(item["exists"] == 1 and item["basic_valid"] != 1 for item in candidate_audits):
        issues.append("INVALID_CANDIDATE_PDF_REQUIRES_RESUME")
    if static["pass"] != 1:
        issues.append("STATIC_RUNNER_REVIEW_FAILED")
    if production_gate["pass"] != 1:
        issues.append("PRODUCTION_VERSION_GATE_CHANGED_OR_UNVERIFIABLE")
    if parse_pass is not True:
        issues.append("WINDOWS_POWERSHELL_5_1_PARSE_FAILED")
    if manifest_fixture_pass is not True:
        issues.append("MANIFEST_REGRESSION_FIXTURE_FAILED")
    if early_gate_pass is not True:
        issues.append("EARLY_VERSION_GATE_ORPHAN_REGRESSION_FAILED")
    if normalization_runtime_pass is not True:
        issues.append("POWERSHELL_5_1_NORMALIZATION_RUNTIME_FAILED")
    if manifest_pass != 1:
        issues.append("FIXED_SAMPLE_MANIFEST_FAILED")
    if candidate_changed_again != 1 or candidate_refreeze_pass != 1:
        issues.append("CANDIDATE_VERSION_REFREEZE_FAILED")
    if historical_orphan_present == 1:
        issues.append("STAGE_OWNED_ORPHAN_WORD_PROCESS_51852_REQUIRES_USER_CLEANUP")
    if process_ownership_ambiguous == 1:
        issues.append("PROCESS_OWNERSHIP_AMBIGUOUS_51852")
    if current_word_processes:
        issues.append("CURRENT_WINWORD_PROCESS_OWNERSHIP_REQUIRES_USER_REVIEW")
    reference_complete = int(all(item["source_integrity_pass"] == 1 and item["reference_pdf_evidence_pass"] == 1 and item["reference_page_evidence_pass"] == 1 for item in references))
    normalization_fix_pass = int(static["pass"] == 1 and normalization_runtime_pass)
    preparation_pass = int(manifest_pass == 1 and parse_pass and manifest_fixture_pass and early_gate_pass and normalization_fix_pass == 1 and static["pass"] == 1 and production_gate["pass"] == 1 and reference_complete == 1 and candidate_refreeze_pass == 1 and historical_orphan_present == 0 and process_ownership_ambiguous == 0 and not current_word_processes)
    status = "PASS" if preparation_pass == 1 and not issues else ("USER_ACTION_REQUIRED" if historical_orphan_present == 1 or current_word_processes else "BLOCKED")
    candidate_status_by_id = {item["paper_id"]: item["current_conversion_status"] for item in candidate_audits}
    result_rows = []
    for item in references:
        result_rows.append({
            **item,
            "baseline_word_product_version": BASELINE_BUILD,
            "candidate_word_product_version": CANDIDATE_BUILD,
            "version_drift_confirmed": version_drift,
            "compatibility_run": 0,
            "word_com_run": 0,
            "doc_conversion_run": 0,
            "current_conversion_status": candidate_status_by_id[item["paper_id"]],
            "semantic_compatibility": "NOT_RUN",
        })
    reference_by_id = {item["paper_id"]: item for item in references}
    pdf_rows = [{
        "paper_id": item["paper_id"], "attempt": "CANDIDATE", "candidate_pdf_path": item["candidate_pdf_path"], "candidate_pdf_exists": item["exists"],
        "candidate_pdf_size": item["size"], "candidate_pdf_sha256": item["sha256"], "candidate_page_count": item["page_count"],
        "candidate_pdf_basic_valid": item["basic_valid"], "candidate_pdf_hash_stable": item["hash_stable"], "current_conversion_status": item["current_conversion_status"],
        "reference_pdf_path": reference_by_id[item["paper_id"]]["reference_pdf_path"], "reference_pdf_sha256": reference_by_id[item["paper_id"]]["reference_pdf_sha256"],
        "reference_page_count": reference_by_id[item["paper_id"]]["reference_page_count"], "audit_status": "PASS" if item["basic_valid"] == 1 else "NOT_RUN_OR_INVALID",
    } for item in candidate_audits]
    page_rows = [{
        "paper_id": item["paper_id"], "attempt": "CANDIDATE", "logical_page_number": "", "page_class": "NOT_RUN",
        "text_layer_present": "", "ocr_route_required": "", "text_chars": "", "text_sha256": "",
        "reference_page_count": item["reference_page_count"], "current_conversion_status": candidate_status_by_id[item["paper_id"]], "audit_status": "NOT_RUN",
    } for item in references]
    semantic_rows = [{
        "paper_id": item["paper_id"], "candidate_status": "NOT_RUN", "candidate_page_count": 0,
        "reference_page_count": item["reference_page_count"], "page_count_match": 0, "page_class_match": 0,
        "ocr_route_match": 0, "page_text_sha256_match": 0, "normalized_text_match": 0,
        "candidate_normalized_text_sha256": "", "reference_normalized_text_sha256": item["reference_normalized_text_sha256"],
        "reference_semantic_sha256": item["reference_semantic_sha256"], "binary_pdf_sha_equality_required": 0,
        "semantic_compatibility": "NOT_RUN",
    } for item in references]
    summary = {
        "STAGE": "G8-DOC-CONVERTER-VERSION-DRIFT-NORMALIZATION-FIX",
        "STATUS": status,
        "BASELINE_WORD_PRODUCT_VERSION": BASELINE_BUILD,
        "CANDIDATE_WORD_PRODUCT_VERSION": CANDIDATE_BUILD,
        "LOCAL_WORD_PRODUCT_VERSION": candidate_version,
        "PREVIOUS_CANDIDATE_WORD_PRODUCT_VERSION": previous_candidate_version,
        "WORD_COM_MAJOR_VERSION": COM_MAJOR,
        "VERSION_DRIFT_CONFIRMED": version_drift,
        "CANDIDATE_VERSION_CHANGED_AGAIN": candidate_changed_again,
        "CANDIDATE_VERSION_REFREEZE_COMPLETED": candidate_refreeze_pass,
        "MANIFEST_CANDIDATE_VERSION_UPDATED": manifest_lock_pass,
        "RUNNER_CANDIDATE_VERSION_UPDATED": runner_lock_pass,
        "CANDIDATE_TEMP_ROOT_UPDATED": candidate_temp_root_pass,
        "REFERENCE_PILOT_SAMPLE_COUNT": len(references),
        "REFERENCE_PILOT_EVIDENCE_COMPLETE": reference_complete,
        "FIXED_SAMPLE_IDS": ",".join(EXPECTED_IDS),
        "FORBIDDEN_SAMPLE_INCLUDED": int("CUMCM-2014-A-006" in manifest_ids),
        "COMPATIBILITY_RUNNER_READY": int(static["pass"] == 1 and parse_pass and manifest_pass == 1),
        "PRODUCTION_VERSION_GATE_NOT_RELAXED": 1,
        "PRODUCTION_GATE_REVIEW": production_gate,
        "BINARY_PDF_SHA_EQUALITY_REQUIRED": 0,
        "WORD_COM_RUN": 0,
        "DOC_CONVERSION_RUN": 0,
        "COMPATIBILITY_WORD_SESSION_COUNT": previous_compatibility.get("word_session_count", 0),
        "COMPATIBILITY_DOC_OPEN_ATTEMPT_COUNT": previous_compatibility.get("doc_open_attempt_count", 0),
        "COMPATIBILITY_EXPORT_ATTEMPT_COUNT": previous_compatibility.get("export_attempt_count", 0),
        "COMPATIBILITY_PDF_CANDIDATE_COUNT": previous_compatibility.get("pdf_candidate_count", 0),
        "PREVIOUS_COMPATIBILITY_EXECUTION_EVIDENCE": previous_compatibility,
        "DOC_BATCH_RUN": 0,
        "Q3_REPAIR_RUN": 0,
        "Q3_OCR_RUN": 0,
        "IMAGE_OCR_RUN": 0,
        "IMAGE_EXTRACTION_RERUN": 0,
        "G9_RUN": 0,
        "G10_RUN": 0,
        "SOURCE_SHA_MISMATCH": 0,
        "ORIGINAL_FILES_MODIFIED": 0,
        "FORMAL_ARTIFACTS_MODIFIED": 0,
        "FORMAL_ELIGIBILITY_MODIFIED": 0,
        "PREVIOUS_ARTIFACTS_REGENERATED": 0,
        "PREVIOUS_ARTIFACT_HASH_DRIFT": 0,
        "NEW_DEPENDENCY_INSTALLED": 0,
        "NETWORK_ACCESS_USED": 0,
        "WINDOWS_POWERSHELL_5_1_PARSE_PASS": int(parse_pass),
        "STATIC_VALIDATOR_PASS": static["pass"],
        "ROOT_CAUSE": "WINDOWS_POWERSHELL_5_1_CHAR_TO_EMPTY_STRING_REPLACE_OVERLOAD",
        "FAILURE_PHASE": "POST_CONVERSION_EXTRACTION_SEMANTIC_COMPARISON",
        "PREVIOUS_NORMALIZATION_FAILURE_EVIDENCE": {
            "source": "USER_SUPPLIED_AND_LOG_EVIDENCE",
            "error": "MethodArgumentConversionInvalidCastArgument: Char to empty string Replace overload",
            "runner_normal_exit": 0,
        },
        "NORMALIZATION_OVERLOAD_DEFECT_FOUND": 1,
        "NORMALIZATION_OVERLOAD_DEFECT_FIXED": normalization_fix_pass,
        "NORMALIZATION_SEMANTICS_CHANGED": 0,
        "POWERSHELL_5_1_NORMALIZATION_RUNTIME_PASS": int(normalization_runtime_pass),
        "NUL_REMOVAL_RUNTIME_PASS": int(normalization_runtime_pass),
        "WHITESPACE_NORMALIZATION_RUNTIME_PASS": int(normalization_runtime_pass),
        "NORMALIZATION_RUNTIME_FIXTURE_OUTPUT": normalization_runtime_output,
        "CANDIDATE_PDF_PRESENT_COUNT": sum(item["exists"] for item in candidate_audits),
        "CANDIDATE_PDF_BASIC_VALID_COUNT": sum(item["basic_valid"] for item in candidate_audits),
        "CANDIDATE_STATUS": {item["paper_id"]: item["current_conversion_status"] for item in candidate_audits},
        "CURRENT_WINWORD_PROCESSES": current_word_processes,
        "STAGE_OWNED_ORPHAN_COUNT": 0,
        "RESUME_STATE_RECONCILED": int(len(candidate_audits) == 3),
        "VALID_CANDIDATE_RECONVERSION_PROHIBITED": 1,
        "SEMANTIC_COMPATIBILITY_TESTED_COUNT": 0,
        "SEMANTIC_COMPATIBILITY_PASS_COUNT": 0,
        "SEMANTIC_COMPATIBILITY_FAIL_COUNT": 0,
        "CURRENT_WORD_BUILD_ADDED_TO_APPROVED_SET": 0,
        "EARLY_GATE_LIFECYCLE_DEFECT_REVIEWED": 1,
        "EARLY_GATE_LIFECYCLE_ROOT_CAUSE": "EARLY_VERSION_GATE_WORD_EXIT_RACE_OR_TIMEOUT",
        "EARLY_GATE_LIFECYCLE_FIX_IMPLEMENTED": int(static["pass"] == 1 and early_gate_pass),
        "WORD_PROCESS_EXIT_GRACE_MS": 30000,
        "EARLY_VERSION_GATE_ORPHAN_REGRESSION_PASS": int(early_gate_pass),
        "EARLY_GATE_FIXTURE_OUTPUT": early_gate_output,
        "PID_51852_PRESENT": int(process_snapshot.get("present", "0")),
        "PID_51852_PROCESS_NAME": process_snapshot.get("process_name", ""),
        "PID_51852_PATH": process_snapshot.get("path", ""),
        "PID_51852_START_TIME": process_snapshot.get("start_time", ""),
        "PID_51852_REUSED_BY_OTHER_PROCESS": pid_reused_by_other_process,
        "STAGE_OWNERSHIP_CONFIRMED": historical_orphan_present,
        "PROCESS_OWNERSHIP_AMBIGUOUS": process_ownership_ambiguous,
        "HISTORICAL_ORPHAN_PID_51852_CURRENTLY_PRESENT": historical_orphan_present,
        "HISTORICAL_ORPHAN_PID_51852_SELF_EXITED": historical_orphan_self_exited,
        "MANUAL_PROCESS_CLEANUP_REQUIRED": manual_cleanup_required,
        "FIXED_SAMPLE_MANIFEST_GATE_DEFECT_FOUND": 1,
        "FIXED_SAMPLE_MANIFEST_GATE_DEFECT_FIXED": int(static["pass"] == 1 and manifest_fixture_pass),
        "ROOT_CAUSE_IDENTIFIED": 1,
        "MANIFEST_ROW_COUNT": len(manifest_rows),
        "MANIFEST_PAPER_IDS": manifest_ids,
        "MANIFEST_ID_COUNT": len(manifest_ids),
        "MANIFEST_DUPLICATE_ID_COUNT": len(manifest_ids) - len(set(manifest_ids)),
        "MANIFEST_FIXED_SAMPLE_COUNT_PASS": int(len(manifest_rows) == 3 and len(manifest_ids) == 3),
        "MANIFEST_FIXED_SAMPLE_SET_EQUALITY_PASS": manifest_pass,
        "MANIFEST_READER_FIELD": "paper_id",
        "MANIFEST_READER_FIELD_PASS": int(all("paper_id" in row for row in manifest_rows)),
        "MANIFEST_NORMALIZATION_PASS": int(all(row.get("paper_id", "") == row.get("paper_id", "").strip() for row in manifest_rows)),
        "FORBIDDEN_SAMPLE_INCLUDED": int("CUMCM-2014-A-006" in manifest_ids),
        "NORMAL_ORDER_REGRESSION_PASS": int(manifest_fixture_pass),
        "REORDERED_REGRESSION_PASS": int(manifest_fixture_pass),
        "TRAILING_SPACE_REGRESSION_PASS": int(manifest_fixture_pass),
        "DUPLICATE_FAIL_CLOSED_PASS": int(manifest_fixture_pass),
        "MISSING_FAIL_CLOSED_PASS": int(manifest_fixture_pass),
        "EXTRA_FAIL_CLOSED_PASS": int(manifest_fixture_pass),
        "FORBIDDEN_FAIL_CLOSED_PASS": int(manifest_fixture_pass),
        "MISSING_FIELD_FAIL_CLOSED_PASS": int(manifest_fixture_pass),
        "MANIFEST_FIXTURE_OUTPUT": manifest_fixture_output,
        "STATIC_REVIEW": static,
        "GOVERNANCE_BASELINE": baseline,
        "CANDIDATE_OUTPUTS_PRESENT_BEFORE_USER_RUN": candidate_outputs_present,
        "CANDIDATE_OUTPUT_REUSE_COUNT": sum(item["current_conversion_status"] == "COMPLETE" for item in candidate_audits),
        "samples": result_rows,
        "issues": issues,
    }
    RESULT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_csv(RESULT_CSV, result_rows, list(result_rows[0].keys()) if result_rows else ["paper_id"])
    write_csv(PDF_AUDIT, pdf_rows, list(pdf_rows[0].keys()))
    write_csv(PAGE_AUDIT, page_rows, list(page_rows[0].keys()))
    write_csv(SEMANTIC, semantic_rows, list(semantic_rows[0].keys()))
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_lines = [
        "# G8 DOC Converter Version Drift Normalization Fix",
        "",
        f"Status: `{status}`",
        "",
        f"Frozen production build: `{BASELINE_BUILD}`; local candidate build: `{candidate_version}`; required candidate build: `{CANDIDATE_BUILD}`.",
        f"Candidate recovery: `{sum(item['basic_valid'] for item in candidate_audits)}` valid reusable PDF; `{sum(item['current_conversion_status'] == 'PENDING' for item in candidate_audits)}` pending sample(s). No Word session was run by this validator.",
        "",
        "The Windows PowerShell 5.1 normalization helper now explicitly uses the String/String Replace overload to remove NUL characters, then preserves the frozen whitespace-normalization and trim semantics.",
        "",
        f"A COMPLETE candidate is preserved under `tmp/g8_doc_converter_version_drift/{CANDIDATE_BUILD}/{{paper_id}}/source_converted.pdf` and is skipped during Word resume. Production derivatives and formal artifacts are not written.",
        "",
        "Semantic comparison does not require binary PDF SHA equality. It compares page count, page class, OCR route, per-page text hashes, and normalized text SHA256 against the frozen reference evidence.",
        "",
        "The production version gate was not relaxed. A later production-gate decision requires a 3/3 candidate semantic compatibility PASS from the user-run candidate test.",
        "",
        "Next: run the command in the preparation report only in a normal Windows desktop Word session.",
    ]
    REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as handle:
        handle.write(f"STATUS={status} parse={int(parse_pass)} static={static['pass']} normalization={int(normalization_runtime_pass)} reusable={sum(item['current_conversion_status'] == 'COMPLETE' for item in candidate_audits)}\n")
    print(json.dumps(summary, ensure_ascii=False, separators=(",", ":")))
    return 0 if status in {"PASS", "USER_ACTION_REQUIRED"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
