# G11 Manual Sample Preparation Reconcile

## Decision

- Status: `BLOCKED`
- Reconcile attempt: `20260904T112915417775_ee5a9eb7`
- Blocker: `G11_ATTEMPT_LINEAGE_UNRECOVERABLE`
- No Approval Resume, G8 repair, OCR, rendering, artifact generation, or G12 run was executed.

## Attempt evidence

- Old expected attempt: `20260903T171602418687_17165c0c` — no matching attempt/result/checkpoint/manifest/precheck/packet/log file was found in the repository.
- Current stored attempt: `20260903T172404115633_3c748bc1` — represented by the current G11 result, manifest, precheck, and 30-packet tree.
- Attempt lineage classification: `UNKNOWN`.
- Why stored attempt changed: UNKNOWN: the old attempt has no recoverable attempt/result/checkpoint/manifest/precheck/review-packet/log evidence in the workspace; the current result is a later timestamp, but the available evidence cannot distinguish rerun, refinalization, recovery, or new generation.
- The old attempt is not marked SUPERSEDED because its historical evidence is not recoverable.

## Sample comparison

- Old attempt sample count: `30` (user specification only; ordered identity list not recovered).
- Current attempt sample count: `30`.
- Identity-set match: `UNVERIFIED_HISTORICAL_EVIDENCE`.
- Identity-order match: `UNVERIFIED_HISTORICAL_EVIDENCE`.
- Page-selection match count/mismatch count: `UNVERIFIED_HISTORICAL_EVIDENCE` / `UNVERIFIED_HISTORICAL_EVIDENCE`.
- Old fingerprint: `677898FA2C0DE5B8229AC310566A2D0A41465790B5F188320CD2EE46C877D4EF` (user-specified value only).
- Current recomputed fingerprint: `677898FA2C0DE5B8229AC310566A2D0A41465790B5F188320CD2EE46C877D4EF`.
- Fingerprint value match: `1`; this does not establish attempt lineage by itself.

## Current evidence inventory

- Current manifest SHA256: `12FF62A2FD78AE736CD31C956AC817C9868BDE91702208BC2AC421082A40FCDE`; old manifest SHA256: `UNVERIFIED_HISTORICAL_EVIDENCE`.
- Manifest byte-level match: `UNVERIFIED_HISTORICAL_EVIDENCE`.
- Current precheck all PASS: `1`; old/current precheck equivalence: `UNVERIFIED_HISTORICAL_EVIDENCE`.
- Current packet tree: `30` packet directories, `210` files, semantic shape pass=`1`.
- Current packet fingerprint: `929126E088182CDFA0482107A0EE40CAC1FAF76216C0B2065A22D6D543B15042`.
- Old packet fingerprint recoverable: `0`.

## Manual decision applicability

- Reviewed=`30`, pending=`0`, PASS=`2`, MINOR=`17`, MAJOR=`11`, CRITICAL=`0`.
- Decision sheet SHA256 before/after: `8078A66F45C0C58F9BA4CF0C85BEB0E331C2BC405C52B93760B999DE00A8FD21` / `8078A66F45C0C58F9BA4CF0C85BEB0E331C2BC405C52B93760B999DE00A8FD21`; unchanged=`1`.
- Decision content/severity/review-status modification counts: `0/0/0`.
- MAJOR affected-paper list unchanged: `1`.
- The decisions are demonstrably complete for the current files, but their applicability to the unrecovered old attempt cannot be established byte-for-byte.

## No-op boundary

- Formal data/artifact/index/identity/membership/eligibility/backlog/source modification counts are all `0`.
- OCR, PDF render, PDF extraction, body reconstruction, formal artifact generation, G9, G10, G12, Word, network, download, and dependency installation counts are all `0`.

## Outputs

- `catalog\scale\g11_manual_sample_preparation_reconcile_result.json`
- `catalog\scale\g11_manual_sample_attempt_lineage.csv`
- `reports\scale\G11_MANUAL_SAMPLE_PREPARATION_RECONCILE.md`

## Required next evidence

- Restore or provide the original 171602 attempt's machine-readable result/manifest/precheck and review-packet evidence, or an authoritative immutable hash/lineage record covering them.
- Do not run `G11-MANUAL-SAMPLE-APPROVAL-RESUME` until lineage is resolved.
