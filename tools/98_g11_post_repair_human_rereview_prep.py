"""Prepare post-repair human rereview packets for the 11 authoritative G11 MAJORs.

This stage is deliberately read-only with respect to governed inputs.  It reads
already persisted G10/G11 evidence and writes only the new post-repair rereview
packet and decision-sheet outputs.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
STAGE = "G11-POST-REPAIR-HUMAN-REREVIEW-PREP"
EXPECTED_BRANCH = "library-refactor-v1"
EXPECTED_HEAD = "557724fba6572d4d83dc421feda5b17b13ff8d66"
EXPECTED_G9_CSV_SHA = "2E22999E3B44508652F3BB27F3B13B3A6222EC998D26F37FEE6A5D8E4EE75939"
EXPECTED_G9_JSONL_SHA = "60DEDA60A2B1EFAB1098EB044C205D6F6F8C70FE64140D751C54879D8FC8EE4A"
EXPECTED_ORIGINAL_DECISION_SHA = "8078A66F45C0C58F9BA4CF0C85BEB0E331C2BC405C52B93760B999DE00A8FD21"

TARGET_ORDER = [
    "CUMCM-2020-D-003",
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
]

REL_G10_RESULT = Path("catalog/scale/g10_consistency_revalidation_after_g11_repair_result.json")
REL_G10_ATTEMPT = Path("catalog/scale/g10_consistency_revalidation_after_g11_repair_attempt.json")
REL_G10_CHECKS = Path("catalog/scale/g10_consistency_revalidation_checks.csv")
REL_REREVIEW_INPUT = Path("catalog/scale/g11_post_repair_human_rereview_input.csv")
REL_REPAIR_PAGES = Path("catalog/scale/g11_multi_route_formal_repair_pages.csv")
REL_REPAIR_TARGETS = Path("catalog/scale/g11_multi_route_formal_repair_targets.csv")
REL_REPAIR_MANIFEST = Path("catalog/scale/g11_multi_route_formal_repair_manifest.csv")
REL_REPAIR_RESULT = Path("catalog/scale/g11_multi_route_formal_artifact_repair_result.json")
REL_G9_CSV = Path("catalog/scale/g9_paper_index.csv")
REL_G9_JSONL = Path("catalog/scale/g9_paper_index.jsonl")
REL_ARTIFACT_MANIFEST = Path("catalog/scale/g8_artifact_manifest.csv")
REL_ORIGINAL_DECISIONS = Path("catalog/scale/g11_manual_sample_decisions.csv")
REL_ORIGINAL_MANIFEST = Path("catalog/scale/g11_manual_sample_manifest.csv")
REL_TRIAGE = Path("catalog/scale/g11_major_defect_root_cause_triage.csv")
REL_DEEP_DIAGNOSTIC = Path("catalog/scale/g11_major_defect_deep_diagnostic.csv")
REL_MINIMAL_PLAN = Path("catalog/scale/g11_major_defect_minimal_repair_plan_result.json")
REL_ORIGINAL_BASELINE = Path("catalog/scale/g11_manual_sample_authoritative_baseline.json")
REL_APPROVAL_RESUME = Path("catalog/scale/g11_manual_sample_approval_resume_result.json")
REL_TARGETED_APPROVAL = Path("catalog/scale/g11_targeted_visual_diagnostic_approval_result.json")
REL_FINAL_APPROVAL = Path("catalog/scale/g11_marker_only_final_visual_scope_approval_result.json")
REL_REFRESH_INPUT = Path("catalog/scale/g11_repair_g9_refresh_input.csv")

OUT_PACKET_ROOT = Path("reports/scale/g11_post_repair_human_rereview")
OUT_GUIDE = Path("reports/scale/G11_POST_REPAIR_HUMAN_REREVIEW_GUIDE.md")
OUT_REPORT = Path("reports/scale/G11_POST_REPAIR_HUMAN_REREVIEW_PREP.md")
OUT_DECISIONS = Path("catalog/scale/g11_post_repair_human_rereview_decisions.csv")
OUT_RESULT = Path("catalog/scale/g11_post_repair_human_rereview_prep_result.json")


def abs_path(rel: Path) -> Path:
    return ROOT / rel


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(rel: Path) -> dict:
    return json.loads(read_text(abs_path(rel)))


def read_csv(rel: Path) -> List[dict]:
    with abs_path(rel).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_text_atomic(rel: Path, text: str) -> None:
    path = abs_path(rel)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    tmp.replace(path)


def write_bytes_atomic(rel: Path, data: bytes) -> None:
    path = abs_path(rel)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(data)
    tmp.replace(path)


def write_json_atomic(rel: Path, data: dict) -> None:
    write_text_atomic(rel, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def csv_text(rows: List[dict], fieldnames: List[str]) -> str:
    from io import StringIO

    stream = StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def md_value(value: object) -> str:
    if value is None or value == "":
        return "(empty)"
    return str(value).replace("`", "'^")


def rel_string(path: Path) -> str:
    return path.as_posix()


def branch_and_head() -> Tuple[str, str]:
    head_file = ROOT / ".git" / "HEAD"
    raw = head_file.read_text(encoding="utf-8").strip()
    if raw.startswith("ref: "):
        ref = raw[len("ref: "):]
        branch = ref.rsplit("/", 1)[-1]
        ref_path = ROOT / ".git" / Path(ref)
        head = ref_path.read_text(encoding="utf-8").strip()
    else:
        branch = "DETACHED"
        head = raw
    return branch, head


def snapshot_tree(paths: Iterable[Path], excluded: Iterable[Path]) -> Dict[str, str]:
    excluded_abs = {p.resolve() for p in excluded}
    result: Dict[str, str] = {}
    for base in paths:
        if not base.exists():
            continue
        files = [base] if base.is_file() else [p for p in base.rglob("*") if p.is_file()]
        for path in files:
            resolved = path.resolve()
            if resolved in excluded_abs or any(excluded == resolved or excluded in resolved.parents for excluded in excluded_abs):
                continue
            try:
                result[str(resolved)] = sha256_file(path)
            except OSError:
                result[str(resolved)] = "UNREADABLE"
    return result


def target_packet_dir(order: int, paper_id: str) -> Path:
    return OUT_PACKET_ROOT / f"{order:02d}_{paper_id}"


def find_old_packet(paper_id: str) -> Tuple[Path, str]:
    root = abs_path(Path("reports/scale/g11_manual_sample_review"))
    matches = sorted(root.glob(f"*_{paper_id}"))
    if len(matches) != 1:
        raise RuntimeError(f"expected one historical packet for {paper_id}, got {len(matches)}")
    return matches[0], matches[0].name


def trim_evidence(text: str, limit: int = 1800) -> str:
    if len(text) <= limit:
        return text
    tail = min(400, limit // 4)
    head = limit - tail
    return text[:head] + "\n\n[historical excerpt clipped; source file remains authoritative]\n\n" + text[-tail:]


def current_page_segment_marker(body: str, page: int) -> Tuple[str, str]:
    markers = list(re.finditer(r"<!--\s*source_page:\s*(\d+)\s*-->", body, re.IGNORECASE))
    matches = [m for m in markers if int(m.group(1)) == page]
    if len(matches) != 1:
        raise RuntimeError(f"expected one source_page marker for page {page}, got {len(matches)}")
    marker = matches[0]
    end = next((m.start() for m in markers if m.start() > marker.start()), len(body))
    raw_segment = body[marker.start():end]
    content = re.sub(r"^<!--\s*source_page:\s*\d+\s*-->\s*", "", raw_segment, count=1, flags=re.IGNORECASE)
    return raw_segment, content.strip()


def compact_with_map(text: str) -> Tuple[str, List[int]]:
    compact: List[str] = []
    positions: List[int] = []
    for index, char in enumerate(text):
        if not char.isspace():
            compact.append(char)
            positions.append(index)
    return "".join(compact), positions


def current_page_segment_q3(body: str, q3_dir: Path, page: int, page_count: int) -> Tuple[str, str]:
    """Return an exact substring of paper.md using persisted page-text anchors.

    Q3 paper.md has no source_page markers.  The persisted page text is already
    available from the prior Q3 contract, so the only operation here is a
    deterministic whitespace-insensitive anchor lookup in the current paper.md.
    """
    compact_body, positions = compact_with_map(body)
    page_text = read_text(q3_dir / "pages" / f"{page:04d}.txt")
    compact_page, _ = compact_with_map(page_text)
    start = -1
    anchor_len = 0
    for length in (240, 160, 120, 80, 60, 40):
        if len(compact_page) < length:
            continue
        candidate = compact_page[:length]
        found = compact_body.find(candidate)
        if found >= 0:
            start = found
            anchor_len = length
            break
    if start < 0:
        raise RuntimeError(f"cannot anchor Q3 page {page} in current paper.md")

    end_compact = len(compact_body)
    if page < page_count:
        next_text = read_text(q3_dir / "pages" / f"{page + 1:04d}.txt")
        compact_next, _ = compact_with_map(next_text)
        next_start = -1
        for length in (240, 160, 120, 80, 60, 40):
            if len(compact_next) < length:
                continue
            candidate = compact_next[:length]
            found = compact_body.find(candidate, start + anchor_len)
            if found >= 0:
                next_start = found
                break
        if next_start < 0:
            raise RuntimeError(f"cannot find Q3 page {page + 1} boundary in current paper.md")
        end_compact = next_start

    raw_start = positions[start]
    raw_end = len(body) if end_compact >= len(positions) else positions[end_compact]
    raw_segment = body[raw_start:raw_end]
    if compact_body[start:start + anchor_len] != compact_page[:anchor_len]:
        raise RuntimeError(f"Q3 page {page} anchor verification failed")
    return raw_segment, page_text


def markdown_path(path: Path, start: Path) -> str:
    try:
        return Path(__import__("os").path.relpath(abs_path(path), abs_path(start))).as_posix()
    except ValueError:
        return path.as_posix()


def exact_excerpt_file(
    packet_dir: Path,
    page: int,
    paper_id: str,
    body_path: Path,
    body_sha: str,
    raw_segment: str,
    segment_sha: str,
    method: str,
    repair_page: dict,
) -> str:
    return (
        f"# Current Formal Excerpt — {paper_id} — source page {page}\n\n"
        f"- Current body: `{rel_string(body_path)}`\n"
        f"- Current body SHA256: `{body_sha}`\n"
        f"- Current page segment SHA256: `{segment_sha}`\n"
        f"- Extraction method: `{method}`\n"
        f"- Repair route: `{md_value(repair_page.get('route_category'))}`\n"
        f"- Repair layer: `{md_value(repair_page.get('repair_layer'))}`\n"
        f"- Repair page audit: `{rel_string(REL_REPAIR_PAGES)}`\n\n"
        "The block between the delimiters below is copied from the current `paper.md` substring. "
        "No human wording, OCR, rendering, or extraction was added in this stage.\n\n"
        "<!-- BEGIN EXACT CURRENT PAPER.MD SUBSTRING -->\n"
        f"{raw_segment.rstrip()}\n"
        "<!-- END EXACT CURRENT PAPER.MD SUBSTRING -->\n"
    )


def build_before_after(
    paper_id: str,
    target: dict,
    triage: dict,
    old_packet: Path,
    units: List[dict],
    current_excerpt_map: Dict[int, dict],
) -> str:
    lines = [
        f"# Before / After Evidence — {paper_id}",
        "",
        "This is an evidence comparison for the original G11 MAJOR finding. It is not a human decision.",
        "",
        "## Original defective state (historical authoritative evidence)",
        "",
        f"- Original decision sheet: `{rel_string(REL_ORIGINAL_DECISIONS)}`; sample_order `{triage.get('sample_order')}`; severity `{triage.get('overall_severity')}`.",
        f"- Historical body SHA256 before repair: `{target.get('pre_repair_body_sha256')}`.",
        f"- Historical packet: `{old_packet.relative_to(ROOT).as_posix()}`.",
        f"- Original major evidence: {target.get('original_major_evidence') or triage.get('reviewer_comment')}",
        "",
    ]
    for unit in units:
        old_file = abs_path(Path(unit["historical_artifact_excerpt_path"]))
        old_text = trim_evidence(read_text(old_file), 1800)
        lines.extend(
            [
                f"### Historical review unit {unit['review_unit_reference']}",
                "",
                f"- Historical source render: `{unit['historical_source_render_path']}`.",
                f"- Historical formal excerpt: `{unit['historical_artifact_excerpt_path']}`.",
                f"- Historical page-content SHA from triage: `{unit['original_formal_page_content_sha256']}`.",
                "",
                "<pre>",
                old_text,
                "</pre>",
                "",
            ]
        )

    lines.extend(["## Current repaired state (read-only current formal evidence)", ""])
    for page in sorted(current_excerpt_map):
        item = current_excerpt_map[page]
        lines.extend(
            [
                f"### Current source page {page}",
                "",
                f"- Current formal excerpt: `{item['excerpt_path']}`.",
                f"- Current page segment SHA256: `{item['segment_sha256']}`.",
                f"- Raw current excerpt SHA256: `{item['raw_excerpt_sha256']}`.",
                f"- Repair evidence: `{item['repair_evidence_path']}`; evidence SHA256 `{item['repair_evidence_sha256']}`.",
                f"- Programmatic repair validation: `postrepair_pass={item['postrepair_pass']}`.",
                "",
            ]
        )
    lines.extend(
        [
            "The historical block is linked to the original packet evidence; the current block is extracted from the current formal `paper.md`. Human reviewers must compare the original issue with the repaired content and decide the new severity independently.",
            "",
        ]
    )
    return "\n".join(lines)


def build_review_packet(
    packet_dir: Path,
    paper_id: str,
    target: dict,
    triage: dict,
    old_packet_name: str,
    units: List[dict],
    current_excerpt_map: Dict[int, dict],
) -> str:
    lines = [
        f"# {paper_id}",
        "",
        "This packet prepares post-repair human rereview. It makes no post-repair severity decision.",
        "",
        "## Original G11 Major Finding",
        "",
        f"- Original severity: `{triage.get('overall_severity')}`.",
        f"- Original decision reference: `{REL_ORIGINAL_DECISIONS.as_posix()}:paper_id={paper_id};sample_order={triage.get('sample_order')}`.",
        f"- Original review packet: `reports/scale/g11_manual_sample_review/{old_packet_name}/review.md`.",
        f"- Original reviewer comment: {triage.get('reviewer_comment') or '(empty in source evidence)' }",
        f"- Original defect description: {target.get('original_major_evidence') or triage.get('reviewer_comment')}",
        f"- Root-cause category retained from authoritative triage: `{triage.get('root_cause_category')}`.",
        "",
        "## Repair Summary",
        "",
        f"- Repair route: `{target.get('repair_route')}`.",
        f"- Repair layer: `{target.get('repair_layer')}`.",
        f"- Repaired pages: `{target.get('repaired_pages')}`.",
        f"- Historical body SHA256 before repair: `{target.get('pre_repair_body_sha256')}`.",
        f"- Current body SHA256 after repair: `{target.get('current_body_sha256')}`.",
        f"- Repair attempt: `{target.get('repair_attempt_id')}`.",
        f"- Current artifact set: `{target.get('current_artifact_set_id')}`.",
        f"- Current formal body: `{target.get('current_body_path')}`.",
        f"- Repair provenance: `{target.get('repair_provenance_path')}`.",
        "",
        "## Human Re-review Evidence",
        "",
        "Review only whether the original MAJOR issue has been resolved. The page-level evidence below is programmatic binding evidence, not a replacement for human visual/semantic review.",
        "",
    ]
    for unit in units:
        current = current_excerpt_map[unit["source_page"]]
        lines.extend(
            [
                f"### Re-review unit {unit['review_unit_reference']}",
                "",
                f"- Source page / original review location: `{unit['source_page']}` / `{unit['review_unit_reference']}`.",
                f"- Historical source render: `{unit['historical_source_render_path']}`.",
                f"- Historical artifact excerpt: `{unit['historical_artifact_excerpt_path']}`.",
                f"- Original formal page state: `{unit['original_formal_state_summary']}`.",
                f"- Current repaired formal excerpt: `{current['excerpt_path']}`.",
                f"- Current page segment SHA256: `{current['segment_sha256']}`.",
                f"- Repair page evidence: `{current['repair_evidence_path']}`.",
                f"- Repair evidence SHA256: `{current['repair_evidence_sha256']}`.",
                f"- Repair route/layer: `{current['route_category']}` / `{current['repair_layer']}`.",
                f"- Programmatic validation: `preflight_pass={current['preflight_pass']}; postrepair_pass={current['postrepair_pass']}; evidence_quality_status={current['evidence_quality_status']}`.",
                "",
            ]
        )
    lines.extend(
        [
            "## Human Decision",
            "",
            "`PENDING`",
            "",
            "The human reviewer must select exactly one of PASS, MINOR, MAJOR, or CRITICAL in the new decision sheet and record the rationale. Codex has not classified this packet.",
            "",
        ]
    )
    return "\n".join(lines)


def build_guide(targets: List[dict], unit_count: int) -> str:
    lines = [
        "# G11 Post-Repair Human Rereview Guide",
        "",
        "Stage: `G11-POST-REPAIR-HUMAN-REREVIEW-PREP`",
        "",
        "This guide prepares a human rereview of exactly the 11 original G11 MAJOR identities. It does not expand the scope to all 246 repair targets and does not make a severity decision.",
        "",
        "## Required question",
        "",
        "For each identity, answer: **Has the issue that originally caused MAJOR now been resolved in the repaired Formal Artifact?**",
        "",
        f"The prepared evidence contains `{unit_count}` original review units across `{len(targets)}` identities. Each packet binds the historical review render/excerpt, the current repaired `paper.md` page evidence, and the persisted repair audit.",
        "",
        "## Severity contract",
        "",
        "- `PASS`: the original MAJOR issue is resolved and the current rereview scope has no substantive quality problem.",
        "- `MINOR`: the original MAJOR issue is resolved, but an isolated minor issue remains that does not change the main content meaning. MINOR may be accepted for final closure, but it must be recorded.",
        "- `MAJOR`: material omission, meaning-changing OCR/digit/formula error, serious page-content loss, or major table/body defect remains.",
        "- `CRITICAL`: identity/source mismatch, unrelated content, broad body corruption, or serious binding failure is found.",
        "",
        "## Review procedure",
        "",
        "1. Open the packet in the fixed order shown in `00_OVERVIEW.md`.",
        "2. Inspect the existing source render and historical formal excerpt for each Page A/B/C unit. These are authoritative before-state evidence; do not infer the old state from the current artifact.",
        "3. Inspect the linked `current_formal_p<N>.md` excerpt. For marker-route papers it is bounded by strict `source_page` markers. For CUMCM-2020-D-003 it is a deterministic page-text anchor window from current `paper.md`, because that Q3 body has no source-page markers.",
        "4. Compare only the original MAJOR symptom with the repaired content. Do not re-review the entire paper's modeling quality, novelty, or writing style.",
        "5. Write one identity-level decision in `catalog/scale/g11_post_repair_human_rereview_decisions.csv`. Set `new_severity` to one of PASS/MINOR/MAJOR/CRITICAL, write `reviewer_comment`, and change `review_status` to `REVIEWED` only after the human decision is complete.",
        "",
        "## Frozen constraints",
        "",
        "- This preparation leaves the original G11 decision sheet unchanged.",
        "- The prepared new decision sheet is intentionally 11 rows with all `new_severity=PENDING`, empty `reviewer_comment`, and `review_status=PENDING`.",
        "- G11 remains `PARTIAL` until the human rereview approval stage is completed.",
        "- G10 PASS is a binding and consistency gate; it is not an automatic human PASS for the repaired content.",
        "",
        "## Targets",
        "",
        "| # | paper_id | original root cause | repaired pages | packet | status |",
        "|---:|---|---|---|---|---|",
    ]
    for index, target in enumerate(targets, start=1):
        lines.append(
            f"| {index} | {target['paper_id']} | {target['root_cause_category']} | {target['repaired_pages']} | `{target['packet_path']}` | PENDING |"
        )
    lines.append("")
    return "\n".join(lines)


def build_overview(targets: List[dict]) -> str:
    lines = [
        "# G11 Post-Repair Human Rereview Overview",
        "",
        "All rows below are prepared for human review and remain `PENDING`. No automatic severity is asserted.",
        "",
        "| # | paper_id | original MAJOR summary | repair route | repaired page count | packet | status |",
        "|---:|---|---|---|---:|---|---|",
    ]
    for index, target in enumerate(targets, start=1):
        summary = str(target["original_major_evidence"]).replace("|", "/")
        lines.append(
            f"| {index} | {target['paper_id']} | {summary} | {target['repair_route']} | {target['repaired_page_count']} | `{target['packet_path']}` | PENDING |"
        )
    lines.extend(
        [
            "",
            "Start with the individual `REVIEW.md` packet. `before_after.md` provides the historical-to-current evidence comparison, and `current_formal_p<N>.md` contains the current formal excerpt used by that packet.",
            "",
        ]
    )
    return "\n".join(lines)


def build_report(result: dict, targets: List[dict]) -> str:
    lines = [
        "# G11 Post-Repair Human Rereview Preparation",
        "",
        f"Stage status: `{result['STATUS']}`; preparation status: `{result['PREPARATION_STATUS']}`; human rereview status: `{result['HUMAN_REREVIEW_STATUS']}`.",
        "",
        "## Scope and reason",
        "",
        "Only the 11 original G11 MAJOR identities require post-repair human rereview because the repaired content must be judged against the exact historical reasons that caused those MAJOR findings. The 246 repair targets are not a new human-review population; 235 of them were never original G11 MAJOR findings, and sending them all to review would change the approved scope.",
        "",
        "## Original findings retained",
        "",
    ]
    for index, target in enumerate(targets, start=1):
        lines.extend(
            [
                f"{index}. `{target['paper_id']}` — `{target['root_cause_category']}` — {target['original_major_evidence']}",
                f"   - Repaired pages: `{target['repaired_pages']}`; route: `{target['repair_route']}`; packet: `{target['packet_path']}`.",
            ]
        )
    lines.extend(
        [
            "",
            "The 10 marker-route findings are content-missing formal page segments and are bound to current marker-bounded excerpts plus persisted repair evidence. CUMCM-2020-D-003 is the separate `TRUE_CONTENT_QUALITY_MAJOR` Q3 case and is bound to pages 1, 68, and 135, its existing page text, current `paper.md` anchor windows, and Q3 repair provenance.",
            "",
            "## Packet organization",
            "",
            "Each identity has one `REVIEW.md`, one `before_after.md`, and one `current_formal_p<N>.md` for each unique repaired source page needed by its original Page A/B/C units. The new decision sheet has one identity-level row per target and all rows are PENDING. The original decision sheet is kept as historical authoritative evidence and was not edited.",
            "",
            "## Decision rules",
            "",
            "The reviewer should decide PASS, MINOR, MAJOR, or CRITICAL using the original G11 contract. MINOR is acceptable for final closure when the original material issue is resolved, but its residual issue must be recorded. Codex does not convert G10 PASS or a programmatic repair pass into a human severity decision.",
            "",
            "## Why G11 remains PARTIAL",
            "",
            "The evidence packets are prepared, but no human has yet completed the post-repair decisions. Therefore G11 remains PARTIAL and the next stage is `G11-POST-REPAIR-HUMAN-REREVIEW-APPROVAL`.",
            "",
            "## Frozen-operation record",
            "",
            "This stage used only already persisted evidence. No OCR, rendering, extraction, repair, artifact regeneration/promotion, G9/G10/G12 execution, Word, network, dependency installation, or Git operation was performed.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    branch, head = branch_and_head()
    g10 = read_json(REL_G10_RESULT)
    g10_attempt = read_json(REL_G10_ATTEMPT)
    g10_checks = read_csv(REL_G10_CHECKS)
    rereview_input = read_csv(REL_REREVIEW_INPUT)
    repair_pages = read_csv(REL_REPAIR_PAGES)
    repair_targets = read_csv(REL_REPAIR_TARGETS)
    refresh_rows = read_csv(REL_REFRESH_INPUT)
    triage_rows = read_csv(REL_TRIAGE)
    original_decisions = read_csv(REL_ORIGINAL_DECISIONS)
    original_manifest = read_csv(REL_ORIGINAL_MANIFEST)
    g9_rows = read_csv(REL_G9_CSV)
    artifact_rows = read_csv(REL_ARTIFACT_MANIFEST)
    repair_result = read_json(REL_REPAIR_RESULT)
    original_baseline = read_json(REL_ORIGINAL_BASELINE)
    approval_resume = read_json(REL_APPROVAL_RESUME)
    targeted_approval = read_json(REL_TARGETED_APPROVAL)
    final_approval = read_json(REL_FINAL_APPROVAL)

    current_g9_csv_sha = sha256_file(abs_path(REL_G9_CSV))
    current_g9_jsonl_sha = sha256_file(abs_path(REL_G9_JSONL))
    original_decision_sha = sha256_file(abs_path(REL_ORIGINAL_DECISIONS))

    if branch != EXPECTED_BRANCH or head != EXPECTED_HEAD:
        raise RuntimeError(f"repository drift: {branch}@{head}")
    if g10.get("STATUS") != "PASS" or g10.get("G10_REVALIDATION_STATUS") != "PASS":
        raise RuntimeError("G10 source result is not PASS")
    if g10.get("G10_REVALIDATION_ATTEMPT_ID") != "20260905T060442117077Z":
        raise RuntimeError("unexpected G10 attempt")
    if current_g9_csv_sha != EXPECTED_G9_CSV_SHA or current_g9_jsonl_sha != EXPECTED_G9_JSONL_SHA:
        raise RuntimeError("G9 SHA drift")
    if original_decision_sha != EXPECTED_ORIGINAL_DECISION_SHA:
        raise RuntimeError("original decision sheet drift")
    if len(g10_checks) != 96 or sum(row.get("status") == "PASS" for row in g10_checks) != 96:
        raise RuntimeError("G10 check matrix is not 96/96 PASS")

    target_input_by_id = {row["paper_id"]: row for row in rereview_input}
    triage_by_id = {row["paper_id"]: row for row in triage_rows}
    manifest_by_id = {row["paper_id"]: row for row in original_manifest}
    refresh_by_id = {row["paper_id"]: row for row in refresh_rows}
    g9_by_id = {row["paper_id"]: row for row in g9_rows}
    target_audit_by_id = {row["paper_id"]: row for row in repair_targets}
    original_decision_by_id = {row["paper_id"]: row for row in original_decisions}

    if set(target_input_by_id) != set(TARGET_ORDER) or len(target_input_by_id) != len(TARGET_ORDER):
        raise RuntimeError("rereview target set mismatch")
    if len(original_decision_by_id) != 30:
        raise RuntimeError("original decision row count drift")
    if {row.get("overall_severity") for row in original_decisions}.difference({"PASS", "MINOR", "MAJOR", "CRITICAL"}):
        raise RuntimeError("unexpected original severity")
    original_counts = {severity: sum(row.get("overall_severity") == severity for row in original_decisions) for severity in ("PASS", "MINOR", "MAJOR", "CRITICAL")}
    if original_counts != {"PASS": 2, "MINOR": 17, "MAJOR": 11, "CRITICAL": 0}:
        raise RuntimeError(f"original severity counts drift: {original_counts}")
    if sum(row.get("review_status") == "REVIEWED" for row in original_decisions) != 30:
        raise RuntimeError("original review status count drift")
    if original_baseline.get("decision_sheet_sha256") != EXPECTED_ORIGINAL_DECISION_SHA:
        raise RuntimeError("authoritative baseline decision binding drift")
    if approval_resume.get("DECISION_SHEET_SHA256_AFTER") != EXPECTED_ORIGINAL_DECISION_SHA:
        raise RuntimeError("approval/resume decision binding drift")
    if targeted_approval.get("DECISION_SHEET_SHA256_AFTER") != targeted_approval.get("DECISION_SHEET_SHA256_BEFORE"):
        raise RuntimeError("targeted decision sheet changed")
    if final_approval.get("FINAL_VISUAL_DECISION_SHEET_SHA256_AFTER") is None:
        raise RuntimeError("final visual decision binding unavailable")

    protected_roots = [ROOT / "catalog" / "scale", ROOT / "reports" / "scale", ROOT / "derived" / "scale" / "papers"]
    excluded = [abs_path(OUT_GUIDE), abs_path(OUT_REPORT), abs_path(OUT_DECISIONS), abs_path(OUT_RESULT), abs_path(OUT_PACKET_ROOT)]
    before_snapshot = snapshot_tree(protected_roots, excluded)

    targets: List[dict] = []
    all_units: List[dict] = []
    all_current_excerpt_files: List[Path] = []
    original_evidence_pass = 0
    artifact_binding_pass = 0
    index_binding_pass = 0
    provenance_binding_pass = 0
    mapping_pass = 0
    source_evidence_count = 0
    new_source_evidence_count = 0
    formal_missing_count = 0
    true_quality_count = 0

    repair_page_rows_by_key = {(row["paper_id"], int(row["source_page"])): row for row in repair_pages}
    attempt_seed = "|".join([g10.get("G10_REVALIDATION_ATTEMPT_ID", ""), current_g9_csv_sha, *TARGET_ORDER])
    prep_attempt_id = "g11-post-repair-human-rereview-prep-" + sha256_bytes(attempt_seed.encode("utf-8"))[:16].lower()

    for order, paper_id in enumerate(TARGET_ORDER, start=1):
        source = target_input_by_id[paper_id]
        triage = triage_by_id[paper_id]
        old_manifest = manifest_by_id[paper_id]
        refresh = refresh_by_id[paper_id]
        target_audit = target_audit_by_id[paper_id]
        current_body_path = Path(source["current_body_path"])
        current_body_abs = abs_path(current_body_path)
        current_body = read_text(current_body_abs)
        actual_body_sha = sha256_file(current_body_abs)
        old_packet_abs, old_packet_name = find_old_packet(paper_id)
        old_packet_rel = old_packet_abs.relative_to(ROOT)
        g9 = g9_by_id.get(paper_id)
        artifact_rows_for_id = [row for row in artifact_rows if row.get("paper_id") == paper_id]

        if not current_body_abs.exists() or actual_body_sha != source["current_body_sha256"]:
            raise RuntimeError(f"current body binding failure: {paper_id}")
        if not g9 or g9.get("index_status") != "PASS" or g9.get("paper_md_path") != source["current_body_path"] or g9.get("paper_md_sha256") != source["current_body_sha256"]:
            raise RuntimeError(f"current index binding failure: {paper_id}")
        if not artifact_rows_for_id or not abs_path(Path(source["current_artifact_set_id"])).exists() or not abs_path(Path(source["repair_provenance_path"])).exists():
            raise RuntimeError(f"current artifact/provenance binding failure: {paper_id}")
        if refresh.get("current_paper_sha256", "") == "" or refresh.get("candidate_paper_sha256", "") == "":
            raise RuntimeError(f"old/new body SHA unavailable: {paper_id}")
        source_path = abs_path(Path(old_manifest["source_path"]))
        if not source_path.exists() or sha256_file(source_path) != old_manifest["source_sha256"]:
            raise RuntimeError(f"target source SHA mismatch: {paper_id}")

        route_category = triage.get("root_cause_category", "")
        if route_category == "FORMAL_ARTIFACT_PAGE_CONTENT_MISSING":
            formal_missing_count += 1
        elif route_category == "TRUE_CONTENT_QUALITY_MAJOR":
            true_quality_count += 1
        else:
            raise RuntimeError(f"unexpected root cause for {paper_id}: {route_category}")

        if (
            triage.get("overall_severity") != "MAJOR"
            or not triage.get("reviewer_comment")
            or not source.get("original_major_evidence")
            or old_manifest.get("paper_id") != paper_id
            or not (old_packet_abs / "review.md").exists()
        ):
            raise RuntimeError(f"original MAJOR evidence incomplete: {paper_id}")

        units: List[dict] = []
        current_excerpt_map: Dict[int, dict] = {}
        selected_pages = [int(triage[f"selected_page_{label}"]) for label in ("A", "B", "C")]
        for label, page in zip(("A", "B", "C"), selected_pages):
            render_path = old_packet_rel / f"page_{label}.png"
            old_excerpt_path = old_packet_rel / f"page_{label}_artifact_excerpt.txt"
            render_abs = abs_path(render_path)
            old_excerpt_abs = abs_path(old_excerpt_path)
            page_content_sha = triage.get(f"formal_page_{label}_content_sha256", "")
            if not render_abs.exists() or render_abs.stat().st_size <= 0 or not old_excerpt_abs.exists() or old_excerpt_abs.stat().st_size <= 0:
                raise RuntimeError(f"historical source evidence missing: {paper_id} Page {label}")
            source_evidence_count += 1

            repair_page = repair_page_rows_by_key.get((paper_id, page))
            if not repair_page or repair_page.get("postrepair_pass") != "1" or not repair_page.get("evidence_path"):
                raise RuntimeError(f"repair page mapping missing: {paper_id} page {page}")
            repair_evidence_path = Path(repair_page["evidence_path"])
            repair_evidence_abs = abs_path(repair_evidence_path)
            if not repair_evidence_abs.exists() or repair_evidence_abs.stat().st_size <= 0:
                raise RuntimeError(f"repair evidence missing: {paper_id} page {page}")
            expected_evidence_sha = repair_page.get("evidence_sha256", "")
            actual_evidence_sha = sha256_file(repair_evidence_abs)
            if expected_evidence_sha and actual_evidence_sha != expected_evidence_sha:
                raise RuntimeError(f"repair evidence hash mismatch: {paper_id} page {page}")

            if page not in current_excerpt_map:
                if paper_id == "CUMCM-2020-D-003":
                    q3_dir = abs_path(Path("catalog/scale/g8_q3_batch_repair") / paper_id)
                    raw_segment, persisted_page_text = current_page_segment_q3(current_body, q3_dir, page, int(g9.get("page_count", "0")))
                    segment_sha = actual_evidence_sha
                    method = "Q3_EXISTING_PAGE_TEXT_ANCHORED_CURRENT_PAPER_WINDOW"
                    if raw_segment.strip() == "" or not persisted_page_text.strip():
                        raise RuntimeError(f"Q3 current excerpt empty: {paper_id} page {page}")
                else:
                    raw_segment, segment_content = current_page_segment_marker(current_body, page)
                    segment_sha = sha256_bytes(segment_content.encode("utf-8"))
                    expected_candidate_sha = repair_page.get("candidate_segment_sha256", "")
                    method = "STRICT_SOURCE_PAGE_MARKER_BOUNDARY"
                    if not segment_content.strip() or not expected_candidate_sha or segment_sha != expected_candidate_sha:
                        raise RuntimeError(f"marker current excerpt binding failure: {paper_id} page {page}")

                excerpt_rel = target_packet_dir(order, paper_id) / f"current_formal_p{page}.md"
                raw_excerpt_sha = sha256_bytes(raw_segment.encode("utf-8"))
                excerpt_text = exact_excerpt_file(
                    target_packet_dir(order, paper_id),
                    page,
                    paper_id,
                    current_body_path,
                    source["current_body_sha256"],
                    raw_segment,
                    segment_sha,
                    method,
                    repair_page,
                )
                write_text_atomic(excerpt_rel, excerpt_text)
                all_current_excerpt_files.append(excerpt_rel)
                current_excerpt_map[page] = {
                    "excerpt_path": rel_string(excerpt_rel),
                    "segment_sha256": segment_sha,
                    "raw_excerpt_sha256": raw_excerpt_sha,
                    "repair_evidence_path": repair_page["evidence_path"],
                    "repair_evidence_sha256": actual_evidence_sha,
                    "route_category": repair_page.get("route_category", ""),
                    "repair_layer": repair_page.get("repair_layer", ""),
                    "preflight_pass": repair_page.get("preflight_pass", ""),
                    "postrepair_pass": repair_page.get("postrepair_pass", ""),
                    "evidence_quality_status": repair_page.get("evidence_quality_status", ""),
                }
                if not abs_path(excerpt_rel).exists() or abs_path(excerpt_rel).stat().st_size <= 0:
                    raise RuntimeError(f"current excerpt was not written: {paper_id} page {page}")

            current = current_excerpt_map[page]
            unit = {
                "review_unit_reference": f"G11-MANUAL-SAMPLE-{triage['sample_order']}-PAGE-{label}",
                "source_page": page,
                "historical_source_render_path": rel_string(render_path),
                "historical_artifact_excerpt_path": rel_string(old_excerpt_path),
                "original_formal_page_content_sha256": page_content_sha,
                "original_formal_state_summary": (
                    f"present={triage.get(f'formal_page_{label}_content_present')}; "
                    f"char_count={triage.get(f'formal_page_{label}_content_char_count')}; "
                    f"line_count={triage.get(f'formal_page_{label}_content_line_count')}; "
                    f"sha256={page_content_sha}"
                ),
                "repair_evidence_path": repair_page["evidence_path"],
                "repair_page": repair_page,
            }
            units.append(unit)

        if len(units) != 3 or len(current_excerpt_map) == 0:
            raise RuntimeError(f"expected three original review units: {paper_id}")
        all_units.extend(units)
        mapping_pass += 1
        original_evidence_pass += 1
        artifact_binding_pass += 1
        index_binding_pass += 1
        provenance_binding_pass += 1

        packet_dir = target_packet_dir(order, paper_id)
        packet_rel = packet_dir
        target = {
            "paper_id": paper_id,
            "sample_order": int(triage["sample_order"]),
            "original_severity": triage["overall_severity"],
            "original_major_evidence": source["original_major_evidence"],
            "root_cause_category": route_category,
            "repair_route": source["repair_route"],
            "repair_layer": target_audit.get("repair_layer", ""),
            "repaired_pages": source["repaired_pages"],
            "repaired_page_count": len(set(selected_pages)),
            "current_artifact_set_id": source["current_artifact_set_id"],
            "current_body_path": source["current_body_path"],
            "current_body_sha256": source["current_body_sha256"],
            "pre_repair_body_sha256": refresh["current_paper_sha256"],
            "post_repair_body_sha256": refresh["candidate_paper_sha256"],
            "repair_attempt_id": refresh["repair_attempt_id"],
            "repair_provenance_path": source["repair_provenance_path"],
            "packet_path": rel_string(packet_rel),
            "review_packet_file": rel_string(packet_rel / "REVIEW.md"),
            "units": units,
            "current_excerpt_map": current_excerpt_map,
        }
        targets.append(target)

        write_text_atomic(packet_rel / "REVIEW.md", build_review_packet(packet_dir, paper_id, target, triage, old_packet_name, units, current_excerpt_map))
        write_text_atomic(packet_rel / "before_after.md", build_before_after(paper_id, target, triage, old_packet_abs, units, current_excerpt_map))

    if source_evidence_count != len(all_units):
        raise RuntimeError("source evidence unit count mismatch")

    decision_fields = [
        "paper_id",
        "original_severity",
        "original_decision_reference",
        "original_major_summary",
        "repair_route",
        "repaired_pages",
        "current_body_path",
        "current_body_sha256",
        "review_packet_path",
        "new_severity",
        "reviewer_comment",
        "review_status",
    ]
    decision_rows: List[dict] = []
    for target in targets:
        decision_rows.append(
            {
                "paper_id": target["paper_id"],
                "original_severity": target["original_severity"],
                "original_decision_reference": f"{REL_ORIGINAL_DECISIONS.as_posix()}:paper_id={target['paper_id']};sample_order={target['sample_order']}",
                "original_major_summary": target["original_major_evidence"],
                "repair_route": target["repair_route"],
                "repaired_pages": target["repaired_pages"],
                "current_body_path": target["current_body_path"],
                "current_body_sha256": target["current_body_sha256"],
                "review_packet_path": target["review_packet_file"],
                "new_severity": "PENDING",
                "reviewer_comment": "",
                "review_status": "PENDING",
            }
        )
    write_text_atomic(OUT_DECISIONS, csv_text(decision_rows, decision_fields))
    write_text_atomic(OUT_PACKET_ROOT / "00_OVERVIEW.md", build_overview(targets))
    write_text_atomic(OUT_GUIDE, build_guide(targets, len(all_units)))

    decision_sha = sha256_file(abs_path(OUT_DECISIONS))
    if len(decision_rows) != 11 or len({row["paper_id"] for row in decision_rows}) != 11:
        raise RuntimeError("new decision row count/identity uniqueness failure")
    if any(row["new_severity"] != "PENDING" or row["reviewer_comment"] != "" or row["review_status"] != "PENDING" for row in decision_rows):
        raise RuntimeError("new decision sheet is not all PENDING")

    packet_complete = 0
    for target in targets:
        packet_dir = abs_path(Path(target["packet_path"]))
        required = [packet_dir / "REVIEW.md", packet_dir / "before_after.md"]
        required.extend(abs_path(Path(item["excerpt_path"])) for item in target["current_excerpt_map"].values())
        if all(path.exists() and path.stat().st_size > 0 for path in required):
            packet_complete += 1
    packet_incomplete = len(targets) - packet_complete

    after_snapshot = snapshot_tree(protected_roots, excluded)
    changed_protected = sorted(set(before_snapshot) | set(after_snapshot))
    changed_protected = [path for path in changed_protected if before_snapshot.get(path) != after_snapshot.get(path)]

    original_decision_sha_after = sha256_file(abs_path(REL_ORIGINAL_DECISIONS))
    targeted_decision_file = abs_path(Path("catalog/scale/g11_targeted_visual_diagnostic_decisions.csv"))
    final_decision_file = abs_path(Path("catalog/scale/g11_marker_only_final_visual_scope_decisions.csv"))
    targeted_unchanged = targeted_decision_file.exists() and targeted_approval.get("DECISION_SHEET_SHA256_AFTER") == sha256_file(targeted_decision_file)
    final_unchanged = final_decision_file.exists() and final_approval.get("FINAL_VISUAL_DECISION_SHEET_SHA256_AFTER") == sha256_file(final_decision_file)

    result = {
        "STAGE": STAGE,
        "STATUS": "PARTIAL" if not changed_protected else "BLOCKED",
        "BRANCH": branch,
        "HEAD": head,
        "BRANCH_MATCH": int(branch == EXPECTED_BRANCH),
        "HEAD_MATCH": int(head == EXPECTED_HEAD),
        "POST_REPAIR_REREVIEW_PREP_ATTEMPT_ID": prep_attempt_id,
        "SOURCE_G10_REVALIDATION_ATTEMPT_ID": g10.get("G10_REVALIDATION_ATTEMPT_ID"),
        "SOURCE_G10_REVALIDATION_STATUS": g10.get("G10_REVALIDATION_STATUS"),
        "CURRENT_G9_INDEX_CSV_SHA256": current_g9_csv_sha,
        "EXPECTED_G9_INDEX_CSV_SHA256": EXPECTED_G9_CSV_SHA,
        "CURRENT_G9_INDEX_CSV_SHA_MATCH": int(current_g9_csv_sha == EXPECTED_G9_CSV_SHA),
        "CURRENT_G9_INDEX_JSONL_SHA256": current_g9_jsonl_sha,
        "EXPECTED_G9_INDEX_JSONL_SHA256": EXPECTED_G9_JSONL_SHA,
        "CURRENT_G9_INDEX_JSONL_SHA_MATCH": int(current_g9_jsonl_sha == EXPECTED_G9_JSONL_SHA),
        "G10_CHECK_COUNT": len(g10_checks),
        "G10_CHECK_PASS_COUNT": sum(row.get("status") == "PASS" for row in g10_checks),
        "REREVIEW_TARGET_COUNT": len(targets),
        "REREVIEW_TARGET_UNIQUE_IDENTITY_COUNT": len({target["paper_id"] for target in targets}),
        "ORIGINAL_G11_DECISION_SHA256_CURRENT": original_decision_sha_after,
        "ORIGINAL_G11_DECISION_SHA256_MATCH": int(original_decision_sha_after == EXPECTED_ORIGINAL_DECISION_SHA),
        "ORIGINAL_MAJOR_EVIDENCE_BINDING_PASS_COUNT": original_evidence_pass,
        "FORMAL_ARTIFACT_PAGE_CONTENT_MISSING_TARGET_COUNT": formal_missing_count,
        "TRUE_CONTENT_QUALITY_MAJOR_TARGET_COUNT": true_quality_count,
        "REREVIEW_TARGET_REPAIR_BINDING_PASS_COUNT": min(artifact_binding_pass, index_binding_pass, provenance_binding_pass),
        "REREVIEW_TARGET_REPAIR_BINDING_FAIL_COUNT": len(targets) - min(artifact_binding_pass, index_binding_pass, provenance_binding_pass),
        "REREVIEW_UNIT_COUNT": len(all_units),
        "REREVIEW_UNIT_WITH_EXISTING_SOURCE_EVIDENCE_COUNT": source_evidence_count,
        "REREVIEW_UNIT_REQUIRING_NEW_SOURCE_EVIDENCE_COUNT": new_source_evidence_count,
        "REREVIEW_PACKET_COMPLETE_COUNT": packet_complete,
        "REREVIEW_PACKET_INCOMPLETE_COUNT": packet_incomplete,
        "ORIGINAL_MAJOR_TO_REPAIR_MAPPING_PASS_COUNT": mapping_pass,
        "ORIGINAL_MAJOR_TO_REPAIR_MAPPING_FAIL_COUNT": len(targets) - mapping_pass,
        "REREVIEW_TARGET_CURRENT_ARTIFACT_BINDING_PASS_COUNT": artifact_binding_pass,
        "REREVIEW_TARGET_CURRENT_INDEX_BINDING_PASS_COUNT": index_binding_pass,
        "REREVIEW_TARGET_CURRENT_REPAIR_PROVENANCE_PASS_COUNT": provenance_binding_pass,
        "POST_REPAIR_DECISION_ROW_COUNT": len(decision_rows),
        "POST_REPAIR_DECISION_UNIQUE_IDENTITY_COUNT": len({row["paper_id"] for row in decision_rows}),
        "POST_REPAIR_DECISION_SHEET_SHA256": decision_sha,
        "POST_REPAIR_PENDING_COUNT": sum(row["review_status"] == "PENDING" for row in decision_rows),
        "POST_REPAIR_REVIEWED_COUNT": sum(row["review_status"] == "REVIEWED" for row in decision_rows),
        "POST_REPAIR_PASS_COUNT": sum(row["new_severity"] == "PASS" for row in decision_rows),
        "POST_REPAIR_MINOR_COUNT": sum(row["new_severity"] == "MINOR" for row in decision_rows),
        "POST_REPAIR_MAJOR_COUNT": sum(row["new_severity"] == "MAJOR" for row in decision_rows),
        "POST_REPAIR_CRITICAL_COUNT": sum(row["new_severity"] == "CRITICAL" for row in decision_rows),
        "MANUAL_DECISION_SOURCE": "PENDING_USER_HUMAN_REREVIEW",
        "CODEX_INDEPENDENT_REVIEW_JUDGMENT": 0,
        "AUTOMATED_SEVERITY_CLASSIFICATION_RUN": 0,
        "PREPARATION_STATUS": "PASS" if (not changed_protected and packet_complete == 11 and len(decision_rows) == 11 and source_evidence_count == len(all_units)) else "FAIL",
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
        "G11_ORIGINAL_DECISION_MODIFICATION_COUNT": int(original_decision_sha_after != original_decision_sha),
        "TARGETED_VISUAL_DECISION_MODIFICATION_COUNT": int(not targeted_unchanged),
        "FINAL_VISUAL_DECISION_MODIFICATION_COUNT": int(not final_unchanged),
        "ORIGINAL_FILES_MODIFIED": 0,
        "SOURCE_SHA_MISMATCH": 0,
        "OCR_RUN": 0,
        "Q3_OCR_RUN": 0,
        "DIAGNOSTIC_OCR_RUN": 0,
        "PDF_RENDER_RUN": 0,
        "TARGETED_RENDER_RUN": 0,
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
        "HISTORICAL_ORPHAN_PID_43532_CLEANED": 1,
        "PREVIOUS_ARTIFACT_SETS": 308,
        "PREVIOUS_PRIMARY_ARTIFACTS": 924,
        "DOC_MANUAL_BACKLOG": 0,
        "Q3_MANUAL_BACKLOG": 0,
        "TOTAL_REMAINING_ELIGIBLE_BACKLOG": 0,
        "TARGETED_VISUAL_DECISION_SHEET_UNCHANGED": int(targeted_unchanged),
        "FINAL_VISUAL_DECISION_SHEET_UNCHANGED": int(final_unchanged),
        "PROTECTED_INPUT_CHANGED_PATH_COUNT": len(changed_protected),
        "PROTECTED_INPUT_CHANGED_PATHS": changed_protected,
        "OUTPUTS": [
            rel_string(Path("tools/98_g11_post_repair_human_rereview_prep.py")),
            rel_string(OUT_PACKET_ROOT / "00_OVERVIEW.md"),
            rel_string(OUT_GUIDE),
            rel_string(OUT_DECISIONS),
            rel_string(OUT_RESULT),
            rel_string(OUT_REPORT),
            *[target["review_packet_file"] for target in targets],
            *[rel_string(Path(target["packet_path"]) / "before_after.md") for target in targets],
            *[item["excerpt_path"] for target in targets for item in target["current_excerpt_map"].values()],
        ],
        "VALIDATION": [
            "G10 source result is PASS with 96/96 deterministic checks passed.",
            "Current G9 CSV and JSONL SHA256 values match the frozen G10 baseline.",
            "The original G11 decision sheet remains byte-for-byte bound to the authoritative SHA256 and retains 30 REVIEWED rows with 2 PASS, 17 MINOR, 11 MAJOR, and 0 CRITICAL.",
            "Exactly the 11 original MAJOR identities were recovered from the authoritative decision/triage/review-packet evidence.",
            f"Computed {len(all_units)} original A/B/C rereview units; every unit has existing historical source evidence and no new source evidence was requested.",
            "Marker-route current formal excerpts were extracted using strict source_page marker boundaries; the Q3 excerpts use only persisted page-text anchors in the current paper.md because that body has no source_page markers.",
            "Current artifact, index, repair provenance, source-page repair audit, and body SHA bindings passed for all 11 identities.",
            "The new decision sheet has 11 unique identity rows, all PENDING, with empty reviewer comments and no automated severity classification.",
            "Protected governed input hashes did not change while the new preparation outputs were generated.",
        ],
        "ISSUES": [
            "Human post-repair rereview has not yet been performed; all new decisions intentionally remain PENDING.",
            "G11 therefore remains PARTIAL until the next human rereview approval stage.",
        ],
        "BLOCKER": "POST_REPAIR_HUMAN_REREVIEW_REQUIRED",
        "NEXT": "G11-POST-REPAIR-HUMAN-REREVIEW-APPROVAL",
    }
    if result["STATUS"] != "PARTIAL" or result["PREPARATION_STATUS"] != "PASS":
        result["BLOCKER"] = "POST_REPAIR_REREVIEW_BASELINE_DRIFT"
    write_text_atomic(OUT_REPORT, build_report(result, targets))
    write_json_atomic(OUT_RESULT, result)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        raise
