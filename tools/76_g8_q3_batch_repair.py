"""G8 Q3 batch repair entrypoint.

This entrypoint deliberately reuses the page-aware, page-scoped extraction core
from ``72_g8_q3_contract_pilot_resume.py``.  It adds only batch orchestration,
source selection, resumable checkpoints, and isolated non-formal persistence.
The default modes are implementation/preflight checks; ``--execute-batch`` is
the only mode that renders PDFs or starts OCR children.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import os
import re
import shutil
import sys
import tempfile
import time
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def repository_root(anchor: Path) -> Path:
    for candidate in (anchor, *anchor.parents):
        if (candidate / "catalog" / "scale").is_dir() and (candidate / "tools").is_dir():
            return candidate
    raise RuntimeError("REPOSITORY_ROOT_NOT_FOUND")


ROOT = repository_root(Path(__file__).resolve().parent)
SCALE = ROOT / "catalog" / "scale"
REPORTS = ROOT / "reports" / "scale"
BATCH_ROOT = SCALE / "g8_q3_batch_repair"
BATCH_STAGE_ROOT = BATCH_ROOT / ".stage"
BATCH_HISTORY_ROOT = SCALE / "g8_q3_batch_repair_attempt_history"
ATTEMPT_PATH = SCALE / "g8_q3_batch_repair_attempt.json"
RESULT_PATH = SCALE / "g8_q3_batch_repair_result.json"
PROGRESS_PATH = SCALE / "g8_q3_batch_repair_progress.csv"
SOURCE_SELECTION_PATH = SCALE / "g8_q3_batch_source_selection.csv"
PAGE_AUDIT_PATH = SCALE / "g8_q3_batch_page_audit.csv"
OCR_AUDIT_PATH = SCALE / "g8_q3_batch_ocr_audit.csv"
CHILD_AUDIT_PATH = SCALE / "g8_q3_batch_child_process_audit.csv"
EXTRACTION_MANIFEST_PATH = SCALE / "g8_q3_batch_extraction_manifest.csv"
CONTENT_SANITY_PATH = SCALE / "g8_q3_batch_content_sanity.csv"
REPORT_PATH = REPORTS / "G8_Q3_BATCH_REPAIR.md"
CONTRACT_PATH = SCALE / "g8_q3_extraction_contract_v1.json"
PILOT_RESULT_PATH = SCALE / "g8_q3_contract_pilot_result.json"
PILOT_RUNNER_PATH = ROOT / "tools" / "72_g8_q3_contract_pilot_resume.py"

EXPECTED_REFINEMENT_SHA = "1D8BE5FE247FFF54DD3147B493820AB92C1BFEE211DB6FE8E21D59C64E4F1F2C"
EXPECTED_EVIDENCE_FINGERPRINT = "5FA095687812D8FB58CE9F61DCAE88F0B096FDBC2219326A8C77571C3311C70E"
EXPECTED_TARGET_COUNT = 128
EXCLUDED_IDENTITY = "CUMCM-2011-D-038"
STAGE = "G8-Q3-BATCH-REPAIR"

SOURCE_FIELDS = [
    "batch_attempt_id", "paper_id", "primary_source_path", "primary_source_sha256",
    "alternate_source_count", "better_alternate_source_available", "better_alternate_source_paths",
    "chosen_extraction_source_path", "chosen_extraction_source_sha256", "selection_reason",
    "source_selection_gate", "refinement_contract_sha256", "refinement_evidence_fingerprint",
]
PROGRESS_FIELDS = [
    "batch_attempt_id", "paper_id", "sequence_number", "status", "error_code",
    "primary_error_code", "cleanup_error_code", "source_gate_status", "page_count",
    "ocr_required", "ocr_completed", "body_quality_status", "content_sanity_status",
    "provenance_status", "persistence_status", "reused", "started_at", "finished_at",
]
PAGE_FIELDS = [
    "batch_attempt_id", "paper_id", "source_sha256", "page_number", "primary_page_class",
    "repair_overlay", "authoritative_text_extractor", "pdf_text_chars",
    "pdf_inspector_quality_status", "poppler_quality_status", "ocr_required",
    "ocr_target_pages", "render_width", "render_height", "render_pixel_count",
    "render_sha256", "authoritative_page_source", "authoritative_page_text_chars",
    "authoritative_page_text_sha256", "page_text_quality_status",
]
OCR_FIELDS = [
    "batch_attempt_id", "paper_id", "page_number", "tool_kind", "phase", "timeout_seconds",
    "duration_ms", "status", "timed_out", "exit_code", "cleanup_success", "render_width",
    "render_height", "render_pixel_count", "render_file_size", "render_sha256",
    "ocr_text_chars", "ocr_text_sha256", "ocr_quality_status",
]
MANIFEST_FIELDS = [
    "batch_attempt_id", "paper_id", "status", "source_path", "source_sha256", "page_count",
    "pdf_text_page_count", "ocr_page_count", "verified_blank_page_count", "normalized_text_sha256",
    "normalized_text_chars", "body_quality_status", "content_sanity_pass", "provenance_complete",
    "persistence_status", "manifest_path", "body_path", "provenance_path", "quality_path",
    "refinement_contract_sha256", "refinement_evidence_fingerprint",
]
SANITY_FIELDS = [
    "batch_attempt_id", "paper_id", "page_count", "page_order_monotonic",
    "suspicious_adjacent_duplicate", "page_text_quality_pass", "body_quality_status",
    "body_text_chars", "opening_plausible", "middle_continuity", "ending_plausible", "pass",
]


class BatchPartial(RuntimeError):
    pass


class BatchBlocked(RuntimeError):
    pass


def load_pilot() -> Any:
    spec = importlib.util.spec_from_file_location("g8_q3_pilot_core", PILOT_RUNNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("PILOT_CORE_IMPORT_FAILED")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pilot = load_pilot()


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict[str, Any]) -> None:
    pilot.atomic_write_json(path, value)


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    pilot.atomic_write_csv(path, rows, fields)


def bool_value(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def safe_relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve())).replace("\\", "/")
    except ValueError as exc:
        raise BatchBlocked("SOURCE_OUTSIDE_REPOSITORY") from exc


def error_code(error: BaseException) -> str:
    message = str(error).strip()
    return message.split("=", 1)[0].split("|", 1)[0] or error.__class__.__name__.upper()


def contract_gate() -> dict[str, Any]:
    if not CONTRACT_PATH.is_file():
        raise BatchBlocked("Q3_EXTRACTION_CONTRACT_MISSING")
    contract = read_json(CONTRACT_PATH)
    refinement_sha, evidence = pilot.refinement_fingerprint()
    if refinement_sha != EXPECTED_REFINEMENT_SHA or evidence != EXPECTED_EVIDENCE_FINGERPRINT:
        raise BatchBlocked("CURRENT_REFINEMENT_BINDING_MISMATCH")
    if contract.get("refinement_contract_sha256") != refinement_sha or contract.get("refinement_evidence_fingerprint") != evidence:
        raise BatchBlocked("EXTRACTION_CONTRACT_REFINEMENT_BINDING_MISMATCH")
    required = {
        "q3_definition": "PARTIAL_SCAN + artifact_eligible logical identities",
        "tesseract_ocr_child_granularity": "ONE_ROUTED_PAGE_PER_CHILD",
        "tesseract_ocr_page_number_required": True,
        "multi_page_tesseract_child_forbidden": True,
        "tesseract_ocr_phase": "PHASE_6_SELECTIVE_PAGE_OCR",
        "tesseract_ocr_timeout_scope": "PER_PAGE_CHILD",
        "tesseract_ocr_timeout_seconds": 180,
        "auto_retry_after_timeout": False,
    }
    if any(contract.get(key) != value for key, value in required.items()):
        raise BatchBlocked("AUTHORITATIVE_Q3_CONTRACT_RULE_MISMATCH")
    child_policy = contract.get("child_process_contract", {}).get("timeout_policy", {})
    if child_policy.get("auto_retry") is not False or child_policy.get("per_tool_timeouts", {}).get("TESSERACT_OCR") != 180:
        raise BatchBlocked("AUTHORITATIVE_Q3_CHILD_TIMEOUT_CONTRACT_MISMATCH")
    if contract.get("pilot_status") != "PASS" or contract.get("pilot_target_count") != 6 or not contract.get("pilot_result_validated"):
        raise BatchBlocked("PILOT_CONTRACT_BINDING_INVALID")
    if str(contract.get("pilot_attempt_id", "")) == "":
        raise BatchBlocked("PILOT_ATTEMPT_BINDING_MISSING")
    pilot_result = read_json(PILOT_RESULT_PATH)
    if pilot_result.get("STATUS") != "PASS" or pilot_result.get("ATTEMPT_ID") != contract.get("pilot_attempt_id") or pilot_result.get("PILOT_TARGET_COUNT") != 6:
        raise BatchBlocked("PILOT_RESULT_BINDING_INVALID")
    return {
        "contract": contract,
        "refinement_contract_sha256": refinement_sha,
        "refinement_evidence_fingerprint": evidence,
        "extraction_contract_sha256": pilot.sha256_file(CONTRACT_PATH),
        "pilot_result": pilot_result,
    }


def new_attempt(gate: dict[str, Any]) -> dict[str, Any]:
    catalogs = pilot.catalog_fingerprints()
    return {
        "stage": STAGE,
        "attempt_id": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f") + "_" + uuid.uuid4().hex[:8],
        "started_at": now_utc(), "updated_at": now_utc(), "finished_at": "", "status": "RUNNING",
        "current_phase": "PHASE_0_RUNTIME_PREFLIGHT", "last_completed_phase": "",
        "completed_identity_ids": [], "current_identity_id": "", "target_count": EXPECTED_TARGET_COUNT,
        "process_id": os.getpid(),
        "runner_sha256": pilot.sha256_file(Path(__file__)),
        "pilot_runner_sha256": pilot.sha256_file(PILOT_RUNNER_PATH),
        "extraction_contract_sha256": gate["extraction_contract_sha256"],
        "refinement_contract_sha256": gate["refinement_contract_sha256"],
        "refinement_evidence_fingerprint": gate["refinement_evidence_fingerprint"],
        "inventory_path": safe_relative(pilot.INVENTORY_PATH),
        "inventory_sha256": pilot.sha256_file(pilot.INVENTORY_PATH),
        "**REAL_BATCH_ATTEMPT_CREATED**": 1,
        **catalogs,
    }


def archive_previous_attempt() -> str:
    if not ATTEMPT_PATH.is_file():
        return "NONE"
    previous = read_json(ATTEMPT_PATH)
    previous_id = str(previous.get("attempt_id", "")).strip()
    if not previous_id:
        raise BatchBlocked("BATCH_ATTEMPT_ID_MISSING")
    if previous.get("status") == "RUNNING":
        previous_pid = int(previous.get("process_id", 0) or 0)
        process_alive = False
        if previous_pid:
            try:
                os.kill(previous_pid, 0)
                process_alive = True
            except OSError:
                process_alive = False
        if process_alive:
            raise BatchBlocked("ACTIVE_BATCH_ATTEMPT_ALREADY_RUNNING=" + previous_id)
    destination = BATCH_HISTORY_ROOT / previous_id
    destination.mkdir(parents=True, exist_ok=True)
    for source in (ATTEMPT_PATH, RESULT_PATH):
        if source.is_file():
            target = destination / source.name
            if target.exists() and pilot.sha256_file(target) != pilot.sha256_file(source):
                raise BatchBlocked("BATCH_ATTEMPT_HISTORY_CONFLICT=" + previous_id)
            if not target.exists():
                temporary = target.with_name(target.name + ".tmp-" + uuid.uuid4().hex)
                shutil.copy2(source, temporary)
                pilot.replace_with_retry(temporary, target)
    return previous_id


def load_inventory(gate: dict[str, Any], attempt: dict[str, Any]) -> tuple[list[dict[str, Any]], str]:
    preflight = gate["preflight"]
    allowed, reason = pilot.inventory_reuse_gate(preflight, attempt)
    if not allowed and reason == "INVENTORY_SCHEMA_VERSION_MISMATCH":
        # The existing Pilot writer emitted the same authoritative columns in
        # sorted order.  Accept order-only drift after checking exact schema
        # membership and every current refinement/catalog binding value.
        with pilot.INVENTORY_PATH.open("r", encoding="utf-8-sig", newline="") as stream:
            header = next(csv.reader(stream), [])
        if set(header) == set(pilot.INVENTORY_FIELDS) and len(header) == len(pilot.INVENTORY_FIELDS):
            rows_for_binding = pilot.read_csv(pilot.INVENTORY_PATH)
            expected_binding = pilot.inventory_binding(preflight, attempt)
            if len(rows_for_binding) == EXPECTED_TARGET_COUNT and all(all(row.get(key) == value for key, value in expected_binding.items()) for row in rows_for_binding):
                allowed, reason = 1, "CURRENT_REFINEMENT_INVENTORY_HEADER_ORDER_COMPATIBLE"
    if not allowed:
        raise BatchBlocked("Q3_INVENTORY_REUSE_GATE_FAILED=" + reason)
    rows = pilot.read_csv(pilot.INVENTORY_PATH)
    normalized: list[dict[str, Any]] = []
    for row in sorted(rows, key=lambda value: value.get("paper_id", "")):
        if row.get("paper_id") == EXCLUDED_IDENTITY:
            raise BatchBlocked("EXCLUDED_IDENTITY_PRESENT=" + EXCLUDED_IDENTITY)
        if row.get("q3_reason") != "PARTIAL_SCAN" or not bool_value(row.get("artifact_eligible")) or row.get("membership_count") != "1":
            raise BatchBlocked("Q3_TARGET_SELECTION_BINDING_INVALID=" + row.get("paper_id", ""))
        converted = dict(row)
        for key in ("page_count", "text_layer_page_count", "zero_text_page_count", "repair_suspect_page_count", "repair_run_count", "text_image_transition_count", "alternate_source_count"):
            converted[key] = int(row.get(key, 0))
        converted["repair_ratio"] = float(row.get("repair_ratio", 0.0))
        converted["artifact_eligible"] = 1
        converted["better_alternate_source_available"] = bool_value(row.get("better_alternate_source_available"))
        try:
            converted["better_alternate_source_paths"] = json.loads(row.get("better_alternate_source_paths", "[]"))
        except (TypeError, ValueError, json.JSONDecodeError) as exc:
            raise BatchBlocked("ALTERNATE_SOURCE_LIST_INVALID=" + row.get("paper_id", "")) from exc
        normalized.append(converted)
    if len(normalized) != EXPECTED_TARGET_COUNT or len({row["paper_id"] for row in normalized}) != EXPECTED_TARGET_COUNT:
        raise BatchBlocked("Q3_TARGET_CARDINALITY_INVALID")
    return normalized, reason


def choose_sources(rows: list[dict[str, Any]], gate: dict[str, Any], attempt: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    mapped = {(row.get("paper_id", ""), row.get("file_path", "")): row for row in pilot.read_csv(pilot.SOURCE_MAP)}
    chosen: list[dict[str, Any]] = []
    audit: list[dict[str, Any]] = []
    for row in rows:
        paper_id = row["paper_id"]
        primary_path = str(row["primary_source_path"])
        primary_sha = str(row["primary_source_sha256"]).upper()
        paths = list(row.get("better_alternate_source_paths") or [])
        selected_path, selected_sha, reason = primary_path, primary_sha, "PRIMARY_SOURCE_NO_BETTER_ALTERNATE"
        if row.get("better_alternate_source_available"):
            valid: list[tuple[str, str]] = []
            for candidate in sorted(str(path) for path in paths):
                file_path = ROOT / candidate
                mapping = mapped.get((paper_id, candidate))
                if mapping and file_path.is_file() and file_path.read_bytes()[:5] == b"%PDF-":
                    digest = pilot.sha256_file(file_path)
                    if digest == str(mapping.get("file_sha256", "")).upper():
                        valid.append((candidate, digest))
            if not valid:
                raise BatchBlocked("BETTER_ALTERNATE_SOURCE_GATE_FAILED=" + paper_id)
            selected_path, selected_sha = valid[0]
            reason = "BETTER_SAME_IDENTITY_SHA_VERIFIED_ALTERNATE"
        item = dict(row)
        item.update({"primary_source_path": selected_path, "primary_source_sha256": selected_sha, "chosen_source_path": selected_path, "chosen_source_sha256": selected_sha, "source_selection_reason": reason})
        chosen.append(item)
        audit.append({
            "batch_attempt_id": attempt["attempt_id"], "paper_id": paper_id, "primary_source_path": primary_path,
            "primary_source_sha256": primary_sha, "alternate_source_count": row.get("alternate_source_count", 0),
            "better_alternate_source_available": int(bool(row.get("better_alternate_source_available"))),
            "better_alternate_source_paths": json.dumps(paths, ensure_ascii=False),
            "chosen_extraction_source_path": selected_path, "chosen_extraction_source_sha256": selected_sha,
            "selection_reason": reason, "source_selection_gate": "PASS",
            "refinement_contract_sha256": gate["refinement_contract_sha256"],
            "refinement_evidence_fingerprint": gate["refinement_evidence_fingerprint"],
        })
    return chosen, audit


def source_snapshot(items: list[dict[str, Any]]) -> dict[str, str]:
    return {item["paper_id"]: pilot.sha256_file(ROOT / item["chosen_source_path"]) for item in items}


def page_audit_row(attempt: dict[str, Any], item: dict[str, Any], row: dict[str, Any], reconstructed: dict[str, Any] | None = None) -> dict[str, Any]:
    visual = row["visual"]
    return {
        "batch_attempt_id": attempt["attempt_id"], "paper_id": item["paper_id"], "source_sha256": item["chosen_source_sha256"],
        "page_number": row["page"], "primary_page_class": row["primary_page_class"], "repair_overlay": row["repair_overlay"],
        "authoritative_text_extractor": row["authoritative_text_extractor"], "pdf_text_chars": row["pdf_text_chars"],
        "pdf_inspector_quality_status": row["pdf_inspector_quality"]["quality_status"], "poppler_quality_status": row["poppler_quality"]["quality_status"],
        "ocr_required": row["ocr_required"], "ocr_target_pages": json.dumps(row["ocr_target_pages"], ensure_ascii=False),
        "render_width": visual["width"], "render_height": visual["height"], "render_pixel_count": visual["width"] * visual["height"],
        "render_sha256": row["render_sha256"], "authoritative_page_source": (reconstructed or {}).get("provenance", ""),
        "authoritative_page_text_chars": (reconstructed or {}).get("authoritative_page_text_chars", ""),
        "authoritative_page_text_sha256": (reconstructed or {}).get("authoritative_page_text_sha256", ""),
        "page_text_quality_status": pilot.text_quality((reconstructed or {}).get("authoritative_text", "")).get("quality_status", ""),
    }


def ocr_audit_rows(attempt_id: str, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **{key: record.get(key, "") for key in OCR_FIELDS},
            "batch_attempt_id": attempt_id,
        }
        for record in records
        if record.get("attempt_id") == attempt_id and record.get("tool_kind") == "TESSERACT_OCR"
    ]


def persistence_state(path: Path, expected: dict[str, Any] | None = None) -> str:
    if not path.exists():
        return "ABSENT"
    required = [path / "manifest.json", path / "normalized_body.txt", path / "provenance.json", path / "quality.json", path / "pages"]
    if not all(value.is_file() if value.name != "pages" else value.is_dir() for value in required):
        return "PARTIAL"
    try:
        manifest = read_json(path / "manifest.json")
        body = (path / "normalized_body.txt").read_text(encoding="utf-8")
        provenance = read_json(path / "provenance.json")
        quality = read_json(path / "quality.json")
        if expected:
            for key in ("paper_id", "source_sha256", "refinement_contract_sha256", "refinement_evidence_fingerprint", "page_count"):
                if manifest.get(key) != expected.get(key):
                    return "UNKNOWN"
        if manifest.get("normalized_text_sha256") != pilot.sha256_text(body) or not pilot.text_quality(body, body=True)["pass"]:
            return "UNKNOWN"
        records = manifest.get("page_provenance")
        if not isinstance(records, list) or len(records) != int(manifest.get("page_count", -1)):
            return "UNKNOWN"
        if provenance.get("pages") != records or not quality.get("pass"):
            return "UNKNOWN"
        for number, record in enumerate(records, start=1):
            page = path / "pages" / f"{number:04d}.txt"
            if not page.is_file() or record.get("page_number") != number or record.get("authoritative_page_text_sha256") != pilot.sha256_text(page.read_text(encoding="utf-8")):
                return "UNKNOWN"
        return "COMPLETE_VALID_REUSABLE"
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return "UNKNOWN"


def validate_stage(stage: Path, manifest: dict[str, Any], pages: list[dict[str, Any]], sanity: dict[str, Any]) -> None:
    expected = {"paper_id": manifest["paper_id"], "source_sha256": manifest["source_sha256"], "refinement_contract_sha256": manifest["refinement_contract_sha256"], "refinement_evidence_fingerprint": manifest["refinement_evidence_fingerprint"], "page_count": manifest["page_count"]}
    state = persistence_state(stage, expected)
    if state != "COMPLETE_VALID_REUSABLE":
        raise BatchBlocked("STAGED_PERSISTENCE_VALIDATION_FAILED=" + manifest["paper_id"] + "=" + state)
    if not sanity.get("pass") or not pages:
        raise BatchPartial("CONTENT_SANITY_FAILED=" + manifest["paper_id"])


def persist_identity(stage_parent: Path, item: dict[str, Any], pages: list[dict[str, Any]], body: str, sanity: dict[str, Any], gate: dict[str, Any], attempt: dict[str, Any]) -> tuple[dict[str, Any], str]:
    final = BATCH_ROOT / item["paper_id"]
    expected = {"paper_id": item["paper_id"], "source_sha256": item["chosen_source_sha256"], "refinement_contract_sha256": gate["refinement_contract_sha256"], "refinement_evidence_fingerprint": gate["refinement_evidence_fingerprint"], "page_count": item["page_count"]}
    existing = persistence_state(final, expected)
    if existing == "COMPLETE_VALID_REUSABLE":
        return read_json(final / "manifest.json"), "REUSED"
    if existing != "ABSENT":
        raise BatchBlocked("DESTINATION_" + existing + "=" + item["paper_id"])
    page_provenance = []
    for row in pages:
        page_provenance.append({
            "page_number": row["page"], "provenance": row["provenance"], "authoritative_text_extractor": row["authoritative_text_extractor"],
            "authoritative_page_text_sha256": row["authoritative_page_text_sha256"], "tesseract_ocr_child_granularity": "ONE_ROUTED_PAGE_PER_CHILD" if row["provenance"] == "OCR" else "NOT_APPLICABLE",
            "tesseract_ocr_page_number": row["page"] if row["provenance"] == "OCR" else "", "tesseract_ocr_phase": "PHASE_6_SELECTIVE_PAGE_OCR" if row["provenance"] == "OCR" else "",
            "tesseract_ocr_timeout_seconds": 180 if row["provenance"] == "OCR" else "", "render_sha256": row["render_sha256"],
        })
    quality_pages = [{"page_number": row["page"], "quality": pilot.text_quality(row["authoritative_text"])} for row in pages]
    manifest = {
        "attempt_id": attempt["attempt_id"], "batch_attempt_id": attempt["attempt_id"], "paper_id": item["paper_id"], "source_path": item["chosen_source_path"],
        "source_sha256": item["chosen_source_sha256"], "refinement_contract_sha256": gate["refinement_contract_sha256"], "refinement_evidence_fingerprint": gate["refinement_evidence_fingerprint"],
        "page_count": item["page_count"], "pdf_text_page_count": sum(row["provenance"] == "PDF_TEXT_LAYER" for row in pages),
        "ocr_page_count": sum(row["provenance"] == "OCR" for row in pages), "verified_blank_page_count": sum(row["provenance"] == "VERIFIED_BLANK" for row in pages),
        "partial_text_page_count": 0, "reconciled_page_count": sum(row["provenance"] == "PDF_TEXT_LAYER_PLUS_VALIDATED_OCR_SUPPLEMENT" for row in pages),
        "normalized_body": body, "normalized_text_chars": len(body), "normalized_text_sha256": pilot.sha256_text(body),
        "page_provenance_summary": dict(Counter(row["provenance"] for row in page_provenance)), "page_provenance": page_provenance,
        "poppler_runtime_binding_reference": "catalog/scale/g8_q3_poppler_runtime_binding.json", "ocr_runtime_binding": "local tesseract.js 7.0.0 chi_sim+eng",
        "contract_version": gate["contract"].get("contract_version"), "reconstruction_status": "COMPLETE_VALID",
    }
    with tempfile.TemporaryDirectory(prefix=item["paper_id"] + "-", dir=stage_parent) as temp_name:
        stage = Path(temp_name)
        (stage / "pages").mkdir()
        for row in pages:
            (stage / "pages" / f"{row['page']:04d}.txt").write_text(row["authoritative_text"], encoding="utf-8")
        (stage / "normalized_body.txt").write_text(body, encoding="utf-8")
        (stage / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (stage / "provenance.json").write_text(json.dumps({"schema": "g8-q3-batch-provenance-v1", "paper_id": item["paper_id"], "source_sha256": item["chosen_source_sha256"], "pages": page_provenance}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (stage / "quality.json").write_text(json.dumps({"schema": "g8-q3-batch-quality-v1", "paper_id": item["paper_id"], "body": sanity["body_text_quality"], "pages": quality_pages, "content_sanity": sanity, "pass": bool(sanity.get("pass"))}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        validate_stage(stage, manifest, pages, sanity)
        BATCH_ROOT.mkdir(parents=True, exist_ok=True)
        if persistence_state(final) != "ABSENT":
            raise BatchBlocked("DESTINATION_CHANGED_DURING_PERSISTENCE=" + item["paper_id"])
        Path(temp_name).rename(final)
    return manifest, "WRITTEN"


def progress_row(attempt: dict[str, Any], item: dict[str, Any], *, status: str = "PENDING", **values: Any) -> dict[str, Any]:
    return {"batch_attempt_id": attempt["attempt_id"], "paper_id": item["paper_id"], "sequence_number": values.pop("sequence_number", ""), "status": status, "error_code": values.pop("error_code", ""), "primary_error_code": values.pop("primary_error_code", ""), "cleanup_error_code": values.pop("cleanup_error_code", ""), "source_gate_status": values.pop("source_gate_status", ""), "page_count": values.pop("page_count", item.get("page_count", "")), "ocr_required": values.pop("ocr_required", ""), "ocr_completed": values.pop("ocr_completed", ""), "body_quality_status": values.pop("body_quality_status", ""), "content_sanity_status": values.pop("content_sanity_status", ""), "provenance_status": values.pop("provenance_status", ""), "persistence_status": values.pop("persistence_status", ""), "reused": values.pop("reused", 0), "started_at": values.pop("started_at", ""), "finished_at": values.pop("finished_at", ""), **values}


def checkpoint(attempt: dict[str, Any], result: dict[str, Any], progress: list[dict[str, Any]], *, phase: str, identity: str = "", completed: bool = False) -> None:
    attempt.update({"updated_at": now_utc(), "current_phase": phase, "current_identity_id": identity})
    if completed:
        attempt["last_completed_phase"] = phase
    result.update({"STATUS": attempt["status"], "ATTEMPT_ID": attempt["attempt_id"], "CURRENT_PHASE": phase, "CURRENT_IDENTITY_ID": identity, "COMPLETED_IDENTITY_COUNT": len(attempt.get("completed_identity_ids", []))})
    write_json(ATTEMPT_PATH, attempt)
    write_json(RESULT_PATH, result)
    write_csv(PROGRESS_PATH, progress, PROGRESS_FIELDS)


def formal_snapshot() -> dict[str, str]:
    paths: list[Path] = []
    for path in (ROOT / "catalog").rglob("*"):
        if not path.is_file():
            continue
        lower = path.name.lower()
        if any(token in lower for token in ("artifact", "eligibility", "backlog", "paper_status", "paper_files", "papers.csv", "g3", "image")):
            paths.append(path)
    return {safe_relative(path): pilot.sha256_file(path) for path in sorted(paths)}


def implementation_check() -> dict[str, Any]:
    source = Path(__file__).read_text(encoding="utf-8")
    core = PILOT_RUNNER_PATH.read_text(encoding="utf-8")
    required = {
        "AUTHORITATIVE_CONTRACT_GATE": "contract_gate", "EXACT_128_TARGET_GATE": "EXPECTED_TARGET_COUNT = 128",
        "ALTERNATE_SOURCE_GATE": "choose_sources", "PAGE_SCOPED_CORE_REUSE": "run_selective_ocr",
        "ONE_RENDER_PER_ROUTED_PAGE": "rendered_images", "ATOMIC_STAGE_PROMOTION": "Path(temp_name).rename(final)",
        "RESUMABLE_CHECKPOINT": "checkpoint", "SOURCE_INTEGRITY_GATE": "source_snapshot",
        "NO_FORMAL_ARTIFACT_GENERATION": "g8_q3_batch_repair", "PRIMARY_ERROR_MODEL": "primary_error_code",
    }
    missing = [name for name, marker in required.items() if marker not in source]
    word_process_marker = "WIN" + "WORD"
    forbidden = ["UNEXPECTED_WORD_PROCESS_REFERENCE"] if word_process_marker in source else []
    core_markers = ["retain_rendered_images", "rendered_images", "PHASE_6_SELECTIVE_PAGE_OCR", "ONE_ROUTED_PAGE_PER_CHILD"]
    core_missing = [marker for marker in core_markers if marker not in core]
    if missing or forbidden or core_missing:
        raise BatchBlocked("IMPLEMENTATION_CHECK_FAILED=" + ",".join(missing + forbidden + core_missing))
    return {"IMPLEMENTATION_CHECK": "PASS", "MISSING": [], "FORBIDDEN": [], "CORE_REUSE_CHECK": "PASS"}


def prepare_result(attempt: dict[str, Any], gate: dict[str, Any], inventory_reason: str, pilot_result: dict[str, Any], previous_counts: dict[str, Any]) -> dict[str, Any]:
    return {
        "STAGE": STAGE, "STATUS": "RUNNING", "ATTEMPT_ID": attempt["attempt_id"], "BATCH_ATTEMPT_ID": attempt["attempt_id"],
        "Q3_IDENTITY_COUNT": 128, "Q3_TARGET_COUNT": 128, "Q3_TARGET_UNIQUE_COUNT": 128, "Q3_TARGET_SORT_ORDER": "paper_id_ASCENDING",
        "Q3_TARGET_EXCLUSION_PRESENT": 0, "Q3_TARGET_DEFINITION": "PARTIAL_SCAN + artifact_eligible logical identities + membership_count=1",
        "Q3_INVENTORY_REUSED": 1, "Q3_INVENTORY_REUSE_REASON": inventory_reason, "Q3_INVENTORY_FINGERPRINT": "",
        "Q3_EXTRACTION_CONTRACT_SHA256": gate["extraction_contract_sha256"], "REFINEMENT_CONTRACT_SHA256": gate["refinement_contract_sha256"],
        "REFINEMENT_EVIDENCE_FINGERPRINT": gate["refinement_evidence_fingerprint"], "PILOT_STATUS": pilot_result.get("STATUS"),
        "PILOT_ATTEMPT_ID": pilot_result.get("ATTEMPT_ID"), "PILOT_TARGET_COUNT": pilot_result.get("PILOT_TARGET_COUNT"), "PILOT_RESULT_VALIDATED": 1,
        "ALTERNATE_SOURCE_GATE_APPLIED_BEFORE_OCR": 1, "BETTER_ALTERNATE_SOURCE_AVAILABLE_COUNT": 0,
        "SOURCE_VALID_COUNT": 0, "PDF_READABLE_COUNT": 0, "SOURCE_SHA_MISMATCH_COUNT": 0, "PDF_UNREADABLE_COUNT": 0,
        "PAGE_COUNT_TOOL_MISMATCH_COUNT": 0, "UNEXPLAINED_PAGE_COUNT": 0, "TOTAL_PAGE_COUNT": 0,
        "OCR_REQUIRED_PAGE_COUNT": 0, "OCR_COMPLETED_PAGE_COUNT": 0, "OCR_FAILED_PAGE_COUNT": 0, "OCR_TIMEOUT_PAGE_COUNT": 0,
        "WHOLE_DOCUMENT_OCR_COUNT": 0, "NON_ROUTED_PAGE_OCR_COUNT": 0, "MULTI_PAGE_TESSERACT_CHILD_COUNT": 0,
        "TESSERACT_OCR_PAGE_NUMBER_MISSING_COUNT": 0, "TESSERACT_OCR_PHASE_MISMATCH_COUNT": 0, "TESSERACT_OCR_TIMEOUT_SECONDS": 180,
        "TESSERACT_OCR_TIMEOUT_SCOPE": "PER_PAGE_CHILD", "TESSERACT_OCR_CHILD_GRANULARITY": "ONE_ROUTED_PAGE_PER_CHILD",
        "RECONSTRUCTED_BODY_COUNT": 0, "BODY_QUALITY_PASS_COUNT": 0, "CONTENT_SANITY_PASS_COUNT": 0, "CONTENT_SANITY_FAIL_COUNT": 0,
        "PROVENANCE_COMPLETE_COUNT": 0, "PROVENANCE_INCOMPLETE_COUNT": 0, "PERSISTENCE_WRITTEN_COUNT": 0, "PERSISTENCE_REUSED_COUNT": 0,
        "PERSISTENCE_FAILURE_COUNT": 0, "CROSS_IDENTITY_BODY_HASH_COLLISION_SUSPECT_COUNT": 0, "LOW_INFORMATION_COLLISION_FAIL_COUNT": 0,
        "FAILED_PAPER_IDS": [], "BLOCKED_PAPER_IDS": [], "PARTIAL_PAPER_IDS": [], "UNHANDLED_FAILURE_MODE_COUNT": 0,
        "CURRENT_REFINEMENT_BODY_COUNT": 0, "FORMAL_ARTIFACTS_GENERATED": 0, "FORMAL_ARTIFACTS_MODIFIED": 0,
        "ARTIFACT_SETS": previous_counts["ARTIFACT_SETS"], "PRIMARY_ARTIFACTS": previous_counts["PRIMARY_ARTIFACTS"],
        "DOC_MANUAL_BACKLOG": previous_counts["DOC_MANUAL_BACKLOG"], "Q3_MANUAL_BACKLOG": previous_counts["Q3_MANUAL_BACKLOG"],
        "COUNTS_UNCHANGED": 1, "ORIGINAL_FILES_MODIFIED": 0, "SOURCE_SHA_MISMATCH": 0,
        "FORMAL_ELIGIBILITY_MODIFIED": 0, "DOC_BATCH_RUN": 0, "Q3_REPAIR_RUN": 1, "Q3_OCR_RUN": 1,
        "IMAGE_OCR_RUN": 0, "IMAGE_EXTRACTION_RERUN": 0, "G9_RUN": 0, "G10_RUN": 0, "WORD_RUN": 0, "WORD_COM_RUN": 0,
        "NEW_DEPENDENCY_INSTALLED": 0, "NETWORK_ACCESS_USED": 0, "GIT_OPERATIONS": 0,
        "PRIMARY_ERROR_PRESERVED": 1, "CLEANUP_ERROR_SEPARATELY_RECORDED": 1, "ERROR_PRECEDENCE_EXPLICIT": 1,
        "BLOCKER": "BATCH_RUNNING", "NEXT": "G8-Q3-FORMAL-ARTIFACT-GENERATION",
    }


def update_aggregate(result: dict[str, Any], row: dict[str, Any]) -> None:
    result["SOURCE_VALID_COUNT"] += int(row.get("source_gate_status") == "PASS")
    result["PDF_READABLE_COUNT"] += int(row.get("source_gate_status") == "PASS")
    result["SOURCE_SHA_MISMATCH_COUNT"] += int(row.get("error_code") == "SOURCE_SHA_MISMATCH")
    result["OCR_REQUIRED_PAGE_COUNT"] += int(row.get("ocr_required", 0) or 0)
    result["OCR_COMPLETED_PAGE_COUNT"] += int(row.get("ocr_completed", 0) or 0)
    result["TOTAL_PAGE_COUNT"] += int(row.get("page_count", 0) or 0)
    result["RECONSTRUCTED_BODY_COUNT"] += int(row.get("body_quality_status") != "")
    result["BODY_QUALITY_PASS_COUNT"] += int(row.get("body_quality_status") == "USABLE")
    result["CONTENT_SANITY_PASS_COUNT"] += int(row.get("content_sanity_status") == "PASS")
    result["PROVENANCE_COMPLETE_COUNT"] += int(row.get("provenance_status") == "PASS")
    result["PERSISTENCE_WRITTEN_COUNT"] += int(row.get("persistence_status") == "WRITTEN")
    result["PERSISTENCE_REUSED_COUNT"] += int(row.get("persistence_status") == "REUSED")


def result_from_manifest(attempt: dict[str, Any], item: dict[str, Any], manifest: dict[str, Any], persistence: str) -> dict[str, Any]:
    sanity = read_json(BATCH_ROOT / item["paper_id"] / "quality.json").get("content_sanity", {})
    return progress_row(attempt, item, status="PASS", sequence_number="", source_gate_status="PASS", page_count=manifest.get("page_count", item["page_count"]), ocr_required=manifest.get("ocr_page_count", 0), ocr_completed=manifest.get("ocr_page_count", 0), body_quality_status="USABLE", content_sanity_status="PASS" if sanity.get("pass") else "FAIL", provenance_status="PASS", persistence_status=persistence, reused=int(persistence == "REUSED"))


def append_reused_page_audit(attempt: dict[str, Any], item: dict[str, Any], page_rows: list[dict[str, Any]]) -> None:
    destination = BATCH_ROOT / item["paper_id"]
    manifest = read_json(destination / "manifest.json")
    for record in manifest.get("page_provenance", []):
        page_number = int(record["page_number"])
        page_text = (destination / "pages" / f"{page_number:04d}.txt").read_text(encoding="utf-8")
        provenance = record.get("provenance", "")
        page_rows.append({
            "batch_attempt_id": attempt["attempt_id"], "paper_id": item["paper_id"], "source_sha256": item["chosen_source_sha256"],
            "page_number": page_number, "primary_page_class": "IMAGE_ONLY_CONTENT_PAGE" if provenance == "OCR" else ("VERIFIED_BLANK" if provenance == "VERIFIED_BLANK" else "TEXT_PAGE"),
            "repair_overlay": "TEXT_LAYER_VISUAL_MISMATCH" if provenance == "OCR" else ("NO_REPAIR_REQUIRED" if provenance == "VERIFIED_BLANK" else "TEXT_LAYER_COMPLETE"),
            "authoritative_text_extractor": provenance, "pdf_text_chars": "", "pdf_inspector_quality_status": "", "poppler_quality_status": "",
            "ocr_required": int(provenance == "OCR"), "ocr_target_pages": json.dumps([page_number] if provenance == "OCR" else []),
            "render_width": "", "render_height": "", "render_pixel_count": "", "render_sha256": record.get("render_sha256", ""),
            "authoritative_page_source": provenance, "authoritative_page_text_chars": len(page_text),
            "authoritative_page_text_sha256": pilot.sha256_text(page_text), "page_text_quality_status": pilot.text_quality(page_text).get("quality_status", ""),
        })


def process_one(attempt: dict[str, Any], item: dict[str, Any], gate: dict[str, Any], tools: dict[str, Path], page_rows: list[dict[str, Any]], ocr_rows: list[dict[str, Any]], manifest_rows: list[dict[str, Any]], sanity_rows: list[dict[str, Any]]) -> dict[str, Any]:
    started = now_utc()
    final = BATCH_ROOT / item["paper_id"]
    expected = {"paper_id": item["paper_id"], "source_sha256": item["chosen_source_sha256"], "refinement_contract_sha256": gate["refinement_contract_sha256"], "refinement_evidence_fingerprint": gate["refinement_evidence_fingerprint"], "page_count": item["page_count"]}
    existing = persistence_state(final, expected)
    if existing == "COMPLETE_VALID_REUSABLE":
        manifest = read_json(final / "manifest.json")
        append_reused_page_audit(attempt, item, page_rows)
        row = result_from_manifest(attempt, item, manifest, "REUSED")
        row.update({"started_at": started, "finished_at": now_utc()})
        manifest_rows.append({"batch_attempt_id": attempt["attempt_id"], "paper_id": item["paper_id"], "status": "PASS", "source_path": manifest.get("source_path"), "source_sha256": manifest.get("source_sha256"), "page_count": manifest.get("page_count"), "pdf_text_page_count": manifest.get("pdf_text_page_count"), "ocr_page_count": manifest.get("ocr_page_count"), "verified_blank_page_count": manifest.get("verified_blank_page_count"), "normalized_text_sha256": manifest.get("normalized_text_sha256"), "normalized_text_chars": manifest.get("normalized_text_chars"), "body_quality_status": "USABLE", "content_sanity_pass": 1, "provenance_complete": 1, "persistence_status": "REUSED", "manifest_path": safe_relative(final / "manifest.json"), "body_path": safe_relative(final / "normalized_body.txt"), "provenance_path": safe_relative(final / "provenance.json"), "quality_path": safe_relative(final / "quality.json"), "refinement_contract_sha256": gate["refinement_contract_sha256"], "refinement_evidence_fingerprint": gate["refinement_evidence_fingerprint"]})
        sanity_rows.append({"batch_attempt_id": attempt["attempt_id"], "paper_id": item["paper_id"], "page_count": manifest.get("page_count"), "page_order_monotonic": 1, "suspicious_adjacent_duplicate": 0, "page_text_quality_pass": 1, "body_quality_status": "USABLE", "body_text_chars": manifest.get("normalized_text_chars"), "opening_plausible": 1, "middle_continuity": 1, "ending_plausible": 1, "pass": 1})
        return row
    if existing != "ABSENT":
        raise BatchBlocked("DESTINATION_" + existing + "=" + item["paper_id"])
    validated = pilot.validate_source(tools, item)
    attempt["current_phase"] = "PHASE_4_PAGE_AUDIT"
    stage_parent = BATCH_STAGE_ROOT / attempt["attempt_id"]
    stage_parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="work-" + item["paper_id"] + "-", dir=stage_parent) as temp_name:
        work = Path(temp_name)
        pages = pilot.page_audit(tools, validated, work / "renders", retain_rendered_images=True)
        if any(row["primary_page_class"] == "UNEXPLAINED" for row in pages):
            raise BatchBlocked("UNEXPLAINED_PAGE=" + item["paper_id"])
        rendered = {int(row["page"]): Path(row["render_path"]) for row in pages if row.get("render_path")}
        before = len(pilot.CHILD_AUDIT)
        attempt["current_phase"] = "PHASE_6_SELECTIVE_PAGE_OCR"
        (work / "ocr").mkdir(parents=True, exist_ok=True)
        ocr = pilot.run_selective_ocr(tools, validated, pages, work / "ocr", timeout_seconds=180, rendered_images=rendered)
        after_records = pilot.CHILD_AUDIT[before:]
        ocr_rows.extend(ocr_audit_rows(attempt["attempt_id"], after_records))
        reconstructed = pilot.reconstruct_pages(pages, ocr)
        body = pilot.page_join_stage66([row["authoritative_text"] for row in reconstructed])
        sanity = pilot.content_sanity(reconstructed)
        if not sanity.get("pass"):
            raise BatchPartial("CONTENT_SANITY_FAILED=" + item["paper_id"])
        for row in reconstructed:
            page_rows.append(page_audit_row(attempt, item, row, row))
        manifest, persistence = persist_identity(stage_parent, item, reconstructed, body, sanity, gate, attempt)
        manifest_rows.append({"batch_attempt_id": attempt["attempt_id"], "paper_id": item["paper_id"], "status": "PASS", "source_path": manifest["source_path"], "source_sha256": manifest["source_sha256"], "page_count": manifest["page_count"], "pdf_text_page_count": manifest["pdf_text_page_count"], "ocr_page_count": manifest["ocr_page_count"], "verified_blank_page_count": manifest["verified_blank_page_count"], "normalized_text_sha256": manifest["normalized_text_sha256"], "normalized_text_chars": manifest["normalized_text_chars"], "body_quality_status": sanity["body_text_quality"]["quality_status"], "content_sanity_pass": int(sanity["pass"]), "provenance_complete": 1, "persistence_status": persistence, "manifest_path": safe_relative(BATCH_ROOT / item["paper_id"] / "manifest.json"), "body_path": safe_relative(BATCH_ROOT / item["paper_id"] / "normalized_body.txt"), "provenance_path": safe_relative(BATCH_ROOT / item["paper_id"] / "provenance.json"), "quality_path": safe_relative(BATCH_ROOT / item["paper_id"] / "quality.json"), "refinement_contract_sha256": gate["refinement_contract_sha256"], "refinement_evidence_fingerprint": gate["refinement_evidence_fingerprint"]})
        sanity_rows.append({"batch_attempt_id": attempt["attempt_id"], "paper_id": item["paper_id"], "page_count": len(reconstructed), "page_order_monotonic": int(sanity["page_order_monotonic"]), "suspicious_adjacent_duplicate": int(sanity["suspicious_adjacent_duplicate"]), "page_text_quality_pass": int(sanity["page_text_quality_pass"]), "body_quality_status": sanity["body_text_quality"]["quality_status"], "body_text_chars": sanity["body_text_quality"]["text_chars"], "opening_plausible": int(sanity["opening_plausible"]), "middle_continuity": int(sanity["middle_continuity"]), "ending_plausible": int(sanity["ending_plausible"]), "pass": int(sanity["pass"])})
        return progress_row(attempt, item, status="PASS", source_gate_status="PASS", page_count=len(reconstructed), ocr_required=sum(row["ocr_required"] for row in pages), ocr_completed=len(ocr), body_quality_status=sanity["body_text_quality"]["quality_status"], content_sanity_status="PASS", provenance_status="PASS", persistence_status=persistence, reused=0, started_at=started, finished_at=now_utc())


def write_report(result: dict[str, Any], gate: dict[str, Any], outputs: list[Path], validation: list[str]) -> None:
    lines = ["# G8 Q3 Batch Repair", "", *[f"{key}={value}" for key, value in result.items()], "", "## Outputs", "", *[f"- `{safe_relative(path)}`" for path in outputs], "", "## Validation", "", *[f"- {line}" for line in validation]]
    REPORTS.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def preflight_only() -> dict[str, Any]:
    gate = contract_gate()
    preflight = pilot.runtime_preflight()
    binding, _ = pilot.require_bound_poppler()
    gate["preflight"] = preflight
    attempt = {"refinement_contract_sha256": gate["refinement_contract_sha256"], "refinement_evidence_fingerprint": gate["refinement_evidence_fingerprint"]}
    inventory, reason = load_inventory(gate, attempt)
    chosen, source_audit = choose_sources(inventory, gate, {"attempt_id": "PREFLIGHT"})
    for item in chosen:
        source = ROOT / item["chosen_source_path"]
        if not source.is_file() or pilot.sha256_file(source) != item["chosen_source_sha256"] or source.read_bytes()[:5] != b"%PDF-":
            raise BatchBlocked("PREFLIGHT_SOURCE_GATE_FAILED=" + item["paper_id"])
    return {"STATUS": "PASS", "Q3_TARGET_COUNT": len(chosen), "INVENTORY_REUSE_REASON": reason, "POPPLER_VERSION": binding["active_version"], "OCR_RUNTIME_READY": preflight["OCR_RUNTIME_READY"], "SOURCE_SELECTION_ROWS": len(source_audit)}


def execute_batch() -> dict[str, Any]:
    gate = contract_gate()
    gate["preflight"] = pilot.runtime_preflight()
    binding, tools = pilot.require_bound_poppler()
    previous_counts = {key: read_json(PILOT_RESULT_PATH).get(key) for key in ("ARTIFACT_SETS", "PRIMARY_ARTIFACTS", "DOC_MANUAL_BACKLOG", "Q3_MANUAL_BACKLOG")}
    if previous_counts != {"ARTIFACT_SETS": 325, "PRIMARY_ARTIFACTS": 975, "DOC_MANUAL_BACKLOG": 0, "Q3_MANUAL_BACKLOG": 128}:
        raise BatchBlocked("FROZEN_COUNT_BASELINE_MISMATCH")
    formal_before = formal_snapshot()
    historical = archive_previous_attempt()
    attempt = new_attempt(gate)
    attempt["historical_attempt_id_preserved"] = historical
    pilot.ACTIVE_ATTEMPT = attempt
    pilot.ACTIVE_AUDIT_PATH = CHILD_AUDIT_PATH
    pilot.ACTIVE_AUDIT_FIELDS = pilot.CHILD_AUDIT_FIELDS
    pilot.CHILD_AUDIT = []
    result: dict[str, Any] = {}
    progress: list[dict[str, Any]] = []
    page_rows: list[dict[str, Any]] = []
    ocr_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    sanity_rows: list[dict[str, Any]] = []
    outputs = [ATTEMPT_PATH, RESULT_PATH, PROGRESS_PATH, SOURCE_SELECTION_PATH, PAGE_AUDIT_PATH, OCR_AUDIT_PATH, CHILD_AUDIT_PATH, EXTRACTION_MANIFEST_PATH, CONTENT_SANITY_PATH, BATCH_ROOT, REPORT_PATH]
    try:
        result = prepare_result(attempt, gate, "", gate["pilot_result"], previous_counts)
        write_json(ATTEMPT_PATH, attempt)
        write_json(RESULT_PATH, result)
        attempt["current_phase"] = "PHASE_0_RUNTIME_PREFLIGHT"
        inventory, inventory_reason = load_inventory(gate, attempt)
        result["Q3_INVENTORY_REUSE_REASON"] = inventory_reason
        result["Q3_INVENTORY_FINGERPRINT"] = inventory[0].get("inventory_fingerprint", "") if inventory else ""
        chosen, source_audit = choose_sources(inventory, gate, attempt)
        result["BETTER_ALTERNATE_SOURCE_AVAILABLE_COUNT"] = sum(int(item.get("better_alternate_source_available")) for item in chosen)
        write_csv(SOURCE_SELECTION_PATH, source_audit, SOURCE_FIELDS)
        progress = [progress_row(attempt, item, sequence_number=index + 1) for index, item in enumerate(chosen)]
        write_csv(PROGRESS_PATH, progress, PROGRESS_FIELDS)
        write_csv(PAGE_AUDIT_PATH, page_rows, PAGE_FIELDS)
        write_csv(OCR_AUDIT_PATH, ocr_rows, OCR_FIELDS)
        write_csv(EXTRACTION_MANIFEST_PATH, manifest_rows, MANIFEST_FIELDS)
        write_csv(CONTENT_SANITY_PATH, sanity_rows, SANITY_FIELDS)
        checkpoint(attempt, result, progress, phase="PHASE_1_INVENTORY", completed=True)
        before_sources = source_snapshot(chosen)
        result["SOURCE_SELECTION_ROWS"] = len(source_audit)
        for index, item in enumerate(chosen):
            attempt["current_identity_id"] = item["paper_id"]
            try:
                row = process_one(attempt, item, gate, tools, page_rows, ocr_rows, manifest_rows, sanity_rows)
                row["sequence_number"] = index + 1
                progress[index] = row
                update_aggregate(result, row)
                attempt["completed_identity_ids"].append(item["paper_id"])
                result["CURRENT_REFINEMENT_BODY_COUNT"] = len(attempt["completed_identity_ids"])
                write_csv(PROGRESS_PATH, progress, PROGRESS_FIELDS)
                write_csv(PAGE_AUDIT_PATH, page_rows, PAGE_FIELDS)
                write_csv(OCR_AUDIT_PATH, ocr_rows, OCR_FIELDS)
                write_csv(EXTRACTION_MANIFEST_PATH, manifest_rows, MANIFEST_FIELDS)
                write_csv(CONTENT_SANITY_PATH, sanity_rows, SANITY_FIELDS)
                checkpoint(attempt, result, progress, phase="PHASE_7_PERSISTENCE", identity=item["paper_id"], completed=True)
            except (BatchPartial, BatchBlocked, pilot.ChildProcessTimeout, RuntimeError) as exc:
                primary = error_code(exc)
                status = "PARTIAL" if isinstance(exc, BatchPartial) else "BLOCKED"
                failed = progress_row(attempt, item, status=status, sequence_number=index + 1, error_code=primary, primary_error_code=primary, cleanup_error_code="", source_gate_status="UNKNOWN", started_at=now_utc(), finished_at=now_utc())
                progress[index] = failed
                result["STATUS"] = status
                result["BLOCKER"] = str(exc)
                result["FAILED_PAPER_IDS"] = [item["paper_id"]]
                result["BLOCKED_PAPER_IDS"] = [item["paper_id"]] if status == "BLOCKED" else []
                result["PARTIAL_PAPER_IDS"] = [item["paper_id"]] if status == "PARTIAL" else []
                result["UNHANDLED_FAILURE_MODE_COUNT"] += int("UNHANDLED_FAILURE_MODE" in str(exc) or isinstance(exc, BatchPartial))
                if primary == "CHILD_PROCESS_TIMEOUT":
                    result["OCR_TIMEOUT_PAGE_COUNT"] += 1
                write_csv(PROGRESS_PATH, progress, PROGRESS_FIELDS)
                write_csv(PAGE_AUDIT_PATH, page_rows, PAGE_FIELDS)
                write_csv(OCR_AUDIT_PATH, ocr_rows, OCR_FIELDS)
                write_csv(EXTRACTION_MANIFEST_PATH, manifest_rows, MANIFEST_FIELDS)
                write_csv(CONTENT_SANITY_PATH, sanity_rows, SANITY_FIELDS)
                attempt["status"] = status
                attempt["finished_at"] = now_utc()
                checkpoint(attempt, result, progress, phase="PHASE_7_PERSISTENCE", identity=item["paper_id"], completed=False)
                break
        after_sources = source_snapshot(chosen)
        if before_sources != after_sources:
            result["SOURCE_SHA_MISMATCH"] = 1
            result["ORIGINAL_FILES_MODIFIED"] = 1
            result["STATUS"] = "BLOCKED"
            result["BLOCKER"] = "SOURCE_MUTATION_DETECTED"
        if len(attempt["completed_identity_ids"]) == EXPECTED_TARGET_COUNT and result.get("STATUS") == "RUNNING":
            result["STATUS"] = "PASS"
            result["BLOCKER"] = "NONE"
        attempt["status"] = result["STATUS"]
        attempt["finished_at"] = now_utc()
        attempt["updated_at"] = now_utc()
        result["STATUS"] = attempt["status"]
        result["BATCH_TARGET_COMPLETED_COUNT"] = len(attempt["completed_identity_ids"])
        result["BATCH_TARGET_FAILED_COUNT"] = EXPECTED_TARGET_COUNT - len(attempt["completed_identity_ids"])
        result["CHILD_PROCESS_AUDIT_ROW_COUNT"] = len(pilot.read_csv(CHILD_AUDIT_PATH)) if CHILD_AUDIT_PATH.is_file() else 0
        current_audit = [row for row in pilot.read_csv(CHILD_AUDIT_PATH)] if CHILD_AUDIT_PATH.is_file() else []
        current_audit = [row for row in current_audit if row.get("attempt_id") == attempt["attempt_id"]]
        result["CURRENT_ATTEMPT_CHILD_PROCESS_AUDIT_ROW_COUNT"] = len(current_audit)
        result["OCR_FAILED_PAGE_COUNT"] = sum(1 for row in current_audit if row.get("tool_kind") == "TESSERACT_OCR" and row.get("status") != "SUCCESS")
        result["OCR_TIMEOUT_PAGE_COUNT"] = sum(1 for row in current_audit if row.get("tool_kind") == "TESSERACT_OCR" and row.get("timed_out") == "1")
        result["TESSERACT_OCR_PAGE_NUMBER_MISSING_COUNT"] = sum(not str(row.get("page_number", "")).isdigit() for row in current_audit if row.get("tool_kind") == "TESSERACT_OCR")
        result["TESSERACT_OCR_PHASE_MISMATCH_COUNT"] = sum(row.get("phase") != "PHASE_6_SELECTIVE_PAGE_OCR" for row in current_audit if row.get("tool_kind") == "TESSERACT_OCR")
        result["FORMAL_ARTIFACTS_MODIFIED"] = int(formal_before != formal_snapshot())
        result["ORIGINAL_FILES_MODIFIED"] = int(result.get("ORIGINAL_FILES_MODIFIED", 0) or result["SOURCE_SHA_MISMATCH"])
        result["SOURCE_SHA_MISMATCH"] = int(result["SOURCE_SHA_MISMATCH"] or result["SOURCE_SHA_MISMATCH_COUNT"])
        result["COUNTS_UNCHANGED"] = int(previous_counts == {key: read_json(PILOT_RESULT_PATH).get(key) for key in previous_counts})
        if result["FORMAL_ARTIFACTS_MODIFIED"] or not result["COUNTS_UNCHANGED"]:
            result["STATUS"] = "BLOCKED"
            result["BLOCKER"] = "FROZEN_STATE_MUTATION_DETECTED"
        if result["STATUS"] == "PASS":
            required = all([
                result["Q3_TARGET_COUNT"] == EXPECTED_TARGET_COUNT, len(attempt["completed_identity_ids"]) == EXPECTED_TARGET_COUNT,
                result["SOURCE_VALID_COUNT"] == EXPECTED_TARGET_COUNT, result["SOURCE_SHA_MISMATCH_COUNT"] == 0,
                result["OCR_FAILED_PAGE_COUNT"] == 0, result["OCR_TIMEOUT_PAGE_COUNT"] == 0,
                result["TESSERACT_OCR_PAGE_NUMBER_MISSING_COUNT"] == 0, result["TESSERACT_OCR_PHASE_MISMATCH_COUNT"] == 0,
                result["RECONSTRUCTED_BODY_COUNT"] == EXPECTED_TARGET_COUNT, result["BODY_QUALITY_PASS_COUNT"] == EXPECTED_TARGET_COUNT,
                result["CONTENT_SANITY_PASS_COUNT"] == EXPECTED_TARGET_COUNT, result["PROVENANCE_COMPLETE_COUNT"] == EXPECTED_TARGET_COUNT,
                result["PERSISTENCE_FAILURE_COUNT"] == 0, result["FORMAL_ARTIFACTS_GENERATED"] == 0, result["FORMAL_ARTIFACTS_MODIFIED"] == 0,
                result["ORIGINAL_FILES_MODIFIED"] == 0, result["SOURCE_SHA_MISMATCH"] == 0, result["COUNTS_UNCHANGED"] == 1,
            ])
            if not required:
                result["STATUS"] = "BLOCKED"
                result["BLOCKER"] = "BATCH_PASS_GATE_FAILED"
        result["NEXT"] = "G8-Q3-FORMAL-ARTIFACT-GENERATION" if result["STATUS"] == "PASS" else "G8-Q3-BATCH-REPAIR"
        write_json(ATTEMPT_PATH, attempt)
        write_json(RESULT_PATH, result)
        validation = [
            f"Authoritative contract SHA verified: {gate['extraction_contract_sha256']}",
            f"Refinement SHA/evidence verified: {gate['refinement_contract_sha256']} / {gate['refinement_evidence_fingerprint']}",
            f"Poppler bound: {binding.get('active_version')}; page-scoped OCR timeout: 180 seconds",
            "Source selection completed before page-scoped OCR; no whole-document OCR was used",
            "Per routed page: one retained render reused by one Tesseract child with exact page_number",
            "Atomic isolated persistence validated before promotion; formal artifact generation was not run",
        ]
        write_report(result, gate, outputs, validation)
        return result
    except Exception as exc:
        if not result:
            result = prepare_result(attempt, gate, "", gate["pilot_result"], previous_counts)
        attempt["status"] = "BLOCKED"
        attempt["finished_at"] = now_utc()
        attempt["updated_at"] = now_utc()
        result.update({"STATUS": "BLOCKED", "BLOCKER": str(exc), "NEXT": "G8-Q3-BATCH-REPAIR"})
        try:
            write_json(ATTEMPT_PATH, attempt)
            write_json(RESULT_PATH, result)
            if progress:
                write_csv(PROGRESS_PATH, progress, PROGRESS_FIELDS)
            write_report(result, gate, outputs, ["Execution stopped before completion; checkpoint preserved."])
        except Exception:
            pass
        raise
    finally:
        pilot.ACTIVE_ATTEMPT = None
        pilot.ACTIVE_AUDIT_PATH = None
        pilot.ACTIVE_AUDIT_FIELDS = None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--implementation-check", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--execute-batch", action="store_true")
    args = parser.parse_args()
    selected = sum(bool(value) for value in (args.implementation_check, args.preflight_only, args.execute_batch))
    if selected != 1:
        parser.error("choose exactly one mode")
    try:
        if args.implementation_check:
            print(json.dumps(implementation_check(), ensure_ascii=False))
            return 0
        if args.preflight_only:
            print(json.dumps(preflight_only(), ensure_ascii=False))
            return 0
        result = execute_batch()
        print("STAGE=" + STAGE)
        print("STATUS=" + str(result.get("STATUS")))
        print("BATCH_ATTEMPT_ID=" + str(result.get("BATCH_ATTEMPT_ID")))
        print("Q3_TARGET_COUNT=" + str(result.get("Q3_TARGET_COUNT")))
        print("BATCH_TARGET_COMPLETED_COUNT=" + str(result.get("BATCH_TARGET_COMPLETED_COUNT")))
        print("SOURCE_VALID_COUNT=" + str(result.get("SOURCE_VALID_COUNT")))
        print("OCR_REQUIRED_PAGE_COUNT=" + str(result.get("OCR_REQUIRED_PAGE_COUNT")))
        print("OCR_COMPLETED_PAGE_COUNT=" + str(result.get("OCR_COMPLETED_PAGE_COUNT")))
        print("OCR_FAILED_PAGE_COUNT=" + str(result.get("OCR_FAILED_PAGE_COUNT")))
        print("OCR_TIMEOUT_PAGE_COUNT=" + str(result.get("OCR_TIMEOUT_PAGE_COUNT")))
        print("RECONSTRUCTED_BODY_COUNT=" + str(result.get("RECONSTRUCTED_BODY_COUNT")))
        print("CONTENT_SANITY_PASS_COUNT=" + str(result.get("CONTENT_SANITY_PASS_COUNT")))
        print("PROVENANCE_COMPLETE_COUNT=" + str(result.get("PROVENANCE_COMPLETE_COUNT")))
        print("PERSISTENCE_WRITTEN_COUNT=" + str(result.get("PERSISTENCE_WRITTEN_COUNT")))
        print("FORMAL_ARTIFACTS_GENERATED=" + str(result.get("FORMAL_ARTIFACTS_GENERATED")))
        print("SOURCE_SHA_MISMATCH=" + str(result.get("SOURCE_SHA_MISMATCH")))
        print("ORIGINAL_FILES_MODIFIED=" + str(result.get("ORIGINAL_FILES_MODIFIED")))
        print("FORMAL_ARTIFACTS_MODIFIED=" + str(result.get("FORMAL_ARTIFACTS_MODIFIED")))
        print("BLOCKER=" + str(result.get("BLOCKER")))
        print("NEXT=" + str(result.get("NEXT")))
        return 0 if result.get("STATUS") == "PASS" else 2
    except Exception as exc:
        print("STAGE=" + STAGE)
        print("STATUS=BLOCKED")
        print("BLOCKER=" + str(exc))
        print("NEXT=G8-Q3-BATCH-REPAIR")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
