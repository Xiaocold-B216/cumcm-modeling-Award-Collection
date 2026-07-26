# 2015—2025 A1—A8执行计划

This human-readable plan is generated from `analysis-index/00_control/stage_plan_2015_2025.json` and the committed A4-A8 stage definition files.

## 1. 计划元信息

- **Repository:** Xiaocold-B216/cumcm-modeling-Award-Collection
- **Branch:** analysis/corpus-index
- **Definition base commit:** cae3bbe7006b3616bd94578518d20dee7f6e8d3b
- **Stages total:** 8
- **Completed stages:** A1, A2, A3
- **Formally defined future stages:** A4, A5, A6, A7, A8
- **Bootstrap state at generation:** blocked: missing_required_file; this file is the missing artifact being added; final status is determined only after commit and remote readback.

## 2. 全局执行规则

- Each run executes exactly one stage.
- Each stage is committed independently; its contract requires commit, push, and remote readback before the next stage.
- Remote readback is required at every stage boundary.
- There is no silent stage advance.
- Force push is forbidden.
- The worktree must be clean at a stage boundary.
- When blocked, perform only the minimum action needed to resolve the listed blocker; do not advance the stage.
- Original materials are read-only.
- Business facts remain read-only until an explicit repair stage.

Machine-readable policy values:
- `one_stage_per_run`: `true`
- `remote_readback_required`: `true`
- `no_silent_stage_advance`: `true`
- `no_force_push`: `true`
- `working_tree_must_be_clean_at_boundary`: `true`
- `original_materials_read_only`: `true`
- `business_facts_read_only_until_explicit_repair_stage`: `true`

## 3. 阶段总览

| Stage | Status | Purpose | Depends on | Main outputs | Stop rule |
|---|---|---|---|---|---|
| A1 | passed | Historical completed stage; preserve its verified commit and remote readback without re-execution. | none | verified A1 commit and remote readback | Do not re-run or rewrite A1 during later stages. |
| A2 | passed | Historical completed stage; preserve its verified commit and remote readback without re-execution. | A1 | verified A2 commit and remote readback | Do not re-run, amend, roll back, or rewrite A2 during later stages. |
| A3 | passed | Historical completed stage; preserve its verified audit outputs without re-execution. | A2 | analysis-index/00_control/test_integrity_audit_2015_2025.json<br>analysis-index/00_control/test_change_justification.md | Use A3 as a read-only input to A4; do not repeat its audit here. |
| A4 | defined_not_started | Run the 2015-2025 annual tests, establish an evidence-backed runtime baseline, and classify each A3 finding without broad repair. | A3 | analysis-index/00_control/a4_test_execution_summary.json<br>analysis-index/00_control/a4_test_failure_inventory.jsonl<br>analysis-index/00_control/a4_test_runtime_profile.json<br>analysis-index/00_control/a4_a3_findings_validation.md<br>analysis-index/00_control/a4_stage_report.md | After A4 remote readback, stop. Do not execute A5 or any later stage. |
| A5 | defined_not_started | Reconcile status claims against gates, checkpoints, reports, queues, missing requests, and A4 results; propose repairs without applying them. | A4 | analysis-index/00_control/a5_status_reconciliation_2015_2025.json<br>analysis-index/00_control/a5_status_reconciliation_2015_2025.md<br>analysis-index/00_control/a5_proposed_repairs.json<br>analysis-index/00_control/a5_human_review_queue.jsonl<br>analysis-index/00_control/a5_stage_report.md | After A5 remote readback, stop. Do not execute A6. |
| A6 | defined_not_started | Apply only A5-approved, evidence-bound minimal repairs and run affected-scope regression. | A5 | analysis-index/00_control/a6_repair_manifest.json<br>analysis-index/00_control/a6_regression_results.json<br>analysis-index/00_control/a6_stage_report.md | After A6 remote readback, stop. Do not execute A7. |
| A7 | defined_not_started | Run full regression and cross-file consistency checks after A6 repairs, without introducing new repairs. | A6 | analysis-index/00_control/a7_full_regression_summary.json<br>analysis-index/00_control/a7_cross_file_consistency.json<br>analysis-index/00_control/a7_runtime_benchmark.json<br>analysis-index/00_control/a7_stage_report.md | After A7 remote readback, stop. Do not execute A8. |
| A8 | defined_not_started | Summarize A1-A7, create the final recovery and verification package, and deliver it with remote readback; do not add business repairs. | A7 | analysis-index/00_control/a1_a8_final_summary.json<br>analysis-index/00_control/a1_a8_final_summary.md<br>analysis-index/00_control/final_remote_readback.json<br>analysis-index/09_checkpoints/a8_final_checkpoint.json | A8 is the terminal stage. Do not start another stage automatically. |

A4-A8 are formally defined but have not been executed. No future stage is represented as passed or ready before its own execution and remote readback.

## 4. A4—A8 详细摘要

### A4: Annual test baseline execution and A3 finding validation

- **purpose:** Run the 2015-2025 annual tests, establish an evidence-backed runtime baseline, and classify each A3 finding without broad repair.
- **depends_on:** A3
- **authoritative_inputs:** analysis-index/00_control/test_integrity_audit_2015_2025.json; analysis-index/00_control/test_change_justification.md; tests/test_2015_manual.py through tests/test_2025_manual.py
- **read_only_inputs:** current gates; current checkpoints; annual reports; queues; progress.json; schema; business and source materials
- **allowed_writes:** analysis-index/00_control/a4_test_execution_summary.json; analysis-index/00_control/a4_test_failure_inventory.jsonl; analysis-index/00_control/a4_test_runtime_profile.json; analysis-index/00_control/a4_a3_findings_validation.md; analysis-index/00_control/a4_stage_report.md
- **forbidden_writes:** tests/; analysis-index/01_inventory/ through analysis-index/09_checkpoints/; analysis-index/00_control/progress.json; analysis-index/00_control/manual_review_queue.jsonl; analysis-index/00_control/missing_segment_requests.jsonl; original papers, archives, images, data, or trusted baseline
- **required_outputs:** analysis-index/00_control/a4_test_execution_summary.json; analysis-index/00_control/a4_test_failure_inventory.jsonl; analysis-index/00_control/a4_test_runtime_profile.json; analysis-index/00_control/a4_a3_findings_validation.md; analysis-index/00_control/a4_stage_report.md
- **acceptance_criteria:** all 11 annual test files collect successfully or have an explicit collection blocker; every annual test is run independently with an exit code; results are structured with passed, failed, skipped, error, duration, and failure IDs; every A3 finding has an allowed classification; BOM acceptance is separated from no-BOM output policy; tests and business facts are unchanged; commit, push, and remote readback pass
- **blocked_reasons:** missing_dependency, pytest_collection_failure, environment_failure, missing_test_file, unreadable_input, network, authentication, permission, remote_divergence, human_review_required
- **human_review_triggers:** two independent checks conflict on a finding; a source, queue, boundary, skip, or encoding conclusion lacks evidence
- **time_controls:** {"annual_runs_are_independent": true, "collect_before_annual": true, "logs_outside_repository": true, "no_implicit_full_suite_repeat": true}
- **stop_rule:** After A4 remote readback, stop. Do not execute A5 or any later stage.
- **Definition file:** `analysis-index/00_control/stage_definitions/A4.md`

### A5: 2015-2025 status reconciliation and evidence-first repair plan

- **purpose:** Reconcile status claims against gates, checkpoints, reports, queues, missing requests, and A4 results; propose repairs without applying them.
- **depends_on:** A4
- **authoritative_inputs:** A4 outputs; remote-read gates; checkpoints; annual reports; source and page evidence
- **read_only_inputs:** progress.json; manual_review_queue.jsonl; missing_segment_requests.jsonl; business and source materials
- **allowed_writes:** analysis-index/00_control/a5_status_reconciliation_2015_2025.json; analysis-index/00_control/a5_status_reconciliation_2015_2025.md; analysis-index/00_control/a5_proposed_repairs.json; analysis-index/00_control/a5_human_review_queue.jsonl; analysis-index/00_control/a5_stage_report.md
- **forbidden_writes:** progress.json; queue deletion; gate or checkpoint rewrite; tests/; original materials
- **required_outputs:** analysis-index/00_control/a5_status_reconciliation_2015_2025.json; analysis-index/00_control/a5_status_reconciliation_2015_2025.md; analysis-index/00_control/a5_proposed_repairs.json; analysis-index/00_control/a5_human_review_queue.jsonl; analysis-index/00_control/a5_stage_report.md
- **acceptance_criteria:** each year has a status; each conflict has both evidence paths; unknown is not converted to absent; the A6 minimal repair list is machine-readable; remote readback passes
- **blocked_reasons:** missing_dependency, unreadable_input, permission, network, remote_divergence, human_review_required
- **human_review_triggers:** unresolved evidence conflict; request lacks source path or hash
- **time_controls:** {"one_stage_per_run": true, "repair_application_forbidden": true}
- **stop_rule:** After A5 remote readback, stop. Do not execute A6.
- **Definition file:** `analysis-index/00_control/stage_definitions/A5.md`

### A6: Confirmed minimal repair and local regression

- **purpose:** Apply only A5-approved, evidence-bound minimal repairs and run affected-scope regression.
- **depends_on:** A5
- **authoritative_inputs:** A5 proposed repair manifest; human confirmations; A4 test baseline
- **read_only_inputs:** unaffected years; original materials; trusted baseline
- **allowed_writes:** only files explicitly named by the A5 repair manifest
- **forbidden_writes:** unapproved files; bulk reconstruction; original materials; unapproved queue or status changes; test weakening
- **required_outputs:** analysis-index/00_control/a6_repair_manifest.json; analysis-index/00_control/a6_regression_results.json; analysis-index/00_control/a6_stage_report.md
- **acceptance_criteria:** every repair has evidence and before/after state; targeted regression passes; affected-year regression completes; unaffected years are not changed; remote readback passes
- **blocked_reasons:** missing_dependency, pytest_collection_failure, permission, network, remote_divergence, human_review_required
- **human_review_triggers:** repair scope expands beyond A5 manifest; before/after evidence conflicts
- **time_controls:** {"minimal_repairs_only": true, "targeted_regression_before_broad_regression": true}
- **stop_rule:** After A6 remote readback, stop. Do not execute A7.
- **Definition file:** `analysis-index/00_control/stage_definitions/A6.md`

### A7: Full regression, quality gates, and cross-file consistency

- **purpose:** Run full regression and cross-file consistency checks after A6 repairs, without introducing new repairs.
- **depends_on:** A6
- **authoritative_inputs:** A6 repair and regression outputs; all current control and derived outputs
- **read_only_inputs:** original materials; trusted baseline
- **allowed_writes:** analysis-index/00_control/a7_full_regression_summary.json; analysis-index/00_control/a7_cross_file_consistency.json; analysis-index/00_control/a7_runtime_benchmark.json; analysis-index/00_control/a7_stage_report.md
- **forbidden_writes:** new repairs; original materials; unrecorded test skips; placeholder completion claims
- **required_outputs:** analysis-index/00_control/a7_full_regression_summary.json; analysis-index/00_control/a7_cross_file_consistency.json; analysis-index/00_control/a7_runtime_benchmark.json; analysis-index/00_control/a7_stage_report.md
- **acceptance_criteria:** hard errors are zero; all retained failures are explicitly recorded; no unrecorded skips or unsupported completion claims; cross-file consistency passes; remote readback passes
- **blocked_reasons:** missing_dependency, pytest_collection_failure, environment_failure, permission, network, remote_divergence, human_review_required
- **human_review_triggers:** new contradiction after A6; quality gate cannot distinguish incomplete from passed
- **time_controls:** {"full_regression_required": true, "runtime_benchmark_required": true}
- **stop_rule:** After A7 remote readback, stop. Do not execute A8.
- **Definition file:** `analysis-index/00_control/stage_definitions/A7.md`

### A8: Final summary, release checkpoint, and remote delivery

- **purpose:** Summarize A1-A7, create the final recovery and verification package, and deliver it with remote readback; do not add business repairs.
- **depends_on:** A7
- **authoritative_inputs:** A1-A7 verified commits and outputs
- **read_only_inputs:** all business and source materials; trusted baseline
- **allowed_writes:** analysis-index/00_control/a1_a8_final_summary.json; analysis-index/00_control/a1_a8_final_summary.md; analysis-index/00_control/final_remote_readback.json; analysis-index/09_checkpoints/a8_final_checkpoint.json
- **forbidden_writes:** business repairs; historical commits; automatic branch merge; force push; absolute paths, secrets, cache, or temporary files
- **required_outputs:** analysis-index/00_control/a1_a8_final_summary.json; analysis-index/00_control/a1_a8_final_summary.md; analysis-index/00_control/final_remote_readback.json; analysis-index/09_checkpoints/a8_final_checkpoint.json
- **acceptance_criteria:** final files parse strictly; local and remote content match; working tree is clean; recovery instructions are complete; no incomplete year is represented as complete
- **blocked_reasons:** missing_dependency, permission, network, authentication, remote_divergence, human_review_required
- **human_review_triggers:** final status cannot be supported by A1-A7 evidence; remote readback differs from local bytes
- **time_controls:** {"final_delivery_only": true, "no_new_business_work": true}
- **stop_rule:** A8 is the terminal stage. Do not start another stage automatically.
- **Definition file:** `analysis-index/00_control/stage_definitions/A8.md`

## 5. 依赖链

A1 → A2 → A3 → A4 → A5 → A6 → A7 → A8

- A4 depends on A3.
- A5 depends on A4.
- A6 depends on A5.
- A7 depends on A6.
- A8 depends on A7.

## 6. 阶段职责边界

- A4 only runs, measures, validates, and classifies; it does not perform broad repair.
- A5 only reconciles evidence and proposes repairs; it does not apply repairs.
- A6 applies only approved minimal repairs and runs affected-scope regression.
- A7 runs full regression and cross-file consistency validation without introducing new repairs.
- A8 only performs final summary, checkpoint, and remote delivery; it introduces no business repair.

## 7. 权威性说明

- `analysis-index/00_control/stage_plan_2015_2025.json` is the machine-readable authoritative plan.
- This Markdown file is the human-readable mirror.
- If JSON and Markdown conflict, JSON is authoritative and execution is blocked until the conflict is resolved.
- External chat instructions cannot override committed repository stage definitions.

## Bootstrap boundary

This document only completes the missing human-readable stage plan. It does not execute A4, run annual pytest, modify tests, or change business/control data. After its independent commit is pushed and remotely read back, the bootstrap may be marked `passed`; A4 may then be marked `ready_to_start`, but remains unexecuted.
