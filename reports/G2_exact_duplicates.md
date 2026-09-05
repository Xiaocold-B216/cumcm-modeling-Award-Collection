# CUMCM Award Collection 鈥?G2 Exact Duplicate Report

## Execution Summary

Stage: G2
Status: PASS
Started At: 2026-08-17T19:01:51+08:00
Completed At: 2026-08-17T19:01:53+08:00

## Baseline Reference

Repository: D:\cumcm-modeling-Award-Collection
Branch: library-refactor-v1
HEAD: a042ecf898feaba6fc81d543a10e0188db8b2b12
G0 Recorded At: 2026-08-17T18:16:45+08:00

## G1 Source Verification

Source CSV Records: 3634
Source JSONL Records: 3634
Path Set Match: True
SHA Match: True

## SHA-256 Integrity

Valid SHA-256: 3634
Invalid SHA-256: 0
Targeted Rehash Count: 0

## Duplicate Analysis

Total Files: 3634
Unique SHA-256: 3543
Exact Duplicate Groups: 75
Exact Duplicate Members: 166
Extra Copies: 91
Max Group Size: 4

### Group Characteristics

Same Extension Groups: 71
Mixed Extension Groups: 4
Cross Year Groups: 1
Same Year Groups: 74

## Output Files

- catalog/duplicates.csv: 166 records
- logs/duplicate.log: 27 entries
- reports/G2_exact_duplicates.md: this file

## Safety Verification

Original Files Modified By G2: 0
Original Files Deleted By G2: 0
Original Files Renamed/Moved By G2: 0
Duplicate Files Deleted: 0
Duplicate Files Renamed: 0

## Validation

- Exact Duplicate only determined by SHA-256 match: PASS
- All member_count >= 2 SHA groups in duplicates.csv: PASS
- All member_count == 1 files not in exact duplicate rows: PASS
- duplicate_group deterministic: PASS
- Each duplicate member has exactly one relation row: PASS
- Same path not in two exact duplicate groups: PASS
- Same SHA member count matches member_count: PASS
- duplicate rows SHA-256 matches G1 source: PASS
- No near duplicate executed: PASS
- No same work executed: PASS
- No Paper ID assigned: PASS
- No pdf-inspector run: PASS
- No PDF Audit executed: PASS
- No PDF Repair executed: PASS
- No duplicate files deleted: PASS
- No duplicate files moved: PASS
- No duplicate files renamed: PASS
- G1 frozen catalog not modified: PASS

## Notes

- G1 introduced-change count semantics may differ from output file list, does not affect G2 SHA/duplicate facts
- All duplicate groups are deterministic and based solely on SHA-256 match
- No files were deleted, moved, or renamed
- No modifications to original files
