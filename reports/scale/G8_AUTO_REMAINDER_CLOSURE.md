STAGE=G8-AUTO-REMAINDER-CLOSURE
STATUS=PASS
BRANCH=library-refactor-v1
HEAD=a042ecf898feaba6fc81d543a10e0188db8b2b12
RESUME_MODE=1
RESUME_STATE_VALID=1
DEFERRED_CANONICAL_PATH=catalog/scale/g8_deferred_review.csv
DEFERRED_CANONICAL_PATH_EXISTS=1
DEFERRED_PATH_CONSTRUCTION_BUG_PRESENT=0
DEFERRED_PATH_CONSTRUCTION_BUG_FIXED=0
DEFERRED_ROWS_LOST=0
DEFERRED_DUPLICATE_PAPER_IDS=0
DEFERRED_BEFORE=183
DEFERRED_AFTER=183
DEFERRED_RESOLVED=0
ELIGIBLE_PAPERS=417
COMPLETED_ELIGIBLE_PAPERS=289
ELIGIBLE_INCOMPLETE_PAPERS=128
ELIGIBLE_INCOMPLETE_ACCOUNTED=128
PREVIOUS_ARTIFACT_SETS_EXPECTED=283
PREVIOUS_ARTIFACT_SETS_VALID=283
PREVIOUS_PRIMARY_ARTIFACTS_VALID=849
PREVIOUS_ARTIFACTS_REGENERATED=0
PREVIOUS_ARTIFACT_HASH_DRIFT=0
Q2_PREVIOUS_TARGET=11
Q2_CURRENT_TARGET=12
Q2_TARGET_DELTA=1
Q2_TARGET_DELTA_EXPLAINED=1
Q2_ALREADY_COMPLETE=6
Q2_REMAINDER_BEFORE=6
Q2_NEWLY_COMPLETED=6
Q2_MANUAL_REQUIRED=0
Q2_REMAINDER_AFTER=0
Q2_TOTAL_NEW_PAGES=202
Q2_UNEXPLAINED_PAGES=0
SYSTEMATIC_Q2_FAILURE=0
OTHER_DEFERRED_BEFORE=55
OTHER_RESOLVED_INELIGIBLE=0
OTHER_RESOLVED_ELIGIBLE_SUPPORTED=0
OTHER_MANUAL_ELIGIBILITY=15
OTHER_MANUAL_UNSUPPORTED_FORMAT=40
OTHER_MANUAL_REQUIRED=0
OTHER_DEFERRED_AFTER=55
Q3_TARGET_PAPERS=128
Q3_AUTOMATION_ELIGIBLE=0
Q3_REPAIR_ATTEMPTED=0
Q3_MANUAL_BACKLOG=128
Q3_MANUAL_BACKLOG_ROWS=128
DUPLICATE_Q3_MANUAL_BACKLOG_ROWS=0
ARTIFACT_TARGET_DELTA=134
NEW_ARTIFACT_COMPLETED_PAPERS=6
TOTAL_ARTIFACT_COMPLETED_PAPERS=289
PAPER_MD_COUNT=289
METADATA_COUNT=289
KNOWLEDGE_CARD_COUNT=289
PRIMARY_ARTIFACT_COUNT=867
MANUAL_BACKLOG_TOTAL=183
MANUAL_Q3_BACKLOG=128
MANUAL_Q2_BACKLOG=0
MANUAL_UNSUPPORTED_FORMAT_BACKLOG=40
MANUAL_ELIGIBILITY_BACKLOG=15
MANUAL_ARTIFACT_BACKLOG=0
MANUAL_OTHER_BACKLOG=0
SOURCE_SHA_MISMATCH=0
ARTIFACT_SHA_MISMATCH=0
ORIGINAL_FILES_MODIFIED=0
ORIGINAL_FILES_DELETED=0
ORIGINAL_FILES_MOVED_OR_RENAMED=0
PILOT_FROZEN_OUTPUTS_MODIFIED=0
G3_IDENTITY_MODIFIED=0
G3_MEMBERSHIP_MODIFIED=0
G8_INT_STATUS=PARTIAL
G9_RUN=0
G10_RUN=0
UNCHANGED_ARTIFACT_HASH_DRIFT=0
IDEMPOTENCY_PASS=1
OUTPUTS=
- catalog/scale/g8_run_state.json
- catalog/scale/g8_deferred_review.csv
- catalog/scale/g8_q2_remainder_diagnosis.csv
- catalog/scale/g8_q2_page_audit.csv
- catalog/scale/g8_q2_ocr_results.csv
- catalog/scale/g8_remainder_reconciliation.csv
- catalog/scale/g8_q3_manual_backlog.csv
- catalog/scale/g8_manual_backlog.csv
- catalog/scale/g8_artifact_manifest.csv
- catalog/scale/g8_paper_status.csv
- reports/scale/G8_AUTO_REMAINDER_CLOSURE.md
- logs/scale/g8_auto_remainder_closure.log
- tools/43_g8_auto_remainder_closure.py
Q2_RECONCILIATION=
- paper_id: CUMCM-2012-A-001
  prior_status: DEFERRED_Q2_EXTRACTION_ANOMALY
  final_status: COMPLETE
  action: reused existing derivative, completed page audit, generated Artifact
- paper_id: CUMCM-2012-A-A285
  prior_status: DEFERRED_Q2_EXTRACTION_ANOMALY
  final_status: COMPLETE
  action: reused existing derivative, completed page audit, generated Artifact
- paper_id: CUMCM-2013-C-010
  prior_status: DEFERRED_Q2_EXTRACTION_ANOMALY
  final_status: COMPLETE
  action: reused existing derivative, completed page audit, generated Artifact
- paper_id: CUMCM-2014-B-B1801
  prior_status: DEFERRED_Q2_EXTRACTION_ANOMALY
  final_status: COMPLETE
  action: reused existing derivative, completed page audit, generated Artifact
- paper_id: CUMCM-2018-B-001
  prior_status: DEFERRED_Q2_EXTRACTION_ANOMALY
  final_status: COMPLETE
  action: reused existing derivative, completed page audit, generated Artifact
- paper_id: CUMCM-2018-D-004
  prior_status: DEFERRED_Q2_EXTRACTION_ANOMALY
  final_status: COMPLETE
  action: reused existing derivative, completed page audit, generated Artifact
OTHER_DEFERRED_RECONCILIATION=
- paper_id: CUMCM-1993-A-001
  prior_reason: MANUAL_ELIGIBILITY_REVIEW
  final_status: ELIGIBILITY_MANUAL
  resolution: manual subject-type/membership review
- paper_id: CUMCM-2011-A-003
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2011-C-002
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2011-C-003
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2011-D-001
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2011-D-007
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2011-D-013
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2011-D-038
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2012-A-003
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2012-B-005
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2012-B-007
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2012-C-001
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2012-C-003
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2012-C-004
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2012-D-001
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2012-D-D044
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2013-A-002
  prior_reason: MANUAL_ELIGIBILITY_REVIEW
  final_status: ELIGIBILITY_MANUAL
  resolution: manual subject-type/membership review
- paper_id: CUMCM-2013-A-006
  prior_reason: MANUAL_ELIGIBILITY_REVIEW
  final_status: ELIGIBILITY_MANUAL
  resolution: manual subject-type/membership review
- paper_id: CUMCM-2013-C-001
  prior_reason: MANUAL_ELIGIBILITY_REVIEW
  final_status: ELIGIBILITY_MANUAL
  resolution: manual subject-type/membership review
- paper_id: CUMCM-2013-C-002
  prior_reason: MANUAL_ELIGIBILITY_REVIEW
  final_status: ELIGIBILITY_MANUAL
  resolution: manual subject-type/membership review
- paper_id: CUMCM-2013-C-003
  prior_reason: MANUAL_ELIGIBILITY_REVIEW
  final_status: ELIGIBILITY_MANUAL
  resolution: manual subject-type/membership review
- paper_id: CUMCM-2013-C-004
  prior_reason: MANUAL_ELIGIBILITY_REVIEW
  final_status: ELIGIBILITY_MANUAL
  resolution: manual subject-type/membership review
- paper_id: CUMCM-2013-C-005
  prior_reason: MANUAL_ELIGIBILITY_REVIEW
  final_status: ELIGIBILITY_MANUAL
  resolution: manual subject-type/membership review
- paper_id: CUMCM-2013-C-006
  prior_reason: MANUAL_ELIGIBILITY_REVIEW
  final_status: ELIGIBILITY_MANUAL
  resolution: manual subject-type/membership review
- paper_id: CUMCM-2013-C-007
  prior_reason: MANUAL_ELIGIBILITY_REVIEW
  final_status: ELIGIBILITY_MANUAL
  resolution: manual subject-type/membership review
- paper_id: CUMCM-2013-C-008
  prior_reason: MANUAL_ELIGIBILITY_REVIEW
  final_status: ELIGIBILITY_MANUAL
  resolution: manual subject-type/membership review
- paper_id: CUMCM-2013-C-009
  prior_reason: MANUAL_ELIGIBILITY_REVIEW
  final_status: ELIGIBILITY_MANUAL
  resolution: manual subject-type/membership review
- paper_id: CUMCM-2013-D-001
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2013-D-002
  prior_reason: MANUAL_ELIGIBILITY_REVIEW
  final_status: ELIGIBILITY_MANUAL
  resolution: manual subject-type/membership review
- paper_id: CUMCM-2013-D-003
  prior_reason: MANUAL_ELIGIBILITY_REVIEW
  final_status: ELIGIBILITY_MANUAL
  resolution: manual subject-type/membership review
- paper_id: CUMCM-2013-D-004
  prior_reason: MANUAL_ELIGIBILITY_REVIEW
  final_status: ELIGIBILITY_MANUAL
  resolution: manual subject-type/membership review
- paper_id: CUMCM-2014-A-006
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2014-B-001
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2014-B-B1604
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2014-D-002
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2014-D-003
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2021-A-A028
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2021-A-A115
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2021-A-A217
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2021-B-B007
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2021-B-B026
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2021-B-B050
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2021-B-B106
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2021-C-C066
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2021-C-C085
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2021-C-C169
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2021-C-C283
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2021-D-D017
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2021-D-D026
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2021-D-D034
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2021-E-E014
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2021-E-E025
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2021-E-E037
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2022-C-C229
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
- paper_id: CUMCM-2022-E-E014
  prior_reason: MANUAL_UNSUPPORTED_FORMAT
  final_status: UNSUPPORTED_FORMAT_MANUAL
  resolution: confirmed Paper has no supported alternate input
MANUAL_BACKLOG_SUMMARY=
- Q3 repair manual: 128
- Q2 manual: 0
- unsupported format manual: 40
- eligibility manual: 15
- artifact manual: 0
- other: 0
ARTIFACT_PROGRESS_SUMMARY=
- before: 283
- newly completed: 6
- final complete: 289
- final primary artifacts: 867
VALIDATION=
- Resume baseline validated exactly: 283 completed Paper sets and 849 primary artifacts.
- Existing 283 Artifact sets were reused; no previous artifact SHA changed.
- Q2 target delta 11 to 12 is explained by CUMCM-2013-C-010 entering the supported PDF Q2 workset during prior Eligibility reconciliation.
- Remaining Q2 processing reused existing local derivatives and did not OCR the six already successful Q2 Papers.
- Q3 classification was frozen as PARTIAL_SCAN; no repair, OCR, PDF conversion, or new contract was attempted.
- G9/G10 were not run.
ISSUES=
- The 40 unresolved Paper sources remain unsupported-format manual backlog.
- The 15 unresolved subject-type/membership cases remain Eligibility manual backlog.
- Q3 remains an independent 128-Paper manual backlog.
BLOCKER=NONE
APPROVAL=All safely automatable G8 remainder closed; only frozen manual backlog remains
NEXT=G8-Q3-MANUAL-PLAN
