"""G11 marker-only residual scope diagnostic.

This is a read-only diagnostic of the residual G11 marker-only page scope.
It invokes the frozen Poppler pdftotext executable once per source page with
an exact ``-f N -l N`` boundary.  It does not run OCR, render PDFs, mutate
formal artifacts, or update any governance decision sheet.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCALE = ROOT / "catalog" / "scale"
REPORTS = ROOT / "reports" / "scale"
PDFTOTEXT = Path(r"D:\texlive\2026\bin\windows\pdftotext.exe")
PDFINFO = Path(r"D:\texlive\2026\bin\windows\pdfinfo.exe")
UPSTREAM_RESULT = SCALE / "g11_marker_only_scope_confirmation_result.json"
RESIDUAL_INPUT = SCALE / "g11_marker_only_residual_visual_input.csv"
SCOPE_INPUT = SCALE / "g11_marker_only_scope_confirmation.csv"
CONFIRMED_TARGETS = SCALE / "g11_marker_only_confirmed_repair_targets.csv"
TARGET_DECISIONS = SCALE / "g11_targeted_visual_diagnostic_decisions.csv"
DEEP_PAGE = SCALE / "g11_marker_only_page_deep_diagnostic.csv"
DEEP_RESULT = SCALE / "g11_major_defect_deep_diagnostic_result.json"
VISUAL_APPROVAL = SCALE / "g11_targeted_visual_diagnostic_approval_result.json"
DIAGNOSTIC_CSV = SCALE / "g11_marker_only_residual_scope_diagnostic.csv"
IMAGE_RESIDUAL_CSV = SCALE / "g11_marker_only_image_residual_input.csv"
RESULT_JSON = SCALE / "g11_marker_only_residual_scope_diagnostic_result.json"
REPORT = REPORTS / "G11_MARKER_ONLY_RESIDUAL_SCOPE_DIAGNOSTIC.md"
RESIDUAL_TEXT_DIR = SCALE / "g11_residual_pdftotext_pages"
CALIBRATION_DIR = SCALE / "g11_residual_pdftotext_calibration"
FORMAL_ELIGIBILITY = SCALE / "g8_artifact_eligibility.csv"
FORMAL_ARTIFACT_MANIFEST = SCALE / "g8_artifact_manifest.csv"
FORMAL_INDEX = SCALE / "g9_paper_index.csv"
DOC_MANUAL_BACKLOG = SCALE / "g8_manual_backlog.csv"
Q3_MANUAL_BACKLOG = SCALE / "g8_q3_manual_backlog.csv"
STAMP = timezone(timedelta(hours=8))
PROBE_TIMEOUT_SECONDS = 60
MAX_WORKERS = 8

DIAGNOSTIC_FIELDS = [
    "paper_id", "year", "problem", "source_page", "source_path",
    "source_sha256", "artifact_set_id", "formal_body_path",
    "formal_body_sha256", "prior_scope_status", "pdftotext_probe_status",
    "pdftotext_output_path", "pdftotext_output_sha256", "raw_char_count",
    "normalized_char_count", "normalized_line_count",
    "substantive_text_detected", "substantive_detection_basis",
    "text_probe_classification", "new_scope_status", "scope_confidence",
    "residual_class", "requires_render", "requires_ocr", "notes",
]


class GateError(RuntimeError):
    pass


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_current_formal_baseline() -> dict[str, int]:
    """Read the live formal baseline instead of carrying a historical snapshot."""
    eligibility = read_csv(FORMAL_ELIGIBILITY)
    manifest = read_csv(FORMAL_ARTIFACT_MANIFEST)
    index = read_csv(FORMAL_INDEX)
    doc_backlog = read_csv(DOC_MANUAL_BACKLOG)
    q3_backlog = read_csv(Q3_MANUAL_BACKLOG)
    if len({row.get("paper_id", "") for row in eligibility}) != len(eligibility):
        raise GateError("CURRENT_FORMAL_BASELINE_DUPLICATE_IDENTITY")
    eligible = [row for row in eligibility if row.get("artifact_eligible") == "1"]
    ineligible = [row for row in eligibility if row.get("artifact_eligible") == "0"]
    artifact_sets = {row.get("paper_id", "") for row in manifest}
    if any(row.get("subject_type") == "PROBLEM_PACKAGE" for row in eligibility + manifest + index):
        raise GateError("CURRENT_FORMAL_BASELINE_PROBLEM_PACKAGE_LEAK")
    return {
        "formal_identities": len(eligibility),
        "eligible_identities": len(eligible),
        "ineligible_identities": len(ineligible),
        "artifact_sets": len(artifact_sets),
        "primary_artifacts": len(manifest),
        "formal_index_records": len(index),
        "doc_manual_backlog": len(doc_backlog),
        "q3_manual_backlog": len(q3_backlog),
        "total_manual_backlog": len(doc_backlog) + len(q3_backlog),
    }


def write_csv(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


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


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def now() -> str:
    return datetime.now(STAMP).isoformat(timespec="seconds")


def git_value(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False)
    if result.returncode != 0:
        raise GateError(f"GIT_READ_FAILED={' '.join(args)}")
    return result.stdout.decode("utf-8", errors="replace").strip()


def key(row: dict[str, Any]) -> tuple[str, int]:
    return (str(row["paper_id"]), int(row["source_page"]))


def identity(row: dict[str, Any]) -> str:
    return str(row["paper_id"])


def assert_unique(rows: list[dict[str, Any]], label: str) -> set[tuple[str, int]]:
    keys = [key(row) for row in rows]
    if len(keys) != len(set(keys)):
        raise GateError(f"{label}_DUPLICATE_PAGE_KEYS")
    return set(keys)


def normalize_text(text: str) -> str:
    """Normalize only line endings, Unicode form, and repeated blank lines."""
    text = unicodedata.normalize("NFC", text.replace("\r\n", "\n").replace("\r", "\n"))
    lines = text.split("\n")
    normalized: list[str] = []
    previous_blank = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if not previous_blank:
                normalized.append("")
            previous_blank = True
            continue
        normalized.append(stripped)
        previous_blank = False
    while normalized and normalized[0] == "":
        normalized.pop(0)
    while normalized and normalized[-1] == "":
        normalized.pop()
    return "\n".join(normalized)


def looks_like_page_noise(line: str) -> bool:
    compact = re.sub(r"\s+", "", line)
    if not compact:
        return True
    if re.fullmatch(r"[\-—–_·•.]*\d+[\-—–_·•.]*", compact):
        return True
    if re.fullmatch(r"(?:page|p)\.?\d+", compact, flags=re.IGNORECASE):
        return True
    if re.fullmatch(r"\d+[/／]\d+", compact):
        return True
    if re.fullmatch(r"https?://\S+|www\.\S+", compact, flags=re.IGNORECASE):
        return True
    return False


def has_unreliable_encoding(text: str) -> bool:
    if "\ufffd" in text or "\x00" in text:
        return True
    if any(0x80 <= ord(char) <= 0x9F for char in text):
        return True
    controls = sum(
        1 for char in text
        if ord(char) < 32 and char not in "\r\n\t"
    )
    return controls > 0


def classify_text(raw: str, probe_status: str) -> dict[str, Any]:
    normalized = normalize_text(raw)
    lines = [line for line in normalized.split("\n") if line and not looks_like_page_noise(line)]
    content = "\n".join(lines)
    cjk = len(re.findall(r"[\u3400-\u9fff]", content))
    letters = len(re.findall(r"[A-Za-z]", content))
    words = re.findall(r"[A-Za-z]{2,}", content)
    digits = len(re.findall(r"\d", content))
    lexical = cjk + letters

    if probe_status == "TIMEOUT":
        classification = "TEXT_PROBE_TIMEOUT"
        basis = "pdftotext did not complete within the 60-second per-page timeout."
        substantive = 0
    elif probe_status == "ERROR":
        classification = "TEXT_PROBE_ERROR"
        basis = "pdftotext returned a non-zero exit status for the exact source page probe."
        substantive = 0
    elif has_unreliable_encoding(raw):
        classification = "TEXT_LAYER_GARBLED_OR_UNRELIABLE"
        basis = "The page-scoped output contains replacement, NUL, C1, or other control characters."
        substantive = 0
    elif lexical >= 8 and ((cjk >= 8 and (len(content) >= 20 or len(lines) >= 2)) or (letters >= 20 and len(words) >= 3)):
        classification = "TEXT_LAYER_SUBSTANTIVE"
        basis = (
            f"Conservative lexical test met: cjk_chars={cjk}, alphabetic_chars={letters}, "
            f"word_tokens={len(words)}, digits={digits}, non_noise_lines={len(lines)}."
        )
        substantive = 1
    elif lexical >= 12 and len(content) >= 30 and len(lines) >= 2:
        classification = "TEXT_LAYER_SUBSTANTIVE"
        basis = (
            f"Conservative multi-line lexical test met: lexical_chars={lexical}, "
            f"non_noise_lines={len(lines)}, normalized_chars={len(normalized)}."
        )
        substantive = 1
    else:
        classification = "TEXT_LAYER_NON_SUBSTANTIVE_OR_EMPTY"
        if not normalized:
            basis = "The exact page-scoped pdftotext output is empty after conservative normalization."
        elif not content:
            basis = "The output contains only blank lines or obvious page-number/URL noise after normalization."
        else:
            basis = (
                f"Conservative substantive threshold not met: cjk_chars={cjk}, "
                f"alphabetic_chars={letters}, word_tokens={len(words)}, "
                f"non_noise_lines={len(lines)}; this is not treated as legitimate blank evidence."
            )
        substantive = 0
    return {
        "normalized": normalized,
        "normalized_line_count": len(normalized.split("\n")) if normalized else 0,
        "substantive_text_detected": substantive,
        "substantive_detection_basis": basis,
        "text_probe_classification": classification,
    }


def pdfinfo_page_count(path: Path) -> int | None:
    if not PDFINFO.is_file():
        return None
    result = subprocess.run([str(PDFINFO), str(path)], capture_output=True, check=False)
    output = (result.stdout + result.stderr).decode("utf-8", errors="replace")
    match = re.search(r"^Pages:\s*(\d+)", output, flags=re.MULTILINE)
    return int(match.group(1)) if result.returncode == 0 and match else None


def probe_page(row: dict[str, Any], output_root: Path) -> dict[str, Any]:
    source = ROOT / str(row["source_path"])
    page = int(row["source_page"])
    output_path = output_root / str(row["paper_id"]) / f"source_page_{page}.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    stdout = b""
    stderr = b""
    probe_status = "SUCCESS"
    return_code = 0
    try:
        completed = subprocess.run(
            [str(PDFTOTEXT), "-f", str(page), "-l", str(page), "-enc", "UTF-8", str(source), "-"],
            capture_output=True,
            timeout=PROBE_TIMEOUT_SECONDS,
            check=False,
        )
        stdout = completed.stdout
        stderr = completed.stderr
        return_code = completed.returncode
        if return_code != 0:
            probe_status = "ERROR"
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or b""
        stderr = exc.stderr or b""
        probe_status = "TIMEOUT"
        return_code = -1
    raw = stdout.decode("utf-8", errors="replace")
    output_path.write_text(raw, encoding="utf-8", newline="\n")
    classification = classify_text(raw, probe_status)
    classification["probe_status"] = probe_status
    classification["return_code"] = return_code
    classification["raw"] = raw
    classification["raw_char_count"] = len(raw)
    classification["stderr"] = stderr.decode("utf-8", errors="replace").strip()
    classification["output_path"] = output_path
    classification["output_sha256"] = sha256(output_path)
    return classification


def run_probes(rows: list[dict[str, Any]], output_root: Path) -> list[dict[str, Any]]:
    results: list[dict[str, Any] | None] = [None] * len(rows)
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(probe_page, row, output_root): index for index, row in enumerate(rows)}
        completed_count = 0
        for future in as_completed(futures):
            index = futures[future]
            results[index] = future.result()
            completed_count += 1
            if completed_count % 250 == 0 or completed_count == len(rows):
                print(f"PROBE_PROGRESS={completed_count}/{len(rows)}", flush=True)
    if any(result is None for result in results):
        raise GateError("PROBE_RESULT_CARDINALITY_FAILED")
    return [result for result in results if result is not None]


def snapshot(paths: list[Path]) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in paths:
        if path.is_file():
            result[rel(path)] = sha256(path)
    return result


def protected_paths(source_paths: list[Path]) -> tuple[dict[str, str], dict[str, str], dict[str, str]]:
    source_snapshot = snapshot(source_paths)
    formal_paths = [path for path in (ROOT / "derived" / "scale" / "papers").rglob("*") if path.is_file()]
    formal_snapshot = snapshot(formal_paths)
    catalog_names = [
        "g11_marker_only_scope_confirmation_input.csv",
        "g11_marker_only_scope_confirmation.csv",
        "g11_marker_only_confirmed_repair_targets.csv",
        "g11_marker_only_residual_visual_input.csv",
        "g11_targeted_visual_diagnostic_decisions.csv",
        "g11_targeted_visual_diagnostic_manifest.csv",
        "g11_marker_only_page_deep_diagnostic.csv",
        "g11_major_defect_deep_diagnostic.csv",
        "g11_major_defect_deep_diagnostic_result.json",
        "g11_targeted_visual_diagnostic_approval_result.json",
        "g8_artifact_manifest.csv",
        "g8_eligibility_reconciliation.csv",
        "g9_paper_index.csv",
    ]
    catalog_snapshot = snapshot([SCALE / name for name in catalog_names])
    return source_snapshot, formal_snapshot, catalog_snapshot


def load_inputs() -> dict[str, Any]:
    required = [
        RESIDUAL_INPUT, SCOPE_INPUT, UPSTREAM_RESULT, CONFIRMED_TARGETS,
        TARGET_DECISIONS, DEEP_PAGE, DEEP_RESULT, VISUAL_APPROVAL,
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise GateError("MISSING_INPUT=" + ";".join(missing))
    residual = read_csv(RESIDUAL_INPUT)
    scope = read_csv(SCOPE_INPUT)
    confirmed_targets = read_csv(CONFIRMED_TARGETS)
    target_decisions = read_csv(TARGET_DECISIONS)
    deep_page = read_csv(DEEP_PAGE)
    upstream = read_json(UPSTREAM_RESULT)
    deep_result = read_json(DEEP_RESULT)
    visual_approval = read_json(VISUAL_APPROVAL)

    residual_keys = assert_unique(residual, "RESIDUAL_INPUT")
    scope_keys = assert_unique(scope, "SCOPE_INPUT")
    deep_keys = assert_unique(deep_page, "DEEP_PAGE")
    if len(residual) != 2951 or len(residual_keys) != 2951:
        raise GateError("RESIDUAL_INPUT_CARDINALITY_FAILED")
    if residual_keys != scope_keys:
        raise GateError("RESIDUAL_AND_SCOPE_INPUT_KEY_MISMATCH")
    if any(row.get("current_scope_status") != "UNRESOLVED" for row in residual):
        raise GateError("RESIDUAL_INPUT_PRIOR_STATUS_NOT_UNRESOLVED")
    if any(row.get("scope_status") != "UNRESOLVED" for row in scope):
        raise GateError("SCOPE_INPUT_PRIOR_STATUS_NOT_UNRESOLVED")
    if len(deep_page) != 3033 or len(deep_keys) != 3033:
        raise GateError("DEEP_PAGE_CARDINALITY_FAILED")
    if any(row.get("marker_only_detected") != "1" for row in deep_page):
        raise GateError("DEEP_PAGE_MARKER_ONLY_GATE_FAILED")
    if len(target_decisions) != 53 or len(assert_unique(target_decisions, "TARGET_DECISIONS")) != 53:
        raise GateError("TARGET_DECISION_CARDINALITY_FAILED")
    if any(row.get("review_status") != "REVIEWED" or row.get("source_visual_classification") != "SUBSTANTIVE_CONTENT" for row in target_decisions):
        raise GateError("TARGET_DECISION_APPROVAL_GATE_FAILED")

    old_confirmed = {
        key(row) for row in deep_page
        if row.get("classification") == "CONFIRMED_DEFECTIVE_CONTENT_MISSING"
    }
    visual_confirmed = {key(row) for row in target_decisions}
    if len(old_confirmed) != 29:
        raise GateError(f"PREVIOUS_CONFIRMED_PAGE_COUNT={len(old_confirmed)}")
    if len(old_confirmed & visual_confirmed) != 0:
        raise GateError("TARGETED_VISUAL_OVERLAPS_PREVIOUS_CONFIRMED")
    preexisting_confirmed = old_confirmed | visual_confirmed
    residual_expected = deep_keys - preexisting_confirmed
    if residual_expected != residual_keys:
        raise GateError("RESIDUAL_SCOPE_NOT_EXACT_COMPLEMENT_OF_82_CONFIRMED")
    if len(preexisting_confirmed) != 82:
        raise GateError("PREEXISTING_CONFIRMED_PAGE_COUNT_NOT_82")

    identity_meta: dict[str, dict[str, Any]] = {}
    for row in read_csv(SCALE / "g11_major_defect_deep_diagnostic.csv"):
        identity_meta[row["paper_id"]] = {
            "year": row["year"],
            "problem": row["problem"],
            "artifact_set_id": row["artifact_set_id"],
            "formal_body_path": row["formal_body_path"],
            "formal_body_sha256": row["formal_body_sha256"],
            "source_path": row["source_path"],
            "source_sha256": row["source_sha256"].upper(),
        }
    for row in residual:
        identity_meta[row["paper_id"]] = {
            "year": row["year"],
            "problem": row["problem"],
            "artifact_set_id": row["artifact_set_id"],
            "formal_body_path": row["formal_body_path"],
            "formal_body_sha256": row["formal_body_sha256"].upper(),
            "source_path": row["source_path"],
            "source_sha256": row["source_sha256"].upper(),
        }
    for row in target_decisions:
        identity_meta[row["paper_id"]] = {
            "year": row["year"],
            "problem": row["problem"],
            "artifact_set_id": f"derived/scale/papers/{row['paper_id']}",
            "formal_body_path": row["formal_artifact_path"],
            "formal_body_sha256": row["formal_artifact_sha256"].upper(),
            "source_path": row["source_path"],
            "source_sha256": row["source_sha256"].upper(),
        }
    for row in residual:
        if row["paper_id"] not in identity_meta:
            raise GateError(f"IDENTITY_METADATA_MISSING={row['paper_id']}")

    return {
        "residual": residual,
        "scope": scope,
        "target_decisions": target_decisions,
        "deep_page": deep_page,
        "confirmed_targets": confirmed_targets,
        "upstream": upstream,
        "deep_result": deep_result,
        "visual_approval": visual_approval,
        "old_confirmed": old_confirmed,
        "visual_confirmed": visual_confirmed,
        "preexisting_confirmed": preexisting_confirmed,
        "identity_meta": identity_meta,
    }


def make_calibration_rows(inputs: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    meta = inputs["identity_meta"]
    positive: list[dict[str, Any]] = []
    for paper_id, page in sorted(inputs["preexisting_confirmed"]):
        item = dict(meta[paper_id])
        item.update({"paper_id": paper_id, "source_page": page, "known_label": "SUBSTANTIVE_CONTENT"})
        positive.append(item)

    negative: list[dict[str, Any]] = []
    # These are existing G5/G6 independently verified blank pages.  They are
    # used only as a negative classifier calibration set; they are not G11
    # residual pages and are never promoted into a G11 decision.
    reconciliation = SCALE.parent / "pilot" / "g6_q2_garbled_reconciliation.csv"
    source_map_path = SCALE.parent / "pilot" / "g6_file_source_map.csv"
    source_map = {
        row["paper_id"]: row
        for row in read_csv(source_map_path)
        if row.get("paper_id")
    } if source_map_path.is_file() else {}
    if reconciliation.is_file():
        for row in read_csv(reconciliation):
            if row.get("visual_type") != "VERIFIED_BLANK_PAGE":
                continue
            mapped = source_map.get(row["paper_id"], {})
            source_path = row.get("original_file_path") or mapped.get("file_path", "")
            source_sha = (row.get("original_sha256") or mapped.get("file_sha256", "")).upper()
            source = ROOT / source_path
            if not source.is_file() or sha256(source) != source_sha:
                raise GateError(f"NEGATIVE_CALIBRATION_SOURCE_GATE_FAILED={source_path}")
            negative.append({
                "paper_id": row["paper_id"],
                "year": "2025",
                "problem": "C",
                "source_page": int(row["source_page"]),
                "source_path": source_path,
                "source_sha256": source_sha,
                "artifact_set_id": "EXISTING_G5_G6_NEGATIVE_CALIBRATION",
                "formal_body_path": "",
                "formal_body_sha256": "",
                "known_label": "VERIFIED_BLANK_SOURCE_PAGE",
            })
    return positive, negative


def load_saved_probes(rows: list[dict[str, Any]], output_root: Path, status_by_key: dict[tuple[str, int], str] | None = None) -> list[dict[str, Any]]:
    """Reclassify already persisted raw page output without invoking Poppler again."""
    results: list[dict[str, Any]] = []
    for row in rows:
        output_path = output_root / str(row["paper_id"]) / f"source_page_{int(row['source_page'])}.txt"
        if not output_path.is_file():
            raise GateError(f"SAVED_PROBE_OUTPUT_MISSING={output_path}")
        raw = output_path.read_text(encoding="utf-8", errors="replace")
        status = (status_by_key or {}).get(key(row), "SUCCESS")
        item = classify_text(raw, status)
        item.update({
            "probe_status": status,
            "return_code": 0 if status == "SUCCESS" else -1,
            "raw": raw,
            "raw_char_count": len(raw),
            "stderr": "",
            "output_path": output_path,
            "output_sha256": sha256(output_path),
        })
        results.append(item)
    return results


def base_result(inputs: dict[str, Any], branch: str, head: str) -> dict[str, Any]:
    upstream = inputs["upstream"]
    baseline = load_current_formal_baseline()
    attempt_id = "g11-marker-only-residual-scope-diagnostic-" + str(upstream.get("DECISION_SHEET_SHA256", "unknown"))[:16].lower()
    return {
        "STAGE": "G11-MARKER-ONLY-RESIDUAL-SCOPE-DIAGNOSTIC",
        "STATUS": "PARTIAL",
        "BRANCH": branch,
        "HEAD": head,
        "RESIDUAL_SCOPE_DIAGNOSTIC_ATTEMPT_ID": attempt_id,
        "RESIDUAL_DIAGNOSTIC_ATTEMPT_ID": attempt_id,
        "SOURCE_SCOPE_CONFIRMATION_ATTEMPT_ID": upstream.get("SCOPE_CONFIRMATION_ATTEMPT_ID"),
        "STARTED_AT": now(),
        "PDFTOTEXT_EXECUTABLE": str(PDFTOTEXT),
        "PDFTOTEXT_VERSION": "25.02.0",
        "PDFTOTEXT_PROBE_ARGUMENT_TEMPLATE": "pdftotext -f N -l N -enc UTF-8 input.pdf -",
        "PROBE_TIMEOUT_SECONDS": PROBE_TIMEOUT_SECONDS,
        "INPUT_PATH": rel(RESIDUAL_INPUT),
        "INPUT_ROW_COUNT": 2951,
        "INPUT_UNIQUE_PAPER_PAGE_COUNT": 2951,
        "RESIDUAL_INPUT_ROW_COUNT": 2951,
        "RESIDUAL_INPUT_UNIQUE_PAPER_PAGE_COUNT": 2951,
        "INPUT_PRIOR_SCOPE_STATUS": "UNRESOLVED",
        "SOURCE_PAGE_MARKER_SEMANTICS": "PAGE_LOCAL_STRICT_BOUNDARY",
        "ALL_RESIDUAL_INPUT_KEYS_FROZEN": 1,
        "RESIDUAL_INPUT_ADD_COUNT": 0,
        "RESIDUAL_INPUT_DELETE_COUNT": 0,
        "RESIDUAL_INPUT_REPLACE_COUNT": 0,
        "SCOPE_CONFIRMATION_PREVIOUS_UNRESOLVED_PAGE_COUNT": int(upstream.get("REMAINING_UNRESOLVED_PAGE_COUNT", 2951)),
        "SCOPE_CONFIRMATION_PREVIOUS_UNRESOLVED_IDENTITY_COUNT": int(upstream.get("FINAL_UNRESOLVED_IDENTITY_COUNT", 238)),
        "CURRENT_FORMAL_IDENTITY_COUNT": baseline["formal_identities"],
        "CURRENT_ELIGIBLE_IDENTITY_COUNT": baseline["eligible_identities"],
        "CURRENT_INELIGIBLE_IDENTITY_COUNT": baseline["ineligible_identities"],
        "CURRENT_ARTIFACT_SETS": baseline["artifact_sets"],
        "CURRENT_PRIMARY_ARTIFACTS": baseline["primary_artifacts"],
        "CURRENT_FORMAL_INDEX_RECORDS": baseline["formal_index_records"],
        "CURRENT_DOC_MANUAL_BACKLOG": baseline["doc_manual_backlog"],
        "CURRENT_Q3_MANUAL_BACKLOG": baseline["q3_manual_backlog"],
        "CURRENT_TOTAL_MANUAL_BACKLOG": baseline["total_manual_backlog"],
        "PREVIOUS_ARTIFACT_SETS": baseline["artifact_sets"],
        "PREVIOUS_PRIMARY_ARTIFACTS": baseline["primary_artifacts"],
    }


def identity_stats(confirmed_pages: set[tuple[str, int]], unresolved_pages: set[tuple[str, int]]) -> dict[str, int]:
    confirmed_ids = {paper_id for paper_id, _ in confirmed_pages}
    unresolved_ids = {paper_id for paper_id, _ in unresolved_pages}
    return {
        "confirmed_identity_count": len(confirmed_ids),
        "unresolved_identity_count": len(unresolved_ids),
        "unresolved_only_identity_count": len(unresolved_ids - confirmed_ids),
        "confirmed_with_residual_unresolved_identity_count": len(confirmed_ids & unresolved_ids),
        "confirmed_with_no_residual_unresolved_identity_count": len(confirmed_ids - unresolved_ids),
    }


def diagnostic_row(source_row: dict[str, Any], probe: dict[str, Any]) -> dict[str, Any]:
    substantive = int(probe["substantive_text_detected"])
    probe_status = str(probe["probe_status"])
    classification = str(probe["text_probe_classification"])
    if substantive:
        new_status = "CONFIRMED_DEFECTIVE"
        residual_class = "TEXT_LAYER_SUBSTANTIVE"
        confidence = "HIGH"
        requires_render = 0
    elif classification == "TEXT_LAYER_GARBLED_OR_UNRELIABLE":
        new_status = "UNRESOLVED"
        residual_class = "TEXT_LAYER_GARBLED"
        confidence = "LOW"
        requires_render = 1
    elif classification == "TEXT_PROBE_TIMEOUT":
        new_status = "UNRESOLVED"
        residual_class = "TEXT_PROBE_TIMEOUT"
        confidence = "LOW"
        requires_render = 1
    elif classification == "TEXT_PROBE_ERROR":
        new_status = "UNRESOLVED"
        residual_class = "TEXT_PROBE_ERROR"
        confidence = "LOW"
        requires_render = 1
    else:
        new_status = "UNRESOLVED"
        residual_class = "IMAGE_ONLY_OR_NO_TEXT_LAYER"
        confidence = "LOW"
        requires_render = 1
    stderr = str(probe.get("stderr", ""))
    notes = (
        "Exact source-page probe only; no OCR, render, pdf-inspector extraction, or visual judgment. "
        "Source page uses 1-based numbering."
    )
    if stderr:
        notes += " stderr=" + re.sub(r"\s+", " ", stderr)[:500]
    return {
        "paper_id": source_row["paper_id"],
        "year": source_row["year"],
        "problem": source_row["problem"],
        "source_page": source_row["source_page"],
        "source_path": source_row["source_path"],
        "source_sha256": source_row["source_sha256"].upper(),
        "artifact_set_id": source_row["artifact_set_id"],
        "formal_body_path": source_row["formal_body_path"],
        "formal_body_sha256": source_row["formal_body_sha256"].upper(),
        "prior_scope_status": source_row["current_scope_status"],
        "pdftotext_probe_status": probe_status,
        "pdftotext_output_path": rel(probe["output_path"]),
        "pdftotext_output_sha256": probe["output_sha256"],
        "raw_char_count": probe["raw_char_count"],
        "normalized_char_count": len(probe["normalized"]),
        "normalized_line_count": probe["normalized_line_count"],
        "substantive_text_detected": substantive,
        "substantive_detection_basis": probe["substantive_detection_basis"],
        "text_probe_classification": classification,
        "new_scope_status": new_status,
        "scope_confidence": confidence,
        "residual_class": residual_class,
        "requires_render": requires_render,
        "requires_ocr": 0,
        "notes": notes,
    }


def write_image_residual(rows: list[dict[str, Any]]) -> None:
    residual = [
        {
            "paper_id": row["paper_id"],
            "year": row["year"],
            "problem": row["problem"],
            "source_page": row["source_page"],
            "source_path": row["source_path"],
            "source_sha256": row["source_sha256"],
            "artifact_set_id": row["artifact_set_id"],
            "formal_body_path": row["formal_body_path"],
            "formal_body_sha256": row["formal_body_sha256"],
            "prior_scope_status": row["prior_scope_status"],
            "residual_class": row["residual_class"],
            "text_probe_classification": row["text_probe_classification"],
            "image_review_required": 1,
            "render_required": row["requires_render"],
            "ocr_run_in_this_stage": 0,
            "deterministic_sort_key": f"{row['paper_id']}|{int(row['source_page']):06d}",
        }
        for row in rows
        if row["new_scope_status"] != "CONFIRMED_DEFECTIVE"
    ]
    fields = list(residual[0].keys()) if residual else [
        "paper_id", "year", "problem", "source_page", "source_path", "source_sha256",
        "artifact_set_id", "formal_body_path", "formal_body_sha256", "prior_scope_status",
        "residual_class", "text_probe_classification", "image_review_required", "render_required",
        "ocr_run_in_this_stage", "deterministic_sort_key",
    ]
    write_csv(IMAGE_RESIDUAL_CSV, fields, sorted(residual, key=lambda row: row["deterministic_sort_key"]))


def write_report(result: dict[str, Any], classifications: Counter[str]) -> None:
    lines = [
        "# G11 Marker-Only Residual Scope Diagnostic",
        "",
        f"- Stage: `{result['STAGE']}`",
        f"- Status: `{result['STATUS']}`",
        f"- Branch / HEAD: `{result['BRANCH']}` / `{result['HEAD']}`",
        f"- Attempt: `{result['RESIDUAL_SCOPE_DIAGNOSTIC_ATTEMPT_ID']}`",
        "",
        "## Scope and method",
        "",
        f"The frozen residual input contains {result['INPUT_ROW_COUNT']} unique paper/page rows, all previously `UNRESOLVED`. The input key set was compared exactly with the prior scope output; add, delete, and replace counts are all zero.",
        f"Each page was probed independently with `{result['PDFTOTEXT_PROBE_ARGUMENT_TEMPLATE']}` using the frozen executable `{result['PDFTOTEXT_EXECUTABLE']}`. The per-page timeout was {result['PROBE_TIMEOUT_SECONDS']} seconds. No OCR, PDF rendering, pdf-inspector extraction, formal extraction, or visual judgment was performed.",
        "",
        "## Identity metrics before the exact-page probe",
        "",
        f"- Any unresolved page: {result['IDENTITY_WITH_ANY_UNRESOLVED_PAGE_COUNT_BEFORE']} identities.",
        f"- Unresolved-only: {result['UNRESOLVED_ONLY_IDENTITY_COUNT_BEFORE']} identities.",
        f"- Confirmed identities with residual unresolved pages: {result['CONFIRMED_DEFECTIVE_WITH_RESIDUAL_UNRESOLVED_IDENTITY_COUNT_BEFORE']}.",
        f"- Confirmed identities with no residual unresolved pages: {result['CONFIRMED_DEFECTIVE_WITH_NO_RESIDUAL_UNRESOLVED_IDENTITY_COUNT_BEFORE']}.",
        "",
        "The earlier value of 235 was the identity count attached to the 3,004-page unresolved population before the targeted visual sample was promoted. The current value of 238 is calculated over the current 2,951-page residual complement after 82 pages were confirmed. The difference is a metric-scope/timepoint change, not a change to source or identity data.",
        "",
        "## Calibration",
        "",
        f"Positive calibration used {result['POSITIVE_CALIBRATION_PAGE_COUNT']} previously confirmed pages; substantive text was recovered on {result['POSITIVE_CALIBRATION_SUBSTANTIVE_DETECTED_COUNT']} and not recovered on {result['POSITIVE_CALIBRATION_NOT_RECOVERED_COUNT']}.",
        f"Negative calibration used {result['NEGATIVE_CALIBRATION_PAGE_COUNT']} existing verified-blank pages; false substantive classifications: {result['NEGATIVE_CALIBRATION_FALSE_SUBSTANTIVE_COUNT']}.",
        "Empty or noise-only page-scoped output was retained as unresolved. It was never promoted to legitimate noncontent solely because text was absent.",
        "",
        "## Probe classification",
        "",
    ]
    for name in [
        "TEXT_LAYER_SUBSTANTIVE", "TEXT_LAYER_NON_SUBSTANTIVE_OR_EMPTY",
        "TEXT_LAYER_GARBLED_OR_UNRELIABLE", "TEXT_PROBE_TIMEOUT", "TEXT_PROBE_ERROR",
    ]:
        lines.append(f"- `{name}`: {classifications.get(name, 0)}")
    lines.extend(["", "## Residual classes", ""])
    for residual_class, page_count in sorted(result["RESIDUAL_CLASSES"].items()):
        identity_count = result["RESIDUAL_CLASS_IDENTITY_COUNTS"].get(residual_class, 0)
        lines.append(f"- `{residual_class}`: page_count={page_count}; identity_count={identity_count}")
    lines.extend([
        "",
        f"Newly confirmed pages: {result['NEWLY_CONFIRMED_DEFECTIVE_PAGE_COUNT']}; final unresolved pages: {result['FINAL_RESIDUAL_UNRESOLVED_PAGE_COUNT']}. The residual image/text-empty input was written only for unresolved pages and remains outside repair scope.",
        "",
        "## Safety and governance gates",
        "",
        "Source PDFs were checked read-only for existence, SHA256, and page validity. Formal bodies, artifacts, identity/membership/eligibility registries, decision sheets, backlog, G9/G10 outputs, and frozen samples were not modified. No dependency installation, network access, OCR, rendering, Word, or formal artifact generation occurred.",
        "",
        "## Outputs",
        "",
    ])
    for output in result["OUTPUTS"]:
        lines.append(f"- `{output}`")
    lines.extend(["", "## Next", "", f"`{result['NEXT']}`", ""])
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> int:
    if not PDFTOTEXT.is_file():
        raise GateError(f"FROZEN_PDFTOTEXT_MISSING={PDFTOTEXT}")
    inputs = load_inputs()
    branch = git_value("branch", "--show-current")
    head = git_value("rev-parse", "HEAD")
    source_paths = sorted({ROOT / row["source_path"] for row in inputs["residual"]})
    source_before, formal_before, catalog_before = protected_paths(source_paths)

    source_missing_count = 0
    source_sha_mismatch_count = 0
    invalid_page_count = 0
    page_counts: dict[Path, int | None] = {}
    for source in source_paths:
        if not source.is_file():
            source_missing_count += sum(1 for row in inputs["residual"] if ROOT / row["source_path"] == source)
            continue
        page_counts[source] = pdfinfo_page_count(source)
    for row in inputs["residual"]:
        source = ROOT / row["source_path"]
        if not source.is_file():
            continue
        if sha256(source) != row["source_sha256"].upper():
            source_sha_mismatch_count += 1
        page_count = page_counts.get(source)
        page = int(row["source_page"])
        if page < 1 or page_count is None or page > page_count:
            invalid_page_count += 1
    if source_missing_count or source_sha_mismatch_count or invalid_page_count:
        raise GateError(
            f"SOURCE_INTEGRITY_GATE_FAILED=missing:{source_missing_count};"
            f"sha:{source_sha_mismatch_count};invalid_page:{invalid_page_count}"
        )

    positive, negative = make_calibration_rows(inputs)
    reuse_existing = "--reuse-existing-probes" in sys.argv[1:]
    if reuse_existing:
        previous_diagnostics = read_csv(DIAGNOSTIC_CSV)
        previous_status = {key(row): row["pdftotext_probe_status"] for row in previous_diagnostics}
        positive_probe = load_saved_probes(positive, CALIBRATION_DIR / "positive") if positive else []
        residual_probe = load_saved_probes(inputs["residual"], RESIDUAL_TEXT_DIR, previous_status)
    else:
        positive_probe = run_probes(positive, CALIBRATION_DIR / "positive") if positive else []
        residual_probe = run_probes(inputs["residual"], RESIDUAL_TEXT_DIR)
    # The negative calibration set was absent from the first pass because the
    # legacy evidence uses verified_blank_page=1 alongside a different final
    # page class.  Probe those four pages once after correcting the selector.
    if reuse_existing and negative:
        negative_probe = load_saved_probes(negative, CALIBRATION_DIR / "negative")
    else:
        negative_probe = run_probes(negative, CALIBRATION_DIR / "negative") if negative else []

    diagnostic_rows = [
        diagnostic_row(source_row, probe)
        for source_row, probe in zip(inputs["residual"], residual_probe)
    ]
    write_csv(DIAGNOSTIC_CSV, DIAGNOSTIC_FIELDS, diagnostic_rows)
    write_image_residual(diagnostic_rows)

    positive_substantive = sum(int(item["substantive_text_detected"]) for item in positive_probe)
    negative_false_substantive = sum(int(item["substantive_text_detected"]) for item in negative_probe)
    newly_confirmed = {
        key(row) for row in diagnostic_rows if row["new_scope_status"] == "CONFIRMED_DEFECTIVE"
    }
    final_confirmed = inputs["preexisting_confirmed"] | newly_confirmed
    final_unresolved = set(key(row) for row in diagnostic_rows if row["new_scope_status"] != "CONFIRMED_DEFECTIVE")
    before_stats = identity_stats(inputs["preexisting_confirmed"], set(key(row) for row in inputs["residual"]))
    final_stats = identity_stats(final_confirmed, final_unresolved)
    classifications = Counter(row["text_probe_classification"] for row in diagnostic_rows)
    probe_statuses = Counter(row["pdftotext_probe_status"] for row in diagnostic_rows)
    residual_classes = Counter(row["residual_class"] for row in diagnostic_rows if row["new_scope_status"] != "CONFIRMED_DEFECTIVE")

    source_after, formal_after, catalog_after = protected_paths(source_paths)
    source_modified = int(source_before != source_after)
    formal_modified = int(formal_before != formal_after)
    catalog_modified = int(catalog_before != catalog_after)
    if source_modified or formal_modified or catalog_modified:
        raise GateError(
            f"PROTECTED_DATA_CHANGED=source:{source_modified};formal:{formal_modified};catalog:{catalog_modified}"
        )

    result = base_result(inputs, branch, head)
    result.update({
        "SOURCE_MISSING_PAGE_COUNT": source_missing_count,
        "SOURCE_PATH_MISSING_COUNT": source_missing_count,
        "SOURCE_SHA_MISMATCH_PAGE_COUNT": source_sha_mismatch_count,
        "SOURCE_SHA_MISMATCH_COUNT": source_sha_mismatch_count,
        "SOURCE_INVALID_PAGE_COUNT": invalid_page_count,
        "INVALID_SOURCE_PAGE_COUNT": invalid_page_count,
        "SOURCE_INTEGRITY_GATE_PASS": int(not (source_missing_count or source_sha_mismatch_count or invalid_page_count)),
        "IDENTITY_WITH_ANY_UNRESOLVED_PAGE_COUNT_BEFORE": before_stats["unresolved_identity_count"],
        "UNRESOLVED_ONLY_IDENTITY_COUNT_BEFORE": before_stats["unresolved_only_identity_count"],
        "CONFIRMED_DEFECTIVE_WITH_RESIDUAL_UNRESOLVED_IDENTITY_COUNT_BEFORE": before_stats["confirmed_with_residual_unresolved_identity_count"],
        "CONFIRMED_DEFECTIVE_WITH_NO_RESIDUAL_UNRESOLVED_IDENTITY_COUNT_BEFORE": before_stats["confirmed_with_no_residual_unresolved_identity_count"],
        "OLD_UNRESOLVED_IDENTITY_COUNT": int(inputs["deep_result"].get("OLD_UNRESOLVED_IDENTITY_COUNT", 235)),
        "OLD_UNRESOLVED_PAGE_COUNT": int(inputs["deep_result"].get("STILL_UNRESOLVED_PAGE_COUNT", 3004)),
        "OLD_235_VS_238_SEMANTICS_RESOLVED": 1,
        "OLD_VS_CURRENT_IDENTITY_METRIC_EXPLANATION": "235 counts the earlier 3,004-page unresolved population before targeted visual promotion; 238 counts the current 2,951-page residual complement after 82 confirmed pages. Scope/timepoint difference, not data error.",
        "OLD_235_VS_238_EXPLANATION": "235 counts the earlier 3,004-page unresolved population before targeted visual promotion; 238 counts the current 2,951-page residual complement after 82 confirmed pages. Scope/timepoint difference, not data error.",
        "POSITIVE_CALIBRATION_PAGE_COUNT": len(positive),
        "POSITIVE_CALIBRATION_SUBSTANTIVE_DETECTED_COUNT": positive_substantive,
        "POSITIVE_CALIBRATION_TEXT_LAYER_SUBSTANTIVE_COUNT": positive_substantive,
        "POSITIVE_CALIBRATION_NOT_RECOVERED_COUNT": len(positive) - positive_substantive,
        "NEGATIVE_CALIBRATION_PAGE_COUNT": len(negative),
        "NEGATIVE_CALIBRATION_FALSE_SUBSTANTIVE_COUNT": negative_false_substantive,
        "NEGATIVE_CALIBRATION_SUFFICIENT": int(len(negative) > 0),
        "RESIDUAL_TEXT_PROBE_ATTEMPTED_COUNT": len(diagnostic_rows),
        "RESIDUAL_TEXT_PROBE_SUCCESS_COUNT": probe_statuses.get("SUCCESS", 0),
        "RESIDUAL_TEXT_PROBE_TIMEOUT_COUNT": probe_statuses.get("TIMEOUT", 0),
        "RESIDUAL_TEXT_PROBE_ERROR_COUNT": probe_statuses.get("ERROR", 0),
        "TEXT_LAYER_SUBSTANTIVE_PAGE_COUNT": classifications.get("TEXT_LAYER_SUBSTANTIVE", 0),
        "TEXT_LAYER_NON_SUBSTANTIVE_OR_EMPTY_PAGE_COUNT": classifications.get("TEXT_LAYER_NON_SUBSTANTIVE_OR_EMPTY", 0),
        "TEXT_LAYER_GARBLED_OR_UNRELIABLE_PAGE_COUNT": classifications.get("TEXT_LAYER_GARBLED_OR_UNRELIABLE", 0),
        "TEXT_PROBE_TIMEOUT_PAGE_COUNT": classifications.get("TEXT_PROBE_TIMEOUT", 0),
        "TEXT_PROBE_ERROR_PAGE_COUNT": classifications.get("TEXT_PROBE_ERROR", 0),
        "NEWLY_CONFIRMED_DEFECTIVE_PAGE_COUNT": len(newly_confirmed),
        "NEWLY_CONFIRMED_DEFECTIVE_BY_TEXT_LAYER_PAGE_COUNT": len(newly_confirmed),
        "NEWLY_CONFIRMED_DEFECTIVE_BY_TEXT_LAYER_IDENTITY_COUNT": len({paper_id for paper_id, _ in newly_confirmed}),
        "NEWLY_CONFIRMED_LEGITIMATE_NONCONTENT_PAGE_COUNT": 0,
        "NEWLY_CONFIRMED_LEGITIMATE_NONCONTENT_BY_EMPTY_TEXT_COUNT": 0,
        "PREEXISTING_CONFIRMED_DEFECTIVE_PAGE_COUNT": len(inputs["preexisting_confirmed"]),
        "FINAL_CONFIRMED_DEFECTIVE_PAGE_COUNT": len(final_confirmed),
        "FINAL_RESIDUAL_UNRESOLVED_PAGE_COUNT": len(final_unresolved),
        "FINAL_CONFIRMED_LEGITIMATE_NONCONTENT_PAGE_COUNT": 0,
        "IDENTITY_WITH_ANY_UNRESOLVED_PAGE_COUNT_FINAL": final_stats["unresolved_identity_count"],
        "FINAL_RESIDUAL_UNRESOLVED_IDENTITY_WITH_ANY_COUNT": final_stats["unresolved_identity_count"],
        "FINAL_UNRESOLVED_ONLY_IDENTITY_COUNT": final_stats["unresolved_only_identity_count"],
        "FINAL_CONFIRMED_DEFECTIVE_WITH_RESIDUAL_UNRESOLVED_IDENTITY_COUNT": final_stats["confirmed_with_residual_unresolved_identity_count"],
        "FINAL_CONFIRMED_DEFECTIVE_WITH_NO_RESIDUAL_UNRESOLVED_IDENTITY_COUNT": final_stats["confirmed_with_no_residual_unresolved_identity_count"],
        "FINAL_CONFIRMED_DEFECTIVE_IDENTITY_COUNT": final_stats["confirmed_identity_count"],
        "CONFIRMED_MARKER_ONLY_REPAIR_TARGET_COUNT": final_stats["confirmed_identity_count"],
        "CUMCM_2020_D_003_REPAIR_TARGET": 1,
        "TOTAL_G11_REPAIR_TARGET_LOWER_BOUND": final_stats["confirmed_identity_count"] + 1,
        "RESIDUAL_CLASS_COUNT": len(residual_classes),
        "RESIDUAL_CLASS_COUNTS": dict(sorted(residual_classes.items())),
        "RESIDUAL_CLASSES": dict(sorted(residual_classes.items())),
        "RESIDUAL_CLASS_PAGE_COUNT": len(final_unresolved),
        "RESIDUAL_CLASS_IDENTITY_COUNT": len({paper_id for paper_id, _ in final_unresolved}),
        "RESIDUAL_CLASS_IDENTITY_COUNTS": {
            residual_class: len({row["paper_id"] for row in diagnostic_rows if row["residual_class"] == residual_class and row["new_scope_status"] != "CONFIRMED_DEFECTIVE"})
            for residual_class in sorted(residual_classes)
        },
        "FULL_MARKER_ONLY_REPAIR_SCOPE_FROZEN": int(len(final_unresolved) == 0),
        "SCOPE_CONFIRMATION_STATUS": "PASS" if len(final_unresolved) == 0 else "PARTIAL",
        "G11_STATUS_REMAINS": "PASS" if len(final_unresolved) == 0 else "PARTIAL",
        "SOURCE_SHA_MISMATCH": source_modified,
        "ORIGINAL_FILES_MODIFIED": source_modified,
        "FORMAL_ARTIFACTS_MODIFIED": formal_modified,
        "FORMAL_DATA_MODIFIED": catalog_modified,
        "FORMAL_DATA_MODIFICATION_COUNT": catalog_modified,
        "FORMAL_ELIGIBILITY_MODIFIED": catalog_modified,
        "BACKLOG_MODIFICATION_COUNT": 0,
        "DOC_BATCH_RUN": 0,
        "Q3_REPAIR_RUN": 0,
        "Q3_OCR_RUN": 0,
        "IMAGE_OCR_RUN": 0,
        "IMAGE_EXTRACTION_RERUN": 0,
        "OCR_RUN": 0,
        "PDF_RENDER_RUN": 0,
        "TARGETED_RENDER_RUN": 0,
        "PDF_INSPECTOR_EXTRACTION_RUN": 0,
        "FORMAL_EXTRACTION_RUN": 0,
        "EXTRACTION_RUN": 0,
        "BODY_RECONSTRUCTION_RUN": 0,
        "ARTIFACT_REGENERATION_RUN": 0,
        "REVIEW_PACKET_REGENERATION_RUN": 0,
        "G9_RUN": 0,
        "G10_RUN": 0,
        "G9_REBUILD_RUN": 0,
        "G10_REBUILD_RUN": 0,
        "G12_RUN": 0,
        "G11_ORIGINAL_DECISION_MODIFICATION_COUNT": 0,
        "TARGETED_VISUAL_DECISION_MODIFICATION_COUNT": 0,
        "FORMAL_ARTIFACT_CONTENT_MODIFICATION_COUNT": 0,
        "FORMAL_INDEX_MODIFICATION_COUNT": 0,
        "IDENTITY_MODIFICATION_COUNT": 0,
        "MEMBERSHIP_MODIFICATION_COUNT": 0,
        "DOWNLOAD_RUN": 0,
        "WORD_RUN": 0,
        "WORD_COM_RUN": 0,
        "DOC_CONVERSION_RUN": 0,
        "PRINT_JOB_RUN": 0,
        "GIT_OPERATIONS": 0,
        "NEW_DEPENDENCY_INSTALLED": 0,
        "NETWORK_ACCESS_USED": 0,
        "WORD_COM_PILOT_STARTED": 0,
        "WORD_COM_INSTANCE_CREATED": 0,
        "DOC_OPENED": 0,
        "DOC_CONVERSION_ATTEMPTED": 0,
        "PDFTOTEXT_PAGE_PROBE_RUN": 1,
        "PAGES_CLASSIFIED_WITHOUT_NEW_RENDER_COUNT": 0,
        "OUTPUTS": [
            rel(DIAGNOSTIC_CSV), rel(IMAGE_RESIDUAL_CSV), rel(RESULT_JSON), rel(REPORT),
            rel(RESIDUAL_TEXT_DIR), rel(CALIBRATION_DIR / "positive"), rel(CALIBRATION_DIR / "negative"),
        ],
        "VALIDATION": [
            "Residual input has exactly 2,951 unique paper/page keys, all prior UNRESOLVED, with zero add/delete/replace drift.",
            "All residual source paths passed existence, SHA256, and source-page validity checks.",
            f"Frozen pdftotext exact-page probes completed with success={probe_statuses.get('SUCCESS', 0)}, timeout={probe_statuses.get('TIMEOUT', 0)}, error={probe_statuses.get('ERROR', 0)}.",
            "Only TEXT_LAYER_SUBSTANTIVE is eligible for new confirmation; empty, noise, garbled, timeout, and error pages remain unresolved.",
            f"Positive calibration covered {len(positive)} preexisting confirmed pages; negative calibration covered {len(negative)} existing verified-blank pages.",
            "Protected source files, formal bodies/artifacts, decision sheets, formal data, eligibility, and index inputs remained byte-identical during this stage.",
            "No OCR, rendering, pdf-inspector extraction, formal artifact generation, G9/G10, Word, network, or dependency installation occurred.",
        ],
        "ISSUES": (
            [f"{len(final_unresolved)} residual pages remain unresolved after exact-page text probing; their residual classes are recorded in the image/text residual input."]
            if final_unresolved else []
        ),
        "BLOCKER": "NONE" if not final_unresolved else (
            "TEXT_PROBE_FAILURE_RESIDUAL_SCOPE_UNRESOLVED"
            if set(residual_classes).issubset({"PDFTOTEXT_TIMEOUT", "PDFTOTEXT_ERROR"})
            else "IMAGE_OR_TEXT_EMPTY_RESIDUAL_SCOPE_UNRESOLVED"
        ),
        "NEXT": "G11-CLOSURE-REVIEW" if not final_unresolved else (
            "G11-MARKER-ONLY-PDFTOTEXT-FAILURE-DIAGNOSTIC"
            if set(residual_classes).issubset({"PDFTOTEXT_TIMEOUT", "PDFTOTEXT_ERROR"})
            else "G11-MARKER-ONLY-IMAGE-RESIDUAL-SCOPE-DIAGNOSTIC"
        ),
        "COMPLETED_AT": now(),
    })
    json_text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    RESULT_JSON.parent.mkdir(parents=True, exist_ok=True)
    RESULT_JSON.write_text(json_text, encoding="utf-8", newline="\n")
    write_report(result, classifications)
    print(json_text)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GateError as exc:
        print(f"GATE_ERROR={exc}", file=sys.stderr)
        raise SystemExit(2)
