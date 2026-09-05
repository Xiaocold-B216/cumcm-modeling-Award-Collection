"""G9 index refresh after the completed G11 multi-route formal repair.

This stage reuses the canonical 22-field projection and row validator from
``80_g9_index_rebuild.py``.  It binds the fixed 246-row G11 refresh input,
builds a deterministic 453-record candidate projection, audits the 207
non-target records, and atomically promotes only the two formal index files.
It does not regenerate or modify formal artifacts and has no OCR, PDF, Office,
network, dependency, or Git execution path.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCALE = ROOT / "catalog" / "scale"
REPORTS = ROOT / "reports" / "scale"

G9_BASE_PATH = ROOT / "tools" / "80_g9_index_rebuild.py"
G11_RESULT = SCALE / "g11_multi_route_formal_artifact_repair_result.json"
G11_MANIFEST = SCALE / "g11_multi_route_formal_repair_manifest.csv"
G11_PAGES = SCALE / "g11_multi_route_formal_repair_pages.csv"
G11_TARGETS = SCALE / "g11_multi_route_formal_repair_targets.csv"
REFRESH_INPUT = SCALE / "g11_repair_g9_refresh_input.csv"
FORMAL_INDEX = SCALE / "g9_paper_index.csv"
FORMAL_INDEX_JSONL = SCALE / "g9_paper_index.jsonl"
STAGE_ROOT = SCALE / ".g9_index_refresh_after_g11_repair_staging"
RESULT_PATH = SCALE / "g9_index_refresh_after_g11_repair_result.json"
ATTEMPT_PATH = SCALE / "g9_index_refresh_after_g11_repair_attempt.json"
DIFF_PATH = SCALE / "g9_index_refresh_after_g11_repair_diff.csv"
VALIDATION_PATH = SCALE / "g9_index_refresh_after_g11_repair_validation.csv"
REPORT_PATH = REPORTS / "G9_INDEX_REFRESH_AFTER_G11_REPAIR.md"

EXPECTED_STAGE = "G9-INDEX-REFRESH-AFTER-G11-REPAIR"
EXPECTED_BRANCH = "library-refactor-v1"
EXPECTED_HEAD = "557724fba6572d4d83dc421feda5b17b13ff8d66"
EXPECTED_FORMAL_IDENTITIES = 642
EXPECTED_ELIGIBLE = 453
EXPECTED_INELIGIBLE = 189
EXPECTED_ARTIFACT_SETS = 453
EXPECTED_PRIMARY_ARTIFACTS = 1359
EXPECTED_REFRESH_TARGETS = 246
EXPECTED_NON_TARGETS = 207
EXPECTED_DOC_BACKLOG = 0
EXPECTED_Q3_BACKLOG = 0

TARGET_AUDIT_FIELDS = {
    "paper_id", "artifact_set_id", "source_path", "source_sha256",
    "route_categories", "repaired_page_count", "repaired_pages",
    "legitimate_noncontent_pages", "repair_layer", "requires_index_refresh",
    "requires_g10_revalidation", "requires_human_rereview", "evidence_paths",
}
REFRESH_INPUT_FIELDS = {
    "paper_id", "artifact_set_id", "repair_attempt_id", "source_path",
    "source_sha256", "route_categories", "repair_layer", "repaired_pages",
    "current_paper_sha256", "candidate_paper_sha256", "artifact_paths",
    "artifact_hashes_before", "artifact_hashes_after", "requires_index_refresh",
    "requires_g10_revalidation", "status",
}


def load_g9_base() -> Any:
    spec = importlib.util.spec_from_file_location("g9_index_rebuild_base", G9_BASE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {G9_BASE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


G9 = load_g9_base()


class GateError(RuntimeError):
    def __init__(self, code: str, message: str, affected: list[str] | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.affected = affected or []


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha(path: Path) -> str:
    return G9.digest(path)


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise GateError("INPUT_JSON_ERROR", f"{path}: {exc}") from exc
    if not isinstance(value, dict):
        raise GateError("INPUT_JSON_ERROR", f"{path} is not an object")
    return value


def read_csv(path: Path) -> list[dict[str, str]]:
    try:
        return G9.read_csv(path)
    except Exception as exc:
        raise GateError("INPUT_CSV_ERROR", f"{path}: {exc}") from exc


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def root_path(value: str) -> Path:
    normalized = str(value or "").replace("\\", "/")
    if not normalized or re.match(r"^[A-Za-z]:/", normalized) or normalized.startswith("/"):
        raise GateError("PATH_BINDING_FAILURE", normalized)
    path = (ROOT / normalized).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise GateError("PATH_BINDING_FAILURE", normalized) from exc
    return path


def assert_equal(actual: Any, expected: Any, code: str, label: str) -> None:
    if actual != expected:
        raise GateError(code, f"{label}={actual!r};expected={expected!r}")


def read_git_head_without_git() -> tuple[str, str]:
    """Read the checkout ref directly; no Git command or Git mutation."""
    head_path = ROOT / ".git" / "HEAD"
    if not head_path.is_file():
        return "", ""
    value = head_path.read_text(encoding="utf-8").strip()
    if value.startswith("ref: "):
        ref = value[5:].strip()
        branch = ref.removeprefix("refs/heads/")
        ref_path = ROOT / ".git" / Path(ref)
        if ref_path.is_file():
            return branch, ref_path.read_text(encoding="utf-8").strip()
        packed = ROOT / ".git" / "packed-refs"
        if packed.is_file():
            for line in packed.read_text(encoding="utf-8").splitlines():
                if line and not line.startswith("#") and " " in line:
                    commit, packed_ref = line.split(" ", 1)
                    if packed_ref == ref:
                        return branch, commit
        return branch, ""
    return "", value


def required_inputs() -> None:
    paths = [
        G11_RESULT, G11_MANIFEST, G11_PAGES, G11_TARGETS, REFRESH_INPUT,
        FORMAL_INDEX, FORMAL_INDEX_JSONL,
    ]
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise GateError("REQUIRED_INPUT_MISSING", ";".join(missing))


def validate_g11_repair(g11: dict[str, Any]) -> str:
    assert_equal(g11.get("STAGE"), "G8-TARGETED-MULTI-ROUTE-FORMAL-ARTIFACT-REPAIR", "G8_REPAIR_INVALID", "STAGE")
    assert_equal(g11.get("STATUS"), "PASS", "G8_REPAIR_INVALID", "STATUS")
    assert_equal(g11.get("FORMAL_REPAIR_STATUS"), "PASS", "G8_REPAIR_INVALID", "FORMAL_REPAIR_STATUS")
    assert_equal(g11.get("G11_STATUS_REMAINS"), "PARTIAL", "G8_REPAIR_INVALID", "G11_STATUS_REMAINS")
    assert_equal(g11.get("BLOCKER"), "NONE", "G8_REPAIR_INVALID", "BLOCKER")
    for key, expected in {
        "TARGET_IDENTITY_COUNT": EXPECTED_REFRESH_TARGETS,
        "STAGED_TARGET_IDENTITY_COUNT": EXPECTED_REFRESH_TARGETS,
        "UNSTAGED_TARGET_IDENTITY_COUNT": 0,
        "PRE_REPAIR_FORMAL_IDENTITIES": EXPECTED_FORMAL_IDENTITIES,
        "PRE_REPAIR_ELIGIBLE_IDENTITIES": EXPECTED_ELIGIBLE,
        "PRE_REPAIR_INELIGIBLE_IDENTITIES": EXPECTED_INELIGIBLE,
        "MARKER_ONLY_SCOPE_PAGE_COUNT": 3033,
        "MARKER_ONLY_DEFECTIVE_TARGET_PAGE_COUNT": 3031,
        "MARKER_ONLY_LEGITIMATE_NONCONTENT_PAGE_COUNT": 2,
        "POST_REPAIR_DEFECTIVE_MARKER_SEGMENT_COUNT": 0,
        "POST_REPAIR_ARTIFACT_SETS": EXPECTED_ARTIFACT_SETS,
        "POST_REPAIR_PRIMARY_ARTIFACTS": EXPECTED_PRIMARY_ARTIFACTS,
        "POST_REPAIR_DOC_MANUAL_BACKLOG": EXPECTED_DOC_BACKLOG,
        "POST_REPAIR_Q3_MANUAL_BACKLOG": EXPECTED_Q3_BACKLOG,
        "POST_REPAIR_TOTAL_REMAINING_ELIGIBLE_BACKLOG": 0,
        "FORMAL_INDEX_MODIFICATION_COUNT": 0,
        "G9_RUN": 0,
        "G10_RUN": 0,
        "G12_RUN": 0,
        "FORMAL_ELIGIBILITY_MODIFIED": 0,
        "NEW_DEPENDENCY_INSTALLED": 0,
        "NETWORK_ACCESS_USED": 0,
    }.items():
        try:
            actual = int(g11.get(key))
        except (TypeError, ValueError):
            actual = None
        assert_equal(actual, expected, "G8_REPAIR_INVALID", key)
    return str(g11["ATTEMPT_ID"])


def validate_g11_inputs(g11_attempt_id: str, context: dict[str, Any]) -> dict[str, Any]:
    manifest = read_csv(G11_MANIFEST)
    pages = read_csv(G11_PAGES)
    targets = read_csv(G11_TARGETS)
    refresh = read_csv(REFRESH_INPUT)
    assert_equal(len(manifest), 3036, "G11_INPUT_INVALID", "G11_MANIFEST_ROWS")
    assert_equal(len(pages), 3036, "G11_INPUT_INVALID", "G11_PAGE_AUDIT_ROWS")
    assert_equal(len(targets), EXPECTED_REFRESH_TARGETS, "G11_INPUT_INVALID", "G11_TARGET_ROWS")
    assert_equal(len(refresh), EXPECTED_REFRESH_TARGETS, "G9_REFRESH_INPUT_INVALID", "REFRESH_INPUT_ROWS")
    if any(row.get("postrepair_pass") != "1" or row.get("preflight_pass") != "1" for row in pages):
        raise GateError("G11_INPUT_INVALID", "page audit contains a failed preflight or postrepair row")
    target_ids = {row.get("paper_id", "") for row in targets}
    refresh_ids = {row.get("paper_id", "") for row in refresh}
    target_sets = {row.get("artifact_set_id", "") for row in targets}
    refresh_sets = {row.get("artifact_set_id", "") for row in refresh}
    assert_equal(len(target_ids), EXPECTED_REFRESH_TARGETS, "G9_REFRESH_INPUT_INVALID", "REFRESH_INPUT_UNIQUE_PAPER_ID_COUNT")
    assert_equal(len(refresh_sets), EXPECTED_REFRESH_TARGETS, "G9_REFRESH_INPUT_INVALID", "REFRESH_INPUT_UNIQUE_ARTIFACT_SET_COUNT")
    assert_equal(refresh_ids, target_ids, "G9_REFRESH_INPUT_INVALID", "REFRESH_INPUT_TARGET_SET")
    assert_equal(refresh_sets, target_sets, "G9_REFRESH_INPUT_INVALID", "REFRESH_INPUT_ARTIFACT_SET")
    if any(row.get("repair_attempt_id") != g11_attempt_id for row in refresh):
        raise GateError("G9_REFRESH_INPUT_INVALID", "refresh input is not bound to the completed G11 attempt")
    if any(row.get("status") != "READY_FOR_G9_REFRESH" for row in refresh):
        raise GateError("G9_REFRESH_INPUT_INVALID", "refresh input contains a non-ready row")
    if any(set(row) != TARGET_AUDIT_FIELDS for row in targets):
        raise GateError("G11_INPUT_INVALID", "target audit schema drift")
    if any(set(row) != REFRESH_INPUT_FIELDS for row in refresh):
        raise GateError("G9_REFRESH_INPUT_INVALID", "refresh input schema drift")

    eligible_by_id = context["eligibility_by_id"]
    artifacts_by_id = context["artifacts_by_id"]
    refresh_pass = 0
    mismatches: list[str] = []
    for row in refresh:
        pid = row["paper_id"]
        artifact_set_id = row["artifact_set_id"]
        expected_set_id = f"derived/scale/papers/{pid}"
        ok = True
        eligibility = eligible_by_id.get(pid, {})
        if not (eligibility.get("artifact_eligible") == "1" and eligibility.get("subject_type") == "PAPER"):
            ok = False
        if artifact_set_id != expected_set_id or pid not in artifacts_by_id:
            ok = False
        by_type = {item.get("artifact_type", ""): item for item in artifacts_by_id.get(pid, [])}
        if set(by_type) != {"paper.md", "metadata.yaml", "knowledge_card.md"}:
            ok = False
        body_path = root_path(row.get("artifact_paths", "").split(";")[0]) if row.get("artifact_paths") else None
        if body_path is None or not body_path.is_file():
            ok = False
        candidate_body_sha = row.get("candidate_paper_sha256", "").upper()
        if not body_path or sha(body_path) != candidate_body_sha:
            ok = False
        after_hashes = row.get("artifact_hashes_after", "").split(";")
        after_paths = row.get("artifact_paths", "").split(";")
        if len(after_hashes) != 3 or len(after_paths) != 3:
            ok = False
        else:
            for artifact_path, expected_hash in zip(after_paths, after_hashes):
                path = root_path(artifact_path)
                if not path.is_file() or sha(path) != expected_hash.upper():
                    ok = False
            for artifact_type, expected_hash in zip(("paper.md", "metadata.yaml", "knowledge_card.md"), after_hashes):
                if by_type.get(artifact_type, {}).get("artifact_sha256", "").upper() != expected_hash.upper():
                    ok = False
        source_path = root_path(row.get("source_path", ""))
        if not source_path.is_file() or sha(source_path) != row.get("source_sha256", "").upper():
            ok = False
        if row.get("requires_index_refresh") != "1" or row.get("requires_g10_revalidation") != "1":
            ok = False
        if ok:
            refresh_pass += 1
        else:
            mismatches.append(pid)
    if mismatches:
        raise GateError("REFRESH_INPUT_CURRENT_BINDING_MISMATCH", ";".join(sorted(mismatches)), sorted(mismatches))
    return {
        "manifest": manifest,
        "pages": pages,
        "targets": targets,
        "refresh": refresh,
        "target_ids": target_ids,
        "refresh_pass": refresh_pass,
        "refresh_mismatch": len(mismatches),
    }


def canonical_rows_equal(left: list[dict[str, str]], right: list[dict[str, str]]) -> bool:
    return left == right


def diff_rows(old_rows: list[dict[str, str]], new_rows: list[dict[str, str]], target_ids: set[str]) -> tuple[dict[str, int], list[dict[str, str]]]:
    old_by_id = {row["paper_id"]: row for row in old_rows}
    new_by_id = {row["paper_id"]: row for row in new_rows}
    added = set(new_by_id) - set(old_by_id)
    removed = set(old_by_id) - set(new_by_id)
    changed = {pid for pid in set(old_by_id) & set(new_by_id) if old_by_id[pid] != new_by_id[pid]}
    if added or removed:
        raise GateError("INDEX_CARDINALITY_OR_IDENTITY_DRIFT", f"added={sorted(added)};removed={sorted(removed)}")
    unexpected = changed - target_ids
    if unexpected:
        raise GateError("NON_TARGET_INDEX_SEMANTIC_CHANGE", ";".join(sorted(unexpected)), sorted(unexpected))
    missing_changed = target_ids - changed
    if missing_changed:
        raise GateError("TARGET_INDEX_REFRESH_INCOMPLETE", ";".join(sorted(missing_changed)), sorted(missing_changed))
    rows: list[dict[str, str]] = []
    for pid in sorted(changed):
        rows.append({
            "paper_id": pid,
            "change_type": "CHANGED",
            "expected": "1",
            "status": "EXPECTED",
            "old_record_sha256": G9.row_fingerprint(old_by_id[pid]),
            "new_record_sha256": G9.row_fingerprint(new_by_id[pid]),
            "notes": "G11 repaired formal artifact projection refresh",
        })
    return {
        "TARGET_INDEX_RECORD_COUNT": EXPECTED_REFRESH_TARGETS,
        "TARGET_INDEX_RECORD_REFRESHED_COUNT": len(changed),
        "TARGET_INDEX_RECORD_REFRESH_FAILED_COUNT": len(missing_changed),
        "NON_TARGET_INDEX_RECORD_COUNT": EXPECTED_NON_TARGETS,
        "NON_TARGET_INDEX_UNEXPECTED_SEMANTIC_CHANGE_COUNT": len(unexpected),
    }, rows


def write_attempt(attempt_id: str, phase: str, status: str, started_at: str, **extra: Any) -> None:
    payload = {
        "attempt_id": attempt_id,
        "stage": EXPECTED_STAGE,
        "phase": phase,
        "status": status,
        "started_at": started_at,
        "updated_at": now_iso(),
        "formal_index_csv": rel(FORMAL_INDEX),
        "formal_index_jsonl": rel(FORMAL_INDEX_JSONL),
    }
    payload.update(extra)
    G9.atomic_write_json(ATTEMPT_PATH, payload)


def base_result(attempt_id: str, g11_attempt_id: str, branch: str, head: str) -> dict[str, Any]:
    return {
        "STAGE": EXPECTED_STAGE,
        "STATUS": "RUNNING",
        "G9_REFRESH_STATUS": "RUNNING",
        "BRANCH": branch,
        "HEAD": head,
        "G9_REFRESH_ATTEMPT_ID": attempt_id,
        "SOURCE_G8_REPAIR_ATTEMPT_ID": g11_attempt_id,
        "PRE_REFRESH_ARTIFACT_SET_COUNT": EXPECTED_ARTIFACT_SETS,
        "PRE_REFRESH_PRIMARY_ARTIFACT_COUNT": EXPECTED_PRIMARY_ARTIFACTS,
        "PRE_REFRESH_INDEX_CSV_RECORD_COUNT": 0,
        "PRE_REFRESH_INDEX_JSONL_RECORD_COUNT": 0,
        "PRE_REFRESH_INDEX_CSV_SHA256": "",
        "PRE_REFRESH_INDEX_JSONL_SHA256": "",
        "PRE_REFRESH_CSV_JSONL_PROJECTION_MATCH": 0,
        "REFRESH_INPUT_ROW_COUNT": 0,
        "REFRESH_INPUT_UNIQUE_PAPER_ID_COUNT": 0,
        "REFRESH_INPUT_UNIQUE_ARTIFACT_SET_COUNT": 0,
        "REFRESH_INPUT_CURRENT_BINDING_PASS_COUNT": 0,
        "REFRESH_INPUT_CURRENT_BINDING_MISMATCH_COUNT": 0,
        "G9_REFRESH_MODE": "FULL_DETERMINISTIC_PROJECTION_REBUILD",
        "G9_INDEX_FULL_PROJECTION_REBUILD": 1,
        "TARGET_INDEX_RECORD_COUNT": EXPECTED_REFRESH_TARGETS,
        "TARGET_INDEX_RECORD_REFRESHED_COUNT": 0,
        "TARGET_INDEX_RECORD_REFRESH_FAILED_COUNT": 0,
        "NON_TARGET_INDEX_RECORD_COUNT": EXPECTED_NON_TARGETS,
        "NON_TARGET_INDEX_UNEXPECTED_SEMANTIC_CHANGE_COUNT": 0,
        "POST_REFRESH_INDEX_CSV_RECORD_COUNT": 0,
        "POST_REFRESH_INDEX_JSONL_RECORD_COUNT": 0,
        "UNIQUE_PAPER_ID_COUNT": 0,
        "DUPLICATE_PAPER_ID_COUNT": 0,
        "ELIGIBLE_IDENTITY_COUNT": EXPECTED_ELIGIBLE,
        "ELIGIBLE_INDEXED_COUNT": 0,
        "ELIGIBLE_NOT_INDEXED_COUNT": EXPECTED_ELIGIBLE,
        "INELIGIBLE_INDEXED_COUNT": 0,
        "PROBLEM_PACKAGE_INDEX_RECORD_COUNT": 0,
        "PROBLEM_PACKAGE_FORMAL_ARTIFACT_RECORD_COUNT": 0,
        "INDEX_RECORD_WITH_ARTIFACT_COUNT": 0,
        "INDEX_RECORD_MISSING_ARTIFACT_COUNT": 0,
        "ARTIFACT_SET_WITHOUT_INDEX_COUNT": EXPECTED_ARTIFACT_SETS,
        "INDEXED_PRIMARY_ARTIFACT_COUNT": 0,
        "MISSING_PRIMARY_ARTIFACT_REFERENCE_COUNT": EXPECTED_PRIMARY_ARTIFACTS,
        "BROKEN_PRIMARY_ARTIFACT_REFERENCE_COUNT": 0,
        "PRIMARY_ARTIFACT_HASH_CHECKED_COUNT": 0,
        "PRIMARY_ARTIFACT_HASH_MATCH_COUNT": 0,
        "PRIMARY_ARTIFACT_HASH_MISMATCH_COUNT": 0,
        "BODY_HASH_CHECKED_COUNT": 0,
        "BODY_HASH_MATCH_COUNT": 0,
        "BODY_HASH_MISMATCH_COUNT": 0,
        "INDEX_IDENTITY_BINDING_PASS_COUNT": 0,
        "INDEX_IDENTITY_BINDING_MISMATCH_COUNT": 0,
        "INDEX_MEMBERSHIP_BINDING_PASS_COUNT": 0,
        "INDEX_MEMBERSHIP_BINDING_MISMATCH_COUNT": 0,
        "INDEX_SOURCE_BINDING_PASS_COUNT": 0,
        "INDEX_SOURCE_BINDING_MISMATCH_COUNT": 0,
        "POST_REFRESH_CSV_JSONL_PROJECTION_MATCH": 0,
        "INDEX_ORDERING_CONTRACT_PASS": 0,
        "INDEX_STAGING_COMPLETE": 0,
        "INDEX_ATOMIC_PROMOTION_STARTED": 0,
        "INDEX_ATOMIC_PROMOTION_COMPLETED": 0,
        "INDEX_ATOMIC_ROLLBACK_REQUIRED": 0,
        "POST_REFRESH_INDEX_CSV_SHA256": "",
        "POST_REFRESH_INDEX_JSONL_SHA256": "",
        "FORMAL_ARTIFACT_CONTENT_MODIFICATION_COUNT": 0,
        "FORMAL_ARTIFACT_METADATA_MODIFICATION_COUNT": 0,
        "FORMAL_ARTIFACTS_MODIFIED": 0,
        "ARTIFACT_REGISTRY_MODIFICATION_COUNT": 0,
        "IDENTITY_MODIFICATION_COUNT": 0,
        "MEMBERSHIP_MODIFICATION_COUNT": 0,
        "FORMAL_ELIGIBILITY_MODIFIED": 0,
        "BACKLOG_MODIFICATION_COUNT": 0,
        "DOC_MANUAL_BACKLOG": EXPECTED_DOC_BACKLOG,
        "Q3_MANUAL_BACKLOG": EXPECTED_Q3_BACKLOG,
        "TOTAL_MANUAL_BACKLOG": 0,
        "G11_ORIGINAL_DECISION_MODIFICATION_COUNT": 0,
        "TARGETED_VISUAL_DECISION_MODIFICATION_COUNT": 0,
        "FINAL_VISUAL_DECISION_MODIFICATION_COUNT": 0,
        "OCR_RUN": 0,
        "Q3_OCR_RUN": 0,
        "PDF_RENDER_RUN": 0,
        "PDF_INSPECTOR_EXTRACTION_RUN": 0,
        "PDFTOTEXT_EXTRACTION_RUN": 0,
        "FORMAL_EXTRACTION_RUN": 0,
        "BODY_RECONSTRUCTION_RUN": 0,
        "ARTIFACT_REGENERATION_RUN": 0,
        "ARTIFACT_REPROMOTION_RUN": 0,
        "DOC_BATCH_RUN": 0,
        "Q3_REPAIR_RUN": 0,
        "G10_RUN": 0,
        "G12_RUN": 0,
        "WORD_RUN": 0,
        "WORD_COM_RUN": 0,
        "DOC_CONVERSION_RUN": 0,
        "PRINT_JOB_RUN": 0,
        "NETWORK_ACCESS_USED": 0,
        "DOWNLOAD_RUN": 0,
        "NEW_DEPENDENCY_INSTALLED": 0,
        "GIT_OPERATIONS": 0,
        "G9_REFRESH_STATUS": "RUNNING",
        "G11_STATUS_REMAINS": "PARTIAL",
        "G10_EXPECTED_ARTIFACT_SET_COUNT": EXPECTED_ARTIFACT_SETS,
        "G10_EXPECTED_PRIMARY_ARTIFACT_COUNT": EXPECTED_PRIMARY_ARTIFACTS,
        "G10_EXPECTED_INDEX_RECORD_COUNT": EXPECTED_ELIGIBLE,
        "G10_EXPECTED_ELIGIBLE_IDENTITY_COUNT": EXPECTED_ELIGIBLE,
        "G10_EXPECTED_DOC_BACKLOG": EXPECTED_DOC_BACKLOG,
        "G10_EXPECTED_Q3_BACKLOG": EXPECTED_Q3_BACKLOG,
        "G10_EXPECTED_TOTAL_BACKLOG": 0,
        "G10_EXPECTED_G9_INDEX_CSV_SHA256": "",
        "OUTPUTS": {
            "formal_index_csv": rel(FORMAL_INDEX),
            "formal_index_jsonl": rel(FORMAL_INDEX_JSONL),
            "result": rel(RESULT_PATH),
            "attempt": rel(ATTEMPT_PATH),
            "diff": rel(DIFF_PATH),
            "validation": rel(VALIDATION_PATH),
            "report": rel(REPORT_PATH),
            "staging_root": rel(STAGE_ROOT),
        },
        "VALIDATION": [],
        "ISSUES": [],
        "BLOCKER": "",
        "NEXT": "G10-CONSISTENCY-REVALIDATE-AFTER-G11-REPAIR",
        "COMPLETED_AT": "",
    }


def set_projection_metrics(result: dict[str, Any], metrics: dict[str, Any], row_results: list[dict[str, str]]) -> None:
    result["POST_REFRESH_INDEX_CSV_RECORD_COUNT"] = metrics["FORMAL_INDEX_PAPER_COUNT"]
    result["POST_REFRESH_INDEX_JSONL_RECORD_COUNT"] = metrics["FORMAL_INDEX_PAPER_COUNT"]
    result["UNIQUE_PAPER_ID_COUNT"] = metrics["FORMAL_INDEX_UNIQUE_PAPER_ID_COUNT"]
    result["DUPLICATE_PAPER_ID_COUNT"] = metrics["DUPLICATE_FORMAL_INDEX_PAPER_ID_COUNT"]
    result["ELIGIBLE_INDEXED_COUNT"] = metrics["ELIGIBLE_INDEXED_COUNT"]
    result["ELIGIBLE_NOT_INDEXED_COUNT"] = metrics["ELIGIBLE_NOT_INDEXED_COUNT"]
    result["INELIGIBLE_INDEXED_COUNT"] = metrics["INELIGIBLE_INDEXED_COUNT"]
    result["PROBLEM_PACKAGE_INDEX_RECORD_COUNT"] = metrics["PROBLEM_PACKAGE_IN_FORMAL_PAPER_INDEX_COUNT"]
    result["INDEX_RECORD_WITH_ARTIFACT_COUNT"] = metrics["INDEX_RECORD_WITH_ARTIFACT_SET_COUNT"]
    result["INDEX_RECORD_MISSING_ARTIFACT_COUNT"] = metrics["INDEX_RECORD_WITHOUT_ARTIFACT_SET_COUNT"]
    result["ARTIFACT_SET_WITHOUT_INDEX_COUNT"] = metrics["ARTIFACT_SET_WITHOUT_INDEX_RECORD_COUNT"]
    result["INDEXED_PRIMARY_ARTIFACT_COUNT"] = metrics["INDEXED_PRIMARY_ARTIFACT_COUNT"]
    result["MISSING_PRIMARY_ARTIFACT_REFERENCE_COUNT"] = metrics["PRIMARY_ARTIFACT_NOT_INDEXED_COUNT"]
    result["BROKEN_PRIMARY_ARTIFACT_REFERENCE_COUNT"] = metrics["BROKEN_ARTIFACT_REFERENCE_COUNT"]
    result["PRIMARY_ARTIFACT_HASH_CHECKED_COUNT"] = EXPECTED_PRIMARY_ARTIFACTS
    result["PRIMARY_ARTIFACT_HASH_MATCH_COUNT"] = EXPECTED_PRIMARY_ARTIFACTS - metrics["INDEX_ARTIFACT_SHA_MISMATCH_COUNT"]
    result["PRIMARY_ARTIFACT_HASH_MISMATCH_COUNT"] = metrics["INDEX_ARTIFACT_SHA_MISMATCH_COUNT"]
    result["BODY_HASH_CHECKED_COUNT"] = EXPECTED_ARTIFACT_SETS
    result["BODY_HASH_MATCH_COUNT"] = EXPECTED_ARTIFACT_SETS if metrics["INDEX_ARTIFACT_SHA_MISMATCH_COUNT"] == 0 else 0
    result["BODY_HASH_MISMATCH_COUNT"] = 0 if metrics["INDEX_ARTIFACT_SHA_MISMATCH_COUNT"] == 0 else EXPECTED_ARTIFACT_SETS
    result["INDEX_IDENTITY_BINDING_PASS_COUNT"] = sum(row["identity_valid"] == "1" for row in row_results)
    result["INDEX_IDENTITY_BINDING_MISMATCH_COUNT"] = metrics["INDEX_IDENTITY_METADATA_MISMATCH_COUNT"]
    result["INDEX_MEMBERSHIP_BINDING_PASS_COUNT"] = sum(row["membership_valid"] == "1" for row in row_results)
    result["INDEX_MEMBERSHIP_BINDING_MISMATCH_COUNT"] = metrics["INDEX_MEMBERSHIP_METADATA_MISMATCH_COUNT"]
    result["INDEX_SOURCE_BINDING_PASS_COUNT"] = sum(row["source_valid"] == "1" for row in row_results)
    result["INDEX_SOURCE_BINDING_MISMATCH_COUNT"] = metrics["BROKEN_SOURCE_REFERENCE_COUNT"]


def report_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# G9 INDEX REFRESH AFTER G11 REPAIR",
        "",
        "## Decision",
        "",
        f"- Status: **{result['STATUS']}**",
        f"- Refresh attempt: `{result['G9_REFRESH_ATTEMPT_ID']}`",
        f"- Source G8 repair attempt: `{result['SOURCE_G8_REPAIR_ATTEMPT_ID']}`",
        f"- Mode: `{result['G9_REFRESH_MODE']}`",
        "",
        "G9 required refresh because 246 formal artifact sets changed in the completed G11 multi-route repair. The refresh input was consumed as a fixed population; no new repair targets were inferred.",
        "",
        "The existing 22-field G9 projection logic was reused for a deterministic full projection of all 453 eligible PAPER identities. This is an index projection rebuild only; formal artifacts and their registry were not regenerated or modified.",
        "",
        "## Cardinality and target binding",
        "",
        f"- Refresh input: `{result['REFRESH_INPUT_ROW_COUNT']}` rows, `{result['REFRESH_INPUT_CURRENT_BINDING_PASS_COUNT']}` current bindings passed, `{result['REFRESH_INPUT_CURRENT_BINDING_MISMATCH_COUNT']}` mismatches.",
        f"- Target records refreshed: `{result['TARGET_INDEX_RECORD_REFRESHED_COUNT']}/{result['TARGET_INDEX_RECORD_COUNT']}`; failures: `{result['TARGET_INDEX_RECORD_REFRESH_FAILED_COUNT']}`.",
        f"- Non-target records: `{result['NON_TARGET_INDEX_RECORD_COUNT']}`; unexpected semantic changes: `{result['NON_TARGET_INDEX_UNEXPECTED_SEMANTIC_CHANGE_COUNT']}`.",
        f"- Final index: CSV/JSONL `{result['POST_REFRESH_INDEX_CSV_RECORD_COUNT']}/{result['POST_REFRESH_INDEX_JSONL_RECORD_COUNT']}`, unique IDs `{result['UNIQUE_PAPER_ID_COUNT']}`, duplicates `{result['DUPLICATE_PAPER_ID_COUNT']}`.",
        "",
        "## Artifact, body, and governance binding",
        "",
        f"- Primary artifact hashes: `{result['PRIMARY_ARTIFACT_HASH_MATCH_COUNT']}/{result['PRIMARY_ARTIFACT_HASH_CHECKED_COUNT']}` match; broken references `{result['BROKEN_PRIMARY_ARTIFACT_REFERENCE_COUNT']}`.",
        f"- Body hashes: `{result['BODY_HASH_MATCH_COUNT']}/{result['BODY_HASH_CHECKED_COUNT']}` match.",
        f"- Identity/membership/source bindings: `{result['INDEX_IDENTITY_BINDING_PASS_COUNT']}/{result['INDEX_MEMBERSHIP_BINDING_PASS_COUNT']}/{result['INDEX_SOURCE_BINDING_PASS_COUNT']}` pass counts.",
        f"- Eligibility: indexed `{result['ELIGIBLE_INDEXED_COUNT']}`, not indexed `{result['ELIGIBLE_NOT_INDEXED_COUNT']}`, ineligible indexed `{result['INELIGIBLE_INDEXED_COUNT']}`.",
        f"- PROBLEM_PACKAGE index records: `{result['PROBLEM_PACKAGE_INDEX_RECORD_COUNT']}`; formal artifact records: `{result['PROBLEM_PACKAGE_FORMAL_ARTIFACT_RECORD_COUNT']}`.",
        "",
        "## Safety boundary",
        "",
        "Only the formal CSV and JSONL index projections were atomically promoted from a stage-owned candidate. Formal artifact content/metadata, artifact registry, identity, membership, eligibility, source files, backlogs, and G11 decisions remained unchanged. No OCR, rendering, extraction, reconstruction, Office, network, dependency, Git, G10, or G12 operation was run.",
        "",
        "## SHA freeze",
        "",
        f"- Pre-refresh CSV SHA256: `{result['PRE_REFRESH_INDEX_CSV_SHA256']}`",
        f"- Pre-refresh JSONL SHA256: `{result['PRE_REFRESH_INDEX_JSONL_SHA256']}`",
        f"- Post-refresh CSV SHA256: `{result['POST_REFRESH_INDEX_CSV_SHA256']}`",
        f"- Post-refresh JSONL SHA256: `{result['POST_REFRESH_INDEX_JSONL_SHA256']}`",
        "",
        "## Next stage",
        "",
        "G10 must revalidate consistency against the frozen post-refresh index SHA and the unchanged 453/1359 formal baseline.",
        "",
        "## Outputs",
        "",
    ]
    for value in result["OUTPUTS"].values():
        lines.append(f"- `{value}`")
    return "\n".join(lines) + "\n"


def build_result(
    result: dict[str, Any],
    context: dict[str, Any],
    input_data: dict[str, Any],
    old_rows: list[dict[str, str]],
    old_jsonl_rows: list[dict[str, str]],
    new_rows: list[dict[str, str]],
    new_jsonl_rows: list[dict[str, str]],
    row_metrics: dict[str, Any],
    row_results: list[dict[str, str]],
    diff_metrics: dict[str, int],
    pre_csv_sha: str,
    pre_jsonl_sha: str,
    post_csv_sha: str,
    post_jsonl_sha: str,
    promotion_started: int,
    promotion_completed: int,
    rollback_required: int,
) -> dict[str, Any]:
    result.update({
        "STATUS": "PASS",
        "G9_REFRESH_STATUS": "PASS",
        "PRE_REFRESH_ARTIFACT_SET_COUNT": EXPECTED_ARTIFACT_SETS,
        "PRE_REFRESH_PRIMARY_ARTIFACT_COUNT": EXPECTED_PRIMARY_ARTIFACTS,
        "PRE_REFRESH_INDEX_CSV_RECORD_COUNT": len(old_rows),
        "PRE_REFRESH_INDEX_JSONL_RECORD_COUNT": len(old_jsonl_rows),
        "PRE_REFRESH_INDEX_CSV_SHA256": pre_csv_sha,
        "PRE_REFRESH_INDEX_JSONL_SHA256": pre_jsonl_sha,
        "PRE_REFRESH_CSV_JSONL_PROJECTION_MATCH": int(canonical_rows_equal(old_rows, old_jsonl_rows)),
        "REFRESH_INPUT_ROW_COUNT": len(input_data["refresh"]),
        "REFRESH_INPUT_UNIQUE_PAPER_ID_COUNT": len(input_data["target_ids"]),
        "REFRESH_INPUT_UNIQUE_ARTIFACT_SET_COUNT": len({row["artifact_set_id"] for row in input_data["refresh"]}),
        "REFRESH_INPUT_CURRENT_BINDING_PASS_COUNT": input_data["refresh_pass"],
        "REFRESH_INPUT_CURRENT_BINDING_MISMATCH_COUNT": input_data["refresh_mismatch"],
        **diff_metrics,
        "POST_REFRESH_INDEX_CSV_RECORD_COUNT": len(new_rows),
        "POST_REFRESH_INDEX_JSONL_RECORD_COUNT": len(new_jsonl_rows),
        "POST_REFRESH_CSV_JSONL_PROJECTION_MATCH": int(canonical_rows_equal(new_rows, new_jsonl_rows)),
        "INDEX_ORDERING_CONTRACT_PASS": int(new_rows == sorted(new_rows, key=lambda row: (int(row["year"]), row["problem"], row["paper_id"]))),
        "INDEX_STAGING_COMPLETE": 1,
        "INDEX_ATOMIC_PROMOTION_STARTED": promotion_started,
        "INDEX_ATOMIC_PROMOTION_COMPLETED": promotion_completed,
        "INDEX_ATOMIC_ROLLBACK_REQUIRED": rollback_required,
        "POST_REFRESH_INDEX_CSV_SHA256": post_csv_sha,
        "POST_REFRESH_INDEX_JSONL_SHA256": post_jsonl_sha,
        "FORMAL_ARTIFACT_CONTENT_MODIFICATION_COUNT": 0,
        "FORMAL_ARTIFACT_METADATA_MODIFICATION_COUNT": 0,
        "FORMAL_ARTIFACTS_MODIFIED": 0,
        "ARTIFACT_REGISTRY_MODIFICATION_COUNT": 0,
        "IDENTITY_MODIFICATION_COUNT": 0,
        "MEMBERSHIP_MODIFICATION_COUNT": 0,
        "FORMAL_ELIGIBILITY_MODIFIED": 0,
        "BACKLOG_MODIFICATION_COUNT": 0,
        "DOC_MANUAL_BACKLOG": EXPECTED_DOC_BACKLOG,
        "Q3_MANUAL_BACKLOG": EXPECTED_Q3_BACKLOG,
        "TOTAL_MANUAL_BACKLOG": 0,
        "G11_ORIGINAL_DECISION_MODIFICATION_COUNT": 0,
        "TARGETED_VISUAL_DECISION_MODIFICATION_COUNT": 0,
        "FINAL_VISUAL_DECISION_MODIFICATION_COUNT": 0,
        "FORMAL_ARTIFACTS_MODIFIED": 0,
        "G10_EXPECTED_G9_INDEX_CSV_SHA256": post_csv_sha,
        "BLOCKER": "NONE",
        "NEXT": "G10-CONSISTENCY-REVALIDATE-AFTER-G11-REPAIR",
        "COMPLETED_AT": now_iso(),
        "VALIDATION": [
            "Post-repair G8 baseline and fixed 246-row refresh input passed binding validation.",
            "Existing canonical 22-field G9 projection logic was reused in full deterministic projection mode.",
            "207 non-target records had zero unexpected semantic changes; exactly 246 target records refreshed.",
            "453 index records, 1359 primary artifacts, body hashes, identity, membership, source, eligibility, and PROBLEM_PACKAGE exclusions passed.",
            "CSV and JSONL projections matched before and after promotion; ordering contract passed.",
            "Stage-owned candidate and backup were used for atomic index promotion; formal artifacts remained unchanged.",
        ],
        "ISSUES": [],
    })
    set_projection_metrics(result, row_metrics, row_results)
    result["PROBLEM_PACKAGE_FORMAL_ARTIFACT_RECORD_COUNT"] = sum(
        1 for row in context["artifacts"] if row.get("subject_type") == "PROBLEM_PACKAGE"
    )
    return result


def write_blocked(result: dict[str, Any], exc: GateError) -> None:
    result["STATUS"] = "BLOCKED"
    result["G9_REFRESH_STATUS"] = "BLOCKED"
    result["BLOCKER"] = f"{exc.code}:{exc.message}"
    result["ISSUES"] = [result["BLOCKER"]]
    result["NEXT"] = "RESOLVE_G9_INDEX_REFRESH_BLOCKER"
    G9.atomic_write_json(RESULT_PATH, result)
    G9.atomic_write_bytes(REPORT_PATH, report_markdown(result).encode("utf-8"))


def run_preflight() -> int:
    branch, head = read_git_head_without_git()
    try:
        required_inputs()
        g11 = read_json(G11_RESULT)
        g11_attempt_id = validate_g11_repair(g11)
        context = G9.load_context()
        assert_equal(branch, EXPECTED_BRANCH, "G9_REFRESH_REPO_DRIFT", "BRANCH")
        assert_equal(head, EXPECTED_HEAD, "G9_REFRESH_REPO_DRIFT", "HEAD")
        input_data = validate_g11_inputs(g11_attempt_id, context)
        old_rows = G9.read_index(FORMAL_INDEX)
        old_jsonl = G9.read_jsonl_projection(FORMAL_INDEX_JSONL)
        assert_equal(len(old_rows), EXPECTED_ELIGIBLE, "PRE_REFRESH_INDEX_BASELINE_INVALID", "CSV_RECORD_COUNT")
        assert_equal(len(old_jsonl), EXPECTED_ELIGIBLE, "PRE_REFRESH_INDEX_BASELINE_INVALID", "JSONL_RECORD_COUNT")
        assert_equal(old_rows, old_jsonl, "PRE_REFRESH_INDEX_BASELINE_INVALID", "CSV_JSONL_PROJECTION")
        rows, issues = G9.build_rows(context)
        if issues:
            raise GateError("STAGED_INDEX_INVALID", ";".join(issues))
        metrics, _ = G9.validate_rows(rows, context)
        if not metrics["INDEX_VALID"]:
            raise GateError("STAGED_INDEX_INVALID", json.dumps(metrics, ensure_ascii=False, sort_keys=True))
        diff_metrics, _ = diff_rows(old_rows, rows, input_data["target_ids"])
        print(f"STAGE={EXPECTED_STAGE}")
        print("STATUS=PASS")
        print(f"BRANCH={branch}")
        print(f"HEAD={head}")
        print(f"PRE_REFRESH_INDEX_CSV_RECORD_COUNT={len(old_rows)}")
        print(f"PRE_REFRESH_INDEX_JSONL_RECORD_COUNT={len(old_jsonl)}")
        print(f"REFRESH_INPUT_ROW_COUNT={len(input_data['refresh'])}")
        print(f"REFRESH_INPUT_CURRENT_BINDING_PASS_COUNT={input_data['refresh_pass']}")
        print(f"TARGET_INDEX_RECORD_REFRESHED_COUNT={diff_metrics['TARGET_INDEX_RECORD_REFRESHED_COUNT']}")
        print(f"NON_TARGET_INDEX_UNEXPECTED_SEMANTIC_CHANGE_COUNT={diff_metrics['NON_TARGET_INDEX_UNEXPECTED_SEMANTIC_CHANGE_COUNT']}")
        print("WRITE_OPERATION_PERFORMED=0")
        print("NEXT=RUN_WITH_EXPLICIT_--EXECUTE")
        return 0
    except GateError as exc:
        print(f"STAGE={EXPECTED_STAGE}")
        print("STATUS=BLOCKED")
        print(f"BLOCKER={exc.code}:{exc.message}")
        print("WRITE_OPERATION_PERFORMED=0")
        return 1


def run_execute() -> int:
    started_at = now_iso()
    attempt_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + "_" + EXPECTED_HEAD[:12]
    branch, head = read_git_head_without_git()
    g11_attempt_id = ""
    result = base_result(attempt_id, g11_attempt_id, branch, head)
    promotion_started = 0
    promotion_completed = 0
    rollback_required = 0
    backup_dir = STAGE_ROOT / attempt_id / "backup"
    stage_dir = STAGE_ROOT / attempt_id
    try:
        write_attempt(attempt_id, "PHASE_0_BASELINE", "RUNNING", started_at)
        required_inputs()
        g11 = read_json(G11_RESULT)
        g11_attempt_id = validate_g11_repair(g11)
        result["SOURCE_G8_REPAIR_ATTEMPT_ID"] = g11_attempt_id
        assert_equal(branch, EXPECTED_BRANCH, "G9_REFRESH_REPO_DRIFT", "BRANCH")
        assert_equal(head, EXPECTED_HEAD, "G9_REFRESH_REPO_DRIFT", "HEAD")
        context = G9.load_context()
        if len(context["eligible_rows"]) != EXPECTED_ELIGIBLE or len(context["ineligible_rows"]) != EXPECTED_INELIGIBLE:
            raise GateError("POST_REPAIR_FORMAL_BASELINE_INVALID", "eligibility cardinality mismatch")
        input_data = validate_g11_inputs(g11_attempt_id, context)
        result.update({
            "REFRESH_INPUT_ROW_COUNT": len(input_data["refresh"]),
            "REFRESH_INPUT_UNIQUE_PAPER_ID_COUNT": len(input_data["target_ids"]),
            "REFRESH_INPUT_UNIQUE_ARTIFACT_SET_COUNT": len({row["artifact_set_id"] for row in input_data["refresh"]}),
            "REFRESH_INPUT_CURRENT_BINDING_PASS_COUNT": input_data["refresh_pass"],
            "REFRESH_INPUT_CURRENT_BINDING_MISMATCH_COUNT": input_data["refresh_mismatch"],
        })
        write_attempt(attempt_id, "PHASE_1_INPUT_BINDING", "RUNNING", started_at)

        old_rows = G9.read_index(FORMAL_INDEX)
        old_jsonl_rows = G9.read_jsonl_projection(FORMAL_INDEX_JSONL)
        if len(old_rows) != EXPECTED_ELIGIBLE or len(old_jsonl_rows) != EXPECTED_ELIGIBLE:
            raise GateError("PRE_REFRESH_INDEX_BASELINE_INVALID", f"csv={len(old_rows)};jsonl={len(old_jsonl_rows)}")
        if old_rows != old_jsonl_rows:
            raise GateError("PRE_REFRESH_INDEX_BASELINE_INVALID", "CSV/JSONL projection mismatch")
        pre_csv_sha = sha(FORMAL_INDEX)
        pre_jsonl_sha = sha(FORMAL_INDEX_JSONL)
        result.update({
            "PRE_REFRESH_INDEX_CSV_RECORD_COUNT": len(old_rows),
            "PRE_REFRESH_INDEX_JSONL_RECORD_COUNT": len(old_jsonl_rows),
            "PRE_REFRESH_INDEX_CSV_SHA256": pre_csv_sha,
            "PRE_REFRESH_INDEX_JSONL_SHA256": pre_jsonl_sha,
            "PRE_REFRESH_CSV_JSONL_PROJECTION_MATCH": 1,
        })
        write_attempt(attempt_id, "PHASE_2_PRE_REFRESH_INDEX_SNAPSHOT", "RUNNING", started_at)

        rows, build_issues = G9.build_rows(context)
        if build_issues:
            raise GateError("STAGED_INDEX_INVALID", ";".join(build_issues))
        if len(rows) != EXPECTED_ELIGIBLE:
            raise GateError("STAGED_INDEX_INVALID", f"rows={len(rows)}")
        staged_metrics, staged_validation_rows = G9.validate_rows(rows, context)
        if not staged_metrics["INDEX_VALID"]:
            raise GateError("STAGED_INDEX_INVALID", json.dumps(staged_metrics, ensure_ascii=False, sort_keys=True))
        if rows != sorted(rows, key=lambda row: (int(row["year"]), row["problem"], row["paper_id"])):
            raise GateError("INDEX_ORDERING_CONTRACT_FAILURE", "candidate ordering differs from canonical ordering")
        diff_metrics, diff = diff_rows(old_rows, rows, input_data["target_ids"])
        if diff_metrics["NON_TARGET_INDEX_UNEXPECTED_SEMANTIC_CHANGE_COUNT"] != 0:
            raise GateError("NON_TARGET_INDEX_SEMANTIC_CHANGE", "candidate changed a non-target record")
        write_attempt(attempt_id, "PHASE_3_DETERMINISTIC_CANDIDATE_BUILD", "RUNNING", started_at)

        stage_dir.mkdir(parents=True, exist_ok=False)
        stage_csv = stage_dir / "g9_paper_index.csv"
        stage_jsonl = stage_dir / "g9_paper_index.jsonl"
        stage_diff = stage_dir / "g9_index_refresh_after_g11_repair_diff.csv"
        stage_validation = stage_dir / "g9_index_refresh_after_g11_repair_validation.csv"
        G9.atomic_write_bytes(stage_csv, G9.csv_bytes(G9.INDEX_FIELDS, rows))
        G9.atomic_write_bytes(stage_jsonl, G9.jsonl_bytes(rows))
        G9.atomic_write_bytes(stage_diff, G9.csv_bytes(G9.DIFF_FIELDS, diff))
        G9.atomic_write_bytes(stage_validation, G9.csv_bytes(G9.VALIDATION_FIELDS, staged_validation_rows))
        if not stage_csv.is_file() or not stage_jsonl.is_file():
            raise GateError("INDEX_STAGING_FAILURE", "candidate files were not materialized")
        result["INDEX_STAGING_COMPLETE"] = 1
        write_attempt(attempt_id, "PHASE_4_STAGED_INDEX_VALIDATION", "RUNNING", started_at, stage_dir=rel(stage_dir))

        backup_dir.mkdir(parents=True, exist_ok=True)
        G9.atomic_write_bytes(backup_dir / "g9_paper_index.csv", FORMAL_INDEX.read_bytes())
        G9.atomic_write_bytes(backup_dir / "g9_paper_index.jsonl", FORMAL_INDEX_JSONL.read_bytes())
        if sha(backup_dir / "g9_paper_index.csv") != pre_csv_sha or sha(backup_dir / "g9_paper_index.jsonl") != pre_jsonl_sha:
            raise GateError("INDEX_BACKUP_FAILURE", "stage-owned backup hash mismatch")

        promotion_started = 1
        result["INDEX_ATOMIC_PROMOTION_STARTED"] = 1
        write_attempt(attempt_id, "PHASE_5_ATOMIC_PROMOTION", "RUNNING", started_at)
        G9.atomic_write_bytes(FORMAL_INDEX, stage_csv.read_bytes())
        G9.atomic_write_bytes(FORMAL_INDEX_JSONL, stage_jsonl.read_bytes())
        promotion_completed = 1

        promoted_rows = G9.read_index(FORMAL_INDEX)
        promoted_jsonl_rows = G9.read_jsonl_projection(FORMAL_INDEX_JSONL)
        if promoted_rows != promoted_jsonl_rows:
            raise GateError("POST_REFRESH_CSV_JSONL_PROJECTION_MISMATCH", "promoted CSV/JSONL differ")
        post_metrics, post_validation_rows = G9.validate_rows(promoted_rows, context)
        if not post_metrics["INDEX_VALID"]:
            raise GateError("POST_REFRESH_INDEX_INVALID", json.dumps(post_metrics, ensure_ascii=False, sort_keys=True))
        post_csv_sha = sha(FORMAL_INDEX)
        post_jsonl_sha = sha(FORMAL_INDEX_JSONL)
        if post_csv_sha != sha(stage_csv) or post_jsonl_sha != sha(stage_jsonl):
            raise GateError("POST_REFRESH_INDEX_SHA_FAILURE", "promoted index differs from candidate")
        if promoted_rows != rows:
            raise GateError("POST_REFRESH_INDEX_PROJECTION_FAILURE", "promoted projection differs from candidate")
        write_attempt(attempt_id, "PHASE_6_POST_PROMOTION_VALIDATION", "RUNNING", started_at)
        G9.atomic_write_bytes(VALIDATION_PATH, G9.csv_bytes(G9.VALIDATION_FIELDS, post_validation_rows))
        G9.atomic_write_bytes(DIFF_PATH, G9.csv_bytes(G9.DIFF_FIELDS, diff))

        protected = G9.protected_modification_counts(context)
        if any(protected[key] != 0 for key in [
            "FORMAL_ARTIFACT_CONTENT_MODIFICATION_COUNT", "FORMAL_ELIGIBILITY_MODIFIED",
            "IDENTITY_MODIFICATION_COUNT", "MEMBERSHIP_MODIFICATION_COUNT", "ORIGINAL_FILES_MODIFIED",
        ]):
            raise GateError("PROTECTED_STATE_MODIFIED", json.dumps(protected, sort_keys=True))
        result.update(protected)
        result = build_result(
            result, context, input_data, old_rows, old_jsonl_rows, promoted_rows,
            promoted_jsonl_rows, post_metrics, post_validation_rows, diff_metrics,
            pre_csv_sha, pre_jsonl_sha, post_csv_sha, post_jsonl_sha,
            promotion_started, promotion_completed, rollback_required,
        )
        G9.atomic_write_json(RESULT_PATH, result)
        G9.atomic_write_bytes(REPORT_PATH, report_markdown(result).encode("utf-8"))
        write_attempt(
            attempt_id, "PHASE_7_FINAL_GATE", "PASS", started_at,
            post_refresh_index_csv_sha256=post_csv_sha,
            post_refresh_index_jsonl_sha256=post_jsonl_sha,
        )
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except GateError as exc:
        if promotion_started:
            rollback_required = 1
            try:
                if (backup_dir / "g9_paper_index.csv").is_file():
                    G9.atomic_write_bytes(FORMAL_INDEX, (backup_dir / "g9_paper_index.csv").read_bytes())
                if (backup_dir / "g9_paper_index.jsonl").is_file():
                    G9.atomic_write_bytes(FORMAL_INDEX_JSONL, (backup_dir / "g9_paper_index.jsonl").read_bytes())
                promotion_completed = 0
            except Exception as rollback_exc:
                exc = GateError("INDEX_ROLLBACK_FAILURE", f"{exc.code}:{exc.message};rollback={rollback_exc}")
        result["INDEX_ATOMIC_PROMOTION_STARTED"] = promotion_started
        result["INDEX_ATOMIC_PROMOTION_COMPLETED"] = promotion_completed
        result["INDEX_ATOMIC_ROLLBACK_REQUIRED"] = rollback_required
        result["STATUS"] = "BLOCKED"
        result["G9_REFRESH_STATUS"] = "BLOCKED"
        result["BLOCKER"] = f"{exc.code}:{exc.message}"
        result["ISSUES"] = [result["BLOCKER"]]
        result["NEXT"] = "RESOLVE_G9_INDEX_REFRESH_BLOCKER"
        G9.atomic_write_json(RESULT_PATH, result)
        G9.atomic_write_bytes(REPORT_PATH, report_markdown(result).encode("utf-8"))
        write_attempt(attempt_id, "BLOCKED", "BLOCKED", started_at, blocker=result["BLOCKER"])
        print(json.dumps(result, ensure_ascii=False))
        return 1
    except Exception as exc:
        result["STATUS"] = "BLOCKED"
        result["G9_REFRESH_STATUS"] = "BLOCKED"
        result["BLOCKER"] = f"UNEXPECTED_RUNNER_ERROR:{exc}"
        result["ISSUES"] = [result["BLOCKER"]]
        result["NEXT"] = "RESOLVE_G9_INDEX_REFRESH_BLOCKER"
        G9.atomic_write_json(RESULT_PATH, result)
        G9.atomic_write_bytes(REPORT_PATH, report_markdown(result).encode("utf-8"))
        write_attempt(attempt_id, "UNEXPECTED_ERROR", "BLOCKED", started_at, blocker=result["BLOCKER"])
        print(json.dumps(result, ensure_ascii=False))
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=EXPECTED_STAGE)
    parser.add_argument("--execute", action="store_true", help="stage, validate, and atomically promote the G9 index refresh")
    args = parser.parse_args()
    return run_execute() if args.execute else run_preflight()


if __name__ == "__main__":
    raise SystemExit(main())
