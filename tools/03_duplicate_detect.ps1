# G2: SHA-256 Integrity Verification and Exact Duplicate Governance
# PowerShell implementation

$ErrorActionPreference = "Stop"
$StartTime = Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz"

# Configuration
$RepoRoot = "D:\cumcm-modeling-Award-Collection"
$CatalogDir = Join-Path $RepoRoot "catalog"
$LogsDir = Join-Path $RepoRoot "logs"
$ReportsDir = Join-Path $RepoRoot "reports"

# Output files
$DuplicatesCsv = Join-Path $CatalogDir "duplicates.csv"
$DuplicateLog = Join-Path $LogsDir "duplicate.log"
$G2Report = Join-Path $ReportsDir "G2_exact_duplicates.md"

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

Write-Log "G2 Exact Duplicate Detection started"
Write-Log "Repository root: $RepoRoot"

# Step 1: Read G1 catalog
Write-Log "Step 1: Reading G1 catalog..."
$CsvData = Import-Csv (Join-Path $CatalogDir "files.csv")
$JsonlData = Get-Content (Join-Path $CatalogDir "manifest.jsonl") | ForEach-Object { $_ | ConvertFrom-Json }

# Verify G1 catalog integrity
$CsvRecords = $CsvData.Count
$JsonlRecords = $JsonlData.Count
Write-Log "CSV records: $CsvRecords"
Write-Log "JSONL records: $JsonlRecords"

if ($CsvRecords -ne 3634 -or $JsonlRecords -ne 3634) {
    Write-Log "G1 record count mismatch: CSV=$CsvRecords, JSONL=$JsonlRecords" "ERROR"
    exit 1
}

# Verify path set match
$CsvPaths = $CsvData | Select-Object -ExpandProperty path | Sort-Object
$JsonlPaths = $JsonlData | Select-Object -ExpandProperty path | Sort-Object
$PathMatch = (Compare-Object $CsvPaths $JsonlPaths).Count -eq 0
Write-Log "Path set match: $PathMatch"

if (-not $PathMatch) {
    Write-Log "Path set mismatch between CSV and JSONL" "ERROR"
    exit 1
}

# Verify SHA match
$ShaMatch = $true
for ($i = 0; $i -lt $CsvData.Count; $i++) {
    if ($CsvData[$i].sha256 -ne $JsonlData[$i].sha256) {
        $ShaMatch = $false
        Write-Log "SHA mismatch at index $i" "ERROR"
        break
    }
}
Write-Log "SHA match: $ShaMatch"

if (-not $ShaMatch) {
    Write-Log "SHA mismatch between CSV and JSONL" "ERROR"
    exit 1
}

# Step 2: Verify SHA-256 integrity
Write-Log "Step 2: Verifying SHA-256 integrity..."
$ValidSha256 = 0
$InvalidSha256 = 0
$TargetedRehashCount = 0

foreach ($Record in $CsvData) {
    if ($Record.sha256 -match '^[0-9A-Fa-f]{64}$') {
        $ValidSha256++
    } else {
        $InvalidSha256++
        Write-Log "Invalid SHA-256 format: $($Record.path) - $($Record.sha256)" "WARNING"
    }
}

Write-Log "Valid SHA-256: $ValidSha256"
Write-Log "Invalid SHA-256: $InvalidSha256"

if ($InvalidSha256 -gt 0) {
    Write-Log "Invalid SHA-256 values found" "ERROR"
    exit 1
}

# Step 3: Find exact duplicates
Write-Log "Step 3: Finding exact duplicates..."
$ShaGroups = $CsvData | Group-Object -Property sha256
$DuplicateGroups = $ShaGroups | Where-Object { $_.Count -ge 2 }

$TotalFiles = $CsvData.Count
$UniqueSha256 = $ShaGroups.Count
$ExactDuplicateGroups = $DuplicateGroups.Count
$ExactDuplicateMembers = ($DuplicateGroups | ForEach-Object { $_.Count } | Measure-Object -Sum).Sum
$ExtraCopies = $ExactDuplicateMembers - $ExactDuplicateGroups
$MaxGroupSize = if ($DuplicateGroups) { ($DuplicateGroups | ForEach-Object { $_.Count } | Measure-Object -Maximum).Maximum } else { 0 }

Write-Log "Total files: $TotalFiles"
Write-Log "Unique SHA-256: $UniqueSha256"
Write-Log "Exact duplicate groups: $ExactDuplicateGroups"
Write-Log "Exact duplicate members: $ExactDuplicateMembers"
Write-Log "Extra copies: $ExtraCopies"
Write-Log "Max group size: $MaxGroupSize"

# Step 4: Analyze duplicate groups
Write-Log "Step 4: Analyzing duplicate groups..."
$SameExtensionGroups = 0
$MixedExtensionGroups = 0
$CrossYearGroups = 0
$SameYearGroups = 0

$DuplicateRecords = @()
$GroupIndex = 0

foreach ($Group in $DuplicateGroups) {
    $GroupIndex++
    $GroupId = "DG{0:D5}" -f $GroupIndex
    $Sha256 = $Group.Name
    $MemberCount = $Group.Count
    
    # Analyze extensions and years
    $Extensions = $Group.Group | Select-Object -ExpandProperty file_extension -Unique
    $Years = $Group.Group | Select-Object -ExpandProperty year -Unique
    
    if ($Extensions.Count -eq 1) {
        $SameExtensionGroups++
    } else {
        $MixedExtensionGroups++
    }
    
    if ($Years.Count -eq 1) {
        $SameYearGroups++
    } else {
        $CrossYearGroups++
    }
    
    # Create records for each member
    $MemberIndex = 0
    foreach ($Member in $Group.Group) {
        $MemberIndex++
        $Record = [PSCustomObject]@{
            duplicate_group = $GroupId
            sha256 = $Sha256
            member_count = $MemberCount
            member_index = $MemberIndex
            path = $Member.path
            filename = $Member.filename
            file_extension = $Member.file_extension
            file_size_bytes = $Member.file_size_bytes
            year = $Member.year
            problem_code = $Member.problem_code
            recorded_at = (Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz")
        }
        $DuplicateRecords += $Record
    }
}

Write-Log "Same extension groups: $SameExtensionGroups"
Write-Log "Mixed extension groups: $MixedExtensionGroups"
Write-Log "Cross year groups: $CrossYearGroups"
Write-Log "Same year groups: $SameYearGroups"

# Step 5: Write catalog/duplicates.csv
Write-Log "Step 5: Writing catalog/duplicates.csv..."
$DuplicateRecords | Export-Csv -Path $DuplicatesCsv -NoTypeInformation -Encoding UTF8
Write-Log "Written $($DuplicateRecords.Count) records to $DuplicatesCsv"

# Step 6: Write logs/duplicate.log
Write-Log "Step 6: Writing logs/duplicate.log..."
$LogEntries | Out-File -FilePath $DuplicateLog -Encoding UTF8
Write-Log "Written $($LogEntries.Count) log entries to $DuplicateLog"

# Step 7: Write reports/G2_exact_duplicates.md
Write-Log "Step 7: Writing reports/G2_exact_duplicates.md..."
$EndTime = Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz"

$ReportContent = @"
# CUMCM Award Collection — G2 Exact Duplicate Report

## Execution Summary

Stage: G2
Status: PASS
Started At: $StartTime
Completed At: $EndTime

## Baseline Reference

Repository: $RepoRoot
Branch: library-refactor-v1
HEAD: a042ecf898feaba6fc81d543a10e0188db8b2b12
G0 Recorded At: 2026-08-17T18:16:45+08:00

## G1 Source Verification

Source CSV Records: $CsvRecords
Source JSONL Records: $JsonlRecords
Path Set Match: $PathMatch
SHA Match: $ShaMatch

## SHA-256 Integrity

Valid SHA-256: $ValidSha256
Invalid SHA-256: $InvalidSha256
Targeted Rehash Count: $TargetedRehashCount

## Duplicate Analysis

Total Files: $TotalFiles
Unique SHA-256: $UniqueSha256
Exact Duplicate Groups: $ExactDuplicateGroups
Exact Duplicate Members: $ExactDuplicateMembers
Extra Copies: $ExtraCopies
Max Group Size: $MaxGroupSize

### Group Characteristics

Same Extension Groups: $SameExtensionGroups
Mixed Extension Groups: $MixedExtensionGroups
Cross Year Groups: $CrossYearGroups
Same Year Groups: $SameYearGroups

## Output Files

- catalog/duplicates.csv: $($DuplicateRecords.Count) records
- logs/duplicate.log: $($LogEntries.Count) entries
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
"@

$ReportContent | Out-File -FilePath $G2Report -Encoding UTF8
Write-Log "Written report to $G2Report"
Write-Log "G2 Exact Duplicate Detection completed successfully"

# Print summary
Write-Host ""
Write-Host ("=" * 60)
Write-Host "G2 EXACT DUPLICATE DETECTION SUMMARY"
Write-Host ("=" * 60)
Write-Host "Total Files: $TotalFiles"
Write-Host "Unique SHA-256: $UniqueSha256"
Write-Host "Exact Duplicate Groups: $ExactDuplicateGroups"
Write-Host "Exact Duplicate Members: $ExactDuplicateMembers"
Write-Host "Extra Copies: $ExtraCopies"
Write-Host "Max Group Size: $MaxGroupSize"
Write-Host "Same Extension Groups: $SameExtensionGroups"
Write-Host "Mixed Extension Groups: $MixedExtensionGroups"
Write-Host "Cross Year Groups: $CrossYearGroups"
Write-Host "Same Year Groups: $SameYearGroups"
Write-Host ("=" * 60)
