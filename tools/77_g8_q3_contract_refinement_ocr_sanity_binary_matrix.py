"""Freeze the binary-matrix OCR sanity refinement without replaying the batch."""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import os
import re
import tempfile
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
REFINEMENT_PATH = SCALE / "g8_q3_contract_refinement_v1.json"
EXTRACTION_PATH = SCALE / "g8_q3_extraction_contract_v1.json"
BATCH_RESULT_PATH = SCALE / "g8_q3_batch_repair_result.json"
BATCH_PAGE_AUDIT_PATH = SCALE / "g8_q3_batch_page_audit.csv"
BATCH_OCR_AUDIT_PATH = SCALE / "g8_q3_batch_ocr_audit.csv"
BATCH_SOURCE_SELECTION_PATH = SCALE / "g8_q3_batch_source_selection.csv"
BATCH_ROOT = SCALE / "g8_q3_batch_repair"
VALIDATION_PATH = SCALE / "g8_q3_binary_matrix_sanity_validation.csv"
RESULT_PATH = SCALE / "g8_q3_binary_matrix_sanity_refinement_result.json"
PLAN_PATH = SCALE / "g8_q3_batch_revalidation_plan.json"
REPORT_PATH = REPORTS / "G8_Q3_BINARY_MATRIX_SANITY_REFINEMENT.md"
PILOT_PATH = ROOT / "tools" / "72_g8_q3_contract_pilot_resume.py"
EXPECTED_POST_MUTATION_SHA = "20BE796500A62654DC997911929E9D60A0F1D770BB6878DFA19C2428688B78C7"
EXPECTED_OLD_REFINEMENT_SHA = "1D8BE5FE247FFF54DD3147B493820AB92C1BFEE211DB6FE8E21D59C64E4F1F2C"
EXPECTED_OLD_EVIDENCE = "5FA095687812D8FB58CE9F61DCAE88F0B096FDBC2219326A8C77571C3311C70E"
EXPECTED_BATCH_ATTEMPT = "20260902T181812821882_f3ed3664"
FALSE_POSITIVE_ID = "CUMCM-2020-B-005"
FALSE_POSITIVE_PAGE = 23
CSV_FIELDS = [
    "case_id", "case_kind", "paper_id", "page_number", "text_sha256", "text_chars",
    "source_sha256", "render_sha256", "ocr_text_sha256", "old_sanity_status",
    "new_sanity_status", "expected_status", "binary_matrix_pass", "candidate_row_count",
    "candidate_row_length_mode", "candidate_row_length_mode_count", "candidate_row_length_regularity",
    "candidate_char_ratio", "context_marker_hit_count", "single_symbol_run_count",
    "alternating_binary_run_count", "replacement_ratio", "control_ratio", "plausible_ratio",
    "deterministic_evidence_pass",
]


def load_pilot() -> Any:
    spec = importlib.util.spec_from_file_location("g8_q3_pilot_core", PILOT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("PILOT_CORE_IMPORT_FAILED")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pilot = load_pilot()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest().upper()


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp-" + os.urandom(8).hex())
    try:
        temporary.write_text(text, encoding="utf-8", newline="\n")
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def atomic_write_json(path: Path, value: Any) -> None:
    atomic_write_text(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp-" + os.urandom(8).hex())
    try:
        with temporary.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS)
            writer.writeheader()
            writer.writerows(rows)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def legacy_ocr_sanity(text: str) -> dict[str, Any]:
    encoded = text.encode("utf-8", errors="replace")
    replacement = text.count("\ufffd") / max(1, len(text))
    control = sum(ord(char) < 32 and char not in "\n\r\t" for char in text) / max(1, len(text))
    visible = sum(char.isalnum() or "\u4e00" <= char <= "\u9fff" for char in text) / max(1, len(text.strip()))
    repeated = bool(re.search(r"([^\s\W_])\1{19,}", text))
    passed = bool(encoded and text.strip() and replacement <= 0.02 and control <= 0.02 and visible >= 0.15 and not repeated)
    return {"pass": passed, "replacement_ratio": replacement, "control_ratio": control, "plausible_ratio": visible, "repeated_symbol": repeated}


def metric_row(case_id: str, case_kind: str, text: str, expected: bool, *, paper_id: str = "", page_number: str = "", source_sha: str = "", render_sha: str = "", ocr_sha: str = "") -> dict[str, Any]:
    old = legacy_ocr_sanity(text)
    new = pilot.ocr_sanity(text, True)
    matrix = new["binary_matrix_evidence"]
    passed = bool(new["pass"] == expected)
    return {
        "case_id": case_id, "case_kind": case_kind, "paper_id": paper_id, "page_number": page_number,
        "text_sha256": pilot.sha256_text(text), "text_chars": len(text), "source_sha256": source_sha,
        "render_sha256": render_sha, "ocr_text_sha256": ocr_sha,
        "old_sanity_status": "PASS" if old["pass"] else "FAIL", "new_sanity_status": "PASS" if new["pass"] else "FAIL",
        "expected_status": "PASS" if expected else "FAIL", "binary_matrix_pass": int(matrix["pass"]),
        "candidate_row_count": matrix["candidate_row_count"], "candidate_row_length_mode": matrix["candidate_row_length_mode"],
        "candidate_row_length_mode_count": matrix["candidate_row_length_mode_count"], "candidate_row_length_regularity": matrix["candidate_row_length_regularity"],
        "candidate_char_ratio": matrix["candidate_char_ratio"], "context_marker_hit_count": matrix["context_marker_hit_count"],
        "single_symbol_run_count": matrix["single_symbol_run_count"], "alternating_binary_run_count": matrix["alternating_binary_run_count"],
        "replacement_ratio": new["replacement_ratio"], "control_ratio": new["control_ratio"], "plausible_ratio": new["plausible_ratio"],
        "deterministic_evidence_pass": int(passed),
    }


def recover_contract_mutation() -> tuple[str, str, list[dict[str, Any]]]:
    raw = EXTRACTION_PATH.read_bytes()
    post = sha256_bytes(raw)
    pattern = re.compile(
        rb'  "pilot_status": "PASS",\n'
        rb'  "pilot_attempt_id": "[^"]+",\n'
        rb'  "pilot_target_count": 6,\n'
        rb'  "pilot_result_validated": true,\n'
    )
    pre_bytes, count = pattern.subn(b"", raw)
    if count != 1 or post != EXPECTED_POST_MUTATION_SHA:
        raise RuntimeError("CONTRACT_MUTATION_RECOVERY_FAILED")
    pre = sha256_bytes(pre_bytes)
    fields = [
        {"path": "$.pilot_status", "old_value": "<absent>", "new_value": "PASS", "reason": "bind the completed Pilot result to the authoritative extraction contract", "semantic_category": "operational-only governance metadata"},
        {"path": "$.pilot_attempt_id", "old_value": "<absent>", "new_value": "20260902T134704174291_30625ec2", "reason": "bind the exact Pilot attempt", "semantic_category": "operational-only governance metadata"},
        {"path": "$.pilot_target_count", "old_value": "<absent>", "new_value": 6, "reason": "bind the frozen Pilot target cardinality", "semantic_category": "operational-only governance metadata"},
        {"path": "$.pilot_result_validated", "old_value": "<absent>", "new_value": True, "reason": "make the Pilot result validation gate explicit", "semantic_category": "operational-only governance metadata"},
    ]
    return pre, post, fields


def page_evidence() -> tuple[dict[str, Any], str, str, str]:
    batch = read_json(BATCH_RESULT_PATH)
    if batch.get("ATTEMPT_ID") != EXPECTED_BATCH_ATTEMPT or batch.get("STATUS") != "PASS":
        raise RuntimeError("BATCH_EVIDENCE_BINDING_INVALID")
    page = next((row for row in read_csv(BATCH_PAGE_AUDIT_PATH) if row.get("paper_id") == FALSE_POSITIVE_ID and row.get("page_number") == str(FALSE_POSITIVE_PAGE)), None)
    ocr = next((row for row in read_csv(BATCH_OCR_AUDIT_PATH) if row.get("paper_id") == FALSE_POSITIVE_ID and row.get("page_number") == str(FALSE_POSITIVE_PAGE)), None)
    if page is None or ocr is None:
        raise RuntimeError("PAGE_23_PERSISTED_EVIDENCE_MISSING")
    selection = next((row for row in read_csv(BATCH_SOURCE_SELECTION_PATH) if row.get("paper_id") == FALSE_POSITIVE_ID), None)
    if selection is None:
        raise RuntimeError("PAGE_23_SOURCE_SELECTION_MISSING")
    text_path = BATCH_ROOT / FALSE_POSITIVE_ID / "pages" / f"{FALSE_POSITIVE_PAGE:04d}.txt"
    text = text_path.read_text(encoding="utf-8")
    checks = {
        "source_unchanged": page.get("source_sha256") == selection.get("chosen_extraction_source_sha256") == selection.get("primary_source_sha256"),
        "ocr_success": ocr.get("status") == "SUCCESS" and ocr.get("timed_out") == "0" and ocr.get("ocr_quality_status") == "PASS",
        "render_unchanged": page.get("render_sha256") == ocr.get("render_sha256"),
        "ocr_text_persisted": pilot.sha256_text(text) == ocr.get("ocr_text_sha256"),
        "page_scoped": ocr.get("phase") == "PHASE_6_SELECTIVE_PAGE_OCR" and ocr.get("page_number") == str(FALSE_POSITIVE_PAGE),
    }
    if not all(checks.values()):
        raise RuntimeError("PAGE_23_PERSISTED_EVIDENCE_CHECK_FAILED")
    return {"page": page, "ocr": ocr, "text": text, "checks": checks}, text, page["source_sha256"], page["render_sha256"]


def prepare_validation() -> dict[str, Any]:
    pre_sha, post_sha, mutation_fields = recover_contract_mutation()
    evidence, text, source_sha, render_sha = page_evidence()
    rows = [metric_row("real_page_23", "REAL_PAGE", text, True, paper_id=FALSE_POSITIVE_ID, page_number=str(FALSE_POSITIVE_PAGE), source_sha=source_sha, render_sha=render_sha, ocr_sha=evidence["ocr"]["ocr_text_sha256"])]
    positive_rows = [
        "010000000000000000000000100", "001100000000000000000000000", "010100000000000000000000100",
        "001010000000000000000001100", "000101000000000000000001000", "000010100000000000000011000",
    ]
    positive = "附录 程序源代码 p=I\n" + "\n".join(positive_rows) + "\ndis=p; for i=1"
    rows.append(metric_row("synthetic_binary_matrix_positive", "SYNTHETIC_POSITIVE", positive, True))
    rows.append(metric_row("synthetic_single_symbol_ones", "SYNTHETIC_NEGATIVE", "111111111111111111", False))
    rows.append(metric_row("synthetic_single_symbol_zeroes", "SYNTHETIC_NEGATIVE", "000000000000000000", False))
    rows.append(metric_row("synthetic_alternating_binary_noise", "SYNTHETIC_NEGATIVE", "101010101010101010", False))
    rows.append(metric_row("synthetic_replacement_corruption", "SYNTHETIC_NEGATIVE", "abc" * 30 + "\ufffd" * 30, False))
    rows.append(metric_row("synthetic_control_corruption", "SYNTHETIC_NEGATIVE", "abc" * 30 + "\x01" * 30, False))
    write_csv(VALIDATION_PATH, rows)
    refinement_sha, evidence_fingerprint = pilot.refinement_fingerprint()
    result = {
        "STAGE": "G8-Q3-CONTRACT-REFINEMENT-OCR-SANITY-BINARY-MATRIX", "STATUS": "PREPARED",
        "BRANCH": "library-refactor-v1", "HEAD": "557724fba6572d4d83dc421feda5b17b13ff8d66",
        "SOURCE_BATCH_ATTEMPT_ID": EXPECTED_BATCH_ATTEMPT, "SOURCE_BATCH_REPORTED_STATUS": "PASS", "SOURCE_BATCH_EFFECTIVE_STATUS": "PARTIAL",
        "FALSE_POSITIVE_PAPER_ID": FALSE_POSITIVE_ID, "FALSE_POSITIVE_PAGE_NUMBER": FALSE_POSITIVE_PAGE,
        "FALSE_POSITIVE_CLASSIFICATION": "LEGITIMATE_BINARY_MATRIX_FALSE_POSITIVE",
        "PRE_MUTATION_Q3_EXTRACTION_CONTRACT_SHA256": pre_sha, "POST_MUTATION_Q3_EXTRACTION_CONTRACT_SHA256": post_sha,
        "CONTRACT_MUTATION_FILE_COUNT": 1, "CONTRACT_MUTATION_FIELD_COUNT": len(mutation_fields), "CONTRACT_MUTATION_FIELDS": mutation_fields,
        "CONTRACT_MUTATION_DIFF_RESOLVED": 1, "RUNNER_SANITY_RULE_MODIFICATION_COUNT": 1,
        "PAGE_23_OLD_SANITY_STATUS": rows[0]["old_sanity_status"], "PAGE_23_NEW_SANITY_STATUS": rows[0]["new_sanity_status"],
        "PAGE_23_OCR_TEXT_CHANGED": int(rows[0]["text_sha256"] != rows[0]["ocr_text_sha256"]),
        "SYNTHETIC_BINARY_MATRIX_POSITIVE_PASS": rows[1]["deterministic_evidence_pass"],
        "SYNTHETIC_REPEATED_SYMBOL_GARBAGE_REJECT_PASS": int(all(rows[index]["deterministic_evidence_pass"] for index in (2, 3, 4))),
        "SYNTHETIC_CORRUPT_TEXT_REJECT_PASS": int(all(rows[index]["deterministic_evidence_pass"] for index in (5, 6))),
        "EXTRACTION_CONTENT_SEMANTICS_CHANGED": 0, "OCR_ROUTING_SEMANTICS_CHANGED": 0, "OCR_ENGINE_OR_RUNTIME_CHANGED": 0,
        "TEXT_NORMALIZATION_CHANGED": 0, "BODY_RECONSTRUCTION_CHANGED": 0, "SANITY_ACCEPTANCE_RULE_CHANGED": 1, "OPERATIONAL_RUNTIME_CHANGED": 0,
        "REFINEMENT_CONTRACT_UPDATED": 1, "REFINEMENT_VERSION": "g8-q3-refinement-v1", "REFINEMENT_CONTRACT_SHA256": refinement_sha,
        "REFINEMENT_EVIDENCE_FINGERPRINT": evidence_fingerprint, "Q3_EXTRACTION_CONTRACT_UPDATED": 0, "Q3_EXTRACTION_CONTRACT_SHA256": "PENDING",
        "BATCH_PERSISTENCE_DELETED_COUNT": 0, "BATCH_REPLAY_REQUIRED": 0, "BATCH_REPLAY_SCOPE": "NO_OCR_REPLAY; persisted page/body revalidation only",
        "FORMAL_ARTIFACTS_GENERATED": 0, "ARTIFACT_SETS": 325, "PRIMARY_ARTIFACTS": 975, "DOC_MANUAL_BACKLOG": 0, "Q3_MANUAL_BACKLOG": 128,
        "ELIGIBLE": 453, "INELIGIBLE": 189, "FORMAL_ELIGIBILITY_MODIFIED": 0, "IDENTITY_MODIFICATION_COUNT": 0, "MEMBERSHIP_MODIFICATION_COUNT": 0,
        "ORIGINAL_FILES_MODIFIED": 0, "FULL_Q3_BATCH_RUN": 0, "FULL_BATCH_OCR_REPLAY": 0, "OCR_REPLAY_PAGE_COUNT": 0,
        "NETWORK_ACCESS_USED": 0, "DOWNLOAD_RUN": 0, "NEW_DEPENDENCY_INSTALLED": 0, "WORD_RUN": 0, "WORD_COM_RUN": 0,
        "DOC_CONVERSION_RUN": 0, "PRINT_JOB_RUN": 0, "G9_RUN": 0, "G10_RUN": 0, "GIT_OPERATIONS": 0,
        "PAGE_23_EVIDENCE_CHECKS": evidence["checks"], "VALIDATION_ROWS": len(rows),
    }
    atomic_write_json(RESULT_PATH.with_name(RESULT_PATH.stem + "_prepared.json"), result)
    print(json.dumps({"STATUS": "PREPARED", "PRE_MUTATION_Q3_EXTRACTION_CONTRACT_SHA256": pre_sha, "POST_MUTATION_Q3_EXTRACTION_CONTRACT_SHA256": post_sha, "REFINEMENT_CONTRACT_SHA256": refinement_sha, "REFINEMENT_EVIDENCE_FINGERPRINT": evidence_fingerprint, "VALIDATION_PATH": str(VALIDATION_PATH), "PAGE_23_OLD_SANITY_STATUS": rows[0]["old_sanity_status"], "PAGE_23_NEW_SANITY_STATUS": rows[0]["new_sanity_status"], "PAGE_23_OCR_TEXT_CHANGED": result["PAGE_23_OCR_TEXT_CHANGED"]}, ensure_ascii=False))
    return result


def finalize() -> dict[str, Any]:
    if not VALIDATION_PATH.is_file():
        raise RuntimeError("BINARY_MATRIX_VALIDATION_EVIDENCE_MISSING")
    prepared = read_json(RESULT_PATH.with_name(RESULT_PATH.stem + "_prepared.json"))
    extraction = read_json(EXTRACTION_PATH)
    refinement_sha, evidence_fingerprint = pilot.refinement_fingerprint()
    if extraction.get("refinement_contract_sha256") != refinement_sha or extraction.get("refinement_evidence_fingerprint") != evidence_fingerprint:
        raise RuntimeError("EXTRACTION_CONTRACT_NOT_BOUND_TO_FROZEN_REFINEMENT")
    q3_sha = pilot.sha256_file(EXTRACTION_PATH)
    rows = read_csv(VALIDATION_PATH)
    if any(row.get("deterministic_evidence_pass") != "1" for row in rows):
        raise RuntimeError("BINARY_MATRIX_VALIDATION_FAILED")
    result = dict(prepared)
    result.update({"STATUS": "PASS", "REFINEMENT_CONTRACT_SHA256": refinement_sha, "REFINEMENT_EVIDENCE_FINGERPRINT": evidence_fingerprint, "Q3_EXTRACTION_CONTRACT_UPDATED": 1, "Q3_EXTRACTION_CONTRACT_SHA256": q3_sha, "BATCH_PERSISTENCE_DELETED_COUNT": 0, "BATCH_REPLAY_REQUIRED": 0})
    atomic_write_json(RESULT_PATH, result)
    plan = {
        "STAGE": "G8-Q3-BATCH-REVALIDATE-UNDER-FROZEN-CONTRACT", "STATUS": "PLANNED", "target_count": 128,
        "target_source": "catalog/scale/g8_q3_batch_repair/", "refinement_contract_sha256": refinement_sha,
        "refinement_evidence_fingerprint": evidence_fingerprint, "q3_extraction_contract_sha256": q3_sha,
        "batch_replay_required": 0, "ocr_replay_page_count": 0, "body_reconstruction_required": 0,
        "batch_persistence_deleted_count": 0,
        "checks": ["source SHA", "page count", "authoritative page hashes", "OCR provenance", "page text quality", "body hash", "body quality", "binary-matrix-aware sanity", "collision gate", "provenance", "persistence structure"],
        "policy": "Do not replace persisted contract SHA fields directly; validate all 128 identities before any rebinding.",
    }
    atomic_write_json(PLAN_PATH, plan)
    report_lines = [
        "# G8 Q3 Binary Matrix OCR Sanity Refinement", "", *[f"{key}={value}" for key, value in result.items() if key != "CONTRACT_MUTATION_FIELDS"],
        "", "CONTRACT_MUTATION_FIELDS=" + json.dumps(result["CONTRACT_MUTATION_FIELDS"], ensure_ascii=False),
        "", "## Outputs", "", *[f"- `{path.relative_to(ROOT).as_posix()}`" for path in (RESULT_PATH, VALIDATION_PATH, PLAN_PATH, REPORT_PATH)],
        "", "## Validation", "", "- Persisted page-23 OCR text and OCR audit hash are unchanged; only acceptance semantics changed.",
        "- Binary positive and all negative synthetic fixtures passed their expected sanity outcomes.",
        "- No OCR replay, full batch replay, persistence deletion, formal artifact generation, network, dependency, Word, or Git operation was performed.",
        "", "## Revalidation", "", "- All 128 persisted identities are frozen as the next-stage revalidation target.",
        "- Content, routing, normalization, and reconstruction are unchanged; lightweight revalidation is permitted.",
    ]
    atomic_write_text(REPORT_PATH, "\n".join(report_lines) + "\n")
    print(json.dumps({"STATUS": "PASS", "REFINEMENT_CONTRACT_SHA256": refinement_sha, "REFINEMENT_EVIDENCE_FINGERPRINT": evidence_fingerprint, "Q3_EXTRACTION_CONTRACT_SHA256": q3_sha, "PLAN_PATH": str(PLAN_PATH)}, ensure_ascii=False))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--finalize", action="store_true")
    args = parser.parse_args()
    if args.prepare == args.finalize:
        raise SystemExit("choose exactly one of --prepare or --finalize")
    prepare_validation() if args.prepare else finalize()


if __name__ == "__main__":
    main()
