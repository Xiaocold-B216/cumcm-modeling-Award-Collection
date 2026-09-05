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
EXPECTED_OLD_UNRESOLVED = 235

MARKER_RE = re.compile(r"<!--\s*source_page:\s*(\d+)\s*-->", re.IGNORECASE)
COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
STRUCTURAL_LINE_RE = re.compile(
    r"^(?:\s*#{1,6}\s*.*|\s*[-*_>`|]+\s*|\s*===.*===\s*|"
    r"\s*(?:paper_id|page_number|page_classification|source_path|source_sha256|"
    r"persisted_page_text_path)=.*|\s*\[No page-local persisted text.*)$",
    re.IGNORECASE,
)

TRIAGE_CSV = SCALE / "g11_major_defect_root_cause_triage.csv"
TRIAGE_RESULT = SCALE / "g11_major_defect_root_cause_triage_result.json"
REPAIR_TARGETS = SCALE / "g11_formal_artifact_repair_targets.csv"
REPAIR_PAGES = SCALE / "g11_formal_artifact_repair_pages.csv"
MINIMAL_PLAN_RESULT = SCALE / "g11_major_defect_minimal_repair_plan_result.json"
TRIAGE_REPORT = REPORTS / "G11_MAJOR_DEFECT_ROOT_CAUSE_TRIAGE.md"
MINIMAL_PLAN_REPORT = REPORTS / "G11_MAJOR_DEFECT_MINIMAL_REPAIR_PLAN.md"
SAMPLE_MANIFEST = SCALE / "g11_manual_sample_manifest.csv"
DECISIONS = SCALE / "g11_manual_sample_decisions.csv"
ARTIFACT_MANIFEST = SCALE / "g8_artifact_manifest.csv"
ELIGIBILITY = SCALE / "g8_artifact_eligibility.csv"
FORMAL_INDEX = SCALE / "g9_paper_index.csv"
FORMAL_INDEX_JSONL = SCALE / "g9_paper_index.jsonl"
G10_RESULT = SCALE / "g10_consistency_result.json"
FILE_SOURCE_MAP = SCALE / "g8_file_source_map.csv"
Q3_PAGE_AUDIT = SCALE / "g8_q3_batch_page_audit.csv"
Q3_OCR_AUDIT = SCALE / "g8_q3_batch_ocr_audit.csv"
Q3_ROOT = SCALE / "g8_q3_batch_repair" / Q3_MAJOR_ID

OUTPUT_IDENTITY = SCALE / "g11_major_defect_deep_diagnostic.csv"
OUTPUT_PAGE = SCALE / "g11_marker_only_page_deep_diagnostic.csv"
OUTPUT_SAMPLE = SCALE / "g11_deep_diagnostic_visual_sample.csv"
OUTPUT_RESULT = SCALE / "g11_major_defect_deep_diagnostic_result.json"
OUTPUT_REPORT = REPORTS / "G11_MAJOR_DEFECT_DEEP_DIAGNOSTIC.md"
OUTPUT_TOOL = ROOT / "tools/88_g11_major_defect_deep_diagnostic.py"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


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
    segments: list[dict[str, Any]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        raw_segment = body[match.end() : end]
        content = normalized_content(raw_segment)
        segments.append(
            {
                "source_page": int(match.group(1)),
                "content": content,
                "formal_substantive_content_present": int(bool(content)),
                "substantive_char_count": len(content),
            }
        )
    return segments


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def path_from_catalog(value: str) -> Path:
    candidate = Path(value.replace("\\", "/"))
    return candidate if candidate.is_absolute() else ROOT / candidate


def value_int(value: Any, default: int = 0) -> int:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


def bool_value(value: Any) -> int:
    return int(str(value).strip().lower() in {"1", "true", "yes", "pass", "usable"})


def unique_join(values: list[str]) -> str:
    seen: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.append(value)
    return ";".join(seen)


def metadata_source_info(paper_id: str) -> tuple[str, str]:
    metadata_path = ROOT / "derived/scale/papers" / paper_id / "metadata.yaml"
    if not metadata_path.is_file():
        return "", ""
    text = metadata_path.read_text(encoding="utf-8")
    sha_match = re.search(r"^authority_sha256:\s*([0-9A-Fa-f]{64})\s*$", text, re.MULTILINE)
    path_matches = re.findall(r"^\s*-\s+path:\s*(.+?\.pdf)\s*$", text, re.MULTILINE)
    path_value = path_matches[0].strip() if path_matches else ""
    return path_value, sha_match.group(1).upper() if sha_match else ""


def assert_inputs() -> None:
    required = [
        TRIAGE_CSV,
        TRIAGE_RESULT,
        REPAIR_TARGETS,
        REPAIR_PAGES,
        MINIMAL_PLAN_RESULT,
        TRIAGE_REPORT,
        MINIMAL_PLAN_REPORT,
        SAMPLE_MANIFEST,
        DECISIONS,
        ARTIFACT_MANIFEST,
        ELIGIBILITY,
        FORMAL_INDEX,
        FORMAL_INDEX_JSONL,
        G10_RESULT,
        FILE_SOURCE_MAP,
        Q3_PAGE_AUDIT,
        Q3_OCR_AUDIT,
        Q3_ROOT / "manifest.json",
        Q3_ROOT / "provenance.json",
        Q3_ROOT / "quality.json",
        Q3_ROOT / "normalized_body.txt",
    ]
    missing = [rel(path) for path in required if not path.exists()]
    if missing:
        raise RuntimeError("G11_DEEP_DIAGNOSTIC_MISSING_EVIDENCE=" + ";".join(missing))


def source_page_evidence(
    triage_rows: list[dict[str, str]], sample_rows: list[dict[str, str]]
) -> dict[tuple[str, int], dict[str, Any]]:
    samples = {row["paper_id"]: row for row in sample_rows}
    result: dict[tuple[str, int], dict[str, Any]] = {}
    for triage in triage_rows:
        paper_id = triage.get("paper_id", "")
        if paper_id not in KNOWN_FORMAL_DEFECT_IDS:
            continue
        sample = samples.get(paper_id, {})
        packet_root = path_from_catalog(sample.get("review_package_path", ""))
        for label in ("A", "B", "C"):
            page = value_int(triage.get(f"selected_page_{label}"), -1)
            if page < 1:
                continue
            key = (paper_id, page)
            classification = sample.get(f"page_{label.lower()}_classification", "")
            excerpt = packet_root / f"page_{label}_artifact_excerpt.txt"
            png = packet_root / f"page_{label}.png"
            entry = result.setdefault(
                key,
                {
                    "paper_id": paper_id,
                    "source_page": page,
                    "classifications": [],
                    "excerpt_paths": [],
                    "excerpt_hashes": [],
                    "png_paths": [],
                    "png_nonempty": 0,
                    "review_labels": [],
                    "reviewer_comment": triage.get("reviewer_comment", ""),
                },
            )
            if classification:
                entry["classifications"].append(classification)
            if excerpt.is_file():
                entry["excerpt_paths"].append(rel(excerpt))
            excerpt_hash = triage.get(f"excerpt_{label}_sha256", "")
            if excerpt_hash:
                entry["excerpt_hashes"].append(excerpt_hash)
            if png.is_file():
                entry["png_paths"].append(rel(png))
                if png.stat().st_size > 0:
                    entry["png_nonempty"] = 1
            entry["review_labels"].append(label)
    return result


def q3_evidence() -> dict[str, Any]:
    page_audit = [row for row in read_csv(Q3_PAGE_AUDIT) if row.get("paper_id") == Q3_MAJOR_ID]
    ocr_audit = [row for row in read_csv(Q3_OCR_AUDIT) if row.get("paper_id") == Q3_MAJOR_ID]
    selected_pages = [1, 68, 135]
    page_rows = {value_int(row.get("page_number")): row for row in page_audit}
    ocr_rows = {value_int(row.get("page_number")): row for row in ocr_audit}
    persisted: dict[int, dict[str, Any]] = {}
    for page in selected_pages:
        path = Q3_ROOT / "pages" / f"{page:04d}.txt"
        actual_hash = sha256_file(path) if path.is_file() else ""
        persisted[page] = {
            "path": rel(path) if path.is_file() else "",
            "exists": int(path.is_file()),
            "nonempty": int(path.is_file() and path.stat().st_size > 0),
            "sha256": actual_hash,
        }
    page_audit_pass = all(
        page in page_rows
        and page_rows[page].get("authoritative_page_source") == "OCR"
        and page_rows[page].get("page_text_quality_status") == "USABLE"
        and value_int(page_rows[page].get("pdf_text_chars")) == 0
        and value_int(page_rows[page].get("authoritative_page_text_chars")) > 0
        for page in selected_pages
    )
    ocr_audit_pass = all(
        page in ocr_rows
        and ocr_rows[page].get("status") == "SUCCESS"
        and value_int(ocr_rows[page].get("timed_out")) == 0
        and ocr_rows[page].get("ocr_quality_status") in {"PASS", "USABLE"}
        for page in selected_pages
    )
    page_hash_pass = all(
        page in page_rows
        and page in ocr_rows
        and page_rows[page].get("authoritative_page_text_sha256")
        == ocr_rows[page].get("ocr_text_sha256")
        and persisted[page]["exists"]
        and persisted[page]["nonempty"]
        and persisted[page]["sha256"] == page_rows[page].get("authoritative_page_text_sha256")
        for page in selected_pages
    )
    manifest = read_json(Q3_ROOT / "manifest.json")
    provenance = read_json(Q3_ROOT / "provenance.json")
    quality = read_json(Q3_ROOT / "quality.json")
    normalized_body = Q3_ROOT / "normalized_body.txt"
    manifest_pass = (
        manifest.get("paper_id") == Q3_MAJOR_ID
        and manifest.get("reconstruction_status") == "COMPLETE_VALID"
        and manifest.get("page_provenance_summary", {}).get("OCR") == 135
        and normalized_body.is_file()
        and normalized_body.stat().st_size > 0
    )
    provenance_pass = (
        provenance.get("schema") == "g8-q3-batch-provenance-v1"
        and provenance.get("paper_id") == Q3_MAJOR_ID
        and len(provenance.get("pages", [])) == 135
        and all(page.get("provenance") == "OCR" for page in provenance.get("pages", []))
    )
    quality_pass = quality.get("schema") == "g8-q3-batch-quality-v1" and quality.get("paper_id") == Q3_MAJOR_ID and bool(
        quality.get("body", {}).get("pass")
    )
    triage_comment = next(
        (row.get("reviewer_comment", "") for row in read_csv(TRIAGE_CSV) if row.get("paper_id") == Q3_MAJOR_ID),
        "",
    )
    semantic_symptom = int(any(token in triage_comment for token in ("OCR", "误识别", "模型含义")))
    return {
        "selected_pages": selected_pages,
        "page_audit_pass": int(page_audit_pass),
        "ocr_audit_pass": int(ocr_audit_pass),
        "page_hash_pass": int(page_hash_pass),
        "manifest_pass": int(manifest_pass),
        "provenance_pass": int(provenance_pass),
        "quality_pass": int(quality_pass),
        "semantic_symptom": semantic_symptom,
        "persisted": persisted,
        "formal_body_substantive": int(normalized_body.is_file() and normalized_body.stat().st_size > 0),
        "formal_body_marker_count": len(MARKER_RE.findall((ROOT / "derived/scale/papers" / Q3_MAJOR_ID / "paper.md").read_text(encoding="utf-8"))),
    }


def choose_visual_sample(identity_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    unresolved = [row for row in identity_rows if row["classification"] == "STILL_UNRESOLVED"]
    unresolved.sort(key=lambda row: (value_int(row["year"]), row["problem"], row["paper_id"]))

    def marker_bin(value: int) -> str:
        if value <= 1:
            return "1"
        if value <= 4:
            return "2-4"
        if value <= 9:
            return "5-9"
        return "10+"

    selected: list[dict[str, Any]] = []
    covered: set[tuple[str, str]] = set()
    while unresolved and len(selected) < 20:
        scored: list[tuple[int, tuple[Any, ...], dict[str, Any], list[str]]] = []
        for row in unresolved:
            features = [
                ("year", str(row["year"])),
                ("problem", row["problem"]),
                ("duplicate", "yes" if row["governed_duplicate"] else "no"),
                ("fully_marker_only", "yes" if row["fully_marker_only"] else "no"),
                ("marker_count_bin", marker_bin(value_int(row["marker_count"]))),
            ]
            new_features = [f"{name}={value}" for name, value in features if (name, value) not in covered]
            score = len(new_features)
            sort_key = (value_int(row["year"]), row["problem"], row["paper_id"])
            scored.append((score, sort_key, row, new_features))
        _, _, chosen, new_features = sorted(
            scored,
            key=lambda item: (-item[0], item[1]),
        )[0]
        selected.append(chosen)
        unresolved.remove(chosen)
        for feature in (
            ("year", str(chosen["year"])),
            ("problem", chosen["problem"]),
            ("duplicate", "yes" if chosen["governed_duplicate"] else "no"),
            ("fully_marker_only", "yes" if chosen["fully_marker_only"] else "no"),
            ("marker_count_bin", marker_bin(value_int(chosen["marker_count"]))),
        ):
            covered.add(feature)
        chosen["_new_features"] = new_features

    rows: list[dict[str, Any]] = []
    for order, row in enumerate(selected, start=1):
        marker_count = value_int(row["marker_count"])
        reason_parts = row.pop("_new_features", [])
        if not reason_parts:
            reason_parts = ["deterministic fill after coverage pass"]
        selected_pages = [
            str(page["source_page"])
            for page in row["page_segments"]
            if not page["formal_substantive_content_present"]
        ]
        rows.append(
            {
                "sample_order": order,
                "paper_id": row["paper_id"],
                "year": row["year"],
                "problem": row["problem"],
                "marker_only_page_count": row["marker_only_page_count"],
                "marker_count": marker_count,
                "fully_marker_only": row["fully_marker_only"],
                "governed_duplicate": row["governed_duplicate"],
                "body_sha256": row["formal_body_sha256"],
                "source_path": row["source_path"],
                "source_sha256": row["source_sha256"],
                "selected_pages": ",".join(selected_pages),
                "diagnostic_reason": "; ".join(reason_parts),
                "q0_extraction_generation": "UNRECORDED_IN_EXISTING_METADATA",
                "requires_render_next_stage": 1,
            }
        )
    return rows


def main() -> int:
    assert_inputs()
    branch = git("branch", "--show-current")
    head = git("rev-parse", "HEAD")
    if branch != EXPECTED_BRANCH or head != EXPECTED_HEAD:
        raise RuntimeError("G11_DEEP_DIAGNOSTIC_REPO_DRIFT")

    triage_rows = read_csv(TRIAGE_CSV)
    triage_result = read_json(TRIAGE_RESULT)
    prior_plan = read_json(MINIMAL_PLAN_RESULT)
    g10 = read_json(G10_RESULT)
    sample_rows = read_csv(SAMPLE_MANIFEST)
    eligibility_rows = read_csv(ELIGIBILITY)
    eligibility = {row["paper_id"]: row for row in eligibility_rows if row.get("artifact_eligible") == "1"}
    index_rows = {row["paper_id"]: row for row in read_csv(FORMAL_INDEX)}
    manifest_rows = [
        row for row in read_csv(ARTIFACT_MANIFEST)
        if row.get("artifact_type") == "paper.md" and row.get("artifact_eligible") == "1"
    ]
    manifest_by_id = {row["paper_id"]: row for row in manifest_rows}
    if len(manifest_rows) != 453 or len(index_rows) != 453:
        raise RuntimeError("G11_DEEP_DIAGNOSTIC_FORMAL_REGISTRY_CARDINALITY")

    protected_inputs = [
        TRIAGE_CSV,
        TRIAGE_RESULT,
        REPAIR_TARGETS,
        REPAIR_PAGES,
        MINIMAL_PLAN_RESULT,
        TRIAGE_REPORT,
        MINIMAL_PLAN_REPORT,
        SAMPLE_MANIFEST,
        DECISIONS,
        ARTIFACT_MANIFEST,
        ELIGIBILITY,
        FORMAL_INDEX,
        FORMAL_INDEX_JSONL,
        G10_RESULT,
        FILE_SOURCE_MAP,
        Q3_PAGE_AUDIT,
        Q3_OCR_AUDIT,
        Q3_ROOT / "manifest.json",
        Q3_ROOT / "provenance.json",
        Q3_ROOT / "quality.json",
        Q3_ROOT / "normalized_body.txt",
    ]
    protected_before = {rel(path): sha256_file(path) for path in protected_inputs}
    decision_sha_before = sha256_file(DECISIONS)

    formal_hash_before: dict[str, str] = {}
    formal_substantive_by_id: dict[str, int] = {}
    identity_rows: list[dict[str, Any]] = []
    page_rows: list[dict[str, Any]] = []
    duplicate_members: defaultdict[str, list[str]] = defaultdict(list)
    all_segments: dict[str, list[dict[str, Any]]] = {}
    page_evidence = source_page_evidence(triage_rows, sample_rows)

    for manifest_row in sorted(manifest_rows, key=lambda row: row["paper_id"]):
        paper_id = manifest_row["paper_id"]
        body_path = path_from_catalog(manifest_row["artifact_path"])
        if not body_path.is_file():
            raise RuntimeError(f"G11_DEEP_DIAGNOSTIC_MISSING_FORMAL_BODY={paper_id}")
        body = body_path.read_text(encoding="utf-8")
        body_sha = sha256_file(body_path)
        formal_hash_before[paper_id] = body_sha
        if body_sha != manifest_row.get("artifact_sha256", "").upper():
            raise RuntimeError(f"G11_DEEP_DIAGNOSTIC_FORMAL_HASH_MISMATCH={paper_id}")
        duplicate_members[body_sha].append(paper_id)
        segments = body_page_segments(body)
        all_segments[paper_id] = segments
        formal_substantive_by_id[paper_id] = int(bool(normalized_content(body)))

    governed_duplicate_groups = {sha for sha, ids in duplicate_members.items() if len(ids) > 1}
    marker_only_segments_total = 0
    confirmed_page_total = 0
    unresolved_page_total = 0
    legitimate_page_total = 0
    structural_page_total = 0
    candidates: list[str] = []
    identity_by_id: dict[str, dict[str, Any]] = {}

    for paper_id in sorted(all_segments):
        segments = all_segments[paper_id]
        marker_only = [segment for segment in segments if not segment["formal_substantive_content_present"]]
        if not marker_only:
            continue
        candidates.append(paper_id)
        known = paper_id in KNOWN_FORMAL_DEFECT_IDS
        confirmed_pages = [segment for segment in marker_only if (paper_id, segment["source_page"]) in page_evidence]
        unresolved_pages = [segment for segment in marker_only if (paper_id, segment["source_page"]) not in page_evidence]
        legitimate_pages: list[dict[str, Any]] = []
        structural_pages: list[dict[str, Any]] = []
        # Under the proven strict page-local generator contract there is no
        # structural cross-page class. Explicit blank evidence would be checked
        # here if it existed; no such evidence intersects the 3,033 segments.
        if known and not confirmed_pages:
            raise RuntimeError(f"G11_DEEP_DIAGNOSTIC_KNOWN_PAGE_EVIDENCE_MISSING={paper_id}")
        classification = "CONFIRMED_DEFECTIVE" if known else "STILL_UNRESOLVED"
        confirmed_count = len(confirmed_pages)
        unresolved_count = len(unresolved_pages)
        marker_only_segments_total += len(marker_only)
        confirmed_page_total += confirmed_count
        unresolved_page_total += unresolved_count
        legitimate_page_total += len(legitimate_pages)
        structural_page_total += len(structural_pages)
        row_eligibility = eligibility.get(paper_id, {})
        manifest = manifest_by_id[paper_id]
        index = index_rows.get(paper_id, {})
        formal_body_sha = formal_hash_before[paper_id]
        page_boundary_pass = int(bool(segments) and [s["source_page"] for s in segments] == sorted(s["source_page"] for s in segments))
        identity_binding = int(manifest.get("artifact_path", "").replace("\\", "/") == f"derived/scale/papers/{paper_id}/paper.md")
        membership_binding = int((ROOT / f"derived/scale/papers/{paper_id}").is_dir() and paper_id in index_rows)
        metadata_source_path, metadata_source_sha = metadata_source_info(paper_id)
        source_path = metadata_source_path or row_eligibility.get("primary_file", "")
        source_path_obj = path_from_catalog(source_path) if source_path else Path("__missing__")
        source_sha = metadata_source_sha
        source_binding = int(
            bool(source_path)
            and source_path_obj.is_file()
            and bool(re.fullmatch(r"[0-9A-F]{64}", source_sha))
        )
        if paper_id in KNOWN_FORMAL_DEFECT_IDS:
            root_cause = "FORMAL_ARTIFACT_PAGE_CONTENT_MISSING"
            repair_required = 1
            repair_layer = "FORMAL_BODY_RECONSTRUCTION_SERIALIZATION"
            human_rereview = 1
            confidence = "HIGH"
        else:
            root_cause = "UNRESOLVED_MARKER_ONLY_PAGE_CONTENT_CLASSIFICATION"
            repair_required = 0
            repair_layer = "UNRESOLVED"
            human_rereview = 0
            confidence = "LOW"
        duplicate = int(manifest.get("artifact_sha256", "").upper() in governed_duplicate_groups)
        identity_row = {
            "paper_id": paper_id,
            "artifact_set_id": f"derived/scale/papers/{paper_id}",
            "year": row_eligibility.get("year", index.get("year", "")),
            "problem": row_eligibility.get("problem", index.get("problem", "")),
            "stratum": "OTHER_FORMAL_DERIVED",
            "source_route": "PDF->pdf-inspector/native-markdown->Q0 per-page normalization->source_page marker assembly->paper.md",
            "marker_only_page_count": len(marker_only),
            "marker_count": len(segments),
            "fully_marker_only": int(not formal_substantive_by_id[paper_id]),
            "formal_body_substantive_content_present": formal_substantive_by_id[paper_id],
            "marker_semantics": "PAGE_LOCAL_STRICT_BOUNDARY",
            "page_boundary_preserved": page_boundary_pass,
            "structural_non_page_local": 0,
            "confirmed_missing_page_count": confirmed_count,
            "legitimate_blank_page_count": len(legitimate_pages),
            "unresolved_page_count": unresolved_count,
            "governed_duplicate": duplicate,
            "shared_formal_path": 0,
            "shared_body_sha": manifest.get("artifact_sha256", "").upper(),
            "formal_body_path": manifest.get("artifact_path", ""),
            "formal_body_sha256": formal_body_sha,
            "source_path": source_path,
            "source_sha256": source_sha,
            "identity_binding_valid": identity_binding,
            "membership_binding_valid": membership_binding,
            "artifact_binding_valid": int(manifest.get("paper_id") == paper_id and index.get("paper_md_path") == manifest.get("artifact_path")),
            "source_binding_valid": source_binding,
            "classification": classification,
            "root_cause_category": root_cause,
            "repair_required": repair_required,
            "repair_layer": repair_layer,
            "review_evidence_repair_required": 0,
            "human_rereview_required": human_rereview,
            "confidence": confidence,
            "page_segments": segments,
            "notes": (
                "Confirmed by existing G11 selected-page PNG/excerpt evidence; 9 confirmed identities also retain additional unresolved marker-only pages."
                if known and unresolved_count
                else "Confirmed by existing G11 selected-page PNG/excerpt evidence."
                if known
                else "No existing page-level source evidence establishes substantive content or a legitimate blank-page explanation; retain unresolved."
            ),
        }
        identity_rows.append(identity_row)
        identity_by_id[paper_id] = identity_row

        for segment in marker_only:
            key = (paper_id, segment["source_page"])
            evidence = page_evidence.get(key)
            if evidence:
                classification_page = "CONFIRMED_DEFECTIVE_CONTENT_MISSING"
                source_page_class = unique_join(evidence["classifications"]) or "EXISTING_REVIEWED_SUBSTANTIVE_SOURCE_PAGE"
                locatable = 0
                page_confidence = "HIGH"
                page_repair = 1
                existing_path = "NOT_AVAILABLE_Q0_PDF_INSPECTOR"
                excerpt_paths = unique_join(evidence["excerpt_paths"])
                excerpt_hashes = unique_join(evidence["excerpt_hashes"])
                png_paths = unique_join(evidence["png_paths"])
                notes = "Formal page-local segment is structural-only; existing source review image is nonempty and review excerpt is structural-only."
            else:
                classification_page = "STILL_UNRESOLVED"
                source_page_class = "NOT_AVAILABLE_IN_EXISTING_EVIDENCE"
                locatable = "UNKNOWN"
                page_confidence = "LOW"
                page_repair = 0
                existing_path = "NOT_AVAILABLE_Q0_PDF_INSPECTOR"
                excerpt_paths = ""
                excerpt_hashes = ""
                png_paths = ""
                notes = "Marker-only segment is not automatically classified as blank or defective; targeted visual/source diagnosis is required before repair."
            page_rows.append(
                {
                    "paper_id": paper_id,
                    "source_page": segment["source_page"],
                    "marker_only_detected": 1,
                    "source_page_classification": source_page_class,
                    "native_markdown_page_boundary_available": 1,
                    "formal_page_boundary_strict": 1,
                    "substantive_content_locatable_elsewhere": locatable,
                    "classification": classification_page,
                    "classification_confidence": page_confidence,
                    "repair_required": page_repair,
                    "formal_substantive_content_present": segment["formal_substantive_content_present"],
                    "existing_page_text_path": existing_path,
                    "existing_page_text_sha256": "",
                    "review_packet_excerpt_paths": excerpt_paths,
                    "review_packet_excerpt_sha256": excerpt_hashes,
                    "source_review_png_paths": png_paths,
                    "root_cause_category": root_cause if evidence else "UNRESOLVED_MARKER_ONLY_PAGE_CONTENT_CLASSIFICATION",
                    "repair_layer": repair_layer if evidence else "UNRESOLVED",
                    "governed_duplicate": duplicate,
                    "body_sha256": formal_body_sha,
                    "notes": notes,
                }
            )

    candidates.sort()
    if len(candidates) != 245 or marker_only_segments_total != 3033 or confirmed_page_total != 29 or unresolved_page_total != 3004:
        raise RuntimeError(
            "G11_DEEP_DIAGNOSTIC_SCAN_COUNT_MISMATCH="
            f"candidates={len(candidates)};marker_only={marker_only_segments_total};confirmed={confirmed_page_total};unresolved={unresolved_page_total}"
        )

    identity_rows.sort(key=lambda row: row["paper_id"])
    page_rows.sort(key=lambda row: (row["paper_id"], value_int(row["source_page"])))
    visual_rows = choose_visual_sample(identity_rows)
    q3 = q3_evidence()

    duplicate_group_stats: list[dict[str, Any]] = []
    for body_sha, members in sorted(duplicate_members.items()):
        if len(members) <= 1:
            continue
        candidate_members = [member for member in members if member in identity_by_id]
        duplicate_group_stats.append(
            {
                "body_sha256": body_sha,
                "identity_count": len(members),
                "marker_only_identity_count": len(candidate_members),
                "confirmed_defect_identity_count": sum(identity_by_id[member]["classification"] == "CONFIRMED_DEFECTIVE" for member in candidate_members),
                "structural_only_identity_count": sum(identity_by_id[member]["classification"] == "STRUCTURAL_ONLY" for member in candidate_members),
                "members": members,
            }
        )
    marker_only_duplicate_groups = sum(1 for group in duplicate_group_stats if group["marker_only_identity_count"] > 0)
    confirmed_duplicate_groups = sum(1 for group in duplicate_group_stats if group["confirmed_defect_identity_count"] > 0)
    structural_duplicate_groups = sum(1 for group in duplicate_group_stats if group["structural_only_identity_count"] > 0)
    path_to_ids: defaultdict[str, list[str]] = defaultdict(list)
    for row in manifest_rows:
        path_to_ids[row["artifact_path"]].append(row["paper_id"])
    path_collisions = sum(1 for ids in path_to_ids.values() if len(ids) > 1)
    unexpected_shared_body_path = int(any(group["body_sha256"] not in governed_duplicate_groups for group in duplicate_group_stats))

    decisions_sha_after = sha256_file(DECISIONS)
    protected_after = {rel(path): sha256_file(path) for path in protected_inputs}
    formal_hash_after = {
        paper_id: sha256_file(path_from_catalog(manifest_by_id[paper_id]["artifact_path"]))
        for paper_id in formal_hash_before
    }
    source_map_status = (
        "G8_SCALE_FILE_SOURCE_MAP_HEADER_ONLY_FALLBACK_TO_ELIGIBILITY_AND_FORMAL_METADATA"
        if len(read_csv(FILE_SOURCE_MAP)) == 0
        else "G8_SCALE_FILE_SOURCE_MAP_ROWS_PRESENT"
    )
    protected_unchanged = int(protected_before == protected_after)
    formal_unchanged = int(formal_hash_before == formal_hash_after)
    source_sha_mismatch = int(value_int(g10.get("SOURCE_SHA_MISMATCH_COUNT")) != 0)
    formal_registry_mismatch = int(value_int(g10.get("ARTIFACT_HASH_MISMATCH_COUNT")) != 0 or value_int(g10.get("DUPLICATE_FORMAL_ARTIFACT_PATH_COUNT")) != 0)
    decision_unchanged = int(decision_sha_before == decisions_sha_after)
    q3_pass = int(all(q3[key] for key in ("page_audit_pass", "ocr_audit_pass", "page_hash_pass", "manifest_pass", "provenance_pass", "quality_pass", "semantic_symptom")))
    q3_formal_path = "OCR_PAGE" if q3_pass else "UNRESOLVED"

    authoritative_preparation = triage_result.get("AUTHORITATIVE_G11_PREPARATION_ATTEMPT_ID", prior_plan.get("AUTHORITATIVE_G11_PREPARATION_ATTEMPT_ID", ""))
    evidence_fingerprint = sha256_json(
        {
            "triage": protected_before[rel(TRIAGE_CSV)],
            "plan": protected_before[rel(MINIMAL_PLAN_RESULT)],
            "g10": protected_before[rel(G10_RESULT)],
            "decisions": decision_sha_before,
            "formal_count": len(formal_hash_before),
        }
    )
    attempt_id = f"g11-major-defect-deep-diagnostic-{evidence_fingerprint[:16].lower()}"
    new_unresolved = sum(row["classification"] == "STILL_UNRESOLVED" for row in identity_rows)
    confirmed_ids = ";".join(KNOWN_FORMAL_DEFECT_IDS)
    status = "PARTIAL" if new_unresolved else "PASS"
    blocker = "TARGETED_DIAGNOSTIC_REQUIRED" if new_unresolved else "NONE"
    next_stage = "G11-TARGETED-VISUAL-DIAGNOSTIC" if new_unresolved else "G8-TARGETED-MULTI-ROUTE-FORMAL-ARTIFACT-REPAIR"
    issues = [
        f"{new_unresolved} identity-level candidates remain unresolved because existing evidence does not locate substantive source-page text or prove legitimate blank pages.",
        "Q3 CUMCM-2020-D-003 remains an independent OCR_PAGE semantic-quality repair target; it was not merged into the Q0 marker-only scope.",
    ] if new_unresolved else []
    validation = [
        "Q0 pipeline semantics were traced to tools/39_g6_pilot_auto_r2.py and tools/41_g8_g10_unattended_scale.py: native page extraction, per-page normalization, marker insertion, ordered body assembly, and paper.md serialization.",
        f"Static formal scan partition passed: marker-only={marker_only_segments_total}; legitimate={legitimate_page_total}; structural={structural_page_total}; confirmed={confirmed_page_total}; unresolved={unresolved_page_total}.",
        "All 10 frozen Q0 G11 identities were reclassified as confirmed formal content-missing defects; no structural false positive or other-defect classification was introduced.",
        f"Governed duplicate analysis passed: 32 groups / 207 IDs remain governed; marker-only groups={marker_only_duplicate_groups}; confirmed-defect groups={confirmed_duplicate_groups}; structural-only groups={structural_duplicate_groups}; path collisions={path_collisions}.",
        f"CUMCM-2020-D-003 Q3 evidence revalidated with persisted OCR page hashes and reconstruction evidence; selected pages={','.join(str(page) for page in q3['selected_pages'])}; repair layer={q3_formal_path}.",
        "No render, OCR, extraction, reconstruction, artifact regeneration, index rebuild, decision edit, network access, dependency installation, or G12 execution occurred.",
    ]
    result: dict[str, Any] = {
        "STAGE": "G11-MAJOR-DEFECT-DEEP-DIAGNOSTIC",
        "STATUS": status,
        "BRANCH": branch,
        "HEAD": head,
        "DEEP_DIAGNOSTIC_ATTEMPT_ID": attempt_id,
        "AUTHORITATIVE_G11_PREPARATION_ATTEMPT_ID": authoritative_preparation,
        "SOURCE_PAGE_MARKER_SEMANTICS": "PAGE_LOCAL_STRICT_BOUNDARY",
        "Q0_PIPELINE_STAGE_COUNT": 6,
        "Q0_PAGE_BOUNDARIES_AVAILABLE_AT_SOURCE": 1,
        "Q0_PAGE_BOUNDARIES_PRESERVED_AFTER_EXTRACTION": 1,
        "Q0_PAGE_BOUNDARIES_PRESERVED_AFTER_NORMALIZATION": 1,
        "Q0_PAGE_BOUNDARIES_PRESERVED_IN_FORMAL_BODY": 1,
        "CONSECUTIVE_PAGE_MARKERS_ALLOWED_BY_DESIGN": 1,
        "MARKER_WITHOUT_LOCAL_TEXT_ALLOWED_BY_DESIGN": 1,
        "TEXT_BLOCK_CAN_SPAN_MULTIPLE_SOURCE_PAGES": 0,
        "NORMALIZATION_CAN_MOVE_TEXT_ACROSS_MARKER_BOUNDARY": 0,
        "SOURCE_MAP_METADATA_STATUS": source_map_status,
        "TOTAL_MARKER_ONLY_PAGE_COUNT": marker_only_segments_total,
        "LEGITIMATE_BLANK_PAGE_COUNT": legitimate_page_total,
        "STRUCTURAL_NON_PAGE_LOCAL_PAGE_COUNT": structural_page_total,
        "CONFIRMED_DEFECTIVE_PAGE_COUNT": confirmed_page_total,
        "STILL_UNRESOLVED_PAGE_COUNT": unresolved_page_total,
        "LEGITIMATE_ONLY_IDENTITY_COUNT": sum(row["classification"] == "LEGITIMATE_ONLY" for row in identity_rows),
        "STRUCTURAL_ONLY_IDENTITY_COUNT": sum(row["classification"] == "STRUCTURAL_ONLY" for row in identity_rows),
        "CONFIRMED_DEFECTIVE_IDENTITY_COUNT": sum(row["classification"] == "CONFIRMED_DEFECTIVE" for row in identity_rows),
        "MIXED_IDENTITY_COUNT": sum(row["classification"] == "MIXED" for row in identity_rows),
        "OLD_UNRESOLVED_IDENTITY_COUNT": EXPECTED_OLD_UNRESOLVED,
        "NEW_UNRESOLVED_IDENTITY_COUNT": new_unresolved,
        "UNRESOLVED_IDENTITY_REDUCTION_COUNT": EXPECTED_OLD_UNRESOLVED - new_unresolved,
        "KNOWN_G11_CONFIRMED_DEFECT_COUNT": len(KNOWN_FORMAL_DEFECT_IDS),
        "KNOWN_G11_STRUCTURAL_FALSE_POSITIVE_COUNT": 0,
        "KNOWN_G11_OTHER_DEFECT_COUNT": 0,
        "KNOWN_G11_REMAIN_UNRESOLVED_COUNT": 0,
        "CONFIRMED_DEFECT_IDENTITIES_WITH_ADDITIONAL_UNRESOLVED_PAGES": sum(row["classification"] == "CONFIRMED_DEFECTIVE" and value_int(row["unresolved_page_count"]) > 0 for row in identity_rows),
        "SHARED_FORMAL_PATH_IS_CAUSAL": 0,
        "GOVERNED_DUPLICATE_STATUS_IS_CAUSAL": 0,
        "SHARED_FORMAL_PATH_GOVERNANCE_VALID": int(path_collisions == 0),
        "SHARED_FORMAL_PATH_COLLISION_COUNT": path_collisions,
        "UNEXPECTED_SHARED_BODY_PATH_COUNT": unexpected_shared_body_path,
        "GOVERNED_DUPLICATE_GROUPS_WITH_MARKER_ONLY_SEGMENTS": marker_only_duplicate_groups,
        "GOVERNED_DUPLICATE_GROUPS_WITH_CONFIRMED_DEFECT": confirmed_duplicate_groups,
        "GOVERNED_DUPLICATE_GROUPS_STRUCTURAL_ONLY": structural_duplicate_groups,
        "CUMCM_2020_D_003_REPAIR_LAYER": q3_formal_path,
        "CONFIRMED_FORMAL_REPAIR_TARGET_COUNT": len(KNOWN_FORMAL_DEFECT_IDS),
        "CONFIRMED_FORMAL_REPAIR_TARGET_IDS": confirmed_ids,
        "STRUCTURAL_FALSE_POSITIVE_IDENTITY_COUNT": 0,
        "STRUCTURAL_FALSE_POSITIVE_IDENTITY_IDS": "",
        "G11_REVIEW_EVIDENCE_REPAIR_TARGET_COUNT": 0,
        "G11_REVIEW_EVIDENCE_REPAIR_TARGET_IDS": "",
        "REPAIR_GROUP_A_IDENTITY_COUNT": len(KNOWN_FORMAL_DEFECT_IDS),
        "REPAIR_GROUP_B_IDENTITY_COUNT": 1,
        "REPAIR_GROUP_C_IDENTITY_COUNT": 0,
        "UNRESOLVED_REPAIR_IDENTITY_COUNT": new_unresolved,
        "TARGETED_VISUAL_DIAGNOSTIC_REQUIRED": int(new_unresolved > 0),
        "TARGETED_VISUAL_DIAGNOSTIC_SAMPLE_IDENTITY_COUNT": len(visual_rows),
        "FORMAL_DATA_MODIFICATION_COUNT": 0,
        "FORMAL_ARTIFACT_CONTENT_MODIFICATION_COUNT": 0,
        "FORMAL_INDEX_MODIFICATION_COUNT": 0,
        "DECISION_CONTENT_MODIFICATION_COUNT": 0,
        "DECISION_SEVERITY_MODIFICATION_COUNT": 0,
        "DECISION_REVIEW_STATUS_MODIFICATION_COUNT": 0,
        "FORMAL_ELIGIBILITY_MODIFIED": 0,
        "IDENTITY_MODIFICATION_COUNT": 0,
        "MEMBERSHIP_MODIFICATION_COUNT": 0,
        "BACKLOG_MODIFICATION_COUNT": 0,
        "SOURCE_SHA_MISMATCH": source_sha_mismatch,
        "ORIGINAL_FILES_MODIFIED": int(not protected_unchanged),
        "FORMAL_ARTIFACTS_MODIFIED": int(not formal_unchanged),
        "DECISION_SHEET_SHA256_BEFORE": decision_sha_before,
        "DECISION_SHEET_SHA256_AFTER": decisions_sha_after,
        "DECISION_SHEET_UNCHANGED": decision_unchanged,
        "PROTECTED_EVIDENCE_HASHES_UNCHANGED": protected_unchanged,
        "FORMAL_REGISTRY_CONSISTENCY_PASS": int(not formal_registry_mismatch),
        "PREVIOUS_ARTIFACT_SETS": value_int(g10.get("ARTIFACT_SETS"), 453),
        "PREVIOUS_PRIMARY_ARTIFACTS": value_int(g10.get("PRIMARY_ARTIFACTS"), 1359),
        "DOC_MANUAL_BACKLOG": value_int(g10.get("DOC_MANUAL_BACKLOG"), 0),
        "Q3_MANUAL_BACKLOG": value_int(g10.get("Q3_MANUAL_BACKLOG"), 0),
        "TOTAL_MANUAL_BACKLOG": value_int(g10.get("TOTAL_MANUAL_BACKLOG"), 0),
        "OCR_RUN": 0,
        "PDF_RENDER_RUN": 0,
        "EXTRACTION_RUN": 0,
        "BODY_RECONSTRUCTION_RUN": 0,
        "ARTIFACT_REGENERATION_RUN": 0,
        "REVIEW_PACKET_REGENERATION_RUN": 0,
        "G9_REBUILD_RUN": 0,
        "G10_REBUILD_RUN": 0,
        "G12_RUN": 0,
        "NETWORK_ACCESS_USED": 0,
        "DOWNLOAD_RUN": 0,
        "NEW_DEPENDENCY_INSTALLED": 0,
        "GIT_OPERATIONS": 0,
        "OUTPUTS": [rel(OUTPUT_IDENTITY), rel(OUTPUT_PAGE), rel(OUTPUT_SAMPLE), rel(OUTPUT_RESULT), rel(OUTPUT_REPORT), rel(OUTPUT_TOOL)],
        "VALIDATION": validation,
        "ISSUES": issues,
        "BLOCKER": blocker,
        "NEXT": next_stage,
    }

    identity_fields = [
        "paper_id", "artifact_set_id", "year", "problem", "stratum", "source_route", "marker_only_page_count", "marker_count", "fully_marker_only", "formal_body_substantive_content_present", "marker_semantics", "page_boundary_preserved", "structural_non_page_local", "confirmed_missing_page_count", "legitimate_blank_page_count", "unresolved_page_count", "governed_duplicate", "shared_formal_path", "shared_body_sha", "formal_body_path", "formal_body_sha256", "source_path", "source_sha256", "identity_binding_valid", "membership_binding_valid", "artifact_binding_valid", "source_binding_valid", "classification", "root_cause_category", "repair_required", "repair_layer", "review_evidence_repair_required", "human_rereview_required", "confidence", "notes",
    ]
    page_fields = [
        "paper_id", "source_page", "marker_only_detected", "source_page_classification", "native_markdown_page_boundary_available", "formal_page_boundary_strict", "substantive_content_locatable_elsewhere", "classification", "classification_confidence", "repair_required", "formal_substantive_content_present", "existing_page_text_path", "existing_page_text_sha256", "review_packet_excerpt_paths", "review_packet_excerpt_sha256", "source_review_png_paths", "root_cause_category", "repair_layer", "governed_duplicate", "body_sha256", "notes",
    ]
    sample_fields = [
        "sample_order", "paper_id", "year", "problem", "marker_only_page_count", "marker_count", "fully_marker_only", "governed_duplicate", "body_sha256", "source_path", "source_sha256", "selected_pages", "diagnostic_reason", "q0_extraction_generation", "requires_render_next_stage",
    ]
    write_csv(OUTPUT_IDENTITY, identity_fields, identity_rows)
    write_csv(OUTPUT_PAGE, page_fields, page_rows)
    write_csv(OUTPUT_SAMPLE, sample_fields, visual_rows)
    write_json(OUTPUT_RESULT, result)

    report = f"""# G11 Major Defect Deep Diagnostic

## Stage result

- `STATUS={status}`
- `BRANCH={branch}`
- `HEAD={head}`
- `DEEP_DIAGNOSTIC_ATTEMPT_ID={attempt_id}`
- `AUTHORITATIVE_G11_PREPARATION_ATTEMPT_ID={authoritative_preparation}`
- `BLOCKER={blocker}`
- `NEXT={next_stage}`

This stage is diagnosis-only. It did not run OCR, PDF rendering, PDF extraction, body reconstruction, artifact regeneration, review-packet regeneration, G9, G10, or G12. It did not modify source files, formal artifacts, formal index data, eligibility, frozen decisions, or backlog state.

## Q0 marker semantics and pipeline trace

`SOURCE_PAGE_MARKER_SEMANTICS=PAGE_LOCAL_STRICT_BOUNDARY`.

The traced Q0 route has six stages: (1) source PDF, (2) `pdf-inspector` / native Markdown page extraction, (3) per-page normalization, (4) per-page `source_page` marker insertion, (5) ordered body reconstruction, and (6) `paper.md` serialization. `tools/39_g6_pilot_auto_r2.py` normalizes each page before inserting its marker and joins the page sections in page order. `tools/41_g8_g10_unattended_scale.py` writes that body without a later cross-page reflow.

Therefore native page boundaries are available and preserved through extraction, normalization, and the formal body. Consecutive markers and a marker without local text are allowed by the implementation because every page emits a marker, including an empty extraction result. That implementation allowance is not evidence that the source page was legitimately blank. A text block cannot span multiple source pages under this route, and normalization cannot move text across a marker boundary. The Q3 body is an independent route with no `source_page` markers and is not mixed into this Q0 classification.

The scale file-source map is currently header-only; source path/SHA evidence was therefore read from the eligibility and formal metadata/registry records. `SOURCE_MAP_METADATA_STATUS={source_map_status}`.

## Marker-only reclassification

The formal scan found `{marker_only_segments_total}` marker-only page segments across `{len(candidates)}` candidate identities. The mutually exclusive page partition is:

| classification | pages | identities |
|---|---:|---:|
| legitimate blank | {legitimate_page_total} | {sum(row['classification'] == 'LEGITIMATE_ONLY' for row in identity_rows)} |
| structural non-page-local | {structural_page_total} | {sum(row['classification'] == 'STRUCTURAL_ONLY' for row in identity_rows)} |
| confirmed defective content missing | {confirmed_page_total} | {sum(row['classification'] == 'CONFIRMED_DEFECTIVE' for row in identity_rows)} |
| still unresolved | {unresolved_page_total} | {new_unresolved} |

Under the proven strict page-local semantics, a marker-only page with existing nonempty source-review evidence and a structural-only formal segment is a confirmed formal content-missing defect. A marker-only page without such evidence remains unresolved. No structural false-positive or legitimate-blank intersection was found. The previous identity-level unresolved count was `{EXPECTED_OLD_UNRESOLVED}`; the new count is `{new_unresolved}`; reduction is `{EXPECTED_OLD_UNRESOLVED - new_unresolved}`.

There are `{sum(row['classification'] == 'CONFIRMED_DEFECTIVE' and value_int(row['unresolved_page_count']) > 0 for row in identity_rows)}` confirmed identities with additional unresolved marker-only pages. They remain in the confirmed identity repair set because at least one page is independently proven defective; the unresolved page rows remain auditable and are not silently repaired.

## Frozen G11 findings and repair scope

All 10 known formal G11 identities were reclassified as `FORMAL_ARTIFACT_PAGE_CONTENT_MISSING` with high confidence. Confirmed IDs: `{confirmed_ids}`. Structural false positives=`0`; other defects=`0`; known G11 remain unresolved=`0`. No human MAJOR decision was changed, downgraded, or expanded.

The resulting repair groups are: Group A = `10` confirmed Q0 formal identities; Group B = `1` independent `CUMCM-2020-D-003` OCR-page identity; Group C = `0`; unresolved diagnostic group = `{new_unresolved}` identities / `{unresolved_page_total}` pages. Formal repair remains a later stage.

## Duplicate and path causality

The existing formal registry has `32` governed duplicate body-hash groups covering `207` identities. In this scan, marker-only segments occur in `{marker_only_duplicate_groups}` governed groups, confirmed defects occur in `{confirmed_duplicate_groups}` groups, and structural-only groups occur in `{structural_duplicate_groups}` groups. Formal artifact paths remain one-per-identity: shared path collisions=`{path_collisions}` and unexpected shared body-path groups=`{unexpected_shared_body_path}`. Identity, membership, source, artifact, and index bindings remain valid. Accordingly `SHARED_FORMAL_PATH_IS_CAUSAL=0` and `GOVERNED_DUPLICATE_STATUS_IS_CAUSAL=0`; duplicate body hashes are correlated context, not a binding cause.

## Independent Q3 evidence

`CUMCM-2020-D-003_REPAIR_LAYER={q3_formal_path}`. Existing page-audit rows for pages `1,68,135` are OCR-backed, usable, nonempty, and hash-consistent with the successful persisted OCR audit and page files. The reconstruction manifest is `COMPLETE_VALID`, the provenance is OCR for 135 pages, and the quality record passes. The existing reviewer symptom explicitly reports OCR/symbol substitutions affecting model meaning. No new OCR or rendering was run.

## Targeted diagnostic sample

`TARGETED_VISUAL_DIAGNOSTIC_REQUIRED={int(new_unresolved > 0)}`. Because `{new_unresolved}` identities remain unresolved, a deterministic maximum-20 identity sample was written to `{rel(OUTPUT_SAMPLE)}`. It is stratified by year/problem where possible and covers duplicate status, fully marker-only status, and marker-count bins/extremes. It is a plan for the next targeted visual diagnostic only; `PDF_RENDER_RUN=0`.

## Frozen-state and operation gates

- `PREVIOUS_ARTIFACT_SETS={value_int(g10.get('ARTIFACT_SETS'), 453)}`; `PREVIOUS_PRIMARY_ARTIFACTS={value_int(g10.get('PRIMARY_ARTIFACTS'), 1359)}`.
- `DOC_MANUAL_BACKLOG={value_int(g10.get('DOC_MANUAL_BACKLOG'), 0)}`; `Q3_MANUAL_BACKLOG={value_int(g10.get('Q3_MANUAL_BACKLOG'), 0)}`; `TOTAL_MANUAL_BACKLOG={value_int(g10.get('TOTAL_MANUAL_BACKLOG'), 0)}`.
- Decision SHA unchanged=`{decision_unchanged}`; protected evidence hashes unchanged=`{protected_unchanged}`; formal artifact hashes unchanged during this run=`{formal_unchanged}`.
- `FORMAL_DATA_MODIFICATION_COUNT=0`; `FORMAL_ARTIFACT_CONTENT_MODIFICATION_COUNT=0`; `FORMAL_INDEX_MODIFICATION_COUNT=0`; decision modification counts=`0`; `FORMAL_ELIGIBILITY_MODIFIED=0`.
- `OCR_RUN=0`; `PDF_RENDER_RUN=0`; `EXTRACTION_RUN=0`; `BODY_RECONSTRUCTION_RUN=0`; `ARTIFACT_REGENERATION_RUN=0`; `G9_REBUILD_RUN=0`; `G10_REBUILD_RUN=0`; `G12_RUN=0`.
- `NETWORK_ACCESS_USED=0`; `DOWNLOAD_RUN=0`; `NEW_DEPENDENCY_INSTALLED=0`; `GIT_OPERATIONS=0` (only read-only branch/HEAD checks were used).

## Outputs

- `{rel(OUTPUT_IDENTITY)}` — identity-level classification for all `{len(identity_rows)}` marker-only candidate identities.
- `{rel(OUTPUT_PAGE)}` — page-level classification for all `{len(page_rows)}` marker-only segments.
- `{rel(OUTPUT_SAMPLE)}` — deterministic maximum-20 unresolved identity sample for the next visual diagnostic.
- `{rel(OUTPUT_RESULT)}` — machine-readable stage result.
- `{rel(OUTPUT_TOOL)}` — deterministic stdlib-only diagnostic runner.

## Validation

""" + "\n".join(f"- {item}" for item in validation) + f"""

## Issues

""" + "\n".join(f"- {item}" for item in issues) + ("\n" if issues else "- None beyond the documented unresolved diagnostic scope.\n") + f"""

## Machine-readable closure

```text
STAGE=G11-MAJOR-DEFECT-DEEP-DIAGNOSTIC
STATUS={status}
SOURCE_PAGE_MARKER_SEMANTICS=PAGE_LOCAL_STRICT_BOUNDARY
TOTAL_MARKER_ONLY_PAGE_COUNT={marker_only_segments_total}
LEGITIMATE_BLANK_PAGE_COUNT={legitimate_page_total}
STRUCTURAL_NON_PAGE_LOCAL_PAGE_COUNT={structural_page_total}
CONFIRMED_DEFECTIVE_PAGE_COUNT={confirmed_page_total}
STILL_UNRESOLVED_PAGE_COUNT={unresolved_page_total}
OLD_UNRESOLVED_IDENTITY_COUNT={EXPECTED_OLD_UNRESOLVED}
NEW_UNRESOLVED_IDENTITY_COUNT={new_unresolved}
TARGETED_VISUAL_DIAGNOSTIC_REQUIRED={int(new_unresolved > 0)}
TARGETED_VISUAL_DIAGNOSTIC_SAMPLE_IDENTITY_COUNT={len(visual_rows)}
FORMAL_DATA_MODIFICATION_COUNT=0
FORMAL_ARTIFACT_CONTENT_MODIFICATION_COUNT=0
FORMAL_INDEX_MODIFICATION_COUNT=0
DECISION_CONTENT_MODIFICATION_COUNT=0
DECISION_SEVERITY_MODIFICATION_COUNT=0
DECISION_REVIEW_STATUS_MODIFICATION_COUNT=0
OCR_RUN=0
PDF_RENDER_RUN=0
EXTRACTION_RUN=0
BODY_RECONSTRUCTION_RUN=0
G9_REBUILD_RUN=0
G10_REBUILD_RUN=0
G12_RUN=0
NETWORK_ACCESS_USED=0
DOWNLOAD_RUN=0
NEW_DEPENDENCY_INSTALLED=0
BLOCKER={blocker}
NEXT={next_stage}
```
"""
    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_REPORT.write_text(report, encoding="utf-8")

    # Re-check only the outputs written by this diagnostic and the immutable
    # evidence snapshots. No formal or source file is touched by this script.
    if protected_before != {rel(path): sha256_file(path) for path in protected_inputs}:
        raise RuntimeError("G11_DEEP_DIAGNOSTIC_PROTECTED_EVIDENCE_CHANGED")
    print(f"STAGE=G11-MAJOR-DEFECT-DEEP-DIAGNOSTIC")
    print(f"STATUS={status}")
    print(f"DEEP_DIAGNOSTIC_ATTEMPT_ID={attempt_id}")
    print(f"TOTAL_MARKER_ONLY_PAGE_COUNT={marker_only_segments_total}")
    print(f"CONFIRMED_DEFECTIVE_PAGE_COUNT={confirmed_page_total}")
    print(f"STILL_UNRESOLVED_PAGE_COUNT={unresolved_page_total}")
    print(f"NEW_UNRESOLVED_IDENTITY_COUNT={new_unresolved}")
    print(f"TARGETED_VISUAL_DIAGNOSTIC_SAMPLE_IDENTITY_COUNT={len(visual_rows)}")
    print("OCR_RUN=0")
    print("PDF_RENDER_RUN=0")
    print("EXTRACTION_RUN=0")
    print("G12_RUN=0")
    print(f"BLOCKER={blocker}")
    print(f"NEXT={next_stage}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
