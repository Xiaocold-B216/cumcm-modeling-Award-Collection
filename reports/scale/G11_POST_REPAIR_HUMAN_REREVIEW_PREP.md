# G11 Post-Repair Human Rereview Preparation

Stage status: `PARTIAL`; preparation status: `PASS`; human rereview status: `PENDING`.

## Scope and reason

Only the 11 original G11 MAJOR identities require post-repair human rereview because the repaired content must be judged against the exact historical reasons that caused those MAJOR findings. The 246 repair targets are not a new human-review population; 235 of them were never original G11 MAJOR findings, and sending them all to review would change the approved scope.

## Original findings retained

1. `CUMCM-2020-D-003` — `TRUE_CONTENT_QUALITY_MAJOR` — 长篇OCR样本首/中/末页均存在并与源页面主题一致，未见明显页序错乱或末尾截断；正文和代码主体可辨，但中后部代码/符号存在局部OCR误识别。关键变量、坐标或运算符部分被改写并影响模型含义。
   - Repaired pages: `1;68;135`; route: `Q3_SELECTIVE_PAGE_OCR_REPAIR`; packet: `reports/scale/g11_post_repair_human_rereview/01_CUMCM-2020-D-003`.
2. `CUMCM-1999-B-003` — `FORMAL_ARTIFACT_PAGE_CONTENT_MISSING` — 源页面明显包含实质正文、图形/数学内容，但三个artifact excerpt基本只剩# Extracted Paper和source_page页标记，没有对应正文文本。按G11“重要章节/大段内容缺失”定义，回查该governed-duplicate artifact的正文生成/绑定是否为空。
   - Repaired pages: `1;2;3;4;5;6`; route: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION;MARKER_ONLY_DIAGNOSTIC_OCR_REUSE`; packet: `reports/scale/g11_post_repair_human_rereview/02_CUMCM-1999-B-003`.
3. `CUMCM-2008-C-004` — `FORMAL_ARTIFACT_PAGE_CONTENT_MISSING` — 源页面包含连续正文和公式/模型内容，但artifact excerpt仅有页码标记，未提供对应正文，存在明显实质内容缺失。建议检查formal artifact是否生成了空正文。
   - Repaired pages: `1;2;3;4;5;6;7;8;9;10;11;12;13;14`; route: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION;MARKER_ONLY_DIAGNOSTIC_OCR_REUSE`; packet: `reports/scale/g11_post_repair_human_rereview/03_CUMCM-2008-C-004`.
4. `CUMCM-1992-A-003` — `FORMAL_ARTIFACT_PAGE_CONTENT_MISSING` — 源页面有连续正文和大量公式，但artifact excerpt只包含source_page标记，没有实际论文文本。属于明显大段内容缺失，建议回查formal artifact正文是否为空。
   - Repaired pages: `1;2;3;4;5`; route: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION;MARKER_ONLY_DIAGNOSTIC_OCR_REUSE`; packet: `reports/scale/g11_post_repair_human_rereview/04_CUMCM-1992-A-003`.
5. `CUMCM-1993-B-001` — `FORMAL_ARTIFACT_PAGE_CONTENT_MISSING` — 源页面可见正文和表格/排名数据，但artifact excerpt仅有页码标记，实际正文为空，无法完成内容连续性、文字可读性和表格内容核验。
   - Repaired pages: `1;2`; route: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION`; packet: `reports/scale/g11_post_repair_human_rereview/05_CUMCM-1993-B-001`.
6. `CUMCM-1996-B-001` — `FORMAL_ARTIFACT_PAGE_CONTENT_MISSING` — 源页面包含完整正文与公式，但artifact excerpt没有对应文本，仅保留source_page标记。属于实质正文缺失，而非轻微OCR错误。
   - Repaired pages: `1;2;3;4;5`; route: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION;MARKER_ONLY_DIAGNOSTIC_OCR_REUSE`; packet: `reports/scale/g11_post_repair_human_rereview/06_CUMCM-1996-B-001`.
7. `CUMCM-1997-A-008` — `FORMAL_ARTIFACT_PAGE_CONTENT_MISSING` — 源页面包含正文和数学公式，artifact excerpt基本为空，仅有source_page标记；抽样内容无法在formal artifact中找到对应文本。
   - Repaired pages: `1;2;3;4;5`; route: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION;MARKER_ONLY_DIAGNOSTIC_OCR_REUSE`; packet: `reports/scale/g11_post_repair_human_rereview/07_CUMCM-1997-A-008`.
8. `CUMCM-1998-A-007` — `FORMAL_ARTIFACT_PAGE_CONTENT_MISSING` — 源页面可见正文、公式及数据表，而artifact excerpt只有页标记、没有实质文本，存在明显正文/表格内容缺失。
   - Repaired pages: `1;2;3;4;5`; route: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION;MARKER_ONLY_DIAGNOSTIC_OCR_REUSE`; packet: `reports/scale/g11_post_repair_human_rereview/08_CUMCM-1998-A-007`.
9. `CUMCM-2000-A-005` — `FORMAL_ARTIFACT_PAGE_CONTENT_MISSING` — DNA分类论文源页面包含正文、流程图和公式，但artifact excerpt仅有source_page标记，没有对应正文，属于明显内容缺失。
   - Repaired pages: `1;2;3;4;5;6;7;8;9`; route: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION;MARKER_ONLY_DIAGNOSTIC_OCR_REUSE`; packet: `reports/scale/g11_post_repair_human_rereview/09_CUMCM-2000-A-005`.
10. `CUMCM-2001-A-001` — `FORMAL_ARTIFACT_PAGE_CONTENT_MISSING` — 源页面包含正文、图形及英文尾页内容，但artifact excerpt没有实际论文文本，仅有页标记，按G11标准属于material missing section。
   - Repaired pages: `1;2;3;4;5;6`; route: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION;MARKER_ONLY_DIAGNOSTIC_OCR_REUSE`; packet: `reports/scale/g11_post_repair_human_rereview/10_CUMCM-2001-A-001`.
11. `CUMCM-2002-B-005` — `FORMAL_ARTIFACT_PAGE_CONTENT_MISSING` — 源页面包含彩票模型正文和公式，artifact excerpt只保留页标记、没有实质文本，存在明显大段正文缺失。
   - Repaired pages: `1;2;3;4;5;6;7`; route: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION;MARKER_ONLY_DIAGNOSTIC_OCR_REUSE`; packet: `reports/scale/g11_post_repair_human_rereview/11_CUMCM-2002-B-005`.

The 10 marker-route findings are content-missing formal page segments and are bound to current marker-bounded excerpts plus persisted repair evidence. CUMCM-2020-D-003 is the separate `TRUE_CONTENT_QUALITY_MAJOR` Q3 case and is bound to pages 1, 68, and 135, its existing page text, current `paper.md` anchor windows, and Q3 repair provenance.

## Packet organization

Each identity has one `REVIEW.md`, one `before_after.md`, and one `current_formal_p<N>.md` for each unique repaired source page needed by its original Page A/B/C units. The new decision sheet has one identity-level row per target and all rows are PENDING. The original decision sheet is kept as historical authoritative evidence and was not edited.

## Decision rules

The reviewer should decide PASS, MINOR, MAJOR, or CRITICAL using the original G11 contract. MINOR is acceptable for final closure when the original material issue is resolved, but its residual issue must be recorded. Codex does not convert G10 PASS or a programmatic repair pass into a human severity decision.

## Why G11 remains PARTIAL

The evidence packets are prepared, but no human has yet completed the post-repair decisions. Therefore G11 remains PARTIAL and the next stage is `G11-POST-REPAIR-HUMAN-REREVIEW-APPROVAL`.

## Frozen-operation record

This stage used only already persisted evidence. No OCR, rendering, extraction, repair, artifact regeneration/promotion, G9/G10/G12 execution, Word, network, dependency installation, or Git operation was performed.
