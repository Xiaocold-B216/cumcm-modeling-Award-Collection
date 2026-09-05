# G11 Marker-Only Final Visual Scope Review Guide

This is a human review gate for exactly three rendered source pages. Check
only the three PNGs in the review packet and then fill the corresponding rows
in `catalog/scale/g11_marker_only_final_visual_scope_decisions.csv`.

Use exactly one classification per page:

- `SUBSTANTIVE_CONTENT`: the image contains substantive paper content,
  including a title, formula, table, figure, caption, reference, appendix, or
  data.
- `LEGITIMATE_NONCONTENT`: the image contains only blank space, a watermark,
  QR code, advertisement, divider, or other non-paper material.
- `UNCLEAR`: the page cannot be determined reliably from the image.

Do not infer a classification from the prior OCR diagnostic class. The
initial `source_visual_classification` and `review_status` values are
intentionally `PENDING`; no Codex visual classification has been made.
