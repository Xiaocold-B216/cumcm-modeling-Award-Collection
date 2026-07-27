# A5 阶段报告：2015—2025 状态对账

## 结果

- 阶段：A5
- 输入提交：`92d4889122d4bdb818c1fd896d410cce971901e9`
- 阶段目标：对照 gate、checkpoint、报告、队列、progress 和 A4 结果，形成逐年证据结论与 A6 最小修复建议。
- 当前结论：已完成证据对账；最终 `passed` 还必须由独立提交、普通 push 和远端原始字节回读确认。
- A6：未启动，禁止在本轮进入。

## 已完成内容

1. 覆盖 2015—2025 全部 11 个年度。
2. 将 A4 当前测试事实与历史 gate/checkpoint 测试摘要分开记录，没有用历史结果覆盖当前结果。
3. 保留 A4 总量闭合：`267 = 194 + 47 + 2 + 0 + 24`。
4. 保留 2017：24 collected、0 terminal outcomes、24 unresolved due to timeout、exit 124、timeout 300 秒。
5. 逐条验证中央 `missing_segment_requests.jsonl` 的 12 条 2017 open/blocking 请求，未编造节点 ID，未关闭请求。
6. 区分年度队列与全局队列；既有 `2025-MR-001` 被引用而非复制或关闭。
7. 记录 9 个冲突/历史快照差异，所有冲突均列出两侧证据路径和处理原则。
8. 生成 15 项机器可读 A6 建议和 11 项人工复核任务；没有实施任何建议。

## 五个允许输出

- `analysis-index/00_control/a5_status_reconciliation_2015_2025.json`
- `analysis-index/00_control/a5_status_reconciliation_2015_2025.md`
- `analysis-index/00_control/a5_proposed_repairs.json`
- `analysis-index/00_control/a5_human_review_queue.jsonl`
- `analysis-index/00_control/a5_stage_report.md`

## 禁止事项核对

- `tests_run: false`；本轮不运行 pytest。
- 未修改 `progress.json`、gate、checkpoint、年度报告、队列、测试、业务资料或原始资料。
- 未实施修复；`repair_applied: false`。
- 未启动 A6；`next_stage_started: false`。
- A4 的五个产物、阶段定义和 A1—A3 产物未修改。

## 质量门

- JSON 必须严格解析，禁止 非标准数值、注释和 BOM。
- JSONL 必须逐行解析，review ID 和 repair ID 必须唯一。
- Markdown、JSON、JSONL 必须为 UTF-8、无 BOM、末尾 LF。
- 所有证据路径必须为仓库相对路径且存在；不得写入本地绝对路径、凭据或外部个人路径。
- Git diff 只能包含上述五个 A5 输出。
- 自检通过后才允许创建提交。

## 交付与停止

提交信息：`audit(control): reconcile 2015-2025 authoritative states`

交付必须使用普通 push 到 `analysis/corpus-index`，随后执行 `git ls-remote`、`git fetch`、本地/远端 `rev-parse`、`git diff --exit-code`、`git status --short`，并以 `git cat-file blob` 对五个文件执行远端原始字节回读。若远端分叉、网络、权限、认证或回读失败，A5 应按对应原因 blocked；不得伪报 passed。

远端回读通过后，A5 才能记为 `passed`，A6 才具备 `ready_to_start` 条件。本轮在远端回读后停止。
