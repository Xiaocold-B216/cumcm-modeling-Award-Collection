# CUMCM-1996-B-001

This packet prepares post-repair human rereview. It makes no post-repair severity decision.

## Original G11 Major Finding

- Original severity: `MAJOR`.
- Original decision reference: `catalog/scale/g11_manual_sample_decisions.csv:paper_id=CUMCM-1996-B-001;sample_order=25`.
- Original review packet: `reports/scale/g11_manual_sample_review/25_CUMCM-1996-B-001/review.md`.
- Original reviewer comment: 源页面包含完整正文与公式，但artifact excerpt没有对应文本，仅保留source_page标记。属于实质正文缺失，而非轻微OCR错误。
- Original defect description: 源页面包含完整正文与公式，但artifact excerpt没有对应文本，仅保留source_page标记。属于实质正文缺失，而非轻微OCR错误。
- Root-cause category retained from authoritative triage: `FORMAL_ARTIFACT_PAGE_CONTENT_MISSING`.

## Repair Summary

- Repair route: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION;MARKER_ONLY_DIAGNOSTIC_OCR_REUSE`.
- Repair layer: `G11_MARKER_ONLY_PAGE_LOCAL_FORMAL_BODY`.
- Repaired pages: `1;2;3;4;5`.
- Historical body SHA256 before repair: `1D9182549363CD07A8F3D657C2AD60D5197D3991577AD22ACB1BFC0A2C456E59`.
- Current body SHA256 after repair: `C0E0C7FB83EF4607F0545A1D026AD455AB54F15DD405A38DD5D6654B44C00E62`.
- Repair attempt: `20260905T045418589698Z_557724fba657`.
- Current artifact set: `derived/scale/papers/CUMCM-1996-B-001`.
- Current formal body: `derived/scale/papers/CUMCM-1996-B-001/paper.md`.
- Repair provenance: `catalog/scale/g11_multi_route_formal_repair_targets.csv`.

## Human Re-review Evidence

Review only whether the original MAJOR issue has been resolved. The page-level evidence below is programmatic binding evidence, not a replacement for human visual/semantic review.

### Re-review unit G11-MANUAL-SAMPLE-25-PAGE-A

- Source page / original review location: `1` / `G11-MANUAL-SAMPLE-25-PAGE-A`.
- Historical source render: `reports/scale/g11_manual_sample_review/25_CUMCM-1996-B-001/page_A.png`.
- Historical artifact excerpt: `reports/scale/g11_manual_sample_review/25_CUMCM-1996-B-001/page_A_artifact_excerpt.txt`.
- Original formal page state: `present=0; char_count=0; line_count=0; sha256=E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855`.
- Current repaired formal excerpt: `reports/scale/g11_post_repair_human_rereview/06_CUMCM-1996-B-001/current_formal_p1.md`.
- Current page segment SHA256: `4CD667F4EB18C3FD83C4C366011442EE9383A856A916518D099BE3171F223230`.
- Repair page evidence: `catalog/scale/g11_residual_pdftotext_calibration/positive/CUMCM-1996-B-001/source_page_1.txt`.
- Repair evidence SHA256: `59CF42EE461FA4961FC6FB06D4530812061A2E412096E63E00A4A94197A8D092`.
- Repair route/layer: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION` / `G11_MARKER_ONLY_PAGE_LOCAL_FORMAL_BODY`.
- Programmatic validation: `preflight_pass=1; postrepair_pass=1; evidence_quality_status=PASS`.

### Re-review unit G11-MANUAL-SAMPLE-25-PAGE-B

- Source page / original review location: `3` / `G11-MANUAL-SAMPLE-25-PAGE-B`.
- Historical source render: `reports/scale/g11_manual_sample_review/25_CUMCM-1996-B-001/page_B.png`.
- Historical artifact excerpt: `reports/scale/g11_manual_sample_review/25_CUMCM-1996-B-001/page_B_artifact_excerpt.txt`.
- Original formal page state: `present=0; char_count=0; line_count=0; sha256=E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855`.
- Current repaired formal excerpt: `reports/scale/g11_post_repair_human_rereview/06_CUMCM-1996-B-001/current_formal_p3.md`.
- Current page segment SHA256: `1898278FB519EC4C2E311D81B88AF47CFF374513D773C8DC00DD68A0CC590A23`.
- Repair page evidence: `catalog/scale/g11_residual_pdftotext_calibration/positive/CUMCM-1996-B-001/source_page_3.txt`.
- Repair evidence SHA256: `EBC77A051585BE278BF03BB34D45EA109A6B742E561B6EDB24F3E10389E9EC67`.
- Repair route/layer: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION` / `G11_MARKER_ONLY_PAGE_LOCAL_FORMAL_BODY`.
- Programmatic validation: `preflight_pass=1; postrepair_pass=1; evidence_quality_status=PASS`.

### Re-review unit G11-MANUAL-SAMPLE-25-PAGE-C

- Source page / original review location: `5` / `G11-MANUAL-SAMPLE-25-PAGE-C`.
- Historical source render: `reports/scale/g11_manual_sample_review/25_CUMCM-1996-B-001/page_C.png`.
- Historical artifact excerpt: `reports/scale/g11_manual_sample_review/25_CUMCM-1996-B-001/page_C_artifact_excerpt.txt`.
- Original formal page state: `present=0; char_count=0; line_count=0; sha256=E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855`.
- Current repaired formal excerpt: `reports/scale/g11_post_repair_human_rereview/06_CUMCM-1996-B-001/current_formal_p5.md`.
- Current page segment SHA256: `E683E4D2C06FD0E0B4C53AB35755A1C44024F95244E084DDA7D7C5AF2B3DD5DB`.
- Repair page evidence: `catalog/scale/g11_residual_pdftotext_calibration/positive/CUMCM-1996-B-001/source_page_5.txt`.
- Repair evidence SHA256: `DE61E2AA2B098C579B5A1803157DFF842328B424A66ED8EBC7654D6E60EDF472`.
- Repair route/layer: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION` / `G11_MARKER_ONLY_PAGE_LOCAL_FORMAL_BODY`.
- Programmatic validation: `preflight_pass=1; postrepair_pass=1; evidence_quality_status=PASS`.

## Human Decision

`PENDING`

The human reviewer must select exactly one of PASS, MINOR, MAJOR, or CRITICAL in the new decision sheet and record the rationale. Codex has not classified this packet.

## Source Page Images

These are byte-for-byte copies of existing historical G11 source renders. They are provided as visual evidence for human rereview; this section asserts no severity or repair conclusion.

### G11-MANUAL-SAMPLE-25-PAGE-A

- Source page: `1`.
- Existing source image: [source_unit_01_p1.png](source_images/source_unit_01_p1.png).
- Current repaired formal excerpt: [current_formal_p1.md](current_formal_p1.md).
- Original issue: 源页面包含完整正文与公式，但artifact excerpt没有对应文本，仅保留source_page标记。属于实质正文缺失，而非轻微OCR错误。
- SHARED_SOURCE_IMAGE_BINDING=0.

### G11-MANUAL-SAMPLE-25-PAGE-B

- Source page: `3`.
- Existing source image: [source_unit_02_p3.png](source_images/source_unit_02_p3.png).
- Current repaired formal excerpt: [current_formal_p3.md](current_formal_p3.md).
- Original issue: 源页面包含完整正文与公式，但artifact excerpt没有对应文本，仅保留source_page标记。属于实质正文缺失，而非轻微OCR错误。
- SHARED_SOURCE_IMAGE_BINDING=0.

### G11-MANUAL-SAMPLE-25-PAGE-C

- Source page: `5`.
- Existing source image: [source_unit_03_p5.png](source_images/source_unit_03_p5.png).
- Current repaired formal excerpt: [current_formal_p5.md](current_formal_p5.md).
- Original issue: 源页面包含完整正文与公式，但artifact excerpt没有对应文本，仅保留source_page标记。属于实质正文缺失，而非轻微OCR错误。
- SHARED_SOURCE_IMAGE_BINDING=0.
