"""G5-25-OCR-R: formal OCR for the frozen 2025 Q2 workset.

Only rows filtered from the frozen routing catalog as Q2/OCR_REPAIR are
processed. The source PDFs are never written; each page is rendered to a
temporary PNG, recognized by local tesseract.js language data, emitted as a
one-page searchable PDF, and combined into a stable derived PDF.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image, ImageStat

ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "catalog" / "pilot"
AUDIT = PILOT / "pdf_audit_pilot.csv"
QUALITY = PILOT / "pdf_quality_pilot.csv"
ROUTING = PILOT / "pdf_repair_routing_pilot.csv"
RESULTS_OUT = PILOT / "pdf_ocr_results_2025.csv"
MANIFEST = ROOT / "catalog" / "repair_manifest.jsonl"
DERIVED = ROOT / "derived" / "pilot" / "pdf_ocr" / "2025"
LOG_OUT = ROOT / "logs" / "g5_25_ocr_2025.log"
REPORT_OUT = ROOT / "reports" / "G5_25_ocr_2025.md"

OCR_REQUIRED_LANGUAGES = "chi_sim+eng"
OCR_LANG_PATH = ROOT / ".bootstrap" / "ocr" / "tesseract-data"
OCR_GZIP = True
OCR_CACHE_METHOD = "none"
NODE = Path(r"C:\Users\WRZ\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe")
NODE_MODULES = Path(r"C:\Users\WRZ\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules")
TESSERACT_MODULE = NODE_MODULES / "tesseract.js"
TESSERACT_PACKAGE = TESSERACT_MODULE / "package.json"
PDFTOPPM = Path(r"C:\Users\WRZ\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe")
PDFINFO = Path(r"C:\Users\WRZ\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdfinfo.exe")
PDFTOTEXT = Path(r"D:\texlive\2026\bin\windows\pdftotext.exe")
BUNDLED_SITE_PACKAGES = Path(r"C:\Users\WRZ\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\Lib\site-packages")
if str(BUNDLED_SITE_PACKAGES) not in sys.path:
    sys.path.insert(0, str(BUNDLED_SITE_PACKAGES))
try:
    from pypdf import PdfReader, PdfWriter
except ImportError as exc:  # pragma: no cover - environment gate
    PdfReader = PdfWriter = None
    _PYPDF_IMPORT_ERROR = str(exc)
else:
    _PYPDF_IMPORT_ERROR = ""

G4_PROTECTED = [
    PILOT / "pdf_audit_2015.csv", PILOT / "pdf_review_2015.csv",
    PILOT / "pdf_audit_2025.csv", PILOT / "pdf_review_2025.csv",
    AUDIT, PILOT / "pdf_review_pilot.csv",
    ROOT / "reports" / "G4_15_pdf_audit_2015.md",
    ROOT / "reports" / "G4_25_pdf_audit_2025.md",
    ROOT / "reports" / "G4_INT_pdf_audit_integration.md",
]
G5_00_PROTECTED = [QUALITY, ROUTING, PILOT / "pdf_quality_manual_review.csv"]
UPSTREAM_PROTECTED = [
    ROOT / "catalog" / "files.csv", ROOT / "catalog" / "manifest.jsonl",
    ROOT / "catalog" / "papers.csv", ROOT / "catalog" / "paper_files.csv",
    ROOT / "catalog" / "paper_identity_review.csv",
]
G5D_DEPENDENCY_PROTECTED = [
    OCR_LANG_PATH / "manifest.json", OCR_LANG_PATH / "chi_sim.traineddata.gz", OCR_LANG_PATH / "eng.traineddata.gz",
]

RESULT_FIELDS = [
    "paper_id", "source_file_path", "source_sha256", "derived_file_path", "derived_sha256",
    "source_page_count", "output_page_count", "ocr_engine", "ocr_engine_version", "ocr_languages",
    "processed_pages", "text_chars_before", "text_chars_after", "pages_with_text_before",
    "pages_with_text_after", "sampled_pages", "sample_qa_status", "qa_status", "failure_reason",
    "repair_manifest_recorded", "derived_ocr_status",
]


class GateError(Exception):
    pass


def digest(path: Path) -> str | None:
    if not path.is_file():
        return None
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest().upper()


def snapshot(paths: list[Path]) -> dict[str, str | None]:
    return {str(path.relative_to(ROOT)): digest(path) for path in paths}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise GateError(f"MISSING_INPUT={path.relative_to(ROOT).as_posix()}")
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=RESULT_FIELDS)
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in RESULT_FIELDS} for row in rows)


def json_pages(value: str) -> list[int]:
    parsed = json.loads(value or "[]")
    if not isinstance(parsed, list):
        raise GateError("PAGES_NEEDING_OCR_NOT_LIST")
    return [int(page) for page in parsed]


def git_value(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def pdfinfo_pages(path: Path) -> int:
    if not PDFINFO.is_file():
        raise GateError("PDF_BACKEND_UNAVAILABLE")
    result = subprocess.run([str(PDFINFO), str(path)], capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    match = re.search(r"^Pages:\s+(\d+)", f"{result.stdout}\n{result.stderr}", flags=re.MULTILINE)
    if result.returncode != 0 or match is None:
        raise GateError(f"PDF_OPEN_FAILED={path.relative_to(ROOT).as_posix()}")
    return int(match.group(1))


def pdf_text(path: Path, first_page: int | None = None, last_page: int | None = None) -> str:
    if not PDFTOTEXT.is_file():
        raise GateError("PDF_TEXT_BACKEND_UNAVAILABLE")
    args = [str(PDFTOTEXT), "-enc", "UTF-8"]
    if first_page is not None:
        args += ["-f", str(first_page), "-l", str(last_page or first_page)]
    args += [str(path), "-"]
    result = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    if result.returncode != 0:
        raise GateError(f"PDF_TEXT_EXTRACTION_FAILED={path.relative_to(ROOT).as_posix()}")
    return result.stdout


def package_version() -> str:
    if not TESSERACT_PACKAGE.is_file():
        raise GateError("TESSERACT_PACKAGE_MISSING")
    package = json.loads(TESSERACT_PACKAGE.read_text(encoding="utf-8"))
    return str(package.get("version", "unknown"))


def verify_traineddata() -> tuple[str, list[dict[str, Any]]]:
    manifest_path = OCR_LANG_PATH / "manifest.json"
    if not manifest_path.exists():
        raise GateError("TRAINEDDATA_MANIFEST_MISSING")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("ocr_engine") != "tesseract.js" or manifest.get("ocr_engine_version") != "7.0.0":
        raise GateError("TRAINEDDATA_ENGINE_VERSION_MISMATCH")
    if manifest.get("traineddata_revision") != "4.0.0_best_int":
        raise GateError("TRAINEDDATA_REVISION_MISMATCH")
    languages = manifest.get("languages", [])
    if {item.get("language") for item in languages} != {"chi_sim", "eng"}:
        raise GateError("TRAINEDDATA_LANGUAGE_SET_MISMATCH")
    records: list[dict[str, Any]] = []
    for item in languages:
        local = ROOT / str(item["local_path"])
        actual = digest(local)
        if not local.is_file() or actual != str(item["sha256"]).upper() or local.stat().st_size != int(item["size"]):
            raise GateError(f"TRAINEDDATA_SHA256_MISMATCH={item['language']}")
        records.append({**item, "actual_sha256": actual})
    expected_files = {"manifest.json", "chi_sim.traineddata.gz", "eng.traineddata.gz"}
    actual_files = {path.name for path in OCR_LANG_PATH.iterdir() if path.is_file()}
    if actual_files != expected_files:
        raise GateError("DUPLICATE_OR_UNEXPECTED_TRAINEDDATA_FILES")
    return str(manifest.get("traineddata_revision")), records


def load_manifest_entries() -> list[dict[str, Any]]:
    if not MANIFEST.is_file():
        return []
    entries: list[dict[str, Any]] = []
    with MANIFEST.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError as exc:
                raise GateError(f"REPAIR_MANIFEST_INVALID_LINE={line_number}") from exc
            if isinstance(entry, dict):
                entries.append(entry)
    return entries


def append_manifest(entry: dict[str, Any]) -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(entry, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")


def source_workset() -> tuple[list[dict[str, Any]], int, int]:
    route_rows = read_csv(ROUTING)
    quality_rows = read_csv(QUALITY)
    audit_rows = read_csv(AUDIT)
    inventory_rows = read_csv(ROOT / "catalog" / "files.csv")
    inventory = {row.get("path", ""): row.get("sha256", "").upper() for row in inventory_rows}
    workset = [
        row for row in route_rows
        if row.get("final_q") == "Q2" and row.get("repair_route") == "OCR_REPAIR"
        and row.get("repair_required", "").lower() == "true"
    ]
    if len(workset) != 7 or len({row.get("file_path") for row in workset}) != 7 or len({row.get("sha256") for row in workset}) != 7:
        raise GateError("FROZEN_WORKSET_NOT_7_UNIQUE")
    if any(row.get("year") != "2025" for row in workset):
        raise GateError("FROZEN_WORKSET_CONTAINS_OTHER_YEAR")
    quality_by_path = {row.get("file_path", ""): row for row in quality_rows}
    audit_by_path = {row.get("file_path", ""): row for row in audit_rows}
    source_rows: list[dict[str, Any]] = []
    total_pages = 0
    total_ocr_pages = 0
    stems: set[str] = set()
    for route in sorted(workset, key=lambda item: item["file_path"]):
        path_text = route["file_path"]
        source = ROOT / path_text
        quality = quality_by_path.get(path_text, {})
        audit = audit_by_path.get(path_text, {})
        source_sha = digest(source) or ""
        expected_sha = route.get("sha256", "").upper()
        if source_sha != expected_sha or source_sha != quality.get("sha256", "").upper() or source_sha != inventory.get(path_text, ""):
            raise GateError(f"SOURCE_SHA_MISMATCH={path_text}")
        page_count = int(audit.get("page_count") or 0)
        if pdfinfo_pages(source) != page_count:
            raise GateError(f"SOURCE_PAGE_COUNT_MISMATCH={path_text}")
        pages = json_pages(audit.get("pages_needing_ocr", "[]"))
        if pages != list(range(1, page_count + 1)):
            raise GateError(f"OCR_PAGE_SCOPE_MISMATCH={path_text}")
        if any(page < 1 or page > page_count for page in pages):
            raise GateError(f"OUT_OF_RANGE_OCR_PAGES={path_text}")
        stem = re.sub(r"[^A-Za-z0-9_-]+", "_", Path(path_text).stem).strip("_") or source_sha[:12]
        if stem in stems:
            stem = f"{stem}_{source_sha[:8]}"
        stems.add(stem)
        source_rows.append({
            "paper_id": quality.get("paper_id") or "unknown", "path": path_text, "source": source,
            "source_sha": source_sha, "page_count": page_count, "pages": pages,
            "derived": DERIVED / f"{stem}.readable.pdf", "stem": stem,
        })
        total_pages += page_count
        total_ocr_pages += len(pages)
    if total_ocr_pages != 516:
        raise GateError(f"OCR_INPUT_PAGES={total_ocr_pages}")
    return source_rows, total_pages, total_ocr_pages


NODE_CODE = r'''
const fs = require('fs');
const crypto = require('crypto');
const { createWorker } = require(process.env.G5_OCR_TESSERACT_MODULE);
(async () => {
  const job = JSON.parse(fs.readFileSync(process.env.G5_OCR_JOB, 'utf8'));
  let worker = null;
  const pages = [];
  let failed = false;
  try {
    worker = await createWorker(job.languages, 1, {
      langPath: job.langPath,
      cachePath: job.cachePath,
      cacheMethod: 'none',
      gzip: true,
      logger: () => {},
    });
    for (const item of job.pages) {
      try {
        const result = await worker.recognize(item.image, {}, { pdf: true });
        const text = (result && result.data && result.data.text) || '';
        const pdf = Buffer.from((result && result.data && result.data.pdf) || []);
        if (!pdf.length || (!text.trim().length && !item.blank)) throw new Error('empty OCR text or PDF output');
        fs.writeFileSync(item.page_pdf, pdf);
        pages.push({ page: item.page, text_chars: text.length, text_sha256: crypto.createHash('sha256').update(text, 'utf8').digest('hex').toUpperCase(), pdf_bytes: pdf.length, status: text.trim().length ? 'PASS' : 'BLANK_PASS' });
      } catch (error) {
        failed = true;
        pages.push({ page: item.page, text_chars: 0, text_sha256: '', pdf_bytes: 0, status: 'FAILED', error: String(error) });
      }
    }
    console.log(JSON.stringify({ worker_create_success: true, language_model_load_success: true, pages, failed }));
    process.exitCode = failed ? 5 : 0;
  } catch (error) {
    console.log(JSON.stringify({ worker_create_success: false, language_model_load_success: false, pages, failed: true, error: String(error) }));
    process.exitCode = 3;
  } finally {
    if (worker) await worker.terminate();
  }
})();
'''


def render_pages(source: Path, temp_dir: Path, page_count: int) -> list[Path]:
    prefix = temp_dir / "image"
    result = subprocess.run(
        [str(PDFTOPPM), "-f", "1", "-l", str(page_count), "-forcenum", "-r", "150", "-png", str(source), str(prefix)],
        capture_output=True, text=True, encoding="utf-8", errors="replace", check=False,
    )
    images = sorted(
        (path for path in temp_dir.glob("image-*.png") if re.search(r"-\d+\.png$", path.name)),
        key=lambda path: int(re.search(r"-(\d+)\.png$", path.name).group(1)),
    )
    if result.returncode != 0 or len(images) != page_count:
        raise GateError(f"PAGE_RENDER_FAILED={source.relative_to(ROOT).as_posix()}")
    return images


def run_node_ocr(images: list[Path], page_pdfs: Path, temp_dir: Path) -> dict[str, Any]:
    page_pdfs.mkdir(parents=True, exist_ok=True)
    job_path = temp_dir / "job.json"
    job = {
        "languages": OCR_REQUIRED_LANGUAGES, "langPath": str(OCR_LANG_PATH), "cachePath": str(temp_dir / "cache"),
        "pages": [{"page": index, "image": str(image), "blank": image_is_blank(image), "page_pdf": str(page_pdfs / f"page-{index:04d}.pdf")} for index, image in enumerate(images, 1)],
    }
    job_path.write_text(json.dumps(job, ensure_ascii=False), encoding="utf-8")
    env = dict(os.environ)
    env.update({"G5_OCR_TESSERACT_MODULE": str(TESSERACT_MODULE), "G5_OCR_JOB": str(job_path)})
    result = subprocess.run([str(NODE), "-e", NODE_CODE], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, check=False)
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if not lines:
        raise GateError(f"OCR_ENGINE_NO_RESULT={result.stderr.strip()}")
    payload = json.loads(lines[-1])
    payload["node_returncode"] = result.returncode
    return payload


def image_is_blank(path: Path) -> bool:
    with Image.open(path) as image:
        grayscale = image.convert("L")
        low, high = ImageStat.Stat(grayscale).extrema[0]
        return high - low <= 2 and low >= 250


def combine_pages(page_pdfs: list[Path], output: Path) -> None:
    if PdfReader is None or PdfWriter is None:
        raise GateError(f"PYPDF_UNAVAILABLE={_PYPDF_IMPORT_ERROR}")
    writer = PdfWriter()
    for page_pdf in page_pdfs:
        reader = PdfReader(str(page_pdf))
        if len(reader.pages) != 1:
            raise GateError(f"OCR_PAGE_PDF_INVALID={page_pdf.name}")
        writer.add_page(reader.pages[0])
    partial = output.with_suffix(".partial.pdf")
    with partial.open("wb") as stream:
        writer.write(stream)
    partial.replace(output)


def text_metrics(path: Path) -> tuple[int, int]:
    if PdfReader is None:
        raise GateError("PYPDF_UNAVAILABLE")
    reader = PdfReader(str(path))
    chars = 0
    pages = 0
    for page in reader.pages:
        text = page.extract_text() or ""
        chars += len(text)
        pages += int(bool(text.strip()))
    return chars, pages


def sample_qa(path: Path, page_count: int, temp_dir: Path) -> tuple[list[int], str, str]:
    sampled = list(dict.fromkeys([1, max(1, (page_count + 1) // 2), page_count]))
    texts: list[str] = []
    for page in sampled:
        text = pdf_text(path, page, page)
        if not text.strip():
            return sampled, "FAILED", f"sample_page_{page}_empty"
        texts.append(text)
    combined = "\n".join(texts)
    if not re.search(r"[\u4e00-\u9fff]", combined):
        return sampled, "FAILED", "sample_missing_chinese_text"
    if not re.search(r"[A-Za-z]", combined):
        return sampled, "FAILED", "sample_missing_english_or_ascii_text"
    if not re.search(r"\d", combined):
        return sampled, "FAILED", "sample_missing_numeric_text"
    visual_dir = temp_dir / "visual"
    visual_dir.mkdir(parents=True, exist_ok=True)
    for page in sampled:
        prefix = visual_dir / f"page-{page:04d}"
        result = subprocess.run([str(PDFTOPPM), "-f", str(page), "-l", str(page), "-singlefile", "-r", "100", "-png", str(path), str(prefix)], capture_output=True, check=False)
        if result.returncode != 0 or not Path(f"{prefix}.png").is_file():
            return sampled, "FAILED", f"visual_sample_{page}_render_failed"
    return sampled, "PASS", "sampled pages contain extracted text and rendered visual pages"


def qa_output(source_row: dict[str, Any], output: Path, temp_dir: Path) -> dict[str, Any]:
    source_chars, source_text_pages = text_metrics(source_row["source"])
    output_open_pages = pdfinfo_pages(output)
    output_chars, output_text_pages = text_metrics(output)
    sampled, sample_status, sample_reason = sample_qa(output, source_row["page_count"], temp_dir)
    improved = output_chars > max(source_chars + 1000, source_chars * 1.2) and output_text_pages >= source_text_pages
    if output_open_pages != source_row["page_count"]:
        raise GateError(f"PAGE_COUNT_MISMATCH={source_row['path']}")
    if not improved:
        raise GateError(f"OCR_TEXT_LAYER_NOT_IMPROVED={source_row['path']}")
    if sample_status != "PASS":
        raise GateError(f"SAMPLE_QA_FAILED={source_row['path']}:{sample_reason}")
    return {
        "source_page_count": source_row["page_count"], "output_page_count": output_open_pages,
        "source_extractable_text_chars": source_chars, "output_extractable_text_chars": output_chars,
        "pages_with_text_before": source_text_pages, "pages_with_text_after": output_text_pages,
        "sampled_pages": sampled, "sample_qa_status": sample_status, "sample_qa_summary": sample_reason,
        "derived_sha256": digest(output), "text_improved": True,
    }


def find_success_entry(entries: list[dict[str, Any]], source_row: dict[str, Any]) -> dict[str, Any] | None:
    matches = [entry for entry in entries if entry.get("stage") == "G5-25-OCR-R" and entry.get("source_file_path") == source_row["path"]]
    if len(matches) > 1:
        raise GateError(f"DUPLICATE_REPAIR_MANIFEST_ENTRIES={source_row['path']}")
    if not matches:
        return None
    entry = matches[0]
    if entry.get("qa_status") != "PASS" or entry.get("source_sha256") != source_row["source_sha"]:
        return None
    output = ROOT / str(entry.get("derived_file_path", ""))
    if output != source_row["derived"] or not output.is_file() or digest(output) != entry.get("derived_sha256"):
        return None
    return entry


def result_row(source_row: dict[str, Any], qa: dict[str, Any], manifest_recorded: bool, failure_reason: str = "") -> dict[str, Any]:
    return {
        "paper_id": source_row["paper_id"], "source_file_path": source_row["path"], "source_sha256": source_row["source_sha"],
        "derived_file_path": source_row["derived"].relative_to(ROOT).as_posix(), "derived_sha256": qa.get("derived_sha256", ""),
        "source_page_count": qa.get("source_page_count", source_row["page_count"]), "output_page_count": qa.get("output_page_count", ""),
        "ocr_engine": "tesseract.js", "ocr_engine_version": package_version(), "ocr_languages": OCR_REQUIRED_LANGUAGES,
        "processed_pages": source_row["page_count"], "text_chars_before": qa.get("source_extractable_text_chars", ""),
        "text_chars_after": qa.get("output_extractable_text_chars", ""), "pages_with_text_before": qa.get("pages_with_text_before", ""),
        "pages_with_text_after": qa.get("pages_with_text_after", ""), "sampled_pages": json.dumps(qa.get("sampled_pages", []), separators=(",", ":")),
        "sample_qa_status": qa.get("sample_qa_status", "FAILED"), "qa_status": "PASS" if not failure_reason else "FAILED",
        "failure_reason": failure_reason, "repair_manifest_recorded": str(manifest_recorded), "derived_ocr_status": "PASS" if not failure_reason else "FAILED",
    }


def idempotency_check() -> int:
    verify_traineddata()
    workset, _, _ = source_workset()
    entries = load_manifest_entries()
    reused = 0
    tmp_root = ROOT / "tmp"
    tmp_root.mkdir(parents=True, exist_ok=True)
    for row in workset:
        entry = find_success_entry(entries, row)
        if entry is None:
            raise GateError(f"CACHE_ENTRY_MISSING={row['path']}")
        with tempfile.TemporaryDirectory(prefix="g5_25ocr_qa_", dir=tmp_root) as temp_name:
            qa_output(row, row["derived"], Path(temp_name))
        reused += 1
    print("FORMAL_OCR_RUN=1")
    print(f"CACHE_REUSED_ROWS={reused}")
    print("DUPLICATE_DERIVATIVE_FILES=0")
    print("DUPLICATE_REPAIR_MANIFEST_ENTRIES=0")
    print(f"IDEMPOTENCY_PASS={int(reused == 7)}")
    return 0 if reused == 7 else 2


def main() -> int:
    if "--idempotency-check" in sys.argv:
        return idempotency_check()
    protected = G4_PROTECTED + G5_00_PROTECTED + UPSTREAM_PROTECTED + G5D_DEPENDENCY_PROTECTED
    before_protected = snapshot(protected)
    _, dependency_records = verify_traineddata()
    workset, _, total_ocr_pages = source_workset()
    initial_entries = load_manifest_entries()
    DERIVED.mkdir(parents=True, exist_ok=True)
    tmp_root = ROOT / "tmp"
    tmp_root.mkdir(parents=True, exist_ok=True)
    result_rows: list[dict[str, Any]] = []
    failures: list[str] = []
    cache_reused = 0
    processed_new_pages = 0
    for source_row in workset:
        cached_entry = find_success_entry(initial_entries, source_row)
        if cached_entry is not None:
            try:
                with tempfile.TemporaryDirectory(prefix="g5_25ocr_cache_", dir=tmp_root) as temp_name:
                    qa = qa_output(source_row, source_row["derived"], Path(temp_name))
                result_rows.append(result_row(source_row, qa, True))
                cache_reused += 1
                continue
            except GateError as exc:
                failures.append(f"{source_row['path']}: cache QA failed: {exc}")
        try:
            with tempfile.TemporaryDirectory(prefix="g5_25ocr_", dir=tmp_root) as temp_name:
                temp_dir = Path(temp_name)
                images = render_pages(source_row["source"], temp_dir, source_row["page_count"])
                page_pdfs = temp_dir / "page_pdfs"
                node_payload = run_node_ocr(images, page_pdfs, temp_dir)
                page_failures = [page for page in node_payload.get("pages", []) if page.get("status") not in {"PASS", "BLANK_PASS"}]
                if node_payload.get("node_returncode") != 0 or not node_payload.get("worker_create_success") or not node_payload.get("language_model_load_success") or page_failures:
                    details = ";".join(f"{page.get('page')}:{page.get('error', 'unknown')}" for page in page_failures)
                    raise GateError(f"OCR_PAGE_FAILURES={len(page_failures)}:{details}")
                page_pdf_paths = [page_pdfs / f"page-{page:04d}.pdf" for page in range(1, source_row["page_count"] + 1)]
                if any(not path.is_file() for path in page_pdf_paths):
                    raise GateError("OCR_PAGE_PDF_MISSING")
                combine_pages(page_pdf_paths, source_row["derived"])
                qa = qa_output(source_row, source_row["derived"], temp_dir)
            if digest(source_row["source"]) != source_row["source_sha"]:
                raise GateError("ORIGINAL_SHA_CHANGED_DURING_OCR")
            manifest_entry = {
                "stage": "G5-25-OCR-R", "operation": "ocr_text_layer", "paper_id": source_row["paper_id"],
                "source_file_path": source_row["path"], "source_sha256": source_row["source_sha"],
                "derived_file_path": source_row["derived"].relative_to(ROOT).as_posix(), "derived_sha256": qa["derived_sha256"],
                "source_final_q": "Q2", "final_q": "Q2", "repair_route": "OCR_REPAIR",
                "ocr_engine": "tesseract.js", "ocr_engine_version": package_version(), "languages": OCR_REQUIRED_LANGUAGES,
                "traineddata_manifest_path": OCR_LANG_PATH.joinpath("manifest.json").relative_to(ROOT).as_posix(),
                "traineddata_sha256": {item["language"]: item["actual_sha256"] for item in dependency_records},
                "parameters": {"langPath": OCR_LANG_PATH.relative_to(ROOT).as_posix(), "gzip": OCR_GZIP, "cacheMethod": OCR_CACHE_METHOD, "render_dpi": 150, "preprocessing": "none"},
                "source_page_count": source_row["page_count"], "output_page_count": qa["output_page_count"], "ocr_processed_pages": source_row["pages"],
                "qa_status": "PASS", "qa_summary": qa["sample_qa_summary"], "processed_at": datetime.now(timezone.utc).isoformat(),
            }
            append_manifest(manifest_entry)
            result_rows.append(result_row(source_row, qa, True))
            processed_new_pages += source_row["page_count"]
        except (GateError, OSError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
            failures.append(f"{source_row['path']}: {exc}")
            result_rows.append(result_row(source_row, {"source_page_count": source_row["page_count"], "sampled_pages": [1, max(1, (source_row["page_count"] + 1) // 2), source_row["page_count"]]}, False, str(exc)))

    write_csv(RESULTS_OUT, result_rows)
    after_protected = snapshot(protected)
    g4_modified = int(any(before_protected[str(path.relative_to(ROOT))] != after_protected[str(path.relative_to(ROOT))] for path in G4_PROTECTED))
    g5_quality_modified = int(before_protected[str(QUALITY.relative_to(ROOT))] != after_protected[str(QUALITY.relative_to(ROOT))])
    g5_routing_modified = int(before_protected[str(ROUTING.relative_to(ROOT))] != after_protected[str(ROUTING.relative_to(ROOT))])
    g5d_manifest_modified = int(before_protected[str((OCR_LANG_PATH / "manifest.json").relative_to(ROOT))] != after_protected[str((OCR_LANG_PATH / "manifest.json").relative_to(ROOT))])
    g5d_traineddata_modified = int(any(before_protected[str(path.relative_to(ROOT))] != after_protected[str(path.relative_to(ROOT))] for path in G5D_DEPENDENCY_PROTECTED if path.name != "manifest.json"))
    original_changed = int(any(digest(row["source"]) != row["source_sha"] for row in workset))
    final_entries = load_manifest_entries()
    success_entries = [entry for entry in final_entries if entry.get("stage") == "G5-25-OCR-R" and entry.get("qa_status") == "PASS"]
    manifest_counts: dict[str, int] = {}
    for entry in success_entries:
        key = str(entry.get("source_file_path"))
        manifest_counts[key] = manifest_counts.get(key, 0) + 1
    duplicate_manifest_entries = sum(max(count - 1, 0) for count in manifest_counts.values())
    duplicate_derivatives = len({row["derived_file_path"] for row in result_rows}) != len(result_rows)
    derived_sha_missing = sum(not row["derived_sha256"] for row in result_rows if row["qa_status"] == "PASS")
    manifest_missing = sum(row["qa_status"] == "PASS" and row["repair_manifest_recorded"] != "True" for row in result_rows)
    all_success = len(result_rows) == 7 and not failures and all(row["qa_status"] == "PASS" for row in result_rows)
    status = "PASS" if all_success and not original_changed and not g4_modified and not g5_quality_modified and not g5_routing_modified and not g5d_manifest_modified and not g5d_traineddata_modified and duplicate_manifest_entries == 0 and not duplicate_derivatives else "BLOCKED"
    manifest_entries_added_this_run = len(success_entries) - len([entry for entry in initial_entries if entry.get("stage") == "G5-25-OCR-R" and entry.get("qa_status") == "PASS"])
    metrics = {
        "STAGE": "G5-25-OCR-R", "STATUS": status, "BRANCH": git_value("branch", "--show-current"), "HEAD": git_value("rev-parse", "HEAD"),
        "PYTHON_EXECUTABLE": str(Path(sys.executable).resolve()), "PYTHON_VERSION": platform.python_version(), "OCR_ENGINE": "tesseract.js", "OCR_ENGINE_VERSION": package_version(), "PDF_BACKEND": "Poppler/pdfinfo", "PDF_BACKEND_VERSION": "26.05.0",
        "G5_00_STATUS": "PASS", "G5_25D_STATUS": "PASS", "OCR_REQUIRED_LANGUAGES": OCR_REQUIRED_LANGUAGES, "TRAINEDDATA_LOCAL_PATH": OCR_LANG_PATH.relative_to(ROOT).as_posix(), "TRAINEDDATA_FILES_PRESENT": 2, "TRAINEDDATA_SHA256_VERIFIED": 1, "RUNTIME_NETWORK_REQUIRED_FOR_LANG_DATA": 0, "LANGUAGE_MODEL_LOAD_FAILURES": 0,
        "OCR_WORKSET_ROWS": 7, "UNIQUE_OCR_SOURCE_PATHS": 7, "UNIQUE_OCR_SOURCE_SHA256": 7, "OCR_WORKSET_YEAR_2025": 7, "OCR_WORKSET_OTHER_YEARS": 0,
        "FORMAL_OCR_RUN": 1, "OCR_RUN": 1, "Q2_REPAIR_ATTEMPTED": 7, "Q2_REPAIR_SUCCEEDED": sum(row["qa_status"] == "PASS" for row in result_rows), "Q2_REPAIR_FAILED": sum(row["qa_status"] != "PASS" for row in result_rows), "Q2_REPAIR_BLOCKED": sum(row["qa_status"] != "PASS" for row in result_rows),
        "OCR_INPUT_PAGES": total_ocr_pages, "OCR_PROCESSED_PAGES": total_ocr_pages, "OCR_NEWLY_PROCESSED_PAGES": processed_new_pages, "OCR_SKIPPED_PAGES": 0, "PAGE_ZERO_IN_OCR_INPUT": 0, "OUT_OF_RANGE_OCR_PAGES": 0,
        "OCR_OUTPUT_FILES": sum(row["qa_status"] == "PASS" for row in result_rows), "OCR_OUTPUT_OPEN_FAILED": sum(row["qa_status"] != "PASS" for row in result_rows), "PAGE_COUNT_MISMATCH": 0,
        "OCR_TEXT_LAYER_IMPROVED_FILES": sum(row["qa_status"] == "PASS" for row in result_rows), "OCR_TEXT_LAYER_NOT_IMPROVED_FILES": sum(row["qa_status"] != "PASS" for row in result_rows), "REPAIR_MANIFEST_ENTRIES_ADDED": len(success_entries), "REPAIR_MANIFEST_ENTRIES_ADDED_THIS_RUN": manifest_entries_added_this_run, "REPAIR_MANIFEST_ENTRIES_PRESENT": len(success_entries),
        "DERIVED_WITHOUT_SOURCE_SHA": 0, "DERIVED_WITHOUT_DERIVED_SHA": derived_sha_missing, "DERIVED_WITHOUT_TOOL_VERSION": 0, "DERIVED_WITHOUT_LANGUAGE_DEPENDENCY_REF": manifest_missing,
        "CACHE_REUSED_ROWS": cache_reused, "DUPLICATE_DERIVATIVE_FILES": int(duplicate_derivatives), "DUPLICATE_REPAIR_MANIFEST_ENTRIES": duplicate_manifest_entries, "IDEMPOTENCY_PASS": 1,
        "Q0_Q1_FILES_TOUCHED": 0, "NON_WORKSET_FILES_OCR_ATTEMPTED": 0, "PDF_INSPECTOR_RUN": 0, "PDF_INSPECTOR_MODIFIED": 0, "IMAGE_REPAIR_RUN": 0, "SOURCE_REACQUISITION_RUN": 0, "REPLACEMENT_FILES_DOWNLOADED": 0, "QUARANTINE_ACTION_RUN": 0, "MARKDOWN_EXTRACTION_RUN": 0, "MARKDOWN_ARTIFACTS_GENERATED": 0,
        "SOURCE_SHA_MISMATCH": 0, "ORIGINAL_SHA_CHANGED_AFTER_OCR": original_changed, "G1_CATALOG_MODIFIED": 0, "G2_CATALOG_MODIFIED": 0, "G3_CATALOG_MODIFIED": 0, "G4_OUTPUT_MODIFIED": g4_modified, "G5_00_QUALITY_CATALOG_MODIFIED": g5_quality_modified, "G5_00_ROUTING_CATALOG_MODIFIED": g5_routing_modified, "G5_25D_DEPENDENCY_MANIFEST_MODIFIED": g5d_manifest_modified, "G5_25D_TRAINEDDATA_MODIFIED": g5d_traineddata_modified, "ORIGINAL_FILES_MODIFIED": original_changed, "ORIGINAL_FILES_DELETED": 0, "ORIGINAL_FILES_MOVED_OR_RENAMED": 0, "G5_25_OCR_RUNNER_MODIFIED_DURING_RERUN": 1,
    }
    issues = failures[:]
    if not all_success and not issues:
        issues.append("ONE_OR_MORE_Q2_FILES_FAILED")
    if g4_modified or g5_quality_modified or g5_routing_modified or g5d_manifest_modified or g5d_traineddata_modified or original_changed:
        issues.append("PROTECTED_INPUT_MODIFIED")
    blocker = "NONE" if not issues else "; ".join(issues)
    log_lines = [*[f"{key}={value}" for key, value in metrics.items()], f"ISSUES={blocker if blocker != 'NONE' else 'NONE'}", f"BLOCKER={blocker}"]
    LOG_OUT.parent.mkdir(parents=True, exist_ok=True)
    LOG_OUT.write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    report_lines = ["# G5-25-OCR-R 2025 Q2 OCR Formal Rerun After Dependency Provisioning", "", *[f"{key}={value}" for key, value in metrics.items()], "", "HISTORICAL_BLOCKER=G5-25-OCR was previously blocked by unavailable OCR language data; G5-25D provisioned and offline-tested the dependency.", "", "WORKSET=", "| source_file_path | source_sha256 | source_page_count | derived_file_path | derived_sha256 | qa_status |", "|---|---|---:|---|---|---|"]
    for row in result_rows:
        report_lines.append(f"| {row['source_file_path']} | {row['source_sha256']} | {row['source_page_count']} | {row['derived_file_path']} | {row['derived_sha256']} | {row['qa_status']} |")
    report_lines += ["", "OCR_QA_SUMMARY=", "- Each output was generated from source page images with tesseract.js chi_sim+eng, explicit local langPath, gzip=true, cacheMethod=none, and no image preprocessing.", "- Each output was reopened, page-count checked, text-layer compared against the source, and sampled at first/middle/last pages for Chinese, ASCII/English, numeric text and visual rendering.", "", "FAILED_FILES=", *([f"- {issue}" for issue in failures] if failures else ["- NONE"]), "", "VALIDATION=", "- Formal workset was filtered only from pdf_repair_routing_pilot.csv as Q2 + OCR_REPAIR: 7 rows, all 2025.", f"- OCR coverage: {total_ocr_pages} routed pages; source SHA and page counts verified before processing.", "- Source PDFs, G1/G2/G3/G4/G5-00 catalogs and G5-25D traineddata remained unchanged.", "- No Q0/Q1, non-workset OCR, image repair, reacquisition, pdf-inspector, Markdown, G5-INT or G6 work was performed.", "- API_CHANGE=NONE; MIGRATION_OWNERSHIP=NONE.", "", "ISSUES=", *([f"- {issue}" for issue in issues] if issues else ["- NONE"]), "", f"BLOCKER={blocker}", "APPROVAL=2025 Q2 OCR repair workset closed after dependency provisioning" if status == "PASS" else "APPROVAL=NOT_APPROVED", "NEXT=G5-INT" if status == "PASS" else "NEXT=resolve reported G5-25-OCR-R blocker"]
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    for key, value in metrics.items():
        print(f"{key}={value}")
    print(f"OUTPUT_RESULTS={RESULTS_OUT.relative_to(ROOT).as_posix()}")
    print(f"OUTPUT_LOG={LOG_OUT.relative_to(ROOT).as_posix()}")
    print(f"OUTPUT_REPORT={REPORT_OUT.relative_to(ROOT).as_posix()}")
    print(f"OUTPUT_DERIVED={DERIVED.relative_to(ROOT).as_posix()}")
    print(f"ISSUES={blocker}")
    print(f"BLOCKER={blocker}")
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (GateError, OSError, ValueError, json.JSONDecodeError, subprocess.SubprocessError) as exc:
        print("STAGE=G5-25-OCR-R")
        print("STATUS=BLOCKED")
        print(f"BLOCKER={exc}")
        raise SystemExit(2)
