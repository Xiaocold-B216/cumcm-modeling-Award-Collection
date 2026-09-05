STAGE=G6-00H-R
STATUS=PASS
BRANCH=library-refactor-v1
HEAD=a042ecf898feaba6fc81d543a10e0188db8b2b12
PYTHON_EXECUTABLE=D:\python\python.exe
PYTHON_VERSION=3.13.15
TARGET_REVIEW_CANDIDATES=5
TARGET_ROWS=5
TARGET_SUBJECT_TYPE_RESOLVED=5
TARGET_SUBJECT_TYPE_AMBIGUOUS=0
TARGET_ARTIFACT_ELIGIBILITY_RESOLVED=5
TARGET_PAPER_COUNT=0
TARGET_PROBLEM_PACKAGE_COUNT=5
TARGET_SUPPORTING_MATERIAL_COUNT=0
TARGET_AMBIGUOUS_COUNT=0
TARGET_ARTIFACT_ELIGIBLE_COUNT=0
TARGET_ARTIFACT_INELIGIBLE_COUNT=5
TARGETS_FORM_A_E_PROBLEM_SET=1
PILOT_UNIQUE_IDENTITIES=28
PILOT_ARTIFACT_ELIGIBLE_ENTITIES=22
PILOT_ARTIFACT_INELIGIBLE_ENTITIES=6
PILOT_AMBIGUOUS_ENTITIES=0
EXPECTED_PAPER_ARTIFACT_SETS=22
EXPECTED_PRIMARY_G6_ARTIFACTS=66
G6_PAPER_ARTIFACT_MAP_R2_ROWS=28
PAPER_ARTIFACT_MAP_R2_UNKNOWN_ELIGIBILITY=0
PAPER_ARTIFACT_MAP_R2_EXPECTED_ARTIFACT_SUM=66
ELIGIBILITY_REVIEWED_ROWS=6
REMAINING_ELIGIBILITY_REVIEW_CANDIDATES=0
DUPLICATE_ELIGIBILITY_ROWS=0
DUPLICATE_ELIGIBILITY_PAPER_IDS=0
DUPLICATE_PAPER_ARTIFACT_MAP_R2_ROWS=0
SOURCE_SHA_MISMATCH=0
G1_CATALOG_MODIFIED=0
G2_CATALOG_MODIFIED=0
G3_IDENTITY_MODIFIED=0
G3_MEMBERSHIP_MODIFIED=0
G4_OUTPUT_MODIFIED=0
G5_OUTPUT_MODIFIED=0
G5_REPAIR_MANIFEST_MODIFIED=0
G5_OCR_DERIVATIVES_MODIFIED=0
G6_FILE_SOURCE_MAP_MODIFIED=0
G6_HISTORY_MODIFIED=0
ORIGINAL_FILES_MODIFIED=0
ORIGINAL_FILES_DELETED=0
ORIGINAL_FILES_MOVED_OR_RENAMED=0
OCR_RUN=0
PDF_REPAIR_RUN=0
SOURCE_REACQUISITION_RUN=0
DOC_TO_PDF_CONVERSION_RUN=0
NEW_EXTRACTION_BACKEND_INSTALLED=0
FULL_PILOT_EXTRACTION_RUN=0
FORMAL_G6_ARTIFACTS_GENERATED=0
G6_15_RUN=0
G6_25_RUN=0
G6_INT_RUN=0
G7_RUN=0
IDEMPOTENCY_PASS=1

TARGET_CLASSIFICATION_SUMMARY=
- paper_id: CUMCM-2025-A-001
  subject_type: PROBLEM_PACKAGE
  artifact_eligible: 0
  reason: Official 2025 A-E competition problem package, not a contestant paper body; retain G3 identity but exclude from Paper-level G6 artifacts.
  evidence: Parent directory 2025年数学建模国赛真题+优秀论文/2025年数学建模国赛真题！/A题; sibling directories A题, B题, C题, D题, E题 form the A-E set; primary filename A题.pdf; one canonical primary membership; Paper metadata title/authors are unknown; source identifier 001 is an internal ID, not proof of a paper; no dedicated sources.csv row; catalog/files.csv inventory and PaperFileMembership are authoritative; no paper/优秀论文/参赛作品 signal.
- paper_id: CUMCM-2025-B-001
  subject_type: PROBLEM_PACKAGE
  artifact_eligible: 0
  reason: Official 2025 A-E competition problem package, not a contestant paper body; retain G3 identity but exclude from Paper-level G6 artifacts.
  evidence: Parent directory 2025年数学建模国赛真题+优秀论文/2025年数学建模国赛真题！/B题; sibling directories A题, B题, C题, D题, E题 form the A-E set; primary filename B题.pdf; one canonical primary membership; Paper metadata title/authors are unknown; source identifier 001 is an internal ID, not proof of a paper; no dedicated sources.csv row; catalog/files.csv inventory and PaperFileMembership are authoritative; no paper/优秀论文/参赛作品 signal.
- paper_id: CUMCM-2025-C-001
  subject_type: PROBLEM_PACKAGE
  artifact_eligible: 0
  reason: Official 2025 A-E competition problem package, not a contestant paper body; retain G3 identity but exclude from Paper-level G6 artifacts.
  evidence: Parent directory 2025年数学建模国赛真题+优秀论文/2025年数学建模国赛真题！/C题; sibling directories A题, B题, C题, D题, E题 form the A-E set; primary filename C题.pdf; one canonical primary membership; Paper metadata title/authors are unknown; source identifier 001 is an internal ID, not proof of a paper; no dedicated sources.csv row; catalog/files.csv inventory and PaperFileMembership are authoritative; no paper/优秀论文/参赛作品 signal.
- paper_id: CUMCM-2025-D-001
  subject_type: PROBLEM_PACKAGE
  artifact_eligible: 0
  reason: Official 2025 A-E competition problem package, not a contestant paper body; retain G3 identity but exclude from Paper-level G6 artifacts.
  evidence: Parent directory 2025年数学建模国赛真题+优秀论文/2025年数学建模国赛真题！/D题; sibling directories A题, B题, C题, D题, E题 form the A-E set; primary filename D题.pdf; one canonical primary membership; Paper metadata title/authors are unknown; source identifier 001 is an internal ID, not proof of a paper; no dedicated sources.csv row; catalog/files.csv inventory and PaperFileMembership are authoritative; no paper/优秀论文/参赛作品 signal.
- paper_id: CUMCM-2025-E-001
  subject_type: PROBLEM_PACKAGE
  artifact_eligible: 0
  reason: Official 2025 A-E competition problem package, not a contestant paper body; retain G3 identity but exclude from Paper-level G6 artifacts.
  evidence: Parent directory 2025年数学建模国赛真题+优秀论文/2025年数学建模国赛真题！/E题; sibling directories A题, B题, C题, D题, E题 form the A-E set; primary filename E题.pdf; one canonical primary membership; Paper metadata title/authors are unknown; source identifier 001 is an internal ID, not proof of a paper; no dedicated sources.csv row; catalog/files.csv inventory and PaperFileMembership are authoritative; no paper/优秀论文/参赛作品 signal.

PILOT_ELIGIBILITY_SUMMARY=
- unique identities: 28
- eligible: 22
- ineligible: 6
- ambiguous: 0
- expected artifact sets: 22
- expected primary artifacts: 66

OUTPUTS=
- catalog/pilot/g6_artifact_eligibility.csv
- catalog/pilot/g6_paper_artifact_map_r2.csv
- logs/g6_00hr_artifact_eligibility_closure.log
- reports/G6_00HR_artifact_eligibility_closure.md
- tools/38_g6_00hr_artifact_eligibility_closure.py

PRE_EXISTING_CHANGES=?? .bootstrap/
?? .github/
?? .gitignore
?? 2016_missing_files.txt
?? 2017_missing_files.txt
?? 2018_missing_files.txt
?? catalog/
?? derived/
?? logs/
?? reports/
?? tools/
G6_00HR_INTRODUCED_CHANGES=tools/38_g6_00hr_artifact_eligibility_closure.py; catalog/pilot/g6_artifact_eligibility.csv; catalog/pilot/g6_paper_artifact_map_r2.csv; logs/g6_00hr_artifact_eligibility_closure.log; reports/G6_00HR_artifact_eligibility_closure.md

VALIDATION=
- Only the five specified 2025 A-E candidates were subject-type reviewed; ordinary Pilot papers were not re-reviewed.
- All five targets are metadata-resolved PROBLEM_PACKAGE entities from the same A-E sibling set; no PDF content inspection was required.
- G3 identities, memberships, sources, G6 file map, G6 history, G5 outputs, and original files remained protected.
- Eligibility overlay has 6 unique reviewed rows; R2 map closes 28 Pilot identities with expected artifacts computed from eligibility.
- Checked 30 Pilot source members against catalog/files.csv; mismatches=0.
- No OCR, PDF repair, DOC conversion, source reacquisition, new extraction backend, full Pilot extraction, or formal artifact generation occurred.

ISSUES=
- NONE
BLOCKER=NONE
APPROVAL=Pilot artifact eligibility fully reconciled and final G6 artifact population frozen
NEXT=G6-PILOT-AUTO-R2 only after explicit authorization; do not auto-run and do not start G7
