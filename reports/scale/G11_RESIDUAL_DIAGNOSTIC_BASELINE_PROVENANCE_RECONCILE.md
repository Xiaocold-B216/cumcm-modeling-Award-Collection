# G11 Residual Diagnostic Baseline Provenance Reconcile

- Stage: `G11-RESIDUAL-DIAGNOSTIC-BASELINE-PROVENANCE-RECONCILE`
- Status: `PASS`
- Current formal baseline: `642` identities; `453` artifact sets; `1359` primary artifacts; index `453`; backlog `0`.

## Baseline conclusion

The live formal state is 453 artifact sets and 1,359 primary artifacts, not 308 and 924. DOC and Q3 current backlogs are both zero. The four stale values are mixed historical/reporting provenance: the 308/924 values are the old DOC-generation pre-Q3 snapshot and hardcoded baseline constants, while 18/128 are historical DOC-contract/content-review reporting values and the old Q3 backlog before Q3 formal promotion.

## Provenance

- 308: `catalog/scale/g8_doc_formal_artifact_generation_result.json:EXISTING_ARTIFACT_SET_COUNT_BEFORE=308; tools/65_g8_doc_formal_artifact_generation.py:line 39: historical DOC baseline constant`
- 924: `catalog/scale/g8_doc_formal_artifact_generation_result.json:EXISTING_PRIMARY_ARTIFACT_COUNT_BEFORE=924; tools/65_g8_doc_formal_artifact_generation.py:line 39: historical DOC baseline constant`
- 18: `tools/g8_doc_content_sanity_review.py:line 256:18; reports/scale/G8_DOC_CONTENT_SANITY_REVIEW.md:line 8: historical before/after report`
- 128: `catalog/scale/g8_doc_formal_artifact_generation_result.json:Q3_MANUAL_BACKLOG=128; tools/65_g8_doc_formal_artifact_generation.py:line 39: historical pre-Q3 backlog constant`
- Classification: `MIXED_CAUSE`; no live formal-state regression was found.

## Evidence binding

- All `2951` residual rows bind to current identity, artifact, formal body, source, membership, and G9 index state with zero mismatches.
- The `82` confirmed pages across `30` identities bind to the same current state with zero mismatches.
- CUMCM-2020-D-003 remains eligible, artifact-present, index-present, source-bound, with root cause `Q3_OCR_PAGE`.
- Existing 2,951 pdftotext outputs, 82 positive calibration outputs, and 4 negative calibration outputs were checked read-only; no probe was rerun.

## Identity semantics

`215 + 23 = 238`: unresolved-only plus confirmed-with-residual identities equals identities with any residual unresolved page. `23 + 7 = 30`: confirmed-with-residual plus confirmed-without-residual equals confirmed identities.

## Safety

No source, formal artifact, identity, membership, eligibility, backlog, G9/G10, or prior G11 evidence was modified. No OCR, rendering, extraction, Word, network, dependency installation, or PDF page probe was run.

## Outputs

- `catalog/scale/g11_residual_diagnostic_baseline_reconcile_result.json`
- `reports/scale/G11_RESIDUAL_DIAGNOSTIC_BASELINE_PROVENANCE_RECONCILE.md`

## Next

`G11-MARKER-ONLY-IMAGE-RESIDUAL-SCOPE-DIAGNOSTIC`
