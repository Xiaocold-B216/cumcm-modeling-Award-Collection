# A4 Stage Report

## A4 objective

Execute the 2015-2025 annual test baseline, record real runtime outcomes, and validate/classify A3 findings without modifying tests or business facts.

## Actual completion

- Definition and inputs read and found consistent.
- All 11 annual files collected successfully.
- All 11 annual runs were attempted independently.
- Full logs were stored outside the repository using run IDs; no temporary logs were committed.
- A3 findings were classified in `a4_a3_findings_validation.md`.
- A4 stopped before A5.

## Collection result

| Metric | Value |
|---|---:|
| Annual files | 11 |
| Collected nodes | 267 |
| Collection exit code | 0 |
| Collection wall-clock seconds | 0.641 |

## Annual result summary

| Year | Collected | Passed | Failed | Skipped | Errors | Exit | Wall seconds | Status |
|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 2015 | 36 | 26 | 10 | 0 | 0 | 1 | 0.782 | failed |
| 2016 | 28 | 26 | 2 | 0 | 0 | 1 | 0.672 | failed |
| 2017 | 24 | 0 | 0 | 0 | 0 | 124 | 300.171 | timeout |
| 2018 | 16 | 12 | 4 | 0 | 0 | 1 | 7.706 | failed |
| 2019 | 11 | 10 | 1 | 0 | 0 | 1 | 0.599 | failed |
| 2020 | 32 | 21 | 11 | 0 | 0 | 1 | 0.561 | failed |
| 2021 | 20 | 18 | 2 | 0 | 0 | 1 | 0.848 | failed |
| 2022 | 24 | 18 | 4 | 2 | 0 | 1 | 0.804 | failed |
| 2023 | 28 | 24 | 4 | 0 | 0 | 1 | 0.746 | failed |
| 2024 | 24 | 19 | 5 | 0 | 0 | 1 | 0.586 | failed |
| 2025 | 24 | 20 | 4 | 0 | 0 | 1 | 8.055 | failed |

## Totals

- Collected: 267
- Passed: 194
- Failed: 47
- Skipped: 2
- Errors: 0
- Annual wall-clock seconds: 321.53
- Slowest observed run: 2017 timeout at 300 seconds.
- All-tests-passed claim: false; failures and the timeout are explicitly recorded.

## A3 validation

- Classifications: confirmed defects, intentional behavior, and out-of-scope-for-A4 findings are recorded with two independent checks.
- Human-review triggers: none; no contradictory evidence was found.
- See `analysis-index/00_control/a4_a3_findings_validation.md` for the per-finding evidence.

## Modified files

- Tests modified: no.
- Business files modified: no.
- New A4 outputs: five files under `analysis-index/00_control/`.

## Git and boundary

- The A4 output commit must be independent and use ordinary push plus remote readback.
- The worktree must be clean at the boundary.
- A5 and later stages are not executed.

## Final A4 status

`passed_with_failures_recorded` ? the A4 execution baseline and evidence capture are complete, but the annual tests did not all pass. This status does not authorize A5 execution in this run; stop after remote readback.
