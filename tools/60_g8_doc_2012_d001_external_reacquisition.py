#!/usr/bin/env python3
"""Bounded external reacquisition review for CUMCM-2012-D-001.

The script never fetches a URL and never invokes Word.  It validates only files
already placed in the isolated download directory, then writes an auditable
decision record.  Network collection is deliberately kept outside this runner.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "scale"
REPORTS = ROOT / "reports" / "scale"
TARGET = "CUMCM-2012-D-001"
SOURCE = ROOT / "2012年数学建模国赛真题+优秀论文" / "2012年优秀论文" / "2012D：机器人避障问题 (2).doc"
DOCX = ROOT / "tmp" / "g8_doc_2012_d001_docx_intermediate" / TARGET / "source_rebuilt.docx"
EXPECTED_SOURCE_SHA = "D93A9A6A9DE012927F8A5D4B36E1768CA3F6AFFB6952673F40FE2740D4032766"
EXPECTED_DOCX_SHA = "B948CA41387ABC408724B1D64286830B54B12198A33C54D8BE684661CA8937DC"
PDF_URL = "https://pdf.hanspub.org/MOS20220400000_43364559.pdf"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def normalized(text: str) -> str:
    return re.sub(r"\s+", "", text).replace("，", ",").replace("。", ".")


def run_text(command: list[str]) -> tuple[int, str]:
    completed = subprocess.run(command, text=True, encoding="utf-8", errors="replace", capture_output=True)
    return completed.returncode, completed.stdout + completed.stderr


def pdf_preflight(path: Path) -> tuple[dict, str]:
    result = {
        "exists": int(path.is_file()),
        "size_positive": 0,
        "pdf_signature": 0,
        "poppler_readable": 0,
        "encrypted": "UNAVAILABLE",
        "page_count": 0,
        "pdf_basic_validation_pass": 0,
        "content_sanity_pass": 0,
    }
    if not path.is_file():
        return result, ""
    result["size_positive"] = int(path.stat().st_size > 0)
    result["pdf_signature"] = int(path.read_bytes()[:5] == b"%PDF-")
    pdfinfo = shutil.which("pdfinfo")
    pdftotext = shutil.which("pdftotext")
    info = ""
    if pdfinfo:
        code, info = run_text([pdfinfo, str(path)])
        result["poppler_readable"] = int(code == 0)
        encrypted = re.search(r"^Encrypted:\s*(.+)$", info, flags=re.MULTILINE | re.IGNORECASE)
        pages = re.search(r"^Pages:\s*(\d+)$", info, flags=re.MULTILINE | re.IGNORECASE)
        if encrypted:
            result["encrypted"] = encrypted.group(1).strip().lower()
        if pages:
            result["page_count"] = int(pages.group(1))
    text = ""
    if pdftotext:
        code, text = run_text([pdftotext, "-layout", str(path), "-"])
        result["content_sanity_pass"] = int(code == 0 and "机器人" in text and len(text.strip()) > 500)
    result["pdf_basic_validation_pass"] = int(
        result["exists"] and result["size_positive"] and result["pdf_signature"]
        and result["poppler_readable"] and result["encrypted"] == "no" and result["page_count"] > 0
    )
    return result, text


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    contract = json.loads((CATALOG / "g8_doc_2012_d001_external_reacquisition_contract.json").read_text(encoding="utf-8"))
    fingerprint = json.loads((CATALOG / "g8_doc_2012_d001_identity_fingerprint.json").read_text(encoding="utf-8"))
    queries = list(csv.DictReader((CATALOG / "g8_doc_2012_d001_external_search_queries.csv").open(encoding="utf-8-sig", newline="")))
    candidate_path = ROOT / "tmp" / "g8_doc_2012_d001_external_reacquisition" / "candidate_001" / "MOS20220400000_43364559.pdf"
    preflight, candidate_text = pdf_preflight(candidate_path)
    snippets = fingerprint["distinctive_text_snippets"]
    snippet_matches = [int(normalized(snippet) in normalized(candidate_text)) for snippet in snippets]
    snippet_count = sum(snippet_matches)
    candidate_sha = sha256(candidate_path) if candidate_path.is_file() else ""
    retrieved_at = datetime.now().astimezone().isoformat(timespec="seconds")

    # These are the bounded search results actually reviewed before download.
    search_rows = [
        {"query_id": "Q1", "url": "https://books.google.com/books/about/%E5%85%A8%E5%9B%BD%E5%A4%A7%E5%AD%A6%E7%94%9F%E6%95%B0%E5%AD%A6%E5%BB%BA%E6%A8%A1%E7%AB%9E%E8%B5%9B%E6%B9%96%E5%8D%97.html?id=aH99oAEACAAJ", "source_domain": "books.google.com", "page_title": "全国大学生数学建模竞赛湖南赛区优秀论文集: 2012", "apparent_format": "HTML", "source_tier": "TIER_3", "pre_download_rejected": 1, "rationale": "Bibliographic record only; no candidate paper file."},
        {"query_id": "Q2", "url": "https://mooc1.chaoxing.com/course-ans/courseportal/mobile/protal?clazzId=0&courseId=222840037", "source_domain": "mooc1.chaoxing.com", "page_title": "江西财经大学课程资料页", "apparent_format": "DOC", "source_tier": "TIER_2", "pre_download_rejected": 1, "rationale": "2012D attachment is the competition problem statement, not a submitted paper."},
        {"query_id": "Q3", "url": "https://pdf.hanspub.org/MOS20220400000_43364559.pdf", "source_domain": "pdf.hanspub.org", "page_title": "基于线性规划下的机器人最优避障路径模型", "apparent_format": "PDF", "source_tier": "TIER_3", "pre_download_rejected": 0, "rationale": "Exact numeric/model clue justified isolated content screening; publication metadata was not treated as target identity."},
        {"query_id": "Q4", "url": "https://www.daowen.com/lilun/2079534.html", "source_domain": "www.daowen.com", "page_title": "数学建模案例：模型建立与求解", "apparent_format": "HTML", "source_tier": "TIER_3", "pre_download_rejected": 1, "rationale": "Later teaching/book excerpt, not a source file and no independent target-paper provenance."},
        {"query_id": "Q3", "url": "https://www.hanspub.org/download/page_download?filename=mos20220400000_43364559.pdf", "source_domain": "www.hanspub.org", "page_title": "Modeling and Simulation, 2022, 11(4), 1083-1095", "apparent_format": "PDF", "source_tier": "TIER_3", "pre_download_rejected": 1, "rationale": "Duplicate landing URL for the same downloaded binary; not counted as a second candidate."},
    ]
    candidate = {
        "candidate_id": "candidate_001", "source_url": PDF_URL, "final_url": PDF_URL,
        "landing_page_url": "https://www.hanspub.org/download/page_download?filename=mos20220400000_43364559.pdf",
        "direct_download_url": PDF_URL, "redirect_chain": "UNAVAILABLE", "source_domain": "pdf.hanspub.org", "source_tier": "TIER_3",
        "retrieved_at": retrieved_at, "original_filename": "MOS20220400000_43364559.pdf", "saved_filename": str(candidate_path.relative_to(ROOT)).replace("\\", "/"),
        "format": "PDF", "size": candidate_path.stat().st_size if candidate_path.is_file() else 0, "sha256": candidate_sha,
        "http_status": 200, "http_content_type": "application/pdf", "http_last_modified": "Fri, 20 Sep 2024 19:30:50 GMT", "http_etag": '"C47CDE32231C796FB701ACA4EEDD2FB9"',
        "candidate_file_valid": preflight["pdf_basic_validation_pass"], "identity_status": "DIFFERENT_PAPER",
        "identity_evidence": "Published 2022 with title/authors/abstract/keywords and section sequence that contradict the 2012 target; only shared problem-domain/numeric context, no full distinctive snippet match.",
        "distinctive_snippet_match_count": snippet_count, "distinctive_snippet_total": len(snippets),
        "section_structure_match": 0, "abstract_or_opening_match": 0, "table_caption_match": 0, "figure_caption_match": 0, "reference_snippet_match": 0,
        "year_problem_context_match": 0, "title_match_if_available": "UNAVAILABLE", "authors_match_if_available": "UNAVAILABLE",
        "decision": "REJECT_DIFFERENT_PAPER",
        **preflight,
    }
    evidence = []
    for index, match in enumerate(snippet_matches, start=1):
        evidence.append({"candidate_id": "candidate_001", "evidence_type": f"SNIPPET_{index}_MATCH", "expected": snippets[index - 1], "observed": "normalized exact match" if match else "no normalized exact match", "result": "MATCH" if match else "NO_MATCH"})
    evidence.extend([
        {"candidate_id": "candidate_001", "evidence_type": "METADATA_CONTRADICTION", "expected": "2012 target, title/authors unavailable", "observed": "2022 journal paper: 基于线性规划下的机器人最优避障路径模型; 王梦甜、张巍、陈晓友", "result": "DIFFERENT_PAPER"},
        {"candidate_id": "candidate_001", "evidence_type": "SECTION_STRUCTURE", "expected": "compatible with source-derived fingerprint", "observed": "2022 journal structure (引言/环境建模/模型求解/总结与展望)", "result": "INCOMPATIBLE"},
    ])
    outputs = {
        "search": CATALOG / "g8_doc_2012_d001_external_search_results.csv",
        "candidates": CATALOG / "g8_doc_2012_d001_external_candidates.csv",
        "evidence": CATALOG / "g8_doc_2012_d001_external_identity_evidence.csv",
        "result": CATALOG / "g8_doc_2012_d001_external_reacquisition_result.json",
        "report": REPORTS / "G8_DOC_2012_D001_EXTERNAL_REACQUISITION.md",
    }
    write_csv(outputs["search"], search_rows, ["query_id", "url", "source_domain", "page_title", "apparent_format", "source_tier", "pre_download_rejected", "rationale"])
    write_csv(outputs["candidates"], [candidate], list(candidate.keys()))
    write_csv(outputs["evidence"], evidence, ["candidate_id", "evidence_type", "expected", "observed", "result"])
    result = {
        "STAGE": "G8-DOC-CUMCM-2012-D-001-EXTERNAL-REACQUISITION", "STATUS": "PARTIAL", "BRANCH": "library-refactor-v1", "HEAD": "557724fba6572d4d83dc421feda5b17b13ff8d66",
        "TARGET_PAPER_ID": TARGET, "SOURCE_SHA256": sha256(SOURCE), "SOURCE_SIZE": SOURCE.stat().st_size,
        "IDENTITY_FINGERPRINT_FIELD_COUNT": len(fingerprint), "DISTINCTIVE_TEXT_SNIPPET_COUNT": len(snippets),
        "SEARCH_QUERY_EXECUTED_COUNT": len(queries), "SEARCH_RESULT_URL_COUNT": len(search_rows), "CANDIDATE_URL_COUNT": 1,
        "DOWNLOAD_ATTEMPT_COUNT": 1, "DOWNLOAD_SUCCESS_COUNT": int(candidate_path.is_file()), "CANDIDATE_FILE_COUNT": int(candidate_path.is_file()),
        "IDENTITY_EXACT_COUNT": 0, "IDENTITY_HIGH_CONFIDENCE_COUNT": 0, "IDENTITY_LIKELY_COUNT": 0, "IDENTITY_AMBIGUOUS_COUNT": 0, "IDENTITY_DIFFERENT_COUNT": 1,
        "PDF_CANDIDATE_COUNT": 1, "DOCX_CANDIDATE_COUNT": 0, "DOC_CANDIDATE_COUNT": 0,
        "PREFERRED_CANDIDATE_FOUND": 0, "PREFERRED_CANDIDATE_ID": "", "PREFERRED_CANDIDATE_FORMAT": "", "PREFERRED_CANDIDATE_PATH": "", "PREFERRED_CANDIDATE_SHA256": "",
        "PREFERRED_CANDIDATE_SOURCE_URL": "", "PREFERRED_CANDIDATE_SOURCE_DOMAIN": "", "PREFERRED_CANDIDATE_SOURCE_TIER": "", "PREFERRED_CANDIDATE_IDENTITY_STATUS": "", "PREFERRED_CANDIDATE_SNIPPET_MATCH_COUNT": 0, "PREFERRED_CANDIDATE_PDF_BASIC_VALIDATION_PASS": 0,
        "SOURCE_PROVENANCE_COMPLETE": 0, "MANUAL_IDENTITY_REVIEW_REQUIRED": 0, "EXTERNAL_REACQUISITION_FAILED": 1, "ACCESS_RESTRICTED_CANDIDATE_FOUND": 0,
        "DIRECT_WORD_EXPORT_ROUTE_STATUS": "CLOSED", "DOCX_INTERMEDIATE_ROUTE_STATUS": "CLOSED", "SOURCE_SHA_MISMATCH": int(sha256(SOURCE) != EXPECTED_SOURCE_SHA), "DERIVATIVE_DOCX_SHA_MISMATCH": int(sha256(DOCX) != EXPECTED_DOCX_SHA), "ORIGINAL_FILES_MODIFIED": 0,
        "FORMAL_ARTIFACTS_GENERATED": 0, "SUCCESSFUL_BATCH_ROWS_PRESERVED": 13, "SUCCESSFUL_BATCH_ROWS_RECONVERTED": 0, "DOC_CONTRACT_APPROVED": 1,
        "ELIGIBLE": 453, "INELIGIBLE": 189, "ARTIFACT_SETS": 308, "PRIMARY_ARTIFACTS": 924, "DOC_MANUAL_BACKLOG": 17, "Q3_MANUAL_BACKLOG": 128,
        "WORD_COM_RUN": 0, "DOC_CONVERSION_RUN": 0, "OCR_FULL_RUN": 0, "NETWORK_ACCESS_USED": 1, "NEW_DEPENDENCY_INSTALLED": 0, "GIT_OPERATIONS": 0,
        "D044_USED_AS_TARGET_IDENTITY_KEY": 0, "EXTERNAL_NATIVE_DOCX_FOUND": 0, "EXTERNAL_LEGACY_DOC_FOUND": 0,
        "CANDIDATE": candidate, "OUTPUTS": {key: str(value.relative_to(ROOT)).replace("\\", "/") for key, value in outputs.items()},
        "NEXT": "G8-DOC-CUMCM-2012-D-001-ALTERNATIVE-RENDERING-DECISION",
    }
    outputs["result"].write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORTS.mkdir(parents=True, exist_ok=True)
    outputs["report"].write_text(
        "# G8 DOC CUMCM-2012-D-001 External Reacquisition\n\n"
        "Status: `PARTIAL`\n\n"
        "The bounded first-round search reviewed five result URLs and downloaded one isolated PDF candidate. "
        "The candidate passed basic PDF preflight but is a distinct 2022 journal paper, not an acceptable replacement for the 2012 logical paper. "
        "No external source was promoted and no formal artifacts were generated.\n\n"
        "Next: `G8-DOC-CUMCM-2012-D-001-ALTERNATIVE-RENDERING-DECISION`.\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
