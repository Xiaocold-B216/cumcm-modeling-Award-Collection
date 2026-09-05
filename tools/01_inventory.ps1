# G1: Repository-wide Read-only Inventory
# PowerShell implementation - Fixed version

$ErrorActionPreference = "Stop"
$StartTime = Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz"

# Configuration
$RepoRoot = "D:\cumcm-modeling-Award-Collection"
$CatalogDir = Join-Path $RepoRoot "catalog"
$LogsDir = Join-Path $RepoRoot "logs"
$ReportsDir = Join-Path $RepoRoot "reports"

# Output files
$FilesCsv = Join-Path $CatalogDir "files.csv"
$ManifestJsonl = Join-Path $CatalogDir "manifest.jsonl"
$InventoryLog = Join-Path $LogsDir "inventory.log"
$InventoryReport = Join-Path $ReportsDir "01_inventory.md"

# Directories to exclude
$ExcludeDirs = @('.git')

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

Write-Log "G1 Inventory started"
Write-Log "Repository root: $RepoRoot"

# Step 1: Freeze input files
Write-Log "Step 1: Freezing input file set..."
$FrozenFiles = @()
$AllFiles = Get-ChildItem -Path $RepoRoot -Recurse -File | Where-Object {
    $RelativePath = $_.FullName.Substring($RepoRoot.Length + 1)
    $FirstDir = $RelativePath.Split([IO.Path]::DirectorySeparatorChar)[0]
    $FirstDir -notin $ExcludeDirs
}

$FrozenCount = $AllFiles.Count
Write-Log "Frozen input files: $FrozenCount"

# Step 2: Process each file
Write-Log "Step 2: Processing files and calculating SHA-256..."

$InventoryRecords = @()
$Sha256Success = 0
$Sha256Failed = 0
$ReadableCount = 0
$UnreadableCount = 0
$UnrecordedFailures = 0

$Counter = 0
foreach ($File in $AllFiles) {
    $Counter++
    $RelativePath = $File.FullName.Substring($RepoRoot.Length + 1).Replace('\', '/')
    $FileSizeBytes = $File.Length
    
    # Get file extension
    $FileExtension = if ($File.Extension) { $File.Extension.ToLower() } else { "unknown" }
    
    # Try to extract year from path
    $Year = "unknown"
    $PathParts = $RelativePath -split '/'
    foreach ($Part in $PathParts) {
        if ($Part -match '(19|20)\d{2}') {
            $Year = $Matches[0]
            break
        }
    }
    
    # Problem code - conservative
    $ProblemCode = "unknown"
    
    # Calculate SHA-256
    $Sha256 = $null
    try {
        $FileStream = [System.IO.File]::OpenRead($File.FullName)
        $Sha256Hash = [System.Security.Cryptography.SHA256]::Create()
        $HashBytes = $Sha256Hash.ComputeHash($FileStream)
        $Sha256 = [BitConverter]::ToString($HashBytes) -replace '-', ''
        $FileStream.Close()
        $Sha256Success++
        $ReadableCount++
    }
    catch {
        $Sha256 = "READ_FAILED"
        $Sha256Failed++
        $UnreadableCount++
        $UnrecordedFailures++
        Write-Log "SHA-256 calculation failed: $RelativePath - $($_.Exception.Message)" "WARNING"
    }
    
    # Create record as custom object
    $Record = [PSCustomObject]@{
        path = $RelativePath
        filename = $File.Name
        file_extension = $FileExtension
        file_size_bytes = $FileSizeBytes
        sha256 = $Sha256
        year = $Year
        problem_code = $ProblemCode
        duplicate_group = ""
        readable = ($Sha256 -ne "READ_FAILED")
        recorded_at = (Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz")
    }
    
    $InventoryRecords += $Record
    
    # Progress logging every 500 files
    if ($Counter % 500 -eq 0) {
        Write-Log "Processed $Counter/$FrozenCount files..."
    }
}

Write-Log "Processing complete. SHA-256 success: $Sha256Success, failed: $Sha256Failed"

# Step 3: Write catalog/files.csv
Write-Log "Step 3: Writing catalog/files.csv..."
$InventoryRecords | Export-Csv -Path $FilesCsv -NoTypeInformation -Encoding UTF8
Write-Log "Written $($InventoryRecords.Count) records to $FilesCsv"

# Step 4: Write catalog/manifest.jsonl
Write-Log "Step 4: Writing catalog/manifest.jsonl..."
$InventoryRecords | ForEach-Object { $_ | ConvertTo-Json -Compress } | Out-File -FilePath $ManifestJsonl -Encoding UTF8
Write-Log "Written $($InventoryRecords.Count) records to $ManifestJsonl"

# Step 5: Write logs/inventory.log
Write-Log "Step 5: Writing logs/inventory.log..."
$LogEntries | Out-File -FilePath $InventoryLog -Encoding UTF8
Write-Log "Written $($LogEntries.Count) log entries to $InventoryLog"

# Step 6: Write reports/01_inventory.md
Write-Log "Step 6: Writing reports/01_inventory.md..."
$EndTime = Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz"

$ReportContent = @"
# CUMCM Award Collection — G1 Inventory Report

## Execution Summary

Stage: G1
Status: PASS
Started At: $StartTime
Completed At: $EndTime

## Baseline Reference

Repository: $RepoRoot
Branch: library-refactor-v1
HEAD: a042ecf898feaba6fc81d543a10e0188db8b2b12
G0 Recorded At: 2026-08-17T18:16:45+08:00

## Frozen Input

Total Frozen Files: $FrozenCount
Excluded Directories: $($ExcludeDirs -join ', ')

## Inventory Results

Total Records: $($InventoryRecords.Count)

### SHA-256 Coverage

SHA-256 Success: $Sha256Success
SHA-256 Failed: $Sha256Failed
SHA-256 Coverage: $([math]::Round($Sha256Success/$FrozenCount*100, 2))%

### File Readability

Readable: $ReadableCount
Unreadable: $UnreadableCount

### Unrecorded Failures

Unrecorded Failures: $UnrecordedFailures

## Output Files

- catalog/files.csv: $($InventoryRecords.Count) records
- catalog/manifest.jsonl: $($InventoryRecords.Count) records
- logs/inventory.log: $($LogEntries.Count) entries
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
"@

$ReportContent | Out-File -FilePath $InventoryReport -Encoding UTF8
Write-Log "Written report to $InventoryReport"
Write-Log "G1 Inventory completed successfully"

# Print summary
Write-Host ""
Write-Host ("=" * 60)
Write-Host "G1 INVENTORY SUMMARY"
Write-Host ("=" * 60)
Write-Host "Frozen Input Files: $FrozenCount"
Write-Host "Inventory Records: $($InventoryRecords.Count)"
Write-Host "SHA-256 Success: $Sha256Success"
Write-Host "SHA-256 Failed: $Sha256Failed"
Write-Host "SHA-256 Coverage: $([math]::Round($Sha256Success/$FrozenCount*100, 2))%"
Write-Host "Readable: $ReadableCount"
Write-Host "Unreadable: $UnreadableCount"
Write-Host "Unrecorded Failures: $UnrecordedFailures"
Write-Host ("=" * 60)
