# A8 最终汇总与远端交付验收

## 执行摘要

本报告是 A1—A8 工作流的终止交付记录。A1—A7 的历史提交、控制产物、年度 Gate/Checkpoint/Report、测试记录、Schema 和源完整性证据已读取并汇总。A8 不执行业务修复，不升级任何不完整、conditional、missing、unknown 或 pending 状态。

首次 A8 汇总提交和首次普通 push/远端回读已经通过；本文件正在由第二个独立 A8 闭环提交固化最终交付状态。

## 可信恢复点

- 仓库：`Xiaocold-B216/cumcm-modeling-Award-Collection`
- 分支：`analysis/corpus-index`
- A8 输入 HEAD：`fb670937d61d8394ecbf4ec0dd1bb3d58e503086`
- 可信源基线：`a042ecf898feaba6fc81d543a10e0188db8b2b12`
- 基线对象：commit；基线条目 3614；缺失 0；源 blob 差异 0。
- Python：3.14.6；pytest：9.1.1；PyMuPDF：1.28.0；jsonschema：4.26.0。
- 工作区初始状态：clean；A7 远端持久化和回读：passed。

## A1—A8 阶段表

| 阶段 | 输入提交 | 主提交 / 终止提交 | 状态 | 核心输出 | 残余风险 |
|---|---|---|---|---|---|
| A1 | `53819844...` | `400d5c38989585ec027b4c579fba4b700542e55c` | passed | 历史模型变更审计 | 历史未决项转入后续审计 |
| A2 | `400d5c...` | `66af72432901aec7068942d09aee41c8bf0ac8f2` | passed | 实验性产物移除核验 | 测试完整性问题转入 A3 |
| A3 | `66af724...` | `cae3bbe7006b3616bd94578518d20dee7f6e8d3b` | passed | 年度测试完整性审计 | 需运行时验证 |
| Bootstrap | `cae3bbe...` | `ed56c65...` / `b306c7b...` | passed | A4—A8 正式定义和人类可读计划 | 无 |
| A4 | `b306c7b...` | `1ab43d4...` → `92d4889122d4bdb818c1fd896d410cce971901e9` | passed_with_failures_recorded | 年度基线和 2017 timeout 核算 | 47 failures、24 unresolved timeout nodes |
| A5 | `92d4889...` | `2027a39cf32a878812ef8f290738e063eea94131` | passed | 逐年对账、15 个修复候选、11 个人工复核项 | conditional/incomplete 年份保留 |
| A6 | `2027a39...` | `2f318cef8415ca49b8e4088ebd266443406c73f5` | passed_with_recorded_failures | 批准的最小测试策略修复和 2017 诊断 | 3 个 2017 既有失败、延后修复 |
| A7 | `2f318cef...` | `b4d31fc...` → `fb670937d61d8394ecbf4ec0dd1bb3d58e503086` | passed_with_recorded_failures | 全量回归、Schema、跨文件审计 | 25 annual、12 additional failures、2 skips |
| A8 | `fb670937...` | `b5fd0be...` → 本次闭环提交 | final_delivery_closure_pending | 最终汇总和恢复检查点 | 最终四文件回读后终止 |

A7 的完整恢复链保留为：`b4d31fc` → `d07dcfdd41fc778947e768835a13f9e3029f79cd` → `173393b` → `1d343f5` → `d830e61` → `fb67093`。其中 `d830e61` 仅修复精确派生控制文件分类和 Git 中文路径严格解码；未修改业务资料。

## 2015—2025 年度状态

| 年份 | Gate | Checkpoint | 最终可信状态 | Blocking | Human Review | Missing Source |
|---:|---|---|---|---:|---:|---:|
| 2015 | conditional_pass | conditional_pass | conditional_pass | 2 | 2 | 未量化 |
| 2016 | conditional_pass | conditional_pass | conditional_pass | 0 | 3 | 1 |
| 2017 | conditional_pass | conditional_pass | incomplete | 12 | 12 | 12 |
| 2018 | conditional_pass | conditional_pass | incomplete | 0 | 1 | 5 |
| 2019 | conditional_pass | conditional_pass | conditional_pass | 0 | 0 | 未量化 |
| 2020 | conditional_pass | conditional_pass | conditional_pass | 0 | 4 | 2 |
| 2021 | conditional_pass | conditional_pass_pending_remote_readback | conditional_pass_pending_remote_readback | 0 | 2 | 未量化 |
| 2022 | conditional_pass | conditional_pass | incomplete | 7 | 3 | 7 |
| 2023 | pass | pass_pending_remote_readback | conditional_pass_pending_remote_readback | 0 | 0 | 未量化 |
| 2024 | conditional_pass | conditional_pass | incomplete | 7 | 2 | 7 |
| 2025 | conditional_pass | conditional_pass | conditional_pass_pending_remote_readback | 0 | 1 | 未量化 |

`未量化` 表示该年度控制证据没有提供可等价合并的中央缺段请求数量，不表示缺失为零。2017 的 12 条 blocking 缺段请求和 24 个 A4 timeout 未决节点分别保留；2022 的 2 个环境变量门控 skip 不转化为 source completeness；2021、2023 的 remote-readback scope 差异不被覆盖。

## 测试与 Schema 验证

- A4 历史基线：267 collected、194 passed、47 failed、2 skipped、0 errors、24 unresolved due to 2017 timeout。
- A6 targeted：33 passed、0 failed、0 errors；2017 定向诊断 24 节点为 21 passed、3 既有 failed、0 timeout。
- A7 年度回归：267 collected、240 passed、25 retained failed、2 skipped、0 errors、0 timeout。
- A7 额外正式回归：28 collected、16 passed、12 retained failed、0 errors。
- A7 全量：306 collected、267 passed、37 failed、2 skipped、0 errors；collection/import/syntax errors 为 0。
- Infrastructure：11 passed、0 failed、0 errors。
- Schema：4 definitions、5314 instances、0 validation errors。
- 严格 JSON/JSONL/CSV/Markdown 结构审计通过；新失败 0；hard errors 0。

这些数字只表达各阶段真实执行和记录的结果，不表达“全部测试通过”。

## 源资料完整性

源基线 `a042ecf...` 的 3614 个 Git 条目均可解析，缺失 0，当前源 blob 差异 0，原始和提交源修改均为 0。Manifest 2157 条中 107 条为直接可解析路径且哈希核验通过；2050 条仍属于 upload、archive-member 或 external-source scope，未被错误判为哈希差异。文件存在不被推断为内容完整，unknown 不被推断为 absent。

## 未解决问题和人工复核项

- 2017：12 条中央缺段请求仍 open/blocking；接收集不是完整年度源；A1 PDF font encoding 仍需视觉复核；A4 timeout 的 24 个节点没有逐节点终态。
- 2018、2022、2024：明确的缺源文件/附件和 supporting-data 不完整状态保持不变。
- 2021、2023：年度 checkpoint/report 的 remote-readback pending scope 差异保持不变。
- 2025：`2025-MR-001` 的跨标签字节相同 E 视频需要源确认，且官方总体完整性未观察到。
- 全局人工复核：`2025-MR-001`；A5 人工复核队列仍有 11 项，年度队列分别保留在年度证据中。
- Retained failures：25 个年度失败、12 个额外正式失败、2 个环境变量门控 skip。

## 恢复说明

跨机器恢复使用占位符，不依赖个人绝对路径：

```powershell
Set-Location <REPOSITORY_ROOT>
git clone <repository>
git fetch origin analysis/corpus-index
git checkout analysis/corpus-index
git rev-parse HEAD
git cat-file -e a042ecf898feaba6fc81d543a10e0188db8b2b12^{commit}
git fetch --no-tags --filter=blob:none origin a042ecf898feaba6fc81d543a10e0188db8b2b12

$env:PYTHONDONTWRITEBYTECODE = "1"
<APPROVED_PYTHON> -m pytest -p no:cacheprovider tests/test_infrastructure.py
<APPROVED_PYTHON> -m pytest --collect-only -q -p no:cacheprovider tests
<APPROVED_PYTHON> -m pytest -q -p no:cacheprovider tests
git fetch origin
git ls-remote origin refs/heads/analysis/corpus-index
git rev-parse HEAD
git rev-parse origin/analysis/corpus-index
git diff --exit-code HEAD origin/analysis/corpus-index
```

批准运行时版本：Python 3.14.6、pytest 9.1.1、PyMuPDF 1.28.0、jsonschema 4.26.0；已记录传递依赖为 attrs 26.1.0、jsonschema-specifications 2025.9.1、referencing 0.37.0、rpds-py 2026.6.3。

## 远端交付结果

首次 A8 汇总提交 `b5fd0be23922cb1ad2d2cc97e8b203e146643d5d` 已普通 push，首次远端回读已通过：四个 A8 文件、四个 A7 最终产物、`scripts/build_index.py` 和 A8 定义均 HTTP 200、非 HTML、本地/Git blob/raw 三方字节一致。当前正在创建最终闭环提交；A8 不使用 force push，不修改 A1—A7，不提交测试 XML、日志、缓存或临时文件。

## 终止声明

A8 是终止阶段。最终闭环提交 push 并完成四个 A8 文件远端回读后，状态固化为 `A8 = passed`、`workflow = completed`、`terminal = true`、`next_stage = null`，随后停止，不启动 A9 或任何其他阶段。
