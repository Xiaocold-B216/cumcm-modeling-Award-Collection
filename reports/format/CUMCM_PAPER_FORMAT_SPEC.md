# CUMCM 获奖论文数据库排版格式规范

## 1. 文档说明

本文是基于当前项目正式 Paper 身份与可直接分析主 PDF 的数据库经验审计，不是竞赛官方文件。所有结论区分 OBSERVED、INFERRED、RECOMMENDED 和 UNKNOWN；推荐值仅用于后续 Word / LaTeX 排版与自动检查的起点。

## 2. 数据来源与分析覆盖

正式身份全集：677 个；通过 G8 初筛并经语义复核保留的正式 Paper PDF：412 个。页面可分析 412 个，字体/文本可靠样本 282 个。OCR 全文运行=0。题目包等语义排除仍保留在全量清单。详见 `derived/format/paper_format_inventory.csv`、`paper_format_observations.csv` 和 `paper_format_summary.csv`。

## 3. 并行任务与语料快照说明

检测到 G8-Q3 及 G8 scale 运行证据在工作区存在/近期更新；其只读运行证据不属于正式语料身份。FORMAT-AUDIT 使用按 Paper、路径和 SHA-256 定义的 corpus-aware snapshot，判定为 `PARALLEL_SAFE_WITH_SNAPSHOT`。

开始/结束语料漂移：identity=0，source SHA=0，path=0，membership=0；`CORPUS_DRIFT=0`，`OPERATIONAL_EVIDENCE_DRIFT_ONLY=1`。

## 4. 页面总体设置

| 项目 | 推荐值 | 数据库主流值 | 样本比例 | 置信度 |
|---|---|---|---:|---|
| 纸张 | A4（PRACTICAL_RECOMMENDATION, n=412, ratio=0.5461, HIGH) | True | 0.5461 | HIGH |
| 页面方向 | PORTRAIT（DATABASE_CONSENSUS, n=412, ratio=1.0, HIGH) | PORTRAIT | 1.0 | HIGH |
| 上边距 | 25.4mm（PRACTICAL_RECOMMENDATION, n=225, ratio=0.3323, HIGH) | median=25.421 mm | - | HIGH |
| 下边距 | 19.5mm（PRACTICAL_RECOMMENDATION, n=225, ratio=0.3323, HIGH) | median=19.526 mm | - | HIGH |
| 左边距 | 25.0mm（PRACTICAL_RECOMMENDATION, n=225, ratio=0.3323, HIGH) | median=25.027 mm | - | HIGH |
| 右边距 | 14.0mm（PRACTICAL_RECOMMENDATION, n=225, ratio=0.3323, HIGH) | median=13.953 mm | - | HIGH |
| 页眉 | 0（DATABASE_CONSENSUS, n=412, ratio=0.6626, HIGH) | 0 | 0.6626 | HIGH |
| 页脚 | 0（RECENT_TREND, n=412, ratio=0.5971, HIGH) | 0 | 0.5971 | HIGH |
| 页码位置 | BOTTOM | BOTTOM | - | MEDIUM |

## 5. 论文标题

推荐：SimSun/Song（DATABASE_CONSENSUS, n=190, ratio=0.8158, HIGH)，15.0pt（PRACTICAL_RECOMMENDATION, n=188, ratio=0.4563, HIGH)，加粗=False，对齐=CENTER。标题识别以首屏位置、文本内容、字号、粗体和上下文综合判断。

## 6. 摘要与关键词

摘要标题：14.0pt（PRACTICAL_RECOMMENDATION, n=114, ratio=0.2767, HIGH)，加粗=False，对齐=CENTER。摘要正文：12.0pt（PRACTICAL_RECOMMENDATION, n=111, ratio=0.2694, HIGH)，行距倍数=1.3，首行缩进=8.5mm。关键词标签：12.0pt（PRACTICAL_RECOMMENDATION, n=142, ratio=0.3447, HIGH)；关键词分隔符和数量属于数据库差异，不设官方硬性值。

## 7. 正文

推荐：SimSun/Song（DATABASE_CONSENSUS, n=201, ratio=0.806, HIGH)，12.0pt（PRACTICAL_RECOMMENDATION, n=200, ratio=0.4854, HIGH)（小四），行距观测中位数=15.8pt、倍数=1.5，首行缩进=11.2mm，对齐=LEFT_OR_MIXED。行距来自 PDF 基线间距估计，不等同于 Word 的单倍/固定值。

## 8. 标题层级

| 层级 | 推荐字号 | 中文字号 | 加粗 | 对齐 | 编号 | 置信度 |
|---|---:|---|---|---|---|---|
| 1 级标题 | 12.0pt | 小四 | False | CENTER | decimal | HIGH |
| 2 级标题 | 12.0pt | 小四 | False | LEFT | bracket | HIGH |
| 3 级标题 | 12.0pt | 小四 | False | LEFT | bracket | HIGH |
| 4 级标题 | 当前数据库证据不足 | 小四 | False | JUSTIFIED_OR_FULL | bracket | LOW |

三级及以下若样本不足，继续使用 UNKNOWN/低置信度，不强行统一。

## 9. 图

图题推荐：12.0pt（PRACTICAL_RECOMMENDATION, n=125, ratio=0.3034, HIGH)，对齐=CENTER，编号格式=caption。图居中和图题位置需结合视觉抽检；当前文本层只对图题行和图像对象做启发式识别。

## 10. 表

表题：12.0pt（PRACTICAL_RECOMMENDATION, n=128, ratio=0.3107, HIGH)，表中文字：当前数据库证据不足（INSUFFICIENT_EVIDENCE, n=0, ratio=0, LOW)。三线表采用率：UNKNOWN；仅凭当前 PDF 文本坐标未可靠取得线条拓扑，不能编造比例。

## 11. 数学公式

公式候选：11.9pt（PRACTICAL_RECOMMENDATION, n=195, ratio=0.4733, HIGH)；公式编号：11.9pt（PRACTICAL_RECOMMENDATION, n=104, ratio=0.2524, HIGH)。公式居中、编号位置及变量斜体当前只能部分启发式识别；公式来源工具（MathType、Word Equation 或 LaTeX）不作断言。

## 12. 参考文献

参考文献标题：14.0pt（PRACTICAL_RECOMMENDATION, n=47, ratio=0.1141, MEDIUM)；条目：12.0pt（PRACTICAL_RECOMMENDATION, n=47, ratio=0.1141, MEDIUM)，编号格式=none。数据库存在 `[1]`、`［1］`、`1.` 等差异，不能宣称全部严格符合 GB/T 7714。

## 13. 附录

附录标题：12.0pt（PRACTICAL_RECOMMENDATION, n=76, ratio=0.1845, HIGH)；正文：11.6pt（PRACTICAL_RECOMMENDATION, n=76, ratio=0.1845, HIGH)；代码：12.0pt（PRACTICAL_RECOMMENDATION, n=61, ratio=0.1481, HIGH)。代码附录不是每篇论文的必备组成部分。

## 14. 页眉、页脚与页码

页眉存在=0（DATABASE_CONSENSUS, n=412, ratio=0.6626, HIGH)；页脚存在=0（RECENT_TREND, n=412, ratio=0.5971, HIGH)；页码存在=0（RECENT_TREND, n=412, ratio=0.5534, HIGH)；位置=BOTTOM。

## 15. 数字、单位与中英文混排

当前 PDF 文本层可识别数字、英文和单位的共现，但字符间距、具体字体映射和单位排版约定证据不足，建议沿用正文/公式的局部风格并在检查器中只做弱提示。

## 16. 不同年份格式变化

按年份的 Paper 数、PDF 数、文本层和字体资格见 `CUMCM_PAPER_FORMAT_EVIDENCE.md` 的年份表。早期样本扫描/图像型比例更高，近期 PDF 字体对象和文本层更常见；这会影响字体统计，不能把可观测性变化直接写成格式趋势。

## 17. 不同题目格式比较

按 A/B/C/D/E 的覆盖统计见证据报告。未把题目类别与主要排版格式的关系写成规律；当前证据不足以支持稳定系统性关联。

## 18. 数据库中常见格式差异

常见差异包括纸张 MediaBox、摘要与关键词是否同段、标题编号层级、图表编号空格、参考文献编号括号、页码是否可见、扫描/文本 PDF 混用以及附录代码排法。异常清单见 `derived/format/format_outliers.csv`。

## 19. 推荐统一排版规范

以下是基于当前数据库主流值与可实现性的 RECOMMENDED 组合，不是官方要求：

- 标题：字体候选 SimSun/Song，字号 15.0pt，行距倍数 当前数据库证据不足，首行缩进 当前数据库证据不足，对齐 CENTER。
- 摘要正文：字体候选 SimSun/Song，字号 12.0pt，行距倍数 1.3，首行缩进 8.5mm，对齐 JUSTIFIED_OR_FULL。
- 一级标题：字体候选 SimSun/Song，字号 12.0pt，行距倍数 1.9，首行缩进 当前数据库证据不足，对齐 CENTER。
- 二级标题：字体候选 SimSun/Song，字号 12.0pt，行距倍数 当前数据库证据不足，首行缩进 当前数据库证据不足，对齐 LEFT。
- 三级标题：字体候选 SimSun/Song，字号 12.0pt，行距倍数 当前数据库证据不足，首行缩进 当前数据库证据不足，对齐 LEFT。
- 正文：字体候选 SimSun/Song，字号 12.0pt，行距倍数 1.5，首行缩进 11.2mm，对齐 LEFT_OR_MIXED。
- 图题：字体候选 SimSun/Song，字号 12.0pt，行距倍数 当前数据库证据不足，首行缩进 当前数据库证据不足，对齐 CENTER。
- 表题：字体候选 SimSun/Song，字号 12.0pt，行距倍数 当前数据库证据不足，首行缩进 当前数据库证据不足，对齐 CENTER。
- 参考文献：字体候选 SimSun/Song，字号 12.0pt，行距倍数 1.3，首行缩进 14.8mm，对齐 LEFT。
- 附录正文：字体候选 SimSun/Song，字号 11.6pt，行距倍数 1.3，首行缩进 13.0mm，对齐 LEFT_OR_MIXED。

## 20. 一页式格式速查表

| 元素 | 推荐速查 |
|---|---|
| 页面 | A4，PORTRAIT，上/下/左/右边距 25.4mm/19.5mm/25.0mm/14.0mm |
| 标题 | SimSun/Song，15.0pt，加粗 False，CENTER |
| 摘要 | 12.0pt，行距倍数 1.3，首行缩进 8.5mm |
| 关键词 | 12.0pt；数量/分隔符按内容清晰度设置 |
| 一级标题 | 12.0pt，False，CENTER |
| 二级标题 | 12.0pt，False，LEFT |
| 三级标题 | 12.0pt，False，LEFT |
| 正文 | SimSun/Song，12.0pt，行距 1.5，首行缩进 11.2mm |
| 图题 | 12.0pt，CENTER |
| 表题 | 12.0pt，CENTER |
| 表格正文 | 当前数据库证据不足；三线表率 UNKNOWN |
| 公式 | LEFT_OR_MIXED；编号 none |
| 参考文献 | 12.0pt，编号 none |
| 附录 | 11.6pt；代码单独使用等宽字体仅在实际代码块成立时 |
| 页码 | BOTTOM |

## 21. Word 排版参数建议

- Layout：A4，PORTRAIT；Margins：上/下/左/右 25.4mm/19.5mm/25.0mm/14.0mm。
- Normal：SimSun/Song，12.0pt，首行缩进 11.2mm，对齐 LEFT_OR_MIXED；行距按观测倍数 1.5 校准。
- Title：SimSun/Song，15.0pt，False，CENTER。
- Heading 1/2/3：分别使用 12.0pt/12.0pt/12.0pt，编号层级保持一致。
- Abstract / Keywords / Caption / Table body / Reference / Appendix：分别参照速查表；三线表、公式变量斜体和字符间距只作人工复核项。
- Header / Footer / Page Number：按数据库识别结果设置；不可识别时保留 UNKNOWN，不强加页眉线。

## 22. LaTeX 排版参数建议

- `geometry`：使用 A4、PORTRAIT、margin=25.4mm（若四边不同则分别设置 top/bottom/left/right）。
- `ctex` / `fontspec`：中文字体使用 SimSun/Song 作为候选，Latin 字体按实际环境可用性选择；PDF 资源未逐字映射时保留人工核验。
- `titlesec`：把 heading 1/2/3 的字号映射为 12.0pt/12.0pt/12.0pt。
- `setspace`：正文行距以观测倍数 1.5 为起点；不要把 PDF 基线距离硬写成官方行距。
- `caption` / `booktabs` / `enumitem` / `fancyhdr`：分别用于图表标题、可选三线表、列表缩进和页眉页脚；具体开关应由视觉 QA 决定。

## 23. 证据强度与尚不能确定的事项

高置信度主要来自大量文本层样本且跨论文一致的页面/字号统计；字体家族、行距语义、三线表拓扑、公式变量斜体、表格线型、Word/LaTeX 来源仍受 PDF 资源映射限制。扫描、字体转轮廓、CIDFont 或编码异常样本不会被 OCR 结果冒充原始字体。

## 附录 A：样本统计

### 按年份

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

### 按题目类别

| 类别 | Paper | PDF | 文本层 | 字体资格 | A4 |
|---|---:|---:|---:|---:|---:|
| A | 229 | 178 | 178 | 117 | 92 |
| B | 200 | 152 | 152 | 111 | 78 |
| C | 100 | 46 | 46 | 31 | 28 |
| D | 134 | 33 | 33 | 23 | 27 |
| E | 14 | 3 | 3 | 0 | 0 |

## 附录 B：异常样本

异常记录 404 条，涉及 398 个 Paper。详细字段、页码和是否排除共识见 `derived/format/format_outliers.csv`。

## 结论逐项回答

1. 纸张：见页面总体设置，A4 仅在实际 MediaBox 统计达到共识时推荐。
2. 页面方向：数据库主流为纵向/推荐值见 JSON。
3. 上边距：采用文本 bounding box 的 Paper 中位数。
4. 下边距：采用文本 bounding box 的 Paper 中位数。
5. 左边距：采用文本 bounding box 的 Paper 中位数。
6. 右边距：采用文本 bounding box 的 Paper 中位数。
7. 标题字体：使用文档级字体候选，逐字映射不足时为 UNKNOWN。
8. 标题字号：见标题推荐。
9. 标题字重：按粗体对象比例统计。
10. 摘要标题：见摘要部分。
11. 摘要正文：见摘要部分。
12. 关键词：标签和正文分开统计，数量/分隔符不作官方硬性规定。
13. 一级标题：见标题层级表。
14. 二级标题：见标题层级表。
15. 三级标题：见标题层级表；低覆盖时保留低置信度。
16. 正文字体：见正文部分；字体家族映射存在限制。
17. 正文字号：见正文部分。
18. 正文行距：提供观测基线距离和倍数，不冒充 Word 行距。
19. 正文首行缩进：来自正文行起点差异估计。
20. 图题排法：编号和样式见图部分，位置需视觉 QA。
21. 图题字体字号：见图部分。
22. 表题排法：见表部分。
23. 表格正文：当前表体字号证据覆盖不足时不强制。
24. 三线表：当前证据不足，标记 UNKNOWN。
25. 公式对齐：启发式识别，无法可靠统一时人工复核。
26. 公式编号：见公式部分。
27. 数学变量斜体：当前证据不足，不强行断言。
28. 参考文献标题：见参考文献部分。
29. 参考文献正文：见参考文献部分。
30. 参考文献缩进：当前 PDF 证据不充分，建议以悬挂缩进作为可读性推荐并人工检查。
31. 附录标题：见附录部分。
32. 附录正文：见附录部分。
33. 代码附录：不是必备组成部分；实际代码可使用等宽字体。
34. 页眉页脚：见页眉、页脚与页码。
35. 页码位置：按边缘数字文本启发式识别。
36. 高度一致做法：页面方向、常规正文层级和基本图表编号较稳定的部分。
37. 明显分歧：扫描/文本 PDF、标题层级、参考文献编号、附录和页眉页脚。
38. 近期变化：近期文本层/字体元数据可观测性增强，不能等同于排版规范变化。
39. 证据不足项目：三线表、公式语义、字符间距、逐字字体映射等。
40. 统一格式：以第 19 节推荐组合为起点，并保留低置信度项目人工确认。

本轮只生成 FORMAT-AUDIT 规定的分析证据与报告；不生成 Word 模板、LaTeX 模板工程或格式检查器。
