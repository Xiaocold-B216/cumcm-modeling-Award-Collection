# GIT Checkpoint G11 Rereview Ready — Local Handoff Preparation

This file is included in the checkpoint evidence prepared for the user-run
local push. Git metadata writes remain intentionally deferred because the
Codex session must not create `.git/index.lock` or execute the local push
script.

## Pre-commit audit

- Base branch: `library-refactor-v1`
- Base HEAD: `557724fba6572d4d83dc421feda5b17b13ff8d66`
- New branch: `library-refactor-v1-g11-rereview-ready`
- Remote: `origin`
- Fetch URL: `https://github.com/Xiaocold-B216/cumcm-modeling-Award-Collection.git`
- Push URL: `https://github.com/Xiaocold-B216/cumcm-modeling-Award-Collection.git`
- Tracked modified files in the checkpoint index: `11`
- Tracked deleted files: `0`
- Current staged paths before local handoff: `16001`
- Current required INCLUDE paths before preparation outputs: `19057`
- Final expected INCLUDE paths: `19061`
- Final required-but-unstaged paths: `3060`
- Q3 batch repair paths: `2632`
- Q3 pilot extraction paths: `260`
- Historical delta paths in Q3 quarantine: `161`
- Additional current INCLUDE path outside the two primary Q3 trees: `1`
- Excluded transient files: `3961`
- Excluded CI/bootstrap files: `13`
- Ambiguous files: `0`
- Potential secrets after the scoped false-positive exemption: `0`
- Largest included new file: `derived/pilot/pdf_ocr/2025/C023.readable.pdf` (`60083587` bytes)
- New files over 50 MB: `1`
- New files over 100 MB: `0`
- Required path-list SHA-256: `7be0654d31caa13af46c6cefcca79428ab639cd5df7ddacc552c1325643a33e7`
- Expected path-list SHA-256: `d6604af2a10accfca5376275d4f76e164f99d76bf104bb4dd3eec0039265a2c0`

## Secret audit

- Candidate: `derived/pilot/papers/CUMCM-2025-B-B060/paper.md`
- Scanner category: `AWS_ACCESS_KEY`
- Exact scoped token SHA-256: `C0633ABA5C4D2C4B3F9BCAF2E0EE8B58EBE8ECE83DF84D0F47E646CD8D91FD2C`
- Classification: `FALSE_POSITIVE`
- Context: OCR artifact; no credential context or associated secret/session indicator
- Unresolved secret-like matches after exemption: `0`

## Scope

The checkpoint includes the current governance lineage, including formal
artifact outputs, catalog evidence, reports, tools, logs, and the G11
post-repair rereview source-image packet. Runtime temporary directories,
staging/backup directories, bootstrap bundles, and unrelated CI automation are
excluded.

## Local handoff contract

- Commit message: `checkpoint: G11 repair complete, human rereview ready`
- Force push: `0`
- Hard reset: `0`
- Clean: `0`
- Rebase: `0`
- Local push script: `tools/100_git_checkpoint_g11_rereview_ready_local_push.ps1`
- Local push script executed by Codex: `0`
- Final commit SHA: `PENDING_USER_LOCAL_RUN`
- Push status: `PENDING_USER_LOCAL_RUN`
- Remote branch SHA: `PENDING_USER_LOCAL_RUN`
- Local/remote SHA match: `PENDING_USER_LOCAL_RUN`
- Post-commit worktree: `PENDING_USER_LOCAL_RUN`
- Original branch HEAD unchanged: `PENDING_USER_LOCAL_RUN`
- G11 status: `PARTIAL`
- Post-repair human rereview decisions: `11 PENDING`
- G12: `NOT RUN`

## Local push script hash-gate patch

The local script now derives its initial staged gate from the exact normalized
path-set difference:

`EXPECTED_CHECKPOINT_PATH_SET - REQUIRED_UNSTAGED_PATH_SET`

All path comparisons use trimmed `/`-normalized repo-relative paths in an
ordinal, case-sensitive `HashSet`. Duplicate paths are rejected for the
expected manifest, required-unstaged manifest, and current staged set.

Serialized path-list SHA-256 values remain diagnostic only; differences caused
by encoding, line endings, or serialization cannot block an otherwise equal
ordinal path set. Final staged validation uses the same exact path-set gate.

Required/expected manifest SHA checks are also diagnostic-only. The authoritative
semantic gates now verify that required paths are inside the expected set, do not
overlap the initial staged set, the initial staged set is inside the expected
set, and the initial-plus-required union exactly equals the expected set. The
count identity `16001 + 3060 = 19061` is retained as an auxiliary check.

The patch was statically parsed by Windows PowerShell 5.1 with `PARSE_PASS`.
The local push script was not executed by Codex; Git metadata and ACL mutation
counts remain `0`.

## UTF-8 interrupted-staging resume patch

The local script now explicitly configures UTF-8 console encoding, reads both
path manifests with `-Encoding UTF8`, and uses `core.quotepath=false` for Git
path reads. It derives the baseline staged set from `EXPECTED_SET -
ORIGINAL_REQUIRED_SET`, accepts already staged required paths, and stages only
the remaining required set after per-path existence checks. The interrupted
staging accounting and final exact path-set gates remain authoritative; the
manifest SHA checks remain diagnostic-only.

The current read-only audit identified the UTF-8 manifest entry at line `1`:
`2025年数学建模国赛真题+优秀论文/2025年数学建模国赛真题！/abc.zip`, and the
corresponding file exists. The current index remains at the original 16001
staged paths, so the observed mode is `FRESH`; the implementation also supports
`PARTIAL_STAGING` when a prior run leaves required paths staged.

## Access-denied diagnostic patch

The runner now records the active operation and exact Unicode repo-relative
path, captures Git exit code/stdout/stderr, and reports a classified failure
without replacing it with a generic `Access is denied`. Before staging it runs
a disposable `.git` filesystem write probe, checks for `index.lock`, validates
each remaining path exists, and performs a read-only .NET file-open probe.

Required-path staging uses `GIT_LITERAL_PATHSPECS=1`, one exact path per `git
add`, periodic progress output, and restoration of the prior environment value.
On any staging failure the runner re-reads the current staged set and reports
resume accounting; it never resets or unstages existing paths.

## Native Git invoke/output discipline patch

The exact staging path is `Invoke-GitChecked` -> `Invoke-GitCaptured` -> direct
PowerShell native invocation (`@(& git @Arguments 2>&1)`) followed immediately
by `$LASTEXITCODE`. It does not use `Start-Process`, a custom process API, or
temporary stdout/stderr redirection files. `GIT_LITERAL_PATHSPECS=1` remains
scoped around the required-path `git add -- <single-path>` calls.

The previously unbounded failure path was the combination of the full staged
path-list stdout retained by `Get-StagedPaths` and the failure reporter's
unbounded `-join ' | '` formatting in `Get-CheckpointFailureBlocker` and
`Fail-Checkpoint`. The runner now stores bounded Git diagnostics and emits at
most `4000` characters per failure-detail field, with
`FAILED_GIT_DETAIL_TRUNCATED=1` when truncation occurs. Failure context still
contains only the single current operation path; it never receives an expected,
staged, remaining, or all-changed path set. Collection mutation return values
are explicitly suppressed so path-set helpers cannot leak into the success
pipeline.

Windows PowerShell 5.1 and PowerShell 7 parse checks passed. The local push
runner was not executed by Codex and no Git write was performed.
