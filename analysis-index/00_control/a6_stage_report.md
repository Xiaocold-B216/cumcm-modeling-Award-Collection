# A6 Stage Report: Confirmed Minimal Repair and Local Regression

## Status

- Stage: A6
- Input commit: `2027a39cf32a878812ef8f290738e063eea94131`
- Local status: `completed_locally_pending_remote_readback`
- A5 was not re-run.
- A7 was not started.
- The final A6 status is intentionally left for commit, push, and remote readback.

## Approved scope

The current human approval authorizes only A5-RP-013, A5-RP-014, and A5-RP-015, plus diagnostic-only A5-RP-004. No source delivery or business-data repair was authorized. A5-RP-001 through A5-RP-012 remain deferred.

## Runtime recovery and collection

Validation used the approved existing Anaconda interpreter and no dependency operation. The interpreter reported Python 3.14.6 and pytest 9.1.1. A clean detached worktree at the input commit and the current worktree were collected with the same interpreter:

- baseline: 267 collected, 2017: 24, exit 0;
- current: 267 collected, 2017: 24, exit 0;
- node ID sets: equal;
- collection, import, and syntax errors: zero.

The repository artifacts omit the personal absolute interpreter path; the execution record retains that path outside the repository audit files.

## Applied repairs

- A5-RP-013: queue assertions are year-scoped where appropriate, global gate counts remain explicit, and progress checks respect the partial historical status model.
- A5-RP-014: silent `errors=ignore` scans in 2017, 2018, 2019, and 2025 were replaced with strict UTF-8 decoding and explicit repository-relative decode diagnostics.
- A5-RP-015: page and worksheet upper bounds now use representation, carrier, inspection, observed-page, missing-page, or sheet evidence; BOM input tolerance remains separate from strict output policy.

Only the 11 annual test files named in the repair manifest were modified. A4 artifacts, A5 artifacts, gates, checkpoints, queues, progress, source materials, and business data were not modified.

## Regression results

The 33 approved affected nodes passed. The 2017 annual file was not rerun as a whole. Instead, all 24 nodes were run independently in both trees: current results were 21 passed and 3 failures, with no timeout or error; those 3 failures were the same pre-existing failures as the clean baseline. The baseline-only timeout was `test_20_unknown_not_absent`, and the current strict year-scoped scan completed it successfully.

The other ten annual files (2015, 2016, and 2018-2025) completed independently in baseline/current pairs. Current failures were never greater than the corresponding clean baseline failures, and no new code-induced failure was observed. Existing failures remain explicitly recorded in `a6_regression_results.json`; A6 does not claim that all annual tests pass.

## Quality and boundary checks

- Python compilation of all 11 modified test files passed.
- `git diff --check` passed.
- No new `skip` or `xfail` was introduced.
- No modified test contains `errors='ignore'` or `errors="ignore"`.
- The temporary cache created by validation was removed before the final cache gate check; the cache gate passed.
- No A4 output, A5 output, test input, source material, queue, progress, gate, checkpoint, or report was changed.
- Remote delivery and byte-for-byte remote readback remain pending.

## Stop rule

After the three A6 artifacts are committed, pushed normally, and read back from `origin/analysis/corpus-index`, A6 will be marked passed only if the local and remote commits and artifact bytes match. The workflow then stops. A7 must not be executed in this task.
