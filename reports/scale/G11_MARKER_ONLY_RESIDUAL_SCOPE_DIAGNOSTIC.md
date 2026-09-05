# G11 Marker-Only Residual Scope Diagnostic

- Stage: `G11-MARKER-ONLY-RESIDUAL-SCOPE-DIAGNOSTIC`
- Status: `PARTIAL`
- Branch / HEAD: `library-refactor-v1` / `557724fba6572d4d83dc421feda5b17b13ff8d66`
- Attempt: `g11-marker-only-residual-scope-diagnostic-f6288a9bd9006c8c`

## Scope and method

The frozen residual input contains 2951 unique paper/page rows, all previously `UNRESOLVED`. The input key set was compared exactly with the prior scope output; add, delete, and replace counts are all zero.
Each page was probed independently with `pdftotext -f N -l N -enc UTF-8 input.pdf -` using the frozen executable `D:\texlive\2026\bin\windows\pdftotext.exe`. The per-page timeout was 60 seconds. No OCR, PDF rendering, pdf-inspector extraction, formal extraction, or visual judgment was performed.

## Identity metrics before the exact-page probe

- Any unresolved page: 238 identities.
- Unresolved-only: 215 identities.
- Confirmed identities with residual unresolved pages: 23.
- Confirmed identities with no residual unresolved pages: 7.

The earlier value of 235 was the identity count attached to the 3,004-page unresolved population before the targeted visual sample was promoted. The current value of 238 is calculated over the current 2,951-page residual complement after 82 pages were confirmed. The difference is a metric-scope/timepoint change, not a change to source or identity data.

## Calibration

Positive calibration used 82 previously confirmed pages; substantive text was recovered on 0 and not recovered on 82.
Negative calibration used 4 existing verified-blank pages; false substantive classifications: 0.
Empty or noise-only page-scoped output was retained as unresolved. It was never promoted to legitimate noncontent solely because text was absent.

## Probe classification

- `TEXT_LAYER_SUBSTANTIVE`: 0
- `TEXT_LAYER_NON_SUBSTANTIVE_OR_EMPTY`: 0
- `TEXT_LAYER_GARBLED_OR_UNRELIABLE`: 2951
- `TEXT_PROBE_TIMEOUT`: 0
- `TEXT_PROBE_ERROR`: 0

## Residual classes

- `TEXT_LAYER_GARBLED`: page_count=2951; identity_count=238

Newly confirmed pages: 0; final unresolved pages: 2951. The residual image/text-empty input was written only for unresolved pages and remains outside repair scope.

## Safety and governance gates

Source PDFs were checked read-only for existence, SHA256, and page validity. Formal bodies, artifacts, identity/membership/eligibility registries, decision sheets, backlog, G9/G10 outputs, and frozen samples were not modified. No dependency installation, network access, OCR, rendering, Word, or formal artifact generation occurred.

## Outputs

- `catalog/scale/g11_marker_only_residual_scope_diagnostic.csv`
- `catalog/scale/g11_marker_only_image_residual_input.csv`
- `catalog/scale/g11_marker_only_residual_scope_diagnostic_result.json`
- `reports/scale/G11_MARKER_ONLY_RESIDUAL_SCOPE_DIAGNOSTIC.md`
- `catalog/scale/g11_residual_pdftotext_pages`
- `catalog/scale/g11_residual_pdftotext_calibration/positive`
- `catalog/scale/g11_residual_pdftotext_calibration/negative`

## Next

`G11-MARKER-ONLY-IMAGE-RESIDUAL-SCOPE-DIAGNOSTIC`
