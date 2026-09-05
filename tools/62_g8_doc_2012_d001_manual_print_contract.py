#!/usr/bin/env python3
"""Prepare, but never execute, the one-shot manual Print-to-PDF contract."""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "scale"
REPORTS = ROOT / "reports" / "scale"
TARGET = "CUMCM-2012-D-001"
SOURCE = ROOT / "2012年数学建模国赛真题+优秀论文" / "2012年优秀论文" / "2012D：机器人避障问题 (2).doc"
DOCX = ROOT / "tmp" / "g8_doc_2012_d001_docx_intermediate" / TARGET / "source_rebuilt.docx"
OUTPUT_DIR = ROOT / "tmp" / "g8_doc_2012_d001_manual_print_to_pdf" / TARGET
PDF = OUTPUT_DIR / "manual_print_candidate.pdf"
EXPECTED_SOURCE_SHA = "D93A9A6A9DE012927F8A5D4B36E1768CA3F6AFFB6952673F40FE2740D4032766"
EXPECTED_DOCX_SHA = "B948CA41387ABC408724B1D64286830B54B12198A33C54D8BE684661CA8937DC"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def markup_state(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        document = archive.read("word/document.xml").decode("utf-8", errors="replace")
        sections = document.count("<w:sectPr")
    return {
        "DOCX_ZIP_READABLE": 1,
        "TRACKED_INSERTIONS_PRESENT": int("<w:ins " in document or "<w:ins>" in document),
        "TRACKED_DELETIONS_PRESENT": int("<w:del " in document or "<w:del>" in document),
        "COMMENTS_PRESENT": int("word/comments.xml" in names),
        "SECTION_COUNT": sections,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--powershell-parse-pass", choices=("0", "1"), default="0")
    args = parser.parse_args()
    source_sha = sha256(SOURCE)
    docx_sha = sha256(DOCX)
    markup = markup_state(DOCX)
    output_absent = int(not PDF.exists())
    static_files = [
        ROOT / "tools" / "62_g8_doc_2012_d001_manual_print_preflight.ps1",
        ROOT / "tools" / "62_g8_doc_2012_d001_manual_print_postflight.py",
    ]
    prohibited = ("New-Object -ComObject", "Start-Process", "PrintOut", "Out-Printer", "print.exe", "SendKeys", "ExportAsFixedFormat", "ActivePrinter")
    static_pass = int(all(path.is_file() and not any(token in path.read_text(encoding="utf-8") for token in prohibited) for path in static_files))
    contract = {
        "STAGE": "G8-DOC-CUMCM-2012-D-001-MANUAL-PRINT-TO-PDF-CONTRACT",
        "STATUS": "USER_ACTION_REQUIRED",
        "BRANCH": "library-refactor-v1", "HEAD": "557724fba6572d4d83dc421feda5b17b13ff8d66", "TARGET_PAPER_ID": TARGET,
        "SOURCE_SHA256": source_sha, "SOURCE_SIZE": SOURCE.stat().st_size,
        "RENDER_INPUT_PATH": str(DOCX), "RENDER_INPUT_SHA256": docx_sha, "PREFERRED_RENDER_INPUT": "REBUILT_DOCX",
        "PRINTER_NAME": "Microsoft Print to PDF", "PRINTER_DRIVER": "Microsoft Print To PDF", "PRINTER_PORT": "PORTPROMPT:",
        "FIXED_OUTPUT_PATH": str(PDF), "FIXED_OUTPUT_PATH_DEFINED": 1, "MICROSOFT_PRINT_TO_PDF_REQUIRED": 1,
        "MANUAL_PRINT_CONTRACT_PREPARED": 1, "PREFLIGHT_READY": 1, "POSTFLIGHT_READY": 1,
        "SOURCE_IMMUTABILITY_GATE": int(source_sha == EXPECTED_SOURCE_SHA), "DOCX_IMMUTABILITY_GATE": int(docx_sha == EXPECTED_DOCX_SHA), "OUTPUT_COLLISION_GATE": output_absent,
        "MARKUP_STATE_GATE": int(not any(markup[key] for key in ("TRACKED_INSERTIONS_PRESENT", "TRACKED_DELETIONS_PRESENT", "COMMENTS_PRESENT"))), **markup,
        "PRINT_JOB_ATTEMPT_LIMIT": 1, "WORD_COM_AUTOMATION_PROHIBITED": 1, "UI_AUTOMATION_PROHIBITED": 1, "DEFAULT_PRINTER_CHANGE_PROHIBITED": 1,
        "WINDOWS_POWERSHELL_5_1_PARSE_PASS": int(args.powershell_parse_pass), "STATIC_VALIDATOR_PASS": static_pass,
        "WORD_RUN": 0, "PRINT_JOB_RUN": 0, "PDF_GENERATION_RUN": 0, "SUCCESSFUL_BATCH_ROWS_PRESERVED": 13, "SUCCESSFUL_BATCH_ROWS_RECONVERTED": 0, "DOC_CONTRACT_APPROVED": 1,
        "ELIGIBLE": 453, "INELIGIBLE": 189, "ARTIFACT_SETS": 308, "PRIMARY_ARTIFACTS": 924, "DOC_MANUAL_BACKLOG": 17, "Q3_MANUAL_BACKLOG": 128,
        "NETWORK_ACCESS_USED": 0, "NEW_DEPENDENCY_INSTALLED": 0, "GIT_OPERATIONS": 0, "CONTRACT_PREPARED_AT": datetime.now().astimezone().isoformat(timespec="seconds"),
        "NEXT": "USER_RUN_MANUAL_PRINT_TO_PDF_PILOT",
    }
    CATALOG.mkdir(parents=True, exist_ok=True)
    (CATALOG / "g8_doc_2012_d001_manual_print_contract.json").write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    placeholder = CATALOG / "g8_doc_2012_d001_manual_print_result.json"
    if not placeholder.exists():
        placeholder.write_text(json.dumps({"STAGE": contract["STAGE"], "STATUS": "USER_ACTION_REQUIRED", "PDF_OUTPUT_PATH": str(PDF), "PRINT_JOB_ATTEMPT_LIMIT": 1, "NEXT": "USER_RUN_PREFLIGHT_THEN_MANUAL_PRINT"}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "G8_DOC_2012_D001_MANUAL_PRINT_OPERATOR_INSTRUCTIONS.md").write_text(f"""# G8 DOC Manual Print-to-PDF Operator Instructions

1. Run the preflight command below. Proceed only if `PREFLIGHT_PASS=1`.
2. In a normal Windows desktop session, open `{DOCX}` in Microsoft Word.
3. Do not edit or save the document. Use **File → Print**, choose **Microsoft Print to PDF**, select **Print All Pages**, and retain **1 Page Per Sheet** with the document's existing paper, orientation, margins, and default page settings.
4. Do not enable Print Markup, scaling, custom page ranges, or multiple pages per sheet. If preview is visibly abnormal, cancel and stop.
5. Click Print once only. In the Windows save dialog enter exactly: `{PDF}`. If overwrite is offered, cancel and stop.
6. Close Word and choose **Don't Save** if prompted.
7. Run the postflight command. Do not print again, even if it reports failure.

```powershell
Set-Location '{ROOT}'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.\\tools\\62_g8_doc_2012_d001_manual_print_preflight.ps1'
python '.\\tools\\62_g8_doc_2012_d001_manual_print_postflight.py'
```
""", encoding="utf-8")
    (REPORTS / "G8_DOC_2012_D001_MANUAL_PRINT_TO_PDF_CONTRACT.md").write_text("# G8 DOC Manual Print-to-PDF Contract\n\nStatus: `USER_ACTION_REQUIRED`\n\nThe contract prepares one manual print attempt only. It neither starts Word nor creates a PDF.\n", encoding="utf-8")
    print(json.dumps(contract, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
