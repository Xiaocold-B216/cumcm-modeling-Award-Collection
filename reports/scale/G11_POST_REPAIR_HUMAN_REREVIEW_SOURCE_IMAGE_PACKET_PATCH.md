# G11 Post-Repair Human Rereview Source Image Packet Patch

## Purpose

The preparation stage produced the correct Markdown evidence but did not place the already-rendered source-page PNGs inside the new packet directories. This patch adds only byte-for-byte copies of those historical PNGs and explicit local links, so a human can inspect each original source page beside the repaired formal excerpt.

## Evidence source and operation boundary

All 33 images came from the original authoritative G11 review packets (`reports/scale/g11_manual_sample_review/*`). No new render, OCR, extraction, annotation, recompression, Word operation, network operation, or dependency installation was performed.

## Binding and coverage

The 33 rereview units were recovered from the current post-repair packet unit references and bound to their original historical Page A/B/C render. Each destination name contains the source page number. The repeated source page in CUMCM-1993-B-001 is recorded as a legitimate shared-page binding, while each unit still has its own deterministic copied PNG.

- Targets: `11`
- Rereview units: `33`
- Source PNGs located/checked: `33`
- PNG copies with matching SHA256: `33`
- Updated packets: `11`

## Packet changes

Each packet received a `source_images/` directory. `REVIEW.md` now links each source page image to its corresponding current formal excerpt and repeats the original issue summary. `before_after.md` retains its existing historical/current content and gains only a source-image link section. `00_OVERVIEW.md` gains `SOURCE_IMAGE_STATUS=READY` while decision status remains PENDING.

## ZIP

The complete ZIP is `reports/scale/g11_post_repair_human_rereview_with_source_images.zip` with `90` entries: `57` Markdown files and `33` PNG files. ZIP opening and CRC validation passed; no PDF, DOC, catalog, cache, staging backup, or Git metadata was included.

## Decision boundary

The post-repair decision sheet SHA256 remained unchanged before/after: `9F81352331BCDEF28F95FAAC7D6EF53AFDC20470CA867BC9C9B98DF48A05DC55`. All 11 rows remain `new_severity=PENDING`, empty `reviewer_comment`, and `review_status=PENDING`. Codex made no visual or severity judgment. Human rereview is still required, so G11 remains PARTIAL.

## Next action

Open the ZIP or the local packet directory, inspect the original source PNG and linked repaired excerpt for each unit, and provide the identity-level PASS/MINOR/MAJOR/CRITICAL decision in the separate human approval stage.
