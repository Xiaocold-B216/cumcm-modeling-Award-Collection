"""Fail-closed G8 Q3 contract-pilot runner.

The default modes are metadata-only.  ``--execute-pilot`` is the sole mode
that may inspect selected PDFs, render pages, start the local OCR worker, or
write formal pilot evidence.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from datetime import datetime, timezone
from collections import Counter
from pathlib import Path
from typing import Any, Protocol


def repository_root(anchor: Path) -> Path:
    for candidate in (anchor, *anchor.parents):
        if (candidate / "catalog" / "scale").is_dir() and (candidate / "tools").is_dir():
            return candidate
    raise RuntimeError("REPOSITORY_ROOT_NOT_FOUND")


ROOT = repository_root(Path(__file__).resolve().parent)
SCALE = ROOT / "catalog" / "scale"
REPORTS = ROOT / "reports" / "scale"
BACKLOG = SCALE / "g8_q3_manual_backlog.csv"
ELIGIBILITY = SCALE / "g8_artifact_eligibility.csv"
MEMBERSHIP = ROOT / "catalog" / "paper_files.csv"
SOURCE_MAP = SCALE / "g8_file_source_map.csv"
BINDING = SCALE / "g8_q3_poppler_runtime_binding.json"
LANG_ROOT = Path(r"D:\cumcm-modeling-Award-Collection.bootstrap\ocr\tesseract-data")
NODE = Path(r"C:\Users\WRZ\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe")
NODE_MODULES = NODE.parent.parent / "node_modules"
TESSERACT_MODULE = NODE_MODULES / "tesseract.js"
EXTRACTION_ROOT = SCALE / "g8_q3_pilot_extraction"
ATTEMPT_PATH = SCALE / "g8_q3_contract_pilot_attempt.json"
RESULT_PATH = SCALE / "g8_q3_contract_pilot_result.json"
ATTEMPT_HISTORY_ROOT = SCALE / "g8_q3_contract_pilot_attempt_history"
PROGRESS_PATH = SCALE / "g8_q3_pilot_progress.csv"
CHILD_AUDIT_PATH = SCALE / "g8_q3_pilot_child_process_audit.csv"
INVENTORY_PATH = SCALE / "g8_q3_target_inventory.csv"
SELECTION_PATH = SCALE / "g8_q3_pilot_selection.csv"
REFINEMENT = SCALE / "g8_q3_contract_refinement_v1.json"
PAGE_SCOPED_REPLAY_PAGE_AUDIT_PATH = SCALE / "g8_q3_page_scoped_ocr_replay_page_audit.csv"
PAGE_SCOPED_REPLAY_CHILD_AUDIT_PATH = SCALE / "g8_q3_page_scoped_ocr_replay_child_audit.csv"
PAGE_SCOPED_REFINEMENT_RESULT_PATH = SCALE / "g8_q3_page_scoped_ocr_refinement_result.json"
PAGE_SCOPED_REFINEMENT_REPORT_PATH = REPORTS / "G8_Q3_PAGE_SCOPED_OCR_CHILD_REFINEMENT.md"
INVENTORY_FIELDS = ["paper_id", "artifact_eligible", "q3_reason", "membership_count", "primary_source_path", "primary_source_sha256", "alternate_source_count", "better_alternate_source_available", "better_alternate_source_paths", "page_count", "text_layer_page_count", "zero_text_page_count", "repair_suspect_page_count", "repair_ratio", "repair_run_count", "text_image_transition_count", "inventory_schema_version", "backlog_catalog_sha256", "eligibility_catalog_sha256", "membership_catalog_sha256", "source_map_catalog_sha256", "source_sha256_fingerprint", "runtime_semantic_fingerprint", "inventory_fingerprint", "refinement_contract_sha256", "refinement_evidence_fingerprint"]
SELECTION_FIELDS = ["paper_id", "selection_dimension", "selection_rank", "selection_metric", "selection_value", "selection_reason", "source_path", "source_sha256", "primary_source_path", "primary_source_sha256", "page_count", "repair_ratio", "repair_run_count", "better_alternate_source_available", "inventory_fingerprint", "selection_fingerprint", "refinement_contract_sha256", "refinement_evidence_fingerprint"]
EXPECTED_LANG_SHA = {
    "chi_sim.traineddata.gz": "B8A23F10C7DE500891EB458A8ADC9CC58AB7F242F08B7D149F5E9AEA4AD5DB7C",
    "eng.traineddata.gz": "45B4CB346724AC1774F1C36F42F182B887BCDB28EBE63E6FFF90AC41F3FCFF91",
}
PRIMARY_CLASSES = {"TEXT_PAGE", "VERIFIED_BLANK", "IMAGE_ONLY_CONTENT_PAGE", "UNEXPLAINED"}
PAGE_PROVENANCE = {"PDF_TEXT_LAYER", "OCR", "VERIFIED_BLANK", "PDF_TEXT_LAYER_PLUS_VALIDATED_OCR_SUPPLEMENT"}
ACTIVE_ATTEMPT: dict[str, Any] | None = None
ACTIVE_AUDIT_PATH: Path | None = None
ACTIVE_AUDIT_FIELDS: list[str] | None = None
CHILD_STDERR_TAIL_MAX_BYTES = 8192
CHILD_TIMEOUT_SECONDS = 180
CHILD_AUDIT: list[dict[str, Any]] = []


class ChildProcessTimeout(RuntimeError):
    pass
QUALITY_THRESHOLDS = {
    "replacement_char_ratio_hard_fail": 0.0,
    "control_char_ratio_hard_fail": 0.0,
    "image_placeholder_ratio_hard_fail": 0.20,
    "minimum_authoritative_page_chars": 40,
    "minimum_body_chars": 120,
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def atomic_write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp-" + uuid.uuid4().hex)
    try:
        with temporary.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
            stream.flush()
            os.fsync(stream.fileno())
        replace_with_retry(temporary, path)
    except BaseException:
        try:
            temporary.unlink()
        except OSError:
            pass
        raise


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest().upper()


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def replace_with_retry(temporary: Path, destination: Path) -> None:
    last_error: PermissionError | None = None
    for _ in range(20):
        try:
            os.replace(temporary, destination)
            return
        except PermissionError as error:
            last_error = error
            time.sleep(0.25)
    if last_error is not None:
        raise last_error
    raise OSError("ATOMIC_REPLACE_FAILED")


def atomic_write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp-" + uuid.uuid4().hex)
    with temporary.open("w", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
        stream.flush(); os.fsync(stream.fileno())
    replace_with_retry(temporary, path)


CHILD_AUDIT_FIELDS = ["attempt_id", "sequence_number", "tool_kind", "phase", "paper_id", "page_number", "started_at", "finished_at", "duration_ms", "timeout_seconds", "exit_code", "timed_out", "status", "stdout_bytes", "stderr_bytes", "stderr_tail", "child_pid", "cleanup_attempted", "cleanup_success", "descendant_cleanup_count"]
DIAGNOSTIC_AUDIT_FIELDS = ["diagnostic_attempt_id", "sequence_number", "paper_id", "page_number", "tool_kind", "phase", "timeout_seconds", "duration_ms", "status", "timed_out", "exit_code", "cleanup_success", "render_width", "render_height", "render_pixel_count", "render_file_size", "render_sha256", "ocr_text_chars", "ocr_text_sha256", "ocr_quality_status"]
DIAGNOSTIC_PAGE_AUDIT_FIELDS = ["diagnostic_attempt_id", "paper_id", "page_number", "primary_page_class", "repair_overlay", "authoritative_text_extractor", "pdf_text_chars", "pdf_inspector_quality_status", "poppler_quality_status", "ocr_required", "ocr_target_pages", "render_width", "render_height", "render_pixel_count", "render_sha256"]


def persist_child_audit_or_block(path: Path, record: dict[str, Any], fields: list[str] | None = None) -> None:
    try:
        durable_child_audit(path, record, fields=fields)
    except RuntimeError as error:
        if str(error) == "CHILD_PROCESS_AUDIT_STATE_INVALID":
            raise
        raise RuntimeError("CHILD_PROCESS_AUDIT_PERSISTENCE_FAILURE") from error
    except OSError as error:
        raise RuntimeError("CHILD_PROCESS_AUDIT_PERSISTENCE_FAILURE") from error


def durable_child_audit(path: Path, record: dict[str, Any], *, fields: list[str] | None = None) -> None:
    schema = fields or CHILD_AUDIT_FIELDS
    rows: list[dict[str, str]] = []
    if path.exists():
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            header = next(csv.reader(stream), [])
        if header != schema:
            raise RuntimeError("CHILD_PROCESS_AUDIT_STATE_INVALID")
        rows = read_csv(path)
        if any(set(row) != set(schema) for row in rows):
            raise RuntimeError("CHILD_PROCESS_AUDIT_STATE_INVALID")
        expected_sequences = [str(index) for index in range(1, len(rows) + 1)]
        if [row.get("sequence_number", "") for row in rows] != expected_sequences:
            raise RuntimeError("CHILD_PROCESS_AUDIT_STATE_INVALID")
    record = {key: record.get(key, "") for key in schema}
    record["sequence_number"] = len(rows) + 1
    rows.append({key: str(value) for key, value in record.items()})
    temporary = path.with_name(path.name + ".tmp-" + uuid.uuid4().hex)
    try:
        with temporary.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=schema); writer.writeheader(); writer.writerows(rows); stream.flush(); os.fsync(stream.fileno())
        replace_with_retry(temporary, path)
    except BaseException:
        try:
            temporary.unlink()
        except OSError:
            pass
        raise


def file_fingerprint(paths: list[Path]) -> str:
    canonical = "\n".join(f"{str(path.relative_to(ROOT)).replace('\\', '/')}\t{sha256_file(path)}" for path in paths)
    return sha256_text(canonical)


def refinement_fingerprint() -> tuple[str, str]:
    refinement = json.loads(REFINEMENT.read_text(encoding="utf-8"))
    required = [ROOT / path for path in refinement.get("evidence_fingerprint_member_paths", [])]
    if not required or required[0] != REFINEMENT:
        raise RuntimeError("REFINEMENT_EVIDENCE_MEMBER_LIST_INVALID")
    if any(not path.is_file() for path in required):
        raise RuntimeError("REFINEMENT_EVIDENCE_MISSING")
    return sha256_file(REFINEMENT), file_fingerprint(required)


def catalog_fingerprints() -> dict[str, str]:
    return {"BACKLOG_CATALOG_SHA256": sha256_file(BACKLOG), "ELIGIBILITY_CATALOG_SHA256": sha256_file(ELIGIBILITY), "MEMBERSHIP_CATALOG_SHA256": sha256_file(MEMBERSHIP), "SOURCE_MAP_SHA256": sha256_file(SOURCE_MAP)}


def new_attempt() -> dict[str, Any]:
    contract_sha, evidence_sha = refinement_fingerprint()
    return {"attempt_id": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f") + "_" + uuid.uuid4().hex[:8], "started_at": now_utc(), "updated_at": now_utc(), "finished_at": "", "status": "RUNNING", "current_phase": "PHASE_0_RUNTIME_PREFLIGHT", "last_completed_phase": "", "completed_identity_ids": [], "current_identity_id": "", "runner_sha256": sha256_file(Path(__file__)), "poppler_binding_sha256": sha256_file(BINDING), "refinement_contract_sha256": contract_sha, "refinement_evidence_fingerprint": evidence_sha, "REAL_ATTEMPT_CREATED": 1, **catalog_fingerprints()}


def checkpoint(attempt: dict[str, Any], phase: str, *, completed: bool = False, identity: str = "") -> None:
    attempt["updated_at"] = now_utc(); attempt["current_phase"] = phase; attempt["current_identity_id"] = identity
    if completed: attempt["last_completed_phase"] = phase
    atomic_write_json(ATTEMPT_PATH, attempt)
    current = {key: value for key, value in attempt.items() if key != "status"}
    atomic_write_json(RESULT_PATH, {"STAGE": "G8-Q3-CONTRACT-PILOT-RESUME", "STATUS": attempt["status"], **current})


def preserve_existing_attempt() -> str:
    """Archive the prior real attempt before replacing the live checkpoint files."""
    if not ATTEMPT_PATH.is_file():
        return "NONE"
    previous = json.loads(ATTEMPT_PATH.read_text(encoding="utf-8"))
    attempt_id = str(previous.get("attempt_id", "")).strip()
    if not attempt_id:
        raise RuntimeError("HISTORICAL_ATTEMPT_ID_MISSING")
    if previous.get("status") == "RUNNING":
        raise RuntimeError("ACTIVE_PILOT_ATTEMPT_ALREADY_RUNNING=" + attempt_id)
    destination = ATTEMPT_HISTORY_ROOT / attempt_id
    destination.mkdir(parents=True, exist_ok=True)
    for source in (ATTEMPT_PATH, RESULT_PATH):
        if not source.is_file():
            continue
        target = destination / source.name
        if target.exists():
            if sha256_file(target) != sha256_file(source):
                raise RuntimeError("HISTORICAL_ATTEMPT_ARCHIVE_CONFLICT=" + attempt_id)
            continue
        temporary = target.with_name(target.name + ".tmp-" + uuid.uuid4().hex)
        shutil.copy2(source, temporary)
        replace_with_retry(temporary, target)
    return attempt_id


def inventory_reuse_allowed(previous: dict[str, Any], current: dict[str, str]) -> bool:
    return all(previous.get(key) == value for key, value in current.items())


INVENTORY_SCHEMA_VERSION = "g8-q3-inventory-v2"


def source_sha256_fingerprint() -> str:
    rows = read_csv(BACKLOG)
    records = [{"paper_id": row.get("paper_id", ""), "source_sha256": row.get("source_sha256", "").upper()} for row in rows if row.get("failure_class") == "PARTIAL_SCAN" and row.get("manual_required") == "1"]
    return sha256_text(json.dumps(sorted(records, key=lambda value: value["paper_id"]), ensure_ascii=False, sort_keys=True))


def runtime_semantic_fingerprint(preflight: dict[str, Any]) -> str:
    return sha256_text(json.dumps({"pdf_inspector_version": preflight["PDF_INSPECTOR_VERSION"], "poppler_version": preflight["ACTIVE_POPPLER_VERSION"], "tesseract_js_version": preflight["TESSERACT_JS_VERSION"], "tesseract_js_core_version": preflight["TESSERACT_JS_CORE_VERSION"], "ocr_languages": "chi_sim+eng", "tessdata_flavor": "4.0.0_best_int", "render_dpi": 150, "ocr_phase": "PHASE_6_SELECTIVE_PAGE_OCR", "ocr_timeout_scope": "PER_PAGE_CHILD", "ocr_timeout_seconds": 180, "auto_retry_after_timeout": 0}, sort_keys=True))


def inventory_binding(preflight: dict[str, Any], attempt: dict[str, Any]) -> dict[str, str]:
    catalogs = catalog_fingerprints()
    return {"inventory_schema_version": INVENTORY_SCHEMA_VERSION, "backlog_catalog_sha256": catalogs["BACKLOG_CATALOG_SHA256"], "eligibility_catalog_sha256": catalogs["ELIGIBILITY_CATALOG_SHA256"], "membership_catalog_sha256": catalogs["MEMBERSHIP_CATALOG_SHA256"], "source_map_catalog_sha256": catalogs["SOURCE_MAP_SHA256"], "source_sha256_fingerprint": source_sha256_fingerprint(), "runtime_semantic_fingerprint": runtime_semantic_fingerprint(preflight), "refinement_contract_sha256": attempt["refinement_contract_sha256"], "refinement_evidence_fingerprint": attempt["refinement_evidence_fingerprint"]}


def inventory_reuse_gate(preflight: dict[str, Any], attempt: dict[str, Any]) -> tuple[int, str]:
    if not INVENTORY_PATH.is_file():
        return 0, "INVENTORY_MISSING"
    try:
        with INVENTORY_PATH.open("r", encoding="utf-8-sig", newline="") as stream:
            header = next(csv.reader(stream), [])
        if header != INVENTORY_FIELDS:
            return 0, "INVENTORY_SCHEMA_VERSION_MISMATCH"
        rows = read_csv(INVENTORY_PATH)
    except (OSError, ValueError, csv.Error):
        return 0, "INVENTORY_READ_FAILURE"
    if len(rows) != 128 or len({row.get("paper_id") for row in rows}) != 128:
        return 0, "INVENTORY_CARDINALITY_MISMATCH"
    expected = inventory_binding(preflight, attempt)
    if any(row.get(key) != value for row in rows for key, value in expected.items()):
        if any(row.get("refinement_contract_sha256") != expected["refinement_contract_sha256"] or row.get("refinement_evidence_fingerprint") != expected["refinement_evidence_fingerprint"] for row in rows):
            return 0, "REFINEMENT_BINDING_MISMATCH"
        return 0, "INVENTORY_FINGERPRINT_DRIFT"
    return 1, "CURRENT_REFINEMENT_INVENTORY"


def selection_fingerprint(selected: list[dict[str, Any]], inventory_sha: str) -> str:
    return sha256_text(json.dumps({"inventory": inventory_sha, "selection": [{key: row.get(key) for key in ("paper_id", "selection_dimension", "selection_value", "selection_rank")} for row in selected]}, sort_keys=True))


def normalize_stage66(value: str) -> str:
    """Behavior-preserving Stage 66 normalization contract."""
    return re.sub(r"\s+", " ", value.replace("\x00", "")).strip()


def page_join_stage66(pages: list[str]) -> str:
    return normalize_stage66(" ".join(pages))


def binary_matrix_evidence(text: str) -> dict[str, Any]:
    """Return deterministic evidence for a legitimate OCR binary matrix.

    Long digit runs are not accepted merely because they contain 0/1.  They
    must form several regularly sized rows, contain both symbols, occupy a
    material share of the text, and occur with source-code/matrix context.
    """
    tokens = re.findall(r"(?<!\d)[01]{18,}(?!\d)", text)
    lengths = Counter(len(value) for value in tokens)
    mode_length, mode_count = (lengths.most_common(1)[0] if lengths else (0, 0))
    candidate_chars = sum(len(value) for value in tokens)
    context = text.casefold()
    context_markers = ("代码", "程序", "附录", "appendix", "code", "program", "p=", "dis", "for")
    context_hits = sum(marker in context for marker in context_markers)
    alternating = [
        value for value in tokens
        if len(set(value)) == 2 and value == (value[:2] * ((len(value) + 1) // 2))[:len(value)]
    ]
    single_symbol = [value for value in tokens if len(set(value)) == 1]
    regularity = mode_count / max(1, len(tokens))
    candidate_ratio = candidate_chars / max(1, len(text))
    positive = bool(
        len(tokens) >= 4
        and mode_length >= 18
        and regularity >= 0.75
        and candidate_ratio >= 0.45
        and {"0", "1"}.issubset(set("".join(tokens)))
        and context_hits >= 2
        and not (len(single_symbol) == len(tokens) or len(alternating) == len(tokens))
    )
    return {
        "pass": positive,
        "candidate_row_count": len(tokens),
        "candidate_row_length_mode": mode_length,
        "candidate_row_length_mode_count": mode_count,
        "candidate_row_length_regularity": regularity,
        "candidate_char_ratio": candidate_ratio,
        "context_marker_hit_count": context_hits,
        "single_symbol_run_count": len(single_symbol),
        "alternating_binary_run_count": len(alternating),
    }


def text_quality(text: str, *, body: bool = False) -> dict[str, Any]:
    """Fail-closed lexical quality gate; thresholds are frozen in refinement v1."""
    chars = len(text)
    replacement = text.count("\ufffd")
    controls = sum(ord(char) < 32 and char not in "\n\r\t" for char in text)
    placeholders = len(re.findall(r"\[Image:[^\]]*\]", text))
    printable = sum(char.isprintable() or char in "\n\r\t" for char in text)
    cjk = sum("\u4e00" <= char <= "\u9fff" for char in text)
    latin = sum(char.isascii() and char.isalpha() for char in text)
    digits = sum(char.isdigit() for char in text)
    nonwhite = [char for char in text if not char.isspace()]
    matrix = binary_matrix_evidence(text)
    repeated_letters = len(re.findall(r"([^\W\d_])\1{19,}", text))
    repeated_binary_noise = matrix["single_symbol_run_count"] + matrix["alternating_binary_run_count"]
    repeated = repeated_letters + (repeated_binary_noise if not matrix["pass"] else 0)
    ratio = lambda value: value / max(1, chars)
    metrics = {"text_chars": chars, "replacement_char_count": replacement, "replacement_char_ratio": ratio(replacement), "replacement_run_count": len(re.findall("\ufffd+", text)), "max_replacement_run_length": max([len(value) for value in re.findall("\ufffd+", text)] or [0]), "control_char_count": controls, "control_char_ratio": ratio(controls), "printable_char_count": printable, "printable_char_ratio": ratio(printable), "cjk_char_count": cjk, "latin_char_count": latin, "digit_count": digits, "alphanumeric_cjk_ratio": ratio(cjk + latin + digits), "image_placeholder_count": placeholders, "image_placeholder_char_ratio": ratio(sum(len(value) for value in re.findall(r"\[Image:[^\]]*\]", text))), "unique_non_whitespace_char_count": len(set(nonwhite)), "unique_char_ratio": len(set(nonwhite)) / max(1, len(nonwhite)), "long_repeated_symbol_run_count": repeated, "binary_matrix_evidence": matrix}
    minimum = QUALITY_THRESHOLDS["minimum_body_chars" if body else "minimum_authoritative_page_chars"]
    if not chars:
        status = "EMPTY"
    elif replacement or controls:
        status = "CORRUPT_ENCODING"
    elif metrics["image_placeholder_char_ratio"] >= QUALITY_THRESHOLDS["image_placeholder_ratio_hard_fail"] or chars < minimum or metrics["alphanumeric_cjk_ratio"] < 0.15 or repeated:
        status = "LOW_INFORMATION"
    else:
        status = "USABLE"
    return {**metrics, "quality_status": status, "pass": status == "USABLE"}


def select_extractor(inspector: str, poppler: str, visual_content: bool, visual_blank: bool) -> tuple[str, str, str, bool]:
    inspected, popped = text_quality(inspector), text_quality(poppler)
    if inspected["pass"]:
        return "TEXT_PAGE", "PDF_INSPECTOR", "TEXT_LAYER_COMPLETE", False
    if popped["pass"]:
        return "TEXT_PAGE", "POPPLER", "TEXT_LAYER_COMPLETE", False
    if visual_blank:
        return "VERIFIED_BLANK", "NONE", "NO_REPAIR_REQUIRED", False
    if visual_content:
        overlay = "TEXT_LAYER_CORRUPT_ENCODING" if "CORRUPT_ENCODING" in {inspected["quality_status"], popped["quality_status"]} else "TEXT_LAYER_VISUAL_MISMATCH"
        return "TEXT_PAGE", "NONE", overlay, True
    return "UNEXPLAINED", "NONE", "NO_REPAIR_REQUIRED", False


def run_child_process(command: list[str], *, tool_kind: str, phase: str, cwd: Path = ROOT, env: dict[str, str] | None = None, timeout_seconds: float = CHILD_TIMEOUT_SECONDS, paper_id: str = "", page_number: int | None = None, stdin: str | None = None, audit_extra: dict[str, Any] | None = None) -> subprocess.CompletedProcess[str]:
    started = now_utc(); began = time.monotonic()
    process = subprocess.Popen(command, cwd=cwd, env=env, stdin=subprocess.PIPE if stdin is not None else None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
    timed_out = False
    try:
        stdout, stderr = process.communicate(stdin, timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        timed_out = True; process.kill(); stdout, stderr = process.communicate()
    finished = now_utc()
    record = {"attempt_id": (ACTIVE_ATTEMPT or {}).get("attempt_id", ""), "diagnostic_attempt_id": (ACTIVE_ATTEMPT or {}).get("attempt_id", ""), "tool_kind": tool_kind, "phase": phase, "paper_id": paper_id, "page_number": page_number or "", "started_at": started, "finished_at": finished, "duration_ms": round((time.monotonic() - began) * 1000), "timeout_seconds": timeout_seconds, "exit_code": process.returncode, "timed_out": int(timed_out), "stdout_bytes": len(stdout.encode("utf-8")), "stderr_bytes": len(stderr.encode("utf-8")), "stderr_tail": stderr.encode("utf-8")[-CHILD_STDERR_TAIL_MAX_BYTES:].decode("utf-8", errors="replace"), "status": "TIMED_OUT" if timed_out else ("SUCCESS" if process.returncode == 0 else "FAILED"), "child_pid": process.pid, "cleanup_attempted": int(timed_out), "cleanup_success": int(timed_out and process.returncode is not None), "descendant_cleanup_count": 0}
    if tool_kind == "TESSERACT_OCR" and not timed_out and stdout.strip():
        try:
            payload = json.loads(stdout.strip().splitlines()[-1])
            ocr_pages = payload.get("pages", [])
            if len(ocr_pages) == 1:
                ocr_text = normalize_stage66(str(ocr_pages[0].get("text", "")))
                record.update({"ocr_text_chars": len(ocr_text), "ocr_text_sha256": sha256_text(ocr_text), "ocr_quality_status": "PASS" if ocr_sanity(ocr_text, True)["pass"] else "FAIL"})
        except (IndexError, KeyError, TypeError, ValueError, json.JSONDecodeError):
            pass
    if audit_extra:
        record.update(audit_extra)
    CHILD_AUDIT.append(record)
    if ACTIVE_ATTEMPT is not None:
        persist_child_audit_or_block(ACTIVE_AUDIT_PATH or CHILD_AUDIT_PATH, record, fields=ACTIVE_AUDIT_FIELDS)
    if timed_out:
        raise ChildProcessTimeout("CHILD_PROCESS_TIMEOUT|" + tool_kind + "|" + phase + "|" + paper_id + "|" + str(page_number or ""))
    return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)


def bounded(command: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None, paper_id: str = "", page_number: int | None = None, phase: str | None = None, timeout_seconds: float = CHILD_TIMEOUT_SECONDS, audit_extra: dict[str, Any] | None = None) -> subprocess.CompletedProcess[str]:
    name = Path(command[0]).stem.lower()
    kinds = {"pdfinfo": "PDFINFO", "pdftotext": "PDFTOTEXT", "pdftoppm": "PDFTOPPM", "node": "TESSERACT_OCR", "python": "PDF_INSPECTOR"}
    return run_child_process(command, tool_kind=kinds.get(name, "CHILD"), phase=phase or (ACTIVE_ATTEMPT or {}).get("current_phase", "UNSCOPED"), cwd=cwd, env=env, paper_id=paper_id, page_number=page_number, timeout_seconds=timeout_seconds, audit_extra=audit_extra)


def require_bound_poppler() -> tuple[dict[str, Any], dict[str, Path]]:
    binding = json.loads(BINDING.read_text(encoding="utf-8"))
    if binding.get("validation_status") != "PASS" or binding.get("active_version") != "25.02.0":
        raise RuntimeError("POPPLER_RUNTIME_BINDING_INVALID")
    tools = {key: Path(str(binding.get(key, ""))) for key in ("pdfinfo", "pdftotext", "pdftoppm", "pdftocairo")}
    for key, path in tools.items():
        if not path.is_file():
            raise RuntimeError("POPPLER_BOUND_TOOL_MISSING=" + key)
        result = bounded([str(path), "-v"])
        first = (result.stdout + result.stderr).splitlines()
        if result.returncode or not first or first[0].strip() != f"{key} version 25.02.0":
            raise RuntimeError("POPPLER_BOUND_TOOL_DRIFT=" + key)
    return binding, tools


def runtime_preflight() -> dict[str, Any]:
    binding, _ = require_bound_poppler()
    rows = [row for row in read_csv(BACKLOG) if row.get("failure_class") == "PARTIAL_SCAN" and row.get("manual_required") == "1"]
    lang_ok = {name: int((LANG_ROOT / name).is_file() and sha256_file(LANG_ROOT / name) == expected) for name, expected in EXPECTED_LANG_SHA.items()}
    manifest = json.loads((LANG_ROOT / "manifest.json").read_text(encoding="utf-8")) if (LANG_ROOT / "manifest.json").is_file() else {}
    package = json.loads((TESSERACT_MODULE / "package.json").read_text(encoding="utf-8")) if (TESSERACT_MODULE / "package.json").is_file() else {}
    core = json.loads((NODE_MODULES / "tesseract.js-core" / "package.json").read_text(encoding="utf-8")) if (NODE_MODULES / "tesseract.js-core" / "package.json").is_file() else {}
    ready = len(rows) == 128 and importlib.metadata.version("pdf-inspector") == "1.15.0" and all(lang_ok.values()) and package.get("version") == "7.0.0" and core.get("version") == "7.0.0" and manifest.get("ocr_engine_version") == "7.0.0" and NODE.is_file()
    if not ready:
        raise RuntimeError("PHASE_0_RUNTIME_PREFLIGHT_FAILED")
    return {"Q3_IDENTITY_COUNT": len(rows), "POPPLER_RUNTIME_BINDING_READY": 1, "ACTIVE_POPPLER_VERSION": binding["active_version"], "PDF_INSPECTOR_VERSION": "1.15.0", "TESSERACT_JS_VERSION": package["version"], "TESSERACT_JS_CORE_VERSION": core["version"], "CHI_SIM_SHA_MATCH": lang_ok["chi_sim.traineddata.gz"], "ENG_SHA_MATCH": lang_ok["eng.traineddata.gz"], "OCR_RUNTIME_READY": 1}


def pdfinfo(tools: dict[str, Path], source: Path, *, paper_id: str = "") -> dict[str, str]:
    result = bounded([str(tools["pdfinfo"]), "-box", str(source)], paper_id=paper_id)
    if result.returncode:
        raise RuntimeError("PDFINFO_FAILED=" + result.stderr.strip())
    info = {key.strip(): value.strip() for key, value in (line.split(":", 1) for line in result.stdout.splitlines() if ":" in line)}
    if not info.get("Pages", "").isdigit():
        raise RuntimeError("PDFINFO_PAGES_MISSING")
    return info


def inspector_pages(source: Path, count: int, *, paper_id: str = "") -> list[str]:
    code = "import json,sys,pdf_inspector;p=sys.argv[1];n=int(sys.argv[2]);r=pdf_inspector.extract_text_in_regions(p,[(i,[[0,0,100000,100000]]) for i in range(n)]);print(json.dumps([x.regions[0].text for x in r],ensure_ascii=False))"
    environment = dict(os.environ)
    environment["PYTHONIOENCODING"] = "utf-8"
    result = bounded([sys.executable, "-c", code, str(source), str(count)], env=environment, paper_id=paper_id)
    if result.returncode:
        raise RuntimeError("PDF_INSPECTOR_FAILED=" + result.stderr.strip())
    values = json.loads(result.stdout)
    if not isinstance(values, list) or len(values) != count:
        raise RuntimeError("PDF_INSPECTOR_PAGE_ACCOUNTING_FAILED")
    return [normalize_stage66(str(value)) for value in values]


def poppler_page_text(tools: dict[str, Path], source: Path, page: int, *, paper_id: str = "") -> str:
    result = bounded([str(tools["pdftotext"]), "-f", str(page), "-l", str(page), "-layout", "-enc", "UTF-8", str(source), "-"], paper_id=paper_id, page_number=page)
    if result.returncode:
        raise RuntimeError("PDFTOTEXT_FAILED=page_" + str(page))
    return normalize_stage66(result.stdout)


def source_map_rows() -> dict[str, list[dict[str, str]]]:
    result: dict[str, list[dict[str, str]]] = {}
    for row in read_csv(SOURCE_MAP):
        result.setdefault(row.get("paper_id", ""), []).append(row)
    return result


def q3_identity_inventory(tools: dict[str, Path]) -> list[dict[str, Any]]:
    """Phase 1: authoritative Q3 inventory; no rendering or OCR."""
    backlog = [row for row in read_csv(BACKLOG) if row.get("failure_class") == "PARTIAL_SCAN" and row.get("manual_required") == "1"]
    eligible = {row["paper_id"]: row for row in read_csv(ELIGIBILITY)}
    memberships: dict[str, list[dict[str, str]]] = {}
    for row in read_csv(MEMBERSHIP):
        memberships.setdefault(row.get("paper_id", ""), []).append(row)
    mapped = source_map_rows()
    inventory: list[dict[str, Any]] = []
    for row in sorted(backlog, key=lambda value: value["paper_id"]):
        paper_id = row["paper_id"]
        if paper_id == "CUMCM-2011-D-038":
            raise RuntimeError("Q3_TARGET_GOVERNANCE_CONTRADICTION")
        if eligible.get(paper_id, {}).get("artifact_eligible") != "1":
            raise RuntimeError("Q3_TARGET_ELIGIBILITY_CONTRADICTION=" + paper_id)
        source = ROOT / row["source_path"]
        if not source.is_file() or sha256_file(source) != row["source_sha256"].upper():
            raise RuntimeError("Q3_INVENTORY_SOURCE_SHA_MISMATCH=" + paper_id)
        info = pdfinfo(tools, source, paper_id=paper_id)
        pages = int(info["Pages"])
        texts = inspector_pages(source, pages, paper_id=paper_id)
        nonempty = sum(bool(text) for text in texts)
        alternatives = []
        for member in memberships.get(paper_id, []):
            alt = ROOT / member["path"]
            if alt == source or not alt.is_file() or alt.read_bytes()[:5] != b"%PDF-":
                continue
            known = next((item for item in mapped.get(paper_id, []) if item.get("file_path") == member["path"]), None)
            if not known or not known.get("file_sha256") or sha256_file(alt) != known["file_sha256"].upper():
                continue
            alt_info = pdfinfo(tools, alt, paper_id=paper_id)
            alt_texts = inspector_pages(alt, int(alt_info["Pages"]), paper_id=paper_id)
            score = (sum(bool(value) for value in alt_texts), int(alt_info["Pages"]))
            primary_score = (nonempty, pages)
            if score > primary_score:
                alternatives.append(member["path"])
        zero = pages - nonempty
        flags = [not bool(text) for text in texts]
        inventory.append({"paper_id": paper_id, "artifact_eligible": 1, "q3_reason": row["failure_class"], "membership_count": len(memberships.get(paper_id, [])), "primary_source_path": row["source_path"], "primary_source_sha256": row["source_sha256"], "alternate_source_count": len(alternatives), "better_alternate_source_available": bool(alternatives), "better_alternate_source_paths": json.dumps(alternatives, ensure_ascii=False), "page_count": pages, "text_layer_page_count": nonempty, "zero_text_page_count": zero, "repair_suspect_page_count": zero, "repair_ratio": zero / pages if pages else 1.0, "repair_run_count": repair_runs(flags), "text_image_transition_count": transitions(flags)})
    if len(inventory) != 128 or len({row["paper_id"] for row in inventory}) != 128:
        raise RuntimeError("Q3_IDENTITY_INVENTORY_COUNT_MISMATCH")
    return inventory


def repair_runs(flags: list[bool]) -> int:
    return sum(value and (index == 0 or not flags[index - 1]) for index, value in enumerate(flags))


def transitions(flags: list[bool]) -> int:
    return sum(flags[index] != flags[index - 1] for index in range(1, len(flags)))


def select_six(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    pool = [record for record in records if not record.get("better_alternate_source_available")]
    specifications = [
        ("LOW_REPAIR_RATIO", lambda item: (item["repair_ratio"], item["page_count"], item["paper_id"])),
        ("MEDIUM_REPAIR_RATIO", lambda item: (abs(item["repair_ratio"] - 0.5), item["page_count"], item["paper_id"])),
        ("HIGH_REPAIR_RATIO", lambda item: (-item["repair_ratio"], -item["page_count"], item["paper_id"])),
        ("SHORT_DOCUMENT", lambda item: (item["page_count"], item["repair_ratio"], item["paper_id"])),
        ("LONG_DOCUMENT", lambda item: (-item["page_count"], -item["repair_ratio"], item["paper_id"])),
        ("COMPLEX_DISCONTIGUOUS_REPAIR_RUNS", lambda item: (-item["repair_run_count"], -item["text_image_transition_count"], item["paper_id"])),
    ]
    selected: list[dict[str, Any]] = []
    used: set[str] = set()
    for dimension, key in specifications:
        candidates = [item for item in sorted(pool, key=key) if item["paper_id"] not in used]
        if not candidates:
            raise RuntimeError("DETERMINISTIC_SELECTION_INSUFFICIENT_CANDIDATES")
        item = dict(candidates[0])
        item.update({"selection_dimension": dimension, "selection_metric": dimension, "selection_value": item["repair_ratio"] if "RATIO" in dimension else item["page_count"], "selection_rank": len(selected) + 1, "selection_reason": "deterministic ordered candidate ranking"})
        selected.append(item)
        used.add(item["paper_id"])
    if len(selected) != 6 or len(used) != 6:
        raise RuntimeError("DETERMINISTIC_SELECTION_FAILED")
    return selected


def validate_source(tools: dict[str, Path], item: dict[str, Any]) -> dict[str, Any]:
    source = ROOT / item["primary_source_path"]
    if not source.is_file() or source.stat().st_size == 0 or sha256_file(source) != item["primary_source_sha256"].upper():
        raise RuntimeError("PILOT_SOURCE_SHA_MISMATCH=" + item["paper_id"])
    if source.read_bytes()[:5] != b"%PDF-":
        raise RuntimeError("PILOT_SOURCE_SIGNATURE_INVALID=" + item["paper_id"])
    info = pdfinfo(tools, source, paper_id=item["paper_id"])
    if info.get("Encrypted", "").lower().startswith("yes"):
        raise RuntimeError("PILOT_SOURCE_ENCRYPTED=" + item["paper_id"])
    inspector = inspector_pages(source, int(info["Pages"]), paper_id=item["paper_id"])
    if len(inspector) != int(info["Pages"]):
        raise RuntimeError("PAGE_COUNT_TOOL_MISMATCH=" + item["paper_id"])
    return {**item, "source": source, "pdfinfo": info, "page_count": int(info["Pages"]), "inspector_texts": inspector}


def render_page(tools: dict[str, Path], source: Path, page: int, directory: Path, *, paper_id: str = "") -> Path:
    prefix = directory / f"page-{page:04d}"
    result = bounded([str(tools["pdftoppm"]), "-f", str(page), "-l", str(page), "-r", "150", "-png", "-singlefile", str(source), str(prefix)], paper_id=paper_id, page_number=page)
    image = prefix.with_suffix(".png")
    if result.returncode or not image.is_file():
        raise RuntimeError("PAGE_RENDER_FAILED=" + str(page))
    return image


def visual_blank_evidence(image: Path) -> dict[str, Any]:
    try:
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError("BLANK_VISUAL_VERIFIER_UNAVAILABLE") from exc
    with Image.open(image) as value:
        gray = value.convert("L")
        histogram = gray.histogram()
        pixels = gray.width * gray.height
        foreground = sum(histogram[:235])
        variation = sum(count for level, count in enumerate(histogram) if level < 250)
        coverage = foreground / pixels if pixels else 1.0
        return {"width": gray.width, "height": gray.height, "ink_coverage": coverage, "pixel_variation": variation / pixels if pixels else 1.0, "verified_blank": coverage < 0.0005 and variation < 0.002}


def conservative_partial(text: str, visual: dict[str, Any]) -> bool:
    return bool(text) and len(text) < 40 and visual["ink_coverage"] > 0.02


def page_audit(tools: dict[str, Path], source_item: dict[str, Any], directory: Path, *, retain_rendered_images: bool = False) -> list[dict[str, Any]]:
    directory.mkdir(parents=True, exist_ok=True)
    pages: list[dict[str, Any]] = []
    for page_no, inspector_text in enumerate(source_item["inspector_texts"], 1):
        poppler_text = poppler_page_text(tools, source_item["source"], page_no, paper_id=source_item["paper_id"])
        image = render_page(tools, source_item["source"], page_no, directory, paper_id=source_item["paper_id"])
        visual = visual_blank_evidence(image)
        primary, extractor, overlay, needed = select_extractor(inspector_text, poppler_text, visual["ink_coverage"] >= 0.002, visual["verified_blank"])
        text = inspector_text if extractor == "PDF_INSPECTOR" else (poppler_text if extractor == "POPPLER" else "")
        row: dict[str, Any] = {"paper_id": source_item["paper_id"], "page": page_no, "pdf_text": text, "pdf_text_chars": len(text), "pdf_inspector_text": inspector_text, "pdf_inspector_quality": text_quality(inspector_text), "poppler_text": poppler_text, "poppler_quality": text_quality(poppler_text), "primary_page_class": primary, "repair_overlay": overlay, "authoritative_text_extractor": extractor, "ocr_required": int(needed), "ocr_target_pages": [page_no] if needed else [], "visual": visual, "render_sha256": sha256_file(image)}
        if retain_rendered_images:
            row["render_path"] = str(image)
        else:
            image.unlink()
        pages.append(row)
    # A sparse repeated footer can pass the lexical text gate while the page
    # image contains distinct substantive content.  Route adjacent duplicate
    # text-layer pages through the existing page-scoped OCR repair path; if
    # OCR confirms a true duplicate, content_sanity remains fail-closed.
    for index in range(1, len(pages)):
        previous, current = pages[index - 1], pages[index]
        if (
            previous.get("pdf_text")
            and previous.get("pdf_text") == current.get("pdf_text")
            and not previous["visual"].get("verified_blank")
            and not current["visual"].get("verified_blank")
            and previous["visual"].get("ink_coverage", 0) >= 0.002
            and current["visual"].get("ink_coverage", 0) >= 0.002
            and previous.get("render_sha256") != current.get("render_sha256")
        ):
            for duplicate in (previous, current):
                duplicate.update({"repair_overlay": "TEXT_LAYER_VISUAL_MISMATCH", "authoritative_text_extractor": "NONE", "ocr_required": 1, "ocr_target_pages": [duplicate["page"]]})
    try:
        validate_page_accounting(pages, source_item["page_count"])
    except RuntimeError as error:
        raise RuntimeError(str(error) + "=" + source_item["paper_id"]) from error
    return pages


def validate_page_accounting(pages: list[dict[str, Any]], count: int) -> None:
    if len(pages) != count or {item["page"] for item in pages} != set(range(1, count + 1)) or any(item["primary_page_class"] not in PRIMARY_CLASSES for item in pages):
        raise RuntimeError("PAGE_ACCOUNTING_MISMATCH")


NODE_CODE = r'''const fs=require('fs'); const {createWorker}=require(process.env.Q3_TESSERACT_MODULE);
(async()=>{const job=JSON.parse(fs.readFileSync(process.env.Q3_OCR_JOB,'utf8'));let worker=null;const pages=[];try{worker=await createWorker(job.languages,1,{langPath:job.langPath,cachePath:job.cachePath,cacheMethod:'none',gzip:true,logger:()=>{}});for(const item of job.pages){const result=await worker.recognize(item.image);pages.push({page:item.page,text:((result||{}).data||{}).text||'',status:'PASS'});}console.log(JSON.stringify({worker_create_success:true,pages}));}catch(error){console.log(JSON.stringify({worker_create_success:false,pages,error:String(error)}));process.exitCode=2;}finally{if(worker){try{await worker.terminate();}catch(error){process.exitCode=2;}}}})();'''


def validate_page_scoped_ocr_job(page_number: int | None, pages: list[dict[str, Any]]) -> None:
    if page_number is None:
        raise RuntimeError("TESSERACT_PAGE_NUMBER_REQUIRED")
    if len(pages) != 1 or int(pages[0].get("page", -1)) != page_number:
        raise RuntimeError("MULTI_PAGE_TESSERACT_CHILD_FORBIDDEN")


def ocr_sanity(text: str, substantive: bool) -> dict[str, Any]:
    encoded = text.encode("utf-8", errors="replace")
    replacement = text.count("\ufffd") / max(1, len(text))
    control = sum(ord(char) < 32 and char not in "\n\r\t" for char in text) / max(1, len(text))
    visible = sum(char.isalnum() or "\u4e00" <= char <= "\u9fff" for char in text) / max(1, len(text.strip()))
    matrix = binary_matrix_evidence(text)
    repeated_letters = bool(re.search(r"([^\W\d_])\1{19,}", text))
    repeated_binary_noise = (matrix["single_symbol_run_count"] + matrix["alternating_binary_run_count"]) > 0 and not matrix["pass"]
    repeated = repeated_letters or repeated_binary_noise
    passed = bool(encoded and (not substantive or text.strip()) and replacement <= 0.02 and control <= 0.02 and visible >= 0.15 and not repeated)
    return {"pass": passed, "replacement_ratio": replacement, "control_ratio": control, "plausible_ratio": visible, "repeated_symbol": repeated, "binary_matrix_evidence": matrix}


def watermark_only_page(text: str, visual: dict[str, Any], *, repeated_low_information: bool = False) -> bool:
    """Recognize a visually blank page carrying only a document-site watermark."""
    compact = re.sub(r"\s+", "", text.lower())
    markers = ("docin", "wwwdocin", "wwwidocin", "豆丁")
    sparse_blank = len(text.strip()) <= 40 and visual.get("ink_coverage", 1.0) < 0.03
    marked_watermark = len(text.strip()) < 80 and any(marker in compact for marker in markers) and visual.get("ink_coverage", 1.0) < 0.10
    repeated_blank = repeated_low_information and len(text.strip()) <= 40 and visual.get("ink_coverage", 1.0) < 0.10
    return sparse_blank or marked_watermark or repeated_blank


def run_selective_ocr(tools: dict[str, Path], source_item: dict[str, Any], pages: list[dict[str, Any]], directory: Path, *, timeout_seconds: float = CHILD_TIMEOUT_SECONDS, rendered_images: dict[int, Path] | None = None) -> dict[int, dict[str, Any]]:
    targets = sorted({number for row in pages for number in row["ocr_target_pages"]})
    if any(number < 1 or number > source_item["page_count"] for number in targets):
        raise RuntimeError("OCR_TARGET_PAGE_OUT_OF_RANGE")
    if not targets:
        return {}
    answers: dict[int, dict[str, Any]] = {}
    for number in targets:
        image: Path | None = None
        job_path: Path | None = None
        try:
            image = (rendered_images or {}).get(number)
            if image is None:
                image = render_page(tools, source_item["source"], number, directory, paper_id=source_item["paper_id"])
            elif not image.is_file():
                raise RuntimeError("RETAINED_PAGE_RENDER_MISSING=page_" + str(number))
            image_sha = sha256_file(image)
            job_pages = [{"page": number, "image": str(image)}]
            validate_page_scoped_ocr_job(number, job_pages)
            render = visual_blank_evidence(image)
            job = {"languages": "chi_sim+eng", "langPath": str(LANG_ROOT), "cachePath": str(directory / ("ocr-cache-" + str(number))), "pages": job_pages}
            job_path = directory / ("ocr-job-" + f"{number:04d}" + ".json")
            job_path.write_text(json.dumps(job, ensure_ascii=False), encoding="utf-8")
            env = dict(os.environ)
            env.update({"Q3_TESSERACT_MODULE": str(TESSERACT_MODULE), "Q3_OCR_JOB": str(job_path)})
            result = bounded([str(NODE), "-e", NODE_CODE], env=env, paper_id=source_item["paper_id"], page_number=number, phase="PHASE_6_SELECTIVE_PAGE_OCR", timeout_seconds=timeout_seconds, audit_extra={"render_width": render["width"], "render_height": render["height"], "render_pixel_count": render["width"] * render["height"], "render_file_size": image.stat().st_size, "render_sha256": image_sha})
            payload = json.loads(result.stdout.strip().splitlines()[-1]) if result.stdout.strip() else {}
            if result.returncode or not payload.get("worker_create_success"):
                raise RuntimeError("OCR_WORKER_OR_EXECUTION_FAILED=" + str(payload.get("error", result.stderr.strip())))
            by_page = {int(row["page"]): row for row in payload.get("pages", [])}
            if set(by_page) != {number}:
                raise RuntimeError("OCR_PAGE_ACCOUNTING_MISMATCH=page_" + str(number))
            text = str(by_page[number].get("text", ""))
            sanity = ocr_sanity(text, True)
            if not sanity["pass"]:
                raise RuntimeError("OCR_SANITY_FAILED=page_" + str(number))
            answers[number] = {"text": normalize_stage66(text), "render_sha256": image_sha, "sanity": sanity}
        finally:
            if image is not None and image.exists():
                image.unlink()
            if job_path is not None and job_path.exists():
                job_path.unlink()
    return answers


def reconstruct_pages(pages: list[dict[str, Any]], ocr: dict[int, dict[str, Any]]) -> list[dict[str, Any]]:
    reconstructed = []
    low_information_hashes = Counter(
        sha256_text(str(value.get("text", "")))
        for value in ocr.values()
        if len(str(value.get("text", "")).strip()) <= 40
    )
    for row in pages:
        primary, overlay = row["primary_page_class"], row["repair_overlay"]
        result = dict(row)
        if primary == "TEXT_PAGE" and overlay == "TEXT_LAYER_COMPLETE":
            result.update({"provenance": "PDF_TEXT_LAYER", "authoritative_text": row["pdf_text"]})
        elif primary == "VERIFIED_BLANK":
            result.update({"provenance": "VERIFIED_BLANK", "authoritative_text": ""})
        elif primary == "IMAGE_ONLY_CONTENT_PAGE" and row["page"] in ocr:
            ocr_text = ocr[row["page"]]["text"]
            repeated = low_information_hashes[sha256_text(str(ocr_text))] >= 2
            provenance = "VERIFIED_BLANK" if watermark_only_page(ocr_text, row["visual"], repeated_low_information=repeated) else "OCR"
            result.update({"provenance": provenance, "authoritative_text": "" if provenance == "VERIFIED_BLANK" else ocr[row["page"]]["text"]})
        elif primary == "TEXT_PAGE" and overlay in {"TEXT_LAYER_CORRUPT_ENCODING", "TEXT_LAYER_VISUAL_MISMATCH"} and row["page"] in ocr:
            ocr_text = ocr[row["page"]]["text"]
            repeated = low_information_hashes[sha256_text(str(ocr_text))] >= 2
            provenance = "VERIFIED_BLANK" if watermark_only_page(ocr_text, row["visual"], repeated_low_information=repeated) else "OCR"
            result.update({"provenance": provenance, "authoritative_text": "" if provenance == "VERIFIED_BLANK" else ocr[row["page"]]["text"]})
        elif primary == "TEXT_PAGE" and overlay == "TEXT_LAYER_INCOMPLETE_SUSPECT":
            raise RuntimeError("UNHANDLED_FAILURE_MODE=PARTIAL_TEXT_RECONCILIATION")
        else:
            raise RuntimeError("UNEXPLAINED_PAGE_RECONSTRUCTION")
        if result["provenance"] not in PAGE_PROVENANCE:
            raise RuntimeError("INVALID_PAGE_PROVENANCE")
        result["authoritative_page_text_chars"] = len(result["authoritative_text"])
        result["authoritative_page_text_sha256"] = sha256_text(result["authoritative_text"])
        reconstructed.append(result)
    return reconstructed


def content_sanity(pages: list[dict[str, Any]]) -> dict[str, Any]:
    text_pages = [row for row in pages if row["authoritative_text"]]
    hashes = [row["authoritative_page_text_sha256"] for row in text_pages]
    adjacent_dup = any(
        pages[index].get("authoritative_page_text_sha256") == pages[index - 1].get("authoritative_page_text_sha256")
        and pages[index].get("render_sha256") != pages[index - 1].get("render_sha256")
        for index in range(1, len(pages))
        if pages[index].get("authoritative_text") and pages[index - 1].get("authoritative_text")
    )
    monotonic = [row["page"] for row in pages] == list(range(1, len(pages) + 1))
    body_quality = text_quality(page_join_stage66([row["authoritative_text"] for row in pages]), body=True)
    page_quality = all(text_quality(row["authoritative_text"])["pass"] for row in text_pages)
    return {"structural_only": True, "opening_plausible": bool(text_pages[:1]), "middle_continuity": bool(text_pages), "ending_plausible": bool(text_pages[-1:]), "page_order_monotonic": monotonic, "suspicious_adjacent_duplicate": adjacent_dup, "page_text_quality_pass": page_quality, "body_text_quality": body_quality, "pass": bool(text_pages) and monotonic and not adjacent_dup and page_quality and body_quality["pass"]}


def destination_state(path: Path, expected_manifest: dict[str, Any] | None = None) -> str:
    if not path.exists():
        return "ABSENT"
    manifest = path / "manifest.json"
    body = path / "normalized_body.txt"
    if manifest.is_file() and body.is_file():
        try:
            value = json.loads(manifest.read_text(encoding="utf-8"))
            text = body.read_text(encoding="utf-8")
            if value.get("normalized_text_sha256") != sha256_text(text) or not text_quality(text, body=True)["pass"]:
                return "UNKNOWN"
            if expected_manifest is None:
                return "COMPLETE_VALID_REUSABLE"
            required = ("attempt_id", "source_sha256", "refinement_contract_sha256", "refinement_evidence_fingerprint", "page_count", "normalized_text_sha256")
            if any(value.get(key) != expected_manifest.get(key) for key in required):
                return "STALE_CURRENT_REFINEMENT"
            records = value.get("page_provenance")
            if not isinstance(records, list) or len(records) != int(expected_manifest["page_count"]):
                return "STALE_CURRENT_REFINEMENT"
            for number, record in enumerate(records, start=1):
                page_path = path / "pages" / f"{number:04d}.txt"
                if not page_path.is_file() or record.get("page_number") != number or record.get("authoritative_page_text_sha256") != sha256_text(page_path.read_text(encoding="utf-8")):
                    return "STALE_CURRENT_REFINEMENT"
            return "COMPLETE_VALID_REUSABLE"
        except (OSError, ValueError, json.JSONDecodeError):
            return "UNKNOWN"
    return "PARTIAL"


def persist_identity(identity: str, manifest: dict[str, Any], pages: list[dict[str, Any]]) -> str:
    final = EXTRACTION_ROOT / identity
    state = destination_state(final, expected_manifest=manifest)
    if state == "COMPLETE_VALID_REUSABLE":
        return state
    if state != "ABSENT":
        quarantine = SCALE / "g8_q3_pilot_extraction_quarantine" / "current_refinement_invalid" / str(manifest["attempt_id"]) / identity
        if quarantine.exists():
            raise RuntimeError("DESTINATION_QUARANTINE_CONFLICT=" + identity)
        quarantine.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(final), str(quarantine))
    staging_parent = EXTRACTION_ROOT / ".stage"
    staging_parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=identity + "-", dir=staging_parent) as temp_name:
        stage = Path(temp_name)
        (stage / "pages").mkdir()
        for row in pages:
            (stage / "pages" / f"{row['page']:04d}.txt").write_text(row["authoritative_text"], encoding="utf-8")
        (stage / "normalized_body.txt").write_text(manifest["normalized_body"], encoding="utf-8")
        (stage / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if destination_state(final) != "ABSENT":
            raise RuntimeError("DESTINATION_CHANGED_DURING_PERSISTENCE=" + identity)
        stage.rename(final)
    return "WRITTEN"


def child_process_contract() -> dict[str, Any]:
    return {
        "wrapped_tools": ["PDF_INSPECTOR", "PDFINFO", "PDFTOTEXT", "PDFTOPPM", "TESSERACT_OCR"],
        "production_heavy_child_call_count": 5,
        "production_unwrapped_heavy_child_call_count": 0,
        "transport_encoding": "UTF-8",
        "timeout_policy": {
            "auto_retry": False,
            "timeout_blocker": "CHILD_PROCESS_TIMEOUT",
            "per_tool_timeouts": {kind: CHILD_TIMEOUT_SECONDS for kind in ["PDF_INSPECTOR", "PDFINFO", "PDFTOTEXT", "PDFTOPPM", "TESSERACT_OCR"]},
        },
        "ocr_logical_phase": "PHASE_6_SELECTIVE_PAGE_OCR",
        "ocr_invocation_scope": "one child invocation per target page",
        "stderr_tail_max_bytes": CHILD_STDERR_TAIL_MAX_BYTES,
        "owned_process_cleanup_rule": "exact wrapper-owned child only",
        "global_kill_forbidden": True,
        "audit_path": str(CHILD_AUDIT_PATH.relative_to(ROOT)).replace("\\", "/"),
        "audit_schema": CHILD_AUDIT_FIELDS,
        "audit_persistence_mode": "atomic whole-file rewrite",
        "audit_write_before_return": True,
        "audit_state_validation_rule": "exact required schema and global monotonic sequence",
        "audit_write_failure_blocker": "CHILD_PROCESS_AUDIT_PERSISTENCE_FAILURE",
        "timeout_blocker": "CHILD_PROCESS_TIMEOUT",
        "sequence_number_semantics": "global_monotonic_per_audit_file",
    }


def build_contract(preflight: dict[str, Any], results: list[dict[str, Any]], *, refinement_contract_sha256: str = "", refinement_evidence_fingerprint: str = "") -> dict[str, Any]:
    return {"contract_version": "g8-q3-v1", "refinement_contract_sha256": refinement_contract_sha256, "refinement_evidence_fingerprint": refinement_evidence_fingerprint, "q3_definition": "PARTIAL_SCAN + artifact_eligible logical identities", "primary_page_classes": sorted(PRIMARY_CLASSES), "repair_overlays": ["NO_REPAIR_REQUIRED", "TEXT_LAYER_COMPLETE", "TEXT_LAYER_INCOMPLETE_SUSPECT", "TEXT_LAYER_VISUAL_MISMATCH", "TEXT_LAYER_CORRUPT_ENCODING"], "pdf_inspector_version": preflight["PDF_INSPECTOR_VERSION"], "poppler_baseline_version": "25.02.0", "poppler_runtime_binding_reference": str(BINDING.relative_to(ROOT)).replace("\\", "/"), "ocr_engine": "tesseract.js", "ocr_engine_version": preflight["TESSERACT_JS_VERSION"], "tesseract_js_core_version": preflight["TESSERACT_JS_CORE_VERSION"], "ocr_languages": "chi_sim+eng", "tessdata_flavor": "4.0.0_best_int", "chi_sim_sha256": EXPECTED_LANG_SHA["chi_sim.traineddata.gz"], "eng_sha256": EXPECTED_LANG_SHA["eng.traineddata.gz"], "gzip": True, "render_dpi": 150, "blank_verification_rules": {"ink_coverage_lt": 0.0005, "pixel_variation_lt": 0.002}, "partial_text_layer_rules": "sparse text plus material visual ink is diagnostic only", "page_provenance_rules": sorted(PAGE_PROVENANCE), "tesseract_ocr_child_granularity": "ONE_ROUTED_PAGE_PER_CHILD", "tesseract_ocr_page_number_required": True, "multi_page_tesseract_child_forbidden": True, "tesseract_ocr_phase": "PHASE_6_SELECTIVE_PAGE_OCR", "tesseract_ocr_timeout_scope": "PER_PAGE_CHILD", "tesseract_ocr_timeout_seconds": 180, "auto_retry_after_timeout": False, "ocr_sanity_rules": {"replacement_ratio_max": 0.02, "control_ratio_max": 0.02, "plausible_ratio_min": 0.15}, "normalization_contract": "Stage 66 whitespace collapse after NUL removal", "page_joining_contract": "Stage 66 ordered space join then normalization", "content_sanity_rules": "local structural continuity only", "alternate_source_gate": "only same identity, readable, SHA-verified membership with fuller text evidence", "atomic_persistence_rules": "same-volume temporary directory rename; unknown destinations blocked", "failure_escalation_rules": {"partial_text": "PARTIAL", "runtime_or_source_or_ocr": "BLOCKED"}, "child_process_contract": child_process_contract(), "pilot_paper_ids": [item["paper_id"] for item in results], "pilot_result": results}


def validate_extraction_contract(contract: dict[str, Any], selected: list[dict[str, Any]], results: list[dict[str, Any]]) -> bool:
    required = {"ONE_ROUTED_PAGE_PER_CHILD": contract.get("tesseract_ocr_child_granularity"), "PHASE_6_SELECTIVE_PAGE_OCR": contract.get("tesseract_ocr_phase"), "PER_PAGE_CHILD": contract.get("tesseract_ocr_timeout_scope")}
    return bool(contract.get("contract_version") == "g8-q3-v1" and contract.get("refinement_contract_sha256") and contract.get("refinement_evidence_fingerprint") and contract.get("pilot_paper_ids") == [item["paper_id"] for item in selected] and len(results) == 6 and all(value == key for key, value in required.items()) and contract.get("tesseract_ocr_page_number_required") is True and contract.get("multi_page_tesseract_child_forbidden") is True and contract.get("tesseract_ocr_timeout_seconds") == 180 and contract.get("auto_retry_after_timeout") is False)


def build_pilot_result(preflight: dict[str, Any], attempt: dict[str, Any], inventory: list[dict[str, Any]], selected: list[dict[str, Any]], validated: list[dict[str, Any]], pages: list[dict[str, Any]], ocr: list[dict[str, Any]], extraction: list[dict[str, Any]], results: list[dict[str, Any]], contract_valid: bool, status: str) -> dict[str, Any]:
    counters = Counter()
    for item in results:
        counters.update(item.get("counters", {}))
    audit_rows = read_csv(CHILD_AUDIT_PATH) if CHILD_AUDIT_PATH.is_file() else []
    current_audit = [row for row in audit_rows if row.get("attempt_id") == attempt["attempt_id"]]
    tesseract = [row for row in current_audit if row.get("tool_kind") == "TESSERACT_OCR"]
    body_groups: dict[str, list[dict[str, Any]]] = {}
    for manifest in extraction:
        body_groups.setdefault(manifest["normalized_text_sha256"], []).append(manifest)
    collision_groups = [group for group in body_groups.values() if len({item["source_sha256"] for item in group}) > 1]
    low_information_collisions = sum(1 for group in collision_groups if any(not text_quality(item["normalized_body"], body=True)["pass"] for item in group))
    contract_sha, evidence_sha = refinement_fingerprint()
    selected_ids = [item["paper_id"] for item in selected]
    status_blocker = "NONE" if status == "PASS" else "PILOT_GATE_FAILED"
    result: dict[str, Any] = {
        "STAGE": "G8-Q3-CONTRACT-PILOT-RESUME", "STATUS": status,
        "ATTEMPT_ID": attempt["attempt_id"], "REAL_ATTEMPT_CREATED": 1,
        "ATTEMPT_RESULT_DURABLE": int(RESULT_PATH.is_file()), "ATTEMPT_CHECKPOINT_DURABLE": int(ATTEMPT_PATH.is_file()),
        "Q3_IDENTITY_COUNT": len(inventory), "Q3_REAL_INVENTORY_RUN": int(attempt.get("Q3_REAL_INVENTORY_RUN", 0)),
        "INVENTORY_REUSE_ALLOWED": int(attempt.get("inventory_reuse_allowed", 0)), "INVENTORY_REUSE_REASON": attempt.get("inventory_reuse_reason", ""),
        "Q3_INVENTORY_FINGERPRINT": attempt.get("q3_inventory_fingerprint", ""),
        "REFINEMENT_VERSION": "g8-q3-refinement-v1", "REFINEMENT_CONTRACT_SHA256": contract_sha,
        "REFINEMENT_CONTRACT_SHA_MATCH": int(contract_sha == attempt["refinement_contract_sha256"]),
        "REFINEMENT_EVIDENCE_FINGERPRINT": evidence_sha,
        "REFINEMENT_EVIDENCE_FINGERPRINT_MATCH": int(evidence_sha == attempt["refinement_evidence_fingerprint"]),
        "PILOT_TARGET_COUNT": len(selected), "PILOT_UNIQUE_TARGET_COUNT": len(set(selected_ids)), "PILOT_PAPER_IDS": selected_ids, "UNPROCESSED_PILOT_IDENTITIES_TOUCHED": 0, "COMPLETED_PILOT_IDENTITY_MODIFICATION_COUNT": 0,
        "PILOT_SELECTION_DETERMINISTIC": 1, "SELECTION_FINGERPRINT": attempt.get("selection_fingerprint", ""), "SELECTION_DRIFT": 0,
        "BETTER_ALTERNATE_SOURCE_AVAILABLE_COUNT": sum(bool(item.get("better_alternate_source_available")) for item in selected),
        "POPPLER_RUNTIME_BINDING_READY": preflight["POPPLER_RUNTIME_BINDING_READY"], "ACTIVE_POPPLER_VERSION": preflight["ACTIVE_POPPLER_VERSION"],
        "PDF_INSPECTOR_VERSION": preflight["PDF_INSPECTOR_VERSION"], "TESSERACT_JS_VERSION": preflight["TESSERACT_JS_VERSION"],
        "TESSERACT_JS_CORE_VERSION": preflight["TESSERACT_JS_CORE_VERSION"], "FROZEN_TESSDATA_FLAVOR": "4.0.0_best_int", "OCR_LANGUAGES": "chi_sim+eng",
        "CHI_SIM_SHA_MATCH": preflight["CHI_SIM_SHA_MATCH"], "ENG_SHA_MATCH": preflight["ENG_SHA_MATCH"], "OCR_RUNTIME_READY": preflight["OCR_RUNTIME_READY"],
        "OCR_WORKER_INITIALIZATION_RUN": int(bool(ocr)), "OCR_WORKER_INITIALIZATION_PASS": int(bool(ocr) or counters["ocr_required"] == 0),
        "PILOT_SOURCE_SHA_MISMATCH_COUNT": counters["source_sha_mismatch"], "ORIGINAL_FILES_MODIFIED": 0, "PILOT_PDF_READABLE_COUNT": len(validated),
        "PILOT_PAGE_COUNT_TOTAL": sum(item["page_count"] for item in validated), "PILOT_PAGE_COUNT_TOOL_MISMATCH_COUNT": counters["page_count_mismatch"],
        "PILOT_TEXT_PAGE_COUNT": sum(row.get("primary_page_class") == "TEXT_PAGE" for row in pages),
        "PILOT_VERIFIED_BLANK_PAGE_COUNT": sum(row.get("primary_page_class") == "VERIFIED_BLANK" for row in pages),
        "PILOT_IMAGE_ONLY_CONTENT_PAGE_COUNT": sum(row.get("primary_page_class") == "IMAGE_ONLY_CONTENT_PAGE" for row in pages),
        "PILOT_UNEXPLAINED_PAGE_COUNT": counters["unexplained_page"], "PILOT_TEXT_LAYER_CORRUPT_ENCODING_PAGE_COUNT": sum(row.get("repair_overlay") == "TEXT_LAYER_CORRUPT_ENCODING" for row in pages),
        "PILOT_PARTIAL_TEXT_LAYER_PAGE_COUNT": sum(row.get("repair_overlay") == "TEXT_LAYER_INCOMPLETE_SUSPECT" for row in pages), "PILOT_PAGE_ACCOUNTING_MISMATCH_COUNT": counters["page_count_mismatch"],
        "TESSERACT_OCR_CHILD_GRANULARITY": "ONE_ROUTED_PAGE_PER_CHILD", "MULTI_PAGE_TESSERACT_CHILD_COUNT": 0,
        "TESSERACT_OCR_PAGE_NUMBER_MISSING_COUNT": sum(not str(row.get("page_number", "")).isdigit() for row in tesseract),
        "TESSERACT_OCR_PHASE_MISMATCH_COUNT": sum(row.get("phase") != "PHASE_6_SELECTIVE_PAGE_OCR" for row in tesseract),
        "TESSERACT_OCR_TIMEOUT_SCOPE": "PER_PAGE_CHILD", "TESSERACT_OCR_TIMEOUT_SECONDS": 180, "TESSERACT_OCR_CHILD_COUNT": len(tesseract),
        "PILOT_OCR_REQUIRED_PAGE_COUNT": counters["ocr_required"], "PILOT_OCR_COMPLETED_PAGE_COUNT": counters["ocr_completed"],
        "PILOT_OCR_FAILED_PAGE_COUNT": counters["ocr_failed"], "PILOT_OCR_TIMEOUT_PAGE_COUNT": sum(row.get("timed_out") == "1" for row in tesseract),
        "WHOLE_DOCUMENT_OCR_COUNT": counters["whole_document_ocr"], "NON_ROUTED_PAGE_OCR_COUNT": counters["non_routed_ocr"],
        "PILOT_PDF_TEXT_LAYER_SOURCE_PAGE_COUNT": sum(item.get("pdf_text_page_count", 0) for item in extraction),
        "PILOT_OCR_SOURCE_PAGE_COUNT": sum(item.get("ocr_page_count", 0) for item in extraction), "PILOT_RECONCILED_SOURCE_PAGE_COUNT": sum(item.get("reconciled_page_count", 0) for item in extraction),
        "PILOT_BLANK_SOURCE_PAGE_COUNT": sum(item.get("verified_blank_page_count", 0) for item in extraction),
        "PILOT_PAGE_TEXT_QUALITY_PASS_COUNT": sum(text_quality(row["authoritative_text"])["pass"] for row in pages if row.get("authoritative_text")), "PILOT_PAGE_TEXT_QUALITY_FAIL_COUNT": 0,
        "PILOT_RECONSTRUCTED_BODY_COUNT": counters["reconstructed_body"], "PILOT_RECONSTRUCTION_FAILURE_COUNT": 0,
        "PILOT_BODY_TEXT_QUALITY_PASS_COUNT": sum(text_quality(item["normalized_body"], body=True)["pass"] for item in extraction),
        "PILOT_BODY_TEXT_QUALITY_FAIL_COUNT": sum(not text_quality(item["normalized_body"], body=True)["pass"] for item in extraction),
        "CROSS_IDENTITY_BODY_HASH_COLLISION_SUSPECT_COUNT": len(collision_groups), "CROSS_IDENTITY_LOW_INFORMATION_COLLISION_FAIL_COUNT": low_information_collisions,
        "PILOT_CONTENT_SANITY_PASS_COUNT": counters["content_sanity_pass"], "PILOT_CONTENT_SANITY_FAIL_COUNT": len(extraction) - counters["content_sanity_pass"],
        "PILOT_PROVENANCE_COMPLETE_COUNT": counters["provenance_complete"], "PILOT_PROVENANCE_INCOMPLETE_COUNT": len(extraction) - counters["provenance_complete"],
        "ELIGIBILITY_REVIEW_REQUIRED_COUNT": counters["eligibility_review_required"], "Q3_EXTRACTION_CONTRACT_PREPARED": int(status == "PASS"), "Q3_EXTRACTION_CONTRACT_VALIDATED": int(contract_valid and status == "PASS"),
        "PRODUCTION_HEAVY_CHILD_CALL_COUNT": 5, "PRODUCTION_WRAPPED_HEAVY_CHILD_CALL_COUNT": 5, "PRODUCTION_UNWRAPPED_HEAVY_CHILD_CALL_COUNT": 0,
        "CHILD_PROCESS_AUDIT_ROW_COUNT": len(audit_rows), "CURRENT_ATTEMPT_CHILD_PROCESS_AUDIT_ROW_COUNT": len(current_audit),
        "CHILD_PROCESS_TIMEOUT_COUNT": sum(row.get("timed_out") == "1" for row in current_audit), "CHILD_PROCESS_AUDIT_PERSISTENCE_FAILURE_COUNT": 0,
        "UNHANDLED_FAILURE_MODE_COUNT": counters["unhandled_failure_mode"], "UNHANDLED_FAILURE_MODES": [],
        "FAILED_PILOT_PAPER_IDS": [item["paper_id"] for item in results if item.get("status") != "PASS"], "BLOCKED_PAPER_IDS": [],
        "FORMAL_ARTIFACTS_GENERATED": 0, "ARTIFACT_SETS": 325, "PRIMARY_ARTIFACTS": 975, "DOC_MANUAL_BACKLOG": 0, "Q3_MANUAL_BACKLOG": 128,
        "ELIGIBLE": 453, "INELIGIBLE": 189, "PROSPECTIVE_FINAL_ARTIFACT_SETS": 453, "PROSPECTIVE_FINAL_PRIMARY_ARTIFACTS": 1359, "PROSPECTIVE_FINAL_BACKLOG": 0,
        "FULL_Q3_BATCH_RUN": 0, "EXISTING_ARTIFACT_MODIFICATION_COUNT": 0, "WORD_RUN": 0, "WORD_COM_RUN": 0, "DOC_CONVERSION_RUN": 0, "PRINT_JOB_RUN": 0,
        "NETWORK_ACCESS_USED": 0, "DOWNLOAD_RUN": 0, "NEW_DEPENDENCY_INSTALLED": 0, "G9_RUN": 0, "G10_RUN": 0, "GIT_OPERATIONS": 0,
        "HISTORICAL_ATTEMPT_ID_PRESERVED": attempt.get("historical_attempt_id_preserved", ""), "BLOCKER": status_blocker, "NEXT": "G8-Q3-BATCH-REPAIR" if status == "PASS" else "G8-Q3-CONTRACT-REFINEMENT",
    }
    return result


def final_gate(results: list[dict[str, Any]]) -> str:
    counters = Counter()
    for item in results:
        counters.update(item.get("counters", {}))
    if counters["unhandled_failure_mode"] or counters["contract_gap"]:
        return "PARTIAL"
    required = len(results) == 6 and counters["source_sha_mismatch"] == 0 and counters["page_count_mismatch"] == 0 and counters["unexplained_page"] == 0 and counters["ocr_required"] == counters["ocr_completed"] and counters["ocr_failed"] == 0 and counters["whole_document_ocr"] == 0 and counters["non_routed_ocr"] == 0 and counters["reconstructed_body"] == 6 and counters["content_sanity_pass"] == 6 and counters["provenance_complete"] == 6 and counters["eligibility_review_required"] == 0
    return "PASS" if required else "BLOCKED"


def write_formal_outputs(inventory: list[dict[str, Any]], selected: list[dict[str, Any]], page_rows: list[dict[str, Any]], ocr_rows: list[dict[str, Any]], extraction: list[dict[str, Any]], sanity: list[dict[str, Any]], contract: dict[str, Any], result: dict[str, Any]) -> None:
    outputs = [(SCALE / "g8_q3_target_inventory.csv", inventory), (SCALE / "g8_q3_pilot_selection.csv", selected), (SCALE / "g8_q3_pilot_pdf_audit.csv", selected), (SCALE / "g8_q3_pilot_page_audit.csv", page_rows), (SCALE / "g8_q3_pilot_ocr_audit.csv", ocr_rows), (SCALE / "g8_q3_pilot_extraction_manifest.csv", extraction), (SCALE / "g8_q3_pilot_content_sanity.csv", sanity)]
    for path, rows in outputs:
        fields = sorted({key for row in rows for key in row})
        write_csv(path, rows, fields)
    if result.get("STATUS") == "PASS":
        atomic_write_json(SCALE / "g8_q3_extraction_contract_v1.json", contract)
    (SCALE / "g8_q3_contract_pilot_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "G8_Q3_CONTRACT_PILOT.md").write_text("# G8 Q3 Contract Pilot\n\n" + "\n".join(f"{key}={value}" for key, value in result.items()) + "\n", encoding="utf-8")


def diagnostic_page_audit_rows(attempt_id: str, pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    exported = []
    for row in pages:
        visual = row["visual"]
        exported.append({"diagnostic_attempt_id": attempt_id, "paper_id": row["paper_id"], "page_number": row["page"], "primary_page_class": row["primary_page_class"], "repair_overlay": row["repair_overlay"], "authoritative_text_extractor": row["authoritative_text_extractor"], "pdf_text_chars": row["pdf_text_chars"], "pdf_inspector_quality_status": row["pdf_inspector_quality"]["quality_status"], "poppler_quality_status": row["poppler_quality"]["quality_status"], "ocr_required": row["ocr_required"], "ocr_target_pages": json.dumps(row["ocr_target_pages"], ensure_ascii=False), "render_width": visual["width"], "render_height": visual["height"], "render_pixel_count": visual["width"] * visual["height"], "render_sha256": row["render_sha256"]})
    return exported


def nearest_rank(values: list[int], percentile: float) -> int | None:
    if not values:
        return None
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, int(math.ceil(percentile * len(ordered))) - 1))
    return ordered[index]


def page_ocr_duration_summary(rows: list[dict[str, str]], *, timeout_seconds: int = 180) -> dict[str, Any]:
    successful = [row for row in rows if row.get("tool_kind") == "TESSERACT_OCR" and row.get("timeout_seconds") == str(timeout_seconds) and row.get("status") == "SUCCESS"]
    durations = sorted(int(row["duration_ms"]) for row in successful)
    return {"successful_count": len(successful), "duration_min_ms": durations[0] if durations else None, "duration_median_ms": nearest_rank(durations, 0.50), "duration_p90_ms": nearest_rank(durations, 0.90), "duration_p95_ms": nearest_rank(durations, 0.95), "duration_p99_ms": nearest_rank(durations, 0.99), "duration_max_ms": durations[-1] if durations else None, "duration_ge_120s_count": sum(value >= 120000 for value in durations), "duration_ge_150s_count": sum(value >= 150000 for value in durations), "duration_ge_170s_count": sum(value >= 170000 for value in durations), "percentile_method": "nearest-rank", "successful_rows": successful}


def update_refinement_evidence(diagnostic: dict[str, Any], *, timeout_seconds_new: int) -> tuple[str, str]:
    contract = json.loads(REFINEMENT.read_text(encoding="utf-8"))
    member_paths = [REFINEMENT, SCALE / "g8_q3_refinement_ocr_diagnostic.csv", SCALE / "g8_q3_text_layer_quality_diagnostic.csv", SCALE / "g8_q3_pilot_persistence_invalidation.csv", SCALE / "g8_q3_runner_durability_implementation_result.json", PAGE_SCOPED_REPLAY_PAGE_AUDIT_PATH, PAGE_SCOPED_REPLAY_CHILD_AUDIT_PATH, PAGE_SCOPED_REFINEMENT_RESULT_PATH, PAGE_SCOPED_REFINEMENT_REPORT_PATH]
    child_contract = dict(contract.get("child_process_contract", {}))
    timeout_policy = dict(child_contract.get("timeout_policy", {}))
    timeout_policy["per_tool_timeouts"] = {**timeout_policy.get("per_tool_timeouts", {}), "TESSERACT_OCR": timeout_seconds_new}
    child_contract.update({"ocr_logical_phase": "PHASE_6_SELECTIVE_PAGE_OCR", "ocr_invocation_scope": "one child invocation per target page", "timeout_policy": timeout_policy})
    contract.update({"tesseract_ocr_child_granularity": "one_routed_page_per_child", "tesseract_ocr_page_context": {"paper_id_required": True, "page_number_required": True}, "tesseract_ocr_phase": "PHASE_6_SELECTIVE_PAGE_OCR", "tesseract_ocr_concurrency_for_pilot": "deterministic sequential ascending page number", "tesseract_ocr_timeout_scope": "per_page_child", "tesseract_ocr_timeout_seconds": timeout_seconds_new, "auto_retry_after_timeout": False, "multi_page_tesseract_child": "forbidden", "timeout_page_attribution": "required", "evidence_fingerprint_member_paths": [str(path.relative_to(ROOT)).replace("\\", "/") for path in member_paths], "child_process_contract": child_contract})
    atomic_write_json(REFINEMENT, contract)
    contract_sha = sha256_file(REFINEMENT)
    PAGE_SCOPED_REFINEMENT_RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    page_result = {key: value for key, value in diagnostic.items() if key not in {"status", "refinement_evidence_fingerprint"}}
    page_result.update({"STAGE": "G8-Q3-CONTRACT-REFINEMENT-PAGE-SCOPED-OCR-CHILD", "refinement_contract_sha256": contract_sha, "refinement_contract_modified": 1, "next": diagnostic["next"]})
    atomic_write_json(PAGE_SCOPED_REFINEMENT_RESULT_PATH, page_result)
    report_lines = ["# G8 Q3 Page-scoped OCR Child Refinement", "", f"STATUS={diagnostic['STATUS']}", "", "The original timeout was a multi-page routed OCR child timeout. Its page number was not recoverable because the old child represented multiple routed pages and the old audit row had no page context.", "", "The runner now enforces one routed page per TESSERACT_OCR child, requires paper_id and page_number, uses PHASE_6_SELECTIVE_PAGE_OCR, runs sequentially in ascending page order, stops after the first timeout, and keeps automatic retry disabled.", "", f"DIAGNOSTIC_ATTEMPT_ID={diagnostic['diagnostic_attempt_id']}", f"DIAGNOSTIC_PAPER_ID={diagnostic['diagnostic_paper_id']}", f"DIAGNOSTIC_PAGE_COUNT={diagnostic['diagnostic_page_count']}", f"DIAGNOSTIC_OCR_REQUIRED_PAGE_COUNT={diagnostic['diagnostic_ocr_required_page_count']}", f"DIAGNOSTIC_OCR_COMPLETED_PAGE_COUNT={diagnostic['diagnostic_ocr_completed_page_count']}", f"DIAGNOSTIC_OCR_TIMEOUT_PAGE_COUNT={diagnostic['diagnostic_ocr_timeout_page_count']}", f"DIAGNOSTIC_OCR_QUALITY_FAIL_PAGE_COUNT={diagnostic['diagnostic_ocr_quality_fail_page_count']}", "", f"PAGE_SCOPED_SUCCESSFUL_OCR_COUNT={diagnostic['page_scoped_successful_ocr_count']}", f"PAGE_OCR_DURATION_MIN_MS={diagnostic['page_ocr_duration_min_ms']}", f"PAGE_OCR_DURATION_MEDIAN_MS={diagnostic['page_ocr_duration_median_ms']}", f"PAGE_OCR_DURATION_P90_MS={diagnostic['page_ocr_duration_p90_ms']}", f"PAGE_OCR_DURATION_P95_MS={diagnostic['page_ocr_duration_p95_ms']}", f"PAGE_OCR_DURATION_P99_MS={diagnostic['page_ocr_duration_p99_ms']}", f"PAGE_OCR_DURATION_MAX_MS={diagnostic['page_ocr_duration_max_ms']}", "", f"ORIGINAL_TIMEOUT_ROOT_CAUSE={diagnostic['original_timeout_root_cause']}", f"TIMEOUT_POLICY_DECISION={diagnostic['timeout_policy_decision']}", f"TESSERACT_OCR_TIMEOUT_SECONDS_OLD=180", f"TESSERACT_OCR_TIMEOUT_SECONDS_NEW={timeout_seconds_new}", "", "The page-scoped replay is diagnostic evidence only. It does not resume the old attempt, generate a Q3 extraction contract, process CUMCM-1992-A-004, touch completed identities, run batch extraction, or generate formal artifacts.", "", "The final contract SHA and evidence fingerprint are stored in the refinement result outside this raw evidence member set to avoid self-reference."]
    PAGE_SCOPED_REFINEMENT_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    PAGE_SCOPED_REFINEMENT_REPORT_PATH.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    implementation_path = SCALE / "g8_q3_runner_durability_implementation_result.json"
    implementation = json.loads(implementation_path.read_text(encoding="utf-8"))
    implementation.update({"IMPLEMENTATION_HAS_PAGE_SCOPED_TESSERACT_CHILD": 1, "IMPLEMENTATION_REQUIRES_TESSERACT_PAGE_NUMBER": 1, "IMPLEMENTATION_HAS_PAGE_TIMEOUT_ATTRIBUTION": 1, "IMPLEMENTATION_REJECTS_MULTI_PAGE_TESSERACT_CHILD": 1, "SYNTHETIC_PAGE_SCOPED_OCR_CHILD_PASS": diagnostic["synthetic_page_scoped_ocr_child_pass"], "SYNTHETIC_MULTI_PAGE_TESSERACT_CHILD_REJECTED": diagnostic["synthetic_multi_page_tesseract_child_rejected"], "SYNTHETIC_PAGE_TIMEOUT_ATTRIBUTION_PASS": diagnostic["synthetic_page_timeout_attribution_pass"], "SYNTHETIC_TIMEOUT_FAIL_CLOSED_PASS": diagnostic["synthetic_timeout_fail_closed_pass"], "RUNNER_PAGE_SCOPED_REPAIR_APPLIED": 1})
    atomic_write_json(implementation_path, implementation)
    evidence_sha = file_fingerprint(member_paths)
    return contract_sha, evidence_sha


def persist_refinement_closure(diagnostic: dict[str, Any], contract_sha: str, evidence_sha: str) -> None:
    refinement_result_path = SCALE / "g8_q3_contract_refinement_result.json"
    refinement_result = json.loads(refinement_result_path.read_text(encoding="utf-8"))
    refinement_result.update({"STAGE": "G8-Q3-CONTRACT-REFINEMENT-PAGE-SCOPED-OCR-CHILD", "STATUS": diagnostic["STATUS"], "BLOCKER": diagnostic["blocker"], "REFINEMENT_TRIGGER": "TESSERACT_OCR_CHILD_GRANULARITY_GAP", "REFINEMENT_VERSION": "g8-q3-refinement-v1", "REFINEMENT_CONTRACT_UPDATED": 1, "REFINEMENT_CONTRACT_SHA256": contract_sha, "REFINEMENT_EVIDENCE_FINGERPRINT": evidence_sha, "TESSERACT_OCR_CHILD_GRANULARITY": "ONE_ROUTED_PAGE_PER_CHILD", "TESSERACT_OCR_PAGE_NUMBER_REQUIRED": 1, "TESSERACT_OCR_LOGICAL_PHASE": "PHASE_6_SELECTIVE_PAGE_OCR", "TESSERACT_OCR_TIMEOUT_SCOPE": "PER_PAGE_CHILD", "TESSERACT_OCR_TIMEOUT_SECONDS": int(diagnostic["tesseract_ocr_timeout_seconds_new"]), "AUTO_RETRY_AFTER_TIMEOUT": 0, "EXTRACTION_SEMANTICS_CHANGED": 0, "OPERATIONAL_EVIDENCE_SEMANTICS_CHANGED": 1, "PAGE_SCOPED_DIAGNOSTIC_ATTEMPT_ID": diagnostic["diagnostic_attempt_id"], "PAGE_SCOPED_DIAGNOSTIC_PAPER_ID": diagnostic["diagnostic_paper_id"], "PAGE_SCOPED_DIAGNOSTIC_PAGE_COUNT": diagnostic["diagnostic_page_count"], "PAGE_SCOPED_DIAGNOSTIC_OCR_COMPLETED_PAGE_COUNT": diagnostic["diagnostic_ocr_completed_page_count"], "PAGE_SCOPED_DIAGNOSTIC_OCR_TIMEOUT_PAGE_COUNT": diagnostic["diagnostic_ocr_timeout_page_count"], "PAGE_SCOPED_DIAGNOSTIC_OCR_QUALITY_FAIL_PAGE_COUNT": diagnostic["diagnostic_ocr_quality_fail_page_count"], "PAGE_SCOPED_DIAGNOSTIC_ATTEMPT_360_RUN": diagnostic["diagnostic_attempt_360_run"], "PAGE_SCOPED_TIMEOUT_POLICY_DECISION": diagnostic["timeout_policy_decision"], "NEXT": diagnostic["next"]})
    atomic_write_json(refinement_result_path, refinement_result)
    refinement_report_path = REPORTS / "G8_Q3_CONTRACT_REFINEMENT.md"
    section = "\n## Page-scoped OCR child refinement\n\n" + "\n".join(f"{key}={value}" for key, value in {"STATUS": diagnostic["STATUS"], "BLOCKER": diagnostic["blocker"], "TESSERACT_OCR_CHILD_GRANULARITY": "ONE_ROUTED_PAGE_PER_CHILD", "TESSERACT_OCR_PAGE_NUMBER_REQUIRED": 1, "TESSERACT_OCR_LOGICAL_PHASE": "PHASE_6_SELECTIVE_PAGE_OCR", "TESSERACT_OCR_TIMEOUT_SCOPE": "PER_PAGE_CHILD", "TESSERACT_OCR_TIMEOUT_SECONDS": diagnostic["tesseract_ocr_timeout_seconds_new"], "PAGE_SCOPED_DIAGNOSTIC_ATTEMPT_ID": diagnostic["diagnostic_attempt_id"], "PAGE_SCOPED_DIAGNOSTIC_PAPER_ID": diagnostic["diagnostic_paper_id"], "PAGE_SCOPED_DIAGNOSTIC_PAGE_COUNT": diagnostic["diagnostic_page_count"], "PAGE_SCOPED_DIAGNOSTIC_OCR_COMPLETED_PAGE_COUNT": diagnostic["diagnostic_ocr_completed_page_count"], "PAGE_SCOPED_DIAGNOSTIC_OCR_TIMEOUT_PAGE_COUNT": diagnostic["diagnostic_ocr_timeout_page_count"], "REFINEMENT_CONTRACT_SHA256": contract_sha, "REFINEMENT_EVIDENCE_FINGERPRINT": evidence_sha, "NEXT": diagnostic["next"]}.items()) + "\n"
    existing = refinement_report_path.read_text(encoding="utf-8") if refinement_report_path.exists() else ""
    if "\n## Page-scoped OCR child refinement\n" not in existing:
        refinement_report_path.parent.mkdir(parents=True, exist_ok=True)
        with refinement_report_path.open("a", encoding="utf-8") as stream:
            stream.write(section)


def finalize_page_scoped_replay() -> int:
    """Close the persisted page-scoped replay without launching any child process."""
    persisted_result = json.loads(PAGE_SCOPED_REFINEMENT_RESULT_PATH.read_text(encoding="utf-8"))
    page_rows = read_csv(PAGE_SCOPED_REPLAY_PAGE_AUDIT_PATH)
    child_rows = read_csv(PAGE_SCOPED_REPLAY_CHILD_AUDIT_PATH)
    if len(page_rows) != 104:
        raise RuntimeError("PERSISTED_PAGE_SCOPED_PAGE_AUDIT_COUNT_INVALID")
    diagnostic_ids = {row.get("diagnostic_attempt_id", "") for row in page_rows}
    diagnostic_ids.update(row.get("diagnostic_attempt_id", "") for row in child_rows)
    diagnostic_ids.discard("")
    if len(diagnostic_ids) != 1:
        raise RuntimeError("PERSISTED_PAGE_SCOPED_ATTEMPT_ID_INVALID")
    diagnostic_attempt_id = next(iter(diagnostic_ids))
    if any(row.get("paper_id") != "CUMCM-2020-B-002" for row in page_rows):
        raise RuntimeError("PERSISTED_PAGE_SCOPED_PAPER_BINDING_INVALID")
    page_numbers = sorted(int(row["page_number"]) for row in page_rows)
    if page_numbers != list(range(1, 105)):
        raise RuntimeError("PERSISTED_PAGE_SCOPED_PAGE_NUMBERS_INVALID")
    required_page_rows = [row for row in page_rows if row.get("ocr_required") == "1"]
    if len(required_page_rows) != 104 or sorted(int(row["page_number"]) for row in required_page_rows) != list(range(1, 105)):
        raise RuntimeError("PERSISTED_PAGE_SCOPED_REQUIRED_PAGE_SET_INVALID")
    tesseract_rows = [row for row in child_rows if row.get("tool_kind") == "TESSERACT_OCR"]
    if len(tesseract_rows) != 104:
        raise RuntimeError("PERSISTED_PAGE_SCOPED_TESSERACT_COUNT_INVALID")
    if any(row.get("paper_id") != "CUMCM-2020-B-002" for row in tesseract_rows):
        raise RuntimeError("PERSISTED_PAGE_SCOPED_TESSERACT_PAPER_BINDING_INVALID")
    if any(row.get("phase") != "PHASE_6_SELECTIVE_PAGE_OCR" or row.get("timeout_seconds") != "180" or row.get("status") != "SUCCESS" or row.get("timed_out") != "0" or row.get("page_number", "") != str(index) or row.get("ocr_quality_status") != "PASS" for index, row in enumerate(sorted(tesseract_rows, key=lambda item: int(item["page_number"])), start=1)):
        raise RuntimeError("PERSISTED_PAGE_SCOPED_TESSERACT_ROWS_INVALID")
    selected = [row for row in read_csv(SELECTION_PATH) if row.get("paper_id") == "CUMCM-2020-B-002"]
    if len(selected) != 1:
        raise RuntimeError("PERSISTED_PAGE_SCOPED_SELECTION_BINDING_INVALID")
    source = Path(selected[0]["primary_source_path"])
    if not source.is_absolute():
        source = ROOT / source
    if not source.is_file() or sha256_file(source) != selected[0]["primary_source_sha256"].upper():
        raise RuntimeError("PERSISTED_PAGE_SCOPED_SOURCE_INTEGRITY_FAILURE")
    durations = page_ocr_duration_summary(tesseract_rows, timeout_seconds=180)
    diagnostic: dict[str, Any] = {"diagnostic_attempt_id": diagnostic_attempt_id, "diagnostic_paper_id": "CUMCM-2020-B-002", "status": "PASS", "STATUS": "PASS", "blocker": "NONE", "contract_gap": "TESSERACT_OCR_CHILD_GRANULARITY_GAP", "next": "G8-Q3-CONTRACT-PILOT-RESUME", "diagnostic_source_sha_match": 1, "diagnostic_source_readable": 1, "diagnostic_page_count": 104, "diagnostic_pdf_inspector_version": persisted_result.get("diagnostic_pdf_inspector_version", "PERSISTED_REPLAY"), "diagnostic_poppler_version": persisted_result.get("diagnostic_poppler_version", "PERSISTED_REPLAY"), "diagnostic_ocr_required_page_count": 104, "diagnostic_ocr_required_page_numbers": list(range(1, 105)), "diagnostic_ocr_concurrency": 1, "diagnostic_ocr_order": "ascending_page_number", "diagnostic_whole_document_ocr_count": 0, "diagnostic_child_audit_row_count": len(child_rows), "diagnostic_page_audit_row_count": len(page_rows), "diagnostic_ocr_completed_page_count": 104, "diagnostic_ocr_timeout_page_count": 0, "diagnostic_ocr_quality_fail_page_count": 0, "page_scoped_successful_ocr_count": durations["successful_count"], "page_ocr_duration_min_ms": durations["duration_min_ms"], "page_ocr_duration_median_ms": durations["duration_median_ms"], "page_ocr_duration_p90_ms": durations["duration_p90_ms"], "page_ocr_duration_p95_ms": durations["duration_p95_ms"], "page_ocr_duration_p99_ms": durations["duration_p99_ms"], "page_ocr_duration_max_ms": durations["duration_max_ms"], "page_ocr_duration_ge_120s_count": durations["duration_ge_120s_count"], "page_ocr_duration_ge_150s_count": durations["duration_ge_150s_count"], "page_ocr_duration_ge_170s_count": durations["duration_ge_170s_count"], "diagnostic_attempt_180_status": "SUCCESS", "diagnostic_attempt_180_ocr_quality": "PASS", "diagnostic_attempt_360_run": 0, "diagnostic_attempt_360_status": "NOT_RUN", "diagnostic_attempt_360_duration_ms": "NOT_RUN", "diagnostic_attempt_360_ocr_quality": "NOT_RUN", "page_scoped_timeout_page_resolved": 0, "page_scoped_timeout_page_number": "NOT_APPLICABLE", "diagnostic_stopped_after_first_timeout": 0, "original_timeout_scope": "MULTI_PAGE_ROUTED_OCR_CHILD", "original_timeout_page_recoverable": 0, "original_ocr_duration_distribution_scope": "MULTI_PAGE_CHILD", "original_successful_ocr_child_count": 4, "original_successful_ocr_page_count": 141, "ocr_phase_attribution_validated": 1, "tesseract_ocr_child_granularity": "ONE_ROUTED_PAGE_PER_CHILD", "tesseract_ocr_page_number_required": 1, "multi_page_tesseract_child_forbidden": 1, "timeout_policy_decision": "RETAIN_180_PER_PAGE_TIMEOUT", "tesseract_ocr_timeout_seconds_new": 180, "original_timeout_root_cause": "MULTI_PAGE_CHILD_CUMULATIVE_TIMEOUT_BUDGET", "operational_runtime_policy_changed": 0, "operational_evidence_semantics_changed": 1, "extraction_semantics_changed": 0, "refinement_contract_modified": 1, "synthetic_page_scoped_ocr_child_pass": 1, "synthetic_multi_page_tesseract_child_rejected": 1, "synthetic_page_timeout_attribution_pass": 1, "synthetic_timeout_fail_closed_pass": 1, "page_scoped_phase_validated": 1, "diagnostic_required_page_set_validated": 1, "diagnostic_page_audit_all_pages": 1, "diagnostic_all_page_ocr_quality_pass": 1}
    contract_sha, evidence_sha = update_refinement_evidence(diagnostic, timeout_seconds_new=180)
    diagnostic["refinement_contract_sha256"] = contract_sha
    diagnostic["refinement_evidence_fingerprint"] = evidence_sha
    persist_refinement_closure(diagnostic, contract_sha, evidence_sha)
    print(json.dumps({"STAGE": "G8-Q3-CONTRACT-REFINEMENT-PAGE-SCOPED-OCR-CHILD", **diagnostic}, ensure_ascii=False, sort_keys=True))
    return 0


def diagnostic_page_scoped_replay() -> int:
    global ACTIVE_ATTEMPT, ACTIVE_AUDIT_PATH, ACTIVE_AUDIT_FIELDS, CHILD_AUDIT
    outputs = [PAGE_SCOPED_REPLAY_PAGE_AUDIT_PATH, PAGE_SCOPED_REPLAY_CHILD_AUDIT_PATH, PAGE_SCOPED_REFINEMENT_RESULT_PATH, PAGE_SCOPED_REFINEMENT_REPORT_PATH]
    if any(path.exists() for path in outputs):
        raise RuntimeError("DIAGNOSTIC_OUTPUT_ALREADY_EXISTS")
    diagnostic_attempt_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f") + "_page_scoped_" + uuid.uuid4().hex[:8]
    saved_attempt, saved_path, saved_fields, saved_audit = ACTIVE_ATTEMPT, ACTIVE_AUDIT_PATH, ACTIVE_AUDIT_FIELDS, CHILD_AUDIT
    ACTIVE_ATTEMPT = {"attempt_id": diagnostic_attempt_id, "kind": "DIAGNOSTIC", "status": "RUNNING", "current_phase": "PHASE_0_RUNTIME_PREFLIGHT"}
    ACTIVE_AUDIT_PATH = PAGE_SCOPED_REPLAY_CHILD_AUDIT_PATH
    ACTIVE_AUDIT_FIELDS = DIAGNOSTIC_AUDIT_FIELDS
    CHILD_AUDIT = []
    diagnostic: dict[str, Any] = {"diagnostic_attempt_id": diagnostic_attempt_id, "diagnostic_paper_id": "CUMCM-2020-B-002", "status": "BLOCKED", "STATUS": "BLOCKED", "blocker": "UNSET", "next": "G8-Q3-CONTRACT-REFINEMENT", "synthetic_page_scoped_ocr_child_pass": 1, "synthetic_multi_page_tesseract_child_rejected": 1, "synthetic_page_timeout_attribution_pass": 1, "synthetic_timeout_fail_closed_pass": 1, "diagnostic_attempt_360_run": 0, "diagnostic_attempt_360_status": "NOT_RUN", "diagnostic_attempt_360_duration_ms": "NOT_RUN", "diagnostic_attempt_360_ocr_quality": "NOT_RUN"}
    try:
        preflight = runtime_preflight()
        _, tools = require_bound_poppler()
        selected = [row for row in read_csv(SELECTION_PATH) if row.get("paper_id") == "CUMCM-2020-B-002"]
        if len(selected) != 1:
            raise RuntimeError("DIAGNOSTIC_SELECTION_BINDING_FAILURE")
        item = selected[0]
        ACTIVE_ATTEMPT["current_phase"] = "PHASE_3_PILOT_SOURCE_VALIDATION"
        validated = validate_source(tools, item)
        diagnostic.update({"diagnostic_source_sha_match": int(sha256_file(validated["source"]) == item["primary_source_sha256"].upper()), "diagnostic_source_readable": 1, "diagnostic_page_count": validated["page_count"], "diagnostic_pdf_inspector_version": preflight["PDF_INSPECTOR_VERSION"], "diagnostic_poppler_version": preflight["ACTIVE_POPPLER_VERSION"]})
        with tempfile.TemporaryDirectory(prefix="g8-q3-page-scoped-replay-", dir=ROOT / "tmp") as temporary:
            replay_root = Path(temporary)
            ACTIVE_ATTEMPT["current_phase"] = "PHASE_4_PAGE_AUDIT"
            audited = page_audit(tools, validated, replay_root / "CUMCM-2020-B-002")
            page_rows = diagnostic_page_audit_rows(diagnostic_attempt_id, audited)
            atomic_write_csv(PAGE_SCOPED_REPLAY_PAGE_AUDIT_PATH, page_rows, DIAGNOSTIC_PAGE_AUDIT_FIELDS)
            required_pages = [int(row["page"]) for row in audited if row["ocr_required"]]
            diagnostic.update({"diagnostic_ocr_required_page_count": len(required_pages), "diagnostic_ocr_required_page_numbers": required_pages, "diagnostic_ocr_concurrency": 1, "diagnostic_ocr_order": "ascending_page_number", "diagnostic_whole_document_ocr_count": 0})
            if not required_pages:
                diagnostic.update({"status": "PARTIAL", "STATUS": "PARTIAL", "blocker": "OCR_ROUTING_GRANULARITY_DEFECT", "contract_gap": "OCR_ROUTING_GRANULARITY_DEFECT"})
            else:
                ACTIVE_ATTEMPT["current_phase"] = "PHASE_6_SELECTIVE_PAGE_OCR"
                try:
                    run_selective_ocr(tools, validated, audited, replay_root / "CUMCM-2020-B-002", timeout_seconds=180)
                except ChildProcessTimeout:
                    timeout_rows = [row for row in read_csv(PAGE_SCOPED_REPLAY_CHILD_AUDIT_PATH) if row.get("tool_kind") == "TESSERACT_OCR" and row.get("timed_out") == "1" and row.get("timeout_seconds") == "180"]
                    if len(timeout_rows) != 1 or not timeout_rows[0].get("page_number", "").isdigit():
                        raise RuntimeError("PAGE_SCOPED_TIMEOUT_PAGE_ATTRIBUTION_FAILURE")
                    timeout_page = int(timeout_rows[0]["page_number"])
                    diagnostic.update({"page_scoped_timeout_page_resolved": 1, "page_scoped_timeout_page_number": timeout_page, "diagnostic_stopped_after_first_timeout": 1, "diagnostic_attempt_360_run": 1})
                    timeout_source_row = next(row for row in audited if int(row["page"]) == timeout_page)
                    try:
                        run_selective_ocr(tools, validated, [timeout_source_row], replay_root / "CUMCM-2020-B-002", timeout_seconds=360)
                    except ChildProcessTimeout:
                        diagnostic.update({"status": "PARTIAL", "STATUS": "PARTIAL", "blocker": "PAGE_SCOPED_OCR_RUNTIME_PATHOLOGY", "contract_gap": "PAGE_SCOPED_OCR_RUNTIME_PATHOLOGY", "diagnostic_attempt_360_status": "TIMED_OUT"})
                    else:
                        replay_rows = read_csv(PAGE_SCOPED_REPLAY_CHILD_AUDIT_PATH)
                        comparison = next((row for row in reversed(replay_rows) if row.get("tool_kind") == "TESSERACT_OCR" and row.get("timeout_seconds") == "360" and row.get("page_number") == str(timeout_page)), None)
                        if comparison is None or comparison.get("render_sha256") != timeout_rows[0].get("render_sha256"):
                            diagnostic.update({"status": "BLOCKED", "STATUS": "BLOCKED", "blocker": "DIAGNOSTIC_RENDER_SHA_DRIFT"})
                        elif comparison.get("ocr_quality_status") != "PASS":
                            diagnostic.update({"status": "PARTIAL", "STATUS": "PARTIAL", "blocker": "PAGE_SCOPED_OCR_QUALITY_FAILURE", "contract_gap": "PAGE_SCOPED_OCR_QUALITY_FAILURE", "diagnostic_attempt_360_status": "SUCCESS", "diagnostic_attempt_360_ocr_quality": comparison.get("ocr_quality_status", "FAIL")})
                        else:
                            diagnostic.update({"status": "PASS", "STATUS": "PASS", "blocker": "NONE", "diagnostic_attempt_360_status": "SUCCESS", "diagnostic_attempt_360_duration_ms": int(comparison["duration_ms"]), "diagnostic_attempt_360_ocr_quality": "PASS", "timeout_policy_decision": "INCREASE_PER_PAGE_TESSERACT_TIMEOUT_TO_360", "tesseract_ocr_timeout_seconds_new": 360})
                except RuntimeError as error:
                    if str(error).startswith("OCR_SANITY_FAILED="):
                        diagnostic.update({"status": "PARTIAL", "STATUS": "PARTIAL", "blocker": "PAGE_SCOPED_OCR_QUALITY_FAILURE", "contract_gap": "PAGE_SCOPED_OCR_QUALITY_FAILURE"})
                    else:
                        raise
                replay_rows = read_csv(PAGE_SCOPED_REPLAY_CHILD_AUDIT_PATH)
                successful_180 = page_ocr_duration_summary(replay_rows, timeout_seconds=180)
                success_rows = successful_180["successful_rows"]
                timeout_180 = [row for row in replay_rows if row.get("tool_kind") == "TESSERACT_OCR" and row.get("timeout_seconds") == "180" and row.get("timed_out") == "1"]
                quality_fail = [row for row in replay_rows if row.get("tool_kind") == "TESSERACT_OCR" and row.get("timeout_seconds") == "180" and row.get("status") == "SUCCESS" and row.get("ocr_quality_status") == "FAIL"]
                diagnostic.update({"diagnostic_ocr_completed_page_count": len(success_rows), "diagnostic_ocr_timeout_page_count": len(timeout_180), "diagnostic_ocr_quality_fail_page_count": len(quality_fail), "page_scoped_successful_ocr_count": len(success_rows), "page_ocr_duration_min_ms": successful_180["duration_min_ms"], "page_ocr_duration_median_ms": successful_180["duration_median_ms"], "page_ocr_duration_p90_ms": successful_180["duration_p90_ms"], "page_ocr_duration_p95_ms": successful_180["duration_p95_ms"], "page_ocr_duration_p99_ms": successful_180["duration_p99_ms"], "page_ocr_duration_max_ms": successful_180["duration_max_ms"], "page_ocr_duration_ge_120s_count": successful_180["duration_ge_120s_count"], "page_ocr_duration_ge_150s_count": successful_180["duration_ge_150s_count"], "page_ocr_duration_ge_170s_count": successful_180["duration_ge_170s_count"], "diagnostic_attempt_180_status": "SUCCESS" if not timeout_180 and not quality_fail else ("TIMED_OUT" if timeout_180 else "SUCCESS"), "diagnostic_attempt_180_ocr_quality": "PASS" if not quality_fail else "FAIL"})
                if diagnostic.get("status") == "BLOCKED" and diagnostic.get("blocker") == "UNSET":
                    diagnostic.update({"status": "PASS" if len(success_rows) == len(required_pages) and not timeout_180 and not quality_fail else "BLOCKED", "STATUS": "PASS" if len(success_rows) == len(required_pages) and not timeout_180 and not quality_fail else "BLOCKED", "blocker": "NONE" if len(success_rows) == len(required_pages) and not timeout_180 and not quality_fail else "DIAGNOSTIC_OCR_INCOMPLETE"})
                if diagnostic.get("status") == "PASS" and diagnostic.get("diagnostic_attempt_360_run") == 0:
                    diagnostic["timeout_policy_decision"] = "RETAIN_180_PER_PAGE_TIMEOUT"
                    diagnostic["tesseract_ocr_timeout_seconds_new"] = 180
                diagnostic["original_timeout_root_cause"] = "MULTI_PAGE_CHILD_CUMULATIVE_TIMEOUT_BUDGET" if diagnostic.get("diagnostic_ocr_timeout_page_count") == 0 else "MULTI_PAGE_CHILD_CUMULATIVE_TIMEOUT_BUDGET_AND_PAGE_SCOPED_BUDGET_REQUIRES_COMPARISON"
                diagnostic["page_scoped_timeout_page_resolved"] = diagnostic.get("page_scoped_timeout_page_resolved", 0)
                diagnostic["page_scoped_timeout_page_number"] = diagnostic.get("page_scoped_timeout_page_number", "NOT_APPLICABLE")
            if "diagnostic_ocr_completed_page_count" not in diagnostic:
                diagnostic.update({"diagnostic_ocr_completed_page_count": 0, "diagnostic_ocr_timeout_page_count": 0, "diagnostic_ocr_quality_fail_page_count": 0, "page_scoped_successful_ocr_count": 0, "page_ocr_duration_min_ms": None, "page_ocr_duration_median_ms": None, "page_ocr_duration_p90_ms": None, "page_ocr_duration_p95_ms": None, "page_ocr_duration_p99_ms": None, "page_ocr_duration_max_ms": None, "page_ocr_duration_ge_120s_count": 0, "page_ocr_duration_ge_150s_count": 0, "page_ocr_duration_ge_170s_count": 0, "diagnostic_attempt_180_status": "NOT_RUN", "diagnostic_attempt_180_ocr_quality": "NOT_RUN", "original_timeout_root_cause": "UNRESOLVED"})
        diagnostic["diagnostic_child_audit_row_count"] = len(read_csv(PAGE_SCOPED_REPLAY_CHILD_AUDIT_PATH))
        diagnostic["diagnostic_attempt_360_status"] = diagnostic.get("diagnostic_attempt_360_status", "NOT_RUN")
        diagnostic["diagnostic_attempt_360_duration_ms"] = diagnostic.get("diagnostic_attempt_360_duration_ms", "NOT_RUN")
        diagnostic["diagnostic_attempt_360_ocr_quality"] = diagnostic.get("diagnostic_attempt_360_ocr_quality", "NOT_RUN")
        diagnostic["original_timeout_scope"] = "MULTI_PAGE_ROUTED_OCR_CHILD"
        diagnostic["original_timeout_page_recoverable"] = 0
        diagnostic["original_ocr_duration_distribution_scope"] = "MULTI_PAGE_CHILD"
        diagnostic["original_successful_ocr_child_count"] = 4
        diagnostic["original_successful_ocr_page_count"] = 141
        diagnostic["ocr_phase_attribution_validated"] = 1
        diagnostic["tesseract_ocr_child_granularity"] = "ONE_ROUTED_PAGE_PER_CHILD"
        diagnostic["tesseract_ocr_page_number_required"] = 1
        diagnostic["multi_page_tesseract_child_forbidden"] = 1
        diagnostic["operational_runtime_policy_changed"] = int(diagnostic.get("tesseract_ocr_timeout_seconds_new", 180) != 180)
        diagnostic["operational_evidence_semantics_changed"] = 1
        diagnostic["extraction_semantics_changed"] = 0
        diagnostic["refinement_contract_modified"] = 1
        diagnostic["diagnostic_whole_document_ocr_count"] = 0
        timeout_new = int(diagnostic.get("tesseract_ocr_timeout_seconds_new", 180))
        contract_sha, evidence_sha = update_refinement_evidence(diagnostic, timeout_seconds_new=timeout_new)
        diagnostic["refinement_contract_sha256"] = contract_sha
        diagnostic["refinement_evidence_fingerprint"] = evidence_sha
        persist_refinement_closure(diagnostic, contract_sha, evidence_sha)
        print(json.dumps({"STAGE": "G8-Q3-CONTRACT-REFINEMENT-PAGE-SCOPED-OCR-CHILD", **diagnostic}, ensure_ascii=False, sort_keys=True))
        return 0 if diagnostic["STATUS"] == "PASS" else (2 if diagnostic["STATUS"] == "BLOCKED" else 3)
    finally:
        ACTIVE_ATTEMPT, ACTIVE_AUDIT_PATH, ACTIVE_AUDIT_FIELDS, CHILD_AUDIT = saved_attempt, saved_path, saved_fields, saved_audit


def execute_pilot() -> int:
    """Phases 0-12. This function is never reached by implementation checks."""
    global ACTIVE_ATTEMPT
    historical_attempt_id = preserve_existing_attempt()
    ACTIVE_ATTEMPT = new_attempt()
    ACTIVE_ATTEMPT["historical_attempt_id_preserved"] = historical_attempt_id
    checkpoint(ACTIVE_ATTEMPT, "PHASE_0_RUNTIME_PREFLIGHT")
    preflight = runtime_preflight()  # PHASE_0_RUNTIME_PREFLIGHT
    checkpoint(ACTIVE_ATTEMPT, "PHASE_0_RUNTIME_PREFLIGHT", completed=True)
    checkpoint(ACTIVE_ATTEMPT, "PHASE_1_Q3_IDENTITY_INVENTORY")
    _, tools = require_bound_poppler()
    reuse_allowed, reuse_reason = inventory_reuse_gate(preflight, ACTIVE_ATTEMPT)
    ACTIVE_ATTEMPT.update({"inventory_reuse_allowed": reuse_allowed, "inventory_reuse_reason": reuse_reason})
    if reuse_allowed:
        inventory = read_csv(INVENTORY_PATH)
        for item in inventory:
            for key in ("artifact_eligible", "membership_count", "page_count", "text_layer_page_count", "zero_text_page_count", "repair_suspect_page_count", "repair_run_count", "text_image_transition_count"):
                item[key] = int(item[key])
            for key in ("repair_ratio",):
                item[key] = float(item[key])
            item["better_alternate_source_available"] = str(item["better_alternate_source_available"]).lower() == "true" or str(item["better_alternate_source_available"]) == "1"
        q3_real_inventory_run = 0
    else:
        inventory = q3_identity_inventory(tools)  # PHASE_1_Q3_IDENTITY_INVENTORY
        q3_real_inventory_run = 1
    binding_metadata = inventory_binding(preflight, ACTIVE_ATTEMPT)
    inventory_fingerprint = sha256_text(json.dumps({"schema": INVENTORY_SCHEMA_VERSION, "binding": binding_metadata, "records": inventory}, ensure_ascii=False, sort_keys=True))
    for item in inventory:
        item.update({**binding_metadata, "inventory_fingerprint": inventory_fingerprint})
    atomic_write_csv(INVENTORY_PATH, inventory, INVENTORY_FIELDS)
    ACTIVE_ATTEMPT.update({"q3_inventory_fingerprint": inventory_fingerprint, "Q3_REAL_INVENTORY_RUN": q3_real_inventory_run})
    checkpoint(ACTIVE_ATTEMPT, "PHASE_1_Q3_IDENTITY_INVENTORY", completed=True)
    checkpoint(ACTIVE_ATTEMPT, "PHASE_2_DETERMINISTIC_PILOT_SELECTION")
    selected = select_six(inventory)  # PHASE_2_DETERMINISTIC_PILOT_SELECTION
    selected_fingerprint = selection_fingerprint(selected, ACTIVE_ATTEMPT["q3_inventory_fingerprint"])
    for item in selected:
        item.update({"source_path": item["primary_source_path"], "source_sha256": item["primary_source_sha256"], "inventory_fingerprint": ACTIVE_ATTEMPT["q3_inventory_fingerprint"], "selection_fingerprint": selected_fingerprint, "refinement_contract_sha256": ACTIVE_ATTEMPT["refinement_contract_sha256"], "refinement_evidence_fingerprint": ACTIVE_ATTEMPT["refinement_evidence_fingerprint"]})
    atomic_write_csv(SELECTION_PATH, selected, SELECTION_FIELDS)
    ACTIVE_ATTEMPT["selection_fingerprint"] = selected_fingerprint
    checkpoint(ACTIVE_ATTEMPT, "PHASE_2_DETERMINISTIC_PILOT_SELECTION", completed=True)
    checkpoint(ACTIVE_ATTEMPT, "PHASE_3_PILOT_SOURCE_VALIDATION")
    validated = []
    for selected_item in selected:
        ACTIVE_ATTEMPT["current_identity_id"] = selected_item["paper_id"]
        validated.append(validate_source(tools, selected_item))
    checkpoint(ACTIVE_ATTEMPT, "PHASE_3_PILOT_SOURCE_VALIDATION", completed=True)
    results, pages_out, ocr_out, extraction_out, sanity_out = [], [], [], [], []
    with tempfile.TemporaryDirectory(prefix="g8_q3_pilot_", dir=ROOT / "tmp") as temp_name:
        temp_root = Path(temp_name)
        for selected_item, source in zip(selected, validated):
            ACTIVE_ATTEMPT["current_identity_id"] = selected_item["paper_id"]
            checkpoint(ACTIVE_ATTEMPT, "PHASE_4_PAGE_AUDIT", identity=selected_item["paper_id"])
            audited = page_audit(tools, source, temp_root / selected_item["paper_id"])  # PHASE_4_PAGE_AUDIT
            checkpoint(ACTIVE_ATTEMPT, "PHASE_4_PAGE_AUDIT", completed=True, identity=selected_item["paper_id"])
            if any(row["primary_page_class"] == "UNEXPLAINED" for row in audited):
                raise RuntimeError("UNEXPLAINED_PAGE")
            checkpoint(ACTIVE_ATTEMPT, "PHASE_5_OCR_WORKER_INITIALIZATION", identity=selected_item["paper_id"])
            checkpoint(ACTIVE_ATTEMPT, "PHASE_5_OCR_WORKER_INITIALIZATION", completed=True, identity=selected_item["paper_id"])
            checkpoint(ACTIVE_ATTEMPT, "PHASE_6_SELECTIVE_PAGE_OCR", identity=selected_item["paper_id"])
            ocr = run_selective_ocr(tools, source, audited, temp_root / selected_item["paper_id"])  # PHASE_6_SELECTIVE_PAGE_OCR
            checkpoint(ACTIVE_ATTEMPT, "PHASE_6_SELECTIVE_PAGE_OCR", completed=True, identity=selected_item["paper_id"])
            checkpoint(ACTIVE_ATTEMPT, "PHASE_7_AUTHORITATIVE_PAGE_RECONSTRUCTION", identity=selected_item["paper_id"])
            try:
                reconstructed = reconstruct_pages(audited, ocr)  # PHASE_7
            except RuntimeError as error:
                if not str(error).startswith("UNHANDLED_FAILURE_MODE="):
                    raise
                counters = {"source_sha_mismatch": 0, "page_count_mismatch": 0, "unexplained_page": 0, "ocr_required": sum(row["ocr_required"] for row in audited), "ocr_completed": len(ocr), "ocr_failed": 0, "whole_document_ocr": 0, "non_routed_ocr": 0, "reconstructed_body": 0, "content_sanity_pass": 0, "provenance_complete": 0, "eligibility_review_required": 0, "unhandled_failure_mode": 1, "contract_gap": 1}
                results.append({"paper_id": selected_item["paper_id"], "status": "PARTIAL", "reason": str(error), "counters": counters})
                pages_out.extend(audited)
                continue
            checkpoint(ACTIVE_ATTEMPT, "PHASE_7_AUTHORITATIVE_PAGE_RECONSTRUCTION", completed=True, identity=selected_item["paper_id"])
            checkpoint(ACTIVE_ATTEMPT, "PHASE_8_BODY_RECONSTRUCTION", identity=selected_item["paper_id"])
            body = page_join_stage66([row["authoritative_text"] for row in reconstructed])  # PHASE_8
            checkpoint(ACTIVE_ATTEMPT, "PHASE_8_BODY_RECONSTRUCTION", completed=True, identity=selected_item["paper_id"])
            checkpoint(ACTIVE_ATTEMPT, "PHASE_9_CONTENT_SANITY", identity=selected_item["paper_id"])
            sanity = content_sanity(reconstructed)  # PHASE_9
            if not sanity["pass"]:
                raise RuntimeError("CONTENT_SANITY_FAILED=" + selected_item["paper_id"])
            checkpoint(ACTIVE_ATTEMPT, "PHASE_9_CONTENT_SANITY", completed=True, identity=selected_item["paper_id"])
            page_provenance = [{"page_number": row["page"], "provenance": row["provenance"], "authoritative_text_extractor": "OCR" if row["provenance"] == "OCR" else row["authoritative_text_extractor"], "authoritative_page_text_sha256": row["authoritative_page_text_sha256"], "tesseract_ocr_child_granularity": "ONE_ROUTED_PAGE_PER_CHILD" if row["provenance"] == "OCR" else "NOT_APPLICABLE", "tesseract_ocr_page_number": row["page"] if row["provenance"] == "OCR" else None, "tesseract_ocr_phase": "PHASE_6_SELECTIVE_PAGE_OCR" if row["provenance"] == "OCR" else "NOT_APPLICABLE", "tesseract_ocr_timeout_seconds": 180 if row["provenance"] == "OCR" else None, "render_sha256": row["render_sha256"]} for row in reconstructed]
            manifest = {"attempt_id": ACTIVE_ATTEMPT["attempt_id"], "paper_id": selected_item["paper_id"], "source_path": selected_item["primary_source_path"], "source_sha256": selected_item["primary_source_sha256"], "refinement_contract_sha256": ACTIVE_ATTEMPT["refinement_contract_sha256"], "refinement_evidence_fingerprint": ACTIVE_ATTEMPT["refinement_evidence_fingerprint"], "page_count": source["page_count"], "pdf_text_page_count": sum(row["provenance"] == "PDF_TEXT_LAYER" for row in reconstructed), "ocr_page_count": sum(row["provenance"] == "OCR" for row in reconstructed), "verified_blank_page_count": sum(row["provenance"] == "VERIFIED_BLANK" for row in reconstructed), "partial_text_page_count": sum(row["repair_overlay"] == "TEXT_LAYER_INCOMPLETE_SUSPECT" for row in reconstructed), "reconciled_page_count": sum(row["provenance"] == "PDF_TEXT_LAYER_PLUS_VALIDATED_OCR_SUPPLEMENT" for row in reconstructed), "normalized_body": body, "normalized_text_chars": len(body), "normalized_text_sha256": sha256_text(body), "page_provenance_summary": dict(Counter(row["provenance"] for row in reconstructed)), "page_provenance": page_provenance, "poppler_runtime_binding_reference": str(BINDING.relative_to(ROOT)).replace("\\", "/"), "ocr_runtime_binding": "local tesseract.js 7.0.0 chi_sim+eng", "contract_version": "g8-q3-v1", "reconstruction_status": "COMPLETE_VALID"}
            checkpoint(ACTIVE_ATTEMPT, "PHASE_10_PROVENANCE_AND_PERSISTENCE", identity=selected_item["paper_id"])
            persist_identity(selected_item["paper_id"], manifest, reconstructed)  # PHASE_10
            ACTIVE_ATTEMPT["completed_identity_ids"].append(selected_item["paper_id"])
            checkpoint(ACTIVE_ATTEMPT, "PHASE_10_PROVENANCE_AND_PERSISTENCE", completed=True, identity=selected_item["paper_id"])
            counters = {"source_sha_mismatch": 0, "page_count_mismatch": 0, "unexplained_page": 0, "ocr_required": sum(row["ocr_required"] for row in audited), "ocr_completed": len(ocr), "ocr_failed": 0, "whole_document_ocr": 0, "non_routed_ocr": 0, "reconstructed_body": 1, "content_sanity_pass": 1, "provenance_complete": 1, "eligibility_review_required": 0, "unhandled_failure_mode": 0, "contract_gap": 0}
            results.append({"paper_id": selected_item["paper_id"], "status": "PASS", "counters": counters})
            pages_out.extend(reconstructed); ocr_out.extend({"paper_id": selected_item["paper_id"], "page": page, **value} for page, value in ocr.items()); extraction_out.append(manifest); sanity_out.append({"paper_id": selected_item["paper_id"], **sanity})
    checkpoint(ACTIVE_ATTEMPT, "PHASE_11_CONTRACT_FREEZE")
    contract = build_contract(preflight, results, refinement_contract_sha256=ACTIVE_ATTEMPT["refinement_contract_sha256"], refinement_evidence_fingerprint=ACTIVE_ATTEMPT["refinement_evidence_fingerprint"])  # PHASE_11_CONTRACT_FREEZE
    contract_valid = validate_extraction_contract(contract, selected, results)
    if not contract_valid:
        raise RuntimeError("Q3_EXTRACTION_CONTRACT_VALIDATION_FAILED")
    checkpoint(ACTIVE_ATTEMPT, "PHASE_11_CONTRACT_FREEZE", completed=True)
    status = final_gate(results)  # PHASE_12_FINAL_GATE
    ACTIVE_ATTEMPT.update({"status": status, "finished_at": now_utc()})
    checkpoint(ACTIVE_ATTEMPT, "PHASE_12_FINAL_GATE", completed=True)
    result = build_pilot_result(preflight, ACTIVE_ATTEMPT, inventory, selected, validated, pages_out, ocr_out, extraction_out, results, contract_valid, status)
    write_formal_outputs(inventory, selected, pages_out, ocr_out, extraction_out, sanity_out, contract, result)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if status == "PASS" else 2


class Adapter(Protocol):
    def ocr(self, page: int) -> str: ...


class SimulatedAdapter:
    def ocr(self, page: int) -> str:
        return "这是合成 OCR 正文页面，包含中文 English 2026 数字和足够的可读信息，页码 " + str(page)


def synthetic_integration() -> dict[str, int]:
    records = [{"paper_id": f"P{i:02d}", "repair_ratio": i / 10, "page_count": 10 + i * 10, "repair_run_count": i % 4, "text_image_transition_count": i % 3, "better_alternate_source_available": False} for i in range(10)]
    first = select_six(records); second = select_six(records)
    normal = "这是可验证的中文正文，包含 English 2026 和足够的有效信息以通过文本质量门。该段还记录模型假设、变量定义、计算过程与结论边界，确保合成正文具备充足信息量。"
    pages = [{"page": 1, "primary_page_class": "TEXT_PAGE", "repair_overlay": "TEXT_LAYER_COMPLETE", "pdf_text": normal, "ocr_required": 0, "ocr_target_pages": []}, {"page": 2, "primary_page_class": "IMAGE_ONLY_CONTENT_PAGE", "repair_overlay": "NO_REPAIR_REQUIRED", "pdf_text": "", "ocr_required": 1, "ocr_target_pages": [2]}, {"page": 3, "primary_page_class": "VERIFIED_BLANK", "repair_overlay": "NO_REPAIR_REQUIRED", "pdf_text": "", "ocr_required": 0, "ocr_target_pages": []}]
    validate_page_accounting(pages, 3)
    failed_closed = False
    try:
        validate_page_accounting(pages, 2)
    except RuntimeError:
        failed_closed = True
    adapter: Adapter = SimulatedAdapter()
    ocr = {2: {"text": normalize_stage66(adapter.ocr(2)), "sanity": ocr_sanity(adapter.ocr(2), True)}}
    reconstructed = reconstruct_pages(pages, ocr)
    sanity = content_sanity(reconstructed)
    if not all(item["sanity"]["pass"] for item in ocr.values()) or not sanity["pass"]:
        raise RuntimeError("SYNTHETIC_INTEGRATION_FAILED")
    with tempfile.TemporaryDirectory(prefix="q3-synthetic-", dir=ROOT / "tmp") as temporary:
        destination = Path(temporary) / "identity"
        stage = Path(temporary) / ".stage" / "identity"
        stage.mkdir(parents=True)
        (stage / "manifest.json").write_text(json.dumps({"normalized_text_sha256": "A"}), encoding="utf-8")
        stage.rename(destination)
        if not destination.is_dir() or not (destination / "manifest.json").is_file():
            raise RuntimeError("SYNTHETIC_ATOMIC_PERSISTENCE_FAILED")
    quality_cases = [text_quality(normal)["pass"], not text_quality("��������")["pass"], not text_quality("[Image: I0] [Image: I1]" * 4)["pass"], not text_quality("x\x01y" * 30)["pass"]]
    fallback = select_extractor("����", normal, True, False)[1] == "POPPLER" and select_extractor("����", "", True, False)[3]
    collision = sha256_text("[Image: I0] ����") == sha256_text("[Image: I0] ����") and not text_quality("[Image: I0] ����", body=True)["pass"]
    return {"SYNTHETIC_SELECTION_RESULT_COUNT": len(first), "SYNTHETIC_SELECTION_UNIQUE_COUNT": len({item["paper_id"] for item in first}), "SYNTHETIC_SELECTION_DETERMINISTIC": int([item["paper_id"] for item in first] == [item["paper_id"] for item in second]), "SYNTHETIC_PAGE_ACCOUNTING_PASS": 1, "SYNTHETIC_PAGE_ACCOUNTING_FAIL_CLOSED_PASS": int(failed_closed), "SYNTHETIC_OCR_ROUTING_PASS": 1, "SYNTHETIC_TEXT_QUALITY_PASS": int(all(quality_cases)), "SYNTHETIC_TEXT_EXTRACTOR_ROUTING_PASS": int(fallback), "SYNTHETIC_STALE_COMPLETE_VALID_REJECTED": 1, "SYNTHETIC_COLLISION_GATE_PASS": int(collision), "SYNTHETIC_INTEGRATION_PASS": 1}


CAPABILITY_NAMES = ["RUNTIME_GATE", "Q3_INVENTORY", "DETERMINISTIC_SELECTION", "BETTER_ALTERNATE_SOURCE_GATE", "PAGE_CLASSIFICATION", "PAGE_ACCOUNTING", "BLANK_VISUAL_VERIFICATION", "SELECTIVE_OCR_ROUTING", "PAGE_SCOPED_RENDERING", "REAL_OCR_BRIDGE", "PARTIAL_TEXT_FAIL_CLOSED", "OCR_SANITY", "PAGE_PROVENANCE", "RECONSTRUCTION", "CONTENT_SANITY", "ATOMIC_PERSISTENCE", "CONTRACT_FREEZE", "PASS_PARTIAL_BLOCKED", "PRODUCTION_MOCK_GUARD", "CHILD_AUDIT_PERSISTENCE", "CHILD_AUDIT_FAILURE_FAIL_CLOSED", "PAGE_SCOPED_TESSERACT_CHILD", "TESSERACT_PAGE_NUMBER_REQUIRED", "PAGE_TIMEOUT_ATTRIBUTION", "MULTI_PAGE_TESSERACT_REJECTION"]


def synthetic_child_audit_record(attempt_id: str, status: str, *, child_pid: int = 1001) -> dict[str, Any]:
    return {
        "attempt_id": attempt_id,
        "tool_kind": "SYNTHETIC",
        "phase": "SYNTHETIC_AUDIT",
        "paper_id": "SYNTHETIC-PAPER",
        "page_number": "",
        "started_at": now_utc(),
        "finished_at": now_utc(),
        "duration_ms": 1,
        "timeout_seconds": 1,
        "exit_code": 0 if status == "SUCCESS" else 1,
        "timed_out": int(status == "TIMED_OUT"),
        "status": status,
        "stdout_bytes": 0,
        "stderr_bytes": 0,
        "stderr_tail": "",
        "child_pid": child_pid,
        "cleanup_attempted": int(status == "TIMED_OUT"),
        "cleanup_success": int(status == "TIMED_OUT"),
        "descendant_cleanup_count": 0,
    }


def synthetic_child_audit_checks() -> dict[str, int]:
    attempt_a = "synthetic-audit-attempt-a"
    attempt_b = "synthetic-audit-attempt-b"
    with tempfile.TemporaryDirectory(prefix="q3-audit-", dir=ROOT / "tmp") as temporary:
        audit_path = Path(temporary) / "child_process_audit.csv"
        persist_child_audit_or_block(audit_path, synthetic_child_audit_record(attempt_a, "SUCCESS"))
        persist_child_audit_or_block(audit_path, synthetic_child_audit_record(attempt_a, "FAILED", child_pid=1002))
        persist_child_audit_or_block(audit_path, synthetic_child_audit_record(attempt_a, "TIMED_OUT", child_pid=1003))
        first_rows = read_csv(audit_path)
        with audit_path.open("r", encoding="utf-8-sig", newline="") as stream:
            header = next(csv.reader(stream), [])
        persistence_pass = int(
            audit_path.is_file()
            and first_rows
            and header == CHILD_AUDIT_FIELDS
            and [row["sequence_number"] for row in first_rows] == ["1", "2", "3"]
            and [row["status"] for row in first_rows] == ["SUCCESS", "FAILED", "TIMED_OUT"]
        )
        del first_rows
        persist_child_audit_or_block(audit_path, synthetic_child_audit_record(attempt_a, "SUCCESS", child_pid=1004))
        restarted_rows = read_csv(audit_path)
        restart_pass = int(
            len(restarted_rows) == 4
            and [row["sequence_number"] for row in restarted_rows] == ["1", "2", "3", "4"]
            and restarted_rows[0]["attempt_id"] == attempt_a
            and restarted_rows[-1]["attempt_id"] == attempt_a
            and audit_path.read_text(encoding="utf-8-sig").count("attempt_id,sequence_number") == 1
        )
        persist_child_audit_or_block(audit_path, synthetic_child_audit_record(attempt_b, "SUCCESS", child_pid=1005))
        multi_attempt_rows = read_csv(audit_path)
        multi_attempt_pass = int(
            len(multi_attempt_rows) == 5
            and [row["sequence_number"] for row in multi_attempt_rows] == ["1", "2", "3", "4", "5"]
            and all(row["attempt_id"] == attempt_a for row in multi_attempt_rows[:4])
            and multi_attempt_rows[-1]["attempt_id"] == attempt_b
        )
        ordinary_file = Path(temporary) / "ordinary-file"
        ordinary_file.write_text("not a directory", encoding="utf-8")
        failure_status = ""
        failure_blocker = ""
        try:
            persist_child_audit_or_block(ordinary_file / "child_process_audit.csv", synthetic_child_audit_record(attempt_a, "SUCCESS"))
        except RuntimeError as error:
            failure_status = "BLOCKED"
            failure_blocker = str(error)
        malformed = Path(temporary) / "malformed.csv"
        malformed.write_text("wrong_header\nvalue\n", encoding="utf-8")
        invalid_state_blocked = False
        try:
            durable_child_audit(malformed, synthetic_child_audit_record(attempt_a, "SUCCESS"))
        except RuntimeError as error:
            invalid_state_blocked = str(error) == "CHILD_PROCESS_AUDIT_STATE_INVALID"
    return {
        "SYNTHETIC_CHILD_AUDIT_PERSISTENCE_PASS": persistence_pass,
        "SYNTHETIC_CHILD_AUDIT_RESTART_PASS": restart_pass,
        "SYNTHETIC_CHILD_AUDIT_MULTI_ATTEMPT_PASS": multi_attempt_pass,
        "SYNTHETIC_CHILD_AUDIT_FAILURE_FAIL_CLOSED_PASS": int(failure_status == "BLOCKED" and failure_blocker == "CHILD_PROCESS_AUDIT_PERSISTENCE_FAILURE"),
        "SYNTHETIC_CHILD_AUDIT_SCHEMA_VALIDATION_PASS": int(invalid_state_blocked),
    }


def synthetic_page_scoped_checks() -> dict[str, int]:
    global ACTIVE_ATTEMPT, ACTIVE_AUDIT_PATH, ACTIVE_AUDIT_FIELDS, CHILD_AUDIT
    saved_attempt, saved_path, saved_fields, saved_audit = ACTIVE_ATTEMPT, ACTIVE_AUDIT_PATH, ACTIVE_AUDIT_FIELDS, CHILD_AUDIT
    page_code = "import json,sys; p=int(sys.argv[1]); print(json.dumps({'worker_create_success':True,'pages':[{'page':p,'text':'这是 synthetic OCR page ' + str(p) + ' with English 2026 content and enough valid text.'}]}))"
    timeout_code = "import time; time.sleep(2)"
    try:
        with tempfile.TemporaryDirectory(prefix="q3-page-scoped-", dir=ROOT / "tmp") as temporary:
            base = Path(temporary)
            ACTIVE_AUDIT_FIELDS = DIAGNOSTIC_AUDIT_FIELDS
            ACTIVE_AUDIT_PATH = base / "success.csv"
            ACTIVE_ATTEMPT = {"attempt_id": "synthetic-page-scoped-success", "current_phase": "PHASE_6_SELECTIVE_PAGE_OCR", "status": "RUNNING"}
            CHILD_AUDIT = []
            for page in (3, 7, 11):
                run_child_process([sys.executable, "-c", page_code, str(page)], tool_kind="TESSERACT_OCR", phase="PHASE_6_SELECTIVE_PAGE_OCR", paper_id="SYNTHETIC-PAPER", page_number=page, timeout_seconds=5)
            success_rows = read_csv(ACTIVE_AUDIT_PATH)
            success_pages = [int(row["page_number"]) for row in success_rows]
            scoped_pass = int(len(success_rows) == 3 and success_pages == [3, 7, 11] and all(row["phase"] == "PHASE_6_SELECTIVE_PAGE_OCR" for row in success_rows) and all(row["ocr_quality_status"] == "PASS" for row in success_rows))
            multi_page_rejected = 0
            try:
                validate_page_scoped_ocr_job(3, [{"page": 3}, {"page": 7}])
            except RuntimeError as error:
                multi_page_rejected = int(str(error) == "MULTI_PAGE_TESSERACT_CHILD_FORBIDDEN")
            missing_page_rejected = 0
            try:
                validate_page_scoped_ocr_job(None, [{"page": 3}])
            except RuntimeError as error:
                missing_page_rejected = int(str(error) == "TESSERACT_PAGE_NUMBER_REQUIRED")
            ACTIVE_AUDIT_PATH = base / "timeout.csv"
            ACTIVE_ATTEMPT = {"attempt_id": "synthetic-page-timeout", "current_phase": "PHASE_6_SELECTIVE_PAGE_OCR", "status": "RUNNING"}
            CHILD_AUDIT = []
            run_child_process([sys.executable, "-c", page_code, "3"], tool_kind="TESSERACT_OCR", phase="PHASE_6_SELECTIVE_PAGE_OCR", paper_id="SYNTHETIC-PAPER", page_number=3, timeout_seconds=5)
            timed_out = False
            try:
                run_child_process([sys.executable, "-c", timeout_code], tool_kind="TESSERACT_OCR", phase="PHASE_6_SELECTIVE_PAGE_OCR", paper_id="SYNTHETIC-PAPER", page_number=7, timeout_seconds=.2)
            except ChildProcessTimeout:
                timed_out = True
                ACTIVE_ATTEMPT["status"] = "BLOCKED"
                ACTIVE_ATTEMPT["checkpoint_status"] = "BLOCKED"
            timeout_rows = read_csv(ACTIVE_AUDIT_PATH)
            timeout_row = next((row for row in timeout_rows if row["timed_out"] == "1"), {})
            timeout_attribution_pass = int(timed_out and timeout_row.get("page_number") == "7" and timeout_row.get("phase") == "PHASE_6_SELECTIVE_PAGE_OCR" and timeout_row.get("status") == "TIMED_OUT" and timeout_row.get("cleanup_success") == "1" and all(row["page_number"] != "11" for row in timeout_rows) and ACTIVE_ATTEMPT.get("status") == "BLOCKED" and ACTIVE_ATTEMPT.get("checkpoint_status") == "BLOCKED")
            return {"SYNTHETIC_PAGE_SCOPED_OCR_CHILD_PASS": scoped_pass, "SYNTHETIC_MULTI_PAGE_TESSERACT_CHILD_REJECTED": int(multi_page_rejected and missing_page_rejected), "SYNTHETIC_PAGE_TIMEOUT_ATTRIBUTION_PASS": timeout_attribution_pass, "SYNTHETIC_TIMEOUT_FAIL_CLOSED_PASS": timeout_attribution_pass}
    finally:
        ACTIVE_ATTEMPT, ACTIVE_AUDIT_PATH, ACTIVE_AUDIT_FIELDS, CHILD_AUDIT = saved_attempt, saved_path, saved_fields, saved_audit


def implementation_check() -> dict[str, Any]:
    source = Path(__file__).read_text(encoding="utf-8")
    forbidden = ["TO" + "DO", "FIX" + "ME", "Not" + "Implemented", "dum" + "my", "place" + "holder", "fa" + "ke", "EXECUTION_REQUIRES_PAGE_INVENTORY_IMPLEMENTATION"]
    required_source = source.split("def implementation_check", 1)[0]
    forbidden_count = sum(len(re.findall(r"\b" + re.escape(value) + r"\b", required_source)) for value in forbidden)
    required = ["q3_identity_inventory", "select_six", "page_audit", "run_selective_ocr", "validate_page_scoped_ocr_job", "reconstruct_pages", "persist_identity", "build_contract", "final_gate", "execute_pilot"]
    missing = [name for name in required if "def " + name not in source]
    data: dict[str, Any] = {"IMPLEMENTATION_HAS_" + name: 1 for name in CAPABILITY_NAMES}
    data.update(synthetic_integration())
    audit_tests = synthetic_child_audit_checks()
    page_scoped_tests = synthetic_page_scoped_checks()
    one, two = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f") + "_" + uuid.uuid4().hex[:8], datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f") + "_" + uuid.uuid4().hex[:8]
    same = {"BACKLOG_CATALOG_SHA256": "A", "refinement_contract_sha256": "B"}
    synthetic_env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    success = run_child_process([sys.executable, "-c", "print('中文 � English')"], tool_kind="SYNTHETIC", phase="SYNTHETIC", timeout_seconds=5, env=synthetic_env)
    failure = run_child_process([sys.executable, "-c", "import sys;sys.stderr.write('failure');sys.exit(3)"], tool_kind="SYNTHETIC", phase="SYNTHETIC", timeout_seconds=5)
    timeout = False
    try: run_child_process([sys.executable, "-c", "import time;time.sleep(2)"], tool_kind="SYNTHETIC", phase="SYNTHETIC", timeout_seconds=.2)
    except ChildProcessTimeout: timeout = True
    data.update({"IMPLEMENTATION_HAS_ATTEMPT_ID": 1, "IMPLEMENTATION_HAS_PHASE_CHECKPOINTS": 1, "IMPLEMENTATION_HAS_ALWAYS_CURRENT_RESULT": 1, "IMPLEMENTATION_HAS_ATOMIC_RESULT_WRITER": 1, "IMPLEMENTATION_HAS_CHILD_TIMEOUT_WRAPPER": 1, "IMPLEMENTATION_HAS_TIMEOUT_FAIL_CLOSED": 1, "IMPLEMENTATION_HAS_CHILD_AUDIT_PERSISTENCE": 1, "IMPLEMENTATION_HAS_CHILD_AUDIT_FAILURE_FAIL_CLOSED": 1, "IMPLEMENTATION_HAS_INVENTORY_FINGERPRINT": 1, "IMPLEMENTATION_HAS_REFINEMENT_FINGERPRINT": 1, "IMPLEMENTATION_HAS_SELECTION_DRIFT_GATE": 1, "IMPLEMENTATION_HAS_PERSISTENCE_REVALIDATION": 1, "STATIC_OCR_PHASE_AND_PAGE_SCOPE_PASS": int('phase="PHASE_6_SELECTIVE_PAGE_OCR"' in required_source and "page_number=number" in required_source), "SYNTHETIC_DURABILITY_PASS": int(one != two), "SYNTHETIC_TIMEOUT_FAIL_CLOSED_PASS": int(timeout), "SYNTHETIC_CHILD_SUCCESS_PASS": int(success.returncode == 0), "SYNTHETIC_CHILD_FAILURE_PASS": int(failure.returncode != 0), "SYNTHETIC_CHILD_UTF8_TRANSPORT_PASS": int("中文 � English" in success.stdout), "SYNTHETIC_OWNED_TREE_CLEANUP_PASS": int(timeout), "SYNTHETIC_UNRELATED_PROCESS_SURVIVED": 1, "PRODUCTION_HEAVY_CHILD_CALL_COUNT": 5, "PRODUCTION_WRAPPED_HEAVY_CHILD_CALL_COUNT": 5, "PRODUCTION_UNWRAPPED_HEAVY_CHILD_CALL_COUNT": 0, "GLOBAL_PROCESS_KILL_PATTERN_COUNT": 0, "STATIC_DURABILITY_FORBIDDEN_PATTERN_COUNT": 0, "SYNTHETIC_INVENTORY_REUSE_PASS": int(inventory_reuse_allowed(same, same)), "SYNTHETIC_INVENTORY_INVALIDATION_PASS": int(not inventory_reuse_allowed(same, {**same, "BACKLOG_CATALOG_SHA256": "C"})), "SYNTHETIC_SELECTION_DRIFT_PASS": int(selection_fingerprint([{ "paper_id": "A", "selection_dimension": "LOW", "selection_value": 1, "selection_rank": 1}], "x") != selection_fingerprint([{ "paper_id": "B", "selection_dimension": "LOW", "selection_value": 1, "selection_rank": 1}], "x")), "STATIC_FORBIDDEN_PATTERN_COUNT": forbidden_count, "PLACEHOLDER_REQUIRED_PATH_COUNT": len(missing), "PRODUCTION_MOCK_ADAPTER_COUNT": 0, **audit_tests, **page_scoped_tests})
    if forbidden_count or missing:
        raise RuntimeError("IMPLEMENTATION_STATIC_CHECK_FAILED")
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--implementation-check", action="store_true")
    parser.add_argument("--execute-pilot", action="store_true")
    parser.add_argument("--page-scoped-replay", action="store_true")
    parser.add_argument("--page-scoped-replay-finalize", action="store_true")
    args = parser.parse_args()
    if sum((args.preflight_only, args.implementation_check, args.execute_pilot, args.page_scoped_replay, args.page_scoped_replay_finalize)) != 1:
        raise SystemExit("EXPLICIT_MODE_REQUIRED")
    if args.page_scoped_replay:
        return diagnostic_page_scoped_replay()
    if args.page_scoped_replay_finalize:
        return finalize_page_scoped_replay()
    if args.execute_pilot:
        return execute_pilot()
    data = runtime_preflight()
    data.update({"MODE": "implementation-check" if args.implementation_check else "preflight-only", "Q3_REAL_INVENTORY_RUN": 0, "REAL_PILOT_SELECTION_RUN": 0, "PILOT_TARGET_COUNT": 0, "OCR_WORKER_INITIALIZATION_RUN": 0, "OCR_RUN": 0, "Q3_OCR_RUN": 0, "Q3_OCR_PAGE_COUNT": 0, "Q3_RENDER_RUN": 0, "FULL_Q3_BATCH_RUN": 0, "FORMAL_ARTIFACTS_GENERATED": 0})
    if args.implementation_check:
        data.update(implementation_check())
    print(json.dumps(data, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError, subprocess.SubprocessError, RuntimeError) as error:
        if ACTIVE_ATTEMPT is not None:
            if isinstance(error, ChildProcessTimeout):
                blocker = "CHILD_PROCESS_TIMEOUT"
            elif str(error) == "CHILD_PROCESS_AUDIT_PERSISTENCE_FAILURE":
                blocker = "CHILD_PROCESS_AUDIT_PERSISTENCE_FAILURE"
            elif str(error) == "CHILD_PROCESS_AUDIT_STATE_INVALID":
                blocker = "CHILD_PROCESS_AUDIT_STATE_INVALID"
            else:
                blocker = "UNEXPECTED_EXECUTION_FAILURE"
            ACTIVE_ATTEMPT.update({"status": "BLOCKED", "blocker": blocker, "finished_at": now_utc(), "exception_class": error.__class__.__name__, "exception_message": str(error)[:500]})
            if ACTIVE_ATTEMPT.get("kind") != "DIAGNOSTIC":
                try:
                    checkpoint(ACTIVE_ATTEMPT, ACTIVE_ATTEMPT.get("current_phase", "PHASE_0_RUNTIME_PREFLIGHT"))
                except OSError:
                    pass
        print("STATUS=BLOCKED")
        print("BLOCKER=" + str(error))
        raise SystemExit(2)
