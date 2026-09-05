# G3-02R Relation Candidate Accounting Reconciliation

## Baseline

Stage: G3-02R
Status: PASS
Started At: 2026-08-18T22:38:22+08:00
Completed At: 2026-08-18T22:41:13+08:00

Repository: D:\cumcm-modeling-Award-Collection
Branch: library-refactor-v1
HEAD: a042ecf898feaba6fc81d543a10e0188db8b2b12

## Source Verification

G1 Records: 3634
G2 Exact Duplicate Groups: 75
Formal Papers: 670
Paper File Memberships: 2372

## Candidate Definition

Candidate Definition: A pair of papers/files identified by the relation generation pipeline as potentially having a relationship (near_duplicate, same_work_different_format, or same_work_different_version).
Candidate Blocks: Year-Problem groups for Near Duplicate; Source-ID groups for Same Work Format; Filename patterns for Same Work Version.
Candidate Blocks Meaning: Groups of papers/files that are compared against each other to identify potential relations.

## Candidate Statistics

All Pairs Scan: 0
Total Relation Candidate Pairs: 30
Total Relation Candidate Evaluations: 30
Duplicate Candidate Pairs: 110

## Exact Duplicate Relations

Exact Relations: 110
Exact Groups Projected: 75
Exact Groups Without Relation: 0
Exact Relations Without G2 Source: 0

## Near Duplicate

Near Duplicate Candidates: 28
Near Duplicate Relations: 0
Near Duplicate Review Candidates: 27
Near Duplicate Rejected: 1
Near Duplicate Unaccounted: 0

Root Cause: G3-02 script created NearDuplicateCandidates but did not add them to NearDuplicateReview. Candidates were counted but not processed into formal review pipeline.

## Same Work Different Format

Same Work Format Candidates: 0
Same Work Format Relations: 0
Same Work Format Review Candidates: 0
Same Work Format Rejected: 0
Same Work Format Unaccounted: 0

## Same Work Different Version

Same Work Version Candidates: 2
Same Work Version Relations: 0
Same Work Version Review Candidates: 2
Same Work Version Rejected: 0
Same Work Version Unaccounted: 0

Root Cause: G3-02 script added items directly to SameWorkVersionReview without incrementing SameWorkVersionCandidates count. The review items were detected directly in the version pattern matching loop.

## Review Summary

Total Relation Review Rows: 29
Near Review Rows: 27
Format Review Rows: 0
Version Review Rows: 2
Other Review Rows: 0

Orphan Review Candidates: 0
Formal Non-exact Relations Without Candidate: 0
Relation Candidates Unaccounted: 0

## Formal Relations

Total Formal Relations: 110
Formal Relations Added: 0
Formal Relations Removed: 0
Review Rows Added: 29
Review Rows Removed: 0
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

## Safety

Identity Catalog Modified: False
Upstream Catalog Modified: False
Relation Contract Modified: False
Original Files Modified: 0
Original Files Deleted: 0
Original Files Moved/Renamed: 0

## Gate

- Candidate definition established: PASS
- Total Relation Candidate Pairs > 0: PASS
- Near Duplicate candidates fully accounted: PASS
- Same Work Format candidates fully accounted: PASS
- Same Work Version candidates fully accounted: PASS
- Orphan Review Candidates = 0: PASS
- Formal Non-exact Relations Without Candidate = 0: PASS
- Relation Candidates Unaccounted = 0: PASS
- Self Relations = 0: PASS
- Duplicate Relation Rows = 0: PASS
- Relation Orphans = 0: PASS
- Paper Identity unchanged: PASS
- Membership unchanged: PASS
- Source Registry unchanged: PASS
- Upstream catalog unchanged: PASS
- Contract unchanged: PASS
- Original files unchanged: PASS
- No O(n虏) similarity scan: PASS
- No PDF content processing: PASS
