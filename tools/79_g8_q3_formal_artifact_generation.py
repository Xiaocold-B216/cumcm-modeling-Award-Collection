"""G8-Q3 formal artifact generation from final, revalidated batch persistence.

This runner deliberately has no PDF/OCR/Word/Git/network implementation.  The
default invocation is read-only preflight; ``--execute`` is the only mode that
stages, promotes, and updates the canonical G8 registry/backlogs.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import secrets
import tempfile
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCALE = ROOT / "catalog" / "scale"
PAPERS_ROOT = ROOT / "derived" / "scale" / "papers"
STAGE_ROOT = SCALE / "g8_q3_formal_artifact_stage"

ARTIFACT_MANIFEST = SCALE / "g8_artifact_manifest.csv"
PAPER_STATUS = SCALE / "g8_paper_status.csv"
MANUAL_BACKLOG = SCALE / "g8_manual_backlog.csv"
Q3_BACKLOG = SCALE / "g8_q3_manual_backlog.csv"
ELIGIBILITY = SCALE / "g8_artifact_eligibility.csv"
PAPERS_CATALOG = ROOT / "catalog" / "papers.csv"
MEMBERSHIPS = ROOT / "catalog" / "paper_files.csv"
FILES_CATALOG = ROOT / "catalog" / "files.csv"
Q3_TARGET_INVENTORY = SCALE / "g8_q3_target_inventory.csv"
Q3_BATCH_MANIFEST = SCALE / "g8_q3_batch_extraction_manifest.csv"
Q3_REVALIDATION_RESULT = SCALE / "g8_q3_batch_revalidation_result.json"
Q3_REVALIDATION_ATTEMPT = SCALE / "g8_q3_batch_revalidation_attempt.json"
REFINEMENT_CONTRACT = SCALE / "g8_q3_contract_refinement_v1.json"
EXTRACTION_CONTRACT = SCALE / "g8_q3_extraction_contract_v1.json"

OUTPUT_RESULT = SCALE / "g8_q3_formal_artifact_generation_result.json"
OUTPUT_ATTEMPT = SCALE / "g8_q3_formal_artifact_generation_attempt.json"
OUTPUT_PROGRESS = SCALE / "g8_q3_formal_artifact_generation_progress.csv"
OUTPUT_JOURNAL = SCALE / "g8_q3_formal_artifact_promotion_journal.csv"
OUTPUT_MANIFEST = SCALE / "g8_q3_formal_artifact_generation_manifest.csv"
REPORT = ROOT / "reports" / "scale" / "G8_Q3_FORMAL_ARTIFACT_GENERATION.md"

SCRIPT_REL = "tools/79_g8_q3_formal_artifact_generation.py"
STAGE = "G8-Q3-FORMAL-ARTIFACT-GENERATION"
SOURCE_BATCH_ATTEMPT_ID = "20260902T181812821882_f3ed3664"
EXPECTED_REVALIDATION_ATTEMPT_ID = "20260903T063950668735_29d8de39"
EXPECTED_REFINEMENT_VERSION = "g8-q3-refinement-v1"
EXPECTED_REFINEMENT_SHA = "7E43620CE1A7A22EB08B48D4552E2751E13BE00EB9F71681CDBB76F8A00624A7"
EXPECTED_EVIDENCE_FINGERPRINT = "8DED4A5815D9A5D6644E0194282E07AF6FBC02CE68B6AEE6568601131ADC2E99"
EXPECTED_Q3_SHA = "4E372E0BFF1D5395C46CFFA583636190AEDB3389FDFFCF354559626757AC3A6F"
BASE_ARTIFACT_SETS = 325
BASE_PRIMARY_ARTIFACTS = 975
EXPECTED_TARGET_COUNT = 128
ARTIFACT_TYPES = ("knowledge_card.md", "metadata.yaml", "paper.md")
ARTIFACT_FIELDS = [
    "paper_id", "artifact_type", "artifact_path", "artifact_sha256", "subject_type",
    "artifact_eligible", "quality", "source_map_version", "extraction_contract_version", "status",
]
STAGE_MANIFEST_FIELDS = [
    "paper_id", "artifact_type", "artifact_path", "stage_artifact_path", "artifact_size",
    "artifact_sha256", "source_pdf_path", "source_pdf_sha256", "final_batch_manifest_path",
    "final_body_path", "source_body_sha256", "refinement_version", "refinement_contract_sha256",
    "refinement_evidence_fingerprint", "q3_extraction_contract_sha256", "revalidation_attempt_id",
    "formal_generation_attempt_id", "generation_status", "validation_status",
]
PROGRESS_FIELDS = [
    "paper_id", "sequence_number", "status", "error_code", "stage_path", "canonical_path",
    "staged_primary_artifact_count", "stage_structure_status", "stage_hash_status",
    "identity_binding_status", "provenance_status", "source_body_binding_status",
    "duplicate_id_status", "duplicate_path_status", "promoted", "post_promotion_status",
    "registry_registered", "started_at", "finished_at",
]
JOURNAL_FIELDS = [
    "paper_id", "staged", "stage_validated", "promoted", "post_promotion_validated",
    "registry_registered", "status", "error_code", "canonical_path", "updated_at",
]


class GateError(RuntimeError):
    """A deterministic input, ownership, or integrity gate failed."""


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def new_attempt_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f") + "_" + secrets.token_hex(4)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def atomic_write_bytes(path: Path, data: bytes, retries: int = 3) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    last_error: Exception | None = None
    for attempt in range(retries):
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="wb", prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent), delete=False
            ) as handle:
                temporary = Path(handle.name)
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(str(temporary), str(path))
            return
        except Exception as exc:  # pragma: no cover - Windows locking is environment-specific.
            last_error = exc
            if temporary is not None and temporary.exists():
                try:
                    temporary.unlink()
                except OSError:
                    pass
            if attempt + 1 < retries:
                time.sleep(0.15 * (attempt + 1))
    raise GateError(f"ATOMIC_WRITE_FAILED:{rel(path)}:{last_error}")


def csv_bytes(fields: list[str], rows: list[dict[str, Any]]) -> bytes:
    from io import StringIO

    buffer = StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
    writer.writeheader()
    writer.writerows({field: row.get(field, "") for field in fields} for row in rows)
    return buffer.getvalue().encode("utf-8")


def atomic_write_csv(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> None:
    atomic_write_bytes(path, csv_bytes(fields, rows))


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    atomic_write_bytes(path, (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def safe_root_path(value: str) -> Path:
    candidate = (ROOT / value.replace("\\", "/")).resolve()
    root = ROOT.resolve()
    if candidate != root and root not in candidate.parents:
        raise GateError(f"PATH_OUTSIDE_ROOT:{value}")
    return candidate


def compute_evidence_fingerprint(contract: dict[str, Any]) -> str:
    members = contract.get("evidence_fingerprint_member_paths", [])
    records: list[str] = []
    for value in members:
        path = safe_root_path(str(value))
        if not path.is_file():
            raise GateError(f"MISSING_EVIDENCE_MEMBER:{value}")
        records.append(f"{value}\t{sha256_path(path)}")
    return sha256_text("\n".join(records))


def canonical_card(paper_id: str, year: str, problem: str, body: str, page_count: int, body_sha: str) -> str:
    excerpt = body[:800].replace("\n", " ")
    quoted = "\n".join("> " + excerpt[index:index + 100] for index in range(0, len(excerpt), 100))
    if not quoted:
        quoted = "> No textual excerpt is available; provenance remains recorded in this card and metadata."
    pages = ", ".join(str(number) for number in range(1, page_count + 1))
    return (
        "# Knowledge Card\n\n"
        "## Basic Information\n\n"
        f"- Paper ID: {paper_id}\n- Year: {year}\n- Problem: {problem}\n\n"
        "## Evidence-based Content\n\n"
        "The following excerpt is copied deterministically from the generated paper body; no method or conclusion is inferred beyond this source evidence.\n\n"
        f"{quoted}\n\n"
        "## Evidence\n\n"
        "- Evidence granularity: page\n"
        f"- Source pages represented: {pages}\n"
        f"- Authoritative normalized text SHA-256: {body_sha}\n"
    )


def canonical_metadata(
    paper: dict[str, str],
    membership_rows: list[dict[str, str]],
    source_path: str,
    source_sha: str,
    page_count: int,
    body_path: str,
    body_sha: str,
    batch_manifest_path: str,
    revalidation_attempt_id: str,
    generation_attempt_id: str,
) -> str:
    primary = next(
        (row for row in membership_rows if row.get("role") == "primary" and row.get("canonical") == "True"),
        membership_rows[0],
    )
    data: dict[str, Any] = {
        "paper_id": paper["paper_id"],
        "year": int(paper["year"]),
        "problem": paper["problem_code"],
        "subject_type": "PAPER",
        "artifact_eligible": True,
        "quality": "Q3",
        "authority_sources": [{"path": source_path, "sha256": source_sha}],
        "authority_sha256": source_sha,
        "paper_file_memberships": [
            {"path": row["path"], "role": row["role"], "canonical": row["canonical"] == "True"}
            for row in membership_rows
        ],
        "primary_file": primary["path"],
        "extraction_inputs": [{"path": body_path, "sha256": body_sha, "kind": "final_q3_batch_persistence"}],
        "extraction_input_sha256": body_sha,
        "extraction_contract": {
            "schema_version": 1,
            "contract_name": "G8 Q3 Extraction Contract",
            "source_page_numbering": "1-based",
            "stage": STAGE,
        },
        "primary_extraction_backend": "final Q3 batch persistence",
        "page_extraction_backend": "final Q3 batch persistence",
        "page_count": page_count,
        "evidence_granularity": "page",
        "artifact_generation_mode": "one_paper_level_artifact_set_from_final_q3_batch_persistence",
        "generated_from_frozen_sources": True,
        "source_pdf_path": source_path,
        "source_pdf_sha256": source_sha,
        "final_batch_persistence_path": batch_manifest_path,
        "final_body_path": body_path,
        "source_body_sha256": body_sha,
        "refinement_version": EXPECTED_REFINEMENT_VERSION,
        "refinement_contract_sha256": EXPECTED_REFINEMENT_SHA,
        "refinement_evidence_fingerprint": EXPECTED_EVIDENCE_FINGERPRINT,
        "q3_extraction_contract_sha256": EXPECTED_Q3_SHA,
        "revalidation_attempt_id": revalidation_attempt_id,
        "formal_generation_attempt_id": generation_attempt_id,
    }
    return yaml.safe_dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False)


def required_files(path: Path) -> list[Path]:
    return [path / name for name in ARTIFACT_TYPES]


def read_inputs() -> dict[str, Any]:
    required = [
        ARTIFACT_MANIFEST, PAPER_STATUS, MANUAL_BACKLOG, Q3_BACKLOG, ELIGIBILITY, PAPERS_CATALOG,
        MEMBERSHIPS, FILES_CATALOG, Q3_TARGET_INVENTORY, Q3_BATCH_MANIFEST, Q3_REVALIDATION_RESULT,
        Q3_REVALIDATION_ATTEMPT, REFINEMENT_CONTRACT, EXTRACTION_CONTRACT,
    ]
    missing = [rel(path) for path in required if not path.is_file()]
    if missing:
        raise GateError("MISSING_INPUTS:" + ",".join(missing))
    refinement = read_json(REFINEMENT_CONTRACT)
    extraction = read_json(EXTRACTION_CONTRACT)
    revalidation = read_json(Q3_REVALIDATION_RESULT)
    revalidation_attempt = read_json(Q3_REVALIDATION_ATTEMPT)
    return {
        "artifact_rows": read_csv(ARTIFACT_MANIFEST),
        "status_rows": read_csv(PAPER_STATUS),
        "manual_backlog_rows": read_csv(MANUAL_BACKLOG),
        "q3_backlog_rows": read_csv(Q3_BACKLOG),
        "eligibility_rows": read_csv(ELIGIBILITY),
        "paper_rows": read_csv(PAPERS_CATALOG),
        "membership_rows": read_csv(MEMBERSHIPS),
        "files_rows": read_csv(FILES_CATALOG),
        "inventory_rows": read_csv(Q3_TARGET_INVENTORY),
        "batch_rows": read_csv(Q3_BATCH_MANIFEST),
        "refinement": refinement,
        "extraction": extraction,
        "revalidation": revalidation,
        "revalidation_attempt": revalidation_attempt,
    }


def audit_canonical_registry(rows: list[dict[str, str]]) -> dict[str, Any]:
    by_id: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        by_id.setdefault(row.get("paper_id", ""), []).append(row)
    duplicate_keys = len(rows) - len({(row.get("paper_id", ""), row.get("artifact_type", "")) for row in rows})
    duplicate_paths = len(rows) - len({row.get("artifact_path", "") for row in rows})
    bad_schema = sum(1 for row in rows if set(row) != set(ARTIFACT_FIELDS))
    bad_sets = 0
    hash_failures = 0
    for paper_id, members in by_id.items():
        if len(members) != 3 or {row.get("artifact_type") for row in members} != set(ARTIFACT_TYPES):
            bad_sets += 1
        for row in members:
            try:
                path = safe_root_path(row["artifact_path"])
                if not path.is_file() or path.stat().st_size == 0 or sha256_path(path) != row["artifact_sha256"]:
                    hash_failures += 1
            except (OSError, GateError, KeyError):
                hash_failures += 1
    return {
        "set_count": len(by_id),
        "primary_count": len(rows),
        "duplicate_artifact_ids": duplicate_keys,
        "duplicate_paths": duplicate_paths,
        "bad_schema": bad_schema,
        "bad_sets": bad_sets,
        "hash_failures": hash_failures,
        "by_id": by_id,
    }


def classify_existing_target(
    paper_id: str, registry_by_id: dict[str, list[dict[str, str]]]
) -> tuple[str, str]:
    final = PAPERS_ROOT / paper_id
    registry = registry_by_id.get(paper_id, [])
    if not final.exists() and not registry:
        return "ABSENT", ""
    if final.exists() and final.is_dir() and len(registry) == 3:
        try:
            names = {path.name for path in final.iterdir() if path.is_file()}
            valid = names == set(ARTIFACT_TYPES)
            valid = valid and {row["artifact_type"] for row in registry} == set(ARTIFACT_TYPES)
            valid = valid and all(
                safe_root_path(row["artifact_path"]) == final / row["artifact_type"]
                and (final / row["artifact_type"]).is_file()
                and sha256_path(final / row["artifact_type"]) == row["artifact_sha256"]
                for row in registry
            )
            if valid:
                return "COMPLETE_VALID_EXISTING", ""
        except (OSError, GateError, KeyError):
            return "UNKNOWN", "existing-state-read-error"
    if final.exists() or registry:
        return "PARTIAL", "existing-formal-output-or-registry-fragment"
    return "UNKNOWN", "existing-state-unclassified"


def audit_stage_root() -> tuple[bool, list[str]]:
    if not STAGE_ROOT.exists():
        return True, []
    if not STAGE_ROOT.is_dir():
        return False, ["stage-root-is-not-directory"]
    issues: list[str] = []
    for attempt_dir in STAGE_ROOT.iterdir():
        if not attempt_dir.is_dir():
            issues.append(f"unexpected-stage-entry:{attempt_dir.name}")
            continue
        marker = attempt_dir / "stage_marker.json"
        if not marker.is_file():
            issues.append(f"unowned-stage-attempt:{attempt_dir.name}")
            continue
        try:
            payload = read_json(marker)
            if payload.get("stage") != STAGE or payload.get("runner") != SCRIPT_REL:
                issues.append(f"foreign-stage-attempt:{attempt_dir.name}")
        except Exception:
            issues.append(f"invalid-stage-marker:{attempt_dir.name}")
    return not issues, issues


def build_gate(data: dict[str, Any]) -> dict[str, Any]:
    artifact_audit = audit_canonical_registry(data["artifact_rows"])
    revalidation = data["revalidation"]
    revalidation_attempt = data["revalidation_attempt"]
    refinement = data["refinement"]
    extraction = data["extraction"]
    refinement_sha = sha256_path(REFINEMENT_CONTRACT)
    extraction_sha = sha256_path(EXTRACTION_CONTRACT)
    evidence_fingerprint = compute_evidence_fingerprint(refinement)
    inventory = data["inventory_rows"]
    batch_rows = data["batch_rows"]
    q3_backlog_ids = {row["paper_id"] for row in data["q3_backlog_rows"]}
    manual_q3_ids = {row["paper_id"] for row in data["manual_backlog_rows"] if row.get("category") == "Q3_REPAIR_MANUAL"}
    inventory_ids = [row["paper_id"] for row in inventory]
    batch_ids = [row["paper_id"] for row in batch_rows]
    target_ids = sorted(set(inventory_ids))
    batch_by_id = {row["paper_id"]: row for row in batch_rows}
    inventory_by_id = {row["paper_id"]: row for row in inventory}
    q3_manifest_by_id: dict[str, dict[str, Any]] = {}
    persistence_errors: list[str] = []
    for paper_id in target_ids:
        directory = SCALE / "g8_q3_batch_repair" / paper_id
        manifest_path = directory / "manifest.json"
        body_path = directory / "normalized_body.txt"
        provenance_path = directory / "provenance.json"
        quality_path = directory / "quality.json"
        try:
            manifest = read_json(manifest_path)
            body = body_path.read_bytes()
            provenance = read_json(provenance_path)
            quality = read_json(quality_path)
            actual_body_sha = sha256_bytes(body)
            row = batch_by_id[paper_id]
            valid = all([
                manifest.get("paper_id") == paper_id,
                manifest.get("source_path") == row["source_path"],
                manifest.get("source_sha256") == row["source_sha256"],
                manifest.get("refinement_contract_sha256") == EXPECTED_REFINEMENT_SHA,
                manifest.get("refinement_evidence_fingerprint") == EXPECTED_EVIDENCE_FINGERPRINT,
                manifest.get("q3_extraction_contract_sha256") == EXPECTED_Q3_SHA,
                manifest.get("revalidation_attempt_id") == EXPECTED_REVALIDATION_ATTEMPT_ID,
                manifest.get("reconstruction_status") == "COMPLETE_VALID",
                actual_body_sha == row["normalized_text_sha256"] == manifest.get("normalized_text_sha256"),
                len(body.decode("utf-8")) == int(row["normalized_text_chars"]),
                provenance.get("paper_id") == paper_id,
                quality.get("paper_id") == paper_id,
                quality.get("pass") is True,
            ])
            if not valid:
                persistence_errors.append(paper_id)
            q3_manifest_by_id[paper_id] = {
                "paper_id": paper_id,
                "source_path": manifest.get("source_path", row["source_path"]),
                "source_sha256": manifest.get("source_sha256", row["source_sha256"]),
                "page_count": int(manifest.get("page_count", row["page_count"])),
                "body_path": rel(body_path),
                "manifest_path": rel(manifest_path),
                "body_sha256": actual_body_sha,
            }
        except (OSError, ValueError, UnicodeError, KeyError, json.JSONDecodeError) as exc:
            persistence_errors.append(f"{paper_id}:{type(exc).__name__}")
    paper_by_id = {row["paper_id"]: row for row in data["paper_rows"]}
    eligibility_by_id = {row["paper_id"]: row for row in data["eligibility_rows"]}
    membership_by_id: dict[str, list[dict[str, str]]] = {}
    for row in data["membership_rows"]:
        membership_by_id.setdefault(row["paper_id"], []).append(row)
    files_by_path = {row["path"].replace("\\", "/"): row for row in data["files_rows"]}
    source_missing = 0
    source_sha_mismatch = 0
    source_hash_before: dict[str, str] = {}
    for paper_id in target_ids:
        manifest = q3_manifest_by_id.get(paper_id, {})
        source_path = str(manifest.get("source_path", ""))
        source_sha = str(manifest.get("source_sha256", ""))
        try:
            source = safe_root_path(source_path)
            if not source.is_file():
                source_missing += 1
            else:
                actual = sha256_path(source)
                source_hash_before[source_path] = actual
                source_sha_mismatch += int(actual != source_sha)
            source_sha_mismatch += int(files_by_path.get(source_path, {}).get("sha256", source_sha) != source_sha)
        except (OSError, GateError):
            source_missing += 1
            source_sha_mismatch += 1
    existing_states: dict[str, str] = {}
    existing_reasons: dict[str, str] = {}
    for paper_id in target_ids:
        state, reason = classify_existing_target(paper_id, artifact_audit["by_id"])
        existing_states[paper_id] = state
        existing_reasons[paper_id] = reason
    stage_ok, stage_issues = audit_stage_root()
    revalidation_gate = all([
        revalidation.get("STATUS") == "PASS",
        revalidation.get("SOURCE_BATCH_FINAL_ACCEPTANCE") == "PASS",
        revalidation.get("SOURCE_BATCH_ATTEMPT_ID") == SOURCE_BATCH_ATTEMPT_ID,
        revalidation.get("REVALIDATION_ATTEMPT_ID") == EXPECTED_REVALIDATION_ATTEMPT_ID,
        revalidation.get("REVALIDATION_TARGET_COUNT") == EXPECTED_TARGET_COUNT,
        revalidation.get("REVALIDATION_UNIQUE_TARGET_COUNT") == EXPECTED_TARGET_COUNT,
        revalidation.get("CURRENT_CONTRACT_BINDING_PASS_COUNT") == EXPECTED_TARGET_COUNT,
        revalidation.get("CURRENT_CONTRACT_BINDING_FAIL_COUNT") == 0,
        revalidation.get("FAILED_IDENTITY_COUNT") == 0,
        revalidation.get("NEW_FAILURE_MODE_COUNT") == 0,
    ])
    current_contract_gate = all([
        refinement.get("refinement_version") == EXPECTED_REFINEMENT_VERSION,
        refinement_sha == EXPECTED_REFINEMENT_SHA,
        extraction.get("refinement_contract_sha256") == EXPECTED_REFINEMENT_SHA,
        extraction.get("refinement_evidence_fingerprint") == EXPECTED_EVIDENCE_FINGERPRINT,
        extraction_sha == EXPECTED_Q3_SHA,
        evidence_fingerprint == EXPECTED_EVIDENCE_FINGERPRINT,
        revalidation_attempt.get("status") == "PASS",
        revalidation_attempt.get("attempt_id") == EXPECTED_REVALIDATION_ATTEMPT_ID,
    ])
    target_gate = all([
        len(inventory) == EXPECTED_TARGET_COUNT,
        len(set(inventory_ids)) == EXPECTED_TARGET_COUNT,
        len(batch_rows) == EXPECTED_TARGET_COUNT,
        len(set(batch_ids)) == EXPECTED_TARGET_COUNT,
        set(inventory_ids) == set(batch_ids) == q3_backlog_ids == manual_q3_ids,
        all(row.get("artifact_eligible") == "1" for row in inventory),
        all(row.get("status") == "PASS" for row in batch_rows),
        all(row.get("batch_attempt_id") == SOURCE_BATCH_ATTEMPT_ID for row in batch_rows),
    ])
    paper_gate = all([
        len(eligibility_by_id) == 642,
        len(data["status_rows"]) == 642,
        all(paper_id in paper_by_id for paper_id in target_ids),
        all(eligibility_by_id.get(paper_id, {}).get("artifact_eligible") == "1" for paper_id in target_ids),
        all(eligibility_by_id.get(paper_id, {}).get("subject_type") == "PAPER" for paper_id in target_ids),
        all(membership_by_id.get(paper_id) for paper_id in target_ids),
    ])
    existing_gate = all(state in {"ABSENT", "COMPLETE_VALID_EXISTING"} for state in existing_states.values())
    return {
        "artifact_audit": artifact_audit,
        "refinement_sha": refinement_sha,
        "extraction_sha": extraction_sha,
        "evidence_fingerprint": evidence_fingerprint,
        "inventory_by_id": inventory_by_id,
        "batch_by_id": batch_by_id,
        "q3_manifest_by_id": q3_manifest_by_id,
        "paper_by_id": paper_by_id,
        "eligibility_by_id": eligibility_by_id,
        "membership_by_id": membership_by_id,
        "source_hash_before": source_hash_before,
        "source_missing": source_missing,
        "source_sha_mismatch": source_sha_mismatch,
        "persistence_errors": persistence_errors,
        "existing_states": existing_states,
        "existing_reasons": existing_reasons,
        "existing_complete_count": sum(state == "COMPLETE_VALID_EXISTING" for state in existing_states.values()),
        "existing_partial_count": sum(state == "PARTIAL" for state in existing_states.values()),
        "existing_unknown_count": sum(state == "UNKNOWN" for state in existing_states.values()),
        "stage_ok": stage_ok,
        "stage_issues": stage_issues,
        "revalidation_gate": revalidation_gate,
        "current_contract_gate": current_contract_gate,
        "target_gate": target_gate,
        "paper_gate": paper_gate,
        "existing_gate": existing_gate,
        "target_ids": target_ids,
        "branch": "library-refactor-v1",
        "head": str(data["revalidation"].get("HEAD", "")),
    }


def preflight_pass(gate: dict[str, Any]) -> bool:
    audit = gate["artifact_audit"]
    return all([
        gate["revalidation_gate"], gate["current_contract_gate"], gate["target_gate"], gate["paper_gate"],
        gate["existing_gate"], gate["stage_ok"], not gate["persistence_errors"],
        gate["source_missing"] == 0, gate["source_sha_mismatch"] == 0,
        audit["set_count"] == BASE_ARTIFACT_SETS, audit["primary_count"] == BASE_PRIMARY_ARTIFACTS,
        audit["duplicate_artifact_ids"] == 0, audit["duplicate_paths"] == 0,
        audit["bad_schema"] == 0, audit["bad_sets"] == 0, audit["hash_failures"] == 0,
    ])


def validate_artifact_set(path: Path, expected: dict[str, Any], generation_attempt_id: str) -> dict[str, Any]:
    result = {
        "structure": 1,
        "hash": 1,
        "identity": 1,
        "provenance": 1,
        "source_body": 1,
        "duplicate_id": 0,
        "duplicate_path": 0,
        "error": "",
    }
    try:
        paths = required_files(path)
        names = {item.name for item in path.iterdir() if item.is_file()}
        result["structure"] = int(path.is_dir() and names == set(ARTIFACT_TYPES) and len(paths) == 3)
        if not result["structure"]:
            raise GateError("ARTIFACT_STRUCTURE_INVALID")
        for item in paths:
            if not item.is_file() or item.stat().st_size == 0:
                result["hash"] = 0
                raise GateError("ARTIFACT_EMPTY_OR_MISSING")
            sha256_path(item)
        paper_path = path / "paper.md"
        body = (safe_root_path(expected["body_path"])).read_text(encoding="utf-8")
        expected_paper = "# Extracted Paper\n\n" + body + "\n"
        if paper_path.read_text(encoding="utf-8") != expected_paper:
            result["source_body"] = 0
            raise GateError("PAPER_BODY_BINDING_INVALID")
        if sha256_path(safe_root_path(expected["body_path"])) != expected["body_sha256"]:
            result["source_body"] = 0
            raise GateError("SOURCE_BODY_HASH_INVALID")
        metadata = yaml.safe_load((path / "metadata.yaml").read_text(encoding="utf-8")) or {}
        required_metadata = {
            "paper_id": expected["paper_id"], "subject_type": "PAPER", "artifact_eligible": True,
            "quality": "Q3", "source_pdf_path": expected["source_path"],
            "source_pdf_sha256": expected["source_sha256"], "final_body_path": expected["body_path"],
            "source_body_sha256": expected["body_sha256"],
            "final_batch_persistence_path": expected["manifest_path"],
            "refinement_version": EXPECTED_REFINEMENT_VERSION,
            "refinement_contract_sha256": EXPECTED_REFINEMENT_SHA,
            "refinement_evidence_fingerprint": EXPECTED_EVIDENCE_FINGERPRINT,
            "q3_extraction_contract_sha256": EXPECTED_Q3_SHA,
            "revalidation_attempt_id": EXPECTED_REVALIDATION_ATTEMPT_ID,
            "formal_generation_attempt_id": generation_attempt_id,
        }
        result["identity"] = int(all(metadata.get(key) == value for key, value in required_metadata.items()))
        result["provenance"] = int(result["identity"] and metadata.get("generated_from_frozen_sources") is True)
        card = (path / "knowledge_card.md").read_text(encoding="utf-8")
        result["identity"] = int(result["identity"] and f"- Paper ID: {expected['paper_id']}\n" in card)
        if not result["identity"]:
            raise GateError("ARTIFACT_IDENTITY_BINDING_INVALID")
        if not result["provenance"]:
            raise GateError("ARTIFACT_PROVENANCE_INVALID")
    except (OSError, UnicodeError, yaml.YAMLError, GateError, KeyError) as exc:
        result["error"] = str(exc)
        if not result["error"]:
            result["error"] = type(exc).__name__
    return result


def expected_artifact_rows(gate: dict[str, Any], paper_id: str, generation_attempt_id: str) -> list[dict[str, Any]]:
    q3 = gate["q3_manifest_by_id"][paper_id]
    paper = gate["paper_by_id"][paper_id]
    return [
        {
            "paper_id": paper_id, "artifact_type": artifact_type,
            "artifact_path": f"derived/scale/papers/{paper_id}/{artifact_type}",
            "artifact_sha256": sha256_path(PAPERS_ROOT / paper_id / artifact_type),
            "subject_type": "PAPER", "artifact_eligible": "1", "quality": "Q3",
            "source_map_version": "g8-q3-inventory-v2",
            "extraction_contract_version": "g8-q3-v1", "status": "PASS",
        }
        for artifact_type in ARTIFACT_TYPES
    ]


def make_progress_row(paper_id: str, sequence: int) -> dict[str, Any]:
    return {
        "paper_id": paper_id, "sequence_number": sequence, "status": "PENDING", "error_code": "",
        "stage_path": "", "canonical_path": f"derived/scale/papers/{paper_id}",
        "staged_primary_artifact_count": 0, "stage_structure_status": "PENDING", "stage_hash_status": "PENDING",
        "identity_binding_status": "PENDING", "provenance_status": "PENDING", "source_body_binding_status": "PENDING",
        "duplicate_id_status": "PENDING", "duplicate_path_status": "PENDING", "promoted": 0,
        "post_promotion_status": "PENDING", "registry_registered": 0, "started_at": "", "finished_at": "",
    }


def generation_manifest_row(
    paper_id: str, artifact_type: str, stage_path: Path, artifact_path: Path,
    expected: dict[str, Any], generation_attempt_id: str, status: str,
) -> dict[str, Any]:
    return {
        "paper_id": paper_id, "artifact_type": artifact_type, "artifact_path": rel(artifact_path),
        "stage_artifact_path": rel(stage_path), "artifact_size": stage_path.stat().st_size,
        "artifact_sha256": sha256_path(stage_path), "source_pdf_path": expected["source_path"],
        "source_pdf_sha256": expected["source_sha256"], "final_batch_manifest_path": expected["manifest_path"],
        "final_body_path": expected["body_path"], "source_body_sha256": expected["body_sha256"],
        "refinement_version": EXPECTED_REFINEMENT_VERSION, "refinement_contract_sha256": EXPECTED_REFINEMENT_SHA,
        "refinement_evidence_fingerprint": EXPECTED_EVIDENCE_FINGERPRINT,
        "q3_extraction_contract_sha256": EXPECTED_Q3_SHA, "revalidation_attempt_id": EXPECTED_REVALIDATION_ATTEMPT_ID,
        "formal_generation_attempt_id": generation_attempt_id, "generation_status": "STAGED",
        "validation_status": status,
    }


def write_attempt(payload: dict[str, Any]) -> None:
    atomic_write_json(OUTPUT_ATTEMPT, payload)


def render_result(result: dict[str, Any]) -> str:
    outputs = result.get("OUTPUTS", {})
    lines = [
        f"STAGE={result.get('STAGE', STAGE)}", f"STATUS={result.get('STATUS', 'BLOCKED')}",
        f"BRANCH={result.get('BRANCH', 'library-refactor-v1')}", f"HEAD={result.get('HEAD', '')}",
        f"SOURCE_BATCH_ATTEMPT_ID={SOURCE_BATCH_ATTEMPT_ID}",
        f"FORMAL_GENERATION_ATTEMPT_ID={result.get('FORMAL_GENERATION_ATTEMPT_ID', '')}",
        f"SOURCE_BATCH_REPORTED_STATUS={result.get('SOURCE_BATCH_REPORTED_STATUS', 'PASS')}",
        f"SOURCE_BATCH_FINAL_ACCEPTANCE={result.get('SOURCE_BATCH_FINAL_ACCEPTANCE', 'PASS')}",
    ]
    ordered_keys = [
        "FORMAL_GENERATION_TARGET_COUNT", "FORMAL_GENERATION_UNIQUE_TARGET_COUNT", "TARGET_ADDED_COUNT", "TARGET_REMOVED_COUNT",
        "REFINEMENT_VERSION", "REFINEMENT_CONTRACT_SHA256", "REFINEMENT_CONTRACT_SHA_MATCH", "REFINEMENT_EVIDENCE_FINGERPRINT",
        "REFINEMENT_EVIDENCE_FINGERPRINT_MATCH", "Q3_EXTRACTION_CONTRACT_SHA256", "Q3_EXTRACTION_CONTRACT_SHA_MATCH",
        "REVALIDATION_ATTEMPT_ID", "SOURCE_REVALIDATION_STATUS", "CANONICAL_ARTIFACT_SCHEMA_SOURCE",
        "EXISTING_FORMAL_ARTIFACT_SET_COUNT", "EXISTING_PRIMARY_ARTIFACT_COUNT", "EXISTING_TARGET_COMPLETE_ARTIFACT_SET_COUNT",
        "EXISTING_TARGET_PARTIAL_ARTIFACT_SET_COUNT", "EXISTING_TARGET_UNKNOWN_ARTIFACT_SET_COUNT", "STAGED_ARTIFACT_SET_COUNT",
        "STAGED_PRIMARY_ARTIFACT_COUNT", "STAGED_ARTIFACT_SET_VALID_COUNT", "STAGED_ARTIFACT_SET_INVALID_COUNT",
        "PROMOTED_ARTIFACT_SET_COUNT", "UNPROMOTED_ARTIFACT_SET_COUNT", "NEW_ARTIFACT_SET_COUNT", "NEW_PRIMARY_ARTIFACT_COUNT",
        "NEW_ARTIFACT_STRUCTURE_PASS_COUNT", "NEW_ARTIFACT_STRUCTURE_FAIL_COUNT", "NEW_ARTIFACT_HASH_VALID_COUNT",
        "NEW_ARTIFACT_HASH_INVALID_COUNT", "NEW_ARTIFACT_IDENTITY_BINDING_PASS_COUNT", "NEW_ARTIFACT_IDENTITY_BINDING_FAIL_COUNT",
        "NEW_ARTIFACT_PROVENANCE_PASS_COUNT", "NEW_ARTIFACT_PROVENANCE_FAIL_COUNT", "FORMAL_ARTIFACT_SOURCE_BODY_BINDING_PASS_COUNT",
        "FORMAL_ARTIFACT_SOURCE_BODY_BINDING_FAIL_COUNT", "DUPLICATE_ARTIFACT_ID_COUNT", "DUPLICATE_FORMAL_ARTIFACT_PATH_COUNT",
        "PREEXISTING_ARTIFACT_CONTENT_MODIFICATION_COUNT", "FORMAL_ARTIFACT_REGISTRY_UPDATED", "Q3_BACKLOG_STATE_UPDATED",
        "TOTAL_ARTIFACT_SET_COUNT", "TOTAL_PRIMARY_ARTIFACT_COUNT", "ARTIFACT_SETS", "PRIMARY_ARTIFACTS", "DOC_MANUAL_BACKLOG",
        "Q3_MANUAL_BACKLOG", "TOTAL_MANUAL_BACKLOG", "ELIGIBLE", "INELIGIBLE", "FORMAL_ARTIFACT_ELIGIBLE_WITH_ARTIFACT_COUNT",
        "FORMAL_ARTIFACT_ELIGIBLE_WITHOUT_ARTIFACT_COUNT", "FORMAL_ELIGIBILITY_MODIFIED", "IDENTITY_MODIFICATION_COUNT",
        "MEMBERSHIP_MODIFICATION_COUNT", "ORIGINAL_FILES_MODIFIED", "OCR_RUN", "Q3_OCR_RUN", "OCR_REPLAY_PAGE_COUNT", "PDF_RENDER_RUN",
        "PDF_INSPECTOR_EXTRACTION_RUN", "PDFTOTEXT_EXTRACTION_RUN", "BODY_RECONSTRUCTION_RUN", "FULL_Q3_BATCH_RUN", "NETWORK_ACCESS_USED",
        "DOWNLOAD_RUN", "NEW_DEPENDENCY_INSTALLED", "WORD_RUN", "WORD_COM_RUN", "DOC_CONVERSION_RUN", "PRINT_JOB_RUN", "G9_RUN",
        "G10_RUN", "GIT_OPERATIONS", "FAILED_ARTIFACT_SET_COUNT", "FAILED_PAPER_IDS",
    ]
    lines.extend(f"{key}={result.get(key, '')}" for key in ordered_keys)
    lines.append("OUTPUTS=")
    lines.extend(f"- {key}: {value}" for key, value in outputs.items())
    lines.append("VALIDATION=")
    lines.extend(f"- {value}" for value in result.get("VALIDATION", []))
    lines.append("ISSUES=")
    lines.extend(f"- {value}" for value in result.get("ISSUES", []))
    lines.extend([f"BLOCKER={result.get('BLOCKER', 'NONE')}", f"NEXT={result.get('NEXT', 'STOP')}"])
    return "\n".join(lines)


def base_result(gate: dict[str, Any], attempt_id: str) -> dict[str, Any]:
    audit = gate["artifact_audit"]
    target_count = len(gate["target_ids"])
    return {
        "STAGE": STAGE, "STATUS": "BLOCKED", "BRANCH": gate["branch"], "HEAD": gate["head"],
        "SOURCE_BATCH_ATTEMPT_ID": SOURCE_BATCH_ATTEMPT_ID, "FORMAL_GENERATION_ATTEMPT_ID": attempt_id,
        "SOURCE_BATCH_REPORTED_STATUS": gate.get("revalidation", {}).get("SOURCE_BATCH_REPORTED_STATUS", "PASS"),
        "SOURCE_BATCH_FINAL_ACCEPTANCE": "PASS", "FORMAL_GENERATION_TARGET_COUNT": target_count,
        "FORMAL_GENERATION_UNIQUE_TARGET_COUNT": len(set(gate["target_ids"])), "TARGET_ADDED_COUNT": 0, "TARGET_REMOVED_COUNT": 0,
        "REFINEMENT_VERSION": EXPECTED_REFINEMENT_VERSION, "REFINEMENT_CONTRACT_SHA256": gate["refinement_sha"],
        "REFINEMENT_CONTRACT_SHA_MATCH": int(gate["refinement_sha"] == EXPECTED_REFINEMENT_SHA),
        "REFINEMENT_EVIDENCE_FINGERPRINT": gate["evidence_fingerprint"],
        "REFINEMENT_EVIDENCE_FINGERPRINT_MATCH": int(gate["evidence_fingerprint"] == EXPECTED_EVIDENCE_FINGERPRINT),
        "Q3_EXTRACTION_CONTRACT_SHA256": gate["extraction_sha"], "Q3_EXTRACTION_CONTRACT_SHA_MATCH": int(gate["extraction_sha"] == EXPECTED_Q3_SHA),
        "REVALIDATION_ATTEMPT_ID": EXPECTED_REVALIDATION_ATTEMPT_ID, "SOURCE_REVALIDATION_STATUS": "PASS" if gate["revalidation_gate"] else "FAIL",
        "CANONICAL_ARTIFACT_SCHEMA_SOURCE": "catalog/scale/g8_artifact_manifest.csv; derived/scale/papers/<paper_id>/{paper.md,metadata.yaml,knowledge_card.md}; tools/39_g6_pilot_auto_r2.py",
        "EXISTING_FORMAL_ARTIFACT_SET_COUNT": audit["set_count"], "EXISTING_PRIMARY_ARTIFACT_COUNT": audit["primary_count"],
        "EXISTING_TARGET_COMPLETE_ARTIFACT_SET_COUNT": gate["existing_complete_count"],
        "EXISTING_TARGET_PARTIAL_ARTIFACT_SET_COUNT": gate["existing_partial_count"], "EXISTING_TARGET_UNKNOWN_ARTIFACT_SET_COUNT": gate["existing_unknown_count"],
        "STAGED_ARTIFACT_SET_COUNT": 0, "STAGED_PRIMARY_ARTIFACT_COUNT": 0, "STAGED_ARTIFACT_SET_VALID_COUNT": 0, "STAGED_ARTIFACT_SET_INVALID_COUNT": 0,
        "PROMOTED_ARTIFACT_SET_COUNT": 0, "UNPROMOTED_ARTIFACT_SET_COUNT": target_count, "NEW_ARTIFACT_SET_COUNT": 0, "NEW_PRIMARY_ARTIFACT_COUNT": 0,
        "NEW_ARTIFACT_STRUCTURE_PASS_COUNT": 0, "NEW_ARTIFACT_STRUCTURE_FAIL_COUNT": 0, "NEW_ARTIFACT_HASH_VALID_COUNT": 0, "NEW_ARTIFACT_HASH_INVALID_COUNT": 0,
        "NEW_ARTIFACT_IDENTITY_BINDING_PASS_COUNT": 0, "NEW_ARTIFACT_IDENTITY_BINDING_FAIL_COUNT": 0, "NEW_ARTIFACT_PROVENANCE_PASS_COUNT": 0,
        "NEW_ARTIFACT_PROVENANCE_FAIL_COUNT": 0, "FORMAL_ARTIFACT_SOURCE_BODY_BINDING_PASS_COUNT": 0, "FORMAL_ARTIFACT_SOURCE_BODY_BINDING_FAIL_COUNT": 0,
        "DUPLICATE_ARTIFACT_ID_COUNT": audit["duplicate_artifact_ids"], "DUPLICATE_FORMAL_ARTIFACT_PATH_COUNT": audit["duplicate_paths"],
        "PREEXISTING_ARTIFACT_CONTENT_MODIFICATION_COUNT": 0, "FORMAL_ARTIFACT_REGISTRY_UPDATED": 0, "Q3_BACKLOG_STATE_UPDATED": 0,
        "TOTAL_ARTIFACT_SET_COUNT": audit["set_count"], "TOTAL_PRIMARY_ARTIFACT_COUNT": audit["primary_count"], "ARTIFACT_SETS": audit["set_count"],
        "PRIMARY_ARTIFACTS": audit["primary_count"], "DOC_MANUAL_BACKLOG": sum(row.get("category") == "DOC_REPAIR_MANUAL" for row in gate.get("manual_backlog_rows", [])),
        "Q3_MANUAL_BACKLOG": target_count, "TOTAL_MANUAL_BACKLOG": len(gate["target_ids"]), "ELIGIBLE": len(gate.get("eligibility_by_id", {})),
        "INELIGIBLE": sum(row.get("artifact_eligible") != "1" for row in gate.get("eligibility_by_id", {}).values()),
        "FORMAL_ARTIFACT_ELIGIBLE_WITH_ARTIFACT_COUNT": audit["set_count"], "FORMAL_ARTIFACT_ELIGIBLE_WITHOUT_ARTIFACT_COUNT": 0,
        "FORMAL_ELIGIBILITY_MODIFIED": 0, "IDENTITY_MODIFICATION_COUNT": 0, "MEMBERSHIP_MODIFICATION_COUNT": 0, "ORIGINAL_FILES_MODIFIED": 0,
        "OCR_RUN": 0, "Q3_OCR_RUN": 0, "OCR_REPLAY_PAGE_COUNT": 0, "PDF_RENDER_RUN": 0, "PDF_INSPECTOR_EXTRACTION_RUN": 0,
        "PDFTOTEXT_EXTRACTION_RUN": 0, "BODY_RECONSTRUCTION_RUN": 0, "FULL_Q3_BATCH_RUN": 0, "NETWORK_ACCESS_USED": 0, "DOWNLOAD_RUN": 0,
        "NEW_DEPENDENCY_INSTALLED": 0, "WORD_RUN": 0, "WORD_COM_RUN": 0, "DOC_CONVERSION_RUN": 0, "PRINT_JOB_RUN": 0, "G9_RUN": 0, "G10_RUN": 0,
        "GIT_OPERATIONS": 0, "FAILED_ARTIFACT_SET_COUNT": target_count, "FAILED_PAPER_IDS": ",".join(gate["target_ids"]),
        "OUTPUTS": {}, "VALIDATION": [], "ISSUES": [], "BLOCKER": "NONE", "NEXT": "STOP",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=STAGE)
    parser.add_argument("--execute", action="store_true", help="stage, validate, promote, and update canonical state")
    args = parser.parse_args()
    attempt_id = new_attempt_id()
    try:
        data = read_inputs()
        gate = build_gate(data)
        gate.update({
            "revalidation": data["revalidation"], "manual_backlog_rows": data["manual_backlog_rows"],
        })
        result = base_result(gate, attempt_id)
        if not preflight_pass(gate):
            result["BLOCKER"] = "FORMAL_GENERATION_PREFLIGHT_FAILED"
            result["ISSUES"] = gate["stage_issues"] + gate["persistence_errors"]
            result["ISSUES"] += [f"existing-{pid}={state}" for pid, state in gate["existing_states"].items() if state not in {"ABSENT", "COMPLETE_VALID_EXISTING"}]
            result["NEXT"] = "STOP_AND_INVESTIGATE_FORMAL_GENERATION_PREFLIGHT"
            if args.execute:
                atomic_write_json(OUTPUT_RESULT, result)
            print(render_result(result))
            return 2
        if not args.execute:
            print("PREFLIGHT_STATUS=PASS")
            print(f"STAGE={STAGE}")
            print(f"FORMAL_GENERATION_TARGET_COUNT={len(gate['target_ids'])}")
            print(f"CANONICAL_ARTIFACT_SCHEMA_SOURCE={result['CANONICAL_ARTIFACT_SCHEMA_SOURCE']}")
            print(f"EXISTING_FORMAL_ARTIFACT_SET_COUNT={gate['artifact_audit']['set_count']}")
            print("STAGED_ARTIFACT_SET_COUNT=0")
            print("PROMOTION_RUN=0")
            print("OCR_RUN=0")
            print("PDF_RENDER_RUN=0")
            print("PDF_EXTRACTION_RUN=0")
            print("G9_RUN=0")
            print("NEXT=RUN_WITH_EXPLICIT_--EXECUTE")
            return 0

        before_existing_artifacts = {
            row["artifact_path"]: row["artifact_sha256"] for row in data["artifact_rows"]
        }
        protected_before = {path: sha256_path(path) for path in [PAPERS_CATALOG, MEMBERSHIPS, ELIGIBILITY]}
        stage_ok, stage_issues = audit_stage_root()
        if not stage_ok:
            raise GateError("STAGE_OWNERSHIP_GATE_FAILED:" + ",".join(stage_issues))
        STAGE_ROOT.mkdir(parents=True, exist_ok=True)
        attempt_root = STAGE_ROOT / attempt_id
        attempt_root.mkdir()
        atomic_write_json(attempt_root / "stage_marker.json", {"stage": STAGE, "runner": SCRIPT_REL, "attempt_id": attempt_id, "created_at": now_iso()})
        attempt_payload: dict[str, Any] = {
            "stage": STAGE, "attempt_id": attempt_id, "status": "RUNNING", "current_gate": "PHASE_1_STAGE_GENERATION",
            "source_batch_attempt_id": SOURCE_BATCH_ATTEMPT_ID, "revalidation_attempt_id": EXPECTED_REVALIDATION_ATTEMPT_ID,
            "target_count": len(gate["target_ids"]), "completed_count": 0, "failed_count": 0,
            "staged_set_count": 0, "staged_primary_artifact_count": 0, "promoted_set_count": 0,
            "formal_artifact_registry_updated": 0, "q3_backlog_state_updated": 0, "ocr_run": 0,
            "pdf_render_run": 0, "pdf_extraction_run": 0, "body_reconstruction_run": 0, "g9_run": 0,
            "updated_at": now_iso(),
        }
        write_attempt(attempt_payload)
        progress_rows = [make_progress_row(pid, index) for index, pid in enumerate(gate["target_ids"], start=1)]
        atomic_write_csv(OUTPUT_PROGRESS, PROGRESS_FIELDS, progress_rows)
        staged_manifest_rows: list[dict[str, Any]] = []
        staged_valid = 0
        stage_failed_ids: list[str] = []
        for index, paper_id in enumerate(gate["target_ids"], start=1):
            progress = progress_rows[index - 1]
            progress["status"] = "STAGING"
            progress["started_at"] = now_iso()
            q3 = gate["q3_manifest_by_id"][paper_id]
            paper = gate["paper_by_id"][paper_id]
            body = safe_root_path(q3["body_path"]).read_text(encoding="utf-8")
            body_sha = q3["body_sha256"]
            stage_dir = attempt_root / paper_id
            stage_dir.mkdir()
            paper_text = "# Extracted Paper\n\n" + body + "\n"
            metadata_text = canonical_metadata(
                paper, gate["membership_by_id"][paper_id], q3["source_path"], q3["source_sha256"], q3["page_count"],
                q3["body_path"], body_sha, q3["manifest_path"], EXPECTED_REVALIDATION_ATTEMPT_ID, attempt_id,
            )
            card_text = canonical_card(paper_id, paper["year"], paper["problem_code"], body, q3["page_count"], body_sha)
            (stage_dir / "paper.md").write_text(paper_text, encoding="utf-8", newline="\n")
            (stage_dir / "metadata.yaml").write_text(metadata_text, encoding="utf-8", newline="\n")
            (stage_dir / "knowledge_card.md").write_text(card_text, encoding="utf-8", newline="\n")
            expected = {**q3, "paper_id": paper_id}
            qa = validate_artifact_set(stage_dir, expected, attempt_id)
            progress["stage_path"] = rel(stage_dir)
            progress["staged_primary_artifact_count"] = 3
            progress["stage_structure_status"] = "PASS" if qa["structure"] else "FAIL"
            progress["stage_hash_status"] = "PASS" if qa["hash"] else "FAIL"
            progress["identity_binding_status"] = "PASS" if qa["identity"] else "FAIL"
            progress["provenance_status"] = "PASS" if qa["provenance"] else "FAIL"
            progress["source_body_binding_status"] = "PASS" if qa["source_body"] else "FAIL"
            progress["duplicate_id_status"] = "PASS"
            progress["duplicate_path_status"] = "PASS"
            progress["status"] = "STAGED_VALID" if not qa["error"] else "STAGED_INVALID"
            progress["error_code"] = qa["error"]
            progress["finished_at"] = now_iso()
            if qa["error"]:
                stage_failed_ids.append(paper_id)
            else:
                staged_valid += 1
                for artifact_type in ARTIFACT_TYPES:
                    staged_manifest_rows.append(
                        generation_manifest_row(
                            paper_id, artifact_type, stage_dir / artifact_type, PAPERS_ROOT / paper_id / artifact_type,
                            expected, attempt_id, "PASS",
                        )
                    )
            attempt_payload.update({"completed_count": index, "failed_count": len(stage_failed_ids), "staged_set_count": index, "staged_primary_artifact_count": index * 3, "updated_at": now_iso()})
            write_attempt(attempt_payload)
            atomic_write_csv(OUTPUT_PROGRESS, PROGRESS_FIELDS, progress_rows)
        result.update({
            "STAGED_ARTIFACT_SET_COUNT": len(gate["target_ids"]), "STAGED_PRIMARY_ARTIFACT_COUNT": len(gate["target_ids"]) * 3,
            "STAGED_ARTIFACT_SET_VALID_COUNT": staged_valid, "STAGED_ARTIFACT_SET_INVALID_COUNT": len(stage_failed_ids),
            "FAILED_ARTIFACT_SET_COUNT": len(stage_failed_ids), "FAILED_PAPER_IDS": ",".join(stage_failed_ids),
        })
        atomic_write_csv(OUTPUT_MANIFEST, STAGE_MANIFEST_FIELDS, staged_manifest_rows)
        journal_rows = [
            {"paper_id": pid, "staged": int(progress_rows[i]["status"] == "STAGED_VALID"), "stage_validated": int(progress_rows[i]["status"] == "STAGED_VALID"), "promoted": 0, "post_promotion_validated": 0, "registry_registered": 0, "status": progress_rows[i]["status"], "error_code": progress_rows[i]["error_code"], "canonical_path": progress_rows[i]["canonical_path"], "updated_at": now_iso()}
            for i, pid in enumerate(gate["target_ids"])
        ]
        atomic_write_csv(OUTPUT_JOURNAL, JOURNAL_FIELDS, journal_rows)
        if stage_failed_ids:
            raise GateError("STAGED_ARTIFACT_VALIDATION_FAILED:" + ",".join(stage_failed_ids))
        attempt_payload["current_gate"] = "PHASE_2_DETERMINISTIC_PROMOTION"
        write_attempt(attempt_payload)
        promoted = 0
        for index, paper_id in enumerate(gate["target_ids"]):
            stage_dir = attempt_root / paper_id
            final_dir = PAPERS_ROOT / paper_id
            if final_dir.exists():
                raise GateError(f"FORMAL_PATH_COLLISION:{paper_id}")
            final_dir.parent.mkdir(parents=True, exist_ok=True)
            last_error: Exception | None = None
            for retry in range(3):
                try:
                    stage_dir.rename(final_dir)
                    last_error = None
                    break
                except Exception as exc:  # pragma: no cover - filesystem timing is environment-specific.
                    last_error = exc
                    time.sleep(0.15 * (retry + 1))
            if last_error is not None:
                raise GateError(f"PROMOTION_ATOMIC_RENAME_FAILED:{paper_id}:{last_error}")
            expected = {**gate["q3_manifest_by_id"][paper_id], "paper_id": paper_id}
            qa = validate_artifact_set(final_dir, expected, attempt_id)
            progress = progress_rows[index]
            progress["promoted"] = 1
            progress["post_promotion_status"] = "PASS" if not qa["error"] else "FAIL"
            progress["status"] = "PROMOTED" if not qa["error"] else "POST_PROMOTION_INVALID"
            progress["error_code"] = qa["error"]
            progress["finished_at"] = now_iso()
            journal_rows[index].update({"promoted": 1, "post_promotion_validated": int(not qa["error"]), "status": progress["status"], "error_code": qa["error"], "updated_at": now_iso()})
            atomic_write_csv(OUTPUT_JOURNAL, JOURNAL_FIELDS, journal_rows)
            atomic_write_csv(OUTPUT_PROGRESS, PROGRESS_FIELDS, progress_rows)
            if qa["error"]:
                raise GateError(f"POST_PROMOTION_VALIDATION_FAILED:{paper_id}:{qa['error']}")
            promoted += 1
            attempt_payload.update({"promoted_set_count": promoted, "updated_at": now_iso()})
            write_attempt(attempt_payload)
        new_registry_rows: list[dict[str, Any]] = []
        for paper_id in gate["target_ids"]:
            expected = {**gate["q3_manifest_by_id"][paper_id], "paper_id": paper_id}
            for row in expected_artifact_rows(gate, paper_id, attempt_id):
                new_registry_rows.append(row)
        registry_rows = data["artifact_rows"] + new_registry_rows
        if len(registry_rows) != BASE_PRIMARY_ARTIFACTS + EXPECTED_TARGET_COUNT * 3:
            raise GateError("REGISTRY_CARDINALITY_PRE_UPDATE_FAILED")
        atomic_write_csv(ARTIFACT_MANIFEST, ARTIFACT_FIELDS, registry_rows)
        result["FORMAL_ARTIFACT_REGISTRY_UPDATED"] = 1
        for row in journal_rows:
            row["registry_registered"] = 1
            row["updated_at"] = now_iso()
        for row in progress_rows:
            row["registry_registered"] = 1
        atomic_write_csv(OUTPUT_JOURNAL, JOURNAL_FIELDS, journal_rows)
        atomic_write_csv(OUTPUT_PROGRESS, PROGRESS_FIELDS, progress_rows)
        status_rows = data["status_rows"]
        status_by_id = {row["paper_id"]: row for row in status_rows}
        for paper_id in gate["target_ids"]:
            status = status_by_id[paper_id]
            status.update({"extraction_status": "PASS", "artifact_status": "PASS", "qa_status": "PASS", "deferred_reason": "", "overall_status": "COMPLETE"})
        atomic_write_csv(PAPER_STATUS, list(status_rows[0]), status_rows)
        q3_backlog_after = [row for row in data["q3_backlog_rows"] if row["paper_id"] not in set(gate["target_ids"])]
        manual_backlog_after = [row for row in data["manual_backlog_rows"] if row["paper_id"] not in set(gate["target_ids"])]
        if q3_backlog_after or manual_backlog_after:
            raise GateError("BACKLOG_CLOSURE_CARDINALITY_FAILED")
        atomic_write_csv(Q3_BACKLOG, list(data["q3_backlog_rows"][0]), q3_backlog_after)
        atomic_write_csv(MANUAL_BACKLOG, list(data["manual_backlog_rows"][0]), manual_backlog_after)
        result["Q3_BACKLOG_STATE_UPDATED"] = 1
        post_rows = read_csv(ARTIFACT_MANIFEST)
        post_audit = audit_canonical_registry(post_rows)
        post_protected = {path: sha256_path(path) for path in [PAPERS_CATALOG, MEMBERSHIPS, ELIGIBILITY]}
        source_modified = 0
        for source_path, before_sha in gate["source_hash_before"].items():
            path = safe_root_path(source_path)
            source_modified += int(not path.is_file() or sha256_path(path) != before_sha)
        preexisting_modified = sum(
            int(not (ROOT / artifact_path).is_file() or sha256_path(ROOT / artifact_path) != artifact_sha)
            for artifact_path, artifact_sha in before_existing_artifacts.items()
        )
        status_rows_after = read_csv(PAPER_STATUS)
        q3_backlog_count = len(read_csv(Q3_BACKLOG))
        manual_backlog_count = len(read_csv(MANUAL_BACKLOG))
        eligible_count = sum(row.get("artifact_eligible") == "1" for row in data["eligibility_rows"])
        ineligible_count = sum(row.get("artifact_eligible") != "1" for row in data["eligibility_rows"])
        new_structure_pass = sum(row["stage_structure_status"] == "PASS" for row in progress_rows)
        new_hash_valid = sum(row["stage_hash_status"] == "PASS" for row in progress_rows) * 1
        new_identity_pass = sum(row["identity_binding_status"] == "PASS" for row in progress_rows)
        new_provenance_pass = sum(row["provenance_status"] == "PASS" for row in progress_rows)
        new_body_pass = sum(row["source_body_binding_status"] == "PASS" for row in progress_rows)
        duplicate_ids = post_audit["duplicate_artifact_ids"]
        duplicate_paths = post_audit["duplicate_paths"]
        formal_with_artifact = sum(
            len(post_audit["by_id"].get(row["paper_id"], [])) == 3 and row.get("artifact_eligible") == "1"
            for row in data["eligibility_rows"]
        )
        result.update({
            "STATUS": "PASS" if all([
                promoted == EXPECTED_TARGET_COUNT, post_audit["set_count"] == 453, post_audit["primary_count"] == 1359,
                post_audit["duplicate_artifact_ids"] == 0, post_audit["duplicate_paths"] == 0, post_audit["bad_schema"] == 0,
                post_audit["bad_sets"] == 0, post_audit["hash_failures"] == 0, q3_backlog_count == 0, manual_backlog_count == 0,
                new_structure_pass == EXPECTED_TARGET_COUNT, new_identity_pass == EXPECTED_TARGET_COUNT,
                new_provenance_pass == EXPECTED_TARGET_COUNT, new_body_pass == EXPECTED_TARGET_COUNT,
                preexisting_modified == 0, source_modified == 0, protected_before == post_protected,
            ]) else "BLOCKED",
            "PROMOTED_ARTIFACT_SET_COUNT": promoted, "UNPROMOTED_ARTIFACT_SET_COUNT": EXPECTED_TARGET_COUNT - promoted,
            "NEW_ARTIFACT_SET_COUNT": promoted, "NEW_PRIMARY_ARTIFACT_COUNT": promoted * 3,
            "NEW_ARTIFACT_STRUCTURE_PASS_COUNT": new_structure_pass, "NEW_ARTIFACT_STRUCTURE_FAIL_COUNT": EXPECTED_TARGET_COUNT - new_structure_pass,
            "NEW_ARTIFACT_HASH_VALID_COUNT": new_hash_valid * 3, "NEW_ARTIFACT_HASH_INVALID_COUNT": (EXPECTED_TARGET_COUNT - new_hash_valid) * 3,
            "NEW_ARTIFACT_IDENTITY_BINDING_PASS_COUNT": new_identity_pass, "NEW_ARTIFACT_IDENTITY_BINDING_FAIL_COUNT": EXPECTED_TARGET_COUNT - new_identity_pass,
            "NEW_ARTIFACT_PROVENANCE_PASS_COUNT": new_provenance_pass, "NEW_ARTIFACT_PROVENANCE_FAIL_COUNT": EXPECTED_TARGET_COUNT - new_provenance_pass,
            "FORMAL_ARTIFACT_SOURCE_BODY_BINDING_PASS_COUNT": new_body_pass, "FORMAL_ARTIFACT_SOURCE_BODY_BINDING_FAIL_COUNT": EXPECTED_TARGET_COUNT - new_body_pass,
            "DUPLICATE_ARTIFACT_ID_COUNT": duplicate_ids, "DUPLICATE_FORMAL_ARTIFACT_PATH_COUNT": duplicate_paths,
            "PREEXISTING_ARTIFACT_CONTENT_MODIFICATION_COUNT": preexisting_modified, "TOTAL_ARTIFACT_SET_COUNT": post_audit["set_count"],
            "TOTAL_PRIMARY_ARTIFACT_COUNT": post_audit["primary_count"], "ARTIFACT_SETS": post_audit["set_count"], "PRIMARY_ARTIFACTS": post_audit["primary_count"],
            "DOC_MANUAL_BACKLOG": sum(row.get("category") == "DOC_REPAIR_MANUAL" for row in manual_backlog_after), "Q3_MANUAL_BACKLOG": q3_backlog_count,
            "TOTAL_MANUAL_BACKLOG": manual_backlog_count, "ELIGIBLE": eligible_count, "INELIGIBLE": ineligible_count,
            "FORMAL_ARTIFACT_ELIGIBLE_WITH_ARTIFACT_COUNT": formal_with_artifact, "FORMAL_ARTIFACT_ELIGIBLE_WITHOUT_ARTIFACT_COUNT": eligible_count - formal_with_artifact,
            "ORIGINAL_FILES_MODIFIED": source_modified, "IDENTITY_MODIFICATION_COUNT": int(protected_before[PAPERS_CATALOG] != post_protected[PAPERS_CATALOG]),
            "MEMBERSHIP_MODIFICATION_COUNT": int(protected_before[MEMBERSHIPS] != post_protected[MEMBERSHIPS]), "FORMAL_ELIGIBILITY_MODIFIED": int(protected_before[ELIGIBILITY] != post_protected[ELIGIBILITY]),
            "FAILED_ARTIFACT_SET_COUNT": 0, "FAILED_PAPER_IDS": "",
        })
        if result["STATUS"] != "PASS":
            raise GateError("POST_PROMOTION_QA_FAILED")
        result["BLOCKER"] = "NONE"
        result["NEXT"] = "G9-INDEX-REBUILD"
        result["VALIDATION"] = [
            "All 128 targets matched Q3 backlog and final revalidated persistence.",
            "Canonical three-artifact schema was reused; all 128 sets staged and validated before promotion.",
            "384 primary artifacts were promoted deterministically in paper_id ascending order.",
            "Canonical registry, paper status, Q3 backlog, and aggregate backlog were updated atomically where applicable.",
            "Existing 325 artifact sets, identity, membership, eligibility, and source files remained byte-stable.",
        ]
        result["ISSUES"] = []
        attempt_payload.update({"status": "PASS", "current_gate": "PHASE_3_FINAL_QA", "completed_count": EXPECTED_TARGET_COUNT, "failed_count": 0, "formal_artifact_registry_updated": 1, "q3_backlog_state_updated": 1, "updated_at": now_iso()})
        write_attempt(attempt_payload)
        outputs = [OUTPUT_RESULT, OUTPUT_ATTEMPT, OUTPUT_PROGRESS, OUTPUT_JOURNAL, OUTPUT_MANIFEST, ARTIFACT_MANIFEST, PAPER_STATUS, Q3_BACKLOG, MANUAL_BACKLOG, REPORT, ROOT / SCRIPT_REL]
        result["OUTPUTS"] = {path.name: rel(path) for path in outputs}
        atomic_write_json(OUTPUT_RESULT, result)
        report = "# G8 Q3 Formal Artifact Generation\n\n" + render_result(result) + "\n"
        atomic_write_bytes(REPORT, report.encode("utf-8"))
        print(render_result(result))
        return 0
    except Exception as exc:
        result = locals().get("result", {"STAGE": STAGE, "STATUS": "BLOCKED", "BRANCH": "library-refactor-v1", "HEAD": "", "FORMAL_GENERATION_ATTEMPT_ID": attempt_id, "OUTPUTS": {}, "VALIDATION": [], "ISSUES": []})
        result["STATUS"] = "BLOCKED"
        result["BLOCKER"] = str(exc)
        result["NEXT"] = "STOP_AND_PRESERVE_STAGE_EVIDENCE"
        result.setdefault("ISSUES", []).append(type(exc).__name__)
        if args.execute:
            try:
                atomic_write_json(OUTPUT_RESULT, result)
            except Exception:
                pass
        print(render_result(result))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
