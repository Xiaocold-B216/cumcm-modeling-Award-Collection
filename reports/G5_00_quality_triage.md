# G5-00 Pilot Final-Q Evidence Closure & Repair Routing Freeze

STAGE=G5-00
STATUS=PASS
BRANCH=library-refactor-v1
HEAD=a042ecf898feaba6fc81d543a10e0188db8b2b12
PYTHON_EXECUTABLE=D:\python\python.exe
PYTHON_VERSION=3.13.15
G4_STATUS=CLOSED
G4_INT_R_STATUS=PASS
INPUT_PDF_ROWS=29
UNIQUE_INPUT_PATHS=29
UNIQUE_INPUT_SHA256=29
FINAL_Q_ASSIGNED=29
FINAL_Q_UNASSIGNED=0
PDF_QUALITY_RATING_RATE=100.0
Q0_COUNT=19
Q1_COUNT=3
Q2_COUNT=7
Q3_COUNT=0
Q4_COUNT=0
Q5_COUNT=0
DIRECT_PDF_TYPE_TO_FINAL_Q_MAPPING=0
DIRECT_MACHINE_ROUTING_TO_FINAL_Q_MAPPING=0
ASSIGNED_Q_WITHOUT_INDEPENDENT_EVIDENCE=0
VISUAL_REVIEW_REQUIRED_INPUT=10
VISUAL_REVIEW_COMPLETED=10
VISUAL_REVIEW_UNRESOLVED=0
ISSUE_CODED_ABNORMAL_PDFS=10
ABNORMAL_PDFS_WITHOUT_ISSUE_CODE=0
ROUTED_ROWS=29
UNROUTED_GRADED_ROWS=0
NO_PDF_REPAIR_COUNT=22
OCR_REPAIR_COUNT=7
IMAGE_REPAIR_AND_OCR_COUNT=0
SOURCE_REACQUISITION_COUNT=0
QUARANTINE_AND_REACQUISITION_COUNT=0
MANUAL_REVIEW_ROUTE_COUNT=0
OCR_RUN=0
OCR_OUTPUT_FILES=0
PDF_REPAIR_RUN=0
REPAIRED_PDF_FILES=0
SOURCE_REACQUISITION_RUN=0
REPLACEMENT_FILES_DOWNLOADED=0
MARKDOWN_EXTRACTION_RUN=0
MARKDOWN_ARTIFACTS_GENERATED=0
REPAIR_MANIFEST_REPAIR_ENTRIES_ADDED=0
SOURCE_SHA_MISMATCH=0
ORIGINAL_SHA_CHANGED_AFTER_G5_00=0
G1_CATALOG_MODIFIED=0
G2_CATALOG_MODIFIED=0
G3_CATALOG_MODIFIED=0
G4_15_OUTPUT_MODIFIED=0
G4_25R_OUTPUT_MODIFIED=0
G4_INT_R_OUTPUT_MODIFIED=0
ORIGINAL_FILES_MODIFIED=0
ORIGINAL_FILES_DELETED=0
ORIGINAL_FILES_MOVED_OR_RENAMED=0

OUTPUTS=
- catalog/pilot/pdf_quality_pilot.csv
- catalog/pilot/pdf_repair_routing_pilot.csv
- catalog/pilot/pdf_quality_manual_review.csv
- logs/g5_00_quality_triage.log
- reports/G5_00_quality_triage.md

QUALITY_EVIDENCE=
- Q0 uses representative-page visual review plus G4 native-text/no-issue evidence.
- Q1 uses representative-page visual review plus the recorded trailing blank-page anomaly.
- Q2 uses representative-page visual review plus G4 no-reliable-text-layer/OCR-route evidence.
- No quality grade is assigned from classification or machine routing alone.

Q_EVIDENCE_ROWS=
| file_path | year | paper_id | final_q | evidence_source | issue_codes | visual_status |
|---|---:|---|---|---|---|---|
| 2015年数学建模国赛真题+优秀论文/2015年优秀论文/2015A：太阳影子定位 (1).pdf | 2015 | CUMCM-2015-A-007 | Q0 | G5-00 representative-page visual review + G4 native-text audit | [] | not_required |
| 2015年数学建模国赛真题+优秀论文/2015年优秀论文/2015A：太阳影子定位 (2).pdf | 2015 | CUMCM-2015-A-003 | Q0 | G5-00 representative-page visual review + G4 native-text audit | [] | not_required |
| 2015年数学建模国赛真题+优秀论文/2015年优秀论文/2015A：太阳影子定位 (3).pdf | 2015 | CUMCM-2015-A-008 | Q0 | G5-00 representative-page visual review + G4 native-text audit | [] | not_required |
| 2015年数学建模国赛真题+优秀论文/2015年优秀论文/2015A：太阳影子定位 (4).pdf | 2015 | CUMCM-2015-A-001 | Q0 | G5-00 representative-page visual review + G4 native-text audit | [] | not_required |
| 2015年数学建模国赛真题+优秀论文/2015年优秀论文/2015A：太阳影子定位 (5).pdf | 2015 | CUMCM-2015-A-005 | Q1 | G5-00 representative-page visual review + G4 mixed-text audit | ["PDF_BLANK_PAGE"] | completed |
| 2015年数学建模国赛真题+优秀论文/2015年优秀论文/2015A：太阳影子定位 (6).pdf | 2015 | CUMCM-2015-A-004 | Q1 | G5-00 representative-page visual review + G4 mixed-text audit | ["PDF_BLANK_PAGE"] | completed |
| 2015年数学建模国赛真题+优秀论文/2015年优秀论文/2015A：太阳影子定位 (7).pdf | 2015 | CUMCM-2015-A-006 | Q0 | G5-00 representative-page visual review + G4 native-text audit | [] | not_required |
| 2015年数学建模国赛真题+优秀论文/2015年优秀论文/2015B：互联网+_时代的出租车资源配置 (1).pdf | 2015 | CUMCM-2015-B-003 | Q1 | G5-00 representative-page visual review + G4 mixed-text audit | ["PDF_BLANK_PAGE"] | completed |
| 2015年数学建模国赛真题+优秀论文/2015年优秀论文/2015B：互联网+_时代的出租车资源配置 (2).pdf | 2015 | CUMCM-2015-B-002 | Q0 | G5-00 representative-page visual review + G4 native-text audit | [] | not_required |
| 2015年数学建模国赛真题+优秀论文/2015年优秀论文/2015B：互联网+_时代的出租车资源配置 (3).pdf | 2015 | CUMCM-2015-B-006 | Q0 | G5-00 representative-page visual review + G4 native-text audit | [] | not_required |
| 2015年数学建模国赛真题+优秀论文/2015年优秀论文/2015B：互联网+_时代的出租车资源配置 (4).pdf | 2015 | CUMCM-2015-B-004 | Q0 | G5-00 representative-page visual review + G4 native-text audit | [] | not_required |
| 2015年数学建模国赛真题+优秀论文/2015年优秀论文/2015B：互联网+_时代的出租车资源配置 (5).pdf | 2015 | CUMCM-2015-B-001 | Q0 | G5-00 representative-page visual review + G4 native-text audit | [] | not_required |
| 2015年数学建模国赛真题+优秀论文/2015年优秀论文/2015C：月上柳梢头，人约黄昏后 (3).pdf | 2015 | CUMCM-2015-C-005 | Q0 | G5-00 representative-page visual review + G4 native-text audit | [] | not_required |
| 2015年数学建模国赛真题+优秀论文/2015年优秀论文/2015C：月上柳梢头，人约黄昏后 (4).pdf | 2015 | CUMCM-2015-C-002 | Q0 | G5-00 representative-page visual review + G4 native-text audit | [] | not_required |
| 2015年数学建模国赛真题+优秀论文/2015年优秀论文/2015D：众筹筑屋规划方案设计 (3).pdf | 2015 | CUMCM-2015-D-003 | Q0 | G5-00 representative-page visual review + G4 native-text audit | [] | not_required |
| 2015年数学建模国赛真题+优秀论文/2015年赛题/2015年国赛D题附件2 中华人民共和国土地增值税暂行条例.pdf | 2015 | unknown | Q0 | G5-00 representative-page visual review + G4 native-text audit | [] | not_required |
| 2015年数学建模国赛真题+优秀论文/2015年赛题/2015年国赛D题附件3 其他相关说明.pdf | 2015 | unknown | Q0 | G5-00 representative-page visual review + G4 native-text audit | [] | not_required |
| 2025年数学建模国赛真题+优秀论文/2025年数学建模国赛真题！/A题/A题.pdf | 2025 | CUMCM-2025-A-001 | Q0 | G5-00 representative-page visual review + G4 native-text audit | [] | not_required |
| 2025年数学建模国赛真题+优秀论文/2025年数学建模国赛真题！/B题/B题.pdf | 2025 | CUMCM-2025-B-001 | Q0 | G5-00 representative-page visual review + G4 native-text audit | [] | not_required |
| 2025年数学建模国赛真题+优秀论文/2025年数学建模国赛真题！/C题/C题.pdf | 2025 | CUMCM-2025-C-001 | Q0 | G5-00 representative-page visual review + G4 native-text audit | [] | not_required |
| 2025年数学建模国赛真题+优秀论文/2025年数学建模国赛真题！/D题/D题.pdf | 2025 | CUMCM-2025-D-001 | Q0 | G5-00 representative-page visual review + G4 native-text audit | [] | not_required |
| 2025年数学建模国赛真题+优秀论文/2025年数学建模国赛真题！/E题/E题.pdf | 2025 | CUMCM-2025-E-001 | Q0 | G5-00 representative-page visual review + G4 native-text audit | [] | not_required |
| 2025年数学建模国赛真题+优秀论文/2025数学建模国赛优秀论文/A066.pdf | 2025 | unknown | Q2 | G5-00 representative-page visual review + G4 text-layer/OCR-route evidence | ["PDF_NO_TEXT_LAYER"] | completed |
| 2025年数学建模国赛真题+优秀论文/2025数学建模国赛优秀论文/A196.pdf | 2025 | unknown | Q2 | G5-00 representative-page visual review + G4 text-layer/OCR-route evidence | ["PDF_NO_TEXT_LAYER"] | completed |
| 2025年数学建模国赛真题+优秀论文/2025数学建模国赛优秀论文/B060.pdf | 2025 | unknown | Q2 | G5-00 representative-page visual review + G4 text-layer/OCR-route evidence | ["PDF_NO_TEXT_LAYER"] | completed |
| 2025年数学建模国赛真题+优秀论文/2025数学建模国赛优秀论文/C023.pdf | 2025 | unknown | Q2 | G5-00 representative-page visual review + G4 text-layer/OCR-route evidence | ["PDF_NO_TEXT_LAYER"] | completed |
| 2025年数学建模国赛真题+优秀论文/2025数学建模国赛优秀论文/C132.pdf | 2025 | unknown | Q2 | G5-00 representative-page visual review + G4 text-layer/OCR-route evidence | ["PDF_NO_TEXT_LAYER"] | completed |
| 2025年数学建模国赛真题+优秀论文/2025数学建模国赛优秀论文/D037.pdf | 2025 | unknown | Q2 | G5-00 representative-page visual review + G4 text-layer/OCR-route evidence | ["PDF_NO_TEXT_LAYER"] | completed |
| 2025年数学建模国赛真题+优秀论文/2025数学建模国赛优秀论文/E030.pdf | 2025 | unknown | Q2 | G5-00 representative-page visual review + G4 text-layer/OCR-route evidence | ["PDF_NO_TEXT_LAYER"] | completed |

ROUTING_SUMMARY=
- NO_PDF_REPAIR: 22
- OCR_REPAIR: 7
- IMAGE_REPAIR_AND_OCR: 0
- SOURCE_REACQUISITION: 0
- QUARANTINE_AND_REACQUISITION: 0
- MANUAL_REVIEW: 0

VALIDATION=
- G4-15, G4-25R and G4-INT-R inputs parsed; 29 paths and 29 SHA values verified against G1 inventory and current original files.
- Representative pages were rendered only for targeted quality review; no full-Pilot PDF reclassification was run.
- OCR, PDF repair, source reacquisition, Markdown extraction, migration and API changes were not performed.

ISSUES=
- NONE

BLOCKER=NONE
APPROVAL=G5 Pilot Final-Q evidence and repair routing frozen
NEXT=G5 repair/reacquisition execution for 2015 and 2025
