STAGE=G6-00H
STATUS=PASS
BRANCH=library-refactor-v1
HEAD=a042ecf898feaba6fc81d543a10e0188db8b2b12
PYTHON_EXECUTABLE=D:\python\python.exe
PYTHON_VERSION=3.13.15
TARGET_ENTITY_ROWS=1
TARGET_PAPER_ID=CUMCM-2015-D-002
TARGET_MEMBER_FILE_COUNT=3
TARGET_PRIMARY_MEMBER=2015年数学建模国赛真题+优秀论文/2015年赛题/2015年国赛D题.doc
TARGET_ATTACHMENT_COUNT=2
DIRECTORY_SUBJECT_SIGNAL=PROBLEM_PACKAGE_STRONG
SIBLING_PATTERN_SUPPORTS_PROBLEM_PACKAGE=1
FILENAME_PATTERN_SUPPORTS_PROBLEM_PACKAGE=1
TARGET_SUBJECT_TYPE=PROBLEM_PACKAGE
TARGET_SUBJECT_TYPE_RESOLVED=1
TARGET_SUBJECT_TYPE_AMBIGUOUS=0
TARGET_ARTIFACT_ELIGIBLE=0
TARGET_ARTIFACT_ELIGIBILITY_RESOLVED=1
TARGET_PAPER_ARTIFACT_EXCLUSION_REQUIRED=1
DOC_EXTRACTION_CONTRACT_REQUIRED=0
PILOT_UNIQUE_IDENTITIES=28
PILOT_ARTIFACT_ELIGIBLE_PAPERS=27
PILOT_ARTIFACT_INELIGIBLE_ENTITIES=1
EXPECTED_PRIMARY_G6_ARTIFACTS_PREVIEW=81
OTHER_ARTIFACT_ELIGIBILITY_REVIEW_CANDIDATES=5
G3_IDENTITY_MODIFIED=0
G3_MEMBERSHIP_MODIFIED=0
G4_OUTPUT_MODIFIED=0
G5_OUTPUT_MODIFIED=0
G5_REPAIR_MANIFEST_MODIFIED=0
G5_OCR_DERIVATIVES_MODIFIED=0
G6_HISTORY_MODIFIED=0
SOURCE_SHA_MISMATCH=0
ORIGINAL_FILES_MODIFIED=0
ORIGINAL_FILES_DELETED=0
ORIGINAL_FILES_MOVED_OR_RENAMED=0
OCR_RUN=0
PDF_REPAIR_RUN=0
SOURCE_REACQUISITION_RUN=0
DOC_TO_PDF_CONVERSION_RUN=0
NEW_DOC_EXTRACTION_BACKEND_INSTALLED=0
FORMAL_G6_ARTIFACTS_GENERATED=0
G6_15_RUN=0
G6_25_RUN=0
G6_INT_RUN=0
G7_RUN=0
DUPLICATE_ELIGIBILITY_ROWS=0
IDEMPOTENCY_PASS=1

TARGET_EVIDENCE=
- parent_directory: 2015年数学建模国赛真题+优秀论文/2015年赛题
- primary_filename: 2015年国赛D题.doc
- attachment_filenames: 2015年国赛D题附件2 中华人民共和国土地增值税暂行条例.pdf; 2015年国赛D题附件3 其他相关说明.pdf
- source_metadata: G1 original inventory; no dedicated sources.csv row for target files; target SHA records match catalog/files.csv
- sibling_pattern: ['2015年国赛A题.doc', '2015年国赛A题附件1-3.xls', '2015年国赛A题附件4下载说明.doc', '2015年国赛B题.doc', '2015年国赛C题.docx', '2015年国赛D题.doc', '2015年国赛D题附件1 赛题所需的相关数据.doc', '2015年国赛D题附件2 中华人民共和国土地增值税暂行条例.pdf', '2015年国赛D题附件3 其他相关说明.pdf', '全国大学生数学建模竞赛论文格式规范.doc']
- content_evidence: content inspection was not required; directory, membership roles, and filename evidence were decisive.

TARGET_CLASSIFICATION_SUMMARY=
- paper_id: CUMCM-2015-D-002
  subject_type: PROBLEM_PACKAGE
  artifact_eligible: 0
  reason: 2015 D competition problem package, not a contestant paper body
  evidence: primary problem DOC plus official attachments in 2015年赛题 directory; no paper-body evidence.

PILOT_ELIGIBILITY_SUMMARY=
- unique identities: 28
- artifact eligible: 27
- artifact ineligible: 1
- expected artifact sets: 27
- expected primary artifacts: 81

REVIEW_CANDIDATES=
- CUMCM-2025-A-001: 2025年数学建模国赛真题+优秀论文/2025年数学建模国赛真题！/A题/A题.pdf (metadata-only screen: problem/package filename or directory signal; no automatic reclassification)
- CUMCM-2025-B-001: 2025年数学建模国赛真题+优秀论文/2025年数学建模国赛真题！/B题/B题.pdf (metadata-only screen: problem/package filename or directory signal; no automatic reclassification)
- CUMCM-2025-C-001: 2025年数学建模国赛真题+优秀论文/2025年数学建模国赛真题！/C题/C题.pdf (metadata-only screen: problem/package filename or directory signal; no automatic reclassification)
- CUMCM-2025-D-001: 2025年数学建模国赛真题+优秀论文/2025年数学建模国赛真题！/D题/D题.pdf (metadata-only screen: problem/package filename or directory signal; no automatic reclassification)
- CUMCM-2025-E-001: 2025年数学建模国赛真题+优秀论文/2025年数学建模国赛真题！/E题/E题.pdf (metadata-only screen: problem/package filename or directory signal; no automatic reclassification)

OUTPUTS=
- catalog/pilot/g6_artifact_eligibility.csv
- logs/g6_00h_artifact_eligibility.log
- reports/G6_00H_artifact_eligibility.md
- tools/37_g6_00h_artifact_eligibility.py

PRE_EXISTING_CHANGES=all prior untracked workspace entries preserved; G3/G5/G6 inputs were read-only
G6_00H_INTRODUCED_CHANGES=tools/37_g6_00h_artifact_eligibility.py; catalog/pilot/g6_artifact_eligibility.csv; logs/g6_00h_artifact_eligibility.log; reports/G6_00H_artifact_eligibility.md

VALIDATION=
- The target is formally retained as a G3 Paper identity and retains all three PaperFileMembership rows.
- Subject type is classified from directory semantics, sibling problem-file pattern, membership roles, and explicit filenames; no DOC/PDF content extraction was needed.
- The target is excluded from Paper-level G6 artifact generation, reducing the preview from 28 identities / 84 artifacts to 27 eligible Papers / 81 artifacts.
- Metadata-only screening found 5 other candidate(s) for future eligibility review; none was modified.
- No OCR, PDF repair, DOC conversion, new extractor, G6 artifact generation, or G7 run occurred.

ISSUES=
- NONE
BLOCKER=NONE
APPROVAL=CUMCM-2015-D-002 classified as competition problem package and excluded from Paper artifact generation
NEXT=G6-00H-R only after explicit authorization; do not auto-run G6-PILOT-AUTO-R2
