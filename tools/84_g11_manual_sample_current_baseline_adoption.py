from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / "catalog/scale/g11_manual_sample_result.json"
MANIFEST_PATH = ROOT / "catalog/scale/g11_manual_sample_manifest.csv"
DECISIONS_PATH = ROOT / "catalog/scale/g11_manual_sample_decisions.csv"
PRECHECK_PATH = ROOT / "catalog/scale/g11_manual_sample_precheck.csv"
RECONCILE_RESULT_PATH = ROOT / "catalog/scale/g11_manual_sample_preparation_reconcile_result.json"
LINEAGE_INPUT_PATH = ROOT / "catalog/scale/g11_manual_sample_attempt_lineage.csv"
GUIDE_PATH = ROOT / "reports/scale/G11_MANUAL_SAMPLE_REVIEW_GUIDE.md"
SUMMARY_PATH = ROOT / "reports/scale/G11_MANUAL_SAMPLE_SUMMARY.md"
PACKET_ROOT = ROOT / "reports/scale/g11_manual_sample_review"
BASELINE_PATH = ROOT / "catalog/scale/g11_manual_sample_authoritative_baseline.json"
LINEAGE_PATH = ROOT / "catalog/scale/g11_manual_sample_baseline_lineage.csv"
REPORT_PATH = ROOT / "reports/scale/G11_MANUAL_SAMPLE_CURRENT_BASELINE_ADOPTION.md"

EXPECTED_BRANCH = "library-refactor-v1"
EXPECTED_HEAD = "557724fba6572d4d83dc421feda5b17b13ff8d66"
OLD_ATTEMPT_ID = "20260903T171602418687_17165c0c"
CURRENT_ATTEMPT_ID = "20260903T172404115633_3c748bc1"
EXPECTED_FINGERPRINT = "677898FA2C0DE5B8229AC310566A2D0A41465790B5F188320CD2EE46C877D4EF"
EXPECTED_MANIFEST_SHA = "12FF62A2FD78AE736CD31C956AC817C9868BDE91702208BC2AC421082A40FCDE"
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


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest().upper()


def run_git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def packet_check(manifest: list[dict[str, str]]) -> tuple[int, int, list[dict[str, object]]]:
    passed = 0
    failed = 0
    inventory: list[dict[str, object]] = []
    for row in manifest:
        packet = (ROOT / row["review_package_path"]).resolve()
        try:
            packet.relative_to(ROOT.resolve())
        except ValueError:
            failed += 1
            continue
        files = {path.name: path for path in packet.iterdir() if path.is_file()} if packet.is_dir() else {}
        review_text = files.get("review.md")
        ok = (
            packet.is_dir()
            and set(files) == PACKET_FILES
            and all(path.stat().st_size > 0 for path in files.values())
            and review_text is not None
            and row["paper_id"] in review_text.read_text(encoding="utf-8")
        )
        if ok:
            passed += 1
        else:
            failed += 1
        for filename in sorted(files):
            path = files[filename]
            inventory.append(
                {
                    "path": path.relative_to(ROOT).as_posix(),
                    "paper_id": row["paper_id"],
                    "size": path.stat().st_size,
                    "sha256": sha256_file(path),
                }
            )
    return passed, failed, inventory


def main() -> int:
    required = [
        RESULT_PATH,
        MANIFEST_PATH,
        DECISIONS_PATH,
        PRECHECK_PATH,
        RECONCILE_RESULT_PATH,
        LINEAGE_INPUT_PATH,
        GUIDE_PATH,
        SUMMARY_PATH,
        PACKET_ROOT,
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        raise RuntimeError("MISSING_CURRENT_EVIDENCE=" + ";".join(missing))

    result_raw = RESULT_PATH.read_bytes()
    result = json.loads(result_raw.decode("utf-8"))
    manifest = sorted(read_csv(MANIFEST_PATH), key=lambda row: int(row["sample_order"]))
    decisions = sorted(read_csv(DECISIONS_PATH), key=lambda row: int(row["sample_order"]))
    precheck = read_csv(PRECHECK_PATH)
    reconcile_result = json.loads(RECONCILE_RESULT_PATH.read_text(encoding="utf-8"))
    _ = read_csv(LINEAGE_INPUT_PATH)

    branch = run_git("branch", "--show-current")
    head = run_git("rev-parse", "HEAD")
    branch_match = int(branch == EXPECTED_BRANCH)
    head_match = int(head == EXPECTED_HEAD)

    sample_lines = [
        f"{row['sample_order']}|{row['paper_id']}|{row['page_a']}|{row['page_b']}|{row['page_c']}"
        for row in manifest
    ]
    current_fingerprint = sha256_text(CONTRACT + "\n" + "\n".join(sample_lines))
    current_manifest_sha = sha256_file(MANIFEST_PATH)
    current_precheck_sha = sha256_file(PRECHECK_PATH)
    preparation_result_sha = sha256_text(result_raw.decode("utf-8"))
    decision_before = sha256_file(DECISIONS_PATH)

    packet_pass, packet_fail, packet_inventory = packet_check(manifest)
    packet_payload = "\n".join(
        f"{item['path']}|{item['size']}|{item['sha256']}" for item in packet_inventory
    )
    current_packet_fingerprint = sha256_text(packet_payload)
    packet_directory_count = len(
        [path for path in PACKET_ROOT.iterdir() if path.is_dir()]
    )

    manifest_ids = [row.get("paper_id", "") for row in manifest]
    decision_ids = [row.get("paper_id", "") for row in decisions]
    binding_fields = ("sample_order", "paper_id", "year", "problem", "stratum")
    binding_mismatches = []
    decision_by_order = {row.get("sample_order"): row for row in decisions}
    for manifest_row in manifest:
        decision_row = decision_by_order.get(manifest_row.get("sample_order"))
        if decision_row is None or any(
            decision_row.get(field, "") != manifest_row.get(field, "") for field in binding_fields
        ):
            binding_mismatches.append(manifest_row.get("sample_order", ""))
    identity_set_match = int(
        len(manifest) == 30
        and len(decisions) == 30
        and len(set(manifest_ids)) == 30
        and len(set(decision_ids)) == 30
        and set(manifest_ids) == set(decision_ids)
    )
    identity_order_match = int(
        len(manifest) == len(decisions)
        and [row.get("paper_id") for row in manifest] == [row.get("paper_id") for row in decisions]
    )

    pending_count = sum(1 for row in decisions if row.get("review_status", "").strip() in ("", "PENDING"))
    reviewed_count = sum(1 for row in decisions if row.get("review_status", "").strip() not in ("", "PENDING"))
    severity_counts = {
        severity: sum(1 for row in decisions if row.get("overall_severity") == severity)
        for severity in ("PASS", "MINOR", "MAJOR", "CRITICAL")
    }
    dimension_incomplete_count = sum(
        1
        for row in decisions
        if any(row.get(dimension, "") not in {"PASS", "MINOR", "MAJOR", "CRITICAL"} for dimension in DIMENSIONS)
    )
    precheck_all_pass = int(bool(precheck) and all(row.get("status") == "PASS" for row in precheck))
    current_result_candidate_match = int(
        result.get("G11_ATTEMPT_ID") == CURRENT_ATTEMPT_ID
        and result.get("G11_SAMPLE_IDENTITY_COUNT") == 30
        and result.get("G11_SAMPLE_UNIQUE_IDENTITY_COUNT") == 30
        and result.get("G11_SAMPLE_FINGERPRINT") == EXPECTED_FINGERPRINT
        and result.get("PREPARATION_STATUS") == "PASS"
    )
    reconcile_history_read = int(
        reconcile_result.get("OLD_ATTEMPT_ID") == OLD_ATTEMPT_ID
        and reconcile_result.get("CURRENT_STORED_ATTEMPT_ID") == CURRENT_ATTEMPT_ID
        and reconcile_result.get("ATTEMPT_LINEAGE_RESOLVED") == 0
        and reconcile_result.get("OLD_PACKET_FINGERPRINT_RECOVERABLE") == 0
    )
    major_ids_current = [
        row.get("paper_id") for row in decisions if row.get("overall_severity") == "MAJOR"
    ]
    major_ids_unchanged = int(major_ids_current == EXPECTED_MAJOR_IDS)
    all_current_valid = int(
        branch_match
        and head_match
        and current_fingerprint == EXPECTED_FINGERPRINT
        and current_manifest_sha == EXPECTED_MANIFEST_SHA
        and current_packet_fingerprint == EXPECTED_PACKET_FINGERPRINT
        and len(manifest) == 30
        and len(set(manifest_ids)) == 30
        and packet_directory_count == 30
        and identity_set_match
        and identity_order_match
        and not binding_mismatches
        and packet_pass == 30
        and packet_fail == 0
        and precheck_all_pass
        and current_result_candidate_match
        and reconcile_history_read
        and reviewed_count == 30
        and pending_count == 0
        and severity_counts == {"PASS": 2, "MINOR": 17, "MAJOR": 11, "CRITICAL": 0}
        and dimension_incomplete_count == 0
        and decision_before == EXPECTED_DECISION_SHA
        and major_ids_unchanged
    )

    existing_baseline = None
    if BASELINE_PATH.exists():
        existing_baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    adoption_attempt = (
        existing_baseline.get("baseline_adoption_attempt_id")
        if existing_baseline and existing_baseline.get("authoritative_preparation_attempt_id") == CURRENT_ATTEMPT_ID
        else datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f") + "_" + uuid.uuid4().hex[:8]
    )
    created_at = (
        existing_baseline.get("created_at")
        if existing_baseline and existing_baseline.get("baseline_adoption_attempt_id") == adoption_attempt
        else datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    )

    status = "PASS" if all_current_valid else "BLOCKED"
    blocker = "NONE" if all_current_valid else "CURRENT_G11_PREPARATION_DRIFT"
    next_stage = "G11-MANUAL-SAMPLE-APPROVAL-RESUME" if all_current_valid else "G11-MANUAL-SAMPLE-CURRENT-BASELINE-ADOPTION"

    baseline = {
        "baseline_version": "G11-CURRENT-BASELINE-V1",
        "baseline_adoption_attempt_id": adoption_attempt,
        "repo_branch": branch,
        "repo_head": head,
        "authoritative_preparation_attempt_id": CURRENT_ATTEMPT_ID if all_current_valid else "",
        "sample_identity_count": len(manifest),
        "sample_unique_identity_count": len(set(manifest_ids)),
        "sample_fingerprint": current_fingerprint,
        "manifest_sha256": current_manifest_sha,
        "precheck_sha256": current_precheck_sha,
        "preparation_result_sha256": preparation_result_sha,
        "review_packet_fingerprint": current_packet_fingerprint,
        "decision_sheet_sha256": decision_before,
        "manual_reviewed_identity_count": reviewed_count,
        "manual_pending_count": pending_count,
        "manual_pass_count": severity_counts["PASS"],
        "manual_minor_count": severity_counts["MINOR"],
        "manual_major_count": severity_counts["MAJOR"],
        "manual_critical_count": severity_counts["CRITICAL"],
        "historical_old_attempt_id": OLD_ATTEMPT_ID,
        "historical_old_attempt_evidence_recoverable": 0,
        "historical_attempt_lineage_resolved": 0,
        "historical_equivalence_claimed": 0,
        "current_baseline_adopted": int(all_current_valid),
        "adoption_status": status,
        "adoption_reason": (
            "The historical predecessor evidence is unrecoverable. No equivalence between the historical attempt and current attempt is asserted. "
            "The current stored preparation is the only complete recoverable G11 preparation evidence. The completed human decision sheet is directly bound to this current preparation. "
            "Therefore the current preparation is explicitly adopted as the authoritative G11 preparation baseline."
        ),
        "created_at": created_at,
    }
    BASELINE_PATH.write_text(json.dumps(baseline, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lineage_fields = [
        "attempt_id",
        "role",
        "evidence_recoverable",
        "authoritative",
        "historical_lineage_verified",
        "current_evidence_verified",
        "status",
        "evidence_scope",
        "notes",
    ]
    lineage_rows = [
        {
            "attempt_id": OLD_ATTEMPT_ID,
            "role": "HISTORICAL_REFERENCE",
            "evidence_recoverable": 0,
            "authoritative": 0,
            "historical_lineage_verified": 0,
            "current_evidence_verified": "UNAVAILABLE",
            "status": "HISTORICAL_UNRECOVERABLE",
            "evidence_scope": "No old attempt/result/checkpoint/manifest/precheck/packet/log evidence found",
            "notes": "Retained as historical reference; no equivalence or supersession claim is made.",
        },
        {
            "attempt_id": CURRENT_ATTEMPT_ID,
            "role": "AUTHORITATIVE_CURRENT_BASELINE",
            "evidence_recoverable": 1 if all_current_valid else 0,
            "authoritative": 1 if all_current_valid else 0,
            "historical_lineage_verified": 0,
            "current_evidence_verified": 1 if all_current_valid else 0,
            "status": "ADOPTED" if all_current_valid else "CANDIDATE",
            "evidence_scope": "Current result/manifest/precheck/decision/packet evidence",
            "notes": "Current state is adopted without asserting historical equivalence.",
        },
    ]
    write_csv(LINEAGE_PATH, lineage_fields, lineage_rows)

    result_before_update = sha256_file(RESULT_PATH)
    if all_current_valid:
        result.update(
            {
                "authoritative_preparation_attempt_id": CURRENT_ATTEMPT_ID,
                "baseline_adoption_status": "PASS",
                "baseline_adoption_attempt_id": adoption_attempt,
                "historical_old_attempt_id": OLD_ATTEMPT_ID,
                "historical_lineage_status": "UNRESOLVED_ACCEPTED_LIMITATION",
                "CURRENT_BASELINE_ADOPTED": 1,
                "HISTORICAL_OLD_ATTEMPT_EVIDENCE_RECOVERABLE": 0,
                "HISTORICAL_ATTEMPT_LINEAGE_RESOLVED": 0,
                "HISTORICAL_EQUIVALENCE_CLAIMED": 0,
                "CURRENT_BASELINE_MANIFEST_SHA256": current_manifest_sha,
                "CURRENT_BASELINE_PRECHECK_SHA256": current_precheck_sha,
                "CURRENT_BASELINE_PACKET_FINGERPRINT": current_packet_fingerprint,
                "CURRENT_BASELINE_DECISION_SHEET_SHA256": decision_before,
            }
        )
        RESULT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    result_after_update = sha256_file(RESULT_PATH)

    decision_after = sha256_file(DECISIONS_PATH)
    if decision_after != decision_before:
        raise RuntimeError("DECISION_SHEET_CHANGED_DURING_ADOPTION")

    report_lines = [
        "# G11 Manual Sample Current Baseline Adoption",
        "",
        "## Decision",
        "",
        f"- Status: `{status}`",
        f"- Baseline adoption attempt: `{adoption_attempt}`",
        f"- Blocker: `{blocker}`",
        f"- Next: `{next_stage}`",
        "- `G11-MANUAL-SAMPLE-APPROVAL-RESUME` was not executed.",
        "",
        "## Historical limitation accepted",
        "",
        f"- Historical old attempt: `{OLD_ATTEMPT_ID}`.",
        "- Historical old attempt evidence recoverable: `0`.",
        "- Historical attempt lineage resolved: `0`.",
        "- Historical equivalence claimed: `0`.",
        "- The old attempt cannot remain a mandatory approval baseline because its machine-readable result, manifest, precheck, packet tree, checkpoint, and log evidence are unavailable.",
        "- Reconciliation is not repeated. No claim is made that the old attempt and current attempt are the same sample or a same-sample rerun/refinalization.",
        "",
        "## Current preparation validation",
        "",
        f"- Current stored attempt: `{CURRENT_ATTEMPT_ID}`.",
        f"- Sample identities: `{len(manifest)}`; unique: `{len(set(manifest_ids))}`; packet directories: `{packet_directory_count}`.",
        f"- Sample fingerprint: `{current_fingerprint}`.",
        f"- Manifest SHA256: `{current_manifest_sha}`.",
        f"- Precheck SHA256: `{current_precheck_sha}`; all current prechecks PASS=`{precheck_all_pass}`.",
        f"- Preparation result SHA256 before adoption fields: `{preparation_result_sha}`.",
        f"- Review packet fingerprint: `{current_packet_fingerprint}`; packet binding pass/fail=`{packet_pass}/{packet_fail}`.",
        f"- Manifest/decision identity set/order match=`{identity_set_match}/{identity_order_match}`; field mismatch count=`{len(binding_mismatches)}`.",
        "",
        "## Human decision binding",
        "",
        f"- Decision SHA256 before/after: `{decision_before}` / `{decision_after}`.",
        f"- Reviewed=`{reviewed_count}`, pending=`{pending_count}`, PASS=`{severity_counts['PASS']}`, MINOR=`{severity_counts['MINOR']}`, MAJOR=`{severity_counts['MAJOR']}`, CRITICAL=`{severity_counts['CRITICAL']}`.",
        f"- Dimension-incomplete count=`{dimension_incomplete_count}`.",
        f"- MAJOR affected-paper IDs unchanged=`{major_ids_unchanged}`.",
        "- The 11 MAJOR findings are preserved and not repaired in this stage.",
        "",
        "## Adoption rule",
        "",
        "- The current stored preparation is the only complete recoverable G11 preparation evidence.",
        "- The completed human decision sheet is directly bound to this current preparation by sample order, paper ID, year, problem, and stratum.",
        f"- Authoritative G11 preparation attempt adopted: `{CURRENT_ATTEMPT_ID}`.",
        "- This adoption does not resolve historical lineage and does not claim historical equivalence.",
        "",
        "## No-op boundary",
        "",
        "- Formal data, formal artifact content, formal index, identity, membership, eligibility, backlog, and original source modification counts are `0`.",
        "- OCR, Q3 OCR, PDF render/extraction, body reconstruction, formal artifact generation, review packet regeneration, G9, G10, G12, Word, network, download, dependency installation, and write Git operations are `0`.",
        "",
        "## Outputs",
        "",
        f"- `{BASELINE_PATH.relative_to(ROOT)}`",
        f"- `{LINEAGE_PATH.relative_to(ROOT)}`",
        f"- `{REPORT_PATH.relative_to(ROOT)}`",
        f"- Updated governance fields in `{RESULT_PATH.relative_to(ROOT)}` only.",
        "",
        "## Handoff",
        "",
        f"- The next Approval Resume must use source attempt `{CURRENT_ATTEMPT_ID}`.",
        "- Proceed only to `G11-MANUAL-SAMPLE-APPROVAL-RESUME`; do not execute G8 repair or G12 from this stage.",
    ]
    REPORT_PATH.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(f"STATUS={status}")
    print(f"BASELINE_ADOPTION_ATTEMPT={adoption_attempt}")
    print(f"CURRENT_BASELINE_ADOPTED={int(all_current_valid)}")
    print(f"CURRENT_RESULT_SHA_BEFORE={result_before_update}")
    print(f"CURRENT_RESULT_SHA_AFTER={result_after_update}")
    print(f"CURRENT_FINGERPRINT={current_fingerprint}")
    print(f"CURRENT_PACKET_FINGERPRINT={current_packet_fingerprint}")
    print(f"DECISION_HASH_UNCHANGED={int(decision_before == decision_after)}")
    print(f"BLOCKER={blocker}")
    print(f"NEXT={next_stage}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
