# G4-25 2025 PDF Audit

## Baseline

Expected PDFs: 12
Audit Rows: 12

## Runtime

Python: 3.13.15
pdf-inspector: 1.15.0
Schema: 1

## Coverage

Expected: 12
Audited: 12
Missing: 0
Extra: 0
Duplicate: 0

## Classification

text_based: 5
scanned: 0
image_based: 7
mixed: 0
failed: 0

## Pages

Total: 524
OCR Routed: 516

## Issues

Issue counts: {}

## Visual Review

Required: 7
Not Required: 5

## Final-Q Evidence Correction

Q values are assigned only from independent quality evidence. The previous Q values below were derived from machine routing and were cleared.

| file_path | sha256 | classification | machine_routing | current_preliminary_q | current_final_q | q_evidence_source | q_evidence_independent_of_pdf_type | recommended_corrected_q_state |
|---|---|---|---|---|---|---|---|---|
| 2025年数学建模国赛真题+优秀论文/2025数学建模国赛优秀论文/A066.pdf | 9C14EAB19304FE45A36E45A965FA740E2636690630ECD8528335D4E4AEC3E2D4 | image_based | IMAGE_VISUAL_REVIEW | Q4 |  | tools/17_g4_25_audit_2025.py:181-192 machine_routing -> q_class | False | unassigned; retain visual_review_required=true and status=pending |
| 2025年数学建模国赛真题+优秀论文/2025数学建模国赛优秀论文/A196.pdf | B5FB5FE4B2D06998BC85BB9276CF16AFC1755913D91F18C01D5209F8F13ADA92 | image_based | IMAGE_VISUAL_REVIEW | Q4 |  | tools/17_g4_25_audit_2025.py:181-192 machine_routing -> q_class | False | unassigned; retain visual_review_required=true and status=pending |
| 2025年数学建模国赛真题+优秀论文/2025数学建模国赛优秀论文/B060.pdf | 17C1B7E255DCBB8E8AC34C0A750E39D7DF1EE4A5ED0D0323B46388F168090330 | image_based | IMAGE_VISUAL_REVIEW | Q4 |  | tools/17_g4_25_audit_2025.py:181-192 machine_routing -> q_class | False | unassigned; retain visual_review_required=true and status=pending |
| 2025年数学建模国赛真题+优秀论文/2025数学建模国赛优秀论文/C023.pdf | 515FD73059B427606FFD099781A124D34BAC3306BEE87C61D47259622351EB17 | image_based | IMAGE_VISUAL_REVIEW | Q4 |  | tools/17_g4_25_audit_2025.py:181-192 machine_routing -> q_class | False | unassigned; retain visual_review_required=true and status=pending |
| 2025年数学建模国赛真题+优秀论文/2025数学建模国赛优秀论文/C132.pdf | 08EC307CDC65A673E6838E2E3D00B2337DA414E7891284617E10F370E5F246B5 | image_based | IMAGE_VISUAL_REVIEW | Q4 |  | tools/17_g4_25_audit_2025.py:181-192 machine_routing -> q_class | False | unassigned; retain visual_review_required=true and status=pending |
| 2025年数学建模国赛真题+优秀论文/2025数学建模国赛优秀论文/D037.pdf | BDBED46FF5D5841AF82FA6441C8AB3D83A62658672857E445DEADFD8DAD1F0AC | image_based | IMAGE_VISUAL_REVIEW | Q4 |  | tools/17_g4_25_audit_2025.py:181-192 machine_routing -> q_class | False | unassigned; retain visual_review_required=true and status=pending |
| 2025年数学建模国赛真题+优秀论文/2025数学建模国赛优秀论文/E030.pdf | 7270DACAB35167E998141D5D34C34D12A912B3620249A892697211F24D009E0D | image_based | IMAGE_VISUAL_REVIEW | Q4 |  | tools/17_g4_25_audit_2025.py:181-192 machine_routing -> q_class | False | unassigned; retain visual_review_required=true and status=pending |

## Q Status

Assigned: 0
Unassigned: 12

DIRECT_PDF_TYPE_TO_FINAL_Q_MAPPING: 0
ASSIGNED_Q_WITHOUT_INDEPENDENT_EVIDENCE: 0
VISUAL_REVIEW_EXECUTED: 0

## Duplicate Cache

Unique SHA: 12
Reused: 0

## Integrity

SHA Mismatch: 0
SHA Changed After Audit: 0
Page Zero: 0
Out of Range: 0

## Gate

STATUS: PASS
BLOCKER: NONE
