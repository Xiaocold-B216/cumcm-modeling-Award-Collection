# G8 Q3 Contract Refinement

STATUS=PASS
STAGE=G8-Q3-CONTRACT-REFINEMENT-DURABILITY-EVIDENCE-CLOSURE

The frozen refinement evidence records a text-layer quality gap for three
identities: all six diagnostic pages were corrupt under pdf-inspector and
low-information under Poppler 25.02.0. The existing six-page OCR diagnostic is
read as evidence only: all six required pages completed with quality PASS. The
three invalid pilot caches remain quarantined, the stage directory is empty,
and the final extraction cache remains empty.

Runner durability is now closed in
`tools/72_g8_q3_contract_pilot_resume.py`. It has attempt IDs, atomic phase
checkpoints, an always-current result writer, timeout fail-closed behavior, and
a single child-process wrapper. The wrapper records SUCCESS, FAILED, and
TIMED_OUT rows through an atomic child-audit writer before returning. Existing
audit schema and global sequence state are validated; write failures block as
`CHILD_PROCESS_AUDIT_PERSISTENCE_FAILURE`.

The temp-only implementation suite passed persistence, restart preservation,
multi-attempt isolation, schema validation, and controlled persistence-failure
blocking. No formal child audit or Pilot evidence was created by this stage.

REFINEMENT_CONTRACT_SHA256=CAED643919AD35E2CD67938E116AE5BCA008C9FB05CC243E28DE2930A38723DB
REFINEMENT_EVIDENCE_FINGERPRINT=3235CCCE44CC467414DE6C4344B1A4C220342E2DCF6A18A2B19235E794D97AC1
REFINEMENT_EVIDENCE_FINGERPRINT_SCOPE=the five frozen member paths listed in g8_q3_contract_refinement_v1.json; final value is kept outside the contract member to avoid self-reference

ARTIFACT_SETS=325
PRIMARY_ARTIFACTS=975
DOC_MANUAL_BACKLOG=0
Q3_MANUAL_BACKLOG=128
ELIGIBLE=453
INELIGIBLE=189

NEXT=G8-Q3-CONTRACT-PILOT-RESUME

## Page-scoped OCR child refinement

STATUS=PASS
BLOCKER=NONE
TESSERACT_OCR_CHILD_GRANULARITY=ONE_ROUTED_PAGE_PER_CHILD
TESSERACT_OCR_PAGE_NUMBER_REQUIRED=1
TESSERACT_OCR_LOGICAL_PHASE=PHASE_6_SELECTIVE_PAGE_OCR
TESSERACT_OCR_TIMEOUT_SCOPE=PER_PAGE_CHILD
TESSERACT_OCR_TIMEOUT_SECONDS=180
PAGE_SCOPED_DIAGNOSTIC_ATTEMPT_ID=20260902T130335889202_page_scoped_c6d2bda3
PAGE_SCOPED_DIAGNOSTIC_PAPER_ID=CUMCM-2020-B-002
PAGE_SCOPED_DIAGNOSTIC_PAGE_COUNT=104
PAGE_SCOPED_DIAGNOSTIC_OCR_COMPLETED_PAGE_COUNT=104
PAGE_SCOPED_DIAGNOSTIC_OCR_TIMEOUT_PAGE_COUNT=0
REFINEMENT_CONTRACT_SHA256=1D8BE5FE247FFF54DD3147B493820AB92C1BFEE211DB6FE8E21D59C64E4F1F2C
REFINEMENT_EVIDENCE_FINGERPRINT=5FA095687812D8FB58CE9F61DCAE88F0B096FDBC2219326A8C77571C3311C70E
NEXT=G8-Q3-CONTRACT-PILOT-RESUME
