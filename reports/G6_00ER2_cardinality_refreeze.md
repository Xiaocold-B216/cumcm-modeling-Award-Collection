STAGE=G6-00E-R2
STATUS=PASS
BRANCH=library-refactor-v1
HEAD=a042ecf898feaba6fc81d543a10e0188db8b2b12
PYTHON_EXECUTABLE=D:\python\python.exe
PYTHON_VERSION=3.13.15
PDF_INSPECTOR_VERSION=1.15.0
POPPLER_VERSION=25.02.0
PILOT_PDF_FILES=29
PILOT_UNIQUE_PAPERS=28
PILOT_MULTI_FILE_PAPERS=1
PILOT_FILES_WITH_FORMAL_PAPER_ID=29
PILOT_FILES_WITHOUT_FORMAL_PAPER_ID=0
G6_FILE_SOURCE_MAP_ROWS=29
G6_PAPER_ARTIFACT_MAP_ROWS=28
DUPLICATE_PAPER_ENTITIES=0
DUPLICATE_FILE_MEMBERSHIPS=0
MULTI_FILE_PAPERS=1
ORIGINAL_EXTRACTION_FILE_ROWS=22
Q2_READABLE_EXTRACTION_FILE_ROWS=7
AUTHORITY_SOURCE_SHA_MISMATCH=0
EXTRACTION_INPUT_SHA_MISMATCH=0
READABLE_SHA_MISMATCH=0
Q2_PROVENANCE_COMPLETE=7
Q2_PROVENANCE_MISSING=0
Q0_Q1_NATIVE_MARKDOWN_SMOKE_FILES=2
Q0_Q1_NATIVE_MARKDOWN_SMOKE_FAILURES=0
Q2_PAGE_AUDIT_ROWS=516
Q2_TOTAL_PAGES=516
FINAL_TEXT_PAGES=508
FINAL_VERIFIED_BLANK_PAGES=4
FINAL_IMAGE_ONLY_CONTENT_PAGES=4
FINAL_UNEXPLAINED_PAGES=0
GARBLED_RECONCILIATION_ROWS=8
GARBLED_FLAGGED_PAGES=8
UNRESOLVED_GARBLED_PAGES=0
FILES_WITH_SYSTEMATIC_TEXT_LOSS=0
EXTRACTION_CONTRACT_VALID=1
EXTRACTION_CONTRACT_FROZEN=1
EXTRACTION_CONTRACT_MODIFIED=0
EXPECTED_PRIMARY_G6_ARTIFACTS=84
FORMAL_G6_ARTIFACTS_GENERATED=0
FULL_516_PAGE_EXTRACTION_RERUN=0
OCR_RUN=0
PDF_REPAIR_RUN=0
IMAGE_REPAIR_RUN=0
SOURCE_REACQUISITION_RUN=0
FORMAL_MARKDOWN_GENERATION_RUN=0
FORMAL_METADATA_GENERATION_RUN=0
FORMAL_KNOWLEDGE_CARD_GENERATION_RUN=0
G6_15_RUN=0
G6_25_RUN=0
G6_INT_RUN=0
G1_CATALOG_MODIFIED=0
G2_CATALOG_MODIFIED=0
G3_IDENTITY_MODIFIED=0
G3_MEMBERSHIP_MODIFIED=0
G4_OUTPUT_MODIFIED=0
G5_OUTPUT_MODIFIED=0
G5_REPAIR_MANIFEST_MODIFIED=0
G5_OCR_DERIVATIVES_MODIFIED=0
G6_00F_HISTORY_MODIFIED=0
G6_00G_HISTORY_MODIFIED=0
G6_00GR_HISTORY_MODIFIED=0
G6_00ER_HISTORY_MODIFIED=0
G3_15R_HISTORY_MODIFIED=0
ORIGINAL_FILES_MODIFIED=0
ORIGINAL_FILES_DELETED=0
ORIGINAL_FILES_MOVED_OR_RENAMED=0
DUPLICATE_FILE_SOURCE_MAP_ROWS=0
DUPLICATE_PAPER_ARTIFACT_MAP_ROWS=0
IDEMPOTENCY_PASS=1

OUTPUTS=
- catalog/pilot/g6_file_source_map.csv
- catalog/pilot/g6_paper_artifact_map.csv
- logs/g6_00er2_cardinality_refreeze.log
- reports/G6_00ER2_cardinality_refreeze.md
- tools/35_g6_00er2_cardinality_refreeze.py

FILE_LEVEL_SUMMARY=
- files: 29
- Q0: 19
- Q1: 3
- Q2: 7
- model: File -> Paper -> extraction input

PAPER_LEVEL_SUMMARY=
- unique papers: 28
- multi-file papers: 1
- expected formal artifact sets: 84 (Paper-level, 3 per Paper)
- model: Paper -> formal memberships -> one future artifact set

MULTI_FILE_PAPER_SUMMARY=
- paper_id: CUMCM-2015-D-002
  member_file_count: 3
  primary_file: 2015年数学建模国赛真题+优秀论文/2015年赛题/2015年国赛D题.doc
  attachment_files: 2015年数学建模国赛真题+优秀论文/2015年赛题/2015年国赛D题.doc;2015年数学建模国赛真题+优秀论文/2015年赛题/2015年国赛D题附件2 中华人民共和国土地增值税暂行条例.pdf;2015年数学建模国赛真题+优秀论文/2015年赛题/2015年国赛D题附件3 其他相关说明.pdf
  status: PASS; one Paper-level row, multiple File-level inputs; no duplicate Paper entity

Q2_CONTRACT_SUMMARY=
- authority: original PDF
- extraction input: G5 readable PDF
- completeness: pdf-inspector whole-document text
- page extraction: Poppler single-page
- source_page: 1-based
- TEXT_PAGE: 508
- VERIFIED_BLANK_PAGE: 4
- IMAGE_ONLY_CONTENT_PAGE: 4
- UNEXPLAINED_PAGE: 0
- unresolved garbled: 0

PRE_EXISTING_CHANGES=all prior untracked workspace entries preserved; G3-15R membership repair and G6-00E-R history were read-only in this stage
G6_00ER2_INTRODUCED_CHANGES=tools/35_g6_00er2_cardinality_refreeze.py; catalog/pilot/g6_file_source_map.csv; catalog/pilot/g6_paper_artifact_map.csv; logs/g6_00er2_cardinality_refreeze.log; reports/G6_00ER2_cardinality_refreeze.md

VALIDATION=
- File-level mapping consumes formal PaperFileMembership rows, including the two CUMCM-2015-D-002 attachments.
- Paper-level mapping aggregates memberships and selects the canonical primary membership; CUMCM-2015-D-002 has one Paper row and multiple file memberships.
- Q0/Q1 native Markdown smoke ran on one 2015 file and one 2025 file only; no batch formal Markdown was generated.
- Existing Q2 516-page audit and 8-row reconciliation were reused without extraction or visual re-audit.
- Source-map contents stable on this invocation: file_map=1; paper_map=1.

ISSUES=
- NONE
BLOCKER=NONE
APPROVAL=Pilot file-level and paper-level G6 source contracts re-frozen successfully
NEXT=G6-PILOT-AUTO-R only after explicit authorization; do not auto-run
