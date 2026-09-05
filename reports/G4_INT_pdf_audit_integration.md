# G4-INT Pilot PDF Audit Integration

STAGE=G4-INT
STATUS=PASS
BRANCH=library-refactor-v1
HEAD=a042ecf898feaba6fc81d543a10e0188db8b2b12
PYTHON_EXECUTABLE=D:\python\python.exe
PYTHON_VERSION=3.13.15
PDF_AUDIT_SCHEMA_VERSION=1
EXPECTED_PDF_FILES=29
AUDIT_ROWS=29
UNIQUE_AUDITED_FILE_PATHS=29
MISSING_AUDIT_ROWS=0
EXTRA_AUDIT_ROWS=0
DUPLICATE_AUDIT_ROWS=0
AUDIT_SCHEMA_COMPATIBLE=1
REVIEW_SCHEMA_COMPATIBLE=1
SOURCE_SHA_MISMATCH=0
ORIGINAL_SHA_CHANGED_AFTER_INTEGRATION=0
UNIQUE_PDF_SHA256=29
TEXT_BASED=19
SCANNED=0
IMAGE_BASED=7
MIXED=3
TOTAL_PAGE_COUNT=1004
TOTAL_OCR_ROUTED_PAGES=528
PAGE_ZERO_IN_PROJECT_OUTPUT=0
OUT_OF_RANGE_PROJECT_PAGES=0
VISUAL_REVIEW_REQUIRED=10
VISUAL_REVIEW_NOT_REQUIRED=19
FINAL_Q_ASSIGNED=0
FINAL_Q_UNASSIGNED=29
DIRECT_PDF_TYPE_TO_FINAL_Q_MAPPING=0
NEAR_DUPLICATE_INFERENCE_RUN=0
OCR_RUN=0
OCR_OUTPUT_FILES=0
PDF_REPAIR_RUN=0
REPAIRED_PDF_FILES=0
MARKDOWN_EXTRACTION_RUN=0
MARKDOWN_ARTIFACTS_GENERATED=0
SOURCE_REACQUISITION_RUN=0
DEPENDENCY_INSTALL_RUN=0
G4_15_OUTPUT_MODIFIED=0
G4_25_OUTPUT_MODIFIED=0
G1_CATALOG_MODIFIED=0
G2_CATALOG_MODIFIED=0
G3_CATALOG_MODIFIED=0
ORIGINAL_FILES_MODIFIED=0
ORIGINAL_FILES_DELETED=0
ORIGINAL_FILES_MOVED_OR_RENAMED=0

OUTPUTS=
- catalog/pilot/pdf_audit_pilot.csv
- catalog/pilot/pdf_review_pilot.csv
- logs/pdf_audit_pilot_integration.log
- reports/G4_INT_pdf_audit_integration.md

SCHEMA_NOTES=
- Annual raw columns are preserved; only audit_year/audit_source_file and review_year/review_source_file provenance columns were added.
- 2015 schema version is verified from its PASS report and the shared catalog/schema/pdf_audit_schema.json contract; 2025 row values are verified as 1.

VALIDATION=
- Annual audit/review CSVs parsed and merged in deterministic year/path order.
- Inventory, targeted original PDF SHA-256, path coverage, review links, page/OCR routing, and protected-input snapshots checked.
- No OCR, PDF repair, Markdown extraction, source reacquisition, duplicate inference, dependency installation, or API change performed.

ISSUES=
- NONE

DIRECT_MAPPING_EVIDENCE=No direct PDF type/routing to Final Q mapping evidence detected
BLOCKER=NONE
APPROVAL=G4 Pilot PDF audit integration closed
NEXT=G5
