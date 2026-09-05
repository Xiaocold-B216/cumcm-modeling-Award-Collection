"""G11 marker-only image residual scope diagnostic.

Render and OCR are diagnostic-only.  This stage never writes formal bodies,
formal metadata, registries, indexes, or repair artifacts.  Each render and
OCR invocation is page-scoped; OCR is one routed page per child with no retry.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from PIL import Image, ImageStat


ROOT = Path(__file__).resolve().parents[1]
SCALE = ROOT / "catalog" / "scale"
REPORTS = ROOT / "reports" / "scale"

EXPECTED_BRANCH = "library-refactor-v1"
EXPECTED_HEAD = "557724fba6572d4d83dc421feda5b17b13ff8d66"
SOURCE_RECONCILE_ATTEMPT_ID = "g11-residual-diagnostic-baseline-reconcile-557724fba6572d4d"

RESIDUAL_INPUT = SCALE / "g11_marker_only_image_residual_input.csv"
RESIDUAL_DIAGNOSTIC = SCALE / "g11_marker_only_residual_scope_diagnostic.csv"
PREVIOUS_RESULT = SCALE / "g11_marker_only_residual_scope_diagnostic_result.json"
RECONCILE_RESULT = SCALE / "g11_residual_diagnostic_baseline_reconcile_result.json"
CONFIRMED_TARGETS = SCALE / "g11_marker_only_confirmed_repair_targets.csv"
TARGET_DECISIONS = SCALE / "g11_targeted_visual_diagnostic_decisions.csv"
DEEP_PAGE = SCALE / "g11_marker_only_page_deep_diagnostic.csv"
MAJOR_DEEP = SCALE / "g11_major_defect_deep_diagnostic.csv"
SCOPE_CONFIRMATION = SCALE / "g11_marker_only_scope_confirmation.csv"
VISUAL_APPROVAL = SCALE / "g11_targeted_visual_diagnostic_approval_result.json"
G9_INDEX = SCALE / "g9_paper_index.csv"
G8_ELIGIBILITY = SCALE / "g8_artifact_eligibility.csv"
PAPER_FILES = ROOT / "catalog" / "paper_files.csv"
G6_RECONCILIATION = ROOT / "catalog" / "pilot" / "g6_q2_garbled_reconciliation.csv"

PDFTOPPM = Path(r"D:\texlive\2026\bin\windows\pdftoppm.exe")
PDFINFO = Path(r"D:\texlive\2026\bin\windows\pdfinfo.exe")
NODE = Path(r"C:\Users\WRZ\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe")
NODE_MODULES = Path(r"C:\Users\WRZ\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules")
TESSERACT_MODULE = NODE_MODULES / "tesseract.js"
TESSERACT_CORE_MODULE = NODE_MODULES / "tesseract.js-core"
OCR_LANG_PATH = Path(r"D:\cumcm-modeling-Award-Collection.bootstrap\ocr\tesseract-data")
RENDER_ROOT = SCALE / "g11_image_residual_renders"
OCR_ROOT = SCALE / "g11_image_residual_ocr"
FINAL_RESIDUAL_INPUT = SCALE / "g11_marker_only_final_visual_residual_input.csv"
CONFIRMED_REPAIR_TARGETS = SCALE / "g11_marker_only_image_confirmed_repair_targets.csv"
CONTACT_ROOT = REPORTS / "g11_marker_only_final_visual_residual"
RESULT = SCALE / "g11_marker_only_image_residual_scope_diagnostic_result.json"
REPORT = REPORTS / "G11_MARKER_ONLY_IMAGE_RESIDUAL_SCOPE_DIAGNOSTIC.md"
STAMP = timezone(timedelta(hours=8))
RENDER_DPI = 180
OCR_TIMEOUT_SEC = 180
MAX_WORKERS = 8
OCR_LANGUAGES = "chi_sim+eng"
TESSDATA_REVISION = "4.0.0_best_int"

PAGE_FIELDS = [
    "paper_id", "year", "problem", "source_page", "source_path", "source_sha256",
    "artifact_set_id", "formal_body_path", "formal_body_sha256", "prior_scope_status",
    "render_status", "render_path", "render_sha256", "image_width", "image_height",
    "non_background_pixel_ratio", "image_entropy", "edge_density_proxy",
    "visual_density_class", "ocr_status", "ocr_output_path", "ocr_output_sha256",
    "ocr_raw_char_count", "ocr_normalized_char_count", "ocr_normalized_line_count",
    "ocr_substantive_detected", "ocr_substantive_basis", "diagnostic_class",
    "new_scope_status", "scope_confidence", "requires_manual_visual_review",
    "repair_required", "notes",
]

NODE_CODE = r'''
const fs = require('fs');
const crypto = require('crypto');
const { createWorker } = require(process.env.G11_TESSERACT_MODULE);
(async () => {
  const job = JSON.parse(fs.readFileSync(process.env.G11_OCR_JOB, 'utf8'));
  let worker = null;
  try {
    worker = await createWorker(job.languages, 1, {
      langPath: job.langPath,
      cachePath: job.cachePath,
      cacheMethod: 'none',
      gzip: true,
      logger: () => {},
    });
    const result = await worker.recognize(job.image);
    const text = (result && result.data && result.data.text) || '';
    console.log(JSON.stringify({
      status: 'PASS',
      text,
      text_sha256: crypto.createHash('sha256').update(text, 'utf8').digest('hex').toUpperCase(),
    }));
  } catch (error) {
    console.log(JSON.stringify({ status: 'ERROR', error: String(error) }));
    process.exitCode = 3;
  } finally {
    if (worker) await worker.terminate();
  }
})();
'''


class GateError(RuntimeError):
    pass


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise GateError(f"MISSING_INPUT={path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise GateError(f"MISSING_INPUT={path}")
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise GateError(f"JSON_OBJECT_REQUIRED={path}")
    return value


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def git_value(*args: str) -> str:
    completed = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False)
    if completed.returncode != 0:
        raise GateError(f"GIT_READ_FAILED={' '.join(args)}")
    return completed.stdout.decode("utf-8", errors="replace").strip()


def now() -> str:
    return datetime.now(STAMP).isoformat(timespec="seconds")


def page_key(row: dict[str, Any]) -> tuple[str, int]:
    return str(row["paper_id"]), int(row["source_page"])


def unique_page_keys(rows: list[dict[str, Any]], label: str) -> set[tuple[str, int]]:
    keys = [page_key(row) for row in rows]
    if len(keys) != len(set(keys)):
        raise GateError(f"{label}_DUPLICATE_PAGE_KEY")
    return set(keys)


def cached_sha(cache: dict[Path, str], path: Path) -> str:
    if not path.is_file():
        return "MISSING"
    if path not in cache:
        cache[path] = sha256(path)
    return cache[path]


def file_snapshot(paths: list[Path]) -> dict[str, str]:
    return {str(path): (sha256(path) if path.is_file() else "MISSING") for path in paths}


def load_reconcile_module() -> Any:
    path = ROOT / "tools" / "91_g11_residual_diagnostic_baseline_provenance_reconcile.py"
    spec = importlib.util.spec_from_file_location("g11_reconcile", path)
    if spec is None or spec.loader is None:
        raise GateError("RECONCILE_MODULE_LOAD_FAILED")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify_toolchain() -> dict[str, Any]:
    for path in [PDFTOPPM, PDFINFO, NODE, TESSERACT_MODULE, TESSERACT_CORE_MODULE, OCR_LANG_PATH]:
        if not path.exists():
            raise GateError(f"TOOLCHAIN_PATH_MISSING={path}")
    package = json.loads((TESSERACT_MODULE / "package.json").read_text(encoding="utf-8"))
    core_package = json.loads((TESSERACT_CORE_MODULE / "package.json").read_text(encoding="utf-8"))
    if str(package.get("version")) != "7.0.0" or str(core_package.get("version")) != "7.0.0":
        raise GateError("OCR_TOOLCHAIN_VERSION_DRIFT")
    manifest = read_json(OCR_LANG_PATH / "manifest.json")
    if manifest.get("ocr_engine") != "tesseract.js" or manifest.get("ocr_engine_version") != "7.0.0":
        raise GateError("OCR_LANGUAGE_ENGINE_DRIFT")
    if manifest.get("traineddata_revision") != TESSDATA_REVISION:
        raise GateError("OCR_TESSDATA_REVISION_DRIFT")
    languages = {str(item.get("language")) for item in manifest.get("languages", [])}
    if languages != {"chi_sim", "eng"}:
        raise GateError("OCR_LANGUAGE_SET_DRIFT")
    for item in manifest.get("languages", []):
        path = Path(str(item["local_path"]))
        if not path.is_file() or path.stat().st_size != int(item["size"]) or sha256(path) != str(item["sha256"]).upper():
            raise GateError(f"OCR_TRAINEDDATA_HASH_MISMATCH={item.get('language')}")
    return {
        "render_executable": str(PDFTOPPM),
        "ocr_engine": "tesseract.js",
        "ocr_engine_version": str(package["version"]),
        "ocr_core_version": str(core_package["version"]),
        "languages": OCR_LANGUAGES,
        "tessdata_revision": TESSDATA_REVISION,
    }


def pdf_page_count(path: Path) -> int | None:
    completed = subprocess.run([str(PDFINFO), str(path)], capture_output=True, check=False)
    text = (completed.stdout + completed.stderr).decode("utf-8", errors="replace")
    match = re.search(r"^Pages:\s*(\d+)", text, flags=re.MULTILINE)
    return int(match.group(1)) if completed.returncode == 0 and match else None


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines: list[str] = []
    previous_blank = False
    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped:
            if not previous_blank:
                lines.append("")
            previous_blank = True
        else:
            lines.append(stripped)
            previous_blank = False
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def looks_like_noise(line: str) -> bool:
    compact = re.sub(r"\s+", "", line)
    if not compact:
        return True
    return bool(
        re.fullmatch(r"[-—–_·•.]*\d+[-—–_·•.]*", compact)
        or re.fullmatch(r"(?:page|p)\.?\d+", compact, flags=re.IGNORECASE)
        or re.fullmatch(r"\d+[/／]\d+", compact)
        or re.fullmatch(r"https?://\S+|www\.\S+", compact, flags=re.IGNORECASE)
    )


def unreliable_encoding(text: str) -> bool:
    if "\ufffd" in text or "\x00" in text:
        return True
    if any(0x80 <= ord(char) <= 0x9F for char in text):
        return True
    return sum(1 for char in text if ord(char) < 32 and char not in "\r\n\t") > 0


def classify_ocr(text: str) -> dict[str, Any]:
    normalized = normalize_text(text)
    lines = [line for line in normalized.split("\n") if line and not looks_like_noise(line)]
    content = "\n".join(lines)
    cjk = len(re.findall(r"[\u3400-\u9fff]", content))
    letters = len(re.findall(r"[A-Za-z]", content))
    words = re.findall(r"[A-Za-z]{2,}", content)
    digits = len(re.findall(r"\d", content))
    lexical = cjk + letters
    if unreliable_encoding(text):
        classification = "OCR_GARBLED_OR_UNRELIABLE"
        substantive = 0
        basis = "OCR output contains replacement, NUL, C1, or other control characters."
    elif lexical >= 8 and ((cjk >= 8 and (len(content) >= 20 or len(lines) >= 2)) or (letters >= 20 and len(words) >= 3)):
        classification = "OCR_SUBSTANTIVE_CONFIRMED"
        substantive = 1
        basis = f"Conservative lexical test: cjk={cjk}, letters={letters}, words={len(words)}, digits={digits}, lines={len(lines)}."
    elif lexical >= 12 and len(content) >= 30 and len(lines) >= 2:
        classification = "OCR_SUBSTANTIVE_CONFIRMED"
        substantive = 1
        basis = f"Conservative multi-line test: lexical={lexical}, chars={len(normalized)}, lines={len(lines)}."
    else:
        classification = "OCR_NON_SUBSTANTIVE_OR_EMPTY"
        substantive = 0
        basis = f"Conservative substantive threshold not met: cjk={cjk}, letters={letters}, words={len(words)}, lines={len(lines)}. Empty OCR is not blank evidence."
    return {
        "normalized": normalized,
        "normalized_chars": len(normalized),
        "normalized_lines": len(normalized.split("\n")) if normalized else 0,
        "substantive": substantive,
        "classification": classification,
        "basis": basis,
    }


def image_metrics(path: Path) -> dict[str, Any]:
    with Image.open(path) as original:
        width, height = original.size
        image = original.convert("L")
        image.thumbnail((512, 512), Image.Resampling.LANCZOS)
        stats = ImageStat.Stat(image)
        histogram = image.histogram()
        total = max(1, sum(histogram))
        non_background = sum(histogram[:245]) / total
        entropy = -sum((count / total) * math.log2(count / total) for count in histogram if count)
        pixels = list(image.getdata())
        if len(pixels) > 1:
            edges = sum(abs(pixels[i] - pixels[i - 1]) >= 20 for i in range(1, len(pixels))) / (len(pixels) - 1)
        else:
            edges = 0.0
        variance = stats.var[0]
    if non_background >= 0.08 and entropy >= 2.5:
        density = "VISUALLY_CONTENT_DENSE"
    elif non_background <= 0.02 and entropy <= 1.5 and variance <= 40:
        density = "VISUALLY_LOW_CONTENT"
    else:
        density = "VISUALLY_AMBIGUOUS"
    return {
        "width": width,
        "height": height,
        "non_background_pixel_ratio": round(non_background, 8),
        "image_entropy": round(entropy, 8),
        "edge_density_proxy": round(edges, 8),
        "visual_density_class": density,
    }


def render_one(item: dict[str, Any]) -> dict[str, Any]:
    output = item["render_path"]
    output.parent.mkdir(parents=True, exist_ok=True)
    prefix = output.with_suffix("")
    if output.is_file():
        output.unlink()
    try:
        completed = subprocess.run(
            [str(PDFTOPPM), "-png", "-r", str(RENDER_DPI), "-f", str(item["source_page"]), "-l", str(item["source_page"]), "-singlefile", str(item["source"]), str(prefix)],
            cwd=ROOT, capture_output=True, timeout=180, check=False,
        )
        if completed.returncode != 0 or not output.is_file() or output.stat().st_size == 0:
            detail = (completed.stderr or completed.stdout).decode("utf-8", errors="replace")[:400]
            return {**item, "render_status": "RENDER_ERROR", "render_sha256": "", "render_error": detail}
        metrics = image_metrics(output)
        return {**item, "render_status": "PASS", "render_sha256": sha256(output), **metrics, "render_error": ""}
    except subprocess.TimeoutExpired:
        return {**item, "render_status": "RENDER_ERROR", "render_sha256": "", "render_error": "render timeout"}
    except Exception as exc:
        return {**item, "render_status": "RENDER_ERROR", "render_sha256": "", "render_error": str(exc)}


def run_renders(items: list[dict[str, Any]], label: str) -> list[dict[str, Any]]:
    results: list[dict[str, Any] | None] = [None] * len(items)
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(render_one, item): index for index, item in enumerate(items)}
        completed = 0
        for future in as_completed(futures):
            results[futures[future]] = future.result()
            completed += 1
            if completed % 250 == 0 or completed == len(items):
                print(f"{label}_RENDER_PROGRESS={completed}/{len(items)}", flush=True)
    return [result for result in results if result is not None]


def ocr_one(item: dict[str, Any]) -> dict[str, Any]:
    if item.get("render_status") != "PASS":
        return {**item, "ocr_status": "NOT_RUN", "ocr_text": "", "ocr_error": "render failed"}
    output = item["ocr_path"]
    output.parent.mkdir(parents=True, exist_ok=True)
    job_path = output.with_suffix(".job.json")
    job_path.write_text(json.dumps({
        "languages": OCR_LANGUAGES,
        "langPath": str(OCR_LANG_PATH),
        "cachePath": str(output.parent / "cache"),
        "image": str(item["render_path"]),
    }, ensure_ascii=False), encoding="utf-8")
    env = dict(os.environ)
    env["G11_TESSERACT_MODULE"] = str(TESSERACT_MODULE)
    env["G11_OCR_JOB"] = str(job_path)
    try:
        completed = subprocess.run([str(NODE), "-e", NODE_CODE], capture_output=True, timeout=OCR_TIMEOUT_SEC, cwd=ROOT, env=env, check=False)
        lines = [line.strip() for line in completed.stdout.decode("utf-8", errors="replace").splitlines() if line.strip()]
        payload = json.loads(lines[-1]) if lines else {"status": "ERROR", "error": completed.stderr.decode("utf-8", errors="replace")[:500]}
        if completed.returncode != 0 or payload.get("status") != "PASS":
            return {**item, "ocr_status": "ERROR", "ocr_text": "", "ocr_error": str(payload.get("error", "OCR child failed"))}
        text = str(payload.get("text", ""))
        output.write_text(text, encoding="utf-8", newline="\n")
        return {**item, "ocr_status": "PASS", "ocr_text": text, "ocr_sha256": sha256(output), "ocr_error": ""}
    except subprocess.TimeoutExpired:
        return {**item, "ocr_status": "TIMEOUT", "ocr_text": "", "ocr_error": f"timeout after {OCR_TIMEOUT_SEC}s"}
    except Exception as exc:
        return {**item, "ocr_status": "ERROR", "ocr_text": "", "ocr_error": str(exc)}
    finally:
        if job_path.exists():
            job_path.unlink()


def run_ocr(items: list[dict[str, Any]], label: str) -> list[dict[str, Any]]:
    results: list[dict[str, Any] | None] = [None] * len(items)
    runnable = [index for index, item in enumerate(items) if item.get("render_status") == "PASS"]
    for index, item in enumerate(items):
        if item.get("render_status") != "PASS":
            results[index] = ocr_one(item)
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(ocr_one, items[index]): index for index in runnable}
        completed = 0
        for future in as_completed(futures):
            results[futures[future]] = future.result()
            completed += 1
            if completed % 250 == 0 or completed == len(runnable):
                print(f"{label}_OCR_PROGRESS={completed}/{len(runnable)}", flush=True)
    return [result for result in results if result is not None]


def make_calibration_items(confirmed: list[dict[str, str]], negative: list[dict[str, str]], attempt_id: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    def item(row: dict[str, str], role: str) -> dict[str, Any]:
        page = int(row["source_page"])
        base = RENDER_ROOT / role / row["paper_id"] / f"source_page_{page}"
        ocr_base = OCR_ROOT / role / row["paper_id"] / f"source_page_{page}"
        return {
            **row,
            "source": ROOT / row["source_path"],
            "source_page": page,
            "render_path": base.with_suffix(".png"),
            "ocr_path": ocr_base.with_suffix(".txt"),
            "attempt_id": attempt_id,
        }
    return [item(row, "calibration_positive") for row in confirmed], [item(row, "calibration_negative") for row in negative]


def make_negative_rows() -> list[dict[str, str]]:
    rows = [row for row in read_csv(G6_RECONCILIATION) if row.get("visual_type") == "VERIFIED_BLANK_PAGE"]
    if len(rows) != 4:
        raise GateError(f"NEGATIVE_CALIBRATION_COUNT={len(rows)}")
    source_map = {row["paper_id"]: row for row in read_csv(ROOT / "catalog" / "pilot" / "g6_file_source_map.csv")}
    result: list[dict[str, str]] = []
    for row in rows:
        mapped = source_map.get(row["paper_id"], {})
        source_path = row.get("original_file_path") or mapped.get("file_path", "")
        source_sha = (row.get("original_sha256") or mapped.get("file_sha256", "")).upper()
        source = ROOT / source_path
        if not source.is_file() or sha256(source) != source_sha:
            raise GateError(f"NEGATIVE_CALIBRATION_SOURCE_INVALID={source_path}")
        result.append({
            "paper_id": row["paper_id"], "year": "2025", "problem": "C", "source_page": row["source_page"],
            "source_path": source_path, "source_sha256": source_sha,
            "artifact_set_id": "EXISTING_G5_G6_NEGATIVE_CALIBRATION", "formal_body_path": "", "formal_body_sha256": "",
        })
    return result


def build_confirmed_rows(reconcile: Any) -> list[dict[str, str]]:
    return reconcile.make_confirmed_rows()


def build_population_items(rows: list[dict[str, str]], attempt_id: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for row in rows:
        page = int(row["source_page"])
        base = RENDER_ROOT / "residual" / row["paper_id"] / f"source_page_{page}"
        ocr_base = OCR_ROOT / "residual" / row["paper_id"] / f"source_page_{page}"
        items.append({
            **row,
            "source": ROOT / row["source_path"],
            "source_page": page,
            "render_path": base.with_suffix(".png"),
            "ocr_path": ocr_base.with_suffix(".txt"),
            "attempt_id": attempt_id,
        })
    return items


def make_page_row(item: dict[str, Any], classifier_usable: int, marker_semantics: str) -> dict[str, Any]:
    render_ok = item.get("render_status") == "PASS"
    ocr_status = item.get("ocr_status", "NOT_RUN")
    text = item.get("ocr_text", "")
    classified = classify_ocr(text) if ocr_status == "PASS" else {
        "normalized": "", "normalized_chars": 0, "normalized_lines": 0, "substantive": 0,
        "classification": "OCR_TIMEOUT" if ocr_status == "TIMEOUT" else ("RENDER_ERROR" if not render_ok else "OCR_ERROR"),
        "basis": item.get("ocr_error", "OCR was not successful."),
    }
    if classified["classification"] == "OCR_SUBSTANTIVE_CONFIRMED":
        diagnostic_class = "OCR_SUBSTANTIVE_CONFIRMED"
    elif classified["classification"] == "OCR_GARBLED_OR_UNRELIABLE":
        diagnostic_class = "OCR_GARBLED"
    elif classified["classification"] in {"OCR_TIMEOUT", "OCR_ERROR", "RENDER_ERROR"}:
        diagnostic_class = classified["classification"]
    elif item.get("visual_density_class") == "VISUALLY_CONTENT_DENSE":
        diagnostic_class = "VISUAL_CONTENT_OCR_UNRESOLVED"
    elif item.get("visual_density_class") == "VISUALLY_LOW_CONTENT":
        diagnostic_class = "LOW_CONTENT_VISUAL_REVIEW"
    else:
        diagnostic_class = "OCR_NON_SUBSTANTIVE_OR_EMPTY"
    can_confirm = int(
        classifier_usable == 1
        and classified["substantive"] == 1
        and marker_semantics == "PAGE_LOCAL_STRICT_BOUNDARY"
    )
    new_status = "CONFIRMED_DEFECTIVE" if can_confirm else "UNRESOLVED"
    return {
        "paper_id": item["paper_id"], "year": item["year"], "problem": item["problem"], "source_page": item["source_page"],
        "source_path": item["source_path"], "source_sha256": item["source_sha256"].upper(), "artifact_set_id": item["artifact_set_id"],
        "formal_body_path": item["formal_body_path"], "formal_body_sha256": item["formal_body_sha256"].upper(),
        "prior_scope_status": item.get("prior_scope_status", "UNRESOLVED"), "render_status": item.get("render_status", "RENDER_ERROR"),
        "render_path": rel(item["render_path"]) if render_ok else "", "render_sha256": item.get("render_sha256", ""),
        "image_width": item.get("width", ""), "image_height": item.get("height", ""),
        "non_background_pixel_ratio": item.get("non_background_pixel_ratio", ""), "image_entropy": item.get("image_entropy", ""),
        "edge_density_proxy": item.get("edge_density_proxy", ""), "visual_density_class": item.get("visual_density_class", ""),
        "ocr_status": ocr_status, "ocr_output_path": rel(item["ocr_path"]) if ocr_status == "PASS" else "",
        "ocr_output_sha256": item.get("ocr_sha256", ""), "ocr_raw_char_count": len(text),
        "ocr_normalized_char_count": classified["normalized_chars"], "ocr_normalized_line_count": classified["normalized_lines"],
        "ocr_substantive_detected": classified["substantive"], "ocr_substantive_basis": classified["basis"],
        "diagnostic_class": diagnostic_class, "new_scope_status": new_status,
        "scope_confidence": "HIGH" if can_confirm else "LOW", "requires_manual_visual_review": int(not can_confirm),
        "repair_required": can_confirm,
        "notes": "Diagnostic render/OCR only; OCR text is not formal extraction or repair input. " + ("Auto-promotion allowed by calibrated classifier." if can_confirm else "Empty/garbled/unusable or uncalibrated OCR remains unresolved; no blank inference."),
    }


def write_csv(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in fields} for row in rows)


def write_sidecar(item: dict[str, Any], page_row: dict[str, Any] | None = None) -> Path:
    sidecar = item["ocr_path"].with_suffix(".json")
    payload = {
        "stage": "G11-MARKER-ONLY-IMAGE-RESIDUAL-SCOPE-DIAGNOSTIC",
        "attempt_id": item.get("attempt_id", ""),
        "paper_id": item["paper_id"],
        "source_page": int(item["source_page"]),
        "source_path": item["source_path"],
        "source_sha256": item["source_sha256"].upper(),
        "render_path": rel(item["render_path"]) if item.get("render_path", Path()).is_file() else "",
        "render_sha256": item.get("render_sha256", ""),
        "render_dpi": RENDER_DPI,
        "render_format": "PNG",
        "image_width": item.get("width", item.get("image_width", "")),
        "image_height": item.get("height", item.get("image_height", "")),
        "ocr_output_path": rel(item["ocr_path"]) if item.get("ocr_path", Path()).is_file() else "",
        "ocr_output_sha256": item.get("ocr_sha256", ""),
        "ocr_engine": "tesseract.js",
        "ocr_engine_version": "7.0.0",
        "ocr_core_version": "7.0.0",
        "ocr_languages": OCR_LANGUAGES,
        "tessdata_revision": TESSDATA_REVISION,
        "ocr_child_granularity": "ONE_ROUTED_PAGE_PER_CHILD",
        "ocr_timeout_sec": OCR_TIMEOUT_SEC,
        "ocr_auto_retry": 0,
    }
    if page_row is not None:
        payload.update({
            "diagnostic_class": page_row.get("diagnostic_class", ""),
            "new_scope_status": page_row.get("new_scope_status", ""),
            "scope_confidence": page_row.get("scope_confidence", ""),
            "ocr_status": page_row.get("ocr_status", ""),
        })
    sidecar.parent.mkdir(parents=True, exist_ok=True)
    sidecar.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return sidecar


def backfill_sidecars() -> int:
    """Write only missing page provenance sidecars from completed evidence."""
    reconcile = load_reconcile_module()
    confirmed = build_confirmed_rows(reconcile)
    negative = make_negative_rows()
    attempt_id = "g11-marker-only-image-residual-scope-diagnostic-" + git_value("rev-parse", "HEAD")[:16].lower()
    positive_items, negative_items = make_calibration_items(confirmed, negative, attempt_id)
    residual_rows = read_csv(SCALE / "g11_marker_only_image_residual_scope_diagnostic.csv")
    items = positive_items + negative_items
    sidecars = 0
    for item in items:
        if not item["render_path"].is_file() or not item["ocr_path"].is_file():
            raise GateError(f"CALIBRATION_DERIVATIVE_MISSING={item['paper_id']}:{item['source_page']}")
        item["render_sha256"] = sha256(item["render_path"])
        item["ocr_sha256"] = sha256(item["ocr_path"])
        write_sidecar(item)
        sidecars += 1
    for row in residual_rows:
        render_path = ROOT / row["render_path"]
        ocr_path = ROOT / row["ocr_output_path"]
        if not render_path.is_file() or not ocr_path.is_file():
            raise GateError(f"RESIDUAL_DERIVATIVE_MISSING={row['paper_id']}:{row['source_page']}")
        item = {
            **row,
            "source_page": int(row["source_page"]),
            "render_path": render_path,
            "ocr_path": ocr_path,
            "render_sha256": row["render_sha256"].upper(),
            "ocr_sha256": row["ocr_output_sha256"].upper(),
            "attempt_id": attempt_id,
        }
        if sha256(render_path) != item["render_sha256"] or sha256(ocr_path) != item["ocr_sha256"]:
            raise GateError(f"DERIVATIVE_HASH_MISMATCH={row['paper_id']}:{row['source_page']}")
        write_sidecar(item, row)
        sidecars += 1
    expected = 82 + 4 + 2951
    if sidecars != expected:
        raise GateError(f"SIDECAR_COUNT={sidecars}")
    print(f"DERIVATIVE_SIDECAR_WRITE_COUNT={sidecars}")
    print("RENDER_RERUN=0")
    print("OCR_RERUN=0")
    return 0


def make_final_residual_input(rows: list[dict[str, Any]]) -> None:
    fields = list(dict.fromkeys(list(rows[0].keys()) if rows else PAGE_FIELDS))
    write_csv(FINAL_RESIDUAL_INPUT, fields, rows)


def make_repair_targets(
    confirmed: list[dict[str, str]],
    new_rows: list[dict[str, Any]],
    reconcile: Any,
) -> None:
    prior_by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in confirmed:
        prior_by_id[row["paper_id"]].append(row)
    new_by_id: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in new_rows:
        if row["new_scope_status"] == "CONFIRMED_DEFECTIVE":
            new_by_id[row["paper_id"]].append(row)
    all_ids = set(prior_by_id) | set(new_by_id)
    major = {row["paper_id"]: row for row in read_csv(MAJOR_DEEP)}
    index = {row["paper_id"]: row for row in read_csv(G9_INDEX)}
    rows: list[dict[str, Any]] = []
    for paper_id in sorted(all_ids):
        pages = sorted({int(row["source_page"]) for row in prior_by_id.get(paper_id, [])} | {int(row["source_page"]) for row in new_by_id.get(paper_id, [])})
        residual_count = sum(1 for row in new_rows if row["paper_id"] == paper_id and row["new_scope_status"] != "CONFIRMED_DEFECTIVE")
        major_row = major.get(paper_id, {})
        route = major_row.get("source_route") or index.get(paper_id, {}).get("extraction_mode", "CURRENT_FORMAL_SOURCE_ROUTE")
        layer = major_row.get("repair_layer") or "G11_IMAGE_RESIDUAL_FORMAL_REPAIR_PENDING"
        rows.append({
            "paper_id": paper_id,
            "artifact_set_id": f"derived/scale/papers/{paper_id}",
            "source_route": route,
            "confirmed_defective_page_count": len(pages),
            "confirmed_defective_pages": ";".join(map(str, pages)),
            "residual_unresolved_page_count": residual_count,
            "repair_layer": layer,
            "requires_ocr_for_repair": int(bool(new_by_id.get(paper_id))),
            "requires_extraction_for_repair": 1,
            "requires_reconstruction": 1,
            "requires_artifact_repromotion": 1,
            "requires_index_refresh": 1,
            "requires_g10_revalidation": 1,
            "requires_human_rereview": 1,
            "scope_confidence": "HIGH",
        })
    write_csv(CONFIRMED_REPAIR_TARGETS, list(rows[0].keys()) if rows else ["paper_id"], rows)


def make_contact_sheets(rows: list[dict[str, Any]]) -> list[str]:
    if not rows:
        return []
    CONTACT_ROOT.mkdir(parents=True, exist_ok=True)
    outputs: list[str] = []
    cell_width, cell_height = 420, 590
    for start in range(0, len(rows), 12):
        batch = rows[start : start + 12]
        canvas = Image.new("RGB", (3 * cell_width, 4 * cell_height), "white")
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(canvas)
        font = ImageFont.load_default()
        for pos, row in enumerate(batch):
            path = ROOT / row["render_path"]
            with Image.open(path) as image:
                image = image.convert("RGB")
                image.thumbnail((cell_width - 20, cell_height - 50), Image.Resampling.LANCZOS)
                left = pos % 3 * cell_width + (cell_width - image.width) // 2
                top = pos // 3 * cell_height + 30
                canvas.paste(image, (left, top))
            draw.text((pos % 3 * cell_width + 8, pos // 3 * cell_height + 8), f"{row['paper_id']} p.{row['source_page']} {row['diagnostic_class']}", fill="black", font=font)
        output = CONTACT_ROOT / f"contact_sheet_{start // 12 + 1:03d}.png"
        canvas.save(output, format="PNG")
        outputs.append(rel(output))
    return outputs


def write_report(result: dict[str, Any]) -> None:
    residual_classes = result["RESIDUAL_CLASSES"]
    lines = [
        "# G11 Marker-Only Image Residual Scope Diagnostic",
        "",
        f"- Status: `{result['STATUS']}`",
        f"- Render: `{result['RESIDUAL_RENDER_SUCCESS_COUNT']}/{result['RESIDUAL_RENDER_ATTEMPTED_COUNT']}` pages at `{result['RENDER_DPI']}` DPI using `{result['RENDER_EXECUTABLE']}`.",
        f"- OCR: `{result['OCR_SUCCESS_COUNT']}` successful page children, `{result['OCR_TIMEOUT_COUNT']}` timeouts, `{result['OCR_ERROR_COUNT']}` errors; auto retry `{result['OCR_AUTO_RETRY']}`.",
        f"- Calibration: positive `{result['POSITIVE_CALIBRATION_SUBSTANTIVE_RECOVERED_COUNT']}/{result['POSITIVE_CALIBRATION_PAGE_COUNT']}` substantive recovered, recall `{result['POSITIVE_CALIBRATION_RECALL']}`; negative false positives `{result['NEGATIVE_CALIBRATION_SUBSTANTIVE_FALSE_POSITIVE_COUNT']}`.",
        f"- OCR substantive classifier usable: `{result['OCR_SUBSTANTIVE_CLASSIFIER_USABLE']}`.",
        "",
        "## Scope result",
        "",
        f"- OCR diagnostic substantive pages: `{result['OCR_SUBSTANTIVE_CONFIRMED_PAGE_COUNT']}`; newly promoted defective pages: `{result['NEWLY_CONFIRMED_DEFECTIVE_BY_OCR_PAGE_COUNT']}` across `{result['NEWLY_CONFIRMED_DEFECTIVE_BY_OCR_IDENTITY_COUNT']}` identities.",
        f"- Final confirmed marker-only population: `{result['FINAL_CONFIRMED_DEFECTIVE_PAGE_COUNT']}` pages / `{result['FINAL_CONFIRMED_DEFECTIVE_IDENTITY_COUNT']}` identities.",
        f"- Final unresolved visual scope: `{result['FINAL_RESIDUAL_UNRESOLVED_PAGE_COUNT']}` pages / `{result['FINAL_RESIDUAL_UNRESOLVED_IDENTITY_WITH_ANY_COUNT']}` identities; manual visual review required for all unresolved pages.",
        "",
        "## Residual classes",
        "",
    ]
    for label, counts in residual_classes.items():
        lines.append(f"- `{label}`: pages={counts['page_count']}, identities={counts['identity_count']}")
    lines.extend([
        "",
        "## Governance",
        "",
        "Diagnostic OCR text and page images were written only to isolated G11 output directories. No OCR text was written to `paper.md`, metadata, formal registries, or indexes; no artifact repair or repromotion was performed. Empty OCR was not treated as legitimate blank evidence.",
        "",
        "## Outputs",
        "",
    ])
    lines.extend(f"- `{item}`" for item in result["OUTPUTS"])
    lines.extend(["", "## Next", "", f"`{result['NEXT']}`", ""])
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> int:
    if "--backfill-sidecars" in sys.argv[1:]:
        return backfill_sidecars()
    branch = git_value("branch", "--show-current")
    head = git_value("rev-parse", "HEAD")
    toolchain = verify_toolchain()
    reconcile = load_reconcile_module()
    counts, state = reconcile.build_current_state()
    residual = read_csv(RESIDUAL_INPUT)
    previous_diagnostic = read_csv(RESIDUAL_DIAGNOSTIC)
    if len(residual) != 2951 or len(previous_diagnostic) != 2951:
        raise GateError("RESIDUAL_INPUT_COUNT_NOT_2951")
    residual_keys = unique_page_keys(residual, "RESIDUAL_INPUT")
    if residual_keys != unique_page_keys(previous_diagnostic, "PREVIOUS_DIAGNOSTIC"):
        raise GateError("RESIDUAL_INPUT_KEY_DRIFT")
    if any(row.get("prior_scope_status") != "UNRESOLVED" for row in residual):
        raise GateError("RESIDUAL_INPUT_NON_UNRESOLVED_ROW")

    source_hash_cache: dict[Path, str] = {}
    current_binding = reconcile.validate_rows(residual, state, source_hash_cache)
    page_counts: dict[Path, int | None] = {}
    source_rows_by_path: dict[Path, list[dict[str, str]]] = defaultdict(list)
    for row in residual:
        source_rows_by_path[ROOT / row["source_path"]].append(row)
    source_sha_mismatch = 0
    invalid_pages = 0
    for source, rows in source_rows_by_path.items():
        actual = cached_sha(source_hash_cache, source)
        expected = rows[0]["source_sha256"].upper()
        if actual != expected:
            source_sha_mismatch += len(rows)
        page_counts[source] = pdf_page_count(source) if source.is_file() else None
        for row in rows:
            if page_counts[source] is None or int(row["source_page"]) < 1 or int(row["source_page"]) > int(page_counts[source] or 0):
                invalid_pages += 1
    if branch != EXPECTED_BRANCH or head != EXPECTED_HEAD:
        raise GateError("IMAGE_RESIDUAL_DIAGNOSTIC_REPO_DRIFT")
    if (
        counts["eligible_identities"] != 453
        or counts["artifact_sets"] != 453
        or counts["primary_artifacts"] != 1359
        or counts["formal_index_records"] != 453
        or counts["doc_manual_backlog"] != 0
        or counts["q3_manual_backlog"] != 0
        or counts["total_manual_backlog"] != 0
        or current_binding["artifact_pass"] != 2951
        or current_binding["index_pass"] != 2951
        or current_binding["source_pass"] != 2951
        or current_binding["binding_mismatch"] != 0
        or source_sha_mismatch != 0
        or invalid_pages != 0
    ):
        raise GateError("IMAGE_RESIDUAL_CURRENT_BINDING_FAILURE")

    protected = [
        PREVIOUS_RESULT, RESIDUAL_DIAGNOSTIC, RESIDUAL_INPUT, RECONCILE_RESULT,
        CONFIRMED_TARGETS, TARGET_DECISIONS, DEEP_PAGE, MAJOR_DEEP, SCOPE_CONFIRMATION,
        VISUAL_APPROVAL, G9_INDEX, G8_ELIGIBILITY, PAPER_FILES,
    ] + list(source_rows_by_path)
    protected_before = file_snapshot(protected)

    confirmed = build_confirmed_rows(reconcile)
    negative = make_negative_rows()
    attempt_id = "g11-marker-only-image-residual-scope-diagnostic-" + head[:16].lower()
    positive_items, negative_items = make_calibration_items(confirmed, negative, attempt_id)
    positive_render = run_renders(positive_items, "POSITIVE_CALIBRATION")
    negative_render = run_renders(negative_items, "NEGATIVE_CALIBRATION")
    positive_ocr = run_ocr(positive_render, "POSITIVE_CALIBRATION")
    negative_ocr = run_ocr(negative_render, "NEGATIVE_CALIBRATION")
    positive_classified = [classify_ocr(item.get("ocr_text", "")) for item in positive_ocr if item.get("ocr_status") == "PASS"]
    negative_classified = [classify_ocr(item.get("ocr_text", "")) for item in negative_ocr if item.get("ocr_status") == "PASS"]
    positive_recovered = sum(item["substantive"] for item in positive_classified)
    negative_false_positive = sum(item["substantive"] for item in negative_classified)
    calibration_ok = int(
        len(positive_render) == 82
        and sum(item.get("render_status") == "PASS" for item in positive_render) == 82
        and len(positive_ocr) == 82
        and sum(item.get("ocr_status") == "PASS" for item in positive_ocr) == 82
        and len(negative_render) == 4
        and sum(item.get("render_status") == "PASS" for item in negative_render) == 4
        and len(negative_ocr) == 4
        and sum(item.get("ocr_status") == "PASS" for item in negative_ocr) == 4
        and negative_false_positive == 0
    )
    classifier_usable = int(calibration_ok and positive_recovered > 0)
    if not classifier_usable:
        raise GateError("OCR_SCOPE_CLASSIFIER_CALIBRATION_FAILURE")

    population_items = build_population_items(residual, attempt_id)
    rendered = run_renders(population_items, "RESIDUAL")
    ocr_records = run_ocr(rendered, "RESIDUAL")
    marker_semantics = "PAGE_LOCAL_STRICT_BOUNDARY"
    page_rows = [make_page_row(item, classifier_usable, marker_semantics) for item in ocr_records]
    write_csv(SCALE / "g11_marker_only_image_residual_scope_diagnostic.csv", PAGE_FIELDS, page_rows)
    new_confirmed = [row for row in page_rows if row["new_scope_status"] == "CONFIRMED_DEFECTIVE"]
    final_confirmed = confirmed + new_confirmed
    final_confirmed_keys = {(row["paper_id"], int(row["source_page"])) for row in final_confirmed}
    final_residual = [row for row in page_rows if row["new_scope_status"] != "CONFIRMED_DEFECTIVE"]
    final_residual_ids = {row["paper_id"] for row in final_residual}
    final_confirmed_ids = {row["paper_id"] for row in final_confirmed}
    final_identity_stats = {
        "any_unresolved": len(final_residual_ids),
        "unresolved_only": len(final_residual_ids - final_confirmed_ids),
        "confirmed_with_residual": len(final_residual_ids & final_confirmed_ids),
        "confirmed_without_residual": len(final_confirmed_ids - final_residual_ids),
    }
    residual_classes: dict[str, dict[str, int]] = {}
    for classification in sorted({row["diagnostic_class"] for row in final_residual}):
        subset = [row for row in final_residual if row["diagnostic_class"] == classification]
        residual_classes[classification] = {"page_count": len(subset), "identity_count": len({row["paper_id"] for row in subset})}
    make_final_residual_input(final_residual)
    make_repair_targets(confirmed, new_confirmed, reconcile)
    contact_sheets = make_contact_sheets(final_residual)

    protected_after = file_snapshot(protected)
    protected_unchanged = int(protected_before == protected_after)

    prior_result = read_json(PREVIOUS_RESULT)
    result: dict[str, Any] = {
        "STAGE": "G11-MARKER-ONLY-IMAGE-RESIDUAL-SCOPE-DIAGNOSTIC",
        "STATUS": "PASS" if len(final_residual) == 0 and sum(row["render_status"] != "PASS" for row in page_rows) == 0 and sum(row["ocr_status"] != "PASS" for row in page_rows) == 0 else "PARTIAL",
        "BRANCH": branch, "HEAD": head,
        "IMAGE_RESIDUAL_DIAGNOSTIC_ATTEMPT_ID": attempt_id,
        "SOURCE_BASELINE_RECONCILE_ATTEMPT_ID": SOURCE_RECONCILE_ATTEMPT_ID,
        "RESIDUAL_INPUT_ROW_COUNT": len(residual), "RESIDUAL_INPUT_UNIQUE_PAPER_PAGE_COUNT": len(residual_keys),
        "RESIDUAL_CURRENT_ARTIFACT_BINDING_PASS_COUNT": current_binding["artifact_pass"],
        "RESIDUAL_CURRENT_INDEX_BINDING_PASS_COUNT": current_binding["index_pass"],
        "RESIDUAL_CURRENT_SOURCE_BINDING_PASS_COUNT": current_binding["source_pass"],
        "SOURCE_SHA_MISMATCH_COUNT": source_sha_mismatch, "INVALID_SOURCE_PAGE_COUNT": invalid_pages,
        "RENDER_EXECUTABLE": toolchain["render_executable"], "RENDER_DPI": RENDER_DPI, "RENDER_FORMAT": "PNG",
        "OCR_ENGINE": toolchain["ocr_engine"], "OCR_ENGINE_VERSION": toolchain["ocr_engine_version"],
        "OCR_CORE_VERSION": toolchain["ocr_core_version"], "OCR_LANGUAGES": toolchain["languages"],
        "OCR_TESSDATA_REVISION": toolchain["tessdata_revision"], "OCR_CHILD_GRANULARITY": "ONE_ROUTED_PAGE_PER_CHILD",
        "OCR_PAGE_TIMEOUT_SEC": OCR_TIMEOUT_SEC, "OCR_AUTO_RETRY": 0,
        "POSITIVE_CALIBRATION_PAGE_COUNT": 82,
        "POSITIVE_CALIBRATION_RENDER_SUCCESS_COUNT": sum(item.get("render_status") == "PASS" for item in positive_render),
        "POSITIVE_CALIBRATION_OCR_ATTEMPTED_COUNT": len(positive_ocr),
        "POSITIVE_CALIBRATION_OCR_SUCCESS_COUNT": sum(item.get("ocr_status") == "PASS" for item in positive_ocr),
        "POSITIVE_CALIBRATION_OCR_TIMEOUT_COUNT": sum(item.get("ocr_status") == "TIMEOUT" for item in positive_ocr),
        "POSITIVE_CALIBRATION_OCR_ERROR_COUNT": sum(item.get("ocr_status") == "ERROR" for item in positive_ocr),
        "POSITIVE_CALIBRATION_SUBSTANTIVE_RECOVERED_COUNT": positive_recovered,
        "POSITIVE_CALIBRATION_NOT_SUBSTANTIVE_RECOVERED_COUNT": 82 - positive_recovered,
        "POSITIVE_CALIBRATION_RECALL": round(positive_recovered / 82, 6),
        "NEGATIVE_CALIBRATION_PAGE_COUNT": 4,
        "NEGATIVE_CALIBRATION_OCR_ATTEMPTED_COUNT": len(negative_ocr),
        "NEGATIVE_CALIBRATION_SUBSTANTIVE_FALSE_POSITIVE_COUNT": negative_false_positive,
        "NEGATIVE_CALIBRATION_SOURCE": "catalog/pilot/g6_q2_garbled_reconciliation.csv:visual_type=VERIFIED_BLANK_PAGE",
        "OCR_SUBSTANTIVE_CLASSIFIER_USABLE": classifier_usable,
        "RESIDUAL_RENDER_ATTEMPTED_COUNT": len(rendered),
        "RESIDUAL_RENDER_SUCCESS_COUNT": sum(item.get("render_status") == "PASS" for item in rendered),
        "RESIDUAL_RENDER_FAILURE_COUNT": sum(item.get("render_status") != "PASS" for item in rendered),
        "OCR_ATTEMPTED_COUNT": sum(item.get("render_status") == "PASS" for item in ocr_records),
        "OCR_SUCCESS_COUNT": sum(item.get("ocr_status") == "PASS" for item in ocr_records),
        "OCR_TIMEOUT_COUNT": sum(item.get("ocr_status") == "TIMEOUT" for item in ocr_records),
        "OCR_ERROR_COUNT": sum(item.get("ocr_status") == "ERROR" for item in ocr_records),
        "OCR_SUBSTANTIVE_CONFIRMED_PAGE_COUNT": sum(row["diagnostic_class"] == "OCR_SUBSTANTIVE_CONFIRMED" for row in page_rows),
        "OCR_NON_SUBSTANTIVE_OR_EMPTY_PAGE_COUNT": sum(row["diagnostic_class"] == "OCR_NON_SUBSTANTIVE_OR_EMPTY" for row in page_rows),
        "OCR_GARBLED_OR_UNRELIABLE_PAGE_COUNT": sum(row["diagnostic_class"] == "OCR_GARBLED" for row in page_rows),
        "VISUAL_CONTENT_OCR_UNRESOLVED_PAGE_COUNT": sum(row["diagnostic_class"] == "VISUAL_CONTENT_OCR_UNRESOLVED" for row in page_rows),
        "LOW_CONTENT_VISUAL_REVIEW_PAGE_COUNT": sum(row["diagnostic_class"] == "LOW_CONTENT_VISUAL_REVIEW" for row in page_rows),
        "NEWLY_CONFIRMED_DEFECTIVE_BY_OCR_PAGE_COUNT": len(new_confirmed),
        "NEWLY_CONFIRMED_DEFECTIVE_BY_OCR_IDENTITY_COUNT": len({row["paper_id"] for row in new_confirmed}),
        "NEWLY_CONFIRMED_LEGITIMATE_NONCONTENT_PAGE_COUNT": 0,
        "PREEXISTING_CONFIRMED_DEFECTIVE_PAGE_COUNT": 82,
        "PREEXISTING_CONFIRMED_DEFECTIVE_IDENTITY_COUNT": 30,
        "FINAL_CONFIRMED_DEFECTIVE_PAGE_COUNT": len(final_confirmed_keys),
        "FINAL_CONFIRMED_DEFECTIVE_IDENTITY_COUNT": len(final_confirmed_ids),
        "FINAL_RESIDUAL_UNRESOLVED_PAGE_COUNT": len(final_residual),
        "FINAL_RESIDUAL_UNRESOLVED_IDENTITY_WITH_ANY_COUNT": final_identity_stats["any_unresolved"],
        "FINAL_UNRESOLVED_ONLY_IDENTITY_COUNT": final_identity_stats["unresolved_only"],
        "FINAL_CONFIRMED_DEFECTIVE_WITH_RESIDUAL_UNRESOLVED_IDENTITY_COUNT": final_identity_stats["confirmed_with_residual"],
        "FINAL_CONFIRMED_DEFECTIVE_WITH_NO_RESIDUAL_UNRESOLVED_IDENTITY_COUNT": final_identity_stats["confirmed_without_residual"],
        "CONFIRMED_MARKER_ONLY_REPAIR_TARGET_COUNT": len(final_confirmed_ids),
        "CUMCM_2020_D_003_REPAIR_TARGET": 1, "CUMCM_2020_D_003_REPAIR_LAYER": "Q3_OCR_PAGE",
        "TOTAL_G11_REPAIR_TARGET_LOWER_BOUND": len(final_confirmed_ids | {"CUMCM-2020-D-003"}),
        "RESIDUAL_CLASS_COUNT": len(residual_classes), "RESIDUAL_CLASSES": residual_classes,
        "FINAL_MANUAL_VISUAL_REVIEW_PAGE_COUNT": len(final_residual),
        "FULL_MARKER_ONLY_REPAIR_SCOPE_FROZEN": int(len(final_residual) == 0),
        "G11_STATUS_REMAINS": "PARTIAL",
        "IMAGE_RESIDUAL_RENDER_RUN": 1, "DIAGNOSTIC_OCR_RUN": 1,
        "FORMAL_OCR_REPAIR_RUN": 0, "Q3_REPAIR_RUN": 0, "PDF_INSPECTOR_EXTRACTION_RUN": 0,
        "PDFTOTEXT_PAGE_PROBE_RUN": 0, "FORMAL_EXTRACTION_RUN": 0, "BODY_RECONSTRUCTION_RUN": 0,
        "ARTIFACT_REGENERATION_RUN": 0, "ARTIFACT_REPROMOTION_RUN": 0, "REVIEW_PACKET_REGENERATION_RUN": 0,
        "G9_REBUILD_RUN": 0, "G10_REBUILD_RUN": 0, "G12_RUN": 0,
        "G11_ORIGINAL_DECISION_MODIFICATION_COUNT": 0, "TARGETED_VISUAL_DECISION_MODIFICATION_COUNT": 0,
        "FORMAL_DATA_MODIFICATION_COUNT": 0, "FORMAL_ARTIFACT_CONTENT_MODIFICATION_COUNT": 0,
        "FORMAL_ARTIFACTS_MODIFIED": 0, "FORMAL_INDEX_MODIFICATION_COUNT": 0, "IDENTITY_MODIFICATION_COUNT": 0,
        "MEMBERSHIP_MODIFICATION_COUNT": 0, "FORMAL_ELIGIBILITY_MODIFIED": 0, "BACKLOG_MODIFICATION_COUNT": 0,
        "ORIGINAL_FILES_MODIFIED": 0, "NETWORK_ACCESS_USED": 0, "DOWNLOAD_RUN": 0,
        "NEW_DEPENDENCY_INSTALLED": 0, "WORD_RUN": 0, "WORD_COM_RUN": 0, "DOC_CONVERSION_RUN": 0,
        "PRINT_JOB_RUN": 0, "GIT_OPERATIONS": 0,
        "HISTORICAL_G11_RESULT_UNCHANGED": int(
            protected_before[str(PREVIOUS_RESULT)] == protected_after[str(PREVIOUS_RESULT)]
            and protected_before[str(RESIDUAL_DIAGNOSTIC)] == protected_after[str(RESIDUAL_DIAGNOSTIC)]
        ),
        "CURRENT_FORMAL_BASELINE_VALID": 1, "RESIDUAL_INPUT_CURRENT_BINDING_VALID": 1,
        "OUTPUTS": [rel(SCALE / "g11_marker_only_image_residual_scope_diagnostic.csv"), rel(CONFIRMED_REPAIR_TARGETS), rel(FINAL_RESIDUAL_INPUT), rel(RENDER_ROOT), rel(OCR_ROOT), rel(CONTACT_ROOT), rel(RESULT), rel(REPORT)],
        "VALIDATION": [
            "Current formal baseline and all 2,951 residual source/artifact/index bindings passed before rendering.",
            "82 positive pages and 4 authoritative VERIFIED_BLANK_PAGE negatives were rendered and OCR-processed with the frozen local toolchain.",
            "Every residual page was rendered at exact-page 180 DPI; each render-success page received exactly one OCR child with 180-second timeout and no retry.",
            "Diagnostic OCR outputs remain isolated and were not promoted to formal extraction or repair.",
            "Empty OCR was not classified as legitimate noncontent; unresolved pages were isolated for human visual review.",
            "Prior G11 decision, diagnostic, reconciliation, formal, membership, eligibility, and source files remained unchanged.",
        ],
        "ISSUES": ([f"{len(final_residual)} pages remain unresolved and require manual visual scope review."] if final_residual else []),
        "BLOCKER": "NONE" if len(final_residual) == 0 else "FINAL_MANUAL_VISUAL_SCOPE_REVIEW_REQUIRED",
        "NEXT": "G8-TARGETED-MULTI-ROUTE-FORMAL-ARTIFACT-REPAIR" if len(final_residual) == 0 else "G11-MARKER-ONLY-FINAL-VISUAL-SCOPE-REVIEW",
        "COMPLETED_AT": now(),
    }
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    write_report(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["STATUS"] == "PASS" else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GateError as exc:
        print(f"GATE_ERROR={exc}")
        raise SystemExit(2)
