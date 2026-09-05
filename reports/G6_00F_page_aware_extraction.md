STAGE=G6-00F
STATUS=BLOCKED
BRANCH=library-refactor-v1
HEAD=a042ecf898feaba6fc81d543a10e0188db8b2b12
PYTHON_EXECUTABLE=D:\python\python.exe
PYTHON_VERSION=3.13.15
PDF_INSPECTOR_VERSION=1.15.0
PDF_INSPECTOR_IMPORT_SUCCESS=1
PDF_INSPECTOR_MODIFIED=0
Q2_WORKSET_ROWS=7
Q2_UNKNOWN_PAPER_ID=0
UNIQUE_Q2_PAPER_IDS=7
UNIQUE_Q2_SOURCE_PATHS=7
UNIQUE_Q2_DERIVED_PATHS=7
Q2_SOURCE_SHA_MISMATCH=0
Q2_DERIVED_MISSING=0
Q2_DERIVED_SHA_MISMATCH=0
Q2_PAGE_COUNT_MISMATCH=0
PROCESS_PDF_PAGE_SCOPED_AVAILABLE=1
EXTRACT_TEXT_PAGE_SCOPED_AVAILABLE=0
POSITIONED_TEXT_PAGE_SCOPED_AVAILABLE=1
MARKDOWN_PAGE_SCOPED_AVAILABLE=1
PAGE_SCOPED_EXTRACTION_AVAILABLE=1
PAGE_SCOPED_EXTRACTION_API=extract_text_in_regions
PAGE_FILTER_PARAMETER=page_regions=[(page_0indexed, [[x1,y1,x2,y2]])]
PAGE_FILTER_INDEX_BASE=0-based
SOURCE_PAGE_NUMBERING=1-based
Q2_TOTAL_PAGES=516
PAGE_AUDIT_ROWS=516
PAGE_ZERO_PRESENT=0
PAGE_GAPS=0
DUPLICATE_SOURCE_PAGES=0
OUT_OF_RANGE_PAGES=0
VERIFIED_BLANK_PAGES=4
PAGE_TEXT_EMPTY_VERIFIED_BLANK=4
PAGE_TEXT_EMPTY_UNEXPECTED=4
NONBLANK_PAGES=512
NONBLANK_PAGES_WITH_TEXT=508
NONBLANK_PAGES_WITHOUT_TEXT=4
GARBLED_PAGE_COUNT=0
WHOLE_DOCUMENT_TEXT_CHARS=742965
PAGE_JOINED_TEXT_CHARS=635631
PAGE_JOINED_RELATIVE_CHAR_DIFFERENCE=0.000123
PAGE_JOINED_TEXT_COVERAGE_ACCEPTABLE=1
Q2_PAGE_AWARE_MARKDOWN_PREVIEW_SUCCESS=7
PAGE_AWARE_CONTRACT_FROZEN=0
FORMAL_G6_ARTIFACTS_GENERATED=0
TEMP_PREVIEW_FILES_REMAINING=0
OCR_RUN=0
PDF_REPAIR_RUN=0
IMAGE_REPAIR_RUN=0
SOURCE_REACQUISITION_RUN=0
FORMAL_MARKDOWN_GENERATION_RUN=0
FORMAL_METADATA_GENERATION_RUN=0
FORMAL_KNOWLEDGE_CARD_GENERATION_RUN=0
G6_00E_RERUN=0
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
ORIGINAL_FILES_MODIFIED=0
ORIGINAL_FILES_DELETED=0
ORIGINAL_FILES_MOVED_OR_RENAMED=0
DUPLICATE_PAGE_AUDIT_ROWS=0
DUPLICATE_CONTRACT_FILES=0
IDEMPOTENCY_PASS=0

OUTPUTS=
- D:\cumcm-modeling-Award-Collection\catalog\pilot\g6_q2_page_extraction_audit.csv
- page-aware contract not frozen because the audit is blocked
- D:\cumcm-modeling-Award-Collection\logs\g6_00f_page_aware_extraction.log
- D:\cumcm-modeling-Award-Collection\reports\G6_00F_page_aware_extraction.md
- D:\cumcm-modeling-Award-Collection\tools\30_g6_00f_page_aware_extraction.py

PRE_EXISTING_CHANGES=all pre-existing untracked workspace entries preserved; G3-25R outputs were read-only in this stage
G6_00F_INTRODUCED_CHANGES=tools/30_g6_00f_page_aware_extraction.py; catalog/pilot/g6_q2_page_extraction_audit.csv; logs/g6_00f_page_aware_extraction.log; reports/G6_00F_page_aware_extraction.md

PAGE_EXTRACTION_SUMMARY=
- paper_id: CUMCM-2025-A-A066
  pages: 86
  nonblank_pages: 86
  unexpected_empty_pages: 0
  unexpected_empty_page_numbers: []
  verified_blank_pages: []
  status: PASS
- paper_id: CUMCM-2025-A-A196
  pages: 98
  nonblank_pages: 98
  unexpected_empty_pages: 0
  unexpected_empty_page_numbers: []
  verified_blank_pages: []
  status: PASS
- paper_id: CUMCM-2025-B-B060
  pages: 72
  nonblank_pages: 71
  unexpected_empty_pages: 1
  unexpected_empty_page_numbers: [71]
  verified_blank_pages: []
  status: BLOCKED
- paper_id: CUMCM-2025-C-C023
  pages: 122
  nonblank_pages: 120
  unexpected_empty_pages: 2
  unexpected_empty_page_numbers: [9, 26]
  verified_blank_pages: []
  status: BLOCKED
- paper_id: CUMCM-2025-C-C132
  pages: 65
  nonblank_pages: 61
  unexpected_empty_pages: 0
  unexpected_empty_page_numbers: []
  verified_blank_pages: [7, 8, 10, 36]
  status: PASS
- paper_id: CUMCM-2025-D-D037
  pages: 37
  nonblank_pages: 36
  unexpected_empty_pages: 1
  unexpected_empty_page_numbers: [37]
  verified_blank_pages: []
  status: BLOCKED
- paper_id: CUMCM-2025-E-E030
  pages: 36
  nonblank_pages: 36
  unexpected_empty_pages: 0
  unexpected_empty_page_numbers: []
  verified_blank_pages: []
  status: PASS

CONTRACT_SUMMARY=
- backend: pdf-inspector
- input: G5 readable PDF
- mode: page-scoped text extraction
- api: extract_text_in_regions with one full-page region
- final source_page numbering: 1-based
- deterministic Markdown wrapper: allowed
- whole-document artificial page splitting: forbidden
- secondary extractor fallback: forbidden
- OCR in G6: forbidden

VALIDATION=
- pdf-inspector 1.15.0 was imported from the fixed D:\python environment; no dependency installation ran.
- Page selection was explicit and 0-based; every audit source_page is api_page_index + 1.
- Four marker-only pages in C132 matched the four G5-verified blank pages; four additional marker-only pages conflicted with G5 text-page counts and therefore blocked the stage.
- Page-joined native text was compared in memory with whole-document extract_text after whitespace normalization.
- Temporary previews were created only for validation and removed; formal G6 artifacts were not generated.

ISSUES=
- extract_text has no page parameter; positioned text and native Markdown page calls remain diagnostic-only for Q2 because they return image markers/empty Markdown.

BLOCKER=PAGE_TEXT_EMPTY_UNEXPECTED=4; NONBLANK_PAGES_WITHOUT_TEXT=4
APPROVAL=NOT_APPROVED
NEXT=resolve pdf-inspector page-scoped text gaps or reconcile formal G5 blank-page evidence; do not rerun G6-00E
