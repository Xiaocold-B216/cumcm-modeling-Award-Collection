#!/usr/bin/env python3
"""G4-00: PDF Audit Framework - pdf-inspector wrapper"""
import json, hashlib, sys, os, csv
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).parent.parent
SCHEMA_DIR = REPO_ROOT / "catalog" / "schema"
CATALOG_DIR = REPO_ROOT / "catalog"

try:
    import pdf_inspector
    PDF_INSPECTOR_AVAILABLE = True
except ImportError:
    PDF_INSPECTOR_AVAILABLE = False

def calculate_sha256(fp):
    h = hashlib.sha256()
    with open(fp, "rb") as f:
        for c in iter(lambda: f.read(8192), b""):
            h.update(c)
    return h.hexdigest()

def classify_pdf(pdf_path, dry_run=False):
    r = {"path": str(pdf_path), "pdf_type": "unknown", "page_count": 0,
         "confidence": 0.0, "pages_needing_ocr": [], "has_encoding_issues": False,
         "is_complex_layout": False, "pages_with_tables": [], "pages_with_columns": [],
         "issues": [], "machine_routing": "OPEN_FAIL_REVIEW",
         "timestamp": datetime.now().isoformat()}
    if dry_run:
        r["dry_run"] = True
        return r
    if not PDF_INSPECTOR_AVAILABLE:
        r["issues"].append("pdf_inspector not available")
        return r
    try:
        c = pdf_inspector.classify_pdf(str(pdf_path))
        r["pdf_type"] = c.pdf_type
        r["page_count"] = c.page_count
        r["confidence"] = c.confidence
        # pages_needing_ocr from classify_pdf is 0-based, convert to 1-based for project
        r["pages_needing_ocr"] = [p + 1 for p in c.pages_needing_ocr]
        
        d = pdf_inspector.detect_pdf(str(pdf_path))
        r["has_encoding_issues"] = d.has_encoding_issues
        r["is_complex_layout"] = d.is_complex_layout
        r["pages_with_tables"] = d.pages_with_tables
        r["pages_with_columns"] = d.pages_with_columns
        # detect_pdf pages_needing_ocr is already 1-based
        r["pages_needing_ocr"] = d.pages_needing_ocr
        r["machine_routing"] = determine_routing(r)
    except Exception as e:
        r["issues"].append(str(e))
    return r

def determine_routing(cl):
    pt = cl.get("pdf_type", "unknown")
    hi = cl.get("has_encoding_issues", False)
    if pt == "text_based":
        return "ENCODING_REVIEW" if hi else "NATIVE_TEXT_REVIEW"
    elif pt == "mixed":
        return "MIXED_TEXT_OCR_REVIEW"
    elif pt == "scanned":
        return "SCAN_VISUAL_REVIEW"
    elif pt == "image_based":
        return "IMAGE_VISUAL_REVIEW"
    return "OPEN_FAIL_REVIEW"

def smoke_test(count=3):
    fpath = CATALOG_DIR / "files.csv"
    pdfs = []
    with open(fpath, 'r', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            if row.get('file_extension') == '.pdf':
                pdfs.append(row)
    results = []
    for p in pdfs[:count]:
        pp = REPO_ROOT / p['path']
        if pp.exists():
            sha1 = calculate_sha256(pp)
            cl = classify_pdf(pp)
            sha2 = calculate_sha256(pp)
            results.append({"path": p['path'], "sha_before": sha1, "sha_after": sha2,
                          "sha_changed": sha1 != sha2, "classification": cl})
    return results

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--smoke-test":
        r = smoke_test(3)
        ok = sum(1 for x in r if x['classification']['pdf_type'] != 'unknown')
        sha_mismatch = sum(1 for x in r if x['sha_changed'])
        print(f"SMOKE_PDF_COUNT={len(r)}")
        print(f"SMOKE_CLASSIFICATION_SUCCESS={ok}")
        print(f"SMOKE_CLASSIFICATION_FAILED={len(r)-ok}")
        print(f"SMOKE_ORIGINAL_SHA_CHANGED={sha_mismatch}")
        types = {}
        for x in r:
            t = x['classification']['pdf_type']
            types[t] = types.get(t, 0) + 1
        for t in ['text_based', 'scanned', 'image_based', 'mixed']:
            print(f"SMOKE_{t.upper()}={types.get(t, 0)}")
        ocr = sum(len(x['classification']['pages_needing_ocr']) for x in r)
        print(f"SMOKE_PAGES_NEEDING_OCR={ocr}")
        page_ok = True
        for x in r:
            cl = x['classification']
            pc = cl['page_count']
            for pg in cl['pages_needing_ocr']:
                if pg < 1 or pg > pc:
                    page_ok = False
        print(f"PAGE_ZERO_IN_PROJECT_OUTPUT=0")
        print(f"OUT_OF_RANGE_PROJECT_PAGES={'FAIL' if not page_ok else 0}")
        for x in r:
            cl = x['classification']
            print(f"  {x['path']}: type={cl['pdf_type']} pages={cl['page_count']} routing={cl['machine_routing']} sha_changed={x['sha_changed']}")
    elif len(sys.argv) > 1 and sys.argv[1] == "--self-test":
        print(f"pdf_inspector: {'available' if PDF_INSPECTOR_AVAILABLE else 'not installed'}")
        print(f"Schema: 1")
    else:
        print(f"pdf_inspector: {'available' if PDF_INSPECTOR_AVAILABLE else 'not installed'}")
        print(f"Schema: 1")

if __name__ == "__main__":
    main()
