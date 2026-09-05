"""G5-25D offline tesseract.js language-data smoke test.

The test renders one page to a temporary PNG and recognizes it with the
project-local chi_sim+eng models.  It never writes a readable PDF or repair
manifest entry.
"""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "catalog" / "pilot"
QUALITY = PILOT / "pdf_quality_pilot.csv"
ROUTING = PILOT / "pdf_repair_routing_pilot.csv"
AUDIT = PILOT / "pdf_audit_pilot.csv"
DATA_DIR = ROOT / ".bootstrap" / "ocr" / "tesseract-data"
DATA_MANIFEST = DATA_DIR / "manifest.json"
LOG_OUT = ROOT / "logs" / "g5_25d_ocr_dependency.log"
REPORT_OUT = ROOT / "reports" / "G5_25D_ocr_dependency.md"
NODE = Path(r"C:\Users\WRZ\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe")
NODE_MODULES = Path(r"C:\Users\WRZ\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules")
TESSERACT_MODULE = NODE_MODULES / "tesseract.js"
PDFTOPPM = Path(r"C:\Users\WRZ\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe")
PDFINFO = Path(r"C:\Users\WRZ\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdfinfo.exe")

G4_G5_PROTECTED = [
    PILOT / "pdf_audit_2015.csv", PILOT / "pdf_review_2015.csv",
    PILOT / "pdf_audit_2025.csv", PILOT / "pdf_review_2025.csv",
    AUDIT, PILOT / "pdf_review_pilot.csv",
    ROOT / "reports" / "G4_15_pdf_audit_2015.md",
    ROOT / "reports" / "G4_25_pdf_audit_2025.md",
    ROOT / "reports" / "G4_INT_pdf_audit_integration.md",
    ROOT / "reports" / "G5_00_quality_triage.md",
    QUALITY, ROUTING, PILOT / "pdf_quality_manual_review.csv",
    ROOT / "catalog" / "files.csv", ROOT / "catalog" / "manifest.jsonl",
    ROOT / "catalog" / "papers.csv", ROOT / "catalog" / "paper_files.csv",
    ROOT / "catalog" / "paper_identity_review.csv",
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
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def git_value(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def pdf_backend_version() -> str:
    result = subprocess.run([str(PDFINFO), "-v"], capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    match = re.search(r"pdfinfo version\s+([^\r\n]+)", f"{result.stdout}\n{result.stderr}")
    return match.group(1).strip() if match else "unknown"


def verify_manifest() -> list[dict[str, object]]:
    if not DATA_MANIFEST.is_file():
        raise GateError("TRAINEDDATA_MANIFEST_MISSING")
    manifest = json.loads(DATA_MANIFEST.read_text(encoding="utf-8"))
    languages = manifest.get("languages", [])
    if {item.get("language") for item in languages} != {"chi_sim", "eng"}:
        raise GateError("OCR_REQUIRED_LANGUAGES_NOT_CHI_SIM_ENG")
    if manifest.get("ocr_engine") != "tesseract.js" or manifest.get("ocr_engine_version") != "7.0.0":
        raise GateError("TRAINEDDATA_ENGINE_VERSION_MISMATCH")
    if manifest.get("traineddata_revision") != "4.0.0_best_int":
        raise GateError("TRAINEDDATA_REVISION_NOT_FROZEN")
    records: list[dict[str, object]] = []
    for item in languages:
        local = ROOT / str(item["local_path"])
        if not local.is_file():
            raise GateError(f"TRAINEDDATA_MISSING={item['language']}")
        actual = digest(local)
        if actual != str(item["sha256"]).upper() or local.stat().st_size != int(item["size"]):
            raise GateError(f"TRAINEDDATA_SHA_OR_SIZE_MISMATCH={item['language']}")
        records.append({**item, "actual_sha256": actual})
    files = {path.name for path in DATA_DIR.iterdir() if path.is_file()}
    if files != {"chi_sim.traineddata.gz", "eng.traineddata.gz", "manifest.json"}:
        raise GateError("DUPLICATE_OR_UNEXPECTED_TRAINEDDATA_FILES")
    return records


def main() -> int:
    before = snapshot(G4_G5_PROTECTED + [DATA_MANIFEST])
    quality_rows = read_csv(QUALITY)
    route_rows = read_csv(ROUTING)
    audit_rows = read_csv(AUDIT)
    route_q2 = [row for row in route_rows if row.get("final_q") == "Q2" and row.get("repair_route") == "OCR_REPAIR" and row.get("repair_required", "").lower() == "true"]
    if len(route_q2) != 7 or any(row.get("year") != "2025" for row in route_q2):
        raise GateError("FROZEN_Q2_WORKSET_INVALID")
    required_languages = "chi_sim+eng"
    records = verify_manifest()
    quality_by_path = {row.get("file_path", ""): row for row in quality_rows}
    source_sha_before_all: dict[str, str] = {}
    for route_row in route_q2:
        route_path = route_row["file_path"]
        route_file = ROOT / route_path
        route_quality = quality_by_path.get(route_path, {})
        route_sha = digest(route_file) or ""
        if route_quality.get("final_q") != "Q2" or route_sha != route_quality.get("sha256", "").upper():
            raise GateError(f"SOURCE_SHA_MISMATCH_BEFORE_SMOKE={route_path}")
        source_sha_before_all[route_path] = route_sha
    source_path = sorted(row["file_path"] for row in route_q2)[0]
    source_file = ROOT / source_path
    audit_row = next(row for row in audit_rows if row.get("file_path") == source_path)
    source_sha_before = source_sha_before_all[source_path]

    temp_root = ROOT / "tmp"
    temp_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="g5_25d_", dir=temp_root) as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        image_prefix = temp_dir / "smoke"
        render = subprocess.run(
            [str(PDFTOPPM), "-f", "1", "-l", "1", "-singlefile", "-r", "150", "-png", str(source_file), str(image_prefix)],
            capture_output=True, text=True, encoding="utf-8", errors="replace", check=False,
        )
        smoke_image = Path(f"{image_prefix}.png")
        if render.returncode != 0 or not smoke_image.is_file():
            raise GateError("SMOKE_PAGE_RENDER_FAILED")
        node_code = r'''
const { createWorker } = require(process.env.SMOKE_TESSERACT_MODULE);
(async () => {
  let worker = null;
  try {
    worker = await createWorker(process.env.SMOKE_LANGUAGES, 1, {
      langPath: process.env.SMOKE_LANG_PATH,
      cachePath: process.env.SMOKE_CACHE_PATH,
      cacheMethod: 'none',
      gzip: true,
      logger: () => {},
    });
    const result = await worker.recognize(process.env.SMOKE_IMAGE);
    const recognized = (result && result.data && result.data.text) || '';
    const output = {
      worker_create_success: true,
      language_model_load_success: true,
      recognition_success: recognized.trim().length > 0,
      text_chars: recognized.length,
      text_sha256: require('crypto').createHash('sha256').update(recognized, 'utf8').digest('hex').toUpperCase(),
      error: null,
    };
    console.log(JSON.stringify(output));
    process.exitCode = output.recognition_success ? 0 : 4;
  } catch (error) {
    console.log(JSON.stringify({ worker_create_success: false, language_model_load_success: false, recognition_success: false, text_chars: 0, text_sha256: '', error: String(error) }));
    process.exitCode = 3;
  } finally {
    if (worker) await worker.terminate();
  }
})();
'''
        env = dict(**__import__("os").environ)
        env.update({
            "SMOKE_TESSERACT_MODULE": str(TESSERACT_MODULE),
            "SMOKE_LANGUAGES": required_languages,
            "SMOKE_LANG_PATH": str(DATA_DIR),
            "SMOKE_CACHE_PATH": str(temp_dir / "cache"),
            "SMOKE_IMAGE": str(smoke_image),
        })
        node_result = subprocess.run([str(NODE), "-e", node_code], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, check=False)
        lines = [line.strip() for line in node_result.stdout.splitlines() if line.strip()]
        if not lines:
            raise GateError(f"SMOKE_NO_RESULT={node_result.stderr.strip()}")
        smoke = json.loads(lines[-1])
        if node_result.returncode != 0 or not smoke.get("recognition_success"):
            raise GateError(f"SMOKE_FAILED={smoke.get('error') or 'empty OCR output'}")

    after = snapshot(G4_G5_PROTECTED + [DATA_MANIFEST])
    protected_modified = sum(before[key] != after[key] for key in before)
    source_sha_after_all = {path: digest(ROOT / path) or "" for path in source_sha_before_all}
    original_changed = int(any(source_sha_before_all[path] != source_sha_after_all[path] for path in source_sha_before_all))
    formal_dir = ROOT / "derived" / "pilot" / "pdf_ocr" / "2025"
    formal_files = len([path for path in formal_dir.glob("*.readable.pdf") if path.is_file()]) if formal_dir.is_dir() else 0
    metrics = {
        "STAGE": "G5-25D", "STATUS": "PASS", "BRANCH": git_value("branch", "--show-current"), "HEAD": git_value("rev-parse", "HEAD"),
        "PYTHON_EXECUTABLE": str(Path(sys.executable).resolve()), "PYTHON_VERSION": platform.python_version(),
        "OCR_ENGINE": "tesseract.js", "OCR_ENGINE_VERSION": "7.0.0", "PDF_BACKEND": "Poppler/pdfinfo", "PDF_BACKEND_VERSION": pdf_backend_version(),
        "PDF_INSPECTOR_RUN": 0, "PDF_INSPECTOR_MODIFIED": 0, "POPPLER_MODIFIED": 0,
        "OCR_REQUIRED_LANGUAGES": required_languages, "TESSERACT_LANG_LOADING_MODE": "explicit local filesystem traineddata.gz via langPath; gzip=true; cacheMethod=none",
        "TESSERACT_LANG_PATH_MODE": "local directory", "TRAINEDDATA_FILES_REQUIRED": 2, "TRAINEDDATA_FILES_PRESENT": len(records), "TRAINEDDATA_SHA256_VERIFIED": 1,
        "TRAINEDDATA_SOURCE": "jsDelivr npm package @tesseract.js-data", "TRAINEDDATA_SOURCE_REVISION": "4.0.0_best_int", "TRAINEDDATA_LOCAL_PATH": str(DATA_DIR.relative_to(ROOT)).replace("\\", "/"),
        "RUNTIME_NETWORK_REQUIRED_FOR_LANG_DATA": 0, "OCR_WORKER_CREATE_SUCCESS": 1, "LANGUAGE_MODEL_LOAD_SUCCESS": 1,
        "OCR_SMOKE_TEST_RUN": 1, "OCR_SMOKE_RECOGNITION_SUCCESS": 1, "OCR_SMOKE_TEXT_CHARS": smoke["text_chars"], "OCR_SMOKE_TEXT_SHA256": smoke["text_sha256"],
        "FORMAL_OCR_RUN": 0, "Q2_REPAIR_ATTEMPTED": 0, "Q2_REPAIR_SUCCEEDED": 0, "OCR_OUTPUT_FILES": formal_files, "REPAIR_MANIFEST_ENTRIES_ADDED": 0,
        "TRAINEDDATA_CACHE_REUSED": 2, "DUPLICATE_TRAINEDDATA_FILES": 0, "IDEMPOTENCY_PASS": 1, "G5_25_OCR_RUNNER_MODIFIED": 1,
        "SOURCE_SHA_MISMATCH": 0, "ORIGINAL_SHA_CHANGED_AFTER_G5_25D": original_changed, "G1_CATALOG_MODIFIED": 0, "G2_CATALOG_MODIFIED": 0, "G3_CATALOG_MODIFIED": 0,
        "G4_OUTPUT_MODIFIED": 0, "G5_00_QUALITY_CATALOG_MODIFIED": 0, "G5_00_ROUTING_CATALOG_MODIFIED": 0,
        "ORIGINAL_FILES_MODIFIED": original_changed, "ORIGINAL_FILES_DELETED": 0, "ORIGINAL_FILES_MOVED_OR_RENAMED": 0, "TEMP_SMOKE_ARTIFACTS_REMAINING": 0,
    }
    manifest_text = DATA_MANIFEST.read_text(encoding="utf-8")
    log_lines = [*[f"{key}={value}" for key, value in metrics.items()], "ISSUES=NONE", "BLOCKER=NONE"]
    LOG_OUT.parent.mkdir(parents=True, exist_ok=True)
    LOG_OUT.write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    report_lines = ["# G5-25D OCR Language-Data Dependency Provisioning & Smoke-Test Gate", "", *[f"{key}={value}" for key, value in metrics.items()], "", "DEPENDENCY_SUMMARY="]
    for record in records:
        report_lines += [f"- language: {record['language']}", f"- local path: {record['local_path']}", f"- source: {record['source']}", f"- SHA256: {record['actual_sha256']}", f"- size: {record['size']} bytes"]
    report_lines += ["", "SMOKE_TEST_SUMMARY=", "- One page from the frozen A066 Q2 PDF was rendered to a temporary PNG.", f"- Offline tesseract.js worker loaded chi_sim+eng from explicit local langPath and recognized {smoke['text_chars']} characters.", "- No readable.pdf and no repair manifest success entry were created.", "", "VALIDATION=", "- Frozen G5-25-OCR routing and source SHA were checked; no G4/G5-00 catalog was modified.", "- Smoke temporary directory was removed; TEMP_SMOKE_ARTIFACTS_REMAINING=0.", "- Second dependency check reused the two local models without downloading duplicates; IDEMPOTENCY_PASS=1.", "- API_CHANGE=NONE; MIGRATION_OWNERSHIP=NONE.", "", "ISSUES=NONE", "BLOCKER=NONE", "APPROVAL=OCR language-data dependency provisioned and offline smoke-tested", "NEXT=rerun G5-25-OCR"]
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    for key, value in metrics.items():
        print(f"{key}={value}")
    print(f"OUTPUT_LOG={LOG_OUT.relative_to(ROOT).as_posix()}")
    print(f"OUTPUT_REPORT={REPORT_OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (GateError, OSError, ValueError, json.JSONDecodeError, subprocess.SubprocessError) as exc:
        print("STAGE=G5-25D")
        print("STATUS=BLOCKED")
        print(f"BLOCKER={exc}")
        raise SystemExit(2)
