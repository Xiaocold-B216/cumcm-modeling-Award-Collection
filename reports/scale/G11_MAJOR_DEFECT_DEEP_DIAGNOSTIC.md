# G11 Major Defect Deep Diagnostic

## Stage result

- `STATUS=PARTIAL`
- `BRANCH=library-refactor-v1`
- `HEAD=557724fba6572d4d83dc421feda5b17b13ff8d66`
- `DEEP_DIAGNOSTIC_ATTEMPT_ID=g11-major-defect-deep-diagnostic-7a065914b3abca5d`
- `AUTHORITATIVE_G11_PREPARATION_ATTEMPT_ID=20260903T172404115633_3c748bc1`
- `BLOCKER=TARGETED_DIAGNOSTIC_REQUIRED`
- `NEXT=G11-TARGETED-VISUAL-DIAGNOSTIC`

This stage is diagnosis-only. It did not run OCR, PDF rendering, PDF extraction, body reconstruction, artifact regeneration, review-packet regeneration, G9, G10, or G12. It did not modify source files, formal artifacts, formal index data, eligibility, frozen decisions, or backlog state.

## Q0 marker semantics and pipeline trace

`SOURCE_PAGE_MARKER_SEMANTICS=PAGE_LOCAL_STRICT_BOUNDARY`.

The traced Q0 route has six stages: (1) source PDF, (2) `pdf-inspector` / native Markdown page extraction, (3) per-page normalization, (4) per-page `source_page` marker insertion, (5) ordered body reconstruction, and (6) `paper.md` serialization. `tools/39_g6_pilot_auto_r2.py` normalizes each page before inserting its marker and joins the page sections in page order. `tools/41_g8_g10_unattended_scale.py` writes that body without a later cross-page reflow.

Therefore native page boundaries are available and preserved through extraction, normalization, and the formal body. Consecutive markers and a marker without local text are allowed by the implementation because every page emits a marker, including an empty extraction result. That implementation allowance is not evidence that the source page was legitimately blank. A text block cannot span multiple source pages under this route, and normalization cannot move text across a marker boundary. The Q3 body is an independent route with no `source_page` markers and is not mixed into this Q0 classification.

The scale file-source map is currently header-only; source path/SHA evidence was therefore read from the eligibility and formal metadata/registry records. `SOURCE_MAP_METADATA_STATUS=G8_SCALE_FILE_SOURCE_MAP_HEADER_ONLY_FALLBACK_TO_ELIGIBILITY_AND_FORMAL_METADATA`.

## Marker-only reclassification

The formal scan found `3033` marker-only page segments across `245` candidate identities. The mutually exclusive page partition is:

| classification | pages | identities |
|---|---:|---:|
| legitimate blank | 0 | 0 |
| structural non-page-local | 0 | 0 |
| confirmed defective content missing | 29 | 10 |
| still unresolved | 3004 | 235 |

Under the proven strict page-local semantics, a marker-only page with existing nonempty source-review evidence and a structural-only formal segment is a confirmed formal content-missing defect. A marker-only page without such evidence remains unresolved. No structural false-positive or legitimate-blank intersection was found. The previous identity-level unresolved count was `235`; the new count is `235`; reduction is `0`.

There are `9` confirmed identities with additional unresolved marker-only pages. They remain in the confirmed identity repair set because at least one page is independently proven defective; the unresolved page rows remain auditable and are not silently repaired.

## Frozen G11 findings and repair scope

All 10 known formal G11 identities were reclassified as `FORMAL_ARTIFACT_PAGE_CONTENT_MISSING` with high confidence. Confirmed IDs: `CUMCM-1999-B-003;CUMCM-2008-C-004;CUMCM-1992-A-003;CUMCM-1993-B-001;CUMCM-1996-B-001;CUMCM-1997-A-008;CUMCM-1998-A-007;CUMCM-2000-A-005;CUMCM-2001-A-001;CUMCM-2002-B-005`. Structural false positives=`0`; other defects=`0`; known G11 remain unresolved=`0`. No human MAJOR decision was changed, downgraded, or expanded.

The resulting repair groups are: Group A = `10` confirmed Q0 formal identities; Group B = `1` independent `CUMCM-2020-D-003` OCR-page identity; Group C = `0`; unresolved diagnostic group = `235` identities / `3004` pages. Formal repair remains a later stage.

## Duplicate and path causality

The existing formal registry has `32` governed duplicate body-hash groups covering `207` identities. In this scan, marker-only segments occur in `31` governed groups, confirmed defects occur in `6` groups, and structural-only groups occur in `0` groups. Formal artifact paths remain one-per-identity: shared path collisions=`0` and unexpected shared body-path groups=`0`. Identity, membership, source, artifact, and index bindings remain valid. Accordingly `SHARED_FORMAL_PATH_IS_CAUSAL=0` and `GOVERNED_DUPLICATE_STATUS_IS_CAUSAL=0`; duplicate body hashes are correlated context, not a binding cause.

## Independent Q3 evidence

`CUMCM-2020-D-003_REPAIR_LAYER=OCR_PAGE`. Existing page-audit rows for pages `1,68,135` are OCR-backed, usable, nonempty, and hash-consistent with the successful persisted OCR audit and page files. The reconstruction manifest is `COMPLETE_VALID`, the provenance is OCR for 135 pages, and the quality record passes. The existing reviewer symptom explicitly reports OCR/symbol substitutions affecting model meaning. No new OCR or rendering was run.

## Targeted diagnostic sample

`TARGETED_VISUAL_DIAGNOSTIC_REQUIRED=1`. Because `235` identities remain unresolved, a deterministic maximum-20 identity sample was written to `catalog/scale/g11_deep_diagnostic_visual_sample.csv`. It is stratified by year/problem where possible and covers duplicate status, fully marker-only status, and marker-count bins/extremes. It is a plan for the next targeted visual diagnostic only; `PDF_RENDER_RUN=0`.

## Frozen-state and operation gates

- `PREVIOUS_ARTIFACT_SETS=453`; `PREVIOUS_PRIMARY_ARTIFACTS=1359`.
- `DOC_MANUAL_BACKLOG=0`; `Q3_MANUAL_BACKLOG=0`; `TOTAL_MANUAL_BACKLOG=0`.
- Decision SHA unchanged=`1`; protected evidence hashes unchanged=`1`; formal artifact hashes unchanged during this run=`1`.
- `FORMAL_DATA_MODIFICATION_COUNT=0`; `FORMAL_ARTIFACT_CONTENT_MODIFICATION_COUNT=0`; `FORMAL_INDEX_MODIFICATION_COUNT=0`; decision modification counts=`0`; `FORMAL_ELIGIBILITY_MODIFIED=0`.
- `OCR_RUN=0`; `PDF_RENDER_RUN=0`; `EXTRACTION_RUN=0`; `BODY_RECONSTRUCTION_RUN=0`; `ARTIFACT_REGENERATION_RUN=0`; `G9_REBUILD_RUN=0`; `G10_REBUILD_RUN=0`; `G12_RUN=0`.
- `NETWORK_ACCESS_USED=0`; `DOWNLOAD_RUN=0`; `NEW_DEPENDENCY_INSTALLED=0`; `GIT_OPERATIONS=0` (only read-only branch/HEAD checks were used).

## Outputs

- `catalog/scale/g11_major_defect_deep_diagnostic.csv` — identity-level classification for all `245` marker-only candidate identities.
- `catalog/scale/g11_marker_only_page_deep_diagnostic.csv` — page-level classification for all `3033` marker-only segments.
- `catalog/scale/g11_deep_diagnostic_visual_sample.csv` — deterministic maximum-20 unresolved identity sample for the next visual diagnostic.
- `catalog/scale/g11_major_defect_deep_diagnostic_result.json` — machine-readable stage result.
- `tools/88_g11_major_defect_deep_diagnostic.py` — deterministic stdlib-only diagnostic runner.

## Validation

- Q0 pipeline semantics were traced to tools/39_g6_pilot_auto_r2.py and tools/41_g8_g10_unattended_scale.py: native page extraction, per-page normalization, marker insertion, ordered body assembly, and paper.md serialization.
- Static formal scan partition passed: marker-only=3033; legitimate=0; structural=0; confirmed=29; unresolved=3004.
- All 10 frozen Q0 G11 identities were reclassified as confirmed formal content-missing defects; no structural false positive or other-defect classification was introduced.
- Governed duplicate analysis passed: 32 groups / 207 IDs remain governed; marker-only groups=31; confirmed-defect groups=6; structural-only groups=0; path collisions=0.
- CUMCM-2020-D-003 Q3 evidence revalidated with persisted OCR page hashes and reconstruction evidence; selected pages=1,68,135; repair layer=OCR_PAGE.
- No render, OCR, extraction, reconstruction, artifact regeneration, index rebuild, decision edit, network access, dependency installation, or G12 execution occurred.

## Issues

- 235 identity-level candidates remain unresolved because existing evidence does not locate substantive source-page text or prove legitimate blank pages.
- Q3 CUMCM-2020-D-003 remains an independent OCR_PAGE semantic-quality repair target; it was not merged into the Q0 marker-only scope.


## Machine-readable closure

```text
STAGE=G11-MAJOR-DEFECT-DEEP-DIAGNOSTIC
STATUS=PARTIAL
SOURCE_PAGE_MARKER_SEMANTICS=PAGE_LOCAL_STRICT_BOUNDARY
TOTAL_MARKER_ONLY_PAGE_COUNT=3033
LEGITIMATE_BLANK_PAGE_COUNT=0
STRUCTURAL_NON_PAGE_LOCAL_PAGE_COUNT=0
CONFIRMED_DEFECTIVE_PAGE_COUNT=29
STILL_UNRESOLVED_PAGE_COUNT=3004
OLD_UNRESOLVED_IDENTITY_COUNT=235
NEW_UNRESOLVED_IDENTITY_COUNT=235
TARGETED_VISUAL_DIAGNOSTIC_REQUIRED=1
TARGETED_VISUAL_DIAGNOSTIC_SAMPLE_IDENTITY_COUNT=20
FORMAL_DATA_MODIFICATION_COUNT=0
FORMAL_ARTIFACT_CONTENT_MODIFICATION_COUNT=0
FORMAL_INDEX_MODIFICATION_COUNT=0
DECISION_CONTENT_MODIFICATION_COUNT=0
DECISION_SEVERITY_MODIFICATION_COUNT=0
DECISION_REVIEW_STATUS_MODIFICATION_COUNT=0
OCR_RUN=0
PDF_RENDER_RUN=0
EXTRACTION_RUN=0
BODY_RECONSTRUCTION_RUN=0
G9_REBUILD_RUN=0
G10_REBUILD_RUN=0
G12_RUN=0
NETWORK_ACCESS_USED=0
DOWNLOAD_RUN=0
NEW_DEPENDENCY_INSTALLED=0
BLOCKER=TARGETED_DIAGNOSTIC_REQUIRED
NEXT=G11-TARGETED-VISUAL-DIAGNOSTIC
```
