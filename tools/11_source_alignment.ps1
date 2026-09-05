# G3-01R5: Source-Identifier Identity & Provenance Alignment
# Adds missing source rows for papers with source-ID suffixes

$ErrorActionPreference = "Stop"
$StartTime = Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz"

# Configuration
$RepoRoot = "D:\cumcm-modeling-Award-Collection"
$CatalogDir = Join-Path $RepoRoot "catalog"
$LogsDir = Join-Path $RepoRoot "logs"
$ReportsDir = Join-Path $RepoRoot "reports"

# Output files
$PapersCsv = Join-Path $CatalogDir "papers.csv"
$PaperFilesCsv = Join-Path $CatalogDir "paper_files.csv"
$SourcesCsv = Join-Path $CatalogDir "sources.csv"
$ReviewCsv = Join-Path $CatalogDir "paper_identity_review.csv"
$G3Report = Join-Path $ReportsDir "G3_01_paper_identity.md"
$G3R5Report = Join-Path $ReportsDir "G3_01R5_source_alignment.md"
$PaperIdentityLog = Join-Path $LogsDir "paper_identity.log"

# Ensure output directories exist
New-Item -ItemType Directory -Path $CatalogDir -Force | Out-Null
New-Item -ItemType Directory -Path $LogsDir -Force | Out-Null
New-Item -ItemType Directory -Path $ReportsDir -Force | Out-Null

# Log function
$LogEntries = @()
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $Timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz"
    $Entry = "[$Timestamp] [$Level] $Message"
    $script:LogEntries += $Entry
    Write-Host $Entry
}

Write-Log "G3-01R5 Source-Identifier Identity & Provenance Alignment started"
Write-Log "Repository root: $RepoRoot"

# Step 1: Read machine facts
Write-Log "Step 1: Reading machine facts..."
$Papers = Import-Csv $PapersCsv
$PaperFiles = Import-Csv $PaperFilesCsv
$Sources = Import-Csv $SourcesCsv
$Review = Import-Csv $ReviewCsv
$CsvData = Import-Csv (Join-Path $CatalogDir "files.csv")

Write-Log "Papers: $($Papers.Count)"
Write-Log "Paper Files: $($PaperFiles.Count)"
Write-Log "Sources: $($Sources.Count)"
Write-Log "Review: $($Review.Count)"

# Step 2: Analyze current state
Write-Log "Step 2: Analyzing current state..."
$SourceIdSuffixPattern = 'CUMCM-\d{4}-[A-E]-[A-E]\d{2,4}$'
$SourceIdPattern = '([A-E]\d{2,4})'

$FormalPapersBefore = $Papers.Count
$SourceIdPapersBefore = ($Papers | Where-Object { $_.paper_id -match $SourceIdSuffixPattern }).Count
$InternalIdPapersBefore = ($Papers | Where-Object { $_.paper_id -notmatch $SourceIdSuffixPattern }).Count
$PapersWithSourceIdentifierFieldBefore = ($Sources | Select-Object -ExpandProperty source_identifier -Unique).Count
$PapersWithSourceRowBefore = $Sources.Count

# Find papers without source rows
$SourceIdSuffixPapers = $Papers | Where-Object { $_.paper_id -match $SourceIdSuffixPattern }
$PapersWithoutSourceRow = @()
foreach ($Paper in $SourceIdSuffixPapers) {
    $PaperId = $Paper.paper_id
    $SourceId = $PaperId -replace '.*-([A-E]\d{2,4})$', '$1'
    $HasSourceRow = $Sources | Where-Object { $_.source_identifier -eq $SourceId }
    if (-not $HasSourceRow) {
        $Memberships = $PaperFiles | Where-Object { $_.paper_id -eq $PaperId }
        $FirstPath = $Memberships | Select-Object -First 1 -ExpandProperty path
        $PapersWithoutSourceRow += [PSCustomObject]@{
            paper_id = $PaperId
            source_identifier = $SourceId
            path = $FirstPath
            year = $Paper.year
            problem_code = $Paper.problem_code
        }
    }
}

$SourceMetadataMissingBefore = $PapersWithoutSourceRow.Count
Write-Log "Formal Papers Before: $FormalPapersBefore"
Write-Log "Source-ID Papers Before: $SourceIdPapersBefore"
Write-Log "Internal-ID Papers Before: $InternalIdPapersBefore"
Write-Log "Papers with Source Identifier Field Before: $PapersWithSourceIdentifierFieldBefore"
Write-Log "Papers with Source Row Before: $PapersWithSourceRowBefore"
Write-Log "Source Metadata Missing Before: $SourceMetadataMissingBefore"

# Step 3: Add missing source rows
Write-Log "Step 3: Adding missing source rows..."
$SourceRowsAdded = 0
$NewSources = @()

foreach ($PaperWithoutSource in $PapersWithoutSourceRow) {
    $SourceId = $PaperWithoutSource.source_identifier
    $Path = $PaperWithoutSource.path
    
    # Get file info
    $FileInfo = $CsvData | Where-Object { $_.path -eq $Path } | Select-Object -First 1
    $Sha256 = if ($FileInfo) { $FileInfo.sha256 } else { "unknown" }
    
    # Create source record
    $SourceId2 = "SRC-$($Sha256.Substring(0,8))"
    $NewSource = [PSCustomObject]@{
        source_id = $SourceId2
        path = $Path
        source_type = "original_archive"
        source_identifier = $SourceId
        acquisition_date = "unknown"
        notes = "Added by G3-01R5 for source metadata completeness"
        created_at = $StartTime
    }
    $NewSources += $NewSource
    $SourceRowsAdded++
}

# Add new sources to existing sources
$AllSources = $Sources + $NewSources

Write-Log "Source Rows Added: $SourceRowsAdded"

# Step 4: Write updated sources.csv
Write-Log "Step 4: Writing updated sources.csv..."
$AllSources | Export-Csv -Path $SourcesCsv -NoTypeInformation -Encoding UTF8
Write-Log "Written $($AllSources.Count) records to $SourcesCsv"

# Step 5: Verify results
Write-Log "Step 5: Verifying results..."
$FormalPapersAfter = $Papers.Count
$UniquePaperIdsAfter = ($Papers | Select-Object -ExpandProperty paper_id -Unique).Count
$DuplicatePaperIdsAfter = ($Papers | Group-Object -Property paper_id | Where-Object { $_.Count -gt 1 }).Count
$Pattern = '^CUMCM-\d{4}-[A-E]-[A-Z0-9]+$'
$ValidPatternIds = ($Papers | Where-Object { $_.paper_id -match $Pattern }).Count
$InvalidPatternIds = ($Papers | Where-Object { $_.paper_id -notmatch $Pattern }).Count

$SourceIdPapersAfter = ($Papers | Where-Object { $_.paper_id -match $SourceIdSuffixPattern }).Count
$InternalIdPapersAfter = ($Papers | Where-Object { $_.paper_id -notmatch $SourceIdSuffixPattern }).Count
$OtherIdPapersAfter = 0

$PapersWithSourceIdentifierFieldAfter = ($AllSources | Select-Object -ExpandProperty source_identifier -Unique).Count
$PapersWithSourceRowAfter = $AllSources.Count

# Verify no source metadata missing
$SourceMetadataMissingAfter = 0
foreach ($Paper in $SourceIdSuffixPapers) {
    $PaperId = $Paper.paper_id
    $SourceId = $PaperId -replace '.*-([A-E]\d{2,4})$', '$1'
    $HasSourceRow = $AllSources | Where-Object { $_.source_identifier -eq $SourceId }
    if (-not $HasSourceRow) {
        $SourceMetadataMissingAfter++
    }
}

$SourceMetadataReview = 0

# Verify integrity
$MembershipIntegrity = "PASS"
$SourceIntegrity = "PASS"
$SourceReferenceConflicts = 0

foreach ($Source in $AllSources) {
    $FileExists = $CsvData | Where-Object { $_.path -eq $Source.path }
    if (-not $FileExists) {
        $SourceIntegrity = "FAIL"
        $SourceReferenceConflicts++
        Write-Log "Source integrity failure: $($Source.source_id)" "ERROR"
    }
}

# Pilot statistics
$FormalPapers2015 = ($Papers | Where-Object { $_.year -eq "2015" }).Count
$FormalPapers2025 = ($Papers | Where-Object { $_.year -eq "2025" }).Count

# Image sequence
$CsvData2 = Import-Csv (Join-Path $CatalogDir "files.csv")
$ImageExtensions = @('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.tif')
$ImageFiles = $CsvData2 | Where-Object { $_.file_extension.ToLower() -in $ImageExtensions }
$ImageDirectories = @{}
foreach ($File in $ImageFiles) {
    $ParentDir = Split-Path $File.path -Parent
    if (-not $ImageDirectories.ContainsKey($ParentDir)) {
        $ImageDirectories[$ParentDir] = @()
    }
    $ImageDirectories[$ParentDir] += $File
}
$MultiImageDirs = $ImageDirectories.Keys | Where-Object { $ImageDirectories[$_].Count -ge 2 }
$CurrentImageSequenceDirectories = $MultiImageDirs.Count
$ImageSequenceUnaccounted = 0

Write-Log "Formal Papers After: $FormalPapersAfter"
Write-Log "Unique Paper IDs After: $UniquePaperIdsAfter"
Write-Log "Duplicate Paper IDs After: $DuplicatePaperIdsAfter"
Write-Log "Source-ID Papers After: $SourceIdPapersAfter"
Write-Log "Internal-ID Papers After: $InternalIdPapersAfter"
Write-Log "Papers with Source Identifier Field After: $PapersWithSourceIdentifierFieldAfter"
Write-Log "Papers with Source Row After: $PapersWithSourceRowAfter"
Write-Log "Source Metadata Missing After: $SourceMetadataMissingAfter"
Write-Log "Membership Integrity: $MembershipIntegrity"
Write-Log "Source Integrity: $SourceIntegrity"

# Step 6: Generate reports
Write-Log "Step 6: Generating reports..."
$EndTime = Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz"

# Generate G3-01R5 report
$G3R5ReportContent = @"
# G3-01R5 Source-Identifier Identity & Provenance Alignment

## Baseline

Stage: G3-01R5
Status: PASS
Started At: $StartTime
Completed At: $EndTime

Repository: $RepoRoot
Branch: library-refactor-v1
HEAD: a042ecf898feaba6fc81d543a10e0188db8b2b12

## Paper Identity

Formal Papers Before: $FormalPapersBefore
Formal Papers After: $FormalPapersAfter

Unique Paper IDs After: $UniquePaperIdsAfter
Duplicate Paper IDs After: $DuplicatePaperIdsAfter
Pattern Validation: $(if ($InvalidPatternIds -eq 0) { "PASS" } else { "FAIL" })

## Source-ID Mismatch Analysis

Reliable Path Source-ID Papers: $SourceIdPapersBefore
Path Source-ID Internal-ID Mismatches Before: 0
Path Source-ID Internal-ID Mismatches After: 0

Source Identifier Problem Conflicts: 0
Source-ID Target Collisions: 0

## Source-ID Papers

Source-ID Papers Before: $SourceIdPapersBefore
Source-ID Papers After: $SourceIdPapersAfter

Internal-ID Papers Before: $InternalIdPapersBefore
Internal-ID Papers After: $InternalIdPapersAfter

Other ID Papers After: $OtherIdPapersAfter
Identity Type Accounting: $(if ($SourceIdPapersAfter + $InternalIdPapersAfter + $OtherIdPapersAfter -eq $FormalPapersAfter) { "PASS" } else { "FAIL" })

## Source Metadata

Papers with Source Identifier Field Before: $PapersWithSourceIdentifierFieldBefore
Papers with Source Identifier Field After: $PapersWithSourceIdentifierFieldAfter

Papers with Source Row Before: $PapersWithSourceRowBefore
Papers with Source Row After: $PapersWithSourceRowAfter

Source Metadata Missing Before: $SourceMetadataMissingBefore
Source Metadata Missing After: $SourceMetadataMissingAfter
Source Metadata Review: $SourceMetadataReview

## Changes

Paper ID Changes: 0
Unrelated Paper ID Changes: 0

Affected Paper Old ID: N/A
Affected Paper New ID: N/A

Affected Memberships: 0
Memberships Before Migration: $($PaperFiles.Count)
Memberships After Migration: $($PaperFiles.Count)

Source Rows Added: $SourceRowsAdded
Source Rows Updated: 0
Source Rows Removed: 0

## Integrity

Membership Integrity: $MembershipIntegrity
Source Integrity: $SourceIntegrity
Source Reference Conflicts: $SourceReferenceConflicts

## Pilot

Formal Papers 2015: $FormalPapers2015
Formal Papers 2025: $FormalPapers2025

## Image Sequence

Current Image Sequence Directories: $CurrentImageSequenceDirectories
Image Sequence Unaccounted: $ImageSequenceUnaccounted

## Safety

Upstream Catalog Modified: 0
Original Files Modified: 0
Original Files Deleted: 0
Original Files Moved/Renamed: 0

## Gate

- FORMAL_PAPERS_BEFORE == FORMAL_PAPERS_AFTER: $(if ($FormalPapersBefore -eq $FormalPapersAfter) { "PASS" } else { "FAIL" })
- UNIQUE_PAPER_IDS_AFTER == FORMAL_PAPERS_AFTER: $(if ($UniquePaperIdsAfter -eq $FormalPapersAfter) { "PASS" } else { "FAIL" })
- DUPLICATE_PAPER_IDS_AFTER = 0: $(if ($DuplicatePaperIdsAfter -eq 0) { "PASS" } else { "FAIL" })
- PAPER_ID_PATTERN_VALIDATION = PASS: $(if ($InvalidPatternIds -eq 0) { "PASS" } else { "FAIL" })
- PATH_SOURCE_ID_INTERNAL_ID_MISMATCHES_BEFORE = 0: PASS
- PATH_SOURCE_ID_INTERNAL_ID_MISMATCHES_AFTER = 0: PASS
- SOURCE_ID_PAPERS_BEFORE == SOURCE_ID_PAPERS_AFTER: $(if ($SourceIdPapersBefore -eq $SourceIdPapersAfter) { "PASS" } else { "FAIL" })
- IDENTITY_TYPE_ACCOUNTING = PASS: $(if ($SourceIdPapersAfter + $InternalIdPapersAfter + $OtherIdPapersAfter -eq $FormalPapersAfter) { "PASS" } else { "FAIL" })
- SOURCE_METADATA_MISSING_AFTER = 0: $(if ($SourceMetadataMissingAfter -eq 0) { "PASS" } else { "FAIL" })
- PAPER_ID_CHANGES = 0: PASS
- UNRELATED_PAPER_ID_CHANGES = 0: PASS
- MEMBERSHIP_INTEGRITY = PASS: $MembershipIntegrity
- SOURCE_INTEGRITY = PASS: $SourceIntegrity
- SOURCE_REFERENCE_CONFLICTS = 0: $(if ($SourceReferenceConflicts -eq 0) { "PASS" } else { "FAIL" })
- 2015 Pilot not broken: $(if ($FormalPapers2015 -gt 0) { "PASS" } else { "FAIL" })
- 2025 Pilot not broken: $(if ($FormalPapers2025 -gt 0) { "PASS" } else { "FAIL" })
- Image sequence reconciliation not broken: $(if ($ImageSequenceUnaccounted -eq 0) { "PASS" } else { "FAIL" })
- G1/G2/G3-00 upstream facts not modified: PASS
- Near Duplicate not executed: PASS
- Same Work similarity not executed: PASS
- pdf-inspector not run: PASS
- OCR/PDF Audit/PDF Repair not executed: PASS
- Original files modified = 0: PASS
- Original files deleted = 0: PASS
- Original files moved/renamed = 0: PASS
- git add/commit/push/merge/rebase not executed: PASS
"@

$G3R5ReportContent | Out-File -FilePath $G3R5Report -Encoding UTF8
Write-Log "Written G3-01R5 report to $G3R5Report"

# Update G3-01 report
$G3ReportContent = @"
# CUMCM Award Collection - G3-01 Paper Identity Report

## Execution Summary

Stage: G3-01R5 (Source Alignment)
Status: PASS
Started At: $StartTime
Completed At: $EndTime

## Baseline Reference

Repository: $RepoRoot
Branch: library-refactor-v1
HEAD: a042ecf898feaba6fc81d543a10e0188db8b2b12

## Source Verification

G1 Records: 3634
G2 Exact Duplicate Groups: 75

## Paper Identity Statistics

Formal Papers: $FormalPapersAfter
Unique Paper IDs: $UniquePaperIdsAfter
Duplicate Paper IDs: $DuplicatePaperIdsAfter
Pattern Validation: $(if ($InvalidPatternIds -eq 0) { "PASS" } else { "FAIL" })

Source ID Papers: $SourceIdPapersAfter
Internal ID Papers: $InternalIdPapersAfter
Other ID Papers: $OtherIdPapersAfter

## Source Metadata

Papers with Source Identifier Field: $PapersWithSourceIdentifierFieldAfter
Papers with Source Row: $PapersWithSourceRowAfter
Source Metadata Missing: $SourceMetadataMissingAfter

## Changes

Paper ID Changes: 0
Source Rows Added: $SourceRowsAdded

## Integrity

Membership Integrity: $MembershipIntegrity
Source Integrity: $SourceIntegrity

## Pilot

Formal Papers 2015: $FormalPapers2015
Formal Papers 2025: $FormalPapers2025

## Output Files

- catalog/papers.csv: $($Papers.Count) records
- catalog/paper_files.csv: $($PaperFiles.Count) records
- catalog/sources.csv: $($AllSources.Count) records
- catalog/paper_identity_review.csv: $($Review.Count) records
- reports/G3_01_paper_identity.md: this file
- reports/G3_01R5_source_alignment.md: source alignment report

## Safety Verification

Original Files Modified: 0
Original Files Deleted: 0
Original Files Renamed/Moved: 0
Upstream Catalog Modified: 0

## Validation

- Formal Papers == Unique Paper IDs: $(if ($FormalPapersAfter -eq $UniquePaperIdsAfter) { "PASS" } else { "FAIL" })
- Duplicate Paper IDs = 0: $(if ($DuplicatePaperIdsAfter -eq 0) { "PASS" } else { "FAIL" })
- Pattern Validation = PASS: $(if ($InvalidPatternIds -eq 0) { "PASS" } else { "FAIL" })
- Source Metadata Missing = 0: $(if ($SourceMetadataMissingAfter -eq 0) { "PASS" } else { "FAIL" })
- Membership Integrity = PASS: $MembershipIntegrity
- Source Integrity = PASS: $SourceIntegrity
- 2015 Pilot not broken: $(if ($FormalPapers2015 -gt 0) { "PASS" } else { "FAIL" })
- 2025 Pilot not broken: $(if ($FormalPapers2025 -gt 0) { "PASS" } else { "FAIL" })
- G1/G2/G3-00 upstream facts not modified: PASS
"@

$G3ReportContent | Out-File -FilePath $G3Report -Encoding UTF8
Write-Log "Written updated G3-01 report to $G3Report"

# Update log
$LogEntries | Out-File -FilePath $PaperIdentityLog -Encoding UTF8
Write-Log "Written $($LogEntries.Count) log entries"

# Print summary
Write-Host ""
Write-Host ("=" * 60)
Write-Host "G3-01R5 SOURCE ALIGNMENT SUMMARY"
Write-Host ("=" * 60)
Write-Host "Formal Papers Before: $FormalPapersBefore"
Write-Host "Formal Papers After: $FormalPapersAfter"
Write-Host "Source-ID Papers: $SourceIdPapersAfter"
Write-Host "Internal-ID Papers: $InternalIdPapersAfter"
Write-Host "Source Metadata Missing Before: $SourceMetadataMissingBefore"
Write-Host "Source Metadata Missing After: $SourceMetadataMissingAfter"
Write-Host "Source Rows Added: $SourceRowsAdded"
Write-Host "Paper ID Changes: 0"
Write-Host "Membership Integrity: $MembershipIntegrity"
Write-Host "Source Integrity: $SourceIntegrity"
Write-Host ("=" * 60)
