# G11 Post-Repair Human Rereview Overview

All rows below are prepared for human review and remain `PENDING`. No automatic severity is asserted.

| # | paper_id | original MAJOR summary | repair route | repaired page count | packet | status |
|---:|---|---|---|---:|---|---|
| 1 | CUMCM-2020-D-003 | 长篇OCR样本首/中/末页均存在并与源页面主题一致，未见明显页序错乱或末尾截断；正文和代码主体可辨，但中后部代码/符号存在局部OCR误识别。关键变量、坐标或运算符部分被改写并影响模型含义。 | Q3_SELECTIVE_PAGE_OCR_REPAIR | 3 | `reports/scale/g11_post_repair_human_rereview/01_CUMCM-2020-D-003` | PENDING |
| 2 | CUMCM-1999-B-003 | 源页面明显包含实质正文、图形/数学内容，但三个artifact excerpt基本只剩# Extracted Paper和source_page页标记，没有对应正文文本。按G11“重要章节/大段内容缺失”定义，回查该governed-duplicate artifact的正文生成/绑定是否为空。 | DOC_EXISTING_EXTRACTION_RECONSTRUCTION;MARKER_ONLY_DIAGNOSTIC_OCR_REUSE | 3 | `reports/scale/g11_post_repair_human_rereview/02_CUMCM-1999-B-003` | PENDING |
| 3 | CUMCM-2008-C-004 | 源页面包含连续正文和公式/模型内容，但artifact excerpt仅有页码标记，未提供对应正文，存在明显实质内容缺失。建议检查formal artifact是否生成了空正文。 | DOC_EXISTING_EXTRACTION_RECONSTRUCTION;MARKER_ONLY_DIAGNOSTIC_OCR_REUSE | 3 | `reports/scale/g11_post_repair_human_rereview/03_CUMCM-2008-C-004` | PENDING |
| 4 | CUMCM-1992-A-003 | 源页面有连续正文和大量公式，但artifact excerpt只包含source_page标记，没有实际论文文本。属于明显大段内容缺失，建议回查formal artifact正文是否为空。 | DOC_EXISTING_EXTRACTION_RECONSTRUCTION;MARKER_ONLY_DIAGNOSTIC_OCR_REUSE | 3 | `reports/scale/g11_post_repair_human_rereview/04_CUMCM-1992-A-003` | PENDING |
| 5 | CUMCM-1993-B-001 | 源页面可见正文和表格/排名数据，但artifact excerpt仅有页码标记，实际正文为空，无法完成内容连续性、文字可读性和表格内容核验。 | DOC_EXISTING_EXTRACTION_RECONSTRUCTION | 2 | `reports/scale/g11_post_repair_human_rereview/05_CUMCM-1993-B-001` | PENDING |
| 6 | CUMCM-1996-B-001 | 源页面包含完整正文与公式，但artifact excerpt没有对应文本，仅保留source_page标记。属于实质正文缺失，而非轻微OCR错误。 | DOC_EXISTING_EXTRACTION_RECONSTRUCTION;MARKER_ONLY_DIAGNOSTIC_OCR_REUSE | 3 | `reports/scale/g11_post_repair_human_rereview/06_CUMCM-1996-B-001` | PENDING |
| 7 | CUMCM-1997-A-008 | 源页面包含正文和数学公式，artifact excerpt基本为空，仅有source_page标记；抽样内容无法在formal artifact中找到对应文本。 | DOC_EXISTING_EXTRACTION_RECONSTRUCTION;MARKER_ONLY_DIAGNOSTIC_OCR_REUSE | 3 | `reports/scale/g11_post_repair_human_rereview/07_CUMCM-1997-A-008` | PENDING |
| 8 | CUMCM-1998-A-007 | 源页面可见正文、公式及数据表，而artifact excerpt只有页标记、没有实质文本，存在明显正文/表格内容缺失。 | DOC_EXISTING_EXTRACTION_RECONSTRUCTION;MARKER_ONLY_DIAGNOSTIC_OCR_REUSE | 3 | `reports/scale/g11_post_repair_human_rereview/08_CUMCM-1998-A-007` | PENDING |
| 9 | CUMCM-2000-A-005 | DNA分类论文源页面包含正文、流程图和公式，但artifact excerpt仅有source_page标记，没有对应正文，属于明显内容缺失。 | DOC_EXISTING_EXTRACTION_RECONSTRUCTION;MARKER_ONLY_DIAGNOSTIC_OCR_REUSE | 3 | `reports/scale/g11_post_repair_human_rereview/09_CUMCM-2000-A-005` | PENDING |
| 10 | CUMCM-2001-A-001 | 源页面包含正文、图形及英文尾页内容，但artifact excerpt没有实际论文文本，仅有页标记，按G11标准属于material missing section。 | DOC_EXISTING_EXTRACTION_RECONSTRUCTION;MARKER_ONLY_DIAGNOSTIC_OCR_REUSE | 3 | `reports/scale/g11_post_repair_human_rereview/10_CUMCM-2001-A-001` | PENDING |
| 11 | CUMCM-2002-B-005 | 源页面包含彩票模型正文和公式，artifact excerpt只保留页标记、没有实质文本，存在明显大段正文缺失。 | DOC_EXISTING_EXTRACTION_RECONSTRUCTION;MARKER_ONLY_DIAGNOSTIC_OCR_REUSE | 3 | `reports/scale/g11_post_repair_human_rereview/11_CUMCM-2002-B-005` | PENDING |

Start with the individual `REVIEW.md` packet. `before_after.md` provides the historical-to-current evidence comparison, and `current_formal_p<N>.md` contains the current formal excerpt used by that packet.

## Source Image Status

The source images below are ready for human inspection. This does not change the human decision status, which remains `PENDING`.

- `CUMCM-2020-D-003`: `SOURCE_IMAGE_STATUS=READY`; units=3; status=`PENDING`.
- `CUMCM-1999-B-003`: `SOURCE_IMAGE_STATUS=READY`; units=3; status=`PENDING`.
- `CUMCM-2008-C-004`: `SOURCE_IMAGE_STATUS=READY`; units=3; status=`PENDING`.
- `CUMCM-1992-A-003`: `SOURCE_IMAGE_STATUS=READY`; units=3; status=`PENDING`.
- `CUMCM-1993-B-001`: `SOURCE_IMAGE_STATUS=READY`; units=3; status=`PENDING`.
- `CUMCM-1996-B-001`: `SOURCE_IMAGE_STATUS=READY`; units=3; status=`PENDING`.
- `CUMCM-1997-A-008`: `SOURCE_IMAGE_STATUS=READY`; units=3; status=`PENDING`.
- `CUMCM-1998-A-007`: `SOURCE_IMAGE_STATUS=READY`; units=3; status=`PENDING`.
- `CUMCM-2000-A-005`: `SOURCE_IMAGE_STATUS=READY`; units=3; status=`PENDING`.
- `CUMCM-2001-A-001`: `SOURCE_IMAGE_STATUS=READY`; units=3; status=`PENDING`.
- `CUMCM-2002-B-005`: `SOURCE_IMAGE_STATUS=READY`; units=3; status=`PENDING`.
