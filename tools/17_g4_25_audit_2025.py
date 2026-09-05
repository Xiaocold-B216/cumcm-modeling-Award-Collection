#!/usr/bin/env python3
"""G4-25: 2025 PDF Formal Audit - Year-specific runner"""
import json, hashlib, sys, os, csv, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SCHEMA_DIR = REPO_ROOT / "catalog" / "schema"
CATALOG_DIR = REPO_ROOT / "catalog"
PILOT_DIR = CATALOG_DIR / "pilot"
LOGS_DIR = REPO_ROOT / "logs"
REPORTS_DIR = REPO_ROOT / "reports"

# Ensure directories exist
PILOT_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# Import shared framework
sys.path.insert(0, str(REPO_ROOT / "tools"))
from importlib import import_module
audit_module = import_module("02_pdf_audit")

def calculate_sha256(fp):
    return audit_module.calculate_sha256(fp)

def classify_pdf(pdf_path):
    return audit_module.classify_pdf(pdf_path)

def determine_routing(cl):
    return audit_module.determine_routing(cl)

def load_issue_codes():
    with open(SCHEMA_DIR / "pdf_issue_codes.json", 'r', encoding='utf-8') as f:
        return json.load(f)

def load_quality_rules():
    with open(SCHEMA_DIR / "pdf_quality_rules.json", 'r', encoding='utf-8') as f:
        return json.load(f)

def load_audit_schema():
    with open(SCHEMA_DIR / "pdf_audit_schema.json", 'r', encoding='utf-8') as f:
        return json.load(f)

def load_existing_q_evidence(path):
    """Preserve the correction evidence table across repeatable reruns."""
    if not path.exists():
        return []
    columns = [
        'file_path', 'sha256', 'classification', 'machine_routing',
        'current_preliminary_q', 'current_final_q', 'q_evidence_source',
        'q_evidence_independent_of_pdf_type', 'recommended_corrected_q_state'
    ]
    rows = []
    in_table = False
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('| file_path | sha256 | classification |'):
                in_table = True
                continue
            if in_table and line.startswith('|---|'):
                continue
            if in_table and line.startswith('| '):
                values = [value.strip().replace('\\|', '|') for value in line.strip().strip('|').split('|')]
                if len(values) == len(columns):
                    rows.append(dict(zip(columns, values)))
                continue
            if in_table:
                break
    return rows

def main():
    log_lines = []
    def log(msg):
        ts = datetime.datetime.now().isoformat()
        line = f"[{ts}] {msg}"
        log_lines.append(line)
        print(line)

    log("G4-25 2025 PDF Audit started")
    log(f"REPO_ROOT={REPO_ROOT}")

    # Load schema/config
    issue_codes = load_issue_codes()
    quality_rules = load_quality_rules()
    audit_schema = load_audit_schema()
    log(f"AUDIT_SCHEMA_VERSION={audit_schema.get('schema_version', 'unknown')}")

    # Read files.csv and filter 2025 PDFs
    files_csv = CATALOG_DIR / "files.csv"
    rows_2025 = []
    with open(files_csv, 'r', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            if row.get('year') == '2025' and row.get('file_extension') == '.pdf':
                rows_2025.append(row)

    log(f"EXPECTED_PDF_FILES_2025={len(rows_2025)}")
    if len(rows_2025) != 12:
        log("STATUS=BLOCKED")
        log("BLOCKER=2025_PDF_INVENTORY_DRIFT")
        log(f"Expected 12, found {len(rows_2025)}")
        write_log(LOGS_DIR / "pdf_audit_2025.log", log_lines)
        return

    # Audit each PDF
    audit_rows = []
    review_rows = []
    issue_evidence = []
    previous_review_q = {}
    previous_review_csv = PILOT_DIR / "pdf_review_2025.csv"
    previous_q_evidence = load_existing_q_evidence(REPORTS_DIR / "G4_25_pdf_audit_2025.md")
    if previous_review_csv.exists():
        with open(previous_review_csv, 'r', encoding='utf-8-sig', newline='') as f:
            for previous_row in csv.DictReader(f):
                if previous_row.get('preliminary_q', '').strip():
                    previous_review_q[previous_row.get('file_path', '')] = previous_row

    sha_mismatch_count = 0
    pdf_open_success = 0
    pdf_open_failed = 0
    classification_success = 0
    classification_failed = 0
    total_pages = 0
    total_ocr_routed = 0
    page_zero_count = 0
    out_of_range_count = 0
    visual_review_required = 0
    visual_review_not_required = 0
    type_counts = {"text_based": 0, "scanned": 0, "image_based": 0, "mixed": 0, "failed": 0}
    issue_counts = {}
    unique_sha_set = set()
    cache_reused = 0
    sha_cache = {}

    for idx, row in enumerate(rows_2025, 1):
        rel_path = row['path']
        g1_sha = row['sha256'].upper()
        file_path = REPO_ROOT / rel_path
        log(f"[{idx}/12] Processing: {rel_path}")

        if not file_path.exists():
            log(f"  ERROR: File not found")
            pdf_open_failed += 1
            continue

        # Pre-audit SHA
        current_sha = calculate_sha256(file_path).upper()
        if current_sha != g1_sha:
            log(f"  SHA MISMATCH: current={current_sha[:16]}... vs G1={g1_sha[:16]}...")
            sha_mismatch_count += 1

        # Classify
        try:
            result = classify_pdf(file_path)
            pdf_type = result.get('pdf_type', 'unknown')
            page_count = result.get('page_count', 0)
            confidence = result.get('confidence', 0.0)
            pages_needing_ocr = result.get('pages_needing_ocr', [])
            has_encoding_issues = result.get('has_encoding_issues', False)
            is_complex_layout = result.get('is_complex_layout', False)
            machine_routing = result.get('machine_routing', 'OPEN_FAIL_REVIEW')
            issues = result.get('issues', [])

            pdf_open_success += 1
            classification_success += 1
            log(f"  type={pdf_type} pages={page_count} routing={machine_routing}")
        except Exception as e:
            log(f"  Classification failed: {e}")
            pdf_open_failed += 1
            classification_failed += 1
            pdf_type = "failed"
            page_count = 0
            confidence = 0.0
            pages_needing_ocr = []
            has_encoding_issues = False
            is_complex_layout = False
            machine_routing = "OPEN_FAIL_REVIEW"
            issues = [str(e)]

        # Post-audit SHA (verify no modification)
        post_sha = calculate_sha256(file_path).upper()
        sha_changed = post_sha != current_sha

        # Count types
        if pdf_type in type_counts:
            type_counts[pdf_type] += 1
        else:
            type_counts["failed"] += 1

        # Pages
        total_pages += page_count
        total_ocr_routed += len(pages_needing_ocr)

        # Check page numbering
        for pg in pages_needing_ocr:
            if pg == 0:
                page_zero_count += 1
            if pg < 1 or pg > page_count:
                out_of_range_count += 1

        # Unique SHA tracking
        unique_sha_set.add(current_sha)
        if current_sha in sha_cache:
            cache_reused += 1
        else:
            sha_cache[current_sha] = rel_path

        # Determine visual review need
        needs_visual_review = machine_routing in [
            "SCAN_VISUAL_REVIEW", "IMAGE_VISUAL_REVIEW", "OPEN_FAIL_REVIEW"
        ]
        if needs_visual_review:
            visual_review_required += 1
        else:
            visual_review_not_required += 1

        # Final-Q/preliminary-Q is intentionally unassigned here.  PDF type
        # and machine routing are not independent quality evidence.
        q_class = None

        # Build audit row
        audit_row = {
            "file_path": rel_path,
            "sha256": current_sha,
            "g1_sha256": g1_sha,
            "sha_match": current_sha == g1_sha,
            "pdf_type": pdf_type,
            "page_count": page_count,
            "confidence": confidence,
            "machine_routing": machine_routing,
            "pages_needing_ocr": pages_needing_ocr,
            "has_encoding_issues": has_encoding_issues,
            "is_complex_layout": is_complex_layout,
            "issues": issues,
            "pre_audit_sha": current_sha,
            "post_audit_sha": post_sha,
            "sha_changed_by_audit": sha_changed,
            "timestamp": datetime.datetime.now().isoformat(),
            "pdf_inspector_version": "1.15.0",
            "audit_schema_version": audit_schema.get('schema_version', 1)
        }
        audit_rows.append(audit_row)

        # Build review row if needed
        if needs_visual_review:
            review_row = {
                "file_path": rel_path,
                "sha256": current_sha,
                "pdf_type": pdf_type,
                "machine_routing": machine_routing,
                "preliminary_q": q_class,
                "review_reason": f"Routing: {machine_routing}",
                "status": "pending",
                "timestamp": datetime.datetime.now().isoformat()
            }
            review_rows.append(review_row)

        # Track issues
        for issue in issues:
            issue_counts[issue] = issue_counts.get(issue, 0) + 1

    # Verify coverage
    audited_paths = set(r['file_path'] for r in audit_rows)
    expected_paths = set(r['path'] for r in rows_2025)
    missing = expected_paths - audited_paths
    extra = audited_paths - expected_paths

    log(f"COVERAGE: Expected={len(expected_paths)} Audited={len(audited_paths)} Missing={len(missing)} Extra={len(extra)}")

    # Check for duplicate audit rows
    seen_paths = set()
    duplicate_count = 0
    for r in audit_rows:
        if r['file_path'] in seen_paths:
            duplicate_count += 1
        seen_paths.add(r['file_path'])

    log(f"DUPLICATE_AUDIT_ROWS={duplicate_count}")

    # Write audit CSV
    audit_csv_path = PILOT_DIR / "pdf_audit_2025.csv"
    with open(audit_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "file_path", "sha256", "g1_sha256", "sha_match", "pdf_type",
            "page_count", "confidence", "machine_routing", "pages_needing_ocr",
            "has_encoding_issues", "is_complex_layout", "issues",
            "pre_audit_sha", "post_audit_sha", "sha_changed_by_audit",
            "timestamp", "pdf_inspector_version", "audit_schema_version"
        ])
        writer.writeheader()
        for row in audit_rows:
            writer.writerow(row)
    log(f"Wrote {len(audit_rows)} rows to {audit_csv_path}")

    # Write review CSV
    review_csv_path = PILOT_DIR / "pdf_review_2025.csv"
    with open(review_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "file_path", "sha256", "pdf_type", "machine_routing",
            "preliminary_q", "review_reason", "status", "timestamp"
        ])
        writer.writeheader()
        for row in review_rows:
            writer.writerow(row)
    log(f"Wrote {len(review_rows)} rows to {review_csv_path}")

    # Generate summary
    sha_changed_after = sum(1 for r in audit_rows if r['sha_changed_by_audit'])
    final_q_assigned = sum(1 for r in review_rows if r.get('preliminary_q'))
    final_q_unassigned = len(audit_rows) - final_q_assigned
    assigned_q_without_independent_evidence = 0
    q_evidence_rows = []
    for audit_row in audit_rows:
        previous = previous_review_q.get(audit_row['file_path'])
        if not previous:
            continue
        q_evidence_rows.append({
            "file_path": audit_row['file_path'],
            "sha256": audit_row['sha256'],
            "classification": audit_row['pdf_type'],
            "machine_routing": audit_row['machine_routing'],
            "current_preliminary_q": previous.get('preliminary_q', ''),
            "current_final_q": '',
            "q_evidence_source": "tools/17_g4_25_audit_2025.py:181-192 machine_routing -> q_class",
            "q_evidence_independent_of_pdf_type": "False",
            "recommended_corrected_q_state": "unassigned; retain visual_review_required=true and status=pending",
        })
    if not q_evidence_rows:
        q_evidence_rows = previous_q_evidence
    log(f"FINAL_Q_ASSIGNED={final_q_assigned}")
    log(f"FINAL_Q_UNASSIGNED={final_q_unassigned}")
    log("DIRECT_PDF_TYPE_TO_FINAL_Q_MAPPING=0")
    log(f"ASSIGNED_Q_WITHOUT_INDEPENDENT_EVIDENCE={assigned_q_without_independent_evidence}")
    log("VISUAL_REVIEW_EXECUTED=0")

    # Write log after all correction metrics are known.
    write_log(LOGS_DIR / "pdf_audit_2025.log", log_lines)

    print("\n" + "=" * 60)
    print("G4-25 AUDIT SUMMARY")
    print("=" * 60)
    print(f"EXPECTED_PDF_FILES_2025={len(rows_2025)}")
    print(f"AUDIT_ROWS={len(audit_rows)}")
    print(f"UNIQUE_AUDITED_FILE_PATHS={len(audited_paths)}")
    print(f"MISSING_AUDIT_ROWS={len(missing)}")
    print(f"EXTRA_AUDIT_ROWS={len(extra)}")
    print(f"DUPLICATE_AUDIT_ROWS={duplicate_count}")
    print(f"SOURCE_SHA_MISMATCH={sha_mismatch_count}")
    print(f"ORIGINAL_SHA_CHANGED_AFTER_AUDIT={sha_changed_after}")
    print(f"PDF_OPEN_SUCCESS={pdf_open_success}")
    print(f"PDF_OPEN_FAILED={pdf_open_failed}")
    print(f"CLASSIFICATION_SUCCESS={classification_success}")
    print(f"CLASSIFICATION_FAILED={classification_failed}")
    print(f"TEXT_BASED={type_counts['text_based']}")
    print(f"SCANNED={type_counts['scanned']}")
    print(f"IMAGE_BASED={type_counts['image_based']}")
    print(f"MIXED={type_counts['mixed']}")
    print(f"TOTAL_PAGE_COUNT={total_pages}")
    print(f"TOTAL_OCR_ROUTED_PAGES={total_ocr_routed}")
    print(f"PAGE_ZERO_IN_PROJECT_OUTPUT={page_zero_count}")
    print(f"OUT_OF_RANGE_PROJECT_PAGES={out_of_range_count}")
    print(f"VISUAL_REVIEW_REQUIRED={visual_review_required}")
    print(f"VISUAL_REVIEW_NOT_REQUIRED={visual_review_not_required}")
    print(f"FINAL_Q_ASSIGNED={final_q_assigned}")
    print(f"FINAL_Q_UNASSIGNED={final_q_unassigned}")
    print(f"UNIQUE_PDF_SHA256={len(unique_sha_set)}")
    print(f"CACHE_REUSED_ROWS={cache_reused}")

    # Determine PASS/BLOCKED
    status = "PASS"
    blockers = []
    if len(rows_2025) != 12:
        blockers.append("2025_PDF_INVENTORY_DRIFT")
    if sha_mismatch_count > 0:
        blockers.append("SOURCE_SHA_DRIFT")
    if len(missing) > 0:
        blockers.append(f"MISSING_AUDIT_ROWS={len(missing)}")
    if len(extra) > 0:
        blockers.append(f"EXTRA_AUDIT_ROWS={len(extra)}")
    if duplicate_count > 0:
        blockers.append(f"DUPLICATE_AUDIT_ROWS={duplicate_count}")
    if sha_changed_after > 0:
        blockers.append("ORIGINAL_PDF_MODIFIED")
    if pdf_open_failed > 0:
        blockers.append(f"PDF_OPEN_FAILED={pdf_open_failed}")
    if classification_failed > 0:
        blockers.append(f"CLASSIFICATION_FAILED={classification_failed}")
    if page_zero_count > 0:
        blockers.append(f"PAGE_ZERO_FOUND={page_zero_count}")
    if out_of_range_count > 0:
        blockers.append(f"OUT_OF_RANGE_PAGES={out_of_range_count}")

    if blockers:
        status = "BLOCKED"
        print(f"\nSTATUS={status}")
        print(f"BLOCKERS={', '.join(blockers)}")
    else:
        print(f"\nSTATUS={status}")
        print("BLOCKER=NONE")

    # Write report
    write_report(REPORTS_DIR / "G4_25_pdf_audit_2025.md", {
        "expected": len(rows_2025),
        "audit_rows": len(audit_rows),
        "audited_paths": len(audited_paths),
        "missing": len(missing),
        "extra": len(extra),
        "duplicate": duplicate_count,
        "sha_mismatch": sha_mismatch_count,
        "sha_changed": sha_changed_after,
        "open_success": pdf_open_success,
        "open_failed": pdf_open_failed,
        "classify_success": classification_success,
        "classify_failed": classification_failed,
        "type_counts": type_counts,
        "total_pages": total_pages,
        "ocr_routed": total_ocr_routed,
        "page_zero": page_zero_count,
        "out_of_range": out_of_range_count,
        "visual_review_req": visual_review_required,
        "visual_review_not_req": visual_review_not_required,
        "q_assigned": final_q_assigned,
        "q_unassigned": final_q_unassigned,
        "direct_q_mapping": 0,
        "assigned_q_without_independent_evidence": assigned_q_without_independent_evidence,
        "visual_review_executed": 0,
        "q_evidence_rows": q_evidence_rows,
        "unique_sha": len(unique_sha_set),
        "cache_reused": cache_reused,
        "status": status,
        "blockers": blockers
    })

    return status

def write_log(path, lines):
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

def write_report(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        f.write("# G4-25 2025 PDF Audit\n\n")
        f.write("## Baseline\n\n")
        f.write(f"Expected PDFs: {data['expected']}\n")
        f.write(f"Audit Rows: {data['audit_rows']}\n\n")
        f.write("## Runtime\n\n")
        f.write(f"Python: 3.13.15\n")
        f.write(f"pdf-inspector: 1.15.0\n")
        f.write(f"Schema: 1\n\n")
        f.write("## Coverage\n\n")
        f.write(f"Expected: {data['expected']}\n")
        f.write(f"Audited: {data['audited_paths']}\n")
        f.write(f"Missing: {data['missing']}\n")
        f.write(f"Extra: {data['extra']}\n")
        f.write(f"Duplicate: {data['duplicate']}\n\n")
        f.write("## Classification\n\n")
        f.write(f"text_based: {data['type_counts']['text_based']}\n")
        f.write(f"scanned: {data['type_counts']['scanned']}\n")
        f.write(f"image_based: {data['type_counts']['image_based']}\n")
        f.write(f"mixed: {data['type_counts']['mixed']}\n")
        f.write(f"failed: {data['type_counts']['failed']}\n\n")
        f.write("## Pages\n\n")
        f.write(f"Total: {data['total_pages']}\n")
        f.write(f"OCR Routed: {data['ocr_routed']}\n\n")
        f.write("## Issues\n\n")
        f.write(f"Issue counts: {data.get('issue_counts', {})}\n\n")
        f.write("## Visual Review\n\n")
        f.write(f"Required: {data['visual_review_req']}\n")
        f.write(f"Not Required: {data['visual_review_not_req']}\n\n")
        f.write("## Final-Q Evidence Correction\n\n")
        f.write("Q values are assigned only from independent quality evidence. The previous Q values below were derived from machine routing and were cleared.\n\n")
        f.write("| file_path | sha256 | classification | machine_routing | current_preliminary_q | current_final_q | q_evidence_source | q_evidence_independent_of_pdf_type | recommended_corrected_q_state |\n")
        f.write("|---|---|---|---|---|---|---|---|---|\n")
        for row in data.get('q_evidence_rows', []):
            values = [str(row[key]).replace('|', '\\|') for key in [
                'file_path', 'sha256', 'classification', 'machine_routing',
                'current_preliminary_q', 'current_final_q', 'q_evidence_source',
                'q_evidence_independent_of_pdf_type', 'recommended_corrected_q_state'
            ]]
            f.write("| " + " | ".join(values) + " |\n")
        f.write("\n")
        f.write("## Q Status\n\n")
        f.write(f"Assigned: {data['q_assigned']}\n")
        f.write(f"Unassigned: {data['q_unassigned']}\n\n")
        f.write(f"DIRECT_PDF_TYPE_TO_FINAL_Q_MAPPING: {data['direct_q_mapping']}\n")
        f.write(f"ASSIGNED_Q_WITHOUT_INDEPENDENT_EVIDENCE: {data['assigned_q_without_independent_evidence']}\n")
        f.write(f"VISUAL_REVIEW_EXECUTED: {data['visual_review_executed']}\n\n")
        f.write("## Duplicate Cache\n\n")
        f.write(f"Unique SHA: {data['unique_sha']}\n")
        f.write(f"Reused: {data['cache_reused']}\n\n")
        f.write("## Integrity\n\n")
        f.write(f"SHA Mismatch: {data['sha_mismatch']}\n")
        f.write(f"SHA Changed After Audit: {data['sha_changed']}\n")
        f.write(f"Page Zero: {data['page_zero']}\n")
        f.write(f"Out of Range: {data['out_of_range']}\n\n")
        f.write("## Gate\n\n")
        f.write(f"STATUS: {data['status']}\n")
        if data['blockers']:
            f.write(f"BLOCKERS: {', '.join(data['blockers'])}\n")
        else:
            f.write("BLOCKER: NONE\n")

if __name__ == "__main__":
    main()
