# G11 Targeted Visual Diagnostic Approval

## Stage and evidence chain

`G11-TARGETED-VISUAL-DIAGNOSTIC-APPROVAL`

This approval consumes the completed transcription resume
`g11-targeted-visual-manual-decision-transcription-resume-f6288a9bd9006c8c`.
The targeted visual preparation is frozen by attempt
`g11-targeted-visual-diagnostic-ab46dea43f4ccbcd` and fingerprint
`AB46DEA43F4CCBCD2DA82CAA0AE3F5318A9BE68E789C140B5AE6BF86D3B71729`.

## Human decision and provenance

The user completed the visual review of all 53 selected source pages and supplied the authoritative decision that every page contains substantive paper content. The approved counts are:

- `SUBSTANTIVE_CONTENT`: 53/53
- `LEGITIMATE_NONCONTENT`: 0/53
- `UNCLEAR`: 0/53
- `REVIEWED`: 53/53

Codex did not independently inspect or classify the pages. Codex only transcribed and validated the user's explicit human visual decisions.

## Sample and identity aggregation

The decision sheet retains 53 rows, 53 unique paper/page keys, and the manifest binding matches in row count, order, paper/page key, and identity set. The 53 pages cover 20 sampled identities. Each sampled identity has at least one substantive selected page, and all selected pages for all 20 identities are substantive:

- identities with a substantive page: `20`
- identities with all selected pages substantive: `20`
- identities with legitimate noncontent: `0`
- identities with unclear pages: `0`

The targeted sample substantive rate is `53/53` (`1.0`). This is diagnostic evidence, not a statistical proof for the full unresolved population.

## Sampled defect confirmation and lower bounds

Under the frozen `PAGE_LOCAL_STRICT_BOUNDARY` marker semantics, each sampled page has source evidence of substantive content while its formal page segment remains marker-only. Therefore these 53 sampled pages are newly confirmed `CONFIRMED_DEFECTIVE_CONTENT_MISSING` pages for governance scope purposes. No formal artifact repair was performed.

The 53 sampled pages have no overlap with the previous 29 confirmed defective pages, and the 20 sampled identities have no overlap with the previous 10 confirmed defective identities. The confirmed lower bounds therefore become:

- confirmed defective pages: `29 + 53 = 82`
- confirmed affected identities: `10 + 20 = 30`

These are lower bounds, not a claim that all pages of the affected identities are repaired or confirmed.

## Population limitation

The previous unresolved population was 3,004 marker-only pages across 235 unresolved identities. The 53/53 sample does not authorize the statement that all 3,004 pages are defective, nor that all 235 identities are confirmed defective. The correct status is:

`ALL_3004_UNRESOLVED_PAGES_DEFECTIVE=UNPROVEN`

`POPULATION_LEVEL_DEFECT_INFERENCE_AUTHORIZED=0`

The deterministic 20-identity sample establishes strong diagnostic evidence that marker-only segments pose a systematic source-presence risk; it does not replace page-level scope confirmation.

## Scope-confirmation input

The next scope-confirmation input is
`catalog/scale/g11_marker_only_scope_confirmation_input.csv`. It contains 2,951 unique pages that were previously unresolved and are not among the 53 newly confirmed sampled pages. Every row remains `current_scope_status=UNRESOLVED`.

The input binds each page to existing identity/source/formal metadata and records marker presence, formal substantive-content presence, source route, governed-duplicate status, existing page classification, extraction/render/visual evidence availability, and current scope status. No unresolved page was automatically relabeled defective.

Existing source hashes, formal page-local metadata, persisted extraction evidence where available, and existing render evidence can support a deterministic evidence-based scope pass for residual classes. Pages that remain ambiguous after those checks may require targeted visual review; another generic sample must not be selected before scope confirmation identifies a specific residual class.

## Gate status and safety

`TARGETED_VISUAL_DIAGNOSTIC_FINAL_STATUS=PASS`

`MANUAL_VISUAL_REVIEW_STATUS=PASS`

`G11_STATUS_REMAINS=PARTIAL`

G11 remains partial because the original 11 MAJOR findings and formal artifact repair remain open. The decision sheet SHA256 was unchanged during approval:

`F6288A9BD9006C8CF17B7281F8CC18217E9F70AFD79B5CF20F678D5B50966047`

The original G11 decision sheet, formal data, formal artifacts, index, identity, membership, eligibility, backlog, and source files were not modified. No OCR, rendering, extraction, formal repair, artifact regeneration, G9, G10, G12, network, dependency installation, Word, or print operation was run.

`BLOCKER=NONE`

`NEXT=G11-MARKER-ONLY-SCOPE-CONFIRMATION`

The machine-readable approval evidence is recorded in
`catalog/scale/g11_targeted_visual_diagnostic_approval_result.json`.
