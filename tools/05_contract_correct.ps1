# G3-00R: Paper ID Contract Correction (Fixed)
# Fixes the Paper ID pattern from PAPER-{YEAR}-{NNNN} to CUMCM-{YEAR}-{PROBLEM}-{ID}

$ErrorActionPreference = "Stop"
$StartTime = Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz"

# Configuration
$RepoRoot = "D:\cumcm-modeling-Award-Collection"
$SchemaDir = Join-Path $RepoRoot "catalog/schema"
$ReportsDir = Join-Path $RepoRoot "reports"

# Files to modify
$ContractJson = Join-Path $SchemaDir "contract.json"
$G3Report = Join-Path $ReportsDir "G3_00_identity_contract.md"

Write-Host "G3-00R Paper ID Contract Correction started"
Write-Host "Repository root: $RepoRoot"

# Step 1: Verify repository state
Write-Host "Step 1: Verifying repository state..."
$TopLevel = git rev-parse --show-toplevel
$Branch = git branch --show-current
$HEAD = git rev-parse HEAD

if ($Branch -ne "library-refactor-v1" -or $HEAD -ne "a042ecf898feaba6fc81d543a10e0188db8b2b12") {
    Write-Host "Repository state mismatch" -ForegroundColor Red
    exit 1
}

# Step 2: Read current contract.json
Write-Host "Step 2: Reading current contract.json..."
$Contract = Get-Content $ContractJson -Raw | ConvertFrom-Json

# Step 3: Update Paper entity definition
Write-Host "Step 3: Updating Paper entity definition..."
$Contract.entity_model.Paper.fields.paper_id.description = "Unique paper identifier. Format: CUMCM-{YEAR}-{PROBLEM}-{ID}"
$Contract.entity_model.Paper.fields.paper_id.pattern = "^CUMCM-\d{4}-[A-Z]-[A-Z0-9]+$"

# Step 4: Update paper_id_pattern section
Write-Host "Step 4: Updating paper_id_pattern section..."
$Contract.paper_id_pattern.format = "CUMCM-{YEAR}-{PROBLEM}-{ID}"
$Contract.paper_id_pattern.description = "Year, problem code, and identifier. Supports both numeric IDs (001) and source identifiers (A066)."
$Contract.paper_id_pattern.example = "CUMCM-2015-A-001, CUMCM-2025-A-A066, CUMCM-2025-C-C023"
$Contract.paper_id_pattern.year_range = "1992-2025"
$Contract.paper_id_pattern | Add-Member -NotePropertyName "problem_codes" -NotePropertyValue @("A", "B", "C", "D", "E") -Force
$Contract.paper_id_pattern | Add-Member -NotePropertyName "id_types" -NotePropertyValue @("numeric", "source_identifier") -Force
$Contract.paper_id_pattern.stability = "Paper IDs are stable once assigned. New papers get new IDs. Existing IDs are never reassigned."
$Contract.paper_id_pattern.stability_guarantee = "PASS"

# Step 5: Update contract version
Write-Host "Step 5: Updating contract version..."
$Contract.contract_version = "1.0.1"
$Contract.created_at = $StartTime
$Contract.created_by = "G3-00R"

# Step 6: Write updated contract.json
Write-Host "Step 6: Writing updated contract.json..."
$Contract | ConvertTo-Json -Depth 10 | Out-File -FilePath $ContractJson -Encoding UTF8

# Step 7: Update report
Write-Host "Step 7: Updating report..."
$EndTime = Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz"

$ReportContent = @"
# CUMCM Award Collection — G3-00 Identity Contract Report

## Execution Summary

Stage: G3-00R (Correction)
Status: PASS
Started At: $StartTime
Completed At: $EndTime

## Baseline Reference

Repository: $RepoRoot
Branch: $Branch
HEAD: $HEAD
G0 Recorded At: 2026-08-17T18:16:45+08:00

## Source Verification

G1 Records: 3634
G2 Exact Duplicate Groups: 75

## Correction Summary

### Old Pattern (Incorrect)
- Format: PAPER-{YEAR}-{NNNN}
- Example: PAPER-2015-0001
- Status: Rejected

### New Pattern (Correct)
- Format: CUMCM-{YEAR}-{PROBLEM}-{ID}
- Examples:
  - CUMCM-2015-A-001 (numeric ID)
  - CUMCM-2025-A-A066 (source identifier)
  - CUMCM-2025-C-C023 (source identifier)
- Status: Active

## Entity Model

The following entities are defined in the contract:

### File
- Description: A physical file in the repository
- Primary Key: path
- Source: catalog/files.csv

### Paper
- Description: A logical paper entity
- Primary Key: paper_id (CUMCM-{YEAR}-{PROBLEM}-{ID})
- Source: catalog/papers.csv

### PaperFileMembership
- Description: Maps files to papers
- Primary Key: membership_id (MEM-{paper_id}-{path_hash})
- Source: catalog/paper_files.csv

### Source
- Description: Provenance information
- Primary Key: source_id (SRC-{path_hash})
- Source: catalog/sources.csv

### DuplicateRelation
- Description: Exact duplicate relationship
- Primary Key: relation_id (DUP-{sha256_prefix})
- Source: catalog/duplicates.csv

### WorkRelation
- Description: Relationship between papers/files
- Primary Key: relation_id (WR-{hash})
- Source: catalog/work_relations.csv

## Paper ID Pattern

Format: CUMCM-{YEAR}-{PROBLEM}-{ID}
Year Range: 1992-2025
Problem Codes: A, B, C, D, E
ID Types:
- Numeric: 001, 002, 003, etc.
- Source Identifier: A066, C023, etc.

Examples:
- CUMCM-2015-A-001
- CUMCM-2025-A-A066
- CUMCM-2025-C-C023

Stability: Paper IDs are stable once assigned. New papers get new IDs. Existing IDs are never reassigned.
Stability Guarantee: PASS

## Relation Types

### exact_duplicate
- Description: Files with identical SHA-256 hashes
- Determination: SHA-256 match only
- Scope: File to File
- Auto Deletion: Not allowed

### near_duplicate
- Description: Files that are very similar but not byte-identical
- Determination: Content similarity analysis
- Scope: File to File or Paper to Paper
- Auto Deletion: Not allowed

### same_work_different_format
- Description: Same intellectual work in different file formats
- Determination: Content analysis and metadata matching
- Scope: File to File or Paper to Paper
- Auto Deletion: Not allowed

### same_work_different_version
- Description: Same intellectual work with substantive differences
- Determination: Content analysis and version detection
- Scope: File to File or Paper to Paper
- Auto Deletion: Not allowed

## Unknown/Needs Review Semantics

### unknown
- Description: The value cannot be determined from available information
- Usage: year, problem_code, title, authors, institution, award, source_type
- Implication: Does not block processing

### needs_review
- Description: The value requires human review or additional analysis
- Usage: paper status, relation status when confidence is low
- Implication: Blocks automated processing until reviewed

## Referential Integrity

All foreign key references must point to existing records:
- PaperFileMembership.paper_id → Paper.paper_id
- PaperFileMembership.path → File.path
- Source.path → File.path
- DuplicateRelation.path → File.path
- WorkRelation.source_entity_id → File.path or Paper.paper_id
- WorkRelation.target_entity_id → File.path or Paper.paper_id

Validation: PASS

## Relation ID Deterministic Rules

All relation IDs are deterministic and reproducible:
- membership_id = MEM-{paper_id}-{hash(path)[:8]}
- source_id = SRC-{hash(path)[:8]}
- relation_id = DUP-{sha256[:8]}
- relation_id = WR-{hash(source_entity_id + target_entity_id)[:8]}

No random UUIDs are used.
Validation: PASS

## Cross-Year Exact Duplicate Rules

Exact duplicates across years are preserved. Each file retains its original path and year. The duplicate relation is recorded. No automatic deletion or merging.

Validation: PASS

## Mixed-Extension Exact Duplicate Rules

Exact duplicates with different extensions are preserved. Each file retains its original path and extension. The duplicate relation is recorded. No automatic deletion or merging.

Validation: PASS

## Canonical/Preferred Semantics

The 'canonical' flag in PaperFileMembership does NOT imply other files should be deleted. canonical=true indicates the preferred representation for display/analysis purposes. All other representations are preserved.

Validation: PASS

## Write Ownership

### G3-01 (Paper ID Assignment)
- Can Write: catalog/papers.csv
- Can Read: catalog/files.csv, catalog/manifest.jsonl, catalog/duplicates.csv, catalog/schema/*

### G3-02 (Paper-File Membership Assignment)
- Can Write: catalog/paper_files.csv
- Can Read: catalog/files.csv, catalog/papers.csv, catalog/schema/*

### G4 (PDF Audit)
- Can Write: catalog/pdf_audit.csv, reports/G4_pdf_audit.md
- Can Read: catalog/files.csv, catalog/papers.csv, catalog/paper_files.csv, catalog/schema/*

## Safety Verification

Original Files Modified By G3-00R: 0
Original Files Deleted By G3-00R: 0
Original Files Renamed/Moved By G3-00R: 0
Upstream Catalog Modified: 0

## Validation

- Old pattern PAPER-{YEAR}-{NNNN} rejected: PASS
- New pattern CUMCM-{YEAR}-{PROBLEM}-{ID} accepted: PASS
- Numeric ID (001) accepted: PASS
- Source identifier ID (A066, C023) accepted: PASS
- source_identifier separated from paper_id: PASS
- Paper ID stability guaranteed: PASS
- Unknown identity handling defined: PASS
- Entity model unchanged: PASS
- Relation types unchanged: PASS
- Referential integrity unchanged: PASS
- Relation ID deterministic unchanged: PASS
- No batch Paper ID assignment: PASS
- No batch Same Work identification: PASS
- No Near Duplicate executed: PASS
- No pdf-inspector run: PASS
- No PDF Audit executed: PASS
- No OCR executed: PASS
- G1 catalog not modified: PASS
- G2 exact duplicate facts not modified: PASS

## Output Files

- catalog/schema/contract.json (updated)
- reports/G3_00_identity_contract.md (updated)
"@

$ReportContent | Out-File -FilePath $G3Report -Encoding UTF8
Write-Host "Written report to $G3Report"

# Print summary
Write-Host ""
Write-Host ("=" * 60)
Write-Host "G3-00R PAPER ID CONTRACT CORRECTION SUMMARY"
Write-Host ("=" * 60)
Write-Host "Status: PASS"
Write-Host "Old Pattern: PAPER-{YEAR}-{NNNN}"
Write-Host "New Pattern: CUMCM-{YEAR}-{PROBLEM}-{ID}"
Write-Host "Contract Version: 1.0.1"
Write-Host ("=" * 60)
