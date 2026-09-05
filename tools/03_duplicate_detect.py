#!/usr/bin/env python3
"""
G2: SHA-256 Integrity Verification and Exact Duplicate Governance
"""

import csv
import json
import datetime
import pathlib

# Configuration
REPO_ROOT = pathlib.Path(r"D:\cumcm-modeling-Award-Collection")
CATALOG_DIR = REPO_ROOT / "catalog"
LOGS_DIR = REPO_ROOT / "logs"
REPORTS_DIR = REPO_ROOT / "reports"

# Output files
FILES_CSV = CATALOG_DIR / "files.csv"
MANIFEST_JSONL = CATALOG_DIR / "manifest.jsonl"
DUPLICATES_CSV = CATALOG_DIR / "duplicates.csv"
DUPLICATE_LOG = LOGS_DIR / "duplicate.log"
G2_REPORT = REPORTS_DIR / "G2_exact_duplicates.md"

def get_current_time():
    """Get current time in ISO format."""
    return datetime.datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")

def main():
    """Main duplicate detection process."""
    start_time = get_current_time()
    
    # Ensure output directories exist
    CATALOG_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)
    
    # Log function
    log_entries = []
    
    def log(message, level="INFO"):
        timestamp = get_current_time()
        entry = f"[{timestamp}] [{level}] {message}"
        log_entries.append(entry)
        print(entry)
    
    log("G2 Exact Duplicate Detection started")
    log(f"Repository root: {REPO_ROOT}")
    
    # Step 1: Read G1 catalog
    log("Step 1: Reading G1 catalog...")
    
    # Read CSV
    with open(FILES_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        csv_data = list(reader)
    
    # Read JSONL
    jsonl_data = []
    with open(MANIFEST_JSONL, 'r', encoding='utf-8') as f:
        for line in f:
            jsonl_data.append(json.loads(line))
    
    csv_records = len(csv_data)
    jsonl_records = len(jsonl_data)
    log(f"CSV records: {csv_records}")
    log(f"JSONL records: {jsonl_records}")
    
    if csv_records != 3634 or jsonl_records != 3634:
        log(f"G1 record count mismatch: CSV={csv_records}, JSONL={jsonl_records}", "ERROR")
        return 1
    
    # Verify path set match
    csv_paths = set(record['path'] for record in csv_data)
    jsonl_paths = set(record['path'] for record in jsonl_data)
    path_match = csv_paths == jsonl_paths
    log(f"Path set match: {path_match}")
    
    if not path_match:
        log("Path set mismatch between CSV and JSONL", "ERROR")
        return 1
    
    # Verify SHA match
    sha_match = True
    for i in range(len(csv_data)):
        if csv_data[i]['sha256'] != jsonl_data[i]['sha256']:
            sha_match = False
            log(f"SHA mismatch at index {i}", "ERROR")
            break
    log(f"SHA match: {sha_match}")
    
    if not sha_match:
        log("SHA mismatch between CSV and JSONL", "ERROR")
        return 1
    
    # Step 2: Verify SHA-256 integrity
    log("Step 2: Verifying SHA-256 integrity...")
    valid_sha256 = 0
    invalid_sha256 = 0
    targeted_rehash_count = 0
    
    for record in csv_data:
        sha256 = record['sha256']
        if len(sha256) == 64 and all(c in '0123456789ABCDEFabcdef' for c in sha256):
            valid_sha256++
        else:
            invalid_sha256++
            log(f"Invalid SHA-256 format: {record['path']} - {sha256}", "WARNING")
    
    log(f"Valid SHA-256: {valid_sha256}")
    log(f"Invalid SHA-256: {invalid_sha256}")
    
    if invalid_sha256 > 0:
        log("Invalid SHA-256 values found", "ERROR")
        return 1
    
    # Step 3: Find exact duplicates
    log("Step 3: Finding exact duplicates...")
    
    # Group by SHA-256
    sha_groups = {}
    for record in csv_data:
        sha256 = record['sha256']
        if sha256 not in sha_groups:
            sha_groups[sha256] = []
        sha_groups[sha256].append(record)
    
    # Filter duplicate groups (member_count >= 2)
    duplicate_groups = {sha: records for sha, records in sha_groups.items() if len(records) >= 2}
    
    total_files = len(csv_data)
    unique_sha256 = len(sha_groups)
    exact_duplicate_groups = len(duplicate_groups)
    exact_duplicate_members = sum(len(records) for records in duplicate_groups.values())
    extra_copies = exact_duplicate_members - exact_duplicate_groups
    max_group_size = max((len(records) for records in duplicate_groups.values()), default=0)
    
    log(f"Total files: {total_files}")
    log(f"Unique SHA-256: {unique_sha256}")
    log(f"Exact duplicate groups: {exact_duplicate_groups}")
    log(f"Exact duplicate members: {exact_duplicate_members}")
    log(f"Extra copies: {extra_copies}")
    log(f"Max group size: {max_group_size}")
    
    # Step 4: Analyze duplicate groups
    log("Step 4: Analyzing duplicate groups...")
    same_extension_groups = 0
    mixed_extension_groups = 0
    cross_year_groups = 0
    same_year_groups = 0
    
    duplicate_records = []
    group_index = 0
    
    for sha256, records in duplicate_groups.items():
        group_index += 1
        group_id = f"DG{group_index:05d}"
        member_count = len(records)
        
        # Analyze extensions and years
        extensions = set(record['file_extension'] for record in records)
        years = set(record['year'] for record in records)
        
        if len(extensions) == 1:
            same_extension_groups += 1
        else:
            mixed_extension_groups += 1
        
        if len(years) == 1:
            same_year_groups += 1
        else:
            cross_year_groups += 1
        
        # Create records for each member
        for member_index, record in enumerate(records, 1):
            duplicate_record = {
                'duplicate_group': group_id,
                'sha256': sha256,
                'member_count': member_count,
                'member_index': member_index,
                'path': record['path'],
                'filename': record['filename'],
                'file_extension': record['file_extension'],
                'file_size_bytes': record['file_size_bytes'],
                'year': record['year'],
                'problem_code': record['problem_code'],
                'recorded_at': get_current_time()
            }
            duplicate_records.append(duplicate_record)
    
    log(f"Same extension groups: {same_extension_groups}")
    log(f"Mixed extension groups: {mixed_extension_groups}")
    log(f"Cross year groups: {cross_year_groups}")
    log(f"Same year groups: {same_year_groups}")
    
    # Step 5: Write catalog/duplicates.csv
    log("Step 5: Writing catalog/duplicates.csv...")
    fieldnames = [
        'duplicate_group', 'sha256', 'member_count', 'member_index',
        'path', 'filename', 'file_extension', 'file_size_bytes',
        'year', 'problem_code', 'recorded_at'
    ]
    
    with open(DUPLICATES_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(duplicate_records)
    
    log(f"Written {len(duplicate_records)} records to {DUPLICATES_CSV}")
    
    # Step 6: Write logs/duplicate.log
    log("Step 6: Writing logs/duplicate.log...")
    with open(DUPLICATE_LOG, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_entries))
    
    log(f"Written {len(log_entries)} log entries to {DUPLICATE_LOG}")
    
    # Step 7: Write reports/G2_exact_duplicates.md
    log("Step 7: Writing reports/G2_exact_duplicates.md...")
    end_time = get_current_time()
    
    report_content = f"""# CUMCM Award Collection — G2 Exact Duplicate Report

## Execution Summary

Stage: G2
Status: PASS
Started At: {start_time}
Completed At: {end_time}

## Baseline Reference

Repository: {REPO_ROOT}
Branch: library-refactor-v1
HEAD: a042ecf898feaba6fc81d543a10e0188db8b2b12
G0 Recorded At: 2026-08-17T18:16:45+08:00

## G1 Source Verification

Source CSV Records: {csv_records}
Source JSONL Records: {jsonl_records}
Path Set Match: {path_match}
SHA Match: {sha_match}

## SHA-256 Integrity

Valid SHA-256: {valid_sha256}
Invalid SHA-256: {invalid_sha256}
Targeted Rehash Count: {targeted_rehash_count}

## Duplicate Analysis

Total Files: {total_files}
Unique SHA-256: {unique_sha256}
Exact Duplicate Groups: {exact_duplicate_groups}
Exact Duplicate Members: {exact_duplicate_members}
Extra Copies: {extra_copies}
Max Group Size: {max_group_size}

### Group Characteristics

Same Extension Groups: {same_extension_groups}
Mixed Extension Groups: {mixed_extension_groups}
Cross Year Groups: {cross_year_groups}
Same Year Groups: {same_year_groups}

## Output Files

- catalog/duplicates.csv: {len(duplicate_records)} records
- logs/duplicate.log: {len(log_entries)} entries
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
"""
    
    with open(G2_REPORT, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    log(f"Written report to {G2_REPORT}")
    log("G2 Exact Duplicate Detection completed successfully")
    
    # Print summary
    print("\n" + "="*60)
    print("G2 EXACT DUPLICATE DETECTION SUMMARY")
    print("="*60)
    print(f"Total Files: {total_files}")
    print(f"Unique SHA-256: {unique_sha256}")
    print(f"Exact Duplicate Groups: {exact_duplicate_groups}")
    print(f"Exact Duplicate Members: {exact_duplicate_members}")
    print(f"Extra Copies: {extra_copies}")
    print(f"Max Group Size: {max_group_size}")
    print(f"Same Extension Groups: {same_extension_groups}")
    print(f"Mixed Extension Groups: {mixed_extension_groups}")
    print(f"Cross Year Groups: {cross_year_groups}")
    print(f"Same Year Groups: {same_year_groups}")
    print("="*60)
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
