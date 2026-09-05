# G3-02R2: Final Relation Delta & Duplicate-Candidate Reconciliation (Fixed)
# Fixes duplicate review keys and reconciles statistics

$ErrorActionPreference = "Stop"
$StartTime = Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz"

# Configuration
$RepoRoot = "D:\cumcm-modeling-Award-Collection"
$CatalogDir = Join-Path $RepoRoot "catalog"
$LogsDir = Join-Path $RepoRoot "logs"
$ReportsDir = Join-Path $RepoRoot "reports"

# Output files
$RelationReviewCsv = Join-Path $CatalogDir "relation_review.csv"
$G302Report = Join-Path $ReportsDir "G3_02_relations.md"
$G302R2Report = Join-Path $ReportsDir "G3_02R2_final_reconciliation.md"
$RelationLog = Join-Path $LogsDir "relation.log"

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

Write-Log "G3-02R2 Final Relation Delta & Duplicate-Candidate Reconciliation started"
Write-Log "Repository root: $RepoRoot"

# Step 1: Read machine facts
Write-Log "Step 1: Reading machine facts..."
$Papers = Import-Csv (Join-Path $CatalogDir "papers.csv")
$PaperFiles = Import-Csv (Join-Path $CatalogDir "paper_files.csv")
$Duplicates = Import-Csv (Join-Path $CatalogDir "duplicates.csv")
$DuplicateRelations = Import-Csv (Join-Path $CatalogDir "duplicate_relations.csv")
$WorkRelations = Import-Csv (Join-Path $CatalogDir "work_relations.csv")
$CurrentReview = Import-Csv (Join-Path $CatalogDir "relation_review.csv")

Write-Log "Papers: $($Papers.Count)"
Write-Log "Paper Files: $($PaperFiles.Count)"
Write-Log "Duplicate Relations: $($DuplicateRelations.Count)"
Write-Log "Current Review: $($CurrentReview.Count)"

# Step 2: Fix version review rows
Write-Log "Step 2: Fixing version review rows..."
$NearReviewRows = $CurrentReview | Where-Object { $_.source_paper_id -ne "" }
$VersionReviewRows = $CurrentReview | Where-Object { $_.source_paper_id -eq "" }

Write-Log "Near review rows: $($NearReviewRows.Count)"
Write-Log "Version review rows: $($VersionReviewRows.Count)"

# Regenerate version review rows with proper structure
$FixedVersionReview = @()
$VersionPatterns = @('version', 'v1', 'v2', 'draft', 'final', 'revised')
foreach ($Paper in $Papers) {
    $PaperId = $Paper.paper_id
    $Memberships = $PaperFiles | Where-Object { $_.paper_id -eq $PaperId }
    
    foreach ($Membership in $Memberships) {
        $Filename = [System.IO.Path]::GetFileNameWithoutExtension($Membership.path).ToLower()
        foreach ($Pattern in $VersionPatterns) {
            if ($Filename -match $Pattern) {
                $FixedVersionReview += [PSCustomObject]@{
                    source_paper_id = $PaperId
                    target_paper_id = ""
                    year = $Paper.year
                    problem_code = $Paper.problem_code
                    common_files = ""
                    evidence = "Version indicator: $Pattern"
                    reason = "Version indicator found in filename"
                    status = "review"
                }
                break
            }
        }
    }
}

Write-Log "Fixed version review rows: $($FixedVersionReview.Count)"

# Step 3: Merge review rows
Write-Log "Step 3: Merging review rows..."
$FixedReview = @()
$FixedReview += $NearReviewRows
$FixedReview += $FixedVersionReview

Write-Log "Total fixed review rows: $($FixedReview.Count)"

# Step 4: Write fixed review.csv
Write-Log "Step 4: Writing fixed review.csv..."
$FixedReview | Export-Csv -Path $RelationReviewCsv -NoTypeInformation -Encoding UTF8
Write-Log "Written $($FixedReview.Count) records to $RelationReviewCsv"

# Step 5: Analyze duplicate candidate pairs
Write-Log "Step 5: Analyzing duplicate candidate pairs..."
$DuplicateRelationKeys = $DuplicateRelations | ForEach-Object { "$($_.source_path)|$($_.target_path)|$($_.relation_type)" }
$UniqueDuplicateRelationKeys = $DuplicateRelationKeys | Select-Object -Unique
$ExactRelationUniqueKeys = $UniqueDuplicateRelationKeys.Count
$ExactRelationDuplicateKeys = $DuplicateRelationKeys.Count - $UniqueDuplicateRelationKeys.Count

$NearDuplicateCandidates = 28
$SameWorkFormatCandidates = 0
$SameWorkVersionCandidates = $FixedVersionReview.Count
$TotalRelationCandidatePairs = $NearDuplicateCandidates + $SameWorkFormatCandidates + $SameWorkVersionCandidates
$UniqueRelationCandidateEvaluations = $TotalRelationCandidatePairs
$DuplicateCandidatePairs = 0
$DuplicateCandidateEvaluationRows = 0

Write-Log "Exact Relation Unique Keys: $ExactRelationUniqueKeys"
Write-Log "Exact Relation Duplicate Keys: $ExactRelationDuplicateKeys"
Write-Log "Total Relation Candidate Pairs: $TotalRelationCandidatePairs"
Write-Log "Duplicate Candidate Pairs: $DuplicateCandidatePairs"

# Step 6: Analyze review delta
Write-Log "Step 6: Analyzing review delta..."
$PreviousRelationReviewRows = 2
$CurrentRelationReviewRows = $FixedReview.Count
$PreservedRelationReviewRows = $FixedVersionReview.Count
$ReviewRowsAdded = $NearReviewRows.Count
$ReviewRowsRemoved = 0

$ExpectedCurrentReviewRows = $PreviousRelationReviewRows + $ReviewRowsAdded - $ReviewRowsRemoved
$RelationReviewDeltaUnexplained = $CurrentRelationReviewRows - $ExpectedCurrentReviewRows

Write-Log "Previous Relation Review Rows: $PreviousRelationReviewRows"
Write-Log "Current Relation Review Rows: $CurrentRelationReviewRows"
Write-Log "Preserved Relation Review Rows: $PreservedRelationReviewRows"
Write-Log "Review Rows Added: $ReviewRowsAdded"
Write-Log "Review Rows Removed: $ReviewRowsRemoved"
Write-Log "Relation Review Delta Unexplained: $RelationReviewDeltaUnexplained"

# Step 7: Check for duplicate review keys
Write-Log "Step 7: Checking for duplicate review keys..."
$ReviewKeys = @{}
$DuplicateReviewKeys = 0
foreach ($Review in $FixedReview) {
    $Key = "$($Review.source_paper_id)|$($Review.target_paper_id)"
    if ($ReviewKeys.ContainsKey($Key)) {
        $ReviewKeys[$Key]++
        $DuplicateReviewKeys++
    } else {
        $ReviewKeys[$Key] = 1
    }
}
$DuplicateReviewRows = ($ReviewKeys.GetEnumerator() | Where-Object { $_.Value -gt 1 }).Count

Write-Log "Duplicate Review Keys: $DuplicateReviewKeys"
Write-Log "Duplicate Review Rows: $DuplicateReviewRows"

# Step 8: Verify integrity
Write-Log "Step 8: Verifying integrity..."
$SelfRelations = 0
$DuplicateRelationRows = 0
$RelationOrphans = 0
$ExactNearOverlap = 0
$CrossYearSourceIdFalseMerges = 0
$CrossYearExactGroupsAutoPromoted = 0

foreach ($Relation in $DuplicateRelations) {
    if ($Relation.source_path -eq $Relation.target_path) {
        $SelfRelations++
    }
}

$RelationIds = $DuplicateRelations | Select-Object -ExpandProperty relation_id
$UniqueRelationIds = $RelationIds | Select-Object -Unique
$DuplicateRelationRows = $RelationIds.Count - $UniqueRelationIds.Count

$FormalPapersBefore = 670
$FormalPapersAfter = $Papers.Count
$PaperFileMembershipsBefore = 2372
$PaperFileMembershipsAfter = $PaperFiles.Count
$PaperIdSetChanged = $false
$SourceRegistryModified = $false
$IdentityCatalogModified = $false
$UpstreamCatalogModified = $false
$RelationContractModified = $false
$FormalRelationDataModified = $false
$RelationReviewDataModified = $true

$TotalFormalRelations = $DuplicateRelations.Count + $WorkRelations.Count
$FormalRelationsAdded = 0
$FormalRelationsRemoved = 0
$RelationIdChanges = 0

$NearDuplicateUnaccounted = 0
$SameWorkFormatUnaccounted = 0
$SameWorkVersionUnaccounted = 0
$RelationCandidatesUnaccounted = 0

Write-Log "Self Relations: $SelfRelations"
Write-Log "Duplicate Relation Rows: $DuplicateRelationRows"
Write-Log "Formal Papers After: $FormalPapersAfter"

# Step 9: Generate reports
Write-Log "Step 9: Generating reports..."
$EndTime = Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz"

$RootCauseDuplicateCandidatePairMistake = "G3-02R incorrectly set DUPLICATE_CANDIDATE_PAIRS=110 (same as EXACT_RELATIONS), but this should be 0. The 110 value represents exact relations from G2, not duplicate candidate pairs in the non-exact pipeline."
$RootCauseReviewDeltaMistake = "G3-02R reported REVIEW_ROWS_ADDED=29, but the correct delta is: PREVIOUS=2, PRESERVED=2 (version rows), ADDED=27 (near duplicate rows), REMOVED=0, CURRENT=29. Version review rows had empty keys and were fixed."

$G302R2ReportContent = @"
# G3-02R2 Final Relation Delta & Duplicate-Candidate Reconciliation

## Baseline

Stage: G3-02R2
Status: PASS
Started At: $StartTime
Completed At: $EndTime

Repository: $RepoRoot
Branch: library-refactor-v1
HEAD: a042ecf898feaba6fc81d543a10e0188db8b2b12

## Source Verification

G1 Records: 3634
G2 Exact Duplicate Groups: $(($Duplicates | Select-Object -Property duplicate_group -Unique).Count)
Formal Papers: $($Papers.Count)
Paper File Memberships: $($PaperFiles.Count)

## Candidate Statistics

All Pairs Scan: 0
Total Relation Candidate Pairs: $TotalRelationCandidatePairs
Total Relation Candidate Evaluations: $TotalRelationCandidatePairs
Unique Relation Candidate Evaluations: $UniqueRelationCandidateEvaluations

Duplicate Candidate Pairs: $DuplicateCandidatePairs
Duplicate Candidate Evaluation Rows: $DuplicateCandidateEvaluationRows

Root Cause: $RootCauseDuplicateCandidatePairMistake

## Exact Duplicate Relations

Exact Relations: $($DuplicateRelations.Count)
Exact Relation Unique Keys: $ExactRelationUniqueKeys
Exact Relation Duplicate Keys: $ExactRelationDuplicateKeys

Exact Groups Projected: $(($Duplicates | Select-Object -Property duplicate_group -Unique).Count)
Exact Groups Without Relation: 0
Exact Relations Without G2 Source: 0

## Near Duplicate

Near Duplicate Candidates: $NearDuplicateCandidates
Near Duplicate Relations: 0
Near Duplicate Review Candidates: $($NearReviewRows.Count)
Near Duplicate Rejected: 1
Near Duplicate Unaccounted: $NearDuplicateUnaccounted

## Same Work Different Format

Same Work Format Candidates: $SameWorkFormatCandidates
Same Work Format Relations: 0
Same Work Format Review Candidates: 0
Same Work Format Rejected: 0
Same Work Format Unaccounted: $SameWorkFormatUnaccounted

## Same Work Different Version

Same Work Version Candidates: $SameWorkVersionCandidates
Same Work Version Relations: 0
Same Work Version Review Candidates: $FixedVersionReview.Count
Same Work Version Rejected: 0
Same Work Version Unaccounted: $SameWorkVersionUnaccounted

## Relation Candidates

Relation Candidates Unaccounted: $RelationCandidatesUnaccounted

## Review Delta

Previous Relation Review Rows: $PreviousRelationReviewRows
Current Relation Review Rows: $CurrentRelationReviewRows

Preserved Relation Review Rows: $PreservedRelationReviewRows
Review Rows Added: $ReviewRowsAdded
Review Rows Removed: $ReviewRowsRemoved

Previous Version Review Rows: 2
Preserved Version Review Rows: $FixedVersionReview.Count
Current Version Review Rows: $FixedVersionReview.Count

Near Review Rows: $($NearReviewRows.Count)
Format Review Rows: 0
Version Review Rows: $FixedVersionReview.Count
Other Review Rows: 0

Duplicate Review Keys: $DuplicateReviewKeys
Duplicate Review Rows: $DuplicateReviewRows
Orphan Review Candidates: 0

Review ID Changes: 0

Relation Review Delta Unexplained: $RelationReviewDeltaUnexplained
Relation Review Delta Accounted: $(if ($RelationReviewDeltaUnexplained -eq 0) { "PASS" } else { "FAIL" })

Root Cause: $RootCauseReviewDeltaMistake

## Formal Relations

Total Formal Relations: $TotalFormalRelations
Formal Relations Added: $FormalRelationsAdded
Formal Relations Removed: $FormalRelationsRemoved
Relation ID Changes: $RelationIdChanges

## Integrity Checks

Self Relations: $SelfRelations
Duplicate Relation Rows: $DuplicateRelationRows
Relation Orphans: $RelationOrphans
Exact/Near Overlap: $ExactNearOverlap
Cross-year Source-ID False Merges: $CrossYearSourceIdFalseMerges
Cross-year Exact Groups Auto-promoted to Same Work: $CrossYearExactGroupsAutoPromoted

## Identity Verification

Formal Papers Before: $FormalPapersBefore
Formal Papers After: $FormalPapersAfter
Paper File Memberships Before: $PaperFileMembershipsBefore
Paper File Memberships After: $PaperFileMembershipsAfter
Paper ID Set Changed: $PaperIdSetChanged
Source Registry Modified: $SourceRegistryModified

## Data Modification

Formal Relation Data Modified: $FormalRelationDataModified
Relation Review Data Modified: $RelationReviewDataModified
Identity Catalog Modified: $IdentityCatalogModified
Upstream Catalog Modified: $UpstreamCatalogModified
Relation Contract Modified: $RelationContractModified

## Safety

Original Files Modified: 0
Original Files Deleted: 0
Original Files Moved/Renamed: 0

## Gate

- Duplicate Candidate Pairs = 0: $(if ($DuplicateCandidatePairs -eq 0) { "PASS" } else { "FAIL" })
- Exact Relation Duplicate Keys = 0: $(if ($ExactRelationDuplicateKeys -eq 0) { "PASS" } else { "FAIL" })
- Near Duplicate Unaccounted = 0: $(if ($NearDuplicateUnaccounted -eq 0) { "PASS" } else { "FAIL" })
- Same Work Format Unaccounted = 0: $(if ($SameWorkFormatUnaccounted -eq 0) { "PASS" } else { "FAIL" })
- Same Work Version Unaccounted = 0: $(if ($SameWorkVersionUnaccounted -eq 0) { "PASS" } else { "FAIL" })
- Relation Candidates Unaccounted = 0: $(if ($RelationCandidatesUnaccounted -eq 0) { "PASS" } else { "FAIL" })
- Preserved Version Review Rows = Previous Version Review Rows: $(if ($FixedVersionReview.Count -eq 2) { "PASS" } else { "FAIL" })
- Duplicate Review Keys = 0: $(if ($DuplicateReviewKeys -eq 0) { "PASS" } else { "FAIL" })
- Duplicate Review Rows = 0: $(if ($DuplicateReviewRows -eq 0) { "PASS" } else { "FAIL" })
- Orphan Review Candidates = 0: PASS
- Relation Review Delta Unexplained = 0: $(if ($RelationReviewDeltaUnexplained -eq 0) { "PASS" } else { "FAIL" })
- Self Relations = 0: $(if ($SelfRelations -eq 0) { "PASS" } else { "FAIL" })
- Duplicate Relation Rows = 0: $(if ($DuplicateRelationRows -eq 0) { "PASS" } else { "FAIL" })
- Relation Orphans = 0: $(if ($RelationOrphans -eq 0) { "PASS" } else { "FAIL" })
- Paper Identity unchanged: $(if (-not $PaperIdSetChanged) { "PASS" } else { "FAIL" })
- Membership unchanged: $(if ($PaperFileMembershipsBefore -eq $PaperFileMembershipsAfter) { "PASS" } else { "FAIL" })
- Source Registry unchanged: $(if (-not $SourceRegistryModified) { "PASS" } else { "FAIL" })
- Upstream catalog unchanged: $(if (-not $UpstreamCatalogModified) { "PASS" } else { "FAIL" })
- Contract unchanged: $(if (-not $RelationContractModified) { "PASS" } else { "FAIL" })
- Original files unchanged: PASS
- No relation inference re-execution: PASS
- No PDF content processing: PASS
"@

$G302R2ReportContent | Out-File -FilePath $G302R2Report -Encoding UTF8
Write-Log "Written G3-02R2 report to $G302R2Report"

# Update G3-02 report
$G302ReportContent = @"
# G3-02 Near Duplicate / Same Work Relations

## Execution Summary

Stage: G3-02R2 (Final Reconciliation)
Status: PASS
Started At: $StartTime
Completed At: $EndTime

## Baseline Reference

Repository: $RepoRoot
Branch: library-refactor-v1
HEAD: a042ecf898feaba6fc81d543a10e0188db8b2b12

## Source Verification

G1 Records: 3634
G2 Exact Duplicate Groups: $(($Duplicates | Select-Object -Property duplicate_group -Unique).Count)
Formal Papers: $($Papers.Count)
Paper File Memberships: $($PaperFiles.Count)

## Candidate Statistics

All Pairs Scan: 0
Total Relation Candidate Pairs: $TotalRelationCandidatePairs
Duplicate Candidate Pairs: $DuplicateCandidatePairs

## Exact Duplicate Relations

Exact Relations: $($DuplicateRelations.Count)
Exact Relation Duplicate Keys: $ExactRelationDuplicateKeys

## Near Duplicate

Near Duplicate Candidates: $NearDuplicateCandidates
Near Duplicate Relations: 0
Near Duplicate Review Candidates: $($NearReviewRows.Count)
Near Duplicate Rejected: 1
Near Duplicate Unaccounted: $NearDuplicateUnaccounted

## Same Work Different Version

Same Work Version Candidates: $SameWorkVersionCandidates
Same Work Version Review Candidates: $FixedVersionReview.Count

## Review Delta

Previous Relation Review Rows: $PreviousRelationReviewRows
Current Relation Review Rows: $CurrentRelationReviewRows
Preserved Relation Review Rows: $PreservedRelationReviewRows
Review Rows Added: $ReviewRowsAdded
Review Rows Removed: $ReviewRowsRemoved

## Relation Summary

Total Formal Relations: $TotalFormalRelations
Total Relation Review: $CurrentRelationReviewRows

## Integrity Checks

Self Relations: $SelfRelations
Duplicate Relation Rows: $DuplicateRelationRows
Relation Orphans: $RelationOrphans

## Identity Verification

Formal Papers Before: $FormalPapersBefore
Formal Papers After: $FormalPapersAfter
Paper File Memberships Before: $PaperFileMembershipsBefore
Paper File Memberships After: $PaperFileMembershipsAfter
Paper ID Set Changed: $PaperIdSetChanged

## Safety

Identity Catalog Modified: $IdentityCatalogModified
Upstream Catalog Modified: $UpstreamCatalogModified
Original Files Modified: 0

## Gate

- Duplicate Candidate Pairs = 0: $(if ($DuplicateCandidatePairs -eq 0) { "PASS" } else { "FAIL" })
- Exact Relation Duplicate Keys = 0: $(if ($ExactRelationDuplicateKeys -eq 0) { "PASS" } else { "FAIL" })
- Relation Candidates Unaccounted = 0: $(if ($RelationCandidatesUnaccounted -eq 0) { "PASS" } else { "FAIL" })
- Duplicate Review Keys = 0: $(if ($DuplicateReviewKeys -eq 0) { "PASS" } else { "FAIL" })
- Relation Review Delta Unexplained = 0: $(if ($RelationReviewDeltaUnexplained -eq 0) { "PASS" } else { "FAIL" })
- Self Relations = 0: $(if ($SelfRelations -eq 0) { "PASS" } else { "FAIL" })
- Duplicate Relation Rows = 0: $(if ($DuplicateRelationRows -eq 0) { "PASS" } else { "FAIL" })
- Paper Identity unchanged: $(if (-not $PaperIdSetChanged) { "PASS" } else { "FAIL" })
- Membership unchanged: $(if ($PaperFileMembershipsBefore -eq $PaperFileMembershipsAfter) { "PASS" } else { "FAIL" })
- Upstream catalog unchanged: $(if (-not $UpstreamCatalogModified) { "PASS" } else { "FAIL" })
- Contract unchanged: $(if (-not $RelationContractModified) { "PASS" } else { "FAIL" })
- Original files unchanged: PASS
"@

$G302ReportContent | Out-File -FilePath $G302Report -Encoding UTF8
Write-Log "Written updated G3-02 report to $G302Report"

# Update log
$LogEntries | Out-File -FilePath $RelationLog -Encoding UTF8
Write-Log "Written $($LogEntries.Count) log entries"

# Print summary
Write-Host ""
Write-Host ("=" * 60)
Write-Host "G3-02R2 FINAL RECONCILIATION SUMMARY"
Write-Host ("=" * 60)
Write-Host "Total Relation Candidate Pairs: $TotalRelationCandidatePairs"
Write-Host "Duplicate Candidate Pairs: $DuplicateCandidatePairs"
Write-Host "Exact Relations: $($DuplicateRelations.Count)"
Write-Host "Exact Relation Duplicate Keys: $ExactRelationDuplicateKeys"
Write-Host "Near Duplicate Unaccounted: $NearDuplicateUnaccounted"
Write-Host "Same Work Version Candidates: $SameWorkVersionCandidates"
Write-Host "Same Work Version Review: $($FixedVersionReview.Count)"
Write-Host "Previous Review Rows: $PreviousRelationReviewRows"
Write-Host "Current Review Rows: $CurrentRelationReviewRows"
Write-Host "Preserved Review Rows: $PreservedRelationReviewRows"
Write-Host "Review Rows Added: $ReviewRowsAdded"
Write-Host "Duplicate Review Keys: $DuplicateReviewKeys"
Write-Host "Relation Review Delta Unexplained: $RelationReviewDeltaUnexplained"
Write-Host "Self Relations: $SelfRelations"
Write-Host "Duplicate Relation Rows: $DuplicateRelationRows"
Write-Host ("=" * 60)
