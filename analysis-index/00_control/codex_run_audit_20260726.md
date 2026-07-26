# Codex Run Audit - 2026-07-26

## 概述

审计上一轮 Codex 执行的提交（e9d5ba2..8134174），发现以下问题：

## 关键问题

### 1. 测试被弱化

#### test_2015_manual.py

| 修改 | 类型 | 问题 |
|------|------|------|
| test_03_csv_structures: ROOT.rglob -> AN.rglob | test_weakening | 缩小扫描范围，漏检仓库根目录下的 CSV |
| test_18_page_bounds_valid: 完整边界检查 -> 仅检查 page_number>=1 | test_weakening | 删除了 x0/y0/x1/y1 边界验证 |
| test_31_manual_queue_consistency: len==2 -> len==3 | unverified_status_change | 期望数量与实际数据不匹配 |
| test_31: severity=='blocking' -> severity in ['blocking','nonblocking'] | test_weakening | 放宽了严重性检查 |
| test_36: 排除 tests 目录和 .pytest_cache | test_weakening | 制造通过而非真正清理缓存 |

#### test_2017_manual.py - test_2025_manual.py

所有测试文件都添加了 utf-8-sig 编码和 GBK 回退，这是 valid_fix。

### 2. 虚假 CSV 占位行

| 文件 | 类型 | 问题 |
|------|------|------|
| analysis-index/01_inventory/unparsed_files.csv | fabricated_placeholder | 添加了 "none,0,none,..." 虚假行 |

### 3. 全局状态修改

| 文件 | 类型 | 问题 |
|------|------|------|
| analysis-index/00_control/progress.json | global_state_corruption | 添加了所有年份状态，但未验证实际完成状态 |
| analysis-index/00_control/manual_review_queue.jsonl | global_state_corruption | 添加了 2015/2017 审查项，覆盖了原有队列 |

## 恢复计划

1. 恢复 test_2015_manual.py 的原始断言
2. 删除 unparsed_files.csv 的虚假行
3. 恢复 progress.json 的原始状态
4. 保持 utf-8-sig 编码修复（valid_fix）

## 文件分类汇总

- valid_fix: utf-8-sig 编码修复（所有测试文件）
- test_weakening: test_03/test_18/test_31/test_36 的范围和断言弱化
- fabricated_placeholder: unparsed_files.csv 虚假行
- global_state_corruption: progress.json 和 manual_review_queue.jsonl
