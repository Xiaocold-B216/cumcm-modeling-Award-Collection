# CUMCM 获奖论文数据库排版格式审计证据

## 审计元数据

```text
STAGE=FORMAT-AUDIT-01
ROOT=D:\cumcm-modeling-Award-Collection
BRANCH=library-refactor-v1
HEAD_START=557724fba6572d4d83dc421feda5b17b13ff8d66
PYTHON=D:\python\python.exe 3.13.15
PDF_INSPECTOR=1.15.0
POPPLER=D:\texlive\2026\bin\windows (25.02.0)
PARALLEL_TASK_DETECTED=1
PARALLEL_TASK_STAGE=G8-Q3-CONTRACT-REFINEMENT-OCR-TIMEOUT / G8 scale
PARALLEL_VERDICT=PARALLEL_SAFE_WITH_SNAPSHOT
FORMAL_PAPERS_FOUND=677
FORMAT_ANALYSIS_SOURCE_COUNT=412
SEMANTIC_PROBLEM_PACKAGE_EXCLUSIONS=5
ELIGIBLE_LAYOUT_PAPERS=412
ELIGIBLE_FONT_PAPERS=282
YEARS_COVERED=1992,1993,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025
PROBLEMS_COVERED=A,B,C,D,E
CORPUS_IDENTITY_FINGERPRINT_START=C5481E220EAE311395EDCBB49B9E7DB9FE846BC9DA0BD93E6FCBFAE0AA72A7DD
CORPUS_IDENTITY_FINGERPRINT_END=C5481E220EAE311395EDCBB49B9E7DB9FE846BC9DA0BD93E6FCBFAE0AA72A7DD
CORPUS_SOURCE_SHA_FINGERPRINT_START=4FE65A92342D1724E3552D0EBE898E67527A6BCBF6BF13CD367894942BE66504
CORPUS_SOURCE_SHA_FINGERPRINT_END=4FE65A92342D1724E3552D0EBE898E67527A6BCBF6BF13CD367894942BE66504
CORPUS_IDENTITY_DRIFT_COUNT=0
CORPUS_SOURCE_SHA_DRIFT_COUNT=0
CORPUS_PATH_DRIFT_COUNT=0
FORMAL_MEMBERSHIP_DRIFT_COUNT=0
CORPUS_DRIFT=0
OPERATIONAL_EVIDENCE_DRIFT_ONLY=1
PAGE_SIZE_DOMINANT=True
TOP_MARGIN_MEDIAN=25.421
BOTTOM_MARGIN_MEDIAN=19.526
LEFT_MARGIN_MEDIAN=25.027
RIGHT_MARGIN_MEDIAN=13.953
BODY_FONT_DOMINANT=SimSun/Song
BODY_FONT_SIZE_DOMINANT=
BODY_LINE_SPACING_DOMINANT=
LEVEL1_HEADING_DOMINANT=
LEVEL2_HEADING_DOMINANT=
LEVEL3_HEADING_DOMINANT=
ABSTRACT_STYLE_IDENTIFIED=1
KEYWORD_STYLE_IDENTIFIED=1
FIGURE_STYLE_IDENTIFIED=1
TABLE_STYLE_IDENTIFIED=1
EQUATION_STYLE_IDENTIFIED=1
REFERENCE_STYLE_IDENTIFIED=1
APPENDIX_STYLE_IDENTIFIED=1
VISUAL_SAMPLES_CHECKED=30
OUTLIER_PAPERS=398
RESOURCE_CONTENTION_RISK=LOW
OCR_RESOURCE_CONTENTION_AVOIDED=1
TMP_NAMESPACE_ISOLATED=1
NETWORK_ACCESS_USED=0
DOWNLOAD_RUN=0
NEW_DEPENDENCY_INSTALLED=0
SOURCE_PDF_MODIFIED=0
SOURCE_PDF_RENAMED=0
SOURCE_PDF_MOVED=0
FORMAL_SET_MODIFIED=0
CATALOG_MODIFIED_BY_FORMAT_AUDIT=0
G8_EVIDENCE_MODIFIED_BY_FORMAT_AUDIT=0
GIT_OPERATIONS=0
```

## 语料范围

- Paper identities: 677
- Direct analyzed Paper PDFs: 412
- Semantic problem-package exclusions: 5
- Layout eligible: 412
- Typography eligible: 282
- Observations: 8652 component rows
- Visual sample pages rendered: 30

## 方法与证据类型

- OBSERVED：catalog identity/membership、实际文件 SHA-256、pdf-inspector classification/text positions、Poppler pdfinfo/pdffonts、页面坐标和渲染页。
- INFERRED：跨 Paper 的主流值、比例、分位数、年份/题目比较。
- RECOMMENDED：结合覆盖率、可读性和 Word/LaTeX 可实现性给出的统一起点。
- UNKNOWN：PDF 证据不足的三线表线型、字符间距、公式语义和逐字字体映射。
- OCR：未运行全文 OCR；不可分析 PDF 不用 OCR 字体冒充原字体。

## 输出之间的绑定

- 冻结语料：`derived/format/format_audit_corpus_snapshot.csv` 与 `format_audit_snapshot.json`。
- Paper 清单：`derived/format/paper_format_inventory.csv`。
- 逐 Paper/组件观察：`derived/format/paper_format_observations.csv`。
- 统计汇总：`derived/format/paper_format_summary.csv`。
- 异常：`derived/format/format_outliers.csv`。
- 机器规范：`derived/format/paper_format_spec.json`。

## 视觉抽检

按年份、题目类别、PDF 类型和边界样本分层，渲染标题页/中间页/末页到 `tmp/format_audit/visual`；清单为 `tmp/format_audit/visual_samples.csv`。渲染不改变源文件，也未用于断言 OCR 字体。

## 按年份

| 年份 | Paper | PDF | 文本层 | 字体资格 | A4 |
|---:|---:|---:|---:|---:|---:|
| 1992 | 6 | 6 | 6 | 5 | 1 |
| 1993 | 4 | 3 | 3 | 1 | 1 |
| 1995 | 15 | 15 | 15 | 0 | 0 |
| 1996 | 12 | 12 | 12 | 2 | 0 |
| 1997 | 16 | 16 | 16 | 4 | 0 |
| 1998 | 15 | 15 | 15 | 10 | 0 |
| 1999 | 16 | 16 | 16 | 16 | 0 |
| 2000 | 21 | 21 | 21 | 21 | 0 |
| 2001 | 25 | 23 | 23 | 23 | 12 |
| 2002 | 25 | 23 | 23 | 16 | 16 |
| 2003 | 27 | 23 | 23 | 14 | 14 |
| 2004 | 17 | 12 | 12 | 1 | 1 |
| 2005 | 22 | 18 | 18 | 18 | 0 |
| 2006 | 15 | 11 | 11 | 11 | 11 |
| 2007 | 34 | 28 | 28 | 15 | 28 |
| 2008 | 32 | 27 | 27 | 24 | 25 |
| 2009 | 26 | 22 | 22 | 13 | 21 |
| 2010 | 23 | 19 | 19 | 13 | 19 |
| 2011 | 65 | 9 | 9 | 8 | 9 |
| 2012 | 37 | 7 | 7 | 6 | 7 |
| 2013 | 27 | 6 | 6 | 6 | 6 |
| 2014 | 36 | 10 | 10 | 10 | 10 |
| 2015 | 23 | 0 | 0 | 0 | 0 |
| 2016 | 19 | 15 | 15 | 15 | 15 |
| 2017 | 22 | 18 | 18 | 18 | 17 |
| 2018 | 16 | 12 | 12 | 12 | 12 |
| 2019 | 17 | 12 | 12 | 0 | 0 |
| 2020 | 18 | 13 | 13 | 0 | 0 |
| 2021 | 22 | 0 | 0 | 0 | 0 |
| 2022 | 2 | 0 | 0 | 0 | 0 |
| 2023 | 5 | 0 | 0 | 0 | 0 |
| 2024 | 5 | 0 | 0 | 0 | 0 |
| 2025 | 12 | 0 | 0 | 0 | 0 |

## 按题目类别

| 类别 | Paper | PDF | 文本层 | 字体资格 | A4 |
|---|---:|---:|---:|---:|---:|
| A | 229 | 178 | 178 | 117 | 92 |
| B | 200 | 152 | 152 | 111 | 78 |
| C | 100 | 46 | 46 | 31 | 28 |
| D | 134 | 33 | 33 | 23 | 27 |
| E | 14 | 3 | 3 | 0 | 0 |

## 统计解释

页面边距是基于普通正文页文本 bounding box 的 Paper 级中位数；封面、页眉页脚、图像对象和无文本页不能被完全排除，因此应作为估计而非原始 Word 设置的直接真值。正文行距是 PDF 基线间距及字号比值，不能反推出源文档段落设置。字体对象名称由 pdffonts 保留，pdf-inspector 的 F/TT 资源 ID同时保留；当二者不能逐字对应时，规范中的字体家族只写文档级候选并降低置信度。

## 漂移与副作用

- Corpus drift: 0 (identity=0, sha=0, path=0, membership=0)
- Operational evidence drift only: 1
- Source PDF modified/renamed/moved: 0/0/0
- Catalog/G8 evidence modified by FORMAT-AUDIT: 0/0
- Git mutation: 0
- Temporary namespace isolated: 1

## 复现

Python runtime: D:\python\python.exe; pdf-inspector 1.15.0; Poppler: D:\texlive\2026\bin\windows\pdfinfo/pdffonts/pdftoppm 25.02.0。重新运行时只应读取同一组 catalog/membership/source SHA，并将输出写入同名 FORMAT 目录。
