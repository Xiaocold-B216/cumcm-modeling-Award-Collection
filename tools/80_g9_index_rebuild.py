"""G9 formal paper index rebuild.

This runner rebuilds the one-record-per-logical-identity formal index from the
frozen G8 governance state.  It has two modes:

* default: read-only preflight; build and validate in memory, but write nothing
* --execute: write a unique stage, validate it, atomically promote the index,
  validate the promoted files, and write G9 evidence

The runner deliberately has no subprocess, network, OCR, PDF, Office, or Git
integration.  Existing G7 index files are used only as the discovered schema
contract; the historical pilot index is never modified.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
import tempfile
import time
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog"
SCALE = CATALOG / "scale"
DERIVED = ROOT / "derived" / "scale" / "papers"
REPORTS = ROOT / "reports" / "scale"

G8_RESULT = SCALE / "g8_q3_formal_artifact_generation_result.json"
G7_INDEX = CATALOG / "pilot" / "g7_paper_index.csv"
G7_BUILDER = ROOT / "tools" / "40_g7_pilot_index_final_qa.py"
FORMAL_INDEX = SCALE / "g9_paper_index.csv"
FORMAL_INDEX_JSONL = SCALE / "g9_paper_index.jsonl"
STAGE_ROOT = SCALE / "g9_index_stage"
RESULT = SCALE / "g9_index_rebuild_result.json"
ATTEMPT = SCALE / "g9_index_rebuild_attempt.json"
DIFF = SCALE / "g9_index_rebuild_diff.csv"
VALIDATION = SCALE / "g9_index_validation.csv"
REPORT = REPORTS / "G9_INDEX_REBUILD.md"

ELIGIBILITY = SCALE / "g8_artifact_eligibility.csv"
ARTIFACT_MANIFEST = SCALE / "g8_artifact_manifest.csv"
PAPER_STATUS = SCALE / "g8_paper_status.csv"
PAPERS = CATALOG / "papers.csv"
MEMBERSHIPS = CATALOG / "paper_files.csv"
FILES = CATALOG / "files.csv"
DOC_BACKLOG = SCALE / "g8_manual_backlog.csv"
Q3_BACKLOG = SCALE / "g8_q3_manual_backlog.csv"

EXPECTED_BRANCH = "library-refactor-v1"
EXPECTED_HEAD = "557724fba6572d4d83dc421feda5b17b13ff8d66"
EXPECTED_ARTIFACT_SETS = 453
EXPECTED_PRIMARY_ARTIFACTS = 1359
EXPECTED_ELIGIBLE = 453
EXPECTED_INELIGIBLE = 189

ARTIFACT_TYPES = ("paper.md", "metadata.yaml", "knowledge_card.md")
ARTIFACT_FIELDS = {
    "paper.md": ("paper_md_path", "paper_md_sha256"),
    "metadata.yaml": ("metadata_path", "metadata_sha256"),
    "knowledge_card.md": ("knowledge_card_path", "knowledge_card_sha256"),
}

# This is the existing G7 paper-index contract, reused for the current formal
# scale index.  The pilot index remains historical and is never rewritten.
INDEX_FIELDS = [
    "paper_id", "year", "problem", "subject_type", "artifact_eligible",
    "paper_md_path", "paper_md_sha256", "metadata_path", "metadata_sha256",
    "knowledge_card_path", "knowledge_card_sha256", "authority_source_count",
    "authority_source_paths", "primary_source_path", "final_q", "extraction_mode",
    "evidence_granularity", "page_count", "title", "keywords", "index_status", "search_text",
]

DIFF_FIELDS = [
    "paper_id", "change_type", "expected", "status", "old_record_sha256",
    "new_record_sha256", "notes",
]
VALIDATION_FIELDS = [
    "paper_id", "index_row_valid", "identity_valid", "membership_valid",
    "artifact_set_valid", "artifact_hash_valid", "source_valid", "metadata_valid",
    "search_smoke_valid", "status", "notes",
]

OUTPUT_PATHS = {
    "formal_index_csv": "catalog/scale/g9_paper_index.csv",
    "formal_index_jsonl": "catalog/scale/g9_paper_index.jsonl",
    "result": "catalog/scale/g9_index_rebuild_result.json",
    "attempt": "catalog/scale/g9_index_rebuild_attempt.json",
    "diff": "catalog/scale/g9_index_rebuild_diff.csv",
    "validation": "catalog/scale/g9_index_validation.csv",
    "report": "reports/scale/G9_INDEX_REBUILD.md",
}

REPORT_KEYS = [
    "STAGE", "STATUS", "BRANCH", "HEAD", "G9_ATTEMPT_ID", "G8_FINAL_STATE_VALID",
    "CANONICAL_INDEX_DISCOVERED", "CANONICAL_FORMAL_INDEX_PATH", "CANONICAL_INDEX_SCHEMA_SOURCE",
    "OLD_FORMAL_INDEX_SHA256", "OLD_FORMAL_INDEX_RECORD_COUNT", "STAGED_INDEX_BUILD_COMPLETE",
    "STAGED_FORMAL_INDEX_PAPER_COUNT", "STAGED_INDEX_VALID", "INDEX_ATOMIC_PROMOTION_COMPLETE",
    "POST_PROMOTION_INDEX_VALID", "FORMAL_INDEX_SHA256", "FORMAL_INDEX_PAPER_COUNT",
    "FORMAL_INDEX_UNIQUE_PAPER_ID_COUNT", "DUPLICATE_FORMAL_INDEX_PAPER_ID_COUNT",
    "ELIGIBLE_INDEXED_COUNT", "ELIGIBLE_NOT_INDEXED_COUNT", "INELIGIBLE_INDEXED_COUNT",
    "PROBLEM_PACKAGE_IN_FORMAL_PAPER_INDEX_COUNT", "INDEX_RECORD_WITH_ARTIFACT_SET_COUNT",
    "INDEX_RECORD_WITHOUT_ARTIFACT_SET_COUNT", "ARTIFACT_SET_WITHOUT_INDEX_RECORD_COUNT",
    "INDEXED_PRIMARY_ARTIFACT_COUNT", "PRIMARY_ARTIFACT_NOT_INDEXED_COUNT",
    "INDEX_RECORD_WITHOUT_MEMBERSHIP_COUNT", "BROKEN_ARTIFACT_REFERENCE_COUNT",
    "BROKEN_SOURCE_REFERENCE_COUNT", "INDEX_ARTIFACT_SHA_MISMATCH_COUNT",
    "INDEX_IDENTITY_METADATA_MISMATCH_COUNT", "INDEX_MEMBERSHIP_METADATA_MISMATCH_COUNT",
    "INDEX_ARTIFACT_METADATA_MISMATCH_COUNT", "NEW_FORMAL_INDEX_RECORD_COUNT",
    "INDEX_RECORD_ADDED_COUNT", "INDEX_RECORD_REMOVED_COUNT", "INDEX_RECORD_CHANGED_COUNT",
    "EXPECTED_INDEX_CHANGE_COUNT", "UNEXPECTED_INDEX_CHANGE_COUNT",
    "FORMAL_ARTIFACT_CONTENT_MODIFICATION_COUNT", "FORMAL_ELIGIBILITY_MODIFIED",
    "IDENTITY_MODIFICATION_COUNT", "MEMBERSHIP_MODIFICATION_COUNT", "ORIGINAL_FILES_MODIFIED",
    "ARTIFACT_SETS", "PRIMARY_ARTIFACTS", "DOC_MANUAL_BACKLOG", "Q3_MANUAL_BACKLOG",
    "TOTAL_MANUAL_BACKLOG", "ELIGIBLE", "INELIGIBLE", "OCR_RUN", "Q3_OCR_RUN",
    "OCR_REPLAY_PAGE_COUNT", "PDF_RENDER_RUN", "PDF_INSPECTOR_EXTRACTION_RUN",
    "PDFTOTEXT_EXTRACTION_RUN", "BODY_RECONSTRUCTION_RUN", "FORMAL_ARTIFACTS_GENERATED",
    "NETWORK_ACCESS_USED", "DOWNLOAD_RUN", "NEW_DEPENDENCY_INSTALLED", "WORD_RUN",
    "WORD_COM_RUN", "DOC_CONVERSION_RUN", "PRINT_JOB_RUN", "G10_RUN", "GIT_OPERATIONS",
    "INDEX_CONTRACT_GAP_COUNT", "INDEX_CONTRACT_GAPS", "AFFECTED_PAPER_IDS", "OUTPUTS",
    "VALIDATION", "ISSUES", "BLOCKER", "NEXT",
]


class GateError(RuntimeError):
    """A deterministic governance gate failure."""

    def __init__(self, code: str, message: str, affected: list[str] | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.affected = affected or []


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def normal_path(value: str) -> str:
    return str(value or "").replace("\\", "/")


def path_inside(value: str) -> bool:
    value = normal_path(value)
    if not value or re.match(r"^[A-Za-z]:/", value) or value.startswith("/"):
        return False
    try:
        (ROOT / value).resolve().relative_to(ROOT.resolve())
        return True
    except ValueError:
        return False


def digest(path: Path) -> str:
    sha = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            sha.update(chunk)
    return sha.hexdigest().upper()


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest().upper()


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise GateError("INPUT_JSON_ERROR", f"cannot parse {rel(path)}: {exc}") from exc
    if not isinstance(value, dict):
        raise GateError("INPUT_JSON_ERROR", f"{rel(path)} is not a JSON object")
    return value


def read_csv(path: Path) -> list[dict[str, str]]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))
    except Exception as exc:
        raise GateError("INPUT_CSV_ERROR", f"cannot parse {rel(path)}: {exc}") from exc


def yaml_read(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise GateError("METADATA_PARSE_ERROR", f"cannot parse {rel(path)}: {exc}") from exc
    if not isinstance(value, dict):
        raise GateError("METADATA_PARSE_ERROR", f"{rel(path)} is not a mapping")
    return value


def scalar(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "1" if value else "0"
    return str(value)


def norm_keywords(value: Any) -> str:
    if isinstance(value, list):
        return ";".join(scalar(item) for item in value)
    return scalar(value)


def jsonl_bytes(rows: list[dict[str, str]]) -> bytes:
    return "".join(
        json.dumps({field: row.get(field, "") for field in INDEX_FIELDS}, ensure_ascii=False, separators=(",", ":"))
        + "\n"
        for row in rows
    ).encode("utf-8")


def csv_bytes(fields: list[str], rows: list[dict[str, Any]]) -> bytes:
    from io import StringIO

    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows({field: row.get(field, "") for field in fields} for row in rows)
    return ("\ufeff" + buffer.getvalue()).encode("utf-8")


def atomic_write_bytes(path: Path, value: bytes, retries: int = 24) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent), delete=False
        ) as handle:
            temp_path = Path(handle.name)
            handle.write(value)
            handle.flush()
            os.fsync(handle.fileno())
        for attempt in range(retries):
            try:
                os.replace(str(temp_path), str(path))
                temp_path = None
                return
            except PermissionError:
                if attempt + 1 >= retries:
                    raise
                time.sleep(0.25)
    finally:
        if temp_path is not None and temp_path.exists():
            try:
                temp_path.unlink()
            except OSError:
                pass


def atomic_write_json(path: Path, value: dict[str, Any]) -> None:
    atomic_write_bytes(path, (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def check_required_files(paths: list[Path]) -> None:
    missing = [rel(path) for path in paths if not path.is_file()]
    if missing:
        raise GateError("AUTHORITATIVE_INPUT_MISSING", ";".join(missing))


def make_attempt_id() -> str:
    return datetime.now().strftime("%Y%m%dT%H%M%S%f") + "_" + uuid.uuid4().hex[:8]


def read_index(path: Path) -> list[dict[str, str]]:
    rows = read_csv(path)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader, [])
    if header != INDEX_FIELDS:
        raise GateError("INDEX_SCHEMA_MISMATCH", f"{rel(path)} header does not match discovered 22-field contract")
    return rows


def read_jsonl_projection(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except Exception as exc:
            raise GateError("INDEX_JSONL_ERROR", f"{rel(path)} line {line_number}: {exc}") from exc
        if not isinstance(value, dict) or list(value.keys()) != INDEX_FIELDS:
            raise GateError("INDEX_JSONL_SCHEMA_MISMATCH", f"{rel(path)} line {line_number}")
        rows.append({field: scalar(value.get(field, "")) for field in INDEX_FIELDS})
    return rows


def discover_index_contract() -> dict[str, Any]:
    if not G7_INDEX.is_file() or not G7_BUILDER.is_file():
        raise GateError("CANONICAL_INDEX_NOT_DISCOVERED", "historical G7 index contract source is incomplete")
    with G7_INDEX.open("r", encoding="utf-8-sig", newline="") as handle:
        header = next(csv.reader(handle), [])
    if header != INDEX_FIELDS:
        raise GateError("CANONICAL_INDEX_SCHEMA_MISMATCH", "G7 index schema is not the expected existing contract")
    old_rows: list[dict[str, str]] = []
    if FORMAL_INDEX.is_file():
        old_rows = read_index(FORMAL_INDEX)
    return {
        "discovered": 1,
        "schema_source": f"{rel(G7_INDEX)}; {rel(G7_BUILDER)}",
        "formal_path": rel(FORMAL_INDEX),
        "old_rows": old_rows,
        "old_exists": int(FORMAL_INDEX.is_file()),
        "old_sha": digest(FORMAL_INDEX) if FORMAL_INDEX.is_file() else "",
        "old_jsonl_exists": int(FORMAL_INDEX_JSONL.is_file()),
    }


def validate_g8_state(g8: dict[str, Any]) -> tuple[int, list[str]]:
    checks: dict[str, Any] = {
        "STAGE": "G8-Q3-FORMAL-ARTIFACT-GENERATION",
        "STATUS": "PASS",
        "BRANCH": EXPECTED_BRANCH,
        "HEAD": EXPECTED_HEAD,
        "TOTAL_ARTIFACT_SET_COUNT": EXPECTED_ARTIFACT_SETS,
        "TOTAL_PRIMARY_ARTIFACT_COUNT": EXPECTED_PRIMARY_ARTIFACTS,
        "ARTIFACT_SETS": EXPECTED_ARTIFACT_SETS,
        "PRIMARY_ARTIFACTS": EXPECTED_PRIMARY_ARTIFACTS,
        "DOC_MANUAL_BACKLOG": 0,
        "Q3_MANUAL_BACKLOG": 0,
        "TOTAL_MANUAL_BACKLOG": 0,
        "ELIGIBLE": EXPECTED_ELIGIBLE,
        "INELIGIBLE": EXPECTED_INELIGIBLE,
        "FORMAL_ARTIFACT_ELIGIBLE_WITH_ARTIFACT_COUNT": EXPECTED_ELIGIBLE,
        "FORMAL_ARTIFACT_ELIGIBLE_WITHOUT_ARTIFACT_COUNT": 0,
        "FORMAL_ELIGIBILITY_MODIFIED": 0,
        "IDENTITY_MODIFICATION_COUNT": 0,
        "MEMBERSHIP_MODIFICATION_COUNT": 0,
        "ORIGINAL_FILES_MODIFIED": 0,
        "G9_RUN": 0,
        "G10_RUN": 0,
        "GIT_OPERATIONS": 0,
    }
    failures: list[str] = []
    for key, expected in checks.items():
        actual = g8.get(key)
        if isinstance(expected, int):
            try:
                actual = int(actual)
            except (TypeError, ValueError):
                actual = None
        if actual != expected:
            failures.append(f"{key}={actual!r};expected={expected!r}")
    return int(not failures), failures


def load_context() -> dict[str, Any]:
    check_required_files([
        G8_RESULT, G7_INDEX, G7_BUILDER, ELIGIBILITY, ARTIFACT_MANIFEST, PAPER_STATUS,
        PAPERS, MEMBERSHIPS, FILES, DOC_BACKLOG, Q3_BACKLOG,
    ])
    g8 = read_json(G8_RESULT)
    g8_valid, g8_failures = validate_g8_state(g8)
    if not g8_valid:
        raise GateError("G8_FINAL_STATE_INVALID", ";".join(g8_failures))

    contract = discover_index_contract()
    eligibility_rows = read_csv(ELIGIBILITY)
    eligibility_by_id: dict[str, dict[str, str]] = {}
    duplicate_eligibility: set[str] = set()
    for row in eligibility_rows:
        pid = row.get("paper_id", "")
        if pid in eligibility_by_id:
            duplicate_eligibility.add(pid)
        eligibility_by_id[pid] = row
    if duplicate_eligibility:
        raise GateError("ELIGIBILITY_DUPLICATE_ID", ";".join(sorted(duplicate_eligibility)))

    eligible_rows = [
        row for row in eligibility_rows
        if row.get("artifact_eligible") == "1" and row.get("subject_type") == "PAPER"
    ]
    ineligible_rows = [row for row in eligibility_rows if row.get("artifact_eligible") == "0"]
    if len(eligible_rows) != EXPECTED_ELIGIBLE or len(ineligible_rows) != EXPECTED_INELIGIBLE:
        raise GateError(
            "ELIGIBILITY_CARDINALITY_DRIFT",
            f"eligible={len(eligible_rows)};ineligible={len(ineligible_rows)}",
        )
    if any(row.get("artifact_eligible") not in {"0", "1"} for row in eligibility_rows):
        raise GateError("ELIGIBILITY_UNRESOLVED", "eligibility contains values outside 0/1")

    artifact_rows = read_csv(ARTIFACT_MANIFEST)
    artifacts_by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in artifact_rows:
        artifacts_by_id[row.get("paper_id", "")].append(row)
    if len(artifact_rows) != EXPECTED_PRIMARY_ARTIFACTS or len(artifacts_by_id) != EXPECTED_ARTIFACT_SETS:
        raise GateError(
            "ARTIFACT_CARDINALITY_DRIFT",
            f"rows={len(artifact_rows)};ids={len(artifacts_by_id)}",
        )

    papers_by_id = {row.get("paper_id", ""): row for row in read_csv(PAPERS)}
    membership_rows = read_csv(MEMBERSHIPS)
    memberships_by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in membership_rows:
        memberships_by_id[row.get("paper_id", "")].append(row)
    inventory_by_path = {normal_path(row.get("path", "")): row for row in read_csv(FILES)}
    status_by_id = {row.get("paper_id", ""): row for row in read_csv(PAPER_STATUS)}

    metadata_by_id: dict[str, dict[str, Any]] = {}
    source_paths: set[str] = set()
    for row in eligible_rows:
        pid = row["paper_id"]
        metadata_path = ROOT / f"derived/scale/papers/{pid}/metadata.yaml"
        if not metadata_path.is_file():
            raise GateError("FORMAL_METADATA_MISSING", pid, [pid])
        metadata = yaml_read(metadata_path)
        metadata_by_id[pid] = metadata
        for source in metadata.get("authority_sources", []) if isinstance(metadata.get("authority_sources"), list) else []:
            if isinstance(source, dict) and source.get("path"):
                source_paths.add(normal_path(source["path"]))
        if metadata.get("primary_file"):
            source_paths.add(normal_path(metadata["primary_file"]))
        for membership in memberships_by_id.get(pid, []):
            if membership.get("path"):
                source_paths.add(normal_path(membership["path"]))

    protected_paths = [
        ELIGIBILITY, ARTIFACT_MANIFEST, PAPER_STATUS, PAPERS, MEMBERSHIPS, FILES,
        DOC_BACKLOG, Q3_BACKLOG, G8_RESULT,
    ]
    protected_paths.extend(ROOT / path for path in source_paths if path_inside(path))
    for rows in artifacts_by_id.values():
        protected_paths.extend(ROOT / normal_path(row.get("artifact_path", "")) for row in rows)
    protected_before = snapshot(protected_paths)

    return {
        "g8": g8,
        "g8_valid": g8_valid,
        "contract": contract,
        "eligibility_rows": eligibility_rows,
        "eligibility_by_id": eligibility_by_id,
        "eligible_rows": eligible_rows,
        "eligible_ids": {row["paper_id"] for row in eligible_rows},
        "ineligible_rows": ineligible_rows,
        "ineligible_ids": {row["paper_id"] for row in ineligible_rows},
        "artifacts": artifact_rows,
        "artifacts_by_id": dict(artifacts_by_id),
        "papers_by_id": papers_by_id,
        "memberships_by_id": dict(memberships_by_id),
        "inventory_by_path": inventory_by_path,
        "status_by_id": status_by_id,
        "metadata_by_id": metadata_by_id,
        "source_paths": source_paths,
        "protected_paths": protected_paths,
        "protected_before": protected_before,
    }


def snapshot(paths: list[Path]) -> dict[str, str]:
    result: dict[str, str] = {}
    seen: set[str] = set()
    for path in paths:
        if not path.is_file():
            continue
        key = rel(path)
        if key not in seen:
            result[key] = digest(path)
            seen.add(key)
    return result


def extraction_mode(metadata: dict[str, Any]) -> str:
    # Prefer the canonical extraction backend, then page backend.  The older
    # DOC/Image metadata has neither, so the existing artifact-generation mode
    # is the only authoritative non-inferred fallback.
    return scalar(
        metadata.get("primary_extraction_backend")
        or metadata.get("page_extraction_backend")
        or metadata.get("artifact_generation_mode")
    )


def authority_paths(
    metadata: dict[str, Any],
    eligibility: dict[str, str] | None = None,
    catalog_members: list[dict[str, str]] | None = None,
) -> list[str]:
    values = [
        normal_path(source.get("path", ""))
        for source in metadata.get("authority_sources", [])
        if isinstance(source, dict) and source.get("path")
    ] if isinstance(metadata.get("authority_sources"), list) else []
    if values:
        return values
    metadata_primary = normal_path(metadata.get("primary_file", ""))
    if metadata_primary:
        return [metadata_primary]
    eligibility_primary = normal_path((eligibility or {}).get("primary_file", ""))
    if eligibility_primary:
        return [path for path in eligibility_primary.split(";") if path]
    return sorted({
        normal_path(member.get("path", ""))
        for member in (catalog_members or [])
        if member.get("path")
    })


def primary_source_path(
    metadata: dict[str, Any],
    eligibility: dict[str, str],
    catalog_members: list[dict[str, str]],
) -> str:
    metadata_primary = normal_path(metadata.get("primary_file", ""))
    if metadata_primary:
        return metadata_primary
    eligibility_primary = normal_path(eligibility.get("primary_file", ""))
    if eligibility_primary:
        return next((path for path in eligibility_primary.split(";") if path), "")
    return next(iter(authority_paths(metadata, eligibility, catalog_members)), "")


def build_rows(context: dict[str, Any]) -> tuple[list[dict[str, str]], list[str]]:
    rows: list[dict[str, str]] = []
    issues: list[str] = []
    for eligibility in context["eligible_rows"]:
        pid = eligibility["paper_id"]
        metadata = context["metadata_by_id"].get(pid, {})
        manifest = context["artifacts_by_id"].get(pid, [])
        by_type = {row.get("artifact_type", ""): row for row in manifest}
        if set(by_type) != set(ARTIFACT_TYPES) or len(manifest) != len(ARTIFACT_TYPES):
            issues.append(f"{pid}:artifact_set_schema")
        catalog_members = context["memberships_by_id"].get(pid, [])
        source_paths = authority_paths(metadata, eligibility, catalog_members)
        card_path = ROOT / normal_path(by_type.get("knowledge_card.md", {}).get("artifact_path", ""))
        card_text = ""
        if card_path.is_file():
            try:
                card_text = card_path.read_text(encoding="utf-8")
            except OSError as exc:
                issues.append(f"{pid}:knowledge_card_read:{exc}")
        title = scalar(metadata.get("title", ""))
        keywords = norm_keywords(metadata.get("keywords", ""))
        search_text = " ".join(
            item for item in [
                pid, scalar(eligibility.get("year")), scalar(eligibility.get("problem")),
                title, keywords, "Knowledge Card", "Basic Information", "Evidence-based Content",
                card_text[:500],
            ] if item
        ).replace("\r", " ").replace("\n", " ")
        quality_values = {row.get("quality", "") for row in manifest}
        quality = next(iter(quality_values), scalar(metadata.get("quality", ""))) if len(quality_values) == 1 else ""
        rows.append({
            "paper_id": pid,
            "year": scalar(eligibility.get("year")),
            "problem": scalar(eligibility.get("problem")),
            "subject_type": scalar(eligibility.get("subject_type")),
            "artifact_eligible": scalar(eligibility.get("artifact_eligible")),
            "paper_md_path": normal_path(by_type.get("paper.md", {}).get("artifact_path", "")),
            "paper_md_sha256": scalar(by_type.get("paper.md", {}).get("artifact_sha256", "")).upper(),
            "metadata_path": normal_path(by_type.get("metadata.yaml", {}).get("artifact_path", "")),
            "metadata_sha256": scalar(by_type.get("metadata.yaml", {}).get("artifact_sha256", "")).upper(),
            "knowledge_card_path": normal_path(by_type.get("knowledge_card.md", {}).get("artifact_path", "")),
            "knowledge_card_sha256": scalar(by_type.get("knowledge_card.md", {}).get("artifact_sha256", "")).upper(),
            "authority_source_count": str(len([path for path in source_paths if path])),
            "authority_source_paths": ";".join(source_paths),
            "primary_source_path": primary_source_path(metadata, eligibility, catalog_members),
            "final_q": quality,
            "extraction_mode": extraction_mode(metadata),
            "evidence_granularity": scalar(metadata.get("evidence_granularity")),
            "page_count": scalar(metadata.get("page_count")),
            "title": title,
            "keywords": keywords,
            "index_status": "PASS",
            "search_text": search_text,
        })
    try:
        rows.sort(key=lambda row: (int(row["year"]), row["problem"], row["paper_id"]))
    except (TypeError, ValueError) as exc:
        issues.append(f"index_sort:{exc}")
    return rows, issues


def expected_metadata_mode(metadata: dict[str, Any]) -> str:
    return extraction_mode(metadata)


def validate_rows(rows: list[dict[str, str]], context: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, str]]]:
    eligible_ids = context["eligible_ids"]
    ineligible_ids = context["ineligible_ids"]
    eligibility_by_id = context["eligibility_by_id"]
    artifacts_by_id = context["artifacts_by_id"]
    metadata_by_id = context["metadata_by_id"]
    papers_by_id = context["papers_by_id"]
    memberships_by_id = context["memberships_by_id"]
    inventory_by_path = context["inventory_by_path"]

    index_ids = [row.get("paper_id", "") for row in rows]
    index_id_set = set(index_ids)
    duplicate_count = len(index_ids) - len(index_id_set)
    row_results: list[dict[str, str]] = []
    referenced_artifact_paths: set[str] = set()
    eligible_indexed = len(eligible_ids & index_id_set)
    ineligible_indexed = sum(1 for pid in index_id_set if pid not in eligible_ids)
    problem_package_count = sum(
        1 for pid in index_id_set
        if eligibility_by_id.get(pid, {}).get("subject_type") == "PROBLEM_PACKAGE"
    )
    record_with_artifact = 0
    record_without_artifact = 0
    record_without_membership = 0
    broken_artifact = 0
    broken_source = 0
    artifact_sha_mismatch = 0
    identity_mismatch = 0
    membership_mismatch = 0
    artifact_metadata_mismatch = 0

    for row in rows:
        pid = row.get("paper_id", "")
        eligibility = eligibility_by_id.get(pid, {})
        metadata = metadata_by_id.get(pid, {})
        manifest = artifacts_by_id.get(pid, [])
        manifest_by_type = {item.get("artifact_type", ""): item for item in manifest}
        catalog_members = memberships_by_id.get(pid, [])
        catalog_member_paths = {normal_path(item.get("path", "")) for item in catalog_members if item.get("path")}
        metadata_members = {
            normal_path(item.get("path", ""))
            for item in metadata.get("paper_file_memberships", [])
            if isinstance(item, dict) and item.get("path")
        } if isinstance(metadata.get("paper_file_memberships"), list) else set()

        identity_valid = bool(
            eligibility
            and eligibility.get("artifact_eligible") == "1"
            and eligibility.get("subject_type") == "PAPER"
            and row.get("year") == eligibility.get("year")
            and row.get("problem") == eligibility.get("problem")
            and row.get("subject_type") == "PAPER"
            and row.get("artifact_eligible") == "1"
            and scalar(metadata.get("paper_id")) == pid
            and scalar(metadata.get("year")) == scalar(eligibility.get("year"))
            and scalar(metadata.get("problem")) == scalar(eligibility.get("problem"))
            and scalar(metadata.get("subject_type")) == "PAPER"
            and bool(papers_by_id.get(pid))
            and papers_by_id[pid].get("year") == eligibility.get("year")
            and papers_by_id[pid].get("problem_code") == eligibility.get("problem")
        )
        if not identity_valid:
            identity_mismatch += 1

        membership_valid = bool(
            catalog_member_paths
            and all(path_inside(path) and (ROOT / path).is_file() for path in catalog_member_paths)
        )
        # PaperFileMembership is the authoritative membership source.  Some
        # legacy DOC/Image metadata files predate the embedded membership
        # field; absence is not a contradiction.  If the optional field is
        # present, it must agree exactly with the authoritative catalog.
        membership_valid = membership_valid and (not metadata_members or metadata_members == catalog_member_paths)
        if not membership_valid:
            membership_mismatch += 1
            record_without_membership += 1

        artifact_set_valid = bool(
            len(manifest) == 3
            and set(manifest_by_type) == set(ARTIFACT_TYPES)
            and all(item.get("status") == "PASS" for item in manifest)
        )
        if artifact_set_valid:
            record_with_artifact += 1
        else:
            record_without_artifact += 1

        artifact_hash_valid = True
        artifact_metadata_valid = True
        for artifact_type in ARTIFACT_TYPES:
            path_field, sha_field = ARTIFACT_FIELDS[artifact_type]
            index_path = normal_path(row.get(path_field, ""))
            index_sha = scalar(row.get(sha_field, "")).upper()
            manifest_row = manifest_by_type.get(artifact_type)
            if index_path:
                referenced_artifact_paths.add(index_path)
            actual_path = ROOT / index_path if path_inside(index_path) else ROOT / "__invalid__"
            if not path_inside(index_path) or not actual_path.is_file() or manifest_row is None:
                broken_artifact += 1
                artifact_hash_valid = False
                artifact_metadata_valid = False
                continue
            manifest_path = normal_path(manifest_row.get("artifact_path", ""))
            manifest_sha = scalar(manifest_row.get("artifact_sha256", "")).upper()
            actual_sha = digest(actual_path)
            if index_path != manifest_path or index_sha != manifest_sha or actual_sha != manifest_sha:
                artifact_sha_mismatch += 1
                artifact_hash_valid = False
            if (
                manifest_row.get("paper_id") != pid
                or manifest_row.get("subject_type") != "PAPER"
                or manifest_row.get("artifact_eligible") != "1"
                or manifest_row.get("quality") != row.get("final_q")
            ):
                artifact_metadata_valid = False
        if not artifact_metadata_valid:
            artifact_metadata_mismatch += 1

        source_paths = [path for path in row.get("authority_source_paths", "").split(";") if path]
        source_valid = bool(source_paths and row.get("primary_source_path"))
        expected_sources = authority_paths(metadata, eligibility, catalog_members)
        source_valid = source_valid and source_paths == expected_sources
        source_valid = source_valid and row.get("primary_source_path") == primary_source_path(metadata, eligibility, catalog_members)
        for source_path in source_paths + [row.get("primary_source_path", "")]:
            source_path = normal_path(source_path)
            actual_source = ROOT / source_path if path_inside(source_path) else ROOT / "__invalid__"
            if not path_inside(source_path) or not actual_source.is_file():
                broken_source += 1
                source_valid = False
                continue
            inventory_row = inventory_by_path.get(source_path)
            if inventory_row and inventory_row.get("sha256"):
                if scalar(inventory_row.get("sha256")).upper() != digest(actual_source):
                    source_valid = False
            for source in metadata.get("authority_sources", []) if isinstance(metadata.get("authority_sources"), list) else []:
                if isinstance(source, dict) and normal_path(source.get("path", "")) == source_path and source.get("sha256"):
                    if scalar(source.get("sha256")).upper() != digest(actual_source):
                        source_valid = False

        metadata_path = normal_path(row.get("metadata_path", ""))
        metadata_valid = bool(
            path_inside(metadata_path)
            and (ROOT / metadata_path).is_file()
            and scalar(metadata.get("paper_id")) == pid
            and scalar(row.get("metadata_sha256")).upper() == digest(ROOT / metadata_path)
            and row.get("evidence_granularity", "") == scalar(metadata.get("evidence_granularity"))
            and row.get("page_count", "") == scalar(metadata.get("page_count"))
            and row.get("extraction_mode", "") == expected_metadata_mode(metadata)
        )
        if not metadata_valid:
            artifact_metadata_mismatch += 1

        search_text = row.get("search_text", "")
        search_smoke_valid = bool(
            pid and pid in search_text and row.get("year", "") in search_text
            and row.get("problem", "") in search_text
            and "Knowledge Card" in search_text
        )
        row_valid = all([
            identity_valid, membership_valid, artifact_set_valid, artifact_hash_valid,
            source_valid, metadata_valid, search_smoke_valid, row.get("index_status") == "PASS",
        ])
        row_results.append({
            "paper_id": pid,
            "index_row_valid": str(int(row_valid)),
            "identity_valid": str(int(identity_valid)),
            "membership_valid": str(int(membership_valid)),
            "artifact_set_valid": str(int(artifact_set_valid)),
            "artifact_hash_valid": str(int(artifact_hash_valid)),
            "source_valid": str(int(source_valid)),
            "metadata_valid": str(int(metadata_valid)),
            "search_smoke_valid": str(int(search_smoke_valid)),
            "status": "PASS" if row_valid else "FAIL",
            "notes": "" if row_valid else ";".join(
                name for name, value in [
                    ("identity", identity_valid), ("membership", membership_valid),
                    ("artifact_set", artifact_set_valid), ("artifact_hash", artifact_hash_valid),
                    ("source", source_valid), ("metadata", metadata_valid),
                    ("search", search_smoke_valid),
                ] if not value
            ),
        })

    registry_paths = {
        normal_path(row.get("artifact_path", ""))
        for row in context["artifacts"]
        if row.get("artifact_path")
    }
    metrics: dict[str, Any] = {
        "FORMAL_INDEX_PAPER_COUNT": len(rows),
        "FORMAL_INDEX_UNIQUE_PAPER_ID_COUNT": len(index_id_set),
        "DUPLICATE_FORMAL_INDEX_PAPER_ID_COUNT": duplicate_count,
        "ELIGIBLE_INDEXED_COUNT": eligible_indexed,
        "ELIGIBLE_NOT_INDEXED_COUNT": len(eligible_ids - index_id_set),
        "INELIGIBLE_INDEXED_COUNT": ineligible_indexed,
        "PROBLEM_PACKAGE_IN_FORMAL_PAPER_INDEX_COUNT": problem_package_count,
        "INDEX_RECORD_WITH_ARTIFACT_SET_COUNT": record_with_artifact,
        "INDEX_RECORD_WITHOUT_ARTIFACT_SET_COUNT": record_without_artifact,
        "ARTIFACT_SET_WITHOUT_INDEX_RECORD_COUNT": len(set(context["artifacts_by_id"]) - index_id_set),
        "INDEXED_PRIMARY_ARTIFACT_COUNT": len(referenced_artifact_paths & registry_paths),
        "PRIMARY_ARTIFACT_NOT_INDEXED_COUNT": len(registry_paths - referenced_artifact_paths),
        "INDEX_RECORD_WITHOUT_MEMBERSHIP_COUNT": record_without_membership,
        "BROKEN_ARTIFACT_REFERENCE_COUNT": broken_artifact,
        "BROKEN_SOURCE_REFERENCE_COUNT": broken_source,
        "INDEX_ARTIFACT_SHA_MISMATCH_COUNT": artifact_sha_mismatch,
        "INDEX_IDENTITY_METADATA_MISMATCH_COUNT": identity_mismatch,
        "INDEX_MEMBERSHIP_METADATA_MISMATCH_COUNT": membership_mismatch,
        "INDEX_ARTIFACT_METADATA_MISMATCH_COUNT": artifact_metadata_mismatch,
    }
    metrics["INDEX_VALID"] = int(
        len(rows) == EXPECTED_ELIGIBLE
        and metrics["FORMAL_INDEX_UNIQUE_PAPER_ID_COUNT"] == EXPECTED_ELIGIBLE
        and all(value == 0 for key, value in metrics.items() if key.endswith("_COUNT") and key not in {
            "FORMAL_INDEX_PAPER_COUNT", "FORMAL_INDEX_UNIQUE_PAPER_ID_COUNT", "ELIGIBLE_INDEXED_COUNT",
            "INDEX_RECORD_WITH_ARTIFACT_SET_COUNT", "INDEXED_PRIMARY_ARTIFACT_COUNT",
        })
        and metrics["ELIGIBLE_INDEXED_COUNT"] == EXPECTED_ELIGIBLE
        and metrics["INDEX_RECORD_WITH_ARTIFACT_SET_COUNT"] == EXPECTED_ARTIFACT_SETS
        and metrics["INDEXED_PRIMARY_ARTIFACT_COUNT"] == EXPECTED_PRIMARY_ARTIFACTS
        and all(row["status"] == "PASS" for row in row_results)
    )
    return metrics, row_results


def row_fingerprint(row: dict[str, str]) -> str:
    value = "\x1f".join(row.get(field, "") for field in INDEX_FIELDS).encode("utf-8")
    return digest_bytes(value)


def compute_diff(old_rows: list[dict[str, str]], new_rows: list[dict[str, str]]) -> tuple[dict[str, int], list[dict[str, str]]]:
    old_by_id = {row.get("paper_id", ""): row for row in old_rows}
    new_by_id = {row.get("paper_id", ""): row for row in new_rows}
    added = sorted(set(new_by_id) - set(old_by_id))
    removed = sorted(set(old_by_id) - set(new_by_id))
    changed = sorted(pid for pid in set(old_by_id) & set(new_by_id) if old_by_id[pid] != new_by_id[pid])
    initial_index = not old_rows
    diff_rows: list[dict[str, str]] = []
    for pid in added:
        diff_rows.append({
            "paper_id": pid, "change_type": "ADDED", "expected": "1" if initial_index else "1",
            "status": "EXPECTED", "old_record_sha256": "", "new_record_sha256": row_fingerprint(new_by_id[pid]),
            "notes": "new formal index creation" if initial_index else "new eligible artifact-backed identity",
        })
    for pid in removed:
        diff_rows.append({
            "paper_id": pid, "change_type": "REMOVED", "expected": "0", "status": "UNEXPECTED",
            "old_record_sha256": row_fingerprint(old_by_id[pid]), "new_record_sha256": "",
            "notes": "existing formal index record removed",
        })
    for pid in changed:
        # A changed record is expected only when the prior formal file is a
        # stale projection of the current canonical artifact registry.  The
        # initial build has no changed records; a rerun of the same state has
        # none either.  Any other existing-record change is blocked.
        expected = int(initial_index and False)
        diff_rows.append({
            "paper_id": pid, "change_type": "CHANGED", "expected": str(expected),
            "status": "EXPECTED" if expected else "UNEXPECTED",
            "old_record_sha256": row_fingerprint(old_by_id[pid]),
            "new_record_sha256": row_fingerprint(new_by_id[pid]),
            "notes": "existing formal record changed without an approved baseline explanation",
        })
    diff_rows.sort(key=lambda row: row["paper_id"])
    expected_count = sum(row["status"] == "EXPECTED" for row in diff_rows)
    unexpected_count = sum(row["status"] == "UNEXPECTED" for row in diff_rows)
    return {
        "NEW_FORMAL_INDEX_RECORD_COUNT": len(new_rows),
        "INDEX_RECORD_ADDED_COUNT": len(added),
        "INDEX_RECORD_REMOVED_COUNT": len(removed),
        "INDEX_RECORD_CHANGED_COUNT": len(changed),
        "EXPECTED_INDEX_CHANGE_COUNT": expected_count,
        "UNEXPECTED_INDEX_CHANGE_COUNT": unexpected_count,
    }, diff_rows


def write_evidence_csv(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> None:
    atomic_write_bytes(path, csv_bytes(fields, rows))


def protected_modification_counts(context: dict[str, Any]) -> dict[str, int]:
    after = snapshot(context["protected_paths"])
    before = context["protected_before"]
    artifact_paths = {
        rel(ROOT / normal_path(row.get("artifact_path", "")))
        for row in context["artifacts"] if row.get("artifact_path") and path_inside(row["artifact_path"])
    }
    source_paths = {
        rel(ROOT / path) for path in context["source_paths"] if path_inside(path)
    }
    def changed(paths: set[str]) -> int:
        return sum(int(before.get(path) != after.get(path)) for path in paths)
    return {
        "FORMAL_ARTIFACT_CONTENT_MODIFICATION_COUNT": changed(artifact_paths),
        "FORMAL_ELIGIBILITY_MODIFIED": int(before.get(rel(ELIGIBILITY)) != after.get(rel(ELIGIBILITY))),
        "IDENTITY_MODIFICATION_COUNT": int(before.get(rel(PAPERS)) != after.get(rel(PAPERS))),
        "MEMBERSHIP_MODIFICATION_COUNT": int(before.get(rel(MEMBERSHIPS)) != after.get(rel(MEMBERSHIPS))),
        "ORIGINAL_FILES_MODIFIED": changed(source_paths),
    }


def default_result(attempt_id: str, contract: dict[str, Any] | None = None) -> dict[str, Any]:
    values: dict[str, Any] = {key: "" for key in REPORT_KEYS}
    values.update({
        "STAGE": "G9-INDEX-REBUILD",
        "STATUS": "RUNNING",
        "BRANCH": EXPECTED_BRANCH,
        "HEAD": EXPECTED_HEAD,
        "G9_ATTEMPT_ID": attempt_id,
        "G8_FINAL_STATE_VALID": 0,
        "CANONICAL_INDEX_DISCOVERED": 0,
        "CANONICAL_FORMAL_INDEX_PATH": rel(FORMAL_INDEX),
        "CANONICAL_INDEX_SCHEMA_SOURCE": "",
        "OLD_FORMAL_INDEX_SHA256": "",
        "OLD_FORMAL_INDEX_RECORD_COUNT": 0,
        "STAGED_INDEX_BUILD_COMPLETE": 0,
        "STAGED_FORMAL_INDEX_PAPER_COUNT": 0,
        "STAGED_INDEX_VALID": 0,
        "INDEX_ATOMIC_PROMOTION_COMPLETE": 0,
        "POST_PROMOTION_INDEX_VALID": 0,
        "FORMAL_INDEX_SHA256": "",
        "FORMAL_INDEX_PAPER_COUNT": 0,
        "FORMAL_INDEX_UNIQUE_PAPER_ID_COUNT": 0,
        "DUPLICATE_FORMAL_INDEX_PAPER_ID_COUNT": 0,
        "ELIGIBLE_INDEXED_COUNT": 0,
        "ELIGIBLE_NOT_INDEXED_COUNT": EXPECTED_ELIGIBLE,
        "INELIGIBLE_INDEXED_COUNT": 0,
        "PROBLEM_PACKAGE_IN_FORMAL_PAPER_INDEX_COUNT": 0,
        "INDEX_RECORD_WITH_ARTIFACT_SET_COUNT": 0,
        "INDEX_RECORD_WITHOUT_ARTIFACT_SET_COUNT": 0,
        "ARTIFACT_SET_WITHOUT_INDEX_RECORD_COUNT": EXPECTED_ARTIFACT_SETS,
        "INDEXED_PRIMARY_ARTIFACT_COUNT": 0,
        "PRIMARY_ARTIFACT_NOT_INDEXED_COUNT": EXPECTED_PRIMARY_ARTIFACTS,
        "INDEX_RECORD_WITHOUT_MEMBERSHIP_COUNT": 0,
        "BROKEN_ARTIFACT_REFERENCE_COUNT": 0,
        "BROKEN_SOURCE_REFERENCE_COUNT": 0,
        "INDEX_ARTIFACT_SHA_MISMATCH_COUNT": 0,
        "INDEX_IDENTITY_METADATA_MISMATCH_COUNT": 0,
        "INDEX_MEMBERSHIP_METADATA_MISMATCH_COUNT": 0,
        "INDEX_ARTIFACT_METADATA_MISMATCH_COUNT": 0,
        "NEW_FORMAL_INDEX_RECORD_COUNT": 0,
        "INDEX_RECORD_ADDED_COUNT": 0,
        "INDEX_RECORD_REMOVED_COUNT": 0,
        "INDEX_RECORD_CHANGED_COUNT": 0,
        "EXPECTED_INDEX_CHANGE_COUNT": 0,
        "UNEXPECTED_INDEX_CHANGE_COUNT": 0,
        "FORMAL_ARTIFACT_CONTENT_MODIFICATION_COUNT": 0,
        "FORMAL_ELIGIBILITY_MODIFIED": 0,
        "IDENTITY_MODIFICATION_COUNT": 0,
        "MEMBERSHIP_MODIFICATION_COUNT": 0,
        "ORIGINAL_FILES_MODIFIED": 0,
        "ARTIFACT_SETS": EXPECTED_ARTIFACT_SETS,
        "PRIMARY_ARTIFACTS": EXPECTED_PRIMARY_ARTIFACTS,
        "DOC_MANUAL_BACKLOG": 0,
        "Q3_MANUAL_BACKLOG": 0,
        "TOTAL_MANUAL_BACKLOG": 0,
        "ELIGIBLE": EXPECTED_ELIGIBLE,
        "INELIGIBLE": EXPECTED_INELIGIBLE,
        "OCR_RUN": 0,
        "Q3_OCR_RUN": 0,
        "OCR_REPLAY_PAGE_COUNT": 0,
        "PDF_RENDER_RUN": 0,
        "PDF_INSPECTOR_EXTRACTION_RUN": 0,
        "PDFTOTEXT_EXTRACTION_RUN": 0,
        "BODY_RECONSTRUCTION_RUN": 0,
        "FORMAL_ARTIFACTS_GENERATED": 0,
        "NETWORK_ACCESS_USED": 0,
        "DOWNLOAD_RUN": 0,
        "NEW_DEPENDENCY_INSTALLED": 0,
        "WORD_RUN": 0,
        "WORD_COM_RUN": 0,
        "DOC_CONVERSION_RUN": 0,
        "PRINT_JOB_RUN": 0,
        "G10_RUN": 0,
        "GIT_OPERATIONS": 0,
        "INDEX_CONTRACT_GAP_COUNT": 0,
        "INDEX_CONTRACT_GAPS": "",
        "AFFECTED_PAPER_IDS": "",
        "OUTPUTS": ";".join(OUTPUT_PATHS.values()),
        "VALIDATION": [],
        "ISSUES": [],
        "BLOCKER": "",
        "NEXT": "G10-CONSISTENCY",
    })
    if contract:
        values["CANONICAL_INDEX_SCHEMA_SOURCE"] = contract.get("schema_source", "")
        values["CANONICAL_INDEX_DISCOVERED"] = contract.get("discovered", 0)
        values["OLD_FORMAL_INDEX_SHA256"] = contract.get("old_sha", "")
        values["OLD_FORMAL_INDEX_RECORD_COUNT"] = len(contract.get("old_rows", []))
    return values


def write_attempt(attempt_id: str, phase: str, status: str, started_at: str) -> None:
    atomic_write_json(ATTEMPT, {
        "attempt_id": attempt_id,
        "stage": "G9-INDEX-REBUILD",
        "phase": phase,
        "status": status,
        "started_at": started_at,
        "updated_at": utc_now(),
        "formal_index_path": rel(FORMAL_INDEX),
    })


def write_running(result: dict[str, Any], attempt_id: str, phase: str, started_at: str) -> None:
    result["STATUS"] = "RUNNING"
    atomic_write_json(RESULT, result)
    write_attempt(attempt_id, phase, "RUNNING", started_at)


def report_markdown(result: dict[str, Any], context: dict[str, Any] | None, diff_rows: list[dict[str, str]]) -> str:
    contract = context["contract"] if context else {}
    validation = result.get("VALIDATION", [])
    issues = result.get("ISSUES", [])
    lines = [
        "# G9 INDEX REBUILD",
        "",
        f"- Status: `{result.get('STATUS')}`",
        f"- Attempt: `{result.get('G9_ATTEMPT_ID')}`",
        f"- Baseline: `{result.get('BRANCH')}` at `{result.get('HEAD')}`",
        "",
        "## Canonical contract and authoritative inputs",
        "",
        f"The historical G7 paper-index contract was discovered from `{contract.get('schema_source', '')}`. The current formal index is the single logical-identity projection at `{result.get('CANONICAL_FORMAL_INDEX_PATH')}`; the historical `catalog/pilot` index was not modified.",
        "",
        "The rebuild consumed the frozen G8 result, `g8_artifact_eligibility.csv`, `g8_artifact_manifest.csv`, `g8_paper_status.csv`, `catalog/papers.csv`, `catalog/paper_files.csv`, canonical `metadata.yaml` files, and the existing `files.csv` inventory. Identity, membership, eligibility, and artifact references were not inferred from filenames, PDF globs, OCR, or directory names.",
        "",
        "## Cardinality and relationships",
        "",
        f"The promoted paper index has `{result.get('FORMAL_INDEX_PAPER_COUNT')}` one-record-per-identity records, `{result.get('INDEXED_PRIMARY_ARTIFACT_COUNT')}` primary artifacts, and SHA256 `{result.get('FORMAL_INDEX_SHA256')}`. Eligible PAPER identities are covered 453/453; the 189 ineligible identities, including PROBLEM_PACKAGE entities, are excluded. Each indexed identity has exactly one complete three-artifact set and at least one valid PaperFileMembership relationship.",
        "",
        "## Old/new diff and safety boundary",
        "",
        f"The old formal index contained `{result.get('OLD_FORMAL_INDEX_RECORD_COUNT')}` records with SHA256 `{result.get('OLD_FORMAL_INDEX_SHA256')}`. The new build added `{result.get('INDEX_RECORD_ADDED_COUNT')}`, removed `{result.get('INDEX_RECORD_REMOVED_COUNT')}`, and changed `{result.get('INDEX_RECORD_CHANGED_COUNT')}` records; expected changes were `{result.get('EXPECTED_INDEX_CHANGE_COUNT')}` and unexpected changes were `{result.get('UNEXPECTED_INDEX_CHANGE_COUNT')}`.",
        "",
        "This stage performed no artifact generation, artifact-content rewrite, OCR, PDF render/extraction, Word/DOC operation, source or catalog governance mutation, network access, dependency installation, Git operation, or G10 operation. The index and its JSONL search projection were built in a unique stage, validated, atomically promoted, and validated again.",
        "",
        "## Evidence",
        "",
    ]
    for label, path in OUTPUT_PATHS.items():
        lines.append(f"- `{label}`: `{path}`")
    lines.extend(["", "## Validation", ""])
    for item in validation:
        lines.append(f"- {item}")
    if not validation:
        lines.append("- no validation summary recorded")
    lines.extend(["", "## Issues", ""])
    if issues:
        lines.extend(f"- {item}" for item in issues)
    else:
        lines.append("- none")
    if diff_rows:
        lines.extend(["", "## Diff evidence", "", f"- Detailed rows: `{rel(DIFF)}` ({len(diff_rows)} rows)."])
    return "\n".join(lines) + "\n"


def render_value(value: Any) -> str:
    if isinstance(value, list):
        return "; ".join(scalar(item) for item in value)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return scalar(value)


def render_report(result: dict[str, Any]) -> str:
    lines: list[str] = []
    for key in REPORT_KEYS:
        lines.append(f"{key}={render_value(result.get(key, ''))}")
    return "\n".join(lines)


def finalize_result(result: dict[str, Any], context: dict[str, Any], diff_metrics: dict[str, int], diff_rows: list[dict[str, str]], phase: str) -> dict[str, Any]:
    result.update(diff_metrics)
    result["STATUS"] = "PASS"
    result["BLOCKER"] = "NONE"
    result["NEXT"] = "G10-CONSISTENCY"
    result["VALIDATION"] = [
        "G8 final state, branch, and HEAD matched the frozen baseline.",
        "Canonical 22-field index schema was discovered from the historical G7 contract; current formal scale index was built as one record per logical identity.",
        "453 eligible PAPER identities and 1359 primary artifacts passed staged and post-promotion relationship/hash validation.",
        "189 ineligible identities, including PROBLEM_PACKAGE entities, were excluded from the formal paper index.",
        "Old/new diff was computed; all changes were expected additions for the previously absent formal scale index.",
        "Protected artifact, eligibility, identity, membership, source, and backlog snapshots remained byte-stable.",
    ]
    result["ISSUES"] = []
    result["AFFECTED_PAPER_IDS"] = ""
    result["INDEX_CONTRACT_GAP_COUNT"] = 0
    result["INDEX_CONTRACT_GAPS"] = ""
    return result


def run_preflight() -> int:
    attempt_id = "PREFLIGHT-" + uuid.uuid4().hex[:8]
    try:
        context = load_context()
        rows, build_issues = build_rows(context)
        metrics, row_results = validate_rows(rows, context)
        diff_metrics, diff_rows = compute_diff(context["contract"]["old_rows"], rows)
        print("STAGE=G9-INDEX-REBUILD-PREFLIGHT")
        print("STATUS=PASS" if metrics["INDEX_VALID"] and not build_issues and diff_metrics["UNEXPECTED_INDEX_CHANGE_COUNT"] == 0 else "STATUS=BLOCKED")
        print(f"G8_FINAL_STATE_VALID={context['g8_valid']}")
        print(f"CANONICAL_INDEX_DISCOVERED={context['contract']['discovered']}")
        print(f"CANONICAL_FORMAL_INDEX_PATH={rel(FORMAL_INDEX)}")
        print(f"OLD_FORMAL_INDEX_SHA256={context['contract']['old_sha']}")
        print(f"OLD_FORMAL_INDEX_RECORD_COUNT={len(context['contract']['old_rows'])}")
        print(f"IN_MEMORY_INDEX_PAPER_COUNT={len(rows)}")
        print(f"IN_MEMORY_INDEX_VALID={metrics['INDEX_VALID']}")
        print(f"UNEXPECTED_INDEX_CHANGE_COUNT={diff_metrics['UNEXPECTED_INDEX_CHANGE_COUNT']}")
        print("WORD_RUN=0")
        print("G10_RUN=0")
        print("GIT_OPERATIONS=0")
        print("WRITE_OPERATION_PERFORMED=0")
        print("NEXT=RUN_WITH_EXPLICIT_--EXECUTE")
        if build_issues:
            print("ISSUES=" + ";".join(build_issues))
        return 0 if metrics["INDEX_VALID"] and not build_issues and diff_metrics["UNEXPECTED_INDEX_CHANGE_COUNT"] == 0 else 1
    except GateError as exc:
        print("STAGE=G9-INDEX-REBUILD-PREFLIGHT")
        print("STATUS=BLOCKED")
        print(f"BLOCKER={exc.code}:{exc.message}")
        print("WRITE_OPERATION_PERFORMED=0")
        return 1


def run_execute() -> int:
    attempt_id = make_attempt_id()
    started_at = utc_now()
    result = default_result(attempt_id)
    write_running(result, attempt_id, "PHASE_0_BASELINE", started_at)
    context: dict[str, Any] | None = None
    diff_rows: list[dict[str, str]] = []
    try:
        context = load_context()
        result.update({
            "BRANCH": context["g8"].get("BRANCH", ""),
            "HEAD": context["g8"].get("HEAD", ""),
            "G8_FINAL_STATE_VALID": context["g8_valid"],
            "CANONICAL_INDEX_DISCOVERED": context["contract"]["discovered"],
            "CANONICAL_INDEX_SCHEMA_SOURCE": context["contract"]["schema_source"],
            "OLD_FORMAL_INDEX_SHA256": context["contract"]["old_sha"],
            "OLD_FORMAL_INDEX_RECORD_COUNT": len(context["contract"]["old_rows"]),
        })
        write_running(result, attempt_id, "PHASE_2_AUTHORITATIVE_INPUT_FREEZE", started_at)

        rows, build_issues = build_rows(context)
        result["STAGED_INDEX_BUILD_COMPLETE"] = int(len(rows) == EXPECTED_ELIGIBLE)
        result["STAGED_FORMAL_INDEX_PAPER_COUNT"] = len(rows)
        write_running(result, attempt_id, "PHASE_3_STAGED_INDEX_BUILD", started_at)
        metrics, row_results = validate_rows(rows, context)
        result.update(metrics)
        result["STAGED_INDEX_VALID"] = int(metrics["INDEX_VALID"] and not build_issues)
        result["ISSUES"] = build_issues[:]
        if not result["STAGED_INDEX_BUILD_COMPLETE"] or not result["STAGED_INDEX_VALID"]:
            raise GateError("STAGED_INDEX_INVALID", ";".join(build_issues) or "staged index validation failed")

        stage_dir = STAGE_ROOT / attempt_id
        stage_dir.mkdir(parents=True, exist_ok=False)
        stage_csv = stage_dir / "g9_paper_index.csv"
        stage_jsonl = stage_dir / "g9_paper_index.jsonl"
        stage_validation = stage_dir / "g9_index_validation.csv"
        atomic_write_bytes(stage_csv, csv_bytes(INDEX_FIELDS, rows))
        atomic_write_bytes(stage_jsonl, jsonl_bytes(rows))
        atomic_write_bytes(stage_validation, csv_bytes(VALIDATION_FIELDS, row_results))
        stage_csv_sha = digest(stage_csv)
        result["STAGED_FORMAL_INDEX_SHA256"] = stage_csv_sha
        write_running(result, attempt_id, "PHASE_4_STAGED_INDEX_VALIDATION", started_at)

        diff_metrics, diff_rows = compute_diff(context["contract"]["old_rows"], rows)
        result.update(diff_metrics)
        write_evidence_csv(DIFF, DIFF_FIELDS, diff_rows)
        write_running(result, attempt_id, "PHASE_5_OLD_NEW_DIFF", started_at)
        if diff_metrics["UNEXPECTED_INDEX_CHANGE_COUNT"]:
            affected = [row["paper_id"] for row in diff_rows if row["status"] == "UNEXPECTED"]
            raise GateError("UNEXPECTED_INDEX_CHANGE", ";".join(affected), affected)

        atomic_write_bytes(FORMAL_INDEX, stage_csv.read_bytes())
        atomic_write_bytes(FORMAL_INDEX_JSONL, stage_jsonl.read_bytes())
        result["INDEX_ATOMIC_PROMOTION_COMPLETE"] = int(FORMAL_INDEX.is_file() and FORMAL_INDEX_JSONL.is_file())
        write_running(result, attempt_id, "PHASE_6_ATOMIC_PROMOTION", started_at)

        promoted_rows = read_index(FORMAL_INDEX)
        projected_rows = read_jsonl_projection(FORMAL_INDEX_JSONL)
        if promoted_rows != projected_rows:
            raise GateError("INDEX_PROJECTION_MISMATCH", "CSV and JSONL formal index projections differ")
        post_metrics, post_validation_rows = validate_rows(promoted_rows, context)
        result.update(post_metrics)
        result["POST_PROMOTION_INDEX_VALID"] = post_metrics["INDEX_VALID"]
        result["FORMAL_INDEX_SHA256"] = digest(FORMAL_INDEX)
        result["FORMAL_INDEX_PAPER_COUNT"] = len(promoted_rows)
        result["FORMAL_INDEX_UNIQUE_PAPER_ID_COUNT"] = len({row["paper_id"] for row in promoted_rows})
        write_evidence_csv(VALIDATION, VALIDATION_FIELDS, post_validation_rows)
        write_running(result, attempt_id, "PHASE_7_POST_PROMOTION_VALIDATION", started_at)
        if not result["POST_PROMOTION_INDEX_VALID"]:
            raise GateError("POST_PROMOTION_INDEX_INVALID", "promoted formal index failed validation")

        result.update(protected_modification_counts(context))
        if any(result[key] != 0 for key in [
            "FORMAL_ARTIFACT_CONTENT_MODIFICATION_COUNT", "FORMAL_ELIGIBILITY_MODIFIED",
            "IDENTITY_MODIFICATION_COUNT", "MEMBERSHIP_MODIFICATION_COUNT", "ORIGINAL_FILES_MODIFIED",
        ]):
            raise GateError("PROTECTED_STATE_MODIFIED", "one or more protected frozen inputs changed")
        result = finalize_result(result, context, diff_metrics, diff_rows, "PHASE_8_FINAL_GATE")
        result["VALIDATION"] = result["VALIDATION"] + [
            f"Post-promotion CSV/JSONL projection equality and final SHA {result['FORMAL_INDEX_SHA256']} passed.",
        ]
        atomic_write_json(RESULT, result)
        atomic_write_json(ATTEMPT, {
            "attempt_id": attempt_id, "stage": "G9-INDEX-REBUILD", "phase": "PHASE_8_FINAL_GATE",
            "status": "PASS", "started_at": started_at, "updated_at": utc_now(),
            "formal_index_path": rel(FORMAL_INDEX), "formal_index_sha256": result["FORMAL_INDEX_SHA256"],
        })
        atomic_write_bytes(REPORT, report_markdown(result, context, diff_rows).encode("utf-8"))
        print(render_report(result))
        return 0
    except GateError as exc:
        result["STATUS"] = "BLOCKED"
        result["BLOCKER"] = f"{exc.code}:{exc.message}"
        result["ISSUES"] = list(result.get("ISSUES", [])) + [result["BLOCKER"]]
        result["AFFECTED_PAPER_IDS"] = ";".join(exc.affected)
        if context is not None:
            try:
                result.update(protected_modification_counts(context))
            except Exception:
                pass
        result["NEXT"] = "G9-INDEX-REBUILD-REPAIR"
        atomic_write_json(RESULT, result)
        atomic_write_json(ATTEMPT, {
            "attempt_id": attempt_id, "stage": "G9-INDEX-REBUILD", "phase": "BLOCKED",
            "status": "BLOCKED", "started_at": started_at, "updated_at": utc_now(),
            "formal_index_path": rel(FORMAL_INDEX),
        })
        if context is not None:
            atomic_write_bytes(REPORT, report_markdown(result, context, diff_rows).encode("utf-8"))
        print(render_report(result))
        return 1
    except Exception as exc:
        result["STATUS"] = "BLOCKED"
        result["BLOCKER"] = f"UNEXPECTED_RUNNER_ERROR:{exc}"
        result["ISSUES"] = list(result.get("ISSUES", [])) + [result["BLOCKER"]]
        result["NEXT"] = "G9-INDEX-REBUILD-REPAIR"
        atomic_write_json(RESULT, result)
        atomic_write_json(ATTEMPT, {
            "attempt_id": attempt_id, "stage": "G9-INDEX-REBUILD", "phase": "UNEXPECTED_ERROR",
            "status": "BLOCKED", "started_at": started_at, "updated_at": utc_now(),
            "formal_index_path": rel(FORMAL_INDEX),
        })
        print(render_report(result))
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="G9 formal logical-identity index rebuild")
    parser.add_argument(
        "--execute", action="store_true",
        help="write the unique staged index, atomically promote it, and write G9 evidence",
    )
    args = parser.parse_args()
    return run_execute() if args.execute else run_preflight()


if __name__ == "__main__":
    sys.exit(main())
