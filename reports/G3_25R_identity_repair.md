STAGE=G3-25R
STATUS=PASS
BRANCH=library-refactor-v1
HEAD=a042ecf898feaba6fc81d543a10e0188db8b2b12
PYTHON_EXECUTABLE=D:\python\python.exe
PYTHON_VERSION=3.13.15
TARGET_ROWS=7
UNIQUE_TARGET_PATHS=7
UNIQUE_TARGET_SHA256=7
PROBLEM_PARSE_FAILED=0
G3_FORMAL_BEFORE=670
G3_FORMAL_AFTER=677
FORMAL_PAPER_DELTA=7
G3_UNIQUE_PAPER_IDS_BEFORE=670
G3_UNIQUE_PAPER_IDS_AFTER=677
G3_SOURCE_ID_PAPERS_BEFORE=34
G3_SOURCE_ID_PAPERS_AFTER=41
G3_INTERNAL_ID_PAPERS_BEFORE=636
G3_INTERNAL_ID_PAPERS_AFTER=636
G3_MEMBERSHIPS_BEFORE=2372
G3_MEMBERSHIPS_AFTER=2379
MEMBERSHIP_DELTA=7
G3_FORMAL_2025_BEFORE=5
G3_FORMAL_2025_AFTER=12
SOURCE_IDENTIFIER_IS_IDENTITY_KEY=1
SOURCE_IDENTIFIER_NAMESPACE=year/problem-scoped source_identifier suffix in CUMCM Paper ID; canonical storage sources.csv
SOURCE_IDENTIFIER_UNIQUE_WITHIN_YEAR_PROBLEM=1
TARGET_EXISTING_PAPER=0
TARGET_NEW_PAPER_REQUIRED=7
TARGET_AMBIGUOUS=0
TARGET_SOURCE_ID_PAPERS=7
TARGET_INTERNAL_ID_PAPERS=0
TARGET_PAPER_ID_RESOLVED=7
TARGET_PAPER_ID_UNKNOWN=0
TARGET_MEMBERSHIP_RESOLVED=7
TARGET_MEMBERSHIP_AMBIGUOUS=0
TARGET_WITHOUT_MEMBERSHIP=0
TARGET_WITH_MULTIPLE_FORMAL_PAPER_MEMBERSHIPS=0
DUPLICATE_FORMAL_PAPER_IDS=0
DUPLICATE_TARGET_MEMBERSHIPS=0
DUPLICATE_SOURCE_RECORDS_CREATED=0
NON_TARGET_PAPER_ID_CHANGED=0
NON_TARGET_MEMBERSHIP_CHANGED=0
UNEXPLAINED_FORMAL_DELTA=0
UNEXPLAINED_MEMBERSHIP_DELTA=0
G5_Q2_PATHS_WITH_FORMAL_PAPER_ID=7
SOURCE_SHA_MISMATCH=0
G1_INVENTORY_FACTS_MODIFIED=0
G2_DUPLICATE_FACTS_MODIFIED=0
G4_OUTPUT_MODIFIED=0
G5_QUALITY_OUTPUT_MODIFIED=0
G5_ROUTING_OUTPUT_MODIFIED=0
G5_OCR_OUTPUT_MODIFIED=0
G5_REPAIR_MANIFEST_MODIFIED=0
G5_DERIVED_PDFS_MODIFIED=0
ORIGINAL_FILES_MODIFIED=0
ORIGINAL_FILES_DELETED=0
ORIGINAL_FILES_MOVED_OR_RENAMED=0
OCR_RUN=0
PDF_REPAIR_RUN=0
SOURCE_REACQUISITION_RUN=0
PDF_INSPECTOR_RUN=0
MARKDOWN_EXTRACTION_RUN=0
G6_RUN=0
IDEMPOTENCY_PASS=1

TARGET_IDENTITY_MAP=
- source_identifier: A066
  paper_id: CUMCM-2025-A-A066
  status: PASS_UNIQUE_SOURCE_ID_MAPPING
- source_identifier: A196
  paper_id: CUMCM-2025-A-A196
  status: PASS_UNIQUE_SOURCE_ID_MAPPING
- source_identifier: B060
  paper_id: CUMCM-2025-B-B060
  status: PASS_UNIQUE_SOURCE_ID_MAPPING
- source_identifier: C023
  paper_id: CUMCM-2025-C-C023
  status: PASS_UNIQUE_SOURCE_ID_MAPPING
- source_identifier: C132
  paper_id: CUMCM-2025-C-C132
  status: PASS_UNIQUE_SOURCE_ID_MAPPING
- source_identifier: D037
  paper_id: CUMCM-2025-D-D037
  status: PASS_UNIQUE_SOURCE_ID_MAPPING
- source_identifier: E030
  paper_id: CUMCM-2025-E-E030
  status: PASS_UNIQUE_SOURCE_ID_MAPPING

OUTPUTS=
- catalog/pilot/g3_25r_q2_identity_map.csv
- logs/g3_25r_identity_repair.log
- reports/G3_25R_identity_repair.md
- catalog/papers.csv (7 target Paper rows appended)
- catalog/paper_files.csv (7 target memberships appended)
- catalog/sources.csv (7 target Source rows appended)
- catalog/paper_identity_review.csv (7 target review rows resolved)

PRE_EXISTING_CHANGES=all pre-existing untracked workspace entries recorded before G3-25R; no overwrite of unrelated files
G3_25R_INTRODUCED_CHANGES=tools/29_g3_25r_identity_repair.py; catalog/papers.csv; catalog/paper_files.csv; catalog/sources.csv; catalog/paper_identity_review.csv; catalog/pilot/g3_25r_q2_identity_map.csv; logs/g3_25r_identity_repair.log; reports/G3_25R_identity_repair.md

VALIDATION=
- Frozen G3 contract read and verified: Source-ID suffixes are an allowed ID type.
- All seven target paths were resolved from catalog/files.csv, not from a guessed path or PDF content.
- Problem parsing used the first character of each official Source-ID; all seven passed.
- New Paper IDs use the existing G3 generator format; membership IDs use the existing SHA-256-prefix convention.
- Existing non-target Paper IDs and memberships were preserved byte-semantically at row level.
- G5 catalogs remain unchanged; G5 bridge fields remain paper_id=unknown by design and are not authoritative identity sources.
- Second invocation reused all seven existing Paper, Source, and membership rows.

ISSUES=
- The prompt spelling of the 2025 excellent-paper directory differs by one 年 character from the actual inventory path; the seven targets were normalized to the unique existing catalog/files.csv paths.

BLOCKER=NONE
APPROVAL=2025 Q2 formal Paper ID and membership mapping repaired
NEXT=G6-00F
