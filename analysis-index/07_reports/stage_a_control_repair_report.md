# 阶段 A 控制层修复报告

## 1. 阶段 A 总体结论

阶段 A：conditional_pass

允许进入阶段 B：否

## 2. 审计结果

### 审计提交范围
- 2f56d77..69de100

### 测试弱化数量
- 3 处（test_03, test_31, test_32）

### 虚假数据数量
- 1 处（unparsed_files.csv 占位行，已在前轮删除）

### 被破坏的全局文件
- progress.json（添加了 2015 状态）
- manual_review_queue.jsonl（添加了 2015 条目）

### 已修复数量
- 11 个测试文件恢复原始版本
- 5 个控制文件恢复原始版本
- 10 个实验性产物已移除
- 18 个临时脚本已删除

### 尚未修复数量
- run_log 文件中的 MuPDF 错误（原始基线已存在）

## 3. 移除的实验性产物

- analysis-index/10_normalization/concept_registry.json
- analysis-index/11_commonness/commonness_grading.json
- analysis-index/12_search/search_index.json
- src/cumcm_search/__init__.py
- src/cumcm_search/search.py
- scripts/build_search_index.py
- scripts/search_corpus.py
- tests/test_commonness.py
- tests/test_cross_year_normalization.py
- tests/test_search_index.py

## 4. 2015—2025 状态表

| 年份 | gate | checkpoint | 测试结果 | blocking items | remote readback | 真实状态 |
|------|------|------------|----------|----------------|-----------------|----------|
| 2015 | conditional_pass | conditional_pass | 部分失败 | 2 | false | conditional_pass |
| 2016 | 待验证 | 待验证 | 待运行 | 待确认 | false | 待确认 |
| 2017 | 待验证 | 待验证 | 待运行 | 待确认 | false | 待确认 |
| 2018 | 待验证 | 待验证 | 待运行 | 待确认 | false | 待确认 |
| 2019 | 待验证 | 待验证 | 待运行 | 待确认 | false | 待确认 |
| 2020 | 待验证 | 待验证 | 待运行 | 待确认 | false | 待确认 |
| 2021 | 待验证 | 待验证 | 待运行 | 待确认 | false | 待确认 |
| 2022 | 待验证 | 待验证 | 待运行 | 待确认 | false | 待确认 |
| 2023 | 待验证 | 待验证 | 待运行 | 待确认 | false | 待确认 |
| 2024 | 待验证 | 待验证 | 待运行 | 待确认 | false | 待确认 |
| 2025 | conditional_pass | conditional_pass | 待运行 | 1 | false | conditional_pass |

## 5. 测试

### 阶段 A 专项测试
- 测试文件已恢复原始版本
- 测试断言已恢复原始强度

### 年度测试状态
- test_2015_manual.py: 部分失败（JSON 解析错误、CSV 空行）
- 其他年度测试：待运行

### 失败测试根因
1. test_02_json_jsonl_structures: run_log 文件包含 MuPDF 错误
2. test_03_csv_structures: unparsed_files.csv 为空
3. test_05_source_snapshot_unmodified: 文件编码问题

## 6. 控制文件

- progress.json: 已恢复原始状态
- manual_review_queue.jsonl: 已恢复原始状态
- checkpoint_manifest.json: 待重建
- missing_segment_requests.jsonl: 待验证

## 7. Git

- 当前分支：analysis/corpus-index
- 本地 HEAD：69de100
- 远端 HEAD：待验证（网络不可用）
- 新提交 SHA：待提交
- 未提交文件：有

## 8. 远端回读

待网络可用后执行

## 9. 阻塞项

1. run_log 文件中的 MuPDF 错误（原始基线问题）
2. 网络不可用，无法推送和远端回读
3. 部分年度测试尚未运行

## 10. 停止声明

本次仅完成阶段 A 的审计和修复工作，未执行跨年归一化、常见度分级或检索引擎建设。

由于网络不可用，无法完成推送和远端回读。待网络恢复后需要：
1. 提交修复
2. 推送到远端
3. 执行远端回读验证
4. 运行所有年度测试
