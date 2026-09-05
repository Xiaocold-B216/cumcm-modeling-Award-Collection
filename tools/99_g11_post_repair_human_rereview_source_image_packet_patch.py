"""Patch the post-repair G11 rereview packets with existing source PNG copies.

The source images are copied byte-for-byte from the authoritative historical
G11 review packets.  No rendering, OCR, extraction, or formal-data operation is
performed here.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
STAGE = "G11-POST-REPAIR-HUMAN-REREVIEW-SOURCE-IMAGE-PACKET-PATCH"
EXPECTED_BRANCH = "library-refactor-v1"
EXPECTED_HEAD = "557724fba6572d4d83dc421feda5b17b13ff8d66"
EXPECTED_PREP_ATTEMPT = "g11-post-repair-human-rereview-prep-f937bdd44f63b575"
EXPECTED_PREP_DECISION_SHA = "9F81352331BCDEF28F95FAAC7D6EF53AFDC20470CA867BC9C9B98DF48A05DC55"

REL_PREP_RESULT = Path("catalog/scale/g11_post_repair_human_rereview_prep_result.json")
REL_PREP_INPUT = Path("catalog/scale/g11_post_repair_human_rereview_input.csv")
REL_DECISIONS = Path("catalog/scale/g11_post_repair_human_rereview_decisions.csv")
REL_TRIAGE = Path("catalog/scale/g11_major_defect_root_cause_triage.csv")
REL_ORIGINAL_MANIFEST = Path("catalog/scale/g11_manual_sample_manifest.csv")
REL_REPAIR_PAGES = Path("catalog/scale/g11_multi_route_formal_repair_pages.csv")
REL_REPAIR_TARGETS = Path("catalog/scale/g11_multi_route_formal_repair_targets.csv")
REL_ORIGINAL_DECISIONS = Path("catalog/scale/g11_manual_sample_decisions.csv")
REL_TARGETED_APPROVAL = Path("catalog/scale/g11_targeted_visual_diagnostic_approval_result.json")
REL_FINAL_APPROVAL = Path("catalog/scale/g11_marker_only_final_visual_scope_approval_result.json")

REL_PACKET_ROOT = Path("reports/scale/g11_post_repair_human_rereview")
REL_GUIDE = Path("reports/scale/G11_POST_REPAIR_HUMAN_REREVIEW_GUIDE.md")
REL_PATCH_REPORT = Path("reports/scale/G11_POST_REPAIR_HUMAN_REREVIEW_SOURCE_IMAGE_PACKET_PATCH.md")
REL_ZIP = Path("reports/scale/g11_post_repair_human_rereview_with_source_images.zip")
REL_SOURCE_MANIFEST = Path("catalog/scale/g11_post_repair_human_rereview_source_image_manifest.csv")
REL_PATCH_RESULT = Path("catalog/scale/g11_post_repair_human_rereview_source_image_patch_result.json")
REL_OVERVIEW = REL_PACKET_ROOT / "00_OVERVIEW.md"
REL_SOURCE_INDEX = REL_PACKET_ROOT / "SOURCE_IMAGE_INDEX.md"


def abs_path(rel: Path) -> Path:
    return ROOT / rel


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(rel: Path) -> dict:
    return json.loads(read_text(abs_path(rel)))


def read_csv(rel: Path) -> List[dict]:
    with abs_path(rel).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def write_text_atomic(rel: Path, content: str) -> None:
    path = abs_path(rel)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as handle:
        handle.write(content)
    tmp.replace(path)


def write_json_atomic(rel: Path, value: dict) -> None:
    write_text_atomic(rel, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def write_csv_atomic(rel: Path, rows: List[dict], fieldnames: List[str]) -> None:
    from io import StringIO

    stream = StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    write_text_atomic(rel, stream.getvalue())


def rel_string(path: Path) -> str:
    return path.as_posix()


def branch_and_head() -> Tuple[str, str]:
    raw = (ROOT / ".git" / "HEAD").read_text(encoding="utf-8").strip()
    if raw.startswith("ref: "):
        ref = raw[len("ref: "):]
        branch = ref.rsplit("/", 1)[-1]
        head = (ROOT / ".git" / Path(ref)).read_text(encoding="utf-8").strip()
        return branch, head
    return "DETACHED", raw


def snapshot_tree(roots: Iterable[Path], excluded: Iterable[Path]) -> Dict[str, str]:
    excluded_abs = {path.resolve() for path in excluded}
    result: Dict[str, str] = {}
    for base in roots:
        if not base.exists():
            continue
        files = [base] if base.is_file() else [path for path in base.rglob("*") if path.is_file()]
        for path in files:
            resolved = path.resolve()
            if resolved in excluded_abs or any(excluded == resolved or excluded in resolved.parents for excluded in excluded_abs):
                continue
            result[str(resolved)] = sha256_file(path)
    return result


def upsert_h2_section(text: str, heading: str, section: str) -> str:
    pattern = re.compile(r"(?m)^" + re.escape(heading) + r"\s*$")
    match = pattern.search(text)
    if match:
        next_heading = re.search(r"(?m)^##\s+", text[match.end():])
        end = match.end() + next_heading.start() if next_heading else len(text)
        prefix = text[:match.start()].rstrip("\r\n")
        suffix = text[end:].lstrip("\r\n")
        middle = section.rstrip("\r\n")
        return prefix + "\n\n" + middle + ("\n\n" + suffix if suffix else "\n")
    return text.rstrip("\r\n") + "\n\n" + section.rstrip("\r\n") + "\n"


def remove_h2_section(text: str, heading: str) -> str:
    pattern = re.compile(r"(?m)^" + re.escape(heading) + r"\s*$")
    match = pattern.search(text)
    if not match:
        return text.rstrip("\r\n")
    next_heading = re.search(r"(?m)^##\s+", text[match.end():])
    end = match.end() + next_heading.start() if next_heading else len(text)
    return (text[:match.start()] + text[end:]).strip("\r\n")


def find_packet(root: Path, paper_id: str) -> Path:
    matches = sorted(root.glob(f"*_{paper_id}"))
    if len(matches) != 1:
        raise RuntimeError(f"expected one packet for {paper_id}, got {len(matches)}")
    return matches[0]


def parse_current_units(review_text: str) -> List[dict]:
    pattern = re.compile(
        r"### Re-review unit (?P<unit>[^\r\n]+)\r?\n\r?\n"
        r"- Source page / original review location: `(?P<page>\d+)`"
    )
    units = []
    for match in pattern.finditer(review_text):
        unit_id = match.group("unit").strip()
        label_match = re.search(r"PAGE-([ABC])$", unit_id)
        if not label_match:
            raise RuntimeError(f"cannot resolve original review slot from {unit_id}")
        units.append({"unit_id": unit_id, "slot": label_match.group(1), "source_page": int(match.group("page"))})
    return units


def parse_historical_render(old_review_text: str, slot: str) -> str:
    pattern = re.compile(r"(?m)^- Page " + re.escape(slot) + r":.*?\[render\]\(([^)]+)\)")
    match = pattern.search(old_review_text)
    if not match:
        raise RuntimeError(f"historical render binding missing for Page {slot}")
    return match.group(1)


def png_signature_valid(path: Path) -> bool:
    return path.suffix.lower() == ".png" and path.stat().st_size > 0 and path.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


def build_image_section(records: List[dict], summary: str) -> str:
    lines = [
        "## Source Page Images",
        "",
        "These are byte-for-byte copies of existing historical G11 source renders. They are provided as visual evidence for human rereview; this section asserts no severity or repair conclusion.",
        "",
    ]
    for record in records:
        filename = Path(record["destination_png_path"]).name
        excerpt_name = f"current_formal_p{record['source_page']}.md"
        lines.extend(
            [
                f"### {record['original_review_unit_id']}",
                "",
                f"- Source page: `{record['source_page']}`.",
                f"- Existing source image: [{filename}](source_images/{filename}).",
                f"- Current repaired formal excerpt: [{excerpt_name}]({excerpt_name}).",
                f"- Original issue: {summary}",
                f"- SHARED_SOURCE_IMAGE_BINDING={record['shared_source_image_binding']}.",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def build_before_after_image_section(records: List[dict]) -> str:
    lines = [
        "## Source Page Images",
        "",
        "Existing historical source-render copies for the corresponding rereview units:",
        "",
    ]
    for record in records:
        filename = Path(record["destination_png_path"]).name
        lines.extend(
            [
                f"- `{record['original_review_unit_id']}` / source page `{record['source_page']}`: "
                f"![Source page {record['source_page']}](source_images/{filename})",
                f"  - Original PNG: `{record['original_source_png_path']}`; SHA256 `{record['original_source_png_sha256']}`.",
                f"  - Copied PNG: `source_images/{filename}`; SHA256 `{record['destination_png_sha256']}`.",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def build_overview_image_section(target_records: Dict[str, List[dict]]) -> str:
    lines = [
        "## Source Image Status",
        "",
        "The source images below are ready for human inspection. This does not change the human decision status, which remains `PENDING`.",
        "",
    ]
    for paper_id, records in target_records.items():
        lines.append(f"- `{paper_id}`: `SOURCE_IMAGE_STATUS=READY`; units={len(records)}; status=`PENDING`.")
    return "\n".join(lines).rstrip() + "\n"


def build_source_index(all_records: List[dict]) -> str:
    lines = [
        "# G11 Post-Repair Rereview Source Image Index",
        "",
        "All images are copied from existing historical G11 review renders. This index is evidence-only and does not make a human severity decision.",
        "",
        "| paper_id | rereview unit | source page | copied PNG | original PNG | original SHA256 | copied SHA256 | repaired excerpt | binding |",
        "|---|---|---:|---|---|---|---|---|---|",
    ]
    for record in all_records:
        copied = Path(record["destination_png_path"]).name
        excerpt = f"../{Path(record['current_packet_dir']).name}/current_formal_p{record['source_page']}.md"
        lines.append(
            f"| {record['paper_id']} | {record['original_review_unit_id']} | {record['source_page']} | "
            f"`{record['current_packet_dir']}/source_images/{copied}` | `{record['original_source_png_path']}` | "
            f"`{record['original_source_png_sha256']}` | `{record['destination_png_sha256']}` | `{excerpt}` | "
            f"{record['binding_status']} |"
        )
    lines.extend(
        [
            "",
            f"Coverage: `{len(all_records)}` rereview units, each with one explicit source-page PNG binding.",
            "",
        ]
    )
    return "\n".join(lines)


def zip_bytes_from_files(files: List[Tuple[Path, str]]) -> bytes:
    from io import BytesIO

    stream = BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source, arcname in sorted(files, key=lambda item: item[1]):
            info = zipfile.ZipInfo(arcname)
            info.date_time = (1980, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 0
            info.external_attr = 0o100644 << 16
            archive.writestr(info, source.read_bytes())
    return stream.getvalue()


def inspect_zip(path: Path) -> Tuple[int, int, int, int, int]:
    entry_count = markdown_count = png_count = crc_errors = 0
    with zipfile.ZipFile(path, "r") as archive:
        infos = archive.infolist()
        entry_count = len(infos)
        for info in infos:
            lower = info.filename.lower()
            if lower.endswith(".md"):
                markdown_count += 1
            if lower.endswith(".png"):
                png_count += 1
            try:
                with archive.open(info, "r") as stream:
                    while stream.read(1024 * 1024):
                        pass
            except (zipfile.BadZipFile, OSError, RuntimeError):
                crc_errors += 1
        testzip_bad = archive.testzip()
        if testzip_bad is not None and crc_errors == 0:
            crc_errors = 1
    return entry_count, markdown_count, png_count, crc_errors, int(crc_errors == 0)


def main() -> int:
    branch, head = branch_and_head()
    if branch != EXPECTED_BRANCH or head != EXPECTED_HEAD:
        raise RuntimeError("SOURCE_IMAGE_PACKET_PATCH_REPO_DRIFT")

    prep = read_json(REL_PREP_RESULT)
    if prep.get("STATUS") != "PARTIAL" or prep.get("PREPARATION_STATUS") != "PASS" or prep.get("HUMAN_REREVIEW_STATUS") != "PENDING":
        raise RuntimeError("post-repair preparation baseline is not PASS/PENDING")
    if prep.get("POST_REPAIR_REREVIEW_PREP_ATTEMPT_ID") != EXPECTED_PREP_ATTEMPT:
        raise RuntimeError("unexpected post-repair preparation attempt")
    if prep.get("REREVIEW_TARGET_COUNT") != 11 or prep.get("REREVIEW_UNIT_COUNT") != 33 or prep.get("REREVIEW_PACKET_COMPLETE_COUNT") != 11:
        raise RuntimeError("post-repair preparation cardinality drift")

    decision_sha_before = sha256_file(abs_path(REL_DECISIONS))
    if decision_sha_before != EXPECTED_PREP_DECISION_SHA:
        raise RuntimeError("post-repair decision sheet drift before patch")
    decision_rows = read_csv(REL_DECISIONS)
    if len(decision_rows) != 11 or len({row["paper_id"] for row in decision_rows}) != 11:
        raise RuntimeError("post-repair decision sheet identity drift")
    if any(row["new_severity"] != "PENDING" or row["reviewer_comment"] != "" or row["review_status"] != "PENDING" for row in decision_rows):
        raise RuntimeError("post-repair decision sheet is not all PENDING")
    target_order = [row["paper_id"] for row in decision_rows]

    prep_input = {row["paper_id"]: row for row in read_csv(REL_PREP_INPUT)}
    triage = {row["paper_id"]: row for row in read_csv(REL_TRIAGE)}
    original_manifest = {row["paper_id"]: row for row in read_csv(REL_ORIGINAL_MANIFEST)}
    repair_pages = {(row["paper_id"], int(row["source_page"])): row for row in read_csv(REL_REPAIR_PAGES)}
    repair_targets = {row["paper_id"]: row for row in read_csv(REL_REPAIR_TARGETS)}
    target_set = set(target_order)
    if (
        target_set != set(prep_input)
        or target_set != set(triage)
        or not target_set.issubset(set(original_manifest))
        or not target_set.issubset(set(repair_targets))
    ):
        raise RuntimeError("11 target binding set mismatch")

    packet_root = abs_path(REL_PACKET_ROOT)
    old_root = abs_path(Path("reports/scale/g11_manual_sample_review"))
    records_by_target: Dict[str, List[dict]] = {}
    all_records: List[dict] = []
    source_before: Dict[str, str] = {}
    target_packet_before: Dict[str, str] = {}
    protected_excluded = [
        abs_path(REL_PACKET_ROOT),
        abs_path(REL_PATCH_REPORT),
        abs_path(REL_ZIP),
        abs_path(REL_SOURCE_MANIFEST),
        abs_path(REL_PATCH_RESULT),
    ]
    protected_before = snapshot_tree([ROOT / "catalog", ROOT / "reports", ROOT / "derived" / "scale" / "papers"], protected_excluded)

    for order, paper_id in enumerate(target_order, start=1):
        current_packet = find_packet(packet_root, paper_id)
        old_packet = find_packet(old_root, paper_id)
        review_rel = current_packet.relative_to(ROOT) / "REVIEW.md"
        before_after_rel = current_packet.relative_to(ROOT) / "before_after.md"
        review_path = abs_path(review_rel)
        before_after_path = abs_path(before_after_rel)
        if not review_path.exists() or not before_after_path.exists():
            raise RuntimeError(f"current packet missing: {paper_id}")
        target_packet_before.update({str(path.resolve()): sha256_file(path) for path in current_packet.rglob("*") if path.is_file()})
        current_units = parse_current_units(read_text(review_path))
        if len(current_units) != 3:
            raise RuntimeError(f"expected three current review units: {paper_id}")
        triage_row = triage[paper_id]
        expected_pages = [int(triage_row[f"selected_page_{slot}"]) for slot in "ABC"]
        if [unit["source_page"] for unit in current_units] != expected_pages:
            raise RuntimeError(f"current/original unit page mismatch: {paper_id}")

        old_review_text = read_text(old_packet / "review.md")
        records: List[dict] = []
        for unit_index, unit in enumerate(current_units, start=1):
            page = unit["source_page"]
            slot = unit["slot"]
            render_name = parse_historical_render(old_review_text, slot)
            original_png_rel = old_packet.relative_to(ROOT) / render_name
            original_png = abs_path(original_png_rel)
            if not original_png.exists():
                raise RuntimeError(f"historical source PNG missing: {paper_id} {unit['unit_id']} page {page}")
            source_before[str(original_png.resolve())] = sha256_file(original_png)
            if not png_signature_valid(original_png):
                raise RuntimeError(f"invalid historical PNG: {paper_id} {unit['unit_id']} page {page}")

            repair_page = repair_pages.get((paper_id, page))
            if not repair_page or repair_page.get("postrepair_pass") != "1":
                raise RuntimeError(f"repair page binding missing: {paper_id} page {page}")
            repair_evidence = abs_path(Path(repair_page["evidence_path"]))
            if not repair_evidence.exists() or sha256_file(repair_evidence) != repair_page.get("evidence_sha256"):
                raise RuntimeError(f"repair evidence binding missing: {paper_id} page {page}")

            current_excerpt = current_packet / f"current_formal_p{page}.md"
            if not current_excerpt.exists() or current_excerpt.stat().st_size <= 0:
                raise RuntimeError(f"current formal excerpt missing: {paper_id} page {page}")
            destination_rel = current_packet.relative_to(ROOT) / "source_images" / f"source_unit_{unit_index:02d}_p{page}.png"
            destination = abs_path(destination_rel)
            records.append(
                {
                    "rereview_unit_id": f"{paper_id}::{unit['unit_id']}",
                    "paper_id": paper_id,
                    "original_review_unit_id": unit["unit_id"],
                    "source_page": page,
                    "original_source_png_path": rel_string(original_png_rel),
                    "original_source_png_sha256": sha256_file(original_png),
                    "original_source_png_size": original_png.stat().st_size,
                    "current_packet_dir": rel_string(current_packet.relative_to(ROOT)),
                    "destination_png_path": rel_string(destination_rel),
                    "destination_png_sha256": "",
                    "destination_png_size": "",
                    "repair_page_binding": f"{REL_REPAIR_PAGES.as_posix()}|paper_id={paper_id}|source_page={page}|postrepair_pass=1",
                    "repair_page_evidence_path": repair_page["evidence_path"],
                    "repair_page_evidence_sha256": repair_page["evidence_sha256"],
                    "repaired_formal_excerpt_path": rel_string(current_excerpt.relative_to(ROOT)),
                    "shared_source_image_binding": 0,
                    "shared_source_image_reason": "",
                    "binding_status": "PASS",
                    "copy_sha_match": 0,
                }
            )

        duplicates: Dict[Tuple[str, int], int] = {}
        for record in records:
            key = (record["paper_id"], record["source_page"])
            duplicates[key] = duplicates.get(key, 0) + 1
        for record in records:
            key = (record["paper_id"], record["source_page"])
            if duplicates[key] > 1:
                record["shared_source_image_binding"] = 1
                record["shared_source_image_reason"] = "The original A/B/C review slots select the same source page; each unit still receives its own deterministic copy."

        records_by_target[paper_id] = records
        all_records.extend(records)

    if len(all_records) != 33:
        raise RuntimeError(f"SOURCE_IMAGE_CARDINALITY_MISMATCH:{len(all_records)}")

    for record in all_records:
        source = abs_path(Path(record["original_source_png_path"]))
        destination = abs_path(Path(record["destination_png_path"]))
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        record["destination_png_sha256"] = sha256_file(destination)
        record["destination_png_size"] = destination.stat().st_size
        record["copy_sha_match"] = int(record["destination_png_sha256"] == record["original_source_png_sha256"] and record["destination_png_size"] == record["original_source_png_size"])
        if record["copy_sha_match"] != 1:
            raise RuntimeError(f"source PNG copy SHA mismatch: {record['paper_id']} page {record['source_page']}")

    for paper_id in target_order:
        current_packet = abs_path(Path(records_by_target[paper_id][0]["current_packet_dir"]))
        summary = prep_input[paper_id]["original_major_evidence"]
        review_path = current_packet / "REVIEW.md"
        before_after_path = current_packet / "before_after.md"
        review_before = read_text(review_path)
        before_after_before = read_text(before_after_path)
        image_section = build_image_section(records_by_target[paper_id], summary)
        before_after_section = build_before_after_image_section(records_by_target[paper_id])
        review_after = upsert_h2_section(review_before, "## Source Page Images", image_section)
        before_after_after = upsert_h2_section(before_after_before, "## Source Page Images", before_after_section)
        if remove_h2_section(review_after, "## Source Page Images") != remove_h2_section(review_before, "## Source Page Images"):
            raise RuntimeError(f"REVIEW.md non-image content changed: {paper_id}")
        if remove_h2_section(before_after_after, "## Source Page Images") != remove_h2_section(before_after_before, "## Source Page Images"):
            raise RuntimeError(f"before_after.md non-image content changed: {paper_id}")
        write_text_atomic(current_packet.relative_to(ROOT) / "REVIEW.md", review_after)
        write_text_atomic(current_packet.relative_to(ROOT) / "before_after.md", before_after_after)

    overview_before = read_text(abs_path(REL_OVERVIEW))
    overview_after = upsert_h2_section(overview_before, "## Source Image Status", build_overview_image_section(records_by_target))
    if remove_h2_section(overview_after, "## Source Image Status") != remove_h2_section(overview_before, "## Source Image Status"):
        raise RuntimeError("00_OVERVIEW non-image content changed")
    write_text_atomic(REL_OVERVIEW, overview_after)

    manifest_fields = [
        "rereview_unit_id", "paper_id", "original_review_unit_id", "source_page",
        "original_source_png_path", "original_source_png_sha256", "original_source_png_size",
        "current_packet_dir", "destination_png_path", "destination_png_sha256", "destination_png_size",
        "repair_page_binding", "repair_page_evidence_path", "repair_page_evidence_sha256",
        "repaired_formal_excerpt_path", "shared_source_image_binding", "shared_source_image_reason",
        "binding_status", "copy_sha_match",
    ]
    write_csv_atomic(REL_SOURCE_MANIFEST, all_records, manifest_fields)
    write_text_atomic(REL_SOURCE_INDEX, build_source_index(all_records))

    zip_files: List[Tuple[Path, str]] = [
        (abs_path(REL_OVERVIEW), "00_OVERVIEW.md"),
        (abs_path(REL_SOURCE_INDEX), "SOURCE_IMAGE_INDEX.md"),
        (abs_path(REL_GUIDE), "G11_POST_REPAIR_HUMAN_REREVIEW_GUIDE.md"),
    ]
    for paper_id in target_order:
        current_packet = abs_path(Path(records_by_target[paper_id][0]["current_packet_dir"]))
        packet_name = current_packet.name
        for path in sorted(current_packet.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(current_packet)
            if relative.suffix.lower() == ".md" or (relative.parent.name == "source_images" and relative.suffix.lower() == ".png"):
                zip_files.append((path, f"{packet_name}/{relative.as_posix()}"))
            else:
                raise RuntimeError(f"unexpected packet file for ZIP: {path}")

    zip_data = zip_bytes_from_files(zip_files)
    zip_path = abs_path(REL_ZIP)
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_zip = zip_path.with_name(zip_path.name + ".tmp")
    tmp_zip.write_bytes(zip_data)
    tmp_zip.replace(zip_path)
    entry_count, markdown_count, png_count, crc_errors, zip_open_pass = inspect_zip(zip_path)
    if png_count != 33 or crc_errors != 0 or zip_open_pass != 1:
        raise RuntimeError(f"ZIP validation failed: entries={entry_count};md={markdown_count};png={png_count};crc={crc_errors}")

    decision_sha_after = sha256_file(abs_path(REL_DECISIONS))
    if decision_sha_after != decision_sha_before:
        raise RuntimeError("post-repair decision sheet changed during patch")
    original_png_after = {path: sha256_file(Path(path)) for path in source_before}
    original_png_modifications = sum(source_before[path] != original_png_after[path] for path in source_before)
    if original_png_modifications != 0:
        raise RuntimeError("historical source PNG was modified")

    target_packet_after = snapshot_tree([packet_root], [])
    allowed_existing_changes = set()
    for path in target_packet_before:
        p = Path(path)
        if p.name in {"REVIEW.md", "before_after.md"} or (p.name == "00_OVERVIEW.md" and p.parent == packet_root.resolve()):
            allowed_existing_changes.add(path)
    packet_root_resolved = packet_root.resolve()
    source_index_path = (packet_root / "SOURCE_IMAGE_INDEX.md").resolve()
    overview_path = (packet_root / "00_OVERVIEW.md").resolve()
    unexpected_packet_changes = []
    for path in set(target_packet_before) | set(target_packet_after):
        if target_packet_before.get(path) == target_packet_after.get(path) or path in allowed_existing_changes:
            continue
        path_obj = Path(path).resolve()
        is_allowed_new_source_png = path not in target_packet_before and path_obj.parent.name == "source_images" and path_obj.suffix.lower() == ".png"
        is_allowed_new_index = path not in target_packet_before and path_obj == source_index_path
        is_allowed_new_overview = path not in target_packet_before and path_obj == overview_path
        if not (is_allowed_new_source_png or is_allowed_new_index or is_allowed_new_overview):
            unexpected_packet_changes.append(path)
    if unexpected_packet_changes:
        raise RuntimeError("unexpected current packet modification: " + ",".join(sorted(unexpected_packet_changes)))

    protected_after = snapshot_tree([ROOT / "catalog", ROOT / "reports", ROOT / "derived" / "scale" / "papers"], protected_excluded)
    protected_changes = [path for path in set(protected_before) | set(protected_after) if protected_before.get(path) != protected_after.get(path)]
    if protected_changes:
        raise RuntimeError("unexpected governed-data modification: " + ",".join(sorted(protected_changes)))

    patch_seed = "|".join([EXPECTED_PREP_ATTEMPT, decision_sha_before, *target_order])
    patch_attempt_id = "g11-post-repair-source-image-patch-" + sha256_bytes(patch_seed.encode("utf-8"))[:16].lower()
    shared_count = sum(record["shared_source_image_binding"] == 1 for record in all_records)
    result = {
        "STAGE": STAGE,
        "STATUS": "PASS",
        "BRANCH": branch,
        "HEAD": head,
        "BRANCH_MATCH": 1,
        "HEAD_MATCH": 1,
        "SOURCE_IMAGE_PATCH_ATTEMPT_ID": patch_attempt_id,
        "SOURCE_POST_REPAIR_REREVIEW_PREP_ATTEMPT_ID": EXPECTED_PREP_ATTEMPT,
        "REREVIEW_TARGET_COUNT": len(target_order),
        "REREVIEW_TARGET_UNIQUE_IDENTITY_COUNT": len(set(target_order)),
        "REREVIEW_UNIT_COUNT": len(all_records),
        "SOURCE_IMAGE_EXPECTED_COUNT": len(all_records),
        "SOURCE_IMAGE_LOCATED_COUNT": len(all_records),
        "SOURCE_IMAGE_UNIT_BINDING_PASS_COUNT": sum(record["binding_status"] == "PASS" for record in all_records),
        "SOURCE_IMAGE_UNIT_BINDING_FAIL_COUNT": sum(record["binding_status"] != "PASS" for record in all_records),
        "SOURCE_IMAGE_MISSING_COUNT": 0,
        "SOURCE_IMAGE_AMBIGUOUS_BINDING_COUNT": 0,
        "SOURCE_PNG_PATH_CHECKED_COUNT": len(all_records),
        "SOURCE_PNG_EXISTS_COUNT": len(all_records),
        "SOURCE_PNG_VALID_SIGNATURE_COUNT": sum(png_signature_valid(abs_path(Path(record["original_source_png_path"]))) for record in all_records),
        "SOURCE_PNG_INVALID_COUNT": 0,
        "SOURCE_IMAGE_COPY_COUNT": len(all_records),
        "SOURCE_IMAGE_COPY_SHA_MATCH_COUNT": sum(record["copy_sha_match"] for record in all_records),
        "SOURCE_IMAGE_COPY_SHA_MISMATCH_COUNT": sum(record["copy_sha_match"] == 0 for record in all_records),
        "ORIGINAL_SOURCE_PNG_MODIFICATION_COUNT": original_png_modifications,
        "SHARED_SOURCE_IMAGE_BINDING_COUNT": shared_count,
        "UPDATED_REREVIEW_PACKET_COUNT": len(records_by_target),
        "SOURCE_IMAGE_INDEX_GENERATED": 1,
        "POST_REPAIR_DECISION_ROW_COUNT": len(decision_rows),
        "POST_REPAIR_PENDING_COUNT": sum(row["review_status"] == "PENDING" for row in decision_rows),
        "POST_REPAIR_REVIEWED_COUNT": sum(row["review_status"] == "REVIEWED" for row in decision_rows),
        "POST_REPAIR_DECISION_SHEET_SHA256_BEFORE": decision_sha_before,
        "POST_REPAIR_DECISION_SHEET_SHA256_AFTER": decision_sha_after,
        "POST_REPAIR_DECISION_SHEET_HASH_UNCHANGED": int(decision_sha_before == decision_sha_after),
        "ZIP_PATH": rel_string(REL_ZIP),
        "ZIP_ENTRY_COUNT": entry_count,
        "ZIP_MARKDOWN_FILE_COUNT": markdown_count,
        "ZIP_PNG_FILE_COUNT": png_count,
        "ZIP_OPEN_PASS": zip_open_pass,
        "ZIP_CRC_ERROR_COUNT": crc_errors,
        "POST_REPAIR_REREVIEW_SOURCE_IMAGE_ZIP_SHA256": sha256_file(zip_path),
        "MANUAL_DECISION_SOURCE": "PENDING_USER_HUMAN_REREVIEW",
        "CODEX_INDEPENDENT_VISUAL_JUDGMENT": 0,
        "AUTOMATED_VISUAL_CLASSIFICATION_RUN": 0,
        "AUTOMATED_SEVERITY_CLASSIFICATION_RUN": 0,
        "HUMAN_REREVIEW_STATUS": "PENDING",
        "G11_STATUS_REMAINS": "PARTIAL",
        "FORMAL_ARTIFACT_CONTENT_MODIFICATION_COUNT": 0,
        "FORMAL_ARTIFACT_METADATA_MODIFICATION_COUNT": 0,
        "ARTIFACT_REGISTRY_MODIFICATION_COUNT": 0,
        "FORMAL_INDEX_MODIFICATION_COUNT": 0,
        "IDENTITY_MODIFICATION_COUNT": 0,
        "MEMBERSHIP_MODIFICATION_COUNT": 0,
        "FORMAL_ELIGIBILITY_MODIFIED": 0,
        "SOURCE_REGISTRY_MODIFICATION_COUNT": 0,
        "BACKLOG_MODIFICATION_COUNT": 0,
        "G11_ORIGINAL_DECISION_MODIFICATION_COUNT": 0,
        "TARGETED_VISUAL_DECISION_MODIFICATION_COUNT": 0,
        "FINAL_VISUAL_DECISION_MODIFICATION_COUNT": 0,
        "POST_REPAIR_HUMAN_REREVIEW_DECISION_MODIFICATION_COUNT": 0,
        "OCR_RUN": 0,
        "Q3_OCR_RUN": 0,
        "DIAGNOSTIC_OCR_RUN": 0,
        "PDF_RENDER_RUN": 0,
        "TARGETED_RENDER_RUN": 0,
        "NEW_SOURCE_IMAGE_GENERATION_RUN": 0,
        "PDF_INSPECTOR_EXTRACTION_RUN": 0,
        "PDFTOTEXT_EXTRACTION_RUN": 0,
        "FORMAL_EXTRACTION_RUN": 0,
        "BODY_RECONSTRUCTION_RUN": 0,
        "ARTIFACT_REGENERATION_RUN": 0,
        "ARTIFACT_REPROMOTION_RUN": 0,
        "G9_REBUILD_RUN": 0,
        "G9_REFRESH_RUN": 0,
        "G10_RUN": 0,
        "G12_RUN": 0,
        "DOC_BATCH_RUN": 0,
        "Q3_REPAIR_RUN": 0,
        "WORD_RUN": 0,
        "WORD_COM_RUN": 0,
        "DOC_CONVERSION_RUN": 0,
        "PRINT_JOB_RUN": 0,
        "NETWORK_ACCESS_USED": 0,
        "DOWNLOAD_RUN": 0,
        "NEW_DEPENDENCY_INSTALLED": 0,
        "GIT_OPERATIONS": 0,
        "SOURCE_IMAGE_PACKET_PATCH_STATUS": "PASS",
        "OUTPUTS": [
            rel_string(Path("tools/99_g11_post_repair_human_rereview_source_image_packet_patch.py")),
            rel_string(REL_SOURCE_MANIFEST),
            rel_string(REL_SOURCE_INDEX),
            rel_string(REL_ZIP),
            rel_string(REL_PATCH_REPORT),
            *[rel_string(Path(records_by_target[paper_id][0]["current_packet_dir"]) / "REVIEW.md") for paper_id in target_order],
        ],
        "VALIDATION": [
            "The 11-target and 33-unit post-repair preparation baseline matched before patching.",
            "All 33 source PNGs were located from the existing authoritative historical G11 review packets; no new source image was generated.",
            "Every source file passed extension, non-empty-size, and PNG-signature checks.",
            "Every destination PNG was copied byte-for-byte and its SHA256 matched the original source PNG.",
            "Each current REVIEW.md and before_after.md received only a Source Page Images section with relative links; original evidence and decision text were preserved.",
            "The source-image index and a ZIP containing the 11 packets, Markdown evidence, and all 33 PNGs were generated and CRC-checked.",
            "The post-repair decision sheet remained byte-for-byte unchanged with 11 PENDING rows.",
            "No formal artifact, index, registry, identity, membership, eligibility, source registry, backlog, or original image was modified.",
        ],
        "ISSUES": [
            "Human post-repair rereview remains pending; this patch adds evidence only.",
            "The next human action is to inspect the 11 packets and then perform the separate approval/transcription stage.",
        ],
        "BLOCKER": "NONE",
        "NEXT": "USER_POST_REPAIR_HUMAN_REREVIEW",
    }
    write_text_atomic(REL_PATCH_REPORT, build_patch_report(result, target_order, records_by_target))
    write_json_atomic(REL_PATCH_RESULT, result)
    return 0


def build_patch_report(result: dict, target_order: List[str], records_by_target: Dict[str, List[dict]]) -> str:
    lines = [
        "# G11 Post-Repair Human Rereview Source Image Packet Patch",
        "",
        "## Purpose",
        "",
        "The preparation stage produced the correct Markdown evidence but did not place the already-rendered source-page PNGs inside the new packet directories. This patch adds only byte-for-byte copies of those historical PNGs and explicit local links, so a human can inspect each original source page beside the repaired formal excerpt.",
        "",
        "## Evidence source and operation boundary",
        "",
        "All 33 images came from the original authoritative G11 review packets (`reports/scale/g11_manual_sample_review/*`). No new render, OCR, extraction, annotation, recompression, Word operation, network operation, or dependency installation was performed.",
        "",
        "## Binding and coverage",
        "",
        f"The 33 rereview units were recovered from the current post-repair packet unit references and bound to their original historical Page A/B/C render. Each destination name contains the source page number. The repeated source page in CUMCM-1993-B-001 is recorded as a legitimate shared-page binding, while each unit still has its own deterministic copied PNG.",
        "",
        f"- Targets: `{len(target_order)}`",
        f"- Rereview units: `{result['REREVIEW_UNIT_COUNT']}`",
        f"- Source PNGs located/checked: `{result['SOURCE_IMAGE_LOCATED_COUNT']}`",
        f"- PNG copies with matching SHA256: `{result['SOURCE_IMAGE_COPY_SHA_MATCH_COUNT']}`",
        f"- Updated packets: `{result['UPDATED_REREVIEW_PACKET_COUNT']}`",
        "",
        "## Packet changes",
        "",
        "Each packet received a `source_images/` directory. `REVIEW.md` now links each source page image to its corresponding current formal excerpt and repeats the original issue summary. `before_after.md` retains its existing historical/current content and gains only a source-image link section. `00_OVERVIEW.md` gains `SOURCE_IMAGE_STATUS=READY` while decision status remains PENDING.",
        "",
        "## ZIP",
        "",
        f"The complete ZIP is `{result['ZIP_PATH']}` with `{result['ZIP_ENTRY_COUNT']}` entries: `{result['ZIP_MARKDOWN_FILE_COUNT']}` Markdown files and `{result['ZIP_PNG_FILE_COUNT']}` PNG files. ZIP opening and CRC validation passed; no PDF, DOC, catalog, cache, staging backup, or Git metadata was included.",
        "",
        "## Decision boundary",
        "",
        f"The post-repair decision sheet SHA256 remained unchanged before/after: `{result['POST_REPAIR_DECISION_SHEET_SHA256_BEFORE']}`. All 11 rows remain `new_severity=PENDING`, empty `reviewer_comment`, and `review_status=PENDING`. Codex made no visual or severity judgment. Human rereview is still required, so G11 remains PARTIAL.",
        "",
        "## Next action",
        "",
        "Open the ZIP or the local packet directory, inspect the original source PNG and linked repaired excerpt for each unit, and provide the identity-level PASS/MINOR/MAJOR/CRITICAL decision in the separate human approval stage.",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        raise
