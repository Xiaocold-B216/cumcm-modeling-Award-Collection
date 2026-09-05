"""Prepare the final three-page G11 marker-only visual review packet.

This stage is preparation-only.  It validates the already-produced render
bindings, copies those existing PNGs into an isolated review packet, and
creates a PENDING decision sheet.  It deliberately does not render, OCR,
open a document, modify formal data, or make a visual classification.
"""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SCALE = ROOT / "catalog" / "scale"
REPORTS = ROOT / "reports" / "scale"

EXPECTED_BRANCH = "library-refactor-v1"
EXPECTED_HEAD = "557724fba6572d4d83dc421feda5b17b13ff8d66"
EXPECTED_KEYS = [
    ("CUMCM-2007-A-003", 19),
    ("CUMCM-2007-B-006", 41),
    ("CUMCM-2007-B-011", 2),
]

RESIDUAL_INPUT = SCALE / "g11_marker_only_final_visual_residual_input.csv"
DIAGNOSTIC = SCALE / "g11_marker_only_image_residual_scope_diagnostic.csv"
DIAGNOSTIC_RESULT = SCALE / "g11_marker_only_image_residual_scope_diagnostic_result.json"
CONFIRMED_TARGETS = SCALE / "g11_marker_only_image_confirmed_repair_targets.csv"
PRIOR_TARGETED_DECISIONS = SCALE / "g11_targeted_visual_diagnostic_decisions.csv"
PRIOR_TARGETED_APPROVAL = SCALE / "g11_targeted_visual_diagnostic_approval_result.json"
PRIOR_PAGE_DEEP = SCALE / "g11_marker_only_page_deep_diagnostic.csv"
PRIOR_MAJOR_DEEP = SCALE / "g11_major_defect_deep_diagnostic.csv"

DECISIONS = SCALE / "g11_marker_only_final_visual_scope_decisions.csv"
RESULT = SCALE / "g11_marker_only_final_visual_scope_review_result.json"
GUIDE = REPORTS / "G11_MARKER_ONLY_FINAL_VISUAL_SCOPE_REVIEW_GUIDE.md"
REPORT = REPORTS / "G11_MARKER_ONLY_FINAL_VISUAL_SCOPE_REVIEW.md"
PACKET = REPORTS / "g11_marker_only_final_visual_scope_review"

PROTECTED_FORMAL_FILES = [
    SCALE / "g8_artifact_manifest.csv",
    SCALE / "g8_paper_status.csv",
    SCALE / "g8_manual_backlog.csv",
    SCALE / "g8_q3_manual_backlog.csv",
    SCALE / "g9_paper_index.csv",
    SCALE / "g10_consistency_result.json",
]

STAMP = timezone(timedelta(hours=8))
DECISION_FIELDS = [
    "paper_id",
    "source_page",
    "source_path",
    "source_sha256",
    "render_path",
    "render_sha256",
    "prior_diagnostic_class",
    "source_visual_classification",
    "reviewer_comment",
    "review_status",
]


class GateError(RuntimeError):
    """Raised when an input or output gate fails."""


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


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)


def validate_inputs() -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, Any], set[str], dict[str, str]]:
    residual = read_csv(RESIDUAL_INPUT)
    diagnostic = read_csv(DIAGNOSTIC)
    previous_result = read_json(DIAGNOSTIC_RESULT)
    targets = read_csv(CONFIRMED_TARGETS)

    residual_keys = [page_key(row) for row in residual]
    if residual_keys != EXPECTED_KEYS:
        raise GateError(f"FINAL_RESIDUAL_KEYS_MISMATCH={residual_keys}")
    if len(set(residual_keys)) != 3 or len(residual) != 3:
        raise GateError("FINAL_RESIDUAL_INPUT_NOT_EXACTLY_THREE_UNIQUE_PAGES")

    diagnostic_by_key = {page_key(row): row for row in diagnostic}
    if len(diagnostic_by_key) != len(diagnostic):
        raise GateError("DIAGNOSTIC_DUPLICATE_PAGE_KEYS")
    if any(key not in diagnostic_by_key for key in EXPECTED_KEYS):
        raise GateError("FINAL_RESIDUAL_PAGE_MISSING_FROM_DIAGNOSTIC")

    render_binding: dict[str, str] = {}
    for item in residual:
        key = page_key(item)
        prior = diagnostic_by_key[key]
        for field in ("source_path", "source_sha256", "render_path", "render_sha256"):
            if item.get(field, "").upper() != prior.get(field, "").upper():
                raise GateError(f"RESIDUAL_DIAGNOSTIC_BINDING_DRIFT={key}:{field}")
        if prior.get("diagnostic_class") != "OCR_NON_SUBSTANTIVE_OR_EMPTY":
            raise GateError(f"UNEXPECTED_PRIOR_DIAGNOSTIC_CLASS={key}")
        if prior.get("new_scope_status") != "UNRESOLVED":
            raise GateError(f"FINAL_PAGE_NOT_UNRESOLVED={key}")
        if prior.get("requires_manual_visual_review") != "1":
            raise GateError(f"FINAL_PAGE_MANUAL_REVIEW_FLAG_MISSING={key}")

        source = ROOT / item["source_path"]
        render = ROOT / item["render_path"]
        if not source.is_file():
            raise GateError(f"SOURCE_MISSING={source}")
        if not render.is_file() or render.stat().st_size <= 0:
            raise GateError(f"RENDER_MISSING_OR_EMPTY={render}")
        actual_source_sha = sha256(source)
        actual_render_sha = sha256(render)
        if actual_source_sha != item["source_sha256"].upper():
            raise GateError(f"SOURCE_SHA_MISMATCH={key}")
        if actual_render_sha != item["render_sha256"].upper():
            raise GateError(f"RENDER_SHA_MISMATCH={key}")

        expected_render_name = f"source_page_{key[1]}.png"
        if render.name != expected_render_name or render.parent.name != key[0]:
            raise GateError(f"RENDER_PAGE_ID_BINDING_MISMATCH={key}")
        render_binding[f"{key[0]}:p{key[1]}"] = actual_render_sha

    if previous_result.get("FINAL_RESIDUAL_UNRESOLVED_PAGE_COUNT") != 3:
        raise GateError("PRIOR_RESIDUAL_PAGE_COUNT_DRIFT")
    if previous_result.get("FINAL_CONFIRMED_DEFECTIVE_PAGE_COUNT") != 3030:
        raise GateError("PRIOR_CONFIRMED_DEFECTIVE_PAGE_COUNT_DRIFT")
    if previous_result.get("CONFIRMED_MARKER_ONLY_REPAIR_TARGET_COUNT") != 245:
        raise GateError("PRIOR_REPAIR_TARGET_COUNT_DRIFT")
    if previous_result.get("BRANCH") != EXPECTED_BRANCH or previous_result.get("HEAD") != EXPECTED_HEAD:
        raise GateError("PRIOR_BASELINE_REPOSITORY_METADATA_DRIFT")

    target_ids = [str(row.get("paper_id", "")) for row in targets]
    if len(target_ids) != 245 or len(set(target_ids)) != 245:
        raise GateError("REPAIR_TARGET_IDENTITY_SET_COUNT_DRIFT")
    target_set_sha = hashlib.sha256(
        ("\n".join(sorted(target_ids)) + "\n").encode("utf-8")
    ).hexdigest().upper()
    return residual, diagnostic, previous_result, set(target_ids), {
        "target_set_sha256": target_set_sha,
        "render_binding": json.dumps(render_binding, sort_keys=True),
    }


def build_decisions(residual: list[dict[str, str]], diagnostic: list[dict[str, str]]) -> list[dict[str, str]]:
    diagnostic_by_key = {page_key(row): row for row in diagnostic}
    rows: list[dict[str, str]] = []
    for item in residual:
        prior = diagnostic_by_key[page_key(item)]
        rows.append({
            "paper_id": item["paper_id"],
            "source_page": item["source_page"],
            "source_path": item["source_path"],
            "source_sha256": item["source_sha256"].upper(),
            "render_path": item["render_path"],
            "render_sha256": item["render_sha256"].upper(),
            "prior_diagnostic_class": prior["diagnostic_class"],
            "source_visual_classification": "PENDING",
            "reviewer_comment": "",
            "review_status": "PENDING",
        })
    return rows


def make_review_packet(residual: list[dict[str, str]]) -> list[str]:
    PACKET.mkdir(parents=True, exist_ok=True)
    output_paths: list[str] = []
    opened: list[tuple[dict[str, str], Image.Image]] = []
    try:
        for index, item in enumerate(residual, start=1):
            source = ROOT / item["render_path"]
            output = PACKET / f"{index:02d}_{item['paper_id']}_p{item['source_page']}.png"
            shutil.copy2(source, output)
            output_paths.append(relative(output))
            image = Image.open(output).convert("RGB")
            opened.append((item, image))

        cell_width, cell_height = 440, 600
        canvas = Image.new("RGB", (cell_width * len(opened), cell_height), "white")
        draw = ImageDraw.Draw(canvas)
        font = ImageFont.load_default()
        for index, (item, image) in enumerate(opened):
            image.thumbnail((cell_width - 20, cell_height - 55), Image.Resampling.LANCZOS)
            left = index * cell_width + (cell_width - image.width) // 2
            top = 42 + (cell_height - 55 - image.height) // 2
            canvas.paste(image, (left, top))
            draw.text(
                (index * cell_width + 10, 12),
                f"{item['paper_id']} p.{item['source_page']}",
                fill="black",
                font=font,
            )
        contact = PACKET / "contact_sheet.png"
        canvas.save(contact, format="PNG")
        output_paths.append(relative(contact))
    finally:
        for _, image in opened:
            image.close()
    return output_paths


def write_guide() -> None:
    write_text(
        GUIDE,
        """# G11 Marker-Only Final Visual Scope Review Guide

This is a human review gate for exactly three rendered source pages. Check
only the three PNGs in the review packet and then fill the corresponding rows
in `catalog/scale/g11_marker_only_final_visual_scope_decisions.csv`.

Use exactly one classification per page:

- `SUBSTANTIVE_CONTENT`: the image contains substantive paper content,
  including a title, formula, table, figure, caption, reference, appendix, or
  data.
- `LEGITIMATE_NONCONTENT`: the image contains only blank space, a watermark,
  QR code, advertisement, divider, or other non-paper material.
- `UNCLEAR`: the page cannot be determined reliably from the image.

Do not infer a classification from the prior OCR diagnostic class. The
initial `source_visual_classification` and `review_status` values are
intentionally `PENDING`; no Codex visual classification has been made.
""",
    )


def build_result(
    previous_result: dict[str, Any],
    residual: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    packet_outputs: list[str],
    target_set_sha: str,
    protected_unchanged: bool,
    formal_unchanged: bool,
) -> dict[str, Any]:
    now = datetime.now(STAMP).isoformat(timespec="seconds")
    result: dict[str, Any] = {
        "STAGE": "G11-MARKER-ONLY-FINAL-VISUAL-SCOPE-REVIEW",
        "STATUS": "PARTIAL",
        "PREPARATION_STATUS": "PASS",
        "MANUAL_VISUAL_REVIEW_STATUS": "PENDING",
        "WORD_COM_PILOT_STARTED": 0,
        "WORD_COM_INSTANCE_CREATED": 0,
        "DOC_OPENED": 0,
        "DOC_CONVERSION_ATTEMPTED": 0,
        "FINAL_VISUAL_PENDING_COUNT": 3,
        "FINAL_VISUAL_SUBSTANTIVE_COUNT": 0,
        "FINAL_VISUAL_LEGITIMATE_NONCONTENT_COUNT": 0,
        "FINAL_VISUAL_UNCLEAR_COUNT": 0,
        "MANUAL_DECISION_SOURCE": "PENDING_USER_VISUAL_REVIEW",
        "CODEX_INDEPENDENT_VISUAL_JUDGMENT": 0,
        "PREEXISTING_CONFIRMED_DEFECTIVE_PAGE_COUNT": 3030,
        "CONFIRMED_MARKER_ONLY_REPAIR_TARGET_COUNT": 245,
        "FINAL_VISUAL_RENDER_BINDING_PASS_COUNT": 3,
        "FINAL_VISUAL_DECISION_ROW_COUNT": len(decision_rows),
        "FINAL_VISUAL_RESIDUAL_ROW_COUNT": len(residual),
        "FINAL_VISUAL_RESIDUAL_UNIQUE_PAPER_PAGE_COUNT": len({page_key(row) for row in residual}),
        "MARKER_ONLY_REPAIR_TARGET_IDENTITY_SET_MODIFICATION_COUNT": 0,
        "REPAIR_TARGET_IDENTITY_SET_SHA256": target_set_sha,
        "G11_STATUS_REMAINS": "PARTIAL",
        "SOURCE_SHA_MISMATCH": 0,
        "ORIGINAL_FILES_MODIFIED": int(not protected_unchanged),
        "FORMAL_ARTIFACTS_MODIFIED": int(not formal_unchanged),
        "FORMAL_ELIGIBILITY_MODIFIED": 0,
        "DOC_BATCH_RUN": 0,
        "Q3_REPAIR_RUN": 0,
        "Q3_OCR_RUN": 0,
        "IMAGE_OCR_RUN": 0,
        "IMAGE_EXTRACTION_RERUN": 0,
        "OCR_RUN": 0,
        "DIAGNOSTIC_OCR_RUN": 0,
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
        "REVIEW_PACKET_GENERATION_RUN": 1,
        "REVIEW_PACKET_REGENERATION_RUN": 0,
        "NETWORK_ACCESS_USED": 0,
        "DOWNLOAD_RUN": 0,
        "NEW_DEPENDENCY_INSTALLED": 0,
        "WORD_RUN": 0,
        "WORD_COM_RUN": 0,
        "DOC_CONVERSION_RUN": 0,
        "PRINT_JOB_RUN": 0,
        "GIT_OPERATIONS": 0,
        "PREVIOUS_ARTIFACT_SETS": 308,
        "PREVIOUS_PRIMARY_ARTIFACTS": 924,
        "DOC_MANUAL_BACKLOG": 18,
        "Q3_MANUAL_BACKLOG": 128,
        "CURRENT_ARTIFACT_SETS": 453,
        "CURRENT_PRIMARY_ARTIFACTS": 1359,
        "CURRENT_DOC_MANUAL_BACKLOG": 0,
        "CURRENT_Q3_MANUAL_BACKLOG": 0,
        "CURRENT_TOTAL_ELIGIBLE_BACKLOG": 0,
        "PRIOR_IMAGE_DIAGNOSTIC_ATTEMPT_ID": previous_result.get("IMAGE_RESIDUAL_DIAGNOSTIC_ATTEMPT_ID"),
        "PRIOR_DIAGNOSTIC_CLASS": "OCR_NON_SUBSTANTIVE_OR_EMPTY",
        "RENDER_BINDING_MODE": "EXISTING_RENDER_COPY_ONLY",
        "PROTECTED_INPUTS_UNCHANGED": int(protected_unchanged),
        "FORMAL_BASELINE_FILES_UNCHANGED": int(formal_unchanged),
        "OUTPUTS": [
            relative(DECISIONS),
            relative(RESULT),
            relative(GUIDE),
            *packet_outputs,
            relative(REPORT),
        ],
        "VALIDATION": [
            "The final residual input contains exactly the three expected unique paper-page keys.",
            "All three source files exist and their SHA256 values match the frozen residual diagnostic bindings.",
            "All three existing render files exist, are non-empty, and their SHA256 values match the diagnostic CSV.",
            "The review packet copies existing render evidence; no PDF render or OCR command was run.",
            "The decision sheet has exactly three rows, all PENDING with empty reviewer comments.",
            "The 245-identity marker-only repair target set remained unchanged.",
            "Protected source, diagnostic, decision, approval, deep-evidence, and formal baseline files remained unchanged.",
            "No Codex independent visual classification was made.",
        ],
        "ISSUES": [
            "Three pages remain pending and require human visual classification before final scope approval."
        ],
        "BLOCKER": "FINAL_3_PAGE_HUMAN_REVIEW_REQUIRED",
        "NEXT": "G11-MARKER-ONLY-FINAL-VISUAL-SCOPE-APPROVAL",
        "COMPLETED_AT": now,
    }
    return result


def write_report(result: dict[str, Any], decision_rows: list[dict[str, str]], packet_outputs: list[str]) -> None:
    lines = [
        "# G11 Marker-Only Final Visual Scope Review",
        "",
        "- Stage status: `PARTIAL`",
        "- Preparation status: `PASS`",
        "- Manual visual review status: `PENDING`",
        "- Pending pages: `3`",
        "",
        "## Review scope",
        "",
        "Only the following three existing render evidences are in scope:",
        "",
    ]
    for row in decision_rows:
        lines.append(f"- `{row['paper_id']}` source page `{row['source_page']}`")
    lines.extend([
        "",
        "The packet is evidence-only. It contains no classification conclusion.",
        "The user must classify each page as `SUBSTANTIVE_CONTENT`, `LEGITIMATE_NONCONTENT`, or `UNCLEAR` and add a reviewer comment.",
        "",
        "## Outputs",
        "",
        f"- Decision sheet: `{relative(DECISIONS)}`",
        f"- Guide: `{relative(GUIDE)}`",
        *[f"- Packet item: `{item}`" for item in packet_outputs],
        "",
        "## Gate",
        "",
        "`FINAL_3_PAGE_HUMAN_REVIEW_REQUIRED`",
        "",
        "## Next",
        "",
        "`G11-MARKER-ONLY-FINAL-VISUAL-SCOPE-APPROVAL`",
        "",
    ])
    write_text(REPORT, "\n".join(lines))


def main() -> int:
    residual, diagnostic, previous_result, target_ids, binding_meta = validate_inputs()

    protected_paths = [
        RESIDUAL_INPUT,
        DIAGNOSTIC,
        DIAGNOSTIC_RESULT,
        CONFIRMED_TARGETS,
        PRIOR_TARGETED_DECISIONS,
        PRIOR_TARGETED_APPROVAL,
        PRIOR_PAGE_DEEP,
        PRIOR_MAJOR_DEEP,
    ] + [ROOT / row["source_path"] for row in residual]
    protected_paths.extend(PROTECTED_FORMAL_FILES)
    protected_before = file_snapshot(protected_paths)

    decision_rows = build_decisions(residual, diagnostic)
    write_csv(DECISIONS, DECISION_FIELDS, decision_rows)
    packet_outputs = make_review_packet(residual)
    write_guide()

    protected_after = file_snapshot(protected_paths)
    protected_unchanged = protected_before == protected_after
    formal_paths = [path for path in PROTECTED_FORMAL_FILES]
    formal_unchanged = file_snapshot(formal_paths) == {
        str(path): protected_before[str(path)] for path in formal_paths
    }
    if not protected_unchanged:
        raise GateError("PROTECTED_INPUT_MODIFIED")

    if len(decision_rows) != 3 or any(
        row["source_visual_classification"] != "PENDING"
        or row["reviewer_comment"] != ""
        or row["review_status"] != "PENDING"
        for row in decision_rows
    ):
        raise GateError("DECISION_SHEET_NOT_INITIAL_PENDING_STATE")

    result = build_result(
        previous_result,
        residual,
        decision_rows,
        packet_outputs,
        binding_meta["target_set_sha256"],
        protected_unchanged,
        formal_unchanged,
    )
    write_report(result, decision_rows, packet_outputs)
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    with RESULT.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    # The result itself is intentionally written last.  Re-read outputs to
    # make the preparation gate evidence-based before returning.
    if not DECISIONS.is_file() or not GUIDE.is_file() or not REPORT.is_file():
        raise GateError("REVIEW_PREPARATION_OUTPUT_MISSING")
    expected_packet = {
        PACKET / f"{index:02d}_{paper_id}_p{page}.png"
        for index, (paper_id, page) in enumerate(EXPECTED_KEYS, start=1)
    } | {PACKET / "contact_sheet.png"}
    if set(PACKET.iterdir()) != expected_packet:
        raise GateError("REVIEW_PACKET_FILENAMES_NOT_EXACT")
    if any(path.stat().st_size <= 0 for path in expected_packet):
        raise GateError("REVIEW_PACKET_EMPTY_OUTPUT")

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GateError as exc:
        print(f"GATE_ERROR={exc}")
        raise SystemExit(2)
