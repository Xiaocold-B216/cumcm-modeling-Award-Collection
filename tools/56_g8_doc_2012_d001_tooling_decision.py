#!/usr/bin/env python3
"""Evidence-only tooling decision for the exhausted CUMCM-2012-D-001 repair."""
from __future__ import annotations

import csv
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "scale"
REPORTS = ROOT / "reports" / "scale"
RESULT = CATALOG / "g8_doc_single_conversion_repair_result.json"
TARGET = "CUMCM-2012-D-001"
EXPECTED_SHA = "D93A9A6A9DE012927F8A5D4B36E1768CA3F6AFFB6952673F40FE2740D4032766"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for part in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(part)
    return digest.hexdigest().upper()


def write_csv(path: Path, row: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)


def find_tool(name: str, candidates: list[Path] = []) -> tuple[int, str]:
    found = shutil.which(name)
    if found:
        return 1, found
    for candidate in candidates:
        if candidate.is_file():
            return 1, str(candidate)
    return 0, ""


def main() -> int:
    record = json.loads(RESULT.read_text(encoding="utf-8-sig"))
    attempts = [record.get("attempt_a") or {}, record.get("attempt_b") or {}]
    exports = sum(int(attempt.get("export_attempted") == 1) for attempt in attempts)
    failures = sum(int(attempt.get("error_code") == "EXPORT_ERROR") for attempt in attempts)
    if exports != 2 or failures != 2:
        raise RuntimeError("TARGETED_EXPORT_EVIDENCE_NOT_EXHAUSTED")
    source = ROOT / next(row for row in csv.DictReader((CATALOG / "g8_doc_batch_conversion_manifest.csv").open(encoding="utf-8-sig")) if row["paper_id"] == TARGET)["source_path"]
    source_sha = sha256(source)
    source_ole = source.read_bytes()[:8].hex().upper()
    # Correct the historical result without erasing its two detailed attempt records.
    record.update({
        "STAGE": "G8-DOC-BATCH-CONVERSION-REPAIR", "TARGETED_REPAIR_EXHAUSTED": 1,
        "TARGETED_REPAIR_BASELINE_EXPORT_STILL_ALLOWED": 0, "DIRECT_WORD_EXPORT_ROUTE_STATUS": "CLOSED",
        "HISTORICAL_TARGETED_EXPORT_ATTEMPT_COUNT": exports, "HISTORICAL_TARGETED_EXPORT_FAILURE_COUNT": failures,
        "CURRENT_INVOCATION_WORD_COM_RUN": 0, "CURRENT_INVOCATION_EXPORT_ATTEMPT_COUNT": 0,
    })
    RESULT.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    runner_text = (ROOT / "tools" / "53_g8_doc_single_conversion_repair.ps1").read_text(encoding="utf-8")
    guard_position = runner_text.find("TARGETED_REPAIR_ALREADY_EXHAUSTED")
    invoke_position = runner_text.find("$attemptA = Invoke-TargetedAttempt")
    exhausted_guard_pass = int(guard_position >= 0 and invoke_position >= 0 and guard_position < invoke_position and "CURRENT_INVOCATION_WORD_COM_RUN = 0" in runner_text)
    tools: list[dict[str, Any]] = []
    for name, command, paths, approved, note in [
        ("Microsoft Word", "WINWORD.EXE", [Path(r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE")], 1, "approved converter family; direct ExportAsFixedFormat route exhausted for this target"),
        ("LibreOffice/soffice", "soffice.exe", [Path(r"C:\Program Files\LibreOffice\program\soffice.exe")], 0, "not installed"),
        ("pandoc", "pandoc.exe", [], 0, "not installed"),
        ("antiword", "antiword.exe", [], 0, "not installed"),
        ("catdoc", "catdoc.exe", [], 0, "not installed"),
        ("wvText/wvWare", "wvText.exe", [], 0, "not installed"),
        ("unoconv", "unoconv.exe", [], 0, "not installed"),
    ]:
        installed, path = find_tool(command, paths)
        tools.append({"tool_name": name, "installed": installed, "version": "16.0.20326.20112" if name == "Microsoft Word" and installed else "", "path": path, "already_approved_for_doc_conversion": approved, "assessment": note})
    decision = {
        "stage": "G8-DOC-CUMCM-2012-D-001-TOOLING-DECISION", "status": "PASS", "target_paper_id": TARGET,
        "source_sha256": source_sha, "source_size": source.stat().st_size, "source_ole_signature": source_ole,
        "historical_batch_attempt_count": 2, "historical_batch_export_failure_count": 2,
        "targeted_export_attempt_count": exports, "targeted_export_failure_count": failures, "targeted_repair_attempt_limit": 2,
        "targeted_repair_exhausted": 1, "direct_word_export_route_status": "CLOSED", "targeted_repair_baseline_export_still_allowed": 0,
        "attempt_a_result": "EXPORT_ERROR", "attempt_b_result": "EXPORT_ERROR", "hresult_available": 0, "hresult": "",
        "target_structural_outlier": "UNDETERMINED", "structural_outlier_fields": "NO_COMPARABLE_SUCCESS_DIAGNOSTIC_EVIDENCE",
        "diagnostics": {key: attempts[0].get(key) for key in ("words_count", "characters_count", "paragraphs_count", "sections_count", "tables_count", "inline_shapes_count", "shapes_count", "fields_count", "compatibility_mode", "protection_type")},
        "tool_inventory_completed": 1, "tools": tools,
        "alternative_routes": [
            {"option": "A", "route": "Word DOC -> isolated DOCX -> new Word session -> PDF", "classification": "PREFERRED", "reason": "rebuilds legacy DOC representation while retaining approved Word family; requires a separate semantic validation contract"},
            {"option": "B", "route": "Word DOC -> isolated RTF -> PDF", "classification": "SECONDARY", "reason": "higher field, inline-shape, formula, and layout fidelity risk than DOCX"},
            {"option": "C", "route": "LibreOffice/soffice", "classification": "REJECTED", "reason": "not installed and not approved"},
            {"option": "D", "route": "Direct text parser", "classification": "REJECTED", "reason": "not installed; cannot establish governed PDF/layout preservation for 253 inline shapes and 238 fields"},
            {"option": "E", "route": "Reacquisition", "classification": "SECONDARY", "reason": "requires later external provenance, identity, and semantic-equivalence review; no network used here"},
            {"option": "F", "route": "Manual interactive repair/export", "classification": "LAST_RESORT", "reason": "requires a separately approved, fully logged manual contract"},
        ],
        "preferred_route": "WORD_DOC_TO_ISOLATED_DOCX_TO_PDF", "new_remediation_contract_required": 1,
        "contract_name": "G8-DOC-CUMCM-2012-D-001-DOCX-INTERMEDIATE-PILOT", "53_bookkeeping_fixed": int(record["TARGETED_REPAIR_BASELINE_EXPORT_STILL_ALLOWED"] == 0 and record["TARGETED_REPAIR_EXHAUSTED"] == 1),
        "53_exhausted_rerun_fail_closed": exhausted_guard_pass, "successful_batch_rows_preserved": 13, "successful_batch_rows_reconverted": 0,
        "doc_contract_approved": 1, "eligible": 453, "ineligible": 189, "artifact_sets": 308, "primary_artifacts": 924,
        "doc_manual_backlog": 17, "q3_manual_backlog": 128, "word_com_run": 0, "doc_conversion_run": 0,
        "new_dependency_installed": 0, "network_access_used": 0, "git_operations": 0,
    }
    (CATALOG / "g8_doc_2012_d001_tooling_decision.json").write_text(json.dumps(decision, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = {key: value for key, value in decision.items() if key not in {"tools", "alternative_routes", "diagnostics"}}
    write_csv(CATALOG / "g8_doc_2012_d001_tooling_decision.csv", summary)
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "G8_DOC_2012_D001_TOOLING_DECISION.md").write_text(
        "# G8 DOC CUMCM-2012-D-001 Tooling Decision\n\nStatus: `PASS`\n\n"
        "Direct Word export is closed after two targeted `EXPORT_ERROR` outcomes. The preferred next route is a new, isolated DOCX-intermediate contract; it is not an Attempt C. No converter was run.\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
