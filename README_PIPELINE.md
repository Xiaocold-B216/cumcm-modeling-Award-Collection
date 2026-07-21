# CUMCM优秀论文库灾难恢复与1992—2010重建流水线

本分支以可信源资料基线 `a042ecf898feaba6fc81d543a10e0188db8b2b12` 为唯一原始资料基线，重建 `analysis-index`，并按年度连续处理1992—2010。

## 核心原则

- 原始资料只读，并与可信基线比较；
- physical file、carrier、segment、logical document、problem、solution lineage、representation分离；
- parse、evidence、segmentation、completeness、eligibility状态分离；
- 字段状态仅使用 `present / absent / unknown / not_applicable`；
- `unknown` 永不计为 `absent`；
- 不执行全库OCR；
- 全文提取缓存、页面渲染缓存和OCR缓存不进入公开提交；
- 每个年度生成独立质量门和检查点；
- 扫描件、多文章载体、语义重复和关系冲突进入人工复核队列。

## 入口

```bash
python scripts/restore_build_index.py
python scripts/build_index.py --year inventory --resume
python scripts/build_index.py --year 1992 --resume
python scripts/build_index.py --year all --resume
python scripts/build_index.py --year summary --resume
```

## 自动执行

GitHub Actions工作流将：

1. 检出 `analysis/corpus-index`；
2. 验证仓库内直接跟踪的解析器（不再使用截断的gzip恢复载荷）；
3. 构建全库清单；
4. 按1992—2010逐年运行；
5. 每年测试、提交、推送；
6. 生成跨年汇总和最终恢复包；
7. 上传可下载检查点artifact。

自动输出属于保守候选结果。只有经过页面视觉核验的内容才能升级为人工确认或完全验证状态。

## 版本

- Schema：1.4.1
- Parser：0.5.2
- 可信源资料基线：`a042ecf898feaba6fc81d543a10e0188db8b2b12`
