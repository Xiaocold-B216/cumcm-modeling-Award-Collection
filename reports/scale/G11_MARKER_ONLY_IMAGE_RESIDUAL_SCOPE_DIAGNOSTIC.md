# G11 Marker-Only Image Residual Scope Diagnostic

- Status: `PARTIAL`
- Render: `2951/2951` pages at `180` DPI using `D:\texlive\2026\bin\windows\pdftoppm.exe`.
- OCR: `2951` successful page children, `0` timeouts, `0` errors; auto retry `0`.
- Calibration: positive `82/82` substantive recovered, recall `1.0`; negative false positives `0`.
- OCR substantive classifier usable: `1`.

## Scope result

- OCR diagnostic substantive pages: `2948`; newly promoted defective pages: `2948` across `238` identities.
- Final confirmed marker-only population: `3030` pages / `245` identities.
- Final unresolved visual scope: `3` pages / `3` identities; manual visual review required for all unresolved pages.

## Residual classes

- `OCR_NON_SUBSTANTIVE_OR_EMPTY`: pages=3, identities=3

## Governance

Diagnostic OCR text and page images were written only to isolated G11 output directories. No OCR text was written to `paper.md`, metadata, formal registries, or indexes; no artifact repair or repromotion was performed. Empty OCR was not treated as legitimate blank evidence.

## Outputs

- `catalog/scale/g11_marker_only_image_residual_scope_diagnostic.csv`
- `catalog/scale/g11_marker_only_image_confirmed_repair_targets.csv`
- `catalog/scale/g11_marker_only_final_visual_residual_input.csv`
- `catalog/scale/g11_image_residual_renders`
- `catalog/scale/g11_image_residual_ocr`
- `reports/scale/g11_marker_only_final_visual_residual`
- `catalog/scale/g11_marker_only_image_residual_scope_diagnostic_result.json`
- `reports/scale/G11_MARKER_ONLY_IMAGE_RESIDUAL_SCOPE_DIAGNOSTIC.md`

## Next

`G11-MARKER-ONLY-FINAL-VISUAL-SCOPE-REVIEW`
