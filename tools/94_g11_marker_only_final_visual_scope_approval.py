"""Transcribe the user's three visual decisions and close G11 scope.

The visual classifications in this stage are supplied explicitly by the user.
This script performs no image inspection, OCR, rendering, extraction, repair,
or automated classification.  It validates existing page-level evidence,
changes only the three authorized decision-sheet fields, and writes isolated
final scope manifests and an approval report.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCALE = ROOT / "catalog" / "scale"
REPORTS = ROOT / "reports" / "scale"

EXPECTED_BRANCH = "library-refactor-v1"
EXPECTED_HEAD = "557724fba6572d4d83dc421feda5b17b13ff8d66"
Q3_TARGET = "CUMCM-2020-D-003"

DECISIONS = SCALE / "g11_marker_only_final_visual_scope_decisions.csv"
FINAL_REVIEW_RESULT = SCALE / "g11_marker_only_final_visual_scope_review_result.json"
FINAL_RESIDUAL_INPUT = SCALE / "g11_marker_only_final_visual_residual_input.csv"
IMAGE_DIAGNOSTIC = SCALE / "g11_marker_only_image_residual_scope_diagnostic.csv"
IMAGE_DIAGNOSTIC_RESULT = SCALE / "g11_marker_only_image_residual_scope_diagnostic_result.json"
IMAGE_TARGETS = SCALE / "g11_marker_only_image_confirmed_repair_targets.csv"
STATUS_CONTRACT = SCALE / "g11_targeted_visual_review_status_contract.json"
PAGE_DEEP = SCALE / "g11_marker_only_page_deep_diagnostic.csv"
MAJOR_DEEP = SCALE / "g11_major_defect_deep_diagnostic.csv"
PRIOR_TARGETED_DECISIONS = SCALE / "g11_targeted_visual_diagnostic_decisions.csv"
PRIOR_TARGETED_APPROVAL = SCALE / "g11_targeted_visual_diagnostic_approval_result.json"
REVIEW_GUIDE = REPORTS / "G11_MARKER_ONLY_FINAL_VISUAL_SCOPE_REVIEW_GUIDE.md"
DIAGNOSTIC_REPORT = REPORTS / "G11_MARKER_ONLY_IMAGE_RESIDUAL_SCOPE_DIAGNOSTIC.md"
REVIEW_PACKET = REPORTS / "g11_marker_only_final_visual_scope_review"

FINAL_SCOPE_MANIFEST = SCALE / "g11_marker_only_final_scope_manifest.csv"
FINAL_REPAIR_TARGETS = SCALE / "g11_marker_only_final_repair_targets.csv"
APPROVAL_RESULT = SCALE / "g11_marker_only_final_visual_scope_approval_result.json"
APPROVAL_REPORT = REPORTS / "G11_MARKER_ONLY_FINAL_VISUAL_SCOPE_APPROVAL.md"

FORMAL_BASELINE_FILES = [
    SCALE / "g8_artifact_manifest.csv",
    SCALE / "g8_paper_status.csv",
    SCALE / "g8_manual_backlog.csv",
    SCALE / "g8_q3_manual_backlog.csv",
    SCALE / "g9_paper_index.csv",
    SCALE / "g10_consistency_result.json",
]

STAMP = timezone(timedelta(hours=8))
AUTHORIZED_DECISION_FIELDS = {
    "source_visual_classification",
    "reviewer_comment",
    "review_status",
}
EXPECTED_KEYS = [
    ("CUMCM-2007-A-003", 19),
    ("CUMCM-2007-B-006", 41),
    ("CUMCM-2007-B-011", 2),
]
USER_DECISIONS = {
    ("CUMCM-2007-A-003", 19): (
        "LEGITIMATE_NONCONTENT",
        "源页面无应进入论文正文数据库的实质论文内容。",
    ),
    ("CUMCM-2007-B-006", 41): (
        "SUBSTANTIVE_CONTENT",
        "源页面包含应进入论文正文数据库的实质论文内容。",
    ),
    ("CUMCM-2007-B-011", 2): (
        "LEGITIMATE_NONCONTENT",
        "源页面无应进入论文正文数据库的实质论文内容。",
    ),
}

MANIFEST_FIELDS = [
    "paper_id",
    "source_page",
    "artifact_set_id",
    "source_path",
    "source_sha256",
    "formal_body_path",
    "formal_body_sha256",
    "final_scope_status",
    "scope_evidence_type",
    "scope_evidence_path",
    "scope_confidence",
    "repair_required",
]

TARGET_FIELDS = [
    "paper_id",
    "artifact_set_id",
    "source_route",
    "confirmed_defective_page_count",
    "confirmed_defective_pages",
    "legitimate_noncontent_page_count",
    "legitimate_noncontent_pages",
    "repair_layer",
    "requires_ocr_for_repair",
    "requires_extraction_for_repair",
    "requires_reconstruction",
    "requires_artifact_repromotion",
    "requires_index_refresh",
    "requires_g10_revalidation",
    "requires_human_rereview",
    "scope_confidence",
]


class GateError(RuntimeError):
    """Raised when the approval gate cannot be completed safely."""


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


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def page_key(row: dict[str, Any]) -> tuple[str, int]:
    try:
        return str(row["paper_id"]), int(row["source_page"])
    except (KeyError, TypeError, ValueError) as exc:
        raise GateError(f"INVALID_PAGE_KEY={row}") from exc


def file_snapshot(paths: list[Path]) -> dict[str, str]:
    return {
        str(path): sha256(path) if path.is_file() else "MISSING"
        for path in paths
    }


def write_csv(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def read_repo_ref() -> tuple[str, str]:
    """Read branch and HEAD directly from .git files without a git command."""
    head_file = ROOT / ".git" / "HEAD"
    if not head_file.is_file():
        raise GateError("GIT_HEAD_FILE_MISSING")
    head_ref = head_file.read_text(encoding="utf-8").strip()
    prefix = "ref: refs/heads/"
    if not head_ref.startswith(prefix):
        raise GateError(f"DETACHED_HEAD={head_ref}")
    branch = head_ref[len(prefix):]
    ref_file = ROOT / ".git" / "refs" / "heads" / branch
    if not ref_file.is_file():
        raise GateError(f"BRANCH_REF_FILE_MISSING={branch}")
    head = ref_file.read_text(encoding="utf-8").strip()
    return branch, head


def parse_pages(value: str, label: str) -> list[int]:
    try:
        pages = [int(item) for item in value.split(";") if item]
    except ValueError as exc:
        raise GateError(f"INVALID_PAGE_LIST={label}:{value}") from exc
    if not pages or any(page < 1 for page in pages) or len(pages) != len(set(pages)):
        raise GateError(f"INVALID_PAGE_LIST={label}:{value}")
    return sorted(pages)


def validate_contract(contract: dict[str, Any]) -> None:
    if contract.get("status") != "PASS":
        raise GateError("STATUS_CONTRACT_NOT_PASS")
    if contract.get("repo_branch") != EXPECTED_BRANCH or contract.get("repo_head") != EXPECTED_HEAD:
        raise GateError("STATUS_CONTRACT_REPO_DRIFT")
    if contract.get("review_status_allowed_values") != ["PENDING", "REVIEWED"]:
        raise GateError("STATUS_CONTRACT_REVIEW_ENUM_DRIFT")
    required_classes = {"PENDING", "SUBSTANTIVE_CONTENT", "LEGITIMATE_NONCONTENT", "UNCLEAR"}
    if set(contract.get("classification_allowed_values", [])) != required_classes:
        raise GateError("STATUS_CONTRACT_CLASSIFICATION_ENUM_DRIFT")


def validate_decisions_before(rows: list[dict[str, str]]) -> tuple[list[str], str]:
    if len(rows) != 3:
        raise GateError(f"FINAL_VISUAL_DECISION_ROW_COUNT_BEFORE={len(rows)}")
    keys = [page_key(row) for row in rows]
    if keys != EXPECTED_KEYS or len(set(keys)) != 3:
        raise GateError(f"FINAL_VISUAL_DECISION_BINDING_DRIFT={keys}")
    if any(row.get("source_visual_classification") != "PENDING" for row in rows):
        raise GateError("FINAL_VISUAL_DECISION_SHEET_NONPENDING_CLASSIFICATION")
    if any(row.get("review_status") != "PENDING" for row in rows):
        raise GateError("FINAL_VISUAL_DECISION_SHEET_NONPENDING_STATUS")
    if any(row.get("reviewer_comment", "") != "" for row in rows):
        raise GateError("FINAL_VISUAL_DECISION_SHEET_NONEMPTY_COMMENT")
    return list(rows[0].keys()), sha256(DECISIONS)


def apply_user_decisions(rows: list[dict[str, str]], fields: list[str]) -> tuple[list[dict[str, str]], dict[str, int]]:
    updated: list[dict[str, str]] = []
    counts = {
        "source_visual_classification": 0,
        "reviewer_comment": 0,
        "review_status": 0,
        "other": 0,
    }
    for row in rows:
        key = page_key(row)
        classification, comment = USER_DECISIONS[key]
        new_row = dict(row)
        new_row["source_visual_classification"] = classification
        new_row["reviewer_comment"] = comment
        new_row["review_status"] = "REVIEWED"
        for field in fields:
            if row.get(field, "") != new_row.get(field, ""):
                if field in AUTHORIZED_DECISION_FIELDS:
                    counts[field] += 1
                else:
                    counts["other"] += 1
        updated.append(new_row)
    if counts["source_visual_classification"] != 3 or counts["reviewer_comment"] != 3 or counts["review_status"] != 3 or counts["other"] != 0:
        raise GateError(f"AUTHORIZED_DECISION_AUDIT_FAILURE={counts}")
    return updated, counts


def load_page_evidence(
    residual: list[dict[str, str]],
    image_diagnostic: list[dict[str, str]],
    image_targets: list[dict[str, str]],
    major_deep: list[dict[str, str]],
    updated_decisions: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]], set[str], dict[str, Any]]:
    target_by_id = {row["paper_id"]: row for row in image_targets}
    major_by_id = {row["paper_id"]: row for row in major_deep}
    if len(target_by_id) != 245 or len(major_by_id) != 245:
        raise GateError("MARKER_ONLY_IDENTITY_COUNT_NOT_245")
    if set(target_by_id) != set(major_by_id):
        raise GateError("MARKER_ONLY_TARGET_IDENTITY_BINDING_DRIFT")

    confirmed_pages: dict[tuple[str, int], dict[str, Any]] = {}
    for target in image_targets:
        pages = parse_pages(target["confirmed_defective_pages"], target["paper_id"])
        if int(target["confirmed_defective_page_count"]) != len(pages):
            raise GateError(f"TARGET_PAGE_COUNT_MISMATCH={target['paper_id']}")
        for page in pages:
            key = (target["paper_id"], page)
            if key in confirmed_pages:
                raise GateError(f"DUPLICATE_CONFIRMED_PAGE={key}")
            confirmed_pages[key] = {"identity": target["paper_id"], "source": target}
    if len(confirmed_pages) != 3030:
        raise GateError(f"PREEXISTING_CONFIRMED_PAGE_COUNT={len(confirmed_pages)}")

    diagnostic_by_key = {page_key(row): row for row in image_diagnostic}
    substantive_keys = {
        page_key(row)
        for row in image_diagnostic
        if row.get("diagnostic_class") == "OCR_SUBSTANTIVE_CONFIRMED"
        and row.get("new_scope_status") == "CONFIRMED_DEFECTIVE"
    }
    if len(substantive_keys) != 2948:
        raise GateError(f"DIAGNOSTIC_SUBSTANTIVE_PAGE_COUNT={len(substantive_keys)}")
    if not substantive_keys.issubset(confirmed_pages):
        raise GateError("DIAGNOSTIC_CONFIRMED_PAGE_NOT_IN_TARGET_SET")
    preexisting_keys = set(confirmed_pages) - substantive_keys
    if len(preexisting_keys) != 82:
        raise GateError(f"PREEXISTING_PAGE_LOWER_BOUND_MISMATCH={len(preexisting_keys)}")

    source_by_id = {
        identity: {
            "artifact_set_id": major["artifact_set_id"],
            "source_path": major["source_path"],
            "source_sha256": major["source_sha256"].upper(),
            "formal_body_path": major["formal_body_path"],
            "formal_body_sha256": major["formal_body_sha256"].upper(),
        }
        for identity, major in major_by_id.items()
    }
    final_rows_by_key = {page_key(row): row for row in residual}
    decision_by_key = {page_key(row): row for row in updated_decisions}
    if set(decision_by_key) != set(EXPECTED_KEYS):
        raise GateError("FINAL_DECISION_BINDING_DRIFT_AFTER_TRANSCRIPTION")

    manifest_rows: list[dict[str, str]] = []
    page_classes: dict[tuple[str, int], str] = {}
    for key, record in confirmed_pages.items():
        identity, page = key
        meta = source_by_id[identity]
        diagnostic = diagnostic_by_key.get(key)
        if key in substantive_keys:
            evidence_type = "DIAGNOSTIC_OCR_CONFIRMED"
            evidence_path = str(diagnostic["ocr_output_path"])
        else:
            evidence_type = "PREEXISTING_CONFIRMED_DEFECTIVE"
            evidence_path = relative(IMAGE_TARGETS)
        manifest_rows.append({
            "paper_id": identity,
            "source_page": str(page),
            "artifact_set_id": meta["artifact_set_id"],
            "source_path": meta["source_path"],
            "source_sha256": meta["source_sha256"],
            "formal_body_path": meta["formal_body_path"],
            "formal_body_sha256": meta["formal_body_sha256"],
            "final_scope_status": "CONFIRMED_DEFECTIVE",
            "scope_evidence_type": evidence_type,
            "scope_evidence_path": evidence_path,
            "scope_confidence": "HIGH",
            "repair_required": "1",
        })
        page_classes[key] = "CONFIRMED_DEFECTIVE"

    for key, decision in decision_by_key.items():
        identity, page = key
        if key in page_classes:
            raise GateError(f"FINAL_DECISION_PAGE_ALREADY_CONFIRMED={key}")
        residual_row = final_rows_by_key[key]
        classification = decision["source_visual_classification"]
        if classification == "SUBSTANTIVE_CONTENT":
            final_status = "CONFIRMED_DEFECTIVE"
            repair_required = "1"
        elif classification == "LEGITIMATE_NONCONTENT":
            final_status = "CONFIRMED_LEGITIMATE_NONCONTENT"
            repair_required = "0"
        else:
            raise GateError(f"FINAL_DECISION_CLASSIFICATION_NOT_CLOSED={key}:{classification}")
        manifest_rows.append({
            "paper_id": identity,
            "source_page": str(page),
            "artifact_set_id": residual_row["artifact_set_id"],
            "source_path": residual_row["source_path"],
            "source_sha256": residual_row["source_sha256"].upper(),
            "formal_body_path": residual_row["formal_body_path"],
            "formal_body_sha256": residual_row["formal_body_sha256"].upper(),
            "final_scope_status": final_status,
            "scope_evidence_type": "USER_EXPLICIT_HUMAN_VISUAL_REVIEW",
            "scope_evidence_path": relative(DECISIONS),
            "scope_confidence": "HIGH",
            "repair_required": repair_required,
        })
        page_classes[key] = final_status

    manifest_rows.sort(key=lambda row: (row["paper_id"], int(row["source_page"])))
    if len(manifest_rows) != 3033 or len(page_classes) != 3033:
        raise GateError(f"FINAL_SCOPE_MANIFEST_PAGE_COUNT={len(manifest_rows)}")
    counts = {
        "defective_pages": sum(value == "CONFIRMED_DEFECTIVE" for value in page_classes.values()),
        "legitimate_pages": sum(value == "CONFIRMED_LEGITIMATE_NONCONTENT" for value in page_classes.values()),
        "unresolved_pages": sum(value not in {"CONFIRMED_DEFECTIVE", "CONFIRMED_LEGITIMATE_NONCONTENT"} for value in page_classes.values()),
    }
    if counts != {"defective_pages": 3031, "legitimate_pages": 2, "unresolved_pages": 0}:
        raise GateError(f"FINAL_PAGE_ACCOUNTING_MISMATCH={counts}")
    return manifest_rows, [
        {"key": f"{identity}|{page}", "status": status}
        for (identity, page), status in sorted(page_classes.items())
    ], set(target_by_id), {"page_classes": page_classes, "counts": counts, "source_by_id": source_by_id, "target_by_id": target_by_id}


def build_final_targets(
    image_targets: list[dict[str, str]],
    page_classes: dict[tuple[str, int], str],
) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    for source in sorted(image_targets, key=lambda row: row["paper_id"]):
        identity = source["paper_id"]
        defective_pages = sorted(
            page for (paper_id, page), status in page_classes.items()
            if paper_id == identity and status == "CONFIRMED_DEFECTIVE"
        )
        legitimate_pages = sorted(
            page for (paper_id, page), status in page_classes.items()
            if paper_id == identity and status == "CONFIRMED_LEGITIMATE_NONCONTENT"
        )
        if not defective_pages:
            raise GateError(f"FINAL_REPAIR_TARGET_WITHOUT_DEFECTIVE_PAGE={identity}")
        result.append({
            "paper_id": identity,
            "artifact_set_id": source["artifact_set_id"],
            "source_route": source["source_route"],
            "confirmed_defective_page_count": str(len(defective_pages)),
            "confirmed_defective_pages": ";".join(map(str, defective_pages)),
            "legitimate_noncontent_page_count": str(len(legitimate_pages)),
            "legitimate_noncontent_pages": ";".join(map(str, legitimate_pages)),
            "repair_layer": source["repair_layer"],
            "requires_ocr_for_repair": source["requires_ocr_for_repair"],
            "requires_extraction_for_repair": source["requires_extraction_for_repair"],
            "requires_reconstruction": source["requires_reconstruction"],
            "requires_artifact_repromotion": source["requires_artifact_repromotion"],
            "requires_index_refresh": source["requires_index_refresh"],
            "requires_g10_revalidation": source["requires_g10_revalidation"],
            "requires_human_rereview": source["requires_human_rereview"],
            "scope_confidence": source["scope_confidence"],
        })
    if len(result) != 245 or sum(int(row["confirmed_defective_page_count"]) for row in result) != 3031:
        raise GateError("FINAL_REPAIR_TARGET_AGGREGATION_MISMATCH")
    return result


def make_report(result: dict[str, Any], decision_rows: list[dict[str, str]]) -> str:
    decision_lines = []
    for row in decision_rows:
        decision_lines.append(
            f"- `{row['paper_id']}` p.{row['source_page']}: `{row['source_visual_classification']}` — {row['reviewer_comment']}"
        )
    return "\n".join([
        "# G11 Marker-Only Final Visual Scope Approval",
        "",
        "## 1. Human decisions",
        "",
        *decision_lines,
        "",
        "These three classifications were explicitly supplied by the user. Codex only transcribed and validated them; no independent visual judgment or automated visual classification was performed.",
        "",
        "## 2. Final page closure",
        "",
        "- Preexisting confirmed defective pages: `3030`.",
        "- User-confirmed substantive page: `CUMCM-2007-B-006` p.41, classified as `CONFIRMED_DEFECTIVE`.",
        "- User-confirmed legitimate noncontent pages: `CUMCM-2007-A-003` p.19 and `CUMCM-2007-B-011` p.2.",
        "- Final accounting: `3031` confirmed defective + `2` confirmed legitimate noncontent + `0` unresolved = `3033` marker-only pages.",
        "- The defective count is `3031`, not `3033`, because the two legitimate noncontent pages are excluded from repair scope.",
        "",
        "## 3. Identity-level scope",
        "",
        "The final marker-only repair identity set remains `245`. The two legitimate pages do not remove `CUMCM-2007-A-003` or `CUMCM-2007-B-011` because each identity also has other confirmed defective marker-only pages; `CUMCM-2007-B-006` also remains defective through p.41 and its other pages. The final identity aggregation is `245` defective identities, `2` mixed page-class identities, `0` legitimate-only identities, and `0` unresolved identities.",
        "",
        "The complete marker-only scope is frozen. `CUMCM-2020-D-003` remains a separate `Q3_OCR_PAGE` repair target; it does not overlap the 245 marker-only identities, so the total G11 repair target population is `246` identities.",
        "",
        "## 4. Gate status",
        "",
        "G11 remains `PARTIAL`: scope approval is complete, but formal repair and post-repair human rereview have not been executed. G12 is not run.",
        "",
        "Next: `G8-TARGETED-MULTI-ROUTE-FORMAL-ARTIFACT-REPAIR`.",
        "",
        "## Outputs",
        "",
        f"- `{relative(DECISIONS)}`",
        f"- `{relative(FINAL_SCOPE_MANIFEST)}`",
        f"- `{relative(FINAL_REPAIR_TARGETS)}`",
        f"- `{relative(APPROVAL_RESULT)}`",
        "",
    ])


def main() -> int:
    branch, head = read_repo_ref()
    if branch != EXPECTED_BRANCH or head != EXPECTED_HEAD:
        raise GateError("FINAL_VISUAL_APPROVAL_REPO_DRIFT")

    contract = read_json(STATUS_CONTRACT)
    validate_contract(contract)
    final_review_result = read_json(FINAL_REVIEW_RESULT)
    if final_review_result.get("PREPARATION_STATUS") != "PASS" or final_review_result.get("MANUAL_VISUAL_REVIEW_STATUS") != "PENDING":
        raise GateError("FINAL_VISUAL_REVIEW_PREPARATION_STATE_DRIFT")

    residual = read_csv(FINAL_RESIDUAL_INPUT)
    image_diagnostic = read_csv(IMAGE_DIAGNOSTIC)
    image_targets = read_csv(IMAGE_TARGETS)
    major_deep = read_csv(MAJOR_DEEP)
    page_deep = read_csv(PAGE_DEEP)
    diagnostic_result = read_json(IMAGE_DIAGNOSTIC_RESULT)
    if len(residual) != 3 or [page_key(row) for row in residual] != EXPECTED_KEYS:
        raise GateError("FINAL_RESIDUAL_INPUT_DRIFT")
    if len(image_diagnostic) != 2951 or len(page_deep) != 3033:
        raise GateError("UPSTREAM_PAGE_EVIDENCE_COUNT_DRIFT")
    if diagnostic_result.get("FINAL_CONFIRMED_DEFECTIVE_PAGE_COUNT") != 3030 or diagnostic_result.get("CONFIRMED_MARKER_ONLY_REPAIR_TARGET_COUNT") != 245:
        raise GateError("UPSTREAM_DIAGNOSTIC_RESULT_DRIFT")

    decision_rows_before = read_csv(DECISIONS)
    decision_fields, decision_sha_before = validate_decisions_before(decision_rows_before)
    decision_rows_after, modification_counts = apply_user_decisions(decision_rows_before, decision_fields)

    manifest_rows, page_status_rows, target_ids, evidence = load_page_evidence(
        residual,
        image_diagnostic,
        image_targets,
        major_deep,
        decision_rows_after,
    )
    final_targets = build_final_targets(image_targets, evidence["page_classes"])

    q3_overlap = int(Q3_TARGET in target_ids)
    total_targets = len(target_ids | {Q3_TARGET})
    if q3_overlap != 0 or total_targets != 246:
        raise GateError(f"G11_REPAIR_TARGET_UNION_MISMATCH=overlap:{q3_overlap},total:{total_targets}")

    protected = [
        FINAL_REVIEW_RESULT,
        FINAL_RESIDUAL_INPUT,
        IMAGE_DIAGNOSTIC,
        IMAGE_DIAGNOSTIC_RESULT,
        IMAGE_TARGETS,
        STATUS_CONTRACT,
        PAGE_DEEP,
        MAJOR_DEEP,
        PRIOR_TARGETED_DECISIONS,
        PRIOR_TARGETED_APPROVAL,
        REVIEW_GUIDE,
        DIAGNOSTIC_REPORT,
    ] + FORMAL_BASELINE_FILES + [ROOT / row["source_path"] for row in residual]
    protected_before = file_snapshot(protected)

    write_csv(DECISIONS, decision_fields, decision_rows_after)
    write_csv(FINAL_SCOPE_MANIFEST, MANIFEST_FIELDS, manifest_rows)
    write_csv(FINAL_REPAIR_TARGETS, TARGET_FIELDS, final_targets)
    decision_sha_after = sha256(DECISIONS)
    if decision_sha_after == decision_sha_before:
        raise GateError("DECISION_SHEET_HASH_DID_NOT_CHANGE")

    protected_after = file_snapshot(protected)
    protected_unchanged = protected_before == protected_after
    if not protected_unchanged:
        raise GateError("PROTECTED_INPUT_MODIFIED")

    manifest_check = read_csv(FINAL_SCOPE_MANIFEST)
    target_check = read_csv(FINAL_REPAIR_TARGETS)
    decisions_check = read_csv(DECISIONS)
    if len(manifest_check) != 3033 or len(target_check) != 245 or len(decisions_check) != 3:
        raise GateError("FINAL_OUTPUT_ROW_COUNT_FAILURE")
    if any(row["final_scope_status"] not in {"CONFIRMED_DEFECTIVE", "CONFIRMED_LEGITIMATE_NONCONTENT"} for row in manifest_check):
        raise GateError("FINAL_SCOPE_MANIFEST_UNRESOLVED_ROW")
    if any(row["review_status"] != "REVIEWED" for row in decisions_check):
        raise GateError("FINAL_DECISION_REVIEW_STATUS_FAILURE")
    if any(row["source_visual_classification"] not in {"SUBSTANTIVE_CONTENT", "LEGITIMATE_NONCONTENT"} for row in decisions_check):
        raise GateError("FINAL_DECISION_CLASSIFICATION_FAILURE")

    defective_ids = {row["paper_id"] for row in manifest_check if row["final_scope_status"] == "CONFIRMED_DEFECTIVE"}
    legitimate_ids = {row["paper_id"] for row in manifest_check if row["final_scope_status"] == "CONFIRMED_LEGITIMATE_NONCONTENT"}
    mixed_ids = {identity for identity in legitimate_ids if identity in defective_ids}
    legitimate_only_ids = legitimate_ids - defective_ids
    unresolved_ids = {row["paper_id"] for row in manifest_check if row["final_scope_status"] not in {"CONFIRMED_DEFECTIVE", "CONFIRMED_LEGITIMATE_NONCONTENT"}}
    if defective_ids != target_ids or len(mixed_ids) != 2 or legitimate_only_ids or unresolved_ids:
        raise GateError("FINAL_IDENTITY_SCOPE_AGGREGATION_FAILURE")

    approval_attempt = "g11-marker-only-final-visual-scope-approval-" + head[:16].lower()
    approval_result: dict[str, Any] = {
        "STAGE": "G11-MARKER-ONLY-FINAL-VISUAL-SCOPE-APPROVAL",
        "STATUS": "PASS",
        "BRANCH": branch,
        "HEAD": head,
        "FINAL_VISUAL_APPROVAL_ATTEMPT_ID": approval_attempt,
        "SOURCE_FINAL_VISUAL_REVIEW_ATTEMPT_ID": "g11-marker-only-final-visual-scope-review-" + head[:16].lower(),
        "SOURCE_FINAL_VISUAL_REVIEW_RESULT": relative(FINAL_REVIEW_RESULT),
        "MANUAL_DECISION_SOURCE": "USER_EXPLICIT_HUMAN_VISUAL_REVIEW",
        "CODEX_INDEPENDENT_VISUAL_JUDGMENT": 0,
        "AUTOMATED_VISUAL_CLASSIFICATION_RUN": 0,
        "FINAL_VISUAL_DECISION_ROW_COUNT_BEFORE": len(decision_rows_before),
        "FINAL_VISUAL_DECISION_ROW_COUNT_AFTER": len(decisions_check),
        "FINAL_VISUAL_UNIQUE_PAPER_PAGE_COUNT_BEFORE": len({page_key(row) for row in decision_rows_before}),
        "FINAL_VISUAL_UNIQUE_PAPER_PAGE_COUNT_AFTER": len({page_key(row) for row in decisions_check}),
        "FINAL_VISUAL_PENDING_COUNT_BEFORE": sum(row["review_status"] == "PENDING" for row in decision_rows_before),
        "FINAL_VISUAL_PENDING_COUNT_AFTER": sum(row["review_status"] == "PENDING" for row in decisions_check),
        "FINAL_VISUAL_REVIEWED_COUNT": sum(row["review_status"] == "REVIEWED" for row in decisions_check),
        "FINAL_VISUAL_SUBSTANTIVE_COUNT": sum(row["source_visual_classification"] == "SUBSTANTIVE_CONTENT" for row in decisions_check),
        "FINAL_VISUAL_LEGITIMATE_NONCONTENT_COUNT": sum(row["source_visual_classification"] == "LEGITIMATE_NONCONTENT" for row in decisions_check),
        "FINAL_VISUAL_UNCLEAR_COUNT": sum(row["source_visual_classification"] == "UNCLEAR" for row in decisions_check),
        "SOURCE_VISUAL_CLASSIFICATION_MODIFICATION_COUNT": modification_counts["source_visual_classification"],
        "REVIEWER_COMMENT_MODIFICATION_COUNT": modification_counts["reviewer_comment"],
        "REVIEW_STATUS_MODIFICATION_COUNT": modification_counts["review_status"],
        "OTHER_COLUMN_MODIFICATION_COUNT": modification_counts["other"],
        "FINAL_VISUAL_DECISION_SHEET_SHA256_BEFORE": decision_sha_before,
        "FINAL_VISUAL_DECISION_SHEET_SHA256_AFTER": decision_sha_after,
        "HASH_CHANGE_EXPLAINED_BY_AUTHORIZED_FIELDS_ONLY": 1,
        "PREEXISTING_CONFIRMED_DEFECTIVE_PAGE_COUNT": 3030,
        "NEWLY_CONFIRMED_DEFECTIVE_BY_FINAL_VISUAL_PAGE_COUNT": 1,
        "NEWLY_CONFIRMED_LEGITIMATE_NONCONTENT_BY_FINAL_VISUAL_PAGE_COUNT": 2,
        "FINAL_CONFIRMED_DEFECTIVE_PAGE_COUNT": evidence["counts"]["defective_pages"],
        "FINAL_CONFIRMED_LEGITIMATE_NONCONTENT_PAGE_COUNT": evidence["counts"]["legitimate_pages"],
        "FINAL_UNRESOLVED_MARKER_ONLY_PAGE_COUNT": evidence["counts"]["unresolved_pages"],
        "FINAL_MARKER_ONLY_PAGE_ACCOUNTING_PASS": int(evidence["counts"] == {"defective_pages": 3031, "legitimate_pages": 2, "unresolved_pages": 0}),
        "FINAL_CONFIRMED_DEFECTIVE_IDENTITY_COUNT": len(defective_ids),
        "FINAL_LEGITIMATE_ONLY_IDENTITY_COUNT": len(legitimate_only_ids),
        "FINAL_MIXED_PAGE_CLASS_IDENTITY_COUNT": len(mixed_ids),
        "FINAL_UNRESOLVED_IDENTITY_COUNT": len(unresolved_ids),
        "FINAL_CONFIRMED_MARKER_ONLY_REPAIR_TARGET_COUNT": len(target_ids),
        "MARKER_ONLY_REPAIR_TARGET_IDENTITY_SET_MODIFICATION_COUNT": 0,
        "FINAL_SCOPE_MANIFEST_ROW_COUNT": len(manifest_check),
        "FINAL_SCOPE_MANIFEST_UNRESOLVED_COUNT": sum(row["final_scope_status"] not in {"CONFIRMED_DEFECTIVE", "CONFIRMED_LEGITIMATE_NONCONTENT"} for row in manifest_check),
        "FULL_MARKER_ONLY_REPAIR_SCOPE_FROZEN": 1,
        "MARKER_ONLY_TOTAL_PAGE_COUNT": 3033,
        "MARKER_ONLY_CONFIRMED_DEFECTIVE_PAGE_COUNT": 3031,
        "MARKER_ONLY_LEGITIMATE_NONCONTENT_PAGE_COUNT": 2,
        "MARKER_ONLY_REPAIR_TARGET_IDENTITY_COUNT": 245,
        "CUMCM_2020_D_003_REPAIR_TARGET": 1,
        "CUMCM_2020_D_003_REPAIR_LAYER": "Q3_OCR_PAGE",
        "Q3_TARGET_OVERLAP_WITH_MARKER_ONLY_TARGETS": q3_overlap,
        "TOTAL_G11_REPAIR_TARGET_COUNT": total_targets,
        "MANUAL_VISUAL_REVIEW_STATUS": "PASS",
        "MARKER_ONLY_SCOPE_STATUS": "PASS",
        "G11_STATUS_REMAINS": "PARTIAL",
        "G11_ORIGINAL_DECISION_MODIFICATION_COUNT": 0,
        "TARGETED_VISUAL_DECISION_MODIFICATION_COUNT": 0,
        "FORMAL_DATA_MODIFICATION_COUNT": 0,
        "FORMAL_ARTIFACT_CONTENT_MODIFICATION_COUNT": 0,
        "FORMAL_ARTIFACTS_MODIFIED": 0,
        "FORMAL_INDEX_MODIFICATION_COUNT": 0,
        "IDENTITY_MODIFICATION_COUNT": 0,
        "MEMBERSHIP_MODIFICATION_COUNT": 0,
        "FORMAL_ELIGIBILITY_MODIFIED": 0,
        "BACKLOG_MODIFICATION_COUNT": 0,
        "ORIGINAL_FILES_MODIFIED": 0,
        "OCR_RUN": 0,
        "DIAGNOSTIC_OCR_RUN": 0,
        "Q3_OCR_RUN": 0,
        "PDF_RENDER_RUN": 0,
        "TARGETED_RENDER_RUN": 0,
        "PDFTOTEXT_PAGE_PROBE_RUN": 0,
        "PDF_INSPECTOR_EXTRACTION_RUN": 0,
        "FORMAL_EXTRACTION_RUN": 0,
        "BODY_RECONSTRUCTION_RUN": 0,
        "ARTIFACT_REGENERATION_RUN": 0,
        "ARTIFACT_REPROMOTION_RUN": 0,
        "G9_REBUILD_RUN": 0,
        "G10_REBUILD_RUN": 0,
        "G12_RUN": 0,
        "DOC_BATCH_RUN": 0,
        "Q3_REPAIR_RUN": 0,
        "IMAGE_OCR_RUN": 0,
        "IMAGE_EXTRACTION_RERUN": 0,
        "NETWORK_ACCESS_USED": 0,
        "DOWNLOAD_RUN": 0,
        "NEW_DEPENDENCY_INSTALLED": 0,
        "WORD_RUN": 0,
        "WORD_COM_RUN": 0,
        "DOC_CONVERSION_RUN": 0,
        "PRINT_JOB_RUN": 0,
        "GIT_OPERATIONS": 0,
        "PROTECTED_INPUTS_UNCHANGED": int(protected_unchanged),
        "OUTPUTS": [
            relative(DECISIONS),
            relative(FINAL_SCOPE_MANIFEST),
            relative(FINAL_REPAIR_TARGETS),
            relative(APPROVAL_RESULT),
            relative(APPROVAL_REPORT),
        ],
        "VALIDATION": [
            "Three explicit user classifications were transcribed with exactly three authorized fields changed per row.",
            "All three decision bindings, source paths, source hashes, render paths, and render hashes remained unchanged.",
            "The final manifest contains 3,033 unique marker-only pages with no unresolved status.",
            "The final repair target manifest contains 245 identities and 3,031 confirmed defective pages.",
            "The two legitimate pages belong to identities that retain other confirmed defective pages; the identity set remains unchanged.",
            "CUMCM-2020-D-003 remains a separate non-overlapping Q3 repair target, giving a 246-identity G11 union.",
            "No OCR, rendering, extraction, repair, artifact regeneration, index rebuild, network, dependency, Word, or Git command was run.",
            "Protected upstream, formal baseline, source, and prior review files remained unchanged.",
        ],
        "ISSUES": [
            "Formal multi-route repair and post-repair human rereview remain pending; G11 therefore remains PARTIAL."
        ],
        "BLOCKER": "NONE",
        "NEXT": "G8-TARGETED-MULTI-ROUTE-FORMAL-ARTIFACT-REPAIR",
        "COMPLETED_AT": datetime.now(STAMP).isoformat(timespec="seconds"),
    }
    write_json(APPROVAL_RESULT, approval_result)
    write_text(APPROVAL_REPORT, make_report(approval_result, decisions_check))
    print(json.dumps(approval_result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GateError as exc:
        print(f"GATE_ERROR={exc}")
        raise SystemExit(2)
