# G3-01R2 Identity Reconciliation

## Baseline

Stage: G3-01R2
Status: PASS
Started At: 2026-08-18T00:16:24+08:00
Completed At: 2026-08-18T00:16:50+08:00

Repository: D:\cumcm-modeling-Award-Collection
Branch: library-refactor-v1
HEAD: a042ecf898feaba6fc81d543a10e0188db8b2b12

## Duplicate Paper ID Audit

Previous Paper Rows: 675
Previous Unique IDs: 668
Previous Duplicate IDs: 7

Root Causes:
- Same Paper Rows: 7
- Internal ID Collision: 0
- Source ID Collision: 0
- Image Sequence: 0
- Other: 0

## Duplicate ID Repairs

Rows Collapsed: 7
Internal IDs Reassigned: 0
Source Conflicts Sent To Review: 0
Paper ID Changes: 0

## Image Sequence Reconciliation

Directories: 41
Formal: 2
Shared: 32
Exact Duplicate Paths: 0
Needs Review: 7
Excluded: 0
Unaccounted: 0

## Paper Registry After Repair

Formal Papers: 670
Unique Paper IDs: 670
Duplicate Paper IDs: 0

## Membership Integrity

Total Memberships: 2372
Multi-File Papers: 40

## Source Integrity

Total Sources: 14

## Safety

Original Files Modified: 0
Original Files Deleted: 0
Original Files Renamed/Moved: 0
Upstream Catalog Modified: 0

## Gate

- Duplicate Paper ID root cause identified: PASS
- FORMAL_PAPERS == UNIQUE_PAPER_IDS: PASS
- DUPLICATE_PAPER_IDS = 0: PASS
- All image sequence directories accounted: PASS
- IMAGE_SEQUENCE_UNACCOUNTED = 0: PASS
- Paper IDs unique: PASS
- Paper ID pattern valid: PASS
- Each Paper has at least one membership: PASS
- All membership foreign keys valid: PASS
- All membership SHA matches G1: PASS
- G1/G2/G3-00 upstream facts not modified: PASS
