# G6-00E-R Pilot G6 Extraction Source Contract Re-freeze

STAGE=G6-00E-R
STATUS=BLOCKED
BRANCH=library-refactor-v1
HEAD=a042ecf898feaba6fc81d543a10e0188db8b2b12
PYTHON_EXECUTABLE=D:\python\python.exe
PYTHON_VERSION=3.13.15
PDF_INSPECTOR_VERSION=1.15.0
POPPLER_VERSION=25.02.0
PILOT_PAPERS=29
PILOT_PAPER_ID_RESOLVED=27
PILOT_PAPER_ID_UNKNOWN=2
PILOT_DUPLICATE_PAPER_ID=1
G6_SOURCE_MAP_ROWS=29
G6_SOURCE_MAP_Q0=19
G6_SOURCE_MAP_Q1=3
G6_SOURCE_MAP_Q2=7
SOURCE_MAP_ACCOUNTING_PASS=1
UNIQUE_SOURCE_MAP_PAPER_IDS=28
DUPLICATE_SOURCE_MAP_PAPER_IDS=1
SOURCE_MAP_UNKNOWN_PAPER_IDS=2
SOURCE_MAP_UNKNOWN_PATHS=0
SOURCE_MAP_UNKNOWN_SHA=0
ORIGINAL_EXTRACTION_ROWS=22
Q2_READABLE_EXTRACTION_ROWS=7
AUTHORITY_SOURCE_SHA_MISMATCH=0
EXTRACTION_INPUT_SHA_MISMATCH=0
READABLE_SHA_MISMATCH=0
PAGE_COUNT_UNKNOWN=0
PAGE_COUNT_MISMATCH=0
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
PAGE_ZERO_PRESENT=0
PAGE_GAPS=0
DUPLICATE_SOURCE_PAGES=0
OUT_OF_RANGE_PAGES=0
FILES_WITH_SYSTEMATIC_TEXT_LOSS=0
EXTRACTION_CONTRACT_VALID=1
EXTRACTION_CONTRACT_FROZEN=1
EXTRACTION_CONTRACT_MODIFIED=0
EXTRACTION_CONTRACT_SEMANTIC_CHANGE=NONE
EXPECTED_PRIMARY_G6_ARTIFACTS=87
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
G3_25R_MAPPING_MODIFIED=0
G4_OUTPUT_MODIFIED=0
G5_OUTPUT_MODIFIED=0
G5_REPAIR_MANIFEST_MODIFIED=0
G5_OCR_DERIVATIVES_MODIFIED=0
G6_00F_HISTORY_MODIFIED=0
G6_00G_HISTORY_MODIFIED=0
G6_00GR_HISTORY_MODIFIED=0
ORIGINAL_FILES_MODIFIED=0
ORIGINAL_FILES_DELETED=0
ORIGINAL_FILES_MOVED_OR_RENAMED=0
DUPLICATE_SOURCE_MAP_ROWS=0
IDEMPOTENCY_PASS=0

OUTPUTS=
- catalog/pilot/g6_source_map.csv
- logs/g6_00er_contract_refreeze.log
- reports/G6_00ER_contract_refreeze.md
- tools/33_g6_00er_contract_refreeze.py

PRE_EXISTING_CHANGES=all previously untracked workspace entries were preserved; only the four G6-00E-R outputs are stage-introduced
G6_00ER_INTRODUCED_CHANGES=tools/33_g6_00er_contract_refreeze.py; catalog/pilot/g6_source_map.csv; logs/g6_00er_contract_refreeze.log; reports/G6_00ER_contract_refreeze.md

SOURCE_MAP_SUMMARY=
- Q0: 19 rows; original PDF -> pdf-inspector native Markdown.
- Q1: 3 rows; original PDF -> pdf-inspector native Markdown.
- Q2: 7 rows; original authority PDF -> G5 readable derivative -> hybrid/page-aware contract.

Q2_CONTRACT_SUMMARY=
- authority: original PDF
- extraction input: G5 readable PDF
- completeness: pdf-inspector whole-document text
- page extraction: Poppler single-page extraction
- source_page: 1-based
- TEXT_PAGE: 508
- VERIFIED_BLANK_PAGE: 4
- IMAGE_ONLY_CONTENT_PAGE: 4
- UNEXPLAINED_PAGE: 0
- unresolved garbled: 0

IDENTITY_BLOCKER=
- Two Q0 rows remain paper_id=unknown: the 2015 D-question attachment 2 and attachment 3 PDFs.
- catalog/paper_files.csv has no formal membership for either path. Assigning both to CUMCM-2015-D-002 would create a duplicate identity, so no G3 mutation or synthetic ID was made.

SMOKE_SUMMARY=
- 2015: 2015年数学建模国赛真题+优秀论文/2015年优秀论文/2015A：太阳影子定位 (1).pdf; process_success=1; markdown_nonempty=1; markdown_chars=1251.
- 2025: 2025年数学建模国赛真题+优秀论文/2025年数学建模国赛真题！/A题/A题.pdf; process_success=1; markdown_nonempty=1; markdown_chars=1597.

VALIDATION=
- Read-only SHA and page-count validation was performed for all 29 extraction inputs; no OCR, repair, reacquisition, or 516-page extraction rerun occurred.
- Existing G6-00G hybrid page audit and G6-00G-R/G6-00G-RF reconciliation evidence were read without modification.
- Extraction contract SHA-256 remains B7E0A4809CAAF64983BF5D149D99F920CE8C64B1D52D4B1C7DFFF75F19A6956F; EXTRACTION_CONTRACT_MODIFIED=0.
- Source-map content stable on this invocation: 0.

ISSUES=
- G3_IDENTITY_UNRESOLVED_FOR_2_2015_D_ATTACHMENT_PDFS
BLOCKER=G3_IDENTITY_UNRESOLVED_FOR_2_2015_D_ATTACHMENT_PDFS
APPROVAL=NOT_APPROVED
NEXT=resolve the two 2015 D attachment Paper identities in the G3-owned catalog, then rerun G6-00E-R; do not auto-run G6-PILOT-AUTO-R
