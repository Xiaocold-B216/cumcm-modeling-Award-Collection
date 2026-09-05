# CUMCM-2002-B-005

This packet prepares post-repair human rereview. It makes no post-repair severity decision.

## Original G11 Major Finding

- Original severity: `MAJOR`.
- Original decision reference: `catalog/scale/g11_manual_sample_decisions.csv:paper_id=CUMCM-2002-B-005;sample_order=30`.
- Original review packet: `reports/scale/g11_manual_sample_review/30_CUMCM-2002-B-005/review.md`.
- Original reviewer comment: 源页面包含彩票模型正文和公式，artifact excerpt只保留页标记、没有实质文本，存在明显大段正文缺失。
- Original defect description: 源页面包含彩票模型正文和公式，artifact excerpt只保留页标记、没有实质文本，存在明显大段正文缺失。
- Root-cause category retained from authoritative triage: `FORMAL_ARTIFACT_PAGE_CONTENT_MISSING`.

## Repair Summary

- Repair route: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION;MARKER_ONLY_DIAGNOSTIC_OCR_REUSE`.
- Repair layer: `G11_MARKER_ONLY_PAGE_LOCAL_FORMAL_BODY`.
- Repaired pages: `1;2;3;4;5;6;7`.
- Historical body SHA256 before repair: `845EAC42B8D7C797245E742A556F6F7B87F8594979C758FB43031CD6D48DB563`.
- Current body SHA256 after repair: `28F3388B2889E9ABCBDDB342B37A2816BC36EFE30A7725B7D6C78ECBBD250502`.
- Repair attempt: `20260905T045418589698Z_557724fba657`.
- Current artifact set: `derived/scale/papers/CUMCM-2002-B-005`.
- Current formal body: `derived/scale/papers/CUMCM-2002-B-005/paper.md`.
- Repair provenance: `catalog/scale/g11_multi_route_formal_repair_targets.csv`.

## Human Re-review Evidence

Review only whether the original MAJOR issue has been resolved. The page-level evidence below is programmatic binding evidence, not a replacement for human visual/semantic review.

### Re-review unit G11-MANUAL-SAMPLE-30-PAGE-A

- Source page / original review location: `1` / `G11-MANUAL-SAMPLE-30-PAGE-A`.
- Historical source render: `reports/scale/g11_manual_sample_review/30_CUMCM-2002-B-005/page_A.png`.
- Historical artifact excerpt: `reports/scale/g11_manual_sample_review/30_CUMCM-2002-B-005/page_A_artifact_excerpt.txt`.
- Original formal page state: `present=0; char_count=0; line_count=0; sha256=E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855`.
- Current repaired formal excerpt: `reports/scale/g11_post_repair_human_rereview/11_CUMCM-2002-B-005/current_formal_p1.md`.
- Current page segment SHA256: `911C5A1368413DC50E7A66A815441B879E7FE00E5322E8AE94F6730EBD00135D`.
- Repair page evidence: `catalog/scale/g11_residual_pdftotext_calibration/positive/CUMCM-2002-B-005/source_page_1.txt`.
- Repair evidence SHA256: `8CFFDE1E18158FC6534AFB6EDC9F6B248E147070D2987D48839451A0ACE7BE24`.
- Repair route/layer: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION` / `G11_MARKER_ONLY_PAGE_LOCAL_FORMAL_BODY`.
- Programmatic validation: `preflight_pass=1; postrepair_pass=1; evidence_quality_status=PASS`.

### Re-review unit G11-MANUAL-SAMPLE-30-PAGE-B

- Source page / original review location: `4` / `G11-MANUAL-SAMPLE-30-PAGE-B`.
- Historical source render: `reports/scale/g11_manual_sample_review/30_CUMCM-2002-B-005/page_B.png`.
- Historical artifact excerpt: `reports/scale/g11_manual_sample_review/30_CUMCM-2002-B-005/page_B_artifact_excerpt.txt`.
- Original formal page state: `present=0; char_count=0; line_count=0; sha256=E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855`.
- Current repaired formal excerpt: `reports/scale/g11_post_repair_human_rereview/11_CUMCM-2002-B-005/current_formal_p4.md`.
- Current page segment SHA256: `47E0FFA95AFF7FCECFF78CDE5099AD4AC867DA1F811315807DF213FD886967D6`.
- Repair page evidence: `catalog/scale/g11_residual_pdftotext_calibration/positive/CUMCM-2002-B-005/source_page_4.txt`.
- Repair evidence SHA256: `D5E6B1D6855D743D7F0F65DE4192052782A5C5CC6446A4065178EEAA3E799988`.
- Repair route/layer: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION` / `G11_MARKER_ONLY_PAGE_LOCAL_FORMAL_BODY`.
- Programmatic validation: `preflight_pass=1; postrepair_pass=1; evidence_quality_status=PASS`.

### Re-review unit G11-MANUAL-SAMPLE-30-PAGE-C

- Source page / original review location: `7` / `G11-MANUAL-SAMPLE-30-PAGE-C`.
- Historical source render: `reports/scale/g11_manual_sample_review/30_CUMCM-2002-B-005/page_C.png`.
- Historical artifact excerpt: `reports/scale/g11_manual_sample_review/30_CUMCM-2002-B-005/page_C_artifact_excerpt.txt`.
- Original formal page state: `present=0; char_count=0; line_count=0; sha256=E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855`.
- Current repaired formal excerpt: `reports/scale/g11_post_repair_human_rereview/11_CUMCM-2002-B-005/current_formal_p7.md`.
- Current page segment SHA256: `9C2C1E73E91AC8B844B2D9FEA54D06AAA55032DF54CCFE9F9879F8E252B43223`.
- Repair page evidence: `catalog/scale/g11_residual_pdftotext_calibration/positive/CUMCM-2002-B-005/source_page_7.txt`.
- Repair evidence SHA256: `C3575E2D7E3F2569A335DA9750A555717BDAA2EE4CC64F4519494FD1ED03B758`.
- Repair route/layer: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION` / `G11_MARKER_ONLY_PAGE_LOCAL_FORMAL_BODY`.
- Programmatic validation: `preflight_pass=1; postrepair_pass=1; evidence_quality_status=PASS`.

## Human Decision

`PENDING`

The human reviewer must select exactly one of PASS, MINOR, MAJOR, or CRITICAL in the new decision sheet and record the rationale. Codex has not classified this packet.

## Source Page Images

These are byte-for-byte copies of existing historical G11 source renders. They are provided as visual evidence for human rereview; this section asserts no severity or repair conclusion.

### G11-MANUAL-SAMPLE-30-PAGE-A

- Source page: `1`.
- Existing source image: [source_unit_01_p1.png](source_images/source_unit_01_p1.png).
- Current repaired formal excerpt: [current_formal_p1.md](current_formal_p1.md).
- Original issue: 源页面包含彩票模型正文和公式，artifact excerpt只保留页标记、没有实质文本，存在明显大段正文缺失。
- SHARED_SOURCE_IMAGE_BINDING=0.

### G11-MANUAL-SAMPLE-30-PAGE-B

- Source page: `4`.
- Existing source image: [source_unit_02_p4.png](source_images/source_unit_02_p4.png).
- Current repaired formal excerpt: [current_formal_p4.md](current_formal_p4.md).
- Original issue: 源页面包含彩票模型正文和公式，artifact excerpt只保留页标记、没有实质文本，存在明显大段正文缺失。
- SHARED_SOURCE_IMAGE_BINDING=0.

### G11-MANUAL-SAMPLE-30-PAGE-C

- Source page: `7`.
- Existing source image: [source_unit_03_p7.png](source_images/source_unit_03_p7.png).
- Current repaired formal excerpt: [current_formal_p7.md](current_formal_p7.md).
- Original issue: 源页面包含彩票模型正文和公式，artifact excerpt只保留页标记、没有实质文本，存在明显大段正文缺失。
- SHARED_SOURCE_IMAGE_BINDING=0.
