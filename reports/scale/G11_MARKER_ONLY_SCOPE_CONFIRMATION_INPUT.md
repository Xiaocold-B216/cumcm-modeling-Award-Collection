# G11 Marker-Only Scope Confirmation Input

## Purpose

This input is the controlled handoff from `G11-TARGETED-VISUAL-DIAGNOSTIC-APPROVAL` to `G11-MARKER-ONLY-SCOPE-CONFIRMATION`. It covers the residual marker-only pages that remain unconfirmed after the user's targeted visual review.

## Evidence boundary

The targeted visual review established `53/53 SUBSTANTIVE_CONTENT` across 20 deterministic sampled identities. Those 53 pages are excluded from this residual input because they are already confirmed for defect scope. The result does not authorize classifying all other marker-only pages as defective.

The previous diagnostic inventory contained 3,033 marker-only pages: 29 previously confirmed defective pages and 3,004 unresolved pages. The 53 newly confirmed sampled pages have zero page overlap with the previous 29 confirmed pages, leaving 2,951 unresolved pages for this input. The input has 2,951 unique `(paper_id, source_page)` keys.

## Input contract

`catalog/scale/g11_marker_only_scope_confirmation_input.csv` contains, for each residual page:

- identity and source binding: `paper_id`, `year`, `problem`, `source_page`, `source_path`, `source_sha256`
- formal binding: `artifact_set_id`, `formal_body_path`, `formal_body_sha256`, `formal_marker_present`, `formal_substantive_content_present`
- governance/evidence route: `source_route`, `governed_duplicate_status`, `existing_page_classification`, `existing_page_text_path`
- evidence availability: `existing_extraction_evidence_available`, `existing_render_evidence_available`, `existing_visual_review_available`
- controlled state: `current_scope_status`

All rows currently have `current_scope_status=UNRESOLVED`. The allowed status vocabulary is `CONFIRMED_DEFECTIVE`, `CONFIRMED_LEGITIMATE_NONCONTENT`, and `UNRESOLVED`; no unresolved row was automatically promoted.

## Recommended scope-confirmation questions

Use existing deterministic source/formal metadata and persisted evidence first to identify pages that can be confirmed without another generic sample. In particular, check whether page-local source-presence evidence, source hashes, formal marker boundaries, existing extraction evidence, or already persisted render evidence can establish a page-level conclusion. Keep the page-level binding and identity-level aggregation explicit.

Only a residual class that cannot be resolved from those existing evidence routes should be considered for further visual review. Do not infer a population-wide defect rate from the 53-page sample, and do not start formal artifact repair until the repair population is explicitly scoped.

## Current handoff

- targeted sample: `53/53` substantive pages
- confirmed defective page lower bound: `82`
- confirmed affected identity lower bound: `30`
- residual scope-confirmation pages: `2,951`
- residual scope-confirmation identities: `238` unique identities in the input; this includes identities with earlier confirmed pages that still retain unresolved pages
- all residual rows: `UNRESOLVED`
- next stage: `G11-MARKER-ONLY-SCOPE-CONFIRMATION`

No OCR, formal repair, body reconstruction, artifact regeneration, G9, G10, or G12 operation is authorized by this handoff.
