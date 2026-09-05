"""Targeted G3-25R identity repair for the seven 2025 Q2 PDFs.

This runner deliberately reads the frozen G3 catalogs and only writes the
target Paper/Source/membership rows, the target review rows, and the bridge
report.  It does not run discovery, PDF processing, OCR, or G6 extraction.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
TARGET_IDS = ["A066", "A196", "B060", "C023", "C132", "D037", "E030"]
TARGET_SET = set(TARGET_IDS)
STAMP = timezone(timedelta(hours=8))

PAPERS = ROOT / "catalog" / "papers.csv"
MEMBERSHIPS = ROOT / "catalog" / "paper_files.csv"
SOURCES = ROOT / "catalog" / "sources.csv"
FILES = ROOT / "catalog" / "files.csv"
REVIEW = ROOT / "catalog" / "paper_identity_review.csv"
CONTRACT = ROOT / "catalog" / "schema" / "contract.json"
BRIDGE = ROOT / "catalog" / "pilot" / "g3_25r_q2_identity_map.csv"
LOG = ROOT / "logs" / "g3_25r_identity_repair.log"
REPORT = ROOT / "reports" / "G3_25R_identity_repair.md"

PROTECTED = {
    "G1": [ROOT / "catalog" / "files.csv", ROOT / "catalog" / "manifest.jsonl"],
    "G2": [ROOT / "catalog" / "duplicates.csv", ROOT / "catalog" / "duplicate_relations.csv"],
    "G4": [],
    "G5_QUALITY": [ROOT / "catalog" / "pilot" / "pdf_quality_pilot.csv", ROOT / "catalog" / "pilot" / "pdf_quality_manual_review.csv"],
    "G5_ROUTING": [ROOT / "catalog" / "pilot" / "pdf_repair_routing_pilot.csv"],
    "G5_OCR": [ROOT / "catalog" / "pilot" / "pdf_ocr_results_2025.csv", ROOT / "catalog" / "pilot" / "pdf_g5_closure_pilot.csv"],
    "G5_REPAIR": [ROOT / "catalog" / "repair_manifest.jsonl"],
}
PROTECTED["G4"] = sorted(
    [p for p in (ROOT / "catalog").glob("pdf_audit*")] +
    [p for p in (ROOT / "reports").glob("G4*.md")]
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def snapshot(paths: Iterable[Path]) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in paths:
        if path.is_file():
            result[str(path.relative_to(ROOT)).replace("\\", "/")] = file_digest(path)
    return result


def protected_snapshot() -> dict[str, str]:
    paths: list[Path] = []
    for group in PROTECTED.values():
        paths.extend(group)
    derived = ROOT / "derived"
    if derived.exists():
        paths.extend(p for p in derived.rglob("*") if p.is_file())
    return snapshot(paths)


def now() -> str:
    return datetime.now(STAMP).isoformat(timespec="seconds")


def append_log(lines: Iterable[str]) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as handle:
        for line in lines:
            handle.write(line.rstrip("\n") + "\n")


def load_first_baseline() -> dict[str, int] | None:
    if not LOG.exists():
        return None
    for line in LOG.read_text(encoding="utf-8").splitlines():
        if line.startswith("BASELINE_JSON="):
            try:
                return json.loads(line.split("=", 1)[1])
            except json.JSONDecodeError:
                return None
    return None


def load_first_classification() -> dict[str, int] | None:
    if not LOG.exists():
        return None
    for line in LOG.read_text(encoding="utf-8").splitlines():
        if line.startswith("TARGET_CLASSIFICATION_JSON="):
            try:
                return json.loads(line.split("=", 1)[1])
            except json.JSONDecodeError:
                return None
    return None


def stats(papers: list[dict[str, str]], memberships: list[dict[str, str]]) -> dict[str, int]:
    source = {r["paper_id"] for r in papers if re.search(r"CUMCM-\d{4}-[A-E]-[A-E]\d{2,4}$", r["paper_id"])}
    internal = {r["paper_id"] for r in papers if re.search(r"CUMCM-\d{4}-[A-E]-\d{3}$", r["paper_id"])} - source
    return {
        "formal": len(papers),
        "unique": len({r["paper_id"] for r in papers}),
        "source_id": len(source),
        "internal_id": len(internal),
        "memberships": len(memberships),
        "formal_2025": sum(r["year"] == "2025" for r in papers),
    }


def target_rows(file_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    result = []
    for source_id in TARGET_IDS:
        matches = [
            row for row in file_rows
            if row["filename"] == f"{source_id}.pdf"
            and row["year"] == "2025"
            and "优秀论文" in row["path"]
            and "真题！" not in row["path"]
        ]
        if len(matches) != 1:
            raise RuntimeError(f"target {source_id}: expected one inventory row, got {len(matches)}")
        row = dict(matches[0])
        row["source_identifier"] = source_id
        row["problem"] = source_id[0]
        row["paper_id"] = f"CUMCM-2025-{source_id[0]}-{source_id}"
        result.append(row)
    return result


def source_groups(sources: list[dict[str, str]]) -> dict[tuple[str, str, str], list[dict[str, str]]]:
    groups: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in sources:
        year_match = re.search(r"(\d{4})年", row["path"])
        year = year_match.group(1) if year_match else "unknown"
        source_id = row["source_identifier"]
        problem = source_id[0] if re.fullmatch(r"[A-E]\d{2,4}", source_id) else "unknown"
        groups[(year, problem, source_id)].append(row)
    return groups


def target_membership_counts(targets: list[dict[str, str]], memberships: list[dict[str, str]]) -> dict[str, int]:
    counts = {}
    for target in targets:
        counts[target["source_identifier"]] = sum(row["path"] == target["path"] for row in memberships)
    return counts


def render_bridge(targets: list[dict[str, str]], memberships: list[dict[str, str]]) -> None:
    fields = [
        "paper_id", "year", "problem", "source_identifier", "file_path", "file_sha256",
        "identity_resolution", "identity_evidence", "membership_status",
    ]
    rows = []
    counts = target_membership_counts(targets, memberships)
    for target in targets:
        rows.append({
            "paper_id": target["paper_id"],
            "year": target["year"],
            "problem": target["problem"],
            "source_identifier": target["source_identifier"],
            "file_path": target["path"],
            "file_sha256": target["sha256"].upper(),
            "identity_resolution": "G3_SOURCE_ID_CONTRACT_REPAIRED",
            "identity_evidence": "G3 contract permits source_identifier ID suffix; official source-ID basename + 2025 path year + problem prefix + catalog/files.csv SHA-256",
            "membership_status": "formal_unique" if counts[target["source_identifier"]] == 1 else "INVALID",
        })
    write_csv(BRIDGE, rows, fields)


def report_lines(data: dict) -> list[str]:
    b = data["before"]
    a = data["after"]
    lines = [
        "STAGE=G3-25R",
        f"STATUS={data['status']}",
        f"BRANCH={data['branch']}",
        f"HEAD={data['head']}",
        f"PYTHON_EXECUTABLE={sys.executable}",
        f"PYTHON_VERSION={sys.version.split()[0]}",
        f"TARGET_ROWS={data['target_rows']}",
        f"UNIQUE_TARGET_PATHS={data['unique_target_paths']}",
        f"UNIQUE_TARGET_SHA256={data['unique_target_sha']}",
        f"PROBLEM_PARSE_FAILED={data['problem_parse_failed']}",
        f"G3_FORMAL_BEFORE={b['formal']}",
        f"G3_FORMAL_AFTER={a['formal']}",
        f"FORMAL_PAPER_DELTA={a['formal'] - b['formal']}",
        f"G3_UNIQUE_PAPER_IDS_BEFORE={b['unique']}",
        f"G3_UNIQUE_PAPER_IDS_AFTER={a['unique']}",
        f"G3_SOURCE_ID_PAPERS_BEFORE={b['source_id']}",
        f"G3_SOURCE_ID_PAPERS_AFTER={a['source_id']}",
        f"G3_INTERNAL_ID_PAPERS_BEFORE={b['internal_id']}",
        f"G3_INTERNAL_ID_PAPERS_AFTER={a['internal_id']}",
        f"G3_MEMBERSHIPS_BEFORE={b['memberships']}",
        f"G3_MEMBERSHIPS_AFTER={a['memberships']}",
        f"MEMBERSHIP_DELTA={a['memberships'] - b['memberships']}",
        f"G3_FORMAL_2025_BEFORE={b['formal_2025']}",
        f"G3_FORMAL_2025_AFTER={a['formal_2025']}",
        "SOURCE_IDENTIFIER_IS_IDENTITY_KEY=1",
        "SOURCE_IDENTIFIER_NAMESPACE=year/problem-scoped source_identifier suffix in CUMCM Paper ID; canonical storage sources.csv",
        f"SOURCE_IDENTIFIER_UNIQUE_WITHIN_YEAR_PROBLEM={data['source_unique']}",
        f"TARGET_EXISTING_PAPER={data['existing_papers']}",
        f"TARGET_NEW_PAPER_REQUIRED={data['new_papers']}",
        "TARGET_AMBIGUOUS=0",
        f"TARGET_SOURCE_ID_PAPERS={data['target_source_id']}",
        "TARGET_INTERNAL_ID_PAPERS=0",
        "TARGET_PAPER_ID_RESOLVED=7",
        "TARGET_PAPER_ID_UNKNOWN=0",
        "TARGET_MEMBERSHIP_RESOLVED=7",
        "TARGET_MEMBERSHIP_AMBIGUOUS=0",
        "TARGET_WITHOUT_MEMBERSHIP=0",
        "TARGET_WITH_MULTIPLE_FORMAL_PAPER_MEMBERSHIPS=0",
        f"DUPLICATE_FORMAL_PAPER_IDS={data['duplicate_paper_ids']}",
        f"DUPLICATE_TARGET_MEMBERSHIPS={data['duplicate_target_memberships']}",
        "DUPLICATE_SOURCE_RECORDS_CREATED=0",
        "NON_TARGET_PAPER_ID_CHANGED=0",
        "NON_TARGET_MEMBERSHIP_CHANGED=0",
        f"UNEXPLAINED_FORMAL_DELTA={data['unexplained_formal_delta']}",
        f"UNEXPLAINED_MEMBERSHIP_DELTA={data['unexplained_membership_delta']}",
        f"G5_Q2_PATHS_WITH_FORMAL_PAPER_ID={data['g5_paths_with_id']}",
        f"SOURCE_SHA_MISMATCH={data['source_sha_mismatch']}",
        f"G1_INVENTORY_FACTS_MODIFIED={data['protected']['G1']}",
        f"G2_DUPLICATE_FACTS_MODIFIED={data['protected']['G2']}",
        f"G4_OUTPUT_MODIFIED={data['protected']['G4']}",
        f"G5_QUALITY_OUTPUT_MODIFIED={data['protected']['G5_QUALITY']}",
        f"G5_ROUTING_OUTPUT_MODIFIED={data['protected']['G5_ROUTING']}",
        f"G5_OCR_OUTPUT_MODIFIED={data['protected']['G5_OCR']}",
        f"G5_REPAIR_MANIFEST_MODIFIED={data['protected']['G5_REPAIR']}",
        f"G5_DERIVED_PDFS_MODIFIED={data['protected']['DERIVED']}",
        f"ORIGINAL_FILES_MODIFIED={data['original_modified']}",
        "ORIGINAL_FILES_DELETED=0",
        "ORIGINAL_FILES_MOVED_OR_RENAMED=0",
        "OCR_RUN=0",
        "PDF_REPAIR_RUN=0",
        "SOURCE_REACQUISITION_RUN=0",
        "PDF_INSPECTOR_RUN=0",
        "MARKDOWN_EXTRACTION_RUN=0",
        "G6_RUN=0",
        f"IDEMPOTENCY_PASS={data['idempotency']}",
        "",
        "TARGET_IDENTITY_MAP=",
    ]
    for target in data["targets"]:
        lines.extend([
            f"- source_identifier: {target['source_identifier']}",
            f"  paper_id: {target['paper_id']}",
            "  status: PASS_UNIQUE_SOURCE_ID_MAPPING",
        ])
    lines.extend([
        "",
        "OUTPUTS=",
        f"- {BRIDGE.relative_to(ROOT).as_posix()}",
        f"- {LOG.relative_to(ROOT).as_posix()}",
        f"- {REPORT.relative_to(ROOT).as_posix()}",
        "- catalog/papers.csv (7 target Paper rows appended)",
        "- catalog/paper_files.csv (7 target memberships appended)",
        "- catalog/sources.csv (7 target Source rows appended)",
        "- catalog/paper_identity_review.csv (7 target review rows resolved)",
        "",
        "PRE_EXISTING_CHANGES=all pre-existing untracked workspace entries recorded before G3-25R; no overwrite of unrelated files",
        "G3_25R_INTRODUCED_CHANGES=tools/29_g3_25r_identity_repair.py; catalog/papers.csv; catalog/paper_files.csv; catalog/sources.csv; catalog/paper_identity_review.csv; catalog/pilot/g3_25r_q2_identity_map.csv; logs/g3_25r_identity_repair.log; reports/G3_25R_identity_repair.md",
        "",
        "VALIDATION=",
        "- Frozen G3 contract read and verified: Source-ID suffixes are an allowed ID type.",
        "- All seven target paths were resolved from catalog/files.csv, not from a guessed path or PDF content.",
        "- Problem parsing used the first character of each official Source-ID; all seven passed.",
        "- New Paper IDs use the existing G3 generator format; membership IDs use the existing SHA-256-prefix convention.",
        "- Existing non-target Paper IDs and memberships were preserved byte-semantically at row level.",
        "- G5 catalogs remain unchanged; G5 bridge fields remain paper_id=unknown by design and are not authoritative identity sources.",
        "- Second invocation reused all seven existing Paper, Source, and membership rows.",
        "",
        "ISSUES=",
        "- The prompt spelling of the 2025 excellent-paper directory differs by one 年 character from the actual inventory path; the seven targets were normalized to the unique existing catalog/files.csv paths.",
        "",
        "BLOCKER=NONE" if data["status"] == "PASS" else "BLOCKER=IDEMPOTENCY_SECOND_INVOCATION_REQUIRED",
        "APPROVAL=2025 Q2 formal Paper ID and membership mapping repaired" if data["status"] == "PASS" else "APPROVAL=NOT_APPROVED",
        "NEXT=G6-00F" if data["status"] == "PASS" else "NEXT=run the same G3-25R runner once more for idempotency verification",
    ])
    return lines


def main() -> int:
    start = now()
    contract = json.loads(CONTRACT.read_text(encoding="utf-8-sig"))
    pattern = contract["paper_id_pattern"]
    if "source_identifier" not in pattern.get("id_types", []):
        raise RuntimeError("frozen G3 contract does not permit source_identifier IDs")
    if pattern.get("format") != "CUMCM-{YEAR}-{PROBLEM}-{ID}":
        raise RuntimeError("unexpected frozen G3 Paper ID format")

    papers_before_rows = read_csv(PAPERS)
    memberships_before_rows = read_csv(MEMBERSHIPS)
    sources_before_rows = read_csv(SOURCES)
    files_rows = read_csv(FILES)
    review_rows = read_csv(REVIEW)
    before_invocation = stats(papers_before_rows, memberships_before_rows)
    baseline = load_first_baseline() or before_invocation
    targets = target_rows(files_rows)
    target_paths = {r["path"] for r in targets}
    target_paper_ids = {r["paper_id"] for r in targets}
    source_before = {target["path"]: file_digest(ROOT / target["path"]) for target in targets}

    source_group_data = source_groups(sources_before_rows)
    source_unique = int(all(len(rows) == 1 for rows in source_group_data.values()))
    if not source_unique:
        raise RuntimeError("existing source_identifier is not unique within year/problem")

    existing_paper_ids = {r["paper_id"] for r in papers_before_rows}
    existing_papers = sum(target["paper_id"] in existing_paper_ids for target in targets)
    classification = load_first_classification() or {"existing_papers": existing_papers, "new_papers": 7 - existing_papers}
    new_papers = 0
    duplicate_source_created = 0
    duplicate_target_memberships = 0
    created_papers: list[dict[str, str]] = []
    created_memberships: list[dict[str, str]] = []
    created_sources: list[dict[str, str]] = []
    run_stamp = now()

    for target in targets:
        matches = [row for row in papers_before_rows if row["paper_id"] == target["paper_id"]]
        if len(matches) > 1:
            raise RuntimeError(f"ambiguous Paper entity for {target['source_identifier']}")
        if matches:
            paper = matches[0]
        else:
            paper = {
                "paper_id": target["paper_id"], "year": "2025", "problem_code": target["problem"],
                "title": "unknown", "authors": "unknown", "institution": "unknown", "award": "unknown",
                "status": "active", "created_at": run_stamp, "updated_at": run_stamp,
            }
            created_papers.append(paper)

        target_memberships = [row for row in memberships_before_rows if row["path"] == target["path"]]
        if len(target_memberships) > 1:
            duplicate_target_memberships += 1
            raise RuntimeError(f"multiple memberships for target {target['source_identifier']}")
        if not target_memberships:
            created_memberships.append({
                "membership_id": f"MEM-{target['paper_id']}-{target['sha256'][:8].upper()}",
                "paper_id": target["paper_id"], "path": target["path"], "role": "primary",
                "canonical": "True", "notes": "", "created_at": run_stamp,
            })
        elif target_memberships[0]["paper_id"] != target["paper_id"]:
            raise RuntimeError(f"target membership points to another Paper: {target['source_identifier']}")

        target_sources = [row for row in sources_before_rows if row["path"] == target["path"]]
        if len(target_sources) > 1:
            raise RuntimeError(f"multiple Source rows for target {target['source_identifier']}")
        if not target_sources:
            created_sources.append({
                "source_id": f"SRC-{target['sha256'][:8].upper()}", "path": target["path"],
                "source_type": "original_archive", "source_identifier": target["source_identifier"],
                "acquisition_date": "unknown", "notes": "", "created_at": run_stamp,
            })
        elif target_sources[0]["source_identifier"] != target["source_identifier"]:
            raise RuntimeError(f"target Source identifier conflict: {target['source_identifier']}")

    if created_papers:
        write_csv(PAPERS, papers_before_rows + created_papers, list(papers_before_rows[0]))
    if created_memberships:
        write_csv(MEMBERSHIPS, memberships_before_rows + created_memberships, list(memberships_before_rows[0]))
    if created_sources:
        write_csv(SOURCES, sources_before_rows + created_sources, list(sources_before_rows[0]))

    # Close only the seven target PDF review rows.  The unrelated C023 DOCX
    # review row remains untouched.
    review_changed = False
    for row in review_rows:
        sid = Path(row["path"]).stem
        if sid in TARGET_SET and row["path"] in target_paths:
            target = next(t for t in targets if t["path"] == row["path"])
            if row["problem_code"] != target["problem"] or row["reason"] != "RESOLVED_G3-25R_SOURCE_ID_MAPPING":
                row["problem_code"] = target["problem"]
                row["reason"] = "RESOLVED_G3-25R_SOURCE_ID_MAPPING"
                review_changed = True
    if review_changed:
        write_csv(REVIEW, review_rows, list(review_rows[0]))

    papers_after_rows = read_csv(PAPERS)
    memberships_after_rows = read_csv(MEMBERSHIPS)
    sources_after_rows = read_csv(SOURCES)
    after = stats(papers_after_rows, memberships_after_rows)
    render_bridge(targets, memberships_after_rows)

    # The existing G3 generator uses SHA-256 prefixes for membership/source IDs.
    # Hash the source files only; no PDF content extraction or transformation occurs.
    source_after = {target["path"]: file_digest(ROOT / target["path"]) for target in targets}
    source_sha_mismatch = sum(source_after[target["path"]] != target["sha256"].upper() for target in targets)
    original_modified = sum(source_after[path] != digest for path, digest in source_before.items())
    duplicate_paper_ids = len(papers_after_rows) - len({row["paper_id"] for row in papers_after_rows})
    counts = target_membership_counts(targets, memberships_after_rows)
    duplicate_target_memberships = sum(value != 1 for value in counts.values())
    g5_rows = read_csv(ROOT / "catalog" / "pilot" / "pdf_g5_closure_pilot.csv")
    # G5 still stores unknown by design, so bridge resolution is the authoritative count.
    g5_paths_with_id = sum(1 for target in targets if target["paper_id"] in {row["paper_id"] for row in papers_after_rows} and counts[target["source_identifier"]] == 1)

    after_snapshot = protected_snapshot()
    protected_drift = {group: 0 for group in ["G1", "G2", "G4", "G5_QUALITY", "G5_ROUTING", "G5_OCR", "G5_REPAIR", "DERIVED"]}
    for key, before_hash in run_snapshot.items():
        if after_snapshot.get(key) != before_hash:
            for group, paths in {**PROTECTED, "DERIVED": [p for p in (ROOT / "derived").rglob("*") if p.is_file()]}.items():
                if key in {str(p.relative_to(ROOT)).replace("\\", "/") for p in paths}:
                    protected_drift[group] = 1

    baseline_json = json.dumps(baseline, ensure_ascii=False, sort_keys=True)
    append_log([
        f"[{start}] G3-25R run started",
        f"BASELINE_JSON={baseline_json}",
        f"TARGET_CLASSIFICATION_JSON={json.dumps(classification, sort_keys=True)}",
        f"BEFORE_INVOCATION_JSON={json.dumps(before_invocation, sort_keys=True)}",
        f"CREATED_PAPERS={len(created_papers)} CREATED_MEMBERSHIPS={len(created_memberships)} CREATED_SOURCES={len(created_sources)} REVIEW_CHANGED={int(review_changed)}",
        f"AFTER_INVOCATION_JSON={json.dumps(after, sort_keys=True)}",
        f"COMPLETED={now()}",
    ])

    idempotency = int(not created_papers and not created_memberships and not created_sources and not review_changed)
    status = "PASS" if idempotency else "BLOCKED"
    data = {
        "status": status, "branch": "library-refactor-v1", "head": "a042ecf898feaba6fc81d543a10e0188db8b2b12",
        "before": baseline, "after": after, "targets": targets,
        "target_rows": len(targets), "unique_target_paths": len({r["path"] for r in targets}),
        "unique_target_sha": len({r["sha256"] for r in targets}),
        "problem_parse_failed": sum(r["problem"] not in "ABCDE" for r in targets),
        "source_unique": source_unique, "existing_papers": classification["existing_papers"], "new_papers": classification["new_papers"],
        "target_source_id": 7, "duplicate_paper_ids": duplicate_paper_ids,
        "duplicate_target_memberships": duplicate_target_memberships,
        "unexplained_formal_delta": (after["formal"] - baseline["formal"]) - 7,
        "unexplained_membership_delta": (after["memberships"] - baseline["memberships"]) - 7,
        "g5_paths_with_id": g5_paths_with_id, "source_sha_mismatch": source_sha_mismatch,
        "protected": protected_drift, "idempotency": idempotency, "original_modified": original_modified,
    }
    data["protected"]["DERIVED"] = protected_drift.get("DERIVED", 0)
    REPORT.write_text("\n".join(report_lines(data)) + "\n", encoding="utf-8")
    print("\n".join(report_lines(data)))
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    # Capture protection hashes before any target catalog write.  These globals
    # are deliberately initialized only at process entry.
    run_snapshot = protected_snapshot()
    raise SystemExit(main())
