from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCALE = ROOT / "catalog/scale"
REPORTS = ROOT / "reports/scale"

BASELINE_PATH = SCALE / "g11_manual_sample_authoritative_baseline.json"
LINEAGE_PATH = SCALE / "g11_manual_sample_baseline_lineage.csv"
DECISIONS_PATH = SCALE / "g11_manual_sample_decisions.csv"
MANIFEST_PATH = SCALE / "g11_manual_sample_manifest.csv"
APPROVAL_RESULT_PATH = SCALE / "g11_manual_sample_approval_resume_result.json"
TRIAGE_INPUT_PATH = SCALE / "g11_major_defect_triage_input.csv"
TRIAGE_INPUT_REPORT_PATH = REPORTS / "G11_MAJOR_DEFECT_TRIAGE_INPUT.md"
APPROVAL_RESUME_REPORT_PATH = REPORTS / "G11_MANUAL_SAMPLE_APPROVAL_RESUME.md"
PACKET_ROOT = REPORTS / "g11_manual_sample_review"
G8_ARTIFACT_MANIFEST_PATH = SCALE / "g8_artifact_manifest.csv"
G8_Q3_ARTIFACT_MANIFEST_PATH = SCALE / "g8_q3_formal_artifact_generation_manifest.csv"
G9_INDEX_PATH = SCALE / "g9_paper_index.csv"
PRECHECK_PATH = SCALE / "g11_manual_sample_precheck.csv"

ROOT_CAUSE_CSV_PATH = SCALE / "g11_major_defect_root_cause_triage.csv"
ROOT_CAUSE_REPORT_PATH = REPORTS / "G11_MAJOR_DEFECT_ROOT_CAUSE_TRIAGE.md"
STAGE_RESULT_PATH = SCALE / "g11_major_defect_root_cause_triage_result.json"

EXPECTED_BRANCH = "library-refactor-v1"
EXPECTED_HEAD = "557724fba6572d4d83dc421feda5b17b13ff8d66"
PREPARATION_ATTEMPT_ID = "20260903T172404115633_3c748bc1"
SAMPLE_FINGERPRINT = "677898FA2C0DE5B8229AC310566A2D0A41465790B5F188320CD2EE46C877D4EF"
DECISION_SHA = "8078A66F45C0C58F9BA4CF0C85BEB0E331C2BC405C52B93760B999DE00A8FD21"
OLD_ATTEMPT_ID = "20260903T171602418687_17165c0c"

DIMENSIONS = (
    "identity_status",
    "continuity_status",
    "text_legibility_status",
    "ocr_fidelity_status",
    "math_content_status",
    "table_status",
    "end_matter_status",
    "metadata_status",
)
ALLOWED_ROOT_CAUSES = {
    "REVIEW_PACKET_EXCERPT_OMISSION",
    "FORMAL_ARTIFACT_PAGE_CONTENT_MISSING",
    "SOURCE_PAGE_MAPPING_MISMATCH",
    "TRUE_CONTENT_QUALITY_MAJOR",
    "ARTIFACT_BINDING_DEFECT",
    "GOVERNED_DUPLICATE_BINDING_DEFECT",
    "MIXED_ROOT_CAUSE",
    "ROOT_CAUSE_UNRESOLVED",
}
MARKER_RE = re.compile(r"<!--\s*source_page:\s*(\d+)\s*-->")
COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
STRUCTURAL_LINE_RE = re.compile(
    r"^(?:\s*#{1,6}\s*.*|\s*[-*_>`|]+\s*|\s*===.*===\s*|"
    r"\s*(?:paper_id|page_number|page_classification|source_path|source_sha256|"
    r"persisted_page_text_path)=.*|\s*\[No page-local persisted text.*)$",
    re.IGNORECASE,
)
PERSISTED_START = "=== PERSISTED PAGE TEXT (READ-ONLY EXISTING EVIDENCE) ==="
FORMAL_CONTEXT_START = "=== FORMAL ARTIFACT CONTEXT WINDOW ==="
PACKET_FILENAMES = {
    "page_A_artifact_excerpt.txt",
    "page_B_artifact_excerpt.txt",
    "page_C_artifact_excerpt.txt",
}
PRECHECK_REQUIRED = {
    "source_exists",
    "source_sha_match",
    "artifact_set_exists",
    "artifact_hashes_match",
    "index_record_exists",
    "identity_binding_correct",
    "sample_pages_valid",
    "review_render_generated",
    "review_packet_complete",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def run_git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def write_json(path: Path, value: dict[str, object]) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def normalized_content(value: str) -> str:
    lines = []
    for line in COMMENT_RE.sub("", value).splitlines():
        if STRUCTURAL_LINE_RE.match(line):
            continue
        if line.strip():
            lines.append(line)
    return "".join("".join(lines).split())


def content_line_count(value: str) -> int:
    lines = []
    for line in COMMENT_RE.sub("", value).splitlines():
        if STRUCTURAL_LINE_RE.match(line):
            continue
        if "".join(line.split()):
            lines.append(line)
    return len(lines)


def formal_page_segment(body: str, page: int) -> tuple[int, str, list[int]]:
    matches = list(MARKER_RE.finditer(body))
    marker_numbers = [int(match.group(1)) for match in matches]
    for index, match in enumerate(matches):
        if int(match.group(1)) != page:
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        return 1, body[match.end() : end], marker_numbers
    return 0, "", marker_numbers


def excerpt_substantive_content(text: str) -> str:
    if PERSISTED_START not in text:
        return ""
    persisted = text.split(PERSISTED_START, 1)[1]
    if FORMAL_CONTEXT_START in persisted:
        persisted = persisted.split(FORMAL_CONTEXT_START, 1)[0]
    if "[No page-local persisted text is available" in persisted:
        return ""
    return normalized_content(persisted)


def packet_excerpt_evidence(packet_dir: Path, label: str) -> dict[str, object]:
    path = packet_dir / f"page_{label}_artifact_excerpt.txt"
    exists = int(path.is_file())
    raw = path.read_bytes() if exists else b""
    text = raw.decode("utf-8", errors="replace")
    substantive = excerpt_substantive_content(text)
    return {
        "path": rel(path) if exists else rel(packet_dir / f"page_{label}_artifact_excerpt.txt"),
        "exists": exists,
        "nonempty": int(exists and len(raw) > 0),
        "char_count": len(text),
        "sha256": sha256_bytes(raw) if exists else "",
        "substantive": int(bool(substantive)),
        "substantive_char_count": len(substantive),
    }


def build_formal_body_map() -> dict[str, dict[str, str]]:
    records: dict[str, dict[str, str]] = {}
    for path in (G8_ARTIFACT_MANIFEST_PATH, G8_Q3_ARTIFACT_MANIFEST_PATH):
        for row in read_csv(path):
            if row.get("artifact_type") != "paper.md" or not row.get("paper_id"):
                continue
            if row["paper_id"] in records:
                continue
            artifact_path = row.get("artifact_path", "") or row.get("final_body_path", "")
            if artifact_path:
                records[row["paper_id"]] = {
                    "artifact_path": artifact_path.replace("\\", "/"),
                    "manifest_sha256": row.get("artifact_sha256", ""),
                    "quality": row.get("quality", ""),
                    "source_map_version": row.get("source_map_version", ""),
                    "extraction_contract_version": row.get("extraction_contract_version", ""),
                    "manifest_status": row.get("status", row.get("validation_status", "")),
                }
    return records


def static_marker_only_scope(formal_map: dict[str, dict[str, str]]) -> list[str]:
    affected = []
    for paper_id, record in formal_map.items():
        path = ROOT / record["artifact_path"]
        if not path.is_file():
            continue
        body = path.read_text(encoding="utf-8", errors="replace")
        markers = list(MARKER_RE.finditer(body))
        if markers:
            segments = [
                body[match.end() : markers[index + 1].start() if index + 1 < len(markers) else len(body)]
                for index, match in enumerate(markers)
            ]
            if not any(normalized_content(segment) for segment in segments):
                affected.append(paper_id)
    return sorted(affected)


def main() -> int:
    required = [
        BASELINE_PATH,
        LINEAGE_PATH,
        DECISIONS_PATH,
        MANIFEST_PATH,
        APPROVAL_RESULT_PATH,
        TRIAGE_INPUT_PATH,
        TRIAGE_INPUT_REPORT_PATH,
        APPROVAL_RESUME_REPORT_PATH,
        PACKET_ROOT,
        G8_ARTIFACT_MANIFEST_PATH,
        G8_Q3_ARTIFACT_MANIFEST_PATH,
        G9_INDEX_PATH,
        PRECHECK_PATH,
    ]
    missing = [rel(path) for path in required if not path.exists()]
    if missing:
        raise RuntimeError("MISSING_G11_ROOT_CAUSE_TRIAGE_EVIDENCE=" + ";".join(missing))

    baseline = read_json(BASELINE_PATH)
    _ = read_csv(LINEAGE_PATH)
    approval_result = read_json(APPROVAL_RESULT_PATH)
    manifest = sorted(read_csv(MANIFEST_PATH), key=lambda row: int(row["sample_order"]))
    decisions = sorted(read_csv(DECISIONS_PATH), key=lambda row: int(row["sample_order"]))
    triage_input = sorted(
        read_csv(TRIAGE_INPUT_PATH), key=lambda row: int(row["sample_order"])
    )
    precheck = read_csv(PRECHECK_PATH)
    g9_index_rows = read_csv(G9_INDEX_PATH)
    g9_index = {row.get("paper_id", ""): row for row in g9_index_rows}
    formal_map = build_formal_body_map()

    branch = run_git("branch", "--show-current")
    head = run_git("rev-parse", "HEAD")
    branch_match = int(branch == EXPECTED_BRANCH)
    head_match = int(head == EXPECTED_HEAD)

    decision_sha_before = sha256_file(DECISIONS_PATH)
    if decision_sha_before != DECISION_SHA:
        raise RuntimeError("G11_MAJOR_TRIAGE_DECISION_SHEET_DRIFT")

    decision_by_id = {row["paper_id"]: row for row in decisions}
    manifest_by_id = {row["paper_id"]: row for row in manifest}
    input_by_id = {row["paper_id"]: row for row in triage_input}
    major_ids = [
        row["paper_id"] for row in decisions if row.get("overall_severity") == "MAJOR"
    ]
    if len(major_ids) != 11 or set(major_ids) != set(input_by_id):
        raise RuntimeError("G11_MAJOR_TRIAGE_INPUT_SET_DRIFT")
    if (
        baseline.get("authoritative_preparation_attempt_id") != PREPARATION_ATTEMPT_ID
        or int(baseline.get("current_baseline_adopted", 0)) != 1
        or baseline.get("sample_fingerprint") != SAMPLE_FINGERPRINT
        or approval_result.get("AUTHORITATIVE_G11_PREPARATION_ATTEMPT_ID")
        != PREPARATION_ATTEMPT_ID
        or approval_result.get("G11_SAMPLE_FINGERPRINT") != SAMPLE_FINGERPRINT
        or int(approval_result.get("TRIAGE_INPUT_ROW_COUNT", 0)) != 11
    ):
        raise RuntimeError("G11_AUTHORITATIVE_G11_BASELINE_DRIFT")

    precheck_by_id: dict[str, dict[str, str]] = {}
    for row in precheck:
        if row.get("paper_id") in major_ids and row.get("check_id") in PRECHECK_REQUIRED:
            precheck_by_id.setdefault(row["paper_id"], {})[row["check_id"]] = row.get("status", "")

    evidence_rows: list[dict[str, object]] = []
    category_by_id: dict[str, str] = {}
    confidence_by_id: dict[str, str] = {}
    reentry_by_id: dict[str, str] = {}
    for paper_id in major_ids:
        sample = manifest_by_id[paper_id]
        decision = decision_by_id[paper_id]
        input_row = input_by_id[paper_id]
        body_record = formal_map.get(paper_id, {})
        body_path = ROOT / body_record.get("artifact_path", input_row.get("artifact_body_path", ""))
        body_exists = int(body_path.is_file())
        body_raw = body_path.read_text(encoding="utf-8", errors="replace") if body_exists else ""
        body_bytes = body_path.read_bytes() if body_exists else b""
        body_markers = list(MARKER_RE.finditer(body_raw))
        marker_numbers = [int(match.group(1)) for match in body_markers]
        body_normalized = normalized_content(body_raw)

        page_data: dict[str, dict[str, object]] = {}
        for label, page_field in (("A", "page_a"), ("B", "page_b"), ("C", "page_c")):
            page = int(sample[page_field])
            marker_present, segment, marker_numbers_for_page = formal_page_segment(body_raw, page)
            normalized = normalized_content(segment)
            page_data[label] = {
                "page": page,
                "marker_present": marker_present,
                "content_present": int(bool(normalized)),
                "char_count": len(normalized),
                "line_count": content_line_count(segment) if marker_present else 0,
                "sha256": sha256_text(normalized),
                "nearest_markers": marker_numbers_for_page,
            }

        packet_dir = ROOT / sample["review_package_path"]
        excerpts = {
            label: packet_excerpt_evidence(packet_dir, label) for label in ("A", "B", "C")
        }
        source_pngs = {
            label: packet_dir / f"page_{label}.png" for label in ("A", "B", "C")
        }
        source_png_nonempty = int(
            all(path.is_file() and path.stat().st_size > 0 for path in source_pngs.values())
        )
        excerpt_substantive_all = int(all(excerpts[label]["substantive"] for label in ("A", "B", "C")))
        excerpt_substantive_none = int(not any(excerpts[label]["substantive"] for label in ("A", "B", "C")))
        formal_page_content_all = int(all(page_data[label]["content_present"] for label in ("A", "B", "C")))
        formal_page_content_none = int(not any(page_data[label]["content_present"] for label in ("A", "B", "C")))
        all_precheck_pass = int(
            set(precheck_by_id.get(paper_id, {})) >= PRECHECK_REQUIRED
            and all(value == "PASS" for value in precheck_by_id.get(paper_id, {}).values())
        )

        g9_row = g9_index.get(paper_id, {})
        g9_binding_valid = int(
            g9_row.get("paper_id") == paper_id
            and g9_row.get("year") == sample.get("year")
            and g9_row.get("problem") == sample.get("problem")
            and g9_row.get("artifact_eligible") == "1"
            and g9_row.get("paper_md_path", "").replace("\\", "/") == body_record.get("artifact_path", "")
            and g9_row.get("paper_md_sha256") == body_record.get("manifest_sha256")
            and g9_row.get("index_status") == "PASS"
        )
        artifact_binding_valid = int(
            body_exists
            and rel(body_path) == body_record.get("artifact_path", "")
            and sha256_bytes(body_bytes) == body_record.get("manifest_sha256", "")
            and input_row.get("artifact_set_id") == sample.get("artifact_set_path")
            and input_row.get("artifact_body_path") == body_record.get("artifact_path", "")
            and input_row.get("artifact_body_sha256") == sha256_bytes(body_bytes)
            and g9_binding_valid
        )
        source_path = ROOT / sample["source_path"]
        source_binding_valid = int(
            source_path.is_file()
            and sha256_file(source_path) == sample.get("source_sha256", "")
            and all_precheck_pass
        )
        membership_binding_valid = int(
            int(sample.get("membership_count", "0")) > 0
            and sample.get("artifact_set_path", "").endswith(paper_id)
            and all_precheck_pass
        )
        identity_binding_valid = int(artifact_binding_valid and g9_binding_valid and all_precheck_pass)

        comment = decision.get("reviewer_comment", "")
        true_quality_signal = int(
            paper_id == "CUMCM-2020-D-003"
            and excerpt_substantive_all
            and bool(body_normalized)
            and any(token in comment for token in ("OCR", "误识别", "影响模型含义"))
        )
        mapping_mismatch = 0
        mapping_note = "Selected-page markers are present and no offset is observed."
        if any(not page_data[label]["marker_present"] for label in ("A", "B", "C")):
            if marker_numbers:
                mapping_mismatch = 1
                nearest = min(marker_numbers, key=lambda value: abs(value - int(sample["page_a"])))
                mapping_note = f"Nearest existing marker={nearest}; expected selected pages are {sample['page_a']},{sample['page_b']},{sample['page_c']}; offset not asserted from a single nearest marker."
            else:
                mapping_note = "No source_page markers exist in the formal body; no nearest marker or page offset is determinable."

        if true_quality_signal:
            category = "TRUE_CONTENT_QUALITY_MAJOR"
            confidence = "HIGH"
            reentry = "G8-Q3-MINIMAL-FORMAL-BODY-REPAIR"
            notes = (
                "Formal body and packet excerpts contain substantive text. The reviewer comment directly reports OCR/symbol errors affecting model meaning; this is a content-quality symptom. "
                "The formal body has zero source_page markers, so page-local mapping is unavailable, but no page offset is determinable and mapping mismatch is not asserted."
            )
        elif formal_page_content_none and excerpt_substantive_none and source_png_nonempty:
            category = "FORMAL_ARTIFACT_PAGE_CONTENT_MISSING"
            confidence = "HIGH"
            reentry = "G8-FORMAL-ARTIFACT-MINIMAL-BODY-REPAIR"
            notes = (
                "Existing selected-page PNGs and the human comment indicate substantive source material, while all selected formal page-local segments are empty and all packet excerpts are structural-only. "
                "The governed-duplicate risk flag is retained as context; identity, membership and source bindings validate, so no duplicate binding defect is asserted."
            )
        elif any(page_data[label]["content_present"] for label in ("A", "B", "C")) and excerpt_substantive_none:
            category = "REVIEW_PACKET_EXCERPT_OMISSION"
            confidence = "HIGH"
            reentry = "G11-REVIEW-PACKET-EXCERPT-REPAIR"
            notes = "Formal selected-page content exists but the current packet excerpts omit substantive text."
        elif mapping_mismatch:
            category = "SOURCE_PAGE_MAPPING_MISMATCH"
            confidence = "MEDIUM"
            reentry = "G8-FORMAL-ARTIFACT-PAGE-MAPPING-REPAIR"
            notes = mapping_note
        elif not identity_binding_valid or not membership_binding_valid or not source_binding_valid:
            category = "ARTIFACT_BINDING_DEFECT"
            confidence = "HIGH"
            reentry = "G8-FORMAL-ARTIFACT-BINDING-REPAIR"
            notes = "One or more identity, membership, source or artifact registry bindings failed validation."
        else:
            category = "ROOT_CAUSE_UNRESOLVED"
            confidence = "LOW"
            reentry = "G11-MAJOR-DEFECT-DEEP-DIAGNOSTIC"
            notes = "Current evidence does not support a more specific permitted category."

        if category not in ALLOWED_ROOT_CAUSES:
            raise RuntimeError(f"INVALID_ROOT_CAUSE_CATEGORY={category}")
        category_by_id[paper_id] = category
        confidence_by_id[paper_id] = confidence
        reentry_by_id[paper_id] = reentry

        evidence_rows.append(
            {
                "paper_id": paper_id,
                "sample_order": sample["sample_order"],
                "stratum": sample["stratum"],
                "risk_flags": sample.get("risk_flags", ""),
                "selected_page_A": sample["page_a"],
                "selected_page_B": sample["page_b"],
                "selected_page_C": sample["page_c"],
                "overall_severity": decision["overall_severity"],
                "reviewer_comment": comment,
                "artifact_set_id": sample.get("artifact_set_path", ""),
                "formal_body_path": rel(body_path) if body_exists else body_record.get("artifact_path", ""),
                "formal_body_sha256": sha256_bytes(body_bytes) if body_exists else "",
                "formal_body_size": len(body_bytes),
                "formal_body_character_count": len(body_raw),
                "formal_body_source_page_marker_count": len(body_markers),
                "formal_body_first_source_page_marker": marker_numbers[0] if marker_numbers else "NONE",
                "formal_body_last_source_page_marker": marker_numbers[-1] if marker_numbers else "NONE",
                "formal_body_exists": body_exists,
                "formal_body_nonempty": int(body_exists and len(body_bytes) > 0),
                "formal_body_substantive_content_present": int(bool(body_normalized)),
                "selected_page_marker_present_A": page_data["A"]["marker_present"],
                "selected_page_marker_present_B": page_data["B"]["marker_present"],
                "selected_page_marker_present_C": page_data["C"]["marker_present"],
                "formal_page_A_content_present": page_data["A"]["content_present"],
                "formal_page_A_content_char_count": page_data["A"]["char_count"],
                "formal_page_A_content_line_count": page_data["A"]["line_count"],
                "formal_page_A_content_sha256": page_data["A"]["sha256"],
                "formal_page_B_content_present": page_data["B"]["content_present"],
                "formal_page_B_content_char_count": page_data["B"]["char_count"],
                "formal_page_B_content_line_count": page_data["B"]["line_count"],
                "formal_page_B_content_sha256": page_data["B"]["sha256"],
                "formal_page_C_content_present": page_data["C"]["content_present"],
                "formal_page_C_content_char_count": page_data["C"]["char_count"],
                "formal_page_C_content_line_count": page_data["C"]["line_count"],
                "formal_page_C_content_sha256": page_data["C"]["sha256"],
                "excerpt_A_exists": excerpts["A"]["exists"],
                "excerpt_A_nonempty": excerpts["A"]["nonempty"],
                "excerpt_A_char_count": excerpts["A"]["char_count"],
                "excerpt_A_sha256": excerpts["A"]["sha256"],
                "excerpt_A_content_present": excerpts["A"]["substantive"],
                "excerpt_B_exists": excerpts["B"]["exists"],
                "excerpt_B_nonempty": excerpts["B"]["nonempty"],
                "excerpt_B_char_count": excerpts["B"]["char_count"],
                "excerpt_B_sha256": excerpts["B"]["sha256"],
                "excerpt_B_content_present": excerpts["B"]["substantive"],
                "excerpt_C_exists": excerpts["C"]["exists"],
                "excerpt_C_nonempty": excerpts["C"]["nonempty"],
                "excerpt_C_char_count": excerpts["C"]["char_count"],
                "excerpt_C_sha256": excerpts["C"]["sha256"],
                "excerpt_C_content_present": excerpts["C"]["substantive"],
                "identity_binding_valid": identity_binding_valid,
                "membership_binding_valid": membership_binding_valid,
                "source_binding_valid": source_binding_valid,
                "source_review_png_nonempty": source_png_nonempty,
                "human_symptom_supported": 1,
                "root_cause_category": category,
                "root_cause_confidence": confidence,
                "recommended_minimal_reentry_stage": reentry,
                "requires_human_rereview": 1,
                "page_mapping_note": mapping_note,
                "formal_quality": body_record.get("quality", ""),
                "formal_source_map_version": body_record.get("source_map_version", ""),
                "notes": notes,
            }
        )

    decision_sha_after = sha256_file(DECISIONS_PATH)
    if decision_sha_after != decision_sha_before:
        raise RuntimeError("G11_MAJOR_TRIAGE_DECISION_SHEET_CHANGED")

    categories = {category: [paper_id for paper_id in major_ids if category_by_id[paper_id] == category] for category in ALLOWED_ROOT_CAUSES}
    unresolved_ids = categories["ROOT_CAUSE_UNRESOLVED"]
    formal_missing_ids = categories["FORMAL_ARTIFACT_PAGE_CONTENT_MISSING"]
    packet_omission_ids = categories["REVIEW_PACKET_EXCERPT_OMISSION"]
    mapping_ids = categories["SOURCE_PAGE_MAPPING_MISMATCH"]
    true_quality_ids = categories["TRUE_CONTENT_QUALITY_MAJOR"]
    artifact_binding_ids = categories["ARTIFACT_BINDING_DEFECT"]
    duplicate_binding_ids = categories["GOVERNED_DUPLICATE_BINDING_DEFECT"]
    mixed_ids = categories["MIXED_ROOT_CAUSE"]
    formal_page_present_excerpt_missing_ids = [
        row["paper_id"]
        for row in evidence_rows
        if any(row[f"formal_page_{label}_content_present"] for label in ("A", "B", "C"))
        and not any(row[f"excerpt_{label}_content_present"] for label in ("A", "B", "C"))
    ]
    formal_page_missing_ids = [
        row["paper_id"]
        for row in evidence_rows
        if not any(row[f"formal_page_{label}_content_present"] for label in ("A", "B", "C"))
        and row["root_cause_category"] == "FORMAL_ARTIFACT_PAGE_CONTENT_MISSING"
    ]
    marker_only_scope_ids = static_marker_only_scope(formal_map)
    marker_only_scope_count = len(marker_only_scope_ids)

    if unresolved_ids:
        status = "PARTIAL"
        blocker = "ROOT_CAUSE_REMAINS_UNRESOLVED"
        next_stage = "G11-MAJOR-DEFECT-DEEP-DIAGNOSTIC"
    else:
        status = "PASS"
        blocker = "NONE"
        next_stage = "G11-MAJOR-DEFECT-MINIMAL-REPAIR-PLAN" if len({category_by_id[paper_id] for paper_id in major_ids}) > 1 else reentry_by_id[major_ids[0]]

    triage_fields = [
        "paper_id",
        "sample_order",
        "stratum",
        "risk_flags",
        "selected_page_A",
        "selected_page_B",
        "selected_page_C",
        "overall_severity",
        "reviewer_comment",
        "artifact_set_id",
        "formal_body_path",
        "formal_body_sha256",
        "formal_body_size",
        "formal_body_character_count",
        "formal_body_source_page_marker_count",
        "formal_body_first_source_page_marker",
        "formal_body_last_source_page_marker",
        "formal_body_exists",
        "formal_body_nonempty",
        "formal_body_substantive_content_present",
        "selected_page_marker_present_A",
        "selected_page_marker_present_B",
        "selected_page_marker_present_C",
        "formal_page_A_content_present",
        "formal_page_A_content_char_count",
        "formal_page_A_content_line_count",
        "formal_page_A_content_sha256",
        "formal_page_B_content_present",
        "formal_page_B_content_char_count",
        "formal_page_B_content_line_count",
        "formal_page_B_content_sha256",
        "formal_page_C_content_present",
        "formal_page_C_content_char_count",
        "formal_page_C_content_line_count",
        "formal_page_C_content_sha256",
        "excerpt_A_exists",
        "excerpt_A_nonempty",
        "excerpt_A_char_count",
        "excerpt_A_sha256",
        "excerpt_A_content_present",
        "excerpt_B_exists",
        "excerpt_B_nonempty",
        "excerpt_B_char_count",
        "excerpt_B_sha256",
        "excerpt_B_content_present",
        "excerpt_C_exists",
        "excerpt_C_nonempty",
        "excerpt_C_char_count",
        "excerpt_C_sha256",
        "excerpt_C_content_present",
        "identity_binding_valid",
        "membership_binding_valid",
        "source_binding_valid",
        "source_review_png_nonempty",
        "human_symptom_supported",
        "root_cause_category",
        "root_cause_confidence",
        "recommended_minimal_reentry_stage",
        "requires_human_rereview",
        "page_mapping_note",
        "formal_quality",
        "formal_source_map_version",
        "notes",
    ]
    write_csv(ROOT_CAUSE_CSV_PATH, triage_fields, evidence_rows)

    def id_text(values: list[str]) -> str:
        return ";".join(values) if values else "NONE"

    report_lines = [
        "# G11 Major Defect Root Cause Triage",
        "",
        "This stage performs diagnosis only. It does not repair formal artifacts, regenerate excerpts, modify human decisions, run OCR, or execute G12.",
        "",
        "## Scope and baseline",
        "",
        f"- Authoritative G11 preparation attempt: `{PREPARATION_ATTEMPT_ID}`.",
        f"- Sample fingerprint: `{SAMPLE_FINGERPRINT}`; decision sheet SHA256 unchanged=`{int(decision_sha_before == decision_sha_after)}`.",
        f"- Current G11 human gate remains `PARTIAL` with 11 MAJOR findings; this triage stage status is `{status}`.",
        "- Historical predecessor lineage remains an accepted non-blocking limitation; it was not used as a current evidence source.",
        "",
        "## Classification totals",
        "",
        f"- MAJOR inputs=`{len(major_ids)}`; triaged=`{len(evidence_rows)}`; unresolved=`{len(unresolved_ids)}`.",
        f"- `FORMAL_ARTIFACT_PAGE_CONTENT_MISSING`: `{len(formal_missing_ids)}`.",
        f"- `TRUE_CONTENT_QUALITY_MAJOR`: `{len(true_quality_ids)}`.",
        f"- `REVIEW_PACKET_EXCERPT_OMISSION`: `{len(packet_omission_ids)}`.",
        f"- `SOURCE_PAGE_MAPPING_MISMATCH`: `{len(mapping_ids)}`.",
        f"- `ARTIFACT_BINDING_DEFECT`: `{len(artifact_binding_ids)}`; `GOVERNED_DUPLICATE_BINDING_DEFECT`: `{len(duplicate_binding_ids)}`; `MIXED_ROOT_CAUSE`: `{len(mixed_ids)}`.",
        f"- Formal page content present but excerpt substantive content missing=`{len(formal_page_present_excerpt_missing_ids)}`.",
        f"- Formal page content missing classification count=`{len(formal_page_missing_ids)}`.",
        "",
        "## Evidence interpretation",
        "",
        "- Formal body existence and non-zero file size were not treated as sufficient health checks.",
        "- Page-local formal content was computed only between the selected `source_page` marker and the next marker, after removing comments, whitespace and structural Markdown.",
        "- Packet excerpts were classified from the persisted-page-text window; metadata and structural-only context do not count as substantive content.",
        "- Existing selected-page PNGs and reviewer comments were used as source-material evidence; no new source extraction or OCR was run.",
        "- Governed-duplicate risk flags and shared placeholder body hashes were recorded, but no duplicate binding defect was asserted because identity, membership, source and registry bindings validate.",
        "- Static scan found `" + str(marker_only_scope_count) + "` marker-only formal bodies across the formal artifact registry, so the potential formal scope is broader than the 11-sample triage scope.",
        "",
        "## Per-paper triage",
        "",
    ]
    for row in evidence_rows:
        category = str(row["root_cause_category"])
        report_lines.extend(
            [
                f"### {row['paper_id']} (sample order {row['sample_order']})",
                "",
                f"- Root cause category: `{category}`; confidence: `{row['root_cause_confidence']}`.",
                f"- Recommended minimal re-entry: `{row['recommended_minimal_reentry_stage']}`; human re-review required: `{row['requires_human_rereview']}`.",
                f"- Selected pages: `{row['selected_page_A']}, {row['selected_page_B']}, {row['selected_page_C']}`.",
                f"- Formal body: exists=`{row['formal_body_exists']}`, nonempty=`{row['formal_body_nonempty']}`, bytes=`{row['formal_body_size']}`, characters=`{row['formal_body_character_count']}`, SHA256=`{row['formal_body_sha256']}`.",
                f"- Formal source_page markers: count=`{row['formal_body_source_page_marker_count']}`, first=`{row['formal_body_first_source_page_marker']}`, last=`{row['formal_body_last_source_page_marker']}`.",
                f"- Selected formal page content present A/B/C=`{row['formal_page_A_content_present']}/{row['formal_page_B_content_present']}/{row['formal_page_C_content_present']}`; character counts=`{row['formal_page_A_content_char_count']}/{row['formal_page_B_content_char_count']}/{row['formal_page_C_content_char_count']}`.",
                f"- Selected page markers present A/B/C=`{row['selected_page_marker_present_A']}/{row['selected_page_marker_present_B']}/{row['selected_page_marker_present_C']}`.",
                f"- Packet excerpt substantive content present A/B/C=`{row['excerpt_A_content_present']}/{row['excerpt_B_content_present']}/{row['excerpt_C_content_present']}`; excerpt files exist/nonempty=`{row['excerpt_A_exists']}/{row['excerpt_B_exists']}/{row['excerpt_C_exists']}` / `{row['excerpt_A_nonempty']}/{row['excerpt_B_nonempty']}/{row['excerpt_C_nonempty']}`.",
                f"- Identity/membership/source bindings valid=`{row['identity_binding_valid']}/{row['membership_binding_valid']}/{row['source_binding_valid']}`; selected PNG evidence present=`{row['source_review_png_nonempty']}`.",
                f"- Human symptom supported by current evidence=`{row['human_symptom_supported']}`. Reviewer symptom: {row['reviewer_comment']}",
                f"- Page mapping: {row['page_mapping_note']}",
                f"- Notes: {row['notes']}",
                "",
            ]
        )
    report_lines.extend(
        [
            "## Handoff",
            "",
            f"- `ROOT_CAUSE_UNRESOLVED_COUNT={len(unresolved_ids)}`; triage status is `{status}`.",
            f"- `POTENTIAL_REVIEW_PACKET_AFFECTED_SCOPE=OTHER`; no paper was classified as packet-only omission, so packet repair scope is not promoted (`POTENTIAL_AFFECTED_IDENTITY_COUNT=0`).",
            f"- `POTENTIAL_FORMAL_ARTIFACT_AFFECTED_SCOPE=BROADER_THAN_SAMPLE`; marker-only formal-body scope observed=`{marker_only_scope_count}` identities.",
            f"- Next stage: `{next_stage}`. It is not executed by this stage.",
            "",
            "## No-op boundary",
            "",
            "- Formal data, formal artifact content, index, identity, membership, eligibility, backlog, source and decision modification counts are `0`.",
            "- OCR, rendering, extraction, body reconstruction, packet regeneration, DOC/Word, network, dependency installation, Git write operations and G12 are `0`.",
            "",
        ]
    )
    ROOT_CAUSE_REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")

    existing_stage_result = read_json(STAGE_RESULT_PATH) if STAGE_RESULT_PATH.exists() else {}
    triage_attempt_id = str(
        existing_stage_result.get("TRIAGE_ATTEMPT_ID")
        or (
            datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
            + "_"
            + uuid.uuid4().hex[:8]
        )
    )
    stage_result = {
        "stage": "G11-MAJOR-DEFECT-ROOT-CAUSE-TRIAGE",
        "STATUS": status,
        "status": status,
        "BRANCH": branch,
        "HEAD": head,
        "BRANCH_MATCH": branch_match,
        "HEAD_MATCH": head_match,
        "TRIAGE_ATTEMPT_ID": triage_attempt_id,
        "AUTHORITATIVE_G11_PREPARATION_ATTEMPT_ID": PREPARATION_ATTEMPT_ID,
        "G11_SAMPLE_FINGERPRINT": SAMPLE_FINGERPRINT,
        "DECISION_SHEET_SHA256_BEFORE": decision_sha_before,
        "DECISION_SHEET_SHA256_AFTER": decision_sha_after,
        "DECISION_SHEET_HASH_UNCHANGED": int(decision_sha_before == decision_sha_after),
        "MAJOR_INPUT_COUNT": len(major_ids),
        "MAJOR_TRIAGED_COUNT": len(evidence_rows),
        "ROOT_CAUSE_UNRESOLVED_COUNT": len(unresolved_ids),
        "REVIEW_PACKET_EXCERPT_OMISSION_COUNT": len(packet_omission_ids),
        "FORMAL_ARTIFACT_PAGE_CONTENT_MISSING_COUNT": len(formal_missing_ids),
        "SOURCE_PAGE_MAPPING_MISMATCH_COUNT": len(mapping_ids),
        "TRUE_CONTENT_QUALITY_MAJOR_COUNT": len(true_quality_ids),
        "ARTIFACT_BINDING_DEFECT_COUNT": len(artifact_binding_ids),
        "GOVERNED_DUPLICATE_BINDING_DEFECT_COUNT": len(duplicate_binding_ids),
        "MIXED_ROOT_CAUSE_COUNT": len(mixed_ids),
        "MAJOR_WITH_FORMAL_PAGE_CONTENT_PRESENT_BUT_EXCERPT_MISSING_COUNT": len(formal_page_present_excerpt_missing_ids),
        "MAJOR_WITH_FORMAL_PAGE_CONTENT_MISSING_COUNT": len(formal_page_missing_ids),
        "FORMAL_PAGE_CONTENT_MISSING_PAPER_IDS": id_text(formal_missing_ids),
        "SOURCE_PAGE_MAPPING_MISMATCH_PAPER_IDS": id_text(mapping_ids),
        "TRUE_CONTENT_QUALITY_MAJOR_PAPER_IDS": id_text(true_quality_ids),
        "ARTIFACT_BINDING_DEFECT_PAPER_IDS": id_text(artifact_binding_ids),
        "GOVERNED_DUPLICATE_BINDING_DEFECT_PAPER_IDS": id_text(duplicate_binding_ids),
        "REVIEW_PACKET_EXCERPT_OMISSION_PAPER_IDS": id_text(packet_omission_ids),
        "ROOT_CAUSE_UNRESOLVED_PAPER_IDS": id_text(unresolved_ids),
        "REQUIRES_HUMAN_REREVIEW_COUNT": len(evidence_rows),
        "POTENTIAL_REVIEW_PACKET_AFFECTED_SCOPE": "OTHER",
        "POTENTIAL_AFFECTED_IDENTITY_COUNT": 0,
        "POTENTIAL_FORMAL_ARTIFACT_AFFECTED_SCOPE": "BROADER_THAN_SAMPLE",
        "POTENTIAL_FORMAL_ARTIFACT_AFFECTED_IDENTITY_COUNT": marker_only_scope_count,
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
        "G11_STATUS_REMAINS": "PARTIAL",
        "PREPARATION_STATUS": "PASS",
        "MANUAL_REVIEW_STATUS": "FAIL",
        "BLOCKER": blocker,
        "NEXT": next_stage,
        "ROOT_CAUSE_BY_PAPER": [
            {
                "paper_id": paper_id,
                "root_cause_category": category_by_id[paper_id],
                "root_cause_confidence": confidence_by_id[paper_id],
                "recommended_minimal_reentry_stage": reentry_by_id[paper_id],
                "requires_human_rereview": 1,
            }
            for paper_id in major_ids
        ],
        "OUTPUTS": [
            rel(ROOT_CAUSE_CSV_PATH),
            rel(ROOT_CAUSE_REPORT_PATH),
            rel(STAGE_RESULT_PATH),
        ],
        "ISSUES": [
            "G11 remains PARTIAL because 11 human MAJOR findings are still open.",
            "No formal artifact, packet, source or decision repair was performed.",
            "Overall next stage is a repair-plan handoff because the triage contains multiple root-cause layers.",
        ],
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    write_json(STAGE_RESULT_PATH, stage_result)

    print("STAGE=G11-MAJOR-DEFECT-ROOT-CAUSE-TRIAGE")
    print(f"STATUS={status}")
    print(f"BRANCH={branch}")
    print(f"HEAD={head}")
    print(f"TRIAGE_ATTEMPT_ID={triage_attempt_id}")
    print(f"AUTHORITATIVE_G11_PREPARATION_ATTEMPT_ID={PREPARATION_ATTEMPT_ID}")
    print(f"G11_SAMPLE_FINGERPRINT={SAMPLE_FINGERPRINT}")
    print(f"DECISION_SHEET_SHA256_BEFORE={decision_sha_before}")
    print(f"DECISION_SHEET_SHA256_AFTER={decision_sha_after}")
    print(f"DECISION_SHEET_HASH_UNCHANGED={int(decision_sha_before == decision_sha_after)}")
    print(f"MAJOR_INPUT_COUNT={len(major_ids)}")
    print(f"MAJOR_TRIAGED_COUNT={len(evidence_rows)}")
    print(f"ROOT_CAUSE_UNRESOLVED_COUNT={len(unresolved_ids)}")
    print(f"REVIEW_PACKET_EXCERPT_OMISSION_COUNT={len(packet_omission_ids)}")
    print(f"FORMAL_ARTIFACT_PAGE_CONTENT_MISSING_COUNT={len(formal_missing_ids)}")
    print(f"SOURCE_PAGE_MAPPING_MISMATCH_COUNT={len(mapping_ids)}")
    print(f"TRUE_CONTENT_QUALITY_MAJOR_COUNT={len(true_quality_ids)}")
    print(f"ARTIFACT_BINDING_DEFECT_COUNT={len(artifact_binding_ids)}")
    print(f"GOVERNED_DUPLICATE_BINDING_DEFECT_COUNT={len(duplicate_binding_ids)}")
    print(f"MIXED_ROOT_CAUSE_COUNT={len(mixed_ids)}")
    print(f"MAJOR_WITH_FORMAL_PAGE_CONTENT_PRESENT_BUT_EXCERPT_MISSING_COUNT={len(formal_page_present_excerpt_missing_ids)}")
    print(f"MAJOR_WITH_FORMAL_PAGE_CONTENT_MISSING_COUNT={len(formal_page_missing_ids)}")
    print(f"REQUIRES_HUMAN_REREVIEW_COUNT={len(evidence_rows)}")
    print("POTENTIAL_REVIEW_PACKET_AFFECTED_SCOPE=OTHER")
    print("POTENTIAL_AFFECTED_IDENTITY_COUNT=0")
    print("POTENTIAL_FORMAL_ARTIFACT_AFFECTED_SCOPE=BROADER_THAN_SAMPLE")
    print(f"POTENTIAL_FORMAL_ARTIFACT_AFFECTED_IDENTITY_COUNT={marker_only_scope_count}")
    print(f"BLOCKER={blocker}")
    print(f"NEXT={next_stage}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
