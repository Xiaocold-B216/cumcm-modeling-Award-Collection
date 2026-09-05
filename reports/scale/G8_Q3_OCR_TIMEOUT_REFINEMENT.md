# G8 Q3 OCR Timeout Refinement

## Status

`STATUS=BLOCKED`

The source attempt `20260902T115802455758_405d9fa9` contains exactly one timeout row for `CUMCM-2020-B-002`, but the durable row has no page number. The original runner sent the complete OCR target-page list for the identity to one Tesseract child, so the timeout is document-scoped rather than page-scoped. There is no persisted page audit or progress file from which the exact timeout page can be recovered.

The source remains intact and readable: SHA256 matches `26781A9C92E48A6FD495960C27AEB6E66B1C0A2A89DB7F07BD6C0362A68E6A9E`, and Poppler reports 104 pages.

## Original timeout evidence

- `tool_kind=TESSERACT_OCR`
- `original_phase=PHASE_4_PAGE_AUDIT`
- `duration_ms=180078`
- `timeout_seconds=180`
- `child_pid=53164`
- `exit_code=1`
- `cleanup_attempted=1`
- `cleanup_success=1`
- `stdout_bytes=0`
- `stderr_bytes=0`
- `TIMEOUT_CHILD_STILL_RUNNING=0`

The phase label was a label-propagation defect: formal Tesseract OCR belongs to `PHASE_6_SELECTIVE_PAGE_OCR`. The runner was minimally repaired so future OCR calls use that phase and one wrapper child is created per target page, with the page number written into the child audit row. This conforms to the existing refinement contract; the refinement contract SHA and evidence fingerprint therefore remain unchanged.

## Successful OCR duration distribution

The original audit contains 4 successful Tesseract child records covering 141 successfully OCR-processed pages. It does not contain 141 page-scoped child records. Using numeric `duration_ms` sorting and nearest-rank percentiles on the 4 durable child records:

| Metric | Value |
|---|---:|
| Successful OCR child records | 4 |
| Successful OCR pages | 141 |
| Minimum | 3653 ms |
| Median | 4121 ms |
| P90 | 166498 ms |
| P95 | 166498 ms |
| P99 | 166498 ms |
| Maximum | 166498 ms |
| >=120 s | 1 |
| >=150 s | 1 |
| >=170 s | 0 |

The slowest successful child was `CUMCM-2020-D-003` at 166498 ms. No successful page was re-OCRed during this refinement.

## Diagnostic decision

No 180-second reproduction was run. The contract requires an exact timeout page before page-scoped classification, rendering, and OCR reproduction. Since the original child was not page-scoped and the exact page was not durably recorded, selecting a page would be an unsupported guess. Consequently, no 360-second comparison was allowed.

`TIMEOUT_POLICY_DECISION=UNRESOLVED_TIMEOUT_PAGE_EVIDENCE`

The 180-second production timeout remains unchanged and automatic retry remains forbidden. The phase attribution correction changes operational evidence semantics only; extraction semantics and timeout policy were not changed.

## Freeze checks

- Inventory and selection were not rerun.
- No pilot identity was processed or modified.
- The four completed identities were not touched.
- `CUMCM-1992-A-004` was not touched.
- No formal artifacts, batch run, G9, G10, Word, network, dependency installation, or Git operation occurred.
- Artifact/backlog state remains 325 sets, 975 primary artifacts, DOC backlog 0, Q3 backlog 128, eligible 453, ineligible 189.

## Outputs

- `catalog/scale/g8_q3_ocr_timeout_diagnostic.csv`
- `catalog/scale/g8_q3_ocr_timeout_refinement_result.json`
- `tools/72_g8_q3_contract_pilot_resume.py`

## Blocker and next step

`BLOCKER=TIMEOUT_PAGE_NUMBER_UNRESOLVED`

The stage remains blocked pending a future refinement that can recover or regenerate durable page-scoped evidence for the original timeout. No full Pilot retry is authorized by this stage.

`NEXT=G8-Q3-CONTRACT-REFINEMENT`
