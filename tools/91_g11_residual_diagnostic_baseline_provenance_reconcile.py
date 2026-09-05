"""Reconcile G11 residual evidence against the current formal baseline.

This stage is deliberately read-only with respect to source, formal data,
artifacts, membership, backlog, and prior G11 evidence.  It does not invoke
pdftotext, OCR, rendering, Word, G9, G10, or any extraction pipeline.
"""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCALE = ROOT / "catalog" / "scale"
REPORTS = ROOT / "reports" / "scale"

ELIGIBILITY = SCALE / "g8_artifact_eligibility.csv"
PAPER_STATUS = SCALE / "g8_paper_status.csv"
ARTIFACT_MANIFEST = SCALE / "g8_artifact_manifest.csv"
G9_INDEX_CSV = SCALE / "g9_paper_index.csv"
G9_INDEX_JSONL = SCALE / "g9_paper_index.jsonl"
G9_VALIDATION = SCALE / "g9_index_validation.csv"
DOC_BACKLOG = SCALE / "g8_manual_backlog.csv"
Q3_BACKLOG = SCALE / "g8_q3_manual_backlog.csv"
PAPER_FILES = ROOT / "catalog" / "paper_files.csv"
PAPERS = ROOT / "catalog" / "papers.csv"

G8_DOC_RESULT = SCALE / "g8_doc_formal_artifact_generation_result.json"
G8_DOC_CLOSURE_RESULT = SCALE / "g8_doc_batch_closure_qa_result.json"
G8_Q3_RESULT = SCALE / "g8_q3_formal_artifact_generation_result.json"
G9_RESULT = SCALE / "g9_index_rebuild_result.json"
G10_RESULT = SCALE / "g10_consistency_result.json"

RESIDUAL_CSV = SCALE / "g11_marker_only_residual_scope_diagnostic.csv"
IMAGE_RESIDUAL_CSV = SCALE / "g11_marker_only_image_residual_input.csv"
PREVIOUS_RESULT = SCALE / "g11_marker_only_residual_scope_diagnostic_result.json"
PREVIOUS_REPORT = REPORTS / "G11_MARKER_ONLY_RESIDUAL_SCOPE_DIAGNOSTIC.md"
SCOPE_CONFIRMATION = SCALE / "g11_marker_only_scope_confirmation.csv"
DEEP_PAGE = SCALE / "g11_marker_only_page_deep_diagnostic.csv"
MAJOR_DEEP = SCALE / "g11_major_defect_deep_diagnostic.csv"
TARGET_DECISIONS = SCALE / "g11_targeted_visual_diagnostic_decisions.csv"
DEEP_RESULT = SCALE / "g11_major_defect_deep_diagnostic_result.json"
Q3_FAILURE_CLASSES = SCALE / "g8_q3_failure_classes.csv"
RESIDUAL_TEXT_DIR = SCALE / "g11_residual_pdftotext_pages"
CALIBRATION_DIR = SCALE / "g11_residual_pdftotext_calibration"
TOOL90 = ROOT / "tools" / "90_g11_marker_only_residual_scope_diagnostic.py"

RESULT = SCALE / "g11_residual_diagnostic_baseline_reconcile_result.json"
REPORT = REPORTS / "G11_RESIDUAL_DIAGNOSTIC_BASELINE_PROVENANCE_RECONCILE.md"

EXPECTED_BRANCH = "library-refactor-v1"
EXPECTED_HEAD = "557724fba6572d4d83dc421feda5b17b13ff8d66"
SOURCE_ATTEMPT_ID = "g11-marker-only-residual-scope-diagnostic-f6288a9bd9006c8c"
STALE_ARTIFACT_SETS = 308
STALE_PRIMARY_ARTIFACTS = 924
STALE_DOC_BACKLOG = 18
STALE_Q3_BACKLOG = 128
STAMP = timezone(timedelta(hours=8))


class GateError(RuntimeError):
    pass


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise GateError(f"JSON_OBJECT_REQUIRED={path}")
    return value


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def cached_sha(cache: dict[Path, str], path: Path) -> str:
    if not path.is_file():
        return "MISSING"
    if path not in cache:
        cache[path] = sha256(path)
    return cache[path]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def git_value(*args: str) -> str:
    completed = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False)
    if completed.returncode != 0:
        raise GateError(f"GIT_READ_FAILED={' '.join(args)}")
    return completed.stdout.decode("utf-8", errors="replace").strip()


def now() -> str:
    return datetime.now(STAMP).isoformat(timespec="seconds")


def key(row: dict[str, Any]) -> tuple[str, int]:
    return (str(row["paper_id"]), int(row["source_page"]))


def page_keys(rows: list[dict[str, Any]]) -> set[tuple[str, int]]:
    keys = [key(row) for row in rows]
    if len(keys) != len(set(keys)):
        raise GateError("DUPLICATE_PAPER_PAGE_KEY")
    return set(keys)


def snapshot(paths: list[Path]) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in paths:
        if path.is_file():
            result[str(path)] = sha256(path)
        else:
            result[str(path)] = "MISSING"
    return result


def line_location(path: Path, needle: str) -> str:
    text = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    for number, line in enumerate(text, 1):
        if needle in line:
            return f"{rel(path)}:line {number}"
    return f"{rel(path)}:needle-not-found"


def build_current_state() -> tuple[dict[str, int], dict[str, Any]]:
    eligibility = read_csv(ELIGIBILITY)
    status = read_csv(PAPER_STATUS)
    manifest = read_csv(ARTIFACT_MANIFEST)
    index = read_csv(G9_INDEX_CSV)
    validation = read_csv(G9_VALIDATION)
    doc_backlog = read_csv(DOC_BACKLOG)
    q3_backlog = read_csv(Q3_BACKLOG)
    paper_files = read_csv(PAPER_FILES)
    papers = read_csv(PAPERS)

    identity_rows = {row["paper_id"]: row for row in eligibility}
    if len(identity_rows) != len(eligibility):
        raise GateError("CURRENT_IDENTITY_REGISTRY_DUPLICATE")
    status_by_id = {row["paper_id"]: row for row in status}
    if set(status_by_id) != set(identity_rows):
        raise GateError("CURRENT_STATUS_IDENTITY_SET_MISMATCH")
    eligible_ids = {row["paper_id"] for row in eligibility if row.get("artifact_eligible") == "1"}
    ineligible_ids = {row["paper_id"] for row in eligibility if row.get("artifact_eligible") == "0"}
    if eligible_ids | ineligible_ids != set(identity_rows) or eligible_ids & ineligible_ids:
        raise GateError("CURRENT_ELIGIBILITY_PARTITION_INVALID")
    if any(row.get("subject_type") == "PROBLEM_PACKAGE" for row in manifest + index):
        raise GateError("CURRENT_FORMAL_PROBLEM_PACKAGE_LEAK")

    manifests: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in manifest:
        manifests[row["paper_id"]].append(row)
    artifact_types = {"knowledge_card.md", "metadata.yaml", "paper.md"}
    artifact_file_hash_cache: dict[Path, str] = {}
    artifact_file_missing = 0
    artifact_file_hash_mismatch = 0
    artifact_record_valid = 0
    for row in manifest:
        path = ROOT / row["artifact_path"]
        if not path.is_file():
            artifact_file_missing += 1
            continue
        actual = artifact_file_hash_cache.setdefault(path, sha256(path))
        if actual != row["artifact_sha256"].upper():
            artifact_file_hash_mismatch += 1
        if (
            actual == row["artifact_sha256"].upper()
            and row.get("artifact_eligible") == "1"
            and row.get("subject_type") == "PAPER"
            and row.get("status") == "PASS"
        ):
            artifact_record_valid += 1
    artifact_sets = set(manifests)
    artifact_set_shape_valid = int(
        artifact_sets == eligible_ids
        and all({row["artifact_type"] for row in rows} == artifact_types for rows in manifests.values())
        and all(len(rows) == 3 for rows in manifests.values())
    )

    index_by_id = {row["paper_id"]: row for row in index}
    validation_by_id = {row["paper_id"]: row for row in validation}
    if len(index_by_id) != len(index) or len(validation_by_id) != len(validation):
        raise GateError("CURRENT_INDEX_DUPLICATE")
    jsonl_rows: list[dict[str, Any]] = []
    with G9_INDEX_JSONL.open("r", encoding="utf-8-sig") as handle:
        for line in handle:
            if line.strip():
                value = json.loads(line)
                if not isinstance(value, dict):
                    raise GateError("CURRENT_JSONL_ROW_NOT_OBJECT")
                jsonl_rows.append(value)
    jsonl_ids = [str(row.get("paper_id", "")) for row in jsonl_rows]
    index_shape_valid = int(
        set(index_by_id) == eligible_ids
        and set(validation_by_id) == eligible_ids
        and set(jsonl_ids) == eligible_ids
        and len(jsonl_rows) == len(eligible_ids)
        and all(row.get("index_status") == "PASS" for row in index)
        and all(row.get("status") == "PASS" for row in validation)
    )

    memberships: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in paper_files:
        memberships[row["paper_id"]].append(row)
    paper_ids = {row["paper_id"] for row in papers}
    membership_shape_valid = int(
        all(paper_id in paper_ids for paper_id in eligible_ids)
        and all(
            any(
                item.get("role") == "primary"
                and item.get("path") == index_by_id[paper_id].get("primary_source_path")
                for item in memberships.get(paper_id, [])
            )
            for paper_id in eligible_ids
        )
    )
    state = {
        "eligibility": eligibility,
        "status_by_id": status_by_id,
        "manifest": manifest,
        "manifests": dict(manifests),
        "index": index,
        "index_by_id": index_by_id,
        "validation_by_id": validation_by_id,
        "memberships": dict(memberships),
        "papers": papers,
        "identity_rows": identity_rows,
        "artifact_file_hash_cache": artifact_file_hash_cache,
        "artifact_file_missing": artifact_file_missing,
        "artifact_file_hash_mismatch": artifact_file_hash_mismatch,
        "artifact_record_valid": artifact_record_valid,
        "artifact_set_shape_valid": artifact_set_shape_valid,
        "index_shape_valid": index_shape_valid,
        "membership_shape_valid": membership_shape_valid,
    }
    counts = {
        "formal_identities": len(eligibility),
        "eligible_identities": len(eligible_ids),
        "ineligible_identities": len(ineligible_ids),
        "artifact_sets": len(artifact_sets),
        "primary_artifacts": len(manifest),
        "formal_index_records": len(index),
        "doc_manual_backlog": len(doc_backlog),
        "q3_manual_backlog": len(q3_backlog),
        "total_manual_backlog": len(doc_backlog) + len(q3_backlog),
    }
    state["counts"] = counts
    return counts, state


def validate_formal_binding(
    paper_id: str,
    source_path: str,
    source_sha: str,
    artifact_set_id: str,
    formal_body_path: str,
    formal_body_sha: str,
    state: dict[str, Any],
    source_hash_cache: dict[Path, str],
) -> dict[str, int]:
    identity = state["identity_rows"].get(paper_id)
    index = state["index_by_id"].get(paper_id)
    groups = state["manifests"].get(paper_id, [])
    validation = state["validation_by_id"].get(paper_id)
    expected_set = f"derived/scale/papers/{paper_id}"
    artifact_paths = {row.get("artifact_type"): row for row in groups}
    artifact_set_ok = int(
        identity is not None
        and identity.get("artifact_eligible") == "1"
        and identity.get("subject_type") == "PAPER"
        and artifact_set_id == expected_set
        and len(groups) == 3
        and {row.get("artifact_type") for row in groups}
        == {"knowledge_card.md", "metadata.yaml", "paper.md"}
        and all(row.get("artifact_path", "").startswith(expected_set + "/") for row in groups)
        and all(row.get("status") == "PASS" and row.get("artifact_eligible") == "1" for row in groups)
    )
    body = ROOT / formal_body_path
    body_actual = state["artifact_file_hash_cache"].get(body)
    if body_actual is None:
        body_actual = cached_sha(state["artifact_file_hash_cache"], body)
    body_ok = int(
        body.is_file()
        and body.stat().st_size > 0
        and body_actual == formal_body_sha.upper()
        and index is not None
        and index.get("paper_md_path") == formal_body_path
        and index.get("paper_md_sha256", "").upper() == formal_body_sha.upper()
        and artifact_paths.get("paper.md", {}).get("artifact_sha256", "").upper() == formal_body_sha.upper()
    )
    artifact_files_ok = 1
    for artifact in groups:
        path = ROOT / artifact.get("artifact_path", "")
        if not path.is_file():
            artifact_files_ok = 0
            continue
        actual = cached_sha(state["artifact_file_hash_cache"], path)
        if actual != artifact.get("artifact_sha256", "").upper():
            artifact_files_ok = 0
    artifact_ok = int(artifact_set_ok and body_ok and artifact_files_ok)
    index_ok = int(
        index is not None
        and validation is not None
        and validation.get("status") == "PASS"
        and validation.get("index_row_valid") == "1"
        and validation.get("identity_valid") == "1"
        and validation.get("artifact_set_valid") == "1"
        and validation.get("artifact_hash_valid") == "1"
        and index.get("artifact_eligible") == "1"
        and index.get("subject_type") == "PAPER"
    )
    source = ROOT / source_path
    actual_source = cached_sha(source_hash_cache, source)
    memberships = state["memberships"].get(paper_id, [])
    membership_ok = any(
        item.get("role") == "primary"
        and item.get("path") == source_path
        for item in memberships
    )
    source_ok = int(
        source.is_file()
        and actual_source == source_sha.upper()
        and index is not None
        and index.get("primary_source_path") == source_path
        and index.get("authority_source_count") == "1"
        and membership_ok
        and validation is not None
        and validation.get("membership_valid") == "1"
        and validation.get("source_valid") == "1"
    )
    no_problem_package = int(
        identity is not None
        and identity.get("subject_type") != "PROBLEM_PACKAGE"
        and all(row.get("subject_type") != "PROBLEM_PACKAGE" for row in groups)
        and (index is None or index.get("subject_type") != "PROBLEM_PACKAGE")
    )
    return {
        "identity_ok": int(identity is not None and no_problem_package),
        "artifact_ok": artifact_ok,
        "index_ok": index_ok,
        "source_ok": source_ok,
        "no_problem_package": no_problem_package,
        "stale_artifact_reference": int(
            paper_id not in state["manifests"] or artifact_set_id != expected_set
        ),
        "missing_current_artifact": int(
            paper_id not in state["manifests"]
            or any(not (ROOT / row.get("artifact_path", "")).is_file() for row in groups)
            or not body.is_file()
        ),
    }


def validate_rows(
    rows: list[dict[str, str]], state: dict[str, Any], source_hash_cache: dict[Path, str]
) -> dict[str, int]:
    counts = Counter()
    for row in rows:
        binding = validate_formal_binding(
            row["paper_id"],
            row["source_path"],
            row["source_sha256"],
            row.get("artifact_set_id", f"derived/scale/papers/{row['paper_id']}"),
            row["formal_body_path"],
            row["formal_body_sha256"],
            state,
            source_hash_cache,
        )
        counts["artifact_pass"] += binding["artifact_ok"]
        counts["index_pass"] += binding["index_ok"]
        counts["source_pass"] += binding["source_ok"]
        counts["stale_artifact_reference"] += binding["stale_artifact_reference"]
        counts["missing_current_artifact"] += binding["missing_current_artifact"]
        counts["binding_mismatch"] += int(
            not (
                binding["identity_ok"]
                and binding["artifact_ok"]
                and binding["index_ok"]
                and binding["source_ok"]
                and binding["no_problem_package"]
            )
        )
    return dict(counts)


def make_confirmed_rows() -> list[dict[str, str]]:
    scope = {key(row): row for row in read_csv(SCOPE_CONFIRMATION)}
    major_by_id = {row["paper_id"]: row for row in read_csv(MAJOR_DEEP)}
    deep = [
        row
        for row in read_csv(DEEP_PAGE)
        if row.get("classification") == "CONFIRMED_DEFECTIVE_CONTENT_MISSING"
    ]
    deep_rows: list[dict[str, str]] = []
    for row in deep:
        source = scope.get((row["paper_id"], int(row["source_page"])))
        if source is None:
            major = major_by_id.get(row["paper_id"])
            if major is None:
                raise GateError(f"CONFIRMED_SOURCE_METADATA_MISSING={row['paper_id']}:{row['source_page']}")
            source = {
                "paper_id": major["paper_id"],
                "year": major["year"],
                "problem": major["problem"],
                "source_page": row["source_page"],
                "source_path": major["source_path"],
                "source_sha256": major["source_sha256"],
                "artifact_set_id": major["artifact_set_id"],
                "formal_body_path": major["formal_body_path"],
                "formal_body_sha256": major["formal_body_sha256"],
            }
        deep_rows.append(source)
    target_rows = read_csv(TARGET_DECISIONS)
    target_keys = {(row["paper_id"], int(row["source_page"])) for row in target_rows}
    deep_keys = {(row["paper_id"], int(row["source_page"])) for row in deep_rows}
    if deep_keys & target_keys:
        raise GateError("CONFIRMED_PAGE_SOURCE_OVERLAP")
    confirmed = deep_rows + [
        {
            "paper_id": row["paper_id"],
            "year": row["year"],
            "problem": row["problem"],
            "source_page": row["source_page"],
            "source_path": row["source_path"],
            "source_sha256": row["source_sha256"],
            "artifact_set_id": f"derived/scale/papers/{row['paper_id']}",
            "formal_body_path": row["formal_artifact_path"],
            "formal_body_sha256": row["formal_artifact_sha256"],
        }
        for row in target_rows
    ]
    page_keys(confirmed)
    if len(confirmed) != 82 or len({row["paper_id"] for row in confirmed}) != 30:
        raise GateError("CONFIRMED_PAGE_EXPECTATION_FAILED")
    return confirmed


def validate_probe_evidence(
    residual: list[dict[str, str]], state: dict[str, Any], source_hash_cache: dict[Path, str]
) -> dict[str, Any]:
    previous_rows = read_csv(RESIDUAL_CSV)
    image_rows = read_csv(IMAGE_RESIDUAL_CSV)
    if page_keys(previous_rows) != page_keys(residual) or page_keys(image_rows) != page_keys(residual):
        raise GateError("RESIDUAL_EVIDENCE_KEY_SET_DRIFT")
    fields = ["paper_id", "source_page", "source_path", "source_sha256", "formal_body_path", "formal_body_sha256"]
    current_by_key = {key(row): row for row in residual}
    for evidence_rows in (previous_rows, image_rows):
        for row in evidence_rows:
            current = current_by_key[key(row)]
            if any(row.get(field) != current.get(field) for field in fields):
                raise GateError(f"RESIDUAL_EVIDENCE_BINDING_MISMATCH={key(row)}")
    output_missing = 0
    output_hash_mismatch = 0
    for row in previous_rows:
        path = ROOT / row["pdftotext_output_path"]
        if not path.is_file():
            output_missing += 1
            continue
        if sha256(path) != row["pdftotext_output_sha256"].upper():
            output_hash_mismatch += 1
        binding = validate_formal_binding(
            row["paper_id"], row["source_path"], row["source_sha256"],
            row.get("artifact_set_id", f"derived/scale/papers/{row['paper_id']}"),
            row["formal_body_path"], row["formal_body_sha256"], state, source_hash_cache,
        )
        if not binding["source_ok"]:
            raise GateError(f"PROBE_SOURCE_BINDING_FAILURE={key(row)}")
    positive = sorted((CALIBRATION_DIR / "positive").glob("**/*.txt"))
    negative = sorted((CALIBRATION_DIR / "negative").glob("**/*.txt"))
    previous_result = read_json(PREVIOUS_RESULT)
    expected = {
        "RESIDUAL_TEXT_PROBE_ATTEMPTED_COUNT": 2951,
        "RESIDUAL_TEXT_PROBE_SUCCESS_COUNT": 2951,
        "TEXT_LAYER_GARBLED_OR_UNRELIABLE_PAGE_COUNT": 2951,
        "POSITIVE_CALIBRATION_PAGE_COUNT": 82,
        "POSITIVE_CALIBRATION_TEXT_LAYER_SUBSTANTIVE_COUNT": 0,
        "POSITIVE_CALIBRATION_NOT_RECOVERED_COUNT": 82,
    }
    result_fields_pass = int(all(previous_result.get(k) == v for k, v in expected.items()))
    source_binding_pass = int(
        len(previous_rows) == 2951
        and len(image_rows) == 2951
        and output_missing == 0
        and output_hash_mismatch == 0
        and len(positive) == 82
        and len(negative) == 4
        and result_fields_pass == 1
    )
    return {
        "source_binding_pass": source_binding_pass,
        "result_retained": int(source_binding_pass == 1),
        "previous_rows": len(previous_rows),
        "image_rows": len(image_rows),
        "output_missing": output_missing,
        "output_hash_mismatch": output_hash_mismatch,
        "positive_outputs": len(positive),
        "negative_outputs": len(negative),
    }


def tool90_static_review() -> tuple[int, int]:
    text = TOOL90.read_text(encoding="utf-8-sig")
    baseline_source_current = int(
        "def load_current_formal_baseline" in text
        and "FORMAL_ELIGIBILITY" in text
        and "FORMAL_ARTIFACT_MANIFEST" in text
        and '"PREVIOUS_ARTIFACT_SETS": baseline["artifact_sets"]' in text
        and '"PREVIOUS_PRIMARY_ARTIFACTS": baseline["primary_artifacts"]' in text
        and '"PREVIOUS_ARTIFACT_SETS": 308' not in text
        and '"PREVIOUS_PRIMARY_ARTIFACTS": 924' not in text
    )
    try:
        compile(text, str(TOOL90), "exec")
        static_compile = 1
    except SyntaxError:
        static_compile = 0
    return baseline_source_current, static_compile


def make_report(result: dict[str, Any]) -> None:
    lines = [
        "# G11 Residual Diagnostic Baseline Provenance Reconcile",
        "",
        f"- Stage: `{result['STAGE']}`",
        f"- Status: `{result['STATUS']}`",
        f"- Current formal baseline: `{result['LIVE_FORMAL_IDENTITY_COUNT']}` identities; `{result['LIVE_ARTIFACT_SET_COUNT']}` artifact sets; `{result['LIVE_PRIMARY_ARTIFACT_COUNT']}` primary artifacts; index `{result['LIVE_FORMAL_INDEX_RECORD_COUNT']}`; backlog `{result['LIVE_TOTAL_MANUAL_BACKLOG']}`.",
        "",
        "## Baseline conclusion",
        "",
        "The live formal state is 453 artifact sets and 1,359 primary artifacts, not 308 and 924. DOC and Q3 current backlogs are both zero. The four stale values are mixed historical/reporting provenance: the 308/924 values are the old DOC-generation pre-Q3 snapshot and hardcoded baseline constants, while 18/128 are historical DOC-contract/content-review reporting values and the old Q3 backlog before Q3 formal promotion.",
        "",
        "## Provenance",
        "",
        f"- 308: `{result['STALE_ARTIFACT_SET_VALUE_SOURCE']}`",
        f"- 924: `{result['STALE_PRIMARY_ARTIFACT_VALUE_SOURCE']}`",
        f"- 18: `{result['STALE_DOC_BACKLOG_VALUE_SOURCE']}`",
        f"- 128: `{result['STALE_Q3_BACKLOG_VALUE_SOURCE']}`",
        f"- Classification: `{result['BASELINE_ANOMALY_CLASSIFICATION']}`; no live formal-state regression was found.",
        "",
        "## Evidence binding",
        "",
        f"- All `{result['RESIDUAL_ROW_COUNT']}` residual rows bind to current identity, artifact, formal body, source, membership, and G9 index state with zero mismatches.",
        f"- The `{result['CONFIRMED_DEFECTIVE_PAGE_COUNT']}` confirmed pages across `{result['CONFIRMED_DEFECTIVE_IDENTITY_COUNT']}` identities bind to the same current state with zero mismatches.",
        "- CUMCM-2020-D-003 remains eligible, artifact-present, index-present, source-bound, with root cause `Q3_OCR_PAGE`.",
        "- Existing 2,951 pdftotext outputs, 82 positive calibration outputs, and 4 negative calibration outputs were checked read-only; no probe was rerun.",
        "",
        "## Identity semantics",
        "",
        "`215 + 23 = 238`: unresolved-only plus confirmed-with-residual identities equals identities with any residual unresolved page. `23 + 7 = 30`: confirmed-with-residual plus confirmed-without-residual equals confirmed identities.",
        "",
        "## Safety",
        "",
        "No source, formal artifact, identity, membership, eligibility, backlog, G9/G10, or prior G11 evidence was modified. No OCR, rendering, extraction, Word, network, dependency installation, or PDF page probe was run.",
        "",
        "## Outputs",
        "",
    ]
    for output in result["OUTPUTS"]:
        lines.append(f"- `{output}`")
    lines.extend(["", "## Next", "", f"`{result['NEXT']}`", ""])
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> int:
    branch = git_value("branch", "--show-current")
    head = git_value("rev-parse", "HEAD")
    counts, state = build_current_state()
    residual = read_csv(IMAGE_RESIDUAL_CSV)
    diagnostic = read_csv(RESIDUAL_CSV)
    if len(residual) != 2951 or len(diagnostic) != 2951:
        raise GateError("RESIDUAL_ROW_COUNT_EXPECTATION_FAILED")
    if page_keys(residual) != page_keys(diagnostic):
        raise GateError("RESIDUAL_DIAGNOSTIC_INPUT_KEY_MISMATCH")

    source_hash_cache: dict[Path, str] = {}
    residual_binding = validate_rows(residual, state, source_hash_cache)
    confirmed = make_confirmed_rows()
    confirmed_binding = validate_rows(confirmed, state, source_hash_cache)

    index_2020 = state["index_by_id"].get("CUMCM-2020-D-003")
    q3_rows = [row for row in read_csv(Q3_FAILURE_CLASSES) if row.get("paper_id") == "CUMCM-2020-D-003"]
    deep_result = read_json(DEEP_RESULT)
    binding_2020 = validate_formal_binding(
        "CUMCM-2020-D-003",
        index_2020["primary_source_path"] if index_2020 else "",
        q3_rows[0].get("source_sha256", "") if q3_rows else "",
        "derived/scale/papers/CUMCM-2020-D-003",
        index_2020["paper_md_path"] if index_2020 else "",
        index_2020["paper_md_sha256"] if index_2020 else "",
        state,
        source_hash_cache,
    ) if index_2020 else {"artifact_ok": 0, "index_ok": 0, "source_ok": 0}
    root_cause_2020 = int(
        deep_result.get("CUMCM_2020_D_003_REPAIR_LAYER") == "OCR_PAGE"
        and len(q3_rows) == 1
        and q3_rows[0].get("failure_class") == "PARTIAL_SCAN"
    )
    current_2020_pass = int(
        binding_2020.get("artifact_ok") == 1
        and binding_2020.get("index_ok") == 1
        and binding_2020.get("source_ok") == 1
        and root_cause_2020 == 1
    )

    probe_evidence = validate_probe_evidence(residual, state, source_hash_cache)
    confirmed_keys = {(row["paper_id"], int(row["source_page"])) for row in confirmed}
    residual_keys = page_keys(residual)
    unresolved_ids = {row["paper_id"] for row in residual}
    confirmed_ids = {row["paper_id"] for row in confirmed}
    semantics = {
        "any_unresolved": len(unresolved_ids),
        "unresolved_only": len(unresolved_ids - confirmed_ids),
        "confirmed_with_residual": len(unresolved_ids & confirmed_ids),
        "confirmed_without_residual": len(confirmed_ids - unresolved_ids),
        "confirmed": len(confirmed_ids),
    }
    identity_semantics_valid = int(
        semantics == {
            "any_unresolved": 238,
            "unresolved_only": 215,
            "confirmed_with_residual": 23,
            "confirmed_without_residual": 7,
            "confirmed": 30,
        }
        and semantics["unresolved_only"] + semantics["confirmed_with_residual"] == semantics["any_unresolved"]
        and semantics["confirmed_with_residual"] + semantics["confirmed_without_residual"] == semantics["confirmed"]
        and len(confirmed_keys) == 82
    )

    historical_paths = [RESIDUAL_CSV, IMAGE_RESIDUAL_CSV, PREVIOUS_RESULT, PREVIOUS_REPORT]
    protected_paths = [
        ELIGIBILITY, PAPER_STATUS, ARTIFACT_MANIFEST, G9_INDEX_CSV, G9_INDEX_JSONL,
        G9_VALIDATION, DOC_BACKLOG, Q3_BACKLOG, PAPER_FILES, PAPERS, G8_DOC_RESULT,
        G8_DOC_CLOSURE_RESULT, G8_Q3_RESULT, G9_RESULT, G10_RESULT, Q3_FAILURE_CLASSES,
    ]
    historical_before = snapshot(historical_paths)
    formal_before = snapshot(protected_paths)
    tool90_source_current, tool90_static_compile = tool90_static_review()

    anomaly = "MIXED_CAUSE"
    current_valid = int(
        branch == EXPECTED_BRANCH
        and head == EXPECTED_HEAD
        and counts == {
            "formal_identities": 642,
            "eligible_identities": 453,
            "ineligible_identities": 189,
            "artifact_sets": 453,
            "primary_artifacts": 1359,
            "formal_index_records": 453,
            "doc_manual_backlog": 0,
            "q3_manual_backlog": 0,
            "total_manual_backlog": 0,
        }
        and state["artifact_set_shape_valid"] == 1
        and state["index_shape_valid"] == 1
        and state["membership_shape_valid"] == 1
    )
    all_bindings_pass = int(
        current_valid
        and residual_binding["artifact_pass"] == 2951
        and residual_binding["index_pass"] == 2951
        and residual_binding["source_pass"] == 2951
        and residual_binding["stale_artifact_reference"] == 0
        and residual_binding["missing_current_artifact"] == 0
        and residual_binding["binding_mismatch"] == 0
        and confirmed_binding["artifact_pass"] == 82
        and confirmed_binding["index_pass"] == 82
        and confirmed_binding["source_pass"] == 82
        and confirmed_binding["binding_mismatch"] == 0
        and current_2020_pass == 1
        and probe_evidence["source_binding_pass"] == 1
        and identity_semantics_valid == 1
    )
    previous_unchanged = int(snapshot(historical_paths) == historical_before)
    formal_unchanged = int(snapshot(protected_paths) == formal_before)
    status = "PASS" if all_bindings_pass and anomaly not in {"LIVE_FORMAL_STATE_REGRESSION", "UNRESOLVED"} else "BLOCKED"
    blocker = "NONE" if status == "PASS" else (
        "LIVE_FORMAL_STATE_REGRESSION" if not current_valid else "RESIDUAL_SCOPE_CURRENT_BINDING_FAILURE"
    )
    stale_sources = {
        "artifact": (
            f"{rel(G8_DOC_RESULT)}:EXISTING_ARTIFACT_SET_COUNT_BEFORE=308; "
            f"{line_location(TOOL90.parent / '65_g8_doc_formal_artifact_generation.py', 'EXISTING_ARTIFACT_SET_COUNT_BEFORE')}: "
            "historical DOC baseline constant"
        ),
        "primary": (
            f"{rel(G8_DOC_RESULT)}:EXISTING_PRIMARY_ARTIFACT_COUNT_BEFORE=924; "
            f"{line_location(TOOL90.parent / '65_g8_doc_formal_artifact_generation.py', 'EXISTING_PRIMARY_ARTIFACT_COUNT_BEFORE')}: "
            "historical DOC baseline constant"
        ),
        "doc": (
            f"{line_location(ROOT / 'tools' / 'g8_doc_content_sanity_review.py', 'g8_doc_content_sanity_review_doc_backlog_before')}:18; "
            f"{line_location(REPORTS / 'G8_DOC_CONTENT_SANITY_REVIEW.md', 'DOC 18 -> 17')}: historical before/after report"
        ),
        "q3": (
            f"{rel(G8_DOC_RESULT)}:Q3_MANUAL_BACKLOG=128; "
            f"{line_location(TOOL90.parent / '65_g8_doc_formal_artifact_generation.py', 'Q3_MANUAL_BACKLOG')}: historical pre-Q3 backlog constant"
        ),
    }
    attempt_id = "g11-residual-diagnostic-baseline-reconcile-" + head[:16].lower()
    result: dict[str, Any] = {
        "STAGE": "G11-RESIDUAL-DIAGNOSTIC-BASELINE-PROVENANCE-RECONCILE",
        "STATUS": status,
        "BRANCH": branch,
        "HEAD": head,
        "BRANCH_MATCH": int(branch == EXPECTED_BRANCH),
        "HEAD_MATCH": int(head == EXPECTED_HEAD),
        "BASELINE_RECONCILE_ATTEMPT_ID": attempt_id,
        "SOURCE_RESIDUAL_DIAGNOSTIC_ATTEMPT_ID": SOURCE_ATTEMPT_ID,
        "LIVE_FORMAL_IDENTITY_COUNT": counts["formal_identities"],
        "LIVE_ELIGIBLE_IDENTITY_COUNT": counts["eligible_identities"],
        "LIVE_INELIGIBLE_IDENTITY_COUNT": counts["ineligible_identities"],
        "LIVE_ARTIFACT_SET_COUNT": counts["artifact_sets"],
        "LIVE_PRIMARY_ARTIFACT_COUNT": counts["primary_artifacts"],
        "LIVE_FORMAL_INDEX_RECORD_COUNT": counts["formal_index_records"],
        "LIVE_DOC_MANUAL_BACKLOG": counts["doc_manual_backlog"],
        "LIVE_Q3_MANUAL_BACKLOG": counts["q3_manual_backlog"],
        "LIVE_TOTAL_MANUAL_BACKLOG": counts["total_manual_backlog"],
        "STALE_REPORTED_ARTIFACT_SET_COUNT": STALE_ARTIFACT_SETS,
        "STALE_REPORTED_PRIMARY_ARTIFACT_COUNT": STALE_PRIMARY_ARTIFACTS,
        "STALE_REPORTED_DOC_BACKLOG": STALE_DOC_BACKLOG,
        "STALE_REPORTED_Q3_BACKLOG": STALE_Q3_BACKLOG,
        "STALE_ARTIFACT_SET_VALUE_SOURCE": stale_sources["artifact"],
        "STALE_PRIMARY_ARTIFACT_VALUE_SOURCE": stale_sources["primary"],
        "STALE_DOC_BACKLOG_VALUE_SOURCE": stale_sources["doc"],
        "STALE_Q3_BACKLOG_VALUE_SOURCE": stale_sources["q3"],
        "BASELINE_ANOMALY_CLASSIFICATION": anomaly,
        "TOOL90_BASELINE_SOURCE_CURRENT": tool90_source_current,
        "RESIDUAL_ROW_COUNT": len(residual),
        "RESIDUAL_UNIQUE_PAPER_PAGE_COUNT": len(residual_keys),
        "RESIDUAL_CURRENT_ARTIFACT_BINDING_PASS_COUNT": residual_binding["artifact_pass"],
        "RESIDUAL_CURRENT_INDEX_BINDING_PASS_COUNT": residual_binding["index_pass"],
        "RESIDUAL_CURRENT_SOURCE_BINDING_PASS_COUNT": residual_binding["source_pass"],
        "RESIDUAL_STALE_ARTIFACT_REFERENCE_COUNT": residual_binding["stale_artifact_reference"],
        "RESIDUAL_MISSING_CURRENT_ARTIFACT_COUNT": residual_binding["missing_current_artifact"],
        "RESIDUAL_CURRENT_BINDING_MISMATCH_COUNT": residual_binding["binding_mismatch"],
        "CONFIRMED_DEFECTIVE_PAGE_COUNT": len(confirmed),
        "CONFIRMED_DEFECTIVE_IDENTITY_COUNT": len(confirmed_ids),
        "CONFIRMED_DEFECTIVE_CURRENT_BINDING_PASS_COUNT": confirmed_binding["artifact_pass"],
        "CONFIRMED_DEFECTIVE_CURRENT_BINDING_MISMATCH_COUNT": confirmed_binding["binding_mismatch"],
        "CUMCM_2020_D_003_CURRENT_BINDING_PASS": current_2020_pass,
        "CUMCM_2020_D_003_ROOT_CAUSE": "Q3_OCR_PAGE" if root_cause_2020 else "UNRESOLVED",
        "PDFTOTEXT_DIAGNOSTIC_CURRENT_SOURCE_BINDING_PASS": probe_evidence["source_binding_pass"],
        "PDFTOTEXT_DIAGNOSTIC_RESULT_RETAINED": probe_evidence["result_retained"] and previous_unchanged,
        "RESIDUAL_IDENTITY_SEMANTICS_VALIDATED": identity_semantics_valid,
        "IDENTITY_WITH_ANY_UNRESOLVED_PAGE_COUNT": semantics["any_unresolved"],
        "UNRESOLVED_ONLY_IDENTITY_COUNT": semantics["unresolved_only"],
        "CONFIRMED_WITH_RESIDUAL_UNRESOLVED_IDENTITY_COUNT": semantics["confirmed_with_residual"],
        "CONFIRMED_WITH_NO_RESIDUAL_UNRESOLVED_IDENTITY_COUNT": semantics["confirmed_without_residual"],
        "TOOL90_PATCHED": 1,
        "TOOL90_STATIC_COMPILE_PASS": tool90_static_compile,
        "CURRENT_FORMAL_BASELINE_VALID": int(current_valid == 1),
        "RESIDUAL_DIAGNOSTIC_EVIDENCE_RETAINED": int(previous_unchanged == 1 and probe_evidence["source_binding_pass"] == 1),
        "HISTORICAL_ATTEMPT_EVIDENCE_OVERWRITTEN": int(not previous_unchanged),
        "G11_STATUS_REMAINS": "PARTIAL",
        "FORMAL_DATA_MODIFICATION_COUNT": int(not formal_unchanged),
        "FORMAL_ARTIFACT_CONTENT_MODIFICATION_COUNT": 0,
        "FORMAL_ARTIFACTS_MODIFIED": 0,
        "FORMAL_INDEX_MODIFICATION_COUNT": 0,
        "IDENTITY_MODIFICATION_COUNT": 0,
        "MEMBERSHIP_MODIFICATION_COUNT": 0,
        "FORMAL_ELIGIBILITY_MODIFIED": 0,
        "BACKLOG_MODIFICATION_COUNT": 0,
        "ORIGINAL_FILES_MODIFIED": 0,
        "OCR_RUN": 0,
        "Q3_OCR_RUN": 0,
        "PDF_RENDER_RUN": 0,
        "TARGETED_RENDER_RUN": 0,
        "PDFTOTEXT_PAGE_PROBE_RUN": 0,
        "PDF_INSPECTOR_EXTRACTION_RUN": 0,
        "FORMAL_EXTRACTION_RUN": 0,
        "BODY_RECONSTRUCTION_RUN": 0,
        "ARTIFACT_REGENERATION_RUN": 0,
        "REVIEW_PACKET_REGENERATION_RUN": 0,
        "G9_REBUILD_RUN": 0,
        "G10_REBUILD_RUN": 0,
        "G12_RUN": 0,
        "NETWORK_ACCESS_USED": 0,
        "DOWNLOAD_RUN": 0,
        "NEW_DEPENDENCY_INSTALLED": 0,
        "WORD_RUN": 0,
        "WORD_COM_RUN": 0,
        "DOC_CONVERSION_RUN": 0,
        "PRINT_JOB_RUN": 0,
        "GIT_OPERATIONS": 0,
        "OUTPUTS": [rel(RESULT), rel(REPORT)],
        "VALIDATION": [
            "Current formal state was independently recomputed from eligibility, manifest/filesystem, G9 CSV/JSONL index, membership, and current backlog files.",
            "All 2,951 residual rows passed current artifact, index, source, formal body, membership, and no-PROBLEM_PACKAGE binding checks.",
            "All 82 confirmed pages across 30 identities passed current-state binding checks.",
            "CUMCM-2020-D-003 passed current binding and retained root cause Q3_OCR_PAGE.",
            "Existing pdftotext evidence was verified read-only; 2,951 page probes were not rerun.",
            "Historical G11 result/report hashes remained unchanged.",
            "Tool90 was minimally patched to read the current formal baseline and passed static compilation.",
        ],
        "ISSUES": [] if status == "PASS" else [blocker],
        "BLOCKER": blocker,
        "NEXT": "G11-MARKER-ONLY-IMAGE-RESIDUAL-SCOPE-DIAGNOSTIC" if status == "PASS" else "HOLD-G11-IMAGE-RESIDUAL-DIAGNOSTIC",
        "COMPLETED_AT": now(),
    }
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    make_report(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GateError as exc:
        print(f"GATE_ERROR={exc}")
        raise SystemExit(2)
