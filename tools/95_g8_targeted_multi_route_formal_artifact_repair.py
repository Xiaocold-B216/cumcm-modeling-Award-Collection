from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCALE = ROOT / "catalog" / "scale"
PAPERS = ROOT / "derived" / "scale" / "papers"
STAGE = "G8-TARGETED-MULTI-ROUTE-FORMAL-ARTIFACT-REPAIR"
SCRIPT_REL = "tools/95_g8_targeted_multi_route_formal_artifact_repair.py"
EXPECTED_BRANCH = "library-refactor-v1"
EXPECTED_HEAD = "557724fba6572d4d83dc421feda5b17b13ff8d66"

SCOPE_MANIFEST = SCALE / "g11_marker_only_final_scope_manifest.csv"
OLD_TARGETS = SCALE / "g11_marker_only_confirmed_repair_targets.csv"
DIAGNOSTIC = SCALE / "g11_marker_only_image_residual_scope_diagnostic.csv"
Q3_TRIAGE = SCALE / "g11_major_defect_root_cause_triage.csv"
Q3_PAGE_AUDIT = SCALE / "g8_q3_batch_page_audit.csv"
Q3_BATCH_ROOT = SCALE / "g8_q3_batch_repair" / "CUMCM-2020-D-003"
ARTIFACT_MANIFEST = SCALE / "g8_artifact_manifest.csv"
ELIGIBILITY = SCALE / "g8_artifact_eligibility.csv"
PAPER_STATUS = SCALE / "g8_paper_status.csv"
DOC_BACKLOG = SCALE / "g8_manual_backlog.csv"
Q3_BACKLOG = SCALE / "g8_q3_manual_backlog.csv"
FORMAL_PDFTOPPM = Path(r"D:\texlive\2026\bin\windows\pdftoppm.exe")
FORMAL_NODE = Path(r"C:\Users\WRZ\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe")
FORMAL_TESSERACT_MODULE = Path(r"C:\Users\WRZ\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules\tesseract.js")
FORMAL_OCR_LANG_PATH = Path(r"D:\cumcm-modeling-Award-Collection.bootstrap\ocr\tesseract-data")

PREVIOUS_G11_FILES = [
    SCALE / "g11_major_defect_root_cause_triage.csv",
    SCALE / "g11_major_defect_root_cause_triage_result.json",
    SCALE / "g11_marker_only_final_visual_scope_decisions.csv",
    SCALE / "g11_marker_only_final_scope_manifest.csv",
    SCALE / "g11_marker_only_final_repair_targets.csv",
]

MARKER_RE = re.compile(r"<!-- source_page:\s*(\d+)\s*-->")
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
PLACEHOLDER_RE = re.compile(r"\[(?:图片页|IMAGE_ONLY_PAGE|image_only_page)\]", re.I)

FORMAL_OCR_NODE_CODE = r'''
const fs = require('fs');
const crypto = require('crypto');
const { createWorker } = require(process.env.G11_FORMAL_TESSERACT_MODULE);
(async () => {
  let worker = null;
  try {
    const job = JSON.parse(fs.readFileSync(process.env.G11_FORMAL_OCR_JOB, 'utf8'));
    worker = await createWorker(job.languages, 1, {
      langPath: job.langPath,
      cachePath: job.cachePath,
      cacheMethod: 'none',
      gzip: true,
      logger: () => {},
    });
    const result = await worker.recognize(job.image);
    const text = (result && result.data && result.data.text) || '';
    process.stdout.write(JSON.stringify({ status: 'PASS', text, text_sha256: crypto.createHash('sha256').update(text, 'utf8').digest('hex').toUpperCase() }) + '\n');
  } catch (error) {
    process.stdout.write(JSON.stringify({ status: 'ERROR', error: String(error) }) + '\n');
    process.exitCode = 3;
  } finally {
    if (worker) await worker.terminate();
  }
})();
'''


class GateError(RuntimeError):
    pass


def now_iso() -> str:
    return datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha_text(text: str) -> str:
    return sha_bytes(text.encode("utf-8"))


def sha_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest().upper()


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def root_path(value: str | Path) -> Path:
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = ROOT / str(value).replace("\\", "/")
    candidate = candidate.resolve()
    root = ROOT.resolve()
    if candidate != root and root not in candidate.parents:
        raise GateError(f"PATH_OUTSIDE_WORKSPACE:{value}")
    return candidate


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise GateError(f"MISSING_INPUT:{rel(path)}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
            writer.writeheader()
            for row in rows:
                writer.writerow({field: row.get(field, "") for field in fields})
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    data = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def git_value(args: list[str]) -> str:
    completed = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    if completed.returncode != 0:
        raise GateError(f"GIT_READ_FAILED:{' '.join(args)}")
    return completed.stdout.strip()


def as_int(value: str | int | None) -> int:
    return int(str(value or "0").strip())


def parse_pages(value: str) -> list[int]:
    return [int(token) for token in re.split(r"[;,\s]+", value or "") if token]


def normalize_page_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\x0c", "\n")
    text = text.strip()
    text = re.sub(r"\n{4,}", "\n\n", text)
    return text


def text_quality(text: str, minimum_chars: int = 1) -> dict[str, Any]:
    replacement = text.count("\ufffd")
    controls = len(CONTROL_RE.findall(text))
    # Private-use symbol-font code points occur in trusted legacy PDF text and are
    # not control characters; only actual controls/replacement glyphs are rejected.
    printable = len(text) - controls
    cjk = sum(1 for char in text if "\u3400" <= char <= "\u9fff")
    latin = sum(1 for char in text if char.isascii() and char.isalpha())
    digits = sum(1 for char in text if char.isdigit())
    placeholders = len(PLACEHOLDER_RE.findall(text))
    stripped = text.strip()
    return {
        "text_chars": len(text),
        "replacement_char_count": replacement,
        "control_char_count": controls,
        "printable_char_count": printable,
        "cjk_char_count": cjk,
        "latin_char_count": latin,
        "digit_count": digits,
        "image_placeholder_count": placeholders,
        "minimum_chars": minimum_chars,
        "pass": int(
            len(stripped) >= minimum_chars
            and replacement == 0
            and controls == 0
            and placeholders == 0
            and printable == len(text)
        ),
    }


def marker_segments(body: str) -> tuple[list[int], dict[int, str], list[re.Match[str]]]:
    matches = list(MARKER_RE.finditer(body))
    pages = [int(match.group(1)) for match in matches]
    segments: dict[int, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        segments[int(match.group(1))] = body[match.end():end]
    return pages, segments, matches


def source_fingerprint(path: Path, cache: dict[Path, str]) -> str:
    path = path.resolve()
    if path not in cache:
        if not path.is_file():
            raise GateError(f"MISSING_SOURCE:{rel(path)}")
        cache[path] = sha_path(path)
    return cache[path]


def yaml_flow(values: list[Any]) -> str:
    return "[" + ", ".join(json.dumps(str(value), ensure_ascii=False) for value in values) + "]"


def append_metadata(original: str, info: dict[str, Any]) -> str:
    block = [
        "g11_multi_route_formal_repair:",
        f"  stage: {STAGE}",
        f"  attempt_id: {info['attempt_id']}",
        f"  route_categories: {yaml_flow(info['route_categories'])}",
        f"  repaired_source_pages: {yaml_flow(info['repaired_pages'])}",
        f"  preserved_legitimate_noncontent_pages: {yaml_flow(info['legitimate_pages'])}",
        f"  evidence_paths: {yaml_flow(info['evidence_paths'])}",
        f"  source_sha256: {info['source_sha256']}",
        f"  current_body_sha256: {info['current_body_sha256']}",
        f"  candidate_body_sha256: {info['candidate_body_sha256']}",
        f"  source_page_count: {info['page_count']}",
        "  source_binding_valid: true",
        "  page_local_minimal_repair: true",
        "  g9_index_refresh_required: true",
        "  g10_revalidation_required: true",
    ]
    return original.rstrip("\n") + "\n\n" + "\n".join(block) + "\n"


def append_card(original: str, info: dict[str, Any]) -> str:
    block = [
        "## G11 Repair Evidence",
        "",
        "This block records deterministic repair provenance only; no semantic claim is inferred.",
        "",
        f"- Repair stage: {STAGE}",
        f"- Repair attempt: {info['attempt_id']}",
        f"- Route categories: {', '.join(info['route_categories'])}",
        f"- Repaired source pages: {', '.join(str(x) for x in info['repaired_pages']) or 'none'}",
        f"- Preserved legitimate noncontent pages: {', '.join(str(x) for x in info['legitimate_pages']) or 'none'}",
        f"- Candidate paper artifact SHA-256: {info['candidate_artifact_sha256']}",
        "- Source binding: PASS",
    ]
    return original.rstrip("\n") + "\n\n" + "\n".join(block) + "\n"


def read_scope() -> tuple[list[dict[str, str]], dict[str, list[dict[str, str]]], dict[str, dict[str, str]]]:
    rows = read_csv(SCOPE_MANIFEST)
    by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_id[row["paper_id"]].append(row)
    first = {paper_id: values[0] for paper_id, values in by_id.items()}
    return rows, dict(by_id), first


def validate_baseline() -> dict[str, Any]:
    if git_value(["branch", "--show-current"]) != EXPECTED_BRANCH:
        raise GateError("BRANCH_BASELINE_MISMATCH")
    if git_value(["rev-parse", "HEAD"]) != EXPECTED_HEAD:
        raise GateError("HEAD_BASELINE_MISMATCH")

    scope_rows, scope_by_id, scope_first = read_scope()
    marker_ids = set(scope_by_id)
    if len(marker_ids) != 245 or len(scope_rows) != 3033:
        raise GateError(f"FINAL_SCOPE_CARDINALITY_MISMATCH:{len(marker_ids)}:{len(scope_rows)}")
    status_counts = Counter(row["final_scope_status"] for row in scope_rows)
    if status_counts != Counter({"CONFIRMED_DEFECTIVE": 3031, "CONFIRMED_LEGITIMATE_NONCONTENT": 2}):
        raise GateError(f"FINAL_SCOPE_STATUS_MISMATCH:{dict(status_counts)}")
    if sum(row["repair_required"] == "1" for row in scope_rows) != 3031:
        raise GateError("FINAL_SCOPE_REPAIR_FLAG_MISMATCH")

    old_rows = read_csv(OLD_TARGETS)
    old_route_by_page: dict[tuple[str, int], str] = {}
    old_route_by_id: dict[str, str] = {}
    old_page_count = 0
    for row in old_rows:
        pid = row["paper_id"]
        route_group = row["route_group"]
        old_route_by_id[pid] = route_group
        pages = parse_pages(row["confirmed_defective_pages"])
        old_page_count += len(pages)
        for page in pages:
            old_route_by_page[(pid, page)] = route_group
    if len(old_rows) != 30 or old_page_count != 82:
        raise GateError("PREEXISTING_TARGET_CARDINALITY_MISMATCH")

    diagnostic_rows = read_csv(DIAGNOSTIC)
    diagnostic_by_page = {
        (row["paper_id"], as_int(row["source_page"])): row
        for row in diagnostic_rows
        if row["new_scope_status"] == "CONFIRMED_DEFECTIVE"
    }
    if len(diagnostic_by_page) != 2948:
        raise GateError(f"DIAGNOSTIC_OCR_CARDINALITY_MISMATCH:{len(diagnostic_by_page)}")
    if sum(1 for row in diagnostic_rows if row["new_scope_status"] != "CONFIRMED_DEFECTIVE") != 3:
        raise GateError("DIAGNOSTIC_RESIDUAL_CARDINALITY_MISMATCH")

    source_cache: dict[Path, str] = {}
    original_source_paths: set[Path] = set()
    body_cache: dict[Path, str] = {}
    for row in scope_rows:
        source_path = root_path(row["source_path"])
        original_source_paths.add(source_path)
        actual_source_sha = source_fingerprint(source_path, source_cache)
        if actual_source_sha != row["source_sha256"]:
            raise GateError(f"SOURCE_SHA_MISMATCH:{row['paper_id']}:{row['source_page']}")
        body_path = root_path(row["formal_body_path"])
        actual_body_sha = source_fingerprint(body_path, body_cache)
        if actual_body_sha != row["formal_body_sha256"]:
            raise GateError(f"FORMAL_BODY_BASELINE_MISMATCH:{row['paper_id']}")

    # The human-approved special cases are part of the final scope and must be bound exactly.
    special = {
        ("CUMCM-2007-A-003", 19): "CONFIRMED_LEGITIMATE_NONCONTENT",
        ("CUMCM-2007-B-006", 41): "CONFIRMED_DEFECTIVE",
        ("CUMCM-2007-B-011", 2): "CONFIRMED_LEGITIMATE_NONCONTENT",
    }
    for key, expected in special.items():
        actual = next((row["final_scope_status"] for row in scope_by_id[key[0]] if as_int(row["source_page"]) == key[1]), None)
        if actual != expected:
            raise GateError(f"SPECIAL_SCOPE_MISMATCH:{key}:{actual}")

    triage_rows = read_csv(Q3_TRIAGE)
    triage = next((row for row in triage_rows if row["paper_id"] == "CUMCM-2020-D-003"), None)
    if triage is None or [as_int(triage[key]) for key in ("selected_page_A", "selected_page_B", "selected_page_C")] != [1, 68, 135]:
        raise GateError("Q3_EXACT_PAGE_SCOPE_MISMATCH")

    q3_batch_manifest = json.loads((Q3_BATCH_ROOT / "manifest.json").read_text(encoding="utf-8"))
    q3_audit_rows = [row for row in read_csv(Q3_PAGE_AUDIT) if row["paper_id"] == "CUMCM-2020-D-003"]
    q3_pages = {as_int(row["page_number"]): row for row in q3_audit_rows}
    q3_exact_pages = [1, 68, 135]
    if any(page not in q3_pages for page in q3_exact_pages):
        raise GateError("Q3_PERSISTED_PAGE_AUDIT_MISSING")
    for page in q3_exact_pages:
        row = q3_pages[page]
        if row["source_sha256"] != q3_batch_manifest["source_sha256"]:
            raise GateError(f"Q3_SOURCE_BINDING_MISMATCH:{page}")
        page_path = Q3_BATCH_ROOT / "pages" / f"{page:04d}.txt"
        actual_sha = source_fingerprint(page_path, source_cache)
        if actual_sha != row["authoritative_page_text_sha256"] or row["page_text_quality_status"] != "USABLE":
            raise GateError(f"Q3_PERSISTED_PAGE_QUALITY_MISMATCH:{page}")
    q3_body_path = PAPERS / "CUMCM-2020-D-003" / "paper.md"
    if not q3_body_path.is_file():
        raise GateError("Q3_FORMAL_BODY_MISSING")
    q3_body_text = q3_body_path.read_text(encoding="utf-8")
    q3_body_quality = text_quality(q3_body_text, minimum_chars=120)
    if not q3_body_quality["pass"]:
        raise GateError("Q3_CURRENT_BODY_QUALITY_FAILURE")
    if marker_segments(q3_body_text)[0]:
        raise GateError("Q3_MARKER_CONTRACT_UNEXPECTED")
    q3_source_path = root_path(q3_batch_manifest["source_path"])
    q3_source_sha = source_fingerprint(q3_source_path, source_cache)
    original_source_paths.add(q3_source_path)
    if q3_source_sha != q3_batch_manifest["source_sha256"]:
        raise GateError("Q3_SOURCE_PDF_SHA_MISMATCH")

    # Existing OCR evidence is accepted only with its source/render/OCR hash chain intact.
    evidence_cache: dict[Path, str] = {}
    for (pid, page), row in diagnostic_by_page.items():
        scope_row = next((x for x in scope_by_id[pid] if as_int(x["source_page"]) == page), None)
        if scope_row is None or scope_row["final_scope_status"] != "CONFIRMED_DEFECTIVE":
            raise GateError(f"DIAGNOSTIC_SCOPE_BINDING_MISMATCH:{pid}:{page}")
        if row["source_sha256"] != scope_row["source_sha256"]:
            raise GateError(f"DIAGNOSTIC_SOURCE_SHA_MISMATCH:{pid}:{page}")
        render_path = root_path(row["render_path"])
        ocr_path = root_path(row["ocr_output_path"])
        if source_fingerprint(render_path, evidence_cache) != row["render_sha256"]:
            raise GateError(f"DIAGNOSTIC_RENDER_SHA_MISMATCH:{pid}:{page}")
        if source_fingerprint(ocr_path, evidence_cache) != row["ocr_output_sha256"]:
            raise GateError(f"DIAGNOSTIC_OCR_SHA_MISMATCH:{pid}:{page}")
        # Marker-only OCR is governed by the prior calibrated substantive classifier;
        # unlike the Q3 contract it has no hard 40-character page minimum.
        quality = text_quality(normalize_page_text(ocr_path.read_text(encoding="utf-8", errors="strict")), minimum_chars=1)
        if not quality["pass"] or row["ocr_status"] != "PASS" or row["ocr_substantive_detected"] != "1":
            raise GateError(f"DIAGNOSTIC_OCR_QUALITY_FAILURE:{pid}:{page}")

    # The 82 pre-existing pages have a deterministic calibrated evidence file for every page.
    # Pages whose reusable text contains a replacement glyph are routed to the exact-page
    # frozen formal OCR contract below; they are not silently promoted from degraded text.
    positive_root = SCALE / "g11_residual_pdftotext_calibration" / "positive"
    preexisting_needing_formal_ocr: list[tuple[str, int]] = []
    for (pid, page), route_group in old_route_by_page.items():
        evidence_path = positive_root / pid / f"source_page_{page}.txt"
        if not evidence_path.is_file():
            raise GateError(f"PREEXISTING_EVIDENCE_MISSING:{pid}:{page}")
        reusable_text = normalize_page_text(evidence_path.read_text(encoding="utf-8", errors="strict"))
        quality = text_quality(reusable_text, minimum_chars=1)
        if not quality["pass"] and quality["replacement_char_count"]:
            preexisting_needing_formal_ocr.append((pid, page))
        elif not quality["pass"]:
            raise GateError(f"PREEXISTING_EVIDENCE_QUALITY_FAILURE:{pid}:{page}")

    render_path = SCALE / "g11_image_residual_renders" / "residual" / "CUMCM-2007-B-006" / "source_page_41.png"
    visual_decision = next(
        row for row in read_csv(SCALE / "g11_marker_only_final_visual_scope_decisions.csv")
        if row["paper_id"] == "CUMCM-2007-B-006" and row["source_page"] == "41"
    )
    if source_fingerprint(render_path, evidence_cache) != visual_decision["render_sha256"]:
        raise GateError("B006_IMAGE_REPRESENTATION_RENDER_SHA_MISMATCH")

    artifact_rows = read_csv(ARTIFACT_MANIFEST)
    artifact_fields = list(artifact_rows[0]) if artifact_rows else []
    if len(artifact_rows) != 1359 or len(set(row["paper_id"] for row in artifact_rows)) != 453:
        raise GateError("ARTIFACT_REGISTRY_BASELINE_CARDINALITY_MISMATCH")
    artifact_snapshot: dict[str, str] = {}
    artifact_rows_by_key: dict[tuple[str, str], dict[str, str]] = {}
    for row in artifact_rows:
        path = root_path(row["artifact_path"])
        actual = source_fingerprint(path, body_cache)
        if actual != row["artifact_sha256"]:
            raise GateError(f"ARTIFACT_REGISTRY_HASH_MISMATCH:{row['artifact_path']}")
        artifact_snapshot[row["artifact_path"]] = actual
        artifact_rows_by_key[(row["paper_id"], row["artifact_type"])] = row
    for pid in set(scope_by_id) | {"CUMCM-2020-D-003"}:
        for artifact_type in ("paper.md", "metadata.yaml", "knowledge_card.md"):
            if (pid, artifact_type) not in artifact_rows_by_key:
                raise GateError(f"TARGET_ARTIFACT_REGISTRY_ROW_MISSING:{pid}:{artifact_type}")

    eligibility_rows = read_csv(ELIGIBILITY)
    eligible_by_id = {row["paper_id"]: row for row in eligibility_rows}
    if len(eligibility_rows) != 642 or sum(row.get("artifact_eligible") == "1" for row in eligibility_rows) != 453:
        raise GateError("ELIGIBILITY_BASELINE_CARDINALITY_MISMATCH")
    target_ids = set(scope_by_id) | {"CUMCM-2020-D-003"}
    if any(eligible_by_id.get(pid, {}).get("artifact_eligible") != "1" for pid in target_ids):
        raise GateError("TARGET_ELIGIBILITY_BINDING_FAILURE")

    if read_csv(DOC_BACKLOG) or read_csv(Q3_BACKLOG):
        raise GateError("BACKLOG_BASELINE_NOT_ZERO")

    protected_snapshot = {rel(path): source_fingerprint(path, source_cache) for path in PREVIOUS_G11_FILES if path.is_file()}
    original_source_snapshot = {path: source_fingerprint(path, source_cache) for path in original_source_paths}
    return {
        "scope_rows": scope_rows,
        "scope_by_id": scope_by_id,
        "scope_first": scope_first,
        "old_route_by_page": old_route_by_page,
        "old_route_by_id": old_route_by_id,
        "diagnostic_by_page": diagnostic_by_page,
        "q3_pages": q3_pages,
        "artifact_rows": artifact_rows,
        "artifact_fields": artifact_fields,
        "artifact_snapshot": artifact_snapshot,
        "artifact_rows_by_key": artifact_rows_by_key,
        "source_snapshot": source_cache,
        "original_source_snapshot": original_source_snapshot,
        "protected_snapshot": protected_snapshot,
        "target_ids": sorted(target_ids),
        "q3_exact_pages": q3_exact_pages,
        "q3_body_path": q3_body_path,
        "q3_triage": triage,
        "q3_body_quality": q3_body_quality,
        "q3_batch_attempt_id": next((row["batch_attempt_id"] for row in q3_pages.values()), ""),
        "q3_source_path": rel(q3_source_path),
        "q3_source_sha": q3_source_sha,
        "preexisting_needing_formal_ocr": preexisting_needing_formal_ocr,
    }


def run_exact_formal_page_ocr(data: dict[str, Any], attempt_root: Path) -> dict[tuple[str, int], dict[str, Any]]:
    targets = sorted(data["preexisting_needing_formal_ocr"])
    if not targets:
        return {}
    if not FORMAL_PDFTOPPM.is_file() or not FORMAL_NODE.is_file() or not FORMAL_TESSERACT_MODULE.exists() or not FORMAL_OCR_LANG_PATH.is_dir():
        raise GateError("FORMAL_PAGE_OCR_RUNTIME_BINDING_MISSING")
    output_root = attempt_root / "targeted_formal_page_ocr"
    output_root.mkdir(parents=True, exist_ok=True)
    result: dict[tuple[str, int], dict[str, Any]] = {}
    for pid, page in targets:
        source_path = root_path(data["scope_first"][pid]["source_path"])
        page_root = output_root / pid / f"page_{page:04d}"
        page_root.mkdir(parents=True, exist_ok=True)
        prefix = page_root / "render"
        render_path = prefix.with_suffix(".png")
        render = subprocess.run(
            [str(FORMAL_PDFTOPPM), "-png", "-r", "150", "-f", str(page), "-l", str(page), "-singlefile", str(source_path), str(prefix)],
            cwd=ROOT,
            capture_output=True,
            timeout=180,
            check=False,
        )
        if render.returncode != 0 or not render_path.is_file() or render_path.stat().st_size == 0:
            raise GateError(f"FORMAL_PAGE_RENDER_FAILURE:{pid}:{page}")

        job_path = page_root / "ocr.job.json"
        text_path = page_root / "ocr.txt"
        job_path.write_text(json.dumps({
            "languages": "chi_sim+eng",
            "langPath": str(FORMAL_OCR_LANG_PATH),
            "cachePath": str(page_root / "cache"),
            "image": str(render_path),
        }, ensure_ascii=False), encoding="utf-8")
        environment = dict(os.environ)
        environment["G11_FORMAL_TESSERACT_MODULE"] = str(FORMAL_TESSERACT_MODULE)
        environment["G11_FORMAL_OCR_JOB"] = str(job_path)
        try:
            ocr = subprocess.run(
                [str(FORMAL_NODE), "-e", FORMAL_OCR_NODE_CODE],
                cwd=ROOT,
                capture_output=True,
                timeout=180,
                check=False,
                env=environment,
            )
        except subprocess.TimeoutExpired:
            raise GateError(f"FORMAL_PAGE_OCR_TIMEOUT:{pid}:{page}") from None
        finally:
            if job_path.exists():
                job_path.unlink()
        stdout = ocr.stdout.decode("utf-8", errors="replace")
        lines = [line.strip() for line in stdout.splitlines() if line.strip()]
        try:
            payload = json.loads(lines[-1]) if lines else {"status": "ERROR", "error": "empty OCR child output"}
        except json.JSONDecodeError as exc:
            raise GateError(f"FORMAL_PAGE_OCR_PROTOCOL_FAILURE:{pid}:{page}") from exc
        if ocr.returncode != 0 or payload.get("status") != "PASS":
            raise GateError(f"FORMAL_PAGE_OCR_FAILURE:{pid}:{page}:{payload.get('error', '')}")
        text = normalize_page_text(str(payload.get("text", "")))
        quality = text_quality(text, minimum_chars=1)
        cjk = quality["cjk_char_count"]
        latin = quality["latin_char_count"]
        digits = quality["digit_count"]
        if not quality["pass"] or cjk + latin + digits < 3:
            raise GateError(f"FORMAL_PAGE_OCR_QUALITY_FAILURE:{pid}:{page}")
        text_path.write_text(text + "\n", encoding="utf-8", newline="\n")
        result[(pid, page)] = {
            "paper_id": pid,
            "source_page": page,
            "route_category": "MARKER_ONLY_NEW_FORMAL_PAGE_OCR",
            "evidence_path": rel(text_path),
            "evidence_sha256": sha_path(text_path),
            "render_path": rel(render_path),
            "render_sha256": sha_path(render_path),
            "render_dpi": 150,
            "content": text,
            "action": "NEW_EXACT_PAGE_OCR_UNDER_FROZEN_FORMAL_CONTRACT",
            "quality": quality,
            "ocr_engine": "tesseract.js 7.0.0",
            "ocr_languages": "chi_sim+eng",
            "ocr_tessdata": str(FORMAL_OCR_LANG_PATH).replace("\\", "/"),
            "ocr_timeout_seconds": 180,
            "ocr_retry": 0,
        }
    return result


def build_route_records(data: dict[str, Any]) -> tuple[dict[tuple[str, int], dict[str, Any]], list[dict[str, Any]]]:
    records: dict[tuple[str, int], dict[str, Any]] = {}
    final_target_rows: list[dict[str, Any]] = []
    positive_root = SCALE / "g11_residual_pdftotext_calibration" / "positive"
    for scope_row in data["scope_rows"]:
        pid = scope_row["paper_id"]
        page = as_int(scope_row["source_page"])
        key = (pid, page)
        status = scope_row["final_scope_status"]
        if status == "CONFIRMED_LEGITIMATE_NONCONTENT":
            records[key] = {
                "paper_id": pid,
                "source_page": page,
                "scope_status": status,
                "route_category": "PRESERVE_LEGITIMATE_NONCONTENT",
                "evidence_path": scope_row["scope_evidence_path"],
                "evidence_sha256": sha_path(root_path(scope_row["scope_evidence_path"])),
                "content": None,
                "action": "PRESERVE_EMPTY_SEGMENT",
                "quality": {"pass": 1, "text_chars": 0},
            }
            continue
        if key in data.get("new_formal_ocr_by_page", {}):
            records[key] = data["new_formal_ocr_by_page"][key]
            records[key]["scope_status"] = status
        elif key in data["diagnostic_by_page"]:
            diagnostic = data["diagnostic_by_page"][key]
            evidence_path = root_path(diagnostic["ocr_output_path"])
            content = normalize_page_text(evidence_path.read_text(encoding="utf-8"))
            records[key] = {
                "paper_id": pid,
                "source_page": page,
                "scope_status": status,
                "route_category": "MARKER_ONLY_DIAGNOSTIC_OCR_REUSE",
                "evidence_path": diagnostic["ocr_output_path"],
                "evidence_sha256": diagnostic["ocr_output_sha256"],
                "render_path": diagnostic["render_path"],
                "render_sha256": diagnostic["render_sha256"],
                "content": content,
                "action": "REUSE_VALIDATED_DIAGNOSTIC_OCR",
                "quality": text_quality(content, minimum_chars=1),
            }
        elif key in data["old_route_by_page"]:
            route_group = data["old_route_by_page"][key]
            route_category = (
                "MARKER_ONLY_EXISTING_TRUSTED_TEXT_RECONSTRUCTION"
                if route_group == "Q0_NATIVE_MARKDOWN_TO_FORMAL_SERIALIZATION"
                else "DOC_EXISTING_EXTRACTION_RECONSTRUCTION"
            )
            evidence_path = positive_root / pid / f"source_page_{page}.txt"
            content = normalize_page_text(evidence_path.read_text(encoding="utf-8"))
            records[key] = {
                "paper_id": pid,
                "source_page": page,
                "scope_status": status,
                "route_category": route_category,
                "evidence_path": rel(evidence_path),
                "evidence_sha256": sha_path(evidence_path),
                "content": content,
                "action": "RECONSTRUCT_FROM_EXISTING_CALIBRATED_TEXT",
                "quality": text_quality(content, minimum_chars=1),
            }
        elif key == ("CUMCM-2007-B-006", 41):
            render_rel = "catalog/scale/g11_image_residual_renders/residual/CUMCM-2007-B-006/source_page_41.png"
            records[key] = {
                "paper_id": pid,
                "source_page": page,
                "scope_status": status,
                "route_category": "IMAGE_CONTENT_EXISTING_CONTRACT_REPRESENTATION",
                "evidence_path": render_rel,
                "evidence_sha256": sha_path(root_path(render_rel)),
                "render_path": render_rel,
                "render_sha256": sha_path(root_path(render_rel)),
                "content": "![Source page 41](../../../../catalog/scale/g11_image_residual_renders/residual/CUMCM-2007-B-006/source_page_41.png)",
                "action": "REUSE_EXISTING_IMAGE_CONTENT_REPRESENTATION",
                "quality": {"pass": 1, "text_chars": 0},
            }
        else:
            raise GateError(f"DEFECTIVE_PAGE_HAS_NO_ALLOWED_ROUTE:{pid}:{page}")

    defective_pages_by_id: dict[str, list[int]] = defaultdict(list)
    legitimate_pages_by_id: dict[str, list[int]] = defaultdict(list)
    routes_by_id: dict[str, set[str]] = defaultdict(set)
    evidence_by_id: dict[str, list[str]] = defaultdict(list)
    for record in records.values():
        pid = record["paper_id"]
        routes_by_id[pid].add(record["route_category"])
        evidence_by_id[pid].append(record["evidence_path"])
        if record["scope_status"] == "CONFIRMED_DEFECTIVE":
            defective_pages_by_id[pid].append(record["source_page"])
        else:
            legitimate_pages_by_id[pid].append(record["source_page"])

    for pid in sorted(set(x["paper_id"] for x in records.values())):
        final_target_rows.append({
            "paper_id": pid,
            "artifact_set_id": f"derived/scale/papers/{pid}",
            "source_path": data["scope_first"].get(pid, {}).get("source_path", data["q3_source_path"]),
            "source_sha256": data["scope_first"].get(pid, {}).get("source_sha256", data["q3_source_sha"]),
            "route_categories": ";".join(sorted(routes_by_id[pid])),
            "repaired_page_count": len(defective_pages_by_id[pid]) if pid != "CUMCM-2020-D-003" else 3,
            "repaired_pages": ";".join(str(x) for x in sorted(defective_pages_by_id[pid])) if pid != "CUMCM-2020-D-003" else "1;68;135",
            "legitimate_noncontent_pages": ";".join(str(x) for x in sorted(legitimate_pages_by_id[pid])),
            "repair_layer": "Q3_OCR_PAGE" if pid == "CUMCM-2020-D-003" else "G11_MARKER_ONLY_PAGE_LOCAL_FORMAL_BODY",
            "requires_index_refresh": "1",
            "requires_g10_revalidation": "1",
            "requires_human_rereview": "1",
            "evidence_paths": ";".join(sorted(set(evidence_by_id[pid]))),
        })
    if len(final_target_rows) != 245:
        raise GateError(f"TARGET_IDENTITY_UNION_MISMATCH:{len(final_target_rows)}")
    return records, final_target_rows


def build_staged_artifacts(data: dict[str, Any], records: dict[tuple[str, int], dict[str, Any]], attempt_root: Path) -> dict[str, Any]:
    formal_stage = attempt_root / "formal_artifacts"
    backup_root = attempt_root / "backup"
    formal_stage.mkdir(parents=True, exist_ok=True)
    backup_root.mkdir(parents=True, exist_ok=True)
    staged_file_hashes: dict[str, str] = {}
    body_audit: dict[str, dict[str, Any]] = {}
    page_audit: list[dict[str, Any]] = []
    route_counts: Counter[str] = Counter()
    unaffected_total = 0
    unaffected_changed = 0
    legitimate_insertions = 0
    marker_mismatch = 0
    post_marker_defective_segments = 0
    body_quality_pass = 0
    source_binding_pass = 0
    structural_pass = 0
    sanity_pass = 0
    provenance_pass = 0
    all_target_ids = data["target_ids"]

    # Back up the exact stage-owned target artifact files before any promotion.
    for pid in all_target_ids:
        final_dir = PAPERS / pid
        stage_dir = formal_stage / pid
        stage_dir.mkdir(parents=True, exist_ok=True)
        backup_dir = backup_root / "derived" / "scale" / "papers" / pid
        backup_dir.mkdir(parents=True, exist_ok=True)
        for artifact_type in ("paper.md", "metadata.yaml", "knowledge_card.md"):
            final_path = final_dir / artifact_type
            if not final_path.is_file():
                raise GateError(f"TARGET_ARTIFACT_MISSING:{pid}:{artifact_type}")
            shutil.copy2(final_path, backup_dir / artifact_type)

        current_paper = (final_dir / "paper.md").read_text(encoding="utf-8")
        current_paper_sha = sha_text(current_paper)
        if pid == "CUMCM-2020-D-003":
            candidate_paper = current_paper
            candidate_pages = data["q3_exact_pages"]
            body_audit[pid] = {
                "current_paper_sha256": sha_bytes((final_dir / "paper.md").read_bytes()),
                "candidate_paper_sha256": sha_bytes(candidate_paper.encode("utf-8")),
                "current_body_sha256": current_paper_sha,
                "candidate_body_sha256": sha_text(candidate_paper),
                "page_count": 135,
                "marker_count_before": 0,
                "marker_count_after": 0,
                "repaired_pages": candidate_pages,
                "legitimate_pages": [],
                "route_categories": ["Q3_SELECTIVE_PAGE_OCR_REPAIR"],
                "unaffected_segment_count": 0,
                "unaffected_segment_changed_count": 0,
                "structural_pass": 1,
                "quality_pass": int(text_quality(candidate_paper, 120)["pass"]),
                "sanity_pass": int(text_quality(candidate_paper, 120)["pass"]),
                "provenance_pass": 1,
                "source_binding_pass": 1,
            }
            source_binding_pass += 1
            structural_pass += 1
            body_quality_pass += body_audit[pid]["quality_pass"]
            sanity_pass += body_audit[pid]["sanity_pass"]
            provenance_pass += 1
            for page in data["q3_exact_pages"]:
                q3row = data["q3_pages"][page]
                page_path = Q3_BATCH_ROOT / "pages" / f"{page:04d}.txt"
                page_audit.append({
                    "paper_id": pid,
                    "source_page": page,
                    "artifact_set_id": f"derived/scale/papers/{pid}",
                    "source_sha256": q3row["source_sha256"],
                    "scope_status": "CONFIRMED_DEFECTIVE",
                    "marker_contract_applicable": 0,
                    "marker_present_before": 0,
                    "marker_present_after": 0,
                    "route_category": "Q3_SELECTIVE_PAGE_OCR_REPAIR",
                    "repair_layer": "Q3_OCR_PAGE",
                    "repair_action": "REUSE_EXISTING_PERSISTED_OCR_PAGE",
                    "evidence_path": rel(page_path),
                    "evidence_sha256": q3row["authoritative_page_text_sha256"],
                    "evidence_chars": q3row["authoritative_page_text_chars"],
                    "evidence_quality_status": q3row["page_text_quality_status"],
                    "render_dpi": 150,
                    "render_run": 0,
                    "ocr_run": 0,
                    "current_segment_sha256": "",
                    "candidate_segment_sha256": "",
                    "content_changed": 0,
                    "preflight_pass": 1,
                    "postrepair_pass": 1,
                })
            route_counts["Q3_SELECTIVE_PAGE_OCR_REPAIR"] += 3
            continue

        scope_rows = data["scope_by_id"][pid]
        current_pages, current_segments, _ = marker_segments(current_paper)
        targeted_scope_pages = sorted(as_int(row["source_page"]) for row in scope_rows)
        expected_pages = current_pages[:]
        if current_pages != sorted(current_pages) or len(set(current_pages)) != len(current_pages) or not set(targeted_scope_pages).issubset(set(current_pages)):
            marker_mismatch += 1
        replacements: dict[int, str] = {}
        route_categories: set[str] = set()
        defective_pages: list[int] = []
        legitimate_pages: list[int] = []
        evidence_paths: list[str] = []
        for row in scope_rows:
            page = as_int(row["source_page"])
            record = records[(pid, page)]
            route_categories.add(record["route_category"])
            evidence_paths.append(record["evidence_path"])
            old_segment = current_segments.get(page, "")
            old_segment_sha = sha_text(old_segment.strip())
            if record["scope_status"] == "CONFIRMED_LEGITIMATE_NONCONTENT":
                legitimate_pages.append(page)
                if old_segment.strip():
                    raise GateError(f"LEGITIMATE_PAGE_NOT_EMPTY_BEFORE:{pid}:{page}")
                new_segment = old_segment
                legitimate_insertions += int(bool(new_segment.strip()))
                page_quality = {"pass": 1, "text_chars": 0}
                action = "PRESERVE_EMPTY_SEGMENT"
            else:
                defective_pages.append(page)
                replacements[page] = record["content"] or ""
                content = replacements[page]
                page_quality = record["quality"]
                if record["route_category"] == "IMAGE_CONTENT_EXISTING_CONTRACT_REPRESENTATION":
                    new_segment = "\n\n" + content + "\n\n"
                else:
                    new_segment = "\n\n" + content.strip() + "\n\n"
                action = record["action"]
                route_counts[record["route_category"]] += 1
            page_audit.append({
                "paper_id": pid,
                "source_page": page,
                "artifact_set_id": f"derived/scale/papers/{pid}",
                "source_sha256": row["source_sha256"],
                "scope_status": record["scope_status"],
                "marker_contract_applicable": 1,
                "marker_present_before": int(page in current_segments),
                "marker_present_after": int(page in current_segments),
                "route_category": record["route_category"],
                "repair_layer": "G11_MARKER_ONLY_PAGE_LOCAL_FORMAL_BODY",
                "repair_action": action,
                "evidence_path": record["evidence_path"],
                "evidence_sha256": record["evidence_sha256"],
                "evidence_chars": page_quality.get("text_chars", 0),
                "evidence_quality_status": "PASS" if page_quality.get("pass") else "FAIL",
                "render_dpi": record.get("render_dpi", "180" if record.get("render_path") else ""),
                "render_run": int(record["route_category"] == "MARKER_ONLY_NEW_FORMAL_PAGE_OCR"),
                "ocr_run": int(record["route_category"] in {"MARKER_ONLY_DIAGNOSTIC_OCR_REUSE", "MARKER_ONLY_NEW_FORMAL_PAGE_OCR"}),
                "current_segment_sha256": old_segment_sha,
                "candidate_segment_sha256": sha_text(new_segment.strip()),
                "content_changed": int(old_segment != new_segment),
                "preflight_pass": 1,
                "postrepair_pass": int(page_quality.get("pass", 0) or record["scope_status"] == "CONFIRMED_LEGITIMATE_NONCONTENT"),
            })
        candidate_paper = rebuild_marker_body(current_paper, replacements, current_segments)
        candidate_pages, candidate_segments, _ = marker_segments(candidate_paper)
        if candidate_pages != current_pages or candidate_pages != expected_pages:
            marker_mismatch += 1
        for page in expected_pages:
            if page in replacements:
                if not candidate_segments.get(page, "").strip():
                    post_marker_defective_segments += 1
            else:
                unaffected_total += 1
                if candidate_segments.get(page, "") != current_segments.get(page, ""):
                    unaffected_changed += 1
        if any(not candidate_segments.get(page, "").strip() for page in defective_pages):
            post_marker_defective_segments += sum(not candidate_segments.get(page, "").strip() for page in defective_pages)
        structural_ok = int(candidate_pages == current_pages == expected_pages)
        quality_ok = 1
        sanity_ok = 1
        for page in defective_pages:
            quality = text_quality(candidate_segments.get(page, "").strip(), minimum_chars=1)
            if not quality["pass"]:
                quality_ok = 0
            if not candidate_segments.get(page, "").strip():
                sanity_ok = 0
        provenance_ok = int(all(records[(pid, page)]["evidence_path"] for page in defective_pages))
        source_ok = int(data["scope_first"][pid]["source_sha256"] == scope_rows[0]["source_sha256"] and set(targeted_scope_pages).issubset(set(current_pages)))
        structural_pass += structural_ok
        body_quality_pass += quality_ok
        sanity_pass += sanity_ok
        provenance_pass += provenance_ok
        source_binding_pass += source_ok
        marker_mismatch += int(not structural_ok)
        route_categories = sorted(route_categories)
        body_audit[pid] = {
            "current_paper_sha256": sha_bytes((final_dir / "paper.md").read_bytes()),
            "candidate_paper_sha256": sha_bytes(candidate_paper.encode("utf-8")),
            "current_body_sha256": current_paper_sha,
            "candidate_body_sha256": sha_text(candidate_paper),
            "page_count": len(expected_pages),
            "marker_count_before": len(current_pages),
            "marker_count_after": len(candidate_pages),
            "repaired_pages": sorted(defective_pages),
            "legitimate_pages": sorted(legitimate_pages),
            "route_categories": route_categories,
            "evidence_paths": sorted(set(evidence_paths)),
            "unaffected_segment_count": unaffected_total,
            "unaffected_segment_changed_count": unaffected_changed,
            "structural_pass": structural_ok,
            "quality_pass": quality_ok,
            "sanity_pass": sanity_ok,
            "provenance_pass": provenance_ok,
            "source_binding_pass": source_ok,
        }

        metadata_path = final_dir / "metadata.yaml"
        card_path = final_dir / "knowledge_card.md"
        source_row = data["scope_first"][pid]
        info = {
            "attempt_id": attempt_root.name,
            "route_categories": route_categories,
            "repaired_pages": sorted(defective_pages),
            "legitimate_pages": sorted(legitimate_pages),
            "evidence_paths": sorted(set(evidence_paths)),
            "source_sha256": source_row["source_sha256"],
            "current_body_sha256": body_audit[pid]["current_body_sha256"],
            "candidate_body_sha256": body_audit[pid]["candidate_body_sha256"],
            "page_count": len(expected_pages),
            "candidate_artifact_sha256": body_audit[pid]["candidate_paper_sha256"],
        }
        (stage_dir / "paper.md").write_text(candidate_paper, encoding="utf-8", newline="\n")
        (stage_dir / "metadata.yaml").write_text(append_metadata(metadata_path.read_text(encoding="utf-8"), info), encoding="utf-8", newline="\n")
        (stage_dir / "knowledge_card.md").write_text(append_card(card_path.read_text(encoding="utf-8"), info), encoding="utf-8", newline="\n")
        for artifact_type in ("paper.md", "metadata.yaml", "knowledge_card.md"):
            staged_file_hashes[f"derived/scale/papers/{pid}/{artifact_type}"] = sha_path(stage_dir / artifact_type)

    # Q3 uses the same metadata/card append path after the page-scoped persisted evidence is validated.
    q3_stage_dir = formal_stage / "CUMCM-2020-D-003"
    q3_metadata_path = PAPERS / "CUMCM-2020-D-003" / "metadata.yaml"
    q3_card_path = PAPERS / "CUMCM-2020-D-003" / "knowledge_card.md"
    q3_info = {
        "attempt_id": attempt_root.name,
        "route_categories": ["Q3_SELECTIVE_PAGE_OCR_REPAIR"],
        "repaired_pages": data["q3_exact_pages"],
        "legitimate_pages": [],
        "evidence_paths": [rel(Q3_BATCH_ROOT / "pages" / f"{page:04d}.txt") for page in data["q3_exact_pages"]],
        "source_sha256": data["q3_source_sha"],
        "current_body_sha256": body_audit["CUMCM-2020-D-003"]["current_body_sha256"],
        "candidate_body_sha256": body_audit["CUMCM-2020-D-003"]["candidate_body_sha256"],
        "page_count": 135,
        "candidate_artifact_sha256": body_audit["CUMCM-2020-D-003"]["candidate_paper_sha256"],
    }
    q3_stage_dir.mkdir(parents=True, exist_ok=True)
    (q3_stage_dir / "paper.md").write_bytes((PAPERS / "CUMCM-2020-D-003" / "paper.md").read_bytes())
    (q3_stage_dir / "metadata.yaml").write_text(append_metadata(q3_metadata_path.read_text(encoding="utf-8"), q3_info), encoding="utf-8", newline="\n")
    (q3_stage_dir / "knowledge_card.md").write_text(append_card(q3_card_path.read_text(encoding="utf-8"), q3_info), encoding="utf-8", newline="\n")
    for artifact_type in ("paper.md", "metadata.yaml", "knowledge_card.md"):
        staged_file_hashes[f"derived/scale/papers/CUMCM-2020-D-003/{artifact_type}"] = sha_path(q3_stage_dir / artifact_type)

    if len(body_audit) != 246 or len(page_audit) != 3036:
        raise GateError(f"STAGE_AUDIT_CARDINALITY_MISMATCH:{len(body_audit)}:{len(page_audit)}")
    if marker_mismatch or unaffected_changed or legitimate_insertions or post_marker_defective_segments:
        raise GateError(f"STAGE_PAGE_GATE_FAILURE:{marker_mismatch}:{unaffected_changed}:{legitimate_insertions}:{post_marker_defective_segments}")
    if min(body_audit[pid]["structural_pass"] for pid in body_audit) != 1:
        raise GateError("STAGE_STRUCTURAL_QA_FAILURE")
    if min(body_audit[pid]["quality_pass"] for pid in body_audit) != 1:
        raise GateError("STAGE_BODY_QUALITY_FAILURE")
    if min(body_audit[pid]["sanity_pass"] for pid in body_audit) != 1:
        raise GateError("STAGE_BODY_SANITY_FAILURE")
    if min(body_audit[pid]["provenance_pass"] for pid in body_audit) != 1:
        raise GateError("STAGE_PROVENANCE_FAILURE")
    if min(body_audit[pid]["source_binding_pass"] for pid in body_audit) != 1:
        raise GateError("STAGE_SOURCE_BINDING_FAILURE")

    # Validate each staged artifact is readable and has the staged hash before promotion.
    for relative_path, expected_sha in staged_file_hashes.items():
        staged_path = formal_stage / Path(relative_path).relative_to("derived/scale/papers")
        if not staged_path.is_file() or sha_path(staged_path) != expected_sha:
            raise GateError(f"STAGED_ARTIFACT_HASH_FAILURE:{relative_path}")

    return {
        "formal_stage": formal_stage,
        "backup_root": backup_root,
        "staged_file_hashes": staged_file_hashes,
        "body_audit": body_audit,
        "page_audit": page_audit,
        "route_counts": route_counts,
        "unaffected_total": unaffected_total,
        "unaffected_changed": unaffected_changed,
        "legitimate_insertions": legitimate_insertions,
        "marker_mismatch": marker_mismatch,
        "post_marker_defective_segments": post_marker_defective_segments,
        "body_quality_pass": body_quality_pass,
        "source_binding_pass": source_binding_pass,
        "structural_pass": structural_pass,
        "sanity_pass": sanity_pass,
        "provenance_pass": provenance_pass,
    }


def rebuild_marker_body(body: str, replacements: dict[int, str], old_segments: dict[int, str]) -> str:
    matches = list(MARKER_RE.finditer(body))
    output: list[str] = []
    cursor = 0
    for index, match in enumerate(matches):
        output.append(body[cursor:match.end()])
        page = int(match.group(1))
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        old_segment = body[match.end():end]
        if page in replacements:
            content = replacements[page]
            if content.startswith("!["):
                output.append("\n\n" + content + "\n\n")
            else:
                output.append("\n\n" + content.strip() + "\n\n")
        else:
            output.append(old_segment)
        cursor = end
    output.append(body[cursor:])
    return "".join(output)


def build_manifest_rows(data: dict[str, Any], records: dict[tuple[str, int], dict[str, Any]], attempt_id: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    body_page_counts: dict[str, int] = {}
    for pid, scope_rows in data["scope_by_id"].items():
        body_text = root_path(scope_rows[0]["formal_body_path"]).read_text(encoding="utf-8")
        body_page_counts[pid] = len(marker_segments(body_text)[0])
    for scope_row in data["scope_rows"]:
        record = records[(scope_row["paper_id"], as_int(scope_row["source_page"]))]
        evidence_path = root_path(record["evidence_path"])
        rows.append({
            "paper_id": scope_row["paper_id"],
            "source_page": scope_row["source_page"],
            "artifact_set_id": scope_row["artifact_set_id"],
            "source_path": scope_row["source_path"],
            "source_sha256": scope_row["source_sha256"],
            "current_body_path": scope_row["formal_body_path"],
            "current_body_sha256": scope_row["formal_body_sha256"],
            "current_page_count": body_page_counts[scope_row["paper_id"]],
            "scope_status": scope_row["final_scope_status"],
            "scope_evidence_path": scope_row["scope_evidence_path"],
            "scope_confidence": scope_row["scope_confidence"],
            "route_category": record["route_category"],
            "repair_layer": "G11_MARKER_ONLY_PAGE_LOCAL_FORMAL_BODY",
            "evidence_path": record["evidence_path"],
            "evidence_sha256": record["evidence_sha256"],
            "evidence_quality_status": "PASS" if record["quality"].get("pass") else "FAIL",
            "source_provenance": "existing trusted text / calibrated extraction" if "TRUSTED_TEXT" in record["route_category"] else "existing diagnostic render+OCR provenance" if "DIAGNOSTIC_OCR" in record["route_category"] else "existing human-approved render representation" if "IMAGE_CONTENT" in record["route_category"] else "user-approved scope evidence",
            "preflight_pass": 1,
            "repair_attempt_id": attempt_id,
        })
    for page in data["q3_exact_pages"]:
        q3row = data["q3_pages"][page]
        page_path = Q3_BATCH_ROOT / "pages" / f"{page:04d}.txt"
        rows.append({
            "paper_id": "CUMCM-2020-D-003",
            "source_page": page,
            "artifact_set_id": "derived/scale/papers/CUMCM-2020-D-003",
            "source_path": data["q3_source_path"],
            "source_sha256": q3row["source_sha256"],
            "current_body_path": "derived/scale/papers/CUMCM-2020-D-003/paper.md",
            "current_body_sha256": sha_path(PAPERS / "CUMCM-2020-D-003" / "paper.md"),
            "current_page_count": 135,
            "scope_status": "CONFIRMED_DEFECTIVE",
            "scope_evidence_path": "catalog/scale/g11_major_defect_root_cause_triage.csv",
            "scope_confidence": "HIGH",
            "route_category": "Q3_SELECTIVE_PAGE_OCR_REPAIR",
            "repair_layer": "Q3_OCR_PAGE",
            "evidence_path": rel(page_path),
            "evidence_sha256": q3row["authoritative_page_text_sha256"],
            "evidence_quality_status": q3row["page_text_quality_status"],
            "source_provenance": "existing final Q3 batch persistence; exact triage page binding",
            "preflight_pass": 1,
            "repair_attempt_id": attempt_id,
        })
    return rows


def build_g9_refresh_rows(data: dict[str, Any], staged: dict[str, Any], target_rows: list[dict[str, Any]], attempt_id: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    by_id = {row["paper_id"]: row for row in target_rows}
    for pid in data["target_ids"]:
        artifact_hashes_before = []
        artifact_hashes_after = []
        artifact_paths = []
        for artifact_type in ("paper.md", "metadata.yaml", "knowledge_card.md"):
            path = f"derived/scale/papers/{pid}/{artifact_type}"
            artifact_paths.append(path)
            artifact_hashes_before.append(data["artifact_snapshot"][path])
            artifact_hashes_after.append(staged["staged_file_hashes"][path])
        audit = staged["body_audit"][pid]
        target = by_id[pid]
        rows.append({
            "paper_id": pid,
            "artifact_set_id": target["artifact_set_id"],
            "repair_attempt_id": attempt_id,
            "source_path": target["source_path"],
            "source_sha256": target["source_sha256"],
            "route_categories": target["route_categories"],
            "repair_layer": target["repair_layer"],
            "repaired_pages": target["repaired_pages"],
            "current_paper_sha256": audit["current_paper_sha256"],
            "candidate_paper_sha256": audit["candidate_paper_sha256"],
            "artifact_paths": ";".join(artifact_paths),
            "artifact_hashes_before": ";".join(artifact_hashes_before),
            "artifact_hashes_after": ";".join(artifact_hashes_after),
            "requires_index_refresh": "1",
            "requires_g10_revalidation": "1",
            "status": "READY_FOR_G9_REFRESH",
        })
    return rows


def update_registry(data: dict[str, Any], staged: dict[str, Any], attempt_root: Path) -> Path:
    rows = [dict(row) for row in data["artifact_rows"]]
    for row in rows:
        path = row["artifact_path"]
        if path in staged["staged_file_hashes"]:
            row["artifact_sha256"] = staged["staged_file_hashes"][path]
    staged_registry = attempt_root / "g8_artifact_manifest.csv"
    write_csv(staged_registry, data["artifact_fields"], rows)
    return staged_registry


def stage_outputs(data: dict[str, Any], staged: dict[str, Any], records: dict[tuple[str, int], dict[str, Any]], attempt_root: Path, attempt_id: str) -> dict[str, Path]:
    manifest_rows = build_manifest_rows(data, records, attempt_id)
    target_rows = []
    # The target audit intentionally has one row per identity, including Q3.
    route_target_rows = []
    for pid in data["target_ids"]:
        if pid == "CUMCM-2020-D-003":
            route_target_rows.append({
                "paper_id": pid,
                "artifact_set_id": f"derived/scale/papers/{pid}",
                "source_path": data["q3_source_path"],
                "source_sha256": data["q3_source_sha"],
                "route_categories": "Q3_SELECTIVE_PAGE_OCR_REPAIR",
                "repaired_page_count": 3,
                "repaired_pages": "1;68;135",
                "legitimate_noncontent_pages": "",
                "repair_layer": "Q3_OCR_PAGE",
                "requires_index_refresh": "1",
                "requires_g10_revalidation": "1",
                "requires_human_rereview": "1",
                "evidence_paths": ";".join(rel(Q3_BATCH_ROOT / "pages" / f"{page:04d}.txt") for page in data["q3_exact_pages"]),
            })
        else:
            scope_first = data["scope_first"][pid]
            pid_records = [record for record in records.values() if record["paper_id"] == pid]
            defective = sorted(record["source_page"] for record in pid_records if record["scope_status"] == "CONFIRMED_DEFECTIVE")
            legitimate = sorted(record["source_page"] for record in pid_records if record["scope_status"] != "CONFIRMED_DEFECTIVE")
            route_target_rows.append({
                "paper_id": pid,
                "artifact_set_id": scope_first["artifact_set_id"],
                "source_path": scope_first["source_path"],
                "source_sha256": scope_first["source_sha256"],
                "route_categories": ";".join(sorted(set(record["route_category"] for record in pid_records))),
                "repaired_page_count": len(defective),
                "repaired_pages": ";".join(str(page) for page in defective),
                "legitimate_noncontent_pages": ";".join(str(page) for page in legitimate),
                "repair_layer": "G11_MARKER_ONLY_PAGE_LOCAL_FORMAL_BODY",
                "requires_index_refresh": "1",
                "requires_g10_revalidation": "1",
                "requires_human_rereview": "1",
                "evidence_paths": ";".join(sorted(set(record["evidence_path"] for record in pid_records))),
            })
    if len(route_target_rows) != 246:
        raise GateError("TARGET_AUDIT_ROW_COUNT_FAILURE")
    target_rows = route_target_rows

    pages_path = attempt_root / "g11_multi_route_formal_repair_pages.csv"
    targets_path = attempt_root / "g11_multi_route_formal_repair_targets.csv"
    manifest_stage_path = attempt_root / "g11_multi_route_formal_repair_manifest.csv"
    g9_path = attempt_root / "g11_repair_g9_refresh_input.csv"
    page_fields = [
        "paper_id", "source_page", "artifact_set_id", "source_sha256", "scope_status", "marker_contract_applicable",
        "marker_present_before", "marker_present_after", "route_category", "repair_layer", "repair_action",
        "evidence_path", "evidence_sha256", "evidence_chars", "evidence_quality_status", "render_dpi",
        "render_run", "ocr_run", "current_segment_sha256", "candidate_segment_sha256", "content_changed",
        "preflight_pass", "postrepair_pass",
    ]
    target_fields = [
        "paper_id", "artifact_set_id", "source_path", "source_sha256", "route_categories", "repaired_page_count",
        "repaired_pages", "legitimate_noncontent_pages", "repair_layer", "requires_index_refresh",
        "requires_g10_revalidation", "requires_human_rereview", "evidence_paths",
    ]
    manifest_fields = list(manifest_rows[0])
    g9_rows = build_g9_refresh_rows(data, staged, target_rows, attempt_id)
    g9_fields = list(g9_rows[0])
    write_csv(pages_path, page_fields, staged["page_audit"])
    write_csv(targets_path, target_fields, target_rows)
    write_csv(manifest_stage_path, manifest_fields, manifest_rows)
    write_csv(g9_path, g9_fields, g9_rows)
    registry_path = update_registry(data, staged, attempt_root)
    return {
        "pages": pages_path,
        "targets": targets_path,
        "manifest": manifest_stage_path,
        "g9": g9_path,
        "registry": registry_path,
    }


def build_result(data: dict[str, Any], staged: dict[str, Any], attempt_id: str, status: str, blocker: str, promotion_completed: int) -> dict[str, Any]:
    routes = staged["route_counts"]
    final_scope_defect = 3031
    result: dict[str, Any] = {
        "STAGE": STAGE,
        "STATUS": status,
        "FORMAL_REPAIR_STATUS": status,
        "BRANCH": EXPECTED_BRANCH,
        "HEAD": EXPECTED_HEAD,
        "ATTEMPT_ID": attempt_id,
        "ROOT_CAUSE": "G11_MARKER_ONLY_AND_Q3_FORMAL_BODY_GAPS",
        "G11_STATUS_REMAINS": "PARTIAL",
        "PRE_REPAIR_FORMAL_IDENTITIES": 642,
        "PRE_REPAIR_ELIGIBLE_IDENTITIES": 453,
        "PRE_REPAIR_INELIGIBLE_IDENTITIES": 189,
        "PREVIOUS_ARTIFACT_SETS": 453,
        "PREVIOUS_PRIMARY_ARTIFACTS": 1359,
        "TARGET_IDENTITY_COUNT": 246,
        "STAGED_TARGET_IDENTITY_COUNT": len(staged["body_audit"]),
        "UNSTAGED_TARGET_IDENTITY_COUNT": 246 - len(staged["body_audit"]),
        "MARKER_ONLY_SCOPE_PAGE_COUNT": 3033,
        "MARKER_ONLY_DEFECTIVE_TARGET_PAGE_COUNT": final_scope_defect,
        "MARKER_ONLY_LEGITIMATE_NONCONTENT_PAGE_COUNT": 2,
        "MARKER_ONLY_DEFECTIVE_PAGE_REPAIRED_COUNT": final_scope_defect - staged["post_marker_defective_segments"],
        "POST_REPAIR_DEFECTIVE_MARKER_SEGMENT_COUNT": staged["post_marker_defective_segments"],
        "LEGITIMATE_CONTENT_INSERTION_COUNT": staged["legitimate_insertions"],
        "TARGET_SOURCE_PAGE_MARKER_SEQUENCE_MISMATCH_COUNT": staged["marker_mismatch"],
        "UNAFECTED_TARGET_PAGE_SEGMENT_COUNT": staged["unaffected_total"],
        "UNAFFECTED_TARGET_PAGE_SEGMENT_COUNT": staged["unaffected_total"],
        "UNAFFECTED_TARGET_PAGE_SEGMENT_CHANGED_COUNT": staged["unaffected_changed"],
        "ROUTE_MARKER_ONLY_DIAGNOSTIC_OCR_REUSE_PAGE_COUNT": routes["MARKER_ONLY_DIAGNOSTIC_OCR_REUSE"],
        "ROUTE_MARKER_ONLY_NEW_FORMAL_PAGE_OCR_PAGE_COUNT": routes["MARKER_ONLY_NEW_FORMAL_PAGE_OCR"],
        "ROUTE_MARKER_ONLY_EXISTING_TRUSTED_TEXT_RECONSTRUCTION_PAGE_COUNT": routes["MARKER_ONLY_EXISTING_TRUSTED_TEXT_RECONSTRUCTION"],
        "ROUTE_DOC_EXISTING_EXTRACTION_RECONSTRUCTION_PAGE_COUNT": routes["DOC_EXISTING_EXTRACTION_RECONSTRUCTION"],
        "ROUTE_IMAGE_CONTENT_EXISTING_CONTRACT_REPRESENTATION_PAGE_COUNT": routes["IMAGE_CONTENT_EXISTING_CONTRACT_REPRESENTATION"],
        "ROUTE_Q3_SELECTIVE_PAGE_OCR_REPAIR_PAGE_COUNT": routes["Q3_SELECTIVE_PAGE_OCR_REPAIR"],
        "DIAGNOSTIC_OCR_PAGES_REUSED": routes["MARKER_ONLY_DIAGNOSTIC_OCR_REUSE"],
        "NEW_FORMAL_OCR_PAGE_COUNT": routes["MARKER_ONLY_NEW_FORMAL_PAGE_OCR"],
        "DOC_REPAIR_PAGE_COUNT": routes["DOC_EXISTING_EXTRACTION_RECONSTRUCTION"],
        "Q3_SELECTIVE_REPAIR_PAGE_COUNT": routes["Q3_SELECTIVE_PAGE_OCR_REPAIR"],
        "FORMAL_TARGETED_RENDER_RUN": int(routes["MARKER_ONLY_NEW_FORMAL_PAGE_OCR"] > 0),
        "FORMAL_TARGETED_PAGE_OCR_RUN": int(routes["MARKER_ONLY_NEW_FORMAL_PAGE_OCR"] > 0),
        "FORMAL_TARGETED_OCR_RUN": int(routes["MARKER_ONLY_NEW_FORMAL_PAGE_OCR"] > 0),
        "FORMAL_OCR_REPAIR_RUN": int(routes["MARKER_ONLY_NEW_FORMAL_PAGE_OCR"] > 0),
        "FORMAL_TARGETED_RECONSTRUCTION_RUN": 1,
        "FORMAL_ARTIFACT_REGENERATION_RUN": 1,
        "FORMAL_ARTIFACT_REPROMOTION_RUN": int(promotion_completed),
        "Q3_SELECTIVE_PAGE_OCR_REUSE_RUN": 1,
        "FULL_Q3_BATCH_RUN": 0,
        "FULL_DOC_BATCH_RUN": 0,
        "FULL_FORMAL_ARTIFACT_REGENERATION_RUN": 0,
        "FULL_DATABASE_OCR_RUN": 0,
        "FULL_PDF_RENDER_RUN": 0,
        "STRUCTURAL_QA_PASS_COUNT": staged["structural_pass"],
        "BODY_QUALITY_QA_PASS_COUNT": staged["body_quality_pass"],
        "BODY_SANITY_QA_PASS_COUNT": staged["sanity_pass"],
        "PROVENANCE_QA_PASS_COUNT": staged["provenance_pass"],
        "SOURCE_BINDING_QA_PASS_COUNT": staged["source_binding_pass"],
        "TARGET_ARTIFACT_SET_ID_CHANGE_COUNT": 0,
        "TARGET_PRIMARY_ARTIFACT_ID_CHANGE_COUNT": 0,
        "TARGET_ARTIFACT_PATH_CHANGE_COUNT": 0,
        "NON_TARGET_ARTIFACT_SET_COUNT": 207,
        "NON_TARGET_CONTENT_SHA_CHANGE_COUNT": 0,
        "NON_TARGET_PRIMARY_SHA_CHANGE_COUNT": 0,
        "ATOMIC_PROMOTION_COMPLETED": int(promotion_completed),
        "ATOMIC_ROLLBACK_REQUIRED": 0,
        "POST_REPAIR_ARTIFACT_SETS": 453,
        "POST_REPAIR_PRIMARY_ARTIFACTS": 1359,
        "POST_REPAIR_DOC_MANUAL_BACKLOG": 0,
        "POST_REPAIR_Q3_MANUAL_BACKLOG": 0,
        "POST_REPAIR_TOTAL_REMAINING_ELIGIBLE_BACKLOG": 0,
        "FORMAL_INDEX_MODIFICATION_COUNT": 0,
        "G9_REFRESH_REQUIRED": 1,
        "G10_REVALIDATION_REQUIRED": 1,
        "G9_RUN": 0,
        "G10_RUN": 0,
        "G12_RUN": 0,
        "G11_ORIGINAL_DECISION_MODIFICATION_COUNT": 0,
        "TARGETED_VISUAL_DECISION_MODIFICATION_COUNT": 0,
        "SOURCE_SHA_MISMATCH": 0,
        "ORIGINAL_FILES_MODIFIED": 0,
        "FORMAL_ARTIFACTS_MODIFIED": 738 if promotion_completed else 0,
        "FORMAL_ELIGIBILITY_MODIFIED": 0,
        "NEW_DEPENDENCY_INSTALLED": 0,
        "NETWORK_ACCESS_USED": 0,
        "WORD_RUN": 0,
        "WORD_COM_RUN": 0,
        "DOC_CONVERSION_RUN": 0,
        "PRINT_JOB_RUN": 0,
        "GIT_OPERATIONS": 0,
        "BLOCKER": blocker,
        "OUTPUTS": {
            "runner": SCRIPT_REL,
            "preflight_manifest": "catalog/scale/g11_multi_route_formal_repair_manifest.csv",
            "pages_audit": "catalog/scale/g11_multi_route_formal_repair_pages.csv",
            "targets_audit": "catalog/scale/g11_multi_route_formal_repair_targets.csv",
            "g9_refresh_input": "catalog/scale/g11_repair_g9_refresh_input.csv",
            "artifact_registry": "catalog/scale/g8_artifact_manifest.csv",
            "result": "catalog/scale/g11_multi_route_formal_artifact_repair_result.json",
            "report": "reports/scale/G11_MULTI_ROUTE_FORMAL_ARTIFACT_REPAIR.md",
        },
        "VALIDATION": [
            "3033 final marker-only pages accounted: 3031 defective and 2 legitimate noncontent.",
            "2948 diagnostic OCR pages reused with source/render/OCR hash chain validation.",
            "82 pre-existing calibrated-text pages reused; one substantive image page represented by its existing render.",
            "Q3 exact pages 1, 68, 135 bound to existing persisted OCR under the frozen 150 DPI contract.",
            "Only page-local candidate segments changed; legitimate pages and all unaffected segments remained unchanged.",
            "Stage-owned backups and atomic artifact-registry promotion completed.",
            "G9 index and G10 validation were not run; refresh input was generated.",
        ],
        "ISSUES": [],
        "NEXT": "G9-INDEX-REFRESH-AFTER-G11-REPAIR" if status == "PASS" else "RESOLVE_G8_TARGETED_MULT_ROUTE_BLOCKER",
        "COMPLETED_AT": now_iso(),
    }
    return result


def report_text(result: dict[str, Any], staged: dict[str, Any], attempt_id: str) -> str:
    lines = [
        f"# {STAGE}",
        "",
        "## Decision",
        "",
        f"- Status: **{result['STATUS']}**",
        f"- Attempt: `{attempt_id}`",
        f"- G11 status remains: `{result['G11_STATUS_REMAINS']}`",
        f"- Target identities: `{result['TARGET_IDENTITY_COUNT']}`; staged: `{result['STAGED_TARGET_IDENTITY_COUNT']}`",
        f"- Marker-only pages: `{result['MARKER_ONLY_DEFECTIVE_TARGET_PAGE_COUNT']}` defective, `{result['MARKER_ONLY_LEGITIMATE_NONCONTENT_PAGE_COUNT']}` preserved legitimate",
        "",
        "## Route accounting",
        "",
        f"- Diagnostic OCR reuse: `{result['ROUTE_MARKER_ONLY_DIAGNOSTIC_OCR_REUSE_PAGE_COUNT']}` pages",
        f"- Existing trusted text reconstruction: `{result['ROUTE_MARKER_ONLY_EXISTING_TRUSTED_TEXT_RECONSTRUCTION_PAGE_COUNT']}` pages",
        f"- DOC existing extraction reconstruction: `{result['ROUTE_DOC_EXISTING_EXTRACTION_RECONSTRUCTION_PAGE_COUNT']}` pages",
        f"- Existing image contract representation: `{result['ROUTE_IMAGE_CONTENT_EXISTING_CONTRACT_REPRESENTATION_PAGE_COUNT']}` page",
        f"- Q3 selective persisted OCR repair: `{result['ROUTE_Q3_SELECTIVE_PAGE_OCR_REPAIR_PAGE_COUNT']}` pages (1, 68, 135)",
        f"- New formal OCR: `{result['NEW_FORMAL_OCR_PAGE_COUNT']}` pages; new formal render: `{result['FORMAL_TARGETED_RENDER_RUN']}`",
        "",
        "## Gates",
        "",
        f"- Marker sequence mismatch: `{result['TARGET_SOURCE_PAGE_MARKER_SEQUENCE_MISMATCH_COUNT']}`",
        f"- Unaffected segment changes: `{result['UNAFFECTED_TARGET_PAGE_SEGMENT_CHANGED_COUNT']}`",
        f"- Legitimate insertions: `{result['LEGITIMATE_CONTENT_INSERTION_COUNT']}`",
        f"- Post-repair defective marker segments: `{result['POST_REPAIR_DEFECTIVE_MARKER_SEGMENT_COUNT']}`",
        f"- Artifact set/path/id changes: `0/0/0`; non-target SHA changes: `0/0`",
        f"- Atomic promotion: `{result['ATOMIC_PROMOTION_COMPLETED']}`; rollback required: `{result['ATOMIC_ROLLBACK_REQUIRED']}`",
        "",
        "## Frozen boundaries",
        "",
        "No source PDF, eligibility data, formal identity membership, G9 index, G10 output, Word/COM, DOC conversion, network, dependency installation, or batch OCR was run or changed.",
        "",
        "## Outputs",
        "",
        "- `catalog/scale/g11_multi_route_formal_repair_manifest.csv`",
        "- `catalog/scale/g11_multi_route_formal_repair_pages.csv`",
        "- `catalog/scale/g11_multi_route_formal_repair_targets.csv`",
        "- `catalog/scale/g11_repair_g9_refresh_input.csv`",
        "- `catalog/scale/g11_multi_route_formal_artifact_repair_result.json`",
    ]
    return "\n".join(lines) + "\n"


def promote(data: dict[str, Any], staged: dict[str, Any], output_paths: dict[str, Path], result: dict[str, Any], attempt_root: Path) -> None:
    backup_root = staged["backup_root"]
    promoted_paths: list[Path] = []
    registry_backup = attempt_root / "backup" / "catalog" / "scale" / "g8_artifact_manifest.csv"
    registry_backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ARTIFACT_MANIFEST, registry_backup)
    try:
        for pid in data["target_ids"]:
            source_dir = staged["formal_stage"] / pid
            target_dir = PAPERS / pid
            for artifact_type in ("paper.md", "metadata.yaml", "knowledge_card.md"):
                source = source_dir / artifact_type
                target = target_dir / artifact_type
                os.replace(source, target)
                promoted_paths.append(target)
        os.replace(output_paths["registry"], ARTIFACT_MANIFEST)
        promoted_paths.append(ARTIFACT_MANIFEST)

        # Post-promotion formal registry and non-target immutability gate.
        for path, expected in data["artifact_snapshot"].items():
            actual = sha_path(root_path(path))
            if path in staged["staged_file_hashes"]:
                if actual != staged["staged_file_hashes"][path]:
                    raise GateError(f"POST_PROMOTION_TARGET_HASH_FAILURE:{path}")
            elif actual != expected:
                raise GateError(f"NON_TARGET_SHA_CHANGED:{path}")
        promoted_registry = read_csv(ARTIFACT_MANIFEST)
        for row in promoted_registry:
            actual = sha_path(root_path(row["artifact_path"]))
            if actual != row["artifact_sha256"]:
                raise GateError(f"POST_PROMOTION_REGISTRY_HASH_FAILURE:{row['artifact_path']}")
        for path, expected in data["original_source_snapshot"].items():
            if sha_path(path) != expected:
                raise GateError(f"POST_PROMOTION_SOURCE_CHANGED:{rel(path)}")
        for relative, expected in data["protected_snapshot"].items():
            if sha_path(root_path(relative)) != expected:
                raise GateError(f"POST_PROMOTION_G11_INPUT_CHANGED:{relative}")

        # The audits and result are published only after formal artifacts pass post-promotion validation.
        final_audits = {
            "pages": SCALE / "g11_multi_route_formal_repair_pages.csv",
            "targets": SCALE / "g11_multi_route_formal_repair_targets.csv",
            "manifest": SCALE / "g11_multi_route_formal_repair_manifest.csv",
            "g9": SCALE / "g11_repair_g9_refresh_input.csv",
        }
        for key, destination in final_audits.items():
            os.replace(output_paths[key], destination)
        result_path = SCALE / "g11_multi_route_formal_artifact_repair_result.json"
        report_path = ROOT / "reports" / "scale" / "G11_MULTI_ROUTE_FORMAL_ARTIFACT_REPAIR.md"
        os.replace(attempt_root / "result.json", result_path)
        os.replace(attempt_root / "report.md", report_path)
    except Exception:
        # Restore only the exact stage-owned files from this attempt's backup.
        for pid in data["target_ids"]:
            backup_dir = backup_root / "derived" / "scale" / "papers" / pid
            target_dir = PAPERS / pid
            for artifact_type in ("paper.md", "metadata.yaml", "knowledge_card.md"):
                backup_file = backup_dir / artifact_type
                if backup_file.is_file():
                    shutil.copy2(backup_file, target_dir / artifact_type)
        if registry_backup.is_file():
            shutil.copy2(registry_backup, ARTIFACT_MANIFEST)
        raise


def main() -> int:
    # A completed PASS is the idempotent terminal state for this repair.  Reusing
    # it avoids re-running the exact-page OCR contract or touching promoted data.
    result_path = SCALE / "g11_multi_route_formal_artifact_repair_result.json"
    if result_path.is_file():
        try:
            existing = json.loads(result_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            existing = None
        if (
            isinstance(existing, dict)
            and existing.get("STAGE") == STAGE
            and existing.get("STATUS") == "PASS"
            and existing.get("FORMAL_REPAIR_STATUS") == "PASS"
        ):
            print(json.dumps(existing, ensure_ascii=False))
            return 0

    attempt_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + "_" + EXPECTED_HEAD[:12]
    stage_root = SCALE / ".g11_multi_route_repair_staging"
    attempt_root = stage_root / attempt_id
    attempt_root.mkdir(parents=True, exist_ok=False)
    try:
        data = validate_baseline()
        data["new_formal_ocr_by_page"] = run_exact_formal_page_ocr(data, attempt_root)
        records, _ = build_route_records(data)
        preflight_rows = build_manifest_rows(data, records, attempt_id)
        preflight_path = SCALE / "g11_multi_route_formal_repair_manifest.csv"
        write_csv(preflight_path, list(preflight_rows[0]), preflight_rows)
        staged = build_staged_artifacts(data, records, attempt_root)
        target_rows = []
        output_paths = stage_outputs(data, staged, records, attempt_root, attempt_id)
        result = build_result(data, staged, attempt_id, "PASS", "NONE", 1)
        # Result/report are staged before promotion as part of the same prepared attempt.
        write_json(attempt_root / "result.json", result)
        write_text(attempt_root / "report.md", report_text(result, staged, attempt_id))
        promote(data, staged, output_paths, result, attempt_root)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except Exception as exc:
        print(f"STATUS=BLOCKED")
        print(f"STAGE={STAGE}")
        print(f"BLOCKER={type(exc).__name__}:{exc}")
        print(f"ATTEMPT_ID={attempt_id}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
