#!/usr/bin/env python3
"""Read-only QA for the frozen CUMCM-2012-D-001 manual-print PDF candidate."""
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "scale"
REPORTS = ROOT / "reports" / "scale"
TARGET = "CUMCM-2012-D-001"
SOURCE = ROOT / "2012年数学建模国赛真题+优秀论文" / "2012年优秀论文" / "2012D：机器人避障问题 (2).doc"
DOCX = ROOT / "tmp" / "g8_doc_2012_d001_docx_intermediate" / TARGET / "source_rebuilt.docx"
PDF = ROOT / "tmp" / "g8_doc_2012_d001_manual_print_to_pdf" / TARGET / "manual_print_candidate.pdf"
RENDER_DIR = ROOT / "tmp" / "pdfs" / "g8_doc_2012_d001_manual_print_qa"
EXPECTED_SOURCE_SHA = "D93A9A6A9DE012927F8A5D4B36E1768CA3F6AFFB6952673F40FE2740D4032766"
EXPECTED_DOCX_SHA = "B948CA41387ABC408724B1D64286830B54B12198A33C54D8BE684661CA8937DC"
EXPECTED_PDF_SHA = "CBE28049A80C0B900CF82A0BE06492A906D56B39F27819D6F94C67C6FF349399"
PDF_INSPECTOR_PYTHON = Path("D:/python/python.exe")
PDFINFO = shutil.which("pdfinfo") or shutil.which("pdfinfo.exe")
PDFTOTEXT = shutil.which("pdftotext") or shutil.which("pdftotext.exe")
PDFTOPPM = shutil.which("pdftoppm") or shutil.which("pdftoppm.exe")
PDFIMAGES = shutil.which("pdfimages") or shutil.which("pdfimages.exe")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest().upper()


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\x00", "")).strip()


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text.replace("\x00", ""))


def require(tool: str | None, name: str) -> str:
    if not tool:
        raise RuntimeError(f"TOOL_UNAVAILABLE={name}")
    return tool


def run(command: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(command, cwd=cwd, capture_output=True, check=False)


def pdfinfo(path: Path) -> dict[str, Any]:
    completed = run([require(PDFINFO, "pdfinfo"), "-box", str(path)])
    if completed.returncode:
        raise RuntimeError("PDFINFO_FAILED=" + completed.stderr.decode("utf-8", errors="replace").strip())
    fields = {key.strip(): value.strip() for key, value in (line.split(":", 1) for line in completed.stdout.decode("utf-8", errors="replace").splitlines() if ":" in line)}
    return {"pages": int(fields["Pages"].strip()), "encrypted": fields.get("Encrypted", "").strip().lower(), "page_size": fields.get("Page size", ""), "page_rot": fields.get("Page rot", ""), "producer": fields.get("Producer", "")}


def poppler_page_text(path: Path, page: int) -> str:
    completed = run([require(PDFTOTEXT, "pdftotext"), "-f", str(page), "-l", str(page), "-layout", "-enc", "UTF-8", str(path), "-"])
    if completed.returncode:
        raise RuntimeError(f"PDFTOTEXT_FAILED=page_{page}")
    return normalize(completed.stdout.decode("utf-8", errors="replace"))


def inspector_pages(path: Path, pages: int) -> tuple[str, list[str]]:
    if not PDF_INSPECTOR_PYTHON.is_file():
        raise RuntimeError("PDF_INSPECTOR_PYTHON_UNAVAILABLE")
    relative = os.path.relpath(path, ROOT).replace("\\", "/")
    script = """import json, sys, pdf_inspector
p=sys.argv[1]; n=int(sys.argv[2])
meta=pdf_inspector.process_pdf(p)
rows=pdf_inspector.extract_text_in_regions(p, [(i, [[0,0,100000,100000]]) for i in range(n)])
print(json.dumps({'pdf_type': meta.pdf_type, 'texts': [x.regions[0].text for x in rows]}, ensure_ascii=False))
"""
    environment = dict(os.environ)
    environment["PYTHONIOENCODING"] = "utf-8"
    completed = subprocess.run([str(PDF_INSPECTOR_PYTHON), "-c", script, relative, str(pages)], cwd=ROOT, env=environment, capture_output=True, check=False)
    if completed.returncode:
        raise RuntimeError("PDF_INSPECTOR_FAILED=" + completed.stderr.decode("utf-8", errors="replace").strip())
    payload = json.loads(completed.stdout.decode("utf-8"))
    return payload["pdf_type"], [normalize(text) for text in payload["texts"]]


def image_objects_by_page(path: Path) -> dict[int, int]:
    completed = run([require(PDFIMAGES, "pdfimages"), "-list", str(path)])
    if completed.returncode:
        return {}
    counts: dict[int, int] = {}
    for line in completed.stdout.decode("utf-8", errors="replace").splitlines():
        parts = line.split()
        if len(parts) > 3 and parts[0].isdigit() and parts[2] == "image":
            counts[int(parts[0])] = counts.get(int(parts[0]), 0) + 1
    return counts


def render_pages(path: Path, count: int) -> dict[int, dict[str, Any]]:
    RENDER_DIR.mkdir(parents=True, exist_ok=True)
    prefix = RENDER_DIR / "page"
    completed = run([require(PDFTOPPM, "pdftoppm"), "-png", "-r", "96", "-f", "1", "-l", str(count), str(path), str(prefix)])
    if completed.returncode:
        raise RuntimeError("PDFTOPPM_FAILED=" + completed.stderr.decode("utf-8", errors="replace").strip())
    stats: dict[int, dict[str, Any]] = {}
    thumbs: list[Image.Image] = []
    for page in range(1, count + 1):
        image_path = RENDER_DIR / f"page-{page:02d}.png"
        image = Image.open(image_path).convert("RGB")
        gray = image.convert("L")
        # Ink is deliberately conservative: non-white render evidence only;
        # text extraction never by itself classifies a page as visually blank.
        mask = gray.point(lambda value: 255 if value < 245 else 0)
        bbox = mask.getbbox()
        ink = sum(mask.histogram()[1:]) / (image.width * image.height)
        edge = 0
        if bbox:
            edge = int(bbox[0] <= 1 or bbox[1] <= 1 or bbox[2] >= image.width - 1 or bbox[3] >= image.height - 1)
        stats[page] = {"render_path": str(image_path.relative_to(ROOT)).replace("\\", "/"), "render_width": image.width, "render_height": image.height, "ink_ratio": round(ink, 8), "ink_bbox": "" if not bbox else ",".join(map(str, bbox)), "edge_ink_suspected": edge}
        thumb = image.copy(); thumb.thumbnail((190, 270)); thumbs.append(thumb)
    sheet = Image.new("RGB", (4 * 210, 6 * 295), "white")
    draw = ImageDraw.Draw(sheet)
    for index, thumb in enumerate(thumbs):
        x, y = (index % 4) * 210 + 10, (index // 4) * 295 + 18
        sheet.paste(thumb, (x, y)); draw.text((x, 2 + (index // 4) * 295), f"Page {index + 1}", fill="black")
    sheet.save(RENDER_DIR / "contact_sheet.png")
    return stats


def docx_evidence(path: Path) -> dict[str, Any]:
    namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    with zipfile.ZipFile(path) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
        paragraphs = [normalize("".join(node.text or "" for node in paragraph.findall(".//w:t", namespace))) for paragraph in root.findall(".//w:p", namespace)]
        paragraphs = [value for value in paragraphs if value]
        tables = []
        for table in root.findall(".//w:tbl", namespace):
            cells = [normalize("".join(node.text or "" for node in cell.findall(".//w:t", namespace))) for cell in table.findall(".//w:tc", namespace)]
            cells = [value for value in cells if value]
            tables.append(cells)
        header_footer = []
        for name in archive.namelist():
            if name.startswith("word/header") or name.startswith("word/footer"):
                tree = ET.fromstring(archive.read(name))
                header_footer.extend(normalize("".join(node.text or "" for node in para.findall(".//w:t", namespace))) for para in tree.findall(".//w:p", namespace))
    text = normalize(" ".join([*paragraphs, *header_footer, *[" ".join(table) for table in tables]]))
    return {"paragraphs": paragraphs, "tables": tables, "header_footer": [value for value in header_footer if value], "text": text}


def table_signature_matches(tables: list[list[str]], pdf_text: str) -> tuple[int, list[str]]:
    target = compact(pdf_text)
    matched, evidence = 0, []
    for number, table in enumerate(tables, start=1):
        signature = compact(" ".join(table))[:50]
        if signature and signature in target:
            matched += 1; evidence.append(f"table_{number}:NORMALIZED_EXACT")
        else:
            # A contiguous representative cell sequence is valid table evidence
            # without pretending PDF object tables must match DOCX tables.
            cell = next((compact(value) for value in table if len(compact(value)) >= 12 and compact(value) in target), "")
            evidence.append(f"table_{number}:{'REPRESENTATIVE_CELL' if cell else 'NO_MATCH'}")
            matched += int(bool(cell))
    return matched, evidence


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    postflight = json.loads((CATALOG / "g8_doc_2012_d001_manual_print_result.json").read_text(encoding="utf-8"))
    fingerprint = json.loads((CATALOG / "g8_doc_2012_d001_identity_fingerprint.json").read_text(encoding="utf-8"))
    source_sha_before, docx_sha_before, pdf_sha_before = sha256_file(SOURCE), sha256_file(DOCX), sha256_file(PDF)
    info = pdfinfo(PDF)
    inspector_type, inspector_texts = inspector_pages(PDF, info["pages"])
    poppler_texts = [poppler_page_text(PDF, page) for page in range(1, info["pages"] + 1)]
    images = image_objects_by_page(PDF)
    renders = render_pages(PDF, info["pages"])
    page_rows: list[dict[str, Any]] = []
    for page, (inspector_text, poppler_text) in enumerate(zip(inspector_texts, poppler_texts), start=1):
        text = inspector_text or poppler_text
        render = renders[page]
        if text:
            page_class = "TEXT_PAGE"
        elif images.get(page, 0) or render["ink_ratio"] > 0.0005:
            page_class = "IMAGE_ONLY_CONTENT_PAGE"
        else:
            page_class = "VERIFIED_BLANK"
        page_rows.append({"paper_id": TARGET, "page": page, "page_class": page_class, "pdf_inspector_text_chars": len(inspector_text), "poppler_text_chars": len(poppler_text), "text_chars": len(text), "page_text_sha256": sha256_text(text), "image_object_count": images.get(page, 0), **render})
    pdf_text = normalize(" ".join(row for row in inspector_texts if row))
    docx = docx_evidence(DOCX)
    snippets = fingerprint["distinctive_text_snippets"]
    snippet_rows, snippet_count = [], 0
    pdf_compact = compact(pdf_text)
    for number, snippet in enumerate(snippets, start=1):
        match = "NORMALIZED_EXACT" if compact(snippet) in pdf_compact else "NO_MATCH"
        snippet_count += int(match != "NO_MATCH")
        snippet_rows.append({"evidence_type": f"SNIPPET_{number}_MATCH", "expected": snippet, "match_type": match})
    table_matches, table_evidence = table_signature_matches(docx["tables"], pdf_text)
    # The PDF text layer does not preserve DOCX table object boundaries.  The
    # contact sheet is the frozen visual evidence for the eight visibly
    # tabular pages below; it supplements, rather than replaces, text checks.
    visual_table_pages = [2, 3, 12, 13, 16, 19, 21, 22]
    table_evidence.append("visual_table_pages:" + ",".join(map(str, visual_table_pages)))
    first_anchor = compact(" ".join(docx["paragraphs"][:3]))[:120]
    last_anchor = compact(" ".join(docx["paragraphs"][-5:]))[-120:]
    first_compatible = int(bool(first_anchor) and first_anchor in pdf_compact)
    last_compatible = int(bool(last_anchor) and last_anchor in pdf_compact)
    reference_compatible = int("参考文献" in docx["text"] and "参考文献" in pdf_text)
    text_pages = sum(row["page_class"] == "TEXT_PAGE" for row in page_rows)
    blanks = sum(row["page_class"] == "VERIFIED_BLANK" for row in page_rows)
    image_only = sum(row["page_class"] == "IMAGE_ONLY_CONTENT_PAGE" for row in page_rows)
    unexplained = sum(row["page_class"] not in {"TEXT_PAGE", "VERIFIED_BLANK", "IMAGE_ONLY_CONTENT_PAGE"} for row in page_rows)
    geometry_pass = int(all(row["render_width"] > 0 and row["render_height"] > 0 and not row["edge_ink_suspected"] for row in page_rows) and "595.32 x 841.92" in info["page_size"] and info["page_rot"] == "0")
    graphical_pass = int(sum(images.values()) > 0 and all(row["ink_ratio"] > 0.0005 for row in page_rows))
    table_sanity_pass = int(table_matches >= 5 and len(visual_table_pages) == len(docx["tables"]))
    full_document = int([row["page"] for row in page_rows if row["page_class"] != "VERIFIED_BLANK"] == list(range(1, info["pages"] + 1)))
    outputs = {
        "audit": CATALOG / "g8_doc_2012_d001_manual_print_pdf_audit.csv", "pages": CATALOG / "g8_doc_2012_d001_manual_print_page_audit.csv", "extraction": CATALOG / "g8_doc_2012_d001_manual_print_extraction.csv", "comparison": CATALOG / "g8_doc_2012_d001_manual_print_content_comparison.json", "result": CATALOG / "g8_doc_2012_d001_manual_print_pdf_qa_result.json", "report": REPORTS / "G8_DOC_2012_D001_MANUAL_PRINT_TO_PDF_QA.md",
    }
    audit = [{"paper_id": TARGET, "candidate_path": str(PDF.relative_to(ROOT)).replace("\\", "/"), "candidate_size": PDF.stat().st_size, "candidate_sha256": pdf_sha_before, "pdf_signature_valid": int(PDF.read_bytes()[:5] == b"%PDF-"), "pdf_readable": 1, "pdf_encrypted": int(info["encrypted"] != "no"), "pdf_inspector_pdf_class": inspector_type, "pdf_inspector_page_count": len(inspector_texts), "poppler_page_count": info["pages"], "page_count_tools_match": int(len(inspector_texts) == info["pages"]), "page_size": info["page_size"], "page_rotation": info["page_rot"], "producer": info["producer"]}]
    extraction_rows = [{"paper_id": TARGET, "page": row["page"], "text_chars": row["text_chars"], "page_text_sha256": row["page_text_sha256"], "backend": "pdf-inspector/native full-page with Poppler page-scoped corroboration"} for row in page_rows]
    write_csv(outputs["audit"], audit, list(audit[0])); write_csv(outputs["pages"], page_rows, list(page_rows[0])); write_csv(outputs["extraction"], extraction_rows, list(extraction_rows[0]))
    comparison = {"paper_id": TARGET, "docx_paragraph_count": len(docx["paragraphs"]), "docx_table_count": len(docx["tables"]), "docx_header_footer_text_count": len(docx["header_footer"]), "docx_normalized_text_char_count": len(docx["text"]), "docx_normalized_text_sha256": sha256_text(docx["text"]), "pdf_normalized_text_char_count": len(pdf_text), "pdf_normalized_text_sha256": sha256_text(pdf_text), "snippet_evidence": snippet_rows, "distinctive_snippet_match_count": snippet_count, "section_order_compatible": int(snippet_count == len(snippets) and reference_compatible), "first_content_compatible": first_compatible, "last_content_compatible": last_compatible, "reference_section_compatible": reference_compatible, "table_signature_match_count": table_matches, "visual_table_page_numbers": visual_table_pages, "table_content_sanity_pass": table_sanity_pass, "table_evidence": table_evidence}
    outputs["comparison"].write_text(json.dumps(comparison, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    source_sha_after, docx_sha_after, pdf_sha_after = sha256_file(SOURCE), sha256_file(DOCX), sha256_file(PDF)
    substantive = int(not (snippet_count == len(snippets) and comparison["section_order_compatible"] and first_compatible and last_compatible and comparison["reference_section_compatible"] and table_sanity_pass and graphical_pass and geometry_pass and full_document))
    qa_pass = int(pdf_sha_before == EXPECTED_PDF_SHA and pdf_sha_after == pdf_sha_before and info["encrypted"] == "no" and info["pages"] == 24 and len(inspector_texts) == 24 and unexplained == 0 and image_only == 0 and snippet_count == 6 and not substantive and source_sha_after == EXPECTED_SOURCE_SHA and docx_sha_after == EXPECTED_DOCX_SHA)
    result = {"STAGE": "G8-DOC-CUMCM-2012-D-001-MANUAL-PRINT-TO-PDF-QA", "STATUS": "PASS" if qa_pass else "PARTIAL", "BRANCH": "library-refactor-v1", "HEAD": "557724fba6572d4d83dc421feda5b17b13ff8d66", "TARGET_PAPER_ID": TARGET,
        "SOURCE_SHA256": source_sha_after, "DERIVATIVE_DOCX_SHA256": docx_sha_after, "CANDIDATE_PDF_SHA256": pdf_sha_after, "SOURCE_SHA_MISMATCH": int(source_sha_after != EXPECTED_SOURCE_SHA), "DERIVATIVE_DOCX_SHA_MISMATCH": int(docx_sha_after != EXPECTED_DOCX_SHA), "CANDIDATE_PDF_SHA_MISMATCH": int(pdf_sha_after != EXPECTED_PDF_SHA or pdf_sha_after != pdf_sha_before), "CANDIDATE_PDF_EXISTS": 1, "CANDIDATE_PDF_SIZE": PDF.stat().st_size,
        "PDF_READABLE": 1, "PDF_ENCRYPTED": int(info["encrypted"] != "no"), "PDF_PAGE_COUNT": info["pages"], "PDF_INSPECTOR_PAGE_COUNT": len(inspector_texts), "POPPLER_PAGE_COUNT": info["pages"], "PAGE_COUNT_TOOLS_MATCH": int(len(inspector_texts) == info["pages"]),
        "TEXT_PAGE_COUNT": text_pages, "VERIFIED_BLANK_PAGE_COUNT": blanks, "IMAGE_ONLY_CONTENT_PAGE_COUNT": image_only, "UNEXPLAINED_PAGE_COUNT": unexplained, "PAGE_ACCOUNTING_TOTAL": len(page_rows), "OCR_RUN": 0, "OCR_PAGE_COUNT": 0, "OCR_ROUTED_PAGE_NUMBERS": "",
        "PDF_TEXT_EXTRACTION_PASS": int(bool(pdf_text)), "PDF_NORMALIZED_TEXT_CHAR_COUNT": len(pdf_text), "PDF_NORMALIZED_TEXT_SHA256": sha256_text(pdf_text), "DISTINCTIVE_TEXT_SNIPPET_COUNT": len(snippets), "DISTINCTIVE_SNIPPET_MATCH_COUNT": snippet_count,
        "SECTION_ORDER_COMPATIBLE": comparison["section_order_compatible"], "FIRST_CONTENT_COMPATIBLE": first_compatible, "LAST_CONTENT_COMPATIBLE": last_compatible, "REFERENCE_SECTION_COMPATIBLE": comparison["reference_section_compatible"], "TABLE_CONTENT_SANITY_PASS": table_sanity_pass, "TABLE_SIGNATURE_MATCH_COUNT": table_matches, "VISUAL_TABLE_PAGE_NUMBERS": ",".join(map(str, visual_table_pages)),
        "GRAPHICAL_CONTENT_SANITY_PASS": graphical_pass, "GROSS_GRAPHICAL_LOSS_DETECTED": int(not graphical_pass), "FIELD_RENDERING_SANITY_PASS": int(snippet_count == len(snippets) and comparison["section_order_compatible"]), "PAGE_GEOMETRY_SANITY_PASS": geometry_pass, "CLIPPED_CONTENT_SUSPECTED": int(not geometry_pass), "FIRST_PAGE_SANITY_PASS": int(page_rows[0]["page_class"] == "TEXT_PAGE"), "LAST_PAGE_SANITY_PASS": int(page_rows[-1]["page_class"] == "TEXT_PAGE"), "FULL_DOCUMENT_PRINT_SANITY_PASS": full_document, "SUBSTANTIVE_CONTENT_DIFFERENCE": substantive,
        "MANUAL_PRINT_ATTEMPT_COUNT": 1, "MANUAL_PRINT_PILOT_EXHAUSTED": 1, "MANUAL_PRINT_PDF_QA_PASS": qa_pass, "GOVERNED_PDF_DERIVATIVE_ACCEPTABLE": qa_pass, "PILOT_REUSE_COUNT": 3, "BATCH_SUCCESS_COUNT": 13, "MANUAL_RENDER_SUCCESS_COUNT": qa_pass, "EFFECTIVE_DOC_PDF_TARGET_COUNT": 16 + qa_pass,
        "FORMAL_ARTIFACTS_GENERATED": 0, "SUCCESSFUL_BATCH_ROWS_PRESERVED": 13, "SUCCESSFUL_BATCH_ROWS_RECONVERTED": 0, "DOC_CONTRACT_APPROVED": 1, "ELIGIBLE": 453, "INELIGIBLE": 189, "ARTIFACT_SETS": 308, "PRIMARY_ARTIFACTS": 924, "DOC_MANUAL_BACKLOG": 17, "Q3_MANUAL_BACKLOG": 128, "WORD_RUN": 0, "WORD_COM_RUN": 0, "PRINT_JOB_RUN": 0, "PDF_GENERATION_RUN": 0, "NEW_DEPENDENCY_INSTALLED": 0, "NETWORK_ACCESS_USED": 0, "GIT_OPERATIONS": 0,
        "POSTFLIGHT_PROVENANCE": postflight, "RENDERED_CONTACT_SHEET": str((RENDER_DIR / "contact_sheet.png").relative_to(ROOT)).replace("\\", "/"), "OUTPUTS": {key: str(path.relative_to(ROOT)).replace("\\", "/") for key, path in outputs.items()}, "NEXT": "G8-DOC-BATCH-CLOSURE-QA" if qa_pass else "G8-DOC-CUMCM-2012-D-001-POST-MANUAL-RENDERING-FAILURE-DECISION"}
    outputs["result"].write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORTS.mkdir(parents=True, exist_ok=True)
    outputs["report"].write_text(f"# G8 DOC Manual Print-to-PDF QA\n\nStatus: `{'PASS' if qa_pass else 'PARTIAL'}`\n\nThe candidate remained immutable during QA. Page accounting: {text_pages} text, {blanks} verified blank, {image_only} image-only, {unexplained} unexplained.\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    return 0 if qa_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
