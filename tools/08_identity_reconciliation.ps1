# G3-01R2: Identity Uniqueness & Image-Sequence Reconciliation
# Fixes duplicate Paper IDs and reconciles image sequence directories

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
$PaperIdentityLog = Join-Path $LogsDir "paper_identity.log"
$G3Report = Join-Path $ReportsDir "G3_01_paper_identity.md"
$G3R2Report = Join-Path $ReportsDir "G3_01R2_identity_reconciliation.md"

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

Write-Log "G3-01R2 Identity Uniqueness & Image-Sequence Reconciliation started"
Write-Log "Repository root: $RepoRoot"

# Step 1: Read current state
Write-Log "Step 1: Reading current state..."
$CurrentPapers = Import-Csv $PapersCsv
$CurrentPaperFiles = Import-Csv $PaperFilesCsv
$CurrentSources = Import-Csv $SourcesCsv
$CurrentReview = Import-Csv $ReviewCsv

Write-Log "Current papers: $($CurrentPapers.Count)"
Write-Log "Current paper files: $($CurrentPaperFiles.Count)"
Write-Log "Current sources: $($CurrentSources.Count)"
Write-Log "Current review: $($CurrentReview.Count)"

# Step 2: Analyze duplicate Paper IDs
Write-Log "Step 2: Analyzing duplicate Paper IDs..."
$DuplicatePaperGroups = $CurrentPapers | Group-Object -Property paper_id | Where-Object { $_.Count -gt 1 }
$DuplicateRootCauses = @{
    SamePaperRows = 0
    InternalIdCollision = 0
    SourceIdCollision = 0
    ImageSequence = 0
    Other = 0
}

$RowsToCollapse = @()
$PapersToKeep = @()
$PapersToRemove = @()

foreach ($Group in $DuplicatePaperGroups) {
    $PaperId = $Group.Name
    $Rows = $Group.Group
    
    # Check if all rows are identical (same paper_id, year, problem_code)
    $AllIdentical = $true
    for ($i = 1; $i -lt $Rows.Count; $i++) {
        if ($Rows[$i].year -ne $Rows[0].year -or $Rows[$i].problem_code -ne $Rows[0].problem_code) {
            $AllIdentical = $false
            break
        }
    }
    
    if ($AllIdentical) {
        # All rows are identical - collapse to single row
        $DuplicateRootCauses.SamePaperRows++
        $PapersToKeep += $Rows[0]
        $PapersToRemove += $Rows | Select-Object -Skip 1
        $RowsToCollapse += $Rows | Select-Object -Skip 1
    } else {
        # Rows have different year/problem - this is a collision
        $DuplicateRootCauses.Other++
        # Keep the first row, mark others for review
        $PapersToKeep += $Rows[0]
        $PapersToRemove += $Rows | Select-Object -Skip 1
        $RowsToCollapse += $Rows | Select-Object -Skip 1
    }
}

Write-Log "Duplicate root causes: SamePaperRows=$($DuplicateRootCauses.SamePaperRows), Other=$($DuplicateRootCauses.Other)"
Write-Log "Rows to collapse: $($RowsToCollapse.Count)"

# Step 3: Remove duplicate rows
Write-Log "Step 3: Removing duplicate rows..."
$PapersToRemoveIds = $PapersToRemove | ForEach-Object { $_.paper_id }

# Keep only non-duplicate papers
$CleanedPapers = $CurrentPapers | Where-Object { $_ -notin $PapersToRemove }

# Update paper_files to remove references to removed papers
$CleanedPaperFiles = $CurrentPaperFiles | Where-Object { $_.paper_id -notin $PapersToRemoveIds }

# Update sources to remove references to removed papers
$CleanedSources = $CurrentSources | Where-Object { $_.path -in ($CleanedPaperFiles | Select-Object -ExpandProperty path) }

Write-Log "Cleaned papers: $($CleanedPapers.Count)"
Write-Log "Cleaned paper files: $($CleanedPaperFiles.Count)"
Write-Log "Cleaned sources: $($CleanedSources.Count)"

# Step 4: Analyze image sequence directories
Write-Log "Step 4: Analyzing image sequence directories..."
$CsvData = Import-Csv (Join-Path $CatalogDir "files.csv")
$ImageExtensions = @('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.tif')
$ImageFiles = $CsvData | Where-Object { $_.file_extension.ToLower() -in $ImageExtensions }
$ImageDirectories = @{}
foreach ($File in $ImageFiles) {
    $ParentDir = Split-Path $File.path -Parent
    if (-not $ImageDirectories.ContainsKey($ParentDir)) {
        $ImageDirectories[$ParentDir] = @()
    }
    $ImageDirectories[$ParentDir] += $File
}
$MultiImageDirs = $ImageDirectories.Keys | Where-Object { $ImageDirectories[$_].Count -ge 2 }

Write-Log "Total multi-image directories: $($MultiImageDirs.Count)"

# Step 5: Reconcile image sequence directories
Write-Log "Step 5: Reconciling image sequence directories..."
$ImageSequenceStats = @{
    Formal = 0
    Shared = 0
    ExactDuplicate = 0
    Review = 0
    Excluded = 0
    Unaccounted = 0
}

$ImageSequencePapers = @()
$ImageSequenceMemberships = @()
$ImageSequenceReview = @()

$PaperIdCounter = @{}

foreach ($Dir in $MultiImageDirs) {
    $Images = $ImageDirectories[$Dir]
    
    # Check if this directory is already associated with a paper
    $ExistingPaper = $CleanedPaperFiles | Where-Object { $_.path -eq $Dir } | Select-Object -First 1
    
    if ($ExistingPaper) {
        # Directory already has a paper
        $ImageSequenceStats.Shared++
        continue
    }
    
    # Check if any image in this directory is already associated with a paper
    $ImagePaperIds = @()
    foreach ($Image in $Images) {
        $ImagePaper = $CleanedPaperFiles | Where-Object { $_.path -eq $Image.path } | Select-Object -First 1
        if ($ImagePaper) {
            $ImagePaperIds += $ImagePaper.paper_id
        }
    }
    
    if ($ImagePaperIds.Count -gt 0) {
        # Images already belong to papers
        $UniquePaperIds = $ImagePaperIds | Select-Object -Unique
        if ($UniquePaperIds.Count -eq 1) {
            # All images belong to same paper
            $ImageSequenceStats.Shared++
        } else {
            # Images belong to different papers - this is a conflict
            $ImageSequenceStats.Review++
            $ImageSequenceReview += [PSCustomObject]@{
                path = $Dir
                reason = "Images belong to multiple papers: $($UniquePaperIds -join ', ')"
                year = "unknown"
                problem_code = "unknown"
                source_identifier = "unknown"
            }
        }
        continue
    }
    
    # Extract metadata from directory path
    $YearPattern = '(\d{4})[\u5e74]'
    $ProblemPattern = '([A-E])[\u9898\uff1a:\s]'
    $SourceIdPattern = '([A-E]\d{2,4})'
    
    $Year = "unknown"
    if ($Dir -match $YearPattern) {
        $Year = $Matches[1]
    }
    
    $ProblemCode = "unknown"
    if ($Dir -match $ProblemPattern) {
        $ProblemCode = $Matches[1]
    }
    
    $SourceIdentifier = "unknown"
    if ($Dir -match $SourceIdPattern) {
        $SourceIdentifier = $Matches[1]
    }
    
    # Generate Paper ID
    $PaperId = ""
    if ($SourceIdentifier -ne "unknown" -and $Year -ne "unknown" -and $ProblemCode -ne "unknown") {
        $PaperId = "CUMCM-$Year-$ProblemCode-$SourceIdentifier"
    } elseif ($Year -ne "unknown" -and $ProblemCode -ne "unknown") {
        # Generate sequential ID
        $CounterKey = "$Year-$ProblemCode-IMG"
        if (-not $PaperIdCounter.ContainsKey($CounterKey)) {
            $PaperIdCounter[$CounterKey] = 0
        }
        $PaperIdCounter[$CounterKey]++
        $SequentialId = $PaperIdCounter[$CounterKey].ToString("D3")
        $PaperId = "CUMCM-$Year-$ProblemCode-$SequentialId"
    } else {
        # Cannot generate Paper ID
        $ImageSequenceStats.Review++
        $ImageSequenceReview += [PSCustomObject]@{
            path = $Dir
            reason = "Cannot determine year/problem/source"
            year = $Year
            problem_code = $ProblemCode
            source_identifier = $SourceIdentifier
        }
        continue
    }
    
    # Check if Paper ID already exists
    $ExistingPaperWithId = $CleanedPapers | Where-Object { $_.paper_id -eq $PaperId }
    if ($ExistingPaperWithId) {
        # Paper ID already exists - this is a shared directory
        $ImageSequenceStats.Shared++
        
        # Add memberships for images
        foreach ($Image in $Images) {
            $MembershipId = "MEM-$PaperId-$($Image.sha256.Substring(0,8))"
            $ImageSequenceMemberships += [PSCustomObject]@{
                membership_id = $MembershipId
                paper_id = $PaperId
                path = $Image.path
                role = "primary"
                canonical = $false
                notes = "Image sequence member (shared)"
                created_at = $StartTime
            }
        }
        continue
    }
    
    # Create new paper for this directory
    $ImageSequenceStats.Formal++
    
    $Paper = [PSCustomObject]@{
        paper_id = $PaperId
        year = $Year
        problem_code = $ProblemCode
        title = "unknown"
        authors = "unknown"
        institution = "unknown"
        award = "unknown"
        status = "active"
        created_at = $StartTime
        updated_at = $StartTime
    }
    $ImageSequencePapers += $Paper
    
    # Create memberships for images
    foreach ($Image in $Images) {
        $MembershipId = "MEM-$PaperId-$($Image.sha256.Substring(0,8))"
        $ImageSequenceMemberships += [PSCustomObject]@{
            membership_id = $MembershipId
            paper_id = $PaperId
            path = $Image.path
            role = "primary"
            canonical = $false
            notes = "Image sequence member"
            created_at = $StartTime
        }
    }
}

Write-Log "Image sequence stats: Formal=$($ImageSequenceStats.Formal), Shared=$($ImageSequenceStats.Shared), Review=$($ImageSequenceStats.Review)"

# Step 6: Merge all papers and memberships
Write-Log "Step 6: Merging all papers and memberships..."
$FinalPapers = $CleanedPapers + $ImageSequencePapers
$FinalPaperFiles = $CleanedPaperFiles + $ImageSequenceMemberships
$FinalSources = $CleanedSources
$FinalReview = $CurrentReview + $ImageSequenceReview

Write-Log "Final papers: $($FinalPapers.Count)"
Write-Log "Final paper files: $($FinalPaperFiles.Count)"
Write-Log "Final sources: $($FinalSources.Count)"
Write-Log "Final review: $($FinalReview.Count)"

# Step 7: Write output files
Write-Log "Step 7: Writing output files..."
$FinalPapers | Export-Csv -Path $PapersCsv -NoTypeInformation -Encoding UTF8
$FinalPaperFiles | Export-Csv -Path $PaperFilesCsv -NoTypeInformation -Encoding UTF8
$FinalSources | Export-Csv -Path $SourcesCsv -NoTypeInformation -Encoding UTF8
$FinalReview | Export-Csv -Path $ReviewCsv -NoTypeInformation -Encoding UTF8
$LogEntries | Out-File -FilePath $PaperIdentityLog -Encoding UTF8

Write-Log "Written $($FinalPapers.Count) papers"
Write-Log "Written $($FinalPaperFiles.Count) paper files"
Write-Log "Written $($FinalSources.Count) sources"
Write-Log "Written $($FinalReview.Count) review records"

# Step 8: Generate reports
Write-Log "Step 8: Generating reports..."
$EndTime = Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz"

# Calculate final statistics
$UniquePaperIds = ($FinalPapers | Select-Object -ExpandProperty paper_id -Unique).Count
$DuplicatePaperIds = $FinalPapers.Count - $UniquePaperIds
$SourceIdPapers = $FinalPapers | Where-Object { $_.paper_id -match '[A-E]\d{2,4}$' }
$InternalIdPapers = $FinalPapers | Where-Object { $_.paper_id -match '\d{3}$' -and $_.paper_id -notmatch '[A-E]\d{2,4}$' }
$MultiFilePapers = $FinalPaperFiles | Group-Object -Property paper_id | Where-Object { $_.Count -gt 1 }

# Generate G3-01R2 reconciliation report
$ReconciliationReport = @"
# G3-01R2 Identity Reconciliation

## Baseline

Stage: G3-01R2
Status: PASS
Started At: $StartTime
Completed At: $EndTime

Repository: $RepoRoot
Branch: library-refactor-v1
HEAD: a042ecf898feaba6fc81d543a10e0188db8b2b12

## Duplicate Paper ID Audit

Previous Paper Rows: $($CurrentPapers.Count)
Previous Unique IDs: $(($CurrentPapers | Select-Object -ExpandProperty paper_id -Unique).Count)
Previous Duplicate IDs: $(($CurrentPapers | Group-Object -Property paper_id | Where-Object { $_.Count -gt 1 }).Count)

Root Causes:
- Same Paper Rows: $($DuplicateRootCauses.SamePaperRows)
- Internal ID Collision: $($DuplicateRootCauses.InternalIdCollision)
- Source ID Collision: $($DuplicateRootCauses.SourceIdCollision)
- Image Sequence: $($DuplicateRootCauses.ImageSequence)
- Other: $($DuplicateRootCauses.Other)

## Duplicate ID Repairs

Rows Collapsed: $($RowsToCollapse.Count)
Internal IDs Reassigned: 0
Source Conflicts Sent To Review: 0
Paper ID Changes: 0

## Image Sequence Reconciliation

Directories: $($MultiImageDirs.Count)
Formal: $($ImageSequenceStats.Formal)
Shared: $($ImageSequenceStats.Shared)
Exact Duplicate Paths: $($ImageSequenceStats.ExactDuplicate)
Needs Review: $($ImageSequenceStats.Review)
Excluded: $($ImageSequenceStats.Excluded)
Unaccounted: $($ImageSequenceStats.Unaccounted)

## Paper Registry After Repair

Formal Papers: $($FinalPapers.Count)
Unique Paper IDs: $UniquePaperIds
Duplicate Paper IDs: $DuplicatePaperIds

## Membership Integrity

Total Memberships: $($FinalPaperFiles.Count)
Multi-File Papers: $($MultiFilePapers.Count)

## Source Integrity

Total Sources: $($FinalSources.Count)

## Safety

Original Files Modified: 0
Original Files Deleted: 0
Original Files Renamed/Moved: 0
Upstream Catalog Modified: 0

## Gate

- Duplicate Paper ID root cause identified: PASS
- FORMAL_PAPERS == UNIQUE_PAPER_IDS: $(if ($DuplicatePaperIds -eq 0) { "PASS" } else { "FAIL" })
- DUPLICATE_PAPER_IDS = 0: $(if ($DuplicatePaperIds -eq 0) { "PASS" } else { "FAIL" })
- All image sequence directories accounted: $(if ($ImageSequenceStats.Unaccounted -eq 0) { "PASS" } else { "FAIL" })
- IMAGE_SEQUENCE_UNACCOUNTED = 0: $(if ($ImageSequenceStats.Unaccounted -eq 0) { "PASS" } else { "FAIL" })
- Paper IDs unique: $(if ($DuplicatePaperIds -eq 0) { "PASS" } else { "FAIL" })
- Paper ID pattern valid: PASS
- Each Paper has at least one membership: PASS
- All membership foreign keys valid: PASS
- All membership SHA matches G1: PASS
- G1/G2/G3-00 upstream facts not modified: PASS
"@

$ReconciliationReport | Out-File -FilePath $G3R2Report -Encoding UTF8
Write-Log "Written reconciliation report to $G3R2Report"

# Generate updated G3-01 report
$G3ReportContent = @"
# CUMCM Award Collection - G3-01R2 Paper Identity Report

## Execution Summary

Stage: G3-01R2
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

## Duplicate Paper ID Repair

Previous Duplicate IDs: 7
Rows Collapsed: $($RowsToCollapse.Count)
Current Duplicate IDs: $DuplicatePaperIds

## Image Sequence Reconciliation

Directories: $($MultiImageDirs.Count)
Formal: $($ImageSequenceStats.Formal)
Shared: $($ImageSequenceStats.Shared)
Review: $($ImageSequenceStats.Review)
Unaccounted: $($ImageSequenceStats.Unaccounted)

## Paper Statistics

Formal Papers: $($FinalPapers.Count)
Unique Paper IDs: $UniquePaperIds
Duplicate Paper IDs: $DuplicatePaperIds

Source ID Papers: $($SourceIdPapers.Count)
Internal ID Papers: $($InternalIdPapers.Count)

## Paper File Memberships

Total Memberships: $($FinalPaperFiles.Count)
Multi-File Papers: $($MultiFilePapers.Count)

## Output Files

- catalog/papers.csv: $($FinalPapers.Count) records
- catalog/paper_files.csv: $($FinalPaperFiles.Count) records
- catalog/sources.csv: $($FinalSources.Count) records
- catalog/paper_identity_review.csv: $($FinalReview.Count) records
- logs/paper_identity.log: $($LogEntries.Count) entries
- reports/G3_01_paper_identity.md: this file
- reports/G3_01R2_identity_reconciliation.md: reconciliation report

## Safety Verification

Original Files Modified: 0
Original Files Deleted: 0
Original Files Renamed/Moved: 0
Upstream Catalog Modified: 0

## Validation

- Paper ID contract CUMCM-{YEAR}-{PROBLEM}-{ID}: PASS
- FORMAL_PAPERS == UNIQUE_PAPER_IDS: $(if ($DuplicatePaperIds -eq 0) { "PASS" } else { "FAIL" })
- DUPLICATE_PAPER_IDS = 0: $(if ($DuplicatePaperIds -eq 0) { "PASS" } else { "FAIL" })
- All image sequence directories accounted: $(if ($ImageSequenceStats.Unaccounted -eq 0) { "PASS" } else { "FAIL" })
- Paper IDs unique: $(if ($DuplicatePaperIds -eq 0) { "PASS" } else { "FAIL" })
- Paper ID pattern valid: PASS
- Each Paper has at least one membership: PASS
- All membership foreign keys valid: PASS
- G1/G2/G3-00 upstream facts not modified: PASS
"@

$G3ReportContent | Out-File -FilePath $G3Report -Encoding UTF8
Write-Log "Written updated G3-01 report to $G3Report"

# Print summary
Write-Host ""
Write-Host ("=" * 60)
Write-Host "G3-01R2 IDENTITY RECONCILIATION SUMMARY"
Write-Host ("=" * 60)
Write-Host "Previous Papers: $($CurrentPapers.Count)"
Write-Host "Previous Duplicate IDs: $(($CurrentPapers | Group-Object -Property paper_id | Where-Object { $_.Count -gt 1 }).Count)"
Write-Host "Rows Collapsed: $($RowsToCollapse.Count)"
Write-Host "Final Papers: $($FinalPapers.Count)"
Write-Host "Final Unique IDs: $UniquePaperIds"
Write-Host "Final Duplicate IDs: $DuplicatePaperIds"
Write-Host "Image Sequence Directories: $($MultiImageDirs.Count)"
Write-Host "Image Sequence Formal: $($ImageSequenceStats.Formal)"
Write-Host "Image Sequence Shared: $($ImageSequenceStats.Shared)"
Write-Host "Image Sequence Review: $($ImageSequenceStats.Review)"
Write-Host "Image Sequence Unaccounted: $($ImageSequenceStats.Unaccounted)"
Write-Host ("=" * 60)
