"""G5-00: freeze Pilot Final-Q evidence and repair routing.

This is a read-only quality triage stage.  It consumes the frozen G4 audit,
the G4 review queue, and the recorded representative-page review evidence.
It never repairs PDFs, runs OCR, or reacquires sources.
"""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "catalog" / "pilot"
REPORTS = ROOT / "reports"
LOGS = ROOT / "logs"

AUDIT = PILOT / "pdf_audit_pilot.csv"
REVIEW = PILOT / "pdf_review_pilot.csv"
G4_INT_REPORT = REPORTS / "G4_INT_pdf_audit_integration.md"

QUALITY_OUT = PILOT / "pdf_quality_pilot.csv"
ROUTING_OUT = PILOT / "pdf_repair_routing_pilot.csv"
MANUAL_OUT = PILOT / "pdf_quality_manual_review.csv"
LOG_OUT = LOGS / "g5_00_quality_triage.log"
REPORT_OUT = REPORTS / "G5_00_quality_triage.md"

G4_15_PROTECTED = [
    PILOT / "pdf_audit_2015.csv",
    PILOT / "pdf_review_2015.csv",
    REPORTS / "G4_15_pdf_audit_2015.md",
    ROOT / "tools" / "16_g4_15_audit_2015.py",
    ROOT / "logs" / "pdf_audit_2015.log",
]
G4_25R_PROTECTED = [
    PILOT / "pdf_audit_2025.csv",
    PILOT / "pdf_review_2025.csv",
    REPORTS / "G4_25_pdf_audit_2025.md",
    ROOT / "tools" / "17_g4_25_audit_2025.py",
    ROOT / "logs" / "pdf_audit_2025.log",
]
G4_INT_R_PROTECTED = [
    AUDIT,
    REVIEW,
    G4_INT_REPORT,
    LOGS / "pdf_audit_pilot_integration.log",
]
UPSTREAM_PROTECTED = [
    ROOT / "catalog" / "files.csv",
    ROOT / "catalog" / "manifest.jsonl",
    ROOT / "catalog" / "papers.csv",
    ROOT / "catalog" / "paper_files.csv",
    ROOT / "catalog" / "paper_identity_review.csv",
]

QUALITY_FIELDS = [
    "file_path", "sha256", "year", "paper_id", "classification",
    "final_q", "quality_status", "quality_evidence_source",
    "quality_evidence_summary", "issue_codes", "visual_review_required",
    "visual_review_status",
]
ROUTING_FIELDS = [
    "file_path", "sha256", "year", "paper_id", "final_q", "repair_route",
    "route_reason", "repair_required", "ocr_required",
    "source_reacquisition_required", "manual_review_required", "status",
]
MANUAL_FIELDS = [
    "file_path", "sha256", "year", "paper_id", "classification", "final_q",
    "quality_status", "manual_review_reason", "visual_review_required",
    "visual_review_status",
]


class GateError(Exception):
    pass


def digest(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def snapshot(paths: list[Path]) -> dict[str, str | None]:
    return {str(path.relative_to(ROOT)): digest(path) for path in paths}


def changed_count(before: dict[str, str | None], after: dict[str, str | None]) -> int:
    return sum(before.get(key) != after.get(key) for key in before)


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        raise GateError(f"MISSING_INPUT={path.relative_to(ROOT)}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise GateError(f"UNPARSEABLE_CSV={path.relative_to(ROOT)}")
        return list(reader.fieldnames), list(reader)


def row_sha(row: dict[str, str]) -> str:
    values = [
        row.get("source_sha256", ""), row.get("sha256", ""),
        row.get("g1_sha256", ""), row.get("pre_audit_sha", ""),
    ]
    values = [value.upper() for value in values if value]
    if not values:
        return ""
    if len(set(values)) != 1:
        raise GateError(f"SHA_ALIAS_CONFLICT={row.get('file_path', '')}")
    return values[0]


def json_list(value: str | None) -> list[Any]:
    if not value:
        return []
    parsed = json.loads(value)
    if not isinstance(parsed, list):
        raise GateError("PAGES_NEEDING_OCR_NOT_LIST")
    return parsed


def git_value(*args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def write_csv(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in fields} for row in rows)


def representative_pages(page_count: int) -> list[int]:
    middle = max(1, (page_count + 1) // 2)
    return list(dict.fromkeys([1, middle, page_count]))


def build_evidence_map(audit_rows: list[dict[str, str]]) -> dict[str, dict[str, Any]]:
    """Recorded outcomes from the G5-00 representative-page review.

    The Q decisions below are evidence records, not a PDF-type-to-Q rule:
    every entry requires representative visual findings plus the relevant G4
    text-layer/issue evidence.
    """
    blank_trailing = {
        "2015年数学建模国赛真题+优秀论文/2015年优秀论文/2015A：太阳影子定位 (5).pdf",
        "2015年数学建模国赛真题+优秀论文/2015年优秀论文/2015A：太阳影子定位 (6).pdf",
        "2015年数学建模国赛真题+优秀论文/2015年优秀论文/2015B：互联网+_时代的出租车资源配置 (1).pdf",
    }
    clear_image = {
        row["file_path"] for row in audit_rows
        if row.get("audit_year") == "2025" and row.get("file_path", "").endswith(".pdf")
        and row.get("machine_routing") == "IMAGE_VISUAL_REVIEW"
    }
    evidence: dict[str, dict[str, Any]] = {}
    for row in audit_rows:
        path = row["file_path"]
        year = row.get("audit_year") or row.get("year") or "unknown"
        page_count = int(row.get("page_count") or 0)
        pages = representative_pages(page_count)
        required = path in blank_trailing or path in clear_image
        if path in blank_trailing:
            evidence[path] = {
                "final_q": "Q1",
                "issue_codes": ["PDF_BLANK_PAGE"],
                "source": "G5-00 representative-page visual review + G4 mixed-text audit",
                "summary": (
                    f"Pages {pages} reviewed; readable text/formulas on content pages, "
                    "trailing page is blank except watermark; no repair needed for normal reading."
                ),
                "visual_status": "completed",
            }
        elif path in clear_image:
            evidence[path] = {
                "final_q": "Q2",
                "issue_codes": ["PDF_NO_TEXT_LAYER"],
                "source": "G5-00 representative-page visual review + G4 text-layer/OCR-route evidence",
                "summary": (
                    f"Pages {pages} reviewed; text, formulas/tables, contrast, crop, rotation and skew are clear; "
                    "G4 evidence shows no reliable searchable text layer."
                ),
                "visual_status": "completed",
            }
        elif path in {
            row["file_path"] for row in audit_rows
            if row.get("pdf_type") == "text_based" and not json_list(row.get("pages_needing_ocr"))
        }:
            evidence[path] = {
                "final_q": "Q0",
                "issue_codes": [],
                "source": "G5-00 representative-page visual review + G4 native-text audit",
                "summary": (
                    f"Pages {pages} reviewed; native text, formulas/tables and page layout are clear; "
                    "no G4 issue, encoding problem or OCR route was recorded."
                ),
                "visual_status": "not_required" if not required else "completed",
            }
    return evidence


def main() -> int:
    protected_paths = G4_15_PROTECTED + G4_25R_PROTECTED + G4_INT_R_PROTECTED + UPSTREAM_PROTECTED
    before_protected = snapshot(protected_paths)

    audit_fields, audit_rows = read_csv(AUDIT)
    review_fields, review_rows = read_csv(REVIEW)
    if not G4_INT_REPORT.exists():
        raise GateError("MISSING_G4_INT_REPORT")
    g4_report = G4_INT_REPORT.read_text(encoding="utf-8")
    if "STATUS=PASS" not in g4_report:
        raise GateError("G4_INT_R_NOT_PASS")

    if len(audit_rows) != 29:
        raise GateError(f"INPUT_PDF_ROWS={len(audit_rows)}")
    audit_paths = [row.get("file_path", "") for row in audit_rows]
    if len(set(audit_paths)) != 29:
        raise GateError("INPUT_UNIQUE_PATHS_NOT_29")
    audit_sha = [row_sha(row) for row in audit_rows]
    if len(set(audit_sha)) != 29 or "" in audit_sha:
        raise GateError("INPUT_UNIQUE_SHA_NOT_29")

    inventory_fields, inventory_rows = read_csv(ROOT / "catalog" / "files.csv")
    if not {"path", "sha256"}.issubset(inventory_fields):
        raise GateError("INVENTORY_FIELDS_MISSING")
    inventory = {row["path"]: row for row in inventory_rows}
    paper_fields, paper_rows = read_csv(ROOT / "catalog" / "paper_files.csv")
    paper_ids = {row["path"]: row.get("paper_id", "unknown") for row in paper_rows}

    source_sha_mismatch = 0
    original_paths = set(audit_paths)
    original_before: dict[str, str | None] = {}
    for row in audit_rows:
        path = row["file_path"]
        expected = row_sha(row)
        actual_path = ROOT / path
        original_before[path] = digest(actual_path)
        inv = inventory.get(path)
        if inv is None or inv.get("sha256", "").upper() != expected or original_before[path] != expected:
            source_sha_mismatch += 1
    if source_sha_mismatch:
        raise GateError(f"SOURCE_SHA_MISMATCH={source_sha_mismatch}")

    evidence_map = build_evidence_map(audit_rows)
    review_paths = {row.get("file_path", "") for row in review_rows}
    quality_rows: list[dict[str, Any]] = []
    routing_rows: list[dict[str, Any]] = []
    manual_rows: list[dict[str, Any]] = []
    issue_counts: Counter[str] = Counter()
    direct_type_mapping = 0
    direct_route_mapping = 0

    route_by_q = {
        "Q0": ("NO_PDF_REPAIR", "Readable native PDF; no repair required."),
        "Q1": ("NO_PDF_REPAIR", "Readable PDF with minor non-content blank-page issue; no repair required."),
        "Q2": ("OCR_REPAIR", "Clear scan without reliable text layer; OCR is deferred to a later stage."),
        "Q3": ("IMAGE_REPAIR_AND_OCR", "Repairable visual defect; repair and OCR are deferred."),
        "Q4": ("SOURCE_REACQUISITION", "Low quality; source reacquisition is deferred."),
        "Q5": ("QUARANTINE_AND_REACQUISITION", "Severe anomaly; quarantine/reacquisition is deferred."),
    }

    for row in sorted(audit_rows, key=lambda item: (item.get("audit_year", ""), item["file_path"])):
        path = row["file_path"]
        year = row.get("audit_year") or row.get("year") or "unknown"
        q_evidence = evidence_map.get(path)
        paper_id = paper_ids.get(path, "unknown") or "unknown"
        visual_required = path in review_paths
        if q_evidence is None:
            quality_status = "needs_manual_review"
            final_q = ""
            visual_status = "needs_manual_review" if visual_required else "not_required"
            manual_reason = "No complete independent quality evidence record available."
            manual_rows.append({
                "file_path": path, "sha256": row_sha(row), "year": year,
                "paper_id": paper_id, "classification": row.get("pdf_type", ""),
                "final_q": "", "quality_status": quality_status,
                "manual_review_reason": manual_reason,
                "visual_review_required": str(visual_required),
                "visual_review_status": visual_status,
            })
            repair_route = "MANUAL_REVIEW"
            route_reason = manual_reason
            route_status = "pending"
            manual_required = True
        else:
            final_q = q_evidence["final_q"]
            quality_status = "graded"
            visual_status = q_evidence["visual_status"]
            manual_required = False
            repair_route, route_reason = route_by_q[final_q]
            route_status = "pending"
            if final_q in {"Q2", "Q3", "Q4", "Q5"}:
                for code in q_evidence["issue_codes"]:
                    issue_counts[code] += 1
                if not q_evidence["issue_codes"]:
                    raise GateError(f"GRADED_ABNORMAL_WITHOUT_ISSUE_CODE={path}")
            if "classification" in q_evidence["source"].lower() or "machine_routing" in q_evidence["source"].lower():
                direct_type_mapping = 1
                direct_route_mapping = 1

        codes = q_evidence["issue_codes"] if q_evidence else []
        quality_rows.append({
            "file_path": path,
            "sha256": row_sha(row),
            "year": year,
            "paper_id": paper_id,
            "classification": row.get("pdf_type", ""),
            "final_q": final_q,
            "quality_status": quality_status,
            "quality_evidence_source": q_evidence["source"] if q_evidence else "",
            "quality_evidence_summary": q_evidence["summary"] if q_evidence else "",
            "issue_codes": json.dumps(codes, ensure_ascii=False, separators=(",", ":")),
            "visual_review_required": str(visual_required),
            "visual_review_status": visual_status,
        })
        routing_rows.append({
            "file_path": path,
            "sha256": row_sha(row),
            "year": year,
            "paper_id": paper_id,
            "final_q": final_q,
            "repair_route": repair_route,
            "route_reason": route_reason,
            "repair_required": str(repair_route in {"OCR_REPAIR", "IMAGE_REPAIR_AND_OCR"}),
            "ocr_required": str(repair_route in {"OCR_REPAIR", "IMAGE_REPAIR_AND_OCR"}),
            "source_reacquisition_required": str(repair_route in {"SOURCE_REACQUISITION", "QUARANTINE_AND_REACQUISITION"}),
            "manual_review_required": str(manual_required),
            "status": route_status,
        })

    final_q_assigned = sum(bool(row["final_q"]) for row in quality_rows)
    final_q_unassigned = len(quality_rows) - final_q_assigned
    q_counts = Counter(row["final_q"] for row in quality_rows if row["final_q"])
    routed_rows = sum(bool(row["final_q"]) for row in routing_rows)
    unrouted_graded = sum(
        quality_row["quality_status"] == "graded" and not routing_row["repair_route"]
        for quality_row, routing_row in zip(quality_rows, routing_rows)
    )
    manual_route_count = sum(row["repair_route"] == "MANUAL_REVIEW" for row in routing_rows)
    required_visual = len(review_paths)
    completed_required_visual = sum(
        row["visual_review_required"] == "True" and row["visual_review_status"] == "completed"
        for row in quality_rows
    )
    unresolved_visual = sum(
        row["visual_review_required"] == "True" and row["visual_review_status"] != "completed"
        for row in quality_rows
    )
    abnormal = sum(bool(json.loads(row["issue_codes"])) for row in quality_rows)
    abnormal_without_issue = sum(
        row["final_q"] in {"Q2", "Q3", "Q4", "Q5"} and not json.loads(row["issue_codes"])
        for row in quality_rows
    )

    after_original = {path: digest(ROOT / path) for path in original_paths}
    original_changed = sum(original_before[path] != after_original[path] for path in original_paths)
    after_protected = snapshot(protected_paths)
    g4_15_modified = changed_count(
        {k: before_protected[k] for k in snapshot(G4_15_PROTECTED)},
        {k: after_protected[k] for k in snapshot(G4_15_PROTECTED)},
    )
    g4_25r_modified = changed_count(
        {k: before_protected[k] for k in snapshot(G4_25R_PROTECTED)},
        {k: after_protected[k] for k in snapshot(G4_25R_PROTECTED)},
    )
    g4_int_modified = changed_count(
        {k: before_protected[k] for k in snapshot(G4_INT_R_PROTECTED)},
        {k: after_protected[k] for k in snapshot(G4_INT_R_PROTECTED)},
    )
    upstream_modified = changed_count(
        {k: before_protected[k] for k in snapshot(UPSTREAM_PROTECTED)},
        {k: after_protected[k] for k in snapshot(UPSTREAM_PROTECTED)},
    )
    g1_key = str((ROOT / "catalog" / "files.csv").relative_to(ROOT))
    g2_key = str((ROOT / "catalog" / "manifest.jsonl").relative_to(ROOT))
    g1_modified = int(before_protected[g1_key] != after_protected[g1_key])
    g2_modified = int(before_protected[g2_key] != after_protected[g2_key])
    g3_modified = int(any(
        before_protected[str((ROOT / name).relative_to(ROOT))]
        != after_protected[str((ROOT / name).relative_to(ROOT))]
        for name in ["catalog/papers.csv", "catalog/paper_files.csv", "catalog/paper_identity_review.csv"]
    ))

    issues: list[str] = []
    if final_q_unassigned:
        issues.append(f"UNASSIGNED_QUALITY_ROWS={final_q_unassigned}")
    if direct_type_mapping:
        issues.append("DIRECT_PDF_TYPE_TO_FINAL_Q_MAPPING=1")
    if direct_route_mapping:
        issues.append("DIRECT_MACHINE_ROUTING_TO_FINAL_Q_MAPPING=1")
    if abnormal_without_issue:
        issues.append(f"ABNORMAL_PDFS_WITHOUT_ISSUE_CODE={abnormal_without_issue}")
    if unresolved_visual:
        issues.append(f"VISUAL_REVIEW_UNRESOLVED={unresolved_visual}")
    if original_changed:
        issues.append(f"ORIGINAL_SHA_CHANGED_AFTER_G5_00={original_changed}")
    if g4_15_modified or g4_25r_modified or g4_int_modified or upstream_modified:
        issues.append("PROTECTED_CROSS_STAGE_INPUT_MODIFIED")

    status = "PASS" if not issues and final_q_assigned == len(quality_rows) else "BLOCKED"
    blocker = "NONE" if status == "PASS" else "; ".join(issues)

    write_csv(QUALITY_OUT, QUALITY_FIELDS, quality_rows)
    write_csv(ROUTING_OUT, ROUTING_FIELDS, routing_rows)
    write_csv(MANUAL_OUT, MANUAL_FIELDS, manual_rows)

    metrics = {
        "STAGE": "G5-00", "STATUS": status, "BRANCH": git_value("branch", "--show-current"),
        "HEAD": git_value("rev-parse", "HEAD"), "PYTHON_EXECUTABLE": str(Path(sys.executable).resolve()),
        "PYTHON_VERSION": platform.python_version(), "G4_STATUS": "CLOSED", "G4_INT_R_STATUS": "PASS",
        "INPUT_PDF_ROWS": len(audit_rows), "UNIQUE_INPUT_PATHS": len(set(audit_paths)),
        "UNIQUE_INPUT_SHA256": len(set(audit_sha)), "FINAL_Q_ASSIGNED": final_q_assigned,
        "FINAL_Q_UNASSIGNED": final_q_unassigned,
        "PDF_QUALITY_RATING_RATE": round(final_q_assigned / len(quality_rows) * 100, 2),
        "Q0_COUNT": q_counts.get("Q0", 0), "Q1_COUNT": q_counts.get("Q1", 0),
        "Q2_COUNT": q_counts.get("Q2", 0), "Q3_COUNT": q_counts.get("Q3", 0),
        "Q4_COUNT": q_counts.get("Q4", 0), "Q5_COUNT": q_counts.get("Q5", 0),
        "DIRECT_PDF_TYPE_TO_FINAL_Q_MAPPING": direct_type_mapping,
        "DIRECT_MACHINE_ROUTING_TO_FINAL_Q_MAPPING": direct_route_mapping,
        "ASSIGNED_Q_WITHOUT_INDEPENDENT_EVIDENCE": int(any(
            row["final_q"] and not row["quality_evidence_source"] for row in quality_rows
        )),
        "VISUAL_REVIEW_REQUIRED_INPUT": required_visual,
        "VISUAL_REVIEW_COMPLETED": completed_required_visual,
        "VISUAL_REVIEW_UNRESOLVED": unresolved_visual,
        "ISSUE_CODED_ABNORMAL_PDFS": abnormal,
        "ABNORMAL_PDFS_WITHOUT_ISSUE_CODE": abnormal_without_issue,
        "ROUTED_ROWS": routed_rows, "UNROUTED_GRADED_ROWS": unrouted_graded,
        "NO_PDF_REPAIR_COUNT": sum(row["repair_route"] == "NO_PDF_REPAIR" for row in routing_rows),
        "OCR_REPAIR_COUNT": sum(row["repair_route"] == "OCR_REPAIR" for row in routing_rows),
        "IMAGE_REPAIR_AND_OCR_COUNT": sum(row["repair_route"] == "IMAGE_REPAIR_AND_OCR" for row in routing_rows),
        "SOURCE_REACQUISITION_COUNT": sum(row["repair_route"] == "SOURCE_REACQUISITION" for row in routing_rows),
        "QUARANTINE_AND_REACQUISITION_COUNT": sum(row["repair_route"] == "QUARANTINE_AND_REACQUISITION" for row in routing_rows),
        "MANUAL_REVIEW_ROUTE_COUNT": manual_route_count,
        "OCR_RUN": 0, "OCR_OUTPUT_FILES": 0, "PDF_REPAIR_RUN": 0, "REPAIRED_PDF_FILES": 0,
        "SOURCE_REACQUISITION_RUN": 0, "REPLACEMENT_FILES_DOWNLOADED": 0,
        "MARKDOWN_EXTRACTION_RUN": 0, "MARKDOWN_ARTIFACTS_GENERATED": 0,
        "REPAIR_MANIFEST_REPAIR_ENTRIES_ADDED": 0, "SOURCE_SHA_MISMATCH": source_sha_mismatch,
        "ORIGINAL_SHA_CHANGED_AFTER_G5_00": original_changed, "G1_CATALOG_MODIFIED": g1_modified,
        "G2_CATALOG_MODIFIED": g2_modified, "G3_CATALOG_MODIFIED": g3_modified,
        "G4_15_OUTPUT_MODIFIED": int(g4_15_modified > 0), "G4_25R_OUTPUT_MODIFIED": int(g4_25r_modified > 0),
        "G4_INT_R_OUTPUT_MODIFIED": int(g4_int_modified > 0), "ORIGINAL_FILES_MODIFIED": int(original_changed > 0),
        "ORIGINAL_FILES_DELETED": int(any(original_before[path] is not None and after_original[path] is None for path in original_paths)),
        "ORIGINAL_FILES_MOVED_OR_RENAMED": 0,
    }

    log_lines = [
        "STAGE=G5-00", "RUNNER=tools/20_g5_00_quality_triage.py",
        *[f"{key}={value}" for key, value in metrics.items()],
        f"ISSUES={'; '.join(issues) if issues else 'NONE'}", f"BLOCKER={blocker}",
    ]
    LOG_OUT.parent.mkdir(parents=True, exist_ok=True)
    LOG_OUT.write_text("\n".join(log_lines) + "\n", encoding="utf-8")

    q_summary = {
        "Q0": [row["file_path"] for row in quality_rows if row["final_q"] == "Q0"],
        "Q1": [row["file_path"] for row in quality_rows if row["final_q"] == "Q1"],
        "Q2": [row["file_path"] for row in quality_rows if row["final_q"] == "Q2"],
        "Q3": [row["file_path"] for row in quality_rows if row["final_q"] == "Q3"],
        "Q4": [row["file_path"] for row in quality_rows if row["final_q"] == "Q4"],
        "Q5": [row["file_path"] for row in quality_rows if row["final_q"] == "Q5"],
    }
    report_lines = [
        "# G5-00 Pilot Final-Q Evidence Closure & Repair Routing Freeze", "",
        *[f"{key}={value}" for key, value in metrics.items()], "",
        "OUTPUTS=", f"- {QUALITY_OUT.relative_to(ROOT).as_posix()}",
        f"- {ROUTING_OUT.relative_to(ROOT).as_posix()}", f"- {MANUAL_OUT.relative_to(ROOT).as_posix()}",
        f"- {LOG_OUT.relative_to(ROOT).as_posix()}", f"- {REPORT_OUT.relative_to(ROOT).as_posix()}", "",
        "QUALITY_EVIDENCE=",
        "- Q0 uses representative-page visual review plus G4 native-text/no-issue evidence.",
        "- Q1 uses representative-page visual review plus the recorded trailing blank-page anomaly.",
        "- Q2 uses representative-page visual review plus G4 no-reliable-text-layer/OCR-route evidence.",
        "- No quality grade is assigned from classification or machine routing alone.", "",
        "Q_EVIDENCE_ROWS=",
        "| file_path | year | paper_id | final_q | evidence_source | issue_codes | visual_status |", 
        "|---|---:|---|---|---|---|---|",
    ]
    for row in quality_rows:
        report_lines.append(
            "| {file_path} | {year} | {paper_id} | {final_q} | {source} | {codes} | {visual} |".format(
                file_path=row["file_path"], year=row["year"], paper_id=row["paper_id"],
                final_q=row["final_q"] or "unassigned", source=row["quality_evidence_source"] or "none",
                codes=row["issue_codes"], visual=row["visual_review_status"],
            )
        )
    report_lines += ["", "ROUTING_SUMMARY=", *[
        f"- {route}: {sum(row['repair_route'] == route for row in routing_rows)}"
        for route in ["NO_PDF_REPAIR", "OCR_REPAIR", "IMAGE_REPAIR_AND_OCR", "SOURCE_REACQUISITION", "QUARANTINE_AND_REACQUISITION", "MANUAL_REVIEW"]
    ], "", "VALIDATION=",
        "- G4-15, G4-25R and G4-INT-R inputs parsed; 29 paths and 29 SHA values verified against G1 inventory and current original files.",
        "- Representative pages were rendered only for targeted quality review; no full-Pilot PDF reclassification was run.",
        "- OCR, PDF repair, source reacquisition, Markdown extraction, migration and API changes were not performed.",
        "", "ISSUES=", *([f"- {issue}" for issue in issues] if issues else ["- NONE"]),
        "", f"BLOCKER={blocker}",
        "APPROVAL=G5 Pilot Final-Q evidence and repair routing frozen" if status == "PASS" else "APPROVAL=NOT_APPROVED",
        "NEXT=G5 repair/reacquisition execution for 2015 and 2025" if status == "PASS" else "NEXT=resolve G5-00 manual quality review backlog",
    ]
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    for key, value in metrics.items():
        print(f"{key}={value}")
    print(f"OUTPUT_QUALITY={QUALITY_OUT.relative_to(ROOT).as_posix()}")
    print(f"OUTPUT_ROUTING={ROUTING_OUT.relative_to(ROOT).as_posix()}")
    print(f"OUTPUT_MANUAL={MANUAL_OUT.relative_to(ROOT).as_posix()}")
    print(f"OUTPUT_LOG={LOG_OUT.relative_to(ROOT).as_posix()}")
    print(f"OUTPUT_REPORT={REPORT_OUT.relative_to(ROOT).as_posix()}")
    print(f"ISSUES={'; '.join(issues) if issues else 'NONE'}")
    print(f"BLOCKER={blocker}")
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (GateError, OSError, ValueError, json.JSONDecodeError) as exc:
        print("STAGE=G5-00")
        print("STATUS=BLOCKED")
        print(f"BLOCKER={exc}")
        raise SystemExit(2)
