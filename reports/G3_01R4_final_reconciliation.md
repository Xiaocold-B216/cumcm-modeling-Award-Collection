# G3-01R4 Final ID-Set Accounting Correction

## Baseline

Stage: G3-01R4
Status: PASS
Started At: 2026-08-18T15:45:43+08:00
Completed At: 2026-08-18T15:47:17+08:00

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

## Row-Level Transition

Previous Formal Rows: 675
Removed Duplicate Rows: 7
Removed From Formal To Review: 0
New Paper Rows Added: 2
Current Formal Rows: 670
Row Transition Unexplained: 0
Row Transition Accounted: PASS

## ID-Set Transition

Previous Unique Paper IDs: 668
Preserved Paper IDs: 668
Removed Paper IDs: 0
Changed Paper IDs: 0
New Paper IDs: 2
Current Unique Paper IDs: 670
ID Set Unexplained: 0
ID Set Accounted: PASS

Root Cause: The old report incorrectly used REMOVED_PAPER_IDS=7, but this was actually REMOVED_DUPLICATE_ROWS=7. All unique Paper IDs were preserved. The correct value is REMOVED_PAPER_IDS=0.

## Source-ID Count Drift

Old Reported Source ID Papers: 35
Current Source ID Papers: 34

Papers with Source Identifier Field: 14
Papers with Source Row: 14
Papers with Source-ID Suffix: 34

Root Cause: G3-01R2 counted papers with source identifier pattern in path (35), but G3-01R3/R4 counted papers with source-ID suffix in paper_id (34). The difference is that 1 paper has a source identifier in the path but the paper_id uses an internal sequential ID instead.
Source-ID Count Drift Explained: PASS

## Pilot

Formal Papers 2015: 23
Formal Papers 2025: 5

## Membership & Source Integrity

Membership Integrity: PASS
Source Integrity: PASS
Source Reference Conflicts: 0

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
- Row-level transition & unique-ID transition separated: PASS
- Row Transition Unexplained = 0: PASS
- REMOVED_DUPLICATE_ROWS not miscounted as REMOVED_PAPER_IDS: PASS
- PREVIOUS_UNIQUE_PAPER_IDS = PRESERVED_PAPER_IDS + REMOVED_PAPER_IDS: PASS
- CURRENT_UNIQUE_PAPER_IDS = PRESERVED_PAPER_IDS + NEW_PAPER_IDS: PASS
- CHANGED_PAPER_IDS = 0: PASS
- ID Set Unexplained = 0: PASS
- Source-ID count drift explained: PASS
- Identity Type Accounting = PASS: PASS
- Membership Integrity = PASS: PASS
- Source Integrity = PASS: PASS
- 2015 Pilot identity remains valid: PASS
- 2025 Pilot identity remains valid: PASS
- Identity Catalog Data Modified = 0: PASS
- Upstream Catalog Modified = 0: PASS
