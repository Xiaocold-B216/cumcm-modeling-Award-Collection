# A7 全量回归、质量门与跨文件一致性复审报告

## 1. 输入与边界

- 既有阻塞提交：`b4d31fc6bb3b0373464f1f7f92322390e0ab446b`
- 本轮格式修复提交：`d07dcfdd41fc778947e768835a13f9e3029f79cd`
- 复审输入：`d07dcfdd41fc778947e768835a13f9e3029f79cd`
- 分支：`analysis/corpus-index`
- A6：`passed_with_recorded_failures`
- 工作区在复审开始时干净；A8 未启动。
- 未修改测试、业务资料、A4/A5/A6 产物、Gate、Checkpoint、报告、progress、队列、索引或统计文件。

本轮阻塞解除只使用已批准的现有运行时恢复：PyMuPDF 1.28.0（提供 `fitz`）和 `jsonschema` 4.26.0 及其必要依赖。Python 3.14.6、pytest 9.1.1 未改变，仓库依赖声明未改变。测试均使用批准解释器、`PYTHONDONTWRITEBYTECODE=1` 和 `-p no:cacheprovider`。

## 2. 收集与全量回归

收集结果：

| 范围 | Collected | Collection errors | Import errors | Syntax errors |
|---|---:|---:|---:|---:|
| 2015—2025 年度套件 | 267 | 0 | 0 | 0 |
| 其中 2017 | 24 | 0 | 0 | 0 |
| 全部 `tests/` | 306 | 0 | 0 | 0 |

年度套件在格式修复前的已记录基线为 `267 = 231 passed + 34 failed + 2 skipped`。格式修复后实际结果为：

| 范围 | Collected | Passed | Failed | Skipped | Errors | Timeout | Exit |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2015—2025 年度套件（修复后） | 267 | 240 | 25 | 2 | 0 | 0 | 1 |
| 2008 与恢复统计额外套件 | 28 | 16 | 12 | 0 | 0 | 0 | 1 |
| 基础设施首次终态结果 | 11 | 9 | 2 | 0 | 0 | 0 | 1 |
| 全部 `tests/` | 306 | 265 | 39 | 2 | 0 | 0 | 1 |

年度失败数减少 9 个是本轮批准修复的直接效果：四份 run log 规范化后，原先仅因全局 JSON/JSONL 解析失败的年度断言转为通过。剩余 25 个年度失败是既有失败的子集；没有新增失败、skip、xfail、error 或 timeout。2017 修复后为 24 collected、22 passed、2 failed、0 skipped、0 errors、0 timeout；两项失败仍为既有 `test_21_missing_requests_exact` 和 `test_23_progress_conservative`。

额外套件仍为 28 collected、16 passed、12 failed。基础设施测试是首次获得可收集运行的独立结果，两个失败不自动归入历史保留失败：

- `tests/test_infrastructure.py::InfrastructureTests::test_source_verification_and_baseline_count`
- `tests/test_infrastructure.py::InfrastructureTests::test_unicode_baseline_paths_are_real_checkout_paths`

两者均因源码声明的基线对象 `a042ecf898feaba6fc81d543a10e0188db8b2b12` 不在本地 Git 对象库中而失败。没有通过修改测试或伪造基线来掩盖该结果。

## 3. Schema 验证

四份 Schema 定义均通过 Draft 2020-12 `check_schema`。从仓库文件字段和生成脚本确定的实例映射如下：

| Schema | 权威实例 | 实例数 | 错误 |
|---|---|---:|---:|
| logical_document | `analysis-index/02_documents/logical_documents.jsonl` | 326 | 0 |
| feature | 上述逻辑文档的 `feature_statistics` | 4238 | 0 |
| representation | `analysis-index/02_documents/representations_1992.jsonl`—`representations_2010.jsonl` | 367 | 0 |
| relation | `analysis-index/04_relations/document_relations.jsonl` | 383 | 0 |

共验证 5314 个实例，字段映射已解析，未使用字段适配或猜测性转换。

## 4. 严格结构与编码质量门

- JSON：1620 个，严格 UTF-8 1620 个，解析成功 1620 个，重复键/NaN/Infinity 0，BOM 0。
- JSONL：570 个、19960 行，逐行解析成功，无坏行、无 BOM。
- CSV：96 个、10371 行，无坏行；86 个历史输入 BOM 按 `utf-8-sig` 规则保留。
- Markdown 控制文件：2346 个严格 UTF-8，BOM 0，末尾 LF 2346 个，NUL 0。
- 四份 run log 已全部为严格 JSON、无 BOM、末尾 LF；两份历史 Markdown 仅移除了开头 BOM，其余字节保持原样。
- AST 语法检查：`tests/` 与 `scripts/` 共 30 个 Python 文件，0 syntax error。
- 无个人绝对路径、凭据、任务产生的缓存或临时文件；未修改测试，没有新增 skip/xfail 或 `errors="ignore"`。

## 5. 跨文件一致性

- Gate/Checkpoint 可比数值不一致：0。
- 2021、2023 保留已记录的远端回读作用域差异，未升级为完整通过。
- progress 缺少 2015—2024 年状态键，属于既有部分历史状态模型，不被解释为年度不存在。
- 队列 ID 重复：0；A5 证据路径孤立：0；全局缺段请求 12 条均为 open/blocking；A5 队列 11 条 open。
- 载体清单 2157 条；按直接 checkout-relative 路径解析 107 条且 SHA-256 全部一致，0 hash mismatch；其余 2050 条属于当前未直接落地的上传、归档成员或外部源范围。
- 索引重复 ID 集合、字段感知外键孤立、年度字段不一致、缺失 preferred representation：均为 0。

## 6. 最终判定

`A7 = blocked: environment`

阻塞只剩首次基础设施结果中的两个源基线校验失败：本地缺少声明的 Git 基线对象。Schema、严格格式、收集、跨文件一致性和风险扫描均已通过或按既有条件项记录。A7 不表示全部测试通过；年度仍有 25 个保留失败，额外套件仍有 12 个保留失败。

由于基础设施阻塞未解除，`A8 = not_ready_to_start`。本轮不执行 A8。
