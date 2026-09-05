STAGE=G3-15R
STATUS=PASS
BRANCH=library-refactor-v1
HEAD=a042ecf898feaba6fc81d543a10e0188db8b2b12
PYTHON_EXECUTABLE=D:\python\python.exe
PYTHON_VERSION=3.13.15
TARGET_ATTACHMENT_FILES=2
TARGET_ATTACHMENT_ROWS=2
UNIQUE_TARGET_PATHS=2
UNIQUE_TARGET_SHA256=2
TARGET_UNKNOWN_PAPER_ID_BEFORE=2
TARGET_EXISTING_PAPER=2
TARGET_NEW_PAPER_REQUIRED=0
TARGET_INDEPENDENT_PAPER=0
TARGET_AMBIGUOUS=0
TARGET_PAPER_ID_RESOLVED=2
TARGET_PAPER_ID_UNKNOWN=0
RESOLVED_UNIQUE_PAPER_IDS=1
RESOLVED_PAPER_IDS=CUMCM-2015-D-002
TARGET_MEMBERSHIP_PRESENT_BEFORE=0
TARGET_MEMBERSHIP_CREATED=2
TARGET_MEMBERSHIP_RESOLVED=2
TARGET_WITHOUT_MEMBERSHIP=0
TARGET_BRIDGE_REPAIRED=0
G3_FORMAL_BEFORE=677
G3_FORMAL_AFTER=677
FORMAL_PAPER_DELTA=0
G3_MEMBERSHIPS_BEFORE=2379
G3_MEMBERSHIPS_AFTER=2381
MEMBERSHIP_DELTA=2
G3_SOURCE_ID_PAPERS_BEFORE=41
G3_SOURCE_ID_PAPERS_AFTER=41
G3_INTERNAL_ID_PAPERS_BEFORE=636
G3_INTERNAL_ID_PAPERS_AFTER=636
DUPLICATE_PAPER_ENTITIES=0
MULTI_FILE_PAPERS=1
DUPLICATE_FILE_MEMBERSHIPS=0
DUPLICATE_SOURCE_RECORDS_CREATED=0
NON_TARGET_PAPER_ID_CHANGED=0
NON_TARGET_MEMBERSHIP_CHANGED=0
NON_TARGET_SOURCE_CHANGED=0
PILOT_PDF_FILES=29
PILOT_UNIQUE_PAPERS=28
PILOT_MULTI_FILE_PAPERS=1
PILOT_FILES_WITH_FORMAL_PAPER_ID=29
PILOT_FILES_WITHOUT_FORMAL_PAPER_ID=0
SOURCE_SHA_MISMATCH=0
G1_INVENTORY_FACTS_MODIFIED=0
G2_DUPLICATE_FACTS_MODIFIED=0
G4_OUTPUT_MODIFIED=0
G5_QUALITY_OUTPUT_MODIFIED=0
G5_ROUTING_OUTPUT_MODIFIED=0
G5_OCR_OUTPUT_MODIFIED=0
G5_REPAIR_MANIFEST_MODIFIED=0
G5_DERIVED_PDFS_MODIFIED=0
G6_EXTRACTION_CONTRACT_MODIFIED=0
G6_00F_HISTORY_MODIFIED=0
G6_00G_HISTORY_MODIFIED=0
G6_00GR_HISTORY_MODIFIED=0
ORIGINAL_FILES_MODIFIED=0
ORIGINAL_FILES_DELETED=0
ORIGINAL_FILES_MOVED_OR_RENAMED=0
OCR_RUN=0
PDF_REPAIR_RUN=0
SOURCE_REACQUISITION_RUN=0
PDF_INSPECTOR_EXTRACTION_RUN=0
MARKDOWN_EXTRACTION_RUN=0
G6_RUN=0
FORMAL_G6_ARTIFACTS_GENERATED=0
NEW_PAPER_CREATED_ON_RERUN=0
NEW_MEMBERSHIP_CREATED_ON_RERUN=0
DUPLICATE_MEMBERSHIP_CREATED=0
IDEMPOTENCY_PASS=1

TARGET_MAPPING=
- file: 2015年数学建模国赛真题+优秀论文/2015年赛题/2015年国赛D题附件2 中华人民共和国土地增值税暂行条例.pdf
  sha256: D5AE5C859D9FD9FFD48D5493455D254334D15CBC082F93109FE2AAB9D8697C42
  relationship: EXISTING_PAPER_ATTACHMENT
  paper_id: CUMCM-2015-D-002
  membership_before: MISSING
  membership_after: PRESENT
  evidence: 2015 D-question directory contains the formal main file 2015年国赛D题.doc; G3 maps that main file to CUMCM-2015-D-002; attachment filename and G1/G5 SHA identify official supporting material; no independent-paper evidence.
  status: PASS
- file: 2015年数学建模国赛真题+优秀论文/2015年赛题/2015年国赛D题附件3 其他相关说明.pdf
  sha256: A3C542CF191AB8F7A6FBE4DA6085F4B8A4BC5871E464916F9BC049C9C7E0C3A4
  relationship: EXISTING_PAPER_ATTACHMENT
  paper_id: CUMCM-2015-D-002
  membership_before: MISSING
  membership_after: PRESENT
  evidence: 2015 D-question directory contains the formal main file 2015年国赛D题.doc; G3 maps that main file to CUMCM-2015-D-002; attachment filename and G1/G5 SHA identify official supporting material; no independent-paper evidence.
  status: PASS

OUTPUTS=
- catalog/pilot/g3_15r_attachment_membership_map.csv
- logs/g3_15r_attachment_membership_reconcile.log
- reports/G3_15R_attachment_membership_reconcile.md
- tools/34_g3_15r_attachment_membership_reconcile.py

PRE_EXISTING_CHANGES=all prior untracked workspace entries preserved; the two target membership rows were the only G3 data changes in this stage
G3_15R_INTRODUCED_CHANGES=tools/34_g3_15r_attachment_membership_reconcile.py; catalog/paper_files.csv (2 attachment memberships); catalog/pilot/g3_15r_attachment_membership_map.csv; logs/g3_15r_attachment_membership_reconcile.log; reports/G3_15R_attachment_membership_reconcile.md

VALIDATION=
- Both targets are 2015 D-question attachments in the same source directory as the formal main file 2015年国赛D题.doc, whose existing G3 membership resolves to CUMCM-2015-D-002.
- The attachment filenames and G1/G5 SHA records identify supporting material; no evidence indicates independent contestant papers, so no Paper rows were created.
- Paper uniqueness and file-membership uniqueness were evaluated separately: one existing Paper now has multiple Pilot files, with zero duplicate Paper entities and zero duplicate file memberships.
- Pilot cardinality is file-level: 29 files, 28 unique Papers, 1 multi-file Paper, and 29/29 formal memberships.
- No PDF was opened or extracted; no OCR, repair, G6, or formal G6 artifact generation ran.

ISSUES=
- NONE
BLOCKER=NONE
APPROVAL=2015 D attachment identities reconciled at PaperFileMembership level
NEXT=G6-00E-R2 only after explicit authorization; do not auto-run
