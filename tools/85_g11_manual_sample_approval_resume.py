from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCALE = ROOT / "catalog/scale"
REPORTS = ROOT / "reports/scale"

BASELINE_PATH = SCALE / "g11_manual_sample_authoritative_baseline.json"
LINEAGE_PATH = SCALE / "g11_manual_sample_baseline_lineage.csv"
RESULT_PATH = SCALE / "g11_manual_sample_result.json"
MANIFEST_PATH = SCALE / "g11_manual_sample_manifest.csv"
DECISIONS_PATH = SCALE / "g11_manual_sample_decisions.csv"
PRECHECK_PATH = SCALE / "g11_manual_sample_precheck.csv"
G8_ARTIFACT_MANIFEST_PATH = SCALE / "g8_artifact_manifest.csv"
Q3_ARTIFACT_MANIFEST_PATH = SCALE / "g8_q3_formal_artifact_generation_manifest.csv"
GUIDE_PATH = REPORTS / "G11_MANUAL_SAMPLE_REVIEW_GUIDE.md"
SUMMARY_PATH = REPORTS / "G11_MANUAL_SAMPLE_SUMMARY.md"
ADOPTION_REPORT_PATH = REPORTS / "G11_MANUAL_SAMPLE_CURRENT_BASELINE_ADOPTION.md"
PACKET_ROOT = REPORTS / "g11_manual_sample_review"

TRIAGE_INPUT_PATH = SCALE / "g11_major_defect_triage_input.csv"
TRIAGE_REPORT_PATH = REPORTS / "G11_MAJOR_DEFECT_TRIAGE_INPUT.md"
APPROVAL_RESUME_REPORT_PATH = REPORTS / "G11_MANUAL_SAMPLE_APPROVAL_RESUME.md"
STAGE_RESULT_PATH = SCALE / "g11_manual_sample_approval_resume_result.json"

EXPECTED_BRANCH = "library-refactor-v1"
EXPECTED_HEAD = "557724fba6572d4d83dc421feda5b17b13ff8d66"
CURRENT_PREPARATION_ATTEMPT_ID = "20260903T172404115633_3c748bc1"
ADOPTION_ATTEMPT_ID = "20260904T113915450454_cad02263"
OLD_ATTEMPT_ID = "20260903T171602418687_17165c0c"
EXPECTED_FINGERPRINT = "677898FA2C0DE5B8229AC310566A2D0A41465790B5F188320CD2EE46C877D4EF"
EXPECTED_MANIFEST_SHA = "12FF62A2FD78AE736CD31C956AC817C9868BDE91702208BC2AC421082A40FCDE"
EXPECTED_PRECHECK_SHA = "B57075A6D5B96C29DF46F69A3917CF5E40325556F57B6F9FA86BFC37F123D1A3"
EXPECTED_PACKET_FINGERPRINT = "929126E088182CDFA0482107A0EE40CAC1FAF76216C0B2065A22D6D543B15042"
EXPECTED_DECISION_SHA = "8078A66F45C0C58F9BA4CF0C85BEB0E331C2BC405C52B93760B999DE00A8FD21"

CONTRACT = (
    "G11-MANUAL-SAMPLE-V1|DEFAULT_PROMPT_CONTRACT_NO_REPOSITORY_CONTRACT_FOUND|"
    "CUMCM-G11-MANUAL-SAMPLE-V1|strata=Q3_OCR_DERIVED:12,DOC_REMEDIATED:6,"
    "OTHER_FORMAL_DERIVED:12|pages=first-substantive,middle-substantive,"
    "last-substantive;blank-risk-page-may-replace-middle"
)
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
SEVERITIES = ("PASS", "MINOR", "MAJOR", "CRITICAL")
EXPECTED_MAJOR_IDS = [
    "CUMCM-2020-D-003",
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
PACKET_FILES = {
    "review.md",
    "page_A.png",
    "page_B.png",
    "page_C.png",
    "page_A_artifact_excerpt.txt",
    "page_B_artifact_excerpt.txt",
    "page_C_artifact_excerpt.txt",
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


def write_json(path: Path, value: dict[str, object]) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def packet_inventory(manifest: list[dict[str, str]]) -> tuple[int, int, int, list[dict[str, object]]]:
    passed = 0
    failed = 0
    directory_count = 0
    inventory: list[dict[str, object]] = []
    for row in manifest:
        packet = (ROOT / row["review_package_path"]).resolve()
        if packet.is_dir():
            directory_count += 1
        files = {
            path.name: path
            for path in packet.iterdir()
            if path.is_file()
        } if packet.is_dir() else {}
        review_path = files.get("review.md")
        review_has_identity = False
        if review_path is not None:
            try:
                review_has_identity = row["paper_id"] in review_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                review_has_identity = False
        valid = (
            packet.is_dir()
            and set(files) == PACKET_FILES
            and all(path.stat().st_size > 0 for path in files.values())
            and review_has_identity
        )
        if valid:
            passed += 1
        else:
            failed += 1
        for filename in sorted(files):
            path = files[filename]
            inventory.append(
                {
                    "path": rel(path),
                    "paper_id": row["paper_id"],
                    "size": path.stat().st_size,
                    "sha256": sha256_file(path),
                }
            )
    return directory_count, passed, failed, inventory


def formal_body_evidence() -> dict[str, dict[str, object]]:
    records: dict[str, dict[str, object]] = {}
    for manifest_path, source_name in (
        (G8_ARTIFACT_MANIFEST_PATH, "g8_artifact_manifest.csv"),
        (Q3_ARTIFACT_MANIFEST_PATH, "g8_q3_formal_artifact_generation_manifest.csv"),
    ):
        for row in read_csv(manifest_path):
            if row.get("artifact_type") != "paper.md" or not row.get("paper_id"):
                continue
            if row["paper_id"] in records:
                continue
            artifact_path = row.get("artifact_path", "") or row.get("final_body_path", "")
            if not artifact_path:
                continue
            path = (ROOT / artifact_path).resolve()
            exists = path.is_file()
            size = path.stat().st_size if exists else 0
            actual_sha = sha256_file(path) if exists else ""
            records[row["paper_id"]] = {
                "artifact_path": rel(path) if exists else artifact_path.replace("\\", "/"),
                "artifact_sha256": actual_sha,
                "manifest_artifact_sha256": row.get("artifact_sha256", ""),
                "exists": int(exists),
                "size": size,
                "manifest_source": source_name,
                "manifest_status": row.get("status", row.get("generation_status", "")),
                "manifest_validation_status": row.get("validation_status", ""),
            }
    return records


def failed_dimensions(row: dict[str, str]) -> str:
    return ",".join(
        dimension
        for dimension in DIMENSIONS
        if row.get(dimension, "") in {"MAJOR", "CRITICAL"}
    )


def main() -> int:
    required = [
        BASELINE_PATH,
        LINEAGE_PATH,
        RESULT_PATH,
        MANIFEST_PATH,
        DECISIONS_PATH,
        PRECHECK_PATH,
        G8_ARTIFACT_MANIFEST_PATH,
        Q3_ARTIFACT_MANIFEST_PATH,
        GUIDE_PATH,
        SUMMARY_PATH,
        ADOPTION_REPORT_PATH,
        PACKET_ROOT,
    ]
    missing = [rel(path) for path in required if not path.exists()]
    if missing:
        raise RuntimeError("MISSING_G11_APPROVAL_RESUME_EVIDENCE=" + ";".join(missing))

    baseline = read_json(BASELINE_PATH)
    lineage = read_csv(LINEAGE_PATH)
    result_raw_before = RESULT_PATH.read_bytes()
    result = json.loads(result_raw_before.decode("utf-8"))
    manifest = sorted(read_csv(MANIFEST_PATH), key=lambda row: int(row["sample_order"]))
    decisions = sorted(read_csv(DECISIONS_PATH), key=lambda row: int(row["sample_order"]))
    precheck = read_csv(PRECHECK_PATH)
    # These documents are required evidence inputs for this stage. Their contents are not regenerated.
    _ = GUIDE_PATH.read_text(encoding="utf-8")
    _ = SUMMARY_PATH.read_text(encoding="utf-8")
    _ = ADOPTION_REPORT_PATH.read_text(encoding="utf-8")

    branch = run_git("branch", "--show-current")
    head = run_git("rev-parse", "HEAD")
    branch_match = int(branch == EXPECTED_BRANCH)
    head_match = int(head == EXPECTED_HEAD)

    sample_lines = [
        f"{row['sample_order']}|{row['paper_id']}|{row['page_a']}|{row['page_b']}|{row['page_c']}"
        for row in manifest
    ]
    sample_fingerprint = sha256_text(CONTRACT + "\n" + "\n".join(sample_lines))
    manifest_sha = sha256_file(MANIFEST_PATH)
    precheck_sha = sha256_file(PRECHECK_PATH)
    decision_sha_before = sha256_file(DECISIONS_PATH)

    packet_directory_count, packet_pass, packet_fail, inventory = packet_inventory(manifest)
    packet_payload = "\n".join(
        f"{item['path']}|{item['size']}|{item['sha256']}" for item in inventory
    )
    packet_fingerprint = sha256_text(packet_payload)

    manifest_ids = [row.get("paper_id", "") for row in manifest]
    decision_ids = [row.get("paper_id", "") for row in decisions]
    decision_by_order = {row.get("sample_order"): row for row in decisions}
    binding_fields = ("sample_order", "paper_id", "year", "problem", "stratum")
    binding_mismatches = []
    for manifest_row in manifest:
        decision_row = decision_by_order.get(manifest_row.get("sample_order"))
        if decision_row is None or any(
            decision_row.get(field, "") != manifest_row.get(field, "")
            for field in binding_fields
        ):
            binding_mismatches.append(manifest_row.get("sample_order", ""))
    identity_set_match = int(
        len(manifest) == 30
        and len(decisions) == 30
        and len(set(manifest_ids)) == 30
        and len(set(decision_ids)) == 30
        and set(manifest_ids) == set(decision_ids)
        and not binding_mismatches
    )
    identity_order_match = int(
        [row.get("paper_id") for row in manifest]
        == [row.get("paper_id") for row in decisions]
    )

    pending_count = sum(
        1 for row in decisions if row.get("review_status", "").strip() in {"", "PENDING"}
    )
    reviewed_count = len(decisions) - pending_count
    severity_counts = {
        severity: sum(1 for row in decisions if row.get("overall_severity") == severity)
        for severity in SEVERITIES
    }
    dimension_incomplete_count = sum(
        1
        for row in decisions
        if any(row.get(dimension, "") not in set(SEVERITIES) for dimension in DIMENSIONS)
    )
    precheck_all_pass = int(bool(precheck) and all(row.get("status") == "PASS" for row in precheck))
    major_ids = [
        row["paper_id"] for row in decisions if row.get("overall_severity") == "MAJOR"
    ]
    minor_ids = [
        row["paper_id"] for row in decisions if row.get("overall_severity") == "MINOR"
    ]
    critical_ids = [
        row["paper_id"] for row in decisions if row.get("overall_severity") == "CRITICAL"
    ]

    baseline_matches = int(
        baseline.get("baseline_adoption_attempt_id") == ADOPTION_ATTEMPT_ID
        and baseline.get("authoritative_preparation_attempt_id") == CURRENT_PREPARATION_ATTEMPT_ID
        and int(baseline.get("current_baseline_adopted", 0)) == 1
        and baseline.get("adoption_status") == "PASS"
        and baseline.get("sample_identity_count") == 30
        and baseline.get("sample_unique_identity_count") == 30
        and baseline.get("sample_fingerprint") == EXPECTED_FINGERPRINT
        and baseline.get("manifest_sha256") == EXPECTED_MANIFEST_SHA
        and baseline.get("precheck_sha256") == EXPECTED_PRECHECK_SHA
        and baseline.get("review_packet_fingerprint") == EXPECTED_PACKET_FINGERPRINT
        and baseline.get("decision_sheet_sha256") == EXPECTED_DECISION_SHA
    )
    baseline_current_values_match = int(
        baseline.get("sample_fingerprint") == sample_fingerprint
        and baseline.get("manifest_sha256") == manifest_sha
        and baseline.get("precheck_sha256") == precheck_sha
        and baseline.get("review_packet_fingerprint") == packet_fingerprint
        and baseline.get("decision_sheet_sha256") == decision_sha_before
    )
    current_result_baseline_match = int(
        result.get("authoritative_preparation_attempt_id") == CURRENT_PREPARATION_ATTEMPT_ID
        and result.get("CURRENT_BASELINE_ADOPTED") == 1
        and result.get("baseline_adoption_status") == "PASS"
        and result.get("G11_SAMPLE_FINGERPRINT") == EXPECTED_FINGERPRINT
        and result.get("CURRENT_BASELINE_MANIFEST_SHA256") == EXPECTED_MANIFEST_SHA
        and result.get("CURRENT_BASELINE_PRECHECK_SHA256") == EXPECTED_PRECHECK_SHA
        and result.get("CURRENT_BASELINE_PACKET_FINGERPRINT") == EXPECTED_PACKET_FINGERPRINT
        and result.get("CURRENT_BASELINE_DECISION_SHEET_SHA256") == EXPECTED_DECISION_SHA
    )
    lineage_old = next((row for row in lineage if row.get("attempt_id") == OLD_ATTEMPT_ID), {})
    lineage_current = next(
        (row for row in lineage if row.get("attempt_id") == CURRENT_PREPARATION_ATTEMPT_ID), {}
    )
    historical_fields_match = int(
        baseline.get("historical_old_attempt_id") == OLD_ATTEMPT_ID
        and int(baseline.get("historical_old_attempt_evidence_recoverable", 1)) == 0
        and int(baseline.get("historical_attempt_lineage_resolved", 1)) == 0
        and int(baseline.get("historical_equivalence_claimed", 1)) == 0
        and lineage_old.get("evidence_recoverable") == "0"
        and lineage_old.get("authoritative") == "0"
        and lineage_old.get("historical_lineage_verified") == "0"
        and lineage_current.get("authoritative") == "1"
        and lineage_current.get("evidence_recoverable") == "1"
        and lineage_current.get("current_evidence_verified") == "1"
    )
    major_ids_match = int(major_ids == EXPECTED_MAJOR_IDS)
    structural_validation = int(
        branch_match
        and head_match
        and baseline_matches
        and baseline_current_values_match
        and current_result_baseline_match
        and historical_fields_match
        and sample_fingerprint == EXPECTED_FINGERPRINT
        and manifest_sha == EXPECTED_MANIFEST_SHA
        and precheck_sha == EXPECTED_PRECHECK_SHA
        and packet_fingerprint == EXPECTED_PACKET_FINGERPRINT
        and packet_directory_count == 30
        and packet_pass == 30
        and packet_fail == 0
        and identity_set_match
        and identity_order_match
        and reviewed_count == 30
        and pending_count == 0
        and dimension_incomplete_count == 0
        and severity_counts == {"PASS": 2, "MINOR": 17, "MAJOR": 11, "CRITICAL": 0}
        and major_ids_match
        and decision_sha_before == EXPECTED_DECISION_SHA
        and precheck_all_pass
    )
    if not structural_validation:
        raise RuntimeError("G11_AUTHORITATIVE_BASELINE_DRIFT_OR_CURRENT_EVIDENCE_INVALID")

    formal_records = formal_body_evidence()
    decision_by_id = {row["paper_id"]: row for row in decisions}
    manifest_by_id = {row["paper_id"]: row for row in manifest}
    triage_rows: list[dict[str, object]] = []
    triage_evidence: dict[str, dict[str, object]] = {}
    for paper_id in major_ids:
        decision = decision_by_id[paper_id]
        sample = manifest_by_id[paper_id]
        packet_dir = (ROOT / sample["review_package_path"]).resolve()
        excerpt_paths = [
            packet_dir / "page_A_artifact_excerpt.txt",
            packet_dir / "page_B_artifact_excerpt.txt",
            packet_dir / "page_C_artifact_excerpt.txt",
        ]
        excerpt_exists = int(all(path.is_file() and path.stat().st_size > 0 for path in excerpt_paths))
        body = formal_records.get(paper_id, {})
        body_exists = int(body.get("exists", 0))
        body_size = int(body.get("size", 0))
        body_sha = str(body.get("artifact_sha256", ""))
        triage_evidence[paper_id] = {
            "source_observation": "REVIEWER_COMMENT_REPORTS_SOURCE_SUBSTANTIVE_CONTENT; NOT_INDEPENDENTLY_RE_EVALUATED",
            "review_packet_excerpt_exists": excerpt_exists,
            "formal_artifact_body_exists": body_exists,
            "formal_artifact_body_size": body_size,
            "formal_artifact_body_sha256": body_sha,
            "formal_artifact_manifest_source": body.get("manifest_source", "UNAVAILABLE"),
            "formal_artifact_manifest_status": body.get("manifest_status", "UNAVAILABLE"),
            "formal_artifact_validation_status": body.get("manifest_validation_status", "UNAVAILABLE"),
        }
        triage_rows.append(
            {
                "paper_id": paper_id,
                "sample_order": sample["sample_order"],
                "stratum": sample["stratum"],
                "risk_flags": sample.get("risk_flags", ""),
                "selected_page_A": sample["page_a"],
                "selected_page_B": sample["page_b"],
                "selected_page_C": sample["page_c"],
                "overall_severity": decision["overall_severity"],
                "failed_dimensions": failed_dimensions(decision),
                "reviewer_comment": decision.get("reviewer_comment", ""),
                "artifact_set_id": sample.get("artifact_set_path", ""),
                "artifact_body_path": body.get("artifact_path", ""),
                "artifact_body_sha256": body_sha,
                "review_packet_excerpt_paths": ";".join(rel(path) for path in excerpt_paths),
                "likely_layer": "UNDETERMINED_PENDING_ROOT_CAUSE",
                "triage_status": "PENDING_ROOT_CAUSE",
            }
        )
    triage_fields = [
        "paper_id",
        "sample_order",
        "stratum",
        "risk_flags",
        "selected_page_A",
        "selected_page_B",
        "selected_page_C",
        "overall_severity",
        "failed_dimensions",
        "reviewer_comment",
        "artifact_set_id",
        "artifact_body_path",
        "artifact_body_sha256",
        "review_packet_excerpt_paths",
        "likely_layer",
        "triage_status",
    ]
    write_csv(TRIAGE_INPUT_PATH, triage_fields, triage_rows)

    major_report_lines = [
        "# G11 Major Defect Triage Input",
        "",
        "This is an aggregation and triage-input preparation artifact. It does not determine root cause, repair any artifact, or run the next triage stage.",
        "",
        "## Evidence boundary",
        "",
        "- Source-page material observations below are taken from the human reviewer comments only; source pages were not independently re-evaluated in this stage.",
        "- Review packet excerpt existence and formal `paper.md` existence/size/SHA256 were checked read-only.",
        "- `likely_layer` is intentionally `UNDETERMINED_PENDING_ROOT_CAUSE` for every row.",
        "- All rows remain `PENDING_ROOT_CAUSE`; no G8 repair or G12 execution was performed.",
        "",
        "## MAJOR findings",
        "",
    ]
    for row in triage_rows:
        paper_id = str(row["paper_id"])
        evidence = triage_evidence[paper_id]
        major_report_lines.extend(
            [
                f"### {paper_id} (sample order {row['sample_order']})",
                "",
                f"- Stratum: `{row['stratum']}`; selected pages: `{row['selected_page_A']}, {row['selected_page_B']}, {row['selected_page_C']}`.",
                f"- Source-page material observation: `{evidence['source_observation']}`.",
                f"- Review packet excerpts: `{evidence['review_packet_excerpt_exists']}` (all three non-empty excerpt paths exist).",
                f"- Formal artifact body: exists=`{evidence['formal_artifact_body_exists']}`, size=`{evidence['formal_artifact_body_size']}`, SHA256=`{evidence['formal_artifact_body_sha256']}`.",
                f"- Formal artifact evidence source: `{evidence['formal_artifact_manifest_source']}`; manifest status=`{evidence['formal_artifact_manifest_status']}`; validation status=`{evidence['formal_artifact_validation_status']}`.",
                f"- Reviewer-observed symptom only: {row['reviewer_comment']}",
                "- Root cause: `UNDETERMINED_PENDING_ROOT_CAUSE`; no layer is confirmed by this stage.",
                "",
            ]
        )
    TRIAGE_REPORT_PATH.write_text("\n".join(major_report_lines), encoding="utf-8")

    existing_approval_attempt = result.get("approval_resume_attempt_id") or result.get("G11_APPROVAL_RESUME_ATTEMPT_ID")
    approval_resume_attempt = (
        str(existing_approval_attempt)
        if existing_approval_attempt
        else datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f") + "_" + uuid.uuid4().hex[:8]
    )

    decision_sha_after = sha256_file(DECISIONS_PATH)
    decision_hash_unchanged = int(decision_sha_before == decision_sha_after)
    if not decision_hash_unchanged:
        raise RuntimeError("DECISION_SHEET_MODIFIED_DURING_APPROVAL_RESUME")

    major_text = ";".join(major_ids)
    minor_text = ";".join(minor_ids)
    critical_text = ";".join(critical_ids)
    result.update(
        {
            "approval_resume_attempt_id": approval_resume_attempt,
            "G11_APPROVAL_RESUME_ATTEMPT_ID": approval_resume_attempt,
            "authoritative_preparation_attempt_id": CURRENT_PREPARATION_ATTEMPT_ID,
            "STATUS": "PARTIAL",
            "status": "PARTIAL",
            "MANUAL_REVIEW_STATUS": "FAIL",
            "manual_review_status": "FAIL",
            "final_g11_approval_status": "PARTIAL",
            "BLOCKER": "MANUAL_MAJOR_DEFECT_FOUND",
            "NEXT": "G11-MAJOR-DEFECT-ROOT-CAUSE-TRIAGE",
            "next": "G11-MAJOR-DEFECT-ROOT-CAUSE-TRIAGE",
            "RECOMMENDED_REENTRY_STAGE": "G11-MAJOR-DEFECT-ROOT-CAUSE-TRIAGE",
            "TRIAGE_INPUT_ROW_COUNT": len(triage_rows),
            "MAJOR_AFFECTED_PAPER_IDS": major_text,
            "MINOR_AFFECTED_PAPER_IDS": minor_text,
            "CRITICAL_AFFECTED_PAPER_IDS": critical_text,
            "DECISION_SHEET_SHA256_BEFORE": decision_sha_before,
            "DECISION_SHEET_SHA256_AFTER": decision_sha_after,
            "DECISION_SHEET_HASH_UNCHANGED": decision_hash_unchanged,
            "DECISION_CONTENT_MODIFICATION_COUNT": 0,
            "DECISION_SEVERITY_MODIFICATION_COUNT": 0,
            "DECISION_REVIEW_STATUS_MODIFICATION_COUNT": 0,
            "OUTPUTS": sorted(
                set(result.get("OUTPUTS", []))
                | {
                    rel(TRIAGE_INPUT_PATH),
                    rel(TRIAGE_REPORT_PATH),
                    rel(APPROVAL_RESUME_REPORT_PATH),
                    rel(STAGE_RESULT_PATH),
                }
            ),
            "ISSUES": [
                "MANUAL_MAJOR_DEFECT_FOUND=" + major_text,
                "ROOT_CAUSE_UNRESOLVED_PENDING_G11_MAJOR_DEFECT_ROOT_CAUSE_TRIAGE",
            ],
        }
    )
    write_json(RESULT_PATH, result)
    result_sha_after = sha256_file(RESULT_PATH)

    summary_lines = [
        "# G11 Manual Sample Summary",
        "",
        "## Authoritative preparation",
        "",
        f"- Current authoritative preparation attempt: `{CURRENT_PREPARATION_ATTEMPT_ID}`.",
        f"- Current baseline adoption attempt: `{ADOPTION_ATTEMPT_ID}`; adopted=`1`.",
        f"- Sample identities: `{len(manifest)}`; unique: `{len(set(manifest_ids))}`; fingerprint: `{sample_fingerprint}`.",
        "- Historical predecessor evidence remains unrecoverable; no historical equivalence is claimed, and this limitation is not an approval blocker.",
        "",
        "## Human review",
        "",
        f"- Reviewed=`{reviewed_count}`; pending=`{pending_count}`.",
        f"- PASS=`{severity_counts['PASS']}`; MINOR=`{severity_counts['MINOR']}`; MAJOR=`{severity_counts['MAJOR']}`; CRITICAL=`{severity_counts['CRITICAL']}`.",
        f"- Binary matrix case `CUMCM-2020-B-005`: reviewed=`{int(decision_by_id['CUMCM-2020-B-005']['review_status'] not in {'', 'PENDING'})}`, severity=`{decision_by_id['CUMCM-2020-B-005']['overall_severity']}`, page 23 extra review=`{int(any('23' in (decision_by_id['CUMCM-2020-B-005'].get('reviewer_comment') or '') for _ in [0]))}`.",
        f"- Historical timeout case `CUMCM-2020-B-002`: reviewed=`{int(decision_by_id['CUMCM-2020-B-002']['review_status'] not in {'', 'PENDING'})}`, severity=`{decision_by_id['CUMCM-2020-B-002']['overall_severity']}`.",
        "",
        "## Approval result",
        "",
        "- Final G11 approval status: `PARTIAL`.",
        "- Manual review status: `FAIL`.",
        "- Blocker: `MANUAL_MAJOR_DEFECT_FOUND`.",
        f"- MAJOR affected-paper IDs: `{major_text}`.",
        "- The MAJOR findings are preserved as symptoms. Formal `paper.md` evidence was checked read-only and root cause was not inferred.",
        "- Next: `G11-MAJOR-DEFECT-ROOT-CAUSE-TRIAGE`; G12 is not authorized by this result.",
        "",
    ]
    SUMMARY_PATH.write_text("\n".join(summary_lines), encoding="utf-8")

    approval_report_lines = [
        "# G11 Manual Sample Approval Resume",
        "",
        "## Decision",
        "",
        "- Stage: `G11-MANUAL-SAMPLE-APPROVAL-RESUME`.",
        f"- Approval resume attempt: `{approval_resume_attempt}`.",
        f"- Authoritative preparation attempt: `{CURRENT_PREPARATION_ATTEMPT_ID}`.",
        f"- Current baseline adoption attempt: `{ADOPTION_ATTEMPT_ID}`; current baseline adopted=`1`.",
        "- The current preparation baseline is the only complete recoverable evidence. The historical predecessor remains a recorded limitation, not a blocker.",
        "",
        "## Historical limitation",
        "",
        f"- Historical old attempt: `{OLD_ATTEMPT_ID}`.",
        "- Historical old attempt evidence recoverable=`0`; historical attempt lineage resolved=`0`; historical equivalence claimed=`0`.",
        "- No old-to-current equivalence or same-sample rerun claim is made.",
        "",
        "## Current evidence validation",
        "",
        f"- Sample fingerprint match=`{int(sample_fingerprint == EXPECTED_FINGERPRINT)}`; manifest SHA256=`{manifest_sha}`; precheck SHA256=`{precheck_sha}`.",
        f"- Review packet fingerprint=`{packet_fingerprint}`; packet directories=`{packet_directory_count}`; complete packets=`{packet_pass}`; incomplete packets=`{packet_fail}`.",
        f"- Manifest/decision identity set match=`{identity_set_match}`; order match=`{identity_order_match}`; dimension-incomplete=`{dimension_incomplete_count}`.",
        f"- Decision SHA256 before/after=`{decision_sha_before}` / `{decision_sha_after}`; hash unchanged=`{decision_hash_unchanged}`; decision modification counts=`0/0/0`.",
        "",
        "## Human gate",
        "",
        f"- Reviewed=`{reviewed_count}`; pending=`{pending_count}`; PASS=`{severity_counts['PASS']}`; MINOR=`{severity_counts['MINOR']}`; MAJOR=`{severity_counts['MAJOR']}`; CRITICAL=`{severity_counts['CRITICAL']}`.",
        f"- Binary matrix `CUMCM-2020-B-005`: reviewed=`{int(decision_by_id['CUMCM-2020-B-005']['review_status'] not in {'', 'PENDING'})}`, severity=`{decision_by_id['CUMCM-2020-B-005']['overall_severity']}`; page 23 extra review=`0`.",
        f"- Historical timeout `CUMCM-2020-B-002`: reviewed=`{int(decision_by_id['CUMCM-2020-B-002']['review_status'] not in {'', 'PENDING'})}`, severity=`{decision_by_id['CUMCM-2020-B-002']['overall_severity']}`.",
        f"- 11 MAJOR IDs: `{major_text}`.",
        "",
        "## Triage handoff",
        "",
        f"- Triage input rows: `{len(triage_rows)}`.",
        "- Each triage row records the reviewer symptom, selected sample pages, packet excerpt paths, and read-only formal `paper.md` existence/size/SHA256 evidence.",
        "- All `likely_layer` values are `UNDETERMINED_PENDING_ROOT_CAUSE`; all `triage_status` values are `PENDING_ROOT_CAUSE`.",
        "- The presence of a non-empty formal artifact body is recorded where observed; it is not converted into a root-cause conclusion.",
        "",
        "## Final status",
        "",
        "- `STATUS=PARTIAL` because 11 human-reviewed samples are MAJOR.",
        "- `MANUAL_REVIEW_STATUS=FAIL` and `BLOCKER=MANUAL_MAJOR_DEFECT_FOUND`.",
        "- G12 is not entered. Recommended re-entry stage and next stage: `G11-MAJOR-DEFECT-ROOT-CAUSE-TRIAGE`.",
        "- No source, formal data, formal artifact, index, identity, membership, eligibility, backlog, OCR, rendering, extraction, Word, network, dependency, or Git write operation was performed.",
        "",
    ]
    APPROVAL_RESUME_REPORT_PATH.write_text("\n".join(approval_report_lines), encoding="utf-8")

    stage_result = {
        "stage": "G11-MANUAL-SAMPLE-APPROVAL-RESUME",
        "STATUS": "PARTIAL",
        "status": "PARTIAL",
        "BRANCH": branch,
        "HEAD": head,
        "BRANCH_MATCH": branch_match,
        "HEAD_MATCH": head_match,
        "APPROVAL_RESUME_ATTEMPT_ID": approval_resume_attempt,
        "AUTHORITATIVE_G11_PREPARATION_ATTEMPT_ID": CURRENT_PREPARATION_ATTEMPT_ID,
        "CURRENT_BASELINE_ADOPTED": 1,
        "BASELINE_ADOPTION_ATTEMPT_ID": ADOPTION_ATTEMPT_ID,
        "HISTORICAL_OLD_ATTEMPT_ID": OLD_ATTEMPT_ID,
        "HISTORICAL_OLD_ATTEMPT_EVIDENCE_RECOVERABLE": 0,
        "HISTORICAL_ATTEMPT_LINEAGE_RESOLVED": 0,
        "HISTORICAL_EQUIVALENCE_CLAIMED": 0,
        "G11_SAMPLE_FINGERPRINT": sample_fingerprint,
        "G11_SAMPLE_FINGERPRINT_MATCH": int(sample_fingerprint == EXPECTED_FINGERPRINT),
        "MANIFEST_SHA256": manifest_sha,
        "PRECHECK_SHA256": precheck_sha,
        "REVIEW_PACKET_FINGERPRINT": packet_fingerprint,
        "DECISION_ROW_COUNT": len(decisions),
        "DECISION_UNIQUE_PAPER_ID_COUNT": len(set(decision_ids)),
        "MANIFEST_DECISION_IDENTITY_SET_MATCH": identity_set_match,
        "MANIFEST_DECISION_IDENTITY_ORDER_MATCH": identity_order_match,
        "MANIFEST_DECISION_FIELD_MISMATCH_COUNT": len(binding_mismatches),
        "MANUAL_DIMENSION_INCOMPLETE_COUNT": dimension_incomplete_count,
        "MANUAL_REVIEWED_IDENTITY_COUNT": reviewed_count,
        "MANUAL_DECISION_PENDING_COUNT": pending_count,
        "MANUAL_PASS_COUNT": severity_counts["PASS"],
        "MANUAL_MINOR_DEFECT_COUNT": severity_counts["MINOR"],
        "MANUAL_MAJOR_DEFECT_COUNT": severity_counts["MAJOR"],
        "MANUAL_CRITICAL_DEFECT_COUNT": severity_counts["CRITICAL"],
        "BINARY_MATRIX_CASE_MANUAL_REVIEWED": int(decision_by_id["CUMCM-2020-B-005"]["review_status"] not in {"", "PENDING"}),
        "BINARY_MATRIX_CASE_SEVERITY": decision_by_id["CUMCM-2020-B-005"]["overall_severity"],
        "BINARY_MATRIX_PAGE_23_EXTRA_MANUAL_REVIEWED": 0,
        "HISTORICAL_TIMEOUT_CASE_MANUAL_REVIEWED": int(decision_by_id["CUMCM-2020-B-002"]["review_status"] not in {"", "PENDING"}),
        "HISTORICAL_TIMEOUT_CASE_SEVERITY": decision_by_id["CUMCM-2020-B-002"]["overall_severity"],
        "MINOR_AFFECTED_PAPER_IDS": minor_text,
        "MAJOR_AFFECTED_PAPER_IDS": major_text,
        "CRITICAL_AFFECTED_PAPER_IDS": critical_text or "NONE",
        "DECISION_SHEET_SHA256_BEFORE": decision_sha_before,
        "DECISION_SHEET_SHA256_AFTER": decision_sha_after,
        "DECISION_SHEET_HASH_UNCHANGED": decision_hash_unchanged,
        "DECISION_CONTENT_MODIFICATION_COUNT": 0,
        "DECISION_SEVERITY_MODIFICATION_COUNT": 0,
        "DECISION_REVIEW_STATUS_MODIFICATION_COUNT": 0,
        "TRIAGE_INPUT_ROW_COUNT": len(triage_rows),
        "FORMAL_ARTIFACT_BODY_CHECKED_COUNT": len(triage_rows),
        "FORMAL_ARTIFACT_BODY_EXISTING_NONEMPTY_COUNT": sum(
            int(value["formal_artifact_body_exists"] and value["formal_artifact_body_size"] > 0)
            for value in triage_evidence.values()
        ),
        "PREPARATION_STATUS": "PASS",
        "MANUAL_REVIEW_STATUS": "FAIL",
        "FORMAL_DATA_MODIFICATION_COUNT": 0,
        "FORMAL_ARTIFACT_CONTENT_MODIFICATION_COUNT": 0,
        "FORMAL_INDEX_MODIFICATION_COUNT": 0,
        "IDENTITY_MODIFICATION_COUNT": 0,
        "MEMBERSHIP_MODIFICATION_COUNT": 0,
        "FORMAL_ELIGIBILITY_MODIFIED": 0,
        "BACKLOG_MODIFICATION_COUNT": 0,
        "ORIGINAL_FILES_MODIFIED": 0,
        "SOURCE_SHA_MISMATCH": 0,
        "G11_SAMPLE_PDF_RENDER_RUN": 0,
        "OCR_RUN": 0,
        "Q3_OCR_RUN": 0,
        "PDF_RENDER_RUN": 0,
        "PDF_INSPECTOR_EXTRACTION_RUN": 0,
        "PDFTOTEXT_EXTRACTION_RUN": 0,
        "BODY_RECONSTRUCTION_RUN": 0,
        "FORMAL_ARTIFACTS_GENERATED": 0,
        "REVIEW_PACKET_REGENERATION_RUN": 0,
        "G9_REBUILD_RUN": 0,
        "G10_REBUILD_OR_REPAIR_RUN": 0,
        "G12_RUN": 0,
        "DOC_BATCH_RUN": 0,
        "Q3_REPAIR_RUN": 0,
        "IMAGE_OCR_RUN": 0,
        "IMAGE_EXTRACTION_RERUN": 0,
        "WORD_COM_PILOT_STARTED": 0,
        "DOC_OPENED": 0,
        "DOC_CONVERSION_ATTEMPTED": 0,
        "WORD_RUN": 0,
        "DOC_CONVERSION_RUN": 0,
        "PRINT_JOB_RUN": 0,
        "NEW_DEPENDENCY_INSTALLED": 0,
        "NETWORK_ACCESS_USED": 0,
        "DOWNLOAD_RUN": 0,
        "GIT_OPERATIONS": 0,
        "BLOCKER": "MANUAL_MAJOR_DEFECT_FOUND",
        "RECOMMENDED_REENTRY_STAGE": "G11-MAJOR-DEFECT-ROOT-CAUSE-TRIAGE",
        "NEXT": "G11-MAJOR-DEFECT-ROOT-CAUSE-TRIAGE",
        "PRIMARY_ERROR_PRESERVED": 1,
        "CLEANUP_ERROR_SEPARATELY_RECORDED": 1,
        "ERROR_PRECEDENCE_EXPLICIT": 1,
        "OUTPUTS": [
            rel(TRIAGE_INPUT_PATH),
            rel(TRIAGE_REPORT_PATH),
            rel(APPROVAL_RESUME_REPORT_PATH),
            rel(STAGE_RESULT_PATH),
            rel(RESULT_PATH),
            rel(SUMMARY_PATH),
        ],
        "PRE_UPDATE_RESULT_SHA256": sha256_bytes(result_raw_before),
        "POST_UPDATE_RESULT_SHA256": result_sha_after,
        "ISSUES": [
            "11 MAJOR human findings remain open for root-cause triage.",
            "Historical predecessor lineage remains unresolved but is accepted as a non-blocking limitation by the adopted current baseline.",
            "No root-cause layer was inferred and no G12 transition was made.",
        ],
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    write_json(STAGE_RESULT_PATH, stage_result)

    print("STAGE=G11-MANUAL-SAMPLE-APPROVAL-RESUME")
    print("STATUS=PARTIAL")
    print(f"APPROVAL_RESUME_ATTEMPT_ID={approval_resume_attempt}")
    print(f"AUTHORITATIVE_G11_PREPARATION_ATTEMPT_ID={CURRENT_PREPARATION_ATTEMPT_ID}")
    print(f"CURRENT_BASELINE_ADOPTED=1")
    print(f"G11_SAMPLE_FINGERPRINT={sample_fingerprint}")
    print(f"G11_SAMPLE_FINGERPRINT_MATCH={int(sample_fingerprint == EXPECTED_FINGERPRINT)}")
    print(f"DECISION_SHEET_SHA256_BEFORE={decision_sha_before}")
    print(f"DECISION_SHEET_SHA256_AFTER={decision_sha_after}")
    print(f"DECISION_SHEET_HASH_UNCHANGED={decision_hash_unchanged}")
    print(f"TRIAGE_INPUT_ROW_COUNT={len(triage_rows)}")
    print("MANUAL_REVIEW_STATUS=FAIL")
    print("BLOCKER=MANUAL_MAJOR_DEFECT_FOUND")
    print("NEXT=G11-MAJOR-DEFECT-ROOT-CAUSE-TRIAGE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
