# CUMCM 论文格式分层证据与 2026 推荐规范

## 1. 证据体系

### 1.1 Historical Format Audit

Historical Format Audit 已冻结并保持 `STATUS=PASS`。本阶段只读引用其历史汇总，不重跑 677 篇、不修改历史 observations，也不把现代样本混入 Historical consensus。

### 1.2 Modern CUMCM Visual Subset

Modern 层使用当前项目内可确认、可读取的近年优秀论文 PDF，独立于 G8 method-evidence eligibility。现代样本仅代表当前数据库可确认的近期视觉证据，不是全国普遍性结论。

### 1.3 2026 Official Specification

`OFFICIAL_2026_SPEC_AVAILABLE=0`；`OFFICIAL_OVERLAY_STATUS=WAITING_FOR_VERIFIED_OFFICIAL_SPEC`。当前项目没有被验证为 2026 CUMCM 官方格式规范的本地文件；未联网补齐，也未把论文实物或非官方文档升级为官方要求。

## 2. 样本覆盖

- 2024 candidate identities scanned: **5**；confirmed excellent papers: **0**；format eligible: **0**。当前 2024 条目均为赛题 PDF，不能作为优秀论文视觉样本。
- 2025 candidate identities scanned: **12**；confirmed excellent papers: **7**；format eligible: **7**。另有 5 份 2025 题目包被排除。
- Modern Visual Subset sample size: **7**；visual review coverage: **7/7**。
- Problem-statement exclusions: **10**；source missing: **0**；PDF unreadable/unrenderable: **0**。

### 2025 逐篇准入记录

- `CUMCM-2025-A-A066`（2025A，86 页，SHA-256 `9C14EAB19304FE45A36E45A965FA740E2636690630ECD8528335D4E4AEC3E2D4`，GOVERNANCE=NOT_IN_G8_STATUS，FORMAT=1）
- `CUMCM-2025-A-A196`（2025A，98 页，SHA-256 `B5FB5FE4B2D06998BC85BB9276CF16AFC1755913D91F18C01D5209F8F13ADA92`，GOVERNANCE=NOT_IN_G8_STATUS，FORMAT=1）
- `CUMCM-2025-B-B060`（2025B，72 页，SHA-256 `17C1B7E255DCBB8E8AC34C0A750E39D7DF1EE4A5ED0D0323B46388F168090330`，GOVERNANCE=NOT_IN_G8_STATUS，FORMAT=1）
- `CUMCM-2025-C-C023`（2025C，122 页，SHA-256 `515FD73059B427606FFD099781A124D34BAC3306BEE87C61D47259622351EB17`，GOVERNANCE=NOT_IN_G8_STATUS，FORMAT=1）
- `CUMCM-2025-C-C132`（2025C，65 页，SHA-256 `08EC307CDC65A673E6838E2E3D00B2337DA414E7891284617E10F370E5F246B5`，GOVERNANCE=NOT_IN_G8_STATUS，FORMAT=1）
- `CUMCM-2025-D-D037`（2025D，37 页，SHA-256 `BDBED46FF5D5841AF82FA6441C8AB3D83A62658672857E445DEADFD8DAD1F0AC`，GOVERNANCE=NOT_IN_G8_STATUS，FORMAT=1）
- `CUMCM-2025-E-E030`（2025E，36 页，SHA-256 `7270DACAB35167E998141D5D34C34D12A912B3620249A892697211F24D009E0D`，GOVERNANCE=NOT_IN_G8_STATUS，FORMAT=1）

## 3. 长期稳定传统

Historical 层继续承担长期传统：A4/纵向页面、宋体/Times 组合、中文论文的摘要—正文—标题层级、图表/公式/参考文献等结构化组织。最终数值以冻结 Historical artifacts 为准。

## 4. 2024–2025 现代视觉趋势

当前 7 篇 2025 样本均完成渲染检查：第一页、摘要区域、典型正文页、标题层级页，以及存在时的图表、公式、参考文献、附录页，并补充密集/稀疏页面。总体可表述为“正式学术报告式的页面组织，具体图表、公式密度和留白存在篇间差异”；不能据此声称全国优秀论文的普遍比例。

## 5. 2026 官方要求

官方覆盖保持 `PENDING`。一旦获得来源可验证的 2026 官方文件，应逐项提取页面、字体、字号、图表、公式、参考文献、附录、页数、命名和提交格式，并按 `OFFICIAL_HARD_REQUIREMENT` / `OFFICIAL_GUIDANCE` 分开记录。

## 6. Historical 与 Modern 差异

本阶段将两层分开统计。比较分类计数：`STABLE_TRADITION=1`，`MODERN_SHIFT=0`，`MODERN_VARIATION=13`，`INSUFFICIENT_MODERN_EVIDENCE=10`。现代样本没有被历史大样本稀释；分类仅描述证据关系，不是官方合规结论。

## 7. Modern 与 Official 差异

没有可验证的 2026 官方值，因此不生成“现代不合规”判断；所有 official comparison 保持 `PENDING`。

## 8. 已被 2026 规范覆盖的历史做法

当前无可验证的 2026 official specification，故没有可列的 superseded practice。

## 9. 最终推荐规范

融合顺序固定为 `OFFICIAL > MODERN > HISTORICAL`。当前 official 缺失时，清晰且一致的现代观察可进入候选推荐；现代证据不足时回退 Historical；两层都不足则保留 `INSUFFICIENT_EVIDENCE`，不补造数值。

## 10. 一页式格式速查表

| 元素 | 最终推荐 | 证据来源 | Historical | Modern | 2026 Official | 优先级原因 | 置信度 |
|---|---|---|---|---|---|---|---|
| 页面尺寸 | A4 | MODERN | UNKNOWN | A4 | PENDING | No verified 2026 official value is available; modern sample is the newest direct visual evidence. | MEDIUM |
| 上边距 | INSUFFICIENT_EVIDENCE | NONE | UNKNOWN | INSUFFICIENT_MODERN_EVIDENCE | PENDING | No evidence layer supports a value. | LOW |
| 下边距 | INSUFFICIENT_EVIDENCE | NONE | UNKNOWN | INSUFFICIENT_MODERN_EVIDENCE | PENDING | No evidence layer supports a value. | LOW |
| 左边距 | INSUFFICIENT_EVIDENCE | NONE | UNKNOWN | INSUFFICIENT_MODERN_EVIDENCE | PENDING | No evidence layer supports a value. | LOW |
| 右边距 | INSUFFICIENT_EVIDENCE | NONE | UNKNOWN | INSUFFICIENT_MODERN_EVIDENCE | PENDING | No evidence layer supports a value. | LOW |
| 标题字体 | Chinese serif/Song-style appearance (visual only) | MODERN | SimSun/Song | Chinese serif/Song-style appearance (visual only) | PENDING | No verified 2026 official value is available; modern sample is the newest direct visual evidence. | MEDIUM |
| 标题字号 | 15.0 | HISTORICAL | 15.0 | INSUFFICIENT_MODERN_EVIDENCE | PENDING | Modern evidence is insufficient; retain the frozen historical evidence layer. | LOW |
| 摘要 | Chinese serif/Song-style appearance (visual only) | MODERN | SimSun/Song | Chinese serif/Song-style appearance (visual only) | PENDING | No verified 2026 official value is available; modern sample is the newest direct visual evidence. | MEDIUM |
| 关键词 | PRESENT_WHERE_EXTRACTED | MODERN | UNKNOWN | PRESENT_WHERE_EXTRACTED | PENDING | No verified 2026 official value is available; modern sample is the newest direct visual evidence. | LOW |
| 一级标题 | 15.0 | HISTORICAL | 15.0 | INSUFFICIENT_MODERN_EVIDENCE | PENDING | Modern evidence is insufficient; retain the frozen historical evidence layer. | LOW |
| 二级标题 | 15.0 | HISTORICAL | 15.0 | INSUFFICIENT_MODERN_EVIDENCE | PENDING | Modern evidence is insufficient; retain the frozen historical evidence layer. | LOW |
| 三级标题 | 15.0 | HISTORICAL | 15.0 | INSUFFICIENT_MODERN_EVIDENCE | PENDING | Modern evidence is insufficient; retain the frozen historical evidence layer. | LOW |
| 正文中文字体 | Chinese serif/Song-style appearance (visual only) | MODERN | SimSun/Song | Chinese serif/Song-style appearance (visual only) | PENDING | No verified 2026 official value is available; modern sample is the newest direct visual evidence. | MEDIUM |
| 正文西文字体 | INSUFFICIENT_EVIDENCE | NONE | INSUFFICIENT_EVIDENCE | INSUFFICIENT_MODERN_EVIDENCE | PENDING | No evidence layer supports a value. | MEDIUM |
| 正文字号 | 15.0 | HISTORICAL | 15.0 | INSUFFICIENT_MODERN_EVIDENCE | PENDING | Modern evidence is insufficient; retain the frozen historical evidence layer. | LOW |
| 行距 | COMPACT_SINGLE_TO_1_5_LIKE | MODERN | UNKNOWN | COMPACT_SINGLE_TO_1_5_LIKE | PENDING | No verified 2026 official value is available; modern sample is the newest direct visual evidence. | MEDIUM |
| 首行缩进 | VISIBLE_FIRST_LINE_INDENT | MODERN | UNKNOWN | VISIBLE_FIRST_LINE_INDENT | PENDING | No verified 2026 official value is available; modern sample is the newest direct visual evidence. | MEDIUM |
| 图题 | PRESENT | MODERN | UNKNOWN | PRESENT | PENDING | No verified 2026 official value is available; modern sample is the newest direct visual evidence. | MEDIUM |
| 表题 | PRESENT | MODERN | UNKNOWN | PRESENT | PENDING | No verified 2026 official value is available; modern sample is the newest direct visual evidence. | MEDIUM |
| 表正文 | BOLD_TOP_BOTTOM_RULES_OBSERVED | MODERN | UNKNOWN | BOLD_TOP_BOTTOM_RULES_OBSERVED | PENDING | No verified 2026 official value is available; modern sample is the newest direct visual evidence. | MEDIUM |
| 公式 | PRESENT | MODERN | UNKNOWN | PRESENT | PENDING | No verified 2026 official value is available; modern sample is the newest direct visual evidence. | MEDIUM |
| 公式编号 | PRESENT | MODERN | UNKNOWN | PRESENT | PENDING | No verified 2026 official value is available; modern sample is the newest direct visual evidence. | MEDIUM |
| 参考文献 | PRESENT | MODERN | UNKNOWN | PRESENT | PENDING | No verified 2026 official value is available; modern sample is the newest direct visual evidence. | MEDIUM |
| 附录 | PRESENT | MODERN | UNKNOWN | PRESENT | PENDING | No verified 2026 official value is available; modern sample is the newest direct visual evidence. | MEDIUM |
| 页眉 | INSUFFICIENT_EVIDENCE | NONE | UNKNOWN | INSUFFICIENT_MODERN_EVIDENCE | PENDING | No evidence layer supports a value. | MEDIUM |
| 页脚 | INSUFFICIENT_EVIDENCE | NONE | UNKNOWN | INSUFFICIENT_MODERN_EVIDENCE | PENDING | No evidence layer supports a value. | MEDIUM |
| 页码 | PRESENT_BOTTOM_CENTERED | MODERN | UNKNOWN | PRESENT_BOTTOM_CENTERED | PENDING | No verified 2026 official value is available; modern sample is the newest direct visual evidence. | MEDIUM |

## 11. Word 参数建议

当前只能将 Modern/Historical 观察作为候选起点：页面尺寸、边距、正文/标题层级、图表题注、公式与参考文献应采用可复现的样式定义。待官方文件出现后再锁定硬参数；不要把单篇论文的排版直接当模板。

## 12. LaTeX 参数建议

建议将页面、中文字体、英文字体、标题层级、摘要、图表题注、公式编号、参考文献和附录全部参数化，并让模板读取 `derived/format/cumcm_format_synthesis_2026.json`。当前 JSON 中 official 值仍为 `PENDING`。

## 13. 格式检查器规则优先级

1. 官方明确硬要求；2. 官方指导性要求；3. Modern 层稳定观察；4. Historical 层长期传统；5. 信息不足时只报警，不强行自动纠正。治理字段、G8 状态和格式观察资格不得混用。

## 14. 尚不能确定事项

2026 官方提交规则、页数上限、文件命名、精确三线表边框、逐字字体映射、现代样本的全国普遍率仍不能从当前证据确定。

SSoT: `derived/format/cumcm_format_synthesis_2026.json`
