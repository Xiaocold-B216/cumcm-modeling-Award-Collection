#!/usr/bin/env python3
"""Validate a manually produced candidate PDF without starting Word."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "scale"
TARGET = "CUMCM-2012-D-001"
SOURCE = ROOT / "2012年数学建模国赛真题+优秀论文" / "2012年优秀论文" / "2012D：机器人避障问题 (2).doc"
DOCX = ROOT / "tmp" / "g8_doc_2012_d001_docx_intermediate" / TARGET / "source_rebuilt.docx"
PDF = ROOT / "tmp" / "g8_doc_2012_d001_manual_print_to_pdf" / TARGET / "manual_print_candidate.pdf"
EXPECTED_SOURCE_SHA = "D93A9A6A9DE012927F8A5D4B36E1768CA3F6AFFB6952673F40FE2740D4032766"
EXPECTED_DOCX_SHA = "B948CA41387ABC408724B1D64286830B54B12198A33C54D8BE684661CA8937DC"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def evaluate(state: dict) -> dict:
    integrity = state["source_match"] and state["docx_match"]
    pdf_ok = all(state[key] for key in ("exists", "positive_size", "pdf_signature", "readable", "unencrypted", "page_count_positive"))
    return {"source_integrity_pass": int(integrity), "pdf_basic_validation_pass": int(pdf_ok), "status": "CANDIDATE_AVAILABLE" if integrity and pdf_ok else "BLOCKED"}


def pdf_state(path: Path) -> dict:
    state = {"exists": path.is_file(), "positive_size": False, "pdf_signature": False, "readable": False, "unencrypted": False, "page_count_positive": False, "page_count": 0}
    if not state["exists"]:
        return state
    state["positive_size"] = path.stat().st_size > 0
    state["pdf_signature"] = path.read_bytes()[:5] == b"%PDF-"
    pdfinfo = shutil.which("pdfinfo")
    if not pdfinfo:
        return state
    completed = subprocess.run([pdfinfo, str(path)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    state["readable"] = completed.returncode == 0
    for line in completed.stdout.splitlines():
        if line.startswith("Encrypted:"):
            state["unencrypted"] = line.split(":", 1)[1].strip().lower() == "no"
        if line.startswith("Pages:"):
            state["page_count"] = int(line.split(":", 1)[1].strip())
            state["page_count_positive"] = state["page_count"] > 0
    return state


def self_test() -> int:
    base = {"source_match": True, "docx_match": True, "exists": True, "positive_size": True, "pdf_signature": True, "readable": True, "unencrypted": True, "page_count_positive": True}
    cases = {"valid_pdf": base, "missing_pdf": {**base, "exists": False}, "zero_byte_pdf": {**base, "positive_size": False}, "html_renamed_pdf": {**base, "pdf_signature": False}, "invalid_signature": {**base, "pdf_signature": False}, "unreadable_pdf": {**base, "readable": False}, "source_sha_drift": {**base, "source_match": False}, "docx_sha_drift": {**base, "docx_match": False}}
    passed = evaluate(cases["valid_pdf"])["status"] == "CANDIDATE_AVAILABLE" and all(evaluate(value)["status"] == "BLOCKED" for name, value in cases.items() if name != "valid_pdf")
    print("POSTFLIGHT_REGRESSION_PASS=" + str(int(passed)))
    return 0 if passed else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output-path", type=Path, default=PDF)
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    source_sha, docx_sha = sha256(SOURCE), sha256(DOCX)
    state = pdf_state(args.output_path)
    verdict = evaluate({"source_match": source_sha == EXPECTED_SOURCE_SHA, "docx_match": docx_sha == EXPECTED_DOCX_SHA, **state})
    result = {
        "STAGE": "G8-DOC-CUMCM-2012-D-001-MANUAL-PRINT-TO-PDF-POSTFLIGHT", "STATUS": verdict["status"], "TARGET_PAPER_ID": TARGET,
        "SOURCE_SHA256": source_sha, "RENDER_INPUT_PATH": str(DOCX), "RENDER_INPUT_SHA256": docx_sha, "SOURCE_SHA_MISMATCH": int(source_sha != EXPECTED_SOURCE_SHA), "DERIVATIVE_DOCX_SHA_MISMATCH": int(docx_sha != EXPECTED_DOCX_SHA), "ORIGINAL_FILES_MODIFIED": 0,
        "PDF_OUTPUT_PATH": str(args.output_path), "PDF_OUTPUT_EXISTS": int(state["exists"]), "PDF_OUTPUT_SIZE": args.output_path.stat().st_size if state["exists"] else 0, "PDF_OUTPUT_SHA256": sha256(args.output_path) if state["exists"] else "", "PDF_SIGNATURE_VALID": int(state["pdf_signature"]), "PDF_POPPLER_READABLE": int(state["readable"]), "PDF_ENCRYPTED": int(not state["unencrypted"]) if state["exists"] else "UNAVAILABLE", "PDF_PAGE_COUNT": state["page_count"], "PDF_BASIC_VALIDATION_PASS": verdict["pdf_basic_validation_pass"],
        "MANUAL_PRINT_PDF_CANDIDATE_AVAILABLE": int(verdict["status"] == "CANDIDATE_AVAILABLE"), "renderer_application": "Microsoft Word", "render_method": "MANUAL_INTERACTIVE_PRINT", "printer_name": "Microsoft Print to PDF", "printer_driver": "Microsoft Print To PDF", "printer_port": "PORTPROMPT:", "manual_operator_required": 1, "automation_used": 0, "word_com_used": 0, "PRINT_CLICK_TIMESTAMP": "UNAVAILABLE", "PRINT_COMPLETION_EVIDENCE_TIMESTAMP": datetime.fromtimestamp(args.output_path.stat().st_mtime).astimezone().isoformat(timespec="seconds") if state["exists"] else "UNAVAILABLE", "POSTFLIGHT_TIMESTAMP": datetime.now().astimezone().isoformat(timespec="seconds"), "FORMAL_ARTIFACTS_GENERATED": 0, "NEXT": "G8-DOC-CUMCM-2012-D-001-MANUAL-PRINT-TO-PDF-QA" if verdict["status"] == "CANDIDATE_AVAILABLE" else "RETURN_TO_GOVERNANCE_WITH_POSTFLIGHT_EVIDENCE",
    }
    (CATALOG / "g8_doc_2012_d001_manual_print_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    return 0 if verdict["status"] == "CANDIDATE_AVAILABLE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
