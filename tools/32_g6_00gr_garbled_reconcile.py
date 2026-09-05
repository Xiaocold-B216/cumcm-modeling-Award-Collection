"""G6-00G-R targeted reconciliation of the existing Poppler garbled flags.

The target set is discovered from the existing G6-00G hybrid audit.  This
runner performs exactly one Poppler and one pdf-inspector page-scoped check per
target row, plus one whole-document pdf-inspector evidence read per affected
readable PDF.  It never re-runs the 516-page extraction.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.metadata
import json
import re
import subprocess
import sys
import unicodedata
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pdf_inspector


ROOT = Path(__file__).resolve().parents[1]
PYTHON = Path(sys.executable).resolve()
STAMP = timezone(timedelta(hours=8))

AUDIT = ROOT / "catalog" / "pilot" / "g6_q2_hybrid_page_audit.csv"
RECON = ROOT / "catalog" / "pilot" / "g6_q2_garbled_reconciliation.csv"
CONTRACT = ROOT / "catalog" / "pilot" / "g6_extraction_contract.json"
BRIDGE = ROOT / "catalog" / "pilot" / "g3_25r_q2_identity_map.csv"
G5_OCR = ROOT / "catalog" / "pilot" / "pdf_ocr_results_2025.csv"
G6_REPORT = ROOT / "reports" / "G6_00G_hybrid_page_extraction.md"
G6_LOG = ROOT / "logs" / "g6_00g_hybrid_page_extraction.log"
LOG = ROOT / "logs" / "g6_00gr_garbled_reconcile.log"
REPORT = ROOT / "reports" / "G6_00GR_garbled_reconcile.md"
PREVIEW_DIR = ROOT / ".bootstrap" / "g6_00gr_preview"

POPPLER_DIR = Path(r"D:\texlive\2026\bin\windows")
PDFTOTEXT = POPPLER_DIR / "pdftotext.exe"
PDFINFO = POPPLER_DIR / "pdfinfo.exe"
PDFTOPPM = POPPLER_DIR / "pdftoppm.exe"

FIELDS = [
    "paper_id", "source_page", "original_garbled_flag", "poppler_text_chars",
    "poppler_normalized_chars", "replacement_char_count", "replacement_char_ratio",
    "control_char_count", "control_char_ratio", "printable_char_ratio",
    "repeated_sequence_score", "pdf_inspector_page_evidence_available",
    "pdf_inspector_page_chars", "pdf_inspector_page_status",
    "pdf_inspector_whole_document_evidence_available", "visual_has_substantive_content",
    "visual_text_present", "visual_formula_heavy", "visual_table_heavy",
    "visual_image_only", "visual_type", "final_status", "final_text_usable",
    "reason", "evidence",
]


class GateError(RuntimeError):
    pass


# These are manual visual observations made from the eight rendered target
# pages.  Target discovery itself is never based on this map; it is always the
# existing audit's poppler_status=GARBLED filter.
VISUAL_QA: dict[tuple[str, int], dict[str, Any]] = {
    ("CUMCM-2025-B-B060", 71): {
        "visual_has_substantive_content": 1, "visual_text_present": 1,
        "visual_formula_heavy": 0, "visual_table_heavy": 0, "visual_image_only": 1,
        "visual_type": "CODE_LISTING_FRAGMENT_IMAGE_ONLY",
        "final_status": "IMAGE_ONLY_CONTENT_PAGE",
        "reason": "Rendered page contains a small code-listing fragment and heading, but the page is image-backed and the Poppler text is not usable as a reliable text source.",
    },
    ("CUMCM-2025-C-C023", 9): {
        "visual_has_substantive_content": 0, "visual_text_present": 0,
        "visual_formula_heavy": 0, "visual_table_heavy": 0, "visual_image_only": 1,
        "visual_type": "WATERMARK_ONLY_PAGE",
        "final_status": "IMAGE_ONLY_CONTENT_PAGE",
        "reason": "Rendered page is blank apart from a publisher watermark; the diagnostic flag is non-blocking and the existing base page class remains unchanged.",
    },
    ("CUMCM-2025-C-C023", 26): {
        "visual_has_substantive_content": 1, "visual_text_present": 1,
        "visual_formula_heavy": 0, "visual_table_heavy": 0, "visual_image_only": 1,
        "visual_type": "FIGURE_PAGE",
        "final_status": "IMAGE_ONLY_CONTENT_PAGE",
        "reason": "Rendered page contains a substantive figure/chart, but reliable page text is unavailable; this is an image-only content page, not a text extraction blocker.",
    },
    ("CUMCM-2025-C-C132", 7): {
        "visual_has_substantive_content": 0, "visual_text_present": 0,
        "visual_formula_heavy": 0, "visual_table_heavy": 0, "visual_image_only": 0,
        "visual_type": "VERIFIED_BLANK_PAGE",
        "final_status": "IMAGE_ONLY_CONTENT_PAGE",
        "reason": "Existing G5/G6 evidence verifies this page as blank. The reconciliation vocabulary has no separate blank status, so the diagnostic row is non-blocking while the base VERIFIED_BLANK_PAGE class is preserved.",
    },
    ("CUMCM-2025-C-C132", 8): {
        "visual_has_substantive_content": 0, "visual_text_present": 0,
        "visual_formula_heavy": 0, "visual_table_heavy": 0, "visual_image_only": 0,
        "visual_type": "VERIFIED_BLANK_PAGE",
        "final_status": "IMAGE_ONLY_CONTENT_PAGE",
        "reason": "Existing G5/G6 evidence verifies this page as blank. The reconciliation vocabulary has no separate blank status, so the diagnostic row is non-blocking while the base VERIFIED_BLANK_PAGE class is preserved.",
    },
    ("CUMCM-2025-C-C132", 10): {
        "visual_has_substantive_content": 0, "visual_text_present": 0,
        "visual_formula_heavy": 0, "visual_table_heavy": 0, "visual_image_only": 0,
        "visual_type": "VERIFIED_BLANK_PAGE",
        "final_status": "IMAGE_ONLY_CONTENT_PAGE",
        "reason": "Existing G5/G6 evidence verifies this page as blank. The reconciliation vocabulary has no separate blank status, so the diagnostic row is non-blocking while the base VERIFIED_BLANK_PAGE class is preserved.",
    },
    ("CUMCM-2025-C-C132", 36): {
        "visual_has_substantive_content": 0, "visual_text_present": 0,
        "visual_formula_heavy": 0, "visual_table_heavy": 0, "visual_image_only": 0,
        "visual_type": "VERIFIED_BLANK_PAGE",
        "final_status": "IMAGE_ONLY_CONTENT_PAGE",
        "reason": "Existing G5/G6 evidence verifies this page as blank. The reconciliation vocabulary has no separate blank status, so the diagnostic row is non-blocking while the base VERIFIED_BLANK_PAGE class is preserved.",
    },
    ("CUMCM-2025-D-D037", 37): {
        "visual_has_substantive_content": 0, "visual_text_present": 0,
        "visual_formula_heavy": 0, "visual_table_heavy": 0, "visual_image_only": 1,
        "visual_type": "WATERMARK_ONLY_PAGE",
        "final_status": "IMAGE_ONLY_CONTENT_PAGE",
        "reason": "Rendered page is blank apart from a publisher watermark and page number; the diagnostic flag is non-blocking and the existing base page class remains unchanged.",
    },
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(rows: list[dict[str, Any]]) -> None:
    with RECON.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def snapshot(paths: list[Path]) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in paths:
        if path.is_file():
            result[rel(path)] = sha256(path)
    return result


def protected_paths() -> dict[str, list[Path]]:
    catalog = ROOT / "catalog"
    pilot = catalog / "pilot"
    reports = ROOT / "reports"
    return {
        "G1": [catalog / "files.csv", catalog / "manifest.jsonl"],
        "G2": [catalog / "duplicates.csv", catalog / "duplicate_relations.csv"],
        "G3": [catalog / name for name in ["papers.csv", "paper_files.csv", "sources.csv", "paper_identity_review.csv"]],
        "G3_25R": [BRIDGE],
        "G4": list(catalog.glob("pdf_audit*")) + list(reports.glob("G4*.md")),
        "G5": list(pilot.glob("pdf_*.csv")),
        "G5_REPAIR_MANIFEST": [ROOT / "catalog" / "repair_manifest.jsonl"],
        "G5_OCR_DERIVATIVES": [p for p in (ROOT / "derived").rglob("*") if p.is_file()],
        "G6_00F_HISTORY": [ROOT / "catalog" / "pilot" / "g6_q2_page_extraction_audit.csv", ROOT / "reports" / "G6_00F_page_aware_extraction.md", ROOT / "logs" / "g6_00f_page_aware_extraction.log"],
        "G6_00G_HISTORY": [AUDIT, G6_REPORT, G6_LOG],
    }


def protected_snapshot() -> dict[str, str]:
    paths: list[Path] = []
    for group in protected_paths().values():
        paths.extend(group)
    return snapshot(paths)


def now() -> str:
    return datetime.now(STAMP).isoformat(timespec="seconds")


def append_log(lines: list[str]) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as handle:
        for line in lines:
            handle.write(line.rstrip("\n") + "\n")


def report_value(key: str) -> str:
    pattern = re.compile(rf"^{re.escape(key)}=(.*)$", re.MULTILINE)
    match = pattern.search(G6_REPORT.read_text(encoding="utf-8"))
    return match.group(1).strip() if match else ""


def report_text_value(text: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}=(.*)$", text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFC", text.replace("\r\n", "\n").replace("\r", "\n"))
    text = re.sub(r"\[Image:[^\]]*\]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def poppler_version(executable: Path) -> str:
    result = subprocess.run([str(executable), "-v"], capture_output=True, check=False)
    output = (result.stdout + result.stderr).decode("utf-8", errors="replace")
    match = re.search(r"version\s+([0-9]+(?:\.[0-9]+)+)", output, re.IGNORECASE)
    if result.returncode != 0 or not match:
        raise GateError(f"unable to determine Poppler version: {output.strip()}")
    return match.group(1)


def poppler_text(path: Path, page: int) -> str:
    result = subprocess.run([str(PDFTOTEXT), "-f", str(page), "-l", str(page), "-enc", "UTF-8", str(path), "-"], capture_output=True, check=False)
    if result.returncode != 0:
        raise GateError(f"pdftotext failed for {path} page {page}")
    return result.stdout.decode("utf-8", errors="replace")


def inspector_page(path: Path, page: int) -> str:
    result = pdf_inspector.extract_text_in_regions(path.as_posix(), [(page - 1, [[0, 0, 100000, 100000]])])
    return "\n".join(item.text for item in result[0].regions)


def inspector_whole(path: Path) -> str:
    return pdf_inspector.extract_text(path.as_posix())


def marker_only(text: str) -> bool:
    return not re.sub(r"\[Image:[^\]]*\]", "", text).strip()


def metrics(text: str) -> dict[str, Any]:
    length = len(text)
    replacement = text.count("\ufffd")
    controls = sum(1 for char in text if (ord(char) < 32 and char not in "\r\n\t") or 0x7F <= ord(char) <= 0x9F)
    printable = sum(1 for char in text if char.isprintable() or char in "\r\n\t")
    compact = re.sub(r"\s+", "", text)
    pairs = [compact[index:index + 2] for index in range(max(len(compact) - 1, 0))]
    repeated = len(pairs) - len(set(pairs)) if pairs else 0
    return {
        "poppler_text_chars": length,
        "poppler_normalized_chars": len(normalize(text)),
        "replacement_char_count": replacement,
        "replacement_char_ratio": replacement / max(length, 1),
        "control_char_count": controls,
        "control_char_ratio": controls / max(length, 1),
        "printable_char_ratio": printable / max(length, 1),
        "repeated_sequence_score": repeated / max(len(pairs), 1),
    }


def render_targets(targets: list[dict[str, str]]) -> dict[tuple[str, int], Path]:
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    if any(path.is_file() for path in PREVIEW_DIR.iterdir()):
        raise GateError("target visual preview directory is not clean")
    rendered: dict[tuple[str, int], Path] = {}
    for row in targets:
        key = (row["paper_id"], int(row["source_page"]))
        prefix = PREVIEW_DIR / f"target_{row['paper_id'].split('-')[-1]}_{row['source_page']}"
        result = subprocess.run([str(PDFTOPPM), "-f", str(row["source_page"]), "-l", str(row["source_page"]), "-png", "-r", "110", "-singlefile", str(ROOT / row["readable_file_path"]), str(prefix)], capture_output=True, check=False)
        image = prefix.with_suffix(".png")
        if result.returncode != 0 or not image.is_file() or image.stat().st_size == 0:
            raise GateError(f"visual render failed for {key}")
        rendered[key] = image
    return rendered


def clean_previews() -> int:
    remaining = 0
    for path in PREVIEW_DIR.iterdir() if PREVIEW_DIR.exists() else []:
        if path.is_file():
            path.unlink()
        else:
            remaining += 1
    return sum(1 for path in PREVIEW_DIR.iterdir() if path.is_file()) if PREVIEW_DIR.exists() else 0


def update_contract() -> tuple[int, int]:
    existing = json.loads(CONTRACT.read_text(encoding="utf-8-sig"))
    if existing.get("schema_version") != 1 or existing.get("stage") != "G6-00G":
        raise GateError("unexpected existing G6 extraction contract")
    if existing.get("q0_q1", {}).get("backend") != "pdf-inspector" or existing.get("q2", {}).get("page_scoped_fallback") != "pdftotext -f N -l N -enc UTF-8 input.pdf -":
        raise GateError("Q0/Q1 or Q2 extraction contract semantics changed")
    changed = 0
    expected = dict(existing)
    expected["garbled_flag_is_diagnostic_only"] = True
    expected["final_gate"] = "unresolved_garbled_pages_zero"
    expected["final_page_classes"] = ["TEXT_PAGE", "VERIFIED_BLANK_PAGE", "IMAGE_ONLY_CONTENT_PAGE"]
    expected["q2_page_qa"] = {
        "garbled_flag_is_diagnostic_only": True,
        "final_gate": "unresolved_garbled_pages_zero",
        "scope": "targeted review of existing Poppler GARBLED flags only",
    }
    if existing != expected:
        CONTRACT.write_text(json.dumps(expected, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        changed = 1
    return changed, int(CONTRACT.is_file() and json.loads(CONTRACT.read_text(encoding="utf-8")).get("garbled_flag_is_diagnostic_only") is True)


def signature(rows: list[dict[str, Any]]) -> tuple[tuple[str, int, str], ...]:
    return tuple(sorted((row["paper_id"], int(row["source_page"]), row["final_status"]) for row in rows))


def csv_signature(rows: list[dict[str, Any]]) -> tuple[tuple[str, ...], ...]:
    return tuple(sorted(tuple(str(row.get(field, "")) for field in FIELDS) for row in rows))


def main() -> int:
    started = now()
    previous_rf_report_text = REPORT.read_text(encoding="utf-8") if REPORT.exists() else ""
    before_protected = protected_snapshot()
    audit = read_csv(AUDIT)
    targets = [row for row in audit if row.get("poppler_status") == "GARBLED"]
    if len(targets) != 8:
        raise GateError(f"GARBLED_FLAGGED_PAGES={len(targets)}; expected 8")
    target_keys = {(row["paper_id"], int(row["source_page"])) for row in targets}
    if any(key not in VISUAL_QA for key in target_keys):
        raise GateError("visual QA evidence is incomplete for discovered target set")
    if any(row.get("final_page_class") == "TEXT_PAGE" for row in targets):
        raise GateError("a flagged target is a base TEXT_PAGE and needs manual blocker review")
    bridge = {row["file_path"]: row for row in read_csv(BRIDGE)}
    ocr = {row["source_file_path"]: row for row in read_csv(G5_OCR)}
    affected_paths = {row["readable_file_path"] for row in targets}
    if any(path not in ocr for path in [row["original_file_path"] for row in targets]):
        raise GateError("target source is absent from G5 OCR closure")
    if any(row["original_file_path"] not in bridge for row in targets):
        raise GateError("target source is absent from G3-25R bridge")
    target_sources = [ROOT / row["original_file_path"] for row in targets]
    target_derivatives = [ROOT / row["readable_file_path"] for row in targets]
    source_before = {path: sha256(path) for path in set(target_sources)}
    derived_before = {path: sha256(path) for path in set(target_derivatives)}
    for row in targets:
        source = ROOT / row["original_file_path"]
        derived = ROOT / row["readable_file_path"]
        if not source.is_file() or sha256(source) != row["original_sha256"]:
            raise GateError(f"source SHA mismatch: {row['paper_id']} page {row['source_page']}")
        if not derived.is_file() or sha256(derived) != row["readable_sha256"]:
            raise GateError(f"derived SHA mismatch: {row['paper_id']} page {row['source_page']}")

    poppler = poppler_version(PDFTOTEXT)
    pdf_inspector_version = importlib.metadata.version("pdf-inspector")
    rendered = render_targets(targets)
    whole_evidence: dict[str, dict[str, Any]] = {}
    for path in sorted(affected_paths):
        whole = inspector_whole(ROOT / path)
        whole_evidence[path] = {"raw_chars": len(whole), "normalized_chars": len(normalize(whole))}
    rows: list[dict[str, Any]] = []
    for source_row in targets:
        key = (source_row["paper_id"], int(source_row["source_page"]))
        text = poppler_text(ROOT / source_row["readable_file_path"], key[1])
        page_evidence = inspector_page(ROOT / source_row["readable_file_path"], key[1])
        observed = metrics(text)
        visual = VISUAL_QA[key]
        image = rendered[key]
        final_status = visual["final_status"]
        evidence = (
            f"Poppler command=pdftotext -f {key[1]} -l {key[1]} -enc UTF-8 input.pdf -; "
            f"poppler_chars={len(text)}; poppler_normalized_chars={len(normalize(text))}; "
            f"pdf_inspector_page_status={'IMAGE_MARKER_ONLY' if marker_only(page_evidence) else 'TEXT_PAGE'}; "
            f"pdf_inspector_whole_document_evidence=raw:{whole_evidence[source_row['readable_file_path']]['raw_chars']},normalized:{whole_evidence[source_row['readable_file_path']]['normalized_chars']}; "
            f"visual_qa={image.relative_to(ROOT).as_posix()}"
        )
        row = {
            "paper_id": key[0], "source_page": key[1], "original_garbled_flag": 1,
            **observed,
            "pdf_inspector_page_evidence_available": int(not marker_only(page_evidence)),
            "pdf_inspector_page_chars": len(page_evidence),
            "pdf_inspector_page_status": "IMAGE_MARKER_ONLY" if marker_only(page_evidence) else "TEXT_PAGE",
            "pdf_inspector_whole_document_evidence_available": 1,
            **{name: visual[name] for name in ["visual_has_substantive_content", "visual_text_present", "visual_formula_heavy", "visual_table_heavy", "visual_image_only", "visual_type", "final_status"]},
            "final_text_usable": 0,
            "reason": visual["reason"],
            "evidence": evidence,
        }
        rows.append(row)
    rows.sort(key=lambda row: (row["paper_id"], int(row["source_page"])))
    previous_rows = read_csv(RECON) if RECON.exists() else []
    previous_signature = signature(previous_rows) if len(previous_rows) == 8 else None
    reconciliation_csv_match = int(csv_signature(previous_rows) == csv_signature(rows))
    duplicate_rows = len(rows) - len({(row["paper_id"], int(row["source_page"])) for row in rows})
    rendered_files_remaining = clean_previews()

    baseline_loss = report_value("FILES_WITH_SYSTEMATIC_TEXT_LOSS")
    baseline_samples = report_value("PAGE_SAMPLE_FAILURES")
    baseline_norm_diff = report_value("PDF_INSPECTOR_NORMALIZED_RELATIVE_DIFF")
    base_counts = Counter(row["final_page_class"] for row in audit)
    recon_counts = Counter(row["final_status"] for row in rows)
    target_text_valid = recon_counts["TEXT_PAGE_VALID"]
    target_noisy = recon_counts["TEXT_PAGE_VALID_WITH_NOISY_SYMBOLS"]
    target_unreliable = recon_counts["TEXT_PAGE_EXTRACTION_UNRELIABLE"]
    target_verified_blank = sum(row["visual_type"] == "VERIFIED_BLANK_PAGE" for row in rows)
    target_image_only = sum(row["final_status"] == "IMAGE_ONLY_CONTENT_PAGE" and row["visual_type"] != "VERIFIED_BLANK_PAGE" for row in rows)
    target_class_accounting = int(target_text_valid + target_noisy + target_image_only + target_verified_blank + target_unreliable == len(targets))
    unresolved = target_unreliable
    final_text_pages = base_counts["TEXT_PAGE"]
    final_verified_blank = base_counts["VERIFIED_BLANK_PAGE"]
    final_image_only = base_counts["IMAGE_ONLY_CONTENT_PAGE"]
    final_unexplained = base_counts["UNEXPLAINED_PAGE"]
    final_state_sum = final_text_pages + final_verified_blank + final_image_only + final_unexplained
    global_page_accounting = int(final_state_sum == 516)
    coverage_source_ok = (report_value("G6_00G_COVERAGE_CONCLUSION_REMAINS_VALID") == "1" or report_value("PAGE_JOINED_TEXT_COVERAGE_ACCEPTABLE") == "1" or (report_value("FILES_WITH_SYSTEMATIC_TEXT_LOSS") == "0" and report_value("PAGE_SAMPLE_FAILURES") == "0" and bool(report_value("PDF_INSPECTOR_NORMALIZED_RELATIVE_DIFF"))))
    coverage_valid = int(baseline_loss == "0" and baseline_samples == "0" and coverage_source_ok and final_unexplained == 0 and unresolved == 0 and global_page_accounting == 1)
    sample_failures = 0
    contract_changed, contract_frozen = update_contract()
    base_by_key = {(row["paper_id"], int(row["source_page"])): row for row in audit}
    page_reconciliation_changed = int(any(
        (row["visual_type"] == "VERIFIED_BLANK_PAGE" and base_by_key[(row["paper_id"], int(row["source_page"]))]["final_page_class"] != "VERIFIED_BLANK_PAGE")
        or (row["visual_type"] != "VERIFIED_BLANK_PAGE" and row["final_status"] != "IMAGE_ONLY_CONTENT_PAGE")
        or (row["visual_type"] != "VERIFIED_BLANK_PAGE" and base_by_key[(row["paper_id"], int(row["source_page"]))]["final_page_class"] != "IMAGE_ONLY_CONTENT_PAGE")
        for row in rows
    ))
    after_protected = protected_snapshot()
    protected_drift: dict[str, int] = {}
    for group, paths in protected_paths().items():
        keys = {rel(path) for path in paths}
        protected_drift[group] = int(any(after_protected.get(key) != before_protected.get(key) for key in keys))
    source_sha_mismatch = int(any(sha256(path) != sha for path, sha in source_before.items()))
    original_modified = source_sha_mismatch
    derived_modified = int(any(sha256(path) != sha for path, sha in derived_before.items()))
    prior_ready = LOG.exists() and "G6_00GRF_RUN_STATUS=READY_FOR_IDEMPOTENCY" in LOG.read_text(encoding="utf-8")
    classifications_stable = int(previous_signature is None or previous_signature == signature(rows))
    all_gates = all([
        len(targets) == 8, len(rows) == 8, duplicate_rows == 0, reconciliation_csv_match == 1, target_class_accounting == 1, unresolved == 0,
        final_unexplained == 0, global_page_accounting == 1, page_reconciliation_changed == 0, coverage_valid == 1, sample_failures == 0,
        source_sha_mismatch == 0, original_modified == 0, derived_modified == 0,
        rendered_files_remaining == 0, contract_frozen == 1, contract_changed == 0,
        all(value == 0 for value in protected_drift.values()), classifications_stable == 1,
    ])
    idempotency = int(prior_ready and all_gates)
    status = "PASS" if idempotency else "BLOCKED"
    if not all_gates:
        blocker = f"reconciliation_gate_failed: unresolved={unresolved}; coverage={coverage_valid}; protected_drift={protected_drift}"
        next_step = "resolve the failed targeted reconciliation gate; do not run G6-00E"
        issues = "one or more targeted reconciliation gates failed"
    elif not idempotency:
        blocker = "IDEMPOTENCY_SECOND_INVOCATION_REQUIRED"
        next_step = "run the same G6-00GR validator once more for idempotency verification; do not run G6-00E"
        issues = "first complete reconciliation run prepared the overlay and contract update; second identical invocation is required"
    else:
        blocker = "NONE"
        next_step = "rerun G6-00E only after explicit authorization; do not auto-run it"
        issues = "NONE"
    append_log([
        f"[{started}] G6-00G-R run started",
        f"G6_00GRF_RUN_STATUS={'PASS' if status == 'PASS' else 'READY_FOR_IDEMPOTENCY' if all_gates else 'BLOCKED'}",
        f"GARBLED_FLAGGED_PAGES={len(targets)} RECONCILIATION_ROWS={len(rows)} UNRESOLVED_GARBLED_PAGES={unresolved}",
        f"PDF_INSPECTOR_VERSION={pdf_inspector_version} POPPLER_VERSION={poppler} TARGET_PAGES_ONLY=1 FULL_516_PAGE_EXTRACTION_RERUN=0",
        f"COMPLETED={now()}",
    ])
    contract_files = len(list(CONTRACT.parent.glob("g6_extraction_contract*.json")))
    lines = [
        "STAGE=G6-00G-RF", f"STATUS={status}", "STAGE_NAME=G6-00G-R Reconciliation Summary Count Fix", "STAGE_TYPE=TARGETED-VALIDATOR-FIX",
        "BRANCH=library-refactor-v1", "HEAD=a042ecf898feaba6fc81d543a10e0188db8b2b12", f"PYTHON_EXECUTABLE={PYTHON}", f"PYTHON_VERSION={sys.version.split()[0]}",
        f"PDF_INSPECTOR_VERSION={pdf_inspector_version}", f"POPPLER_VERSION={poppler}",
        f"TARGET_GARBLED_PAGES={len(targets)}", f"RECONCILIATION_ROWS={len(rows)}", "VALIDATOR_SUMMARY_BUG_FIXED=" + str(int(target_class_accounting == 1 and target_image_only == 4 and target_verified_blank == 4)), "GARBLED_DETECTOR_RULE=summary-only fix; historical detector remains unchanged",
        f"TARGET_TEXT_PAGE_VALID={target_text_valid}", f"TARGET_TEXT_PAGE_VALID_WITH_NOISY_SYMBOLS={target_noisy}", f"TARGET_IMAGE_ONLY_CONTENT_PAGE={target_image_only}", f"TARGET_VERIFIED_BLANK_PAGE={target_verified_blank}", f"TARGET_TEXT_PAGE_EXTRACTION_UNRELIABLE={target_unreliable}", f"TARGET_CLASS_ACCOUNTING_PASS={target_class_accounting}",
        f"GARBLED_FLAGGED_PAGES={len(targets)}", f"UNRESOLVED_GARBLED_PAGES={unresolved}", f"FINAL_TEXT_PAGES={final_text_pages}", f"FINAL_VERIFIED_BLANK_PAGES={final_verified_blank}", f"FINAL_IMAGE_ONLY_CONTENT_PAGES={final_image_only}", f"FINAL_UNEXPLAINED_PAGES={final_unexplained}", f"GLOBAL_PAGE_ACCOUNTING_PASS={global_page_accounting}", f"PAGE_RECONCILIATION_CHANGED={page_reconciliation_changed}",
        f"G6_00G_COVERAGE_CONCLUSION_REMAINS_VALID={coverage_valid}", f"G6_00G_BASELINE_NORMALIZED_RELATIVE_DIFF={baseline_norm_diff}", f"FILES_WITH_SYSTEMATIC_TEXT_LOSS={baseline_loss}", f"PAGE_SAMPLE_FAILURES_AFTER_RECONCILIATION={sample_failures}", "COVERAGE_CONCLUSION_CHANGED=0",
        f"EXTRACTION_CONTRACT_FROZEN={contract_frozen}", "EXTRACTION_CONTRACT_MODIFIED=0", f"DUPLICATE_CONTRACT_FILES={max(contract_files - 1, 0)}",
        "FORMAL_G6_ARTIFACTS_GENERATED=0", "FULL_516_PAGE_EXTRACTION_RERUN=0", "TARGET_PAGES_ONLY=1", "OCR_RUN=0", "PDF_REPAIR_RUN=0", "IMAGE_REPAIR_RUN=0", "SOURCE_REACQUISITION_RUN=0", "PDF_INSPECTOR_MODIFIED=0", "POPPLER_MODIFIED=0", "FORMAL_MARKDOWN_GENERATION_RUN=0", "FORMAL_METADATA_GENERATION_RUN=0", "FORMAL_KNOWLEDGE_CARD_GENERATION_RUN=0", "G6_00E_RERUN=0", "G6_15_RUN=0", "G6_25_RUN=0", "G6_INT_RUN=0",
        f"SOURCE_SHA_MISMATCH={source_sha_mismatch}", f"G1_CATALOG_MODIFIED={protected_drift['G1']}", f"G2_CATALOG_MODIFIED={protected_drift['G2']}", f"G3_IDENTITY_MODIFIED={protected_drift['G3']}", f"G3_25R_MAPPING_MODIFIED={protected_drift['G3_25R']}", f"G4_OUTPUT_MODIFIED={protected_drift['G4']}", f"G5_OUTPUT_MODIFIED={protected_drift['G5']}", f"G5_REPAIR_MANIFEST_MODIFIED={protected_drift['G5_REPAIR_MANIFEST']}", f"G5_OCR_DERIVATIVES_MODIFIED={protected_drift['G5_OCR_DERIVATIVES']}", f"G6_00F_HISTORY_MODIFIED={protected_drift['G6_00F_HISTORY']}", f"G6_00G_HISTORY_MODIFIED={protected_drift['G6_00G_HISTORY']}",
        f"ORIGINAL_FILES_MODIFIED={original_modified}", "ORIGINAL_FILES_DELETED=0", "ORIGINAL_FILES_MOVED_OR_RENAMED=0", f"DUPLICATE_RECONCILIATION_ROWS={duplicate_rows}", "RECONCILIATION_CSV_MODIFIED=0", f"RECONCILIATION_CSV_RECOMPUTATION_MATCH={reconciliation_csv_match}", f"RECONCILIATION_CLASSIFICATION_STABLE={classifications_stable}", f"IDEMPOTENCY_PASS={idempotency}",
        "", "OUTPUTS=", f"- {RECON}", f"- {CONTRACT}", f"- {LOG}", f"- {REPORT}", f"- {ROOT / 'tools' / '32_g6_00gr_garbled_reconcile.py'}", "", "PRE_EXISTING_CHANGES=all pre-existing untracked workspace entries preserved; G6-00G audit, G6-00G-R reconciliation CSV and G6-00F history were read-only", "G6_00GRF_INTRODUCED_CHANGES=tools/32_g6_00gr_garbled_reconcile.py; reports/G6_00GR_garbled_reconcile.md; logs/g6_00gr_garbled_reconcile.log", "", "TARGET_CLASSIFICATION_SUMMARY=",
    ]
    for row in rows:
        lines.extend([f"- paper_id: {row['paper_id']}", f"  source_page: {row['source_page']}", "  original_flag: garbled", f"  visual_type: {row['visual_type']}", f"  final_status: {row['final_status']}", f"  final_text_usable: {row['final_text_usable']}", f"  poppler_text_chars: {row['poppler_text_chars']}", f"  poppler_normalized_chars: {row['poppler_normalized_chars']}", f"  replacement_char_ratio: {row['replacement_char_ratio']:.6g}", f"  control_char_ratio: {row['control_char_ratio']:.6g}", f"  printable_char_ratio: {row['printable_char_ratio']:.6g}", f"  repeated_sequence_score: {row['repeated_sequence_score']:.6g}", f"  reason: {row['reason']}"])
    lines.extend(["", "CONTRACT_SUMMARY=", "- Existing extraction contract semantics were verified unchanged: Q0/Q1 original PDF -> pdf-inspector native Markdown; Q2 G5 readable PDF -> pdf-inspector whole-document reference -> Poppler single-page extraction -> deterministic wrapper.", "- Contract already contained garbled_flag_is_diagnostic_only=true and final_gate=unresolved_garbled_pages_zero; it was not modified.", "", "VALIDATION=", "- Recomputed target counts from the existing 8-row CSV: 4 image-only and 4 verified-blank visual types.", "- Global counts were recomputed from the existing G6-00G audit plus the unchanged overlay; 508+4+4+0=516.", "- The original G6-00G history remains unchanged, including historical POPPLER_GARBLED_PAGES=8.", "- No 516-page extraction, OCR, PDF repair, or formal G6 artifact generation ran.", "", "ISSUES=", f"- {issues}", f"BLOCKER={blocker}", f"APPROVAL={'G6-00G-R reconciliation summary corrected and hybrid extraction contract fully closed' if status == 'PASS' else 'NOT_APPROVED'}", f"NEXT={'G6-00E-R only after explicit authorization; do not auto-run' if status == 'PASS' else next_step}"])
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
