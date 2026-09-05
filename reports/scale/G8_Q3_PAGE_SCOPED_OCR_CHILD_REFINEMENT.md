# G8 Q3 Page-scoped OCR Child Refinement

STATUS=PASS

The original timeout was a multi-page routed OCR child timeout. Its page number was not recoverable because the old child represented multiple routed pages and the old audit row had no page context.

The runner now enforces one routed page per TESSERACT_OCR child, requires paper_id and page_number, uses PHASE_6_SELECTIVE_PAGE_OCR, runs sequentially in ascending page order, stops after the first timeout, and keeps automatic retry disabled.

DIAGNOSTIC_ATTEMPT_ID=20260902T130335889202_page_scoped_c6d2bda3
DIAGNOSTIC_PAPER_ID=CUMCM-2020-B-002
DIAGNOSTIC_PAGE_COUNT=104
DIAGNOSTIC_OCR_REQUIRED_PAGE_COUNT=104
DIAGNOSTIC_OCR_COMPLETED_PAGE_COUNT=104
DIAGNOSTIC_OCR_TIMEOUT_PAGE_COUNT=0
DIAGNOSTIC_OCR_QUALITY_FAIL_PAGE_COUNT=0

PAGE_SCOPED_SUCCESSFUL_OCR_COUNT=104
PAGE_OCR_DURATION_MIN_MS=867
PAGE_OCR_DURATION_MEDIAN_MS=2076
PAGE_OCR_DURATION_P90_MS=2917
PAGE_OCR_DURATION_P95_MS=3089
PAGE_OCR_DURATION_P99_MS=3605
PAGE_OCR_DURATION_MAX_MS=4752

ORIGINAL_TIMEOUT_ROOT_CAUSE=MULTI_PAGE_CHILD_CUMULATIVE_TIMEOUT_BUDGET
TIMEOUT_POLICY_DECISION=RETAIN_180_PER_PAGE_TIMEOUT
TESSERACT_OCR_TIMEOUT_SECONDS_OLD=180
TESSERACT_OCR_TIMEOUT_SECONDS_NEW=180

The page-scoped replay is diagnostic evidence only. It does not resume the old attempt, generate a Q3 extraction contract, process CUMCM-1992-A-004, touch completed identities, run batch extraction, or generate formal artifacts.

The final contract SHA and evidence fingerprint are stored in the refinement result outside this raw evidence member set to avoid self-reference.
