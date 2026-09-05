# G11 Targeted Visual Diagnostic Review Guide

## Purpose

This guide accompanies `catalog/scale/g11_targeted_visual_diagnostic_decisions.csv` and the 20 visual packets under `reports/scale/g11_targeted_visual_diagnostic`. It is an evidence-preparation stage, not a formal artifact repair and not a machine visual decision.

Frozen sample identities: `20`. Rendered source pages: `53` at `180` DPI using `D:\texlive\2026\bin\windows\pdftoppm.exe`. The render budget is at most `60` pages.

## One decision per page

For each `page_X.png`, answer only:

> Does this source page contain substantive paper content that should enter the formal paper database?

Use exactly one human classification:

- `SUBSTANTIVE_CONTENT`: body text, headings, formulas, tables, code, figures/captions, references, appendices, or other paper content.
- `LEGITIMATE_NONCONTENT`: blank/scan blank, QR code, watermark, advertisement, divider, or page without paper content.
- `UNCLEAR`: the page cannot be classified reliably.

Do not infer a classification from the current formal excerpt. The formal excerpts are existing evidence only and are expected to be marker-only for this sample. Do not change the original G11 decision sheet.

## How to record review

Review each page in `reports/scale/g11_targeted_visual_diagnostic` or the contact sheets in `reports/scale/g11_targeted_visual_diagnostic/contact_sheets`. After a human checks a page, update only the corresponding `source_visual_classification`, optional short `reviewer_comment`, and `review_status` in `catalog/scale/g11_targeted_visual_diagnostic_decisions.csv`. Until then every row must remain `PENDING`.

If a page is `SUBSTANTIVE_CONTENT` and its formal excerpt remains marker-only, the later repair stage may classify it as `DEFECTIVE_CONTENT_MISSING`. If it is `LEGITIMATE_NONCONTENT`, the later stage may classify it as `LEGITIMATE_BLANK_NONCONTENT`. `UNCLEAR` requires further targeted diagnosis. Those later classifications are not entered in this preparation stage.

## Scope and safety

All PNGs are complete single-page renders of the original source PDFs; no crop, enhancement, annotation, OCR, text extraction, or source modification was performed. The 20 identities and selected pages are frozen by `catalog/scale/g11_deep_diagnostic_visual_sample.csv`.

## Review Status

The targeted visual diagnostic review status contract is frozen as follows:

PENDING
- 尚未完成人工审核

REVIEWED
- 已由真人完成审核

完成审核后：
`review_status=REVIEWED`

`review_status` and `source_visual_classification` are separate fields. `review_status` records whether the human visual review was completed; `source_visual_classification` records the reviewed source-page classification. The classification remains `PENDING` until the human decision is recorded and is then one of `SUBSTANTIVE_CONTENT`, `LEGITIMATE_NONCONTENT`, or `UNCLEAR`. `review_status` must not be used as a content classification and must not take any value other than `PENDING` or `REVIEWED`.
