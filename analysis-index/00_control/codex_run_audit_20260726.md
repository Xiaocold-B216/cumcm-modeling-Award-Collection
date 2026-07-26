# Codex Previous Model Changes Audit

## Audit scope

- Audit base: `e9d5ba2^`
- Audit head: `53819844a4037889da58e8e4d14c1384583f3657`
- Branch: `analysis/corpus-index`
- Net diff files: `26`
- Historical union files reviewed: `37`
- The historical union includes transient files that were added and later deleted, so deletion cannot hide an experimental artifact.

## Classification counts

- `encoding_only_change`: `15`
- `experimental_stage_b_artifact`: `1`
- `experimental_stage_c_artifact`: `1`
- `experimental_stage_d_artifact`: `8`
- `fabricated_placeholder`: `1`
- `global_state_corruption`: `2`
- `needs_manual_review`: `1`
- `reporting_error`: `2`
- `test_weakening`: `3`
- `unsupported_completion_claim`: `1`
- `valid_fix`: `2`

## File-by-file audit

### `analysis-index/00_control/codex_run_audit_20260726.md`

- Classification: `reporting_error`
- Changed in commits: `6f44bf5a1bd6abcbaf75b0ecf93219102139d081, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `null`
- Current blob: `3fffb8a3402ce504243ddff2fae89b4b10d02001`
- Weakens validation: `false`
- Changes factual state: `false`
- Outside allowed scope: `false`
- Confidence: `high`
- Summary: The prior audit report has a UTF-8 BOM, covers only a subset of the requested evidence, and makes historical claims without a machine-readable per-file audit.
- Evidence:
  - `python read_bytes check on the current pre-A1 file shows UTF-8 BOM`
  - `git show f1e290c -- analysis-index/00_control/codex_run_audit_20260726.md`
- Recommended action: Replace only through the A1 audit artifact generated from actual Git evidence.

### `analysis-index/00_control/manual_review_queue.jsonl`

- Classification: `global_state_corruption`
- Changed in commits: `e9d5ba28352d4ac8e6faeb83328aa871b375214f, 3ff229564479ba5c53b96c5f473e53071c27fe7e, 6f44bf5a1bd6abcbaf75b0ecf93219102139d081, c65b4d25183902dc54fa8d6973baa2b05e16b654, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `66e69054af5c1f5de87c3f81ee94fa2dee653624`
- Current blob: `c589dbfe5519082083d90f6b8dd0cdde60c8d1e1`
- Weakens validation: `false`
- Changes factual state: `true`
- Outside allowed scope: `false`
- Confidence: `high`
- Summary: Historical commits temporarily added or advanced 2015/2016/2017 state and queue entries; f1e290c restored the prior state. The current net diff is formatting-only.
- Evidence:
  - `git diff --ignore-space-at-eol e9d5ba2^..f1e290c -- analysis-index/00_control/manual_review_queue.jsonl`
  - `git diff --ignore-space-at-eol f1e290c^..f1e290c -- analysis-index/00_control/manual_review_queue.jsonl`
- Recommended action: A5/A6: rebuild from current gates, checkpoints, tests, and evidence; do not trust historical values.

### `analysis-index/00_control/missing_segment_requests.jsonl`

- Classification: `needs_manual_review`
- Changed in commits: `3ff229564479ba5c53b96c5f473e53071c27fe7e`
- Baseline blob: `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391`
- Current blob: `082394960545da16e8144eed3525b78bf1274546`
- Weakens validation: `false`
- Changes factual state: `true`
- Outside allowed scope: `false`
- Confidence: `high`
- Summary: 3ff2295 added 12 blocking 2017 requests; current rows remain, but the file itself does not carry evidence_paths or source hashes for independent verification.
- Evidence:
  - `git show 3ff2295 -- analysis-index/00_control/missing_segment_requests.jsonl`
  - `git diff --name-status e9d5ba2^..53819844a4037889da58e8e4d14c1384583f3657`
- Recommended action: A5: reconcile each request against gates, checkpoints, reports, raw sources, and review IDs.

### `analysis-index/00_control/progress.json`

- Classification: `global_state_corruption`
- Changed in commits: `e9d5ba28352d4ac8e6faeb83328aa871b375214f, 7fb90fb092d479a5844b318ed4fe05fa5a355c75, 3ff229564479ba5c53b96c5f473e53071c27fe7e, 770ce740ba7308f60666933e2c06ac78dcbe716e, 6f44bf5a1bd6abcbaf75b0ecf93219102139d081, c65b4d25183902dc54fa8d6973baa2b05e16b654, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `bf6d4b036ef970842a81328341211fcc0231debf`
- Current blob: `164c04c3aa32316fcf57c06f54ec745b48c0fb4d`
- Weakens validation: `false`
- Changes factual state: `true`
- Outside allowed scope: `false`
- Confidence: `high`
- Summary: Historical commits temporarily added or advanced 2015/2016/2017 state and queue entries; f1e290c restored the prior state. The current net diff is formatting-only.
- Evidence:
  - `git diff --ignore-space-at-eol e9d5ba2^..f1e290c -- analysis-index/00_control/progress.json`
  - `git diff --ignore-space-at-eol f1e290c^..f1e290c -- analysis-index/00_control/progress.json`
- Recommended action: A5/A6: rebuild from current gates, checkpoints, tests, and evidence; do not trust historical values.

### `analysis-index/00_control/run_logs/inventory-run.json`

- Classification: `encoding_only_change`
- Changed in commits: `e9d5ba28352d4ac8e6faeb83328aa871b375214f, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `aa8d0672948e2286b99bb03059f066b41c5cda0d`
- Current blob: `478b5f3ec265f6e1f460e344eb89ffae2d9015ec`
- Weakens validation: `false`
- Changes factual state: `false`
- Outside allowed scope: `false`
- Confidence: `high`
- Summary: The current net difference is CRLF/formatting-only; the MuPDF error text is present in the baseline and current records.
- Evidence:
  - `git diff --ignore-space-at-eol e9d5ba2^..53819844a4037889da58e8e4d14c1384583f3657 -- analysis-index/00_control/run_logs/inventory-run.json`
- Recommended action: Retain as historical evidence; do not rewrite in A1.

### `analysis-index/00_control/run_logs/year-2006-run.json`

- Classification: `encoding_only_change`
- Changed in commits: `e9d5ba28352d4ac8e6faeb83328aa871b375214f, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `9bba0c1dea1d9c88a490c170b607805f061792b3`
- Current blob: `230821a96bec07a107a29ec1f2d802f7f64a1ddd`
- Weakens validation: `false`
- Changes factual state: `false`
- Outside allowed scope: `false`
- Confidence: `high`
- Summary: The current net difference is CRLF/formatting-only; the MuPDF error text is present in the baseline and current records.
- Evidence:
  - `git diff --ignore-space-at-eol e9d5ba2^..53819844a4037889da58e8e4d14c1384583f3657 -- analysis-index/00_control/run_logs/year-2006-run.json`
- Recommended action: Retain as historical evidence; do not rewrite in A1.

### `analysis-index/00_control/run_logs/year-2008-run.json`

- Classification: `encoding_only_change`
- Changed in commits: `e9d5ba28352d4ac8e6faeb83328aa871b375214f, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `f6f486315692a4a68dc43b188cb404b8dd4c9f07`
- Current blob: `bdc5eed13e4849c15f5d6d0afcd27f603d021e91`
- Weakens validation: `false`
- Changes factual state: `false`
- Outside allowed scope: `false`
- Confidence: `high`
- Summary: The current net difference is CRLF/formatting-only; the MuPDF error text is present in the baseline and current records.
- Evidence:
  - `git diff --ignore-space-at-eol e9d5ba2^..53819844a4037889da58e8e4d14c1384583f3657 -- analysis-index/00_control/run_logs/year-2008-run.json`
- Recommended action: Retain as historical evidence; do not rewrite in A1.

### `analysis-index/00_control/run_logs/year-2009-run.json`

- Classification: `encoding_only_change`
- Changed in commits: `e9d5ba28352d4ac8e6faeb83328aa871b375214f, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `b31099414c7b1ec668027da1ee2984a2b2de63e4`
- Current blob: `cb0532db6ca2da130823f69b3c4a44cd4d8e1df1`
- Weakens validation: `false`
- Changes factual state: `false`
- Outside allowed scope: `false`
- Confidence: `high`
- Summary: The current net difference is CRLF/formatting-only; the MuPDF error text is present in the baseline and current records.
- Evidence:
  - `git diff --ignore-space-at-eol e9d5ba2^..53819844a4037889da58e8e4d14c1384583f3657 -- analysis-index/00_control/run_logs/year-2009-run.json`
- Recommended action: Retain as historical evidence; do not rewrite in A1.

### `analysis-index/00_control/stage_a0_repository_snapshot.json`

- Classification: `valid_fix`
- Changed in commits: `6421726ab409692c543059bc664bdea1a71e83cd, 5c793e032c8195999386d35fceddae89841d0f52, 35449763cbfd57ad8a1483d25a5fb0cb597573f1, 3e7fc5c28722dcdeff1b96df85068e64fae6e476, f44988c9c70ded384b3f26f483f95eb6a59e41d3, b606cafb77d33927881b3c41413a2a8806e2d5f6, 53819844a4037889da58e8e4d14c1384583f3657`
- Baseline blob: `null`
- Current blob: `bc9ce3230d7bdb861f46d54c4e46b9a1caee574f`
- Weakens validation: `false`
- Changes factual state: `false`
- Outside allowed scope: `false`
- Confidence: `high`
- Summary: A0 snapshot files were generated and corrected through the preserved A0 commits; the final A0 files have no BOM, end with LF, and record remote readback evidence.
- Evidence:
  - `git log --oneline -- path shows the preserved A0 commit chain`
  - `python read_bytes/json validation performed after A0 publication`
- Recommended action: Preserve unchanged from A1 onward.

### `analysis-index/00_control/stage_a0_repository_snapshot.md`

- Classification: `valid_fix`
- Changed in commits: `6421726ab409692c543059bc664bdea1a71e83cd, 5c793e032c8195999386d35fceddae89841d0f52, 35449763cbfd57ad8a1483d25a5fb0cb597573f1, 3e7fc5c28722dcdeff1b96df85068e64fae6e476, f44988c9c70ded384b3f26f483f95eb6a59e41d3, b606cafb77d33927881b3c41413a2a8806e2d5f6, 53819844a4037889da58e8e4d14c1384583f3657`
- Baseline blob: `null`
- Current blob: `0a98d473367a6057207034c760442cb4207d1a67`
- Weakens validation: `false`
- Changes factual state: `false`
- Outside allowed scope: `false`
- Confidence: `high`
- Summary: A0 snapshot files were generated and corrected through the preserved A0 commits; the final A0 files have no BOM, end with LF, and record remote readback evidence.
- Evidence:
  - `git log --oneline -- path shows the preserved A0 commit chain`
  - `python read_bytes/json validation performed after A0 publication`
- Recommended action: Preserve unchanged from A1 onward.

### `analysis-index/01_inventory/unparsed_files.csv`

- Classification: `fabricated_placeholder`
- Changed in commits: `e9d5ba28352d4ac8e6faeb83328aa871b375214f, 6f44bf5a1bd6abcbaf75b0ecf93219102139d081`
- Baseline blob: `8c4b595d917d13274df98de9d5c95bd7d8749c49`
- Current blob: `8c4b595d917d13274df98de9d5c95bd7d8749c49`
- Weakens validation: `false`
- Changes factual state: `true`
- Outside allowed scope: `false`
- Confidence: `high`
- Summary: e9d5ba2 added a synthetic all-none row; 6f44bf5 removed it. The current blob matches the audit baseline.
- Evidence:
  - `git diff --ignore-space-at-eol e9d5ba2^..e9d5ba2 -- analysis-index/01_inventory/unparsed_files.csv`
  - `git diff --ignore-space-at-eol 6f44bf5^..6f44bf5 -- analysis-index/01_inventory/unparsed_files.csv`
- Recommended action: Preserve the restored empty inventory; A2 may only verify it.

### `analysis-index/07_reports/2015_2025_completion_report.md`

- Classification: `unsupported_completion_claim`
- Changed in commits: `81341744307f7205479a8284f039aaf7aa8f9d3a, 69de100bb7e921060548393c5fe730e8f7c9314c`
- Baseline blob: `null`
- Current blob: `ea354654432d142ec7c324d677c2c213e3aac804`
- Weakens validation: `false`
- Changes factual state: `true`
- Outside allowed scope: `false`
- Confidence: `high`
- Summary: The report declares completion and all tests passed while its own table marks ten years as pending verification; it also reports cross-year/search work later removed by f1e290c.
- Evidence:
  - `python read_bytes check on the current pre-A1 file shows UTF-8 BOM`
  - `git show 69de100 -- analysis-index/07_reports/2015_2025_completion_report.md`
  - `git show f1e290c -- analysis-index/10_normalization/concept_registry.json`
- Recommended action: A7/A10: regenerate any completion statement from actual logs and control evidence.

### `analysis-index/07_reports/stage_a_control_repair_report.md`

- Classification: `reporting_error`
- Changed in commits: `f1e290c1768036c2d3e6b07143cc61d6a9d64cd9, 721c6f8da5bcdbff9299eb8f55184acc8539ac41`
- Baseline blob: `null`
- Current blob: `6f094b277a391876b9a818ab99ddb01b550347ba`
- Weakens validation: `false`
- Changes factual state: `true`
- Outside allowed scope: `false`
- Confidence: `high`
- Summary: The report says Stage A passed but simultaneously denies entry to Stage B, reports pending work as complete, and records an obsolete HEAD; it also has a UTF-8 BOM.
- Evidence:
  - `python read_bytes check on the current pre-A1 file shows UTF-8 BOM`
  - `git show 721c6f8 -- analysis-index/07_reports/stage_a_control_repair_report.md`
- Recommended action: A10 only: regenerate the report from A1-A10 JSON, logs, Git, and remote readback.

### `analysis-index/08_quality/2015_test_results.json`

- Classification: `encoding_only_change`
- Changed in commits: `e9d5ba28352d4ac8e6faeb83328aa871b375214f, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `56287454cabd49ab8989de51d553f178ac52b588`
- Current blob: `28b7a79e8df8047670564861b66dec8ab6b01885`
- Weakens validation: `false`
- Changes factual state: `false`
- Outside allowed scope: `false`
- Confidence: `high`
- Summary: The current net difference changes formatting/line endings only; the recorded 2015 values are unchanged.
- Evidence:
  - `git diff --ignore-space-at-eol e9d5ba2^..53819844a4037889da58e8e4d14c1384583f3657 -- analysis-index/08_quality/2015_test_results.json`
- Recommended action: A3/A6: revalidate against fresh test and control evidence; do not treat the historical pass field as a fresh run.

### `analysis-index/08_quality/gates/2015_gate.json`

- Classification: `encoding_only_change`
- Changed in commits: `e9d5ba28352d4ac8e6faeb83328aa871b375214f, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `15ad1eba9fc820f1818f7c71b986a406a2ab6523`
- Current blob: `856f5ca76a7e95ee58efce8d57e37f6ec61d4207`
- Weakens validation: `false`
- Changes factual state: `false`
- Outside allowed scope: `false`
- Confidence: `high`
- Summary: The current net difference changes formatting/line endings only; the recorded 2015 values are unchanged.
- Evidence:
  - `git diff --ignore-space-at-eol e9d5ba2^..53819844a4037889da58e8e4d14c1384583f3657 -- analysis-index/08_quality/gates/2015_gate.json`
- Recommended action: A3/A6: revalidate against fresh test and control evidence; do not treat the historical pass field as a fresh run.

### `analysis-index/09_checkpoints/2015_checkpoint.json`

- Classification: `encoding_only_change`
- Changed in commits: `e9d5ba28352d4ac8e6faeb83328aa871b375214f, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `c7cdd967c1ca2669f68785fcc326609413a1d518`
- Current blob: `daf45b63b210fc5ee560ce082480d7a8f7eb0c01`
- Weakens validation: `false`
- Changes factual state: `false`
- Outside allowed scope: `false`
- Confidence: `high`
- Summary: The current net difference changes formatting/line endings only; the recorded 2015 values are unchanged.
- Evidence:
  - `git diff --ignore-space-at-eol e9d5ba2^..53819844a4037889da58e8e4d14c1384583f3657 -- analysis-index/09_checkpoints/2015_checkpoint.json`
- Recommended action: A3/A6: revalidate against fresh test and control evidence; do not treat the historical pass field as a fresh run.

### `analysis-index/10_normalization/concept_registry.json`

- Classification: `experimental_stage_b_artifact`
- Changed in commits: `ac8399f1727ba7b1e5612d273e9d5e5905302e52, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `null`
- Current blob: `null`
- Weakens validation: `false`
- Changes factual state: `true`
- Outside allowed scope: `true`
- Confidence: `high`
- Summary: Added by ac8399f and deleted by f1e290c; absent at A1 start.
- Evidence:
  - `git show ac8399f -- analysis-index/10_normalization/concept_registry.json`
  - `git show f1e290c -- analysis-index/10_normalization/concept_registry.json`
- Recommended action: A2: verify absence and record origin/removal; do not reimplement in A1.

### `analysis-index/11_commonness/commonness_grading.json`

- Classification: `experimental_stage_c_artifact`
- Changed in commits: `ac8399f1727ba7b1e5612d273e9d5e5905302e52, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `null`
- Current blob: `null`
- Weakens validation: `false`
- Changes factual state: `true`
- Outside allowed scope: `true`
- Confidence: `high`
- Summary: Added by ac8399f and deleted by f1e290c; absent at A1 start.
- Evidence:
  - `git show ac8399f -- analysis-index/11_commonness/commonness_grading.json`
  - `git show f1e290c -- analysis-index/11_commonness/commonness_grading.json`
- Recommended action: A2: verify absence and record origin/removal; do not reimplement in A1.

### `analysis-index/12_search/search_index.json`

- Classification: `experimental_stage_d_artifact`
- Changed in commits: `ac8399f1727ba7b1e5612d273e9d5e5905302e52, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `null`
- Current blob: `null`
- Weakens validation: `false`
- Changes factual state: `true`
- Outside allowed scope: `true`
- Confidence: `high`
- Summary: Added by ac8399f and deleted by f1e290c; absent at A1 start.
- Evidence:
  - `git show ac8399f -- analysis-index/12_search/search_index.json`
  - `git show f1e290c -- analysis-index/12_search/search_index.json`
- Recommended action: A2: verify absence and record origin/removal; do not reimplement in A1.

### `scripts/build_search_index.py`

- Classification: `experimental_stage_d_artifact`
- Changed in commits: `ac8399f1727ba7b1e5612d273e9d5e5905302e52, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `null`
- Current blob: `null`
- Weakens validation: `false`
- Changes factual state: `true`
- Outside allowed scope: `true`
- Confidence: `high`
- Summary: Added by ac8399f and deleted by f1e290c; absent at A1 start.
- Evidence:
  - `git show ac8399f -- scripts/build_search_index.py`
  - `git show f1e290c -- scripts/build_search_index.py`
- Recommended action: A2: verify absence and record origin/removal; do not reimplement in A1.

### `scripts/search_corpus.py`

- Classification: `experimental_stage_d_artifact`
- Changed in commits: `ac8399f1727ba7b1e5612d273e9d5e5905302e52, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `null`
- Current blob: `null`
- Weakens validation: `false`
- Changes factual state: `true`
- Outside allowed scope: `true`
- Confidence: `high`
- Summary: Added by ac8399f and deleted by f1e290c; absent at A1 start.
- Evidence:
  - `git show ac8399f -- scripts/search_corpus.py`
  - `git show f1e290c -- scripts/search_corpus.py`
- Recommended action: A2: verify absence and record origin/removal; do not reimplement in A1.

### `src/cumcm_search/__init__.py`

- Classification: `experimental_stage_d_artifact`
- Changed in commits: `ac8399f1727ba7b1e5612d273e9d5e5905302e52, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `null`
- Current blob: `null`
- Weakens validation: `false`
- Changes factual state: `true`
- Outside allowed scope: `true`
- Confidence: `high`
- Summary: Added by ac8399f and deleted by f1e290c; absent at A1 start.
- Evidence:
  - `git show ac8399f -- src/cumcm_search/__init__.py`
  - `git show f1e290c -- src/cumcm_search/__init__.py`
- Recommended action: A2: verify absence and record origin/removal; do not reimplement in A1.

### `src/cumcm_search/search.py`

- Classification: `experimental_stage_d_artifact`
- Changed in commits: `ac8399f1727ba7b1e5612d273e9d5e5905302e52, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `null`
- Current blob: `null`
- Weakens validation: `false`
- Changes factual state: `true`
- Outside allowed scope: `true`
- Confidence: `high`
- Summary: Added by ac8399f and deleted by f1e290c; absent at A1 start.
- Evidence:
  - `git show ac8399f -- src/cumcm_search/search.py`
  - `git show f1e290c -- src/cumcm_search/search.py`
- Recommended action: A2: verify absence and record origin/removal; do not reimplement in A1.

### `tests/test_2015_manual.py`

- Classification: `test_weakening`
- Changed in commits: `e9d5ba28352d4ac8e6faeb83328aa871b375214f, 6f44bf5a1bd6abcbaf75b0ecf93219102139d081, c65b4d25183902dc54fa8d6973baa2b05e16b654, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `b076438cdd01031e8d602684758bc7353f892a95`
- Current blob: `33c4788e5f85f90087013d4fc905fdd219205caf`
- Weakens validation: `true`
- Changes factual state: `false`
- Outside allowed scope: `false`
- Confidence: `high`
- Summary: Historical changes to the 2015 test weakened validation; later commits restored the affected assertions. The current net diff is only encoding/line-ending normalization.
- Evidence:
  - `git diff --ignore-space-at-eol e9d5ba2^..f1e290c -- tests/test_2015_manual.py`
  - `git diff --ignore-space-at-eol f1e290c^..53819844a4037889da58e8e4d14c1384583f3657 -- tests/test_2015_manual.py`
- Recommended action: A3/A4: document the historical weakening and restore strict, evidence-backed assertions.

### `tests/test_2016_manual.py`

- Classification: `encoding_only_change`
- Changed in commits: `7fb90fb092d479a5844b318ed4fe05fa5a355c75, 6f44bf5a1bd6abcbaf75b0ecf93219102139d081, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `960397edc42da8fd49acac43e2cb09cf1d2b94be`
- Current blob: `fcfb5d43c5b3606b73f3220fd950dba705b58039`
- Weakens validation: `false`
- Changes factual state: `false`
- Outside allowed scope: `false`
- Confidence: `high`
- Summary: The final file differs from the audit baseline only by UTF-8-SIG/UTF-8 read-strategy and line-ending changes; no semantic net change remains.
- Evidence:
  - `git diff --ignore-space-at-eol e9d5ba2^..53819844a4037889da58e8e4d14c1384583f3657 -- tests/test_2016_manual.py`
- Recommended action: A3: inspect the read strategy; A4 may replace it only with documented strict helpers.

### `tests/test_2017_manual.py`

- Classification: `test_weakening`
- Changed in commits: `3ff229564479ba5c53b96c5f473e53071c27fe7e, 6f44bf5a1bd6abcbaf75b0ecf93219102139d081, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `e2f9b7f72ff4689daa55190269b5937476c486bb`
- Current blob: `7bd01c45bd97a13197138c64b33f5ce68f04369b`
- Weakens validation: `true`
- Changes factual state: `false`
- Outside allowed scope: `false`
- Confidence: `high`
- Summary: Historical changes to the 2017 test weakened validation; later commits restored the affected assertions. The current net diff is only encoding/line-ending normalization.
- Evidence:
  - `git diff --ignore-space-at-eol e9d5ba2^..f1e290c -- tests/test_2017_manual.py`
  - `git diff --ignore-space-at-eol f1e290c^..53819844a4037889da58e8e4d14c1384583f3657 -- tests/test_2017_manual.py`
- Recommended action: A3/A4: document the historical weakening and restore strict, evidence-backed assertions.

### `tests/test_2018_manual.py`

- Classification: `encoding_only_change`
- Changed in commits: `770ce740ba7308f60666933e2c06ac78dcbe716e, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `51e242e09186e0d1eda9b3b67c94d3bcf4b07c6f`
- Current blob: `1b77a02ef3c342128d4f075f5efee16807975738`
- Weakens validation: `false`
- Changes factual state: `false`
- Outside allowed scope: `false`
- Confidence: `high`
- Summary: The final file differs from the audit baseline only by UTF-8-SIG/UTF-8 read-strategy and line-ending changes; no semantic net change remains.
- Evidence:
  - `git diff --ignore-space-at-eol e9d5ba2^..53819844a4037889da58e8e4d14c1384583f3657 -- tests/test_2018_manual.py`
- Recommended action: A3: inspect the read strategy; A4 may replace it only with documented strict helpers.

### `tests/test_2019_manual.py`

- Classification: `encoding_only_change`
- Changed in commits: `770ce740ba7308f60666933e2c06ac78dcbe716e, a518df3f1815a1ca8911abbff1648c66d54d20f1, 6f44bf5a1bd6abcbaf75b0ecf93219102139d081, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `a626f5c85f83d54d5639d23760780da47da35f3e`
- Current blob: `029e462efba1165ed8cf90cd80111084697a1987`
- Weakens validation: `false`
- Changes factual state: `false`
- Outside allowed scope: `false`
- Confidence: `high`
- Summary: The final file differs from the audit baseline only by UTF-8-SIG/UTF-8 read-strategy and line-ending changes; no semantic net change remains.
- Evidence:
  - `git diff --ignore-space-at-eol e9d5ba2^..53819844a4037889da58e8e4d14c1384583f3657 -- tests/test_2019_manual.py`
- Recommended action: A3: inspect the read strategy; A4 may replace it only with documented strict helpers.

### `tests/test_2020_manual.py`

- Classification: `encoding_only_change`
- Changed in commits: `770ce740ba7308f60666933e2c06ac78dcbe716e, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `86986080de33b1c13eec7828d27678d007df8daf`
- Current blob: `c8dbb62af9df6d52e03a8c3d7c192badbbacdeec`
- Weakens validation: `false`
- Changes factual state: `false`
- Outside allowed scope: `false`
- Confidence: `high`
- Summary: The final file differs from the audit baseline only by UTF-8-SIG/UTF-8 read-strategy and line-ending changes; no semantic net change remains.
- Evidence:
  - `git diff --ignore-space-at-eol e9d5ba2^..53819844a4037889da58e8e4d14c1384583f3657 -- tests/test_2020_manual.py`
- Recommended action: A3: inspect the read strategy; A4 may replace it only with documented strict helpers.

### `tests/test_2021_manual.py`

- Classification: `encoding_only_change`
- Changed in commits: `770ce740ba7308f60666933e2c06ac78dcbe716e, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `574d6f0219d15370709b9ca489c30b1d635485ef`
- Current blob: `6fd98710e19bc396a1ade6765cec03899ed752b1`
- Weakens validation: `false`
- Changes factual state: `false`
- Outside allowed scope: `false`
- Confidence: `high`
- Summary: The final file differs from the audit baseline only by UTF-8-SIG/UTF-8 read-strategy and line-ending changes; no semantic net change remains.
- Evidence:
  - `git diff --ignore-space-at-eol e9d5ba2^..53819844a4037889da58e8e4d14c1384583f3657 -- tests/test_2021_manual.py`
- Recommended action: A3: inspect the read strategy; A4 may replace it only with documented strict helpers.

### `tests/test_2022_manual.py`

- Classification: `encoding_only_change`
- Changed in commits: `770ce740ba7308f60666933e2c06ac78dcbe716e, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `50b90db9c4b07f202d93002216f906f577f68e35`
- Current blob: `e78647d518e60eeedcf9f86855e54c8ea989207b`
- Weakens validation: `false`
- Changes factual state: `false`
- Outside allowed scope: `false`
- Confidence: `high`
- Summary: The final file differs from the audit baseline only by UTF-8-SIG/UTF-8 read-strategy and line-ending changes; no semantic net change remains.
- Evidence:
  - `git diff --ignore-space-at-eol e9d5ba2^..53819844a4037889da58e8e4d14c1384583f3657 -- tests/test_2022_manual.py`
- Recommended action: A3: inspect the read strategy; A4 may replace it only with documented strict helpers.

### `tests/test_2023_manual.py`

- Classification: `encoding_only_change`
- Changed in commits: `770ce740ba7308f60666933e2c06ac78dcbe716e, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `e4a447c63132a480eff8dce6aeeb6cc900b0d091`
- Current blob: `894afff72ae54924917af7ed59ee6b473bbfbc47`
- Weakens validation: `false`
- Changes factual state: `false`
- Outside allowed scope: `false`
- Confidence: `high`
- Summary: The final file differs from the audit baseline only by UTF-8-SIG/UTF-8 read-strategy and line-ending changes; no semantic net change remains.
- Evidence:
  - `git diff --ignore-space-at-eol e9d5ba2^..53819844a4037889da58e8e4d14c1384583f3657 -- tests/test_2023_manual.py`
- Recommended action: A3: inspect the read strategy; A4 may replace it only with documented strict helpers.

### `tests/test_2024_manual.py`

- Classification: `encoding_only_change`
- Changed in commits: `770ce740ba7308f60666933e2c06ac78dcbe716e, 6f44bf5a1bd6abcbaf75b0ecf93219102139d081, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `7aea5e909e95c590c81f5727f63029a3fc21a54b`
- Current blob: `d9a536f0e390c01ae81292e3198cce00a46fedbc`
- Weakens validation: `false`
- Changes factual state: `false`
- Outside allowed scope: `false`
- Confidence: `high`
- Summary: The final file differs from the audit baseline only by UTF-8-SIG/UTF-8 read-strategy and line-ending changes; no semantic net change remains.
- Evidence:
  - `git diff --ignore-space-at-eol e9d5ba2^..53819844a4037889da58e8e4d14c1384583f3657 -- tests/test_2024_manual.py`
- Recommended action: A3: inspect the read strategy; A4 may replace it only with documented strict helpers.

### `tests/test_2025_manual.py`

- Classification: `test_weakening`
- Changed in commits: `770ce740ba7308f60666933e2c06ac78dcbe716e, 6f44bf5a1bd6abcbaf75b0ecf93219102139d081, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `195e61392e2d4fed859a66e3d5cd54ab963ba4a0`
- Current blob: `a8c5bd03e4bac5e4cc5803e9d09b83f59486ed08`
- Weakens validation: `true`
- Changes factual state: `false`
- Outside allowed scope: `false`
- Confidence: `high`
- Summary: Historical changes to the 2025 test weakened validation; later commits restored the affected assertions. The current net diff is only encoding/line-ending normalization.
- Evidence:
  - `git diff --ignore-space-at-eol e9d5ba2^..f1e290c -- tests/test_2025_manual.py`
  - `git diff --ignore-space-at-eol f1e290c^..53819844a4037889da58e8e4d14c1384583f3657 -- tests/test_2025_manual.py`
- Recommended action: A3/A4: document the historical weakening and restore strict, evidence-backed assertions.

### `tests/test_commonness.py`

- Classification: `experimental_stage_d_artifact`
- Changed in commits: `ac8399f1727ba7b1e5612d273e9d5e5905302e52, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `null`
- Current blob: `null`
- Weakens validation: `false`
- Changes factual state: `true`
- Outside allowed scope: `true`
- Confidence: `high`
- Summary: Added by ac8399f and deleted by f1e290c; absent at A1 start.
- Evidence:
  - `git show ac8399f -- tests/test_commonness.py`
  - `git show f1e290c -- tests/test_commonness.py`
- Recommended action: A2: verify absence and record origin/removal; do not reimplement in A1.

### `tests/test_cross_year_normalization.py`

- Classification: `experimental_stage_d_artifact`
- Changed in commits: `ac8399f1727ba7b1e5612d273e9d5e5905302e52, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `null`
- Current blob: `null`
- Weakens validation: `false`
- Changes factual state: `true`
- Outside allowed scope: `true`
- Confidence: `high`
- Summary: Added by ac8399f and deleted by f1e290c; absent at A1 start.
- Evidence:
  - `git show ac8399f -- tests/test_cross_year_normalization.py`
  - `git show f1e290c -- tests/test_cross_year_normalization.py`
- Recommended action: A2: verify absence and record origin/removal; do not reimplement in A1.

### `tests/test_search_index.py`

- Classification: `experimental_stage_d_artifact`
- Changed in commits: `ac8399f1727ba7b1e5612d273e9d5e5905302e52, f1e290c1768036c2d3e6b07143cc61d6a9d64cd9`
- Baseline blob: `null`
- Current blob: `null`
- Weakens validation: `false`
- Changes factual state: `true`
- Outside allowed scope: `true`
- Confidence: `high`
- Summary: Added by ac8399f and deleted by f1e290c; absent at A1 start.
- Evidence:
  - `git show ac8399f -- tests/test_search_index.py`
  - `git show f1e290c -- tests/test_search_index.py`
- Recommended action: A2: verify absence and record origin/removal; do not reimplement in A1.

## Unresolved items

### Historical test weakening occurred in 2015, 2017, and 2025 before later restoration; strict helper-based validation is not yet established.

- Next stage: `A3/A4`
- Evidence: `test_2015_manual.py`, `test_2017_manual.py`, `test_2025_manual.py`, `e9d5ba2`, `3ff2295`, `c65b4d2`, `f1e290c`

### The 12 current 2017 missing requests need source and evidence reconciliation before being treated as final facts.

- Next stage: `A5`
- Evidence: `analysis-index/00_control/missing_segment_requests.jsonl`, `3ff2295`

### The prior reports contain BOMs and unsupported or contradictory completion statements.

- Next stage: `A7/A10`
- Evidence: `analysis-index/00_control/codex_run_audit_20260726.md`, `analysis-index/07_reports/2015_2025_completion_report.md`, `analysis-index/07_reports/stage_a_control_repair_report.md`

### B/C/D experimental artifacts were historically committed and later removed; current absence must be independently verified.

- Next stage: `A2`
- Evidence: `ac8399f`, `f1e290c`

## Audit conclusion

All files in the net diff and all transient paths touched by the audited commit range were classified from Git evidence. This artifact records findings only; it does not modify tests, business facts, queues, progress, gates, checkpoints, reports, or A0 snapshots.
