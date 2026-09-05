# G11 Targeted Visual Review Status Contract

## Stage

`G11-TARGETED-VISUAL-REVIEW-STATUS-CONTRACT`

This stage closes the contract-definition blocker from the prior manual transcription attempt. It does not perform any of the 53 human page decisions.

## Why the prior transcription was blocked

The targeted visual decision sheet already contained a `review_status` column, but the Review Guide did not define a completed status value or an explicit enum. The prior attempt therefore stopped with `REVIEW_STATUS_ENUM_UNSPECIFIED` before writing any decision row. The 53 rows remain untouched and `PENDING`.

## Frozen contract

`review_status` has exactly two allowed values:

- `PENDING`: 尚未完成人工审核。
- `REVIEWED`: 已由真人完成审核。

After a human finishes reviewing a page, the row must use `review_status=REVIEWED`.

`source_visual_classification` is independent from `review_status`. It describes the page decision and has the allowed values `PENDING`, `SUBSTANTIVE_CONTENT`, `LEGITIMATE_NONCONTENT`, and `UNCLEAR`. `review_status` describes completion of human review; it is not a content classification and must not be replaced with a content label.

The machine-readable contract is recorded in `catalog/scale/g11_targeted_visual_review_status_contract.json`.

## Next transcription use

The next transcription attempt may inspect the frozen visual packets and update the corresponding row's `source_visual_classification`, optional `reviewer_comment`, and `review_status`. For each page that has actually been reviewed, set `review_status=REVIEWED`; retain `review_status=PENDING` for pages not yet reviewed. Do not alter the frozen sample identities, source fields, formal fields, or original G11 decision sheet.

## Scope and validation

This stage only updates the Review Guide and writes the status contract/report. The targeted decision sheet was read-only; its SHA256 was unchanged before and after validation. No Word, OCR, PDF rendering, extraction, batch conversion, formal artifact, index, eligibility, backlog, G9, G10, G12, network, dependency, or Git operation was run.

`BLOCKER=NONE`

`NEXT=G11-TARGETED-VISUAL-DIAGNOSTIC-MANUAL-DECISION-TRANSCRIPTION-RESUME`
