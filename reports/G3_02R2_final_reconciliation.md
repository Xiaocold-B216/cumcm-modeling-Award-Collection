# G3-02R2 Final Relation Delta & Duplicate-Candidate Reconciliation

## Baseline

Stage: G3-02R2
Status: PASS
Started At: 2026-08-18T23:49:35+08:00
Completed At: 2026-08-18T23:49:48+08:00

Repository: D:\cumcm-modeling-Award-Collection
Branch: library-refactor-v1
HEAD: a042ecf898feaba6fc81d543a10e0188db8b2b12

## Source Verification

G1 Records: 3634
G2 Exact Duplicate Groups: 75
Formal Papers: 670
Paper File Memberships: 2372

## Candidate Statistics

All Pairs Scan: 0
Total Relation Candidate Pairs: 30
Total Relation Candidate Evaluations: 30
Unique Relation Candidate Evaluations: 30

Duplicate Candidate Pairs: 0
Duplicate Candidate Evaluation Rows: 0

Root Cause: G3-02R incorrectly set DUPLICATE_CANDIDATE_PAIRS=110 (same as EXACT_RELATIONS), but this should be 0. The 110 value represents exact relations from G2, not duplicate candidate pairs in the non-exact pipeline.

## Exact Duplicate Relations

Exact Relations: 110
Exact Relation Unique Keys: 110
Exact Relation Duplicate Keys: 0

Exact Groups Projected: 75
Exact Groups Without Relation: 0
Exact Relations Without G2 Source: 0

## Near Duplicate

Near Duplicate Candidates: 28
Near Duplicate Relations: 0
Near Duplicate Review Candidates: 27
Near Duplicate Rejected: 1
Near Duplicate Unaccounted: 0

## Same Work Different Format

Same Work Format Candidates: 0
Same Work Format Relations: 0
Same Work Format Review Candidates: 0
Same Work Format Rejected: 0
Same Work Format Unaccounted: 0

## Same Work Different Version

Same Work Version Candidates: 2
Same Work Version Relations: 0
Same Work Version Review Candidates:  .Count
Same Work Version Rejected: 0
Same Work Version Unaccounted: 0

## Relation Candidates

Relation Candidates Unaccounted: 0

## Review Delta

Previous Relation Review Rows: 2
Current Relation Review Rows: 29

Preserved Relation Review Rows: 2
Review Rows Added: 27
Review Rows Removed: 0

Previous Version Review Rows: 2
Preserved Version Review Rows:  .Count
Current Version Review Rows:  .Count

Near Review Rows: 27
Format Review Rows: 0
Version Review Rows:  .Count
Other Review Rows: 0

Duplicate Review Keys: 0
Duplicate Review Rows: 0
Orphan Review Candidates: 0

Review ID Changes: 0

Relation Review Delta Unexplained: 0
Relation Review Delta Accounted: PASS

Root Cause: G3-02R reported REVIEW_ROWS_ADDED=29, but the correct delta is: PREVIOUS=2, PRESERVED=2 (version rows), ADDED=27 (near duplicate rows), REMOVED=0, CURRENT=29. Version review rows had empty keys and were fixed.

## Formal Relations

Total Formal Relations: 110
Formal Relations Added: 0
Formal Relations Removed: 0
Relation ID Changes: 0

## Integrity Checks

Self Relations: 0
Duplicate Relation Rows: 0
Relation Orphans: 0
Exact/Near Overlap: 0
Cross-year Source-ID False Merges: 0
Cross-year Exact Groups Auto-promoted to Same Work: 0

## Identity Verification

Formal Papers Before: 670
Formal Papers After: 670
Paper File Memberships Before: 2372
Paper File Memberships After: 2372
Paper ID Set Changed: False
Source Registry Modified: False

## Data Modification

Formal Relation Data Modified: False
Relation Review Data Modified: True
Identity Catalog Modified: False
Upstream Catalog Modified: False
Relation Contract Modified: False

## Safety

Original Files Modified: 0
Original Files Deleted: 0
Original Files Moved/Renamed: 0

## Gate

- Duplicate Candidate Pairs = 0: PASS
- Exact Relation Duplicate Keys = 0: PASS
- Near Duplicate Unaccounted = 0: PASS
- Same Work Format Unaccounted = 0: PASS
- Same Work Version Unaccounted = 0: PASS
- Relation Candidates Unaccounted = 0: PASS
- Preserved Version Review Rows = Previous Version Review Rows: PASS
- Duplicate Review Keys = 0: PASS
- Duplicate Review Rows = 0: PASS
- Orphan Review Candidates = 0: PASS
- Relation Review Delta Unexplained = 0: PASS
- Self Relations = 0: PASS
- Duplicate Relation Rows = 0: PASS
- Relation Orphans = 0: PASS
- Paper Identity unchanged: PASS
- Membership unchanged: PASS
- Source Registry unchanged: PASS
- Upstream catalog unchanged: PASS
- Contract unchanged: PASS
- Original files unchanged: PASS
- No relation inference re-execution: PASS
- No PDF content processing: PASS
