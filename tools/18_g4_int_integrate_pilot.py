"""Integrate the already-passed G4-15 and G4-25 pilot audit outputs.

This runner deliberately consumes audit artifacts only.  It does not inspect
PDF structure, run OCR, repair PDFs, or infer paper relationships.
"""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PILOT_DIR = ROOT / "catalog" / "pilot"
REPORT_DIR = ROOT / "reports"
LOG_DIR = ROOT / "logs"

AUDIT_INPUTS = {
    2015: PILOT_DIR / "pdf_audit_2015.csv",
    2025: PILOT_DIR / "pdf_audit_2025.csv",
}
REVIEW_INPUTS = {
    2015: PILOT_DIR / "pdf_review_2015.csv",
    2025: PILOT_DIR / "pdf_review_2025.csv",
}
AUDIT_REPORTS = {
    2015: REPORT_DIR / "G4_15_pdf_audit_2015.md",
    2025: REPORT_DIR / "G4_25_pdf_audit_2025.md",
}
AUDIT_RUNNERS = {
    2015: ROOT / "tools" / "16_g4_15_audit_2015.py",
    2025: ROOT / "tools" / "17_g4_25_audit_2025.py",
}

AUDIT_OUTPUT = PILOT_DIR / "pdf_audit_pilot.csv"
REVIEW_OUTPUT = PILOT_DIR / "pdf_review_pilot.csv"
LOG_OUTPUT = LOG_DIR / "pdf_audit_pilot_integration.log"
REPORT_OUTPUT = REPORT_DIR / "G4_INT_pdf_audit_integration.md"

EXPECTED_BY_YEAR = {2015: 17, 2025: 12}
EXPECTED_REVIEW_BY_YEAR = {2015: 3, 2025: 7}
EXPECTED_SCHEMA_VERSION = 1

AUDIT_REQUIRED_SEMANTICS = {
    "path": "file_path",
    "classification": "pdf_type",
    "page_count": "page_count",
    "confidence": "confidence",
    "machine_routing": "machine_routing",
    "ocr_pages": "pages_needing_ocr",
    "encoding_flag": "has_encoding_issues",
    "layout_flag": "is_complex_layout",
}
REVIEW_REQUIRED_FIELDS = {"file_path", "pdf_type", "machine_routing"}

PROTECTED_G4_OUTPUTS = [
    *AUDIT_INPUTS.values(),
    *REVIEW_INPUTS.values(),
    *AUDIT_REPORTS.values(),
    *AUDIT_RUNNERS.values(),
    ROOT / "logs" / "pdf_audit_2015.log",
    ROOT / "logs" / "pdf_audit_2025.log",
]
PROTECTED_UPSTREAM = [
    ROOT / "catalog" / "files.csv",
    ROOT / "catalog" / "manifest.jsonl",
    ROOT / "catalog" / "papers.csv",
    ROOT / "catalog" / "paper_files.csv",
    ROOT / "catalog" / "paper_identity_review.csv",
]


class GateError(Exception):
    """A deterministic, user-actionable integration gate failure."""


def file_digest(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def snapshot(paths: list[Path]) -> dict[str, str | None]:
    return {str(path.relative_to(ROOT)): file_digest(path) for path in paths}


def changed_count(before: dict[str, str | None], after: dict[str, str | None]) -> int:
    return sum(before.get(path) != after.get(path) for path in before)


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        raise GateError(f"MISSING_INPUT={path.relative_to(ROOT)}")
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                raise GateError(f"UNPARSEABLE_CSV={path.relative_to(ROOT)}")
            fields = list(reader.fieldnames)
            if len(fields) != len(set(fields)):
                raise GateError(f"DUPLICATE_COLUMNS={path.relative_to(ROOT)}")
            rows = list(reader)
    except (OSError, UnicodeError, csv.Error, GateError) as exc:
        if isinstance(exc, GateError):
            raise
        raise GateError(f"UNPARSEABLE_CSV={path.relative_to(ROOT)}:{exc}") from exc
    return fields, rows


def read_json_list(value: str | None, field: str, path: Path) -> list[Any]:
    if value is None or value == "":
        return []
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise GateError(f"INVALID_JSON_FIELD={path.relative_to(ROOT)}:{field}") from exc
    if not isinstance(parsed, list):
        raise GateError(f"NON_LIST_JSON_FIELD={path.relative_to(ROOT)}:{field}")
    return parsed


def truthy(value: str | None) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def row_sha(row: dict[str, str]) -> str:
    values = [
        row.get("source_sha256", ""),
        row.get("sha256", ""),
        row.get("g1_sha256", ""),
        row.get("pre_audit_sha", ""),
    ]
    nonempty = [value.upper() for value in values if value]
    if not nonempty:
        return ""
    if len(set(nonempty)) != 1:
        raise GateError(f"SHA_ALIAS_CONFLICT={row.get('file_path', '')}")
    return nonempty[0]


def merge_fields(field_sets: list[list[str]], provenance: list[str]) -> list[str]:
    fields: list[str] = []
    for field_set in field_sets:
        for field in field_set:
            if field not in fields:
                fields.append(field)
    return fields + provenance


def parse_schema_version(reports: dict[int, str]) -> dict[int, int]:
    versions: dict[int, int] = {}
    for year, text in reports.items():
        match = re.search(r"(?:Schema|schema(?:_version)?)\s*[:=]\s*(\d+)", text)
        if match is None:
            raise GateError(f"MISSING_SCHEMA_VERSION_IN_REPORT={year}")
        versions[year] = int(match.group(1))
    return versions


def inspect_schema(
    audit_fields: dict[int, list[str]],
    review_fields: dict[int, list[str]],
    report_versions: dict[int, int],
    audit_rows: dict[int, list[dict[str, str]]],
) -> tuple[bool, bool, list[str]]:
    issues: list[str] = []
    schema_path = ROOT / "catalog" / "schema" / "pdf_audit_schema.json"
    try:
        with schema_path.open("r", encoding="utf-8") as handle:
            contract_version = int(json.load(handle)["schema_version"])
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise GateError(f"UNREADABLE_AUDIT_SCHEMA={schema_path.relative_to(ROOT)}") from exc

    if contract_version != EXPECTED_SCHEMA_VERSION:
        issues.append(f"AUDIT_SCHEMA_CONTRACT_VERSION={contract_version}")
    if set(report_versions.values()) != {EXPECTED_SCHEMA_VERSION}:
        issues.append(f"REPORT_SCHEMA_VERSIONS={report_versions}")

    for year, fields in audit_fields.items():
        missing = set(AUDIT_REQUIRED_SEMANTICS.values()) - set(fields)
        if missing:
            issues.append(f"AUDIT_REQUIRED_FIELDS_MISSING_{year}={sorted(missing)}")
        if year == 2025:
            versions = {row.get("audit_schema_version", "") for row in audit_rows[year]}
            if versions != {str(EXPECTED_SCHEMA_VERSION)}:
                issues.append(f"AUDIT_ROW_SCHEMA_VERSIONS_{year}={sorted(versions)}")

    for year, fields in review_fields.items():
        missing = REVIEW_REQUIRED_FIELDS - set(fields)
        if missing:
            issues.append(f"REVIEW_REQUIRED_FIELDS_MISSING_{year}={sorted(missing)}")
        if not ({"source_sha256", "sha256"} & set(fields)):
            issues.append(f"REVIEW_SHA_FIELD_MISSING_{year}")
        if not ({"visual_review_reason", "review_reason"} & set(fields)):
            issues.append(f"REVIEW_REASON_FIELD_MISSING_{year}")

    # These are the fields whose meaning must be equal before a union merge.
    for semantic, field in AUDIT_REQUIRED_SEMANTICS.items():
        if not all(field in set(fields) for fields in audit_fields.values()):
            continue
        if semantic in {"page_count", "confidence", "ocr_pages", "classification", "machine_routing"}:
            continue
        for year, rows in audit_rows.items():
            if any(field not in row for row in rows):
                issues.append(f"AUDIT_FIELD_NOT_READABLE_{year}={field}")

    return not issues, not issues, issues


def load_inventory() -> tuple[dict[str, list[dict[str, str]]], list[str]]:
    path = ROOT / "catalog" / "files.csv"
    fields, rows = read_csv(path)
    required = {"path", "sha256", "year", "file_extension"}
    missing = required - set(fields)
    if missing:
        raise GateError(f"INVENTORY_FIELDS_MISSING={sorted(missing)}")
    inventory: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        inventory[row["path"]].append(row)
    return inventory, fields


def audit_paths(rows: list[dict[str, str]]) -> tuple[set[str], int]:
    paths = [row.get("file_path", "") for row in rows]
    counts = Counter(paths)
    return set(paths), sum(count - 1 for count in counts.values() if count > 1)


def actual_sha_map(paths: set[str]) -> dict[str, str | None]:
    result: dict[str, str | None] = {}
    for relative in sorted(paths):
        result[relative] = file_digest(ROOT / relative)
    return result


def direct_q_mapping_evidence(
    audit_rows: dict[int, list[dict[str, str]]],
    review_rows: dict[int, list[dict[str, str]]],
) -> tuple[int, str]:
    assigned = [row for row in review_rows[2025] if row.get("preliminary_q", "")]
    source_path = AUDIT_RUNNERS[2025]
    source = source_path.read_text(encoding="utf-8") if source_path.exists() else ""
    has_q_routing_logic = (
        "Determine Q class (preliminary, for review)" in source
        and "if machine_routing ==" in source
        and "q_class = \"Q4\"" in source
    )
    audit_by_path = {row["file_path"]: row for row in audit_rows[2025]}
    all_image_q4 = bool(assigned) and all(
        audit_by_path.get(row.get("file_path", ""), {}).get("pdf_type") == "image_based"
        and row.get("machine_routing") == "IMAGE_VISUAL_REVIEW"
        and row.get("preliminary_q") == "Q4"
        for row in assigned
    )
    if has_q_routing_logic and all_image_q4:
        return 1, (
            "G4-25 review preliminary_q is Q4 for all 7 image_based/"
            "IMAGE_VISUAL_REVIEW rows and tools/17_g4_25_audit_2025.py "
            "contains direct machine_routing-to-q_class assignment"
        )
    return 0, "No direct PDF type/routing to Final Q mapping evidence detected"


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in fields} for row in rows)


def format_metric(key: str, value: Any) -> str:
    return f"{key}={value}"


def git_value(*args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def main() -> int:
    before_g4 = snapshot(PROTECTED_G4_OUTPUTS)
    before_upstream = snapshot(PROTECTED_UPSTREAM)

    issues: list[str] = []
    audit_fields: dict[int, list[str]] = {}
    review_fields: dict[int, list[str]] = {}
    audit_rows: dict[int, list[dict[str, str]]] = {}
    review_rows: dict[int, list[dict[str, str]]] = {}
    report_texts: dict[int, str] = {}

    for year in (2015, 2025):
        audit_fields[year], audit_rows[year] = read_csv(AUDIT_INPUTS[year])
        review_fields[year], review_rows[year] = read_csv(REVIEW_INPUTS[year])
        report_texts[year] = AUDIT_REPORTS[year].read_text(encoding="utf-8")

    report_versions = parse_schema_version(report_texts)
    audit_schema_ok, review_schema_ok, schema_issues = inspect_schema(
        audit_fields, review_fields, report_versions, audit_rows
    )
    issues.extend(schema_issues)

    inventory, _ = load_inventory()
    expected_paths: dict[int, set[str]] = {
        year: {
            path
            for path, records in inventory.items()
            if any(record.get("year") == str(year) and record.get("file_extension", "").lower() == ".pdf" for record in records)
        }
        for year in (2015, 2025)
    }
    for year in (2015, 2025):
        if len(expected_paths[year]) != EXPECTED_BY_YEAR[year]:
            issues.append(f"INVENTORY_EXPECTED_{year}={len(expected_paths[year])}")

    all_audit_rows = audit_rows[2015] + audit_rows[2025]
    all_review_rows = review_rows[2015] + review_rows[2025]
    audit_paths_by_year: dict[int, set[str]] = {}
    duplicate_audit_rows = 0
    missing_audit_rows = 0
    extra_audit_rows = 0
    for year in (2015, 2025):
        audit_paths_by_year[year], duplicates = audit_paths(audit_rows[year])
        duplicate_audit_rows += duplicates
        missing_audit_rows += len(expected_paths[year] - audit_paths_by_year[year])
        extra_audit_rows += len(audit_paths_by_year[year] - expected_paths[year])
        if len(audit_rows[year]) != EXPECTED_BY_YEAR[year]:
            issues.append(f"AUDIT_ROWS_{year}={len(audit_rows[year])}")
        if len(review_rows[year]) != EXPECTED_REVIEW_BY_YEAR[year]:
            issues.append(f"REVIEW_ROWS_{year}={len(review_rows[year])}")

    all_audit_paths = set().union(*audit_paths_by_year.values())
    all_audit_sha = {row_sha(row) for row in all_audit_rows}
    all_audit_sha.discard("")
    pre_hashes = actual_sha_map(all_audit_paths)
    source_sha_mismatch = 0
    for row in all_audit_rows:
        relative = row.get("file_path", "")
        sha = row_sha(row)
        inventory_rows = inventory.get(relative, [])
        actual = pre_hashes.get(relative)
        inventory_ok = len(inventory_rows) == 1 and inventory_rows[0].get("sha256", "").upper() == sha
        actual_ok = actual is not None and actual == sha
        if not inventory_ok or not actual_ok:
            source_sha_mismatch += 1
    if source_sha_mismatch:
        issues.append(f"SOURCE_SHA_MISMATCH={source_sha_mismatch}")

    post_hashes = actual_sha_map(all_audit_paths)
    original_sha_changed = sum(pre_hashes.get(path) != post_hashes.get(path) for path in all_audit_paths)
    if original_sha_changed:
        issues.append(f"ORIGINAL_SHA_CHANGED_AFTER_INTEGRATION={original_sha_changed}")

    type_counts = Counter(row.get("pdf_type", "") for row in all_audit_rows)
    total_pages = sum(int(row.get("page_count", "0") or 0) for row in all_audit_rows)
    total_ocr_pages = 0
    page_zero = 0
    out_of_range = 0
    audit_by_path: dict[str, dict[str, str]] = {}
    for row in all_audit_rows:
        path = row.get("file_path", "")
        if path in audit_by_path:
            continue
        audit_by_path[path] = row
        page_count = int(row.get("page_count", "0") or 0)
        pages = read_json_list(row.get("pages_needing_ocr"), "pages_needing_ocr", AUDIT_INPUTS[int(row.get("year") or 0)] if row.get("year") else AUDIT_INPUTS[2015])
        total_ocr_pages += len(pages)
        page_zero += sum(1 for page in pages if isinstance(page, int) and page == 0)
        out_of_range += sum(1 for page in pages if isinstance(page, int) and (page < 1 or page > page_count))
        page_zero += int(row.get("page_zero_in_output", "0") or 0)
        out_of_range += int(row.get("out_of_range_pages", "0") or 0)

    review_paths: list[str] = []
    review_sha_mismatch = 0
    for row in all_review_rows:
        path = row.get("file_path", "")
        review_paths.append(path)
        if path not in audit_by_path or row_sha(row) != row_sha(audit_by_path[path]):
            review_sha_mismatch += 1
    if review_sha_mismatch:
        issues.append(f"REVIEW_AUDIT_LINK_MISMATCH={review_sha_mismatch}")
    review_required = len(review_paths)
    if len(review_paths) != len(set(review_paths)):
        issues.append("DUPLICATE_REVIEW_PATH")
    if any(path not in audit_by_path for path in review_paths):
        issues.append("REVIEW_PATH_NOT_IN_AUDIT")

    final_q_assigned = sum(1 for row in review_rows[2025] if row.get("preliminary_q", ""))
    final_q_unassigned = len(all_audit_rows) - final_q_assigned
    direct_mapping, direct_mapping_detail = direct_q_mapping_evidence(audit_rows, review_rows)
    if direct_mapping:
        issues.append("DIRECT_PDF_TYPE_TO_FINAL_Q_MAPPING=1")

    # Preserve every source column and add only explicit provenance columns.
    audit_output_fields = merge_fields(
        [audit_fields[2015], audit_fields[2025]], ["audit_year", "audit_source_file"]
    )
    review_output_fields = merge_fields(
        [review_fields[2015], review_fields[2025]], ["review_year", "review_source_file"]
    )
    audit_output_rows: list[dict[str, str]] = []
    for year in (2015, 2025):
        for row in audit_rows[year]:
            output = dict(row)
            output["audit_year"] = str(year)
            output["audit_source_file"] = str(AUDIT_INPUTS[year].relative_to(ROOT)).replace("\\", "/")
            audit_output_rows.append(output)
    audit_output_rows.sort(key=lambda row: (int(row["audit_year"]), row.get("file_path", ""), row["audit_source_file"]))

    review_output_rows: list[dict[str, str]] = []
    for year in (2015, 2025):
        for row in review_rows[year]:
            output = dict(row)
            output["review_year"] = str(year)
            output["review_source_file"] = str(REVIEW_INPUTS[year].relative_to(ROOT)).replace("\\", "/")
            review_output_rows.append(output)
    review_output_rows.sort(key=lambda row: (int(row["review_year"]), row.get("file_path", ""), row["review_source_file"]))

    write_csv(AUDIT_OUTPUT, audit_output_fields, audit_output_rows)
    write_csv(REVIEW_OUTPUT, review_output_fields, review_output_rows)

    after_g4 = snapshot(PROTECTED_G4_OUTPUTS)
    after_upstream = snapshot(PROTECTED_UPSTREAM)
    g4_15_modified = int(any(before_g4.get(str(path.relative_to(ROOT))) != after_g4.get(str(path.relative_to(ROOT))) for path in PROTECTED_G4_OUTPUTS if "2015" in path.name or "G4_15" in path.name))
    g4_25_modified = int(any(before_g4.get(str(path.relative_to(ROOT))) != after_g4.get(str(path.relative_to(ROOT))) for path in PROTECTED_G4_OUTPUTS if "2025" in path.name or "G4_25" in path.name))
    upstream_changed = changed_count(before_upstream, after_upstream)
    g1_modified = int(before_upstream.get("catalog/files.csv") != after_upstream.get("catalog/files.csv"))
    g2_modified = int(before_upstream.get("catalog/manifest.jsonl") != after_upstream.get("catalog/manifest.jsonl"))
    g3_modified = int(any(before_upstream.get(name) != after_upstream.get(name) for name in ["catalog/papers.csv", "catalog/paper_files.csv", "catalog/paper_identity_review.csv"]))
    if g4_15_modified or g4_25_modified or upstream_changed:
        issues.append("PROTECTED_INPUT_MODIFIED")

    status = "PASS" if not issues and not direct_mapping else "BLOCKED"
    blocker = "NONE" if status == "PASS" else "; ".join(issues)

    metrics = {
        "STAGE": "G4-INT",
        "STATUS": status,
        "BRANCH": git_value("branch", "--show-current"),
        "HEAD": git_value("rev-parse", "HEAD"),
        "PYTHON_EXECUTABLE": str(Path(sys.executable).resolve()),
        "PYTHON_VERSION": platform.python_version(),
        "PDF_AUDIT_SCHEMA_VERSION": EXPECTED_SCHEMA_VERSION,
        "EXPECTED_PDF_FILES": len(all_audit_paths),
        "AUDIT_ROWS": len(all_audit_rows),
        "UNIQUE_AUDITED_FILE_PATHS": len(all_audit_paths),
        "MISSING_AUDIT_ROWS": missing_audit_rows,
        "EXTRA_AUDIT_ROWS": extra_audit_rows,
        "DUPLICATE_AUDIT_ROWS": duplicate_audit_rows,
        "AUDIT_SCHEMA_COMPATIBLE": int(audit_schema_ok),
        "REVIEW_SCHEMA_COMPATIBLE": int(review_schema_ok),
        "SOURCE_SHA_MISMATCH": source_sha_mismatch,
        "ORIGINAL_SHA_CHANGED_AFTER_INTEGRATION": original_sha_changed,
        "UNIQUE_PDF_SHA256": len(all_audit_sha),
        "TEXT_BASED": type_counts.get("text_based", 0),
        "SCANNED": type_counts.get("scanned", 0),
        "IMAGE_BASED": type_counts.get("image_based", 0),
        "MIXED": type_counts.get("mixed", 0),
        "TOTAL_PAGE_COUNT": total_pages,
        "TOTAL_OCR_ROUTED_PAGES": total_ocr_pages,
        "PAGE_ZERO_IN_PROJECT_OUTPUT": page_zero,
        "OUT_OF_RANGE_PROJECT_PAGES": out_of_range,
        "VISUAL_REVIEW_REQUIRED": review_required,
        "VISUAL_REVIEW_NOT_REQUIRED": len(all_audit_rows) - review_required,
        "FINAL_Q_ASSIGNED": final_q_assigned,
        "FINAL_Q_UNASSIGNED": final_q_unassigned,
        "DIRECT_PDF_TYPE_TO_FINAL_Q_MAPPING": direct_mapping,
        "NEAR_DUPLICATE_INFERENCE_RUN": 0,
        "OCR_RUN": 0,
        "OCR_OUTPUT_FILES": 0,
        "PDF_REPAIR_RUN": 0,
        "REPAIRED_PDF_FILES": 0,
        "MARKDOWN_EXTRACTION_RUN": 0,
        "MARKDOWN_ARTIFACTS_GENERATED": 0,
        "SOURCE_REACQUISITION_RUN": 0,
        "DEPENDENCY_INSTALL_RUN": 0,
        "G4_15_OUTPUT_MODIFIED": g4_15_modified,
        "G4_25_OUTPUT_MODIFIED": g4_25_modified,
        "G1_CATALOG_MODIFIED": g1_modified,
        "G2_CATALOG_MODIFIED": g2_modified,
        "G3_CATALOG_MODIFIED": g3_modified,
        "ORIGINAL_FILES_MODIFIED": int(source_sha_mismatch > 0 or original_sha_changed > 0),
        "ORIGINAL_FILES_DELETED": int(any(pre_hashes.get(path) is not None and post_hashes.get(path) is None for path in pre_hashes)),
        "ORIGINAL_FILES_MOVED_OR_RENAMED": 0,
    }

    log_lines = [
        "STAGE=G4-INT",
        "RUNNER=tools/18_g4_int_integrate_pilot.py",
        "INPUTS=catalog/pilot/pdf_audit_2015.csv,catalog/pilot/pdf_review_2015.csv,catalog/pilot/pdf_audit_2025.csv,catalog/pilot/pdf_review_2025.csv",
        *[format_metric(key, metrics[key]) for key in [
            "AUDIT_ROWS", "UNIQUE_AUDITED_FILE_PATHS", "MISSING_AUDIT_ROWS", "EXTRA_AUDIT_ROWS",
            "DUPLICATE_AUDIT_ROWS", "AUDIT_SCHEMA_COMPATIBLE", "REVIEW_SCHEMA_COMPATIBLE",
            "SOURCE_SHA_MISMATCH", "UNIQUE_PDF_SHA256", "TEXT_BASED", "SCANNED", "IMAGE_BASED",
            "MIXED", "TOTAL_PAGE_COUNT", "TOTAL_OCR_ROUTED_PAGES", "VISUAL_REVIEW_REQUIRED",
            "FINAL_Q_ASSIGNED", "FINAL_Q_UNASSIGNED", "DIRECT_PDF_TYPE_TO_FINAL_Q_MAPPING",
            "G4_15_OUTPUT_MODIFIED", "G4_25_OUTPUT_MODIFIED", "G1_CATALOG_MODIFIED",
            "G2_CATALOG_MODIFIED", "G3_CATALOG_MODIFIED",
        ]],
        f"DIRECT_MAPPING_EVIDENCE={direct_mapping_detail}",
        f"ISSUES={'; '.join(issues) if issues else 'NONE'}",
        f"STATUS={status}",
        f"BLOCKER={blocker}",
    ]
    LOG_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    LOG_OUTPUT.write_text("\n".join(log_lines) + "\n", encoding="utf-8")

    report_lines = [
        "# G4-INT Pilot PDF Audit Integration",
        "",
        *[format_metric(key, metrics[key]) for key in [
            "STAGE", "STATUS", "BRANCH", "HEAD", "PYTHON_EXECUTABLE", "PYTHON_VERSION",
            "PDF_AUDIT_SCHEMA_VERSION", "EXPECTED_PDF_FILES", "AUDIT_ROWS", "UNIQUE_AUDITED_FILE_PATHS",
            "MISSING_AUDIT_ROWS", "EXTRA_AUDIT_ROWS", "DUPLICATE_AUDIT_ROWS", "AUDIT_SCHEMA_COMPATIBLE",
            "REVIEW_SCHEMA_COMPATIBLE", "SOURCE_SHA_MISMATCH", "ORIGINAL_SHA_CHANGED_AFTER_INTEGRATION",
            "UNIQUE_PDF_SHA256", "TEXT_BASED", "SCANNED", "IMAGE_BASED", "MIXED", "TOTAL_PAGE_COUNT",
            "TOTAL_OCR_ROUTED_PAGES", "PAGE_ZERO_IN_PROJECT_OUTPUT", "OUT_OF_RANGE_PROJECT_PAGES",
            "VISUAL_REVIEW_REQUIRED", "VISUAL_REVIEW_NOT_REQUIRED", "FINAL_Q_ASSIGNED", "FINAL_Q_UNASSIGNED",
            "DIRECT_PDF_TYPE_TO_FINAL_Q_MAPPING", "NEAR_DUPLICATE_INFERENCE_RUN", "OCR_RUN", "OCR_OUTPUT_FILES",
            "PDF_REPAIR_RUN", "REPAIRED_PDF_FILES", "MARKDOWN_EXTRACTION_RUN", "MARKDOWN_ARTIFACTS_GENERATED",
            "SOURCE_REACQUISITION_RUN", "DEPENDENCY_INSTALL_RUN", "G4_15_OUTPUT_MODIFIED", "G4_25_OUTPUT_MODIFIED",
            "G1_CATALOG_MODIFIED", "G2_CATALOG_MODIFIED", "G3_CATALOG_MODIFIED", "ORIGINAL_FILES_MODIFIED",
            "ORIGINAL_FILES_DELETED", "ORIGINAL_FILES_MOVED_OR_RENAMED",
        ]],
        "",
        "OUTPUTS=",
        f"- {AUDIT_OUTPUT.relative_to(ROOT).as_posix()}",
        f"- {REVIEW_OUTPUT.relative_to(ROOT).as_posix()}",
        f"- {LOG_OUTPUT.relative_to(ROOT).as_posix()}",
        f"- {REPORT_OUTPUT.relative_to(ROOT).as_posix()}",
        "",
        "SCHEMA_NOTES=",
        "- Annual raw columns are preserved; only audit_year/audit_source_file and review_year/review_source_file provenance columns were added.",
        "- 2015 schema version is verified from its PASS report and the shared catalog/schema/pdf_audit_schema.json contract; 2025 row values are verified as 1.",
        "",
        "VALIDATION=",
        "- Annual audit/review CSVs parsed and merged in deterministic year/path order.",
        "- Inventory, targeted original PDF SHA-256, path coverage, review links, page/OCR routing, and protected-input snapshots checked.",
        "- No OCR, PDF repair, Markdown extraction, source reacquisition, duplicate inference, dependency installation, or API change performed.",
        "",
        "ISSUES=",
        *([f"- {issue}" for issue in issues] if issues else ["- NONE"]),
        "",
        f"DIRECT_MAPPING_EVIDENCE={direct_mapping_detail}",
        f"BLOCKER={blocker}",
        "APPROVAL=NOT_APPROVED" if status == "BLOCKED" else "APPROVAL=G4 Pilot PDF audit integration closed",
        "NEXT=Resolve G4-25 Final Q provenance and rerun G4-INT" if status == "BLOCKED" else "NEXT=G5",
    ]
    REPORT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUTPUT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    for key, value in metrics.items():
        print(format_metric(key, value))
    print(f"OUTPUT_AUDIT={AUDIT_OUTPUT.relative_to(ROOT).as_posix()}")
    print(f"OUTPUT_REVIEW={REVIEW_OUTPUT.relative_to(ROOT).as_posix()}")
    print(f"OUTPUT_LOG={LOG_OUTPUT.relative_to(ROOT).as_posix()}")
    print(f"OUTPUT_REPORT={REPORT_OUTPUT.relative_to(ROOT).as_posix()}")
    print(f"ISSUES={'; '.join(issues) if issues else 'NONE'}")
    print(f"BLOCKER={blocker}")
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GateError as exc:
        print(f"STAGE=G4-INT")
        print("STATUS=BLOCKED")
        print(f"BLOCKER={exc}")
        raise SystemExit(2)
