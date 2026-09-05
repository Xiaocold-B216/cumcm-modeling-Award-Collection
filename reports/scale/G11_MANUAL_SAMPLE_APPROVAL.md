# G11 Manual Sample Approval

## Decision

- Stage: `G11-MANUAL-SAMPLE-APPROVAL`
- Approval attempt: `20260904T105045672931_d5ec76b6`
- Status: `BLOCKED`
- Manual review status: `FAIL`
- Blocker: `G11_APPROVAL_BASELINE_DRIFT`
- Recommended reentry: `G11-MANUAL-SAMPLE-PREPARATION-RECONCILE`
- G12 readiness: `NOT_READY`

## Baseline and provenance

- Branch: `library-refactor-v1` (match=`1`; expected `library-refactor-v1`)
- HEAD: `557724fba6572d4d83dc421feda5b17b13ff8d66` (match=`1`; expected `557724fba6572d4d83dc421feda5b17b13ff8d66`)
- G10 attempt: `20260903T163405347299_d23183f1` (expected `20260903T163405347299_d23183f1`)
- G10 baseline checks: `1`
- Source G11 attempt expected: `20260903T171602418687_17165c0c`
- Source G11 attempt recorded: `20260903T172404115633_3c748bc1`
- Source G11 attempt match: `0`

## Sampling and completion

- Fingerprint: `677898FA2C0DE5B8229AC310566A2D0A41465790B5F188320CD2EE46C877D4EF`
- Fingerprint match: `1`
- Sample identities: `30`; unique: `30`
- Decision rows: `30`; unique paper IDs: `30`
- Manifest/decision identity set match: `1`
- Reviewed: `30`; pending: `0`
- Dimension-incomplete rows: `0`
- Precheck all PASS: `1`

## Severity aggregation

- PASS: `2`
- MINOR: `17`
- MAJOR: `11`
- CRITICAL: `0`
- Sum check: `1`
- MINOR affected IDs: `CUMCM-2020-B-005;CUMCM-2020-B-002;CUMCM-2010-A-006;CUMCM-2010-B-001;CUMCM-1992-A-004;CUMCM-1993-B-002;CUMCM-1995-B-004;CUMCM-1996-B-002;CUMCM-1997-B-001;CUMCM-1998-A-004;CUMCM-2002-A-014;CUMCM-2011-D-001;CUMCM-2012-D-001;CUMCM-2014-D-003;CUMCM-2012-B-007;CUMCM-2022-E-E014;CUMCM-2021-C-C085`
- MAJOR affected IDs: `CUMCM-2020-D-003;CUMCM-1999-B-003;CUMCM-2008-C-004;CUMCM-1992-A-003;CUMCM-1993-B-001;CUMCM-1996-B-001;CUMCM-1997-A-008;CUMCM-1998-A-007;CUMCM-2000-A-005;CUMCM-2001-A-001;CUMCM-2002-B-005`
- CRITICAL affected IDs: `NONE`
- MAJOR categories: `continuity_status;end_matter_status;math_content_status;ocr_fidelity_status;table_status;text_legibility_status`

## Risk-case results

- `CUMCM-2020-B-005`: reviewed=`1`, severity=`MINOR`, explicit page 23 extra review=`0`.
- `CUMCM-2020-B-002`: reviewed=`1`, severity=`MINOR`.
- Governed duplicate reviewed count: `10`.
- Multi-membership reviewed count: `2`.
- Verified blank reviewed count: `2`.

## MAJOR / CRITICAL findings

- `CUMCM-2020-D-003` | severity=`MAJOR` | stratum=`Q3_OCR_DERIVED` | packet pages=`1,68,135` | dimensions=`text_legibility_status,ocr_fidelity_status,math_content_status` | likely layer=`G8-FORMAL-ARTIFACT-BODY-REPAIR`
  reviewer_comment: 长篇OCR样本首/中/末页均存在并与源页面主题一致，未见明显页序错乱或末尾截断；正文和代码主体可辨，但中后部代码/符号存在局部OCR误识别。关键变量、坐标或运算符部分被改写并影响模型含义。
- `CUMCM-1999-B-003` | severity=`MAJOR` | stratum=`OTHER_FORMAL_DERIVED` | packet pages=`1,3,6` | dimensions=`continuity_status,text_legibility_status,ocr_fidelity_status,math_content_status,table_status,end_matter_status` | likely layer=`G8-FORMAL-ARTIFACT-BODY-REPAIR`
  reviewer_comment: 源页面明显包含实质正文、图形/数学内容，但三个artifact excerpt基本只剩# Extracted Paper和source_page页标记，没有对应正文文本。按G11“重要章节/大段内容缺失”定义，回查该governed-duplicate artifact的正文生成/绑定是否为空。
- `CUMCM-2008-C-004` | severity=`MAJOR` | stratum=`OTHER_FORMAL_DERIVED` | packet pages=`1,7,14` | dimensions=`continuity_status,text_legibility_status,ocr_fidelity_status,math_content_status,end_matter_status` | likely layer=`G8-FORMAL-ARTIFACT-BODY-REPAIR`
  reviewer_comment: 源页面包含连续正文和公式/模型内容，但artifact excerpt仅有页码标记，未提供对应正文，存在明显实质内容缺失。建议检查formal artifact是否生成了空正文。
- `CUMCM-1992-A-003` | severity=`MAJOR` | stratum=`OTHER_FORMAL_DERIVED` | packet pages=`1,3,5` | dimensions=`continuity_status,text_legibility_status,ocr_fidelity_status,math_content_status,end_matter_status` | likely layer=`G8-FORMAL-ARTIFACT-BODY-REPAIR`
  reviewer_comment: 源页面有连续正文和大量公式，但artifact excerpt只包含source_page标记，没有实际论文文本。属于明显大段内容缺失，建议回查formal artifact正文是否为空。
- `CUMCM-1993-B-001` | severity=`MAJOR` | stratum=`OTHER_FORMAL_DERIVED` | packet pages=`1,1,2` | dimensions=`continuity_status,text_legibility_status,ocr_fidelity_status,math_content_status,table_status,end_matter_status` | likely layer=`G8-FORMAL-ARTIFACT-BODY-REPAIR`
  reviewer_comment: 源页面可见正文和表格/排名数据，但artifact excerpt仅有页码标记，实际正文为空，无法完成内容连续性、文字可读性和表格内容核验。
- `CUMCM-1996-B-001` | severity=`MAJOR` | stratum=`OTHER_FORMAL_DERIVED` | packet pages=`1,3,5` | dimensions=`continuity_status,text_legibility_status,ocr_fidelity_status,math_content_status,end_matter_status` | likely layer=`G8-FORMAL-ARTIFACT-BODY-REPAIR`
  reviewer_comment: 源页面包含完整正文与公式，但artifact excerpt没有对应文本，仅保留source_page标记。属于实质正文缺失，而非轻微OCR错误。
- `CUMCM-1997-A-008` | severity=`MAJOR` | stratum=`OTHER_FORMAL_DERIVED` | packet pages=`1,3,5` | dimensions=`continuity_status,text_legibility_status,ocr_fidelity_status,math_content_status,end_matter_status` | likely layer=`G8-FORMAL-ARTIFACT-BODY-REPAIR`
  reviewer_comment: 源页面包含正文和数学公式，artifact excerpt基本为空，仅有source_page标记；抽样内容无法在formal artifact中找到对应文本。
- `CUMCM-1998-A-007` | severity=`MAJOR` | stratum=`OTHER_FORMAL_DERIVED` | packet pages=`1,3,5` | dimensions=`continuity_status,text_legibility_status,ocr_fidelity_status,math_content_status,table_status,end_matter_status` | likely layer=`G8-FORMAL-ARTIFACT-BODY-REPAIR`
  reviewer_comment: 源页面可见正文、公式及数据表，而artifact excerpt只有页标记、没有实质文本，存在明显正文/表格内容缺失。
- `CUMCM-2000-A-005` | severity=`MAJOR` | stratum=`OTHER_FORMAL_DERIVED` | packet pages=`1,5,9` | dimensions=`continuity_status,text_legibility_status,ocr_fidelity_status,math_content_status,end_matter_status` | likely layer=`G8-FORMAL-ARTIFACT-BODY-REPAIR`
  reviewer_comment: DNA分类论文源页面包含正文、流程图和公式，但artifact excerpt仅有source_page标记，没有对应正文，属于明显内容缺失。
- `CUMCM-2001-A-001` | severity=`MAJOR` | stratum=`OTHER_FORMAL_DERIVED` | packet pages=`1,3,6` | dimensions=`continuity_status,text_legibility_status,ocr_fidelity_status,math_content_status,end_matter_status` | likely layer=`G8-FORMAL-ARTIFACT-BODY-REPAIR`
  reviewer_comment: 源页面包含正文、图形及英文尾页内容，但artifact excerpt没有实际论文文本，仅有页标记，按G11标准属于material missing section。
- `CUMCM-2002-B-005` | severity=`MAJOR` | stratum=`OTHER_FORMAL_DERIVED` | packet pages=`1,4,7` | dimensions=`continuity_status,text_legibility_status,ocr_fidelity_status,math_content_status,end_matter_status` | likely layer=`G8-FORMAL-ARTIFACT-BODY-REPAIR`
  reviewer_comment: 源页面包含彩票模型正文和公式，artifact excerpt只保留页标记、没有实质文本，存在明显大段正文缺失。

## MINOR findings

- Count: `17`.
- MINOR findings are retained exactly from the human decision sheet; no severity was changed or inferred.
- Summary: MINOR findings are retained from reviewer comments; localized OCR, symbol, layout, formula/code, table, or conversion-format deviations are allowed by the frozen gate.

## No-op and integrity boundary

- Decision sheet, manifest, and precheck were read; the decision sheet was not rewritten.
- Formal data, artifacts, index, identity, membership, eligibility, backlog, and source files were not modified.
- No rendering, OCR, extraction, DOC/Word conversion, network, download, dependency installation, or G12 run occurred.
- Input hashes captured before output generation: manifest=`12FF62A2FD78AE736CD31C956AC817C9868BDE91702208BC2AC421082A40FCDE`, decisions=`8078A66F45C0C58F9BA4CF0C85BEB0E331C2BC405C52B93760B999DE00A8FD21`, precheck=`B57075A6D5B96C29DF46F69A3917CF5E40325556F57B6F9FA86BFC37F123D1A3`.

## Outputs

- `catalog\scale\g11_manual_sample_decision_audit.csv`
- `catalog\scale\g11_manual_sample_result.json`
- `reports\scale\G11_MANUAL_SAMPLE_SUMMARY.md`
- `reports\scale\G11_MANUAL_SAMPLE_APPROVAL.md`

G12 was not executed. A baseline/provenance reconciliation is required before any G12 handoff.
