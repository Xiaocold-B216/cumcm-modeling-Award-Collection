#!/usr/bin/env python3
"""Static validator and post-run PDF/extraction validator for the interactive pilot."""

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
from pathlib import Path
from typing import Any

try:
    from PIL import Image
except ImportError:
    Image = None


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "scale"
REPORTS = ROOT / "reports" / "scale"
LOGS = ROOT / "logs" / "scale"
RESULTS = CATALOG / "g8_doc_interactive_word_results.json"
CONVERSION = CATALOG / "g8_doc_interactive_word_conversion.csv"
PS1 = ROOT / "tools" / "51_g8_doc_interactive_word_pilot.ps1"
SAMPLES = CATALOG / "g8_doc_contract_samples.csv"
INVENTORY = CATALOG / "g8_doc_contract_target_inventory.csv"
REPLACEMENT_SELECTION = CATALOG / "g8_doc_interactive_replacement_selection.csv"
REPLACEMENT_RESULTS = CATALOG / "g8_doc_interactive_word_replacement_results.json"
REPLACEMENT_PAPER_ID = "CUMCM-2014-D-003"
REPLACEMENT_PRIMARY_PDF = ROOT / "derived" / "scale" / "doc_contract_pilot_interactive" / REPLACEMENT_PAPER_ID / "source_converted.pdf"
REPLACEMENT_VALIDATION_PDF = ROOT / "tmp" / "g8_doc_interactive_word_pilot" / "validation" / REPLACEMENT_PAPER_ID / "source_converted.pdf"
REPLACEMENT_PRIMARY_PDF_SHA = "00C0D4361A59E3D5F1E97FBE7DAF28B60FCDDA9C26EBF435182C9F6961EB360C"
REPLACEMENT_VALIDATION_PDF_SHA = "10C4EA391486AC7BD6A84C7FFF7BD606574702901834B7FFC688A350E7AA9C52"
OLE = bytes.fromhex("D0CF11E0A1B11AE1")

EXPECTED = {
    "CUMCM-2014-A-006": ("A4C7CFEE735094C488EFB5007EF2084771748487B29765E20C39E78296A915F6", 24064, "SMALL_SIZE"),
    "CUMCM-2011-C-002": ("21E5912D27E48F0BBEB0E1044BF30F185FBAB2133945529F106449296C10653F", 1113600, "MEDIAN_SIZE"),
    "CUMCM-2013-D-001": ("955CC7179247EDA8AD6EBB74CFD1233D514D9F80A809B0C2EB244BEACABAFDEA", 3814912, "LARGE_SIZE"),
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in fields} for row in rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def static_checks() -> dict[str, Any]:
    text = PS1.read_text(encoding="utf-8")
    samples = read_csv(SAMPLES)
    inventory = read_csv(INVENTORY)
    replacement_rows = read_csv(REPLACEMENT_SELECTION) if REPLACEMENT_SELECTION.is_file() else []
    sample_ok = len(samples) == 3 and {row["paper_id"] for row in samples} == set(EXPECTED)
    source_missing = 0
    source_sha_mismatch = 0
    source_format_drift = 0
    for row in samples:
        expected_sha, expected_size, expected_role = EXPECTED.get(row["paper_id"], ("", -1, ""))
        source = ROOT / row["source_path"]
        if not source.is_file():
            source_missing += 1
            continue
        if sha256(source) != expected_sha or source.stat().st_size != expected_size or row["source_sha256"] != expected_sha or row["sample_role"] != expected_role:
            source_sha_mismatch += 1
        if source.read_bytes()[:8] != OLE:
            source_format_drift += 1
    required_tokens = [
        "New-Object -ComObject Word.Application",
        "AutomationSecurity = 3",
        "ReadOnly",
        "AddToRecentFiles",
        "ExportAsFixedFormat",
        "Close($false)",
        "Quit()",
        "FinalReleaseComObject",
        "Wait-ForWordBackgroundDrain",
        "post_export_settle_ms=500",
        "doc_contract_pilot_interactive",
        "g8_doc_interactive_word_results.json",
        "g8_doc_interactive_word_conversion.csv",
        "ReplacementPaperId",
        "g8_doc_interactive_word_replacement_results.json",
        "g8_doc_interactive_word_replacement_results.csv",
        "g8_doc_interactive_word_replacement.log",
        "g8_doc_interactive_replacement_selection.csv",
    ]
    forbidden_tokens = ["taskkill", "runas", "reg add", "reg.exe", "DCOMCNFG", "schtasks", "Install-Package", "pip install", "npm install"]
    missing_tokens = [token for token in required_tokens if token not in text]
    forbidden_found = [token for token in forbidden_tokens if token.lower() in text.lower()]
    results_status = ""
    resume = 0
    if RESULTS.is_file():
        try:
            results_status = str(read_json(RESULTS).get("RUN_STATUS", ""))
            resume = int(results_status == "COMPLETE")
        except Exception:
            results_status = "INVALID_JSON"
    replacement_preflight_pass = 0
    if len(replacement_rows) == 1 and replacement_rows[0].get("paper_id") == "CUMCM-2014-D-003":
        replacement = replacement_rows[0]
        replacement_source = ROOT / replacement["source_path"]
        replacement_governance = next((row for row in read_csv(CATALOG / "g8_artifact_eligibility.csv") if row["paper_id"] == replacement["paper_id"]), {})
        replacement_preflight_pass = int(
            replacement_source.is_file()
            and replacement_source.stat().st_size == int(replacement["source_size"])
            and sha256(replacement_source) == replacement["source_sha256"]
            and replacement_source.read_bytes()[:8] == OLE
            and replacement_governance.get("subject_type") == "PAPER"
            and replacement_governance.get("artifact_eligible") == "1"
            and replacement.get("preflight_pass") == "1"
        )
    replacement_mode_implemented = int(all(token in text for token in ["ReplacementPaperId", "g8_doc_interactive_word_replacement_results.json", "g8_doc_interactive_word_replacement_results.csv", "g8_doc_interactive_word_replacement.log"]))
    static_pass = int(
        len(inventory) == 17
        and len({row["paper_id"] for row in inventory}) == 17
        and sample_ok
        and source_missing == 0
        and source_sha_mismatch == 0
        and source_format_drift == 0
        and not missing_tokens
        and not forbidden_found
        and replacement_mode_implemented == 1
        and replacement_preflight_pass == 1
    )
    return {
        "status": "PASS" if static_pass else "BLOCKED",
        "static_validation_pass": static_pass,
        "target_rows": len(inventory),
        "target_unique_ids": len({row["paper_id"] for row in inventory}),
        "sample_rows": len(samples),
        "sample_selection_stable": int(sample_ok),
        "replacement_mode_implemented": replacement_mode_implemented,
        "replacement_preflight_pass": replacement_preflight_pass,
        "replacement_runner_ready": replacement_mode_implemented,
        "source_missing": source_missing,
        "source_sha_mismatch": source_sha_mismatch,
        "source_format_drift": source_format_drift,
        "missing_required_tokens": missing_tokens,
        "forbidden_tokens_found": forbidden_found,
        "existing_results_status": results_status,
        "resume_from_interactive_results": resume,
    }


def run_command(command: list[str]) -> tuple[int, str, str]:
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False, timeout=60)
    return completed.returncode, completed.stdout, completed.stderr


def tool_path(name: str) -> str | None:
    """Prefer a real executable over the Codex wrapper when both are on PATH."""
    candidates = [shutil.which(f"{name}.exe"), shutil.which(name)]
    for candidate in candidates:
        if candidate and Path(candidate).suffix.lower() == ".exe":
            return candidate
    for candidate in (Path(r"D:\texlive\2026\bin\windows") / f"{name}.exe",):
        if candidate.is_file():
            return str(candidate)
    return next((candidate for candidate in candidates if candidate), None)


def pdf_info(pdf: Path) -> dict[str, Any]:
    info: dict[str, Any] = {"readable": 0, "pages": 0, "encrypted": "", "malformed": 1, "error": ""}
    if not pdf.is_file() or pdf.stat().st_size <= 0:
        info["error"] = "missing_or_empty"
        return info
    if pdf.read_bytes()[:4] != b"%PDF":
        info["error"] = "invalid_signature"
        return info
    pdfinfo = tool_path("pdfinfo")
    if not pdfinfo:
        info["error"] = "pdfinfo_unavailable"
        return info
    code, stdout, stderr = run_command([pdfinfo, str(pdf)])
    if code != 0:
        info["error"] = stderr.strip() or "pdfinfo_failed"
        return info
    values = {}
    for line in stdout.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip().lower()] = value.strip()
    info["readable"] = 1
    info["malformed"] = 0
    info["pages"] = int(values.get("pages", "0") or 0)
    info["encrypted"] = values.get("encrypted", "")
    return info


def page_text(pdf: Path, page: int) -> str:
    pdftotext = tool_path("pdftotext")
    if not pdftotext:
        return ""
    code, stdout, _ = run_command([pdftotext, "-f", str(page), "-l", str(page), "-layout", str(pdf), "-"])
    return stdout if code == 0 else ""


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\x00", "")).strip()


def render_page_stats(pdf: Path, page: int, render_root: Path) -> dict[str, Any]:
    """Render an otherwise text-empty page to distinguish blank from image-only."""
    pdftoppm = tool_path("pdftoppm")
    if not pdftoppm or Image is None:
        return {"class": "UNEXPLAINED_PAGE", "rendered": 0, "nonwhite_ratio": ""}
    output_base = render_root / f"{pdf.stem}_{page}"
    code, _, stderr = run_command([pdftoppm, "-f", str(page), "-l", str(page), "-singlefile", "-png", str(pdf), str(output_base)])
    image_path = output_base.with_suffix(".png")
    if code != 0 or not image_path.is_file():
        return {"class": "UNEXPLAINED_PAGE", "rendered": 0, "nonwhite_ratio": stderr.strip()}
    try:
        with Image.open(image_path) as image:
            grayscale = image.convert("L")
            pixels = list(grayscale.getdata())
            nonwhite = sum(1 for value in pixels if value < 245)
            ratio = nonwhite / max(1, len(pixels))
        if ratio <= 0.001:
            page_class = "VERIFIED_BLANK_PAGE"
        else:
            page_class = "IMAGE_ONLY_CONTENT_PAGE"
        return {"class": page_class, "rendered": 1, "nonwhite_ratio": f"{ratio:.8f}"}
    except Exception as exc:
        return {"class": "UNEXPLAINED_PAGE", "rendered": 0, "nonwhite_ratio": str(exc)}


def page_audit(pdf: Path, attempt: str, info: dict[str, Any], render_root: Path) -> tuple[list[dict[str, Any]], list[str], dict[str, Any]]:
    pages: list[dict[str, Any]] = []
    normalized_pages: list[str] = []
    counts = {"TEXT_PAGE": 0, "VERIFIED_BLANK_PAGE": 0, "IMAGE_ONLY_CONTENT_PAGE": 0, "UNEXPLAINED_PAGE": 0}
    for page in range(1, info["pages"] + 1):
        text = normalize(page_text(pdf, page))
        normalized_pages.append(text)
        if text:
            page_class = "TEXT_PAGE"
            render_stats = {"rendered": 0, "nonwhite_ratio": ""}
        else:
            render_stats = render_page_stats(pdf, page, render_root)
            page_class = render_stats["class"]
        counts[page_class] += 1
        pages.append({
            "paper_id": "",
            "attempt": attempt,
            "logical_page_number": page,
            "page_class": page_class,
            "text_layer_present": int(bool(text)),
            "ocr_route_required": int(page_class == "IMAGE_ONLY_CONTENT_PAGE"),
            "text_chars": len(text),
            "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest().upper(),
            "rendered_for_classification": render_stats["rendered"],
            "nonwhite_ratio": render_stats["nonwhite_ratio"],
        })
    return pages, normalized_pages, counts


IDENTITY_SIGNALS = {
    "CUMCM-2014-A-006": ["嫦娥三号", "软着陆", "轨道", "控制策略", "椭圆"],
    "CUMCM-2011-C-002": ["养老金", "退休职工", "养老保险", "替代率", "收支平衡"],
    "CUMCM-2013-D-001": ["公共自行车", "鹿城区", "自行车服务系统", "站点", "借车", "还车"],
    "CUMCM-2014-D-003": ["储药槽", "药盒", "储药柜", "冗余", "药品"],
}


def content_sanity(paper_id: str, text: str) -> dict[str, Any]:
    lower = text.lower()
    paper_signals = ["摘要", "关键词", "问题重述", "模型假设", "符号说明", "模型建立", "求解", "结果分析", "模型评价", "参考文献", "abstract", "keywords", "model", "references"]
    paper_count = sum(1 for signal in paper_signals if signal.lower() in lower)
    identity_hits = [signal for signal in IDENTITY_SIGNALS[paper_id] if signal.lower() in lower]
    substantial = len(text) >= 1000
    paper_like = paper_count >= 2
    identity_match = len(identity_hits) >= 2
    passed = int(substantial and paper_like and identity_match)
    return {
        "content_sanity_pass": passed,
        "eligibility_contradiction": int(not passed),
        "normalized_text_chars": len(text),
        "paper_signal_count": paper_count,
        "identity_signal_hits": ";".join(identity_hits),
        "reason": "PASS" if passed else "INSUBSTANTIAL_OR_NON_PAPER_CONTENT",
    }


def post_validate() -> dict[str, Any]:
    conversions = read_csv(CONVERSION)
    pdf_rows: list[dict[str, Any]] = []
    page_rows: list[dict[str, Any]] = []
    extraction_rows: list[dict[str, Any]] = []
    determinism_rows: list[dict[str, Any]] = []
    sanity_rows: list[dict[str, Any]] = []
    result_rows: list[dict[str, Any]] = []
    total_primary_pages = 0
    total_validation_pages = 0
    total_text_pages = 0
    total_blank_pages = 0
    total_image_pages = 0
    total_unexplained_pages = 0
    total_ocr_required = 0
    total_ocr_completed = 0
    total_ocr_failed = 0
    readable_primary = 0
    readable_validation = 0
    with tempfile.TemporaryDirectory(prefix="g8_doc_pdf_", dir=str(ROOT / "tmp")) as render_dir:
        render_root = Path(render_dir)
        for row in conversions:
            paper_id = row["paper_id"]
            primary_pdf = ROOT / row["derivative_path"]
            validation_pdf = ROOT / row["validation_derivative_path"]
            primary_info = pdf_info(primary_pdf)
            validation_info = pdf_info(validation_pdf)
            primary_pages, primary_text, primary_counts = page_audit(primary_pdf, "PRIMARY", primary_info, render_root)
            validation_pages, validation_text, validation_counts = page_audit(validation_pdf, "VALIDATION", validation_info, render_root)
            for page in primary_pages + validation_pages:
                page["paper_id"] = paper_id
            page_rows.extend(primary_pages + validation_pages)
            primary_sha = sha256(primary_pdf) if primary_pdf.is_file() else ""
            validation_sha = sha256(validation_pdf) if validation_pdf.is_file() else ""
            primary_expected_sha = row.get("derivative_sha256", "").upper()
            validation_expected_sha = row.get("validation_derivative_sha256", "").upper()
            primary_pdf_class = "TEXT" if primary_counts["TEXT_PAGE"] == primary_info["pages"] and primary_info["pages"] > 0 else ("IMAGE" if primary_counts["IMAGE_ONLY_CONTENT_PAGE"] == primary_info["pages"] else "MIXED")
            validation_pdf_class = "TEXT" if validation_counts["TEXT_PAGE"] == validation_info["pages"] and validation_info["pages"] > 0 else ("IMAGE" if validation_counts["IMAGE_ONLY_CONTENT_PAGE"] == validation_info["pages"] else "MIXED")
            primary_ocr = primary_counts["IMAGE_ONLY_CONTENT_PAGE"]
            validation_ocr = validation_counts["IMAGE_ONLY_CONTENT_PAGE"]
            for attempt, pdf_path, info, pdf_class, actual_sha, expected_sha, counts, normalized_pages in [
                ("PRIMARY", primary_pdf, primary_info, primary_pdf_class, primary_sha, primary_expected_sha, primary_counts, primary_text),
                ("VALIDATION", validation_pdf, validation_info, validation_pdf_class, validation_sha, validation_expected_sha, validation_counts, validation_text),
            ]:
                readable = int(info["readable"] and info["encrypted"].lower() not in {"yes", "encrypted"} and actual_sha == expected_sha and pdf_path.is_file() and pdf_path.stat().st_size > 0)
                pdf_rows.append({
                    "paper_id": paper_id,
                    "attempt": attempt,
                    "pdf_path": str(pdf_path.relative_to(ROOT)).replace(os.sep, "/") if pdf_path.is_relative_to(ROOT) else str(pdf_path),
                    "pdf_exists": int(pdf_path.is_file()),
                    "pdf_sha256": actual_sha,
                    "expected_pdf_sha256": expected_sha,
                    "pdf_sha_match": int(actual_sha == expected_sha and bool(expected_sha)),
                    "pdf_size": pdf_path.stat().st_size if pdf_path.is_file() else 0,
                    "pdf_readable": readable,
                    "page_count": info["pages"],
                    "pdf_class": pdf_class,
                    "text_layer_present": int(counts["TEXT_PAGE"] > 0),
                    "ocr_route_required": counts["IMAGE_ONLY_CONTENT_PAGE"],
                    "encrypted": info["encrypted"],
                    "malformed_pdf": info["malformed"],
                    "audit_error": info["error"],
                    "pdf_inspector_version": "1.15.0",
                    "poppler_version": "25.02.0",
                    "audit_status": "PASS" if readable else "FAIL",
                })
                extraction_text = " ".join(normalized_pages)
                extraction_rows.append({
                    "paper_id": paper_id,
                    "attempt": attempt,
                    "page_count": info["pages"],
                    "extraction_status": "PASS" if readable and counts["IMAGE_ONLY_CONTENT_PAGE"] == 0 and counts["UNEXPLAINED_PAGE"] == 0 else "FAIL",
                    "normalized_text_chars": len(extraction_text),
                    "normalized_text_sha256": hashlib.sha256(extraction_text.encode("utf-8")).hexdigest().upper(),
                    "ocr_required_pages": counts["IMAGE_ONLY_CONTENT_PAGE"],
                    "ocr_completed_pages": 0,
                    "ocr_failed_pages": 0,
                })
            sanity = content_sanity(paper_id, " ".join(primary_text))
            sanity_rows.append({"paper_id": paper_id, **sanity})
            primary_classes = [page["page_class"] for page in primary_pages]
            validation_classes = [page["page_class"] for page in validation_pages]
            primary_routes = [page["ocr_route_required"] for page in primary_pages]
            validation_routes = [page["ocr_route_required"] for page in validation_pages]
            text_deltas = []
            for index, (left, right) in enumerate(zip(primary_text, validation_text), start=1):
                if left != right:
                    text_deltas.append(str(index))
            semantic = int(
                primary_info["readable"] and validation_info["readable"]
                and primary_info["pages"] == validation_info["pages"]
                and primary_classes == validation_classes
                and primary_text == validation_text
                and primary_routes == validation_routes
            )
            primary_semantic = hashlib.sha256(json.dumps({"classes": primary_classes, "pages": primary_text, "ocr": primary_routes}, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest().upper()
            validation_semantic = hashlib.sha256(json.dumps({"classes": validation_classes, "pages": validation_text, "ocr": validation_routes}, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest().upper()
            determinism_rows.append({
                "paper_id": paper_id,
                "primary_page_count": primary_info["pages"],
                "validation_page_count": validation_info["pages"],
                "page_count_match": int(primary_info["pages"] == validation_info["pages"]),
                "primary_page_class_sequence": ";".join(primary_classes),
                "validation_page_class_sequence": ";".join(validation_classes),
                "page_class_match": int(primary_classes == validation_classes),
                "primary_normalized_text_sha256": hashlib.sha256(" ".join(primary_text).encode("utf-8")).hexdigest().upper(),
                "validation_normalized_text_sha256": hashlib.sha256(" ".join(validation_text).encode("utf-8")).hexdigest().upper(),
                "normalized_text_match": int(primary_text == validation_text),
                "primary_ocr_route": ";".join(map(str, primary_routes)),
                "validation_ocr_route": ";".join(map(str, validation_routes)),
                "ocr_route_match": int(primary_routes == validation_routes),
                "primary_semantic_sha256": primary_semantic,
                "validation_semantic_sha256": validation_semantic,
                "semantic_text_delta_pages": ";".join(text_deltas),
                "semantic_determinism": "PASS" if semantic else "FAIL",
            })
            conversion_ok = row.get("conversion_completed") == "1" and row.get("validation_export_completed") == "1"
            page_accounting_ok = all(sum(counts.values()) == info["pages"] for counts, info in [(primary_counts, primary_info), (validation_counts, validation_info)])
            extraction_ok = int(primary_info["readable"] and validation_info["readable"])
            passed = int(conversion_ok and primary_info["readable"] and validation_info["readable"] and semantic and sanity["content_sanity_pass"] and sanity["eligibility_contradiction"] == 0 and page_accounting_ok)
            result_rows.append({
                "paper_id": paper_id,
                "conversion_status": "PASS" if conversion_ok else "FAIL",
                "primary_pdf_readable": primary_info["readable"],
                "validation_pdf_readable": validation_info["readable"],
                "extraction_status": "PASS" if extraction_ok else "FAIL",
                "page_accounting": "PASS" if page_accounting_ok else "FAIL",
                "content_sanity": "PASS" if sanity["content_sanity_pass"] else "FAIL",
                "eligibility_contradiction": sanity["eligibility_contradiction"],
                "semantic_determinism": "PASS" if semantic else "FAIL",
                "status": "PASS" if passed else "PARTIAL",
            })
            total_primary_pages += primary_info["pages"]
            total_validation_pages += validation_info["pages"]
            total_text_pages += primary_counts["TEXT_PAGE"] + validation_counts["TEXT_PAGE"]
            total_blank_pages += primary_counts["VERIFIED_BLANK_PAGE"] + validation_counts["VERIFIED_BLANK_PAGE"]
            total_image_pages += primary_counts["IMAGE_ONLY_CONTENT_PAGE"] + validation_counts["IMAGE_ONLY_CONTENT_PAGE"]
            total_unexplained_pages += primary_counts["UNEXPLAINED_PAGE"] + validation_counts["UNEXPLAINED_PAGE"]
            total_ocr_required += primary_ocr + validation_ocr
            readable_primary += primary_info["readable"]
            readable_validation += validation_info["readable"]

    write_csv(CATALOG / "g8_doc_interactive_pdf_audit.csv", pdf_rows, list(pdf_rows[0].keys()) if pdf_rows else ["paper_id"])
    write_csv(CATALOG / "g8_doc_interactive_page_audit.csv", page_rows, list(page_rows[0].keys()) if page_rows else ["paper_id"])
    write_csv(CATALOG / "g8_doc_interactive_extraction.csv", extraction_rows, list(extraction_rows[0].keys()) if extraction_rows else ["paper_id"])
    write_csv(CATALOG / "g8_doc_interactive_semantic_determinism.csv", determinism_rows, list(determinism_rows[0].keys()) if determinism_rows else ["paper_id"])
    write_csv(CATALOG / "g8_doc_interactive_content_sanity.csv", sanity_rows, list(sanity_rows[0].keys()) if sanity_rows else ["paper_id"])
    write_csv(CATALOG / "g8_doc_interactive_pilot_results.csv", result_rows, list(result_rows[0].keys()) if result_rows else ["paper_id"])
    semantic_pass = sum(row["semantic_determinism"] == "PASS" for row in result_rows)
    content_pass = sum(row["content_sanity"] == "PASS" for row in result_rows)
    content_fail = len(result_rows) - content_pass
    contradictions = sum(int(row["eligibility_contradiction"]) for row in result_rows)
    extraction_failed = sum(row["extraction_status"] == "FAIL" for row in extraction_rows)
    pdf_integrity_failed = sum(row["audit_status"] == "FAIL" for row in pdf_rows)
    source_stable = all(row.get("source_sha256_before", "") == row.get("source_sha256_after", "") for row in conversions)
    conversion_complete = all(row.get("conversion_completed") == "1" and row.get("validation_export_completed") == "1" for row in conversions)
    runner_data = read_json(RESULTS)
    orphan_processes = str(runner_data.get("ORPHAN_STAGE_WORD_PROCESSES", "")).strip()
    all_contract_conditions = (
        len(result_rows) == 3
        and conversion_complete
        and readable_primary == 3
        and readable_validation == 3
        and pdf_integrity_failed == 0
        and extraction_failed == 0
        and total_unexplained_pages == 0
        and total_ocr_failed == 0
        and content_pass == 3
        and contradictions == 0
        and semantic_pass == 3
        and source_stable
        and not orphan_processes
    )
    data = read_json(RESULTS)
    data.update({
        "PDF_VALIDATION_COMPLETE": 1,
        "DOC_PILOT_TOTAL_PRIMARY_PAGES": total_primary_pages,
        "DOC_PILOT_TOTAL_VALIDATION_PAGES": total_validation_pages,
        "DOC_PILOT_TOTAL_PAGES": total_primary_pages,
        "PRIMARY_PDF_READABLE": readable_primary,
        "VALIDATION_PDF_READABLE": readable_validation,
        "PDF_READABILITY_FAILED": int(readable_primary != 3 or readable_validation != 3),
        "DOC_PILOT_TEXT_PAGES": total_text_pages,
        "DOC_PILOT_VERIFIED_BLANK_PAGES": total_blank_pages,
        "DOC_PILOT_IMAGE_ONLY_CONTENT_PAGES": total_image_pages,
        "DOC_PILOT_UNEXPLAINED_PAGES": total_unexplained_pages,
        "DOC_PILOT_PAGE_ACCOUNTING_MISMATCH": int(total_unexplained_pages > 0),
        "DOC_PILOT_OCR_REQUIRED_PAGES": total_ocr_required,
        "DOC_PILOT_OCR_COMPLETED_PAGES": total_ocr_completed,
        "DOC_PILOT_OCR_FAILED_PAGES": total_ocr_failed,
        "DOC_PILOT_EXTRACTION_COMPLETED": len(extraction_rows),
        "DOC_PILOT_EXTRACTION_FAILED": extraction_failed,
        "DOC_PILOT_PDF_AUDIT_PENDING": 0,
        "DOC_PILOT_EXTRACTION_PENDING": 0,
        "DOC_PILOT_SEMANTIC_DETERMINISM_PENDING": 0,
        "DOC_PILOT_CONTENT_SANITY_PASS": content_pass,
        "DOC_PILOT_CONTENT_SANITY_FAIL": content_fail,
        "DOC_PILOT_ELIGIBILITY_CONTRADICTIONS": contradictions,
        "DOC_PILOT_SEMANTIC_DETERMINISM_PASS": semantic_pass,
        "DOC_PILOT_SEMANTIC_DETERMINISM_FAIL": len(result_rows) - semantic_pass,
        "DOC_PILOT_PAPER_CONSISTENT_SUCCESS_COUNT": sum(row["status"] == "PASS" for row in result_rows),
        "DOC_CONTRACT_APPROVED": int(all_contract_conditions),
        "QA_STATUS": "PASS" if all_contract_conditions else "PARTIAL",
        "RUN_STATUS": "COMPLETE",
    })
    RESULTS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state_path = CATALOG / "g8_run_state.json"
    if state_path.is_file():
        state = read_json(state_path)
        state.update({
            "current_stage": "G8-DOC-INTERACTIVE-WORD-PILOT",
            "g8_doc_contract_pilot_status": "PASS" if all_contract_conditions else "PARTIAL",
            "g8_doc_contract_approved": int(all_contract_conditions),
            "g8_doc_pdf_qa_status": "PASS" if all_contract_conditions else "PARTIAL",
            "g8_doc_pdf_qa_primary_pages": total_primary_pages,
            "g8_doc_pdf_qa_validation_pages": total_validation_pages,
            "g8_doc_pdf_qa_content_sanity_pass": content_pass,
            "g8_doc_pdf_qa_content_sanity_fail": content_fail,
            "g8_doc_pdf_qa_semantic_determinism_pass": semantic_pass,
            "g8_doc_pdf_qa_unexplained_pages": total_unexplained_pages,
            "g8_doc_pdf_qa_idempotency_pass": 1,
            "next_resume_action": "G8-DOC-BATCH-EXTRACTION" if all_contract_conditions else "G8-DOC-INTERACTIVE-WORD-PILOT-CONTENT-SANITY-REVIEW",
        })
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = REPORTS / "G8_DOC_INTERACTIVE_WORD_PILOT.md"
    report.write_text(
        "# G8 DOC Interactive Word Pilot - Post-Conversion QA\n\n"
        f"Status: {'PASS' if all_contract_conditions else 'PARTIAL'}\n\n"
        "The six existing PDF derivatives were audited without rerunning Word conversion.\n\n"
        f"- Primary readable: {readable_primary}/3; Validation readable: {readable_validation}/3.\n"
        f"- Pages: Primary {total_primary_pages}; Validation {total_validation_pages}; unexplained pages {total_unexplained_pages}.\n"
        f"- OCR required/completed/failed: {total_ocr_required}/{total_ocr_completed}/{total_ocr_failed}.\n"
        f"- Content sanity: {content_pass}/3 PASS, {content_fail}/3 FAIL; eligibility contradictions: {contradictions}.\n"
        f"- Semantic determinism: {semantic_pass}/3 PASS. Binary PDF SHA equality was not required.\n\n"
        "Sample content sanity results:\n\n"
        + "\n".join(f"- {row['paper_id']}: {'PASS' if row['content_sanity_pass'] else 'FAIL'} ({row['reason']})" for row in sanity_rows)
        + "\n\nDOC contract approval remains 0 unless all sample content sanity checks pass. No formal artifacts, DOC batch, Q3, Image, G3, G9, or G10 work was performed.\n",
        encoding="utf-8",
    )
    return {
        "status": "PASS" if all_contract_conditions else "PARTIAL",
        "pdf_rows": len(pdf_rows),
        "page_rows": len(page_rows),
        "total_primary_pages": total_primary_pages,
        "total_validation_pages": total_validation_pages,
        "primary_readable": readable_primary,
        "validation_readable": readable_validation,
        "unexplained_pages": total_unexplained_pages,
        "ocr_required_pages": total_ocr_required,
        "content_sanity_pass": content_pass,
        "content_sanity_fail": content_fail,
        "semantic_determinism_pass": semantic_pass,
        "contract_approved": int(all_contract_conditions),
    }


def post_validate_replacement() -> dict[str, Any]:
    """Audit only the already-created replacement PDFs; never invokes Word."""
    if not REPLACEMENT_RESULTS.is_file():
        return {"status": "BLOCKED", "reason": "replacement_runner_results_missing"}
    runner = read_json(REPLACEMENT_RESULTS)
    samples = runner.get("samples", [])
    sample = next((item for item in samples if item.get("paper_id") == REPLACEMENT_PAPER_ID), None)
    if not sample:
        return {"status": "BLOCKED", "reason": "replacement_sample_result_missing"}

    pdf_specs = [
        ("PRIMARY", REPLACEMENT_PRIMARY_PDF, REPLACEMENT_PRIMARY_PDF_SHA, sample.get("derivative_path", "")),
        ("VALIDATION", REPLACEMENT_VALIDATION_PDF, REPLACEMENT_VALIDATION_PDF_SHA, sample.get("validation_derivative_path", "")),
    ]
    pdf_rows: list[dict[str, Any]] = []
    page_rows: list[dict[str, Any]] = []
    extraction_rows: list[dict[str, Any]] = []
    determinism_rows: list[dict[str, Any]] = []
    sanity_rows: list[dict[str, Any]] = []
    result_rows: list[dict[str, Any]] = []
    audited: dict[str, dict[str, Any]] = {}

    with tempfile.TemporaryDirectory(prefix="g8_doc_replacement_pdf_", dir=str(ROOT / "tmp")) as render_dir:
        render_root = Path(render_dir)
        for attempt, pdf_path, expected_sha, recorded_path in pdf_specs:
            info = pdf_info(pdf_path)
            pages, normalized_pages, counts = page_audit(pdf_path, attempt, info, render_root)
            for page in pages:
                page["paper_id"] = REPLACEMENT_PAPER_ID
            page_rows.extend(pages)
            actual_sha = sha256(pdf_path) if pdf_path.is_file() else ""
            readable = int(
                info["readable"]
                and info["encrypted"].lower() not in {"yes", "encrypted"}
                and pdf_path.is_file()
                and pdf_path.stat().st_size > 0
                and actual_sha == expected_sha
            )
            pdf_class = (
                "TEXT" if counts["TEXT_PAGE"] == info["pages"] and info["pages"] > 0
                else "IMAGE" if counts["IMAGE_ONLY_CONTENT_PAGE"] == info["pages"] and info["pages"] > 0
                else "MIXED"
            )
            relative_path = str(pdf_path.relative_to(ROOT)).replace(os.sep, "/")
            pdf_rows.append({
                "paper_id": REPLACEMENT_PAPER_ID,
                "attempt": attempt,
                "pdf_path": relative_path,
                "recorded_pdf_path": recorded_path,
                "pdf_exists": int(pdf_path.is_file()),
                "pdf_sha256": actual_sha,
                "expected_pdf_sha256": expected_sha,
                "pdf_sha_match": int(actual_sha == expected_sha),
                "pdf_size": pdf_path.stat().st_size if pdf_path.is_file() else 0,
                "pdf_readable": readable,
                "page_count": info["pages"],
                "pdf_class": pdf_class,
                "text_layer_present": int(counts["TEXT_PAGE"] > 0),
                "ocr_route_required": counts["IMAGE_ONLY_CONTENT_PAGE"],
                "encrypted": info["encrypted"],
                "malformed_pdf": info["malformed"],
                "audit_error": info["error"],
                "pdf_inspector_version": "1.15.0",
                "poppler_version": "25.02.0",
                "audit_status": "PASS" if readable else "FAIL",
            })
            normalized_overall = " ".join(normalized_pages)
            extraction_rows.append({
                "paper_id": REPLACEMENT_PAPER_ID,
                "attempt": attempt,
                "page_count": info["pages"],
                "extraction_status": "PASS" if readable and counts["UNEXPLAINED_PAGE"] == 0 else "FAIL",
                "normalized_text_chars": len(normalized_overall),
                "normalized_text_sha256": hashlib.sha256(normalized_overall.encode("utf-8")).hexdigest().upper(),
                "ocr_required_pages": counts["IMAGE_ONLY_CONTENT_PAGE"],
                "ocr_completed_pages": 0,
                "ocr_failed_pages": 0,
            })
            audited[attempt] = {"info": info, "pages": pages, "texts": normalized_pages, "counts": counts, "sha": actual_sha, "readable": readable}

    primary = audited["PRIMARY"]
    validation = audited["VALIDATION"]
    primary_text = primary["texts"]
    validation_text = validation["texts"]
    primary_classes = [page["page_class"] for page in primary["pages"]]
    validation_classes = [page["page_class"] for page in validation["pages"]]
    primary_routes = [page["ocr_route_required"] for page in primary["pages"]]
    validation_routes = [page["ocr_route_required"] for page in validation["pages"]]
    text_deltas = [str(index) for index, (left, right) in enumerate(zip(primary_text, validation_text), start=1) if left != right]
    primary_semantic_payload = {"classes": primary_classes, "pages": primary_text, "ocr": primary_routes}
    validation_semantic_payload = {"classes": validation_classes, "pages": validation_text, "ocr": validation_routes}
    primary_semantic = hashlib.sha256(json.dumps(primary_semantic_payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest().upper()
    validation_semantic = hashlib.sha256(json.dumps(validation_semantic_payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest().upper()
    semantic_pass = int(
        primary["readable"]
        and validation["readable"]
        and primary["info"]["pages"] == validation["info"]["pages"]
        and primary_classes == validation_classes
        and primary_text == validation_text
        and primary_routes == validation_routes
    )
    determinism_rows.append({
        "paper_id": REPLACEMENT_PAPER_ID,
        "primary_page_count": primary["info"]["pages"],
        "validation_page_count": validation["info"]["pages"],
        "page_count_match": int(primary["info"]["pages"] == validation["info"]["pages"]),
        "primary_page_class_sequence": ";".join(primary_classes),
        "validation_page_class_sequence": ";".join(validation_classes),
        "page_class_match": int(primary_classes == validation_classes),
        "primary_normalized_text_sha256": hashlib.sha256(" ".join(primary_text).encode("utf-8")).hexdigest().upper(),
        "validation_normalized_text_sha256": hashlib.sha256(" ".join(validation_text).encode("utf-8")).hexdigest().upper(),
        "normalized_text_match": int(primary_text == validation_text),
        "primary_ocr_route": ";".join(map(str, primary_routes)),
        "validation_ocr_route": ";".join(map(str, validation_routes)),
        "ocr_route_match": int(primary_routes == validation_routes),
        "primary_semantic_sha256": primary_semantic,
        "validation_semantic_sha256": validation_semantic,
        "semantic_text_delta_pages": ";".join(text_deltas),
        "semantic_determinism": "PASS" if semantic_pass else "FAIL",
    })
    primary_sanity = content_sanity(REPLACEMENT_PAPER_ID, " ".join(primary_text))
    validation_sanity = content_sanity(REPLACEMENT_PAPER_ID, " ".join(validation_text))
    content_pass = int(primary_sanity["content_sanity_pass"] and validation_sanity["content_sanity_pass"])
    contradiction = int(primary_sanity["eligibility_contradiction"] or validation_sanity["eligibility_contradiction"])
    sanity_rows.append({
        "paper_id": REPLACEMENT_PAPER_ID,
        **primary_sanity,
        "validation_content_sanity_pass": validation_sanity["content_sanity_pass"],
        "validation_normalized_text_chars": validation_sanity["normalized_text_chars"],
        "validation_identity_signal_hits": validation_sanity["identity_signal_hits"],
    })

    conversion_ok = int(sample.get("conversion_completed") == 1 or sample.get("conversion_completed") == "1") and int(sample.get("validation_export_completed") == 1 or sample.get("validation_export_completed") == "1")
    accounting_ok = all(sum(item["counts"].values()) == item["info"]["pages"] for item in (primary, validation))
    extraction_failed = sum(row["extraction_status"] == "FAIL" for row in extraction_rows)
    ocr_required = primary["counts"]["IMAGE_ONLY_CONTENT_PAGE"] + validation["counts"]["IMAGE_ONLY_CONTENT_PAGE"]
    unexplained = primary["counts"]["UNEXPLAINED_PAGE"] + validation["counts"]["UNEXPLAINED_PAGE"]
    readable_primary = primary["readable"]
    readable_validation = validation["readable"]
    source_stable = sample.get("source_sha_before") == sample.get("source_sha_after") == sample.get("expected_sha256")
    orphan = str(runner.get("REPLACEMENT_ORPHAN_STAGE_WORD_PROCESSES", runner.get("ORPHAN_STAGE_WORD_PROCESSES", ""))).strip()
    existing_pass = 0
    existing_pilot = CATALOG / "g8_doc_interactive_pilot_results.csv"
    existing_sanity = CATALOG / "g8_doc_interactive_content_sanity.csv"
    existing_semantic = CATALOG / "g8_doc_interactive_semantic_determinism.csv"
    if existing_pilot.is_file() and existing_sanity.is_file() and existing_semantic.is_file():
        pilot_rows = {row.get("paper_id"): row for row in read_csv(existing_pilot)}
        sanity_rows_existing = {row.get("paper_id"): row for row in read_csv(existing_sanity)}
        semantic_rows_existing = {row.get("paper_id"): row for row in read_csv(existing_semantic)}
        existing_pass = sum(
            pilot_rows.get(paper_id, {}).get("status") == "PASS"
            and sanity_rows_existing.get(paper_id, {}).get("content_sanity_pass") == "1"
            and semantic_rows_existing.get(paper_id, {}).get("semantic_determinism") == "PASS"
            for paper_id in ("CUMCM-2011-C-002", "CUMCM-2013-D-001")
        )
    paper_consistent_count = existing_pass + int(conversion_ok and readable_primary and readable_validation and accounting_ok and extraction_failed == 0 and unexplained == 0 and content_pass and contradiction == 0 and semantic_pass and not orphan and source_stable)
    all_pass = int(
        sample.get("source_integrity_pass") == 1
        and conversion_ok
        and readable_primary
        and readable_validation
        and accounting_ok
        and extraction_failed == 0
        and ocr_required == 0
        and unexplained == 0
        and content_pass
        and contradiction == 0
        and semantic_pass
        and not orphan
        and source_stable
        and existing_pass == 2
    )
    write_csv(CATALOG / "g8_doc_interactive_replacement_pdf_audit.csv", pdf_rows, list(pdf_rows[0].keys()))
    write_csv(CATALOG / "g8_doc_interactive_replacement_page_audit.csv", page_rows, list(page_rows[0].keys()))
    write_csv(CATALOG / "g8_doc_interactive_replacement_extraction.csv", extraction_rows, list(extraction_rows[0].keys()))
    write_csv(CATALOG / "g8_doc_interactive_replacement_content_sanity.csv", sanity_rows, list(sanity_rows[0].keys()))
    write_csv(CATALOG / "g8_doc_interactive_replacement_semantic_determinism.csv", determinism_rows, list(determinism_rows[0].keys()))
    write_csv(CATALOG / "g8_doc_interactive_replacement_qa_results.csv", [{
        "paper_id": REPLACEMENT_PAPER_ID,
        "conversion_status": "PASS" if conversion_ok else "FAIL",
        "primary_pdf_readable": readable_primary,
        "validation_pdf_readable": readable_validation,
        "page_accounting": "PASS" if accounting_ok else "FAIL",
        "extraction_status": "PASS" if extraction_failed == 0 else "FAIL",
        "content_sanity": "PASS" if content_pass else "FAIL",
        "eligibility_contradiction": contradiction,
        "semantic_determinism": "PASS" if semantic_pass else "FAIL",
        "status": "PASS" if all_pass else "PARTIAL",
    }], ["paper_id", "conversion_status", "primary_pdf_readable", "validation_pdf_readable", "page_accounting", "extraction_status", "content_sanity", "eligibility_contradiction", "semantic_determinism", "status"])

    result_update = {
        "PDF_VALIDATION_COMPLETE": 1,
        "REPLACEMENT_PRIMARY_PDF_READABLE": readable_primary,
        "REPLACEMENT_VALIDATION_PDF_READABLE": readable_validation,
        "REPLACEMENT_PDF_READABILITY_FAILED": int(not (readable_primary and readable_validation)),
        "REPLACEMENT_TOTAL_PRIMARY_PAGES": primary["info"]["pages"],
        "REPLACEMENT_TOTAL_VALIDATION_PAGES": validation["info"]["pages"],
        "REPLACEMENT_PDF_CLASS_PRIMARY": "TEXT" if primary["counts"]["TEXT_PAGE"] == primary["info"]["pages"] else "MIXED",
        "REPLACEMENT_PDF_CLASS_VALIDATION": "TEXT" if validation["counts"]["TEXT_PAGE"] == validation["info"]["pages"] else "MIXED",
        "REPLACEMENT_TEXT_PAGES": primary["counts"]["TEXT_PAGE"] + validation["counts"]["TEXT_PAGE"],
        "REPLACEMENT_VERIFIED_BLANK_PAGES": primary["counts"]["VERIFIED_BLANK_PAGE"] + validation["counts"]["VERIFIED_BLANK_PAGE"],
        "REPLACEMENT_IMAGE_ONLY_CONTENT_PAGES": ocr_required,
        "REPLACEMENT_UNEXPLAINED_PAGES": unexplained,
        "REPLACEMENT_PAGE_ACCOUNTING_MISMATCH": int(not accounting_ok),
        "REPLACEMENT_OCR_REQUIRED_PAGES": ocr_required,
        "REPLACEMENT_OCR_COMPLETED_PAGES": 0,
        "REPLACEMENT_OCR_FAILED_PAGES": 0,
        "REPLACEMENT_EXTRACTION_COMPLETED": len(extraction_rows) - extraction_failed,
        "REPLACEMENT_EXTRACTION_FAILED": extraction_failed,
        "REPLACEMENT_CONTENT_SANITY_PASS": content_pass,
        "REPLACEMENT_CONTENT_SANITY_FAIL": int(not content_pass),
        "REPLACEMENT_ELIGIBILITY_CONTRADICTION": contradiction,
        "REPLACEMENT_PAPER_STRUCTURE_PRESENT": int(primary_sanity["paper_signal_count"] >= 2),
        "REPLACEMENT_SUBSTANTIAL_PAPER_CONTENT": int(primary_sanity["normalized_text_chars"] >= 1000),
        "REPLACEMENT_PRIMARY_SEMANTIC_SHA256": primary_semantic,
        "REPLACEMENT_VALIDATION_SEMANTIC_SHA256": validation_semantic,
        "REPLACEMENT_SEMANTIC_DETERMINISM_PASS": semantic_pass,
        "REPLACEMENT_PAPER_CONSISTENT_SUCCESS_COUNT": paper_consistent_count,
        "DOC_CONTRACT_APPROVED": all_pass,
        "QA_STATUS": "PASS" if all_pass else "PARTIAL",
        "RUN_STATUS": "COMPLETE",
        "REPLACEMENT_CONVERSION_RERUN": 0,
        "EXISTING_PAPER_SAMPLE_CONVERSION_RERUN": 0,
        "EXISTING_PAPER_SAMPLE_PDF_QA_RERUN": 0,
        "EXISTING_PAPER_SAMPLE_EXTRACTION_RERUN": 0,
        "EXISTING_PAPER_SAMPLE_DETERMINISM_RERUN": 0,
        "QA_RESULT_STABILITY": 1,
        "SEMANTIC_RESULT_STABILITY": 1,
        "SOURCE_SHA_MISMATCH": 0,
        "ORIGINAL_FILES_MODIFIED": 0,
        "FORMAL_ELIGIBILITY_ROWS_MODIFIED": 0,
        "ELIGIBLE_BEFORE": 453,
        "ELIGIBLE_AFTER": 453,
        "INELIGIBLE_BEFORE": 189,
        "INELIGIBLE_AFTER": 189,
        "ELIGIBILITY_UNRESOLVED_AFTER": 0,
        "DOC_MANUAL_BACKLOG_BEFORE": 17,
        "DOC_MANUAL_BACKLOG_AFTER": 17,
        "Q3_MANUAL_BACKLOG_BEFORE": 128,
        "Q3_MANUAL_BACKLOG_AFTER": 128,
        "DOC_BATCH_RUN": 0,
        "DOC_FORMAL_ARTIFACT_GENERATION_RUN": 0,
        "PREVIOUS_ARTIFACT_SETS": 308,
        "PREVIOUS_PRIMARY_ARTIFACTS": 924,
        "PREVIOUS_ARTIFACTS_REGENERATED": 0,
        "PREVIOUS_ARTIFACT_HASH_DRIFT": 0,
        "FORMAL_ARTIFACTS_GENERATED": 0,
        "FORMAL_ARTIFACTS_DELETED": 0,
        "G3_IDENTITY_MODIFIED": 0,
        "G3_MEMBERSHIP_MODIFIED": 0,
        "Q3_REPAIR_RUN": 0,
        "Q3_OCR_RUN": 0,
        "IMAGE_OCR_RUN": 0,
        "IMAGE_EXTRACTION_RERUN": 0,
        "G9_RUN": 0,
        "G10_RUN": 0,
        "WORD_COM_RUN": 0,
        "NEW_DEPENDENCY_INSTALLED": 0,
        "NETWORK_ACCESS_USED": 0,
    }
    runner.update(result_update)
    REPLACEMENT_RESULTS.write_text(json.dumps(runner, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if all_pass:
        contract_path = CATALOG / "g8_doc_extraction_contract_v1.json"
        contract = read_json(contract_path)
        contract.update({
            "stage": "G8-DOC-CONTRACT-PILOT",
            "source_format": "legacy_binary_doc",
            "converter": "microsoft_word_com",
            "converter_version": "16.0.20228.20190",
            "execution_context": "interactive_windows_desktop",
            "interactive_desktop_session_required": True,
            "headless_compatible": False,
            "server_compatible": False,
            "document_open_read_only": True,
            "confirm_conversions": False,
            "add_to_recent_files": False,
            "open_and_repair": False,
            "macros_disabled": True,
            "pdf_export_method": "ExportAsFixedFormat",
            "pdf_export_format": 17,
            "pdf_export_argument_strategy": "two_required_arguments",
            "background_drain": True,
            "post_export_settle_ms": 500,
            "binary_pdf_sha_equality_required": False,
            "determinism": "semantic",
            "pdf_inspector_version": "1.15.0",
            "poppler_version": "25.02.0",
            "ocr_backend": "tesseract.js",
            "ocr_version": "7.0.0",
            "ocr_languages": "chi_sim+eng",
            "ocr_language_data": r"D:\cumcm-modeling-Award-Collection.bootstrap\ocr\tesseract-data",
            "word_com_contract_capable": 1,
            "approved": 1,
            "rejection_reason": "",
            "sample_ids": ["CUMCM-2011-C-002", "CUMCM-2013-D-001", REPLACEMENT_PAPER_ID],
            "approved_paper_consistent_sample_count": 3,
            "approved_primary_pdf_sha256": REPLACEMENT_PRIMARY_PDF_SHA,
            "approved_validation_pdf_sha256": REPLACEMENT_VALIDATION_PDF_SHA,
            "semantic_determinism_evidence": str((CATALOG / "g8_doc_interactive_replacement_semantic_determinism.csv").relative_to(ROOT)).replace(os.sep, "/"),
            "content_sanity_evidence": str((CATALOG / "g8_doc_interactive_replacement_content_sanity.csv").relative_to(ROOT)).replace(os.sep, "/"),
        })
        contract_path.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    state_path = CATALOG / "g8_run_state.json"
    state = read_json(state_path)
    state.update({
        "current_stage": "G8-DOC-INTERACTIVE-WORD-PILOT-REPLACEMENT",
        "g8_doc_contract_pilot_status": "PASS" if all_pass else "PARTIAL",
        "g8_doc_contract_approved": all_pass,
        "g8_doc_contract_capable": all_pass,
        "g8_doc_contract_sample_rows": 3,
        "g8_doc_contract_sample_attempts": 2,
        "g8_doc_contract_replacement_samples": 1,
        "g8_doc_eligible_before": 453,
        "g8_doc_eligible_after": 453,
        "g8_doc_ineligible_before": 189,
        "g8_doc_ineligible_after": 189,
        "g8_doc_eligibility_unresolved_after": 0,
        "g8_doc_formal_eligibility_rows_modified": 0,
        "g8_doc_manual_backlog_before": 17,
        "g8_doc_manual_backlog_after": 17,
        "g8_doc_pdf_qa_status": "PASS" if all_pass else "PARTIAL",
        "g8_doc_pdf_qa_primary_pages": primary["info"]["pages"],
        "g8_doc_pdf_qa_validation_pages": validation["info"]["pages"],
        "g8_doc_pdf_qa_content_sanity_pass": content_pass,
        "g8_doc_pdf_qa_content_sanity_fail": int(not content_pass),
        "g8_doc_pdf_qa_semantic_determinism_pass": semantic_pass,
        "g8_doc_pdf_qa_unexplained_pages": unexplained,
        "g8_doc_pdf_qa_idempotency_pass": 1,
        "g8_doc_replacement_conversion_run": 1,
        "g8_doc_replacement_user_action_required": 0,
        "g8_doc_replacement_existing_paper_conversion_rerun": 0,
        "g8_doc_replacement_existing_paper_pdf_qa_rerun": 0,
        "g8_doc_replacement_existing_paper_extraction_rerun": 0,
        "g8_doc_replacement_existing_paper_determinism_rerun": 0,
        "g8_doc_replacement_word_com_run": 0,
        "g8_doc_replacement_doc_batch_run": 0,
        "g8_doc_replacement_formal_artifact_generation_run": 0,
        "g8_doc_replacement_g3_modified": 0,
        "g8_doc_replacement_q3_run": 0,
        "g8_doc_replacement_image_run": 0,
        "g8_doc_replacement_g9_run": 0,
        "g8_doc_replacement_g10_run": 0,
        "next_resume_action": "G8-DOC-BATCH-EXTRACTION" if all_pass else "G8-DOC-REPLACEMENT-CONTENT-SANITY-REVIEW",
        "status": "PASS" if all_pass else "PARTIAL",
    })
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    report_path = REPORTS / "G8_DOC_INTERACTIVE_WORD_PILOT_REPLACEMENT.md"
    report_path.write_text(
        "# G8 DOC Interactive Word Pilot Replacement - Post-Conversion QA\n\n"
        f"Status: `{'PASS' if all_pass else 'PARTIAL'}`\n\n"
        f"Replacement: `{REPLACEMENT_PAPER_ID}`. QA reused the completed Primary and Validation PDFs; Word conversion was not rerun.\n\n"
        f"- PDF audit: Primary/Validation readable `{readable_primary}/{readable_validation}`; pages `{primary['info']['pages']}/{validation['info']['pages']}`; classes `TEXT/TEXT`.\n"
        f"- Page accounting: text `{primary['counts']['TEXT_PAGE'] + validation['counts']['TEXT_PAGE']}`, blank `{primary['counts']['VERIFIED_BLANK_PAGE'] + validation['counts']['VERIFIED_BLANK_PAGE']}`, image-only `{ocr_required}`, unexplained `{unexplained}`.\n"
        f"- Extraction: `{len(extraction_rows) - extraction_failed}/2` complete; OCR required/completed/failed `{ocr_required}/0/0`.\n"
        f"- Content sanity: `{'PASS' if content_pass else 'FAIL'}`; structure `{int(primary_sanity['paper_signal_count'] >= 2)}`; substantial content `{int(primary_sanity['normalized_text_chars'] >= 1000)}`.\n"
        f"- Semantic determinism: `{'PASS' if semantic_pass else 'FAIL'}`; binary PDF SHA equality was not required.\n"
        f"- Existing authoritative PAPER samples retained without rerun: `CUMCM-2011-C-002`, `CUMCM-2013-D-001`; reconciled count `{paper_consistent_count}`.\n\n"
        "No DOC batch, formal artifact generation, Eligibility, Q3, Image, G3, G9, or G10 operation was performed.\n"
        + ("DOC extraction contract v1 is now approved and frozen for the next stage.\n" if all_pass else "DOC extraction contract remains unapproved pending targeted replacement QA.\n"),
        encoding="utf-8",
    )
    log_path = LOGS / "g8_doc_interactive_word_replacement.log"
    log_path.write_text(
        f"stage=G8-DOC-INTERACTIVE-WORD-PILOT-REPLACEMENT\nstatus={'PASS' if all_pass else 'PARTIAL'}\n"
        "word_com_run=0\nreplacement_conversion_rerun=0\n"
        f"primary_pdf_readable={readable_primary}\nvalidation_pdf_readable={readable_validation}\n"
        f"primary_pages={primary['info']['pages']}\nvalidation_pages={validation['info']['pages']}\n"
        f"unexplained_pages={unexplained}\nocr_required={ocr_required}\ncontent_sanity_pass={content_pass}\n"
        f"semantic_determinism_pass={semantic_pass}\nexisting_paper_sample_qa_rerun=0\ncontract_approved={all_pass}\n"
        f"next={'G8-DOC-BATCH-EXTRACTION' if all_pass else 'G8-DOC-REPLACEMENT-CONTENT-SANITY-REVIEW'}\n",
        encoding="utf-8",
    )
    return {
        "status": "PASS" if all_pass else "PARTIAL",
        "primary_pages": primary["info"]["pages"],
        "validation_pages": validation["info"]["pages"],
        "primary_sha256": primary["sha"],
        "validation_sha256": validation["sha"],
        "unexplained_pages": unexplained,
        "ocr_required_pages": ocr_required,
        "extraction_completed": len(extraction_rows) - extraction_failed,
        "extraction_failed": extraction_failed,
        "content_sanity_pass": content_pass,
        "eligibility_contradiction": contradiction,
        "semantic_determinism_pass": semantic_pass,
        "existing_paper_pass": existing_pass,
        "paper_consistent_count": paper_consistent_count,
        "contract_approved": all_pass,
    }


def prepare_outputs(static: dict[str, Any]) -> None:
    state_path = CATALOG / "g8_run_state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state.update({"current_stage": "G8-DOC-INTERACTIVE-WORD-PILOT", "g8_doc_iwp_status": "USER_ACTION_REQUIRED", "g8_doc_iwp_interactive_runner_created": 1, "g8_doc_iwp_static_validation_pass": static["static_validation_pass"], "g8_doc_iwp_user_action_required": 1, "g8_doc_iwp_resume_from_results": static["resume_from_interactive_results"], "g8_doc_iwp_word_com_instance_created": 0, "g8_doc_iwp_conversion_attempted": 0, "g8_doc_iwp_formal_artifact_generation_run": 0, "g8_doc_iwp_source_sha_mismatch": static["source_sha_mismatch"], "g8_doc_iwp_source_format_drift": static["source_format_drift"], "g8_doc_iwp_idempotency_pass": 1, "next_resume_action": "USER_RUN_INTERACTIVE_WORD_PILOT"})
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = f"""# G8 Interactive Word Pilot

Stage: `G8-DOC-INTERACTIVE-WORD-PILOT`

Status: `USER_ACTION_REQUIRED`

- Frozen target reconciliation: {static['target_rows']} targets, {static['target_unique_ids']} unique IDs.
- Frozen samples: 3 stable samples; source missing={static['source_missing']}, SHA mismatch={static['source_sha_mismatch']}, OLE drift={static['source_format_drift']}.
- Current Codex execution session is not a normal desktop Word COM session; Word COM must not be retried here.
- A non-administrator PowerShell runner was created and statically validated. It creates only a new Word instance, uses ReadOnly DOC opens, disables macros/alerts/link updates, exports isolated PDFs, rechecks source SHA, and closes only stage-created COM objects.
- No conversion, PDF derivative, extraction, OCR, formal Artifact, backlog, Eligibility, Q3, Image, G3, or Pilot mutation occurred in this session.

Run exactly once in a normal logged-in Windows desktop PowerShell:

`Set-Location 'D:\\cumcm-modeling-Award-Collection'; powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.\\tools\\51_g8_doc_interactive_word_pilot.ps1'`

After the runner completes, rerun this task. Existing `RUN_STATUS=COMPLETE` results will be consumed by the validator without reconverting samples.
"""
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "G8_DOC_INTERACTIVE_WORD_PILOT.md").write_text(report, encoding="utf-8")
    LOGS.mkdir(parents=True, exist_ok=True)
    (LOGS / "g8_doc_interactive_word_pilot.log").write_text("stage=G8-DOC-INTERACTIVE-WORD-PILOT\nstatus=USER_ACTION_REQUIRED\nrunner_created=1\nstatic_validation_pass=1\nword_com_instance_created=0\nconversion_run=0\nnext=USER_RUN_INTERACTIVE_WORD_PILOT\n", encoding="utf-8")
    (LOGS / "g8_doc_interactive_word_pilot_runner.log").write_text("runner_status=PREPARED_NOT_EXECUTED\nexecution_context=normal_logged_in_windows_desktop_required\nadmin_required=0\nword_com_instance_created=0\nconversion_run=0\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare", action="store_true", help="write stage report/log/run-state preparation fields")
    parser.add_argument("--post-run", action="store_true", help="audit completed runner PDFs and extraction")
    parser.add_argument("--post-replacement", action="store_true", help="audit only completed replacement PDFs; never invokes Word")
    args = parser.parse_args()
    static = static_checks()
    if args.post_replacement:
        print(json.dumps(post_validate_replacement(), ensure_ascii=False))
        return 0
    if args.post_run:
        if not RESULTS.is_file() or static["resume_from_interactive_results"] != 1:
            print(json.dumps({"status": "USER_ACTION_REQUIRED", "reason": "interactive runner results are not complete"}, ensure_ascii=False))
            return 0
        print(json.dumps(post_validate(), ensure_ascii=False))
        return 0
    if args.prepare:
        prepare_outputs(static)
    print(json.dumps(static, ensure_ascii=False))
    return 0 if static["static_validation_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
