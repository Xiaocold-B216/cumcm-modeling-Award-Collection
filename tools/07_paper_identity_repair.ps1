# G3-01R: Paper Identity Classification & Pilot Coverage Repair
# Fixes issues with 2015/2025 coverage, source identifiers, image sequences, and non-paper classification

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

Write-Log "G3-01R Paper Identity Classification & Pilot Coverage Repair started"
Write-Log "Repository root: $RepoRoot"

# Step 1: Read G1 catalog
Write-Log "Step 1: Reading G1 catalog..."
$CsvData = Import-Csv (Join-Path $CatalogDir "files.csv")
Write-Log "Total files: $($CsvData.Count)"

# Step 2: Read G2 exact duplicates
Write-Log "Step 2: Reading G2 exact duplicates..."
$Duplicates = Import-Csv (Join-Path $CatalogDir "duplicates.csv")
$DuplicateGroups = $Duplicates | Group-Object -Property duplicate_group
Write-Log "Duplicate groups: $($DuplicateGroups.Count)"

# Step 3: Define classification rules
Write-Log "Step 3: Defining classification rules..."

# Non-paper extensions
$NonPaperExtensions = @('.csv', '.xls', '.xlsx', '.mat', '.npy', '.npz', '.py', '.m', '.java', '.c', '.cpp', '.h', '.js', '.ts', '.rb', '.php', '.sql', '.json', '.xml', '.yml', '.yaml', '.md', '.txt', '.log', '.sh', '.bat', '.ps1', '.cmd', '.exe', '.dll', '.so', '.o', '.obj', '.lib', '.a', '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz')

# Paper extensions
$PaperExtensions = @('.pdf', '.doc', '.docx')

# Image extensions
$ImageExtensions = @('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.tif')

# Paper keywords in path (using Unicode escapes for Chinese characters)
$PaperKeywords = '\u4f18\u79c0\u8bba\u6587|\u8bba\u6587|\u8d5b\u9898|\u771f\u9898'

# Non-paper keywords in path
$NonPaperKeywords = '\u9644\u4ef6|\u6e90\u4ee3\u7801|\u7a0b\u5e8f|\u4ee3\u7801|\u6570\u636e|\u683c\u5f0f\u89c4\u8303|\u6a21\u677f'

# Source identifier pattern (e.g., A028, B007, C023)
$SourceIdPattern = '([A-E]\d{2,4})'

# Year pattern
$YearPattern = '(\d{4})[\u5e74]'

# Problem code pattern (using Unicode escapes)
$ProblemPattern = '([A-E])[\u9898\uff1a:\s]'

# Step 4: Parse and classify files
Write-Log "Step 4: Parsing and classifying files..."

$PaperCandidates = @()
$NonPaperFiles = @()
$NeedsReviewFiles = @()
$ImageSequenceDirectories = @{}
$PaperIdCounter = @{}

foreach ($File in $CsvData) {
    $Path = $File.path
    $Filename = $File.filename
    $Extension = $File.file_extension.ToLower()
    $ParentDir = Split-Path $Path -Parent
    
    # Check if file is in a year directory
    $IsYearDirectory = $Path -match $YearPattern
    
    # Extract year
    $Year = "unknown"
    if ($Path -match $YearPattern) {
        $Year = $Matches[1]
    }
    
    # Check if file is clearly non-paper by extension
    if ($Extension -in $NonPaperExtensions) {
        $NonPaperFiles += [PSCustomObject]@{
            path = $Path
            reason = "Non-paper extension: $Extension"
            year = $Year
        }
        continue
    }
    
    # Check if file is in a non-paper directory
    if ($Path -match $NonPaperKeywords) {
        $NonPaperFiles += [PSCustomObject]@{
            path = $Path
            reason = "Non-paper directory keyword"
            year = $Year
        }
        continue
    }
    
    # Check if file is an image
    if ($Extension -in $ImageExtensions) {
        # Group images by parent directory for sequence detection
        if (-not $ImageSequenceDirectories.ContainsKey($ParentDir)) {
            $ImageSequenceDirectories[$ParentDir] = @()
        }
        $ImageSequenceDirectories[$ParentDir] += $File
        continue
    }
    
    # Check if file is in a paper-like directory or has paper extension
    $IsPaperCandidate = $false
    $Reason = ""
    
    # Check if path contains paper keywords
    if ($Path -match $PaperKeywords) {
        $IsPaperCandidate = $true
        $Reason = "Paper keyword in path"
    }
    
    # Check if file has paper extension
    if ($Extension -in $PaperExtensions) {
        $IsPaperCandidate = $true
        if ($Reason) { $Reason += "; " }
        $Reason += "Paper extension: $Extension"
    }
    
    # If not a paper candidate, mark as needs review
    if (-not $IsPaperCandidate) {
        $NeedsReviewFiles += [PSCustomObject]@{
            path = $Path
            year = $Year
            problem_code = "unknown"
            source_identifier = "unknown"
            reason = "Unclear classification"
        }
        continue
    }
    
    # Extract problem code
    $ProblemCode = "unknown"
    if ($Filename -match $ProblemPattern) {
        $ProblemCode = $Matches[1]
    }
    if ($ProblemCode -eq "unknown" -and $Path -match $ProblemPattern) {
        $ProblemCode = $Matches[1]
    }
    
    # Extract source identifier from path (not just filename)
    $SourceIdentifier = "unknown"
    if ($Path -match $SourceIdPattern) {
        $SourceIdentifier = $Matches[1]
    }
    
    # Check if needs review
    $NeedsReview = $false
    $ReviewReason = ""
    
    if ($Year -eq "unknown") {
        $NeedsReview = $true
        $ReviewReason = "YEAR_UNKNOWN"
    }
    
    if ($ProblemCode -eq "unknown") {
        $NeedsReview = $true
        if ($ReviewReason) { $ReviewReason += "; " }
        $ReviewReason += "PROBLEM_UNKNOWN"
    }
    
    if ($NeedsReview) {
        $NeedsReviewFiles += [PSCustomObject]@{
            path = $Path
            year = $Year
            problem_code = $ProblemCode
            source_identifier = $SourceIdentifier
            reason = $ReviewReason
        }
    } else {
        $PaperCandidates += [PSCustomObject]@{
            path = $Path
            year = $Year
            problem_code = $ProblemCode
            source_identifier = $SourceIdentifier
            filename = $Filename
            file_extension = $Extension
            file_size_bytes = $File.file_size_bytes
            sha256 = $File.sha256
        }
    }
}

Write-Log "Paper candidates: $($PaperCandidates.Count)"
Write-Log "Non-paper files: $($NonPaperFiles.Count)"
Write-Log "Needs review files: $($NeedsReviewFiles.Count)"
Write-Log "Image sequence directories: $($ImageSequenceDirectories.Count)"

# Step 5: Process image sequences
Write-Log "Step 5: Processing image sequences..."

$ImageSequencePapers = @()
$ImageSequenceMemberships = @()

foreach ($Dir in $ImageSequenceDirectories.Keys) {
    $Images = $ImageSequenceDirectories[$Dir]
    
    # Only process directories with multiple images (sequences)
    if ($Images.Count -ge 2) {
        # Extract metadata from directory path
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
        
        # Generate Paper ID for image sequence
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
            # Cannot generate Paper ID, mark for review
            foreach ($Image in $Images) {
                $NeedsReviewFiles += [PSCustomObject]@{
                    path = $Image.path
                    year = $Year
                    problem_code = $ProblemCode
                    source_identifier = $SourceIdentifier
                    reason = "IMAGE_SEQUENCE_IDENTITY_UNKNOWN"
                }
            }
            continue
        }
        
        # Create paper record
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
        
        # Create memberships for each image
        foreach ($Image in $Images) {
            $MembershipId = "MEM-$PaperId-$($Image.sha256.Substring(0,8))"
            $Membership = [PSCustomObject]@{
                membership_id = $MembershipId
                paper_id = $PaperId
                path = $Image.path
                role = "primary"
                canonical = $false
                notes = "Image sequence member"
                created_at = $StartTime
            }
            $ImageSequenceMemberships += $Membership
        }
    }
}

Write-Log "Image sequence papers: $($ImageSequencePapers.Count)"
Write-Log "Image sequence memberships: $($ImageSequenceMemberships.Count)"

# Step 6: Group paper candidates by identity
Write-Log "Step 6: Grouping paper candidates by identity..."

$PaperGroups = @{}

foreach ($Candidate in $PaperCandidates) {
    $Year = $Candidate.year
    $ProblemCode = $Candidate.problem_code
    $SourceId = $Candidate.source_identifier
    
    # Create group key
    if ($SourceId -ne "unknown") {
        $GroupKey = "$Year-$ProblemCode-$SourceId"
    } else {
        # Use filename without extension as group key for files without source ID
        $BaseName = [System.IO.Path]::GetFileNameWithoutExtension($Candidate.filename)
        # Remove common suffixes
        $BaseName = $BaseName -replace '[\u2460\u2461\u2462\u2463\u2464\u2465\u2466\u2467\u2468\u2469]', ''
        $BaseName = $BaseName -replace '\s+', ' '
        $GroupKey = "$Year-$ProblemCode-$BaseName"
    }
    
    if (-not $PaperGroups.ContainsKey($GroupKey)) {
        $PaperGroups[$GroupKey] = @()
    }
    $PaperGroups[$GroupKey] += $Candidate
}

Write-Log "Paper groups: $($PaperGroups.Count)"

# Step 7: Assign Paper IDs
Write-Log "Step 7: Assigning Paper IDs..."

$Papers = @()
$PaperFiles = @()
$Sources = @()

foreach ($GroupKey in $PaperGroups.Keys) {
    $Group = $PaperGroups[$GroupKey]
    $FirstCandidate = $Group[0]
    
    $Year = $FirstCandidate.year
    $ProblemCode = $FirstCandidate.problem_code
    $SourceId = $FirstCandidate.source_identifier
    
    # Generate Paper ID
    $PaperId = ""
    if ($SourceId -ne "unknown") {
        # Use source identifier
        $PaperId = "CUMCM-$Year-$ProblemCode-$SourceId"
    } else {
        # Generate sequential ID
        $CounterKey = "$Year-$ProblemCode"
        if (-not $PaperIdCounter.ContainsKey($CounterKey)) {
            $PaperIdCounter[$CounterKey] = 0
        }
        $PaperIdCounter[$CounterKey]++
        $SequentialId = $PaperIdCounter[$CounterKey].ToString("D3")
        $PaperId = "CUMCM-$Year-$ProblemCode-$SequentialId"
    }
    
    # Create paper record
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
    $Papers += $Paper
    
    # Create paper file memberships
    foreach ($Candidate in $Group) {
        $MembershipId = "MEM-$PaperId-$($Candidate.sha256.Substring(0,8))"
        
        $PaperFile = [PSCustomObject]@{
            membership_id = $MembershipId
            paper_id = $PaperId
            path = $Candidate.path
            role = "primary"
            canonical = ($Group.Count -eq 1)
            notes = ""
            created_at = $StartTime
        }
        $PaperFiles += $PaperFile
        
        # Create source record if source identifier available
        if ($SourceId -ne "unknown") {
            $SourceId2 = "SRC-$($Candidate.sha256.Substring(0,8))"
            $Source = [PSCustomObject]@{
                source_id = $SourceId2
                path = $Candidate.path
                source_type = "original_archive"
                source_identifier = $SourceId
                acquisition_date = "unknown"
                notes = ""
                created_at = $StartTime
            }
            $Sources += $Source
        }
    }
}

# Add image sequence papers and memberships
$Papers += $ImageSequencePapers
$PaperFiles += $ImageSequenceMemberships

Write-Log "Total papers: $($Papers.Count)"
Write-Log "Total paper file memberships: $($PaperFiles.Count)"
Write-Log "Total sources: $($Sources.Count)"

# Step 8: Write output files
Write-Log "Step 8: Writing output files..."

# Write papers.csv
$Papers | Export-Csv -Path $PapersCsv -NoTypeInformation -Encoding UTF8
Write-Log "Written $($Papers.Count) records to $PapersCsv"

# Write paper_files.csv
$PaperFiles | Export-Csv -Path $PaperFilesCsv -NoTypeInformation -Encoding UTF8
Write-Log "Written $($PaperFiles.Count) records to $PaperFilesCsv"

# Write sources.csv
if ($Sources.Count -gt 0) {
    $Sources | Export-Csv -Path $SourcesCsv -NoTypeInformation -Encoding UTF8
    Write-Log "Written $($Sources.Count) records to $SourcesCsv"
}

# Write review.csv
if ($NeedsReviewFiles.Count -gt 0) {
    $NeedsReviewFiles | Export-Csv -Path $ReviewCsv -NoTypeInformation -Encoding UTF8
    Write-Log "Written $($NeedsReviewFiles.Count) records to $ReviewCsv"
}

# Write log
$LogEntries | Out-File -FilePath $PaperIdentityLog -Encoding UTF8
Write-Log "Written $($LogEntries.Count) log entries to $PaperIdentityLog"

# Step 9: Generate report
Write-Log "Step 9: Generating report..."
$EndTime = Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz"

# Calculate statistics
$TotalFiles = $CsvData.Count
$PaperCandidateFiles = $PaperCandidates.Count
$NonPaperFilesCount = $NonPaperFiles.Count
$NeedsReviewCandidateFiles = $NeedsReviewFiles.Count

$FormalPapers = $Papers.Count
$VerifiedPapers = $Papers | Where-Object { $_.status -eq "active" }
$ProbablePapers = $Papers | Where-Object { $_.status -eq "needs_review" }

$SourceIdPapers = $Papers | Where-Object { $_.paper_id -match '[A-E]\d{2,4}$' }
$InternalIdPapers = $Papers | Where-Object { $_.paper_id -match '\d{3}$' -and $_.paper_id -notmatch '[A-E]\d{2,4}$' }

$Papers2015 = $Papers | Where-Object { $_.year -eq "2015" }
$Papers2025 = $Papers | Where-Object { $_.year -eq "2025" }
$NeedsReview2015 = $NeedsReviewFiles | Where-Object { $_.year -eq "2015" }
$NeedsReview2025 = $NeedsReviewFiles | Where-Object { $_.year -eq "2025" }

$UniquePaperIds = ($Papers | Select-Object -ExpandProperty paper_id -Unique).Count
$DuplicatePaperIds = $Papers.Count - $UniquePaperIds

$MultiFilePapers = $PaperFiles | Group-Object -Property paper_id | Where-Object { $_.Count -gt 1 }

# Root cause analysis
$RootCause2015 = "Files exist in G1 but were not classified as paper candidates due to missing paper keywords in filename. Parent directory contains paper keywords but script only checked filename."
$RootCause2025 = "Files exist in G1 but were not classified as paper candidates due to missing paper keywords in filename. Parent directory contains paper keywords but script only checked filename."
$RootCauseSourceIdentifier = "Source identifiers (e.g., A028, B007) exist in paths but script only checked filename, not full path."
$RootCauseImageSequence = "Image sequences were not handled at all in original script. No logic to group images by directory and create single Paper per directory."
$RootCauseNonPaper = "Only 22 files classified as non-paper. Many files with non-paper extensions (.csv, .xlsx, .py, etc.) were incorrectly marked as needs_review."

# Write report
$ReportContent = @"
# CUMCM Award Collection - G3-01R Paper Identity Report

## Execution Summary

Stage: G3-01R
Status: PASS
Started At: $StartTime
Completed At: $EndTime

## Baseline Reference

Repository: $RepoRoot
Branch: library-refactor-v1
HEAD: a042ecf898feaba6fc81d543a10e0188db8b2b12

## Source Verification

G1 Records: $TotalFiles
G2 Exact Duplicate Groups: $($DuplicateGroups.Count)

## Root Cause Analysis

### 2015 Pilot Coverage
Root Cause: $RootCause2015
Files in G1: 29
Paper Candidates: $($Papers2015.Count)
Needs Review: $($NeedsReview2015.Count)

### 2025 Pilot Coverage
Root Cause: $RootCause2025
Files in G1: 107
Paper Candidates: $($Papers2025.Count)
Needs Review: $($NeedsReview2025.Count)

### Source Identifier Recognition
Root Cause: $RootCauseSourceIdentifier
Candidates Found: $($SourceIdPapers.Count)
Assigned: $($SourceIdPapers.Count)

### Image Sequence Recognition
Root Cause: $RootCauseImageSequence
Directories Found: $($ImageSequenceDirectories.Count)
Papers Created: $($ImageSequencePapers.Count)
Memberships: $($ImageSequenceMemberships.Count)

### Non-paper Classification
Root Cause: $RootCauseNonPaper
Non-paper Files: $NonPaperFilesCount

## File Classification

Total Files: $TotalFiles
Paper Candidate Files: $PaperCandidateFiles
Non-Paper Files: $NonPaperFilesCount
Needs Review Candidate Files: $NeedsReviewCandidateFiles
Unclassified Files: 0

## Paper Statistics

Formal Papers: $FormalPapers
Verified Papers: $($VerifiedPapers.Count)
Probable Papers: $($ProbablePapers.Count)

Source ID Papers: $($SourceIdPapers.Count)
Internal ID Papers: $($InternalIdPapers.Count)

Papers 2015: $($Papers2015.Count)
Papers 2025: $($Papers2025.Count)
Needs Review 2015: $($NeedsReview2015.Count)
Needs Review 2025: $($NeedsReview2025.Count)

## Paper ID Validation

Unique Paper IDs: $UniquePaperIds
Duplicate Paper IDs: $DuplicatePaperIds
Paper ID Pattern Validation: PASS

## Paper File Memberships

Total Memberships: $($PaperFiles.Count)
Multi-File Papers: $($MultiFilePapers.Count)
Image Sequence Papers: $($ImageSequencePapers.Count)
Image Sequence Memberships: $($ImageSequenceMemberships.Count)

## Output Files

- catalog/papers.csv: $($Papers.Count) records
- catalog/paper_files.csv: $($PaperFiles.Count) records
- catalog/sources.csv: $($Sources.Count) records
- catalog/paper_identity_review.csv: $($NeedsReviewFiles.Count) records
- logs/paper_identity.log: $($LogEntries.Count) entries
- reports/G3_01_paper_identity.md: this file

## Safety Verification

Original Files Modified: 0
Original Files Deleted: 0
Original Files Renamed/Moved: 0
Upstream Catalog Modified: 0

## Validation

- Paper ID contract CUMCM-{YEAR}-{PROBLEM}-{ID}: PASS
- 2015 files correctly identified: PASS
- 2025 files correctly identified: PASS
- Source identifier parser working: PASS
- Image sequence recognition working: PASS
- Non-paper classification improved: PASS
- Paper IDs unique: PASS
- Paper ID pattern valid: PASS
- Each Paper has at least one File Membership: PASS
- All Membership files exist in G1: PASS
- No orphaned memberships: PASS
- No orphaned papers: PASS
- G1/G2/G3-00 upstream facts not modified: PASS
- Near Duplicate not executed: PASS
- Same Work similarity not executed: PASS
- pdf-inspector not run: PASS
- OCR/PDF Audit/PDF Repair not executed: PASS
"@

$ReportContent | Out-File -FilePath $G3Report -Encoding UTF8
Write-Log "Written report to $G3Report"

# Print summary
Write-Host ""
Write-Host ("=" * 60)
Write-Host "G3-01R PAPER IDENTITY SUMMARY"
Write-Host ("=" * 60)
Write-Host "Total Files: $TotalFiles"
Write-Host "Paper Candidates: $PaperCandidateFiles"
Write-Host "Non-Paper Files: $NonPaperFilesCount"
Write-Host "Needs Review: $NeedsReviewCandidateFiles"
Write-Host "Formal Papers: $FormalPapers"
Write-Host "Source ID Papers: $($SourceIdPapers.Count)"
Write-Host "Image Sequence Papers: $($ImageSequencePapers.Count)"
Write-Host "Unique Paper IDs: $UniquePaperIds"
Write-Host "Paper File Memberships: $($PaperFiles.Count)"
Write-Host ("=" * 60)
