# G11 Major Defect Root Cause Triage

This stage performs diagnosis only. It does not repair formal artifacts, regenerate excerpts, modify human decisions, run OCR, or execute G12.

## Scope and baseline

- Authoritative G11 preparation attempt: `20260903T172404115633_3c748bc1`.
- Sample fingerprint: `677898FA2C0DE5B8229AC310566A2D0A41465790B5F188320CD2EE46C877D4EF`; decision sheet SHA256 unchanged=`1`.
- Current G11 human gate remains `PARTIAL` with 11 MAJOR findings; this triage stage status is `PASS`.
- Historical predecessor lineage remains an accepted non-blocking limitation; it was not used as a current evidence source.

## Classification totals

- MAJOR inputs=`11`; triaged=`11`; unresolved=`0`.
- `FORMAL_ARTIFACT_PAGE_CONTENT_MISSING`: `10`.
- `TRUE_CONTENT_QUALITY_MAJOR`: `1`.
- `REVIEW_PACKET_EXCERPT_OMISSION`: `0`.
- `SOURCE_PAGE_MAPPING_MISMATCH`: `0`.
- `ARTIFACT_BINDING_DEFECT`: `0`; `GOVERNED_DUPLICATE_BINDING_DEFECT`: `0`; `MIXED_ROOT_CAUSE`: `0`.
- Formal page content present but excerpt substantive content missing=`0`.
- Formal page content missing classification count=`10`.

## Evidence interpretation

- Formal body existence and non-zero file size were not treated as sufficient health checks.
- Page-local formal content was computed only between the selected `source_page` marker and the next marker, after removing comments, whitespace and structural Markdown.
- Packet excerpts were classified from the persisted-page-text window; metadata and structural-only context do not count as substantive content.
- Existing selected-page PNGs and reviewer comments were used as source-material evidence; no new source extraction or OCR was run.
- Governed-duplicate risk flags and shared placeholder body hashes were recorded, but no duplicate binding defect was asserted because identity, membership, source and registry bindings validate.
- Static scan found `215` marker-only formal bodies across the formal artifact registry, so the potential formal scope is broader than the 11-sample triage scope.

## Per-paper triage

### CUMCM-2020-D-003 (sample order 5)

- Root cause category: `TRUE_CONTENT_QUALITY_MAJOR`; confidence: `HIGH`.
- Recommended minimal re-entry: `G8-Q3-MINIMAL-FORMAL-BODY-REPAIR`; human re-review required: `1`.
- Selected pages: `1, 68, 135`.
- Formal body: exists=`1`, nonempty=`1`, bytes=`107265`, characters=`86076`, SHA256=`90CA9CFE4E538A72291F2133FDF3A1B289BC8F88EC983F7DA9BB458BB1D7F559`.
- Formal source_page markers: count=`0`, first=`NONE`, last=`NONE`.
- Selected formal page content present A/B/C=`0/0/0`; character counts=`0/0/0`.
- Selected page markers present A/B/C=`0/0/0`.
- Packet excerpt substantive content present A/B/C=`1/1/1`; excerpt files exist/nonempty=`1/1/1` / `1/1/1`.
- Identity/membership/source bindings valid=`1/1/1`; selected PNG evidence present=`1`.
- Human symptom supported by current evidence=`1`. Reviewer symptom: 长篇OCR样本首/中/末页均存在并与源页面主题一致，未见明显页序错乱或末尾截断；正文和代码主体可辨，但中后部代码/符号存在局部OCR误识别。关键变量、坐标或运算符部分被改写并影响模型含义。
- Page mapping: No source_page markers exist in the formal body; no nearest marker or page offset is determinable.
- Notes: Formal body and packet excerpts contain substantive text. The reviewer comment directly reports OCR/symbol errors affecting model meaning; this is a content-quality symptom. The formal body has zero source_page markers, so page-local mapping is unavailable, but no page offset is determinable and mapping mismatch is not asserted.

### CUMCM-1999-B-003 (sample order 19)

- Root cause category: `FORMAL_ARTIFACT_PAGE_CONTENT_MISSING`; confidence: `HIGH`.
- Recommended minimal re-entry: `G8-FORMAL-ARTIFACT-MINIMAL-BODY-REPAIR`; human re-review required: `1`.
- Selected pages: `1, 3, 6`.
- Formal body: exists=`1`, nonempty=`1`, bytes=`205`, characters=`180`, SHA256=`3556B4100929F4D56319AA760B104EE0CA947F3D5B03F13F7A0DF601179225BE`.
- Formal source_page markers: count=`6`, first=`1`, last=`6`.
- Selected formal page content present A/B/C=`0/0/0`; character counts=`0/0/0`.
- Selected page markers present A/B/C=`1/1/1`.
- Packet excerpt substantive content present A/B/C=`0/0/0`; excerpt files exist/nonempty=`1/1/1` / `1/1/1`.
- Identity/membership/source bindings valid=`1/1/1`; selected PNG evidence present=`1`.
- Human symptom supported by current evidence=`1`. Reviewer symptom: 源页面明显包含实质正文、图形/数学内容，但三个artifact excerpt基本只剩# Extracted Paper和source_page页标记，没有对应正文文本。按G11“重要章节/大段内容缺失”定义，回查该governed-duplicate artifact的正文生成/绑定是否为空。
- Page mapping: Selected-page markers are present and no offset is observed.
- Notes: Existing selected-page PNGs and the human comment indicate substantive source material, while all selected formal page-local segments are empty and all packet excerpts are structural-only. The governed-duplicate risk flag is retained as context; identity, membership and source bindings validate, so no duplicate binding defect is asserted.

### CUMCM-2008-C-004 (sample order 20)

- Root cause category: `FORMAL_ARTIFACT_PAGE_CONTENT_MISSING`; confidence: `HIGH`.
- Recommended minimal re-entry: `G8-FORMAL-ARTIFACT-MINIMAL-BODY-REPAIR`; human re-review required: `1`.
- Selected pages: `1, 7, 14`.
- Formal body: exists=`1`, nonempty=`1`, bytes=`458`, characters=`401`, SHA256=`F501017C13D9B29686DD922D65EDC0CD658E90E82A5785E427A2D829537C8626`.
- Formal source_page markers: count=`14`, first=`1`, last=`14`.
- Selected formal page content present A/B/C=`0/0/0`; character counts=`0/0/0`.
- Selected page markers present A/B/C=`1/1/1`.
- Packet excerpt substantive content present A/B/C=`0/0/0`; excerpt files exist/nonempty=`1/1/1` / `1/1/1`.
- Identity/membership/source bindings valid=`1/1/1`; selected PNG evidence present=`1`.
- Human symptom supported by current evidence=`1`. Reviewer symptom: 源页面包含连续正文和公式/模型内容，但artifact excerpt仅有页码标记，未提供对应正文，存在明显实质内容缺失。建议检查formal artifact是否生成了空正文。
- Page mapping: Selected-page markers are present and no offset is observed.
- Notes: Existing selected-page PNGs and the human comment indicate substantive source material, while all selected formal page-local segments are empty and all packet excerpts are structural-only. The governed-duplicate risk flag is retained as context; identity, membership and source bindings validate, so no duplicate binding defect is asserted.

### CUMCM-1992-A-003 (sample order 23)

- Root cause category: `FORMAL_ARTIFACT_PAGE_CONTENT_MISSING`; confidence: `HIGH`.
- Recommended minimal re-entry: `G8-FORMAL-ARTIFACT-MINIMAL-BODY-REPAIR`; human re-review required: `1`.
- Selected pages: `1, 3, 5`.
- Formal body: exists=`1`, nonempty=`1`, bytes=`174`, characters=`153`, SHA256=`1D9182549363CD07A8F3D657C2AD60D5197D3991577AD22ACB1BFC0A2C456E59`.
- Formal source_page markers: count=`5`, first=`1`, last=`5`.
- Selected formal page content present A/B/C=`0/0/0`; character counts=`0/0/0`.
- Selected page markers present A/B/C=`1/1/1`.
- Packet excerpt substantive content present A/B/C=`0/0/0`; excerpt files exist/nonempty=`1/1/1` / `1/1/1`.
- Identity/membership/source bindings valid=`1/1/1`; selected PNG evidence present=`1`.
- Human symptom supported by current evidence=`1`. Reviewer symptom: 源页面有连续正文和大量公式，但artifact excerpt只包含source_page标记，没有实际论文文本。属于明显大段内容缺失，建议回查formal artifact正文是否为空。
- Page mapping: Selected-page markers are present and no offset is observed.
- Notes: Existing selected-page PNGs and the human comment indicate substantive source material, while all selected formal page-local segments are empty and all packet excerpts are structural-only. The governed-duplicate risk flag is retained as context; identity, membership and source bindings validate, so no duplicate binding defect is asserted.

### CUMCM-1993-B-001 (sample order 24)

- Root cause category: `FORMAL_ARTIFACT_PAGE_CONTENT_MISSING`; confidence: `HIGH`.
- Recommended minimal re-entry: `G8-FORMAL-ARTIFACT-MINIMAL-BODY-REPAIR`; human re-review required: `1`.
- Selected pages: `1, 1, 2`.
- Formal body: exists=`1`, nonempty=`1`, bytes=`81`, characters=`72`, SHA256=`96063CBA314A4F2CBA5DBE2319045D111F6D07789F83372C519D124C7AA4C1B2`.
- Formal source_page markers: count=`2`, first=`1`, last=`2`.
- Selected formal page content present A/B/C=`0/0/0`; character counts=`0/0/0`.
- Selected page markers present A/B/C=`1/1/1`.
- Packet excerpt substantive content present A/B/C=`0/0/0`; excerpt files exist/nonempty=`1/1/1` / `1/1/1`.
- Identity/membership/source bindings valid=`1/1/1`; selected PNG evidence present=`1`.
- Human symptom supported by current evidence=`1`. Reviewer symptom: 源页面可见正文和表格/排名数据，但artifact excerpt仅有页码标记，实际正文为空，无法完成内容连续性、文字可读性和表格内容核验。
- Page mapping: Selected-page markers are present and no offset is observed.
- Notes: Existing selected-page PNGs and the human comment indicate substantive source material, while all selected formal page-local segments are empty and all packet excerpts are structural-only. The governed-duplicate risk flag is retained as context; identity, membership and source bindings validate, so no duplicate binding defect is asserted.

### CUMCM-1996-B-001 (sample order 25)

- Root cause category: `FORMAL_ARTIFACT_PAGE_CONTENT_MISSING`; confidence: `HIGH`.
- Recommended minimal re-entry: `G8-FORMAL-ARTIFACT-MINIMAL-BODY-REPAIR`; human re-review required: `1`.
- Selected pages: `1, 3, 5`.
- Formal body: exists=`1`, nonempty=`1`, bytes=`174`, characters=`153`, SHA256=`1D9182549363CD07A8F3D657C2AD60D5197D3991577AD22ACB1BFC0A2C456E59`.
- Formal source_page markers: count=`5`, first=`1`, last=`5`.
- Selected formal page content present A/B/C=`0/0/0`; character counts=`0/0/0`.
- Selected page markers present A/B/C=`1/1/1`.
- Packet excerpt substantive content present A/B/C=`0/0/0`; excerpt files exist/nonempty=`1/1/1` / `1/1/1`.
- Identity/membership/source bindings valid=`1/1/1`; selected PNG evidence present=`1`.
- Human symptom supported by current evidence=`1`. Reviewer symptom: 源页面包含完整正文与公式，但artifact excerpt没有对应文本，仅保留source_page标记。属于实质正文缺失，而非轻微OCR错误。
- Page mapping: Selected-page markers are present and no offset is observed.
- Notes: Existing selected-page PNGs and the human comment indicate substantive source material, while all selected formal page-local segments are empty and all packet excerpts are structural-only. The governed-duplicate risk flag is retained as context; identity, membership and source bindings validate, so no duplicate binding defect is asserted.

### CUMCM-1997-A-008 (sample order 26)

- Root cause category: `FORMAL_ARTIFACT_PAGE_CONTENT_MISSING`; confidence: `HIGH`.
- Recommended minimal re-entry: `G8-FORMAL-ARTIFACT-MINIMAL-BODY-REPAIR`; human re-review required: `1`.
- Selected pages: `1, 3, 5`.
- Formal body: exists=`1`, nonempty=`1`, bytes=`174`, characters=`153`, SHA256=`1D9182549363CD07A8F3D657C2AD60D5197D3991577AD22ACB1BFC0A2C456E59`.
- Formal source_page markers: count=`5`, first=`1`, last=`5`.
- Selected formal page content present A/B/C=`0/0/0`; character counts=`0/0/0`.
- Selected page markers present A/B/C=`1/1/1`.
- Packet excerpt substantive content present A/B/C=`0/0/0`; excerpt files exist/nonempty=`1/1/1` / `1/1/1`.
- Identity/membership/source bindings valid=`1/1/1`; selected PNG evidence present=`1`.
- Human symptom supported by current evidence=`1`. Reviewer symptom: 源页面包含正文和数学公式，artifact excerpt基本为空，仅有source_page标记；抽样内容无法在formal artifact中找到对应文本。
- Page mapping: Selected-page markers are present and no offset is observed.
- Notes: Existing selected-page PNGs and the human comment indicate substantive source material, while all selected formal page-local segments are empty and all packet excerpts are structural-only. The governed-duplicate risk flag is retained as context; identity, membership and source bindings validate, so no duplicate binding defect is asserted.

### CUMCM-1998-A-007 (sample order 27)

- Root cause category: `FORMAL_ARTIFACT_PAGE_CONTENT_MISSING`; confidence: `HIGH`.
- Recommended minimal re-entry: `G8-FORMAL-ARTIFACT-MINIMAL-BODY-REPAIR`; human re-review required: `1`.
- Selected pages: `1, 3, 5`.
- Formal body: exists=`1`, nonempty=`1`, bytes=`174`, characters=`153`, SHA256=`1D9182549363CD07A8F3D657C2AD60D5197D3991577AD22ACB1BFC0A2C456E59`.
- Formal source_page markers: count=`5`, first=`1`, last=`5`.
- Selected formal page content present A/B/C=`0/0/0`; character counts=`0/0/0`.
- Selected page markers present A/B/C=`1/1/1`.
- Packet excerpt substantive content present A/B/C=`0/0/0`; excerpt files exist/nonempty=`1/1/1` / `1/1/1`.
- Identity/membership/source bindings valid=`1/1/1`; selected PNG evidence present=`1`.
- Human symptom supported by current evidence=`1`. Reviewer symptom: 源页面可见正文、公式及数据表，而artifact excerpt只有页标记、没有实质文本，存在明显正文/表格内容缺失。
- Page mapping: Selected-page markers are present and no offset is observed.
- Notes: Existing selected-page PNGs and the human comment indicate substantive source material, while all selected formal page-local segments are empty and all packet excerpts are structural-only. The governed-duplicate risk flag is retained as context; identity, membership and source bindings validate, so no duplicate binding defect is asserted.

### CUMCM-2000-A-005 (sample order 28)

- Root cause category: `FORMAL_ARTIFACT_PAGE_CONTENT_MISSING`; confidence: `HIGH`.
- Recommended minimal re-entry: `G8-FORMAL-ARTIFACT-MINIMAL-BODY-REPAIR`; human re-review required: `1`.
- Selected pages: `1, 5, 9`.
- Formal body: exists=`1`, nonempty=`1`, bytes=`298`, characters=`261`, SHA256=`1C2FC324063A906FF208763D2826E0A769B059290333B0542241C22CD9C91DE8`.
- Formal source_page markers: count=`9`, first=`1`, last=`9`.
- Selected formal page content present A/B/C=`0/0/0`; character counts=`0/0/0`.
- Selected page markers present A/B/C=`1/1/1`.
- Packet excerpt substantive content present A/B/C=`0/0/0`; excerpt files exist/nonempty=`1/1/1` / `1/1/1`.
- Identity/membership/source bindings valid=`1/1/1`; selected PNG evidence present=`1`.
- Human symptom supported by current evidence=`1`. Reviewer symptom: DNA分类论文源页面包含正文、流程图和公式，但artifact excerpt仅有source_page标记，没有对应正文，属于明显内容缺失。
- Page mapping: Selected-page markers are present and no offset is observed.
- Notes: Existing selected-page PNGs and the human comment indicate substantive source material, while all selected formal page-local segments are empty and all packet excerpts are structural-only. The governed-duplicate risk flag is retained as context; identity, membership and source bindings validate, so no duplicate binding defect is asserted.

### CUMCM-2001-A-001 (sample order 29)

- Root cause category: `FORMAL_ARTIFACT_PAGE_CONTENT_MISSING`; confidence: `HIGH`.
- Recommended minimal re-entry: `G8-FORMAL-ARTIFACT-MINIMAL-BODY-REPAIR`; human re-review required: `1`.
- Selected pages: `1, 3, 6`.
- Formal body: exists=`1`, nonempty=`1`, bytes=`205`, characters=`180`, SHA256=`3556B4100929F4D56319AA760B104EE0CA947F3D5B03F13F7A0DF601179225BE`.
- Formal source_page markers: count=`6`, first=`1`, last=`6`.
- Selected formal page content present A/B/C=`0/0/0`; character counts=`0/0/0`.
- Selected page markers present A/B/C=`1/1/1`.
- Packet excerpt substantive content present A/B/C=`0/0/0`; excerpt files exist/nonempty=`1/1/1` / `1/1/1`.
- Identity/membership/source bindings valid=`1/1/1`; selected PNG evidence present=`1`.
- Human symptom supported by current evidence=`1`. Reviewer symptom: 源页面包含正文、图形及英文尾页内容，但artifact excerpt没有实际论文文本，仅有页标记，按G11标准属于material missing section。
- Page mapping: Selected-page markers are present and no offset is observed.
- Notes: Existing selected-page PNGs and the human comment indicate substantive source material, while all selected formal page-local segments are empty and all packet excerpts are structural-only. The governed-duplicate risk flag is retained as context; identity, membership and source bindings validate, so no duplicate binding defect is asserted.

### CUMCM-2002-B-005 (sample order 30)

- Root cause category: `FORMAL_ARTIFACT_PAGE_CONTENT_MISSING`; confidence: `HIGH`.
- Recommended minimal re-entry: `G8-FORMAL-ARTIFACT-MINIMAL-BODY-REPAIR`; human re-review required: `1`.
- Selected pages: `1, 4, 7`.
- Formal body: exists=`1`, nonempty=`1`, bytes=`236`, characters=`207`, SHA256=`845EAC42B8D7C797245E742A556F6F7B87F8594979C758FB43031CD6D48DB563`.
- Formal source_page markers: count=`7`, first=`1`, last=`7`.
- Selected formal page content present A/B/C=`0/0/0`; character counts=`0/0/0`.
- Selected page markers present A/B/C=`1/1/1`.
- Packet excerpt substantive content present A/B/C=`0/0/0`; excerpt files exist/nonempty=`1/1/1` / `1/1/1`.
- Identity/membership/source bindings valid=`1/1/1`; selected PNG evidence present=`1`.
- Human symptom supported by current evidence=`1`. Reviewer symptom: 源页面包含彩票模型正文和公式，artifact excerpt只保留页标记、没有实质文本，存在明显大段正文缺失。
- Page mapping: Selected-page markers are present and no offset is observed.
- Notes: Existing selected-page PNGs and the human comment indicate substantive source material, while all selected formal page-local segments are empty and all packet excerpts are structural-only. The governed-duplicate risk flag is retained as context; identity, membership and source bindings validate, so no duplicate binding defect is asserted.

## Handoff

- `ROOT_CAUSE_UNRESOLVED_COUNT=0`; triage status is `PASS`.
- `POTENTIAL_REVIEW_PACKET_AFFECTED_SCOPE=OTHER`; no paper was classified as packet-only omission, so packet repair scope is not promoted (`POTENTIAL_AFFECTED_IDENTITY_COUNT=0`).
- `POTENTIAL_FORMAL_ARTIFACT_AFFECTED_SCOPE=BROADER_THAN_SAMPLE`; marker-only formal-body scope observed=`215` identities.
- Next stage: `G11-MAJOR-DEFECT-MINIMAL-REPAIR-PLAN`. It is not executed by this stage.

## No-op boundary

- Formal data, formal artifact content, index, identity, membership, eligibility, backlog, source and decision modification counts are `0`.
- OCR, rendering, extraction, body reconstruction, packet regeneration, DOC/Word, network, dependency installation, Git write operations and G12 are `0`.
