# G11 Major Defect Triage Input

This is an aggregation and triage-input preparation artifact. It does not determine root cause, repair any artifact, or run the next triage stage.

## Evidence boundary

- Source-page material observations below are taken from the human reviewer comments only; source pages were not independently re-evaluated in this stage.
- Review packet excerpt existence and formal `paper.md` existence/size/SHA256 were checked read-only.
- `likely_layer` is intentionally `UNDETERMINED_PENDING_ROOT_CAUSE` for every row.
- All rows remain `PENDING_ROOT_CAUSE`; no G8 repair or G12 execution was performed.

## MAJOR findings

### CUMCM-2020-D-003 (sample order 5)

- Stratum: `Q3_OCR_DERIVED`; selected pages: `1, 68, 135`.
- Source-page material observation: `REVIEWER_COMMENT_REPORTS_SOURCE_SUBSTANTIVE_CONTENT; NOT_INDEPENDENTLY_RE_EVALUATED`.
- Review packet excerpts: `1` (all three non-empty excerpt paths exist).
- Formal artifact body: exists=`1`, size=`107265`, SHA256=`90CA9CFE4E538A72291F2133FDF3A1B289BC8F88EC983F7DA9BB458BB1D7F559`.
- Formal artifact evidence source: `g8_artifact_manifest.csv`; manifest status=`PASS`; validation status=``.
- Reviewer-observed symptom only: 长篇OCR样本首/中/末页均存在并与源页面主题一致，未见明显页序错乱或末尾截断；正文和代码主体可辨，但中后部代码/符号存在局部OCR误识别。关键变量、坐标或运算符部分被改写并影响模型含义。
- Root cause: `UNDETERMINED_PENDING_ROOT_CAUSE`; no layer is confirmed by this stage.

### CUMCM-1999-B-003 (sample order 19)

- Stratum: `OTHER_FORMAL_DERIVED`; selected pages: `1, 3, 6`.
- Source-page material observation: `REVIEWER_COMMENT_REPORTS_SOURCE_SUBSTANTIVE_CONTENT; NOT_INDEPENDENTLY_RE_EVALUATED`.
- Review packet excerpts: `1` (all three non-empty excerpt paths exist).
- Formal artifact body: exists=`1`, size=`205`, SHA256=`3556B4100929F4D56319AA760B104EE0CA947F3D5B03F13F7A0DF601179225BE`.
- Formal artifact evidence source: `g8_artifact_manifest.csv`; manifest status=`PASS`; validation status=``.
- Reviewer-observed symptom only: 源页面明显包含实质正文、图形/数学内容，但三个artifact excerpt基本只剩# Extracted Paper和source_page页标记，没有对应正文文本。按G11“重要章节/大段内容缺失”定义，回查该governed-duplicate artifact的正文生成/绑定是否为空。
- Root cause: `UNDETERMINED_PENDING_ROOT_CAUSE`; no layer is confirmed by this stage.

### CUMCM-2008-C-004 (sample order 20)

- Stratum: `OTHER_FORMAL_DERIVED`; selected pages: `1, 7, 14`.
- Source-page material observation: `REVIEWER_COMMENT_REPORTS_SOURCE_SUBSTANTIVE_CONTENT; NOT_INDEPENDENTLY_RE_EVALUATED`.
- Review packet excerpts: `1` (all three non-empty excerpt paths exist).
- Formal artifact body: exists=`1`, size=`458`, SHA256=`F501017C13D9B29686DD922D65EDC0CD658E90E82A5785E427A2D829537C8626`.
- Formal artifact evidence source: `g8_artifact_manifest.csv`; manifest status=`PASS`; validation status=``.
- Reviewer-observed symptom only: 源页面包含连续正文和公式/模型内容，但artifact excerpt仅有页码标记，未提供对应正文，存在明显实质内容缺失。建议检查formal artifact是否生成了空正文。
- Root cause: `UNDETERMINED_PENDING_ROOT_CAUSE`; no layer is confirmed by this stage.

### CUMCM-1992-A-003 (sample order 23)

- Stratum: `OTHER_FORMAL_DERIVED`; selected pages: `1, 3, 5`.
- Source-page material observation: `REVIEWER_COMMENT_REPORTS_SOURCE_SUBSTANTIVE_CONTENT; NOT_INDEPENDENTLY_RE_EVALUATED`.
- Review packet excerpts: `1` (all three non-empty excerpt paths exist).
- Formal artifact body: exists=`1`, size=`174`, SHA256=`1D9182549363CD07A8F3D657C2AD60D5197D3991577AD22ACB1BFC0A2C456E59`.
- Formal artifact evidence source: `g8_artifact_manifest.csv`; manifest status=`PASS`; validation status=``.
- Reviewer-observed symptom only: 源页面有连续正文和大量公式，但artifact excerpt只包含source_page标记，没有实际论文文本。属于明显大段内容缺失，建议回查formal artifact正文是否为空。
- Root cause: `UNDETERMINED_PENDING_ROOT_CAUSE`; no layer is confirmed by this stage.

### CUMCM-1993-B-001 (sample order 24)

- Stratum: `OTHER_FORMAL_DERIVED`; selected pages: `1, 1, 2`.
- Source-page material observation: `REVIEWER_COMMENT_REPORTS_SOURCE_SUBSTANTIVE_CONTENT; NOT_INDEPENDENTLY_RE_EVALUATED`.
- Review packet excerpts: `1` (all three non-empty excerpt paths exist).
- Formal artifact body: exists=`1`, size=`81`, SHA256=`96063CBA314A4F2CBA5DBE2319045D111F6D07789F83372C519D124C7AA4C1B2`.
- Formal artifact evidence source: `g8_artifact_manifest.csv`; manifest status=`PASS`; validation status=``.
- Reviewer-observed symptom only: 源页面可见正文和表格/排名数据，但artifact excerpt仅有页码标记，实际正文为空，无法完成内容连续性、文字可读性和表格内容核验。
- Root cause: `UNDETERMINED_PENDING_ROOT_CAUSE`; no layer is confirmed by this stage.

### CUMCM-1996-B-001 (sample order 25)

- Stratum: `OTHER_FORMAL_DERIVED`; selected pages: `1, 3, 5`.
- Source-page material observation: `REVIEWER_COMMENT_REPORTS_SOURCE_SUBSTANTIVE_CONTENT; NOT_INDEPENDENTLY_RE_EVALUATED`.
- Review packet excerpts: `1` (all three non-empty excerpt paths exist).
- Formal artifact body: exists=`1`, size=`174`, SHA256=`1D9182549363CD07A8F3D657C2AD60D5197D3991577AD22ACB1BFC0A2C456E59`.
- Formal artifact evidence source: `g8_artifact_manifest.csv`; manifest status=`PASS`; validation status=``.
- Reviewer-observed symptom only: 源页面包含完整正文与公式，但artifact excerpt没有对应文本，仅保留source_page标记。属于实质正文缺失，而非轻微OCR错误。
- Root cause: `UNDETERMINED_PENDING_ROOT_CAUSE`; no layer is confirmed by this stage.

### CUMCM-1997-A-008 (sample order 26)

- Stratum: `OTHER_FORMAL_DERIVED`; selected pages: `1, 3, 5`.
- Source-page material observation: `REVIEWER_COMMENT_REPORTS_SOURCE_SUBSTANTIVE_CONTENT; NOT_INDEPENDENTLY_RE_EVALUATED`.
- Review packet excerpts: `1` (all three non-empty excerpt paths exist).
- Formal artifact body: exists=`1`, size=`174`, SHA256=`1D9182549363CD07A8F3D657C2AD60D5197D3991577AD22ACB1BFC0A2C456E59`.
- Formal artifact evidence source: `g8_artifact_manifest.csv`; manifest status=`PASS`; validation status=``.
- Reviewer-observed symptom only: 源页面包含正文和数学公式，artifact excerpt基本为空，仅有source_page标记；抽样内容无法在formal artifact中找到对应文本。
- Root cause: `UNDETERMINED_PENDING_ROOT_CAUSE`; no layer is confirmed by this stage.

### CUMCM-1998-A-007 (sample order 27)

- Stratum: `OTHER_FORMAL_DERIVED`; selected pages: `1, 3, 5`.
- Source-page material observation: `REVIEWER_COMMENT_REPORTS_SOURCE_SUBSTANTIVE_CONTENT; NOT_INDEPENDENTLY_RE_EVALUATED`.
- Review packet excerpts: `1` (all three non-empty excerpt paths exist).
- Formal artifact body: exists=`1`, size=`174`, SHA256=`1D9182549363CD07A8F3D657C2AD60D5197D3991577AD22ACB1BFC0A2C456E59`.
- Formal artifact evidence source: `g8_artifact_manifest.csv`; manifest status=`PASS`; validation status=``.
- Reviewer-observed symptom only: 源页面可见正文、公式及数据表，而artifact excerpt只有页标记、没有实质文本，存在明显正文/表格内容缺失。
- Root cause: `UNDETERMINED_PENDING_ROOT_CAUSE`; no layer is confirmed by this stage.

### CUMCM-2000-A-005 (sample order 28)

- Stratum: `OTHER_FORMAL_DERIVED`; selected pages: `1, 5, 9`.
- Source-page material observation: `REVIEWER_COMMENT_REPORTS_SOURCE_SUBSTANTIVE_CONTENT; NOT_INDEPENDENTLY_RE_EVALUATED`.
- Review packet excerpts: `1` (all three non-empty excerpt paths exist).
- Formal artifact body: exists=`1`, size=`298`, SHA256=`1C2FC324063A906FF208763D2826E0A769B059290333B0542241C22CD9C91DE8`.
- Formal artifact evidence source: `g8_artifact_manifest.csv`; manifest status=`PASS`; validation status=``.
- Reviewer-observed symptom only: DNA分类论文源页面包含正文、流程图和公式，但artifact excerpt仅有source_page标记，没有对应正文，属于明显内容缺失。
- Root cause: `UNDETERMINED_PENDING_ROOT_CAUSE`; no layer is confirmed by this stage.

### CUMCM-2001-A-001 (sample order 29)

- Stratum: `OTHER_FORMAL_DERIVED`; selected pages: `1, 3, 6`.
- Source-page material observation: `REVIEWER_COMMENT_REPORTS_SOURCE_SUBSTANTIVE_CONTENT; NOT_INDEPENDENTLY_RE_EVALUATED`.
- Review packet excerpts: `1` (all three non-empty excerpt paths exist).
- Formal artifact body: exists=`1`, size=`205`, SHA256=`3556B4100929F4D56319AA760B104EE0CA947F3D5B03F13F7A0DF601179225BE`.
- Formal artifact evidence source: `g8_artifact_manifest.csv`; manifest status=`PASS`; validation status=``.
- Reviewer-observed symptom only: 源页面包含正文、图形及英文尾页内容，但artifact excerpt没有实际论文文本，仅有页标记，按G11标准属于material missing section。
- Root cause: `UNDETERMINED_PENDING_ROOT_CAUSE`; no layer is confirmed by this stage.

### CUMCM-2002-B-005 (sample order 30)

- Stratum: `OTHER_FORMAL_DERIVED`; selected pages: `1, 4, 7`.
- Source-page material observation: `REVIEWER_COMMENT_REPORTS_SOURCE_SUBSTANTIVE_CONTENT; NOT_INDEPENDENTLY_RE_EVALUATED`.
- Review packet excerpts: `1` (all three non-empty excerpt paths exist).
- Formal artifact body: exists=`1`, size=`236`, SHA256=`845EAC42B8D7C797245E742A556F6F7B87F8594979C758FB43031CD6D48DB563`.
- Formal artifact evidence source: `g8_artifact_manifest.csv`; manifest status=`PASS`; validation status=``.
- Reviewer-observed symptom only: 源页面包含彩票模型正文和公式，artifact excerpt只保留页标记、没有实质文本，存在明显大段正文缺失。
- Root cause: `UNDETERMINED_PENDING_ROOT_CAUSE`; no layer is confirmed by this stage.
