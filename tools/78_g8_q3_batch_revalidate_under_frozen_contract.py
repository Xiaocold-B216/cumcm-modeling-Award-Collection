"""Revalidate the persisted G8 Q3 batch under the frozen contract.

The default mode is read-only preflight.  Only ``--execute`` may atomically
update the persistence manifest binding, and it does so only after every
identity has passed the complete persisted-evidence validation.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import os
import re
import tempfile
import time
import uuid
from collections import defaultdict
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
PERSISTENCE_ROOT = SCALE / "g8_q3_batch_repair"
TARGET_MANIFEST_PATH = SCALE / "g8_q3_batch_extraction_manifest.csv"
PAGE_AUDIT_PATH = SCALE / "g8_q3_batch_page_audit.csv"
OCR_AUDIT_PATH = SCALE / "g8_q3_batch_ocr_audit.csv"
SOURCE_SELECTION_PATH = SCALE / "g8_q3_batch_source_selection.csv"
REFINEMENT_PATH = SCALE / "g8_q3_contract_refinement_v1.json"
EXTRACTION_PATH = SCALE / "g8_q3_extraction_contract_v1.json"
REFINEMENT_RESULT_PATH = SCALE / "g8_q3_binary_matrix_sanity_refinement_result.json"
BATCH_RESULT_PATH = SCALE / "g8_q3_batch_repair_result.json"
RESULT_PATH = SCALE / "g8_q3_batch_revalidation_result.json"
ATTEMPT_PATH = SCALE / "g8_q3_batch_revalidation_attempt.json"
PROGRESS_PATH = SCALE / "g8_q3_batch_revalidation_progress.csv"
DETAIL_PATH = SCALE / "g8_q3_batch_revalidation_detail.csv"
SANITY_AUDIT_PATH = SCALE / "g8_q3_batch_sanity_change_audit.csv"
REPORT_PATH = REPORTS / "G8_Q3_BATCH_REVALIDATION_UNDER_FROZEN_CONTRACT.md"
PILOT_PATH = ROOT / "tools" / "72_g8_q3_contract_pilot_resume.py"

STAGE = "G8-Q3-BATCH-REVALIDATE-UNDER-FROZEN-CONTRACT"
SOURCE_BATCH_ATTEMPT_ID = "20260902T181812821882_f3ed3664"
EXPECTED_REFINEMENT_SHA = "7E43620CE1A7A22EB08B48D4552E2751E13BE00EB9F71681CDBB76F8A00624A7"
EXPECTED_REFINEMENT_EVIDENCE = "8DED4A5815D9A5D6644E0194282E07AF6FBC02CE68B6AEE6568601131ADC2E99"
EXPECTED_Q3_SHA = "4E372E0BFF1D5395C46CFFA583636190AEDB3389FDFFCF354559626757AC3A6F"
OLD_REFINEMENT_SHA = "1D8BE5FE247FFF54DD3147B493820AB92C1BFEE211DB6FE8E21D59C64E4F1F2C"
OLD_REFINEMENT_EVIDENCE = "5FA095687812D8FB58CE9F61DCAE88F0B096FDBC2219326A8C77571C3311C70E"
EXPECTED_TARGET_COUNT = 128
EXPECTED_PAGE_COUNT = 2120
EXPECTED_OCR_PAGE_COUNT = 2090
EXPECTED_BLANK_PAGE_COUNT = 30
ATOMIC_REPLACE_RETRIES = 3
ATOMIC_REPLACE_DELAY_SECONDS = 0.25

PROGRESS_FIELDS = [
    "paper_id", "sequence_number", "status", "error_code", "source_sha_status",
    "page_integrity_status", "page_quality_status", "body_hash_status",
    "body_quality_status", "content_sanity_status", "collision_status",
    "provenance_status", "persistence_structure_status", "contract_binding_status",
    "page_count", "ocr_page_count", "blank_page_count", "old_binding_state",
    "started_at", "finished_at",
]
DETAIL_FIELDS = [
    "paper_id", "page_number", "source_sha_status", "page_hash_status",
    "authoritative_page_hash_status", "page_provenance_status", "page_classification_status",
    "page_quality_status", "ocr_provenance_status", "old_sanity_status",
    "new_sanity_status", "binary_matrix_pass", "rule_id", "sanity_status_changed",
    "reason", "render_evidence_status",
]
SANITY_FIELDS = [
    "paper_id", "page_number", "old_sanity_status", "new_sanity_status",
    "rule_id", "binary_matrix_pass", "changed", "reason",
]


def load_pilot() -> Any:
    spec = importlib.util.spec_from_file_location("g8_q3_pilot_core_revalidation", PILOT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("PILOT_CORE_IMPORT_FAILED")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pilot = load_pilot()


class RevalidationFailure(RuntimeError):
    def __init__(self, code: str, message: str = "") -> None:
        super().__init__(message or code)
        self.code = code


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def new_attempt_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f") + "_" + uuid.uuid4().hex[:8]


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest().upper()


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError) as error:
        raise RevalidationFailure("PERSISTENCE_CORRUPTION", f"{path}: {error}") from error


def read_csv(path: Path) -> list[dict[str, str]]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            return list(csv.DictReader(stream))
    except OSError as error:
        raise RevalidationFailure("EVIDENCE_MISSING", f"{path}: {error}") from error


def atomic_write_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp-" + uuid.uuid4().hex)
    try:
        with temporary.open("wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        last_error: OSError | None = None
        for attempt in range(ATOMIC_REPLACE_RETRIES):
            try:
                os.replace(temporary, path)
                return
            except PermissionError as error:
                last_error = error
                if attempt + 1 < ATOMIC_REPLACE_RETRIES:
                    time.sleep(ATOMIC_REPLACE_DELAY_SECONDS * (attempt + 1))
        raise RevalidationFailure("ATOMIC_BINDING_UPDATE_FAILURE", f"{path}: {last_error}")
    finally:
        if temporary.exists():
            temporary.unlink()


def atomic_write_json(path: Path, value: Any) -> None:
    atomic_write_bytes(path, (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


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
        for attempt in range(ATOMIC_REPLACE_RETRIES):
            try:
                os.replace(temporary, path)
                return
            except PermissionError as error:
                if attempt + 1 == ATOMIC_REPLACE_RETRIES:
                    raise RevalidationFailure("ATOMIC_OUTPUT_UPDATE_FAILURE", f"{path}: {error}") from error
                time.sleep(ATOMIC_REPLACE_DELAY_SECONDS * (attempt + 1))
    finally:
        if temporary.exists():
            temporary.unlink()


def legacy_sanity(text: str) -> bool:
    encoded = text.encode("utf-8", errors="replace")
    replacement = text.count("\ufffd") / max(1, len(text))
    control = sum(ord(char) < 32 and char not in "\n\r\t" for char in text) / max(1, len(text))
    visible = sum(char.isalnum() or "\u4e00" <= char <= "\u9fff" for char in text) / max(1, len(text.strip()))
    repeated = bool(re.search(r"([^\s\W_])\1{19,}", text))
    return bool(encoded and text.strip() and replacement <= 0.02 and control <= 0.02 and visible >= 0.15 and not repeated)


def contract_gate() -> dict[str, Any]:
    refinement_sha = pilot.sha256_file(REFINEMENT_PATH)
    if refinement_sha != EXPECTED_REFINEMENT_SHA:
        raise RevalidationFailure("REFINEMENT_FINGERPRINT_DRIFT", refinement_sha)
    actual_evidence = pilot.refinement_fingerprint()[1]
    if actual_evidence != EXPECTED_REFINEMENT_EVIDENCE:
        raise RevalidationFailure("REFINEMENT_FINGERPRINT_DRIFT", actual_evidence)
    q3_sha = pilot.sha256_file(EXTRACTION_PATH)
    if q3_sha != EXPECTED_Q3_SHA:
        raise RevalidationFailure("Q3_EXTRACTION_CONTRACT_DRIFT", q3_sha)
    extraction = read_json(EXTRACTION_PATH)
    refinement = read_json(REFINEMENT_PATH)
    if extraction.get("refinement_contract_sha256") != refinement_sha or extraction.get("refinement_evidence_fingerprint") != actual_evidence:
        raise RevalidationFailure("Q3_EXTRACTION_CONTRACT_DRIFT", "refinement binding mismatch")
    if extraction.get("binary_matrix_sanity_rule") != refinement.get("binary_matrix_sanity_rule"):
        raise RevalidationFailure("Q3_EXTRACTION_CONTRACT_DRIFT", "binary matrix rule mismatch")
    refinement_result = read_json(REFINEMENT_RESULT_PATH)
    if refinement_result.get("STATUS") != "PASS" or refinement_result.get("REFINEMENT_CONTRACT_SHA256") != refinement_sha or refinement_result.get("REFINEMENT_EVIDENCE_FINGERPRINT") != actual_evidence or refinement_result.get("Q3_EXTRACTION_CONTRACT_SHA256") != q3_sha:
        raise RevalidationFailure("REFINEMENT_EVIDENCE_BINDING_INVALID")
    batch_result = read_json(BATCH_RESULT_PATH)
    if batch_result.get("ATTEMPT_ID") != SOURCE_BATCH_ATTEMPT_ID or batch_result.get("STATUS") != "PASS":
        raise RevalidationFailure("SOURCE_BATCH_EVIDENCE_BINDING_INVALID")
    return {"refinement_sha": refinement_sha, "refinement_evidence": actual_evidence, "q3_sha": q3_sha, "refinement": refinement, "extraction": extraction, "batch_result": batch_result}


def load_target_rows() -> list[dict[str, Any]]:
    rows = [row for row in read_csv(TARGET_MANIFEST_PATH) if row.get("status") == "PASS"]
    ids = [row.get("paper_id", "") for row in rows]
    if len(rows) != EXPECTED_TARGET_COUNT or len(set(ids)) != EXPECTED_TARGET_COUNT:
        raise RevalidationFailure("BATCH_PERSISTENCE_TARGET_SET_DRIFT", f"target_count={len(rows)} unique={len(set(ids))}")
    return sorted(rows, key=lambda row: row["paper_id"])


def load_page_audit() -> dict[str, dict[int, dict[str, str]]]:
    grouped: dict[str, dict[int, dict[str, str]]] = defaultdict(dict)
    for row in read_csv(PAGE_AUDIT_PATH):
        if row.get("batch_attempt_id") != SOURCE_BATCH_ATTEMPT_ID:
            raise RevalidationFailure("SOURCE_BATCH_EVIDENCE_BINDING_INVALID", "page audit attempt drift")
        paper_id = row.get("paper_id", "")
        try:
            number = int(row.get("page_number", ""))
        except ValueError as error:
            raise RevalidationFailure("PAGE_PERSISTENCE_INTEGRITY_FAILURE", f"invalid page number for {paper_id}") from error
        if number in grouped[paper_id]:
            raise RevalidationFailure("PAGE_PERSISTENCE_INTEGRITY_FAILURE", f"duplicate page audit {paper_id} {number}")
        grouped[paper_id][number] = row
    if sum(len(value) for value in grouped.values()) != EXPECTED_PAGE_COUNT:
        raise RevalidationFailure("PAGE_PERSISTENCE_INTEGRITY_FAILURE", "batch page audit cardinality drift")
    return grouped


def load_ocr_audit() -> list[dict[str, str]]:
    rows = read_csv(OCR_AUDIT_PATH)
    if any(row.get("batch_attempt_id") != SOURCE_BATCH_ATTEMPT_ID for row in rows):
        raise RevalidationFailure("OCR_PROVENANCE_INVALID", "OCR audit attempt drift")
    return rows


def binding_state(manifest: dict[str, Any], gate: dict[str, Any]) -> str:
    ref = manifest.get("refinement_contract_sha256")
    evidence = manifest.get("refinement_evidence_fingerprint")
    q3 = manifest.get("q3_extraction_contract_sha256")
    if ref == gate["refinement_sha"] and evidence == gate["refinement_evidence"] and q3 == gate["q3_sha"]:
        return "CURRENT"
    if ref == OLD_REFINEMENT_SHA and evidence == OLD_REFINEMENT_EVIDENCE and q3 in (None, ""):
        return "STALE_OLD_BOUND"
    raise RevalidationFailure("PERSISTENCE_CONTRACT_BINDING_DRIFT", manifest.get("paper_id", ""))


def required_files(identity_path: Path) -> tuple[Path, Path, Path, Path]:
    files = (identity_path / "manifest.json", identity_path / "normalized_body.txt", identity_path / "provenance.json", identity_path / "quality.json")
    if not identity_path.is_dir() or any(not path.is_file() for path in files):
        raise RevalidationFailure("PERSISTENCE_STRUCTURE_FAILURE", str(identity_path))
    return files


def page_file_map(identity_path: Path, page_count: int) -> dict[int, Path]:
    page_dir = identity_path / "pages"
    if not page_dir.is_dir():
        raise RevalidationFailure("PERSISTENCE_STRUCTURE_FAILURE", str(page_dir))
    paths = list(page_dir.glob("*.txt"))
    result: dict[int, Path] = {}
    for path in paths:
        if not re.fullmatch(r"\d{4}\.txt", path.name):
            raise RevalidationFailure("PAGE_PERSISTENCE_INTEGRITY_FAILURE", f"unexpected page file {path.name}")
        number = int(path.stem)
        if number in result:
            raise RevalidationFailure("PAGE_PERSISTENCE_INTEGRITY_FAILURE", f"duplicate page file {number}")
        result[number] = path
    expected = set(range(1, page_count + 1))
    if set(result) != expected:
        raise RevalidationFailure("PAGE_PERSISTENCE_INTEGRITY_FAILURE", f"page file set {identity_path.name}")
    return result


def validate_identity(target: dict[str, Any], gate: dict[str, Any], page_audit: dict[str, dict[int, dict[str, str]]]) -> dict[str, Any]:
    paper_id = target["paper_id"]
    identity_path = PERSISTENCE_ROOT / paper_id
    manifest_path, body_path, provenance_path, quality_path = required_files(identity_path)
    manifest = read_json(manifest_path)
    provenance = read_json(provenance_path)
    quality = read_json(quality_path)
    if manifest.get("paper_id") != paper_id or provenance.get("paper_id") != paper_id or quality.get("paper_id") != paper_id:
        raise RevalidationFailure("PERSISTENCE_STRUCTURE_FAILURE", paper_id)
    old_binding = binding_state(manifest, gate)
    source_path = ROOT / str(manifest.get("source_path", ""))
    if not source_path.is_file() or pilot.sha256_file(source_path) != str(manifest.get("source_sha256", "")).upper():
        raise RevalidationFailure("SOURCE_SHA_MISMATCH", paper_id)
    if target.get("source_sha256") and target.get("source_sha256") != manifest.get("source_sha256"):
        raise RevalidationFailure("SOURCE_SHA_MISMATCH", paper_id)
    page_count = int(manifest.get("page_count", 0))
    if page_count <= 0 or int(target.get("page_count", page_count)) != page_count:
        raise RevalidationFailure("PAGE_COUNT_INTEGRITY_FAILURE", paper_id)
    files = page_file_map(identity_path, page_count)
    audit_rows = page_audit.get(paper_id, {})
    if set(audit_rows) != set(files):
        raise RevalidationFailure("PAGE_PERSISTENCE_INTEGRITY_FAILURE", paper_id)
    manifest_pages = manifest.get("page_provenance")
    provenance_pages = provenance.get("pages")
    quality_pages = quality.get("pages")
    if not isinstance(manifest_pages, list) or not isinstance(provenance_pages, list) or not isinstance(quality_pages, list) or len(manifest_pages) != page_count or len(provenance_pages) != page_count or len(quality_pages) != page_count:
        raise RevalidationFailure("PERSISTENCE_STRUCTURE_FAILURE", paper_id)
    manifest_page_map = {int(row.get("page_number")): row for row in manifest_pages}
    provenance_page_map = {int(row.get("page_number")): row for row in provenance_pages}
    quality_page_map = {int(row.get("page_number")): row for row in quality_pages}
    expected_numbers = set(range(1, page_count + 1))
    if set(manifest_page_map) != expected_numbers or set(provenance_page_map) != expected_numbers or set(quality_page_map) != expected_numbers:
        raise RevalidationFailure("PAGE_PERSISTENCE_INTEGRITY_FAILURE", paper_id)
    detail_rows: list[dict[str, Any]] = []
    sanity_rows: list[dict[str, Any]] = []
    page_text_snapshot: dict[int, str] = {}
    ocr_count = 0
    blank_count = 0
    page_quality_pass = True
    ocr_provenance_pass = True
    blank_pass = True
    changed_count = 0
    newly_accepted_count = 0
    unexpected_change_count = 0
    for number in range(1, page_count + 1):
        text = files[number].read_text(encoding="utf-8")
        page_text_snapshot[number] = sha256_bytes(files[number].read_bytes())
        page_record = manifest_page_map[number]
        provenance_record = provenance_page_map[number]
        quality_record = quality_page_map[number]
        audit = audit_rows[number]
        page_sha = pilot.sha256_text(text)
        is_ocr = provenance_record.get("provenance") == "OCR"
        is_blank = provenance_record.get("provenance") == "VERIFIED_BLANK"
        if page_sha != page_record.get("authoritative_page_text_sha256") or page_sha != provenance_record.get("authoritative_page_text_sha256") or page_sha != audit.get("authoritative_page_text_sha256"):
            raise RevalidationFailure("PAGE_TEXT_HASH_MISMATCH", f"{paper_id} page {number}")
        if provenance_record.get("page_number") != number or page_record.get("page_number") != number or int(audit.get("page_number", "0")) != number:
            raise RevalidationFailure("PAGE_PERSISTENCE_INTEGRITY_FAILURE", f"{paper_id} page {number}")
        if provenance_record.get("render_sha256") != page_record.get("render_sha256") or not page_record.get("render_sha256"):
            raise RevalidationFailure("PAGE_PERSISTENCE_INTEGRITY_FAILURE", f"render evidence {paper_id} page {number}")
        if quality_record.get("page_number") != number or not isinstance(quality_record.get("quality"), dict):
            raise RevalidationFailure("PERSISTENCE_STRUCTURE_FAILURE", f"quality evidence {paper_id} page {number}")
        if is_ocr:
            ocr_count += 1
            current_quality = pilot.text_quality(text)
            current_sanity = pilot.ocr_sanity(text, True)
            page_quality_pass = page_quality_pass and bool(current_quality.get("pass"))
            ocr_fields_ok = provenance_record.get("tesseract_ocr_child_granularity") == "ONE_ROUTED_PAGE_PER_CHILD" and provenance_record.get("tesseract_ocr_page_number") == number and provenance_record.get("tesseract_ocr_phase") == "PHASE_6_SELECTIVE_PAGE_OCR" and provenance_record.get("tesseract_ocr_timeout_seconds") == 180 and bool(provenance_record.get("authoritative_page_text_sha256"))
            ocr_provenance_pass = ocr_provenance_pass and ocr_fields_ok
            old_status = "PASS" if legacy_sanity(text) else "FAIL"
            new_status = "PASS" if current_sanity.get("pass") else "FAIL"
            matrix_pass = int(current_sanity.get("binary_matrix_evidence", {}).get("pass", False))
            rule_id = "OCR-SANITY-BINARY-MATRIX-V1" if matrix_pass else "NONE"
            changed = int(old_status != new_status)
            reason = "NO_STATUS_CHANGE"
            if changed:
                changed_count += 1
                if old_status == "PASS" and new_status == "FAIL":
                    unexpected_change_count += 1
                    reason = "UNEXPECTED_PASS_TO_FAIL"
                elif old_status == "FAIL" and new_status == "PASS" and matrix_pass:
                    newly_accepted_count += 1
                    reason = "LEGITIMATE_BINARY_MATRIX_ACCEPTED"
                else:
                    unexpected_change_count += 1
                    reason = "UNVERIFIED_FAIL_TO_PASS"
            sanity_rows.append({"paper_id": paper_id, "page_number": number, "old_sanity_status": old_status, "new_sanity_status": new_status, "rule_id": rule_id, "binary_matrix_pass": matrix_pass, "changed": changed, "reason": reason})
            detail_rows.append({"paper_id": paper_id, "page_number": number, "source_sha_status": "PASS", "page_hash_status": "PASS", "authoritative_page_hash_status": "PASS", "page_provenance_status": "PASS" if provenance_record.get("provenance") == audit.get("authoritative_page_source") else "FAIL", "page_classification_status": "PASS" if audit.get("primary_page_class") else "FAIL", "page_quality_status": "PASS" if current_quality.get("pass") else "FAIL", "ocr_provenance_status": "PASS" if ocr_fields_ok else "FAIL", "old_sanity_status": old_status, "new_sanity_status": new_status, "binary_matrix_pass": matrix_pass, "rule_id": rule_id, "sanity_status_changed": changed, "reason": reason, "render_evidence_status": "PASS"})
        elif is_blank:
            blank_count += 1
            blank_evidence_ok = text == "" and audit.get("primary_page_class") == "VERIFIED_BLANK" and audit.get("authoritative_page_source") == "VERIFIED_BLANK" and audit.get("repair_overlay") == "NO_REPAIR_REQUIRED" and audit.get("ocr_required") == "0" and bool(audit.get("render_sha256")) and audit.get("page_text_quality_status") == "EMPTY"
            blank_pass = blank_pass and blank_evidence_ok
            sanity_rows.append({"paper_id": paper_id, "page_number": number, "old_sanity_status": "VERIFIED_BLANK", "new_sanity_status": "VERIFIED_BLANK", "rule_id": "BLANK-CONTRACT-V1", "binary_matrix_pass": 0, "changed": 0, "reason": "VERIFIED_BLANK_CONTRACT_NO_TEXT_SANITY"})
            detail_rows.append({"paper_id": paper_id, "page_number": number, "source_sha_status": "PASS", "page_hash_status": "PASS", "authoritative_page_hash_status": "PASS", "page_provenance_status": "PASS" if provenance_record.get("provenance") == audit.get("authoritative_page_source") else "FAIL", "page_classification_status": "PASS" if audit.get("primary_page_class") == "VERIFIED_BLANK" else "FAIL", "page_quality_status": "PASS" if blank_evidence_ok else "FAIL", "ocr_provenance_status": "NOT_APPLICABLE", "old_sanity_status": "VERIFIED_BLANK", "new_sanity_status": "VERIFIED_BLANK", "binary_matrix_pass": 0, "rule_id": "BLANK-CONTRACT-V1", "sanity_status_changed": 0, "reason": "VERIFIED_BLANK_CONTRACT_NO_TEXT_SANITY", "render_evidence_status": "PASS" if bool(audit.get("render_sha256")) else "FAIL"})
        else:
            raise RevalidationFailure("PAGE_PROVENANCE_INVALID", f"{paper_id} page {number}")
        if page_record.get("provenance") and page_record.get("provenance") != provenance_record.get("provenance"):
            raise RevalidationFailure("PAGE_PROVENANCE_INVALID", f"{paper_id} page {number}")
    body = body_path.read_text(encoding="utf-8")
    body_snapshot = sha256_bytes(body_path.read_bytes())
    body_hash_ok = pilot.sha256_text(body) == manifest.get("normalized_text_sha256") and len(body) == int(manifest.get("normalized_text_chars", -1))
    if not body_hash_ok:
        raise RevalidationFailure("PERSISTED_BODY_INTEGRITY_FAILURE", paper_id)
    body_quality = pilot.text_quality(body, body=True)
    body_quality_ok = bool(body_quality.get("pass"))
    content_sanity_ok = bool(page_quality_pass and body_quality_ok and blank_pass and list(range(1, page_count + 1)) == sorted(page_text_snapshot) and any(page_text_snapshot.values()))
    if not content_sanity_ok:
        raise RevalidationFailure("CONTENT_SANITY_FAILURE", paper_id)
    if ocr_count != int(manifest.get("ocr_page_count", -1)) or blank_count != int(manifest.get("verified_blank_page_count", -1)) or int(manifest.get("pdf_text_page_count", -1)) != 0 or int(manifest.get("reconciled_page_count", -1)) != 0:
        raise RevalidationFailure("PAGE_PROVENANCE_INVALID", paper_id)
    if ocr_count + blank_count != page_count or not ocr_provenance_pass:
        raise RevalidationFailure("OCR_PROVENANCE_INVALID", paper_id)
    if not page_quality_pass:
        raise RevalidationFailure("PAGE_TEXT_QUALITY_FAILURE", paper_id)
    provenance_complete = bool(provenance.get("schema") and provenance.get("source_sha256") == manifest.get("source_sha256") and len(provenance_pages) == page_count)
    if not provenance_complete:
        raise RevalidationFailure("PROVENANCE_INCOMPLETE", paper_id)
    structure_pass = all(path.is_file() for path in required_files(identity_path)) and len(files) == page_count
    if not structure_pass:
        raise RevalidationFailure("PERSISTENCE_STRUCTURE_FAILURE", paper_id)
    return {"paper_id": paper_id, "identity_path": identity_path, "manifest_path": manifest_path, "manifest": manifest, "body_snapshot": body_snapshot, "page_text_snapshot": page_text_snapshot, "page_count": page_count, "ocr_count": ocr_count, "blank_count": blank_count, "page_quality_pass": int(page_quality_pass), "body_hash_ok": int(body_hash_ok), "body_quality_ok": int(body_quality_ok), "content_sanity_ok": int(content_sanity_ok), "provenance_complete": int(provenance_complete), "structure_pass": int(structure_pass), "old_binding_state": old_binding, "detail_rows": detail_rows, "sanity_rows": sanity_rows, "sanity_changed_count": changed_count, "newly_accepted_count": newly_accepted_count, "unexpected_change_count": unexpected_change_count, "body_hash": manifest.get("normalized_text_sha256")}


def collision_counts(records: list[dict[str, Any]]) -> tuple[int, int]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        groups[record["body_hash"]].append(record)
    collisions = [group for group in groups.values() if len({item["manifest"].get("source_sha256") for item in group}) > 1]
    low_information = sum(1 for group in collisions if any(not item["body_quality_ok"] for item in group))
    return len(collisions), low_information


def update_binding(record: dict[str, Any], gate: dict[str, Any], attempt_id: str) -> None:
    manifest = dict(record["manifest"])
    manifest["refinement_contract_sha256"] = gate["refinement_sha"]
    manifest["refinement_evidence_fingerprint"] = gate["refinement_evidence"]
    manifest["q3_extraction_contract_sha256"] = gate["q3_sha"]
    manifest["revalidation_attempt_id"] = attempt_id
    payload = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with tempfile.NamedTemporaryFile(prefix=".g8-q3-revalidation-", suffix=".json", dir=record["manifest_path"].parent, delete=False) as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
        staged = Path(stream.name)
    try:
        staged_value = json.loads(staged.read_text(encoding="utf-8"))
        if staged_value.get("refinement_contract_sha256") != gate["refinement_sha"] or staged_value.get("refinement_evidence_fingerprint") != gate["refinement_evidence"] or staged_value.get("q3_extraction_contract_sha256") != gate["q3_sha"]:
            raise RevalidationFailure("ATOMIC_BINDING_UPDATE_FAILURE", record["paper_id"])
        last_error: OSError | None = None
        for attempt in range(ATOMIC_REPLACE_RETRIES):
            try:
                os.replace(staged, record["manifest_path"])
                return
            except PermissionError as error:
                last_error = error
                if attempt + 1 < ATOMIC_REPLACE_RETRIES:
                    time.sleep(ATOMIC_REPLACE_DELAY_SECONDS * (attempt + 1))
        raise RevalidationFailure("ATOMIC_BINDING_UPDATE_FAILURE", f"{record['paper_id']}: {last_error}")
    finally:
        if staged.exists():
            staged.unlink()


def progress_row(record: dict[str, Any], sequence: int, status: str, error_code: str = "") -> dict[str, Any]:
    return {"paper_id": record["paper_id"], "sequence_number": sequence, "status": status, "error_code": error_code, "source_sha_status": "PASS", "page_integrity_status": "PASS", "page_quality_status": "PASS" if record.get("page_quality_pass") else "FAIL", "body_hash_status": "PASS" if record.get("body_hash_ok") else "FAIL", "body_quality_status": "PASS" if record.get("body_quality_ok") else "FAIL", "content_sanity_status": "PASS" if record.get("content_sanity_ok") else "FAIL", "collision_status": "PENDING", "provenance_status": "PASS" if record.get("provenance_complete") else "FAIL", "persistence_structure_status": "PASS" if record.get("structure_pass") else "FAIL", "contract_binding_status": record.get("old_binding_state", ""), "page_count": record.get("page_count", ""), "ocr_page_count": record.get("ocr_count", ""), "blank_page_count": record.get("blank_count", ""), "old_binding_state": record.get("old_binding_state", ""), "started_at": record.get("started_at", ""), "finished_at": record.get("finished_at", "")}


def base_result(attempt_id: str, status: str, gate: dict[str, Any], target_count: int = 0) -> dict[str, Any]:
    return {"STAGE": STAGE, "STATUS": status, "BRANCH": "library-refactor-v1", "HEAD": "557724fba6572d4d83dc421feda5b17b13ff8d66", "SOURCE_BATCH_ATTEMPT_ID": SOURCE_BATCH_ATTEMPT_ID, "REVALIDATION_ATTEMPT_ID": attempt_id, "SOURCE_BATCH_REPORTED_STATUS": "PASS", "SOURCE_BATCH_PRE_REVALIDATION_EFFECTIVE_STATUS": "PARTIAL", "SOURCE_BATCH_FINAL_ACCEPTANCE": "PENDING", "REVALIDATION_TARGET_COUNT": target_count, "REVALIDATION_UNIQUE_TARGET_COUNT": target_count, "TARGET_ADDED_COUNT": 0, "TARGET_REMOVED_COUNT": 0, "REFINEMENT_VERSION": "g8-q3-refinement-v1", "REFINEMENT_CONTRACT_SHA256": gate.get("refinement_sha", ""), "REFINEMENT_CONTRACT_SHA_MATCH": int(gate.get("refinement_sha") == EXPECTED_REFINEMENT_SHA), "REFINEMENT_EVIDENCE_FINGERPRINT": gate.get("refinement_evidence", ""), "REFINEMENT_EVIDENCE_FINGERPRINT_MATCH": int(gate.get("refinement_evidence") == EXPECTED_REFINEMENT_EVIDENCE), "Q3_EXTRACTION_CONTRACT_SHA256": gate.get("q3_sha", ""), "Q3_EXTRACTION_CONTRACT_SHA_MATCH": int(gate.get("q3_sha") == EXPECTED_Q3_SHA), "SOURCE_SHA_VALIDATION_PASS_COUNT": 0, "SOURCE_SHA_MISMATCH_COUNT": 0, "TOTAL_PAGE_COUNT": 0, "PAGE_PERSISTENCE_VALID_COUNT": 0, "PAGE_PERSISTENCE_INVALID_COUNT": 0, "OCR_SOURCE_PAGE_COUNT": 0, "BLANK_SOURCE_PAGE_COUNT": 0, "OCR_PROVENANCE_VALID_PAGE_COUNT": 0, "OCR_PROVENANCE_INVALID_PAGE_COUNT": 0, "PAGE_TEXT_QUALITY_PASS_COUNT": 0, "PAGE_TEXT_QUALITY_FAIL_COUNT": 0, "BLANK_PAGE_REVALIDATION_PASS_COUNT": 0, "BLANK_PAGE_REVALIDATION_FAIL_COUNT": 0, "BINARY_MATRIX_PAGE_23_REVALIDATED": 0, "BINARY_MATRIX_PAGE_23_SANITY_PASS": 0, "BINARY_MATRIX_PAGE_23_TEXT_HASH_UNCHANGED": 0, "SANITY_STATUS_CHANGED_PAGE_COUNT": 0, "UNEXPECTED_SANITY_CHANGE_COUNT": 0, "NEWLY_ACCEPTED_BY_BINARY_MATRIX_RULE_PAGE_COUNT": 0, "BODY_HASH_MATCH_COUNT": 0, "BODY_HASH_MISMATCH_COUNT": 0, "BODY_TEXT_QUALITY_PASS_COUNT": 0, "BODY_TEXT_QUALITY_FAIL_COUNT": 0, "BODY_HASH_COLLISION_SUSPECT_COUNT": 0, "LOW_INFORMATION_COLLISION_FAIL_COUNT": 0, "CONTENT_SANITY_PASS_COUNT": 0, "CONTENT_SANITY_FAIL_COUNT": 0, "PROVENANCE_COMPLETE_COUNT": 0, "PROVENANCE_INCOMPLETE_COUNT": 0, "PERSISTENCE_STRUCTURE_PASS_COUNT": 0, "PERSISTENCE_STRUCTURE_FAIL_COUNT": 0, "CURRENT_CONTRACT_BINDING_PASS_COUNT": 0, "CURRENT_CONTRACT_BINDING_FAIL_COUNT": 0, "PAGE_TEXT_MODIFICATION_COUNT": 0, "BODY_TEXT_MODIFICATION_COUNT": 0, "OCR_TEXT_MODIFICATION_COUNT": 0, "OCR_RUN": 0, "OCR_REPLAY_PAGE_COUNT": 0, "PDF_RENDER_RUN": 0, "PDF_INSPECTOR_EXTRACTION_RUN": 0, "PDFTOTEXT_EXTRACTION_RUN": 0, "BODY_RECONSTRUCTION_RUN": 0, "FORMAL_ARTIFACTS_GENERATED": 0, "ARTIFACT_SETS": 325, "PRIMARY_ARTIFACTS": 975, "DOC_MANUAL_BACKLOG": 0, "Q3_MANUAL_BACKLOG": 128, "ELIGIBLE": 453, "INELIGIBLE": 189, "FORMAL_ELIGIBILITY_MODIFIED": 0, "IDENTITY_MODIFICATION_COUNT": 0, "MEMBERSHIP_MODIFICATION_COUNT": 0, "ORIGINAL_FILES_MODIFIED": 0, "NETWORK_ACCESS_USED": 0, "DOWNLOAD_RUN": 0, "NEW_DEPENDENCY_INSTALLED": 0, "WORD_RUN": 0, "WORD_COM_RUN": 0, "DOC_CONVERSION_RUN": 0, "PRINT_JOB_RUN": 0, "G9_RUN": 0, "G10_RUN": 0, "GIT_OPERATIONS": 0, "FAILED_IDENTITY_COUNT": 0, "FAILED_PAPER_IDS": [], "NEW_FAILURE_MODE_COUNT": 0, "NEW_FAILURE_MODES": [], "BLOCKER": "NONE", "CURRENT_GATE": "PHASE_0_CONTRACT_PREFLIGHT"}


def checkpoint(attempt: dict[str, Any], *, status: str | None = None, current_paper_id: str = "", current_gate: str = "", completed_count: int | None = None, failed_count: int | None = None) -> None:
    attempt["updated_at"] = now_utc()
    attempt["current_paper_id"] = current_paper_id
    attempt["current_gate"] = current_gate
    if status is not None:
        attempt["status"] = status
    if completed_count is not None:
        attempt["completed_count"] = completed_count
    if failed_count is not None:
        attempt["failed_count"] = failed_count
    atomic_write_json(ATTEMPT_PATH, attempt)


def run(preflight_only: bool) -> dict[str, Any]:
    attempt_id = new_attempt_id()
    gate: dict[str, Any] = {}
    attempt = {"stage": STAGE, "attempt_id": attempt_id, "status": "RUNNING", "current_paper_id": "", "completed_count": 0, "failed_count": 0, "current_gate": "PHASE_0_CONTRACT_PREFLIGHT", "updated_at": now_utc(), "source_batch_attempt_id": SOURCE_BATCH_ATTEMPT_ID, "binding_update_allowed": int(not preflight_only), "ocr_run": 0, "pdf_render_run": 0, "body_reconstruction_run": 0}
    atomic_write_json(ATTEMPT_PATH, attempt)
    try:
        gate = contract_gate()
        targets = load_target_rows()
        page_audit = load_page_audit()
        load_ocr_audit()
        target_ids = {row["paper_id"] for row in targets}
        persistence_ids = {path.parent.name for path in PERSISTENCE_ROOT.glob("*/manifest.json")}
        if target_ids != persistence_ids:
            raise RevalidationFailure("BATCH_PERSISTENCE_TARGET_SET_DRIFT", f"target={len(target_ids)} persistence={len(persistence_ids)}")
        result = base_result(attempt_id, "RUNNING", gate, len(targets))
        atomic_write_json(RESULT_PATH, result)
        progress: list[dict[str, Any]] = []
        details: list[dict[str, Any]] = []
        sanity_audit: list[dict[str, Any]] = []
        records: list[dict[str, Any]] = []
        failures: list[tuple[str, str]] = []
        for index, target in enumerate(targets, start=1):
            paper_id = target["paper_id"]
            started = now_utc()
            attempt["current_paper_id"] = paper_id
            attempt["current_gate"] = "PHASE_1_PERSISTED_EVIDENCE_REVALIDATION"
            checkpoint(attempt)
            try:
                record = validate_identity(target, gate, page_audit)
                record["started_at"] = started
                record["finished_at"] = now_utc()
                records.append(record)
                progress.append(progress_row(record, index, "PASS"))
                details.extend(record["detail_rows"])
                sanity_audit.extend(record["sanity_rows"])
            except RevalidationFailure as error:
                failures.append((paper_id, error.code))
                failed_record = {"paper_id": paper_id, "started_at": started, "finished_at": now_utc(), "old_binding_state": "FAILED", "page_quality_pass": 0, "body_hash_ok": 0, "body_quality_ok": 0, "content_sanity_ok": 0, "provenance_complete": 0, "structure_pass": 0, "page_count": "", "ocr_count": "", "blank_count": ""}
                progress.append(progress_row(failed_record, index, "BLOCKED", error.code))
            atomic_write_csv(PROGRESS_PATH, progress, PROGRESS_FIELDS)
            atomic_write_csv(DETAIL_PATH, details, DETAIL_FIELDS)
            atomic_write_csv(SANITY_AUDIT_PATH, sanity_audit, SANITY_FIELDS)
            result.update({"CURRENT_GATE": "PHASE_1_PERSISTED_EVIDENCE_REVALIDATION", "SOURCE_SHA_VALIDATION_PASS_COUNT": len(records), "SOURCE_SHA_MISMATCH_COUNT": sum(code == "SOURCE_SHA_MISMATCH" for _, code in failures), "TOTAL_PAGE_COUNT": sum(item.get("page_count", 0) for item in records), "PAGE_PERSISTENCE_VALID_COUNT": sum(item.get("page_count", 0) for item in records), "PAGE_PERSISTENCE_INVALID_COUNT": 0, "OCR_SOURCE_PAGE_COUNT": sum(item.get("ocr_count", 0) for item in records), "BLANK_SOURCE_PAGE_COUNT": sum(item.get("blank_count", 0) for item in records), "OCR_PROVENANCE_VALID_PAGE_COUNT": sum(item.get("ocr_count", 0) for item in records), "OCR_PROVENANCE_INVALID_PAGE_COUNT": 0, "PAGE_TEXT_QUALITY_PASS_COUNT": sum(item.get("ocr_count", 0) for item in records if item.get("page_quality_pass")), "PAGE_TEXT_QUALITY_FAIL_COUNT": 0, "BLANK_PAGE_REVALIDATION_PASS_COUNT": sum(item.get("blank_count", 0) for item in records), "BLANK_PAGE_REVALIDATION_FAIL_COUNT": 0, "BODY_HASH_MATCH_COUNT": sum(item.get("body_hash_ok", 0) for item in records), "BODY_HASH_MISMATCH_COUNT": 0, "BODY_TEXT_QUALITY_PASS_COUNT": sum(item.get("body_quality_ok", 0) for item in records), "BODY_TEXT_QUALITY_FAIL_COUNT": 0, "CONTENT_SANITY_PASS_COUNT": sum(item.get("content_sanity_ok", 0) for item in records), "CONTENT_SANITY_FAIL_COUNT": len(records) - sum(item.get("content_sanity_ok", 0) for item in records), "PROVENANCE_COMPLETE_COUNT": sum(item.get("provenance_complete", 0) for item in records), "PROVENANCE_INCOMPLETE_COUNT": len(records) - sum(item.get("provenance_complete", 0) for item in records), "PERSISTENCE_STRUCTURE_PASS_COUNT": sum(item.get("structure_pass", 0) for item in records), "PERSISTENCE_STRUCTURE_FAIL_COUNT": len(records) - sum(item.get("structure_pass", 0) for item in records), "SANITY_STATUS_CHANGED_PAGE_COUNT": sum(item.get("sanity_changed_count", 0) for item in records), "NEWLY_ACCEPTED_BY_BINARY_MATRIX_RULE_PAGE_COUNT": sum(item.get("newly_accepted_count", 0) for item in records), "UNEXPECTED_SANITY_CHANGE_COUNT": sum(item.get("unexpected_change_count", 0) for item in records), "FAILED_IDENTITY_COUNT": len(failures), "FAILED_PAPER_IDS": [item[0] for item in failures], "NEW_FAILURE_MODE_COUNT": len(set(code for _, code in failures)), "NEW_FAILURE_MODES": sorted(set(code for _, code in failures)), "completed_count": len(records), "failed_count": len(failures)})
            atomic_write_json(RESULT_PATH, result)
            checkpoint(attempt, completed_count=len(records), failed_count=len(failures))
        collision_count, low_info_count = collision_counts(records)
        result["BODY_HASH_COLLISION_SUSPECT_COUNT"] = collision_count
        result["LOW_INFORMATION_COLLISION_FAIL_COUNT"] = low_info_count
        result["CURRENT_GATE"] = "PHASE_3_FINAL_GATE"
        if collision_count or low_info_count:
            failures.append(("<collision-gate>", "BODY_HASH_COLLISION"))
        if not failures and len(records) == EXPECTED_TARGET_COUNT and result["TOTAL_PAGE_COUNT"] == EXPECTED_PAGE_COUNT and result["OCR_SOURCE_PAGE_COUNT"] == EXPECTED_OCR_PAGE_COUNT and result["BLANK_SOURCE_PAGE_COUNT"] == EXPECTED_BLANK_PAGE_COUNT and result["UNEXPECTED_SANITY_CHANGE_COUNT"] == 0:
            if not preflight_only:
                attempt["current_gate"] = "PHASE_2_ATOMIC_CURRENT_CONTRACT_BINDING"
                checkpoint(attempt)
                for record in records:
                    update_binding(record, gate, attempt_id)
                current_pass = 0
                for record in records:
                    current_manifest = read_json(record["manifest_path"])
                    current_pass += int(binding_state(current_manifest, gate) == "CURRENT")
                result["CURRENT_CONTRACT_BINDING_PASS_COUNT"] = current_pass
                result["CURRENT_CONTRACT_BINDING_FAIL_COUNT"] = EXPECTED_TARGET_COUNT - current_pass
                result["PAGE_TEXT_MODIFICATION_COUNT"] = sum(int(record["page_text_snapshot"] != {number: sha256_bytes((record["identity_path"] / "pages" / f"{number:04d}.txt").read_bytes()) for number in record["page_text_snapshot"]}) for record in records)
                result["BODY_TEXT_MODIFICATION_COUNT"] = sum(int(record["body_snapshot"] != sha256_bytes((record["identity_path"] / "normalized_body.txt").read_bytes())) for record in records)
                result["OCR_TEXT_MODIFICATION_COUNT"] = result["PAGE_TEXT_MODIFICATION_COUNT"]
                if result["PAGE_TEXT_MODIFICATION_COUNT"] or result["BODY_TEXT_MODIFICATION_COUNT"]:
                    failures.append(("<post-binding-integrity>", "PERSISTENCE_TEXT_MODIFIED"))
                for row in progress:
                    if row.get("status") == "PASS":
                        row["contract_binding_status"] = "CURRENT"
                atomic_write_csv(PROGRESS_PATH, progress, PROGRESS_FIELDS)
            else:
                result["CURRENT_CONTRACT_BINDING_PASS_COUNT"] = sum(item.get("old_binding_state") == "CURRENT" for item in records)
                result["CURRENT_CONTRACT_BINDING_FAIL_COUNT"] = EXPECTED_TARGET_COUNT - result["CURRENT_CONTRACT_BINDING_PASS_COUNT"]
        result["BINARY_MATRIX_PAGE_23_REVALIDATED"] = int(any(item["paper_id"] == "CUMCM-2020-B-005" and row["page_number"] == 23 for item in records for row in item["sanity_rows"]))
        page23_rows = [row for item in records if item["paper_id"] == "CUMCM-2020-B-005" for row in item["sanity_rows"] if row["page_number"] == 23]
        result["BINARY_MATRIX_PAGE_23_SANITY_PASS"] = int(bool(page23_rows and page23_rows[0]["new_sanity_status"] == "PASS"))
        result["BINARY_MATRIX_PAGE_23_TEXT_HASH_UNCHANGED"] = int(bool(page23_rows))
        result["CURRENT_CONTRACT_BINDING_PASS_COUNT"] = result.get("CURRENT_CONTRACT_BINDING_PASS_COUNT", 0)
        result["CURRENT_CONTRACT_BINDING_FAIL_COUNT"] = result.get("CURRENT_CONTRACT_BINDING_FAIL_COUNT", EXPECTED_TARGET_COUNT)
        if failures:
            result["STATUS"] = "BLOCKED" if any(code not in {"UNEXPECTED_PASS_TO_FAIL", "UNVERIFIED_FAIL_TO_PASS"} for _, code in failures) else "PARTIAL"
            result["SOURCE_BATCH_FINAL_ACCEPTANCE"] = "PENDING"
            result["BLOCKER"] = failures[0][1]
            result["FAILED_IDENTITY_COUNT"] = len(failures)
            result["FAILED_PAPER_IDS"] = [item[0] for item in failures]
            result["NEW_FAILURE_MODE_COUNT"] = len(set(item[1] for item in failures))
            result["NEW_FAILURE_MODES"] = sorted(set(item[1] for item in failures))
        elif preflight_only:
            result["STATUS"] = "PREFLIGHT_PASS"
            result["SOURCE_BATCH_FINAL_ACCEPTANCE"] = "PENDING_BINDING_UPDATE"
            result["BLOCKER"] = "NONE"
        else:
            result["STATUS"] = "PASS"
            result["SOURCE_BATCH_FINAL_ACCEPTANCE"] = "PASS"
            result["BLOCKER"] = "NONE"
        attempt["status"] = result["STATUS"]
        attempt["current_gate"] = "PHASE_3_FINAL_GATE"
        checkpoint(attempt, status=result["STATUS"], current_gate="PHASE_3_FINAL_GATE", completed_count=len(records), failed_count=len(failures))
        atomic_write_json(RESULT_PATH, result)
        report(result, preflight_only)
        print(json.dumps({"STATUS": result["STATUS"], "REVALIDATION_ATTEMPT_ID": attempt_id, "TARGET_COUNT": len(targets), "TOTAL_PAGE_COUNT": result["TOTAL_PAGE_COUNT"], "OCR_SOURCE_PAGE_COUNT": result["OCR_SOURCE_PAGE_COUNT"], "BLANK_SOURCE_PAGE_COUNT": result["BLANK_SOURCE_PAGE_COUNT"], "SANITY_STATUS_CHANGED_PAGE_COUNT": result["SANITY_STATUS_CHANGED_PAGE_COUNT"], "NEWLY_ACCEPTED_BY_BINARY_MATRIX_RULE_PAGE_COUNT": result["NEWLY_ACCEPTED_BY_BINARY_MATRIX_RULE_PAGE_COUNT"], "CURRENT_CONTRACT_BINDING_PASS_COUNT": result["CURRENT_CONTRACT_BINDING_PASS_COUNT"], "BLOCKER": result["BLOCKER"]}, ensure_ascii=False))
        return result
    except RevalidationFailure as error:
        result = base_result(attempt_id, "BLOCKED", gate, 0)
        result.update({"BLOCKER": error.code, "NEW_FAILURE_MODE_COUNT": 1, "NEW_FAILURE_MODES": [error.code], "FAILED_IDENTITY_COUNT": 0, "FAILED_PAPER_IDS": []})
        attempt["status"] = "BLOCKED"
        attempt["current_gate"] = "PHASE_BLOCKED"
        checkpoint(attempt, status="BLOCKED", current_gate="PHASE_BLOCKED")
        atomic_write_json(RESULT_PATH, result)
        report(result, preflight_only)
        print(json.dumps({"STATUS": "BLOCKED", "REVALIDATION_ATTEMPT_ID": attempt_id, "BLOCKER": error.code}, ensure_ascii=False))
        return result


def report(result: dict[str, Any], preflight_only: bool) -> None:
    lines = ["# G8 Q3 Batch Revalidation Under Frozen Contract", "", *[f"{key}={value}" for key, value in result.items()], "", "## Scope", "", "This stage validates the 128 persisted identities from the prior batch under the frozen refinement and extraction contracts.", "No OCR, rendering, PDF text extraction, body reconstruction, network access, dependency installation, Word, Git, or Formal Artifact generation was performed.", "", "## Contract status", "", "The prior batch is governance PARTIAL because its binary-matrix sanity acceptance was corrected during execution. The current run revalidates persisted evidence first and updates only the per-identity persistence manifest binding after all identities pass.", "", "## Sanity change audit", "", "The complete page-level audit is stored in `catalog/scale/g8_q3_batch_sanity_change_audit.csv`; the expected legitimate change is CUMCM-2020-B-005 page 23 FAIL to PASS under OCR-SANITY-BINARY-MATRIX-V1.", "", "## Binding", "", "All current persistence bindings are checked after the atomic update. Page text and normalized body files are snapshotted before and after binding; no text file is rewritten.", "", "## Outputs", "", *[f"- `{path.relative_to(ROOT).as_posix()}`" for path in (RESULT_PATH, ATTEMPT_PATH, PROGRESS_PATH, DETAIL_PATH, SANITY_AUDIT_PATH, REPORT_PATH)], "", "## Next", "", "G8-Q3-FORMAL-ARTIFACT-GENERATION" if result.get("STATUS") == "PASS" and not preflight_only else "G8-Q3-BATCH-REVALIDATE-UNDER-FROZEN-CONTRACT (execute after preflight)" if preflight_only else "G8-Q3-CONTRACT-REFINEMENT"]
    atomic_write_bytes(REPORT_PATH, ("\n".join(lines) + "\n").encode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight-only", action="store_true", help="validate persisted evidence without changing manifests")
    parser.add_argument("--execute", action="store_true", help="validate all identities, then atomically update manifest bindings")
    args = parser.parse_args()
    if args.preflight_only == args.execute:
        parser.error("choose exactly one of --preflight-only or --execute")
    result = run(preflight_only=args.preflight_only)
    return 0 if result.get("STATUS") in {"PASS", "PREFLIGHT_PASS"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
