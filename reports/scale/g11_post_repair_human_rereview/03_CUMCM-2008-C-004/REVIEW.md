# CUMCM-2008-C-004

This packet prepares post-repair human rereview. It makes no post-repair severity decision.

## Original G11 Major Finding

- Original severity: `MAJOR`.
- Original decision reference: `catalog/scale/g11_manual_sample_decisions.csv:paper_id=CUMCM-2008-C-004;sample_order=20`.
- Original review packet: `reports/scale/g11_manual_sample_review/20_CUMCM-2008-C-004/review.md`.
- Original reviewer comment: 源页面包含连续正文和公式/模型内容，但artifact excerpt仅有页码标记，未提供对应正文，存在明显实质内容缺失。建议检查formal artifact是否生成了空正文。
- Original defect description: 源页面包含连续正文和公式/模型内容，但artifact excerpt仅有页码标记，未提供对应正文，存在明显实质内容缺失。建议检查formal artifact是否生成了空正文。
- Root-cause category retained from authoritative triage: `FORMAL_ARTIFACT_PAGE_CONTENT_MISSING`.

## Repair Summary

- Repair route: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION;MARKER_ONLY_DIAGNOSTIC_OCR_REUSE`.
- Repair layer: `G11_MARKER_ONLY_PAGE_LOCAL_FORMAL_BODY`.
- Repaired pages: `1;2;3;4;5;6;7;8;9;10;11;12;13;14`.
- Historical body SHA256 before repair: `F501017C13D9B29686DD922D65EDC0CD658E90E82A5785E427A2D829537C8626`.
- Current body SHA256 after repair: `28881CCFCD68B7F461FCEF1AA44D1C4FDE3BEB8C354EEF184B12E1AA34ED2D7D`.
- Repair attempt: `20260905T045418589698Z_557724fba657`.
- Current artifact set: `derived/scale/papers/CUMCM-2008-C-004`.
- Current formal body: `derived/scale/papers/CUMCM-2008-C-004/paper.md`.
- Repair provenance: `catalog/scale/g11_multi_route_formal_repair_targets.csv`.

## Human Re-review Evidence

Review only whether the original MAJOR issue has been resolved. The page-level evidence below is programmatic binding evidence, not a replacement for human visual/semantic review.

### Re-review unit G11-MANUAL-SAMPLE-20-PAGE-A

- Source page / original review location: `1` / `G11-MANUAL-SAMPLE-20-PAGE-A`.
- Historical source render: `reports/scale/g11_manual_sample_review/20_CUMCM-2008-C-004/page_A.png`.
- Historical artifact excerpt: `reports/scale/g11_manual_sample_review/20_CUMCM-2008-C-004/page_A_artifact_excerpt.txt`.
- Original formal page state: `present=0; char_count=0; line_count=0; sha256=E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855`.
- Current repaired formal excerpt: `reports/scale/g11_post_repair_human_rereview/03_CUMCM-2008-C-004/current_formal_p1.md`.
- Current page segment SHA256: `B803DF42E21AB0A17D60EA5590E8D4E0D11B174077D824A1F7D4E57873648C27`.
- Repair page evidence: `catalog/scale/g11_residual_pdftotext_calibration/positive/CUMCM-2008-C-004/source_page_1.txt`.
- Repair evidence SHA256: `51E41A9E4676686F91457654879DCC71C9382B0AC7DFE74F4E6C6BB723D3DA23`.
- Repair route/layer: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION` / `G11_MARKER_ONLY_PAGE_LOCAL_FORMAL_BODY`.
- Programmatic validation: `preflight_pass=1; postrepair_pass=1; evidence_quality_status=PASS`.

### Re-review unit G11-MANUAL-SAMPLE-20-PAGE-B

- Source page / original review location: `7` / `G11-MANUAL-SAMPLE-20-PAGE-B`.
- Historical source render: `reports/scale/g11_manual_sample_review/20_CUMCM-2008-C-004/page_B.png`.
- Historical artifact excerpt: `reports/scale/g11_manual_sample_review/20_CUMCM-2008-C-004/page_B_artifact_excerpt.txt`.
- Original formal page state: `present=0; char_count=0; line_count=0; sha256=E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855`.
- Current repaired formal excerpt: `reports/scale/g11_post_repair_human_rereview/03_CUMCM-2008-C-004/current_formal_p7.md`.
- Current page segment SHA256: `BBDA6FCA3947E16AEE50DDDC9B4C9946517F012481B475AE1DB8A5630F5BB14A`.
- Repair page evidence: `catalog/scale/g11_residual_pdftotext_calibration/positive/CUMCM-2008-C-004/source_page_7.txt`.
- Repair evidence SHA256: `F358177AAC1B3FC45162860B0A2F05DBC01FF737DD8FD716ABE09822CCD94114`.
- Repair route/layer: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION` / `G11_MARKER_ONLY_PAGE_LOCAL_FORMAL_BODY`.
- Programmatic validation: `preflight_pass=1; postrepair_pass=1; evidence_quality_status=PASS`.

### Re-review unit G11-MANUAL-SAMPLE-20-PAGE-C

- Source page / original review location: `14` / `G11-MANUAL-SAMPLE-20-PAGE-C`.
- Historical source render: `reports/scale/g11_manual_sample_review/20_CUMCM-2008-C-004/page_C.png`.
- Historical artifact excerpt: `reports/scale/g11_manual_sample_review/20_CUMCM-2008-C-004/page_C_artifact_excerpt.txt`.
- Original formal page state: `present=0; char_count=0; line_count=0; sha256=E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855`.
- Current repaired formal excerpt: `reports/scale/g11_post_repair_human_rereview/03_CUMCM-2008-C-004/current_formal_p14.md`.
- Current page segment SHA256: `59106338D441833171B3B83E5D4ED665E6D2A66F41DA2BD661ABCFE52245230A`.
- Repair page evidence: `catalog/scale/g11_residual_pdftotext_calibration/positive/CUMCM-2008-C-004/source_page_14.txt`.
- Repair evidence SHA256: `00B45AEA92F6883138C5E1F85927321E7FF6FE2F5A36BF9C81A3A99563940FF8`.
- Repair route/layer: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION` / `G11_MARKER_ONLY_PAGE_LOCAL_FORMAL_BODY`.
- Programmatic validation: `preflight_pass=1; postrepair_pass=1; evidence_quality_status=PASS`.

## Human Decision

`PENDING`

The human reviewer must select exactly one of PASS, MINOR, MAJOR, or CRITICAL in the new decision sheet and record the rationale. Codex has not classified this packet.

## Source Page Images

These are byte-for-byte copies of existing historical G11 source renders. They are provided as visual evidence for human rereview; this section asserts no severity or repair conclusion.

### G11-MANUAL-SAMPLE-20-PAGE-A

- Source page: `1`.
- Existing source image: [source_unit_01_p1.png](source_images/source_unit_01_p1.png).
- Current repaired formal excerpt: [current_formal_p1.md](current_formal_p1.md).
- Original issue: 源页面包含连续正文和公式/模型内容，但artifact excerpt仅有页码标记，未提供对应正文，存在明显实质内容缺失。建议检查formal artifact是否生成了空正文。
- SHARED_SOURCE_IMAGE_BINDING=0.

### G11-MANUAL-SAMPLE-20-PAGE-B

- Source page: `7`.
- Existing source image: [source_unit_02_p7.png](source_images/source_unit_02_p7.png).
- Current repaired formal excerpt: [current_formal_p7.md](current_formal_p7.md).
- Original issue: 源页面包含连续正文和公式/模型内容，但artifact excerpt仅有页码标记，未提供对应正文，存在明显实质内容缺失。建议检查formal artifact是否生成了空正文。
- SHARED_SOURCE_IMAGE_BINDING=0.

### G11-MANUAL-SAMPLE-20-PAGE-C

- Source page: `14`.
- Existing source image: [source_unit_03_p14.png](source_images/source_unit_03_p14.png).
- Current repaired formal excerpt: [current_formal_p14.md](current_formal_p14.md).
- Original issue: 源页面包含连续正文和公式/模型内容，但artifact excerpt仅有页码标记，未提供对应正文，存在明显实质内容缺失。建议检查formal artifact是否生成了空正文。
- SHARED_SOURCE_IMAGE_BINDING=0.
