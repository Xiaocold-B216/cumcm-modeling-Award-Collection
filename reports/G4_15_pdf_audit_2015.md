# G4-15 2015 PDF Audit Report

## Execution Summary

Stage: G4-15
Status: PASS
Started At: 2026-08-20T11:28:59+0800
Completed At: 2026-08-20T11:29:51+08:00

## Baseline

Expected PDFs: 17
Audit Rows: 17

## Runtime

Python: 3.13.15
pdf-inspector: 1.15.0
Schema: 1

## Coverage

Expected: 17
Audited: 17
Missing: 0
Extra: 0
Duplicate: 0

## Classification

text_based: 14
scanned: 0
image_based: 0
mixed: 3
failed: 0

## Pages

Total: 480
OCR Routed: 12

## Visual Review

Required: 3
Not Required: 14

### Review Queue

- `2015年数学建模国赛真题+优秀论文/2015年优秀论文/2015A：太阳影子定位 (5).pdf`: pdf_type=mixed (pages=26, ocr_pages=[26])
- `2015年数学建模国赛真题+优秀论文/2015年优秀论文/2015A：太阳影子定位 (6).pdf`: pdf_type=mixed (pages=26, ocr_pages=[26])
- `2015年数学建模国赛真题+优秀论文/2015年优秀论文/2015B：互联网+_时代的出租车资源配置 (1).pdf`: pdf_type=mixed (pages=32, ocr_pages=[1, 2, 3, 4, 6, 9, 10, 11, 18, 19])

## Q Status

Assigned: 0
Unassigned: 17

## Duplicate Cache

Unique SHA: 17
Reused: 0

## Integrity

SHA Mismatch: 0
Original SHA Changed: 0
Page Zero: 0
Out of Range: 0

## Scope Protection

OCR Run: 0
Repair Run: 0
Markdown Extraction Run: 0
Dependency Install Run: 0

## Gate

- 2015 expected PDFs = 17: PASS
- 17 physical PDFs all represented: PASS
- Missing = 0: PASS
- Extra = 0: PASS
- Duplicate audit row = 0: PASS
- G1 SHA mismatch = 0: PASS
- Real pdf-inspector executed: PASS
- Classification accounting balanced: PASS
- Project pages remain 1-based: PASS
- Page zero = 0: PASS
- Out of range = 0: PASS
- Visual review queue deterministic: PASS
- Final Q not guessed: PASS
- Shared G4 framework unchanged: PASS
- G1/G2/G3 unchanged: PASS
- 2025 outputs untouched: PASS
- Original PDFs unchanged: PASS
- No OCR: PASS
- No repair: PASS
- No Markdown: PASS
- No dependency install: PASS
