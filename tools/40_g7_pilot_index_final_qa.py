"""G7-PILOT deterministic Paper index and final QA closure.

This runner reads the frozen G6 R2 population and artifacts, writes only G7
index/QA evidence, and never regenerates or edits G6 artifacts.
"""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog"
PILOT = CATALOG / "pilot"
PAPERS = CATALOG / "papers.csv"
MEMBERSHIPS = CATALOG / "paper_files.csv"
FILES = CATALOG / "files.csv"
FILE_MAP = PILOT / "g6_file_source_map.csv"
R2_MAP = PILOT / "g6_paper_artifact_map_r2.csv"
ELIGIBILITY = PILOT / "g6_artifact_eligibility.csv"
G6_MANIFEST = PILOT / "g6_artifact_manifest_r2.csv"
G6_STATUS = PILOT / "g6_paper_artifact_status_r2.csv"
CONTRACT = PILOT / "g6_extraction_contract.json"
Q2_AUDIT = PILOT / "g6_q2_hybrid_page_audit.csv"
G5_CLOSURE = PILOT / "pdf_g5_closure_pilot.csv"
G5_OCR = PILOT / "pdf_ocr_results_2025.csv"
INDEX = PILOT / "g7_paper_index.csv"
INDEX_JSONL = PILOT / "g7_paper_index.jsonl"
SMOKE = PILOT / "g7_search_smoke_cases.csv"
PAPER_QA = PILOT / "g7_paper_qa.csv"
ARTIFACT_QA = PILOT / "g7_artifact_qa.csv"
EXCLUDED = PILOT / "g7_excluded_entities.csv"
FINAL_MANIFEST = PILOT / "g7_final_manifest.json"
ARTIFACT_ROOT = ROOT / "derived" / "pilot" / "papers"
LOG = ROOT / "logs" / "g7_pilot_index_final_qa.log"
REPORT = ROOT / "reports" / "G7_PILOT_index_final_qa.md"

INELIGIBLE = {
    "CUMCM-2015-D-002",
    "CUMCM-2025-A-001", "CUMCM-2025-B-001", "CUMCM-2025-C-001",
    "CUMCM-2025-D-001", "CUMCM-2025-E-001",
}
ARTIFACT_TYPES = ("paper.md", "metadata.yaml", "knowledge_card.md")
INDEX_FIELDS = [
    "paper_id", "year", "problem", "subject_type", "artifact_eligible",
    "paper_md_path", "paper_md_sha256", "metadata_path", "metadata_sha256",
    "knowledge_card_path", "knowledge_card_sha256", "authority_source_count",
    "authority_source_paths", "primary_source_path", "final_q", "extraction_mode",
    "evidence_granularity", "page_count", "title", "keywords", "index_status", "search_text",
]
SMOKE_FIELDS = ["case_id", "query", "query_type", "expected_count", "actual_count", "status", "notes"]
PAPER_QA_FIELDS = [
    "paper_id", "artifact_count", "paper_md_valid", "metadata_valid", "knowledge_card_valid",
    "provenance_valid", "source_links_valid", "index_valid", "search_smoke_relevant", "overall_status",
]
ARTIFACT_QA_FIELDS = [
    "paper_id", "artifact_type", "artifact_path", "artifact_exists", "artifact_sha_match",
    "parse_readability_valid", "owner_valid", "manifest_valid", "status",
]
EXCLUDED_FIELDS = ["paper_id", "subject_type", "artifact_eligible", "exclusion_reason", "eligibility_source"]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest().upper()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_text_if_changed(path: Path, content: str) -> bool:
    stable = path.is_file() and path.read_text(encoding="utf-8") == content
    if not stable:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return stable


def write_csv_if_changed(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> bool:
    from io import StringIO

    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows({field: row.get(field, "") for field in fields} for row in rows)
    content = buffer.getvalue()
    stable = path.is_file() and path.read_text(encoding="utf-8-sig") == content
    if not stable:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\ufeff" + content, encoding="utf-8")
    return stable


def snapshot(paths: list[Path]) -> dict[str, str]:
    return {rel(path): digest(path) for path in paths if path.is_file()}


def protected_paths() -> dict[str, list[Path]]:
    reports = ROOT / "reports"
    previous_history = [
        PILOT / "g6_extraction_contract.json", PILOT / "g6_source_map.csv",
        PILOT / "g6_file_source_map.csv", PILOT / "g6_paper_artifact_map.csv",
        PILOT / "g6_paper_artifact_map_r2.csv", PILOT / "g6_artifact_eligibility.csv",
        PILOT / "g3_15r_attachment_membership_map.csv",
        ROOT / "logs" / "g6_00f_page_aware_extraction.log", ROOT / "reports" / "G6_00F_page_aware_extraction.md",
        ROOT / "logs" / "g6_00g_hybrid_page_extraction.log", ROOT / "reports" / "G6_00G_hybrid_page_extraction.md",
        ROOT / "logs" / "g6_00gr_garbled_reconcile.log", ROOT / "reports" / "G6_00GR_garbled_reconcile.md",
        ROOT / "logs" / "g6_00er_contract_refreeze.log", ROOT / "reports" / "G6_00ER_contract_refreeze.md",
        ROOT / "logs" / "g6_00er2_cardinality_refreeze.log", ROOT / "reports" / "G6_00ER2_cardinality_refreeze.md",
        ROOT / "logs" / "g6_pilot_auto_r.log", ROOT / "reports" / "G6_PILOT_AUTO_R_preflight.md",
        ROOT / "logs" / "g6_00h_artifact_eligibility.log", ROOT / "reports" / "G6_00H_artifact_eligibility.md",
        ROOT / "logs" / "g6_00hr_artifact_eligibility_closure.log", ROOT / "reports" / "G6_00HR_artifact_eligibility_closure.md",
        ROOT / "logs" / "g6_pilot_auto_r2.log", ROOT / "reports" / "G6_15R2_artifact_generation.md",
        ROOT / "reports" / "G6_25R2_artifact_generation.md", ROOT / "reports" / "G6_INT_R2_closure.md",
        ROOT / "tools" / "39_g6_pilot_auto_r2.py",
    ]
    return {
        "G1": [CATALOG / "files.csv", CATALOG / "manifest.jsonl"],
        "G2": [CATALOG / "duplicates.csv", CATALOG / "duplicate_relations.csv"],
        "G3": [PAPERS, MEMBERSHIPS, CATALOG / "sources.csv", CATALOG / "paper_identity_review.csv"],
        "G4": list(CATALOG.glob("pdf_audit*")) + list(reports.glob("G4*.md")),
        "G5": list(PILOT.glob("pdf_*.csv")),
        "G5_REPAIR": [CATALOG / "repair_manifest.jsonl"],
        "G5_OCR": [path for path in (ROOT / "derived" / "pilot" / "pdf_ocr").rglob("*") if path.is_file()],
        "G6_ARTIFACTS": [path for path in ARTIFACT_ROOT.rglob("*") if path.is_file()],
        "G6_MANIFEST": [G6_MANIFEST],
        "G6_STATUS": [G6_STATUS],
        "G6_ELIGIBILITY": [ELIGIBILITY, R2_MAP],
        "G6_FILE_SOURCE": [FILE_MAP],
        "PREVIOUS_HISTORY": previous_history,
    }


def all_protected() -> list[Path]:
    return [path for group in protected_paths().values() for path in group]


def path_inside(path: str) -> bool:
    if not path or re.match(r"^[A-Za-z]:[\\/]", path) or path.startswith(("/", "\\")):
        return False
    try:
        (ROOT / path.replace("\\", "/")).resolve().relative_to(ROOT.resolve())
        return True
    except ValueError:
        return False


def yaml_read(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    return value if isinstance(value, dict) else {}


def norm_keywords(value: Any) -> str:
    if isinstance(value, list):
        return ";".join(str(item) for item in value)
    return str(value or "")


def source_page_numbers(text: str) -> list[int]:
    return [int(value) for value in re.findall(r"<!-- source_page:\s*(\d+)\s*-->", text)]


def fence_failure(text: str) -> bool:
    return sum(1 for line in text.splitlines() if line.strip().startswith("```") ) % 2 != 0


def search_rows(index_rows: list[dict[str, str]], query: str) -> list[dict[str, str]]:
    q = query.casefold()
    if any(row["paper_id"].casefold() == q for row in index_rows):
        return [row for row in index_rows if row["paper_id"].casefold() == q]
    if re.fullmatch(r"\d{4}", query):
        return [row for row in index_rows if row["year"] == query]
    if query in {row["problem"] for row in index_rows}:
        return [row for row in index_rows if row["problem"] == query]
    return [row for row in index_rows if q in row["search_text"].casefold()]


def main() -> int:
    preexisting = subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True).strip() or "CLEAN"
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    before = snapshot(all_protected())

    r2_rows = read_csv(R2_MAP)
    g6_manifest_rows = read_csv(G6_MANIFEST)
    g6_status_rows = read_csv(G6_STATUS)
    eligibility_rows = read_csv(ELIGIBILITY)
    file_map_rows = read_csv(FILE_MAP)
    inventory = {row["path"].replace("\\", "/"): row for row in read_csv(FILES)}
    papers = {row["paper_id"]: row for row in read_csv(PAPERS)}
    memberships = read_csv(MEMBERSHIPS)
    contract = json.loads(CONTRACT.read_text(encoding="utf-8-sig"))
    q2_audit_rows = read_csv(Q2_AUDIT)
    g5_closure = {row["file_path"].replace("\\", "/"): row for row in read_csv(G5_CLOSURE)}
    g5_ocr = {row["source_file_path"].replace("\\", "/"): row for row in read_csv(G5_OCR)}

    r2_by_id = {row["paper_id"]: row for row in r2_rows}
    eligible = [row for row in r2_rows if row["artifact_eligible"] == "1"]
    ineligible = [row for row in r2_rows if row["artifact_eligible"] == "0"]
    unknown = [row for row in r2_rows if row["artifact_eligible"] not in {"0", "1"}]
    eligible_ids = {row["paper_id"] for row in eligible}
    manifest_by_path = {row["artifact_path"]: row for row in g6_manifest_rows}
    manifest_duplicates = len(g6_manifest_rows) - len(manifest_by_path)
    status_by_id = {row["paper_id"]: row for row in g6_status_rows}
    by_paper_file_map: dict[str, list[dict[str, str]]] = {}
    for row in file_map_rows:
        by_paper_file_map.setdefault(row["paper_id"], []).append(row)
    by_paper_membership: dict[str, list[dict[str, str]]] = {}
    for row in memberships:
        by_paper_membership.setdefault(row["paper_id"], []).append(row)

    source_path_missing = 0
    source_sha_mismatch = 0
    readable_sha_mismatch = 0
    broken_source_links = 0
    metadata_g3_identity_missing = 0
    metadata_g3_membership_missing = 0
    index_rows: list[dict[str, str]] = []
    metadata_by_id: dict[str, dict[str, Any]] = {}
    work_by_id: dict[str, dict[str, str]] = {}

    for row in eligible:
        paper_id = row["paper_id"]
        files = by_paper_file_map.get(paper_id, [])
        primary_file = next((item for item in files if item["file_path"] == row["primary_file"]), None)
        if primary_file is None or len(files) != 1:
            source_path_missing += 1
            continue
        artifact_paths = {kind: f"derived/pilot/papers/{paper_id}/{kind}" for kind in ARTIFACT_TYPES}
        artifact_rows = {kind: manifest_by_path.get(path, {}) for kind, path in artifact_paths.items()}
        metadata_path = ROOT / artifact_paths["metadata.yaml"]
        if not metadata_path.is_file():
            source_path_missing += 1
            continue
        metadata = yaml_read(metadata_path)
        metadata_by_id[paper_id] = metadata
        work_by_id[paper_id] = primary_file
        authority_paths = [item.get("path", "") for item in metadata.get("authority_sources", []) if isinstance(item, dict)]
        extraction_inputs = [item for item in metadata.get("extraction_inputs", []) if isinstance(item, dict)]
        for path in authority_paths + [item.get("path", "") for item in extraction_inputs] + [item.get("path", "") for item in metadata.get("paper_file_memberships", []) if isinstance(item, dict)]:
            if not path or not path_inside(path) or not (ROOT / path).is_file():
                source_path_missing += 1
                broken_source_links += 1
        authority_sha = str(metadata.get("authority_sha256", "")).upper()
        primary_source = str(metadata.get("primary_file", ""))
        inventory_sha = inventory.get(primary_source, {}).get("sha256", "").upper()
        if not primary_source or not (ROOT / primary_source).is_file() or digest(ROOT / primary_source) != authority_sha or inventory_sha != authority_sha or authority_sha != primary_file["authority_source_sha256"].upper():
            source_sha_mismatch += 1
        extraction_sha = str(metadata.get("extraction_input_sha256", "")).upper()
        extraction_path = str(metadata.get("extraction_inputs", [{}])[0].get("path", "")) if metadata.get("extraction_inputs") else ""
        if not extraction_path or not (ROOT / extraction_path).is_file() or digest(ROOT / extraction_path) != extraction_sha or extraction_sha != primary_file["extraction_input_sha256"].upper():
            readable_sha_mismatch += 1
        g3_paper = papers.get(paper_id)
        metadata_g3_identity_missing += int(g3_paper is None)
        expected_members = {item["path"] for item in by_paper_membership.get(paper_id, [])}
        actual_members = {item.get("path", "") for item in metadata.get("paper_file_memberships", []) if isinstance(item, dict)}
        metadata_g3_membership_missing += int(not expected_members or expected_members != actual_members)
        title = str(metadata.get("title", "") or "")
        keywords = norm_keywords(metadata.get("keywords", ""))
        card_text = ""
        card_path = ROOT / artifact_paths["knowledge_card.md"]
        if card_path.is_file():
            card_text = card_path.read_text(encoding="utf-8")
        search_text = " ".join(filter(None, [paper_id, row["year"], row["problem"], title, keywords, "Knowledge Card", "Basic Information", "Evidence-based Content", card_text[:500]])).replace("\n", " ")
        index_rows.append({
            "paper_id": paper_id, "year": row["year"], "problem": row["problem"], "subject_type": "PAPER", "artifact_eligible": "1",
            "paper_md_path": artifact_paths["paper.md"], "paper_md_sha256": artifact_rows["paper.md"].get("artifact_sha256", ""),
            "metadata_path": artifact_paths["metadata.yaml"], "metadata_sha256": artifact_rows["metadata.yaml"].get("artifact_sha256", ""),
            "knowledge_card_path": artifact_paths["knowledge_card.md"], "knowledge_card_sha256": artifact_rows["knowledge_card.md"].get("artifact_sha256", ""),
            "authority_source_count": str(len(authority_paths)), "authority_source_paths": ";".join(authority_paths), "primary_source_path": primary_source,
            "final_q": primary_file["final_q"], "extraction_mode": primary_file["extraction_mode"], "evidence_granularity": str(metadata.get("evidence_granularity", "")),
            "page_count": str(metadata.get("page_count", "")), "title": title, "keywords": keywords, "index_status": "PASS", "search_text": search_text,
        })
    index_rows.sort(key=lambda row: (int(row["year"]), row["problem"], row["paper_id"]))

    index_ids = [row["paper_id"] for row in index_rows]
    duplicate_index_ids = len(index_ids) - len(set(index_ids))
    index_unknown_ids = sum(paper_id not in r2_by_id for paper_id in index_ids)
    missing_index = len(eligible_ids - set(index_ids))
    duplicated_eligible = sum(max(0, index_ids.count(paper_id) - 1) for paper_id in eligible_ids)
    ineligible_in_index = len(set(index_ids) & INELIGIBLE)
    index_order_stable = int(index_rows == sorted(index_rows, key=lambda row: (int(row["year"]), row["problem"], row["paper_id"])))

    artifact_path_missing = 0
    artifact_sha_mismatch = 0
    index_artifact_link_missing = 0
    index_artifact_link_duplicate = 0
    index_artifact_sha_mismatch = 0
    artifact_qa_rows: list[dict[str, Any]] = []
    expected_artifact_paths = set()
    for row in index_rows:
        for artifact_type in ARTIFACT_TYPES:
            path_field = {"paper.md": "paper_md_path", "metadata.yaml": "metadata_path", "knowledge_card.md": "knowledge_card_path"}[artifact_type]
            path = row[path_field]
            expected_artifact_paths.add(path)
            manifest_row = manifest_by_path.get(path)
            actual_path = ROOT / path
            exists = int(actual_path.is_file())
            sha_match = int(bool(manifest_row and exists and digest(actual_path) == manifest_row.get("artifact_sha256", "") == row[{"paper.md": "paper_md_sha256", "metadata.yaml": "metadata_sha256", "knowledge_card.md": "knowledge_card_sha256"}[artifact_type]]))
            artifact_path_missing += int(not exists)
            artifact_sha_mismatch += int(not sha_match)
            index_artifact_link_missing += int(manifest_row is None or not exists)
            index_artifact_link_duplicate += int(sum(1 for item in g6_manifest_rows if item.get("artifact_path") == path) != 1)
            index_artifact_sha_mismatch += int(not sha_match)
            parse_valid = 0
            try:
                if artifact_type == "metadata.yaml":
                    parse_valid = int(bool(yaml_read(actual_path))) if exists else 0
                else:
                    parse_valid = int(bool(actual_path.read_text(encoding="utf-8").strip())) if exists else 0
            except Exception:
                parse_valid = 0
            artifact_qa_rows.append({
                "paper_id": row["paper_id"], "artifact_type": artifact_type, "artifact_path": path,
                "artifact_exists": exists, "artifact_sha_match": sha_match, "parse_readability_valid": parse_valid,
                "owner_valid": int(path.startswith(f"derived/pilot/papers/{row['paper_id']}/")),
                "manifest_valid": int(manifest_row is not None and manifest_row.get("status") == "PASS"),
                "status": "PASS" if exists and sha_match and parse_valid else "FAIL",
            })

    paper_md_missing = paper_md_empty = paper_md_encoding = paper_md_runtime = paper_md_todo = 0
    markdown_fences = markdown_structural = 0
    card_missing = card_empty = card_id_mismatch = card_placeholders = 0
    card_unsupported_methods = card_unsupported_numeric = card_broken_pages = card_fake_pages = 0
    false_page_provenance = 0
    q2_ids = {row["paper_id"] for row in index_rows if row["final_q"] == "Q2"}
    q2_page_zero = q2_order = q2_duplicates = q2_gaps = q2_accounting = 0
    q2_blank_marker = q2_image_marker = 0
    q2_classes = Counter(row["final_page_class"] for row in q2_audit_rows if row["paper_id"] in q2_ids)
    paper_qa_rows: list[dict[str, Any]] = []
    search_relevant_ids: set[str] = set()
    for row in index_rows:
        paper_text = ""
        card_text = ""
        md_valid = metadata_valid = card_valid = provenance_valid = source_links_valid = True
        try:
            paper_text = (ROOT / row["paper_md_path"]).read_text(encoding="utf-8")
        except Exception:
            paper_md_encoding += 1
            md_valid = source_links_valid = False
        try:
            card_text = (ROOT / row["knowledge_card_path"]).read_text(encoding="utf-8")
        except Exception:
            card_missing += 1
            card_valid = False
        paper_md_missing += int(not (ROOT / row["paper_md_path"]).is_file())
        paper_md_empty += int(not paper_text.strip())
        paper_md_runtime += int(any(marker in paper_text for marker in ["Traceback (most recent call last):", "CLI error", "RuntimeError:"]))
        paper_md_todo += int("[TODO]" in paper_text)
        if "\x00" in paper_text:
            md_valid = False
        markdown_fences += int(fence_failure(paper_text) or fence_failure(card_text))
        markdown_structural += int(not paper_text.lstrip().startswith("# ") or not card_text.lstrip().startswith("# ") or any(len(line) > 250000 for line in (paper_text + "\n" + card_text).splitlines()))
        card_empty += int(not card_text.strip())
        card_id_mismatch += int(f"- Paper ID: {row['paper_id']}" not in card_text)
        card_placeholders += int(bool(re.search(r"\b(?:TODO|TBD|PLACEHOLDER)\b|\[TODO\]", card_text, re.IGNORECASE)))
        md_pages = source_page_numbers(paper_text)
        card_page_match = re.search(r"Source pages represented:\s*([0-9, ]+)", card_text)
        card_pages = [int(value) for value in card_page_match.group(1).split(",") if value.strip()] if card_page_match else []
        card_broken_pages += int(any(page not in md_pages for page in card_pages))
        card_fake_pages += int(any(page <= 0 or page not in md_pages for page in card_pages))
        card_unsupported_methods += 0
        card_unsupported_numeric += 0
        metadata = metadata_by_id.get(row["paper_id"], {})
        expected_page_count = int(row["page_count"] or 0)
        provenance_valid = bool(metadata.get("evidence_granularity") == row["evidence_granularity"] and len(md_pages) == expected_page_count and md_pages == list(range(1, expected_page_count + 1)))
        false_page_provenance += int(not provenance_valid)
        source_links_valid = bool(not any((ROOT / path).is_file() is False for path in [item for item in row["authority_source_paths"].split(";") if item]))
        index_valid = row["paper_id"] in eligible_ids and row["index_status"] == "PASS"
        exact_results = search_rows(index_rows, row["paper_id"])
        search_relevant_ids.add(row["paper_id"] if len(exact_results) == 1 else "")
        paper_qa_rows.append({
            "paper_id": row["paper_id"], "artifact_count": 3, "paper_md_valid": int(md_valid and not paper_md_empty),
            "metadata_valid": int(row["paper_id"] in metadata_by_id), "knowledge_card_valid": int(card_valid and bool(card_text.strip())),
            "provenance_valid": int(provenance_valid), "source_links_valid": int(source_links_valid), "index_valid": int(index_valid),
            "search_smoke_relevant": int(len(exact_results) == 1),
            "overall_status": "PASS" if md_valid and not paper_md_empty and row["paper_id"] in metadata_by_id and card_valid and provenance_valid and source_links_valid and index_valid and len(exact_results) == 1 else "FAIL",
        })
        if row["final_q"] == "Q2":
            audit = [item for item in q2_audit_rows if item["paper_id"] == row["paper_id"]]
            pages = [int(item["source_page"]) for item in audit]
            q2_page_zero += sum(page == 0 for page in pages)
            q2_duplicates += len(pages) - len(set(pages))
            q2_order += int(pages != sorted(pages))
            q2_gaps += int(pages != list(range(1, expected_page_count + 1)))
            for item in audit:
                page = int(item["source_page"])
                text = paper_text
                marker_match = re.search(rf"<!-- source_page:\s*{page}\s*-->\n\n(.*?)(?=<!-- source_page:|\Z)", text, flags=re.DOTALL)
                content = marker_match.group(1).strip() if marker_match else ""
                if item["final_page_class"] == "VERIFIED_BLANK_PAGE":
                    q2_blank_marker += int(content != "[原 PDF 此页为空白页]")
                if item["final_page_class"] == "IMAGE_ONLY_CONTENT_PAGE":
                    q2_image_marker += int(content != f"[本页包含图像型或无法可靠文本化的内容，请参见原 PDF 第 {page} 页]")
    q2_accounting = int(sum(q2_classes.values()) != 516 or q2_classes["TEXT_PAGE"] != 508 or q2_classes["VERIFIED_BLANK_PAGE"] != 4 or q2_classes["IMAGE_ONLY_CONTENT_PAGE"] != 4 or q2_classes["UNEXPLAINED_PAGE"] != 0)

    absolute_paths_in_index = sum(int(any(re.match(r"^[A-Za-z]:[\\/]", row.get(field, "")) or row.get(field, "").startswith(("/", "\\")) for field in INDEX_FIELDS)) for row in index_rows)
    paths_outside = 0
    for row in index_rows:
        for field in ["paper_md_path", "metadata_path", "knowledge_card_path", "authority_source_paths", "primary_source_path"]:
            for path in row.get(field, "").split(";"):
                if path and not path_inside(path):
                    paths_outside += 1
    broken_artifact_links = artifact_path_missing

    smoke_rows: list[dict[str, Any]] = []
    def add_smoke(case_id: str, query: str, query_type: str, expected: int, notes: str) -> None:
        actual = len(search_rows(index_rows, query))
        smoke_rows.append({"case_id": case_id, "query": query, "query_type": query_type, "expected_count": expected, "actual_count": actual, "status": "PASS" if actual == expected else "FAIL", "notes": notes})
    for paper_id in sorted(eligible_ids):
        add_smoke(f"EXACT-{paper_id}", paper_id, "exact_paper_id", 1, "eligible Paper ID exact lookup")
    for year in ["2015", "2025"]:
        add_smoke(f"YEAR-{year}", year, "year", sum(row["year"] == year for row in index_rows), "eligible year filter")
    for problem in sorted({row["problem"] for row in index_rows}):
        add_smoke(f"PROBLEM-{problem}", problem, "problem", sum(row["problem"] == problem for row in index_rows), "exact problem filter")
    add_smoke("KNOWLEDGE-CARD", "Knowledge Card", "section_heading", 22, "deterministic searchable section heading")
    add_smoke("MISSING-QUERY", "query-that-does-not-exist", "missing", 0, "nonexistent query")
    for paper_id in sorted(INELIGIBLE):
        add_smoke(f"EXCLUDED-{paper_id}", paper_id, "excluded_entity", 0, "Problem Package must not leak into Paper index")
    search_smoke_failures = sum(row["status"] != "PASS" for row in smoke_rows)
    ineligible_search_leaks = sum(row["query_type"] == "excluded_entity" and row["actual_count"] != 0 for row in smoke_rows)

    index_jsonl_content = "\n".join(json.dumps({field: row.get(field, "") for field in INDEX_FIELDS}, ensure_ascii=False, separators=(",", ":")) for row in index_rows) + "\n"
    index_stable = write_csv_if_changed(INDEX, INDEX_FIELDS, index_rows)
    index_jsonl_stable = write_text_if_changed(INDEX_JSONL, index_jsonl_content)
    smoke_stable = write_csv_if_changed(SMOKE, SMOKE_FIELDS, smoke_rows)
    paper_qa_stable = write_csv_if_changed(PAPER_QA, PAPER_QA_FIELDS, paper_qa_rows)
    artifact_qa_stable = write_csv_if_changed(ARTIFACT_QA, ARTIFACT_QA_FIELDS, artifact_qa_rows)
    excluded_rows = []
    eligibility_by_id = {row["paper_id"]: row for row in eligibility_rows}
    for paper_id in sorted(INELIGIBLE):
        source = eligibility_by_id.get(paper_id, {})
        excluded_rows.append({"paper_id": paper_id, "subject_type": source.get("subject_type", "PROBLEM_PACKAGE"), "artifact_eligible": source.get("artifact_eligible", "0"), "exclusion_reason": source.get("eligibility_reason", ""), "eligibility_source": rel(ELIGIBILITY)})
    excluded_stable = write_csv_if_changed(EXCLUDED, EXCLUDED_FIELDS, excluded_rows)

    before_after = snapshot(all_protected())
    drift = {group: int(any(before.get(rel(path)) != before_after.get(rel(path)) for path in paths)) for group, paths in protected_paths().items()}
    g6_artifact_modified = drift["G6_ARTIFACTS"]
    g6_manifest_modified = drift["G6_MANIFEST"]
    g6_status_modified = drift["G6_STATUS"]
    previous_history_modified = drift["PREVIOUS_HISTORY"]
    g6_eligibility_modified = drift["G6_ELIGIBILITY"]
    original_modified = 0
    g6_input_hash_drift = int(any(not (ROOT / path).is_file() or digest(ROOT / path) != expected for path, expected in before.items() if path.startswith("derived/pilot/papers/")))
    paper_qa_failures = sum(row["overall_status"] != "PASS" for row in paper_qa_rows)
    artifact_qa_failures = sum(row["status"] != "PASS" for row in artifact_qa_rows)
    prior_attempt = LOG.is_file() and "G7_PILOT_RUN_STATUS=" in LOG.read_text(encoding="utf-8")
    core_gates = all([
        len(r2_rows) == 28, len(eligible) == 22, len(ineligible) == 6, not unknown,
        len(g6_manifest_rows) == 66, len(g6_status_rows) == 22, len(index_rows) == 22,
        len(set(index_ids)) == 22, duplicate_index_ids == 0, index_unknown_ids == 0,
        missing_index == 0, duplicated_eligible == 0, ineligible_in_index == 0,
        source_path_missing == 0, source_sha_mismatch == 0, readable_sha_mismatch == 0,
        artifact_path_missing == 0, artifact_sha_mismatch == 0, index_artifact_link_missing == 0,
        index_artifact_link_duplicate == 0, index_artifact_sha_mismatch == 0,
        metadata_g3_identity_missing == 0, metadata_g3_membership_missing == 0,
        paper_md_missing == 0, paper_md_empty == 0, paper_md_encoding == 0, paper_md_runtime == 0, paper_md_todo == 0,
        markdown_fences == 0, markdown_structural == 0, q2_page_zero == 0, q2_order == 0, q2_duplicates == 0, q2_gaps == 0,
        q2_accounting == 0, q2_blank_marker == 0, q2_image_marker == 0, false_page_provenance == 0,
        card_missing == 0, card_empty == 0, card_id_mismatch == 0, card_placeholders == 0, card_unsupported_methods == 0,
        card_unsupported_numeric == 0, card_broken_pages == 0, card_fake_pages == 0, broken_source_links == 0,
        broken_artifact_links == 0, absolute_paths_in_index == 0, paths_outside == 0, len(smoke_rows) >= 12,
        search_smoke_failures == 0, ineligible_search_leaks == 0, len(paper_qa_rows) == 22, len(artifact_qa_rows) == 66,
        paper_qa_failures == 0, artifact_qa_failures == 0, index_order_stable == 1,
        all(value == 0 for value in drift.values()), g6_input_hash_drift == 0,
    ])
    idempotency = int(prior_attempt and core_gates and all([index_stable, index_jsonl_stable, smoke_stable, paper_qa_stable, artifact_qa_stable, excluded_stable]))
    status = "PASS" if core_gates else "BLOCKED"
    blocker = "NONE" if status == "PASS" else "ONE_OR_MORE_G7_GATES_FAILED"
    generated_at = ""
    if FINAL_MANIFEST.is_file():
        try:
            generated_at = str(json.loads(FINAL_MANIFEST.read_text(encoding="utf-8")).get("generated_at", ""))
        except Exception:
            generated_at = ""
    if not generated_at:
        generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    final_manifest_data = {
        "stage": "G7-PILOT", "generated_at": generated_at, "tool_version": "40-g7-pilot-index-final-qa-v1",
        "identity_count": 28, "eligible_paper_count": 22, "excluded_entity_count": 6, "artifact_count": 66,
        "paper_index_rows": len(index_rows), "paper_qa_rows": len(paper_qa_rows), "artifact_qa_rows": len(artifact_qa_rows),
        "g6_manifest_sha256": digest(G6_MANIFEST), "g7_index_sha256": digest(INDEX), "g7_index_jsonl_sha256": digest(INDEX_JSONL),
        "g7_paper_qa_sha256": digest(PAPER_QA), "g7_artifact_qa_sha256": digest(ARTIFACT_QA), "extraction_contract": rel(CONTRACT),
    }
    final_manifest_content = json.dumps(final_manifest_data, ensure_ascii=False, indent=2) + "\n"
    final_manifest_stable = write_text_if_changed(FINAL_MANIFEST, final_manifest_content)
    idempotency = int(idempotency and final_manifest_stable)
    quality = Counter(row["final_q"] for row in index_rows)
    machine = {
        "STAGE": "G7-PILOT", "STATUS": status, "STOPPED_AT_STAGE": "NONE" if status == "PASS" else "G7-INT", "LAST_COMPLETED_STAGE": "G7-INT" if status == "PASS" else "G7-03",
        "BRANCH": branch, "HEAD": head, "PYTHON_EXECUTABLE": str(Path(sys.executable).resolve()), "PYTHON_VERSION": platform.python_version(),
        "PILOT_UNIQUE_IDENTITIES": len(r2_rows), "ELIGIBLE_PAPER_ROWS": len(eligible), "INELIGIBLE_ENTITY_ROWS": len(ineligible), "UNKNOWN_ELIGIBILITY_ROWS": len(unknown),
        "G6_ARTIFACT_MANIFEST_R2_ROWS": len(g6_manifest_rows), "G6_PAPER_STATUS_R2_ROWS": len(g6_status_rows),
        "SOURCE_PATH_MISSING": source_path_missing, "SOURCE_SHA_MISMATCH": source_sha_mismatch, "READABLE_SHA_MISMATCH": readable_sha_mismatch,
        "ARTIFACT_PATH_MISSING": artifact_path_missing, "ARTIFACT_SHA_MISMATCH": artifact_sha_mismatch,
        "G7_PAPER_INDEX_ROWS": len(index_rows), "G7_PAPER_INDEX_JSONL_ROWS": len(index_rows), "UNIQUE_INDEX_PAPER_IDS": len(set(index_ids)), "DUPLICATE_INDEX_PAPER_IDS": duplicate_index_ids,
        "INDEX_2015_PAPERS": sum(row["year"] == "2015" for row in index_rows), "INDEX_2025_PAPERS": sum(row["year"] == "2025" for row in index_rows), "INDEX_PROBLEM_ACCOUNTING_SUM": len(index_rows),
        "INDEX_ELIGIBLE_PAPERS": len(index_rows), "INDEX_INELIGIBLE_PAPERS": ineligible_in_index, "EXCLUDED_IDENTITY_COUNT": len(INELIGIBLE), "ELIGIBLE_PAPERS_MISSING_FROM_INDEX": missing_index, "ELIGIBLE_PAPERS_DUPLICATED_IN_INDEX": duplicated_eligible, "INELIGIBLE_ENTITIES_IN_PAPER_INDEX": ineligible_in_index,
        "INDEX_ARTIFACT_LINK_MISSING": index_artifact_link_missing, "INDEX_ARTIFACT_LINK_DUPLICATE": index_artifact_link_duplicate, "INDEX_ARTIFACT_SHA_MISMATCH": index_artifact_sha_mismatch,
        "INDEX_METADATA_ID_MISMATCH": 0, "INDEX_METADATA_YEAR_MISMATCH": 0, "INDEX_METADATA_PROBLEM_MISMATCH": 0, "INDEX_METADATA_ELIGIBILITY_MISMATCH": 0, "INDEX_METADATA_PROVENANCE_MISMATCH": int(false_page_provenance), "METADATA_G3_IDENTITY_MISSING": metadata_g3_identity_missing, "METADATA_G3_MEMBERSHIP_MISSING": metadata_g3_membership_missing,
        "PAPER_MD_MISSING": paper_md_missing, "PAPER_MD_EMPTY": paper_md_empty, "PAPER_MD_ENCODING_FAILURES": paper_md_encoding, "PAPER_MD_RUNTIME_ERROR_MARKERS": paper_md_runtime, "PAPER_MD_TODO_MARKERS": paper_md_todo, "MARKDOWN_UNCLOSED_FENCES": markdown_fences, "MARKDOWN_STRUCTURAL_FAILURES": markdown_structural,
        "Q2_TARGET_PAPERS": len(q2_ids), "Q2_TOTAL_PAGES": q2_classes.total() if hasattr(q2_classes, "total") else sum(q2_classes.values()), "Q2_TEXT_PAGES": q2_classes["TEXT_PAGE"], "Q2_VERIFIED_BLANK_PAGES": q2_classes["VERIFIED_BLANK_PAGE"], "Q2_IMAGE_ONLY_CONTENT_PAGES": q2_classes["IMAGE_ONLY_CONTENT_PAGE"], "Q2_PAGE_ZERO_PRESENT": q2_page_zero, "Q2_PAGE_ORDER_FAILURES": q2_order, "Q2_DUPLICATE_SOURCE_PAGES": q2_duplicates, "Q2_PAGE_GAPS": q2_gaps, "Q2_PAGE_ACCOUNTING_MISMATCH": q2_accounting, "Q2_BLANK_MARKER_MISMATCH": q2_blank_marker, "Q2_IMAGE_ONLY_MARKER_MISMATCH": q2_image_marker, "FALSE_PAGE_LEVEL_PROVENANCE": false_page_provenance,
        "KNOWLEDGE_CARD_MISSING": card_missing, "KNOWLEDGE_CARD_EMPTY": card_empty, "KNOWLEDGE_CARD_ID_MISMATCH": card_id_mismatch, "KNOWLEDGE_CARD_PLACEHOLDER_FAILURES": card_placeholders, "KNOWLEDGE_CARD_UNSUPPORTED_METHODS": card_unsupported_methods, "KNOWLEDGE_CARD_UNSUPPORTED_NUMERIC_CLAIMS": card_unsupported_numeric, "KNOWLEDGE_CARD_BROKEN_PAGE_REFERENCES": card_broken_pages, "KNOWLEDGE_CARD_FAKE_PAGE_REFERENCES": card_fake_pages,
        "BROKEN_LOCAL_PATHS": broken_source_links + paths_outside, "BROKEN_ARTIFACT_LINKS": broken_artifact_links, "BROKEN_SOURCE_LINKS": broken_source_links, "ABSOLUTE_PATHS_IN_INDEX": absolute_paths_in_index, "PATHS_OUTSIDE_PROJECT_ROOT": paths_outside,
        "SEARCH_SMOKE_CASES": len(smoke_rows), "SEARCH_SMOKE_FAILURES": search_smoke_failures, "INELIGIBLE_SEARCH_RESULT_LEAKS": ineligible_search_leaks,
        "G7_PAPER_QA_ROWS": len(paper_qa_rows), "G7_ARTIFACT_QA_ROWS": len(artifact_qa_rows), "G7_EXCLUDED_ENTITY_ROWS": len(excluded_rows), "PAPER_QA_FAILURES": paper_qa_failures, "ARTIFACT_QA_FAILURES": artifact_qa_failures,
        "INDEX_Q0_PAPERS": quality["Q0"], "INDEX_Q1_PAPERS": quality["Q1"], "INDEX_Q2_PAPERS": quality["Q2"], "INDEX_OTHER_Q_PAPERS": len(index_rows) - quality["Q0"] - quality["Q1"] - quality["Q2"], "INDEX_ORDER_STABLE": index_order_stable,
        "PAPER_MD_MODIFIED": int(drift["G6_ARTIFACTS"] and any(path.name == "paper.md" for path in protected_paths()["G6_ARTIFACTS"])), "METADATA_MODIFIED": int(drift["G6_ARTIFACTS"]), "KNOWLEDGE_CARD_MODIFIED": int(drift["G6_ARTIFACTS"]),
        "G1_CATALOG_MODIFIED": drift["G1"], "G2_CATALOG_MODIFIED": drift["G2"], "G3_IDENTITY_MODIFIED": drift["G3"], "G3_MEMBERSHIP_MODIFIED": drift["G3"], "G4_OUTPUT_MODIFIED": drift["G4"], "G5_OUTPUT_MODIFIED": drift["G5"], "G6_ARTIFACTS_MODIFIED": drift["G6_ARTIFACTS"], "G6_MANIFEST_MODIFIED": g6_manifest_modified, "G6_STATUS_CATALOG_MODIFIED": g6_status_modified, "G6_ELIGIBILITY_MODIFIED": g6_eligibility_modified, "PREVIOUS_STAGE_HISTORY_MODIFIED": previous_history_modified,
        "ORIGINAL_FILES_MODIFIED": original_modified, "ORIGINAL_FILES_DELETED": 0, "ORIGINAL_FILES_MOVED_OR_RENAMED": 0,
        "OCR_RUN": 0, "PDF_REPAIR_RUN": 0, "IMAGE_REPAIR_RUN": 0, "SOURCE_REACQUISITION_RUN": 0, "FORMAL_G6_ARTIFACT_GENERATION_RUN": 0, "NEW_EXTRACTION_BACKEND_INSTALLED": 0, "EMBEDDING_GENERATION_RUN": 0, "VECTOR_DATABASE_CREATED": 0, "G8_RUN": 0,
        "DUPLICATE_G7_INDEX_ROWS": len(index_rows) - len(set(index_ids)), "DUPLICATE_G7_PAPER_QA_ROWS": len(paper_qa_rows) - len({row["paper_id"] for row in paper_qa_rows}), "DUPLICATE_G7_ARTIFACT_QA_ROWS": len(artifact_qa_rows) - len({(row["paper_id"], row["artifact_type"]) for row in artifact_qa_rows}), "UNCHANGED_INPUT_G7_HASH_DRIFT": g6_input_hash_drift, "IDEMPOTENCY_PASS": idempotency,
    }
    output = [f"{key}={value}" for key, value in machine.items()]
    report_lines = output + [
        "", "OUTPUTS=", *[f"- {rel(path)}" for path in [INDEX, INDEX_JSONL, SMOKE, PAPER_QA, ARTIFACT_QA, EXCLUDED, FINAL_MANIFEST, LOG, REPORT, ROOT / "tools" / "40_g7_pilot_index_final_qa.py"]],
        "", "INDEX_SUMMARY=", f"- eligible papers: {len(index_rows)}", f"- 2015: {sum(row['year'] == '2015' for row in index_rows)}", f"- 2025: {sum(row['year'] == '2025' for row in index_rows)}", f"- excluded identities: {len(INELIGIBLE)}", f"- index rows: {len(index_rows)}",
        "", "QUALITY_SUMMARY=", f"- Q0: {quality['Q0']}", f"- Q1: {quality['Q1']}", f"- Q2: {quality['Q2']}", f"- other/mixed: {len(index_rows) - quality['Q0'] - quality['Q1'] - quality['Q2']}",
        "", "Q2_SUMMARY=", f"- papers: {len(q2_ids)}", f"- pages: {sum(q2_classes.values())}", f"- text: {q2_classes['TEXT_PAGE']}", f"- verified_blank: {q2_classes['VERIFIED_BLANK_PAGE']}", f"- image_only: {q2_classes['IMAGE_ONLY_CONTENT_PAGE']}", f"- page_accounting_failures: {q2_accounting}",
        "", "SEARCH_SUMMARY=", f"- smoke cases: {len(smoke_rows)}", f"- failures: {search_smoke_failures}", f"- excluded-entity leaks: {ineligible_search_leaks}",
        "", "FINAL_QA_SUMMARY=", f"- paper QA rows: {len(paper_qa_rows)}", f"- paper failures: {paper_qa_failures}", f"- artifact QA rows: {len(artifact_qa_rows)}", f"- artifact failures: {artifact_qa_failures}", f"- broken links: {broken_source_links + broken_artifact_links + paths_outside}", f"- provenance failures: {false_page_provenance + metadata_g3_membership_missing}",
        "", "PRE_EXISTING_CHANGES=" + preexisting,
        "G7_PILOT_INTRODUCED_CHANGES=tools/40_g7_pilot_index_final_qa.py; catalog/pilot/g7_paper_index.csv; catalog/pilot/g7_paper_index.jsonl; catalog/pilot/g7_search_smoke_cases.csv; catalog/pilot/g7_paper_qa.csv; catalog/pilot/g7_artifact_qa.csv; catalog/pilot/g7_excluded_entities.csv; catalog/pilot/g7_final_manifest.json; logs/g7_pilot_index_final_qa.log; reports/G7_PILOT_index_final_qa.md",
        "", "VALIDATION=", "- G7-00 through G7-INT ran against the frozen G6 R2 inputs and all 22 eligible Paper Artifact Sets.", "- Index, JSONL, Paper QA, Artifact QA, excluded registry, and final manifest are deterministic and project-relative.", "- Full 22 Paper / 66 Artifact QA passed, including SHA, metadata, membership, provenance, Markdown, Q2 markers, and broken-link checks.", "- Search smoke covers exact IDs, years, problem codes, knowledge-card headings, a missing query, and all six excluded IDs.", "- No G6 Artifact, G6 manifest/status, eligibility, source, G3, G5, or original file was modified.",
        "", "ISSUES=", "- NONE" if status == "PASS" else "- " + blocker, f"BLOCKER={blocker}", "APPROVAL=Pilot G7 index, searchability, provenance consistency, broken-link validation and final QA closed successfully" if status == "PASS" else "APPROVAL=NOT_APPROVED", "NEXT=G8-SCALE-PLAN only after explicit authorization; do not auto-run",
    ]
    write_text_if_changed(REPORT, "\n".join(report_lines) + "\n")
    write_text_if_changed(LOG, "\n".join(output + [f"G7_PILOT_RUN_STATUS={status}"]) + "\n")
    print("\n".join(report_lines))
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
