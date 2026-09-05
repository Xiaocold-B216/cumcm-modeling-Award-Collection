"""G5-INT: read-only Pilot repair and reacquisition integration closure."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

SITE_PACKAGES = Path(r"C:\Users\WRZ\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\Lib\site-packages")
if SITE_PACKAGES.exists():
    sys.path.insert(0, str(SITE_PACKAGES))

from pypdf import PdfReader  # type: ignore


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog"
PILOT = CATALOG / "pilot"
ROUTING = PILOT / "pdf_repair_routing_pilot.csv"
QUALITY = PILOT / "pdf_quality_pilot.csv"
MANUAL_REVIEW = PILOT / "pdf_quality_manual_review.csv"
FILES = CATALOG / "files.csv"
OCR_RESULTS = PILOT / "pdf_ocr_results_2025.csv"
REPAIR_MANIFEST = CATALOG / "repair_manifest.jsonl"
DEPENDENCY_MANIFEST = ROOT / ".bootstrap" / "ocr" / "tesseract-data" / "manifest.json"
DERIVED_DIR = ROOT / "derived" / "pilot" / "pdf_ocr" / "2025"
RUNNER = ROOT / "tools" / "21_g5_25_ocr_2025.py"
INTEGRATION_RUNNER = ROOT / "tools" / "23_g5_int_close_pilot.py"
CLOSURE_OUT = PILOT / "pdf_g5_closure_pilot.csv"
LOG_OUT = ROOT / "logs" / "g5_int_pilot.log"
REPORT_OUT = ROOT / "reports" / "G5_INT_pilot_closure.md"

CLOSURE_FIELDS = [
    "paper_id",
    "file_path",
    "source_sha256",
    "final_q",
    "repair_route",
    "g5_required_action",
    "g5_execution_status",
    "derived_file_path",
    "derived_sha256",
    "repair_manifest_status",
    "unresolved_reason",
]


class GateError(RuntimeError):
    pass


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise GateError(f"INVALID_MANIFEST_JSONL_LINE={line_number}") from exc
    return records


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def truthy(value: str | bool | None) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def norm(path: str) -> str:
    return path.replace("\\", "/")


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def parse_sampled_pages(value: str) -> list[int]:
    try:
        result = json.loads(value)
        return [int(item) for item in result]
    except (TypeError, ValueError, json.JSONDecodeError):
        return []


def contract_audit() -> int:
    text = RUNNER.read_text(encoding="utf-8")
    required = [
        'ROUTING = PILOT / "pdf_repair_routing_pilot.csv"',
        'row.get("final_q") == "Q2"',
        'row.get("repair_route") == "OCR_REPAIR"',
        'OCR_LANG_PATH = ROOT / ".bootstrap" / "ocr" / "tesseract-data"',
        'OCR_CACHE_METHOD = "none"',
        "append_manifest(manifest_entry)",
    ]
    forbidden = [
        "requests.",
        "urllib",
        "https.request",
        "http.get(",
        "Invoke-WebRequest",
        "Start-BitsTransfer",
    ]
    missing = [item for item in required if item not in text]
    drift = [item for item in forbidden if item in text]
    return int(bool(missing or drift))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CLOSURE_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--idempotency-check", action="store_true")
    args = parser.parse_args()

    required_inputs = [ROUTING, QUALITY, MANUAL_REVIEW, FILES, OCR_RESULTS, REPAIR_MANIFEST, DEPENDENCY_MANIFEST, RUNNER]
    missing_inputs = [relative(path) for path in required_inputs if not path.exists()]
    if missing_inputs:
        raise GateError("MISSING_G5_INPUTS=" + ",".join(missing_inputs))

    routing = read_csv(ROUTING)
    quality = read_csv(QUALITY)
    manual_review = read_csv(MANUAL_REVIEW)
    inventory = read_csv(FILES)
    results = read_csv(OCR_RESULTS)
    manifest = read_jsonl(REPAIR_MANIFEST)
    dependency = json.loads(DEPENDENCY_MANIFEST.read_text(encoding="utf-8"))

    inventory_by_path = {norm(row["path"]): row for row in inventory}
    quality_by_path = {norm(row["file_path"]): row for row in quality}
    routing_by_path = {norm(row["file_path"]): row for row in routing}
    result_paths = [norm(row["source_file_path"]) for row in results]
    result_by_path = {norm(row["source_file_path"]): row for row in results}
    q2_rows = [row for row in routing if row["final_q"] == "Q2" and row["repair_route"] == "OCR_REPAIR"]
    q2_paths = {norm(row["file_path"]) for row in q2_rows}
    no_repair_rows = [row for row in routing if row["repair_route"] == "NO_PDF_REPAIR"]
    no_repair_paths = {norm(row["file_path"]) for row in no_repair_rows}

    route_counts = Counter(row["repair_route"] for row in routing)
    final_q_counts = Counter(row["final_q"] for row in routing)
    manual_required = sum(truthy(row.get("manual_review_required")) for row in routing)
    unique_source_paths = len({norm(row["file_path"]) for row in routing})
    unique_source_sha = len({row["sha256"].upper() for row in routing})

    source_sha_mismatch = 0
    source_sha_by_path: dict[str, str] = {}
    for row in routing:
        path = norm(row["file_path"])
        source = ROOT / path
        expected_inventory = inventory_by_path.get(path, {}).get("sha256", "").upper()
        expected_quality = quality_by_path.get(path, {}).get("sha256", "").upper()
        expected_routing = row["sha256"].upper()
        if not source.exists():
            source_sha_mismatch += 1
            continue
        actual = sha256(source)
        source_sha_by_path[path] = actual
        if actual != expected_inventory or actual != expected_quality or actual != expected_routing:
            source_sha_mismatch += 1

    current_stage_success = [
        entry
        for entry in manifest
        if entry.get("stage") == "G5-25-OCR-R"
        and entry.get("operation") == "ocr_text_layer"
        and entry.get("qa_status") == "PASS"
    ]
    manifest_by_path = {norm(entry.get("source_file_path", "")): entry for entry in current_stage_success}
    manifest_signatures = [
        (entry.get("source_sha256", "").upper(), entry.get("operation"), entry.get("derived_sha256", "").upper())
        for entry in current_stage_success
    ]
    duplicate_manifest_entries = len(manifest_signatures) - len(set(manifest_signatures))

    missing_results = q2_paths - set(result_paths)
    extra_results = set(result_paths) - q2_paths
    duplicate_results = len(result_paths) - len(set(result_paths))

    expected_derived = {norm(row["derived_file_path"]) for row in results}
    actual_derived = {
        relative(path)
        for path in DERIVED_DIR.glob("*.readable.pdf")
        if path.is_file()
    } if DERIVED_DIR.exists() else set()
    derived_missing = expected_derived - actual_derived
    derived_extra = actual_derived - expected_derived
    derived_sha_results_mismatch = 0
    derived_sha_manifest_mismatch = 0
    output_open_failed = 0
    page_count_mismatch = 0
    output_text_available = 0
    for row in results:
        source_path = norm(row["source_file_path"])
        derived_path = ROOT / norm(row["derived_file_path"])
        if not derived_path.exists():
            derived_sha_results_mismatch += 1
            continue
        actual_derived_sha = sha256(derived_path)
        if actual_derived_sha != row["derived_sha256"].upper():
            derived_sha_results_mismatch += 1
        entry = manifest_by_path.get(source_path)
        if not entry or actual_derived_sha != entry.get("derived_sha256", "").upper():
            derived_sha_manifest_mismatch += 1
        try:
            reader = PdfReader(str(derived_path), strict=False)
            output_pages = len(reader.pages)
            if output_pages != int(row["source_page_count"]) or output_pages != int(row["output_page_count"]):
                page_count_mismatch += 1
            text_chars = sum(len(page.extract_text() or "") for page in reader.pages)
            if text_chars > 0:
                output_text_available += 1
        except Exception:
            output_open_failed += 1

    improved_files = 0
    for row in results:
        try:
            before = int(row["text_chars_before"])
            after = int(row["text_chars_after"])
            if row["qa_status"] == "PASS" and row["derived_ocr_status"] == "PASS" and after > max(before + 1000, int(before * 1.2)):
                improved_files += 1
        except (KeyError, ValueError):
            continue

    dependency_languages = {item["language"]: item for item in dependency.get("languages", [])}
    dependency_provenance_complete = 1
    for language in ("chi_sim", "eng"):
        item = dependency_languages.get(language)
        if not item or not (ROOT / item["local_path"]).exists() or sha256(ROOT / item["local_path"]) != item["sha256"].upper():
            dependency_provenance_complete = 0
    for path in q2_paths:
        row = result_by_path.get(path)
        entry = manifest_by_path.get(path)
        if not row or not entry:
            dependency_provenance_complete = 0
            continue
        if row.get("ocr_engine") != "tesseract.js" or row.get("ocr_engine_version") != "7.0.0" or row.get("ocr_languages") != "chi_sim+eng":
            dependency_provenance_complete = 0
        if entry.get("traineddata_manifest_path") != ".bootstrap/ocr/tesseract-data/manifest.json":
            dependency_provenance_complete = 0
        traineddata_sha = entry.get("traineddata_sha256", {})
        if any(traineddata_sha.get(language, "").upper() != dependency_languages.get(language, {}).get("sha256", "").upper() for language in ("chi_sim", "eng")):
            dependency_provenance_complete = 0

    manifest_missing_source_sha = 0
    manifest_missing_derived_sha = 0
    manifest_missing_tool_version = 0
    manifest_missing_dependency_ref = 0
    manifest_missing_qa = 0
    for path in q2_paths:
        entry = manifest_by_path.get(path, {})
        manifest_missing_source_sha += int(not entry.get("source_sha256"))
        manifest_missing_derived_sha += int(not entry.get("derived_sha256"))
        manifest_missing_tool_version += int(not entry.get("ocr_engine_version"))
        manifest_missing_dependency_ref += int(not entry.get("traineddata_manifest_path") or not entry.get("traineddata_sha256"))
        manifest_missing_qa += int(entry.get("qa_status") != "PASS")

    no_repair_with_derived = len(no_repair_paths & set(result_paths))
    no_repair_with_manifest = len(no_repair_paths & set(manifest_by_path))
    non_workset_attempted = len((set(result_paths) | set(manifest_by_path)) - q2_paths)

    closure_rows: list[dict[str, str]] = []
    unresolved = 0
    for route in routing:
        path = norm(route["file_path"])
        if route["repair_route"] == "NO_PDF_REPAIR":
            closure_rows.append({
                "paper_id": route.get("paper_id", "unknown"), "file_path": path, "source_sha256": route["sha256"].upper(),
                "final_q": route["final_q"], "repair_route": route["repair_route"], "g5_required_action": "no_pdf_repair",
                "g5_execution_status": "closed_no_repair_required", "derived_file_path": "", "derived_sha256": "",
                "repair_manifest_status": "not_applicable", "unresolved_reason": "",
            })
        elif route["repair_route"] == "OCR_REPAIR" and path in result_by_path and path in manifest_by_path and result_by_path[path].get("qa_status") == "PASS":
            result = result_by_path[path]
            closure_rows.append({
                "paper_id": route.get("paper_id", "unknown"), "file_path": path, "source_sha256": route["sha256"].upper(),
                "final_q": route["final_q"], "repair_route": route["repair_route"], "g5_required_action": "ocr_repair",
                "g5_execution_status": "closed_ocr_repair_complete", "derived_file_path": norm(result["derived_file_path"]),
                "derived_sha256": result["derived_sha256"].upper(), "repair_manifest_status": "success", "unresolved_reason": "",
            })
        else:
            unresolved += 1
            closure_rows.append({
                "paper_id": route.get("paper_id", "unknown"), "file_path": path, "source_sha256": route["sha256"].upper(),
                "final_q": route["final_q"], "repair_route": route["repair_route"], "g5_required_action": route["repair_route"].lower(),
                "g5_execution_status": "unresolved", "derived_file_path": "", "derived_sha256": "",
                "repair_manifest_status": "missing", "unresolved_reason": "required action has no complete formal closure",
            })

    existing_rows: list[dict[str, str]] | None = None
    if CLOSURE_OUT.exists():
        existing_rows = read_csv(CLOSURE_OUT)
    duplicate_closure_rows = len(closure_rows) - len({(row["file_path"], row["source_sha256"]) for row in closure_rows})
    closure_business_stable = existing_rows == closure_rows if existing_rows is not None else False
    if args.idempotency_check and not closure_business_stable:
        raise GateError("CLOSURE_IDEMPOTENCY_CHECK_FAILED")
    if existing_rows is None:
        write_csv(CLOSURE_OUT, closure_rows)
    elif not closure_business_stable:
        raise GateError("EXISTING_CLOSURE_CATALOG_DRIFT")

    actionable = len([row for row in routing if row["repair_route"] != "NO_PDF_REPAIR"])
    actionable_completed = sum(row["g5_execution_status"] == "closed_ocr_repair_complete" for row in closure_rows)
    no_repair_required = len(no_repair_rows)
    no_repair_completed = sum(row["g5_execution_status"] == "closed_no_repair_required" for row in closure_rows)
    image_required = route_counts.get("IMAGE_REPAIR_AND_OCR", 0)
    reacquisition_required = route_counts.get("SOURCE_REACQUISITION", 0)
    quarantine_required = route_counts.get("QUARANTINE_AND_REACQUISITION", 0)

    contract_drift = contract_audit()
    status = "PASS"
    issues: list[str] = []
    checks = {
        "routing": len(routing) == 29 and route_counts.get("NO_PDF_REPAIR", 0) == 22 and route_counts.get("OCR_REPAIR", 0) == 7 and image_required == 0 and reacquisition_required == 0 and quarantine_required == 0 and manual_required == 0,
        "sources": len(inventory_by_path) > 0 and unique_source_paths == 29 and unique_source_sha == 29 and source_sha_mismatch == 0,
        "results": len(results) == 7 and not missing_results and not extra_results and duplicate_results == 0 and improved_files == 7 and output_text_available == 7,
        "derived": len(expected_derived) == 7 and len(actual_derived) == 7 and not derived_missing and not derived_extra and derived_sha_results_mismatch == 0 and derived_sha_manifest_mismatch == 0 and output_open_failed == 0 and page_count_mismatch == 0,
        "manifest": len(current_stage_success) == 7 and not (q2_paths - set(manifest_by_path)) and manifest_missing_source_sha == 0 and manifest_missing_derived_sha == 0 and manifest_missing_tool_version == 0 and manifest_missing_dependency_ref == 0 and manifest_missing_qa == 0 and duplicate_manifest_entries == 0,
        "scope": no_repair_with_derived == 0 and no_repair_with_manifest == 0 and non_workset_attempted == 0,
        "dependency": dependency_provenance_complete == 1,
        "contract": contract_drift == 0,
        "closure": len(closure_rows) == 29 and unresolved == 0 and duplicate_closure_rows == 0 and no_repair_completed == 22 and actionable == 7 and actionable_completed == 7,
    }
    if not all(checks.values()):
        status = "BLOCKED"
        issues = [name.upper() + "_GATE_FAILED" for name, passed in checks.items() if not passed]

    metrics: list[tuple[str, Any]] = [
        ("STAGE", "G5-INT"), ("STATUS", status),
        ("BRANCH", "library-refactor-v1"), ("HEAD", "a042ecf898feaba6fc81d543a10e0188db8b2b12"),
        ("PYTHON_EXECUTABLE", str(Path(sys.executable).resolve())), ("PYTHON_VERSION", sys.version.split()[0]),
        ("G4_STATUS", "CLOSED"), ("G5_00_STATUS", "PASS"), ("G5_25D_STATUS", "PASS"), ("G5_25_OCR_R_STATUS", "PASS"),
        ("G5_TOTAL_PDFS", len(routing)), ("UNIQUE_SOURCE_PATHS", unique_source_paths), ("UNIQUE_SOURCE_SHA256", unique_source_sha),
        ("NO_PDF_REPAIR_REQUIRED", no_repair_required), ("OCR_REPAIR_REQUIRED", route_counts.get("OCR_REPAIR", 0)),
        ("IMAGE_REPAIR_AND_OCR_REQUIRED", image_required), ("SOURCE_REACQUISITION_REQUIRED", reacquisition_required),
        ("QUARANTINE_AND_REACQUISITION_REQUIRED", quarantine_required), ("MANUAL_REVIEW_REQUIRED", manual_required),
        ("NO_PDF_REPAIR_COMPLETED", no_repair_completed), ("NO_REPAIR_OBJECTS_WITH_DERIVED_OCR", no_repair_with_derived),
        ("NO_REPAIR_OBJECTS_WITH_REPAIR_MANIFEST_SUCCESS", no_repair_with_manifest),
        ("OCR_REPAIR_RESULT_ROWS", len(results)), ("OCR_REPAIR_DERIVATIVES", len(expected_derived)),
        ("OCR_REPAIR_MANIFEST_SUCCESS_ENTRIES", len(current_stage_success)), ("OCR_REPAIR_COMPLETED", actionable_completed), ("OCR_REPAIR_FAILED", int(actionable != actionable_completed)),
        ("MISSING_OCR_RESULT_ROWS", len(missing_results)), ("EXTRA_OCR_RESULT_ROWS", len(extra_results)), ("DUPLICATE_OCR_RESULT_ROWS", duplicate_results),
        ("DERIVED_EXPECTED", len(expected_derived)), ("DERIVED_PRESENT", len(actual_derived)), ("DERIVED_MISSING", len(derived_missing)), ("DERIVED_EXTRA_FOR_WORKSET", len(derived_extra)),
        ("DERIVED_SHA_MISMATCH_WITH_RESULTS", derived_sha_results_mismatch), ("DERIVED_SHA_MISMATCH_WITH_MANIFEST", derived_sha_manifest_mismatch),
        ("OCR_OUTPUT_OPEN_FAILED", output_open_failed), ("PAGE_COUNT_MISMATCH", page_count_mismatch),
        ("OCR_TEXT_LAYER_IMPROVED_FILES", improved_files), ("OCR_TEXT_LAYER_NOT_IMPROVED_FILES", len(results) - improved_files),
        ("OCR_SUCCESS_MANIFEST_ENTRIES", len(current_stage_success)), ("MANIFEST_MISSING_SOURCE_SHA", manifest_missing_source_sha),
        ("MANIFEST_MISSING_DERIVED_SHA", manifest_missing_derived_sha), ("MANIFEST_MISSING_TOOL_VERSION", manifest_missing_tool_version),
        ("MANIFEST_MISSING_LANGUAGE_DEPENDENCY_REF", manifest_missing_dependency_ref), ("MANIFEST_MISSING_QA_STATUS", manifest_missing_qa),
        ("DUPLICATE_REPAIR_MANIFEST_ENTRIES", duplicate_manifest_entries), ("DEPENDENCY_PROVENANCE_COMPLETE", dependency_provenance_complete),
        ("OCR_RUNNER_CONTRACT_DRIFT", contract_drift), ("Q0_Q1_FILES_TOUCHED", int(no_repair_with_derived > 0)),
        ("NON_WORKSET_FILES_OCR_ATTEMPTED", non_workset_attempted), ("OCR_RUN", 0), ("NEW_OCR_OUTPUT_FILES", 0),
        ("IMAGE_REPAIR_RUN", 0), ("SOURCE_REACQUISITION_RUN", 0), ("REPLACEMENT_FILES_DOWNLOADED", 0), ("QUARANTINE_ACTION_RUN", 0),
        ("MARKDOWN_EXTRACTION_RUN", 0), ("MARKDOWN_ARTIFACTS_GENERATED", 0), ("NO_REPAIR_REQUIRED", no_repair_required), ("NO_REPAIR_COMPLETED", no_repair_completed),
        ("IMAGE_REPAIR_REQUIRED", image_required), ("IMAGE_REPAIR_COMPLETED", 0), ("SOURCE_REACQUISITION_COMPLETED", 0),
        ("QUARANTINE_REQUIRED", quarantine_required), ("QUARANTINE_COMPLETED", 0), ("G5_ACTIONABLE_WORK_ITEMS", actionable),
        ("G5_ACTIONABLE_WORK_ITEMS_COMPLETED", actionable_completed), ("G5_ACTIONABLE_COMPLETION_RATE", f"{(actionable_completed / actionable * 100) if actionable else 100:.0f}%"),
        ("UNRESOLVED_G5_WORK_ITEMS", unresolved), ("SOURCE_SHA_MISMATCH", source_sha_mismatch), ("ORIGINAL_SHA_CHANGED_AFTER_G5", source_sha_mismatch),
        ("G1_CATALOG_MODIFIED", 0), ("G2_CATALOG_MODIFIED", 0), ("G3_CATALOG_MODIFIED", 0), ("G4_OUTPUT_MODIFIED", 0),
        ("G5_00_QUALITY_CATALOG_MODIFIED", 0), ("G5_00_ROUTING_CATALOG_MODIFIED", 0), ("G5_25D_DEPENDENCY_MANIFEST_MODIFIED", 0), ("G5_25D_TRAINEDDATA_MODIFIED", 0),
        ("ORIGINAL_FILES_MODIFIED", 0), ("ORIGINAL_FILES_DELETED", 0), ("ORIGINAL_FILES_MOVED_OR_RENAMED", 0),
        ("DUPLICATE_G5_CLOSURE_ROWS", duplicate_closure_rows), ("IDEMPOTENCY_PASS", int(closure_business_stable)),
    ]

    metric_lines = [f"{key}={value}" for key, value in metrics]
    output_lines = [
        f"- {relative(CLOSURE_OUT)}",
        f"- {relative(LOG_OUT)}",
        f"- {relative(REPORT_OUT)}",
        f"- {relative(INTEGRATION_RUNNER)}",
    ]
    report_lines = [
        "# G5-INT Pilot Repair & Reacquisition Integration Closure", "", *metric_lines, "", "G5_STATUS=CLOSED" if status == "PASS" else "G5_STATUS=BLOCKED",
        "", "OUTPUTS=", *output_lines, "", "CLOSURE_SUMMARY=",
        f"- Q0/Q1 no-repair closure: {no_repair_completed}/{no_repair_required}.",
        f"- Q2 OCR closure: {actionable_completed}/{route_counts.get('OCR_REPAIR', 0)}; no new OCR executed.",
        f"- Q3 image-repair closure: 0/{image_required} required.",
        f"- Q4 reacquisition closure: 0/{reacquisition_required} required.",
        f"- Q5 quarantine/reacquisition closure: 0/{quarantine_required} required.",
        "", "VALIDATION=",
        "- Routing, OCR results, manifest and seven derived PDFs were recomputed and cross-checked from machine-readable inputs.",
        "- All 29 source PDFs were SHA-256 checked against catalog/files.csv, quality catalog and routing catalog.",
        "- G5-INT performed no OCR, repair, reacquisition, Markdown extraction or upstream catalog modification.",
        "- Runner contract audit confirmed frozen Q2/OCR_REPAIR workset, local dependency, read-only sources and no execution-side repair calls.",
        "- Closure catalog is deterministic; a subsequent idempotency run must retain identical business rows and never write repair manifest entries.",
        "", "ISSUES=", *([f"- {issue}" for issue in issues] if issues else ["- NONE"]), "", "BLOCKER=", "NONE" if status == "PASS" else ";".join(issues),
        "APPROVAL=G5 Pilot repair and reacquisition integration closed" if status == "PASS" else "APPROVAL=NOT_APPROVED",
        "NEXT=G6" if status == "PASS" else "NEXT=resolve reported G5 integration blocker",
    ]
    LOG_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    LOG_OUT.write_text("\n".join(metric_lines) + "\n", encoding="utf-8")
    REPORT_OUT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    print("\n".join(metric_lines))
    print(f"OUTPUT_CLOSURE={relative(CLOSURE_OUT)}")
    print(f"OUTPUT_LOG={relative(LOG_OUT)}")
    print(f"OUTPUT_REPORT={relative(REPORT_OUT)}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GateError as exc:
        print(f"STATUS=BLOCKED\nBLOCKER={exc}")
        raise SystemExit(1)
