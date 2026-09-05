# G9 INDEX REBUILD

- Status: `PASS`
- Attempt: `20260903T160128144016_9197919c`
- Baseline: `library-refactor-v1` at `557724fba6572d4d83dc421feda5b17b13ff8d66`

## Canonical contract and authoritative inputs

The historical G7 paper-index contract was discovered from `catalog/pilot/g7_paper_index.csv; tools/40_g7_pilot_index_final_qa.py`. The current formal index is the single logical-identity projection at `catalog/scale/g9_paper_index.csv`; the historical `catalog/pilot` index was not modified.

The rebuild consumed the frozen G8 result, `g8_artifact_eligibility.csv`, `g8_artifact_manifest.csv`, `g8_paper_status.csv`, `catalog/papers.csv`, `catalog/paper_files.csv`, canonical `metadata.yaml` files, and the existing `files.csv` inventory. Identity, membership, eligibility, and artifact references were not inferred from filenames, PDF globs, OCR, or directory names.

## Cardinality and relationships

The promoted paper index has `453` one-record-per-identity records, `1359` primary artifacts, and SHA256 `86A9E164D6F313441F415EE853522732F07FF7881943D89F38C7877C1B8E727D`. Eligible PAPER identities are covered 453/453; the 189 ineligible identities, including PROBLEM_PACKAGE entities, are excluded. Each indexed identity has exactly one complete three-artifact set and at least one valid PaperFileMembership relationship.

## Old/new diff and safety boundary

The old formal index contained `0` records with SHA256 ``. The new build added `453`, removed `0`, and changed `0` records; expected changes were `453` and unexpected changes were `0`.

This stage performed no artifact generation, artifact-content rewrite, OCR, PDF render/extraction, Word/DOC operation, source or catalog governance mutation, network access, dependency installation, Git operation, or G10 operation. The index and its JSONL search projection were built in a unique stage, validated, atomically promoted, and validated again.

## Evidence

- `formal_index_csv`: `catalog/scale/g9_paper_index.csv`
- `formal_index_jsonl`: `catalog/scale/g9_paper_index.jsonl`
- `result`: `catalog/scale/g9_index_rebuild_result.json`
- `attempt`: `catalog/scale/g9_index_rebuild_attempt.json`
- `diff`: `catalog/scale/g9_index_rebuild_diff.csv`
- `validation`: `catalog/scale/g9_index_validation.csv`
- `report`: `reports/scale/G9_INDEX_REBUILD.md`

## Validation

- G8 final state, branch, and HEAD matched the frozen baseline.
- Canonical 22-field index schema was discovered from the historical G7 contract; current formal scale index was built as one record per logical identity.
- 453 eligible PAPER identities and 1359 primary artifacts passed staged and post-promotion relationship/hash validation.
- 189 ineligible identities, including PROBLEM_PACKAGE entities, were excluded from the formal paper index.
- Old/new diff was computed; all changes were expected additions for the previously absent formal scale index.
- Protected artifact, eligibility, identity, membership, source, and backlog snapshots remained byte-stable.
- Post-promotion CSV/JSONL projection equality and final SHA 86A9E164D6F313441F415EE853522732F07FF7881943D89F38C7877C1B8E727D passed.

## Issues

- none

## Diff evidence

- Detailed rows: `catalog/scale/g9_index_rebuild_diff.csv` (453 rows).
