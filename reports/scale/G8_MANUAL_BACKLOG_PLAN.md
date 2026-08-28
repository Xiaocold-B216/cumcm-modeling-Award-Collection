STAGE=G8-MANUAL-BACKLOG-PLAN
STATUS=PASS
BRANCH=library-refactor-v1
HEAD=a042ecf898feaba6fc81d543a10e0188db8b2b12
MANUAL_BACKLOG_ROWS=183
MANUAL_BACKLOG_UNIQUE_PAPER_IDS=183
MANUAL_BACKLOG_DUPLICATES=0
MANUAL_ELIGIBILITY_ROWS=15
MANUAL_UNSUPPORTED_FORMAT_ROWS=40
Q3_MANUAL_ROWS=128
BACKLOG_UNKNOWN_IDENTITIES=0
BACKLOG_ORPHAN_ROWS=0
BACKLOG_ALREADY_ARTIFACT_COMPLETE=0
BACKLOG_ARTIFACT_INCOMPLETE=128
BACKLOG_ELIGIBILITY_UNRESOLVED=55
BACKLOG_ELIGIBILITY_FALSE=0
DEFERRED_PATH_RAW=catalog/scale/g8_deferred_review.csv
DEFERRED_PATH_RESOLVED=D:\cumcm-modeling-Award-Collection\catalog\scale\g8_deferred_review.csv
DEFERRED_PATH_NAME=g8_deferred_review.csv
DEFERRED_PATH_PARENT=D:\cumcm-modeling-Award-Collection\catalog\scale
DEFERRED_PATH_IS_FILE=1
DEFERRED_PATH_IS_DIR=0
DEFERRED_PATH_BUG_CONFIRMED=0
ME15_REVIEW_PACKET_ROWS=15
ME15_HIGH_CONFIDENCE=13
ME15_MEDIUM_CONFIDENCE=2
ME15_LOW_CONFIDENCE=0
ME15_RECOMMENDED_PAPER=2
ME15_RECOMMENDED_PROBLEM_PACKAGE=5
ME15_RECOMMENDED_SUPPORTING_MATERIAL=8
ME15_RECOMMENDED_AMBIGUOUS=0
MF40_FORMAT_INVENTORY_ROWS=40
MF40_SUPPORTED_ALTERNATE_MEMBERSHIP=0
MF40_EXISTING_LOCAL_BACKEND_CANDIDATE=22
MF40_NEW_EXTRACTION_CONTRACT_REQUIRED=17
MF40_CONVERSION_CONTRACT_REQUIRED=0
MF40_ELIGIBILITY_REVIEW_FIRST=1
MF40_EXTENSION_SUMMARY=
- extension: .doc
  count: 17
- extension: image sequence
  count: 22
- extension: other
  count: 1
Q3_FAILURE_CLASS_COUNT=1
Q3_FAILURE_CLASS_ACCOUNTING_SUM=128
Q3_REPAIR_SAMPLE_ROWS=5
Q3_AUTOMATION_POTENTIAL_HIGH=0
Q3_AUTOMATION_POTENTIAL_MEDIUM=128
Q3_AUTOMATION_POTENTIAL_LOW=0
Q3_AUTOMATION_POTENTIAL_NONE=0
CURRENT_ELIGIBLE=417
CURRENT_COMPLETED=289
CURRENT_ELIGIBLE_INCOMPLETE=128
FINAL_ELIGIBLE_COUNT_NOT_FROZEN=1
MANUAL_EXECUTION_PLAN_CREATED=1
MANUAL_EXECUTION_PLAN_ROWS=8
PDF_REPAIR_RUN=0
OCR_RUN=0
OFFICE_CONVERSION_RUN=0
NEW_EXTRACTION_BACKEND_INSTALLED=0
FORMAL_ARTIFACT_GENERATION_RUN=0
G9_RUN=0
G10_RUN=0
SOURCE_SHA_MISMATCH=0
ORIGINAL_FILES_MODIFIED=0
ORIGINAL_FILES_DELETED=0
ORIGINAL_FILES_MOVED_OR_RENAMED=0
SCALE_ARTIFACTS_MODIFIED=0
PILOT_ARTIFACTS_MODIFIED=0
PILOT_FROZEN_OUTPUTS_MODIFIED=0
G8_ARTIFACT_ELIGIBILITY_MODIFIED=0
G8_PDF_QUALITY_AUDIT_MODIFIED=0
G3_IDENTITY_MODIFIED=0
G3_MEMBERSHIP_MODIFIED=0
DUPLICATE_PLAN_ROWS=0
Q3_SAMPLE_SELECTION_STABLE=1
PLAN_ORDER_STABLE=1
IDEMPOTENCY_PASS=1
ELIGIBILITY_PLAN_SUMMARY=
- 15 packets retain formal eligibility unchanged; recommendations are evidence-based and require human decisions.
- Recommended split is recorded per row in g8_me15_review_packets.csv.
UNSUPPORTED_FORMAT_SUMMARY=
- 17 .doc primary sources require a separately approved extraction contract.
- 22 image-sequence primary sources are candidates for existing local read-only inspection only.
- 1 .gitkeep source is an eligibility-first review candidate.
- No supported alternate membership was found in the 40-row inventory.
Q3_FAILURE_CLASS_SUMMARY=
- failure_class: PARTIAL_SCAN
  papers: 128
  sample_count: 5
  automation_potential: MEDIUM
  candidate_repair_strategy: deterministic render/repair contract candidate after sample approval
  next_stage: G8-Q3-CONTRACT-PILOT
EXECUTION_PLAN=
1. G8-ME-15 — resolve 15 Eligibility items first.
2. G8-MF-40 — govern 40 unsupported formats after identity decisions.
3. G8-Q3-CONTRACT-PILOT — validate candidate contract on deterministic representative samples.
4. G8-Q3-BATCH-REPAIR — conditional on pilot approval; retain manual subset on failure.
5. G8-MANUAL-ARTIFACT-CLOSURE — generate only after final eligibility and approved inputs.
6. G8-INT-FINAL — reconcile Scale state.
7. G9-FULL-INDEX — gate-dependent and not run.
8. G10-CONSISTENCY — gate-dependent and not run.
OUTPUTS=
- catalog/scale/g8_me15_review_packets.csv
- catalog/scale/g8_mf40_format_inventory.csv
- catalog/scale/g8_q3_failure_class_summary.csv
- catalog/scale/g8_q3_repair_samples.csv
- catalog/scale/g8_q3_repair_contract_candidates.csv
- catalog/scale/g8_manual_execution_plan.csv
- catalog/scale/g8_manual_backlog_plan_manifest.json
- reports/scale/G8_MANUAL_BACKLOG_PLAN.md
- logs/scale/g8_manual_backlog_plan.log
- tools/44_g8_manual_backlog_plan.py
PRE_EXISTING_CHANGES=untracked project outputs and prior task files preserved
G8_MANUAL_BACKLOG_PLAN_INTRODUCED_CHANGES=planner outputs only; formal Scale/Pilot/G3 files unchanged
VALIDATION=
- 183 backlog rows are unique and map to the 642-row Scale identity universe.
- Category accounting is 15 + 40 + 128 = 183.
- Canonical deferred path is an actual file; no historical malformed directory exists.
- Q3 failure-class accounting is 128 and deterministic sample selection is stable.
- Existing local capabilities were inspected without installation; no OCR, repair, conversion or Artifact generation ran.
- Formal eligibility, PDF quality, Artifact, Pilot and G3 hashes remained unchanged.
ISSUES=
- Final eligible count remains intentionally unfrozen until ME15/MF40 decisions.
- Q3 automation potential is a planning assessment, not contract approval.
BLOCKER=NONE
APPROVAL=Scale manual backlog fully reconciled and split into executable eligibility, unsupported-format, and Q3 repair-governance workstreams
NEXT=G8-ME-15
