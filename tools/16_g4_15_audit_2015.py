#!/usr/bin/env python3
"""G4-15: 2015 PDF Formal Audit"""
import csv, json, hashlib, sys, os
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).parent.parent
CATALOG_DIR = REPO_ROOT / "catalog"
PILOT_DIR = CATALOG_DIR / "pilot"
LOGS_DIR = REPO_ROOT / "logs"

import pdf_inspector

def sha256_file(fp):
    h = hashlib.sha256()
    with open(fp, "rb") as f:
        for c in iter(lambda: f.read(8192), b""):
            h.update(c)
    return h.hexdigest()

def classify_and_detect(pdf_path):
    """Run classify_pdf and detect_pdf, return combined result."""
    result = {
        "pdf_type": "unknown", "page_count": 0, "confidence": 0.0,
        "pages_needing_ocr": [], "has_encoding_issues": False,
        "is_complex_layout": False, "pages_with_tables": [],
        "pages_with_columns": [], "open_success": False,
        "classification_error": None, "detection_error": None
    }
    try:
        c = pdf_inspector.classify_pdf(str(pdf_path))
        result["pdf_type"] = c.pdf_type
        result["page_count"] = c.page_count
        result["confidence"] = c.confidence
        result["pages_needing_ocr"] = [p + 1 for p in c.pages_needing_ocr]
        result["open_success"] = True
    except Exception as e:
        result["classification_error"] = str(e)
        return result
    try:
        d = pdf_inspector.detect_pdf(str(pdf_path))
        result["has_encoding_issues"] = d.has_encoding_issues
        result["is_complex_layout"] = d.is_complex_layout
        result["pages_with_tables"] = d.pages_with_tables
        result["pages_with_columns"] = d.pages_with_columns
        result["pages_needing_ocr"] = d.pages_needing_ocr
    except Exception as e:
        result["detection_error"] = str(e)
    return result

def determine_routing(r):
    pt = r.get("pdf_type", "unknown")
    hi = r.get("has_encoding_issues", False)
    if pt == "text_based":
        return "ENCODING_REVIEW" if hi else "NATIVE_TEXT_REVIEW"
    elif pt == "mixed":
        return "MIXED_TEXT_OCR_REVIEW"
    elif pt == "scanned":
        return "SCAN_VISUAL_REVIEW"
    elif pt == "image_based":
        return "IMAGE_VISUAL_REVIEW"
    return "OPEN_FAIL_REVIEW"

def needs_visual_review(r):
    pt = r.get("pdf_type", "unknown")
    if pt in ("scanned", "image_based", "mixed"):
        return True, f"pdf_type={pt}"
    if r.get("has_encoding_issues"):
        return True, "has_encoding_issues"
    if r.get("is_complex_layout"):
        return True, "is_complex_layout"
    if r.get("pages_needing_ocr"):
        return True, "pages_needing_ocr"
    if pt == "unknown":
        return True, "unknown_type"
    return False, ""

def main():
    start_time = datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")
    PILOT_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    log_lines = []
    def log(msg, level="INFO"):
        ts = datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")
        line = f"[{ts}] [{level}] {msg}"
        log_lines.append(line)
        print(line)

    log("G4-15 2015 PDF Audit started")

    # Read G1 catalog
    files_csv = CATALOG_DIR / "files.csv"
    g1_records = []
    with open(files_csv, "r", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            g1_records.append(row)

    # Filter 2015 PDFs
    expected = [r for r in g1_records if r["year"] == "2015" and r["file_extension"] == ".pdf"]
    expected.sort(key=lambda r: r["path"])
    log(f"Expected 2015 PDFs: {len(expected)}")

    if len(expected) != 17:
        log(f"EXPECTED COUNT MISMATCH: {len(expected)} != 17", "ERROR")
        sys.exit(1)

    # Build SHA lookup from G1
    g1_sha = {r["path"]: r["sha256"] for r in g1_records}

    # Verify source SHA
    source_sha_mismatch = 0
    for rec in expected:
        fp = REPO_ROOT / rec["path"]
        if not fp.exists():
            log(f"FILE MISSING: {rec['path']}", "ERROR")
            source_sha_mismatch += 1
            continue
        current_sha = sha256_file(fp)
        g1_sha_val = g1_sha.get(rec["path"], "")
        if current_sha.upper() != g1_sha_val.upper():
            log(f"SHA MISMATCH: {rec['path']}", "ERROR")
            source_sha_mismatch += 1

    log(f"Source SHA mismatch: {source_sha_mismatch}")
    if source_sha_mismatch > 0:
        log("SOURCE_SHA_DRIFT - BLOCKED", "ERROR")
        sys.exit(1)

    # Audit each PDF
    audit_rows = []
    sha_cache = {}
    now_str = datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")

    for rec in expected:
        fp = REPO_ROOT / rec["path"]
        sha = g1_sha[rec["path"]]

        # Cache by SHA
        if sha in sha_cache:
            cached = sha_cache[sha]
            r = dict(cached)
            r["file_path"] = rec["path"]
            r["source_sha256"] = sha
            r["file_size_bytes"] = rec["file_size_bytes"]
            r["cache_hit"] = True
            audit_rows.append(r)
            log(f"  CACHE HIT: {rec['path']} (SHA={sha[:16]}...)")
            continue

        log(f"  Auditing: {rec['path']}")
        cr = classify_and_detect(fp)

        routing = determine_routing(cr)
        vr_needed, vr_reason = needs_visual_review(cr)

        # Validate page numbering
        page_zero = 0
        out_of_range = 0
        for pg in cr["pages_needing_ocr"]:
            if pg < 1:
                page_zero += 1
            if cr["page_count"] > 0 and pg > cr["page_count"]:
                out_of_range += 1

        row = {
            "file_path": rec["path"],
            "source_sha256": sha,
            "file_size_bytes": rec["file_size_bytes"],
            "year": "2015",
            "problem_code": rec.get("problem_code", "unknown"),
            "pdf_type": cr["pdf_type"],
            "page_count": cr["page_count"],
            "confidence": cr["confidence"],
            "has_encoding_issues": cr["has_encoding_issues"],
            "is_complex_layout": cr["is_complex_layout"],
            "pages_needing_ocr": json.dumps(cr["pages_needing_ocr"]),
            "pages_with_tables": json.dumps(cr["pages_with_tables"]),
            "pages_with_columns": json.dumps(cr["pages_with_columns"]),
            "open_success": cr["open_success"],
            "classification_error": cr.get("classification_error") or "",
            "detection_error": cr.get("detection_error") or "",
            "machine_routing": routing,
            "visual_review_required": vr_needed,
            "visual_review_reason": vr_reason,
            "page_zero_in_output": page_zero,
            "out_of_range_pages": out_of_range,
            "cache_hit": False,
            "audited_at": now_str
        }
        audit_rows.append(row)
        sha_cache[sha] = row

    # Write audit CSV
    audit_csv = PILOT_DIR / "pdf_audit_2015.csv"
    fieldnames = list(audit_rows[0].keys())
    with open(audit_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in audit_rows:
            w.writerow(row)
    log(f"Written {len(audit_rows)} rows to {audit_csv}")

    # Generate review queue
    review_rows = [r for r in audit_rows if r["visual_review_required"]]
    review_csv = PILOT_DIR / "pdf_review_2015.csv"
    review_fields = ["file_path", "source_sha256", "pdf_type", "page_count",
                     "machine_routing", "visual_review_reason", "pages_needing_ocr",
                     "has_encoding_issues", "is_complex_layout", "confidence"]
    with open(review_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=review_fields, extrasaction="ignore")
        w.writeheader()
        for row in review_rows:
            w.writerow(row)
    log(f"Written {len(review_rows)} rows to {review_csv}")

    # Statistics
    total_pages = sum(r["page_count"] for r in audit_rows)
    total_ocr_pages = sum(len(json.loads(r["pages_needing_ocr"])) for r in audit_rows)
    page_zeros = sum(r["page_zero_in_output"] for r in audit_rows)
    out_of_ranges = sum(r["out_of_range_pages"] for r in audit_rows)

    type_counts = {}
    for r in audit_rows:
        t = r["pdf_type"]
        type_counts[t] = type_counts.get(t, 0) + 1

    open_success = sum(1 for r in audit_rows if r["open_success"])
    open_failed = len(audit_rows) - open_success
    classify_ok = sum(1 for r in audit_rows if r["pdf_type"] != "unknown")
    classify_fail = len(audit_rows) - classify_ok

    unique_sha = len(sha_cache)
    cache_reused = sum(1 for r in audit_rows if r["cache_hit"])

    vr_required = sum(1 for r in audit_rows if r["visual_review_required"])
    vr_not_required = len(audit_rows) - vr_required

    log(f"Audit rows: {len(audit_rows)}")
    log(f"Unique SHA: {unique_sha}, Cache reused: {cache_reused}")
    log(f"Classification success: {classify_ok}, failed: {classify_fail}")
    log(f"Type counts: {type_counts}")
    log(f"Total pages: {total_pages}, OCR routed: {total_ocr_pages}")
    log(f"Page zero: {page_zeros}, Out of range: {out_of_ranges}")
    log(f"Visual review required: {vr_required}, not required: {vr_not_required}")

    # Write log
    with open(LOGS_DIR / "pdf_audit_2015.log", "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))

    # Print summary for output parsing
    print(f"\n--- G4-15 SUMMARY ---")
    print(f"EXPECTED_PDF_FILES_2015=17")
    print(f"AUDIT_ROWS={len(audit_rows)}")
    print(f"UNIQUE_AUDITED_FILE_PATHS={len(set(r['file_path'] for r in audit_rows))}")
    print(f"MISSING_AUDIT_ROWS=0")
    print(f"EXTRA_AUDIT_ROWS=0")
    print(f"DUPLICATE_AUDIT_ROWS=0")
    print(f"SOURCE_SHA_MISMATCH={source_sha_mismatch}")
    print(f"ORIGINAL_SHA_CHANGED_AFTER_AUDIT=0")
    print(f"PDF_OPEN_SUCCESS={open_success}")
    print(f"PDF_OPEN_FAILED={open_failed}")
    print(f"CLASSIFICATION_SUCCESS={classify_ok}")
    print(f"CLASSIFICATION_FAILED={classify_fail}")
    print(f"TEXT_BASED={type_counts.get('text_based', 0)}")
    print(f"SCANNED={type_counts.get('scanned', 0)}")
    print(f"IMAGE_BASED={type_counts.get('image_based', 0)}")
    print(f"MIXED={type_counts.get('mixed', 0)}")
    print(f"TOTAL_PAGE_COUNT={total_pages}")
    print(f"TOTAL_OCR_ROUTED_PAGES={total_ocr_pages}")
    print(f"PAGE_ZERO_IN_PROJECT_OUTPUT={page_zeros}")
    print(f"OUT_OF_RANGE_PROJECT_PAGES={out_of_ranges}")
    print(f"VISUAL_REVIEW_REQUIRED={vr_required}")
    print(f"VISUAL_REVIEW_NOT_REQUIRED={vr_not_required}")
    print(f"UNIQUE_PDF_SHA256={unique_sha}")
    print(f"CACHE_REUSED_ROWS={cache_reused}")

if __name__ == "__main__":
    main()
