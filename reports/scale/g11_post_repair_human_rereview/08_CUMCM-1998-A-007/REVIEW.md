# CUMCM-1998-A-007

This packet prepares post-repair human rereview. It makes no post-repair severity decision.

## Original G11 Major Finding

- Original severity: `MAJOR`.
- Original decision reference: `catalog/scale/g11_manual_sample_decisions.csv:paper_id=CUMCM-1998-A-007;sample_order=27`.
- Original review packet: `reports/scale/g11_manual_sample_review/27_CUMCM-1998-A-007/review.md`.
- Original reviewer comment: 源页面可见正文、公式及数据表，而artifact excerpt只有页标记、没有实质文本，存在明显正文/表格内容缺失。
- Original defect description: 源页面可见正文、公式及数据表，而artifact excerpt只有页标记、没有实质文本，存在明显正文/表格内容缺失。
- Root-cause category retained from authoritative triage: `FORMAL_ARTIFACT_PAGE_CONTENT_MISSING`.

## Repair Summary

- Repair route: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION;MARKER_ONLY_DIAGNOSTIC_OCR_REUSE`.
- Repair layer: `G11_MARKER_ONLY_PAGE_LOCAL_FORMAL_BODY`.
- Repaired pages: `1;2;3;4;5`.
- Historical body SHA256 before repair: `1D9182549363CD07A8F3D657C2AD60D5197D3991577AD22ACB1BFC0A2C456E59`.
- Current body SHA256 after repair: `34FFD0C7AF3CCAEA34794C03CC2D9EA755C84976D568974A83B0E6C37C3BE72C`.
- Repair attempt: `20260905T045418589698Z_557724fba657`.
- Current artifact set: `derived/scale/papers/CUMCM-1998-A-007`.
- Current formal body: `derived/scale/papers/CUMCM-1998-A-007/paper.md`.
- Repair provenance: `catalog/scale/g11_multi_route_formal_repair_targets.csv`.

## Human Re-review Evidence

Review only whether the original MAJOR issue has been resolved. The page-level evidence below is programmatic binding evidence, not a replacement for human visual/semantic review.

### Re-review unit G11-MANUAL-SAMPLE-27-PAGE-A

- Source page / original review location: `1` / `G11-MANUAL-SAMPLE-27-PAGE-A`.
- Historical source render: `reports/scale/g11_manual_sample_review/27_CUMCM-1998-A-007/page_A.png`.
- Historical artifact excerpt: `reports/scale/g11_manual_sample_review/27_CUMCM-1998-A-007/page_A_artifact_excerpt.txt`.
- Original formal page state: `present=0; char_count=0; line_count=0; sha256=E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855`.
- Current repaired formal excerpt: `reports/scale/g11_post_repair_human_rereview/08_CUMCM-1998-A-007/current_formal_p1.md`.
- Current page segment SHA256: `4B19983960725F4D6D8C715C9A8BCB7B57CAA1B5BBECE11B22640E1441DF692F`.
- Repair page evidence: `catalog/scale/g11_residual_pdftotext_calibration/positive/CUMCM-1998-A-007/source_page_1.txt`.
- Repair evidence SHA256: `249287DA407FB54A58993E32C036BD776D0F892780A47A2FA04123CF6F474260`.
- Repair route/layer: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION` / `G11_MARKER_ONLY_PAGE_LOCAL_FORMAL_BODY`.
- Programmatic validation: `preflight_pass=1; postrepair_pass=1; evidence_quality_status=PASS`.

### Re-review unit G11-MANUAL-SAMPLE-27-PAGE-B

- Source page / original review location: `3` / `G11-MANUAL-SAMPLE-27-PAGE-B`.
- Historical source render: `reports/scale/g11_manual_sample_review/27_CUMCM-1998-A-007/page_B.png`.
- Historical artifact excerpt: `reports/scale/g11_manual_sample_review/27_CUMCM-1998-A-007/page_B_artifact_excerpt.txt`.
- Original formal page state: `present=0; char_count=0; line_count=0; sha256=E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855`.
- Current repaired formal excerpt: `reports/scale/g11_post_repair_human_rereview/08_CUMCM-1998-A-007/current_formal_p3.md`.
- Current page segment SHA256: `DD29C4E52F4509C8C4AD2219F33CFA94DA2646B9D4EFD01203042AF78EB0C205`.
- Repair page evidence: `catalog/scale/g11_residual_pdftotext_calibration/positive/CUMCM-1998-A-007/source_page_3.txt`.
- Repair evidence SHA256: `9CC3C5AF9991A69DA85B45DE938701665CEEE5FA5580AC81D166957C64FA6DC4`.
- Repair route/layer: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION` / `G11_MARKER_ONLY_PAGE_LOCAL_FORMAL_BODY`.
- Programmatic validation: `preflight_pass=1; postrepair_pass=1; evidence_quality_status=PASS`.

### Re-review unit G11-MANUAL-SAMPLE-27-PAGE-C

- Source page / original review location: `5` / `G11-MANUAL-SAMPLE-27-PAGE-C`.
- Historical source render: `reports/scale/g11_manual_sample_review/27_CUMCM-1998-A-007/page_C.png`.
- Historical artifact excerpt: `reports/scale/g11_manual_sample_review/27_CUMCM-1998-A-007/page_C_artifact_excerpt.txt`.
- Original formal page state: `present=0; char_count=0; line_count=0; sha256=E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855`.
- Current repaired formal excerpt: `reports/scale/g11_post_repair_human_rereview/08_CUMCM-1998-A-007/current_formal_p5.md`.
- Current page segment SHA256: `90A341F9A5DEE960591DEBD164D85E6108CD454CB2A3EF59B3B536574CD91092`.
- Repair page evidence: `catalog/scale/g11_residual_pdftotext_calibration/positive/CUMCM-1998-A-007/source_page_5.txt`.
- Repair evidence SHA256: `5342A67DA416B8C183F0F8A78F7D4A09BF106492644AAB61C987648BD22B2EBA`.
- Repair route/layer: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION` / `G11_MARKER_ONLY_PAGE_LOCAL_FORMAL_BODY`.
- Programmatic validation: `preflight_pass=1; postrepair_pass=1; evidence_quality_status=PASS`.

## Human Decision

`PENDING`

The human reviewer must select exactly one of PASS, MINOR, MAJOR, or CRITICAL in the new decision sheet and record the rationale. Codex has not classified this packet.

## Source Page Images

These are byte-for-byte copies of existing historical G11 source renders. They are provided as visual evidence for human rereview; this section asserts no severity or repair conclusion.

### G11-MANUAL-SAMPLE-27-PAGE-A

- Source page: `1`.
- Existing source image: [source_unit_01_p1.png](source_images/source_unit_01_p1.png).
- Current repaired formal excerpt: [current_formal_p1.md](current_formal_p1.md).
- Original issue: 源页面可见正文、公式及数据表，而artifact excerpt只有页标记、没有实质文本，存在明显正文/表格内容缺失。
- SHARED_SOURCE_IMAGE_BINDING=0.

### G11-MANUAL-SAMPLE-27-PAGE-B

- Source page: `3`.
- Existing source image: [source_unit_02_p3.png](source_images/source_unit_02_p3.png).
- Current repaired formal excerpt: [current_formal_p3.md](current_formal_p3.md).
- Original issue: 源页面可见正文、公式及数据表，而artifact excerpt只有页标记、没有实质文本，存在明显正文/表格内容缺失。
- SHARED_SOURCE_IMAGE_BINDING=0.

### G11-MANUAL-SAMPLE-27-PAGE-C

- Source page: `5`.
- Existing source image: [source_unit_03_p5.png](source_images/source_unit_03_p5.png).
- Current repaired formal excerpt: [current_formal_p5.md](current_formal_p5.md).
- Original issue: 源页面可见正文、公式及数据表，而artifact excerpt只有页标记、没有实质文本，存在明显正文/表格内容缺失。
- SHARED_SOURCE_IMAGE_BINDING=0.
