# G11-MAJOR-DEFECT-MINIMAL-REPAIR-PLAN

## Stage result

- `STATUS=PARTIAL`
- `BRANCH=library-refactor-v1`
- `HEAD=557724fba6572d4d83dc421feda5b17b13ff8d66`
- `REPAIR_PLAN_ATTEMPT_ID=g11-major-defect-minimal-repair-plan-3f0e6f95110b0fc2`
- `G11_STATUS_REMAINS=PARTIAL`
- `BLOCKER=REPAIR_SCOPE_OR_LAYER_UNRESOLVED`
- `NEXT=G11-MAJOR-DEFECT-DEEP-DIAGNOSTIC`

This stage is planning-only. No OCR, extraction, rendering, reconstruction, artifact regeneration, index rebuild, G10 rerun, network access, or G12 execution was performed.

## Frozen baseline

`TOTAL_IDENTITIES=642`, `ELIGIBLE=453`, `INELIGIBLE=189`, `ARTIFACT_SETS=453`, `PRIMARY_ARTIFACTS=1359`, `FORMAL_INDEX_RECORDS=453`, `DOC_MANUAL_BACKLOG=0`, `Q3_MANUAL_BACKLOG=0`, and `TOTAL_MANUAL_BACKLOG=0` remained unchanged.

The branch/HEAD gate passed. The decision sheet SHA remained `8078A66F45C0C58F9BA4CF0C85BEB0E331C2BC405C52B93760B999DE00A8FD21`. Protected evidence hashes were unchanged: `1`.

## Full formal scan and classification

- Formal `paper.md` files scanned: `453`
- `source_page` markers: `5114`
- Marker-only page segments: `3033`
- Marker-only candidate identities: `245`
- Fully marker-only formal-body identities: `215`; this exactly rederives the prior `215` subset.
- Legitimate marker-only pages: `0`
- Confirmed defective marker-only pages: `29`
- Unresolved marker-only pages: `3004`
- Confirmed defective identities: `10`
- Unresolved candidate identities: `235`

The classification partition passed: `0 + 29 + 3004 = 3033`. The zero legitimate count is evidence-based: no existing explicit `VERIFIED_BLANK_SOURCE_PAGE` classification intersected this marker-only set. Unobserved pages remain unresolved rather than being guessed as defects.

The previous value `215` is therefore not accepted as the full affected scope. It is the subset whose entire formal body is marker-only. The current broader static candidate scope is `245` identities because it also includes partially populated bodies; only `10` identities have existing source-page evidence sufficient for repair planning. Identity-level unresolved count is non-overlapping: `235` candidates have no confirmed defective page, while `9` of the 10 confirmed targets also contain additional unobserved marker-only pages and remain page-partially unresolved.

## Confirmed formal repair targets

`FORMAL_ARTIFACT_REPAIR_TARGET_COUNT=10`. The target table contains only:

`CUMCM-1999-B-003; CUMCM-2008-C-004; CUMCM-1992-A-003; CUMCM-1993-B-001; CUMCM-1996-B-001; CUMCM-1997-A-008; CUMCM-1998-A-007; CUMCM-2000-A-005; CUMCM-2001-A-001; CUMCM-2002-B-005`

The confirmed page-level repair set contains `29` unique selected source pages. The generated page table also retains all `3033` marker-only segments, including unresolved rows, so unresolved scope is auditable but not actionable.

## Common root cause

`COMMON_ROOT_CAUSE_PATTERN_FOUND=1`

The 10 confirmed defects share this path: `OTHER_FORMAL_DERIVED` → PDF source → Q0 → `pdf-inspector` / native Markdown route → `g8_file_source_map.csv` → extraction contract `1` → page-granular G9 records, while the formal body contains only `source_page` shells for the evidenced pages. The existing OTHER-formal metadata does not record a generator version or formal-generation attempt. Body-hash duplication is correlated context only: all 10 are in governed duplicate groups, but G10 reports `GOVERNED_BODY_HASH_DUPLICATES=32` and `UNEXPECTED_BODY_HASH_DUPLICATES=0`; no identity, membership, source, or duplicate-binding defect was found.

## CUMCM-2020-D-003 independent route

`CUMCM_2020_D_003_REPAIR_LAYER=OCR_PAGE` for selected pages `1, 68, 135`.

Existing Q3 page audit, reconstruction manifest/provenance/quality, and persisted page text are present, nonempty, hash-consistent, and marked OCR-backed. The existing reviewer comment explicitly reports OCR/symbol substitutions affecting variables, coordinates, operators, and model meaning. Therefore the persisted OCR text itself is the supported semantic defect layer, and the minimum plan is selective page OCR followed by reconstruction/body regeneration. The formal body is substantive but has no `source_page` markers; that is a separate page-granularity limitation, not evidence that OCR is correct. Exact corrupt spans are intentionally not invented and must be enumerated in the next targeted page QA stage.

## Repair groups and downstream strategy

- Group A: `10` confirmed Q0 formal marker-only identities. Targeted source text acquisition/extraction, reconstruction, formal body regeneration, artifact repromotion, index refresh, G10 consistency validation, and mandatory human re-review.
- Group B: `1` identity, `CUMCM-2020-D-003`. Selective OCR for pages `1,68,135`, then reconstruction/body regeneration, artifact repromotion, index refresh, G10 validation, and human re-review.
- Group C: `0`.
- Unresolved group: `235` identities / `3004` page segments. Run targeted diagnostic first; do not run full-corpus OCR or automatically add them to repair.

After any actual artifact-content change, plan a targeted artifact promotion followed by a deterministic index projection refresh (full projection rebuild is permitted only if that is the safe implementation) and G10 revalidation of 453 eligible identities, 453 artifact sets, 1359 primary artifacts, hashes, bindings, source provenance, coverage, orphan count, and duplicate governance.

Mandatory G11 re-review remains `11` original MAJOR samples. Newly discovered identities are not added to the frozen 30-sample decision sheet automatically.

## Outputs

- `catalog/scale/g11_formal_artifact_repair_targets.csv`
- `catalog/scale/g11_formal_artifact_repair_pages.csv`
- `catalog/scale/g11_major_defect_minimal_repair_plan_result.json`
- `tools/87_g11_major_defect_minimal_repair_plan.py`

No formal data, formal artifact content, formal index, identity, membership, eligibility, backlog, source, decision, or G12 state was modified.
