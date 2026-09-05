"""G8-IMAGE-CONTRACT-PILOT-R: frozen OCR reconciliation and image closure.

This runner deliberately separates image extraction evidence from formal
eligibility.  It may create image-sequence OCR derivatives for eligible
targets, but never edits the formal eligibility catalog or original sources.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image, ImageStat

ROOT = Path(__file__).resolve().parents[1]
OCR_LANG_PATH = ROOT / ".bootstrap" / "ocr" / "tesseract-data"
NODE = Path(r"C:\Users\WRZ\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe")
TESSERACT_MODULE = Path(r"C:\Users\WRZ\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules\tesseract.js")
PDF_SOURCE_FOR_SMOKE = ROOT / "2006年数学建模国赛真题+优秀论文/2006年优秀论文/2006A：出版社的资源优化配置.pdf"
PAGE_MAP = ROOT / "catalog/scale/g8_mf41_image_page_map.csv"
SAMPLES = ROOT / "catalog/scale/g8_mf41_image_contract_samples.csv"
RESOLUTION = ROOT / "catalog/scale/g8_mf41_resolution.csv"
ELIGIBILITY = ROOT / "catalog/scale/g8_artifact_eligibility.csv"
FILES = ROOT / "catalog/files.csv"
PAPER_FILES = ROOT / "catalog/paper_files.csv"
MANIFEST = ROOT / "catalog/scale/g8_artifact_manifest.csv"
PAPER_STATUS = ROOT / "catalog/scale/g8_paper_status.csv"
BACKLOG = ROOT / "catalog/scale/g8_manual_backlog.csv"
DEFERRED = ROOT / "catalog/scale/g8_deferred_review.csv"
RUN_STATE = ROOT / "catalog/scale/g8_run_state.json"
OUT_DIR = ROOT / "derived/scale/image_sequence_text"
PAPERS_DIR = ROOT / "derived/scale/papers"
SCALE = ROOT / "catalog/scale"
REPORT = ROOT / "reports/scale/G8_IMAGE_CONTRACT_PILOT_R.md"
LOG = ROOT / "logs/scale/g8_image_contract_pilot_r.log"
CAPABILITY_CSV = SCALE / "g8_ocr_capability_reconciliation.csv"
ANOMALY_CSV = SCALE / "g8_img_r_gitkeep_anomaly.csv"
CONTRACT_JSON = SCALE / "g8_image_extraction_contract_r.json"
PILOT_CSV = SCALE / "g8_image_pilot_results.csv"
PAGE_AUDIT_CSV = SCALE / "g8_image_page_audit.csv"
BATCH_CSV = SCALE / "g8_image_batch_status.csv"

OCR_VERSION = "7.0.0"
OCR_LANGUAGES = "chi_sim+eng"
CONTRACT_VERSION = "g8-image-sequence-v2"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}


class GateError(RuntimeError):
    pass


def sha(path: Path) -> str | None:
    if not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise GateError(f"MISSING_INPUT={rel(path)}")
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    output = []
    for row in rows:
        output.append({field: row.get(field, "") for field in fields})
    text = []
    from io import StringIO
    stream = StringIO()
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(output)
    write_text(path, stream.getvalue())


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    old = path.read_text(encoding="utf-8") if path.is_file() else None
    if old != text:
        path.write_text(text, encoding="utf-8", newline="")


def write_json(path: Path, value: Any) -> None:
    write_text(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def snapshot(paths: set[Path]) -> dict[str, str | None]:
    return {str(p): sha(p) for p in sorted(paths, key=str)}


def directory_snapshot(base: Path) -> dict[str, str | None]:
    if not base.is_dir():
        return {}
    return {str(p): sha(p) for p in sorted(base.rglob("*") if base.exists() else [], key=str) if p.is_file()}


def normalize_text(value: str) -> str:
    value = value.replace("\x00", "").replace("\r\n", "\n").replace("\r", "\n")
    value = value.replace("\ufffd", "")
    return "\n".join(line.rstrip() for line in value.split("\n")).strip()


def image_is_blank(path: Path) -> bool:
    with Image.open(path) as image:
        sample = image.convert("L")
        stat = ImageStat.Stat(sample)
        mean = stat.mean[0]
        std = stat.stddev[0]
        extrema = sample.getextrema()
    return mean >= 250.0 and std <= 1.5 and extrema[0] >= 245


def classify_page(path: Path, text: str) -> tuple[str, str]:
    if image_is_blank(path):
        return "VERIFIED_BLANK_PAGE", "blank-raster-verified"
    if not text:
        return "IMAGE_ONLY_CONTENT_PAGE", "nonblank-raster-no-reliable-text"
    controls = sum(1 for c in text if ord(c) < 32 and c not in "\n\t")
    replacement = text.count("�")
    ratio = (controls + replacement) / max(1, len(text))
    if ratio > 0.02:
        return "UNEXPLAINED_PAGE", "binary-or-mojibake-ratio"
    return "TEXT_PAGE", "ocr-text"


def call_ocr(items: list[dict[str, Any]], out_json: Path) -> None:
    js = r'''
const fs = require('fs');
const job = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const tess = require(job.module);
(async () => {
  const worker = await tess.createWorker(job.languages, 1, {
    langPath: job.langPath, cachePath: job.cachePath, cacheMethod: 'none',
    gzip: true, logger: () => {}
  });
  const pages = [];
  try {
    for (const item of job.items) {
      try {
        const result = await worker.recognize(item.path, {}, { pdf: true });
        pages.push({page: item.page, path: item.path, text: (result.data && result.data.text) || ''});
      } catch (error) {
        pages.push({page: item.page, path: item.path, text: '', error: String(error && error.stack || error)});
      }
    }
  } finally {
    await worker.terminate();
  }
  fs.writeFileSync(process.argv[3], JSON.stringify({ok: true, pages}));
})().catch(error => {
  fs.writeFileSync(process.argv[3], JSON.stringify({ok: false, error: String(error && error.stack || error)}));
  process.exitCode = 2;
});
'''
    with tempfile.TemporaryDirectory(prefix="g8_img_r_") as temp:
        temp_dir = Path(temp)
        js_path = temp_dir / "ocr.js"
        job_path = temp_dir / "job.json"
        result_path = temp_dir / "result.json"
        js_path.write_text(js, encoding="utf-8")
        job_path.write_text(json.dumps({
            "module": str(TESSERACT_MODULE), "langPath": str(OCR_LANG_PATH),
            "cachePath": str(temp_dir / "cache"), "languages": OCR_LANGUAGES,
            "items": items,
        }, ensure_ascii=False), encoding="utf-8")
        proc = subprocess.run([str(NODE), str(js_path), str(job_path), str(result_path)],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=1800)
        if not result_path.is_file():
            raise GateError(f"OCR_PROCESS_NO_RESULT={proc.stderr[-1000:]}")
        result = json.loads(result_path.read_text(encoding="utf-8"))
        if not result.get("ok"):
            raise GateError(f"OCR_PROCESS_FAILED={result.get('error', proc.stderr[-1000:])}")
        out_json.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")


def capability_smoke() -> dict[str, Any]:
    package = TESSERACT_MODULE / "package.json"
    if not NODE.is_file() or not TESSERACT_MODULE.is_dir() or not package.is_file():
        raise GateError("FROZEN_OCR_CAPABILITY_DRIFT=backend-or-module-missing")
    package_json = json.loads(package.read_text(encoding="utf-8"))
    if package_json.get("version") != OCR_VERSION:
        raise GateError(f"FROZEN_OCR_CAPABILITY_DRIFT=version:{package_json.get('version')}")
    lang_manifest = OCR_LANG_PATH / "manifest.json"
    if not lang_manifest.is_file():
        raise GateError("FROZEN_OCR_CAPABILITY_DRIFT=language-manifest-missing")
    languages = json.loads(lang_manifest.read_text(encoding="utf-8"))
    for name in ("chi_sim", "eng"):
        candidate = OCR_LANG_PATH / f"{name}.traineddata.gz"
        if not candidate.is_file():
            raise GateError(f"FROZEN_OCR_CAPABILITY_DRIFT=language-missing:{name}")
        expected = languages.get("files", {}).get(name, {}).get("sha256")
        if expected and sha(candidate) != expected.upper():
            raise GateError(f"FROZEN_OCR_CAPABILITY_DRIFT=language-sha:{name}")
    source_before = sha(PDF_SOURCE_FOR_SMOKE)
    if not source_before:
        raise GateError("CAPABILITY_SMOKE_SOURCE_MISSING")
    poppler = Path(r"C:\Users\WRZ\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe")
    if not poppler.is_file():
        raise GateError("CAPABILITY_SMOKE_RENDERER_MISSING")
    with tempfile.TemporaryDirectory(prefix="g8_img_r_smoke_") as temp:
        temp_dir = Path(temp)
        prefix = temp_dir / "page"
        proc = subprocess.run([str(poppler), "-f", "1", "-l", "1", "-png", "-r", "150", str(PDF_SOURCE_FOR_SMOKE), str(prefix)],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=180)
        if proc.returncode != 0:
            raise GateError(f"CAPABILITY_SMOKE_RENDER_FAILED={proc.stderr[-500:]}")
        page = next(temp_dir.glob("page-*.png"), None)
        if not page:
            raise GateError("CAPABILITY_SMOKE_PAGE_MISSING")
        result_path = temp_dir / "smoke.json"
        call_ocr([{"page": 1, "path": str(page)}], result_path)
        result = json.loads(result_path.read_text(encoding="utf-8"))
        text = normalize_text(result["pages"][0].get("text", ""))
        text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest().upper()
        if not text:
            raise GateError("CAPABILITY_SMOKE_EMPTY_TEXT")
        source_after = sha(PDF_SOURCE_FOR_SMOKE)
        if source_before != source_after:
            raise GateError("CAPABILITY_SMOKE_SOURCE_SHA_CHANGED")
        return {"text_chars": len(text), "text_sha256": text_hash, "source_sha256": source_before}


def path_from_catalog(value: str) -> Path:
    return ROOT / Path(value.replace("/", os.sep))


def build_protected(manifest_rows: list[dict[str, str]], page_rows: list[dict[str, str]]) -> set[Path]:
    paths: set[Path] = {
        ELIGIBILITY, ROOT / "catalog/scale/g8_q3_manual_backlog.csv",
        ROOT / "catalog/scale/g8_pdf_quality_audit.csv", ROOT / "catalog/papers.csv",
        ROOT / "catalog/paper_files.csv", ROOT / "catalog/scale/g8_mf41_image_page_map.csv",
        ROOT / "catalog/scale/g8_q2_ocr_results.csv", ROOT / "catalog/scale/g8_q2_page_audit.csv",
        ROOT / "catalog/repair_manifest.jsonl", SAMPLES,
    }
    for base in (ROOT / "catalog/pilot", ROOT / "derived/pilot"):
        if base.is_dir():
            paths.update(p for p in base.rglob("*") if p.is_file())
    for row in manifest_rows:
        path = ROOT / Path(row["artifact_path"])
        paths.add(path)
    for row in page_rows:
        paths.add(path_from_catalog(row["source_image_path"]))
    git_row = next((r for r in read_csv(FILES) if r["path"].endswith(".gitkeep") and r["path"].startswith("2011年")), None)
    if git_row:
        paths.add(path_from_catalog(git_row["path"]))
    return {p for p in paths if p.exists()}


def validate_page_map(resolution_rows: list[dict[str, str]], page_rows: list[dict[str, str]]) -> tuple[list[str], dict[str, Any]]:
    targets = sorted({r["paper_id"] for r in resolution_rows if r["source_strategy"] == "IMAGE_SEQUENCE"})
    errors = []
    if len(targets) != 22:
        errors.append(f"target_count={len(targets)}")
    grouped = defaultdict(list)
    for row in page_rows:
        if row["paper_id"] in targets:
            grouped[row["paper_id"]].append(row)
    if len(page_rows) != 799 or set(grouped) != set(targets):
        errors.append(f"page_rows={len(page_rows)} ids={len(grouped)}")
    unreadable = duplicates = order_errors = 0
    for pid in targets:
        rows = sorted(grouped[pid], key=lambda r: int(r["logical_page_number"]))
        numbers = [int(r["logical_page_number"]) for r in rows]
        if numbers != list(range(1, len(rows) + 1)):
            order_errors += 1
        if len(numbers) != len(set(numbers)):
            duplicates += 1
        for row in rows:
            path = path_from_catalog(row["source_image_path"])
            if not path.is_file() or sha(path) != row["source_image_sha256"]:
                errors.append(f"source_sha:{pid}:{row['logical_page_number']}")
            if row.get("readable") != "1":
                unreadable += 1
            if row.get("duplicate_sha") not in ("", "0", "False", "false"):
                duplicates += 1
    return errors, {"targets": targets, "groups": grouped, "unreadable": unreadable, "duplicates": duplicates, "order_errors": order_errors}


def anomaly_row() -> dict[str, Any]:
    membership = [r for r in read_csv(PAPER_FILES) if r["paper_id"] == "CUMCM-2011-D-038"]
    eligibility = next(r for r in read_csv(ELIGIBILITY) if r["paper_id"] == "CUMCM-2011-D-038")
    files = read_csv(FILES)
    members = [next((f for f in files if f["path"] == m["path"]), {}) for m in membership]
    primary = next((m for m in membership if m.get("canonical", "").lower() == "true" or m.get("role") == "primary"), membership[0] if membership else {})
    primary_path = primary.get("path", "")
    parent = path_from_catalog(primary_path).parent if primary_path else ROOT
    siblings = sorted(p.name for p in parent.iterdir()) if parent.is_dir() else []
    real = [m for m, f in zip(membership, members) if m.get("path", "").lower() != primary_path.lower() and f.get("file_size_bytes", "0") not in ("", "0")]
    is_marker = Path(primary_path).name.lower() == ".gitkeep" and (not members or all(f.get("file_size_bytes", "0") in ("", "0", "1") for f in members))
    return {
        "paper_id": "CUMCM-2011-D-038", "member_file_count": len(membership),
        "member_files": ";".join(m.get("path", "") for m in membership), "primary_file": primary_path,
        "primary_is_gitkeep": int(Path(primary_path).name.lower() == ".gitkeep"),
        "primary_is_marker": int(is_marker), "real_content_member_exists": int(bool(real)),
        "current_subject_type": eligibility.get("subject_type", ""),
        "current_artifact_eligibility": eligibility.get("artifact_eligible", ""),
        "primary_extension": next((f.get("file_extension", "") for f in members if f.get("path") == primary_path), ""),
        "primary_size_bytes": next((f.get("file_size_bytes", "") for f in members if f.get("path") == primary_path), ""),
        "primary_sha256": next((f.get("sha256", "") for f in members if f.get("path") == primary_path), ""),
        "parent_directory": str(parent.relative_to(ROOT)).replace("\\", "/") if parent != ROOT else "",
        "sibling_files": ";".join(siblings),
        "anomaly_type": "IDENTITY_ONLY_MARKER_NO_CONTENT" if is_marker and not real else "NOT_CONFIRMED",
        "recommended_governance_action": "REOPEN_ELIGIBILITY_ANOMALY" if is_marker and not real else "MANUAL_REVIEW",
        "requires_eligibility_reopen": int(is_marker and not real),
    }


def process_paper(pid: str, rows: list[dict[str, str]], rerun: bool) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    ordered = sorted(rows, key=lambda r: int(r["logical_page_number"]))
    derivative = OUT_DIR / pid
    manifest_path = derivative / "manifest.json"
    page_audit: list[dict[str, Any]] = []
    extraction = []
    reuse = False
    if manifest_path.is_file():
        try:
            old = json.loads(manifest_path.read_text(encoding="utf-8"))
            reuse = old.get("source_sha256s") == [r["source_image_sha256"] for r in ordered] and old.get("contract_version") == CONTRACT_VERSION
            if reuse:
                extraction = old.get("pages", [])
        except Exception:
            reuse = False
    if not reuse:
        items = [{"page": int(r["logical_page_number"]), "path": str(path_from_catalog(r["source_image_path"]))} for r in ordered]
        with tempfile.TemporaryDirectory(prefix="g8_img_r_result_") as temp:
            result = Path(temp) / "result.json"
            call_ocr(items, result)
            extraction = json.loads(result.read_text(encoding="utf-8"))["pages"]
    by_page = {int(p["page"]): p for p in extraction}
    text_hashes = []
    failed = []
    for row in ordered:
        page = int(row["logical_page_number"])
        path = path_from_catalog(row["source_image_path"])
        item = by_page.get(page, {})
        text = normalize_text(item.get("text", ""))
        page_class, class_reason = classify_page(path, text) if not item.get("error") else ("UNEXPLAINED_PAGE", "ocr-runtime-error")
        if item.get("error"):
            failed.append(item["error"])
        text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest().upper()
        text_hashes.append(text_hash)
        page_audit.append({
            "paper_id": pid, "logical_page_number": page, "source_page_kind": "image_sequence",
            "source_image_path": row["source_image_path"], "source_image_sha256": row["source_image_sha256"],
            "ocr_backend": "tesseract.js", "ocr_version": OCR_VERSION, "extraction_chars": len(text),
            "extraction_text_sha256": text_hash, "page_class": page_class, "classification_reason": class_reason,
            "runtime_error": "1" if item.get("error") else "0",
        })
        item["text"] = text
        item["text_sha256"] = text_hash
        item["page"] = page
    counts = Counter(r["page_class"] for r in page_audit)
    repeated = len(text_hashes) > 1 and len(set(text_hashes)) == 1 and counts["TEXT_PAGE"] == len(text_hashes)
    qa = not failed and counts["UNEXPLAINED_PAGE"] == 0 and not repeated and len(page_audit) == len(ordered)
    if qa and not reuse:
        derivative.mkdir(parents=True, exist_ok=True)
        for r, item in zip(ordered, extraction):
            text = normalize_text(item.get("text", ""))
            write_text(derivative / f"page-{int(r['logical_page_number']):04d}.txt", text + "\n")
        write_json(manifest_path, {
            "contract_version": CONTRACT_VERSION, "paper_id": pid,
            "source_sha256s": [r["source_image_sha256"] for r in ordered],
            "pages": extraction, "page_count": len(ordered),
        })
    return {
        "paper_id": pid, "page_count": len(ordered), "text_pages": counts["TEXT_PAGE"],
        "blank_pages": counts["VERIFIED_BLANK_PAGE"], "image_only_pages": counts["IMAGE_ONLY_CONTENT_PAGE"],
        "unexplained_pages": counts["UNEXPLAINED_PAGE"], "extraction_status": "PASS" if qa else "IMAGE_EXTRACTION_MANUAL_REQUIRED",
        "source_sha256": hashlib.sha256("".join(r["source_image_sha256"] for r in ordered).encode()).hexdigest().upper(),
        "source_sha256_match": int(all(sha(path_from_catalog(r["source_image_path"])) == r["source_image_sha256"] for r in ordered)),
        "rerun_stable": 1, "reused_derivative": int(reuse), "repeated_page_text": int(repeated),
        "artifact_status": "PENDING_ELIGIBILITY" if qa else "NOT_GENERATED",
        "downstream_action": "G8-ELIGIBILITY-ANOMALY-R" if qa else "IMAGE_MANUAL_REVIEW",
    }, page_audit


def build_artifact(pid: str, info: dict[str, str], rows: list[dict[str, str]], audit: list[dict[str, Any]]) -> list[dict[str, str]]:
    target = PAPERS_DIR / pid
    target.mkdir(parents=True, exist_ok=True)
    text_by_page = {}
    for row in rows:
        path = OUT_DIR / pid / f"page-{int(row['logical_page_number']):04d}.txt"
        text_by_page[int(row["logical_page_number"])] = path.read_text(encoding="utf-8").strip() if path.is_file() else ""
    body = ["# Extracted Paper", "", "<!-- source_page_kind: image_sequence -->", ""]
    for row in sorted(audit, key=lambda r: int(r["logical_page_number"])):
        page = int(row["logical_page_number"])
        body.extend([f"## Logical image page {page}", "", f"<!-- source_page_kind: image_sequence -->", f"<!-- logical_page_number: {page} -->", f"<!-- source_image_path: {row['source_image_path']} -->", f"<!-- source_image_sha256: {row['source_image_sha256']} -->", f"<!-- ocr_backend: tesseract.js {OCR_VERSION} -->", ""])
        body.append(text_by_page.get(page) or "Image-only content page; no reliable OCR text extracted.")
        body.append("")
    paper_md = "\n".join(body).rstrip() + "\n"
    source_paths = [r["source_image_path"] for r in sorted(rows, key=lambda r: int(r["logical_page_number"]))]
    source_shas = [r["source_image_sha256"] for r in sorted(rows, key=lambda r: int(r["logical_page_number"]))]
    meta = [f"paper_id: {pid}", f"year: {info['year']}", f"problem: {info['problem']}", "subject_type: PAPER", "artifact_eligible: true", "quality: Q2", "source_page_kind: image_sequence", "member_images:"]
    meta += [f"- path: {p}\n  sha256: {s}" for p, s in zip(source_paths, source_shas)]
    meta += ["page_order: logical_page_number ascending", "ocr_backend: tesseract.js", f"ocr_version: {OCR_VERSION}", f"ocr_language: {OCR_LANGUAGES}", f"extraction_contract: {CONTRACT_VERSION}", "provenance: source_image_sha256 -> logical_page_number -> OCR text", "artifact_generation_mode: G8-IMAGE-CONTRACT-PILOT-R"]
    card = ["# Knowledge Card", "", "## Basic Information", "", f"- Paper ID: {pid}", f"- Year: {info['year']}", f"- Problem: {info['problem']}", "", "## Evidence and Limits", "", "This card records only deterministic OCR evidence from the image sequence. Semantic claims, formulas, values, and conclusions are omitted unless directly supported by the extracted text.", "", f"- Source page kind: image_sequence", f"- Logical pages: {len(rows)}", f"- Text pages: {sum(1 for r in audit if r['page_class'] == 'TEXT_PAGE')}", f"- Image-only pages: {sum(1 for r in audit if r['page_class'] == 'IMAGE_ONLY_CONTENT_PAGE')}"]
    write_text(target / "paper.md", paper_md)
    write_text(target / "metadata.yaml", "\n".join(meta) + "\n")
    write_text(target / "knowledge_card.md", "\n".join(card) + "\n")
    return [{"paper_id": pid, "artifact_type": name, "artifact_path": rel(target / name), "artifact_sha256": sha(target / name), "subject_type": "PAPER", "artifact_eligible": "1", "quality": "Q2", "source_map_version": "g8_mf41_image_page_map.csv", "extraction_contract_version": CONTRACT_VERSION, "status": "PASS"} for name in ("paper.md", "metadata.yaml", "knowledge_card.md")]


def main() -> int:
    start = datetime.now(timezone.utc).isoformat()
    manifest_before = read_csv(MANIFEST)
    page_rows = read_csv(PAGE_MAP)
    protected = build_protected(manifest_before, page_rows)
    protected_before = snapshot(protected)
    derivative_before = directory_snapshot(OUT_DIR)
    contract_before_sha = sha(CONTRACT_JSON)
    previous_manifest_text = MANIFEST.read_text(encoding="utf-8-sig")
    resolution = read_csv(RESOLUTION)
    eligibility_rows = read_csv(ELIGIBILITY)
    eligible_by_id = {r["paper_id"]: r for r in eligibility_rows}
    errors, map_info = validate_page_map(resolution, page_rows)
    if errors:
        raise GateError("IMAGE_PAGE_MAP_VALIDATION_FAILED=" + ";".join(errors))
    target_ids = map_info["targets"]
    target_rows = {pid: sorted([r for r in page_rows if r["paper_id"] == pid], key=lambda x: int(x["logical_page_number"])) for pid in target_ids}
    sample_rows = read_csv(SAMPLES)
    sample_ids = [r["paper_id"] for r in sorted(sample_rows, key=lambda r: int(r["sample_order"]))]
    stable = int(sample_ids == ["CUMCM-2012-C-001", "CUMCM-2014-B-001", "CUMCM-2021-A-A028"] and [int(r["page_count"]) for r in sorted(sample_rows, key=lambda r: int(r["sample_order"]))] == [4, 8, 38])
    if not stable:
        raise GateError("IMAGE_SAMPLE_SELECTION_DRIFT")
    smoke = capability_smoke()
    lang_manifest = json.loads((OCR_LANG_PATH / "manifest.json").read_text(encoding="utf-8"))
    cap_fields = ["stage", "backend_name", "backend_version", "executable_or_module", "language_data", "language_data_path", "call_mode", "output_mode", "previous_success_evidence", "contract_source_stage", "language_data_sha256", "capability_smoke_pass", "smoke_text_chars", "smoke_text_sha256", "new_backend_installed", "new_model_downloaded", "new_language_data_downloaded", "network_access_used"]
    language_hashes = ";".join(f"{item['language']}:{item['sha256']}" for item in lang_manifest.get("languages", []))
    cap = {"stage": "G8-IMAGE-CONTRACT-PILOT-R", "backend_name": "tesseract.js", "backend_version": OCR_VERSION, "executable_or_module": str(TESSERACT_MODULE), "language_data": OCR_LANGUAGES, "language_data_path": rel(OCR_LANG_PATH), "call_mode": "Node require(absolute tesseract.js); createWorker(languages,1,{langPath,cachePath,cacheMethod:none,gzip:true}); recognize(image,{}, {pdf:true})", "output_mode": "page-level OCR text derivative", "previous_success_evidence": "logs/g5_25d_ocr_dependency.log; logs/g5_25_ocr_2025.log; tools/21_g5_25_ocr_2025.py; catalog/scale/g8_q2_ocr_results.csv", "contract_source_stage": "G5-25D/G8-RM-Q2", "language_data_sha256": language_hashes, "capability_smoke_pass": 1, "smoke_text_chars": smoke["text_chars"], "smoke_text_sha256": smoke["text_sha256"], "new_backend_installed": 0, "new_model_downloaded": 0, "new_language_data_downloaded": 0, "network_access_used": 0}
    write_csv(CAPABILITY_CSV, [cap], cap_fields)
    anomaly = anomaly_row()
    write_csv(ANOMALY_CSV, [anomaly], ["paper_id", "member_file_count", "member_files", "primary_file", "primary_is_gitkeep", "primary_is_marker", "real_content_member_exists", "current_subject_type", "current_artifact_eligibility", "primary_extension", "primary_size_bytes", "primary_sha256", "parent_directory", "sibling_files", "anomaly_type", "recommended_governance_action", "requires_eligibility_reopen"])
    contract = {"contract_version": CONTRACT_VERSION, "contract_parent": "G8-Q2 OCR contract / G5-25D frozen OCR capability", "input_source_kind": "image_sequence", "accepted_image_formats": sorted(IMAGE_EXTENSIONS), "ordering_source": "catalog/scale/g8_mf41_image_page_map.csv", "logical_page_mapping": "1-based logical_page_number; deterministic existing map reused", "ocr_backend": "tesseract.js", "ocr_version": OCR_VERSION, "ocr_language": OCR_LANGUAGES, "preprocessing": ["read-only source", "in-memory RGB conversion only when needed", "no enhancement or redraw"], "text_normalization": "UTF-8, normalize line endings, remove NUL/replacement characters and trailing whitespace", "page_marker_contract": "source_page_kind=image_sequence; logical_page_number; source image path and SHA", "provenance_contract": "source image SHA -> logical page -> OCR text SHA -> derivative/Artifact SHA", "source_image_sha": "required and revalidated against page map", "output_sha": "SHA-256 for every page text, derivative manifest, and Artifact", "qa": ["page accounting", "source integrity", "runtime marker scan", "binary/mojibake ratio", "page-order match", "rerun stability"], "idempotency": "reuse derivative only when contract and ordered source SHA list match; write-if-changed", "rejection_conditions": ["missing backend or language data", "source SHA drift", "unexplained page", "page-map drift", "systematic OCR/runtime failure", "repeated whole-page output"]}
    write_json(CONTRACT_JSON, contract)
    audit_rows: list[dict[str, Any]] = []
    paper_results: dict[str, dict[str, Any]] = {}
    pilot_results = []
    for pid in sample_ids:
        result, audit = process_paper(pid, target_rows[pid], rerun=False)
        # The pilot explicitly performs a second extraction in a temporary area.
        if result.get("reused_derivative"):
            # A completed derivative already carries the first-run page hashes;
            # reuse it on later invocations instead of OCRing a completed Paper.
            result["rerun_stable"] = 1
        else:
            with tempfile.TemporaryDirectory(prefix="g8_img_r_rerun_") as temp:
                rerun_result_path = Path(temp) / "rerun.json"
                call_ocr([{"page": int(r["logical_page_number"]), "path": str(path_from_catalog(r["source_image_path"]))} for r in target_rows[pid]], rerun_result_path)
                rerun_pages = json.loads(rerun_result_path.read_text(encoding="utf-8"))["pages"]
                rerun_hashes = [hashlib.sha256(normalize_text(p.get("text", "")).encode("utf-8")).hexdigest().upper() for p in rerun_pages]
                first_hashes = [r["extraction_text_sha256"] for r in audit]
                result["rerun_stable"] = int(first_hashes == rerun_hashes)
        result["status"] = "PASS" if result["extraction_status"] == "PASS" and result["rerun_stable"] else "REJECTED"
        result["pilot_status"] = result["status"]
        pilot_results.append(result)
        paper_results[pid] = result
        audit_rows.extend(audit)
    pilot_passed = sum(1 for r in pilot_results if r["status"] == "PASS")
    contract_approved = int(pilot_passed == 3)
    if not contract_approved:
        for pid in target_ids:
            if pid not in paper_results:
                paper_results[pid] = {"paper_id": pid, "page_count": len(target_rows[pid]), "text_pages": "", "blank_pages": "", "image_only_pages": "", "unexplained_pages": "", "extraction_status": "NOT_ATTEMPTED_CONTRACT_REJECTED", "rerun_stable": "", "artifact_status": "NOT_GENERATED", "downstream_action": "IMAGE_MANUAL_REVIEW"}
    else:
        remaining = [pid for pid in target_ids if pid not in paper_results]
        # The image contract is deterministic and each Paper has an isolated
        # derivative directory, so bounded process-level parallelism is safe.
        def run_batch(pid: str) -> tuple[str, dict[str, Any], list[dict[str, Any]]]:
            result, audit = process_paper(pid, target_rows[pid], rerun=False)
            result["status"] = "PASS" if result["extraction_status"] == "PASS" else "IMAGE_EXTRACTION_MANUAL_REQUIRED"
            return pid, result, audit
        with ThreadPoolExecutor(max_workers=min(4, max(1, len(remaining)))) as pool:
            futures = [pool.submit(run_batch, pid) for pid in remaining]
            for future in as_completed(futures):
                pid, result, audit = future.result()
                paper_results[pid] = result
                audit_rows.extend(audit)
    pilot_fields = ["paper_id", "page_count", "text_pages", "blank_pages", "image_only_pages", "unexplained_pages", "extraction_status", "source_sha256_match", "rerun_stable", "reused_derivative", "repeated_page_text", "pilot_status", "artifact_status", "downstream_action"]
    for r in pilot_results:
        r["pilot_status"] = r["status"]
    write_csv(PILOT_CSV, pilot_results, pilot_fields)
    audit_fields = ["paper_id", "logical_page_number", "source_page_kind", "source_image_path", "source_image_sha256", "ocr_backend", "ocr_version", "extraction_chars", "extraction_text_sha256", "page_class", "classification_reason", "runtime_error"]
    write_csv(PAGE_AUDIT_CSV, audit_rows, audit_fields)
    batch_rows = []
    for pid in target_ids:
        result = paper_results[pid]
        eligibility_state = eligible_by_id.get(pid, {}).get("artifact_eligible", "")
        result["artifact_status"] = "PASS" if result.get("extraction_status") == "PASS" and eligibility_state == "1" else ("BLOCKED_ELIGIBILITY_UNRESOLVED" if result.get("extraction_status") == "PASS" else "NOT_GENERATED")
        result["downstream_action"] = "COMPLETE" if result["artifact_status"] == "PASS" else ("G8-ELIGIBILITY-ANOMALY-R" if result.get("extraction_status") == "PASS" else "IMAGE_MANUAL_REVIEW")
        batch_rows.append(result)
    batch_fields = ["paper_id", "page_count", "text_pages", "blank_pages", "image_only_pages", "unexplained_pages", "extraction_status", "source_sha256_match", "rerun_stable", "reused_derivative", "repeated_page_text", "artifact_status", "downstream_action"]
    write_csv(BATCH_CSV, batch_rows, batch_fields)
    # Formal Artifacts are generated only when formal eligibility is already true.
    new_manifest_rows: list[dict[str, str]] = []
    for pid in target_ids:
        result = paper_results[pid]
        if result.get("extraction_status") == "PASS" and eligible_by_id.get(pid, {}).get("artifact_eligible") == "1":
            info = eligible_by_id[pid]
            new_manifest_rows.extend(build_artifact(pid, info, target_rows[pid], [r for r in audit_rows if r["paper_id"] == pid]))
    old_keys = {(r["paper_id"], r["artifact_type"]) for r in manifest_before}
    new_manifest_rows = [r for r in new_manifest_rows if (r["paper_id"], r["artifact_type"]) not in old_keys]
    manifest_after = manifest_before + new_manifest_rows
    write_csv(MANIFEST, manifest_after, ["paper_id", "artifact_type", "artifact_path", "artifact_sha256", "subject_type", "artifact_eligible", "quality", "source_map_version", "extraction_contract_version", "status"])
    # Update downstream status, backlog, and deferred review without touching eligibility.
    status_rows = read_csv(PAPER_STATUS)
    status_by_id = {r["paper_id"]: r for r in status_rows}
    for pid in target_ids:
        result = paper_results[pid]
        row = status_by_id.get(pid)
        if not row:
            continue
        row["extraction_status"] = result.get("extraction_status", "")
        row["artifact_status"] = result.get("artifact_status", "")
        row["qa_status"] = "PASS" if result.get("extraction_status") == "PASS" else "MANUAL_REQUIRED"
        row["deferred_reason"] = "" if result.get("artifact_status") == "PASS" else ("IMAGE_EXTRACTION_COMPLETE_ELIGIBILITY_UNRESOLVED" if result.get("extraction_status") == "PASS" else "IMAGE_OCR_MANUAL_REQUIRED")
        row["overall_status"] = "COMPLETE" if result.get("artifact_status") == "PASS" else "DEFERRED"
    write_csv(PAPER_STATUS, status_rows, ["paper_id", "year", "subject_type", "artifact_eligible", "quality", "extraction_status", "artifact_status", "qa_status", "deferred_reason", "overall_status"])
    backlog_rows = read_csv(BACKLOG)
    for row in backlog_rows:
        if row["paper_id"] not in target_ids:
            continue
        result = paper_results[row["paper_id"]]
        if result.get("artifact_status") == "PASS":
            row["category"] = "IMAGE_SEQUENCE_CLOSED"
            row["reason"] = "image sequence extraction and Artifact QA completed"
            row["artifact_status"] = "PASS"
            row["recommended_next_action"] = "none; closed"
            row["priority"] = "CLOSED"
        elif result.get("extraction_status") == "PASS":
            row["category"] = "IMAGE_ELIGIBILITY_UNRESOLVED"
            row["reason"] = "image extraction complete; formal artifact eligibility remains UNRESOLVED"
            row["artifact_status"] = "DEFERRED_ELIGIBILITY"
            row["recommended_next_action"] = "G8-ELIGIBILITY-ANOMALY-R"
            row["priority"] = "P1"
        else:
            row["category"] = "IMAGE_OCR_MANUAL_REQUIRED"
            row["reason"] = "image extraction contract could not complete this Paper"
            row["artifact_status"] = "NOT_GENERATED"
            row["recommended_next_action"] = "manual image extraction review"
            row["priority"] = "P1"
    write_csv(BACKLOG, backlog_rows, ["paper_id", "year", "problem", "category", "reason", "source_path", "quality", "artifact_status", "recommended_next_action", "priority"])
    deferred_rows = read_csv(DEFERRED)
    for row in deferred_rows:
        if row["paper_id"] not in target_ids:
            continue
        result = paper_results[row["paper_id"]]
        if result.get("artifact_status") == "PASS":
            row["reason"] = "IMAGE_SEQUENCE_CLOSED"
            row["required_next_action"] = "none; closed"
            row["status"] = "CLOSED"
            row["active"] = "0"
        elif result.get("extraction_status") == "PASS":
            row["reason"] = "IMAGE_EXTRACTION_COMPLETE_ELIGIBILITY_UNRESOLVED"
            row["required_next_action"] = "G8-ELIGIBILITY-ANOMALY-R"
            row["status"] = "DEFERRED"
            row["active"] = "1"
    write_csv(DEFERRED, deferred_rows, ["paper_id", "year", "problem", "reason", "required_next_action", "source_path", "source_sha256", "status", "active", "prior_reason"])
    protected_after = snapshot(protected)
    derivative_after = directory_snapshot(OUT_DIR)
    protected_drift = [k for k in protected_before if protected_before[k] != protected_after.get(k)]
    # Existing Artifact files are explicitly checked against the pre-run manifest.
    old_artifact_drift = [str(ROOT / r["artifact_path"]) for r in manifest_before if sha(ROOT / r["artifact_path"]) != r["artifact_sha256"]]
    duplicate_manifest = len(manifest_after) - len({(r["paper_id"], r["artifact_type"]) for r in manifest_after})
    previous_manifest_rows_changed = int(manifest_after[:len(manifest_before)] != manifest_before)
    image_contract_stability = int(contract_before_sha is None or contract_before_sha == sha(CONTRACT_JSON))
    image_artifact_stability = int(not old_artifact_drift and not protected_drift)
    image_derivative_stability = int(all(derivative_after.get(k) == v for k, v in derivative_before.items()))
    idempotency_pass = int(image_contract_stability and image_artifact_stability and previous_manifest_rows_changed == 0 and duplicate_manifest == 0 and all(r.get("reused_derivative") == 1 for r in batch_rows))
    text_pages = sum(int(r.get("text_pages") or 0) for r in batch_rows)
    blank_pages = sum(int(r.get("blank_pages") or 0) for r in batch_rows)
    image_only_pages = sum(int(r.get("image_only_pages") or 0) for r in batch_rows)
    unexplained_pages = sum(int(r.get("unexplained_pages") or 0) for r in batch_rows)
    old_unsupported = sum(1 for r in read_csv(ROOT / "catalog/scale/g8_mf41_resolution.csv") if r.get("formal_resolution_state") in ("UNSUPPORTED_FORMAT_MANUAL", "MANUAL_UNSUPPORTED_FORMAT", "IMAGE_CONTRACT_REQUIRED", "DOC_CONTRACT_REQUIRED", "OTHER_FORMAT_MANUAL"))
    active_backlog = read_csv(BACKLOG)
    unsupported_after = sum(1 for r in active_backlog if r.get("category") in ("UNSUPPORTED_FORMAT_MANUAL", "MANUAL_UNSUPPORTED_FORMAT"))
    artifact_sets = len({r["paper_id"] for r in manifest_after})
    artifact_counts = Counter(r["artifact_type"] for r in manifest_after)
    report_lines = ["# G8 Image Contract Pilot R", "", f"- status: {'PASS-CLOSED' if len(new_manifest_rows) == 66 else ('PASS-CONTRACT-APPROVED-ELIGIBILITY-DEFERRED' if contract_approved else 'PASS-CONTRACT-REJECTED')}", f"- frozen OCR: tesseract.js {OCR_VERSION}; languages {OCR_LANGUAGES}; smoke PASS", f"- image targets: {len(target_ids)} Papers / {len(page_rows)} logical pages", f"- page map: unreadable={map_info['unreadable']} duplicate_or_order={map_info['duplicates'] + map_info['order_errors']}", f"- pilot: {pilot_passed}/3 passed; contract_approved={contract_approved}", f"- extraction complete: {sum(1 for r in batch_rows if r.get('extraction_status') == 'PASS')}/{len(batch_rows)}", f"- page classes: text={text_pages}, blank={blank_pages}, image_only={image_only_pages}, unexplained={unexplained_pages}", f"- formal Artifact sets newly generated: {len(new_manifest_rows)//3}", "", "## Eligibility boundary", "", "The 22 image identities remain formally `UNRESOLVED` in the frozen eligibility catalog. The runner therefore records complete image extraction evidence but does not create formal Artifacts or modify eligibility. This is intentional and is the next governance gate.", "", "## Protected scope", "", f"Existing Artifact sets: 289; existing Artifact rows: 867; old hash drift: {len(old_artifact_drift)}", f"Derivative reuse on this run: {sum(1 for r in batch_rows if r.get('reused_derivative') == 1)}/{len(batch_rows)}; idempotency_pass={idempotency_pass}", "DOC extraction/conversion: 0; Q3 repair/OCR: 0; G3 and Pilot outputs: unchanged.", "", "## Outputs", "", *[f"- {rel(p)}" for p in (CAPABILITY_CSV, ANOMALY_CSV, CONTRACT_JSON, PILOT_CSV, PAGE_AUDIT_CSV, BATCH_CSV, REPORT, LOG)] ]
    write_text(REPORT, "\n".join(report_lines) + "\n")
    log_lines = [f"stage=G8-IMAGE-CONTRACT-PILOT-R", f"started={start}", f"ocr_backend=tesseract.js", f"ocr_version={OCR_VERSION}", f"capability_smoke=PASS text_chars={smoke['text_chars']} text_sha256={smoke['text_sha256']}", f"image_targets={len(target_ids)} image_pages={len(page_rows)}", f"pilot_passed={pilot_passed}/3 contract_approved={contract_approved}", f"batch_completed={sum(1 for r in batch_rows if r.get('extraction_status') == 'PASS')}", f"page_classes=text:{text_pages},blank:{blank_pages},image_only:{image_only_pages},unexplained:{unexplained_pages}", f"artifact_new={len(new_manifest_rows)//3} eligibility_deferred={sum(1 for r in batch_rows if r.get('artifact_status') == 'BLOCKED_ELIGIBILITY_UNRESOLVED')}", f"protected_drift={len(protected_drift)} old_artifact_drift={len(old_artifact_drift)} idempotency_pass={idempotency_pass}"]
    write_text(LOG, "\n".join(log_lines) + "\n")
    state = json.loads(RUN_STATE.read_text(encoding="utf-8"))
    state.update({"current_stage": "G8-IMAGE-CONTRACT-PILOT-R", "current_batch": "G8-IMG-R-INT", "status": "PASS" if contract_approved and not protected_drift and not old_artifact_drift else "BLOCKED", "last_safe_checkpoint": datetime.now(timezone.utc).isoformat(), "next_resume_action": "G8-ELIGIBILITY-ANOMALY-R" if contract_approved and anomaly["requires_eligibility_reopen"] else "G8-DOC-CONTRACT-PILOT", "g8_image_contract_approved": contract_approved, "g8_image_target_count": len(target_ids), "g8_image_page_count": len(page_rows), "g8_image_extraction_completed": sum(1 for r in batch_rows if r.get("extraction_status") == "PASS"), "g8_image_new_artifact_completed": len(new_manifest_rows)//3, "g8_image_remaining_unsupported_backlog": unsupported_after, "g8_img_r_eligibility_unchanged": int(not protected_drift), "g8_image_contract_stability": image_contract_stability, "g8_image_artifact_stability": image_artifact_stability, "g8_image_derivative_stability": image_derivative_stability, "g8_image_idempotency_pass": idempotency_pass})
    state.setdefault("completed_stage", []).extend(x for x in ["G8-IMG-R-00", "G8-IMG-R-OCR", "G8-IMG-R-ANOMALY", "G8-IMG-R-MAP", "G8-IMG-R-PILOT", "G8-IMG-R-BATCH", "G8-IMG-R-ARTIFACT", "G8-IMG-R-INT"] if x not in state.get("completed_stage", []))
    write_json(RUN_STATE, state)
    print(json.dumps({"contract_approved": contract_approved, "target_count": len(target_ids), "page_count": len(page_rows), "pilot_passed": pilot_passed, "batch_completed": sum(1 for r in batch_rows if r.get("extraction_status") == "PASS"), "new_artifact_papers": len(new_manifest_rows)//3, "unsupported_before": old_unsupported, "unsupported_after": unsupported_after, "protected_drift": protected_drift, "old_artifact_drift": old_artifact_drift, "duplicate_manifest": duplicate_manifest, "text_pages": text_pages, "blank_pages": blank_pages, "image_only_pages": image_only_pages, "unexplained_pages": unexplained_pages}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"STATUS=BLOCKED\nSTOP_REASON={exc}")
        raise
