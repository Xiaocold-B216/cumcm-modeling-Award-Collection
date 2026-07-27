# A7 Final Closeout and Baseline Verification Disposition

## Input state

- Repository branch: `analysis/corpus-index`
- Local, tracking, and remote HEAD before closeout: `173393b0705ea67088e9683614ac875b891cba6e`
- Prior blocked A7 commit: `b4d31fc6bb3b0373464f1f7f92322390e0ab446b`
- Approved blocker repair commit: `d07dcfdd41fc778947e768835a13f9e3029f79cd`
- Prior A7 rerun commit: `173393b0705ea67088e9683614ac875b891cba6e`
- Initial state check: branch, HEAD, fetch, ls-remote, diff check, and clean worktree all passed.
- A8 was not started.

## Baseline object recovery

Target object: `a042ecf898feaba6fc81d543a10e0188db8b2b12`.

| Attempt | Command class | Exit code | Object available | Result |
|---:|---|---:|---|---|
| 0 | `git cat-file -e <sha>^{commit}` | 128 | No | Local object was missing |
| 1 | Bounded SHA fetch using HTTP/1.1, Schannel, no tags, blob filter | 0 | Yes | Recovery succeeded |
| 2 | Fetch `origin main` | Not run | Yes | Not needed after attempt 1 |
| 3 | Deepen `origin main` by 500 | Not run | Yes | Not needed after attempt 1 |

The recovered object is a commit with subject `data: import award papers 2024-2025`. The environment waiver is not applicable because the object became available.

## Infrastructure terminal result

`tests/test_infrastructure.py` was executed first after recovery:

| Collected | Passed | Failed | Errors | Exit |
|---:|---:|---:|---:|---:|
| 11 | 9 | 2 | 0 | 1 |

The two failures are not waiver-eligible:

1. `test_source_verification_and_baseline_count` found committed protected-source differences: `2016_missing_files.txt`, `2017_missing_files.txt`, `2018_missing_files.txt`, `2021_PACKAGE_README.md`, `2022_missing_files.txt`, and `2024_missing_files.txt`.
2. `test_unicode_baseline_paths_are_real_checkout_paths` failed with a subprocess Unicode decoding error after the object was available.

## A7 quality gates

- Full collection: 306 nodes; collection/import/syntax errors: 0.
- Annual collection: 267 nodes; 2017: 24 nodes.
- Annual regression: 240 passed, 25 retained failed, 2 skipped, 0 errors, 0 timeout.
- Additional regression: 16 passed, 12 retained failed, 0 errors.
- Full regression: 265 passed, 39 failed, 2 skipped, 0 errors.
- No new annual failures, skip, xfail, timeout, or collection error.
- Schema validation: 5,314 mapped instances, 0 errors.
- Strict JSON/JSONL/CSV/Markdown audit: passed; four run logs valid; two Markdown BOMs removed.
- Cross-file numeric mismatches: 0; hash mismatches: 0; queue duplicate IDs: 0.
- Retained assertion failures remain explicitly recorded and were not rewritten or suppressed.
- Unwaived infrastructure failures: 2.
- Hard pytest errors: 0.

## Final conclusion

`A7 = failed`

The bounded object recovery succeeded, so the authorized environment waiver cannot be used. The infrastructure result contains a real protected-source difference and a separate Unicode subprocess failure. These are not pure local-object-availability assertions. No test or business file was modified to bypass them.

`A8 = not_ready_to_start`

A8 was not executed in this round.
