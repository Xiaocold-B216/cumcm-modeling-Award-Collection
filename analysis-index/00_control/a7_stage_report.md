# A7 全量回归与跨文件一致性审计报告

## 输入状态

- 阶段：A7；A8 未启动。
- 分支：`analysis/corpus-index`
- 输入 HEAD：`2f318cef8415ca49b8e4088ebd266443406c73f5`
- A6：`passed_with_recorded_failures`，其独立 push 和远端回读已在 A7 开始前确认通过。
- 工作区：A7 产物创建前干净。
- 运行时：approved interpreter，Python 3.14.6，pytest 9.1.1。
- A6 报告中的 `completed_locally_pending_remote_readback` 被识别为历史提交前文字，没有被当作当前阻塞。

## 执行范围

A7 按 `tests/` 实际内容将 14 个 Python 测试文件视为正式测试，至少包含 2015—2025 的 11 个年度文件，并额外覆盖 2008 终结测试、基础设施测试和恢复统计测试。未修改测试、业务资料、A4/A5/A6、Gate、Checkpoint、报告、progress、队列、索引或统计文件；未安装、升级或降级依赖。

## 测试收集与全量回归

2015—2025 年度完整收集通过：267 节点，2017 年 24 节点，collection/import/syntax errors 为 0。年度全量执行包含 2017，结果为：

| 范围 | Collected | Passed | Failed | Skipped | Errors | Timeout | Exit |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2015—2025 年度套件 | 267 | 231 | 34 | 2 | 0 | 0 | 1 |
| 2008 与恢复统计额外套件 | 28 | 16 | 12 | 0 | 0 | 0 | 1 |

完整 `tests/*.py` 收集在 `tests/test_infrastructure.py` 处因 `ModuleNotFoundError: fitz` 失败，退出码为 2；因此基础设施测试未被伪装为通过。该固定运行时缺少依赖，A7 标记 `blocked: environment`，没有安装依赖。

年度 34 个失败均为 A6 已记录的保留失败，2017 的三个失败仍为：

- `tests/test_2017_manual.py::test_03_json_and_jsonl_parse`
- `tests/test_2017_manual.py::test_21_missing_requests_exact`
- `tests/test_2017_manual.py::test_23_progress_conservative`

相对 A6 没有新失败、错误、超时或节点缺失。两个 skip 是 2022 年已有的环境变量门控，未新增 skip/xfail。

## Schema、结构和编码

- 4 个 Schema 定义 JSON 可严格解析；但固定环境没有 `jsonschema`，仓库也没有可执行的正式 validator，因此 Schema 实例验证未完成，属于环境阻塞。
- 1,617 个 JSON 中 1,613 个严格解析通过；4 个既有 `run_logs` 文件含非 JSON 内容，未改写。
- 570 个 JSONL、19,960 行逐行解析通过；无坏行、重复键、NaN 或 Infinity。
- 96 个 CSV、10,371 行按仓库历史 `utf-8-sig` 规则解析通过，无坏行；86 个历史 CSV 带 BOM，未把历史输入规则误用于 A7 新输出。
- 2,345 个 Markdown 控制文件可严格解码并有末尾 LF；其中 2 个历史文件带 BOM。
- A7 新产物必须在提交前另行验证为 UTF-8、无 BOM、LF-only、末尾 LF。

## 跨文件一致性

- 2015—2025 Gate 与 Checkpoint 的可比数值没有发现不一致。
- 2021 与 2023 的 Gate/Checkpoint 存在已记录的远端回读作用域差异；没有把 `pass_pending_remote_readback` 提升为完整通过。
- `progress.json` 缺少 2015—2024 年度状态键；A5 已明确以更具体的 Gate、Checkpoint 和年度报告为准，未将缺少键解释成年度不存在。
- 全局人工复核队列为 1 条开放项；全局缺段请求为 12 条开放且 blocking，均归属 2017；A5 队列为 11 条开放项，ID 唯一且对全局 2025 复核项的引用闭合。
- 2015—2025 索引检查中，重复 ID、字段可用范围内的外键孤立、年度字段不一致和缺失 preferred representation 均为 0。
- 2,157 条载体清单记录中，159 条可直接解析到仓库文件且 SHA-256 全部一致；1,998 条属于当前仓库不可直接解析的上传、归档成员或外部源范围；未发现已解析文件的哈希不一致。

## 风险与边界

风险扫描未发现个人绝对路径、凭据模式或任务产生的缓存/临时文件。已有 `errors="ignore"` 命中主要是审计说明文字，另有一个未修改脚本命中；已有 skip/xfail 和 placeholder 词均结合上下文记录，未视为 A7 新弱化。A7 没有实施任何修复或返工。

## A7 最终判定

`A7 = blocked: environment`。

阻塞依据是：

1. 仓库正式测试 `tests/test_infrastructure.py` 依赖当前固定环境中不存在的 `fitz`，导致完整 `tests/*.py` 收集不能通过；
2. 当前环境没有 `jsonschema` 且仓库没有可执行 Schema validator，A7 要求的正式 Schema 验证无法完成；
3. 既有 4 个非纯 JSON run-log 和历史 BOM 已如实记录，A7 未修改它们。

本报告不表示所有测试通过，也不实施任何 A7 之外的修复。提交、普通 push 和远端回读是本四文件交付的后置门；A8 不得启动。
