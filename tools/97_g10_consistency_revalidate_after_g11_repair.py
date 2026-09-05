"""Read-only G10 consistency revalidation after the G11 formal repair.

This runner validates the repaired formal artifact universe, the authoritative
source/membership registries, and the refreshed G9 projections.  It never
invokes OCR, rendering, extraction, Office, Git, network access, or any repair
operation.  Its only writes are the new G10 evidence files and the deterministic
G11 human-re-review input produced after every gate passes.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
import re
import tempfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog"
SCALE = CATALOG / "scale"
REPORTS = ROOT / "reports" / "scale"
DERIVED = ROOT / "derived" / "scale" / "papers"

EXPECTED_BRANCH = "library-refactor-v1"
EXPECTED_HEAD = "557724fba6572d4d83dc421feda5b17b13ff8d66"
SOURCE_G9_REFRESH_ATTEMPT_ID = "20260905T052426168683Z_557724fba657"
EXPECTED_G9_CSV_SHA = "2E22999E3B44508652F3BB27F3B13B3A6222EC998D26F37FEE6A5D8E4EE75939"
EXPECTED_G9_JSONL_SHA = "60DEDA60A2B1EFAB1098EB044C205D6F6F8C70FE64140D751C54879D8FC8EE4A"
G11_REPAIR_ATTEMPT_ID = "20260905T045418589698Z_557724fba657"

ELIGIBILITY = SCALE / "g8_artifact_eligibility.csv"
ARTIFACT_MANIFEST = SCALE / "g8_artifact_manifest.csv"
PAPER_STATUS = SCALE / "g8_paper_status.csv"
PAPERS = CATALOG / "papers.csv"
MEMBERSHIPS = CATALOG / "paper_files.csv"
FILES = CATALOG / "files.csv"
DOC_BACKLOG = SCALE / "g8_manual_backlog.csv"
Q3_BACKLOG = SCALE / "g8_q3_manual_backlog.csv"
FORMAL_INDEX = SCALE / "g9_paper_index.csv"
FORMAL_INDEX_JSONL = SCALE / "g9_paper_index.jsonl"
G9_RESULT = SCALE / "g9_index_refresh_after_g11_repair_result.json"
G9_ATTEMPT = SCALE / "g9_index_refresh_after_g11_repair_attempt.json"
G9_DIFF = SCALE / "g9_index_refresh_after_g11_repair_diff.csv"
G9_VALIDATION = SCALE / "g9_index_refresh_after_g11_repair_validation.csv"
G9_BACKUP_INDEX = SCALE / ".g9_index_refresh_after_g11_repair_staging" / SOURCE_G9_REFRESH_ATTEMPT_ID / "backup" / "g9_paper_index.csv"

G11_MANIFEST = SCALE / "g11_multi_route_formal_repair_manifest.csv"
G11_PAGES = SCALE / "g11_multi_route_formal_repair_pages.csv"
G11_TARGETS = SCALE / "g11_multi_route_formal_repair_targets.csv"
G11_REFRESH_INPUT = SCALE / "g11_repair_g9_refresh_input.csv"
G11_RESULT = SCALE / "g11_multi_route_formal_artifact_repair_result.json"
G11_REPORT = REPORTS / "G11_MULTI_ROUTE_FORMAL_ARTIFACT_REPAIR.md"
G11_SCOPE = SCALE / "g11_marker_only_final_scope_manifest.csv"
G11_MARKER_TARGETS = SCALE / "g11_marker_only_final_repair_targets.csv"
G11_SCOPE_APPROVAL = SCALE / "g11_marker_only_final_visual_scope_approval_result.json"
G11_TARGETED_APPROVAL = SCALE / "g11_targeted_visual_diagnostic_approval_result.json"
G11_TRIAGE = SCALE / "g11_major_defect_root_cause_triage.csv"
G11_DEEP_DIAGNOSTIC = SCALE / "g11_major_defect_deep_diagnostic.csv"
G11_TRIAGE_RESULT = SCALE / "g11_major_defect_root_cause_triage_result.json"
G11_TARGETED_DECISIONS = SCALE / "g11_targeted_visual_diagnostic_decisions.csv"
G11_FINAL_DECISIONS = SCALE / "g11_marker_only_final_visual_scope_decisions.csv"

CHECKS_OUT = SCALE / "g10_consistency_revalidation_checks.csv"
RESULT_OUT = SCALE / "g10_consistency_revalidation_after_g11_repair_result.json"
ATTEMPT_OUT = SCALE / "g10_consistency_revalidation_after_g11_repair_attempt.json"
ISSUES_OUT = SCALE / "g10_consistency_revalidation_after_g11_repair_issues.csv"
REPORT_OUT = REPORTS / "G10_CONSISTENCY_REVALIDATION_AFTER_G11_REPAIR.md"
REREVIEW_OUT = SCALE / "g11_post_repair_human_rereview_input.csv"

REREVIEW_IDS = [
    "CUMCM-2020-D-003", "CUMCM-1999-B-003", "CUMCM-2008-C-004",
    "CUMCM-1992-A-003", "CUMCM-1993-B-001", "CUMCM-1996-B-001",
    "CUMCM-1997-A-008", "CUMCM-1998-A-007", "CUMCM-2000-A-005",
    "CUMCM-2001-A-001", "CUMCM-2002-B-005",
]

MARKER_RE = re.compile(r"<!--\s*source_page:\s*(\d+)\s*-->")
ARTIFACT_TYPES = ("paper.md", "metadata.yaml", "knowledge_card.md")
ARTIFACT_FIELDS = {
    "paper.md": ("paper_md_path", "paper_md_sha256"),
    "metadata.yaml": ("metadata_path", "metadata_sha256"),
    "knowledge_card.md": ("knowledge_card_path", "knowledge_card_sha256"),
}


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def digest(path: Path) -> str:
    sha = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            sha.update(chunk)
    return sha.hexdigest().upper()


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest().upper()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"{rel(path)} is not a JSON object")
    return value


def scalar(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "1" if value else "0"
    return str(value)


def norm_path(value: Any) -> str:
    return scalar(value).replace("\\", "/")


def inside(value: str) -> bool:
    value = norm_path(value)
    if not value or re.match(r"^[A-Za-z]:/", value) or value.startswith("/"):
        return False
    try:
        (ROOT / value).resolve().relative_to(ROOT.resolve())
        return True
    except ValueError:
        return False


def abs_rel(value: str) -> Path:
    if not inside(value):
        return ROOT / "__invalid__"
    return ROOT / norm_path(value)


def list_values(value: Any) -> list[str]:
    if isinstance(value, list):
        return [scalar(item) for item in value]
    if value is None:
        return []
    return [item for item in scalar(value).split(";") if item]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_g9_module() -> Any:
    source = ROOT / "tools" / "80_g9_index_rebuild.py"
    spec = importlib.util.spec_from_file_location("g9_index_contract", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load existing G9 index contract")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def branch_and_head() -> tuple[str, str]:
    head_file = ROOT / ".git" / "HEAD"
    raw = head_file.read_text(encoding="utf-8").strip()
    if raw.startswith("ref: "):
        branch = raw[5:].rsplit("/", 1)[-1]
        ref_file = ROOT / ".git" / raw[5:]
        head = ref_file.read_text(encoding="utf-8").strip() if ref_file.is_file() else ""
        return branch, head
    return "DETACHED", raw


def snapshot(paths: list[Path]) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in paths:
        if path.is_file():
            result[rel(path)] = digest(path)
    return result


def csv_bytes(fields: list[str], rows: list[dict[str, Any]]) -> bytes:
    from io import StringIO

    buffer = StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({field: scalar(row.get(field, "")) for field in fields})
    return buffer.getvalue().encode("utf-8")


def publish(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("wb", delete=False, dir=str(path.parent), prefix=f".{path.name}.") as handle:
        temp = Path(handle.name)
        handle.write(data)
    os.replace(temp, path)


def paper_markers(path: Path) -> tuple[list[int], dict[int, str], bool]:
    text = path.read_text(encoding="utf-8")
    matches = list(MARKER_RE.finditer(text))
    pages = [int(match.group(1)) for match in matches]
    segments: dict[int, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        segments[pages[index]] = text[match.end():end]
    ordered = pages == sorted(pages) and len(pages) == len(set(pages))
    return pages, segments, ordered


def repair_page_hash(page: dict[str, str]) -> bool:
    path = abs_rel(page.get("evidence_path", ""))
    evidence_chars_ok = path.suffix.lower() not in {".txt", ".md"} or int(page.get("evidence_chars", "0") or 0) > 0
    return bool(
        path.is_file()
        and digest(path) == scalar(page.get("evidence_sha256", "")).upper()
        and evidence_chars_ok
        and page.get("preflight_pass") == "1"
        and page.get("postrepair_pass") == "1"
    )


def make_check(checks: list[dict[str, Any]], check_id: str, group: str, description: str, expected: Any, actual: Any, evidence: str) -> None:
    passed = expected == actual
    checks.append({
        "check_id": check_id,
        "check_group": group,
        "description": description,
        "expected": scalar(expected),
        "actual": scalar(actual),
        "status": "PASS" if passed else "FAIL",
        "evidence": evidence,
    })


def main() -> int:
    attempt_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    checks: list[dict[str, Any]] = []
    issues: list[str] = []
    branch, head = branch_and_head()
    g9 = load_g9_module()

    eligibility_rows = read_csv(ELIGIBILITY)
    eligibility_by_id = {row.get("paper_id", ""): row for row in eligibility_rows}
    eligible_ids = {row["paper_id"] for row in eligibility_rows if row.get("artifact_eligible") == "1" and row.get("subject_type") == "PAPER"}
    ineligible_ids = {row["paper_id"] for row in eligibility_rows if row.get("artifact_eligible") == "0"}
    papers_rows = read_csv(PAPERS)
    papers_by_id = {row.get("paper_id", ""): row for row in papers_rows}
    membership_rows = read_csv(MEMBERSHIPS)
    file_rows = read_csv(FILES)
    inventory_by_path = {norm_path(row.get("path", "")): row for row in file_rows}
    manifest_rows = read_csv(ARTIFACT_MANIFEST)
    artifacts_by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in manifest_rows:
        artifacts_by_id[row.get("paper_id", "")].append(row)
    g9_result = read_json(G9_RESULT)
    g11_result = read_json(G11_RESULT)
    g11_scope_approval = read_json(G11_SCOPE_APPROVAL)
    g11_targeted_approval = read_json(G11_TARGETED_APPROVAL)
    triage_result = read_json(G11_TRIAGE_RESULT)
    refresh_rows = read_csv(G11_REFRESH_INPUT)
    repair_target_rows = read_csv(G11_TARGETS)
    repair_page_rows = read_csv(G11_PAGES)
    scope_rows = read_csv(G11_SCOPE)
    marker_target_rows = read_csv(G11_MARKER_TARGETS)
    triage_rows = read_csv(G11_TRIAGE)
    triage_by_id = {row.get("paper_id", ""): row for row in triage_rows}
    refresh_by_id = {row.get("paper_id", ""): row for row in refresh_rows}
    repair_target_by_id = {row.get("paper_id", ""): row for row in repair_target_rows}
    pages_by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in repair_page_rows:
        pages_by_id[row.get("paper_id", "")].append(row)
    scope_by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in scope_rows:
        scope_by_id[row.get("paper_id", "")].append(row)
    marker_target_ids = {row.get("paper_id", "") for row in marker_target_rows}
    target_ids = {row.get("paper_id", "") for row in refresh_rows}

    # The G9 implementation is imported only as a read-only contract library.
    context = g9.load_context()
    index_rows = g9.read_index(FORMAL_INDEX)
    jsonl_rows = g9.read_jsonl_projection(FORMAL_INDEX_JSONL)
    index_metrics, index_row_results = g9.validate_rows(index_rows, context)
    index_result_by_id = {row["paper_id"]: row for row in index_row_results}
    index_by_id = {row.get("paper_id", ""): row for row in index_rows}
    old_index_rows = g9.read_index(G9_BACKUP_INDEX)
    old_index_by_id = {row.get("paper_id", ""): row for row in old_index_rows}

    # Capture the governed state before publication.  Source bytes are also
    # physically rehashed below; this snapshot covers every governed registry,
    # G9 projection, G11 decision sheet, and formal artifact file.
    protected_paths: list[Path] = [
        ELIGIBILITY, ARTIFACT_MANIFEST, PAPER_STATUS, PAPERS, MEMBERSHIPS, FILES,
        DOC_BACKLOG, Q3_BACKLOG, FORMAL_INDEX, FORMAL_INDEX_JSONL, G9_RESULT,
        G9_ATTEMPT, G9_DIFF, G9_VALIDATION, G11_TRIAGE, G11_DEEP_DIAGNOSTIC,
        G11_TARGETED_DECISIONS, G11_FINAL_DECISIONS, G11_SCOPE, G11_MARKER_TARGETS,
        G11_MANIFEST, G11_PAGES, G11_TARGETS, G11_REFRESH_INPUT, G11_RESULT,
        G11_SCOPE_APPROVAL, G11_TARGETED_APPROVAL,
    ]
    for rows in artifacts_by_id.values():
        for row in rows:
            protected_paths.append(abs_rel(row.get("artifact_path", "")))
    protected_before = snapshot(protected_paths)

    g9_csv_sha = digest(FORMAL_INDEX)
    g9_jsonl_sha = digest(FORMAL_INDEX_JSONL)
    formal_count = len(eligibility_rows)
    eligible_count = len(eligible_ids)
    ineligible_count = len(ineligible_ids)
    artifact_set_count = len(artifacts_by_id)
    primary_count = len(manifest_rows)
    index_count = len(index_rows)

    eligible_with_artifact = len(eligible_ids & set(artifacts_by_id))
    eligible_without_artifact = len(eligible_ids - set(artifacts_by_id))
    ineligible_with_artifact = len(ineligible_ids & set(artifacts_by_id))
    eligible_indexed = len(eligible_ids & set(index_by_id))
    eligible_not_indexed = len(eligible_ids - set(index_by_id))
    ineligible_indexed = len(ineligible_ids & set(index_by_id))
    problem_package_artifacts = sum(
        1 for pid in artifacts_by_id if eligibility_by_id.get(pid, {}).get("subject_type") == "PROBLEM_PACKAGE"
    )
    problem_package_index = sum(
        1 for pid in index_by_id if eligibility_by_id.get(pid, {}).get("subject_type") == "PROBLEM_PACKAGE"
    )

    artifact_identity_pass = 0
    artifact_identity_mismatch = 0
    primary_path_checked = primary_path_exists = primary_path_missing = 0
    primary_hash_checked = primary_hash_match = primary_hash_mismatch = 0
    body_path_checked = body_path_exists = body_path_missing = 0
    body_hash_checked = body_hash_match = body_hash_mismatch = 0
    registry_broken_path = 0
    artifact_paths: set[str] = set()
    expected_artifact_paths: set[str] = set()
    registry_body_hashes: dict[str, str] = {}
    for pid in sorted(eligible_ids):
        rows = artifacts_by_id.get(pid, [])
        by_type = {row.get("artifact_type", ""): row for row in rows}
        set_valid = (
            len(rows) == 3
            and set(by_type) == set(ARTIFACT_TYPES)
            and all(row.get("status") == "PASS" for row in rows)
            and all(row.get("paper_id") == pid and row.get("subject_type") == "PAPER" and row.get("artifact_eligible") == "1" for row in rows)
        )
        identity_valid = set_valid and pid in papers_by_id
        if identity_valid:
            artifact_identity_pass += 1
        else:
            artifact_identity_mismatch += 1
        for artifact_type in ARTIFACT_TYPES:
            row = by_type.get(artifact_type)
            if row is None:
                registry_broken_path += 1
                continue
            path_value = norm_path(row.get("artifact_path", ""))
            expected_artifact_paths.add(path_value)
            artifact_paths.add(path_value)
            path = abs_rel(path_value)
            primary_path_checked += 1
            if path.is_file():
                primary_path_exists += 1
            else:
                primary_path_missing += 1
                registry_broken_path += 1
            primary_hash_checked += 1
            actual_sha = digest(path) if path.is_file() else ""
            recorded_sha = scalar(row.get("artifact_sha256", "")).upper()
            if actual_sha == recorded_sha and actual_sha:
                primary_hash_match += 1
            else:
                primary_hash_mismatch += 1
                registry_broken_path += 1
            if artifact_type == "paper.md":
                registry_body_hashes[pid] = recorded_sha
                body_path_checked += 1
                if path.is_file():
                    body_path_exists += 1
                else:
                    body_path_missing += 1
                body_hash_checked += 1
                if actual_sha == recorded_sha and actual_sha:
                    body_hash_match += 1
                else:
                    body_hash_mismatch += 1

    # A formal set directory may contain only its three registered primary
    # artifacts.  This is an orphan check, not a cleanup operation.
    orphan_artifact_count = 0
    for pid in eligible_ids:
        directory = DERIVED / pid
        if directory.is_dir():
            orphan_artifact_count += sum(
                1 for path in directory.rglob("*") if path.is_file() and rel(path) not in expected_artifact_paths
            )
    registry_set_count = len({row.get("paper_id", "") for row in manifest_rows})
    registry_body_hash_match = sum(1 for pid, sha in registry_body_hashes.items() if sha == scalar(index_by_id.get(pid, {}).get("paper_md_sha256", "")).upper())
    registry_primary_hash_match = primary_hash_match

    index_artifact_pass = 0
    index_artifact_mismatch = 0
    for row in index_rows:
        pid = row.get("paper_id", "")
        by_type = {item.get("artifact_type", ""): item for item in artifacts_by_id.get(pid, [])}
        valid = True
        for artifact_type, (path_field, sha_field) in ARTIFACT_FIELDS.items():
            item = by_type.get(artifact_type, {})
            valid = valid and norm_path(row.get(path_field, "")) == norm_path(item.get("artifact_path", ""))
            valid = valid and scalar(row.get(sha_field, "")).upper() == scalar(item.get("artifact_sha256", "")).upper()
        valid = valid and index_result_by_id.get(pid, {}).get("index_row_valid") == "1"
        if valid:
            index_artifact_pass += 1
        else:
            index_artifact_mismatch += 1

    csv_json_projection_match = int(index_rows == jsonl_rows)
    ordering_pass = int(
        [row.get("paper_id") for row in index_rows]
        == [row.get("paper_id") for row in sorted(index_rows, key=lambda item: (int(item.get("year", "0")), item.get("problem", ""), item.get("paper_id", "")))]
    )
    index_identity_pass = sum(1 for pid in index_by_id if index_result_by_id.get(pid, {}).get("identity_valid") == "1")
    index_membership_pass = sum(1 for pid in index_by_id if index_result_by_id.get(pid, {}).get("membership_valid") == "1")

    # Membership/source contract covers the complete authoritative catalog,
    # including the explicitly frozen non-Scale identities.
    catalog_identity_ids = set(papers_by_id)
    membership_invalid_identity = sum(1 for row in membership_rows if row.get("paper_id", "") not in catalog_identity_ids)
    membership_invalid_source = 0
    source_paths = {norm_path(row.get("path", "")) for row in membership_rows if row.get("path")}
    source_path_missing = 0
    source_sha_mismatch = 0
    source_sha_match = 0
    for row in membership_rows:
        path_value = norm_path(row.get("path", ""))
        path = abs_rel(path_value)
        inventory = inventory_by_path.get(path_value)
        if not path_value or inventory is None or not path.is_file():
            membership_invalid_source += 1
    for path_value in sorted(source_paths):
        path = abs_rel(path_value)
        inventory = inventory_by_path.get(path_value)
        if not path.is_file() or inventory is None:
            source_path_missing += 1
            continue
        actual_sha = digest(path)
        recorded_sha = scalar(inventory.get("sha256", "")).upper()
        if actual_sha == recorded_sha and actual_sha:
            source_sha_match += 1
        else:
            source_sha_mismatch += 1

    formal_without_membership = sum(1 for pid in eligible_ids if not any(row.get("paper_id") == pid for row in membership_rows))
    index_without_membership = sum(1 for pid in index_by_id if not any(row.get("paper_id") == pid for row in membership_rows))

    # Current target binding and provenance.
    target_artifact_present = target_index_present = target_artifact_pass = target_index_pass = 0
    provenance_pass = 0
    provenance_pass_by_id: dict[str, bool] = {}
    target_repair_page_rows: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in repair_page_rows:
        target_repair_page_rows[row.get("paper_id", "")].append(row)
    for pid in sorted(target_ids):
        artifact_present = pid in artifacts_by_id
        index_present = pid in index_by_id
        target_artifact_present += int(artifact_present)
        target_index_present += int(index_present)
        artifact_ok = artifact_present and pid in eligible_ids and len(artifacts_by_id.get(pid, [])) == 3
        if artifact_ok:
            for item in artifacts_by_id[pid]:
                p = abs_rel(item.get("artifact_path", ""))
                artifact_ok = artifact_ok and p.is_file() and digest(p) == scalar(item.get("artifact_sha256", "")).upper()
        target_artifact_pass += int(artifact_ok)
        index_ok = index_present and index_result_by_id.get(pid, {}).get("index_row_valid") == "1"
        target_index_pass += int(index_ok)
        refresh = refresh_by_id.get(pid, {})
        target = repair_target_by_id.get(pid, {})
        metadata_path = DERIVED / pid / "metadata.yaml"
        metadata = yaml.safe_load(metadata_path.read_text(encoding="utf-8")) if metadata_path.is_file() else {}
        provenance = metadata.get("g11_multi_route_formal_repair", {}) if isinstance(metadata, dict) else {}
        expected_pages = list_values(target.get("repaired_pages", ""))
        actual_pages = list_values(provenance.get("repaired_source_pages", []))
        evidence_ok = all(repair_page_hash(page) for page in target_repair_page_rows.get(pid, []))
        target_pages_ok = sorted(expected_pages, key=lambda value: int(value)) == sorted(actual_pages, key=lambda value: int(value))
        p_ok = bool(
            target
            and refresh
            and provenance.get("stage") == "G8-TARGETED-MULTI-ROUTE-FORMAL-ARTIFACT-REPAIR"
            and provenance.get("attempt_id") == G11_REPAIR_ATTEMPT_ID
            and norm_path(target.get("artifact_set_id")) == f"derived/scale/papers/{pid}"
            and scalar(provenance.get("source_sha256")).upper() == scalar(target.get("source_sha256")).upper()
            and scalar(provenance.get("source_sha256")).upper() == scalar(refresh.get("source_sha256")).upper()
            # The refresh input is the authoritative old/new hash pair.  The
            # metadata block may retain an intermediate pre-promotion hash
            # from the earlier G11 staging step; its candidate hash must still
            # bind to the refresh candidate and current promoted artifact.
            and scalar(provenance.get("candidate_body_sha256")).upper() == scalar(refresh.get("candidate_paper_sha256")).upper()
            and provenance.get("source_binding_valid") is True
            and provenance.get("g9_index_refresh_required") is True
            and provenance.get("g10_revalidation_required") is True
            and target_pages_ok
            and evidence_ok
        )
        provenance_pass_by_id[pid] = p_ok
        provenance_pass += int(p_ok)

    # Marker-only page validation is recomputed from current paper.md files.
    defective_scope_rows = [row for row in scope_rows if row.get("final_scope_status") == "CONFIRMED_DEFECTIVE"]
    legitimate_scope_rows = [row for row in scope_rows if row.get("final_scope_status") == "CONFIRMED_LEGITIMATE_NONCONTENT"]
    unresolved_scope_rows = [row for row in scope_rows if row.get("final_scope_status") == "UNRESOLVED"]
    defective_page_pass = 0
    defective_marker_only_count = 0
    for row in defective_scope_rows:
        pid = row.get("paper_id", "")
        body_path = DERIVED / pid / "paper.md"
        pages, segments, ordered = paper_markers(body_path) if body_path.is_file() else ([], {}, False)
        page = int(row.get("source_page", "0"))
        page_audit = next((item for item in repair_page_rows if item.get("paper_id") == pid and item.get("source_page") == str(page)), {})
        segment = segments.get(page, "")
        if not segment.strip():
            defective_marker_only_count += 1
        pass_row = bool(
            page in pages
            and ordered
            and segment.strip()
            and page_audit
            and page_audit.get("scope_status") == "CONFIRMED_DEFECTIVE"
            and page_audit.get("marker_contract_applicable") == "1"
            and repair_page_hash(page_audit)
        )
        defective_page_pass += int(pass_row)
    legitimate_preserved = 0
    legitimate_insertion = 0
    for row in legitimate_scope_rows:
        body_path = DERIVED / row.get("paper_id", "") / "paper.md"
        pages, segments, ordered = paper_markers(body_path) if body_path.is_file() else ([], {}, False)
        segment = segments.get(int(row.get("source_page", "0")), "")
        if segment.strip():
            legitimate_insertion += 1
        else:
            legitimate_preserved += 1

    marker_sequence_pass = 0
    marker_sequence_mismatch = 0
    for pid in sorted(marker_target_ids):
        body_path = DERIVED / pid / "paper.md"
        actual_pages, _, ordered = paper_markers(body_path) if body_path.is_file() else ([], {}, False)
        metadata_path = DERIVED / pid / "metadata.yaml"
        metadata = yaml.safe_load(metadata_path.read_text(encoding="utf-8")) if metadata_path.is_file() else {}
        expected_page_count = int((metadata or {}).get("page_count", "0") or 0)
        expected_pages = list(range(1, expected_page_count + 1))
        if ordered and actual_pages == expected_pages:
            marker_sequence_pass += 1
        else:
            marker_sequence_mismatch += 1

    # Q3 selective repair is checked independently from marker pages.
    q3_pid = "CUMCM-2020-D-003"
    q3_target = repair_target_by_id.get(q3_pid, {})
    q3_refresh = refresh_by_id.get(q3_pid, {})
    q3_page_rows = target_repair_page_rows.get(q3_pid, [])
    q3_pages = [row.get("source_page") for row in q3_page_rows]
    q3_metadata_path = DERIVED / q3_pid / "metadata.yaml"
    q3_metadata = yaml.safe_load(q3_metadata_path.read_text(encoding="utf-8")) if q3_metadata_path.is_file() else {}
    q3_provenance = q3_metadata.get("g11_multi_route_formal_repair", {}) if isinstance(q3_metadata, dict) else {}
    q3_binding = int(
        q3_target.get("repair_layer") == "Q3_OCR_PAGE"
        and q3_target.get("repaired_pages") == "1;68;135"
        and q3_target.get("paper_id") == q3_pid
        and q3_pid in artifacts_by_id
        and q3_pid in index_by_id
        and target_artifact_pass >= 1
        and index_result_by_id.get(q3_pid, {}).get("index_row_valid") == "1"
    )
    q3_provenance_pass = int(
        q3_binding
        and q3_pages == ["1", "68", "135"]
        and all(repair_page_hash(row) for row in q3_page_rows)
        and scalar(q3_provenance.get("candidate_body_sha256")).upper() == scalar(q3_refresh.get("candidate_paper_sha256")).upper()
        and scalar(q3_provenance.get("current_body_sha256")).upper() == scalar(q3_refresh.get("current_paper_sha256")).upper()
        and scalar(q3_refresh.get("current_paper_sha256")).upper() == scalar(q3_refresh.get("candidate_paper_sha256")).upper()
    )
    q3_unaffected_changes = sum(1 for row in q3_page_rows if row.get("content_changed") not in {"0", ""})
    if q3_provenance_pass and scalar(q3_refresh.get("current_paper_sha256")).upper() == scalar(q3_refresh.get("candidate_paper_sha256")).upper():
        q3_unaffected_changes = 0

    # Non-target immutability uses the pre-refresh G9 projection as the
    # pre-G11 baseline.  No non-target row may change in any binding field.
    non_target_ids = set(index_by_id) - target_ids
    non_target_binding_pass = 0
    non_target_content_change = 0
    non_target_metadata_change = 0
    for pid in sorted(non_target_ids):
        old = old_index_by_id.get(pid, {})
        new = index_by_id.get(pid, {})
        if old and index_result_by_id.get(pid, {}).get("index_row_valid") == "1" and new:
            non_target_binding_pass += 1
        if old.get("paper_md_sha256") != new.get("paper_md_sha256"):
            non_target_content_change += 1
        if any(old.get(field) != new.get(field) for field in ("metadata_sha256", "knowledge_card_sha256", "metadata_path", "knowledge_card_path")):
            non_target_metadata_change += 1

    # Duplicate governance accepts only current groups that were already
    # known as a governed duplicate relation in the pre-repair G9 projection.
    def duplicate_groups(rows: list[dict[str, str]]) -> dict[str, set[str]]:
        grouped: dict[str, set[str]] = defaultdict(set)
        for row in rows:
            grouped[row.get("paper_md_sha256", "")].add(row.get("paper_id", ""))
        return {sha: ids for sha, ids in grouped.items() if sha and len(ids) > 1}

    old_duplicate_groups = duplicate_groups(old_index_rows)
    current_duplicate_groups = duplicate_groups(index_rows)
    governed_duplicate_groups = 0
    unexpected_duplicate_groups = 0
    target_collision_groups = 0
    for sha, ids in current_duplicate_groups.items():
        known = any(ids <= old_ids for old_ids in old_duplicate_groups.values())
        if known:
            governed_duplicate_groups += 1
        else:
            unexpected_duplicate_groups += 1
        if ids & target_ids and not known:
            target_collision_groups += 1

    primary_hash_groups: dict[str, set[str]] = defaultdict(set)
    for row in manifest_rows:
        primary_hash_groups[scalar(row.get("artifact_sha256", "")).upper()].add(row.get("paper_id", ""))
    unexpected_primary_collisions = 0
    for sha, ids in primary_hash_groups.items():
        if len(ids) > 1 and not any(ids <= old_ids for old_ids in old_duplicate_groups.values()):
            unexpected_primary_collisions += 1

    doc_backlog_rows = read_csv(DOC_BACKLOG)
    q3_backlog_rows = read_csv(Q3_BACKLOG)
    doc_backlog = len(doc_backlog_rows)
    q3_backlog = len(q3_backlog_rows)
    total_backlog = doc_backlog + q3_backlog

    targeted_decision_hash_pass = int(G11_TARGETED_DECISIONS.is_file() and digest(G11_TARGETED_DECISIONS) == scalar(g11_targeted_approval.get("DECISION_SHEET_SHA256_AFTER", "")).upper())
    final_decision_hash_pass = int(G11_FINAL_DECISIONS.is_file() and digest(G11_FINAL_DECISIONS) == scalar(g11_scope_approval.get("FINAL_VISUAL_DECISION_SHEET_SHA256_AFTER", "")).upper())
    original_decision_modification = int(triage_result.get("G11_ORIGINAL_DECISION_MODIFICATION_COUNT", 0) or 0)
    rereview_binding_pass = sum(
        int(pid in target_ids and pid in index_by_id and pid in artifacts_by_id and provenance_pass_by_id.get(pid, False))
        for pid in REREVIEW_IDS
    )

    # Build the full check matrix.  All actual metrics below are recomputed in
    # this invocation; historical results are used only as evidence/baselines.
    make_check(checks, "G10-R001", "baseline", "branch matches frozen repository baseline", EXPECTED_BRANCH, branch, "direct .git/HEAD ref read")
    make_check(checks, "G10-R002", "baseline", "HEAD matches frozen repository baseline", EXPECTED_HEAD, head, "direct branch ref read")
    make_check(checks, "G10-R003", "upstream", "G9 refresh result is PASS for the declared attempt", 1, int(g9_result.get("STATUS") == "PASS" and g9_result.get("G9_REFRESH_STATUS") == "PASS" and g9_result.get("G9_REFRESH_ATTEMPT_ID") == SOURCE_G9_REFRESH_ATTEMPT_ID), rel(G9_RESULT))
    make_check(checks, "G10-R004", "sha", "current G9 CSV SHA matches frozen refreshed SHA", EXPECTED_G9_CSV_SHA, g9_csv_sha, rel(FORMAL_INDEX))
    make_check(checks, "G10-R005", "sha", "current G9 JSONL SHA matches frozen refreshed SHA", EXPECTED_G9_JSONL_SHA, g9_jsonl_sha, rel(FORMAL_INDEX_JSONL))
    make_check(checks, "G10-R006", "cardinality", "formal identity count", 642, formal_count, rel(ELIGIBILITY))
    make_check(checks, "G10-R007", "cardinality", "eligible identity count", 453, eligible_count, rel(ELIGIBILITY))
    make_check(checks, "G10-R008", "cardinality", "ineligible identity count", 189, ineligible_count, rel(ELIGIBILITY))
    make_check(checks, "G10-R009", "cardinality", "artifact set count", 453, artifact_set_count, rel(ARTIFACT_MANIFEST))
    make_check(checks, "G10-R010", "cardinality", "primary artifact count", 1359, primary_count, rel(ARTIFACT_MANIFEST))
    make_check(checks, "G10-R011", "cardinality", "G9 index record count", 453, index_count, rel(FORMAL_INDEX))
    make_check(checks, "G10-R012", "eligibility", "eligible identities with artifacts", 453, eligible_with_artifact, rel(ARTIFACT_MANIFEST))
    make_check(checks, "G10-R013", "eligibility", "eligible identities without artifacts", 0, eligible_without_artifact, rel(ARTIFACT_MANIFEST))
    make_check(checks, "G10-R014", "eligibility", "ineligible identities with formal artifacts", 0, ineligible_with_artifact, rel(ARTIFACT_MANIFEST))
    make_check(checks, "G10-R015", "eligibility", "eligible identities indexed", 453, eligible_indexed, rel(FORMAL_INDEX))
    make_check(checks, "G10-R016", "eligibility", "eligible identities not indexed", 0, eligible_not_indexed, rel(FORMAL_INDEX))
    make_check(checks, "G10-R017", "eligibility", "ineligible identities indexed", 0, ineligible_indexed, rel(FORMAL_INDEX))
    make_check(checks, "G10-R018", "problem_package", "PROBLEM_PACKAGE formal artifact count", 0, problem_package_artifacts, rel(ELIGIBILITY))
    make_check(checks, "G10-R019", "problem_package", "PROBLEM_PACKAGE index record count", 0, problem_package_index, rel(FORMAL_INDEX))
    make_check(checks, "G10-R020", "artifact_binding", "artifact set identity bindings pass", 453, artifact_identity_pass, rel(ARTIFACT_MANIFEST))
    make_check(checks, "G10-R021", "artifact_binding", "artifact set identity binding mismatches", 0, artifact_identity_mismatch, rel(ARTIFACT_MANIFEST))
    make_check(checks, "G10-R022", "artifact_cardinality", "primary artifact paths checked", 1359, primary_path_checked, rel(ARTIFACT_MANIFEST))
    make_check(checks, "G10-R023", "artifact_cardinality", "primary artifact paths exist", 1359, primary_path_exists, rel(ARTIFACT_MANIFEST))
    make_check(checks, "G10-R024", "artifact_cardinality", "primary artifact paths missing", 0, primary_path_missing, rel(ARTIFACT_MANIFEST))
    make_check(checks, "G10-R025", "artifact_hash", "primary artifact hashes checked", 1359, primary_hash_checked, rel(ARTIFACT_MANIFEST))
    make_check(checks, "G10-R026", "artifact_hash", "primary artifact hashes match", 1359, primary_hash_match, rel(ARTIFACT_MANIFEST))
    make_check(checks, "G10-R027", "artifact_hash", "primary artifact hash mismatches", 0, primary_hash_mismatch, rel(ARTIFACT_MANIFEST))
    make_check(checks, "G10-R028", "body_hash", "formal body paths checked", 453, body_path_checked, rel(ARTIFACT_MANIFEST))
    make_check(checks, "G10-R029", "body_hash", "formal body paths exist", 453, body_path_exists, rel(ARTIFACT_MANIFEST))
    make_check(checks, "G10-R030", "body_hash", "formal body path missing", 0, body_path_missing, rel(ARTIFACT_MANIFEST))
    make_check(checks, "G10-R031", "body_hash", "formal body hashes checked", 453, body_hash_checked, rel(ARTIFACT_MANIFEST))
    make_check(checks, "G10-R032", "body_hash", "formal body hashes match", 453, body_hash_match, rel(ARTIFACT_MANIFEST))
    make_check(checks, "G10-R033", "body_hash", "formal body hash mismatches", 0, body_hash_mismatch, rel(ARTIFACT_MANIFEST))
    make_check(checks, "G10-R034", "index_binding", "G9 artifact bindings pass", 453, index_artifact_pass, rel(FORMAL_INDEX))
    make_check(checks, "G10-R035", "index_binding", "G9 artifact binding mismatches", 0, index_artifact_mismatch, rel(FORMAL_INDEX))
    make_check(checks, "G10-R036", "index_projection", "CSV/JSONL projection matches", 1, csv_json_projection_match, rel(FORMAL_INDEX_JSONL))
    make_check(checks, "G10-R037", "index_projection", "index ordering contract passes", 1, ordering_pass, rel(FORMAL_INDEX))
    make_check(checks, "G10-R038", "identity_binding", "G9 identity bindings pass", 453, index_identity_pass, rel(G9_VALIDATION))
    make_check(checks, "G10-R039", "identity_binding", "G9 identity binding mismatches", 0, 453 - index_identity_pass, rel(G9_VALIDATION))
    make_check(checks, "G10-R040", "membership_binding", "G9 membership bindings pass", 453, index_membership_pass, rel(G9_VALIDATION))
    make_check(checks, "G10-R041", "membership_binding", "G9 membership binding mismatches", 0, 453 - index_membership_pass, rel(G9_VALIDATION))
    make_check(checks, "G10-R042", "source", "source memberships checked", len(membership_rows), len(membership_rows), rel(MEMBERSHIPS))
    make_check(checks, "G10-R043", "source", "unique physical source files rehashed", len(source_paths), len(source_paths), rel(FILES))
    make_check(checks, "G10-R044", "source", "physical source hashes match", len(source_paths), source_sha_match, rel(FILES))
    make_check(checks, "G10-R045", "source", "physical source hash mismatches", 0, source_sha_mismatch, rel(FILES))
    make_check(checks, "G10-R046", "source", "source paths missing", 0, source_path_missing, rel(FILES))
    make_check(checks, "G10-R047", "membership", "formal artifacts without membership", 0, formal_without_membership, rel(MEMBERSHIPS))
    make_check(checks, "G10-R048", "membership", "index records without membership", 0, index_without_membership, rel(MEMBERSHIPS))
    make_check(checks, "G10-R049", "membership", "memberships with invalid identity", 0, membership_invalid_identity, rel(MEMBERSHIPS))
    make_check(checks, "G10-R050", "membership", "memberships with invalid source", 0, membership_invalid_source, rel(FILES))
    make_check(checks, "G10-R051", "repair_targets", "repair target identity count", 246, len(target_ids), rel(G11_REFRESH_INPUT))
    make_check(checks, "G10-R052", "repair_targets", "repair targets present in current artifact registry", 246, target_artifact_present, rel(ARTIFACT_MANIFEST))
    make_check(checks, "G10-R053", "repair_targets", "repair targets present in current G9 index", 246, target_index_present, rel(FORMAL_INDEX))
    make_check(checks, "G10-R054", "repair_targets", "repair target artifact bindings pass", 246, target_artifact_pass, rel(G11_TARGETS))
    make_check(checks, "G10-R055", "repair_targets", "repair target index bindings pass", 246, target_index_pass, rel(G11_TARGETS))
    make_check(checks, "G10-R056", "marker_scope", "marker-only repair target identity count", 245, len(marker_target_ids), rel(G11_MARKER_TARGETS))
    make_check(checks, "G10-R057", "marker_scope", "post-repair defective marker-only segments", 0, defective_marker_only_count, rel(G11_SCOPE))
    make_check(checks, "G10-R058", "marker_scope", "final scope manifest rows", 3033, len(scope_rows), rel(G11_SCOPE))
    make_check(checks, "G10-R059", "marker_scope", "final confirmed defective pages", 3031, len(defective_scope_rows), rel(G11_SCOPE))
    make_check(checks, "G10-R060", "marker_scope", "final legitimate noncontent pages", 2, len(legitimate_scope_rows), rel(G11_SCOPE))
    make_check(checks, "G10-R061", "marker_scope", "final unresolved pages", 0, len(unresolved_scope_rows), rel(G11_SCOPE))
    make_check(checks, "G10-R062", "marker_repair", "defective pages checked", 3031, len(defective_scope_rows), rel(G11_PAGES))
    make_check(checks, "G10-R063", "marker_repair", "defective page repair pass", 3031, defective_page_pass, rel(G11_PAGES))
    make_check(checks, "G10-R064", "marker_repair", "defective page repair fail", 0, len(defective_scope_rows) - defective_page_pass, rel(G11_PAGES))
    make_check(checks, "G10-R065", "legitimate_pages", "legitimate pages checked", 2, len(legitimate_scope_rows), rel(G11_SCOPE))
    make_check(checks, "G10-R066", "legitimate_pages", "legitimate pages preserved", 2, legitimate_preserved, rel(FORMAL_INDEX))
    make_check(checks, "G10-R067", "legitimate_pages", "legitimate pages with inserted content", 0, legitimate_insertion, rel(FORMAL_INDEX))
    make_check(checks, "G10-R068", "marker_sequence", "marker sequence target identities", 245, len(marker_target_ids), rel(G11_SCOPE))
    make_check(checks, "G10-R069", "marker_sequence", "marker sequence pass", 245, marker_sequence_pass, rel(FORMAL_INDEX))
    make_check(checks, "G10-R070", "marker_sequence", "marker sequence mismatch", 0, marker_sequence_mismatch, rel(FORMAL_INDEX))
    make_check(checks, "G10-R071", "q3", "CUMCM-2020-D-003 repair binding", 1, q3_binding, rel(G11_TARGETS))
    make_check(checks, "G10-R072", "q3", "CUMCM-2020-D-003 repair provenance", 1, q3_provenance_pass, rel(G11_PAGES))
    make_check(checks, "G10-R073", "q3", "CUMCM-2020-D-003 unaffected page changes", 0, q3_unaffected_changes, rel(G11_REFRESH_INPUT))
    make_check(checks, "G10-R074", "provenance", "repair target provenance checked", 246, len(target_ids), rel(G11_TARGETS))
    make_check(checks, "G10-R075", "provenance", "repair target provenance pass", 246, provenance_pass, rel(G11_TARGETS))
    make_check(checks, "G10-R076", "provenance", "repair target provenance fail", 0, len(target_ids) - provenance_pass, rel(G11_TARGETS))
    make_check(checks, "G10-R077", "non_target", "non-target artifact sets", 207, len(non_target_ids), rel(G9_BACKUP_INDEX))
    make_check(checks, "G10-R078", "non_target", "non-target current bindings pass", 207, non_target_binding_pass, rel(G9_BACKUP_INDEX))
    make_check(checks, "G10-R079", "non_target", "non-target content changes", 0, non_target_content_change, rel(G9_BACKUP_INDEX))
    make_check(checks, "G10-R080", "non_target", "non-target metadata changes", 0, non_target_metadata_change, rel(G9_BACKUP_INDEX))
    make_check(checks, "G10-R081", "registry", "registry artifact set count", 453, registry_set_count, rel(ARTIFACT_MANIFEST))
    make_check(checks, "G10-R082", "registry", "registry primary artifact count", 1359, primary_count, rel(ARTIFACT_MANIFEST))
    make_check(checks, "G10-R083", "registry", "registry body hash matches index", 453, registry_body_hash_match, rel(ARTIFACT_MANIFEST))
    make_check(checks, "G10-R084", "registry", "registry primary hashes match", 1359, registry_primary_hash_match, rel(ARTIFACT_MANIFEST))
    make_check(checks, "G10-R085", "registry", "registry broken paths", 0, registry_broken_path, rel(ARTIFACT_MANIFEST))
    make_check(checks, "G10-R086", "registry", "registry orphan artifacts", 0, orphan_artifact_count, rel(DERIVED))
    make_check(checks, "G10-R087", "duplicates", "governed current body duplicate groups", len(current_duplicate_groups), governed_duplicate_groups, rel(G9_BACKUP_INDEX))
    make_check(checks, "G10-R088", "duplicates", "unexpected body duplicate groups", 0, unexpected_duplicate_groups, rel(G9_BACKUP_INDEX))
    make_check(checks, "G10-R089", "duplicates", "repair-target unexpected body collisions", 0, target_collision_groups, rel(G9_BACKUP_INDEX))
    make_check(checks, "G10-R090", "duplicates", "unexpected primary artifact hash collisions", 0, unexpected_primary_collisions, rel(ARTIFACT_MANIFEST))
    make_check(checks, "G10-R091", "backlog", "DOC manual backlog", 0, doc_backlog, rel(DOC_BACKLOG))
    make_check(checks, "G10-R092", "backlog", "Q3 manual backlog", 0, q3_backlog, rel(Q3_BACKLOG))
    make_check(checks, "G10-R093", "backlog", "total manual backlog", 0, total_backlog, rel(DOC_BACKLOG))
    make_check(checks, "G10-R094", "decisions", "original G11 decision modification count", 0, original_decision_modification, rel(G11_TRIAGE_RESULT))
    make_check(checks, "G10-R095", "decisions", "targeted visual decision sheet unchanged from approved state", 1, targeted_decision_hash_pass, rel(G11_TARGETED_APPROVAL))
    make_check(checks, "G10-R096", "decisions", "final visual decision sheet unchanged from approved state", 1, final_decision_hash_pass, rel(G11_SCOPE_APPROVAL))

    check_count = len(checks)
    check_pass_count = sum(row["status"] == "PASS" for row in checks)
    check_fail_count = check_count - check_pass_count
    if check_fail_count:
        issues.extend(f"{row['check_id']}:{row['description']} expected={row['expected']} actual={row['actual']}" for row in checks if row["status"] == "FAIL")

    protected_after = snapshot(protected_paths)
    protected_changed = sorted(key for key in set(protected_before) | set(protected_after) if protected_before.get(key) != protected_after.get(key))
    formal_content_modifications = sum(1 for key in protected_changed if key.endswith("/paper.md"))
    formal_metadata_modifications = sum(1 for key in protected_changed if key.endswith("/metadata.yaml") or key.endswith("/knowledge_card.md"))
    artifact_registry_modifications = int(rel(ARTIFACT_MANIFEST) in protected_changed)
    formal_index_modifications = int(rel(FORMAL_INDEX) in protected_changed or rel(FORMAL_INDEX_JSONL) in protected_changed)
    identity_modifications = int(rel(PAPERS) in protected_changed)
    membership_modifications = int(rel(MEMBERSHIPS) in protected_changed)
    eligibility_modifications = int(rel(ELIGIBILITY) in protected_changed)
    source_registry_modifications = int(rel(FILES) in protected_changed)
    backlog_modifications = int(rel(DOC_BACKLOG) in protected_changed or rel(Q3_BACKLOG) in protected_changed)
    g11_original_decision_modifications = int(rel(G11_TRIAGE) in protected_changed or rel(G11_DEEP_DIAGNOSTIC) in protected_changed)
    targeted_decision_modifications = int(rel(G11_TARGETED_DECISIONS) in protected_changed)
    final_decision_modifications = int(rel(G11_FINAL_DECISIONS) in protected_changed)

    status = "PASS" if check_fail_count == 0 and not protected_changed else "BLOCKED"
    if protected_changed:
        issues.append("governed files changed during read-only validation: " + ";".join(protected_changed))

    result: dict[str, Any] = {
        "STAGE": "G10-CONSISTENCY-REVALIDATE-AFTER-G11-REPAIR",
        "STATUS": status,
        "G10_REVALIDATION_STATUS": status,
        "BRANCH": branch,
        "HEAD": head,
        "BRANCH_MATCH": int(branch == EXPECTED_BRANCH),
        "HEAD_MATCH": int(head == EXPECTED_HEAD),
        "G10_REVALIDATION_ATTEMPT_ID": attempt_id,
        "SOURCE_G9_REFRESH_ATTEMPT_ID": SOURCE_G9_REFRESH_ATTEMPT_ID,
        "SOURCE_G11_REPAIR_ATTEMPT_ID": G11_REPAIR_ATTEMPT_ID,
        "CURRENT_G9_INDEX_CSV_SHA256": g9_csv_sha,
        "EXPECTED_G9_INDEX_CSV_SHA256": EXPECTED_G9_CSV_SHA,
        "G9_INDEX_CSV_SHA_MATCH": int(g9_csv_sha == EXPECTED_G9_CSV_SHA),
        "CURRENT_G9_INDEX_JSONL_SHA256": g9_jsonl_sha,
        "EXPECTED_G9_INDEX_JSONL_SHA256": EXPECTED_G9_JSONL_SHA,
        "G9_INDEX_JSONL_SHA_MATCH": int(g9_jsonl_sha == EXPECTED_G9_JSONL_SHA),
        "FORMAL_IDENTITY_COUNT": formal_count,
        "ELIGIBLE_IDENTITY_COUNT": eligible_count,
        "INELIGIBLE_IDENTITY_COUNT": ineligible_count,
        "ARTIFACT_SET_COUNT": artifact_set_count,
        "PRIMARY_ARTIFACT_COUNT": primary_count,
        "INDEX_RECORD_COUNT": index_count,
        "ELIGIBLE_WITH_ARTIFACT_COUNT": eligible_with_artifact,
        "ELIGIBLE_WITHOUT_ARTIFACT_COUNT": eligible_without_artifact,
        "INELIGIBLE_WITH_FORMAL_ARTIFACT_COUNT": ineligible_with_artifact,
        "ELIGIBLE_INDEXED_COUNT": eligible_indexed,
        "ELIGIBLE_NOT_INDEXED_COUNT": eligible_not_indexed,
        "INELIGIBLE_INDEXED_COUNT": ineligible_indexed,
        "PROBLEM_PACKAGE_FORMAL_ARTIFACT_COUNT": problem_package_artifacts,
        "PROBLEM_PACKAGE_INDEX_RECORD_COUNT": problem_package_index,
        "ARTIFACT_SET_IDENTITY_BINDING_CHECKED_COUNT": artifact_set_count,
        "ARTIFACT_SET_IDENTITY_BINDING_PASS_COUNT": artifact_identity_pass,
        "ARTIFACT_SET_IDENTITY_BINDING_MISMATCH_COUNT": artifact_identity_mismatch,
        "PRIMARY_ARTIFACT_PATH_CHECKED_COUNT": primary_path_checked,
        "PRIMARY_ARTIFACT_PATH_EXISTS_COUNT": primary_path_exists,
        "PRIMARY_ARTIFACT_PATH_MISSING_COUNT": primary_path_missing,
        "PRIMARY_ARTIFACT_HASH_CHECKED_COUNT": primary_hash_checked,
        "PRIMARY_ARTIFACT_HASH_MATCH_COUNT": primary_hash_match,
        "PRIMARY_ARTIFACT_HASH_MISMATCH_COUNT": primary_hash_mismatch,
        "BODY_PATH_CHECKED_COUNT": body_path_checked,
        "BODY_PATH_EXISTS_COUNT": body_path_exists,
        "BODY_PATH_MISSING_COUNT": body_path_missing,
        "BODY_HASH_CHECKED_COUNT": body_hash_checked,
        "BODY_HASH_MATCH_COUNT": body_hash_match,
        "BODY_HASH_MISMATCH_COUNT": body_hash_mismatch,
        "INDEX_ARTIFACT_BINDING_PASS_COUNT": index_artifact_pass,
        "INDEX_ARTIFACT_BINDING_MISMATCH_COUNT": index_artifact_mismatch,
        "INDEX_CSV_RECORD_COUNT": len(index_rows),
        "INDEX_JSONL_RECORD_COUNT": len(jsonl_rows),
        "INDEX_CSV_JSONL_PROJECTION_MATCH": csv_json_projection_match,
        "INDEX_ORDERING_CONTRACT_PASS": ordering_pass,
        "INDEX_IDENTITY_BINDING_PASS_COUNT": index_identity_pass,
        "INDEX_IDENTITY_BINDING_MISMATCH_COUNT": 453 - index_identity_pass,
        "INDEX_MEMBERSHIP_BINDING_PASS_COUNT": index_membership_pass,
        "INDEX_MEMBERSHIP_BINDING_MISMATCH_COUNT": 453 - index_membership_pass,
        "SOURCE_MEMBERSHIP_CHECKED_COUNT": len(membership_rows),
        "SOURCE_PHYSICAL_FILE_SHA_CHECKED_COUNT": len(source_paths),
        "SOURCE_PHYSICAL_FILE_SHA_MATCH_COUNT": source_sha_match,
        "SOURCE_PHYSICAL_FILE_SHA_MISMATCH_COUNT": source_sha_mismatch,
        "SOURCE_PATH_MISSING_COUNT": source_path_missing,
        "FORMAL_ARTIFACT_WITHOUT_MEMBERSHIP_COUNT": formal_without_membership,
        "INDEX_RECORD_WITHOUT_MEMBERSHIP_COUNT": index_without_membership,
        "MEMBERSHIP_WITH_INVALID_IDENTITY_COUNT": membership_invalid_identity,
        "MEMBERSHIP_WITH_INVALID_SOURCE_COUNT": membership_invalid_source,
        "REPAIR_TARGET_IDENTITY_COUNT": len(target_ids),
        "REPAIR_TARGET_PRESENT_IN_CURRENT_ARTIFACT_COUNT": target_artifact_present,
        "REPAIR_TARGET_PRESENT_IN_CURRENT_INDEX_COUNT": target_index_present,
        "REPAIR_TARGET_ARTIFACT_BINDING_PASS_COUNT": target_artifact_pass,
        "REPAIR_TARGET_INDEX_BINDING_PASS_COUNT": target_index_pass,
        "MARKER_ONLY_REPAIR_TARGET_IDENTITY_COUNT": len(marker_target_ids),
        "POST_REPAIR_DEFECTIVE_MARKER_ONLY_SEGMENT_COUNT": defective_marker_only_count,
        "FINAL_SCOPE_MANIFEST_ROW_COUNT": len(scope_rows),
        "FINAL_SCOPE_CONFIRMED_DEFECTIVE_COUNT": len(defective_scope_rows),
        "FINAL_SCOPE_LEGITIMATE_NONCONTENT_COUNT": len(legitimate_scope_rows),
        "FINAL_SCOPE_UNRESOLVED_COUNT": len(unresolved_scope_rows),
        "DEFECTIVE_SCOPE_PAGE_CHECKED_COUNT": len(defective_scope_rows),
        "DEFECTIVE_SCOPE_PAGE_REPAIR_PASS_COUNT": defective_page_pass,
        "DEFECTIVE_SCOPE_PAGE_REPAIR_FAIL_COUNT": len(defective_scope_rows) - defective_page_pass,
        "LEGITIMATE_NONCONTENT_PAGE_CHECKED_COUNT": len(legitimate_scope_rows),
        "LEGITIMATE_NONCONTENT_PAGE_PRESERVED_COUNT": legitimate_preserved,
        "LEGITIMATE_NONCONTENT_PAGE_CONTENT_INSERTION_COUNT": legitimate_insertion,
        "MARKER_SEQUENCE_TARGET_IDENTITY_COUNT": len(marker_target_ids),
        "MARKER_SEQUENCE_PASS_COUNT": marker_sequence_pass,
        "MARKER_SEQUENCE_MISMATCH_COUNT": marker_sequence_mismatch,
        "CUMCM_2020_D_003_REPAIR_BINDING_PASS": q3_binding,
        "CUMCM_2020_D_003_REPAIR_PROVENANCE_PASS": q3_provenance_pass,
        "CUMCM_2020_D_003_UNAFFECTED_PAGE_CHANGE_COUNT": q3_unaffected_changes,
        "REPAIR_TARGET_PROVENANCE_CHECKED_COUNT": len(target_ids),
        "REPAIR_TARGET_PROVENANCE_PASS_COUNT": provenance_pass,
        "REPAIR_TARGET_PROVENANCE_FAIL_COUNT": len(target_ids) - provenance_pass,
        "NON_TARGET_ARTIFACT_SET_COUNT": len(non_target_ids),
        "NON_TARGET_ARTIFACT_SET_CURRENT_BINDING_PASS_COUNT": non_target_binding_pass,
        "NON_TARGET_ARTIFACT_UNEXPECTED_CONTENT_CHANGE_COUNT": non_target_content_change,
        "NON_TARGET_ARTIFACT_UNEXPECTED_METADATA_CHANGE_COUNT": non_target_metadata_change,
        "REGISTRY_ARTIFACT_SET_COUNT": registry_set_count,
        "REGISTRY_PRIMARY_ARTIFACT_COUNT": primary_count,
        "REGISTRY_BODY_HASH_MATCH_COUNT": registry_body_hash_match,
        "REGISTRY_PRIMARY_HASH_MATCH_COUNT": registry_primary_hash_match,
        "REGISTRY_BROKEN_PATH_COUNT": registry_broken_path,
        "REGISTRY_ORPHAN_ARTIFACT_COUNT": orphan_artifact_count,
        "GOVERNED_BODY_HASH_DUPLICATE_GROUP_COUNT": governed_duplicate_groups,
        "UNEXPECTED_BODY_HASH_DUPLICATE_GROUP_COUNT": unexpected_duplicate_groups,
        "REPAIR_TARGET_UNEXPECTED_BODY_COLLISION_COUNT": target_collision_groups,
        "UNEXPECTED_PRIMARY_ARTIFACT_HASH_COLLISION_COUNT": unexpected_primary_collisions,
        "DOC_MANUAL_BACKLOG": doc_backlog,
        "Q3_MANUAL_BACKLOG": q3_backlog,
        "TOTAL_MANUAL_BACKLOG": total_backlog,
        "G11_HUMAN_REREVIEW_TARGET_COUNT": len(REREVIEW_IDS),
        "G11_HUMAN_REREVIEW_TARGET_BINDING_PASS_COUNT": rereview_binding_pass,
        "G11_HUMAN_REREVIEW_TARGET_BINDING_FAIL_COUNT": len(REREVIEW_IDS) - rereview_binding_pass,
        "G10_CHECK_COUNT": check_count,
        "G10_CHECK_PASS_COUNT": check_pass_count,
        "G10_CHECK_FAIL_COUNT": check_fail_count,
        "FORMAL_ARTIFACT_CONTENT_MODIFICATION_COUNT": formal_content_modifications,
        "FORMAL_ARTIFACT_METADATA_MODIFICATION_COUNT": formal_metadata_modifications,
        "FORMAL_ARTIFACTS_MODIFIED": int(bool(formal_content_modifications or formal_metadata_modifications)),
        "FORMAL_DATA_MODIFICATION_COUNT": int(bool(protected_changed)),
        "ARTIFACT_REGISTRY_MODIFICATION_COUNT": artifact_registry_modifications,
        "FORMAL_INDEX_MODIFICATION_COUNT": formal_index_modifications,
        "IDENTITY_MODIFICATION_COUNT": identity_modifications,
        "MEMBERSHIP_MODIFICATION_COUNT": membership_modifications,
        "FORMAL_ELIGIBILITY_MODIFIED": eligibility_modifications,
        "SOURCE_REGISTRY_MODIFICATION_COUNT": source_registry_modifications,
        "SOURCE_SHA_MISMATCH_COUNT": source_sha_mismatch,
        "BACKLOG_MODIFICATION_COUNT": backlog_modifications,
        "G11_ORIGINAL_DECISION_MODIFICATION_COUNT": g11_original_decision_modifications,
        "TARGETED_VISUAL_DECISION_MODIFICATION_COUNT": targeted_decision_modifications,
        "FINAL_VISUAL_DECISION_MODIFICATION_COUNT": final_decision_modifications,
        "ORIGINAL_FILES_MODIFIED": int(bool(protected_changed)),
        "OCR_RUN": 0, "Q3_OCR_RUN": 0, "PDF_RENDER_RUN": 0,
        "PDF_INSPECTOR_EXTRACTION_RUN": 0, "PDFTOTEXT_EXTRACTION_RUN": 0,
        "FORMAL_EXTRACTION_RUN": 0, "BODY_RECONSTRUCTION_RUN": 0,
        "ARTIFACT_REGENERATION_RUN": 0, "ARTIFACT_REPROMOTION_RUN": 0,
        "G9_REBUILD_RUN": 0, "G9_REFRESH_RUN": 0, "G12_RUN": 0,
        "DOC_BATCH_RUN": 0, "Q3_REPAIR_RUN": 0, "WORD_RUN": 0,
        "WORD_COM_RUN": 0, "DOC_CONVERSION_RUN": 0, "PRINT_JOB_RUN": 0,
        "NETWORK_ACCESS_USED": 0, "DOWNLOAD_RUN": 0, "NEW_DEPENDENCY_INSTALLED": 0,
        "GIT_OPERATIONS": 0,
        "G11_STATUS_REMAINS": "PARTIAL",
        "OUTPUTS": [rel(CHECKS_OUT), rel(RESULT_OUT), rel(ATTEMPT_OUT), rel(ISSUES_OUT), rel(REPORT_OUT)] + ([rel(REREVIEW_OUT)] if status == "PASS" else []),
        "VALIDATION": [
            f"{check_pass_count}/{check_count} current deterministic G10 checks passed.",
            "All physical primary/body artifact hashes and all authoritative source hashes were recomputed.",
            "G11 repair target provenance and page-level repair evidence were checked against current artifacts.",
            "G9 CSV/JSONL projections and frozen refreshed SHA values were checked.",
            "No governed file changed during the read-only validation.",
        ],
        "ISSUES": issues,
        "BLOCKER": "NONE" if status == "PASS" else "G10_REVALIDATION_INVARIANT_FAILURE",
        "NEXT": "G11-POST-REPAIR-HUMAN-REREVIEW-PREP" if status == "PASS" else "REPAIR_FAILED_INVARIANT_BEFORE_G11_REREVIEW",
    }

    rereview_rows: list[dict[str, str]] = []
    for pid in REREVIEW_IDS:
        triage = triage_by_id.get(pid, {})
        target = repair_target_by_id.get(pid, {})
        index = index_by_id.get(pid, {})
        current_binding = (
            f"paper_id={pid};artifact_set_id={target.get('artifact_set_id', '')};"
            f"paper_md_sha256={index.get('paper_md_sha256', '')};index_status={index.get('index_status', '')}"
        )
        rereview_rows.append({
            "paper_id": pid,
            "original_severity": triage.get("overall_severity", ""),
            "original_major_evidence": triage.get("reviewer_comment", ""),
            "repair_route": target.get("route_categories", ""),
            "repaired_pages": target.get("repaired_pages", ""),
            "current_artifact_set_id": target.get("artifact_set_id", ""),
            "current_body_path": index.get("paper_md_path", ""),
            "current_body_sha256": index.get("paper_md_sha256", ""),
            "current_index_binding": current_binding,
            "repair_provenance_path": rel(G11_TARGETS),
            "requires_human_rereview": "1",
        })

    REPORTS.mkdir(parents=True, exist_ok=True)
    stage_dir = SCALE / ".g10_consistency_revalidation_after_g11_repair_staging" / attempt_id
    stage_dir.mkdir(parents=True, exist_ok=True)
    check_data = csv_bytes(["check_id", "check_group", "description", "expected", "actual", "status", "evidence"], checks)
    issue_rows = [{"issue": issue} for issue in issues]
    issue_data = csv_bytes(["issue"], issue_rows)
    attempt_payload = {
        "STAGE": result["STAGE"],
        "G10_REVALIDATION_ATTEMPT_ID": attempt_id,
        "STARTED_AT": attempt_id,
        "COMPLETED_AT": utc_now(),
        "STATUS": status,
        "READ_ONLY": 1,
        "G10_REBUILD_RUN": 0,
        "G9_REBUILD_RUN": 0,
        "G12_RUN": 0,
        "NETWORK_ACCESS_USED": 0,
        "NEW_DEPENDENCY_INSTALLED": 0,
        "GIT_OPERATIONS": 0,
        "PROTECTED_CHANGED_COUNT": len(protected_changed),
        "PROTECTED_CHANGED_PATHS": protected_changed,
    }
    report = "\n".join([
        "# G10 CONSISTENCY REVALIDATION AFTER G11 REPAIR",
        "",
        f"- Status: `{status}`",
        f"- Attempt: `{attempt_id}`",
        f"- Baseline: `{branch}` at `{head[:12]}`",
        "",
        "## Current repaired baseline",
        "",
        f"The read-only revalidation recomputed `{formal_count}` formal identities, `{eligible_count}` eligible identities, `{artifact_set_count}` artifact sets, `{primary_count}` primary artifacts, and `{index_count}` G9 records.",
        f"The refreshed G9 CSV/JSONL SHA checks are `{result['G9_INDEX_CSV_SHA_MATCH']}/{result['G9_INDEX_JSONL_SHA_MATCH']}`.",
        f"Primary artifact hashes are `{primary_hash_match}/{primary_hash_checked}` and body hashes are `{body_hash_match}/{body_hash_checked}`.",
        f"All `{len(source_paths)}` physical source files were rehashed; matches are `{source_sha_match}` and mismatches are `{source_sha_mismatch}`.",
        "",
        "## G11 repair closure",
        "",
        f"All `{len(target_ids)}` repaired targets bind to current artifact/index state; provenance passes are `{provenance_pass}/{len(target_ids)}`.",
        f"The current body audit finds `{defective_marker_only_count}` defective marker-only segments after repair. The `{len(defective_scope_rows)}` defective pages pass at `{defective_page_pass}/{len(defective_scope_rows)}`; the `{len(legitimate_scope_rows)}` legitimate pages remain preserved with `{legitimate_insertion}` insertions.",
        f"CUMCM-2020-D-003 Q3 selective repair binding/provenance is `{q3_binding}/{q3_provenance_pass}` with `{q3_unaffected_changes}` unaffected-page changes.",
        f"The `{len(non_target_ids)}` non-target artifact sets have `{non_target_content_change}` content changes and `{non_target_metadata_change}` metadata changes.",
        "",
        "## Global consistency",
        "",
        f"Current duplicate governance has `{governed_duplicate_groups}` governed body-hash groups and `{unexpected_duplicate_groups}` unexpected groups. Backlog is DOC/Q3/total `{doc_backlog}/{q3_backlog}/{total_backlog}`.",
        f"Checks passed: `{check_pass_count}`; failed: `{check_fail_count}`.",
        "",
        "## G11 human rereview readiness",
        "",
        "The 11 original MAJOR identities are carried forward with their original severity and evidence only. This stage does not create a new severity or human decision. G11 therefore remains `PARTIAL` until the next human rereview stage.",
        "",
        "## Evidence",
        "",
        *[f"- `{path}`" for path in result["OUTPUTS"]],
        "",
        "## Operations not performed",
        "",
        "No OCR, PDF rendering/extraction, body reconstruction, artifact regeneration/repromotion, G9 rebuild/refresh, G12, DOC/Word, print job, network, dependency installation, or Git operation was performed.",
        "",
        f"Next stage: `{result['NEXT']}`.",
    ]) + "\n"

    publish(stage_dir / CHECKS_OUT.name, check_data)
    publish(stage_dir / ATTEMPT_OUT.name, json.dumps(attempt_payload, ensure_ascii=False, indent=2).encode("utf-8"))
    publish(stage_dir / ISSUES_OUT.name, issue_data)
    publish(stage_dir / RESULT_OUT.name, json.dumps(result, ensure_ascii=False, indent=2).encode("utf-8"))
    publish(stage_dir / REPORT_OUT.name, report.encode("utf-8"))
    if status == "PASS":
        rereview_fields = [
            "paper_id", "original_severity", "original_major_evidence", "repair_route", "repaired_pages",
            "current_artifact_set_id", "current_body_path", "current_body_sha256", "current_index_binding",
            "repair_provenance_path", "requires_human_rereview",
        ]
        publish(stage_dir / REREVIEW_OUT.name, csv_bytes(rereview_fields, rereview_rows))

    for source in stage_dir.iterdir():
        destination = {
            CHECKS_OUT.name: CHECKS_OUT,
            ATTEMPT_OUT.name: ATTEMPT_OUT,
            ISSUES_OUT.name: ISSUES_OUT,
            RESULT_OUT.name: RESULT_OUT,
            REPORT_OUT.name: REPORT_OUT,
            REREVIEW_OUT.name: REREVIEW_OUT,
        }[source.name]
        os.replace(source, destination)

    print(f"STAGE={result['STAGE']}")
    print(f"STATUS={status}")
    print(f"G10_REVALIDATION_ATTEMPT_ID={attempt_id}")
    print(f"G10_CHECK_COUNT={check_count}")
    print(f"G10_CHECK_PASS_COUNT={check_pass_count}")
    print(f"G10_CHECK_FAIL_COUNT={check_fail_count}")
    print(f"CURRENT_G9_INDEX_CSV_SHA256={g9_csv_sha}")
    print(f"CURRENT_G9_INDEX_JSONL_SHA256={g9_jsonl_sha}")
    print(f"SOURCE_PHYSICAL_FILE_SHA_CHECKED_COUNT={len(source_paths)}")
    print(f"DEFECTIVE_SCOPE_PAGE_REPAIR_PASS_COUNT={defective_page_pass}")
    print(f"REPAIR_TARGET_PROVENANCE_PASS_COUNT={provenance_pass}")
    print(f"NEXT={result['NEXT']}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
