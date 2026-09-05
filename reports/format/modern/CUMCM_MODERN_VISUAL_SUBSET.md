# CUMCM Modern Visual Subset

## 1. 研究目的

本阶段专门研究近年优秀论文的实际视觉风格，不使用 G8 method-evidence eligibility 作为格式研究准入条件。Modern 与 Historical 分开统计，官方 2026 规范若无可信来源则保持待补状态。

## 2. 样本确认

- 2024 identities scanned: 5；confirmed excellent-paper PDFs: 0；format eligible: 0。
- 2025 identities scanned: 12；confirmed excellent-paper PDFs: 7；format eligible: 7。
- `MODERN_SAMPLE_SIZE=7`；`MODERN_VISUAL_REVIEW_COVERAGE=1.0`。

## 3. 2024 样本状态

当前数据库中的 2024 A–E 五个 canonical PDF 均为赛题/题目材料，不是真实优秀论文 PDF。因此 `MODERN_2024_CONFIRMED_EXCELLENT_PAPER_COUNT=0`，没有用网络或其它年份论文替代。

## 4. 2025 样本状态

以下 7 篇位于当前项目的获奖论文目录，具有 canonical primary membership、可读 PDF 和可渲染页面；它们全部纳入现代视觉审阅：

- `CUMCM-2025-A-A066`（2025A，86 页，SHA-256 `9C14EAB19304FE45A36E45A965FA740E2636690630ECD8528335D4E4AEC3E2D4`，GOVERNANCE=NOT_IN_G8_STATUS，FORMAT=1）
- `CUMCM-2025-A-A196`（2025A，98 页，SHA-256 `B5FB5FE4B2D06998BC85BB9276CF16AFC1755913D91F18C01D5209F8F13ADA92`，GOVERNANCE=NOT_IN_G8_STATUS，FORMAT=1）
- `CUMCM-2025-B-B060`（2025B，72 页，SHA-256 `17C1B7E255DCBB8E8AC34C0A750E39D7DF1EE4A5ED0D0323B46388F168090330`，GOVERNANCE=NOT_IN_G8_STATUS，FORMAT=1）
- `CUMCM-2025-C-C023`（2025C，122 页，SHA-256 `515FD73059B427606FFD099781A124D34BAC3306BEE87C61D47259622351EB17`，GOVERNANCE=NOT_IN_G8_STATUS，FORMAT=1）
- `CUMCM-2025-C-C132`（2025C，65 页，SHA-256 `08EC307CDC65A673E6838E2E3D00B2337DA414E7891284617E10F370E5F246B5`，GOVERNANCE=NOT_IN_G8_STATUS，FORMAT=1）
- `CUMCM-2025-D-D037`（2025D，37 页，SHA-256 `BDBED46FF5D5841AF82FA6441C8AB3D83A62658672857E445DEADFD8DAD1F0AC`，GOVERNANCE=NOT_IN_G8_STATUS，FORMAT=1）
- `CUMCM-2025-E-E030`（2025E，36 页，SHA-256 `7270DACAB35167E998141D5D34C34D12A912B3620249A892697211F24D009E0D`，GOVERNANCE=NOT_IN_G8_STATUS，FORMAT=1）

这 7 篇的 `FORMAT_OBSERVATION_ELIGIBILITY=1` 独立于 `GOVERNANCE_ELIGIBILITY`；当前均未因 G8 method-evidence 门槛被静默排除。另有 5 个 2025 canonical 题目包已登记但按 `PROBLEM_STATEMENT` 排除。

## 5. 页面整体视觉

已对全部 7 篇执行页面渲染检查，覆盖第一页、摘要区域、典型正文页、标题层级、存在时的图表和公式、参考文献、附录，并补充视觉密集/稀疏页。整体呈正式学术报告式版面：A4 纵向白底、正文栏较窄且外侧留白明显；第一页通常为居中加粗题名、加粗“摘要”、密集中文摘要和页底关键词/页码。正文普遍采用编号式章节层级；抽查页可见居中公式及右侧括号编号、图/表题注和较强的表格上下边线。彩色图、流程图、统计图与代码附录在样本中均可见，代码附录常使用框线并产生较稀疏的末页。各篇的图表密度、公式密度和留白仍有变化，不能从 7 篇样本推出全国普遍率；页面上的“中国大学生在线”斜向水印属于源文件视觉痕迹，不是推荐排版元素。

## 6. 标题

视觉复核显示题名通常居中、加粗并位于第一页上部；摘要标题同样突出。字体外观只能记录为“中文衬线/宋体风格外观（仅视觉）”，精确嵌入字体与字号因 image-based PDF 或字体资源不足仍保留 `UNKNOWN`，不以 OCR 推测。

## 7. 摘要与关键词

摘要/关键词按文本层和渲染页共同核验。关键词的标识、标点和布局在不同 PDF 中需保持“样本观察”语义，不能升级为 2026 官方硬要求。

## 8. 正文

视觉复核显示正文为紧凑的中文学术段落，常见两端对齐外观、首行缩进和单倍至约 1.5 倍的紧凑行距；这些是视觉描述，不是精确 Word 参数。正文中文/西文字体资源、字号仍同时由 PDF text positions 与 embedded font metadata 记录，无法稳定提取的值保留 `UNKNOWN`。

## 9. 标题层级

一级、二级、三级标题按可识别编号/标签记录，具体值按样本汇总。未能稳定识别的层级不补值。

## 10. 图表

图题、表题和表格存在性由文本位置与渲染页共同记录；现代样本多篇可见彩色图/统计图、流程图，以及粗上/下边线的表格。三线表的精确边框语义仍保持 `UNKNOWN_VISUAL_REVIEW_REQUIRED`，不把“看起来像”变成硬事实。

## 11. 数学公式

抽查页可见居中展示公式，右侧通常有括号式编号；公式页与代码附录页之间的视觉密度差异明显。公式及公式编号按可读文本层和页面渲染记录，单一文档的公式识别不等同于公式语义完整解析。

## 12. 参考文献

7 篇均在人工复核范围内确认了参考文献区段（例如 A066 p.33、A196 p.33、B060 p.30、C023 p.24、C132 p.40、D037 p.17、E030 p.21）；条目密度和中英文混排存在篇间差异，具体引用格式不作统一硬断言。

## 13. 附录

7 篇均在人工复核范围内确认附录或代码/支撑材料区段（例如 A066 p.34、A196 p.34、B060 p.36、C023 p.43、C132 p.47、D037 p.18、E030 p.22）；代码页常有框线，末页可能较稀疏。无附录的样本不被视为缺陷。

## 14. 页眉页脚

页码在 7 篇第一页及复核页中均可见于页底中央或相近位置；B060 另可见正文运行页眉。其它页眉/页脚语义按文本位置与渲染页面记录，不在无证据时补齐。

## 15. Historical vs Modern

比较结果分为 `STABLE_TRADITION`、`MODERN_SHIFT`、`MODERN_VARIATION`、`INSUFFICIENT_MODERN_EVIDENCE`，详见 `modern_visual_spec.json`。现代样本单独统计，不回写 Historical consensus。

## 16. Modern Visual Recommendations

Modern 层适合提供“近期视觉起点”：在多篇一致且可复现的字段上作为候选推荐；在样本分歧或字段缺失处回退 Historical，不能把 7 篇样本写成“全国优秀论文普遍”。最终合规层仍由 `OFFICIAL > MODERN > HISTORICAL` 决定。

## 17. 尚不能确定的事项

2026 官方格式规范、页数上限、文件命名与提交规则当前没有项目内可信来源；三线表精确边框、逐字字体映射、现代样本全国普遍率也不从本阶段推断。官方状态：`OFFICIAL_2026_SPEC_AVAILABLE=0`，`OFFICIAL_OVERLAY_STATUS=WAITING_FOR_VERIFIED_OFFICIAL_SPEC`。

## 交付绑定

- Inventory: `derived/format/modern/modern_visual_subset_inventory.csv`
- Observations: `derived/format/modern/modern_visual_observations.csv`
- Summary: `derived/format/modern/modern_visual_summary.csv`
- Modern spec: `derived/format/modern/modern_visual_spec.json`
- Modern snapshot: `derived/format/modern/modern_visual_snapshot.json`
- Final synthesis report: `reports/format/CUMCM_FORMAT_SYNTHESIS_2026.md`
- Final synthesis SSoT: `derived/format/cumcm_format_synthesis_2026.json`
