# G4-00R pdf-inspector Runtime Binding Report

## Execution Summary

Stage: G4-00R
Status: PASS
Started At: 2026-08-19T22:47:13+08:00
Completed At: 2026-08-19T22:47:13+08:00

## Runtime Verification

Python Executable: D:\python\python.exe
Python Version: 3.13.15
PDF Inspector Version: 1.15.0
Host Python Runtime Visible: PASS

## API Compatibility

PDF Inspector Import: PASS
PDF Inspector Classify API: PASS
PDF Inspector Detect API: PASS
Classify API Compatible: PASS
Detect API Compatible: PASS

## API Details

classify_pdf returns: PdfClassification(pdf_type, page_count, confidence, pages_needing_ocr)
detect_pdf returns: PdfDetection(pdf_type, page_count, confidence, pages_needing_ocr, has_encoding_issues, is_complex_layout, pages_with_tables, pages_with_columns, markdown, ocr_reasons_by_page, processing_time_ms, title)

Page Numbering: classify_pdf pages_needing_ocr is 0-based (converted to 1-based), detect_pdf pages_needing_ocr is 1-based

## Framework

PDF Audit Self Test: PASS
PDF Audit Schema Version: 1

## PDF Statistics

Total PDF Files: 513
PDF Files 2015: 17
PDF Files 2025: 12

## Smoke Test

Smoke Sample Size Gate: PASS (3 PDFs)
Smoke Classification Gate: PASS (3 success)

Smoke PDF Count: 3
Smoke Classification Success: 3
Smoke Classification Failed: 0

Smoke Text Based: 2
Smoke Scanned: 0
Smoke Image Based: 1
Smoke Mixed: 0

Smoke Pages Needing OCR: 3

Project Page Number Base: 1
Page Zero In Project Output: 0
Out Of Range Project Pages: 0

Smoke Source SHA Mismatch: 0
Smoke Original SHA Changed: 0

## Quality Routing

Direct PDF Type to Final Q Mapping: 0

## Safety

PDFs Formally Audited 2015: 0
PDFs Formally Audited 2025: 0
OCR Run: 0
PDF Repair Run: 0
Markdown Artifacts Generated: 0

G1 Catalog Modified: 0
G2 Catalog Modified: 0
G3 Catalog Modified: 0

Original Files Modified: 0
Original Files Deleted: 0
Original Files Moved/Renamed: 0

## Output Files

- tools/02_pdf_audit.py (updated)
- reports/G4_00R_runtime_binding.md

## Gate

- D:\python\python.exe visible: PASS
- Python 3.13.15 usable: PASS
- pdf-inspector 1.15.0 import PASS: PASS
- classify_pdf PASS: PASS
- detect_pdf PASS: PASS
- tools/02_pdf_audit.py self-test PASS: PASS
- PDF inventory unchanged: PASS
- 1 <= smoke count <= 3: PASS
- >=1 smoke classification success: PASS
- real classify_pdf executed: PASS
- real detect_pdf executed: PASS
- project page numbering remains 1-based: PASS
- no page zero: PASS
- no out-of-range pages: PASS
- source SHA before = after = G1: PASS
- no final Q direct mapping: PASS
- no formal 2015 audit: PASS
- no formal 2025 audit: PASS
- no OCR: PASS
- no repair: PASS
- no Markdown: PASS
- no G1/G2/G3 modification: PASS
- no original file modification: PASS
