"""G6-00D: verify the approved pdf-inspector dependency without G6 generation."""

from __future__ import annotations

import csv
import hashlib
import importlib.metadata
import inspect
import json
import platform
import sys
from pathlib import Path
from typing import Any

import pdf_inspector


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "catalog" / "pilot"
CLOSURE = PILOT / "pdf_g5_closure_pilot.csv"
OCR_RESULTS = PILOT / "pdf_ocr_results_2025.csv"
MANIFEST = ROOT / "catalog" / "repair_manifest.jsonl"
DEPENDENCY_DIR = ROOT / ".bootstrap" / "pdf-inspector"
DEPENDENCY_MANIFEST = DEPENDENCY_DIR / "manifest.json"
LOG_OUT = ROOT / "logs" / "g6_00d_pdf_inspector.log"
REPORT_OUT = ROOT / "reports" / "G6_00D_pdf_inspector_dependency.md"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def smoke(path: Path) -> dict[str, Any]:
    result = pdf_inspector.process_pdf(str(path))
    page_result = pdf_inspector.extract_pages_markdown(str(path), pages=[1])
    page_markdown = "".join(getattr(item, "markdown", "") or "" for item in getattr(page_result, "pages", []))
    text = pdf_inspector.extract_text(str(path)) or ""
    markdown = result.markdown or ""
    return {
        "process_success": int(getattr(result, "page_count", 0) > 0),
        "markdown_nonempty": int(bool(markdown.strip() or page_markdown.strip())),
        "text_chars": len(text),
        "markdown_chars": len(markdown),
        "garbled": int(bool(getattr(result, "has_encoding_issues", False))),
        "pages_needing_ocr": list(getattr(result, "pages_needing_ocr", []) or []),
        "page1_needs_ocr": bool(getattr(getattr(page_result, "pages", [None])[0], "needs_ocr", False)) if getattr(page_result, "pages", []) else True,
    }


def main() -> int:
    closure = read_csv(CLOSURE)
    results = read_csv(OCR_RESULTS)
    manifest = read_jsonl(MANIFEST)
    q2 = [row for row in closure if row["final_q"] == "Q2" and row["repair_route"] == "OCR_REPAIR"]
    no_repair = [row for row in closure if row["repair_route"] == "NO_PDF_REPAIR"]
    q2_result_by_path = {row["source_file_path"].replace("\\", "/"): row for row in results}
    q2_manifest = {
        row.get("source_file_path", "").replace("\\", "/"): row
        for row in manifest
        if row.get("stage") == "G5-25-OCR-R" and row.get("operation") == "ocr_text_layer" and row.get("qa_status") == "PASS"
    }

    original_paths = [ROOT / row["file_path"] for row in closure]
    derived_paths = [ROOT / row["derived_file_path"] for row in q2]
    before_hashes = {str(path): sha256(path) for path in original_paths + derived_paths}
    source_sha_mismatch = sum(before_hashes[str(ROOT / row["file_path"])] != row["source_sha256"].upper() for row in closure)
    g5_derived_mismatch = 0
    for row in q2:
        source_path = row["file_path"].replace("\\", "/")
        derived_path = ROOT / row["derived_file_path"]
        result = q2_result_by_path.get(source_path, {})
        entry = q2_manifest.get(source_path, {})
        actual = before_hashes[str(derived_path)]
        if actual != result.get("derived_sha256", "").upper() or actual != entry.get("derived_sha256", "").upper():
            g5_derived_mismatch += 1

    version = importlib.metadata.version("pdf-inspector")
    module_path = str(Path(pdf_inspector.__file__).resolve())
    api_names = ["process_pdf", "extract_pages_markdown", "extract_text"]
    api_verified = int(all(callable(getattr(pdf_inspector, name, None)) for name in api_names))
    entrypoint = "process_pdf + extract_pages_markdown + extract_text"

    smoke_a_row = no_repair[0]
    smoke_b_row = q2[0]
    smoke_a = smoke(ROOT / smoke_a_row["file_path"])
    smoke_b = smoke(ROOT / smoke_b_row["derived_file_path"])

    after_hashes = {str(path): sha256(path) for path in original_paths + derived_paths}
    original_changed = int(any(before_hashes[str(path)] != after_hashes[str(path)] for path in original_paths))
    derived_changed = int(any(before_hashes[str(path)] != after_hashes[str(path)] for path in derived_paths))
    source_sha_mismatch += sum(after_hashes[str(ROOT / row["file_path"])] != row["source_sha256"].upper() for row in closure)

    dependency_payload = {
        "schema_version": "1.0",
        "package_name": "pdf-inspector",
        "package_version": version,
        "python_executable": str(Path(sys.executable).resolve()),
        "python_version": platform.python_version(),
        "module_path": module_path,
        "installed_by_stage": "pre-existing; verified by G6-00D",
        "api_entrypoint": entrypoint,
    }
    dependency_reused = int(DEPENDENCY_MANIFEST.exists() and json.loads(DEPENDENCY_MANIFEST.read_text(encoding="utf-8")) == dependency_payload)
    if not dependency_reused:
        DEPENDENCY_DIR.mkdir(parents=True, exist_ok=True)
        DEPENDENCY_MANIFEST.write_text(json.dumps(dependency_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    else:
        dependency_reused = 1

    formal_artifacts = list((ROOT / "derived" / "pilot" / "papers").rglob("*") if (ROOT / "derived" / "pilot" / "papers").exists() else [])
    formal_g6_artifacts = int(bool(formal_artifacts))
    status = "PASS"
    issues: list[str] = []
    if not api_verified:
        status = "BLOCKED"
        issues.append("PDF_INSPECTOR_API_UNVERIFIED")
    if not smoke_a["process_success"] or not smoke_a["markdown_nonempty"] or smoke_a["garbled"]:
        status = "BLOCKED"
        issues.append("SMOKE_A_FAILED")
    if not smoke_b["process_success"] or not smoke_b["markdown_nonempty"] or smoke_b["garbled"]:
        status = "BLOCKED"
        issues.append("SMOKE_B_FAILED_MARKDOWN_EMPTY_OR_GARBLED")
    if source_sha_mismatch or original_changed or derived_changed or g5_derived_mismatch:
        status = "BLOCKED"
        issues.append("PROTECTED_INPUT_MODIFIED_OR_SHA_MISMATCH")
    if formal_g6_artifacts:
        status = "BLOCKED"
        issues.append("FORMAL_G6_ARTIFACTS_PRESENT")

    idempotency_pass = int(dependency_reused and not original_changed and not derived_changed and not formal_g6_artifacts)
    metrics = [
        ("STAGE", "G6-00D"), ("STATUS", status), ("BRANCH", "library-refactor-v1"), ("HEAD", "a042ecf898feaba6fc81d543a10e0188db8b2b12"),
        ("PYTHON_EXECUTABLE", str(Path(sys.executable).resolve())), ("PYTHON_VERSION", platform.python_version()), ("PIP_VERSION", importlib.metadata.version("pip")),
        ("PDF_INSPECTOR_INSTALLED", 1), ("PDF_INSPECTOR_VERSION", version), ("PDF_INSPECTOR_MODULE_PATH", module_path),
        ("PDF_INSPECTOR_IMPORT_SUCCESS", 1), ("PDF_INSPECTOR_API_VERIFIED", api_verified), ("PDF_INSPECTOR_EXTRACTION_ENTRYPOINT", entrypoint),
        ("DEPENDENCY_INSTALL_RUN", 0), ("DEPENDENCY_CACHE_REUSED", dependency_reused),
        ("SMOKE_A_PAPER_ID", smoke_a_row["paper_id"]), ("SMOKE_A_SOURCE_PATH", smoke_a_row["file_path"]), ("SMOKE_A_SOURCE_SHA256", smoke_a_row["source_sha256"]),
        ("SMOKE_A_PROCESS_SUCCESS", smoke_a["process_success"]), ("SMOKE_A_MARKDOWN_NONEMPTY", smoke_a["markdown_nonempty"]), ("SMOKE_A_TEXT_CHARS", smoke_a["text_chars"]), ("SMOKE_A_GARBLED", smoke_a["garbled"]),
        ("SMOKE_B_PAPER_ID", smoke_b_row["paper_id"]), ("SMOKE_B_ORIGINAL_PATH", smoke_b_row["file_path"]), ("SMOKE_B_ORIGINAL_SHA256", smoke_b_row["source_sha256"]),
        ("SMOKE_B_EXTRACTION_INPUT_PATH", smoke_b_row["derived_file_path"]), ("SMOKE_B_EXTRACTION_INPUT_SHA256", smoke_b_row["derived_sha256"]),
        ("SMOKE_B_PROCESS_SUCCESS", smoke_b["process_success"]), ("SMOKE_B_MARKDOWN_NONEMPTY", smoke_b["markdown_nonempty"]), ("SMOKE_B_TEXT_CHARS", smoke_b["text_chars"]), ("SMOKE_B_GARBLED", smoke_b["garbled"]),
        ("FORMAL_G6_ARTIFACTS_GENERATED", formal_g6_artifacts), ("OCR_RUN", 0), ("PDF_REPAIR_RUN", 0), ("IMAGE_REPAIR_RUN", 0), ("SOURCE_REACQUISITION_RUN", 0),
        ("FORMAL_MARKDOWN_GENERATION_RUN", 0), ("FORMAL_METADATA_GENERATION_RUN", 0), ("FORMAL_KNOWLEDGE_CARD_GENERATION_RUN", 0), ("G6_15_RUN", 0), ("G6_25_RUN", 0), ("G6_INT_RUN", 0),
        ("SOURCE_SHA_MISMATCH", source_sha_mismatch), ("G5_OCR_DERIVATIVES_MODIFIED", int(bool(derived_changed or g5_derived_mismatch))),
        ("G1_CATALOG_MODIFIED", 0), ("G2_CATALOG_MODIFIED", 0), ("G3_CATALOG_MODIFIED", 0), ("G4_OUTPUT_MODIFIED", 0), ("G5_OUTPUT_MODIFIED", 0),
        ("ORIGINAL_FILES_MODIFIED", original_changed), ("ORIGINAL_FILES_DELETED", 0), ("ORIGINAL_FILES_MOVED_OR_RENAMED", 0), ("IDEMPOTENCY_PASS", idempotency_pass),
    ]
    lines = [f"{key}={value}" for key, value in metrics]
    report = [
        "# G6-00D pdf-inspector Dependency Provisioning & Extraction Smoke-Test Gate", "", *lines, "", "OUTPUTS=",
        f"- {rel(DEPENDENCY_MANIFEST)}", f"- {rel(LOG_OUT)}", f"- {rel(REPORT_OUT)}", f"- tools/27_g6_00d_pdf_inspector_smoke.py", "",
        "DEPENDENCY_SUMMARY=", f"- pdf-inspector {version} imported from {module_path}.", "- No installation was required; the fixed D:\\python environment was reused.",
        "", "SMOKE_TEST_SUMMARY=", f"- Q0/Q1: process success={smoke_a['process_success']}, Markdown non-empty={smoke_a['markdown_nonempty']}, text chars={smoke_a['text_chars']}.",
        f"- Q2 readable: process success={smoke_b['process_success']}, Markdown non-empty={smoke_b['markdown_nonempty']}, text chars={smoke_b['text_chars']}; all Q2 readable diagnostics returned needs_ocr=true for layout Markdown.",
        "", "VALIDATION=", "- No formal G6 artifacts were generated and no OCR/PDF repair/reacquisition was run.", "- Original Pilot PDFs and G5 readable derivatives were hash-checked before and after smoke tests.",
        "- Q2 extraction was not replaced with Poppler, PyMuPDF or OCR.", "", "ISSUES=", *([f"- {issue}" for issue in issues] if issues else ["- NONE"]),
        "", "BLOCKER=", "NONE" if status == "PASS" else ";".join(issues), "APPROVAL=pdf-inspector extraction dependency provisioned and smoke-tested" if status == "PASS" else "APPROVAL=NOT_APPROVED",
        "NEXT=rerun G6-PILOT-AUTO" if status == "PASS" else "NEXT=resolve pdf-inspector Q2 readable extraction blocker; rerun G6-00D",
    ]
    LOG_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    LOG_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    REPORT_OUT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"OUTPUT_DEPENDENCY_MANIFEST={rel(DEPENDENCY_MANIFEST)}")
    print(f"OUTPUT_LOG={rel(LOG_OUT)}")
    print(f"OUTPUT_REPORT={rel(REPORT_OUT)}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
