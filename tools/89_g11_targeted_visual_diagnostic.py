from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SCALE = ROOT / "catalog/scale"
REPORTS = ROOT / "reports/scale"

EXPECTED_BRANCH = "library-refactor-v1"
EXPECTED_HEAD = "557724fba6572d4d83dc421feda5b17b13ff8d66"
EXPECTED_DEEP_ATTEMPT = "g11-major-defect-deep-diagnostic-7a065914b3abca5d"
EXPECTED_SAMPLE_COUNT = 20
MAX_RENDER_PAGES = 60
RENDER_DPI = 180
KNOWN_FORMAL_DEFECT_IDS = {
    "CUMCM-1999-B-003",
    "CUMCM-2008-C-004",
    "CUMCM-1992-A-003",
    "CUMCM-1993-B-001",
    "CUMCM-1996-B-001",
    "CUMCM-1997-A-008",
    "CUMCM-1998-A-007",
    "CUMCM-2000-A-005",
    "CUMCM-2001-A-001",
    "CUMCM-2002-B-005",
}

SAMPLE_PATH = SCALE / "g11_deep_diagnostic_visual_sample.csv"
PAGE_DIAGNOSTIC_PATH = SCALE / "g11_marker_only_page_deep_diagnostic.csv"
IDENTITY_DIAGNOSTIC_PATH = SCALE / "g11_major_defect_deep_diagnostic.csv"
DEEP_RESULT_PATH = SCALE / "g11_major_defect_deep_diagnostic_result.json"
DEEP_REPORT_PATH = REPORTS / "G11_MAJOR_DEFECT_DEEP_DIAGNOSTIC.md"
FORMAL_INDEX_PATH = SCALE / "g9_paper_index.csv"
DECISIONS_PATH = SCALE / "g11_manual_sample_decisions.csv"

OUTPUT_ROOT = REPORTS / "g11_targeted_visual_diagnostic"
CONTACT_ROOT = OUTPUT_ROOT / "contact_sheets"
OUTPUT_DECISIONS = SCALE / "g11_targeted_visual_diagnostic_decisions.csv"
OUTPUT_MANIFEST = SCALE / "g11_targeted_visual_diagnostic_manifest.csv"
OUTPUT_RESULT = SCALE / "g11_targeted_visual_diagnostic_result.json"
OUTPUT_GUIDE = REPORTS / "G11_TARGETED_VISUAL_DIAGNOSTIC_REVIEW_GUIDE.md"

PDFTOPPM = Path(r"D:\texlive\2026\bin\windows\pdftoppm.exe")
MARKER_RE = re.compile(r"<!--\s*source_page:\s*(\d+)\s*-->", re.IGNORECASE)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def path_from_catalog(value: str) -> Path:
    candidate = Path(value.replace("\\", "/"))
    return candidate if candidate.is_absolute() else ROOT / candidate


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def formal_excerpt(body: str, page: int) -> tuple[str, bool]:
    matches = list(MARKER_RE.finditer(body))
    for index, match in enumerate(matches):
        if as_int(match.group(1), -1) != page:
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        return body[match.start() : end], True
    return "", False


def select_pages(pages: list[int]) -> list[int]:
    ordered = sorted(set(pages))
    if len(ordered) <= 3:
        return ordered
    return sorted({ordered[0], ordered[(len(ordered) - 1) // 2], ordered[-1]})


def ensure_inputs() -> None:
    required = [
        SAMPLE_PATH,
        PAGE_DIAGNOSTIC_PATH,
        IDENTITY_DIAGNOSTIC_PATH,
        DEEP_RESULT_PATH,
        DEEP_REPORT_PATH,
        FORMAL_INDEX_PATH,
        DECISIONS_PATH,
    ]
    missing = [rel(path) for path in required if not path.exists()]
    if missing:
        raise RuntimeError("G11_TARGETED_VISUAL_MISSING_INPUT=" + ";".join(missing))
    if not PDFTOPPM.is_file():
        raise RuntimeError("G11_TARGETED_VISUAL_MISSING_POPPLER=" + str(PDFTOPPM))


def validate_sample(
    sample_rows: list[dict[str, str]],
    identity_rows: list[dict[str, str]],
    page_rows: list[dict[str, str]],
    deep_result: dict[str, Any],
) -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]], int]:
    if len(sample_rows) != EXPECTED_SAMPLE_COUNT:
        raise RuntimeError(f"G11_TARGETED_VISUAL_SAMPLE_DRIFT_COUNT={len(sample_rows)}")
    if deep_result.get("DEEP_DIAGNOSTIC_ATTEMPT_ID") != EXPECTED_DEEP_ATTEMPT:
        raise RuntimeError("G11_TARGETED_VISUAL_DEEP_ATTEMPT_DRIFT")
    if deep_result.get("SOURCE_PAGE_MARKER_SEMANTICS") != "PAGE_LOCAL_STRICT_BOUNDARY":
        raise RuntimeError("G11_TARGETED_VISUAL_MARKER_SEMANTICS_DRIFT")
    identity_by_id = {row["paper_id"]: row for row in identity_rows}
    page_by_id: dict[str, dict[str, str]] = {}
    for row in page_rows:
        if row.get("classification") != "STILL_UNRESOLVED":
            continue
        page_by_id.setdefault(row["paper_id"], {})[row["source_page"]] = row
    sample_by_id: dict[str, dict[str, str]] = {}
    sample_orders: list[int] = []
    for row in sample_rows:
        paper_id = row.get("paper_id", "")
        if paper_id in sample_by_id or paper_id not in identity_by_id:
            raise RuntimeError(f"G11_TARGETED_VISUAL_SAMPLE_IDENTITY_DRIFT={paper_id}")
        if identity_by_id[paper_id].get("classification") != "STILL_UNRESOLVED":
            raise RuntimeError(f"G11_TARGETED_VISUAL_SAMPLE_NOT_UNRESOLVED={paper_id}")
        if paper_id in KNOWN_FORMAL_DEFECT_IDS:
            raise RuntimeError(f"G11_TARGETED_VISUAL_SAMPLE_KNOWN_DEFECT={paper_id}")
        expected = identity_by_id[paper_id]
        for field in ("source_path", "source_sha256", "body_sha256"):
            expected_field = "formal_body_sha256" if field == "body_sha256" else field
            if row.get(field, "") != expected.get(expected_field, ""):
                raise RuntimeError(f"G11_TARGETED_VISUAL_SAMPLE_BINDING_DRIFT={paper_id}:{field}")
        pages = page_by_id.get(paper_id, {})
        if not pages:
            raise RuntimeError(f"G11_TARGETED_VISUAL_NO_UNRESOLVED_PAGES={paper_id}")
        sample_by_id[paper_id] = row
        sample_orders.append(as_int(row.get("sample_order"), -1))
    if sample_orders != list(range(1, EXPECTED_SAMPLE_COUNT + 1)):
        raise RuntimeError("G11_TARGETED_VISUAL_SAMPLE_ORDER_DRIFT")
    total = 0
    for paper_id, row in sample_by_id.items():
        available = sorted(as_int(page, -1) for page in page_by_id[paper_id])
        selected = select_pages(available)
        if not selected or not set(selected).issubset(set(available)):
            raise RuntimeError(f"G11_TARGETED_VISUAL_PAGE_SELECTION_INVALID={paper_id}")
        total += len(selected)
    if total <= 0 or total > MAX_RENDER_PAGES:
        raise RuntimeError(f"G11_TARGETED_VISUAL_RENDER_BUDGET_INVALID={total}")
    return sample_by_id, page_by_id, total


def validate_source(path: Path, expected_sha: str) -> tuple[int, str]:
    if not path.is_file():
        return 0, "MISSING"
    actual = sha256_file(path)
    return int(actual == expected_sha.upper()), actual


def render_page(source: Path, page: int, output_png: Path) -> tuple[int, str]:
    output_png.parent.mkdir(parents=True, exist_ok=True)
    prefix = output_png.with_suffix("")
    command = [
        str(PDFTOPPM),
        "-png",
        "-r",
        str(RENDER_DPI),
        "-f",
        str(page),
        "-l",
        str(page),
        "-singlefile",
        str(source),
        str(prefix),
    ]
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if completed.returncode != 0 or not output_png.is_file() or output_png.stat().st_size == 0:
        detail = (completed.stderr or completed.stdout or "render failed").strip().replace("\n", " ")
        raise RuntimeError(f"G11_TARGETED_VISUAL_RENDER_FAILED={source}:{page}:{detail}")
    return 1, sha256_file(output_png)


def make_contact_sheets(records: list[dict[str, Any]]) -> list[str]:
    CONTACT_ROOT.mkdir(parents=True, exist_ok=True)
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None
    outputs: list[str] = []
    cell_width, cell_height = 410, 575
    columns, rows_per_sheet = 3, 4
    for batch_start in range(0, len(records), 12):
        batch = records[batch_start : batch_start + 12]
        canvas = Image.new("RGB", (columns * cell_width, rows_per_sheet * cell_height), "white")
        draw = ImageDraw.Draw(canvas)
        for index, record in enumerate(batch):
            image = Image.open(record["png_path"]).convert("RGB")
            image.thumbnail((cell_width - 20, cell_height - 48), Image.Resampling.LANCZOS)
            left = (index % columns) * cell_width + (cell_width - image.width) // 2
            top = (index // columns) * cell_height + 26
            canvas.paste(image, (left, top))
            label = f"{record['paper_id']}  p.{record['source_page']}"
            label_box = (index % columns) * cell_width + 8, (index // columns) * cell_height + 7
            draw.text(label_box, label, fill="black", font=font)
        output = CONTACT_ROOT / f"contact_sheet_{batch_start // 12 + 1:02d}.png"
        canvas.save(output, format="PNG")
        outputs.append(rel(output))
    return outputs


def make_packet_diagnostic(
    sample: dict[str, str],
    records: list[dict[str, Any]],
    formal_path: str,
    formal_sha: str,
) -> None:
    packet_dir = OUTPUT_ROOT / f"{as_int(sample['sample_order']):02d}_{sample['paper_id']}"
    lines = [
        "# Targeted visual diagnostic packet",
        "",
        f"- sample_order: {sample['sample_order']}",
        f"- paper_id: {sample['paper_id']}",
        f"- year: {sample['year']}",
        f"- problem: {sample['problem']}",
        f"- source_path: {sample['source_path']}",
        f"- source_sha256: {sample['source_sha256']}",
        f"- formal_artifact_path: {formal_path}",
        f"- formal_artifact_sha256: {formal_sha}",
        "- source_route: PDF source -> existing Q0 formal artifact evidence",
        f"- governed_duplicate: {sample['governed_duplicate']}",
        f"- selected_source_pages: {','.join(str(record['source_page']) for record in records)}",
        "- marker_semantics: PAGE_LOCAL_STRICT_BOUNDARY",
        "",
        "## Human decision",
        "",
        "For each page unit below, judge only whether the source page contains substantive paper content that should enter the formal paper database.",
        "",
        "Allowed human classifications: SUBSTANTIVE_CONTENT, LEGITIMATE_NONCONTENT, UNCLEAR.",
        "Codex has not filled any visual classification. The central decision sheet remains PENDING.",
        "",
    ]
    for record in records:
        lines.extend(
            [
                f"## page_{record['packet_page_role']} (source page {record['source_page']})",
                "",
                f"- source render: {record['png_rel']}",
                f"- formal excerpt: {record['formal_excerpt_rel']}",
                "- human question: Does this source page contain substantive paper content that belongs in the formal paper database?",
                "- source_visual_classification: PENDING",
                "- review_status: PENDING",
                "",
            ]
        )
    packet_dir.mkdir(parents=True, exist_ok=True)
    (packet_dir / "diagnostic.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ensure_inputs()
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    if branch != EXPECTED_BRANCH or head != EXPECTED_HEAD:
        raise RuntimeError("G11_TARGETED_VISUAL_REPO_DRIFT")

    sample_rows = read_csv(SAMPLE_PATH)
    identity_rows = read_csv(IDENTITY_DIAGNOSTIC_PATH)
    page_rows = read_csv(PAGE_DIAGNOSTIC_PATH)
    deep_result = read_json(DEEP_RESULT_PATH)
    sample_by_id, unresolved_pages_by_id, render_total = validate_sample(sample_rows, identity_rows, page_rows, deep_result)
    index_rows = {row["paper_id"]: row for row in read_csv(FORMAL_INDEX_PATH)}
    protected_paths = [SAMPLE_PATH, PAGE_DIAGNOSTIC_PATH, IDENTITY_DIAGNOSTIC_PATH, DEEP_RESULT_PATH, DEEP_REPORT_PATH, DECISIONS_PATH, FORMAL_INDEX_PATH]
    protected_before = {rel(path): sha256_file(path) for path in protected_paths}
    decision_sha_before = sha256_file(DECISIONS_PATH)

    records: list[dict[str, Any]] = []
    decision_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    source_sha_mismatch = 0
    invalid_pages = 0
    for sample in sorted(sample_rows, key=lambda row: as_int(row["sample_order"])):
        paper_id = sample["paper_id"]
        index = index_rows.get(paper_id, {})
        source_path = path_from_catalog(sample["source_path"])
        source_ok, actual_source_sha = validate_source(source_path, sample["source_sha256"])
        if not source_ok:
            source_sha_mismatch += 1
            raise RuntimeError(f"G11_TARGETED_VISUAL_SOURCE_SHA_MISMATCH={paper_id}")
        formal_path_value = index.get("paper_md_path", f"derived/scale/papers/{paper_id}/paper.md")
        formal_path = path_from_catalog(formal_path_value)
        if not formal_path.is_file():
            raise RuntimeError(f"G11_TARGETED_VISUAL_FORMAL_EVIDENCE_MISSING={paper_id}")
        actual_formal_sha = sha256_file(formal_path)
        if actual_formal_sha != sample["body_sha256"].upper():
            raise RuntimeError(f"G11_TARGETED_VISUAL_FORMAL_EVIDENCE_HASH_MISMATCH={paper_id}")
        body = formal_path.read_text(encoding="utf-8")
        selected_pages = select_pages(sorted(as_int(page) for page in unresolved_pages_by_id[paper_id]))
        for role_index, source_page in enumerate(selected_pages):
            role = ("A", "B", "C")[role_index]
            page_row = unresolved_pages_by_id[paper_id][str(source_page)]
            page_count = as_int(index.get("page_count"), 0)
            if page_count <= 0 or source_page < 1 or source_page > page_count:
                invalid_pages += 1
                raise RuntimeError(f"G11_TARGETED_VISUAL_INVALID_SOURCE_PAGE={paper_id}:{source_page}:{page_count}")
            excerpt, marker_found = formal_excerpt(body, source_page)
            if not marker_found:
                raise RuntimeError(f"G11_TARGETED_VISUAL_FORMAL_MARKER_MISSING={paper_id}:{source_page}")
            packet_dir = OUTPUT_ROOT / f"{as_int(sample['sample_order']):02d}_{paper_id}"
            png_path = packet_dir / f"page_{role}.png"
            excerpt_path = packet_dir / f"page_{role}_formal_excerpt.txt"
            excerpt_path.parent.mkdir(parents=True, exist_ok=True)
            excerpt_path.write_text(excerpt, encoding="utf-8")
            _, render_sha = render_page(source_path, source_page, png_path)
            with Image.open(png_path) as image:
                width, height = image.size
            record = {
                "sample_order": as_int(sample["sample_order"]),
                "paper_id": paper_id,
                "year": sample["year"],
                "problem": sample["problem"],
                "source_page": source_page,
                "packet_page_role": role,
                "source_path": sample["source_path"],
                "source_sha256": sample["source_sha256"],
                "source_sha256_actual": actual_source_sha,
                "formal_artifact_path": formal_path_value,
                "formal_artifact_sha256": actual_formal_sha,
                "formal_excerpt_rel": rel(excerpt_path),
                "formal_excerpt_sha256": sha256_file(excerpt_path),
                "png_path": png_path,
                "png_rel": rel(png_path),
                "render_sha256": render_sha,
                "render_width": width,
                "render_height": height,
                "render_dpi": RENDER_DPI,
                "render_status": "SUCCESS",
                "current_machine_classification": "UNRESOLVED_MARKER_ONLY",
                "source_visual_classification": "PENDING",
                "review_status": "PENDING",
                "page_row_note": page_row.get("notes", ""),
                "governed_duplicate": sample["governed_duplicate"],
            }
            records.append(record)
            decision_rows.append(
                {
                    "sample_order": record["sample_order"],
                    "paper_id": paper_id,
                    "year": sample["year"],
                    "problem": sample["problem"],
                    "source_page": source_page,
                    "packet_page_role": role,
                    "source_path": sample["source_path"],
                    "source_sha256": sample["source_sha256"],
                    "formal_artifact_path": formal_path_value,
                    "formal_artifact_sha256": actual_formal_sha,
                    "formal_excerpt_path": rel(excerpt_path),
                    "visual_packet_path": rel(packet_dir / "diagnostic.md"),
                    "current_machine_classification": "UNRESOLVED_MARKER_ONLY",
                    "source_visual_classification": "PENDING",
                    "reviewer_comment": "",
                    "review_status": "PENDING",
                }
            )
            manifest_rows.append(
                {
                    "sample_order": record["sample_order"],
                    "paper_id": paper_id,
                    "source_page": source_page,
                    "packet_page_role": role,
                    "source_path": sample["source_path"],
                    "source_sha256": sample["source_sha256"],
                    "formal_artifact_path": formal_path_value,
                    "formal_artifact_sha256": actual_formal_sha,
                    "formal_excerpt_path": rel(excerpt_path),
                    "formal_excerpt_sha256": record["formal_excerpt_sha256"],
                    "render_path": rel(png_path),
                    "render_sha256": render_sha,
                    "render_width": width,
                    "render_height": height,
                    "render_dpi": RENDER_DPI,
                }
            )
        make_packet_diagnostic(sample, [r for r in records if r["paper_id"] == paper_id], formal_path_value, actual_formal_sha)

    records.sort(key=lambda row: (row["sample_order"], row["source_page"]))
    decision_rows.sort(key=lambda row: (row["sample_order"], row["source_page"]))
    manifest_rows.sort(key=lambda row: (row["sample_order"], row["source_page"]))
    fingerprint_lines = [
        "|".join(
            [
                row["paper_id"],
                str(row["source_page"]),
                row["source_path"],
                row["source_sha256"].upper(),
                row["formal_artifact_sha256"].upper(),
            ]
        )
        for row in manifest_rows
    ]
    fingerprint = sha256_bytes(("\n".join(fingerprint_lines) + "\n").encode("utf-8"))
    attempt_id = f"g11-targeted-visual-diagnostic-{fingerprint[:16].lower()}"
    contact_sheets = make_contact_sheets(records)
    decision_fields = [
        "sample_order", "paper_id", "year", "problem", "source_page", "packet_page_role", "source_path", "source_sha256", "formal_artifact_path", "formal_artifact_sha256", "formal_excerpt_path", "visual_packet_path", "current_machine_classification", "source_visual_classification", "reviewer_comment", "review_status",
    ]
    manifest_fields = [
        "sample_order", "paper_id", "source_page", "packet_page_role", "source_path", "source_sha256", "formal_artifact_path", "formal_artifact_sha256", "formal_excerpt_path", "formal_excerpt_sha256", "render_path", "render_sha256", "render_width", "render_height", "render_dpi",
    ]
    write_csv(OUTPUT_DECISIONS, decision_fields, decision_rows)
    write_csv(OUTPUT_MANIFEST, manifest_fields, manifest_rows)

    guide = f"""# G11 Targeted Visual Diagnostic Review Guide

## Purpose

This guide accompanies `{rel(OUTPUT_DECISIONS)}` and the 20 visual packets under `{rel(OUTPUT_ROOT)}`. It is an evidence-preparation stage, not a formal artifact repair and not a machine visual decision.

Frozen sample identities: `{EXPECTED_SAMPLE_COUNT}`. Rendered source pages: `{len(records)}` at `{RENDER_DPI}` DPI using `{PDFTOPPM}`. The render budget is at most `{MAX_RENDER_PAGES}` pages.

## One decision per page

For each `page_X.png`, answer only:

> Does this source page contain substantive paper content that should enter the formal paper database?

Use exactly one human classification:

- `SUBSTANTIVE_CONTENT`: body text, headings, formulas, tables, code, figures/captions, references, appendices, or other paper content.
- `LEGITIMATE_NONCONTENT`: blank/scan blank, QR code, watermark, advertisement, divider, or page without paper content.
- `UNCLEAR`: the page cannot be classified reliably.

Do not infer a classification from the current formal excerpt. The formal excerpts are existing evidence only and are expected to be marker-only for this sample. Do not change the original G11 decision sheet.

## How to record review

Review each page in `{rel(OUTPUT_ROOT)}` or the contact sheets in `{rel(CONTACT_ROOT)}`. After a human checks a page, update only the corresponding `source_visual_classification`, optional short `reviewer_comment`, and `review_status` in `{rel(OUTPUT_DECISIONS)}`. Until then every row must remain `PENDING`.

If a page is `SUBSTANTIVE_CONTENT` and its formal excerpt remains marker-only, the later repair stage may classify it as `DEFECTIVE_CONTENT_MISSING`. If it is `LEGITIMATE_NONCONTENT`, the later stage may classify it as `LEGITIMATE_BLANK_NONCONTENT`. `UNCLEAR` requires further targeted diagnosis. Those later classifications are not entered in this preparation stage.

## Scope and safety

All PNGs are complete single-page renders of the original source PDFs; no crop, enhancement, annotation, OCR, text extraction, or source modification was performed. The 20 identities and selected pages are frozen by `{rel(SAMPLE_PATH)}`.
"""
    OUTPUT_GUIDE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_GUIDE.write_text(guide, encoding="utf-8")

    decision_sha_after = sha256_file(DECISIONS_PATH)
    protected_after = {rel(path): sha256_file(path) for path in protected_paths}
    if protected_before != protected_after:
        raise RuntimeError("G11_TARGETED_VISUAL_PROTECTED_EVIDENCE_CHANGED")
    if decision_sha_before != decision_sha_after:
        raise RuntimeError("G11_TARGETED_VISUAL_ORIGINAL_DECISION_CHANGED")

    result: dict[str, Any] = {
        "STAGE": "G11-TARGETED-VISUAL-DIAGNOSTIC",
        "STATUS": "PARTIAL",
        "BRANCH": branch,
        "HEAD": head,
        "TARGETED_VISUAL_ATTEMPT_ID": attempt_id,
        "DEEP_DIAGNOSTIC_ATTEMPT_ID": EXPECTED_DEEP_ATTEMPT,
        "DIAGNOSTIC_SAMPLE_IDENTITY_COUNT": EXPECTED_SAMPLE_COUNT,
        "TARGETED_RENDER_PAGE_COUNT": len(records),
        "TARGETED_RENDER_FAILURE_COUNT": 0,
        "TARGETED_VISUAL_PACKET_COUNT": EXPECTED_SAMPLE_COUNT,
        "TARGETED_VISUAL_DECISION_ROW_COUNT": len(decision_rows),
        "TARGETED_VISUAL_PENDING_COUNT": len(decision_rows),
        "TARGETED_VISUAL_SUBSTANTIVE_COUNT": 0,
        "TARGETED_VISUAL_LEGITIMATE_NONCONTENT_COUNT": 0,
        "TARGETED_VISUAL_UNCLEAR_COUNT": 0,
        "TARGETED_VISUAL_DIAGNOSTIC_FINGERPRINT": fingerprint,
        "TARGETED_RENDER_TOOLCHAIN": str(PDFTOPPM),
        "TARGETED_RENDER_DPI": RENDER_DPI,
        "TARGETED_RENDER_FORMAT": "PNG",
        "TARGETED_RENDER_PAGE_LIMIT": MAX_RENDER_PAGES,
        "TARGETED_SOURCE_PAGE_RENDER_RUN": 1,
        "SOURCE_SHA_MISMATCH": source_sha_mismatch,
        "INVALID_SOURCE_PAGE_COUNT": invalid_pages,
        "G11_ORIGINAL_DECISION_MODIFICATION_COUNT": 0,
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
        "Q3_OCR_RUN": 0,
        "PDF_INSPECTOR_EXTRACTION_RUN": 0,
        "PDFTOTEXT_EXTRACTION_RUN": 0,
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
        "GIT_OPERATIONS": 0,
        "PREPARATION_STATUS": "PASS",
        "MANUAL_VISUAL_REVIEW_STATUS": "PENDING",
        "PROTECTED_EVIDENCE_HASHES_UNCHANGED": 1,
        "ORIGINAL_DECISION_SHA256_BEFORE": decision_sha_before,
        "ORIGINAL_DECISION_SHA256_AFTER": decision_sha_after,
        "OUTPUTS": [
            rel(OUTPUT_ROOT),
            *contact_sheets,
            rel(OUTPUT_DECISIONS),
            rel(OUTPUT_MANIFEST),
            rel(OUTPUT_GUIDE),
            rel(OUTPUT_RESULT),
        ],
        "VALIDATION": [
            "Frozen deterministic diagnostic sample count is 20/20; no identity was added, removed, replaced, or resampled.",
            f"Selected unresolved marker-only pages are {len(records)} and satisfy 0 < count <= {MAX_RENDER_PAGES}.",
            "Every selected source path exists and its SHA256 matches the frozen sample/registry evidence.",
            "Every selected source page is within the current formal index page_count and has an existing formal source_page marker excerpt.",
            "Every PNG is a successful full-page 180 DPI Poppler render; no crop, annotation, enhancement, OCR, or extraction was used.",
            "All central decision rows are initialized as current_machine_classification=UNRESOLVED_MARKER_ONLY, source_visual_classification=PENDING, review_status=PENDING.",
            "Original G11 decision sheet and prior diagnostic evidence hashes are unchanged.",
        ],
        "ISSUES": [
            "Human visual review is still pending for all selected pages; Codex intentionally made zero substantive/noncontent/unclear decisions.",
        ],
        "BLOCKER": "MANUAL_VISUAL_REVIEW_REQUIRED",
        "NEXT": "G11-TARGETED-VISUAL-DIAGNOSTIC-APPROVAL",
    }
    write_json(OUTPUT_RESULT, result)
    print("STAGE=G11-TARGETED-VISUAL-DIAGNOSTIC")
    print("STATUS=PARTIAL")
    print(f"TARGETED_VISUAL_ATTEMPT_ID={attempt_id}")
    print(f"DIAGNOSTIC_SAMPLE_IDENTITY_COUNT={EXPECTED_SAMPLE_COUNT}")
    print(f"TARGETED_RENDER_PAGE_COUNT={len(records)}")
    print(f"TARGETED_VISUAL_PACKET_COUNT={EXPECTED_SAMPLE_COUNT}")
    print(f"TARGETED_VISUAL_DECISION_ROW_COUNT={len(decision_rows)}")
    print(f"TARGETED_VISUAL_PENDING_COUNT={len(decision_rows)}")
    print("TARGETED_VISUAL_SUBSTANTIVE_COUNT=0")
    print("TARGETED_VISUAL_LEGITIMATE_NONCONTENT_COUNT=0")
    print("TARGETED_VISUAL_UNCLEAR_COUNT=0")
    print(f"TARGETED_VISUAL_DIAGNOSTIC_FINGERPRINT={fingerprint}")
    print("SOURCE_SHA_MISMATCH=0")
    print("INVALID_SOURCE_PAGE_COUNT=0")
    print("PREPARATION_STATUS=PASS")
    print("MANUAL_VISUAL_REVIEW_STATUS=PENDING")
    print("BLOCKER=MANUAL_VISUAL_REVIEW_REQUIRED")
    print("NEXT=G11-TARGETED-VISUAL-DIAGNOSTIC-APPROVAL")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
