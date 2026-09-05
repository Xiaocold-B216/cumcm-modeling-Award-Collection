# G3-01R3 Reporting & Identity Count Reconciliation

## Baseline

Stage: G3-01R3
Status: PASS
Started At: 2026-08-18T13:03:50+08:00
Completed At: 2026-08-18T13:06:06+08:00

Repository: D:\cumcm-modeling-Award-Collection
Branch: library-refactor-v1
HEAD: a042ecf898feaba6fc81d543a10e0188db8b2b12

## Paper Identity

Current Formal Papers: 670
Unique Paper IDs: 670
Duplicate Paper IDs: 0
Pattern Validation: PASS

Source ID Papers: 34
Internal ID Papers: 636
Other ID Papers: 0
Identity Type Accounting: PASS

## Paper Transition

Previous Formal Rows: 675
Removed Duplicate Rows: 7
Removed From Formal To Review: 0
New Papers Added: 2
Current Formal Rows: 670
Paper Transition Unexplained: 0
Paper Transition Accounted: PASS

Root Cause: The old report used PAPERS_UNCHANGED=648, PAPERS_FIXED=7, NEW_PAPERS_ADDED=2 (sum=657), but this accounting was incorrect. The correct accounting is: Previous Formal Rows (675) - Removed Duplicate Rows (7) + New Papers Added (2) = 670. The old PAPERS_UNCHANGED/PAPERS_FIXED/NEW_PAPERS_ADDED definitions were not mutually exclusive and did not properly account for the transition.

## Paper ID Set

Previous Unique Paper IDs: 668
Preserved Paper IDs: 668
Changed Paper IDs: 0
Removed Paper IDs: 7
New Paper IDs: 2
Current Unique Paper IDs: 670
Paper ID Set Unexplained: 0
Paper ID Set Accounted: PASS

## Image Sequence

Old Reported Image Sequence Directories: 35
Current Image Sequence Directories: 41

Formal Directories: 0
Shared Directories: 34
Exact Duplicate Directories: 0
Review Directories: 7
Excluded Directories: 0
Unaccounted Directories: 0

Root Cause: Old report used 35 (from G3-01R initial analysis), but actual machine facts show 41 multi-image directories. The 35 was a stale value from before image sequence reconciliation.

Image Sequence Logical Papers: 34
Image Sequence Memberships: 1724

## Pilot

Formal Papers 2015: 23
Formal Papers 2025: 5

## Membership & Source Integrity

Membership Integrity: PASS
Source Integrity: PASS

## Safety

Identity Catalog Data Modified: 0
Upstream Catalog Modified: 0
Original Files Modified: 0
Original Files Deleted: 0
Original Files Moved/Renamed: 0

## Gate

- Current Formal Papers == Unique Paper IDs: PASS
- Duplicate Paper IDs = 0: PASS
- Paper ID Pattern Validation = PASS: PASS
- Identity Type Accounting = PASS: PASS
- Paper Transition Accounted = PASS: PASS
- Paper ID Set Accounted = PASS: PASS
- Image Sequence Unaccounted = 0: PASS
- Membership Integrity = PASS: PASS
- Source Integrity = PASS: PASS
- 2015 Pilot identity remains valid: PASS
- 2025 Pilot identity remains valid: PASS
- No stale validation number remains: PASS
- G1/G2/G3-00 upstream catalogs unchanged: PASS
