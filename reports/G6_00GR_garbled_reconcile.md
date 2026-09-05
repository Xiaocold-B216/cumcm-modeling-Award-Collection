STAGE=G6-00G-RF
STATUS=PASS
STAGE_NAME=G6-00G-R Reconciliation Summary Count Fix
STAGE_TYPE=TARGETED-VALIDATOR-FIX
BRANCH=library-refactor-v1
HEAD=a042ecf898feaba6fc81d543a10e0188db8b2b12
PYTHON_EXECUTABLE=D:\python\python.exe
PYTHON_VERSION=3.13.15
PDF_INSPECTOR_VERSION=1.15.0
POPPLER_VERSION=25.02.0
TARGET_GARBLED_PAGES=8
RECONCILIATION_ROWS=8
VALIDATOR_SUMMARY_BUG_FIXED=1
GARBLED_DETECTOR_RULE=summary-only fix; historical detector remains unchanged
TARGET_TEXT_PAGE_VALID=0
TARGET_TEXT_PAGE_VALID_WITH_NOISY_SYMBOLS=0
TARGET_IMAGE_ONLY_CONTENT_PAGE=4
TARGET_VERIFIED_BLANK_PAGE=4
TARGET_TEXT_PAGE_EXTRACTION_UNRELIABLE=0
TARGET_CLASS_ACCOUNTING_PASS=1
GARBLED_FLAGGED_PAGES=8
UNRESOLVED_GARBLED_PAGES=0
FINAL_TEXT_PAGES=508
FINAL_VERIFIED_BLANK_PAGES=4
FINAL_IMAGE_ONLY_CONTENT_PAGES=4
FINAL_UNEXPLAINED_PAGES=0
GLOBAL_PAGE_ACCOUNTING_PASS=1
PAGE_RECONCILIATION_CHANGED=0
G6_00G_COVERAGE_CONCLUSION_REMAINS_VALID=1
G6_00G_BASELINE_NORMALIZED_RELATIVE_DIFF=5.53247e-05
FILES_WITH_SYSTEMATIC_TEXT_LOSS=0
PAGE_SAMPLE_FAILURES_AFTER_RECONCILIATION=0
COVERAGE_CONCLUSION_CHANGED=0
EXTRACTION_CONTRACT_FROZEN=1
EXTRACTION_CONTRACT_MODIFIED=0
DUPLICATE_CONTRACT_FILES=0
FORMAL_G6_ARTIFACTS_GENERATED=0
FULL_516_PAGE_EXTRACTION_RERUN=0
TARGET_PAGES_ONLY=1
OCR_RUN=0
PDF_REPAIR_RUN=0
IMAGE_REPAIR_RUN=0
SOURCE_REACQUISITION_RUN=0
PDF_INSPECTOR_MODIFIED=0
POPPLER_MODIFIED=0
FORMAL_MARKDOWN_GENERATION_RUN=0
FORMAL_METADATA_GENERATION_RUN=0
FORMAL_KNOWLEDGE_CARD_GENERATION_RUN=0
G6_00E_RERUN=0
G6_15_RUN=0
G6_25_RUN=0
G6_INT_RUN=0
SOURCE_SHA_MISMATCH=0
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
ORIGINAL_FILES_MODIFIED=0
ORIGINAL_FILES_DELETED=0
ORIGINAL_FILES_MOVED_OR_RENAMED=0
DUPLICATE_RECONCILIATION_ROWS=0
RECONCILIATION_CSV_MODIFIED=0
RECONCILIATION_CSV_RECOMPUTATION_MATCH=1
RECONCILIATION_CLASSIFICATION_STABLE=1
IDEMPOTENCY_PASS=1

OUTPUTS=
- D:\cumcm-modeling-Award-Collection\catalog\pilot\g6_q2_garbled_reconciliation.csv
- D:\cumcm-modeling-Award-Collection\catalog\pilot\g6_extraction_contract.json
- D:\cumcm-modeling-Award-Collection\logs\g6_00gr_garbled_reconcile.log
- D:\cumcm-modeling-Award-Collection\reports\G6_00GR_garbled_reconcile.md
- D:\cumcm-modeling-Award-Collection\tools\32_g6_00gr_garbled_reconcile.py

PRE_EXISTING_CHANGES=all pre-existing untracked workspace entries preserved; G6-00G audit, G6-00G-R reconciliation CSV and G6-00F history were read-only
G6_00GRF_INTRODUCED_CHANGES=tools/32_g6_00gr_garbled_reconcile.py; reports/G6_00GR_garbled_reconcile.md; logs/g6_00gr_garbled_reconcile.log

TARGET_CLASSIFICATION_SUMMARY=
- paper_id: CUMCM-2025-B-B060
  source_page: 71
  original_flag: garbled
  visual_type: CODE_LISTING_FRAGMENT_IMAGE_ONLY
  final_status: IMAGE_ONLY_CONTENT_PAGE
  final_text_usable: 0
  poppler_text_chars: 24
  poppler_normalized_chars: 10
  replacement_char_ratio: 0
  control_char_ratio: 0.0416667
  printable_char_ratio: 0.958333
  repeated_sequence_score: 0
  reason: Rendered page contains a small code-listing fragment and heading, but the page is image-backed and the Poppler text is not usable as a reliable text source.
- paper_id: CUMCM-2025-C-C023
  source_page: 9
  original_flag: garbled
  visual_type: WATERMARK_ONLY_PAGE
  final_status: IMAGE_ONLY_CONTENT_PAGE
  final_text_usable: 0
  poppler_text_chars: 23
  poppler_normalized_chars: 9
  replacement_char_ratio: 0
  control_char_ratio: 0.0434783
  printable_char_ratio: 0.956522
  repeated_sequence_score: 0
  reason: Rendered page is blank apart from a publisher watermark; the diagnostic flag is non-blocking and the existing base page class remains unchanged.
- paper_id: CUMCM-2025-C-C023
  source_page: 26
  original_flag: garbled
  visual_type: FIGURE_PAGE
  final_status: IMAGE_ONLY_CONTENT_PAGE
  final_text_usable: 0
  poppler_text_chars: 13
  poppler_normalized_chars: 7
  replacement_char_ratio: 0
  control_char_ratio: 0.0769231
  printable_char_ratio: 0.923077
  repeated_sequence_score: 0
  reason: Rendered page contains a substantive figure/chart, but reliable page text is unavailable; this is an image-only content page, not a text extraction blocker.
- paper_id: CUMCM-2025-C-C132
  source_page: 7
  original_flag: garbled
  visual_type: VERIFIED_BLANK_PAGE
  final_status: IMAGE_ONLY_CONTENT_PAGE
  final_text_usable: 0
  poppler_text_chars: 1
  poppler_normalized_chars: 0
  replacement_char_ratio: 0
  control_char_ratio: 1
  printable_char_ratio: 0
  repeated_sequence_score: 0
  reason: Existing G5/G6 evidence verifies this page as blank. The reconciliation vocabulary has no separate blank status, so the diagnostic row is non-blocking while the base VERIFIED_BLANK_PAGE class is preserved.
- paper_id: CUMCM-2025-C-C132
  source_page: 8
  original_flag: garbled
  visual_type: VERIFIED_BLANK_PAGE
  final_status: IMAGE_ONLY_CONTENT_PAGE
  final_text_usable: 0
  poppler_text_chars: 1
  poppler_normalized_chars: 0
  replacement_char_ratio: 0
  control_char_ratio: 1
  printable_char_ratio: 0
  repeated_sequence_score: 0
  reason: Existing G5/G6 evidence verifies this page as blank. The reconciliation vocabulary has no separate blank status, so the diagnostic row is non-blocking while the base VERIFIED_BLANK_PAGE class is preserved.
- paper_id: CUMCM-2025-C-C132
  source_page: 10
  original_flag: garbled
  visual_type: VERIFIED_BLANK_PAGE
  final_status: IMAGE_ONLY_CONTENT_PAGE
  final_text_usable: 0
  poppler_text_chars: 1
  poppler_normalized_chars: 0
  replacement_char_ratio: 0
  control_char_ratio: 1
  printable_char_ratio: 0
  repeated_sequence_score: 0
  reason: Existing G5/G6 evidence verifies this page as blank. The reconciliation vocabulary has no separate blank status, so the diagnostic row is non-blocking while the base VERIFIED_BLANK_PAGE class is preserved.
- paper_id: CUMCM-2025-C-C132
  source_page: 36
  original_flag: garbled
  visual_type: VERIFIED_BLANK_PAGE
  final_status: IMAGE_ONLY_CONTENT_PAGE
  final_text_usable: 0
  poppler_text_chars: 1
  poppler_normalized_chars: 0
  replacement_char_ratio: 0
  control_char_ratio: 1
  printable_char_ratio: 0
  repeated_sequence_score: 0
  reason: Existing G5/G6 evidence verifies this page as blank. The reconciliation vocabulary has no separate blank status, so the diagnostic row is non-blocking while the base VERIFIED_BLANK_PAGE class is preserved.
- paper_id: CUMCM-2025-D-D037
  source_page: 37
  original_flag: garbled
  visual_type: WATERMARK_ONLY_PAGE
  final_status: IMAGE_ONLY_CONTENT_PAGE
  final_text_usable: 0
  poppler_text_chars: 6
  poppler_normalized_chars: 1
  replacement_char_ratio: 0
  control_char_ratio: 0.166667
  printable_char_ratio: 0.833333
  repeated_sequence_score: 0
  reason: Rendered page is blank apart from a publisher watermark and page number; the diagnostic flag is non-blocking and the existing base page class remains unchanged.

CONTRACT_SUMMARY=
- Existing extraction contract semantics were verified unchanged: Q0/Q1 original PDF -> pdf-inspector native Markdown; Q2 G5 readable PDF -> pdf-inspector whole-document reference -> Poppler single-page extraction -> deterministic wrapper.
- Contract already contained garbled_flag_is_diagnostic_only=true and final_gate=unresolved_garbled_pages_zero; it was not modified.

VALIDATION=
- Recomputed target counts from the existing 8-row CSV: 4 image-only and 4 verified-blank visual types.
- Global counts were recomputed from the existing G6-00G audit plus the unchanged overlay; 508+4+4+0=516.
- The original G6-00G history remains unchanged, including historical POPPLER_GARBLED_PAGES=8.
- No 516-page extraction, OCR, PDF repair, or formal G6 artifact generation ran.

ISSUES=
- NONE
BLOCKER=NONE
APPROVAL=G6-00G-R reconciliation summary corrected and hybrid extraction contract fully closed
NEXT=G6-00E-R only after explicit authorization; do not auto-run
