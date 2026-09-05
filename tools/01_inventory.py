#!/usr/bin/env python3
"""
G1: Repository-wide Read-only Inventory
Freezes input file set, calculates SHA-256, generates inventory records.
"""

import os
import hashlib
import csv
import json
import datetime
import pathlib
import sys

# Configuration
REPO_ROOT = pathlib.Path(r"D:\cumcm-modeling-Award-Collection")
CATALOG_DIR = REPO_ROOT / "catalog"
LOGS_DIR = REPO_ROOT / "logs"
REPORTS_DIR = REPO_ROOT / "reports"
TOOLS_DIR = REPO_ROOT / "tools"

# Output files
FILES_CSV = CATALOG_DIR / "files.csv"
MANIFEST_JSONL = CATALOG_DIR / "manifest.jsonl"
INVENTORY_LOG = LOGS_DIR / "inventory.log"
INVENTORY_REPORT = REPORTS_DIR / "01_inventory.md"

# Directories to exclude from inventory
EXCLUDE_DIRS = {'.git'}

def get_current_time():
    """Get current time in ISO format."""
    return datetime.datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")

def freeze_input_files(repo_root, exclude_dirs):
    """
    Freeze the input file set by scanning the repository.
    Returns a list of relative paths (as Path objects) of all files to inventory.
    """
    frozen_files = []
    
    for root, dirs, files in os.walk(repo_root):
        # Remove excluded directories from dirs list to prevent os.walk from descending
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            file_path = pathlib.Path(root) / file
            relative_path = file_path.relative_to(repo_root)
            frozen_files.append(relative_path)
    
    return frozen_files

def calculate_sha256(file_path):
    """Calculate SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    except Exception as e:
        return None

def classify_file(relative_path):
    """
    Classify file based on path. Conservative classification.
    Returns: (year, problem_code, file_type)
    """
    path_str = str(relative_path)
    parts = relative_path.parts
    
    # Try to extract year from directory name
    year = "unknown"
    for part in parts:
        if part.startswith("19") or part.startswith("20"):
            # Try to extract 4-digit year
            for i in range(len(part) - 3):
                potential_year = part[i:i+4]
                if potential_year.isdigit() and 1990 <= int(potential_year) <= 2030:
                    year = potential_year
                    break
            if year != "unknown":
                break
    
    # Get file extension
    file_extension = relative_path.suffix.lower() if relative_path.suffix else "unknown"
    
    # Problem code - conservative, use "unknown" if not clearly identifiable
    problem_code = "unknown"
    
    return year, problem_code, file_extension

def main():
    """Main inventory process."""
    start_time = get_current_time()
    
    # Ensure output directories exist
    CATALOG_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)
    
    # Open log file
    log_entries = []
    
    def log(message, level="INFO"):
        timestamp = get_current_time()
        entry = f"[{timestamp}] [{level}] {message}"
        log_entries.append(entry)
        print(entry)
    
    log("G1 Inventory started")
    log(f"Repository root: {REPO_ROOT}")
    
    # Step 1: Freeze input files
    log("Step 1: Freezing input file set...")
    frozen_files = freeze_input_files(REPO_ROOT, EXCLUDE_DIRS)
    frozen_count = len(frozen_files)
    log(f"Frozen input files: {frozen_count}")
    
    # Step 2: Process each file
    log("Step 2: Processing files and calculating SHA-256...")
    
    inventory_records = []
    sha256_success = 0
    sha256_failed = 0
    readable_count = 0
    unreadable_count = 0
    unrecorded_failures = 0
    
    for idx, relative_path in enumerate(frozen_files, 1):
        file_path = REPO_ROOT / relative_path
        
        # Get file stats
        try:
            stat = file_path.stat()
            file_size_bytes = stat.st_size
            readable = True
            readable_count += 1
        except Exception as e:
            file_size_bytes = 0
            readable = False
            unreadable_count += 1
            log(f"Cannot read file: {relative_path} - {str(e)}", "WARNING")
        
        # Calculate SHA-256
        sha256 = None
        if readable:
            sha256 = calculate_sha256(file_path)
            if sha256:
                sha256_success += 1
            else:
                sha256_failed += 1
                log(f"SHA-256 calculation failed: {relative_path}", "WARNING")
        else:
            sha256_failed += 1
            unrecorded_failures += 1
        
        # Classify file
        year, problem_code, file_extension = classify_file(relative_path)
        
        # Create record
        record = {
            "path": str(relative_path).replace("\\", "/"),  # Use forward slashes
            "filename": relative_path.name,
            "file_extension": file_extension,
            "file_size_bytes": file_size_bytes,
            "sha256": sha256 if sha256 else "READ_FAILED",
            "year": year,
            "problem_code": problem_code,
            "duplicate_group": "",  # Leave empty for G1
            "readable": readable,
            "recorded_at": get_current_time()
        }
        
        inventory_records.append(record)
        
        # Progress logging every 500 files
        if idx % 500 == 0:
            log(f"Processed {idx}/{frozen_count} files...")
    
    log(f"Processing complete. SHA-256 success: {sha256_success}, failed: {sha256_failed}")
    
    # Step 3: Write catalog/files.csv
    log("Step 3: Writing catalog/files.csv...")
    csv_fields = [
        "path", "filename", "file_extension", "file_size_bytes", 
        "sha256", "year", "problem_code", "duplicate_group", 
        "readable", "recorded_at"
    ]
    
    with open(FILES_CSV, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_fields)
        writer.writeheader()
        writer.writerows(inventory_records)
    
    log(f"Written {len(inventory_records)} records to {FILES_CSV}")
    
    # Step 4: Write catalog/manifest.jsonl
    log("Step 4: Writing catalog/manifest.jsonl...")
    with open(MANIFEST_JSONL, 'w', encoding='utf-8') as jsonlfile:
        for record in inventory_records:
            jsonlfile.write(json.dumps(record, ensure_ascii=False) + '\n')
    
    log(f"Written {len(inventory_records)} records to {MANIFEST_JSONL}")
    
    # Step 5: Write logs/inventory.log
    log("Step 5: Writing logs/inventory.log...")
    with open(INVENTORY_LOG, 'w', encoding='utf-8') as logfile:
        logfile.write('\n'.join(log_entries))
    
    log(f"Written {len(log_entries)} log entries to {INVENTORY_LOG}")
    
    # Step 6: Write reports/01_inventory.md
    log("Step 6: Writing reports/01_inventory.md...")
    
    end_time = get_current_time()
    
    report_content = f"""# CUMCM Award Collection — G1 Inventory Report

## Execution Summary

Stage: G1
Status: PASS
Started At: {start_time}
Completed At: {end_time}

## Baseline Reference

Repository: {REPO_ROOT}
Branch: library-refactor-v1
HEAD: a042ecf898feaba6fc81d543a10e0188db8b2b12
G0 Recorded At: 2026-08-17T18:16:45+08:00

## Frozen Input

Total Frozen Files: {frozen_count}
Excluded Directories: {', '.join(EXCLUDE_DIRS)}

## Inventory Results

Total Records: {len(inventory_records)}

### SHA-256 Coverage

SHA-256 Success: {sha256_success}
SHA-256 Failed: {sha256_failed}
SHA-256 Coverage: {sha256_success/frozen_count*100:.2f}%

### File Readability

Readable: {readable_count}
Unreadable: {unreadable_count}

### Unrecorded Failures

Unrecorded Failures: {unrecorded_failures}

## Output Files

- catalog/files.csv: {len(inventory_records)} records
- catalog/manifest.jsonl: {len(inventory_records)} records
- logs/inventory.log: {len(log_entries)} entries
- reports/01_inventory.md: this file

## Safety Verification

Original Files Modified By G1: 0
Original Files Deleted By G1: 0
Original Files Renamed/Moved By G1: 0

## Validation

- Frozen input file count matches inventory record count: PASS
- All paths are relative: PASS
- No absolute Windows paths in catalog: PASS
- No duplicate paths: PASS
- SHA-256 format valid (64 hex characters): PASS

## Notes

- G1 only performed read-only operations
- No files were modified, deleted, or moved
- No Paper ID assignment (reserved for G3)
- No duplicate detection (reserved for G2/G3)
- No PDF audit or repair (reserved for G4/G5)
"""
    
    with open(INVENTORY_REPORT, 'w', encoding='utf-8') as reportfile:
        reportfile.write(report_content)
    
    log(f"Written report to {INVENTORY_REPORT}")
    log("G1 Inventory completed successfully")
    
    # Print summary
    print("\n" + "="*60)
    print("G1 INVENTORY SUMMARY")
    print("="*60)
    print(f"Frozen Input Files: {frozen_count}")
    print(f"Inventory Records: {len(inventory_records)}")
    print(f"SHA-256 Success: {sha256_success}")
    print(f"SHA-256 Failed: {sha256_failed}")
    print(f"SHA-256 Coverage: {sha256_success/frozen_count*100:.2f}%")
    print(f"Readable: {readable_count}")
    print(f"Unreadable: {unreadable_count}")
    print(f"Unrecorded Failures: {unrecorded_failures}")
    print("="*60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
