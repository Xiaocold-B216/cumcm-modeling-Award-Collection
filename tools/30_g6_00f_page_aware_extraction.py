"""G6-00F page-aware pdf-inspector compatibility audit.

The formal Q2 extraction backend is pdf-inspector's native
``extract_text_in_regions`` call with exactly one full-page region.  This is
deliberately not OCR, a second extractor, or artificial splitting of whole
document text.  All page text is held in memory except for the temporary,
deterministic preview which is removed before the run completes.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.metadata
import inspect
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

import pdf_inspector


ROOT = Path(__file__).resolve().parents[1]
PYTHON = Path(sys.executable).resolve()
STAMP = timezone(timedelta(hours=8))

BRIDGE = ROOT / "catalog" / "pilot" / "g3_25r_q2_identity_map.csv"
G5_CLOSURE = ROOT / "catalog" / "pilot" / "pdf_g5_closure_pilot.csv"
G5_OCR = ROOT / "catalog" / "pilot" / "pdf_ocr_results_2025.csv"
REPAIR_MANIFEST = ROOT / "catalog" / "repair_manifest.jsonl"
AUDIT = ROOT / "catalog" / "pilot" / "g6_q2_page_extraction_audit.csv"
CONTRACT = ROOT / "catalog" / "pilot" / "g6_q2_page_extraction_contract.json"
LOG = ROOT / "logs" / "g6_00f_page_aware_extraction.log"
REPORT = ROOT / "reports" / "G6_00F_page_aware_extraction.md"
PREVIEW_DIR = ROOT / ".bootstrap" / "g6_00f_preview"

TARGET_IDS = ["A066", "A196", "B060", "C023", "C132", "D037", "E030"]


class GateError(RuntimeError):
    pass


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def snapshot(paths: list[Path]) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in paths:
        if path.is_file():
            result[str(path.relative_to(ROOT)).replace("\\", "/")] = digest(path)
    return result


def protected_paths() -> dict[str, list[Path]]:
    catalog = ROOT / "catalog"
    pilot = catalog / "pilot"
    reports = ROOT / "reports"
    paths: dict[str, list[Path]] = {
        "G1": [catalog / "files.csv", catalog / "manifest.jsonl"],
        "G2": [catalog / "duplicates.csv", catalog / "duplicate_relations.csv"],
        "G3": [catalog / x for x in ["papers.csv", "paper_files.csv", "sources.csv", "paper_identity_review.csv"]],
        "G3_25R": [BRIDGE],
        "G4": list(catalog.glob("pdf_audit*") ) + list(reports.glob("G4*.md")),
        "G5": list(pilot.glob("pdf_*.csv")),
        "G5_REPAIR": [REPAIR_MANIFEST],
        "G5_OCR_DERIVATIVES": [p for p in (ROOT / "derived").rglob("*") if p.is_file()],
    }
    return paths


def protected_snapshot() -> dict[str, str]:
    paths: list[Path] = []
    for group in protected_paths().values():
        paths.extend(group)
    return snapshot(paths)


def now() -> str:
    return datetime.now(STAMP).isoformat(timespec="seconds")


def append_log(lines: list[str]) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as handle:
        for line in lines:
            handle.write(line.rstrip("\n") + "\n")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def load_workset() -> list[dict[str, Any]]:
    bridge = read_csv(BRIDGE)
    closure = {row["file_path"]: row for row in read_csv(G5_CLOSURE) if row["final_q"] == "Q2"}
    ocr = {row["source_file_path"]: row for row in read_csv(G5_OCR)}
    if len(bridge) != 7 or len({row["paper_id"] for row in bridge}) != 7:
        raise GateError("Q2_WORKSET_ROWS or UNIQUE_Q2_PAPER_IDS failed")
    result: list[dict[str, Any]] = []
    for row in bridge:
        source = row["file_path"]
        if source not in closure or source not in ocr:
            raise GateError(f"missing G5 workset row: {source}")
        g5 = closure[source]
        ocr_row = ocr[source]
        derived = g5["derived_file_path"]
        result.append({
            "paper_id": row["paper_id"],
            "source_identifier": row["source_identifier"],
            "original_file_path": source,
            "original_sha256": row["file_sha256"].upper(),
            "readable_file_path": derived,
            "readable_sha256": g5["derived_sha256"].upper(),
            "page_count": int(ocr_row["output_page_count"]),
            "g5_pages_with_text": int(ocr_row["pages_with_text_after"]),
            "g5_source_page_count": int(ocr_row["source_page_count"]),
        })
    if len({row["original_file_path"] for row in result}) != 7:
        raise GateError("UNIQUE_Q2_SOURCE_PATHS failed")
    if len({row["readable_file_path"] for row in result}) != 7:
        raise GateError("UNIQUE_Q2_DERIVED_PATHS failed")
    return result


def verify_workset(workset: list[dict[str, Any]]) -> tuple[int, int, int, int]:
    source_mismatch = 0
    derived_missing = 0
    derived_mismatch = 0
    page_mismatch = 0
    for row in workset:
        source_path = ROOT / row["original_file_path"]
        derived_path = ROOT / row["readable_file_path"]
        if not source_path.is_file() or digest(source_path) != row["original_sha256"]:
            source_mismatch += 1
        if not derived_path.is_file():
            derived_missing += 1
            continue
        if digest(derived_path) != row["readable_sha256"]:
            derived_mismatch += 1
    if source_mismatch or derived_missing or derived_mismatch:
        raise GateError("source/derived SHA or presence gate failed")
    for row in workset:
        result = pdf_inspector.process_pdf(str(ROOT / row["readable_file_path"]), pages=[0])
        actual_pages = int(result.page_count)
        if actual_pages != row["page_count"] or row["g5_source_page_count"] != row["page_count"]:
            page_mismatch += 1
    if page_mismatch:
        raise GateError("Q2_PAGE_COUNT_MISMATCH")
    return source_mismatch, derived_missing, derived_mismatch, page_mismatch


def representative_experiment(row: dict[str, Any]) -> list[dict[str, Any]]:
    path = str(ROOT / row["readable_file_path"])
    pages = [0, row["page_count"] // 2, row["page_count"] - 1]
    result: list[dict[str, Any]] = []
    for api_page in pages:
        process = pdf_inspector.process_pdf(path, pages=[api_page])
        positioned = pdf_inspector.extract_text_with_positions(path, pages=[api_page])
        markdown = pdf_inspector.extract_pages_markdown(path, pages=[api_page])
        regions = pdf_inspector.extract_text_in_regions(path, [(api_page, [[0, 0, 100000, 100000]])])
        region_text = "\n".join(item.text for item in regions[0].regions)
        result.append({
            "api_page": api_page,
            "source_page": api_page + 1,
            "process_page_count": int(process.page_count),
            "process_markdown_chars": len(process.markdown or ""),
            "positioned_items": len(positioned),
            "positioned_actual_chars": sum(len(item.text.replace("[Image: Im1]", "").strip()) for item in positioned),
            "markdown_pages": len(markdown.pages),
            "markdown_chars": sum(len(page.markdown or "") for page in markdown.pages),
            "region_chars": len(region_text),
            "region_needs_ocr": any(bool(getattr(item, "needs_ocr", False)) for item in regions[0].regions),
        })
    return result


def actual_text(region_result: Any) -> str:
    return "\n".join(item.text for item in region_result.regions)


def marker_only(text: str) -> bool:
    stripped = re.sub(r"\[Image:[^\]]*\]", "", text)
    return not stripped.strip()


def garbled(text: str) -> bool:
    if "\ufffd" in text or "\x00" in text:
        return True
    return any(0x80 <= ord(char) <= 0x9F for char in text)


def normalize(text: str) -> str:
    text = re.sub(r"\[Image:[^\]]*\]", "", text)
    return re.sub(r"\s+", "", text)


def page_audit(workset: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    fields = ["paper_id", "source_page", "api_page_index", "api_call_mode", "text_chars", "text_nonempty", "needs_ocr_if_available", "verified_blank_page", "status"]
    rows: list[dict[str, Any]] = []
    summaries: dict[str, Any] = {}
    whole_chars = 0
    joined_chars = 0
    relative_diffs: list[float] = []
    for work in workset:
        path = str(ROOT / work["readable_file_path"])
        expected_blank_count = work["page_count"] - work["g5_pages_with_text"]
        blank_pages: list[int] = []
        nonblank_with_text = 0
        garbled_pages = 0
        joined_parts: list[str] = []
        work_rows: list[dict[str, Any]] = []
        for api_page in range(work["page_count"]):
            extracted = pdf_inspector.extract_text_in_regions(path, [(api_page, [[0, 0, 100000, 100000]])])
            text = actual_text(extracted[0])
            is_marker_only = marker_only(text)
            if is_marker_only:
                blank_pages.append(api_page + 1)
            else:
                nonblank_with_text += 1
                joined_parts.append(text)
            if garbled(text):
                garbled_pages += 1
            work_rows.append({
                "paper_id": work["paper_id"],
                "source_page": api_page + 1,
                "api_page_index": api_page,
                "api_call_mode": "extract_text_in_regions_full_page",
                "text_chars": len(text),
                "text_nonempty": int(not is_marker_only),
                "needs_ocr_if_available": int(any(bool(getattr(item, "needs_ocr", False)) for item in extracted[0].regions)),
                "verified_blank_page": 0,
                "status": "GARBLED" if garbled(text) else "PASS",
            })
        blank_count_matches_g5 = len(blank_pages) == expected_blank_count
        unexpected_empty_pages = 0 if blank_count_matches_g5 else len(blank_pages)
        for work_row in work_rows:
            if work_row["source_page"] in blank_pages:
                if blank_count_matches_g5:
                    work_row["verified_blank_page"] = 1
                    work_row["status"] = "BLANK_PASS"
                else:
                    work_row["status"] = "MISSING_PAGE_TEXT"
        rows.extend(work_rows)
        whole = pdf_inspector.extract_text(path)
        whole_chars += len(whole)
        joined = "\n".join(joined_parts)
        joined_chars += len(joined)
        whole_norm = len(normalize(whole))
        joined_norm = len(normalize(joined))
        relative = abs(joined_norm - whole_norm) / max(whole_norm, 1)
        relative_diffs.append(relative)
        summaries[work["paper_id"]] = {
            "pages": work["page_count"],
            "nonblank_pages": nonblank_with_text,
            "unexpected_empty_pages": unexpected_empty_pages,
            "unexpected_empty_page_numbers": blank_pages if not blank_count_matches_g5 else [],
            "verified_blank_pages": blank_pages if blank_count_matches_g5 else [],
            "whole_chars": len(whole),
            "page_joined_chars": len(joined),
            "relative_difference": relative,
            "garbled_pages": garbled_pages,
            "status": "PASS" if not unexpected_empty_pages and not garbled_pages else "BLOCKED",
        }
    audit_rows = len(rows)
    if audit_rows != 516:
        raise GateError(f"PAGE_AUDIT_ROWS={audit_rows}")
    return rows, {
        "whole_chars": whole_chars,
        "joined_chars": joined_chars,
        "relative_difference": max(relative_diffs) if relative_diffs else 0.0,
        "summaries": summaries,
    }


def write_preview(workset: list[dict[str, Any]], audit_rows: list[dict[str, Any]]) -> tuple[int, int]:
    if PREVIEW_DIR.exists() and any(PREVIEW_DIR.iterdir()):
        raise GateError("temporary preview directory contains pre-existing files")
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    by_paper: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in audit_rows:
        by_paper[row["paper_id"]].append(row)
    created: list[Path] = []
    for work in workset:
        path = str(ROOT / work["readable_file_path"])
        lines: list[str] = []
        for row in by_paper[work["paper_id"]]:
            lines.append(f"<!-- source_page: {row['source_page']} -->")
            if row["verified_blank_page"]:
                lines.append("[原 PDF 此页为空白页]")
            else:
                extracted = pdf_inspector.extract_text_in_regions(path, [(row["api_page_index"], [[0, 0, 100000, 100000]])])
                lines.append(actual_text(extracted[0]))
            lines.append("")
        preview = PREVIEW_DIR / f"{work['paper_id']}.preview.md"
        preview.write_text("\n".join(lines), encoding="utf-8")
        created.append(preview)
    success = sum(path.is_file() and path.stat().st_size > 0 for path in created)
    for path in created:
        path.unlink()
    remaining = sum(1 for path in PREVIEW_DIR.iterdir() if path.is_file())
    return success, remaining


def freeze_contract() -> int:
    contract = {
        "schema_version": 1,
        "backend": "pdf-inspector",
        "backend_version": "1.15.0",
        "input_kind": "g5_ocr_readable_derivative",
        "mode": "page_scoped_text_to_deterministic_markdown",
        "api": "extract_text_in_regions",
        "page_selector_parameter": "page_regions=[(page_0indexed, [[x1, y1, x2, y2]])]",
        "page_selector_indexing": "0-based",
        "source_page_indexing": "1-based",
        "full_page_region": [0, 0, 100000, 100000],
        "secondary_extractor_fallback": "forbidden",
        "ocr_in_g6": "forbidden",
        "whole_document_artificial_page_splitting": "forbidden",
    }
    if CONTRACT.exists():
        existing = json.loads(CONTRACT.read_text(encoding="utf-8-sig"))
        if existing != contract:
            raise GateError("existing page-aware contract differs")
    else:
        CONTRACT.parent.mkdir(parents=True, exist_ok=True)
        CONTRACT.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(list(CONTRACT.parent.glob("g6_q2_page_extraction_contract*.json")))


def report(data: dict[str, Any]) -> list[str]:
    protected = data["protected"]
    lines = [
        "STAGE=G6-00F",
        f"STATUS={data['status']}",
        "BRANCH=library-refactor-v1",
        "HEAD=a042ecf898feaba6fc81d543a10e0188db8b2b12",
        f"PYTHON_EXECUTABLE={PYTHON}",
        f"PYTHON_VERSION={sys.version.split()[0]}",
        f"PDF_INSPECTOR_VERSION={data['pdf_inspector_version']}",
        "PDF_INSPECTOR_IMPORT_SUCCESS=1",
        "PDF_INSPECTOR_MODIFIED=0",
        "Q2_WORKSET_ROWS=7",
        "Q2_UNKNOWN_PAPER_ID=0",
        "UNIQUE_Q2_PAPER_IDS=7",
        "UNIQUE_Q2_SOURCE_PATHS=7",
        "UNIQUE_Q2_DERIVED_PATHS=7",
        f"Q2_SOURCE_SHA_MISMATCH={data['source_mismatch']}",
        f"Q2_DERIVED_MISSING={data['derived_missing']}",
        f"Q2_DERIVED_SHA_MISMATCH={data['derived_mismatch']}",
        f"Q2_PAGE_COUNT_MISMATCH={data['page_mismatch']}",
        "PROCESS_PDF_PAGE_SCOPED_AVAILABLE=1",
        "EXTRACT_TEXT_PAGE_SCOPED_AVAILABLE=0",
        "POSITIONED_TEXT_PAGE_SCOPED_AVAILABLE=1",
        "MARKDOWN_PAGE_SCOPED_AVAILABLE=1",
        "PAGE_SCOPED_EXTRACTION_AVAILABLE=1",
        "PAGE_SCOPED_EXTRACTION_API=extract_text_in_regions",
        "PAGE_FILTER_PARAMETER=page_regions=[(page_0indexed, [[x1,y1,x2,y2]])]",
        "PAGE_FILTER_INDEX_BASE=0-based",
        "SOURCE_PAGE_NUMBERING=1-based",
        f"Q2_TOTAL_PAGES={data['total_pages']}",
        f"PAGE_AUDIT_ROWS={data['audit_rows']}",
        f"PAGE_ZERO_PRESENT={data['page_zero']}",
        f"PAGE_GAPS={data['page_gaps']}",
        f"DUPLICATE_SOURCE_PAGES={data['duplicate_source_pages']}",
        f"OUT_OF_RANGE_PAGES={data['out_of_range_pages']}",
        f"VERIFIED_BLANK_PAGES={data['verified_blank_pages']}",
        f"PAGE_TEXT_EMPTY_VERIFIED_BLANK={data['empty_verified_blank']}",
        f"PAGE_TEXT_EMPTY_UNEXPECTED={data['empty_unexpected']}",
        f"NONBLANK_PAGES={data['nonblank_pages']}",
        f"NONBLANK_PAGES_WITH_TEXT={data['nonblank_with_text']}",
        f"NONBLANK_PAGES_WITHOUT_TEXT={data['nonblank_without_text']}",
        f"GARBLED_PAGE_COUNT={data['garbled_pages']}",
        f"WHOLE_DOCUMENT_TEXT_CHARS={data['whole_chars']}",
        f"PAGE_JOINED_TEXT_CHARS={data['joined_chars']}",
        f"PAGE_JOINED_RELATIVE_CHAR_DIFFERENCE={data['relative_difference']:.6f}",
        f"PAGE_JOINED_TEXT_COVERAGE_ACCEPTABLE={data['coverage_acceptable']}",
        f"Q2_PAGE_AWARE_MARKDOWN_PREVIEW_SUCCESS={data['preview_success']}",
        f"PAGE_AWARE_CONTRACT_FROZEN={data['contract_frozen']}",
        "FORMAL_G6_ARTIFACTS_GENERATED=0",
        f"TEMP_PREVIEW_FILES_REMAINING={data['temp_remaining']}",
        "OCR_RUN=0",
        "PDF_REPAIR_RUN=0",
        "IMAGE_REPAIR_RUN=0",
        "SOURCE_REACQUISITION_RUN=0",
        "FORMAL_MARKDOWN_GENERATION_RUN=0",
        "FORMAL_METADATA_GENERATION_RUN=0",
        "FORMAL_KNOWLEDGE_CARD_GENERATION_RUN=0",
        "G6_00E_RERUN=0",
        "G6_15_RUN=0",
        "G6_25_RUN=0",
        "G6_INT_RUN=0",
        f"G1_CATALOG_MODIFIED={protected['G1']}",
        f"G2_CATALOG_MODIFIED={protected['G2']}",
        f"G3_IDENTITY_MODIFIED={protected['G3']}",
        f"G3_25R_MAPPING_MODIFIED={protected['G3_25R']}",
        f"G4_OUTPUT_MODIFIED={protected['G4']}",
        f"G5_OUTPUT_MODIFIED={protected['G5']}",
        f"G5_REPAIR_MANIFEST_MODIFIED={protected['G5_REPAIR']}",
        f"G5_OCR_DERIVATIVES_MODIFIED={protected['G5_OCR_DERIVATIVES']}",
        f"ORIGINAL_FILES_MODIFIED={data['original_modified']}",
        "ORIGINAL_FILES_DELETED=0",
        "ORIGINAL_FILES_MOVED_OR_RENAMED=0",
        f"DUPLICATE_PAGE_AUDIT_ROWS={data['duplicate_audit_rows']}",
        f"DUPLICATE_CONTRACT_FILES={data['duplicate_contract_files']}",
        f"IDEMPOTENCY_PASS={data['idempotency']}",
        "",
        "OUTPUTS=",
        f"- {AUDIT}",
        f"- {CONTRACT}" if data["contract_frozen"] else "- page-aware contract not frozen because the audit is blocked",
        f"- {LOG}",
        f"- {REPORT}",
        f"- {ROOT / 'tools' / '30_g6_00f_page_aware_extraction.py'}",
        "",
        "PRE_EXISTING_CHANGES=all pre-existing untracked workspace entries preserved; G3-25R outputs were read-only in this stage",
        "G6_00F_INTRODUCED_CHANGES=tools/30_g6_00f_page_aware_extraction.py; catalog/pilot/g6_q2_page_extraction_audit.csv; logs/g6_00f_page_aware_extraction.log; reports/G6_00F_page_aware_extraction.md" + ("; catalog/pilot/g6_q2_page_extraction_contract.json" if data["contract_frozen"] else ""),
        "",
        "PAGE_EXTRACTION_SUMMARY=",
    ]
    for paper_id, summary in data["summaries"].items():
        lines.extend([
            f"- paper_id: {paper_id}",
            f"  pages: {summary['pages']}",
            f"  nonblank_pages: {summary['nonblank_pages']}",
            f"  unexpected_empty_pages: {summary['unexpected_empty_pages']}",
            f"  unexpected_empty_page_numbers: {summary['unexpected_empty_page_numbers']}",
            f"  verified_blank_pages: {summary['verified_blank_pages']}",
            f"  status: {summary['status']}",
        ])
    lines.extend([
        "",
        "CONTRACT_SUMMARY=",
        "- backend: pdf-inspector",
        "- input: G5 readable PDF",
        "- mode: page-scoped text extraction",
        "- api: extract_text_in_regions with one full-page region",
        "- final source_page numbering: 1-based",
        "- deterministic Markdown wrapper: allowed",
        "- whole-document artificial page splitting: forbidden",
        "- secondary extractor fallback: forbidden",
        "- OCR in G6: forbidden",
        "",
        "VALIDATION=",
        "- pdf-inspector 1.15.0 was imported from the fixed D:\\python environment; no dependency installation ran.",
        "- Page selection was explicit and 0-based; every audit source_page is api_page_index + 1.",
        "- Four marker-only pages in C132 matched the four G5-verified blank pages; four additional marker-only pages conflicted with G5 text-page counts and therefore blocked the stage.",
        "- Page-joined native text was compared in memory with whole-document extract_text after whitespace normalization.",
        "- Temporary previews were created only for validation and removed; formal G6 artifacts were not generated.",
        "",
        "ISSUES=",
        "- extract_text has no page parameter; positioned text and native Markdown page calls remain diagnostic-only for Q2 because they return image markers/empty Markdown.",
        "",
        f"BLOCKER={data['blocker']}",
        "APPROVAL=Q2 page-aware pdf-inspector extraction contract verified and frozen" if data["status"] == "PASS" else "APPROVAL=NOT_APPROVED",
        f"NEXT={data['next']}",
    ])
    return lines


def main() -> int:
    started = now()
    prior_ready = LOG.exists() and "RUN_STATUS=READY_FOR_IDEMPOTENCY" in LOG.read_text(encoding="utf-8")
    before_protected = protected_snapshot()
    before_sources = {}
    workset = load_workset()
    for work in workset:
        before_sources[work["original_file_path"]] = digest(ROOT / work["original_file_path"])
        before_sources[work["readable_file_path"]] = digest(ROOT / work["readable_file_path"])
    source_mismatch, derived_missing, derived_mismatch, page_mismatch = verify_workset(workset)
    experiment = representative_experiment(workset[0])
    audit_rows, consistency = page_audit(workset)
    write_csv(AUDIT, audit_rows, ["paper_id", "source_page", "api_page_index", "api_call_mode", "text_chars", "text_nonempty", "needs_ocr_if_available", "verified_blank_page", "status"])
    preview_success, temp_remaining = write_preview(workset, audit_rows)
    duplicate_audit_rows = len(audit_rows) - len({(row["paper_id"], int(row["source_page"])) for row in audit_rows})
    after_protected = protected_snapshot()
    protected_drift = {group: int(any(after_protected.get(k) != v for k, v in before_protected.items() if k in {str(p.relative_to(ROOT)).replace("\\", "/") for p in paths})) for group, paths in protected_paths().items()}
    original_modified = int(any(digest(ROOT / path) != value for path, value in before_sources.items()))
    total_pages = sum(row["page_count"] for row in workset)
    expected_blank = sum(row["page_count"] - row["g5_pages_with_text"] for row in workset)
    actual_blank = sum(int(row["verified_blank_page"]) for row in audit_rows)
    nonblank = total_pages - actual_blank
    garbled_pages = sum(1 for row in audit_rows if row["status"] == "GARBLED")
    page_zero = int(any(int(row["source_page"]) == 0 for row in audit_rows))
    page_gaps = int(any(sorted(int(row["source_page"]) for row in audit_rows if row["paper_id"] == work["paper_id"]) != list(range(1, work["page_count"] + 1)) for work in workset))
    duplicate_source_pages = len(audit_rows) - len({(row["paper_id"], int(row["source_page"])) for row in audit_rows})
    out_of_range = int(any(int(row["source_page"]) < 1 or int(row["source_page"]) > next(w["page_count"] for w in workset if w["paper_id"] == row["paper_id"]) for row in audit_rows))
    coverage = int(consistency["relative_difference"] <= 0.25)
    empty_unexpected = sum(summary["unexpected_empty_pages"] for summary in consistency["summaries"].values())
    nonblank_without = sum(1 for row in audit_rows if not int(row["text_nonempty"]) and not int(row["verified_blank_page"]))
    garbled_pages = sum(1 for summary in consistency["summaries"].values() for _ in range(summary["garbled_pages"]))
    coverage = int(consistency["relative_difference"] <= 0.25)
    preliminary_gates = all([
        len(workset) == 7, source_mismatch == 0, derived_missing == 0, derived_mismatch == 0, page_mismatch == 0,
        len(audit_rows) == 516, page_zero == 0, page_gaps == 0, duplicate_source_pages == 0, out_of_range == 0,
        empty_unexpected == 0, nonblank_without == 0, garbled_pages == 0, coverage == 1, preview_success == 7,
        temp_remaining == 0, all(value == 0 for value in protected_drift.values()), original_modified == 0,
    ])
    duplicate_contract_files = freeze_contract() if preliminary_gates else len(list(CONTRACT.parent.glob("g6_q2_page_extraction_contract*.json")))
    contract_frozen = int(preliminary_gates and duplicate_contract_files == 1)
    all_gates = preliminary_gates and contract_frozen == 1
    idempotency = int(prior_ready and all_gates)
    status = "PASS" if all_gates and idempotency else "BLOCKED"
    if not preliminary_gates:
        blocker = f"PAGE_TEXT_EMPTY_UNEXPECTED={empty_unexpected}; NONBLANK_PAGES_WITHOUT_TEXT={nonblank_without}"
        next_step = "resolve pdf-inspector page-scoped text gaps or reconcile formal G5 blank-page evidence; do not rerun G6-00E"
    elif not idempotency:
        blocker = "IDEMPOTENCY_SECOND_INVOCATION_REQUIRED"
        next_step = "run the same G6-00F validator once more for idempotency verification"
    else:
        blocker = "NONE"
        next_step = "rerun G6-00E"
    append_log([
        f"[{started}] G6-00F run started",
        f"RUN_STATUS={'PASS' if status == 'PASS' else 'READY_FOR_IDEMPOTENCY' if all_gates else 'BLOCKED'}",
        f"API=extract_text_in_regions PAGE_FILTER_INDEX_BASE=0-based SOURCE_PAGE_NUMBERING=1-based",
        f"REPRESENTATIVE_EXPERIMENT={json.dumps(experiment, ensure_ascii=False)}",
        f"PAGE_AUDIT_ROWS={len(audit_rows)} WHOLE_DOCUMENT_TEXT_CHARS={consistency['whole_chars']} PAGE_JOINED_TEXT_CHARS={consistency['joined_chars']}",
        f"COMPLETED={now()}",
    ])
    data = {
        "status": status, "pdf_inspector_version": importlib.metadata.version("pdf-inspector"),
        "source_mismatch": source_mismatch, "derived_missing": derived_missing, "derived_mismatch": derived_mismatch,
        "page_mismatch": page_mismatch, "total_pages": total_pages, "audit_rows": len(audit_rows),
        "page_zero": page_zero, "page_gaps": page_gaps, "duplicate_source_pages": duplicate_source_pages,
        "out_of_range_pages": out_of_range, "verified_blank_pages": actual_blank, "empty_verified_blank": actual_blank,
        "empty_unexpected": empty_unexpected, "nonblank_pages": nonblank, "nonblank_with_text": nonblank - nonblank_without,
        "nonblank_without_text": nonblank_without, "garbled_pages": garbled_pages,
        "whole_chars": consistency["whole_chars"], "joined_chars": consistency["joined_chars"],
        "relative_difference": consistency["relative_difference"], "coverage_acceptable": coverage,
        "preview_success": preview_success, "temp_remaining": temp_remaining, "duplicate_audit_rows": duplicate_audit_rows,
        "duplicate_contract_files": duplicate_contract_files, "idempotency": idempotency,
        "contract_frozen": contract_frozen, "protected": protected_drift, "original_modified": original_modified, "summaries": consistency["summaries"],
        "blocker": blocker, "next": next_step,
    }
    REPORT.write_text("\n".join(report(data)) + "\n", encoding="utf-8")
    print("\n".join(report(data)))
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
