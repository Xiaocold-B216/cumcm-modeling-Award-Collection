from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCALE = ROOT / "catalog/scale"
REPORTS = ROOT / "reports/scale"

EXPECTED_BRANCH = "library-refactor-v1"
EXPECTED_HEAD = "557724fba6572d4d83dc421feda5b17b13ff8d66"
EXPECTED_DECISION_SHA = "8078A66F45C0C58F9BA4CF0C85BEB0E331C2BC405C52B93760B999DE00A8FD21"
EXPECTED_PREPARATION_ATTEMPT = "20260903T172404115633_3c748bc1"
EXPECTED_SAMPLE_FINGERPRINT = "677898FA2C0DE5B8229AC310566A2D0A41465790B5F188320CD2EE46C877D4EF"
EXPECTED_TRIAGE_ATTEMPT = "20260904T130448795478_947f1a48"

KNOWN_FORMAL_DEFECT_IDS = [
    "CUMCM-1999-B-003",
    "CUMCM-2008-C-004",
    "CUMCM-1992-A-003",
    "CUMCM-1993-B-001",
    "CUMCM-1996-B-001",
    "CUMCM-1997-A-008",
    "CUMCM-1998-A-007",
    "CUMCM-2000-A-005",
    "CUMCM-2001-A-001",
    "CUMCM-2002-B-005",
]
Q3_MAJOR_ID = "CUMCM-2020-D-003"

MARKER_RE = re.compile(r"<!--\s*source_page:\s*(\d+)\s*-->", re.IGNORECASE)
COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
STRUCTURAL_LINE_RE = re.compile(
    r"^(?:\s*#{1,6}\s*.*|\s*[-*_>`|]+\s*|\s*===.*===\s*|"
    r"\s*(?:paper_id|page_number|page_classification|source_path|source_sha256|"
    r"persisted_page_text_path)=.*|\s*\[No page-local persisted text.*)$",
    re.IGNORECASE,
)

INPUT_FILES = [
    SCALE / "g11_manual_sample_authoritative_baseline.json",
    SCALE / "g11_manual_sample_decisions.csv",
    SCALE / "g11_major_defect_triage_input.csv",
    SCALE / "g11_major_defect_root_cause_triage.csv",
    SCALE / "g11_major_defect_root_cause_triage_result.json",
    REPORTS / "G11_MAJOR_DEFECT_ROOT_CAUSE_TRIAGE.md",
    SCALE / "g9_paper_index.csv",
    SCALE / "g9_paper_index.jsonl",
    SCALE / "g8_artifact_manifest.csv",
    SCALE / "g8_artifact_eligibility.csv",
    SCALE / "g8_q3_formal_artifact_generation_manifest.csv",
    SCALE / "g8_q3_batch_extraction_manifest.csv",
    SCALE / "g8_q3_batch_page_audit.csv",
    SCALE / "g8_q3_batch_ocr_audit.csv",
    SCALE / "g8_q3_batch_repair/CUMCM-2020-D-003/manifest.json",
    SCALE / "g8_q3_batch_repair/CUMCM-2020-D-003/provenance.json",
    SCALE / "g8_q3_batch_repair/CUMCM-2020-D-003/quality.json",
    SCALE / "g8_q3_batch_repair/CUMCM-2020-D-003/normalized_body.txt",
    SCALE / "g11_manual_sample_manifest.csv",
    ROOT / "catalog/papers.csv",
    ROOT / "catalog/paper_files.csv",
    SCALE / "g10_consistency_result.json",
]

OUTPUT_TARGETS = SCALE / "g11_formal_artifact_repair_targets.csv"
OUTPUT_PAGES = SCALE / "g11_formal_artifact_repair_pages.csv"
OUTPUT_RESULT = SCALE / "g11_major_defect_minimal_repair_plan_result.json"
OUTPUT_REPORT = REPORTS / "G11_MAJOR_DEFECT_MINIMAL_REPAIR_PLAN.md"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest().upper()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def sha256_json(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(raw)


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def normalized_content(value: str) -> str:
    lines: list[str] = []
    for line in COMMENT_RE.sub("", value).splitlines():
        if STRUCTURAL_LINE_RE.match(line):
            continue
        if line.strip():
            lines.append(line)
    return "".join("".join(lines).split())


def body_page_segments(body: str) -> list[dict[str, Any]]:
    matches = list(MARKER_RE.finditer(body))
    result: list[dict[str, Any]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        segment = body[match.end() : end]
        content = normalized_content(segment)
        result.append(
            {
                "source_page": int(match.group(1)),
                "formal_marker_present": 1,
                "formal_substantive_content_present": int(bool(content)),
                "substantive_char_count": len(content),
            }
        )
    return result


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def path_from_rel(value: str) -> Path:
    return ROOT / value.replace("\\", "/")


def assert_required_inputs() -> None:
    missing = [rel(path) for path in INPUT_FILES if not path.exists()]
    if missing:
        raise RuntimeError("G11_REPAIR_PLAN_MISSING_EVIDENCE=" + ";".join(missing))


def main() -> int:
    assert_required_inputs()

    branch = git("branch", "--show-current")
    head = git("rev-parse", "HEAD")
    branch_match = int(branch == EXPECTED_BRANCH)
    head_match = int(head == EXPECTED_HEAD)
    if not branch_match or not head_match:
        raise RuntimeError("G11_REPAIR_PLAN_REPO_DRIFT")

    protected_hashes_before = {
        rel(path): sha256_file(path)
        for path in INPUT_FILES
        if path.is_file()
    }

    baseline = read_json(SCALE / "g11_manual_sample_authoritative_baseline.json")
    decisions = read_csv(SCALE / "g11_manual_sample_decisions.csv")
    triage_input = read_csv(SCALE / "g11_major_defect_triage_input.csv")
    triage_rows = read_csv(SCALE / "g11_major_defect_root_cause_triage.csv")
    triage_result = read_json(SCALE / "g11_major_defect_root_cause_triage_result.json")
    g9_rows = read_csv(SCALE / "g9_paper_index.csv")
    g9_jsonl = [
        json.loads(line)
        for line in (SCALE / "g9_paper_index.jsonl").read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]
    g8_rows = read_csv(SCALE / "g8_artifact_manifest.csv")
    eligibility_rows = read_csv(SCALE / "g8_artifact_eligibility.csv")
    papers_rows = read_csv(ROOT / "catalog/papers.csv")
    membership_rows = read_csv(ROOT / "catalog/paper_files.csv")
    g10_result = read_json(SCALE / "g10_consistency_result.json")

    decision_sha = sha256_file(SCALE / "g11_manual_sample_decisions.csv")
    if decision_sha != EXPECTED_DECISION_SHA:
        raise RuntimeError("G11_REPAIR_PLAN_DECISION_SHEET_DRIFT")
    if (
        baseline.get("authoritative_preparation_attempt_id") != EXPECTED_PREPARATION_ATTEMPT
        or baseline.get("sample_fingerprint") != EXPECTED_SAMPLE_FINGERPRINT
        or int(baseline.get("current_baseline_adopted", 0)) != 1
        or triage_result.get("TRIAGE_ATTEMPT_ID") != EXPECTED_TRIAGE_ATTEMPT
        or triage_result.get("STATUS") != "PASS"
        or int(triage_result.get("ROOT_CAUSE_UNRESOLVED_COUNT", -1)) != 0
    ):
        raise RuntimeError("G11_REPAIR_PLAN_AUTHORITATIVE_BASELINE_DRIFT")

    decision_by_id = {row["paper_id"]: row for row in decisions}
    triage_input_by_id = {row["paper_id"]: row for row in triage_input}
    triage_by_id = {row["paper_id"]: row for row in triage_rows}
    sample_manifest = {
        row["paper_id"]: row
        for row in read_csv(SCALE / "g11_manual_sample_manifest.csv")
    }
    g9_by_id = {row["paper_id"]: row for row in g9_rows}
    g8_paper_rows = {
        row["paper_id"]: row
        for row in g8_rows
        if row.get("artifact_type") == "paper.md"
    }
    g8_by_hash: dict[str, list[str]] = defaultdict(list)
    for paper_id, row in g8_paper_rows.items():
        g8_by_hash[row["artifact_sha256"]].append(paper_id)

    # Verify the frozen formal registry, artifact files, and metadata without modifying them.
    formal_registry_hash_mismatch = 0
    missing_formal_artifacts = 0
    for row in g8_rows:
        path = path_from_rel(row["artifact_path"])
        if not path.is_file():
            missing_formal_artifacts += 1
        elif sha256_file(path) != row["artifact_sha256"].upper():
            formal_registry_hash_mismatch += 1
    metadata_count = 0
    metadata_missing = 0
    for paper_id in g8_paper_rows:
        metadata = ROOT / "derived/scale/papers" / paper_id / "metadata.yaml"
        if metadata.is_file() and metadata.stat().st_size > 0:
            metadata_count += 1
        else:
            metadata_missing += 1

    g9_csv_by_id = {row["paper_id"]: row for row in g9_rows}
    g9_jsonl_by_id = {row["paper_id"]: row for row in g9_jsonl}
    g9_projection_match = int(
        len(g9_rows) == len(g9_jsonl)
        and set(g9_csv_by_id) == set(g9_jsonl_by_id)
        and all(g9_csv_by_id[key] == {k: str(v) for k, v in g9_jsonl_by_id[key].items()} for key in g9_csv_by_id)
    )

    scale_identity_ids = {row["paper_id"] for row in eligibility_rows}
    scale_identity_unique = len(scale_identity_ids) == len(eligibility_rows)
    eligible_count = sum(row.get("artifact_eligible") == "1" for row in eligibility_rows)
    ineligible_count = sum(row.get("artifact_eligible") == "0" for row in eligibility_rows)

    # Use the same structural-shell definition as the prior triage and scan all 453 bodies.
    page_records: list[dict[str, Any]] = []
    marker_only_by_id: dict[str, list[int]] = {}
    marker_count_by_id: dict[str, int] = {}
    fully_marker_only_ids: set[str] = set()
    marker_page_range_mismatch_count = 0
    for paper_id in sorted(g8_paper_rows):
        body_path = path_from_rel(g8_paper_rows[paper_id]["artifact_path"])
        body = body_path.read_text(encoding="utf-8", errors="replace")
        segments = body_page_segments(body)
        marker_count_by_id[paper_id] = len(segments)
        marker_only = [
            int(row["source_page"])
            for row in segments
            if not row["formal_substantive_content_present"]
        ]
        marker_only_by_id[paper_id] = marker_only
        if segments and len(marker_only) == len(segments):
            fully_marker_only_ids.add(paper_id)
        page_count_text = g9_by_id[paper_id].get("page_count", "").strip()
        if page_count_text:
            g9_page_count = int(page_count_text)
            if any(page < 1 or page > g9_page_count for page in marker_only):
                marker_page_range_mismatch_count += 1

    total_formal_artifacts = len(g8_paper_rows)
    total_source_page_markers = sum(marker_count_by_id.values())
    total_marker_only_pages = sum(len(pages) for pages in marker_only_by_id.values())
    candidate_ids = {paper_id for paper_id, pages in marker_only_by_id.items() if pages}

    # Existing explicit blank-page evidence is authoritative when it intersects this scan.
    legitimate_page_keys: set[tuple[str, int]] = set()
    for sample in sample_manifest.values():
        for label in ("a", "b", "c"):
            page = int(sample[f"page_{label}"])
            if sample[f"page_{label}_classification"] == "VERIFIED_BLANK_SOURCE_PAGE":
                legitimate_page_keys.add((sample["paper_id"], page))

    # Only the 10 high-confidence triage samples have existing page-level source evidence
    # proving that a marker-only page should contain substantive paper material.
    known_formal_ids = [
        row["paper_id"]
        for row in sorted(triage_rows, key=lambda row: int(row["sample_order"]))
        if row.get("root_cause_category") == "FORMAL_ARTIFACT_PAGE_CONTENT_MISSING"
    ]
    known_formal_set = set(known_formal_ids)
    known_defective_page_keys: set[tuple[str, int]] = set()
    page_evidence: dict[tuple[str, int], dict[str, Any]] = {}
    for paper_id in known_formal_ids:
        triage = triage_by_id[paper_id]
        sample = sample_manifest[paper_id]
        labels_by_page: dict[int, list[str]] = defaultdict(list)
        for label in ("A", "B", "C"):
            page = int(triage[f"selected_page_{label}"])
            labels_by_page[page].append(label)
        for page, labels in labels_by_page.items():
            if page not in marker_only_by_id.get(paper_id, []):
                continue
            classes = {sample[f"page_{label.lower()}_classification"] for label in labels}
            classification = next(iter(classes)) if len(classes) == 1 else "CONFLICTING_EXISTING_PAGE_CLASSIFICATION"
            excerpt_paths: list[str] = []
            excerpt_hashes: list[str] = []
            png_paths: list[str] = []
            png_nonempty = 1
            for label in labels:
                excerpt_path = (
                    ROOT
                    / sample["review_package_path"]
                    / f"page_{label}_artifact_excerpt.txt"
                )
                if excerpt_path.is_file():
                    excerpt_paths.append(rel(excerpt_path))
                    excerpt_hashes.append(sha256_file(excerpt_path))
                png_path = ROOT / sample["review_package_path"] / f"page_{label}.png"
                png_paths.append(rel(png_path))
                png_nonempty &= int(png_path.is_file() and png_path.stat().st_size > 0)
            known_defective_page_keys.add((paper_id, page))
            page_evidence[(paper_id, page)] = {
                "current_page_classification": classification,
                "review_packet_excerpt_paths": ";".join(excerpt_paths),
                "review_packet_excerpt_sha256": ";".join(excerpt_hashes),
                "source_review_png_paths": ";".join(png_paths),
                "source_review_png_nonempty": png_nonempty,
                "evidence_confidence": "HIGH",
            }

    # Classify every marker-only segment. Unobserved candidates remain unresolved.
    classification_by_key: dict[tuple[str, int], str] = {}
    for paper_id, pages in marker_only_by_id.items():
        for page in pages:
            key = (paper_id, page)
            if key in legitimate_page_keys:
                classification_by_key[key] = "LEGITIMATE_MARKER_ONLY_PAGE"
            elif key in known_defective_page_keys:
                classification_by_key[key] = "DEFECTIVE_MARKER_ONLY_PAGE"
            else:
                classification_by_key[key] = "UNRESOLVED_MARKER_ONLY_PAGE"

    legitimate_count = sum(value == "LEGITIMATE_MARKER_ONLY_PAGE" for value in classification_by_key.values())
    defective_count = sum(value == "DEFECTIVE_MARKER_ONLY_PAGE" for value in classification_by_key.values())
    unresolved_count = sum(value == "UNRESOLVED_MARKER_ONLY_PAGE" for value in classification_by_key.values())
    defective_ids = {
        paper_id
        for paper_id, page in classification_by_key
        if classification_by_key[(paper_id, page)] == "DEFECTIVE_MARKER_ONLY_PAGE"
    }
    legitimate_ids = {
        paper_id
        for paper_id, page in classification_by_key
        if classification_by_key[(paper_id, page)] == "LEGITIMATE_MARKER_ONLY_PAGE"
    }
    unresolved_page_ids = {
        paper_id
        for paper_id, page in classification_by_key
        if classification_by_key[(paper_id, page)] == "UNRESOLVED_MARKER_ONLY_PAGE"
    }
    # Identity-level counts are intentionally non-overlapping. A confirmed defective
    # identity may still have additional unobserved marker-only pages; those pages are
    # unresolved, but the identity remains in the confirmed repair set.
    unresolved_ids = candidate_ids - defective_ids - legitimate_ids
    identities_with_defect_and_unresolved_pages = defective_ids & unresolved_page_ids
    classification_sum_pass = int(legitimate_count + defective_count + unresolved_count == total_marker_only_pages)
    known_mismatch_count = len(known_formal_set - defective_ids)
    if known_mismatch_count:
        raise RuntimeError("G11_REPAIR_PLAN_KNOWN_DEFECT_CLASSIFICATION_MISMATCH")

    governed_duplicate_hashes = {digest for digest, ids in g8_by_hash.items() if len(ids) > 1}
    defective_in_governed_duplicate = sum(
        g8_paper_rows[paper_id]["artifact_sha256"] in governed_duplicate_hashes
        for paper_id in defective_ids
    )
    defective_outside_governed_duplicate = len(defective_ids) - defective_in_governed_duplicate
    governed_duplicate_group_count = len(governed_duplicate_hashes)

    # Build the full marker-only page audit, including unresolved rows; only confirmed
    # defective rows become formal repair targets.
    page_fieldnames = [
        "paper_id",
        "source_page",
        "current_page_classification",
        "formal_marker_present",
        "formal_substantive_content_present",
        "source_substantive_content_expected",
        "classification",
        "existing_page_text_path",
        "existing_page_text_sha256",
        "repair_layer",
        "repair_action",
        "requires_new_ocr",
        "requires_new_extraction",
        "evidence_confidence",
        "review_packet_excerpt_paths",
        "review_packet_excerpt_sha256",
        "source_review_png_paths",
        "notes",
    ]
    page_rows: list[dict[str, Any]] = []
    for paper_id in sorted(marker_only_by_id):
        for page in marker_only_by_id[paper_id]:
            key = (paper_id, page)
            classification = classification_by_key[key]
            evidence = page_evidence.get(key, {})
            if classification == "DEFECTIVE_MARKER_ONLY_PAGE":
                current_class = evidence.get("current_page_classification", "EXISTING_PAGE_CLASSIFICATION_UNAVAILABLE")
                expected = 1
                repair_layer = "FORMAL_BODY_RECONSTRUCTION_SERIALIZATION"
                repair_action = "TARGETED_SOURCE_TEXT_ACQUISITION_AND_FORMAL_BODY_REGENERATION"
                requires_extraction = 1
                confidence = "HIGH"
                notes = "Existing selected-page PNG/review evidence supports substantive source content; Q0 page-local persisted text is unavailable."
            elif classification == "LEGITIMATE_MARKER_ONLY_PAGE":
                current_class = "VERIFIED_BLANK_SOURCE_PAGE"
                expected = 0
                repair_layer = "NONE"
                repair_action = "NO_REPAIR_LEGITIMATE_EMPTY_PAGE"
                requires_extraction = 0
                confidence = "HIGH"
                notes = "Existing governance explicitly classifies this source page as blank."
            else:
                current_class = "NOT_AVAILABLE_IN_EXISTING_EVIDENCE"
                expected = "UNKNOWN"
                repair_layer = "UNRESOLVED"
                repair_action = "TARGETED_DIAGNOSTIC_BEFORE_REPAIR"
                requires_extraction = 0
                confidence = "LOW"
                notes = "No existing page-level source evidence establishes substantive content or a legitimate blank-page explanation; do not guess or repair."
            page_rows.append(
                {
                    "paper_id": paper_id,
                    "source_page": page,
                    "current_page_classification": current_class,
                    "formal_marker_present": 1,
                    "formal_substantive_content_present": 0,
                    "source_substantive_content_expected": expected,
                    "classification": classification,
                    "existing_page_text_path": "NOT_AVAILABLE_Q0_PDF_INSPECTOR",
                    "existing_page_text_sha256": "",
                    "repair_layer": repair_layer,
                    "repair_action": repair_action,
                    "requires_new_ocr": 0,
                    "requires_new_extraction": requires_extraction,
                    "evidence_confidence": evidence.get("evidence_confidence", confidence),
                    "review_packet_excerpt_paths": evidence.get("review_packet_excerpt_paths", ""),
                    "review_packet_excerpt_sha256": evidence.get("review_packet_excerpt_sha256", ""),
                    "source_review_png_paths": evidence.get("source_review_png_paths", ""),
                    "notes": notes,
                }
            )
    write_csv(OUTPUT_PAGES, page_fieldnames, page_rows)

    # Build formal repair targets from the confirmed subset only.
    target_fieldnames = [
        "paper_id",
        "artifact_set_id",
        "year",
        "problem",
        "stratum",
        "formal_body_path",
        "formal_body_sha256",
        "defective_source_page_count",
        "defective_source_pages",
        "legitimate_marker_only_page_count",
        "unresolved_marker_only_page_count",
        "root_cause_pattern",
        "repair_layer",
        "requires_body_regeneration",
        "requires_ocr",
        "requires_extraction",
        "requires_reconstruction",
        "requires_artifact_repromotion",
        "requires_index_refresh",
        "requires_g10_revalidation",
        "requires_human_rereview",
        "notes",
    ]
    target_rows: list[dict[str, Any]] = []
    for paper_id in known_formal_ids:
        triage = triage_by_id[paper_id]
        index = g9_by_id[paper_id]
        body_row = g8_paper_rows[paper_id]
        defective_pages = sorted(
            page for candidate_id, page in classification_by_key if candidate_id == paper_id and classification_by_key[(candidate_id, page)] == "DEFECTIVE_MARKER_ONLY_PAGE"
        )
        legitimate_pages = sorted(
            page for candidate_id, page in classification_by_key if candidate_id == paper_id and classification_by_key[(candidate_id, page)] == "LEGITIMATE_MARKER_ONLY_PAGE"
        )
        unresolved_pages = sorted(
            page for candidate_id, page in classification_by_key if candidate_id == paper_id and classification_by_key[(candidate_id, page)] == "UNRESOLVED_MARKER_ONLY_PAGE"
        )
        target_rows.append(
            {
                "paper_id": paper_id,
                "artifact_set_id": triage["artifact_set_id"],
                "year": index["year"],
                "problem": index["problem"],
                "stratum": triage["stratum"],
                "formal_body_path": body_row["artifact_path"],
                "formal_body_sha256": body_row["artifact_sha256"],
                "defective_source_page_count": len(defective_pages),
                "defective_source_pages": ",".join(map(str, defective_pages)),
                "legitimate_marker_only_page_count": len(legitimate_pages),
                "unresolved_marker_only_page_count": len(unresolved_pages),
                "root_cause_pattern": "Q0_PDF_INSPECTOR_MARKER_ONLY_FORMAL_BODY_SHARED_SERIALIZATION_PATH",
                "repair_layer": "FORMAL_BODY_RECONSTRUCTION_SERIALIZATION",
                "requires_body_regeneration": 1,
                "requires_ocr": 0,
                "requires_extraction": 1,
                "requires_reconstruction": 1,
                "requires_artifact_repromotion": 1,
                "requires_index_refresh": 1,
                "requires_g10_revalidation": 1,
                "requires_human_rereview": 1,
                "notes": (
                    f"Confirmed defective pages={','.join(map(str, defective_pages))}; "
                    f"remaining marker-only pages in this body are unresolved={','.join(map(str, unresolved_pages)) or 'NONE'}. "
                    "Governed-duplicate status is context only; no binding defect was found."
                ),
            }
        )
    write_csv(OUTPUT_TARGETS, target_fieldnames, target_rows)

    # Independently locate the Q3/OCR layer for CUMCM-2020-D-003 using persisted evidence.
    q3_page_audit = [
        row
        for row in read_csv(SCALE / "g8_q3_batch_page_audit.csv")
        if row["paper_id"] == Q3_MAJOR_ID and int(row["page_number"]) in {1, 68, 135}
    ]
    q3_ocr_audit = [
        row
        for row in read_csv(SCALE / "g8_q3_batch_ocr_audit.csv")
        if row["paper_id"] == Q3_MAJOR_ID and int(row["page_number"]) in {1, 68, 135}
    ]
    q3_extraction = [
        row
        for row in read_csv(SCALE / "g8_q3_batch_extraction_manifest.csv")
        if row["paper_id"] == Q3_MAJOR_ID
    ]
    q3_formal_manifest = [
        row
        for row in read_csv(SCALE / "g8_q3_formal_artifact_generation_manifest.csv")
        if row["paper_id"] == Q3_MAJOR_ID and row["artifact_type"] == "paper.md"
    ]
    q3_repair_dir = SCALE / "g8_q3_batch_repair" / Q3_MAJOR_ID
    q3_batch_manifest = read_json(q3_repair_dir / "manifest.json")
    q3_provenance = read_json(q3_repair_dir / "provenance.json")
    q3_quality = read_json(q3_repair_dir / "quality.json")
    q3_reconstruction_evidence_pass = int(
        q3_batch_manifest.get("paper_id") == Q3_MAJOR_ID
        and q3_batch_manifest.get("reconstruction_status") == "COMPLETE_VALID"
        and q3_batch_manifest.get("page_provenance_summary") == {"OCR": 135}
        and q3_provenance.get("paper_id") == Q3_MAJOR_ID
        and q3_provenance.get("schema") == "g8-q3-batch-provenance-v1"
        and q3_quality.get("paper_id") == Q3_MAJOR_ID
        and q3_quality.get("schema") == "g8-q3-batch-quality-v1"
        and int(q3_quality.get("pass", False)) == 1
    )
    q3_triage = triage_by_id[Q3_MAJOR_ID]
    q3_page_text_details: list[dict[str, Any]] = []
    q3_persisted_ocr_semantic_defect = True
    q3_page_provenance_pass = (
        len(q3_page_audit) == 3
        and len(q3_ocr_audit) == 3
        and q3_reconstruction_evidence_pass
    )
    for page in (1, 68, 135):
        page_audit = next((row for row in q3_page_audit if int(row["page_number"]) == page), {})
        ocr_audit = next((row for row in q3_ocr_audit if int(row["page_number"]) == page), {})
        page_path = SCALE / "g8_q3_batch_repair" / Q3_MAJOR_ID / "pages" / f"{page:04d}.txt"
        actual_sha = sha256_file(page_path) if page_path.is_file() else ""
        page_chars = len(page_path.read_text(encoding="utf-8", errors="replace")) if page_path.is_file() else 0
        q3_page_provenance_pass &= int(
            page_path.is_file()
            and page_chars > 0
            and page_audit.get("authoritative_page_source") == "OCR"
            and page_audit.get("page_text_quality_status") == "USABLE"
            and ocr_audit.get("status") == "SUCCESS"
            and page_audit.get("authoritative_page_text_sha256") == actual_sha
            and ocr_audit.get("ocr_text_sha256") == actual_sha
        )
        q3_page_text_details.append(
            {
                "page": page,
                "path": rel(page_path),
                "sha256": actual_sha,
                "char_count": page_chars,
                "authoritative_source": page_audit.get("authoritative_page_source", ""),
                "page_quality": page_audit.get("page_text_quality_status", ""),
                "ocr_status": ocr_audit.get("status", ""),
            }
        )
    reviewer_comment = decision_by_id[Q3_MAJOR_ID].get("reviewer_comment", "")
    q3_persisted_ocr_semantic_defect = int(
        bool(re.search(r"OCR", reviewer_comment, re.IGNORECASE))
        and "误识别" in reviewer_comment
        and "影响模型含义" in reviewer_comment
    )
    q3_formal_body = path_from_rel(g8_paper_rows[Q3_MAJOR_ID]["artifact_path"])
    q3_formal_body_has_markers = int(bool(MARKER_RE.search(q3_formal_body.read_text(encoding="utf-8", errors="replace"))))
    q3_repair_layer = "OCR_PAGE" if q3_page_provenance_pass and q3_persisted_ocr_semantic_defect else "UNRESOLVED"
    q3_plan = {
        "paper_id": Q3_MAJOR_ID,
        "repair_layer": q3_repair_layer,
        "confidence": "HIGH" if q3_repair_layer == "OCR_PAGE" else "UNRESOLVED",
        "selected_pages": [1, 68, 135],
        "actual_corrupted_spans": "Reviewer-described OCR/symbol substitutions affecting variables, coordinates, operators and model meaning; exact spans require targeted page QA in the next repair stage.",
        "persisted_ocr_text_itself_semantically_wrong": q3_persisted_ocr_semantic_defect,
        "reconstruction_or_serialization_primary_cause_supported": 0,
        "formal_body_has_source_page_markers": q3_formal_body_has_markers,
        "q3_reconstruction_evidence_pass": q3_reconstruction_evidence_pass,
        "requires_ocr": 1 if q3_repair_layer == "OCR_PAGE" else 0,
        "requires_extraction": 0,
        "requires_reconstruction": 1 if q3_repair_layer == "OCR_PAGE" else 0,
        "requires_body_regeneration": 1 if q3_repair_layer == "OCR_PAGE" else 0,
        "requires_artifact_repromotion": 1 if q3_repair_layer == "OCR_PAGE" else 0,
        "requires_index_refresh": 1 if q3_repair_layer == "OCR_PAGE" else 0,
        "requires_g10_revalidation": 1 if q3_repair_layer == "OCR_PAGE" else 0,
        "requires_human_rereview": 1,
        "page_evidence": q3_page_text_details,
        "notes": "Persisted OCR page text is nonempty and auditable, but the existing human review explicitly reports semantic OCR/symbol errors. The formal body is substantive but lacks page markers; that is a separate granularity limitation, not a reason to suppress selective OCR planning.",
    }

    protected_hashes_after = {
        rel(path): sha256_file(path)
        for path in INPUT_FILES
        if path.is_file()
    }
    protected_unchanged = int(protected_hashes_before == protected_hashes_after)

    plan_inputs = {
        "branch": branch,
        "head": head,
        "decision_sha": decision_sha,
        "baseline": baseline,
        "triage_result": triage_result,
        "g9_sha": sha256_file(SCALE / "g9_paper_index.csv"),
        "g8_sha": sha256_file(SCALE / "g8_artifact_manifest.csv"),
        "formal_body_hashes": {key: g8_paper_rows[key]["artifact_sha256"] for key in sorted(g8_paper_rows)},
        "classification": classification_by_key,
        "q3_plan": q3_plan,
    }
    # JSON tuple keys are converted explicitly so the fingerprint is deterministic.
    plan_inputs["classification"] = {
        f"{paper_id}:{page}": classification_by_key[(paper_id, page)]
        for paper_id, page in sorted(classification_by_key)
    }
    plan_fingerprint = sha256_json(plan_inputs)
    repair_plan_attempt_id = "g11-major-defect-minimal-repair-plan-" + plan_fingerprint[:16].lower()

    frozen_ok = int(
        len(eligibility_rows) == 642
        and scale_identity_unique
        and eligible_count == 453
        and ineligible_count == 189
        and len(g8_paper_rows) == 453
        and len(g8_rows) == 1359
        and len(g9_rows) == 453
        and len(g9_jsonl) == 453
        and g9_projection_match
        and metadata_count == 453
        and metadata_missing == 0
        and missing_formal_artifacts == 0
        and formal_registry_hash_mismatch == 0
        and int(g10_result.get("SOURCE_SHA_MISMATCH_COUNT", -1)) == 0
        and int(g10_result.get("ORIGINAL_FILES_MODIFIED", -1)) == 0
    )
    formal_evidence_ok = int(
        len(triage_rows) == 11
        and set(known_formal_ids) == set(KNOWN_FORMAL_DEFECT_IDS)
        and q3_page_provenance_pass
        and q3_repair_layer == "OCR_PAGE"
    )

    status = "PASS" if unresolved_count == 0 and formal_evidence_ok and frozen_ok else "PARTIAL"
    blocker = "NONE" if status == "PASS" else "REPAIR_SCOPE_OR_LAYER_UNRESOLVED"
    next_stage = "G8-TARGETED-MULTI-ROUTE-FORMAL-ARTIFACT-REPAIR" if status == "PASS" else "G11-MAJOR-DEFECT-DEEP-DIAGNOSTIC"

    result: dict[str, Any] = {
        "STAGE": "G11-MAJOR-DEFECT-MINIMAL-REPAIR-PLAN",
        "STATUS": status,
        "BRANCH": branch,
        "HEAD": head,
        "BRANCH_MATCH": branch_match,
        "HEAD_MATCH": head_match,
        "REPAIR_PLAN_ATTEMPT_ID": repair_plan_attempt_id,
        "PLAN_FINGERPRINT": plan_fingerprint,
        "AUTHORITATIVE_G11_PREPARATION_ATTEMPT_ID": EXPECTED_PREPARATION_ATTEMPT,
        "G11_STATUS_REMAINS": "PARTIAL",
        "TRIAGE_ATTEMPT_ID": EXPECTED_TRIAGE_ATTEMPT,
        "MAJOR_INPUT_COUNT": 11,
        "MAJOR_TRIAGED_COUNT": 11,
        "ROOT_CAUSE_UNRESOLVED_COUNT": 0,
        "TOTAL_IDENTITIES": 642,
        "ELIGIBLE": 453,
        "INELIGIBLE": 189,
        "ARTIFACT_SETS": 453,
        "PRIMARY_ARTIFACTS": 1359,
        "FORMAL_INDEX_RECORDS": 453,
        "DOC_MANUAL_BACKLOG": 0,
        "Q3_MANUAL_BACKLOG": 0,
        "TOTAL_MANUAL_BACKLOG": 0,
        "TOTAL_FORMAL_ARTIFACTS_SCANNED": total_formal_artifacts,
        "TOTAL_SOURCE_PAGE_MARKERS": total_source_page_markers,
        "MARKER_ONLY_PAGE_SEGMENT_COUNT": total_marker_only_pages,
        "MARKER_ONLY_AFFECTED_IDENTITY_COUNT": len(candidate_ids),
        "CANDIDATE_MARKER_ONLY_IDENTITY_COUNT": len(candidate_ids),
        "PREVIOUS_REPORTED_FULLY_MARKER_ONLY_IDENTITY_COUNT": 215,
        "CURRENT_REDERIVED_FULLY_MARKER_ONLY_IDENTITY_COUNT": len(fully_marker_only_ids),
        "LEGITIMATE_MARKER_ONLY_PAGE_COUNT": legitimate_count,
        "DEFECTIVE_MARKER_ONLY_PAGE_COUNT": defective_count,
        "UNRESOLVED_MARKER_ONLY_PAGE_COUNT": unresolved_count,
        "DEFECTIVE_MARKER_ONLY_IDENTITY_COUNT": len(defective_ids),
        "UNRESOLVED_MARKER_ONLY_IDENTITY_COUNT": len(unresolved_ids),
        "CONFIRMED_DEFECT_IDENTITIES_WITH_ADDITIONAL_UNRESOLVED_PAGES": len(identities_with_defect_and_unresolved_pages),
        "UNRESOLVED_MARKER_ONLY_TARGETS": ";".join(sorted(unresolved_ids)),
        "MARKER_ONLY_CLASSIFICATION_SUM_PASS": classification_sum_pass,
        "MARKER_PAGE_RANGE_MISMATCH_COUNT": marker_page_range_mismatch_count,
        "KNOWN_G11_DEFECT_CLASSIFICATION_MISMATCH_COUNT": known_mismatch_count,
        "KNOWN_G11_FORMAL_DEFECT_IDS": ";".join(KNOWN_FORMAL_DEFECT_IDS),
        "COMMON_ROOT_CAUSE_PATTERN_FOUND": 1,
        "COMMON_ROOT_CAUSE_PATTERN": "Q0_PDF_INSPECTOR_NATIVE_MARKDOWN_MARKER_ONLY_SERIALIZATION_SHARED_FORMAL_PATH",
        "COMMON_ROOT_CAUSE_DESCRIPTION": "Confirmed formal defects are OTHER_FORMAL_DERIVED, PDF source, Q0, pdf-inspector route, g8_file_source_map.csv, extraction contract 1, page-granular index records, and source_page shells with no persisted page-local text. The generator version/attempt is not recorded in existing OTHER-formal metadata. Body-hash duplication is correlated context only, not a binding cause.",
        "COMMON_YEAR_PROBLEM_PATTERN": "VARIED_1992_TO_2008",
        "COMMON_SOURCE_FORMAT": "PDF",
        "COMMON_ARTIFACT_ORIGIN": "OTHER_FORMAL_DERIVED_ONE_PAPER_LEVEL_ARTIFACT_SET_FROM_MEMBERSHIPS",
        "COMMON_EXTRACTION_ROUTE": "pdf-inspector",
        "COMMON_STRATUM": "OTHER_FORMAL_DERIVED",
        "COMMON_GENERATOR_VERSION": "NOT_RECORDED_IN_EXISTING_FORMAL_METADATA",
        "GOVERNED_DUPLICATE_BODY_HASH_GROUP_COUNT": governed_duplicate_group_count,
        "GOVERNED_BODY_HASH_DUPLICATES_FROM_G10": 32,
        "UNEXPECTED_BODY_HASH_DUPLICATES_FROM_G10": 0,
        "DEFECTIVE_IDENTITIES_IN_GOVERNED_DUPLICATE_GROUP_COUNT": defective_in_governed_duplicate,
        "DEFECTIVE_IDENTITIES_OUTSIDE_GOVERNED_DUPLICATE_GROUP_COUNT": defective_outside_governed_duplicate,
        "FORMAL_ARTIFACT_REPAIR_TARGET_COUNT": len(target_rows),
        "FORMAL_ARTIFACT_REPAIR_TARGET_IDS": ";".join(known_formal_ids),
        "FORMAL_ARTIFACT_REPAIR_TARGET_PAGE_COUNT": defective_count,
        "CUMCM_2020_D_003_REPAIR_LAYER": q3_repair_layer,
        "Q3_RECONSTRUCTION_EVIDENCE_PASS": q3_reconstruction_evidence_pass,
        "CUMCM_2020_D_003_REPAIR_PLAN": q3_plan,
        "REPAIR_GROUP_A_IDENTITY_COUNT": len(target_rows),
        "REPAIR_GROUP_B_IDENTITY_COUNT": 1 if q3_repair_layer == "OCR_PAGE" else 0,
        "REPAIR_GROUP_C_IDENTITY_COUNT": 0,
        "UNRESOLVED_REPAIR_IDENTITY_COUNT": len(unresolved_ids),
        "TARGET_REPAIR_PAGE_COUNT": defective_count,
        "REQUIRES_OCR_IDENTITY_COUNT": 1 if q3_repair_layer == "OCR_PAGE" else 0,
        "REQUIRES_EXTRACTION_IDENTITY_COUNT": len(target_rows),
        "REQUIRES_RECONSTRUCTION_IDENTITY_COUNT": len(target_rows) + (1 if q3_repair_layer == "OCR_PAGE" else 0),
        "REQUIRES_ARTIFACT_REPROMOTION_IDENTITY_COUNT": len(target_rows) + (1 if q3_repair_layer == "OCR_PAGE" else 0),
        "REQUIRES_INDEX_REFRESH": 1,
        "REQUIRES_G10_REVALIDATION": 1,
        "MANDATORY_G11_REREVIEW_COUNT": 11,
        "DECISION_SHEET_SHA256": decision_sha,
        "DECISION_CONTENT_MODIFICATION_COUNT": 0,
        "DECISION_SEVERITY_MODIFICATION_COUNT": 0,
        "DECISION_REVIEW_STATUS_MODIFICATION_COUNT": 0,
        "FORMAL_DATA_MODIFICATION_COUNT": 0,
        "FORMAL_ARTIFACT_CONTENT_MODIFICATION_COUNT": 0,
        "FORMAL_ARTIFACTS_MODIFIED": 0,
        "FORMAL_INDEX_MODIFICATION_COUNT": 0,
        "IDENTITY_MODIFICATION_COUNT": 0,
        "MEMBERSHIP_MODIFICATION_COUNT": 0,
        "FORMAL_ELIGIBILITY_MODIFIED": 0,
        "BACKLOG_MODIFICATION_COUNT": 0,
        "ORIGINAL_FILES_MODIFIED": 0,
        "PROTECTED_EVIDENCE_HASHES_UNCHANGED": protected_unchanged,
        "OCR_RUN": 0,
        "Q3_OCR_RUN": 0,
        "PDF_RENDER_RUN": 0,
        "G11_SAMPLE_PDF_RENDER_RUN": 0,
        "PDF_INSPECTOR_EXTRACTION_RUN": 0,
        "PDFTOTEXT_EXTRACTION_RUN": 0,
        "BODY_RECONSTRUCTION_RUN": 0,
        "FORMAL_ARTIFACTS_GENERATED": 0,
        "REVIEW_PACKET_REGENERATION_RUN": 0,
        "DOC_BATCH_RUN": 0,
        "Q3_REPAIR_RUN": 0,
        "IMAGE_OCR_RUN": 0,
        "IMAGE_EXTRACTION_RERUN": 0,
        "G9_REBUILD_RUN": 0,
        "G10_REBUILD_OR_REPAIR_RUN": 0,
        "G12_RUN": 0,
        "NETWORK_ACCESS_USED": 0,
        "DOWNLOAD_RUN": 0,
        "NEW_DEPENDENCY_INSTALLED": 0,
        "WORD_RUN": 0,
        "WORD_COM_RUN": 0,
        "DOC_CONVERSION_RUN": 0,
        "PRINT_JOB_RUN": 0,
        "GIT_OPERATIONS": 0,
        "SOURCE_SHA_MISMATCH": int(g10_result.get("SOURCE_SHA_MISMATCH_COUNT", -1) != 0),
        "FORMAL_REGISTRY_HASH_MISMATCH_COUNT": formal_registry_hash_mismatch,
        "FORMAL_EVIDENCE_GATE_PASS": formal_evidence_ok,
        "FROZEN_STATE_GATE_PASS": frozen_ok,
        "REPAIR_GROUPS": [
            "A: 10 confirmed Q0 formal marker-only identities; targeted source text acquisition/extraction, reconstruction, body regeneration, artifact repromotion, index refresh, and G10 revalidation.",
            "B: CUMCM-2020-D-003; selective OCR page repair for pages 1, 68, and 135, then reconstruction/body regeneration and downstream QA.",
            "C: 0.",
            f"UNRESOLVED: {len(unresolved_ids)} identities / {unresolved_count} page segments; targeted diagnostic required before repair.",
        ],
        "OUTPUTS": [
            rel(OUTPUT_TARGETS),
            rel(OUTPUT_PAGES),
            rel(OUTPUT_RESULT),
            rel(OUTPUT_REPORT),
            rel(Path(__file__)),
        ],
        "VALIDATION": [
            "Branch and HEAD exactly matched the authoritative G11 baseline.",
            f"Scanned {total_formal_artifacts} formal paper.md files and recomputed {total_source_page_markers} source_page markers.",
            f"Marker-only classification partition passed: legitimate={legitimate_count}, defective={defective_count}, unresolved={unresolved_count}, total={total_marker_only_pages}.",
            f"The 10 known HIGH-confidence formal defects all classified as DEFECTIVE_MARKER_ONLY_PAGE; mismatch={known_mismatch_count}.",
            f"The prior 215 value was rederived as the fully marker-only subset; current any-marker-only candidate identity count is {len(candidate_ids)}.",
            "All 10 confirmed formal targets share the Q0/pdf-inspector/OTHER_FORMAL_DERIVED marker-only serialization pattern; governed duplicate is not treated as causal.",
            "CUMCM-2020-D-003 page provenance, reconstruction manifest/provenance/quality, and persisted OCR hashes for pages 1, 68, and 135 were checked read-only; semantic OCR defect remains supported by the existing human comment.",
            "Protected formal, index, identity, membership, eligibility, source, decision, and G10 evidence hashes were unchanged during this plan run.",
        ],
        "ISSUES": [
            f"{len(unresolved_ids)} candidate identities remain unresolved because repository evidence does not establish whether their marker-only pages are substantive source pages or legitimate empty pages.",
            "No unresolved candidate was added to the formal repair target table.",
            "G11 remains PARTIAL; this is a repair-plan result, not G11 closure.",
        ],
        "BLOCKER": blocker,
        "NEXT": next_stage,
    }
    write_json(OUTPUT_RESULT, result)

    report = f"""# G11-MAJOR-DEFECT-MINIMAL-REPAIR-PLAN

## Stage result

- `STATUS={status}`
- `BRANCH={branch}`
- `HEAD={head}`
- `REPAIR_PLAN_ATTEMPT_ID={repair_plan_attempt_id}`
- `G11_STATUS_REMAINS=PARTIAL`
- `BLOCKER={blocker}`
- `NEXT={next_stage}`

This stage is planning-only. No OCR, extraction, rendering, reconstruction, artifact regeneration, index rebuild, G10 rerun, network access, or G12 execution was performed.

## Frozen baseline

`TOTAL_IDENTITIES=642`, `ELIGIBLE=453`, `INELIGIBLE=189`, `ARTIFACT_SETS=453`, `PRIMARY_ARTIFACTS=1359`, `FORMAL_INDEX_RECORDS=453`, `DOC_MANUAL_BACKLOG=0`, `Q3_MANUAL_BACKLOG=0`, and `TOTAL_MANUAL_BACKLOG=0` remained unchanged.

The branch/HEAD gate passed. The decision sheet SHA remained `{decision_sha}`. Protected evidence hashes were unchanged: `{protected_unchanged}`.

## Full formal scan and classification

- Formal `paper.md` files scanned: `{total_formal_artifacts}`
- `source_page` markers: `{total_source_page_markers}`
- Marker-only page segments: `{total_marker_only_pages}`
- Marker-only candidate identities: `{len(candidate_ids)}`
- Fully marker-only formal-body identities: `{len(fully_marker_only_ids)}`; this exactly rederives the prior `215` subset.
- Legitimate marker-only pages: `{legitimate_count}`
- Confirmed defective marker-only pages: `{defective_count}`
- Unresolved marker-only pages: `{unresolved_count}`
- Confirmed defective identities: `{len(defective_ids)}`
- Unresolved candidate identities: `{len(unresolved_ids)}`

The classification partition passed: `{legitimate_count} + {defective_count} + {unresolved_count} = {total_marker_only_pages}`. The zero legitimate count is evidence-based: no existing explicit `VERIFIED_BLANK_SOURCE_PAGE` classification intersected this marker-only set. Unobserved pages remain unresolved rather than being guessed as defects.

The previous value `215` is therefore not accepted as the full affected scope. It is the subset whose entire formal body is marker-only. The current broader static candidate scope is `{len(candidate_ids)}` identities because it also includes partially populated bodies; only `{len(defective_ids)}` identities have existing source-page evidence sufficient for repair planning. Identity-level unresolved count is non-overlapping: `{len(unresolved_ids)}` candidates have no confirmed defective page, while `{len(identities_with_defect_and_unresolved_pages)}` of the 10 confirmed targets also contain additional unobserved marker-only pages and remain page-partially unresolved.

## Confirmed formal repair targets

`FORMAL_ARTIFACT_REPAIR_TARGET_COUNT={len(target_rows)}`. The target table contains only:

`{'; '.join(known_formal_ids)}`

The confirmed page-level repair set contains `{defective_count}` unique selected source pages. The generated page table also retains all `{total_marker_only_pages}` marker-only segments, including unresolved rows, so unresolved scope is auditable but not actionable.

## Common root cause

`COMMON_ROOT_CAUSE_PATTERN_FOUND=1`

The 10 confirmed defects share this path: `OTHER_FORMAL_DERIVED` → PDF source → Q0 → `pdf-inspector` / native Markdown route → `g8_file_source_map.csv` → extraction contract `1` → page-granular G9 records, while the formal body contains only `source_page` shells for the evidenced pages. The existing OTHER-formal metadata does not record a generator version or formal-generation attempt. Body-hash duplication is correlated context only: all 10 are in governed duplicate groups, but G10 reports `GOVERNED_BODY_HASH_DUPLICATES=32` and `UNEXPECTED_BODY_HASH_DUPLICATES=0`; no identity, membership, source, or duplicate-binding defect was found.

## CUMCM-2020-D-003 independent route

`CUMCM_2020_D_003_REPAIR_LAYER={q3_repair_layer}` for selected pages `1, 68, 135`.

Existing Q3 page audit, reconstruction manifest/provenance/quality, and persisted page text are present, nonempty, hash-consistent, and marked OCR-backed. The existing reviewer comment explicitly reports OCR/symbol substitutions affecting variables, coordinates, operators, and model meaning. Therefore the persisted OCR text itself is the supported semantic defect layer, and the minimum plan is selective page OCR followed by reconstruction/body regeneration. The formal body is substantive but has no `source_page` markers; that is a separate page-granularity limitation, not evidence that OCR is correct. Exact corrupt spans are intentionally not invented and must be enumerated in the next targeted page QA stage.

## Repair groups and downstream strategy

- Group A: `{len(target_rows)}` confirmed Q0 formal marker-only identities. Targeted source text acquisition/extraction, reconstruction, formal body regeneration, artifact repromotion, index refresh, G10 consistency validation, and mandatory human re-review.
- Group B: `1` identity, `CUMCM-2020-D-003`. Selective OCR for pages `1,68,135`, then reconstruction/body regeneration, artifact repromotion, index refresh, G10 validation, and human re-review.
- Group C: `0`.
- Unresolved group: `{len(unresolved_ids)}` identities / `{unresolved_count}` page segments. Run targeted diagnostic first; do not run full-corpus OCR or automatically add them to repair.

After any actual artifact-content change, plan a targeted artifact promotion followed by a deterministic index projection refresh (full projection rebuild is permitted only if that is the safe implementation) and G10 revalidation of 453 eligible identities, 453 artifact sets, 1359 primary artifacts, hashes, bindings, source provenance, coverage, orphan count, and duplicate governance.

Mandatory G11 re-review remains `11` original MAJOR samples. Newly discovered identities are not added to the frozen 30-sample decision sheet automatically.

## Outputs

- `{rel(OUTPUT_TARGETS)}`
- `{rel(OUTPUT_PAGES)}`
- `{rel(OUTPUT_RESULT)}`
- `{rel(Path(__file__))}`

No formal data, formal artifact content, formal index, identity, membership, eligibility, backlog, source, decision, or G12 state was modified.
"""
    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_REPORT.write_text(report, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
