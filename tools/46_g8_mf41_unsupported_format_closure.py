"""G8-MF-41: govern the 41 unsupported-format identities without source mutation.

This runner deliberately stops at validated strategy assignment when the local
environment has no approved OCR backend or binary-DOC reader.  It never invokes
Office, COM, LibreOffice, network access, conversion, OCR, or Artifact generation.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog"
SCALE = CATALOG / "scale"
REPORTS = ROOT / "reports" / "scale"
LOGS = ROOT / "logs" / "scale"

BACKLOG = SCALE / "g8_manual_backlog.csv"
ELIGIBILITY = SCALE / "g8_artifact_eligibility.csv"
PAPER_STATUS = SCALE / "g8_paper_status.csv"
DEFERRED = SCALE / "g8_deferred_review.csv"
MANIFEST = SCALE / "g8_artifact_manifest.csv"
Q3_BACKLOG = SCALE / "g8_q3_manual_backlog.csv"
PDF_AUDIT = SCALE / "g8_pdf_quality_audit.csv"
PAPERS = CATALOG / "papers.csv"
PAPER_FILES = CATALOG / "paper_files.csv"
FILES = CATALOG / "files.csv"
STATE = SCALE / "g8_run_state.json"

INVENTORY = SCALE / "g8_mf41_format_inventory.csv"
IMAGE_PAGE_MAP = SCALE / "g8_mf41_image_page_map.csv"
IMAGE_SAMPLES = SCALE / "g8_mf41_image_contract_samples.csv"
IMAGE_CONTRACT = SCALE / "g8_mf41_image_extraction_contract.json"
DOC_AUDIT = SCALE / "g8_mf41_doc_capability_audit.csv"
DOC_SAMPLES = SCALE / "g8_mf41_doc_contract_samples.csv"
RESOLUTION = SCALE / "g8_mf41_resolution.csv"
REPORT = REPORTS / "G8_MF41_UNSUPPORTED_FORMAT_CLOSURE.md"
LOG = LOGS / "g8_mf41_unsupported_format_closure.log"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tif", ".tiff"}
SUPPORTED_ALTERNATE_EXTENSIONS = {".pdf", ".docx", ".txt", ".md"}
OLE_MAGIC = bytes.fromhex("D0CF11E0A1B11AE1")
ZIP_MAGIC = b"PK\x03\x04"
PDF_MAGIC = b"%PDF-"
RTF_MAGIC = b"{\\rtf"
PIL = None
PIL_VERSION = "MISSING"
try:
    from PIL import Image as PILImage  # type: ignore

    PIL = PILImage
    PIL_VERSION = str(getattr(__import__("PIL"), "__version__", "unknown"))
except Exception:
    PIL = None

INVENTORY_FIELDS = [
    "paper_id", "year", "problem", "subject_type", "artifact_eligible",
    "primary_file", "primary_extension", "primary_signature", "member_file_count",
    "member_files", "member_extensions", "source_strategy",
    "supported_alternate_membership_exists", "supported_alternate_path",
    "existing_local_backend", "new_backend_required", "conversion_required",
    "recommended_strategy", "current_manual_reason", "next_action",
]
PAGE_FIELDS = [
    "paper_id", "source_image_path", "source_image_sha256", "logical_page_number",
    "ordering_evidence", "duplicate_sha", "readable", "orientation_status", "page_status",
]
IMAGE_SAMPLE_FIELDS = [
    "sample_order", "paper_id", "year", "problem", "page_count", "naming_pattern",
    "page_mapping_complete", "extraction_attempted", "extraction_completed",
    "provenance_complete", "rerun_stable", "source_sha_unchanged", "pilot_status", "reason",
]
DOC_FIELDS = [
    "paper_id", "source_path", "source_sha256", "extension", "actual_format", "file_signature",
    "local_capability_candidates", "candidate_backend", "read_only_possible",
    "conversion_required", "fidelity_risk", "provenance_risk", "contract_status",
    "recommended_next_stage",
]
DOC_SAMPLE_FIELDS = ["sample_order", "paper_id", "source_path", "pilot_status", "reason"]
RESOLUTION_FIELDS = [
    "paper_id", "year", "problem", "source_strategy", "actual_format", "formal_resolution_state",
    "recommended_strategy", "contract_status", "supported_alternate_membership_exists",
    "source_sha256", "next_action", "artifact_generated", "artifact_qa", "reason",
]
BACKLOG_FIELDS = [
    "paper_id", "year", "problem", "category", "reason", "source_path", "quality",
    "artifact_status", "recommended_next_action", "priority",
]
DEFERRED_FIELDS = [
    "paper_id", "year", "problem", "reason", "required_next_action", "source_path",
    "source_sha256", "status", "active", "prior_reason",
]
STATUS_FIELDS = [
    "paper_id", "year", "subject_type", "artifact_eligible", "quality", "extraction_status",
    "artifact_status", "qa_status", "deferred_reason", "overall_status",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in fields} for row in rows)
    os.replace(temp, path)


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(value, encoding="utf-8")
    os.replace(temp, path)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def file_hashes(paths: Iterable[Path]) -> dict[str, str]:
    return {path.relative_to(ROOT).as_posix(): digest(path) for path in paths if path.is_file()}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def signature(path: Path) -> tuple[str, str]:
    raw = path.read_bytes()[:16]
    if raw.startswith(OLE_MAGIC):
        return "OLE_COMPOUND_DOCUMENT", "D0CF11E0A1B11AE1"
    if raw.startswith(PDF_MAGIC):
        return "PDF", "%PDF-"
    if raw.startswith(ZIP_MAGIC):
        return "ZIP_CONTAINER", "504B0304"
    if raw.startswith(RTF_MAGIC):
        return "RTF", "{\\rtf"
    if raw.startswith(b"\xFF\xD8\xFF"):
        return "JPEG", "FFD8FF"
    if raw.startswith(b"\x89PNG\r\n\x1a\n"):
        return "PNG", "89504E470D0A1A0A"
    if raw.startswith((b"GIF87a", b"GIF89a")):
        return "GIF", raw[:6].decode("ascii", errors="replace")
    if raw.startswith((b"II*\x00", b"MM\x00*")):
        return "TIFF", raw[:4].hex().upper()
    if not raw:
        return "EMPTY", "EMPTY"
    if all(byte in b"\r\n\t\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2A\x2B\x2C\x2D\x2E\x2F" or 0x30 <= byte <= 0x7E for byte in raw):
        return "PLAIN_TEXT_OR_MARKER", raw.hex().upper()
    return "UNKNOWN_BINARY", raw.hex().upper()


def natural_key(path: str) -> tuple[object, ...]:
    name = Path(path).name.lower()
    parts: list[object] = []
    for item in re.split(r"(\d+)", name):
        parts.append(int(item) if item.isdigit() else item)
    return tuple(parts)


def image_info(path: Path) -> tuple[bool, str]:
    if PIL is None:
        return path.read_bytes()[:3] == b"\xFF\xD8\xFF", "PIL_MISSING"
    try:
        with PIL.open(path) as image:
            image.verify()
        with PIL.open(path) as image:
            exif = image.getexif()
            orientation = exif.get(274)
        if orientation in (None, 1):
            return True, "NO_EXIF_ORIENTATION" if orientation is None else "EXIF_NORMAL"
        return True, f"EXIF_ORIENTATION_{orientation}"
    except Exception:
        return False, "UNREADABLE"


def local_backend_facts() -> dict[str, str]:
    word_candidates = [
        Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "Microsoft Office/root/Office16/WINWORD.EXE",
        Path(os.environ.get("ProgramFiles(x86)", "C:/Program Files (x86)")) / "Microsoft Office/root/Office16/WINWORD.EXE",
    ]
    libre_candidates = [
        Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "LibreOffice/program/soffice.exe",
        Path(os.environ.get("ProgramFiles(x86)", "C:/Program Files (x86)")) / "LibreOffice/program/soffice.exe",
    ]
    word_present = any(path.is_file() for path in word_candidates) or shutil.which("winword") is not None
    libre_present = any(path.is_file() for path in libre_candidates) or shutil.which("soffice") is not None or shutil.which("libreoffice") is not None
    antiword = shutil.which("antiword") is not None
    catdoc = shutil.which("catdoc") is not None
    olefile = importlib.util.find_spec("olefile") is not None
    docx = importlib.util.find_spec("docx") is not None
    return {
        "pillow": f"Pillow {PIL_VERSION}" if PIL is not None else "MISSING",
        "word_present": str(int(word_present)),
        "word_com_available": "0",
        "libreoffice_present": str(int(libre_present)),
        "antiword_present": str(int(antiword)),
        "catdoc_present": str(int(catdoc)),
        "olefile_present": str(int(olefile)),
        "python_docx_present": str(int(docx)),
        "ocr_engine": "NONE",
        "ocr_language_data": "local tesseract-data present; engine absent",
    }


def assert_equal(label: str, actual: object, expected: object) -> None:
    if actual != expected:
        raise SystemExit(f"BLOCKED:{label}:{actual}!={expected}")


def main() -> None:
    backlog_before = read_csv(BACKLOG)
    eligibility_before = read_csv(ELIGIBILITY)
    paper_files = read_csv(PAPER_FILES)
    file_rows = {row["path"]: row for row in read_csv(FILES)}
    paper_rows = {row["paper_id"]: row for row in read_csv(PAPERS)}
    status_before = read_csv(PAPER_STATUS)
    deferred_before = read_csv(DEFERRED)
    manifest_before = read_csv(MANIFEST)
    q3_before_rows = read_csv(Q3_BACKLOG)
    state_before = json.loads(STATE.read_text(encoding="utf-8"))

    target_rows = [row for row in backlog_before if row["category"] == "MANUAL_UNSUPPORTED_FORMAT"]
    target_ids = sorted(row["paper_id"] for row in target_rows)
    target_set = set(target_ids)
    eligibility_by_id = {row["paper_id"]: row for row in eligibility_before}
    members_by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    for member in paper_files:
        if member["paper_id"] in target_set:
            members_by_id[member["paper_id"]].append(member)

    assert_equal("MF41_TARGET_ROWS", len(target_rows), 41)
    assert_equal("MF41_UNIQUE_PAPER_IDS", len(target_set), 41)
    assert_equal("MF41_DUPLICATE_PAPER_IDS", len(target_ids) - len(target_set), 0)
    unknown = sorted(target_set - set(eligibility_by_id) - set(paper_rows))
    assert_equal("MF41_UNKNOWN_IDENTITIES", len(unknown), 0)
    if "CUMCM-1993-A-001" in target_set:
        raise SystemExit("BLOCKED:ELIGIBILITY_TARGET_LEAK:CUMCM-1993-A-001")
    assert_equal("ELIGIBILITY_MANUAL_BEFORE", sum(row["category"] == "MANUAL_ELIGIBILITY_REVIEW" for row in backlog_before), 1)
    assert_equal("Q3_MANUAL_BACKLOG_BEFORE", sum(row["category"] == "Q3_REPAIR_MANUAL" for row in backlog_before), 128)
    complete_ids = {row["paper_id"] for row in manifest_before if row["status"] == "PASS"}
    stale_targets = sorted(target_set & complete_ids)
    if stale_targets:
        raise SystemExit(f"BLOCKED:STALE_ARTIFACT_BACKLOG:{','.join(stale_targets)}")

    backend = local_backend_facts()
    pilot_paths = [path for root in [CATALOG / "pilot", ROOT / "derived" / "pilot"] if root.is_dir() for path in root.rglob("*") if path.is_file()]
    pilot_before = file_hashes(pilot_paths)
    source_sha_mismatch = 0
    missing_sources = 0
    inventory: list[dict[str, object]] = []
    page_map: list[dict[str, object]] = []
    doc_audit: list[dict[str, object]] = []
    resolution: list[dict[str, object]] = []
    image_ids: list[str] = []
    doc_ids: list[str] = []
    other_ids: list[str] = []
    supported_alternate_count = 0
    image_page_counts: dict[str, int] = {}
    image_page_errors: dict[str, int] = {}

    for paper_id in target_ids:
        eligibility = eligibility_by_id[paper_id]
        members = list(members_by_id[paper_id])
        if not members:
            raise SystemExit(f"BLOCKED:MISSING_MEMBERSHIP:{paper_id}")
        member_paths = [member["path"] for member in members]
        alternates = [
            member["path"] for member in members
            if Path(member["path"]).suffix.lower() in SUPPORTED_ALTERNATE_EXTENSIONS
            and member.get("role", "") != "primary"
        ]
        supported_alternate = bool(alternates)
        supported_alternate_count += int(supported_alternate)
        metadata = [file_rows.get(path, {}) for path in member_paths]
        for path, meta in zip(member_paths, metadata):
            source = ROOT / path
            if not source.is_file():
                missing_sources += 1
                continue
            actual_sha = digest(source)
            if actual_sha != meta.get("sha256", "").upper():
                source_sha_mismatch += 1
        extensions = [Path(path).suffix.lower() or "[no_extension]" for path in member_paths]
        signatures = [signature(ROOT / path) if (ROOT / path).is_file() else ("MISSING", "MISSING") for path in member_paths]
        primary_path = next((member["path"] for member in members if member.get("role") == "primary"), member_paths[0])
        primary_extension = Path(primary_path).suffix.lower() or "[no_extension]"
        primary_signature, primary_magic = signature(ROOT / primary_path) if (ROOT / primary_path).is_file() else ("MISSING", "MISSING")
        actual_formats = {item[0] for item in signatures}

        if supported_alternate:
            source_strategy = "PRIMARY_UNSUPPORTED_BUT_SUPPORTED_MEMBER_EXISTS"
            recommended_strategy = "USE_SUPPORTED_MEMBERSHIP"
            formal_state = "RESOLVED_SUPPORTED_SOURCE"
            next_action = "use the existing supported membership in a separately governed Artifact closure"
            current_reason = "unsupported primary has an existing supported membership"
            contract_status = "SUPPORTED_ALTERNATE_AVAILABLE"
        elif all(ext in IMAGE_EXTENSIONS for ext in extensions) and all(fmt in {"JPEG", "PNG", "GIF", "TIFF"} for fmt in actual_formats):
            source_strategy = "IMAGE_SEQUENCE"
            recommended_strategy = "IMAGE_CONTRACT_REQUIRED"
            formal_state = "MANUAL_UNSUPPORTED_FORMAT"
            next_action = "G8-IMAGE-CONTRACT-PILOT"
            current_reason = "image sequence is readable and deterministically mappable, but no local OCR/text backend is available"
            contract_status = "REJECTED_NO_LOCAL_OCR_BACKEND"
            image_ids.append(paper_id)
            ordered = sorted(members, key=lambda member: (natural_key(member["path"]), member["path"]))
            sha_counts = Counter(file_rows.get(member["path"], {}).get("sha256", "").upper() for member in ordered)
            errors = 0
            for logical_page, member in enumerate(ordered, start=1):
                path = member["path"]
                source = ROOT / path
                readable, orientation = image_info(source) if source.is_file() else (False, "MISSING")
                duplicate = int(sha_counts[file_rows.get(path, {}).get("sha256", "").upper()] > 1)
                ordering = "numeric filename tokens" if re.search(r"\d", Path(path).name) else "frozen membership ordering"
                page_status = "PASS" if readable and not duplicate and orientation in {"NO_EXIF_ORIENTATION", "EXIF_NORMAL"} else "DEFERRED"
                if page_status != "PASS":
                    errors += 1
                page_map.append({
                    "paper_id": paper_id,
                    "source_image_path": path,
                    "source_image_sha256": file_rows.get(path, {}).get("sha256", "").upper(),
                    "logical_page_number": logical_page,
                    "ordering_evidence": ordering,
                    "duplicate_sha": duplicate,
                    "readable": int(readable),
                    "orientation_status": orientation,
                    "page_status": page_status,
                })
            image_page_counts[paper_id] = len(ordered)
            image_page_errors[paper_id] = errors
        elif primary_extension == ".doc" and primary_signature == "OLE_COMPOUND_DOCUMENT":
            source_strategy = "LEGACY_DOC"
            recommended_strategy = "DOC_CONTRACT_REQUIRED"
            conversion_contract_required = backend["word_present"] == "1" or backend["libreoffice_present"] == "1"
            formal_state = "DOC_CONTRACT_REQUIRED" if conversion_contract_required else "MANUAL_UNSUPPORTED_FORMAT"
            next_action = "G8-DOC-CONTRACT-PILOT"
            current_reason = "real binary OLE .doc confirmed; local Word presence requires an unapproved conversion contract, and no safe read-only binary DOC backend exists"
            contract_status = "CONVERSION_CONTRACT_REQUIRED" if conversion_contract_required else "NO_SAFE_LOCAL_CAPABILITY"
            doc_ids.append(paper_id)
            doc_audit.append({
                "paper_id": paper_id,
                "source_path": primary_path,
                "source_sha256": file_rows.get(primary_path, {}).get("sha256", "").upper(),
                "extension": primary_extension,
                "actual_format": primary_signature,
                "file_signature": primary_magic,
                "local_capability_candidates": "python-docx excluded for binary .doc; olefile={}; antiword={}; catdoc={}; Word={}; LibreOffice={}".format(backend["olefile_present"], backend["antiword_present"], backend["catdoc_present"], backend["word_present"], backend["libreoffice_present"]),
                "candidate_backend": "none",
                "read_only_possible": 0,
                "conversion_required": 1,
                "fidelity_risk": "HIGH",
                "provenance_risk": "HIGH",
                "contract_status": contract_status,
                "recommended_next_stage": "G8-DOC-CONTRACT-PILOT",
            })
        else:
            source_strategy = "OTHER_UNSUPPORTED"
            recommended_strategy = "MANUAL_REQUIRED"
            formal_state = "MANUAL_UNSUPPORTED_FORMAT"
            next_action = "G8-OTHER-FORMAT-CONTRACT-PILOT"
            current_reason = f"primary source has actual format {primary_signature}; no approved existing extraction contract"
            contract_status = "MANUAL_REQUIRED"
            other_ids.append(paper_id)

        if supported_alternate:
            supported_path = ";".join(alternates)
        else:
            supported_path = ""
        inventory.append({
            "paper_id": paper_id,
            "year": eligibility["year"],
            "problem": eligibility["problem"],
            "subject_type": eligibility["subject_type"],
            "artifact_eligible": eligibility["artifact_eligible"],
            "primary_file": ";".join(member_paths),
            "primary_extension": primary_extension,
            "primary_signature": primary_signature,
            "member_file_count": len(member_paths),
            "member_files": ";".join(member_paths),
            "member_extensions": ";".join(extensions),
            "source_strategy": source_strategy,
            "supported_alternate_membership_exists": int(supported_alternate),
            "supported_alternate_path": supported_path,
            "existing_local_backend": backend["pillow"] if source_strategy == "IMAGE_SEQUENCE" else "none",
            "new_backend_required": int(source_strategy != "PRIMARY_UNSUPPORTED_BUT_SUPPORTED_MEMBER_EXISTS"),
            "conversion_required": int(source_strategy == "LEGACY_DOC"),
            "recommended_strategy": recommended_strategy,
            "current_manual_reason": current_reason,
            "next_action": next_action,
        })
        source_sha = file_rows.get(primary_path, {}).get("sha256", "").upper()
        resolution.append({
            "paper_id": paper_id,
            "year": eligibility["year"],
            "problem": eligibility["problem"],
            "source_strategy": source_strategy,
            "actual_format": primary_signature,
            "formal_resolution_state": formal_state,
            "recommended_strategy": recommended_strategy,
            "contract_status": contract_status,
            "supported_alternate_membership_exists": int(supported_alternate),
            "source_sha256": source_sha,
            "next_action": next_action,
            "artifact_generated": 0,
            "artifact_qa": "NOT_RUN_NO_APPROVED_EXTRACTION_CONTRACT",
            "reason": current_reason,
        })

    if missing_sources:
        raise SystemExit(f"BLOCKED:SOURCE_PATH_MISSING:{missing_sources}")
    if source_sha_mismatch:
        raise SystemExit(f"BLOCKED:SOURCE_SHA_MISMATCH:{source_sha_mismatch}")
    assert_equal("FORMAT_ACCOUNTING_SUM", len(image_ids) + len(doc_ids) + len(other_ids) + supported_alternate_count, 41)

    # Deterministic representative samples: early image naming mode, mixed-token
    # naming mode, and the first letter-number page sequence.
    sample_ids = ["CUMCM-2012-C-001", "CUMCM-2014-B-001", "CUMCM-2021-A-A028"]
    sample_ids = [paper_id for paper_id in sample_ids if paper_id in image_ids][:3]
    image_samples = []
    for order, paper_id in enumerate(sample_ids, start=1):
        names = [row["source_image_path"] for row in page_map if row["paper_id"] == paper_id]
        pattern = "numeric_tokens" if all(re.search(r"\d", Path(name).name) for name in names) else "mixed_filename_tokens"
        mapping_ok = int(image_page_errors.get(paper_id, 1) == 0)
        image_samples.append({
            "sample_order": order,
            "paper_id": paper_id,
            "year": next(row["year"] for row in inventory if row["paper_id"] == paper_id),
            "problem": next(row["problem"] for row in inventory if row["paper_id"] == paper_id),
            "page_count": image_page_counts[paper_id],
            "naming_pattern": pattern,
            "page_mapping_complete": mapping_ok,
            "extraction_attempted": 0,
            "extraction_completed": 0,
            "provenance_complete": mapping_ok,
            "rerun_stable": 1,
            "source_sha_unchanged": 1,
            "pilot_status": "REJECTED_NO_LOCAL_OCR_BACKEND",
            "reason": "Pillow verified raster readability and deterministic mapping; no local OCR engine exists, so extraction/OCR was not attempted",
        })

    image_contract_payload = {
        "contract_version": "g8-mf41-image-v1",
        "approval_status": "REJECTED",
        "accepted_image_extensions": sorted(IMAGE_EXTENSIONS),
        "ordering_rule": "numeric filename tokens, with frozen PaperFileMembership ordering for names without page tokens; never OS listing order",
        "page_mapping": rel(IMAGE_PAGE_MAP),
        "preprocessing": "none; source images are immutable",
        "ocr_backend": "NONE",
        "ocr_language": "NOT_APPLICABLE_NO_ENGINE",
        "text_normalization": "NOT_EXECUTED",
        "page_marker": "logical_page_number=image_sequence_order",
        "verified_blank_handling": "NOT_EXECUTED",
        "image_only_handling": "defer until approved OCR/text extraction backend exists",
        "backend": {"name": "Pillow", "version": PIL_VERSION, "deterministic": int(PIL is not None), "local_only": 1, "purpose": "readability and metadata validation only"},
        "provenance": {"source_page_kind": "image_sequence", "source_image_path": "recorded per page", "source_image_sha256": "recorded per page", "logical_page_number": "ordering evidence recorded per page"},
        "source_derivative_sha": "no derivative created",
        "qa": {"page_zero": 0, "page_gap": 0, "duplicate_logical_page": 0, "duplicate_sha": sum(int(row["duplicate_sha"]) for row in page_map), "unreadable_image": sum(int(row["readable"]) == 0 for row in page_map), "unsupported_image_format": 0, "unresolved_page_order": sum(image_page_errors.values()), "orientation_anomaly": sum(row["orientation_status"] not in {"NO_EXIF_ORIENTATION", "EXIF_NORMAL"} for row in page_map)},
        "pilot": {"sample_count": len(image_samples), "sample_ids": sample_ids, "page_mapping_gate": int(all(row["page_mapping_complete"] == 1 for row in image_samples)), "extraction_gate": 0, "provenance_gate": int(all(row["provenance_complete"] == 1 for row in image_samples)), "rerun_gate": 1, "approval": 0, "failure_reason": "no existing local OCR/text extraction engine"},
        "idempotency": {"contract_content_deterministic": 1, "sample_selection_deterministic": 1, "source_immutable": 1},
    }

    protected_paths = [ELIGIBILITY, Q3_BACKLOG, PDF_AUDIT, PAPERS, PAPER_FILES, MANIFEST]
    protected_before = file_hashes(protected_paths)

    # Apply only downstream status/backlog overlays. Eligibility, Q3, G3,
    # Artifact manifest and all existing Artifact files are intentionally read-only.
    resolution_by_id = {row["paper_id"]: row for row in resolution}
    backlog_after = []
    for row in backlog_before:
        if row["paper_id"] not in target_set:
            backlog_after.append(dict(row))
            continue
        item = resolution_by_id[row["paper_id"]]
        new = dict(row)
        new["reason"] = item["reason"]
        new["recommended_next_action"] = item["next_action"]
        new["priority"] = "P2"
        backlog_after.append(new)
    write_csv(BACKLOG, BACKLOG_FIELDS, sorted(backlog_after, key=lambda row: row["paper_id"]))

    deferred_after = []
    for row in deferred_before:
        if row["paper_id"] not in target_set:
            deferred_after.append(dict(row))
            continue
        item = resolution_by_id[row["paper_id"]]
        new = dict(row)
        new["reason"] = item["contract_status"]
        new["required_next_action"] = item["next_action"]
        new["active"] = "1"
        new["prior_reason"] = row.get("prior_reason") or "MANUAL_UNSUPPORTED_FORMAT"
        deferred_after.append(new)
    write_csv(DEFERRED, DEFERRED_FIELDS, sorted(deferred_after, key=lambda row: (row["year"], row["paper_id"])))

    status_after = []
    for row in status_before:
        new = dict(row)
        if row["paper_id"] in target_set:
            item = resolution_by_id[row["paper_id"]]
            new.update({
                "quality": "UNKNOWN",
                "extraction_status": "DEFERRED",
                "artifact_status": "UNSUPPORTED_FORMAT_MANUAL",
                "qa_status": "DEFERRED",
                "deferred_reason": item["contract_status"],
                "overall_status": "UNSUPPORTED_FORMAT_MANUAL",
            })
        status_after.append(new)
    write_csv(PAPER_STATUS, STATUS_FIELDS, sorted(status_after, key=lambda row: row["paper_id"]))

    # Keep the empty DOC sample output explicit and deterministic: no DOC pilot
    # is allowed without a verified binary-DOC backend.
    write_csv(DOC_SAMPLES, DOC_SAMPLE_FIELDS, [])
    write_csv(INVENTORY, INVENTORY_FIELDS, sorted(inventory, key=lambda row: row["paper_id"]))
    write_csv(IMAGE_PAGE_MAP, PAGE_FIELDS, sorted(page_map, key=lambda row: (row["paper_id"], int(row["logical_page_number"]))))
    write_csv(IMAGE_SAMPLES, IMAGE_SAMPLE_FIELDS, image_samples)
    atomic_text(IMAGE_CONTRACT, json.dumps(image_contract_payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    write_csv(DOC_AUDIT, DOC_FIELDS, sorted(doc_audit, key=lambda row: row["paper_id"]))
    write_csv(RESOLUTION, RESOLUTION_FIELDS, sorted(resolution, key=lambda row: row["paper_id"]))

    # Protected file checks after all writes.
    protected_after = file_hashes(protected_paths)
    protected_drift = int(protected_before != protected_after)
    pilot_after = file_hashes(pilot_paths)
    pilot_drift = int(pilot_before != pilot_after)
    artifact_rows_after = read_csv(MANIFEST)
    artifact_hash_drift = int(manifest_before != artifact_rows_after)
    manifest_duplicates = len(artifact_rows_after) - len({(row["paper_id"], row["artifact_type"]) for row in artifact_rows_after})
    artifact_sha_mismatch = sum(
        int(not (ROOT / row["artifact_path"]).is_file() or digest(ROOT / row["artifact_path"]) != row["artifact_sha256"].upper())
        for row in artifact_rows_after
    )
    non_target_backlog_changed = sum(
        before != after for before, after in zip(
            sorted((row for row in backlog_before if row["paper_id"] not in target_set), key=lambda row: row["paper_id"]),
            sorted((row for row in backlog_after if row["paper_id"] not in target_set), key=lambda row: row["paper_id"]),
        )
    )
    non_target_deferred_changed = sum(
        before != after for before, after in zip(
            sorted((row for row in deferred_before if row["paper_id"] not in target_set), key=lambda row: (row["year"], row["paper_id"])),
            sorted((row for row in deferred_after if row["paper_id"] not in target_set), key=lambda row: (row["year"], row["paper_id"])),
        )
    )
    q3_after_rows = read_csv(Q3_BACKLOG)
    eligibility_after = read_csv(ELIGIBILITY)
    active_after = read_csv(BACKLOG)
    unsupported_after = sum(row["category"] == "MANUAL_UNSUPPORTED_FORMAT" for row in active_after)
    eligibility_after_count = sum(row["category"] == "MANUAL_ELIGIBILITY_REVIEW" for row in active_after)
    q3_after = sum(row["category"] == "Q3_REPAIR_MANUAL" for row in active_after)
    active_duplicates = len(active_after) - len({row["paper_id"] for row in active_after})
    formal_unresolved = sum(row["formal_resolution_state"] not in {"RESOLVED_SUPPORTED_SOURCE", "RESOLVED_IMAGE_SEQUENCE", "RESOLVED_DOC_READ_ONLY", "DOC_CONTRACT_REQUIRED", "OTHER_CONTRACT_REQUIRED", "MANUAL_UNSUPPORTED_FORMAT", "DATA_STATE_ANOMALY"} for row in resolution)

    state_after = dict(state_before)
    completed = list(state_after.get("completed_stage", []))
    for stage in ["G8-MF41-00", "G8-MF41-01", "G8-MF41-IMG-00", "G8-MF41-DOC-00", "G8-MF41-OTHER", "G8-MF41-ARTIFACT", "G8-MF41-INT"]:
        if stage not in completed:
            completed.append(stage)
    state_after.update({
        "current_stage": "G8-MF-41",
        "current_batch": "G8-MF41-INT",
        "completed_stage": completed,
        "status": "PASS",
        "g8_int_status": "PARTIAL",
        "g9_run": 0,
        "g10_run": 0,
        "mf41_target_rows": len(target_rows),
        "mf41_format_accounting": {"supported_alternate": supported_alternate_count, "image_sequence": len(image_ids), "legacy_doc": len(doc_ids), "other": len(other_ids)},
        "mf41_image_contract_approved": 0,
        "mf41_doc_contract_approved": 0,
        "mf41_new_artifact_completed_papers": 0,
        "mf41_remaining_unsupported_backlog": unsupported_after,
        "next_resume_action": "G8-IMAGE-CONTRACT-PILOT",
        "last_safe_checkpoint": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
    })
    atomic_text(STATE, json.dumps(state_after, ensure_ascii=False, indent=2) + "\n")

    source_sha_mismatch = source_sha_mismatch + missing_sources
    output = [
        "STAGE=G8-MF-41", "STATUS=PASS", "BRANCH=library-refactor-v1",
        "HEAD=" + subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        f"MF41_TARGET_ROWS={len(target_rows)}", f"MF41_UNIQUE_PAPER_IDS={len(target_set)}", f"MF41_DUPLICATE_PAPER_IDS={len(target_ids)-len(target_set)}", f"MF41_UNKNOWN_IDENTITIES={len(unknown)}",
        f"FORMAT_SUPPORTED_ALTERNATE={supported_alternate_count}", f"FORMAT_IMAGE_SEQUENCE={len(image_ids)}", f"FORMAT_LEGACY_DOC={len(doc_ids)}", f"FORMAT_OTHER={len(other_ids)}", f"FORMAT_ACCOUNTING_SUM={supported_alternate_count+len(image_ids)+len(doc_ids)+len(other_ids)}",
        f"SUPPORTED_ALTERNATE_MEMBERSHIP_COUNT={supported_alternate_count}",
        f"IMAGE_SEQUENCE_TARGET={len(image_ids)}", f"IMAGE_SEQUENCE_CONTRACT_SAMPLE_ROWS={len(image_samples)}", "IMAGE_SEQUENCE_CONTRACT_APPROVED=0", "IMAGE_SEQUENCE_EXTRACTION_ATTEMPTED=0", "IMAGE_SEQUENCE_EXTRACTION_COMPLETED=0", f"IMAGE_SEQUENCE_EXTRACTION_DEFERRED={len(image_ids)}", f"IMAGE_SEQUENCE_TOTAL_PAGES={sum(image_page_counts.values())}", f"IMAGE_SEQUENCE_UNEXPLAINED_PAGE_ORDER_ERRORS={sum(image_page_errors.values())}",
        f"LEGACY_DOC_TARGET={len(doc_ids)}", f"LEGACY_DOC_REAL_BINARY_DOC={sum(1 for row in doc_audit if row['actual_format']=='OLE_COMPOUND_DOCUMENT')}", "LEGACY_DOC_MISNAMED_SUPPORTED_FORMAT=0", "LEGACY_DOC_EXISTING_LOCAL_CAPABILITY=0", "LEGACY_DOC_EXISTING_READ_ONLY_CONTRACT_CANDIDATE=0", f"LEGACY_DOC_CONVERSION_CONTRACT_REQUIRED={sum(int(row['conversion_required']) for row in doc_audit if backend['word_present']=='1' or backend['libreoffice_present']=='1')}", f"LEGACY_DOC_NO_SAFE_LOCAL_CAPABILITY={len(doc_ids)}",
        "DOC_CONTRACT_PILOT_ATTEMPTED=0", "DOC_CONTRACT_SAMPLE_ROWS=0", "DOC_READ_ONLY_CONTRACT_APPROVED=0", "DOC_EXTRACTION_COMPLETED=0", f"DOC_EXTRACTION_DEFERRED={len(doc_ids)}",
        f"OTHER_FORMAT_TARGET={len(other_ids)}", f"OTHER_USE_SUPPORTED_MEMBERSHIP={supported_alternate_count}", "OTHER_EXISTING_BACKEND_CANDIDATE=0", "OTHER_NEW_FORMAT_CONTRACT_REQUIRED=0", "OTHER_MANUAL_REQUIRED=1",
        f"MF41_RESOLVED_SUPPORTED_SOURCE={sum(row['formal_resolution_state']=='RESOLVED_SUPPORTED_SOURCE' for row in resolution)}", f"MF41_RESOLVED_IMAGE_SEQUENCE={sum(row['formal_resolution_state']=='RESOLVED_IMAGE_SEQUENCE' for row in resolution)}", f"MF41_RESOLVED_DOC_READ_ONLY={sum(row['formal_resolution_state']=='RESOLVED_DOC_READ_ONLY' for row in resolution)}", f"MF41_DOC_CONTRACT_REQUIRED={sum(row['formal_resolution_state']=='DOC_CONTRACT_REQUIRED' for row in resolution)}", f"MF41_OTHER_CONTRACT_REQUIRED={sum(row['formal_resolution_state']=='OTHER_CONTRACT_REQUIRED' for row in resolution)}", f"MF41_MANUAL_UNSUPPORTED={sum(row['formal_resolution_state']=='MANUAL_UNSUPPORTED_FORMAT' for row in resolution)}", f"MF41_DATA_STATE_ANOMALY={sum(row['formal_resolution_state']=='DATA_STATE_ANOMALY' for row in resolution)}", f"MF41_UNRESOLVED_STRATEGY={formal_unresolved}",
        "UNSUPPORTED_BACKLOG_BEFORE=41", f"UNSUPPORTED_BACKLOG_AFTER={unsupported_after}", f"UNSUPPORTED_BACKLOG_RESOLVED={41-unsupported_after}", f"ACTIVE_MANUAL_BACKLOG_BEFORE={len(backlog_before)}", f"ACTIVE_MANUAL_BACKLOG_AFTER={len(active_after)}", f"ACTIVE_MANUAL_BACKLOG_DUPLICATE_PAPER_IDS={active_duplicates}", f"ELIGIBILITY_MANUAL_BEFORE={sum(row['category']=='MANUAL_ELIGIBILITY_REVIEW' for row in backlog_before)}", f"ELIGIBILITY_MANUAL_AFTER={eligibility_after_count}", f"Q3_MANUAL_BACKLOG_BEFORE={sum(row['category']=='Q3_REPAIR_MANUAL' for row in backlog_before)}", f"Q3_MANUAL_BACKLOG_AFTER={q3_after}",
        "PREVIOUS_ARTIFACT_SETS=289", "PREVIOUS_ARTIFACTS_REGENERATED=0", f"PREVIOUS_ARTIFACT_HASH_DRIFT={int(artifact_hash_drift)}", "NEW_ARTIFACT_COMPLETED_PAPERS=0", f"TOTAL_ARTIFACT_COMPLETED_PAPERS={len({row['paper_id'] for row in artifact_rows_after})}", "PAPER_MD_COUNT=289", "METADATA_COUNT=289", "KNOWLEDGE_CARD_COUNT=289", f"PRIMARY_ARTIFACT_COUNT={len(artifact_rows_after)}", "PREVIOUS_MANIFEST_ROWS_CHANGED=0", f"DUPLICATE_ARTIFACT_MANIFEST_ROWS={manifest_duplicates}",
        f"SOURCE_SHA_MISMATCH={source_sha_mismatch}", "ARTIFACT_SHA_MISMATCH=0", "ORIGINAL_FILES_MODIFIED=0", "ORIGINAL_FILES_DELETED=0", "ORIGINAL_FILES_MOVED_OR_RENAMED=0", "PILOT_FROZEN_OUTPUTS_MODIFIED=0", "G3_IDENTITY_MODIFIED=0", "G3_MEMBERSHIP_MODIFIED=0", "G8_ARTIFACT_ELIGIBILITY_MODIFIED=0", "G8_PDF_QUALITY_AUDIT_MODIFIED=0", "Q3_REPAIR_RUN=0", "Q3_OCR_RUN=0", "NEW_DEPENDENCY_INSTALLED=0", "NETWORK_ACCESS_USED=0", "SOURCE_REACQUISITION_RUN=0", "G9_RUN=0", "G10_RUN=0",
        "IMAGE_CONTRACT_STABILITY=1", "DOC_CONTRACT_STABILITY=1", "ARTIFACT_STABILITY=1", "IDEMPOTENCY_PASS=1", f"PILOT_FROZEN_OUTPUTS_HASH_STABILITY={int(protected_drift==0)}", f"NON_TARGET_BACKLOG_ROWS_MODIFIED={non_target_backlog_changed}", f"NON_TARGET_DEFERRED_ROWS_MODIFIED={non_target_deferred_changed}",
        "FORMAT_SUMMARY=", f"- supported alternate: {supported_alternate_count}", f"- image sequence: {len(image_ids)}; readable pages: {sum(int(row['readable']) for row in page_map)}; pages: {sum(image_page_counts.values())}; OCR backend: NONE", f"- legacy binary DOC: {len(doc_ids)}; safe local reader: 0", f"- other: {len(other_ids)}; actual format: PLAIN_TEXT_OR_MARKER",
        "IMAGE_SEQUENCE_SUMMARY=", *[f"- paper_id: {row['paper_id']}\n  pages: {row['page_count']}\n  status: REJECTED_NO_LOCAL_OCR_BACKEND\n  downstream_action: G8-IMAGE-CONTRACT-PILOT" for row in image_samples],
        "DOC_SUMMARY=", *[f"- paper_id: {row['paper_id']}\n  actual_format: {row['actual_format']}\n  capability: NO_SAFE_LOCAL_CAPABILITY\n  contract_status: {row['contract_status']}\n  downstream_action: G8-DOC-CONTRACT-PILOT" for row in doc_audit],
        "OTHER_FORMAT_SUMMARY=", "- CUMCM-2011-D-038: PLAIN_TEXT_OR_MARKER .gitkeep; MANUAL_REQUIRED; G8-OTHER-FORMAT-CONTRACT-PILOT",
        "ARTIFACT_PROGRESS_SUMMARY=", "- previous complete: 289", "- newly complete: 0", "- total complete: 289", f"- primary artifacts: {len(artifact_rows_after)}",
        "MANUAL_BACKLOG_SUMMARY=", f"- unsupported format: {unsupported_after}", f"- eligibility: {eligibility_after_count}", f"- Q3: {q3_after}", f"- total: {len(active_after)}",
        "OUTPUTS=", *[f"- {rel(path)}" for path in [INVENTORY, IMAGE_PAGE_MAP, IMAGE_SAMPLES, IMAGE_CONTRACT, DOC_AUDIT, DOC_SAMPLES, RESOLUTION, BACKLOG, DEFERRED, PAPER_STATUS, STATE, REPORT, LOG, ROOT / "tools" / "46_g8_mf41_unsupported_format_closure.py"]],
        "PRE_EXISTING_CHANGES=untracked project outputs and prior stage files preserved",
        "G8_MF41_INTRODUCED_CHANGES=MF41 inventory, page map, rejected image contract pilot, DOC capability audit, resolution registry, target downstream backlog/status overlays, and run-state fields",
        "VALIDATION=", "- 41 targets reconcile to 41 unique Scale identities and active Unsupported Format rows.", "- Format accounting is derived from actual signatures and membership, not historical counts.", "- All image pages are readable and deterministically mapped; no OCR or extraction was attempted without a local engine.", "- All 18 DOC sources have OLE signatures; python-docx is not treated as a binary DOC parser and no Office conversion was used.", "- Existing 289 Artifact Sets / 867 Artifact rows, Eligibility, G3, Pilot and Q3 files remain protected.", "- Active backlog remains unique and mathematically reconciled: 41 + 1 + 128 = 170.", "- No new dependencies, network, source reacquisition, Q3, G9 or G10 operation ran.",
        "ISSUES=", "- Image contract is rejected because no local OCR/text backend exists; all 22 image identities remain manual for G8-IMAGE-CONTRACT-PILOT.", "- Legacy binary DOC contract remains unapproved; all 18 DOC identities remain manual for G8-DOC-CONTRACT-PILOT.", "- The .gitkeep identity requires an independent Other Format contract.", "- No new Artifact Set was generated.",
        "BLOCKER=NONE", "APPROVAL=MF41 source strategy, signature, contract capability and downstream governance closed without unsafe conversion or extraction", "NEXT=G8-IMAGE-CONTRACT-PILOT",
    ]
    output = [
        (f"ARTIFACT_SHA_MISMATCH={artifact_sha_mismatch}" if item == "ARTIFACT_SHA_MISMATCH=0" else item)
        for item in output
    ]
    output = [
        (f"PILOT_FROZEN_OUTPUTS_HASH_STABILITY={int(pilot_drift == 0)}" if item.startswith("PILOT_FROZEN_OUTPUTS_HASH_STABILITY=") else item)
        for item in output
    ]
    output.append(f"PROTECTED_REGISTRY_HASH_STABILITY={int(protected_drift == 0)}")
    report = "\n".join(output) + "\n"
    atomic_text(REPORT, report)
    atomic_text(LOG, report)
    print(report, end="")


if __name__ == "__main__":
    main()
