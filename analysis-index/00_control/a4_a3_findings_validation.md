# A4 A3 Findings Validation

## Evidence boundary

A3 was consumed as a read-only static audit. A4 did not repeat the AST audit and did not modify tests or business/control data. Each finding below has two independent checks. No finding had conflicting evidence requiring a third check; `requires_human_review` count is zero.

## A3 audit input

- Files reviewed: 11
- Test functions reviewed: 267
- Weakening-function records: 22
- Issue counts: `{"bom_handling": 69, "confuses_global_and_annual_queue": 9, "depends_on_total_queue_rows": 7, "narrows_scan_scope": 1, "only_checks_file_existence": 12, "page_upper_bound_checked": 22, "rejects_all_empty_csv": 2, "schema_or_current_fact_conflict": 13, "sheet_actual_upper_bound_checked": 2, "uses_hardcoded_quantities": 146}`

### A3-optional-source-2022: intentional_behavior

- Finding: Two optional raw-source checks use explicit pytest.skip when their environment variables are absent.
- Recheck 1: Source inspection: tests/test_2022_manual.py:357-363 and :385-391 contain explicit conditions and reasons.
- Recheck 2: Runtime: 2022 produced two SKIPPED records with the same explicit reasons and no hidden exception.
- Action: Retain as recorded conditional coverage; do not modify tests in A4.

### A3-optional-source-2024: confirmed_defect

- Finding: The optional raw-source hash check returns without a result when /mnt/data sources are absent.
- Recheck 1: Source inspection: tests/test_2024_manual.py:365-371 returns before the assertion when both optional inputs are absent.
- Recheck 2: Runtime: the 2024 annual run contains no skip record for this path, so the return is silent in normal output.
- Action: Record for a later approved repair; no A4 test modification.

### A3-errors-ignore: confirmed_defect

- Finding: Four annual tests use errors=ignore while scanning evidence text.
- Recheck 1: A3 source records identify 2017:209-213, 2018:139-147, 2019:167-175, and 2025:175-183.
- Recheck 2: Runtime independently exposed decode/JSON failures in multiple annual files while these broad scans remain tolerant.
- Action: Record the risk; do not replace the reader or weaken assertions in A4.

### A3-bom-policy: confirmed_defect

- Finding: 69 findings involve BOM handling: 36 BOM-tolerant reads and 33 no-BOM assertions without a uniform input/output distinction.
- Recheck 1: A3 checks count the two strategies across all 267 functions.
- Recheck 2: Runtime shows JSON/decode failures in annual runs, while no single uniform BOM evidence policy is enforced across files.
- Action: Keep input tolerance separate from output conformance; defer implementation to an explicitly permitted repair stage.

### A3-boundary-coverage: confirmed_defect

- Finding: Page and worksheet boundary validation is non-uniform: 22 page-boundary records, 10 page records without an upper-bound check, 2 worksheet records with actual bounds, and 5 without.
- Recheck 1: A3 function records identify the page/sheet coverage counts and locations.
- Recheck 2: Runtime confirms that boundary coverage is distributed across annual tests rather than enforced by one reusable contract; affected runs also contain independent failures.
- Action: Record the gap and defer test changes; no new boundary tests are added in A4.

### A3-queue-progress: confirmed_defect

- Finding: Nine functions confuse global and annual queues and seven depend on total queue rows; the unresolved A3 item names cross-year queue/progress mixing.
- Recheck 1: A3 checks and unresolved_items identify the queue/progress locations and counts.
- Recheck 2: Runtime failures occurred in annual queue/progress assertions in 2015, 2018, 2020, 2022, 2023, 2024, and 2025.
- Action: Defer reconciliation to A5/A6; A4 does not modify progress, gates, checkpoints, reports, or queues.

### A3-static-assertion-families: out_of_scope_for_A4

- Finding: A3 also records 12 existence-only functions, 146 hardcoded-quantity functions, 13 schema/current-fact conflicts, 2 empty-CSV rejection records, and 1 narrowed-scan record.
- Recheck 1: A3 issue_counts and function records provide the static counts.
- Recheck 2: A4 runtime results record failures but cannot safely redesign assertions without changing tests or business facts, which A4 forbids.
- Action: Preserve the findings as scoped follow-up evidence; no test or data edits in A4.

## Runtime evidence

- Collection: 267 nodes collected, exit 0.
- Annual runs: 11 attempts; 47 failed tests, 2 skips, 0 errors, and one 300-second timeout in 2017.
- The 2022 skips are explicit and reason-bearing.
- The 2017 timeout is recorded as a runtime failure; no node identity was inferred from partial output.

## A4 boundary

No test, business fact, progress, gate, checkpoint, report, queue, or source material was modified. Repair of confirmed defects is outside A4 and remains deferred.
