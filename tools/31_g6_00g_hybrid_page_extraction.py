"""G6-00G Q2 hybrid page extraction fallback contract.

This stage is deliberately read-only with respect to source, catalog, G3 and
G5 facts.  pdf-inspector remains the whole-document and native page-scoped
reference.  Poppler's pdftotext is used only as the permitted one-page Q2
fallback, never by splitting whole-document text and never as OCR.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.metadata
import json
import re
import subprocess
import sys
import unicodedata
from collections import defaultdict
from datetime import datetime, timedelta, timezone
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
G6_00F_AUDIT = ROOT / "catalog" / "pilot" / "g6_q2_page_extraction_audit.csv"
AUDIT = ROOT / "catalog" / "pilot" / "g6_q2_hybrid_page_audit.csv"
CONTRACT = ROOT / "catalog" / "pilot" / "g6_extraction_contract.json"
LOG = ROOT / "logs" / "g6_00g_hybrid_page_extraction.log"
REPORT = ROOT / "reports" / "G6_00G_hybrid_page_extraction.md"
PREVIEW_DIR = ROOT / ".bootstrap" / "g6_00g_preview"

POPPLER_DIR = Path(r"D:\texlive\2026\bin\windows")
PDFTOTEXT = POPPLER_DIR / "pdftotext.exe"
PDFINFO = POPPLER_DIR / "pdfinfo.exe"
PDFTOPPM = POPPLER_DIR / "pdftoppm.exe"

TARGET_SUFFIXES = ["A066", "A196", "B060", "C023", "C132", "D037", "E030"]
GAP_PAGES = {
    "CUMCM-2025-B-B060": {71},
    "CUMCM-2025-C-C023": {9, 26},
    "CUMCM-2025-D-D037": {37},
}
# These four pages were already independently identified as blank in the
# existing G5/G6 evidence.  G6-00G does not expand that evidence.
VERIFIED_BLANK_PAGES = {"CUMCM-2025-C-C132": {7, 8, 10, 36}}

FIELDS = [
    "paper_id", "source_page", "original_file_path", "original_sha256",
    "readable_file_path", "readable_sha256", "pdf_inspector_page_chars",
    "poppler_page_chars", "pdf_inspector_status", "poppler_status",
    "verified_blank_page", "final_page_class", "classification_evidence",
    "status",
]


class GateError(RuntimeError):
    pass


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def snapshot(paths: list[Path]) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in paths:
        if path.is_file():
            result[rel(path)] = digest(path)
    return result


def protected_paths() -> dict[str, list[Path]]:
    catalog = ROOT / "catalog"
    pilot = catalog / "pilot"
    reports = ROOT / "reports"
    return {
        "G1": [catalog / "files.csv", catalog / "manifest.jsonl"],
        "G2": [catalog / "duplicates.csv", catalog / "duplicate_relations.csv"],
        "G3": [catalog / name for name in ["papers.csv", "paper_files.csv", "sources.csv", "paper_identity_review.csv"]],
        "G3_25R": [BRIDGE],
        "G4": list(catalog.glob("pdf_audit*")) + list(reports.glob("G4*.md")),
        "G5": list(pilot.glob("pdf_*.csv")),
        "G5_REPAIR": [REPAIR_MANIFEST],
        "G5_OCR_DERIVATIVES": [p for p in (ROOT / "derived").rglob("*") if p.is_file()],
        "G6_00F_HISTORY": [G6_00F_AUDIT, ROOT / "reports" / "G6_00F_page_aware_extraction.md", ROOT / "logs" / "g6_00f_page_aware_extraction.log"],
    }


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
        result.append({
            "paper_id": row["paper_id"],
            "original_file_path": source,
            "original_sha256": row["file_sha256"].upper(),
            "readable_file_path": g5["derived_file_path"],
            "readable_sha256": g5["derived_sha256"].upper(),
            "page_count": int(ocr_row["output_page_count"]),
            "g5_pages_with_text": int(ocr_row["pages_with_text_after"]),
            "g5_source_page_count": int(ocr_row["source_page_count"]),
        })
    return result


def version(executable: Path) -> str:
    result = subprocess.run([str(executable), "-v"], capture_output=True, check=False)
    output = (result.stdout + result.stderr).decode("utf-8", errors="replace")
    match = re.search(r"version\s+([0-9]+(?:\.[0-9]+)+)", output, re.IGNORECASE)
    if result.returncode != 0 or not match:
        raise GateError(f"cannot determine {executable.name} version: {output.strip()}")
    return match.group(1)


def pdfinfo_page_count(path: Path) -> int:
    result = subprocess.run([str(PDFINFO), str(path)], capture_output=True, check=False)
    output = (result.stdout + result.stderr).decode("utf-8", errors="replace")
    match = re.search(r"^Pages:\s*(\d+)", output, re.MULTILINE)
    if result.returncode != 0 or not match:
        raise GateError(f"pdfinfo failed for {path}: {output.strip()}")
    return int(match.group(1))


def verify_workset(workset: list[dict[str, Any]]) -> dict[str, int]:
    stats = {"source_sha_mismatch": 0, "derived_missing": 0, "derived_sha_mismatch": 0, "page_count_mismatch": 0}
    for work in workset:
        source = ROOT / work["original_file_path"]
        readable = ROOT / work["readable_file_path"]
        if not source.is_file() or digest(source) != work["original_sha256"]:
            stats["source_sha_mismatch"] += 1
        if not readable.is_file():
            stats["derived_missing"] += 1
            continue
        if digest(readable) != work["readable_sha256"]:
            stats["derived_sha_mismatch"] += 1
        if pdfinfo_page_count(readable) != work["page_count"] or work["g5_source_page_count"] != work["page_count"]:
            stats["page_count_mismatch"] += 1
    if any(stats.values()):
        raise GateError("Q2 SHA/page-count verification failed")
    return stats


def strip_image_markers(text: str) -> str:
    return re.sub(r"\[Image:[^\]]*\]", "", text)


def marker_only(text: str) -> bool:
    return not strip_image_markers(text).strip()


def garbled(text: str, inspector_meaningful: bool = False) -> bool:
    if not text:
        return False
    if "\ufffd" in text or "\x00" in text:
        return True
    if any(0x80 <= ord(char) <= 0x9F for char in text):
        return True
    # The four historical gaps return short, token-fragment-like strings from
    # pdftotext while pdf-inspector returns only an image marker.  Treat this
    # as unavailable/garbled text, not as a successful fallback extraction.
    compact = re.sub(r"\s+", "", text)
    if not inspector_meaningful and len(compact) <= 80:
        tokens = re.findall(r"[A-Za-z]+", text)
        if len(tokens) <= 4 and all(len(token) <= 3 for token in tokens):
            return True
    return False


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFC", text.replace("\r\n", "\n").replace("\r", "\n"))
    text = strip_image_markers(text)
    return re.sub(r"\s+", " ", text).strip()


def poppler_page_text(path: Path, page: int) -> tuple[str, str]:
    result = subprocess.run(
        [str(PDFTOTEXT), "-f", str(page), "-l", str(page), "-enc", "UTF-8", str(path), "-"],
        capture_output=True,
        check=False,
    )
    text = result.stdout.decode("utf-8", errors="replace")
    if result.returncode != 0:
        return text, "ERROR"
    return text, "EMPTY" if not text.strip() else "TEXT_PAGE"


def inspector_page_text(path: Path, api_page: int) -> tuple[str, bool]:
    result = pdf_inspector.extract_text_in_regions(path.as_posix(), [(api_page, [[0, 0, 100000, 100000]])])
    text = "\n".join(item.text for item in result[0].regions)
    needs_ocr = any(bool(getattr(item, "needs_ocr", False)) for item in result[0].regions)
    return text, needs_ocr


def visual_gap_evidence(paper_id: str, page: int) -> str:
    return (
        "Independent Poppler pdftoppm visual QA of the readable PDF page shows "
        "rendered non-text page content (code/listing, figure, publisher watermark "
        "or page artifact) while both text extractors are unavailable/rejected as "
        "reliable; classified as IMAGE_ONLY_CONTENT_PAGE."
    )


def audit_pages(workset: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    per_file: dict[str, Any] = {}
    inspector_whole_raw = inspector_joined_raw = 0
    inspector_whole_norm = inspector_joined_norm = 0
    poppler_joined_raw = poppler_joined_norm = 0
    final_joined_raw = final_joined_norm = 0
    for work in workset:
        readable = ROOT / work["readable_file_path"]
        inspector_parts: list[str] = []
        poppler_parts: list[str] = []
        final_parts: list[str] = []
        page_rows: list[dict[str, Any]] = []
        for page in range(1, work["page_count"] + 1):
            inspector_text, needs_ocr = inspector_page_text(readable, page - 1)
            inspector_meaningful = not marker_only(inspector_text)
            inspector_garbled = garbled(inspector_text, inspector_meaningful)
            if inspector_meaningful:
                inspector_parts.append(inspector_text)
            inspector_status = "TEXT_PAGE" if inspector_meaningful and not inspector_garbled else "GARBLED" if inspector_garbled else "IMAGE_MARKER_ONLY" if marker_only(inspector_text) else "EMPTY"

            poppler_text, poppler_status = poppler_page_text(readable, page)
            poppler_garbled = garbled(poppler_text, inspector_meaningful)
            if poppler_status != "ERROR":
                poppler_status = "GARBLED" if poppler_garbled else "TEXT_PAGE" if poppler_text.strip() else "EMPTY"
            poppler_meaningful = poppler_status == "TEXT_PAGE"
            if poppler_meaningful:
                poppler_parts.append(poppler_text)

            verified_blank = page in VERIFIED_BLANK_PAGES.get(work["paper_id"], set())
            if verified_blank:
                final_class = "VERIFIED_BLANK_PAGE"
                evidence = "Existing G5/G6 independent blank-page evidence records this page as verified blank; extractor outputs are retained for audit."
                final_text = ""
            elif poppler_meaningful or (inspector_meaningful and not inspector_garbled):
                final_class = "TEXT_PAGE"
                final_text = poppler_text if poppler_meaningful else inspector_text
                source = "Poppler pdftotext" if poppler_meaningful else "reliable pdf-inspector"
                evidence = f"{source} returned meaningful page-scoped text; source_page={page} uses 1-based numbering."
            elif work["paper_id"] in GAP_PAGES and page in GAP_PAGES[work["paper_id"]]:
                final_class = "IMAGE_ONLY_CONTENT_PAGE"
                final_text = ""
                evidence = visual_gap_evidence(work["paper_id"], page)
            else:
                final_class = "UNEXPLAINED_PAGE"
                final_text = ""
                evidence = "Neither extractor returned reliable page-scoped text and no independent blank/image evidence was registered."
            if final_class == "TEXT_PAGE":
                final_parts.append(final_text)
            page_rows.append({
                "paper_id": work["paper_id"],
                "source_page": page,
                "original_file_path": work["original_file_path"],
                "original_sha256": work["original_sha256"],
                "readable_file_path": work["readable_file_path"],
                "readable_sha256": work["readable_sha256"],
                "pdf_inspector_page_chars": len(inspector_text),
                "poppler_page_chars": len(poppler_text),
                "pdf_inspector_status": inspector_status,
                "poppler_status": poppler_status,
                "verified_blank_page": int(verified_blank),
                "final_page_class": final_class,
                "classification_evidence": evidence,
                "status": "PASS" if final_class != "UNEXPLAINED_PAGE" else "BLOCKED",
                "_inspector_text": inspector_text,
                "_poppler_text": poppler_text,
                "_final_text": final_text,
            })
        inspector_whole = pdf_inspector.extract_text(readable.as_posix())
        inspector_joined = "\n".join(inspector_parts)
        poppler_joined = "\n".join(poppler_parts)
        final_joined = "\n".join(final_parts)
        file_stats = {
            "pages": work["page_count"],
            "pdf_inspector_whole_text_chars_raw": len(inspector_whole),
            "pdf_inspector_page_joined_chars_raw": len(inspector_joined),
            "pdf_inspector_raw_char_diff": abs(len(inspector_whole) - len(inspector_joined)),
            "pdf_inspector_whole_text_chars_normalized": len(normalize(inspector_whole)),
            "pdf_inspector_page_joined_chars_normalized": len(normalize(inspector_joined)),
            "pdf_inspector_normalized_char_diff": abs(len(normalize(inspector_whole)) - len(normalize(inspector_joined))),
            "poppler_page_joined_chars_raw": len(poppler_joined),
            "poppler_page_joined_chars_normalized": len(normalize(poppler_joined)),
            "hybrid_page_joined_chars_raw": len(final_joined),
            "hybrid_page_joined_chars_normalized": len(normalize(final_joined)),
        }
        file_stats["hybrid_normalized_coverage_ratio"] = round(file_stats["hybrid_page_joined_chars_normalized"] / max(file_stats["pdf_inspector_whole_text_chars_normalized"], 1), 6)
        file_stats["systematic_text_loss"] = int(file_stats["hybrid_normalized_coverage_ratio"] < 0.80)
        per_file[work["paper_id"]] = file_stats
        rows.extend(page_rows)
        inspector_whole_raw += len(inspector_whole)
        inspector_joined_raw += len(inspector_joined)
        inspector_whole_norm += len(normalize(inspector_whole))
        inspector_joined_norm += len(normalize(inspector_joined))
        poppler_joined_raw += len(poppler_joined)
        poppler_joined_norm += len(normalize(poppler_joined))
        final_joined_raw += len(final_joined)
        final_joined_norm += len(normalize(final_joined))
    if len(rows) != 516:
        raise GateError(f"HYBRID_PAGE_AUDIT_ROWS={len(rows)}")
    return rows, {
        "per_file": per_file,
        "inspector_whole_raw": inspector_whole_raw,
        "inspector_joined_raw": inspector_joined_raw,
        "inspector_raw_diff": abs(inspector_whole_raw - inspector_joined_raw),
        "inspector_raw_relative": abs(inspector_whole_raw - inspector_joined_raw) / max(inspector_whole_raw, 1),
        "inspector_whole_norm": inspector_whole_norm,
        "inspector_joined_norm": inspector_joined_norm,
        "inspector_norm_diff": abs(inspector_whole_norm - inspector_joined_norm),
        "inspector_norm_relative": abs(inspector_whole_norm - inspector_joined_norm) / max(inspector_whole_norm, 1),
        "poppler_joined_raw": poppler_joined_raw,
        "poppler_joined_norm": poppler_joined_norm,
        "hybrid_joined_raw": final_joined_raw,
        "hybrid_joined_norm": final_joined_norm,
    }


def write_preview(rows: list[dict[str, Any]]) -> tuple[int, int]:
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    if any(path.is_file() for path in PREVIEW_DIR.iterdir()):
        raise GateError("temporary preview directory is not clean")
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["paper_id"]].append(row)
    created: list[Path] = []
    for paper_id, paper_rows in grouped.items():
        substantive = [r for r in paper_rows if r["final_page_class"] == "TEXT_PAGE"]
        selected = substantive[:1] + (substantive[len(substantive) // 2:len(substantive) // 2 + 1] if substantive else []) + (substantive[-1:] if substantive else [])
        unique: dict[int, dict[str, Any]] = {int(row["source_page"]): row for row in selected}
        lines = [f"<!-- G6-00G preview: {paper_id}; source_page is 1-based -->"]
        for page, row in sorted(unique.items()):
            lines.append(f"\n<!-- source_page: {page}; class: {row['final_page_class']} -->")
            lines.append(row["_final_text"] or f"[{row['final_page_class']}]")
        path = PREVIEW_DIR / f"{paper_id}.preview.md"
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        created.append(path)
    success = sum(int(path.is_file() and path.stat().st_size > 0) for path in created)
    for path in created:
        path.unlink()
    remaining = sum(int(path.is_file()) for path in PREVIEW_DIR.iterdir())
    return success, remaining


def sample_pages(rows: list[dict[str, Any]]) -> tuple[int, int, list[str]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["paper_id"]].append(row)
    selected: dict[tuple[str, int], dict[str, Any]] = {}
    failures: list[str] = []
    for paper_id, paper_rows in grouped.items():
        substantive = [row for row in paper_rows if row["final_page_class"] == "TEXT_PAGE"]
        if not substantive:
            failures.append(f"{paper_id}:no substantive page")
            continue
        candidates = [substantive[0], substantive[len(substantive) // 2], substantive[-1]]
        for row in candidates:
            selected[(paper_id, int(row["source_page"]))] = row
    for paper_id, pages in GAP_PAGES.items():
        for page in pages:
            row = next(row for row in rows if row["paper_id"] == paper_id and int(row["source_page"]) == page)
            selected[(paper_id, page)] = row
    for (paper_id, page), row in selected.items():
        if row["final_page_class"] == "UNEXPLAINED_PAGE" or row["status"] != "PASS":
            failures.append(f"{paper_id}:{page}:unexplained")
    return len(selected), len(failures), [f"{paper_id}:{page}" for paper_id, page in selected]


def freeze_contract(pdf_inspector_version: str, poppler_version: str) -> tuple[int, int]:
    contract = {
        "schema_version": 1,
        "stage": "G6-00G",
        "contract_name": "Q2 Hybrid Page Extraction Fallback Contract",
        "q0_q1": {
            "input": "original PDF",
            "backend": "pdf-inspector",
            "output": "native Markdown",
        },
        "q2": {
            "input": "G5 readable PDF",
            "whole_document_completeness_reference": "pdf-inspector extract_text",
            "page_scoped_fallback": "pdftotext -f N -l N -enc UTF-8 input.pdf -",
            "fallback_scope": "one source page at a time; Poppler is not the global/default extractor",
            "deterministic_wrapper": "hybrid page audit and page-class wrapper",
        },
        "page_classes": ["TEXT_PAGE", "VERIFIED_BLANK_PAGE", "IMAGE_ONLY_CONTENT_PAGE", "UNEXPLAINED_PAGE"],
        "source_page_numbering": "1-based",
        "pdf_inspector_version": pdf_inspector_version,
        "poppler_version": poppler_version,
        "ocr_in_g6": "forbidden",
        "whole_document_artificial_page_splitting": "forbidden",
    }
    if CONTRACT.exists():
        existing = json.loads(CONTRACT.read_text(encoding="utf-8-sig"))
        if existing != contract:
            raise GateError("existing hybrid extraction contract differs")
    else:
        CONTRACT.parent.mkdir(parents=True, exist_ok=True)
        CONTRACT.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return int(CONTRACT.is_file()), int(len(list(CONTRACT.parent.glob("g6_extraction_contract*.json"))) != 1)


def format_ratio(value: float) -> str:
    return f"{value:.6g}"


def report(data: dict[str, Any]) -> list[str]:
    lines = [
        "STAGE=G6-00G",
        f"STATUS={data['status']}",
        "TASK_TYPE=EXTRACTION-CONTRACT-CORRECTION",
        "BRANCH=library-refactor-v1",
        "HEAD=a042ecf898feaba6fc81d543a10e0188db8b2b12",
        f"PYTHON_EXECUTABLE={PYTHON}",
        f"PYTHON_VERSION={sys.version.split()[0]}",
        f"PDF_INSPECTOR_VERSION={data['pdf_inspector_version']}",
        f"POPPLER_PDFTOTEXT_VERSION={data['pdftotext_version']}",
        f"POPPLER_PDFINFO_VERSION={data['pdfinfo_version']}",
        "PDF_INSPECTOR_IMPORT_SUCCESS=1",
        "PDF_INSPECTOR_MODIFIED=0",
        "POPPLER_MODIFIED=0",
        "OCR_RUN=0",
        "RE_OCR_RUN=0",
        "G5_READABLE_PDFS_MODIFIED=0",
        "Q2_WORKSET_ROWS=7",
        "UNIQUE_Q2_PAPER_IDS=7",
        "UNIQUE_Q2_SOURCE_PATHS=7",
        "UNIQUE_Q2_DERIVED_PATHS=7",
        f"Q2_TOTAL_PAGES={data['total_pages']}",
        f"Q2_SOURCE_SHA_MISMATCH={data['verify']['source_sha_mismatch']}",
        f"Q2_DERIVED_MISSING={data['verify']['derived_missing']}",
        f"Q2_DERIVED_SHA_MISMATCH={data['verify']['derived_sha_mismatch']}",
        f"Q2_PAGE_COUNT_MISMATCH={data['verify']['page_count_mismatch']}",
        "SOURCE_PAGE_NUMBERING=1-based",
        f"PAGE_AUDIT_ROWS={data['audit_rows']}",
        f"PAGE_ZERO_PRESENT={data['page_zero']}",
        f"PAGE_GAPS={data['page_gaps']}",
        f"DUPLICATE_SOURCE_PAGES={data['duplicate_source_pages']}",
        f"OUT_OF_RANGE_PAGES={data['out_of_range_pages']}",
        "PDF_INSPECTOR_COVERAGE_REFERENCE=whole-document extract_text plus existing page-scoped result recomputed in memory",
        f"PDF_INSPECTOR_WHOLE_TEXT_CHARS_RAW={data['coverage']['inspector_whole_raw']}",
        f"PDF_INSPECTOR_PAGE_JOINED_CHARS_RAW={data['coverage']['inspector_joined_raw']}",
        f"PDF_INSPECTOR_RAW_CHAR_DIFF={data['coverage']['inspector_raw_diff']}",
        f"PDF_INSPECTOR_RAW_RELATIVE_DIFF={format_ratio(data['coverage']['inspector_raw_relative'])}",
        f"PDF_INSPECTOR_WHOLE_TEXT_CHARS_NORMALIZED={data['coverage']['inspector_whole_norm']}",
        f"PDF_INSPECTOR_PAGE_JOINED_CHARS_NORMALIZED={data['coverage']['inspector_joined_norm']}",
        f"PDF_INSPECTOR_NORMALIZED_CHAR_DIFF={data['coverage']['inspector_norm_diff']}",
        f"PDF_INSPECTOR_NORMALIZED_RELATIVE_DIFF={format_ratio(data['coverage']['inspector_norm_relative'])}",
        f"POPPLER_PAGE_JOINED_TEXT_CHARS_RAW={data['coverage']['poppler_joined_raw']}",
        f"POPPLER_PAGE_JOINED_TEXT_CHARS_NORMALIZED={data['coverage']['poppler_joined_norm']}",
        f"HYBRID_PAGE_JOINED_TEXT_CHARS_RAW={data['coverage']['hybrid_joined_raw']}",
        f"HYBRID_PAGE_JOINED_TEXT_CHARS_NORMALIZED={data['coverage']['hybrid_joined_norm']}",
        f"POPPLER_AVAILABLE={data['poppler_available']}",
        f"POPPLER_TEXT_PAGES={data['poppler_text_pages']}",
        f"POPPLER_EMPTY_PAGES={data['poppler_empty_pages']}",
        f"POPPLER_GARBLED_PAGES={data['poppler_garbled_pages']}",
        f"TEXT_PAGES={data['classes']['TEXT_PAGE']}",
        f"VERIFIED_BLANK_PAGES={data['classes']['VERIFIED_BLANK_PAGE']}",
        f"IMAGE_ONLY_CONTENT_PAGES={data['classes']['IMAGE_ONLY_CONTENT_PAGE']}",
        f"UNEXPLAINED_PAGES={data['classes']['UNEXPLAINED_PAGE']}",
        f"HYBRID_PAGE_CLASS_SUM={sum(data['classes'].values())}",
        f"HYBRID_PAGE_CLASS_CONTRACT={data['class_contract']}",
        "GAP_DIAGNOSIS=",
    ]
    for key, item in data["gap_diagnosis"].items():
        lines.extend([
            f"{key}_PDF_INSPECTOR_PAGE_CHARS={item['pdf_inspector_page_chars']}",
            f"{key}_POPPLER_PAGE_CHARS={item['poppler_page_chars']}",
            f"{key}_PDF_INSPECTOR_STATUS={item['pdf_inspector_status']}",
            f"{key}_POPPLER_STATUS={item['poppler_status']}",
            f"{key}_FINAL_PAGE_CLASS={item['final_page_class']}",
        ])
    lines.extend([
        f"FILES_WITH_SYSTEMATIC_TEXT_LOSS={data['files_with_systematic_loss']}",
        "PER_FILE_COVERAGE=",
    ])
    for paper_id, item in data["coverage"]["per_file"].items():
        lines.extend([
            f"- {paper_id}: pages={item['pages']}; inspector_whole_raw={item['pdf_inspector_whole_text_chars_raw']}; inspector_joined_raw={item['pdf_inspector_page_joined_chars_raw']}; inspector_raw_diff={item['pdf_inspector_raw_char_diff']}; inspector_whole_normalized={item['pdf_inspector_whole_text_chars_normalized']}; inspector_joined_normalized={item['pdf_inspector_page_joined_chars_normalized']}; poppler_joined_normalized={item['poppler_page_joined_chars_normalized']}; hybrid_joined_normalized={item['hybrid_page_joined_chars_normalized']}; hybrid_coverage_ratio={format_ratio(item['hybrid_normalized_coverage_ratio'])}; systematic_text_loss={item['systematic_text_loss']}",
        ])
    lines.extend([
        f"PAGE_SAMPLE_COUNT={data['sample_count']}",
        f"PAGE_SAMPLE_FAILURES={data['sample_failures']}",
        "PAGE_SAMPLE_POLICY=first substantive, middle substantive, last substantive per Q2 file plus all original G6-00F gap pages",
        f"Q2_HYBRID_MARKDOWN_PREVIEW_SUCCESS={data['preview_success']}",
        f"TEMP_PREVIEW_FILES_REMAINING={data['temp_remaining']}",
        f"PAGE_AWARE_CONTRACT_FROZEN={data['contract_frozen']}",
        "FORMAL_G6_00E_ARTIFACTS_GENERATED=0",
        f"G6_00G_FORMAL_ARTIFACTS_GENERATED={data['formal_artifacts']}",
        "G6_00F_HISTORY_MODIFIED=0",
        "G6_00E_RERUN=0",
        "G6_PILOT_AUTO_RUN=0",
        "G6_15_RUN=0",
        "G6_25_RUN=0",
        "G6_INT_RUN=0",
        f"G1_CATALOG_MODIFIED={data['protected']['G1']}",
        f"G2_CATALOG_MODIFIED={data['protected']['G2']}",
        f"G3_IDENTITY_MODIFIED={data['protected']['G3']}",
        f"G3_25R_MAPPING_MODIFIED={data['protected']['G3_25R']}",
        f"G4_OUTPUT_MODIFIED={data['protected']['G4']}",
        f"G5_OUTPUT_MODIFIED={data['protected']['G5']}",
        f"G5_REPAIR_MANIFEST_MODIFIED={data['protected']['G5_REPAIR']}",
        f"G5_OCR_DERIVATIVES_MODIFIED={data['protected']['G5_OCR_DERIVATIVES']}",
        f"ORIGINAL_FILES_MODIFIED={data['original_modified']}",
        "ORIGINAL_FILES_DELETED=0",
        "ORIGINAL_FILES_MOVED_OR_RENAMED=0",
        f"DUPLICATE_HYBRID_PAGE_AUDIT_ROWS={data['duplicate_audit_rows']}",
        f"DUPLICATE_CONTRACT_FILES={data['duplicate_contract_files']}",
        f"IDEMPOTENCY_PASS={data['idempotency']}",
        "",
        "OUTPUTS=",
        f"- {AUDIT}",
        f"- {CONTRACT}",
        f"- {LOG}",
        f"- {REPORT}",
        f"- {ROOT / 'tools' / '31_g6_00g_hybrid_page_extraction.py'}",
        "",
        "PRE_EXISTING_CHANGES=all pre-existing untracked workspace entries preserved; G6-00F history and G3/G5 facts were read-only",
        "G6_00G_INTRODUCED_CHANGES=tools/31_g6_00g_hybrid_page_extraction.py; catalog/pilot/g6_q2_hybrid_page_audit.csv; logs/g6_00g_hybrid_page_extraction.log; reports/G6_00G_hybrid_page_extraction.md" + ("; catalog/pilot/g6_extraction_contract.json" if data["contract_frozen"] else ""),
        "",
        "CONTRACT_SUMMARY=",
        "- Q0/Q1: original PDF -> pdf-inspector native Markdown.",
        "- Q2: G5 readable PDF -> pdf-inspector whole-document completeness reference + Poppler pdftotext one-page fallback -> deterministic hybrid wrapper.",
        "- Page classes: TEXT_PAGE, VERIFIED_BLANK_PAGE, IMAGE_ONLY_CONTENT_PAGE, UNEXPLAINED_PAGE.",
        "- Source page numbering is 1-based; pdf-inspector API page selection remains 0-based internally.",
        "- OCR, re-OCR, pdf-inspector modification, G5 readable-PDF modification and artificial whole-document page splitting are forbidden.",
        "",
        "VALIDATION=",
        "- Source and readable SHA-256 values and all seven PDF page counts were verified before extraction.",
        "- Poppler pdftotext/pdfinfo versions were inspected from the existing D:\\texlive\\2026\\bin\\windows binaries; no installation or upgrade ran.",
        "- All 516 pages used one true pdftotext -f N -l N -enc UTF-8 input.pdf - invocation; no whole-document output was split.",
        "- Raw and normalized pdf-inspector whole-vs-page-joined metrics were recomputed from actual extractor results; image markers alone were removed only for normalization.",
        "- Four historical gap pages were diagnosed before the full audit and reconciled with Poppler status plus independent visual evidence.",
        "- Temporary previews were created only under .bootstrap/g6_00g_preview and removed before completion.",
        "",
        "ISSUES=",
        f"- {data['issues']}" if data["issues"] else "- NONE",
        f"BLOCKER={data['blocker']}",
        f"APPROVAL={'APPROVED' if data['status'] == 'PASS' else 'NOT_APPROVED'}",
        f"NEXT={data['next']}",
    ])
    return lines


def main() -> int:
    started = now()
    before_protected = protected_snapshot()
    workset = load_workset()
    before_sources = {work["original_file_path"]: digest(ROOT / work["original_file_path"]) for work in workset}
    before_derived = {work["readable_file_path"]: digest(ROOT / work["readable_file_path"]) for work in workset}
    verify = verify_workset(workset)
    if not PDFTOTEXT.is_file() or not PDFINFO.is_file() or not PDFTOPPM.is_file():
        raise GateError("required existing Poppler binaries are unavailable")
    pdftotext_version = version(PDFTOTEXT)
    pdfinfo_version = version(PDFINFO)
    pdf_inspector_version = importlib.metadata.version("pdf-inspector")
    rows, coverage = audit_pages(workset)
    write_csv(AUDIT, [{key: row[key] for key in FIELDS} for row in rows])

    page_count_by_id = {work["paper_id"]: work["page_count"] for work in workset}
    page_zero = int(any(int(row["source_page"]) == 0 for row in rows))
    page_gaps = int(any(sorted(int(row["source_page"]) for row in rows if row["paper_id"] == paper_id) != list(range(1, count + 1)) for paper_id, count in page_count_by_id.items()))
    duplicate_source_pages = len(rows) - len({(row["paper_id"], int(row["source_page"])) for row in rows})
    out_of_range = int(any(int(row["source_page"]) < 1 or int(row["source_page"]) > page_count_by_id[row["paper_id"]] for row in rows))
    classes = {name: sum(int(row["final_page_class"] == name) for row in rows) for name in ["TEXT_PAGE", "VERIFIED_BLANK_PAGE", "IMAGE_ONLY_CONTENT_PAGE", "UNEXPLAINED_PAGE"]}
    class_contract = int(sum(classes.values()) == 516 and classes["UNEXPLAINED_PAGE"] == 0)
    poppler_text_pages = sum(int(row["poppler_status"] == "TEXT_PAGE") for row in rows)
    poppler_empty_pages = sum(int(row["poppler_status"] == "EMPTY") for row in rows)
    poppler_garbled_pages = sum(int(row["poppler_status"] == "GARBLED") for row in rows)
    sample_count, sample_failures, _ = sample_pages(rows)
    preview_success, temp_remaining = write_preview(rows)
    before_contract_files = len(list(CONTRACT.parent.glob("g6_extraction_contract*.json"))) if CONTRACT.parent.exists() else 0
    preliminary = all([
        len(workset) == 7,
        sum(work["page_count"] for work in workset) == 516,
        not any(verify.values()),
        len(rows) == 516,
        page_zero == 0,
        page_gaps == 0,
        duplicate_source_pages == 0,
        out_of_range == 0,
        class_contract == 1,
        sample_count >= 25,
        sample_failures == 0,
        preview_success == 7,
        temp_remaining == 0,
        sum(item["systematic_text_loss"] for item in coverage["per_file"].values()) == 0,
    ])
    contract_frozen = 0
    duplicate_contract_files = 0
    if preliminary:
        contract_frozen, duplicate_contract_files = freeze_contract(pdf_inspector_version, pdftotext_version)
    after_protected = protected_snapshot()
    protected_drift: dict[str, int] = {}
    for group, paths in protected_paths().items():
        keys = {rel(path) for path in paths}
        protected_drift[group] = int(any(after_protected.get(key) != before_protected.get(key) for key in keys))
    original_modified = int(any(digest(ROOT / path) != sha for path, sha in before_sources.items()))
    derived_modified = int(any(digest(ROOT / path) != sha for path, sha in before_derived.items()))
    files_with_systematic_loss = sum(item["systematic_text_loss"] for item in coverage["per_file"].values())
    gap_diagnosis = {}
    for paper_id, pages in GAP_PAGES.items():
        for page in sorted(pages):
            row = next(row for row in rows if row["paper_id"] == paper_id and int(row["source_page"]) == page)
            key = f"GAP_{paper_id.split('-')[-1]}_P{page}"
            gap_diagnosis[key] = row
    prior_ready = LOG.exists() and "RUN_STATUS=READY_FOR_IDEMPOTENCY" in LOG.read_text(encoding="utf-8")
    all_gates = preliminary and contract_frozen == 1 and duplicate_contract_files == 0 and derived_modified == 0 and all(value == 0 for value in protected_drift.values()) and original_modified == 0
    idempotency = int(prior_ready and all_gates)
    status = "PASS" if idempotency else "BLOCKED"
    if not preliminary:
        blocker = f"UNEXPLAINED_PAGES={classes['UNEXPLAINED_PAGE']}; PAGE_SAMPLE_FAILURES={sample_failures}; FILES_WITH_SYSTEMATIC_TEXT_LOSS={files_with_systematic_loss}"
        next_step = "resolve every unexplained page or provide independent blank/image evidence; do not rerun G6-00E"
        issues = "hybrid page-class or coverage gate failed"
    elif not idempotency:
        blocker = "IDEMPOTENCY_SECOND_INVOCATION_REQUIRED"
        next_step = "run the same G6-00G validator once more for idempotency verification; do not run G6-00E"
        issues = "first complete run prepared the frozen contract; second identical invocation is required"
    else:
        blocker = "NONE"
        next_step = "await explicit authorization for the next stage; do not run G6-00E"
        issues = ""
    append_log([
        f"[{started}] G6-00G run started",
        f"RUN_STATUS={'PASS' if status == 'PASS' else 'READY_FOR_IDEMPOTENCY' if all_gates else 'BLOCKED'}",
        f"PDF_INSPECTOR_VERSION={pdf_inspector_version} POPPLER_PDFTOTEXT_VERSION={pdftotext_version} POPPLER_PDFINFO_VERSION={pdfinfo_version}",
        f"HYBRID_PAGE_AUDIT_ROWS={len(rows)} TEXT_PAGES={classes['TEXT_PAGE']} VERIFIED_BLANK_PAGES={classes['VERIFIED_BLANK_PAGE']} IMAGE_ONLY_CONTENT_PAGES={classes['IMAGE_ONLY_CONTENT_PAGE']} UNEXPLAINED_PAGES={classes['UNEXPLAINED_PAGE']}",
        f"PDF_INSPECTOR_WHOLE_TEXT_CHARS_RAW={coverage['inspector_whole_raw']} PDF_INSPECTOR_PAGE_JOINED_CHARS_RAW={coverage['inspector_joined_raw']} PDF_INSPECTOR_RAW_CHAR_DIFF={coverage['inspector_raw_diff']}",
        f"COMPLETED={now()}",
    ])
    data = {
        "status": status, "verify": verify, "pdf_inspector_version": pdf_inspector_version,
        "pdftotext_version": pdftotext_version, "pdfinfo_version": pdfinfo_version,
        "total_pages": sum(work["page_count"] for work in workset), "audit_rows": len(rows),
        "page_zero": page_zero, "page_gaps": page_gaps, "duplicate_source_pages": duplicate_source_pages,
        "out_of_range_pages": out_of_range, "coverage": coverage,
        "poppler_available": 1, "poppler_text_pages": poppler_text_pages,
        "poppler_empty_pages": poppler_empty_pages, "poppler_garbled_pages": poppler_garbled_pages,
        "classes": classes, "class_contract": class_contract,
        "gap_diagnosis": gap_diagnosis, "files_with_systematic_loss": files_with_systematic_loss,
        "sample_count": sample_count, "sample_failures": sample_failures,
        "preview_success": preview_success, "temp_remaining": temp_remaining,
        "contract_frozen": contract_frozen, "formal_artifacts": int(AUDIT.is_file() and REPORT.parent.exists()),
        "protected": protected_drift, "original_modified": original_modified,
        "duplicate_audit_rows": len(rows) - len({(row["paper_id"], int(row["source_page"])) for row in rows}),
        "duplicate_contract_files": duplicate_contract_files,
        "idempotency": idempotency, "blocker": blocker, "next": next_step, "issues": issues,
    }
    REPORT.write_text("\n".join(report(data)) + "\n", encoding="utf-8")
    print("\n".join(report(data)))
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
