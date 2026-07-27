# A5：2015—2025 状态对账与证据优先修复计划

## 1. 阶段结论

- 阶段：A5
- 仓库：`Xiaocold-B216/cumcm-modeling-Award-Collection`
- 分支：`analysis/corpus-index`
- 输入提交：`92d4889122d4bdb818c1fd896d410cce971901e9`
- 正式契约：`analysis-index/00_control/stage_definitions/A5.md`
- 本阶段只对账、分类和提出修复建议；没有实施修复，没有运行测试，没有修改权威输入。
- A5 的最终 `passed` 以五个输出完成独立提交、普通推送和远端原始字节回读为前提。
- A6 尚未启动。本文件和 JSON 中的修复项均为建议，不代表已实施。

## 2. 证据优先级与边界

本次对账采用以下优先级：

1. A4 输出用于当前测试运行事实，特别是 2017 的超时核算。
2. 年度 gate 和 checkpoint 用于年度范围、来源完整性、人工复核和远端状态。
3. 年度报告和状态对账报告用于解释已知问题和声明范围。
4. 年度队列与全局队列分别统计；全局队列不会被复制为每个年度的队列。
5. `progress.json` 是存在但不完整的历史进度输入。它没有 2015—2024 年条目，不能被解释为这些年度不存在。

本阶段没有修改 `progress.json`、gate、checkpoint、年度报告、测试、业务数据、原始资料或队列。

## 3. A4 测试事实保留

总量闭合为：

`267 collected = 194 passed + 47 failed + 2 skipped + 0 errors + 24 unresolved_due_to_2017_timeout`

2017 的事实是：收集 24 个节点，终态 0 个，passed/failed/skipped/errors 均为 0，exit code 为 124，超时阈值为 300 秒，未决超时节点为 24。A5 不推断任何具体 2017 节点通过或失败。

| 年度 | A4 collected | passed | failed | skipped | errors | unresolved timeout | exit |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2015 | 36 | 26 | 10 | 0 | 0 | 0 | 1 |
| 2016 | 28 | 26 | 2 | 0 | 0 | 0 | 1 |
| 2017 | 24 | 0 | 0 | 0 | 0 | 24 | 124 |
| 2018 | 16 | 12 | 4 | 0 | 0 | 0 | 1 |
| 2019 | 11 | 10 | 1 | 0 | 0 | 0 | 1 |
| 2020 | 32 | 21 | 11 | 0 | 0 | 0 | 1 |
| 2021 | 20 | 18 | 2 | 0 | 0 | 0 | 1 |
| 2022 | 24 | 18 | 4 | 2 | 0 | 0 | 1 |
| 2023 | 28 | 24 | 4 | 0 | 0 | 0 | 1 |
| 2024 | 24 | 19 | 5 | 0 | 0 | 0 | 1 |
| 2025 | 24 | 20 | 4 | 0 | 0 | 0 | 1 |

A4 的失败是测试证据，不直接等同于业务资料失败。2017 的 24 个节点是 `unresolved_due_to_timeout`，不得计入任何终态。

## 4. 年度权威结论矩阵

结论枚举严格使用 A5 契约定义的 `verified_pass`、`conditional_pass`、`incomplete`、`conflicted`、`not_verified`。本轮没有把任何年度升级为 `verified_pass`。

| 年度 | gate / checkpoint | 证据一致性 | 权威结论 | 主要未决事项 |
|---|---|---|---|---|
| 2015 | conditional / conditional | conflicted | conditional_pass | 29-carrier uploaded set 不是 full-year pass；A attachment 4、远端回读 |
| 2016 | conditional / conditional | conflicted | conditional_pass | D attachment 2、A05 provenance、远端回读 |
| 2017 | conditional / conditional | conflicted | incomplete | 12 个 blocking missing requests；A4 24 节点超时未决 |
| 2018 | conditional / conditional | conflicted | incomplete | C-01—C-05 五个附件；远端回读 |
| 2019 | conditional / conditional | conflicted | conditional_pass | baseline directory 未独立枚举；远端回读 |
| 2020 | conditional / conditional | conflicted | conditional_pass | 远端回读；两个 optional official source；手工复核 |
| 2021 | conditional / conditional_pending_remote_readback | conflicted | conditional_pass | full-text semantic review 和 external corpus completeness |
| 2022 | conditional / conditional | conflicted | incomplete | A—E 官方题面、C/E workbooks、7 个 source requests |
| 2023 | pass / pass_pending_remote_readback | conflicted | conditional_pass | local/content pass 与 remote-pending scope；A4 当前 4 failures |
| 2024 | conditional / conditional | incomplete | incomplete | 7 个 missing files、A242 页序、人工复核 |
| 2025 | conditional / conditional | incomplete | conditional_pass | global queue `2025-MR-001`、远端回读、官方总体完整性 |

### 4.1 逐年证据摘要

#### 2015

gate 和 checkpoint 都只支持 29-carrier uploaded set 的 conditional pass；full-year completeness 为 false，A attachment 4 和远端回读仍未完成。A4 当前运行是 26 passed、10 failed，与历史 gate 的 36 passed 不同；两者均保留，A4 作为当前测试事实。

#### 2016

可用材料完成了局部核验，但 D attachment 2 缺失，A05 内容和 D attachment 1 仍需人工核验。A4 当前为 26 passed、2 failed；历史 gate/checkpoint 的 28 passed 作为历史快照保留。

#### 2017

gate 只确认 received subset，20 个 physical carriers 中有 12 个缺失，full-year completeness 为 false；中央 `missing_segment_requests.jsonl` 的 12 条请求全部 open/blocking。A4 另记录 24 个收集节点在 300 秒时限内没有终态。checkpoint 中历史性的 `24 passed` 与 A4 timeout 是两组不同运行证据，不能相互覆盖。

#### 2018

观察到的 corpus 可索引，但五个 C-problem data attachments 未提供，supporting-data completeness 为 false。A4 当前为 12 passed、4 failed；历史 16 passed 不能覆盖当前结果。

#### 2019

供应的 carriers 已处理，gate/checkpoint 保持 conditional；2019 baseline directory 未被独立枚举，expert commentary 未观察到，远端回读仍待完成。A4 当前为 10 passed、1 failed。

#### 2020

供应 bundle 在声明范围内完成索引和本地检查，但 remote readback、两个 optional official source 和四项 manual review 仍开放。A4 当前为 21 passed、11 failed；不据此直接判定业务资料错误。

#### 2021

bundle 身份和内部结构有证据，但 full-text semantic review 与 external official corpus completeness 均为 false，checkpoint 仍 pending remote readback。结论保持 conditional。

#### 2022

gate 明确记录 A—E 官方 problem statements、C/E official workbooks 缺失，full-year source complete 为 false，并报告 7 个 source requests。A4 的 2 个 skipped 仍按 skipped 记录，不转换为 failed 或 source absence。

#### 2023

gate 的 `pass` 限于 local/content checks；checkpoint 和报告的 `pass_pending_remote_readback` 是更宽的交付状态。A5 以 conditional_pass 表达这两个范围，不抹去 gate 的 local pass，也不把它升级为远端/全年度 pass。

#### 2024

gate/checkpoint 都保留 conditional，明确有 7 个 missing files、A242 页序问题和人工复核项。没有足够证据形成完整年度结论，因此为 incomplete。

#### 2025

gate/checkpoint 都是 conditional；全局人工队列中的 `2025-MR-001` 仍 open/nonblocking，不能在 A5 中重复或关闭。官方 excellent-paper set 的总体完整性和远端回读仍未观察到。

## 5. 冲突清单

共保留 9 个冲突/快照差异，均列明两侧证据：

- 2015、2016、2018、2019、2020、2021、2022：历史 gate/checkpoint 的测试摘要与当前 A4 运行结果不同。A4 是当前运行事实，历史结果不被删除。
- 2017：checkpoint 的历史 `24 passed` 与当前 A4 的 300 秒 timeout、0 terminal outcomes、24 unresolved 不同。不能推断具体节点结果。
- 2023：gate 的 local/content `pass` 与 checkpoint/report 的 `pass_pending_remote_readback` 是 scope/provenance 差异；A5 保留为 conditional。

这些冲突没有被静默修复，也没有因此修改 gate、checkpoint、报告或测试。

## 6. 缺失请求验证

中央 `missing_segment_requests.jsonl` 共 12 行，全部为 2017、状态 `open`、严重性 `blocking`。A5 逐条保留 request ID 和 requested repository path，引用请求文件、2017 gate、checkpoint 和状态报告进行验证。精确路径在当前索引仓库中未观察到，但这不等同于宣称外部来源不存在；12 条请求没有被关闭、合并或伪造。

2017 的请求 ID 为：`2017-MSR-001` 至 `2017-MSR-012`。逐条机器记录位于 `a5_status_reconciliation_2015_2025.json` 的 `validated_missing_segment_requests`。

## 7. 人工复核队列

新增的 A5 队列有 11 条开放复核任务，均 `blocks_a5: false`、`blocks_a6: true`。它们覆盖：2015 上传集范围、2016 D/A05、2017 缺失载体与 timeout、2018 五个附件、2019 baseline scope、2020 optional source、2021 external corpus、2022 七个 source requests、2023 scope 差异、2024 七个缺失项，以及对既有 `2025-MR-001` 的引用性后续动作。

2025 行引用既有中央队列 ID，不复制原始行，也不在 A5 中关闭它。

## 8. A6 最小修复建议

机器可读清单位于 `a5_proposed_repairs.json`，共 15 项，全部 `implemented: false`，且要求人工批准。建议范围包括：

1. 2015 上传集/附件范围；
2. 2016 D attachment 2 和 A05 provenance；
3. 2017 十二个缺失 trusted-baseline carriers；
4. 2017 仅年度、节点级 timeout diagnosis/continuation；
5. 2018 五个 C 附件；
6. 2019 baseline directory scope；
7. 2020 optional official sources 和远端 provenance；
8. 2021 external corpus 与 semantic review；
9. 2022 官方题面、workbooks 和七个 source requests；
10. 2023 local pass 与 remote-pending scope；
11. 2024 七个缺失项和 A242 页序；
12. 2025 E-video source ownership；
13. 跨年度 queue/progress scope 隔离；
14. `errors=ignore` 编码证据处理；
15. BOM 输入/输出策略与 page/worksheet bounds。

这些建议不允许批量重建、删除断言、批量 skip/xfail、编辑原始资料或扩大年度范围。A6 只有在人工批准、记录 before/after、执行 targeted regression 并保留 rollback 方法后才能实施。

## 9. 独立复核

- Review 1：直接读取正式阶段定义、A4 输出、年度 gate/checkpoint、报告、progress 和中央队列，完成每年度结论绑定。
- Review 2：独立执行严格 JSON/JSONL 解析、路径存在性检查、Git 历史核对、A4 总量重算以及 12 条 2017 请求逐条验证；未运行 pytest，未修改输入。
- 两次复核得到相同的 11 年结论、9 个冲突、A4 总量闭合和 2017 timeout 保留结果。

## 10. 阶段边界与停止规则

- A5 只读对账和生成建议，未实施任何修复。
- `tests_run: false`。
- `authoritative_files_modified: false`。
- `next_stage_started: false`。
- 只有五个 A5 允许输出可出现在本阶段 diff 中。
- 完成远端回读后立即停止；本轮不执行 A6。
