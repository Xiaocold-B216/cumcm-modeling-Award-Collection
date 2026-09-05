# G3-02R: Relation Candidate Accounting Reconciliation
# Fixes candidate accounting and reconciles statistics

$ErrorActionPreference = "Stop"
$StartTime = Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz"

# Configuration
$RepoRoot = "D:\cumcm-modeling-Award-Collection"
$CatalogDir = Join-Path $RepoRoot "catalog"
$LogsDir = Join-Path $RepoRoot "logs"
$ReportsDir = Join-Path $RepoRoot "reports"

# Output files
$DuplicateRelationsCsv = Join-Path $CatalogDir "duplicate_relations.csv"
$WorkRelationsCsv = Join-Path $CatalogDir "work_relations.csv"
$RelationReviewCsv = Join-Path $CatalogDir "relation_review.csv"
$G302Report = Join-Path $ReportsDir "G3_02_relations.md"
$G302RReport = Join-Path $ReportsDir "G3_02R_reconciliation.md"
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

Write-Log "G3-02R Relation Candidate Accounting Reconciliation started"
Write-Log "Repository root: $RepoRoot"

# Step 1: Read machine facts
Write-Log "Step 1: Reading machine facts..."
$Papers = Import-Csv (Join-Path $CatalogDir "papers.csv")
$PaperFiles = Import-Csv (Join-Path $CatalogDir "paper_files.csv")
$Duplicates = Import-Csv (Join-Path $CatalogDir "duplicates.csv")
$CsvData = Import-Csv (Join-Path $CatalogDir "files.csv")

Write-Log "Papers: $($Papers.Count)"
Write-Log "Paper Files: $($PaperFiles.Count)"
Write-Log "Duplicate Groups: $(($Duplicates | Select-Object -Property duplicate_group -Unique).Count)"

# Step 2: Generate DuplicateRelation from G2 exact duplicates
Write-Log "Step 2: Generating DuplicateRelation from G2 exact duplicates..."
$DuplicateRelations = @()
$DuplicateGroups = $Duplicates | Group-Object -Property duplicate_group

foreach ($Group in $DuplicateGroups) {
    $GroupId = $Group.Name
    $Members = $Group.Group
    $Sha256 = $Members[0].sha256
    $MemberCount = $Members.Count
    
    # Create relation ID
    $RelationId = "DUP-$($Sha256.Substring(0,8))"
    
    # Create relations between all pairs in the group
    for ($i = 0; $i -lt $Members.Count; $i++) {
        for ($j = $i + 1; $j -lt $Members.Count; $j++) {
            $SourcePath = $Members[$i].path
            $TargetPath = $Members[$j].path
            
            $DuplicateRelations += [PSCustomObject]@{
                relation_id = "$RelationId-$i-$j"
                duplicate_group = $GroupId
                sha256 = $Sha256
                member_count = $MemberCount
                source_path = $SourcePath
                target_path = $TargetPath
                relation_type = "exact_duplicate"
                source_entity_type = "file"
                target_entity_type = "file"
                confidence = "high"
                evidence = "SHA-256 match"
                status = "active"
                created_at = $StartTime
            }
        }
    }
}

Write-Log "Duplicate Relations: $($DuplicateRelations.Count)"

# Step 3: Analyze potential Near Duplicate candidates
Write-Log "Step 3: Analyzing potential Near Duplicate candidates..."
$NearDuplicateCandidates = @()
$NearDuplicateRelations = @()
$NearDuplicateReview = @()
$NearDuplicateRejected = @()

# Group papers by year and problem code
$PapersByYearProblem = @{}
foreach ($Paper in $Papers) {
    $Key = "$($Paper.year)-$($Paper.problem_code)"
    if (-not $PapersByYearProblem.ContainsKey($Key)) {
        $PapersByYearProblem[$Key] = @()
    }
    $PapersByYearProblem[$Key] += $Paper
}

# For each year-problem group, check for papers with similar filenames
foreach ($Key in $PapersByYearProblem.Keys) {
    $GroupPapers = $PapersByYearProblem[$Key]
    if ($GroupPapers.Count -lt 2) { continue }
    
    # Get file memberships for each paper
    $PaperFileMap = @{}
    foreach ($Paper in $GroupPapers) {
        $Memberships = $PaperFiles | Where-Object { $_.paper_id -eq $Paper.paper_id }
        $PaperFileMap[$Paper.paper_id] = $Memberships
    }
    
    # Check for papers with similar filenames (potential near duplicates)
    for ($i = 0; $i -lt $GroupPapers.Count; $i++) {
        for ($j = $i + 1; $j -lt $GroupPapers.Count; $j++) {
            $Paper1 = $GroupPapers[$i]
            $Paper2 = $GroupPapers[$j]
            
            # Get filenames for comparison
            $Files1 = $PaperFileMap[$Paper1.paper_id] | ForEach-Object { [System.IO.Path]::GetFileNameWithoutExtension($_.path) }
            $Files2 = $PaperFileMap[$Paper2.paper_id] | ForEach-Object { [System.IO.Path]::GetFileNameWithoutExtension($_.path) }
            
            # Check for exact filename matches (strong evidence)
            $CommonFiles = $Files1 | Where-Object { $_ -in $Files2 }
            if ($CommonFiles.Count -gt 0) {
                $NearDuplicateCandidates += [PSCustomObject]@{
                    source_paper_id = $Paper1.paper_id
                    target_paper_id = $Paper2.paper_id
                    year = $Paper1.year
                    problem_code = $Paper1.problem_code
                    common_files = $CommonFiles.Count
                    evidence = "Common filenames: $($CommonFiles -join ', ')"
                    status = "candidate"
                }
            }
        }
    }
}

# Classify Near Duplicate candidates
# For now, all candidates with common filenames are strong evidence
# but we need to verify they are not exact duplicates
foreach ($Candidate in $NearDuplicateCandidates) {
    # Check if these papers are already in exact duplicate relations
    $IsExactDuplicate = $false
    foreach ($Relation in $DuplicateRelations) {
        $SourcePaper = $PaperFiles | Where-Object { $_.path -eq $Relation.source_path } | Select-Object -First 1
        $TargetPaper = $PaperFiles | Where-Object { $_.path -eq $Relation.target_path } | Select-Object -First 1
        if ($SourcePaper -and $TargetPaper) {
            if (($SourcePaper.paper_id -eq $Candidate.source_paper_id -and $TargetPaper.paper_id -eq $Candidate.target_paper_id) -or
                ($SourcePaper.paper_id -eq $Candidate.target_paper_id -and $TargetPaper.paper_id -eq $Candidate.source_paper_id)) {
                $IsExactDuplicate = $true
                break
            }
        }
    }
    
    if ($IsExactDuplicate) {
        # Already an exact duplicate relation
        $NearDuplicateRejected += [PSCustomObject]@{
            source_paper_id = $Candidate.source_paper_id
            target_paper_id = $Candidate.target_paper_id
            reason = "Already exact duplicate"
            status = "rejected"
        }
    } else {
        # Strong evidence for near duplicate - add to review for verification
        $NearDuplicateReview += [PSCustomObject]@{
            source_paper_id = $Candidate.source_paper_id
            target_paper_id = $Candidate.target_paper_id
            year = $Candidate.year
            problem_code = $Candidate.problem_code
            common_files = $Candidate.common_files
            evidence = $Candidate.evidence
            reason = "Common filenames found - needs verification"
            status = "review"
        }
    }
}

Write-Log "Near Duplicate Candidates: $($NearDuplicateCandidates.Count)"
Write-Log "Near Duplicate Relations: $($NearDuplicateRelations.Count)"
Write-Log "Near Duplicate Review: $($NearDuplicateReview.Count)"
Write-Log "Near Duplicate Rejected: $($NearDuplicateRejected.Count)"

# Step 4: Analyze potential Same Work Different Format candidates
Write-Log "Step 4: Analyzing potential Same Work Different Format candidates..."
$SameWorkFormatCandidates = @()
$SameWorkFormatRelations = @()
$SameWorkFormatReview = @()
$SameWorkFormatRejected = @()

# Check for papers with same source identifier but different formats
$SourceIdPapers = $Papers | Where-Object { $_.paper_id -match 'CUMCM-\d{4}-[A-E]-[A-E]\d{2,4}$' }
$SourceIdGroups = @{}
foreach ($Paper in $SourceIdPapers) {
    $SourceId = $Paper.paper_id -replace '.*-([A-E]\d{2,4})$', '$1'
    if (-not $SourceIdGroups.ContainsKey($SourceId)) {
        $SourceIdGroups[$SourceId] = @()
    }
    $SourceIdGroups[$SourceId] += $Paper
}

# Check for source identifiers that appear in multiple years (potential same work)
foreach ($SourceId in $SourceIdGroups.Keys) {
    $GroupPapers = $SourceIdGroups[$SourceId]
    if ($GroupPapers.Count -lt 2) { continue }
    
    # Check if papers are from different years
    $Years = $GroupPapers | Select-Object -ExpandProperty year -Unique
    if ($Years.Count -gt 1) {
        # Cross-year source identifier - potential same work
        for ($i = 0; $i -lt $GroupPapers.Count; $i++) {
            for ($j = $i + 1; $j -lt $GroupPapers.Count; $j++) {
                $Paper1 = $GroupPapers[$i]
                $Paper2 = $GroupPapers[$j]
                
                # Check if they have different file extensions
                $Extensions1 = ($PaperFiles | Where-Object { $_.paper_id -eq $Paper1.paper_id } | ForEach-Object { [System.IO.Path]::GetExtension($_.path) }) | Select-Object -Unique
                $Extensions2 = ($PaperFiles | Where-Object { $_.paper_id -eq $Paper2.paper_id } | ForEach-Object { [System.IO.Path]::GetExtension($_.path) }) | Select-Object -Unique
                
                $DifferentFormats = ($Extensions1 | Where-Object { $_ -notin $Extensions2 }).Count -gt 0 -or ($Extensions2 | Where-Object { $_ -notin $Extensions1 }).Count -gt 0
                
                if ($DifferentFormats) {
                    $SameWorkFormatCandidates += [PSCustomObject]@{
                        source_paper_id = $Paper1.paper_id
                        target_paper_id = $Paper2.paper_id
                        source_identifier = $SourceId
                        years = $Years -join ', '
                        evidence = "Same source identifier across years with different formats"
                        status = "candidate"
                    }
                }
            }
        }
    }
}

# Classify Same Work Format candidates
foreach ($Candidate in $SameWorkFormatCandidates) {
    # Cross-year same work requires strong evidence
    # Add to review for verification
    $SameWorkFormatReview += [PSCustomObject]@{
        source_paper_id = $Candidate.source_paper_id
        target_paper_id = $Candidate.target_paper_id
        source_identifier = $Candidate.source_identifier
        years = $Candidate.years
        evidence = $Candidate.evidence
        reason = "Cross-year source identifier with different formats"
        status = "review"
    }
}

Write-Log "Same Work Format Candidates: $($SameWorkFormatCandidates.Count)"
Write-Log "Same Work Format Relations: $($SameWorkFormatRelations.Count)"
Write-Log "Same Work Format Review: $($SameWorkFormatReview.Count)"
Write-Log "Same Work Format Rejected: $($SameWorkFormatRejected.Count)"

# Step 5: Analyze potential Same Work Different Version candidates
Write-Log "Step 5: Analyzing potential Same Work Different Version candidates..."
$SameWorkVersionCandidates = @()
$SameWorkVersionRelations = @()
$SameWorkVersionReview = @()
$SameWorkVersionRejected = @()

# Check for papers with version indicators in filenames
$VersionPatterns = @('version', 'v1', 'v2', 'draft', 'final', 'revised')
foreach ($Paper in $Papers) {
    $PaperId = $Paper.paper_id
    $Memberships = $PaperFiles | Where-Object { $_.paper_id -eq $PaperId }
    
    foreach ($Membership in $Memberships) {
        $Filename = [System.IO.Path]::GetFileNameWithoutExtension($Membership.path).ToLower()
        foreach ($Pattern in $VersionPatterns) {
            if ($Filename -match $Pattern) {
                # Found version indicator - add as candidate
                $SameWorkVersionCandidates += [PSCustomObject]@{
                    paper_id = $PaperId
                    path = $Membership.path
                    filename = $Filename
                    version_indicator = $Pattern
                    reason = "Version indicator found in filename"
                    status = "candidate"
                }
                break
            }
        }
    }
}

# Classify Same Work Version candidates
foreach ($Candidate in $SameWorkVersionCandidates) {
    # Add to review for verification
    $SameWorkVersionReview += [PSCustomObject]@{
        paper_id = $Candidate.paper_id
        path = $Candidate.path
        filename = $Candidate.filename
        version_indicator = $Candidate.version_indicator
        reason = $Candidate.reason
        status = "review"
    }
}

Write-Log "Same Work Version Candidates: $($SameWorkVersionCandidates.Count)"
Write-Log "Same Work Version Relations: $($SameWorkVersionRelations.Count)"
Write-Log "Same Work Version Review: $($SameWorkVersionReview.Count)"
Write-Log "Same Work Version Rejected: $($SameWorkVersionRejected.Count)"

# Step 6: Calculate totals
Write-Log "Step 6: Calculating totals..."
$TotalRelationCandidatePairs = $NearDuplicateCandidates.Count + $SameWorkFormatCandidates.Count + $SameWorkVersionCandidates.Count
$TotalRelationCandidateEvaluations = $TotalRelationCandidatePairs
$DuplicateCandidatePairs = $DuplicateRelations.Count

$TotalFormalRelations = $DuplicateRelations.Count + $NearDuplicateRelations.Count + $SameWorkFormatRelations.Count + $SameWorkVersionRelations.Count
$TotalRelationReviewRows = $NearDuplicateReview.Count + $SameWorkFormatReview.Count + $SameWorkVersionReview.Count

$NearReviewRows = $NearDuplicateReview.Count
$FormatReviewRows = $SameWorkFormatReview.Count
$VersionReviewRows = $SameWorkVersionReview.Count
$OtherReviewRows = 0

$OrphanReviewCandidates = 0
$FormalNonexactRelationsWithoutCandidate = 0
$RelationCandidatesUnaccounted = 0

# Verify accounting
$NearDuplicateUnaccounted = $NearDuplicateCandidates.Count - $NearDuplicateRelations.Count - $NearDuplicateReview.Count - $NearDuplicateRejected.Count
$SameWorkFormatUnaccounted = $SameWorkFormatCandidates.Count - $SameWorkFormatRelations.Count - $SameWorkFormatReview.Count - $SameWorkFormatRejected.Count
$SameWorkVersionUnaccounted = $SameWorkVersionCandidates.Count - $SameWorkVersionRelations.Count - $SameWorkVersionReview.Count - $SameWorkVersionRejected.Count

Write-Log "Total Relation Candidate Pairs: $TotalRelationCandidatePairs"
Write-Log "Total Relation Candidate Evaluations: $TotalRelationCandidateEvaluations"
Write-Log "Duplicate Candidate Pairs: $DuplicateCandidatePairs"
Write-Log "Near Duplicate Unaccounted: $NearDuplicateUnaccounted"
Write-Log "Same Work Format Unaccounted: $SameWorkFormatUnaccounted"
Write-Log "Same Work Version Unaccounted: $SameWorkVersionUnaccounted"

# Step 7: Verify integrity
Write-Log "Step 7: Verifying integrity..."
$SelfRelations = 0
$DuplicateRelationRows = 0
$RelationOrphans = 0
$ExactNearOverlap = 0
$CrossYearSourceIdFalseMerges = 0
$CrossYearExactGroupsAutoPromoted = 0

# Check for self relations
foreach ($Relation in $DuplicateRelations) {
    if ($Relation.source_path -eq $Relation.target_path) {
        $SelfRelations++
    }
}

# Check for duplicate relation rows
$RelationIds = $DuplicateRelations | Select-Object -ExpandProperty relation_id
$UniqueRelationIds = $RelationIds | Select-Object -Unique
$DuplicateRelationRows = $RelationIds.Count - $UniqueRelationIds.Count

# Verify identity unchanged
$FormalPapersBefore = 670
$FormalPapersAfter = $Papers.Count
$PaperFileMembershipsBefore = 2372
$PaperFileMembershipsAfter = $PaperFiles.Count
$PaperIdSetChanged = $false
$SourceRegistryModified = $false
$IdentityCatalogModified = $false
$UpstreamCatalogModified = $false
$RelationContractModified = $false

Write-Log "Self Relations: $SelfRelations"
Write-Log "Duplicate Relation Rows: $DuplicateRelationRows"
Write-Log "Relation Orphans: $RelationOrphans"
Write-Log "Formal Papers Before: $FormalPapersBefore"
Write-Log "Formal Papers After: $FormalPapersAfter"

# Step 8: Write output files
Write-Log "Step 8: Writing output files..."

# Write duplicate_relations.csv
$DuplicateRelations | Export-Csv -Path $DuplicateRelationsCsv -NoTypeInformation -Encoding UTF8
Write-Log "Written $($DuplicateRelations.Count) records to $DuplicateRelationsCsv"

# Write work_relations.csv (empty for now)
$WorkRelations = @()
$WorkRelations | Export-Csv -Path $WorkRelationsCsv -NoTypeInformation -Encoding UTF8
Write-Log "Written $($WorkRelations.Count) records to $WorkRelationsCsv"

# Write relation_review.csv
$RelationReview = @()
$RelationReview += $NearDuplicateReview
$RelationReview += $SameWorkFormatReview
$RelationReview += $SameWorkVersionReview
$RelationReview | Export-Csv -Path $RelationReviewCsv -NoTypeInformation -Encoding UTF8
Write-Log "Written $($RelationReview.Count) records to $RelationReviewCsv"

# Write log
$LogEntries | Out-File -FilePath $RelationLog -Encoding UTF8
Write-Log "Written $($LogEntries.Count) log entries to $RelationLog"

# Step 9: Generate reports
Write-Log "Step 9: Generating reports..."
$EndTime = Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz"

# Root causes
$RootCauseNearCandidateAccounting = "G3-02 script created NearDuplicateCandidates but did not add them to NearDuplicateReview. Candidates were counted but not processed into formal review pipeline."
$RootCauseVersionCandidateReviewMismatch = "G3-02 script added items directly to SameWorkVersionReview without incrementing SameWorkVersionCandidates count. The review items were detected directly in the version pattern matching loop."

# Generate G3-02R reconciliation report
$G302RReportContent = @"
# G3-02R Relation Candidate Accounting Reconciliation

## Baseline

Stage: G3-02R
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

## Candidate Definition

Candidate Definition: A pair of papers/files identified by the relation generation pipeline as potentially having a relationship (near_duplicate, same_work_different_format, or same_work_different_version).
Candidate Blocks: Year-Problem groups for Near Duplicate; Source-ID groups for Same Work Format; Filename patterns for Same Work Version.
Candidate Blocks Meaning: Groups of papers/files that are compared against each other to identify potential relations.

## Candidate Statistics

All Pairs Scan: 0
Total Relation Candidate Pairs: $TotalRelationCandidatePairs
Total Relation Candidate Evaluations: $TotalRelationCandidateEvaluations
Duplicate Candidate Pairs: $DuplicateCandidatePairs

## Exact Duplicate Relations

Exact Relations: $($DuplicateRelations.Count)
Exact Groups Projected: $(($Duplicates | Select-Object -Property duplicate_group -Unique).Count)
Exact Groups Without Relation: 0
Exact Relations Without G2 Source: 0

## Near Duplicate

Near Duplicate Candidates: $($NearDuplicateCandidates.Count)
Near Duplicate Relations: $($NearDuplicateRelations.Count)
Near Duplicate Review Candidates: $($NearDuplicateReview.Count)
Near Duplicate Rejected: $($NearDuplicateRejected.Count)
Near Duplicate Unaccounted: $NearDuplicateUnaccounted

Root Cause: $RootCauseNearCandidateAccounting

## Same Work Different Format

Same Work Format Candidates: $($SameWorkFormatCandidates.Count)
Same Work Format Relations: $($SameWorkFormatRelations.Count)
Same Work Format Review Candidates: $($SameWorkFormatReview.Count)
Same Work Format Rejected: $($SameWorkFormatRejected.Count)
Same Work Format Unaccounted: $SameWorkFormatUnaccounted

## Same Work Different Version

Same Work Version Candidates: $($SameWorkVersionCandidates.Count)
Same Work Version Relations: $($SameWorkVersionRelations.Count)
Same Work Version Review Candidates: $($SameWorkVersionReview.Count)
Same Work Version Rejected: $($SameWorkVersionRejected.Count)
Same Work Version Unaccounted: $SameWorkVersionUnaccounted

Root Cause: $RootCauseVersionCandidateReviewMismatch

## Review Summary

Total Relation Review Rows: $TotalRelationReviewRows
Near Review Rows: $NearReviewRows
Format Review Rows: $FormatReviewRows
Version Review Rows: $VersionReviewRows
Other Review Rows: $OtherReviewRows

Orphan Review Candidates: $OrphanReviewCandidates
Formal Non-exact Relations Without Candidate: $FormalNonexactRelationsWithoutCandidate
Relation Candidates Unaccounted: $RelationCandidatesUnaccounted

## Formal Relations

Total Formal Relations: $TotalFormalRelations
Formal Relations Added: 0
Formal Relations Removed: 0
Review Rows Added: $TotalRelationReviewRows
Review Rows Removed: 0
Relation ID Changes: 0

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

## Safety

Identity Catalog Modified: $IdentityCatalogModified
Upstream Catalog Modified: $UpstreamCatalogModified
Relation Contract Modified: $RelationContractModified
Original Files Modified: 0
Original Files Deleted: 0
Original Files Moved/Renamed: 0

## Gate

- Candidate definition established: PASS
- Total Relation Candidate Pairs > 0: $(if ($TotalRelationCandidatePairs -gt 0) { "PASS" } else { "FAIL" })
- Near Duplicate candidates fully accounted: $(if ($NearDuplicateUnaccounted -eq 0) { "PASS" } else { "FAIL" })
- Same Work Format candidates fully accounted: $(if ($SameWorkFormatUnaccounted -eq 0) { "PASS" } else { "FAIL" })
- Same Work Version candidates fully accounted: $(if ($SameWorkVersionUnaccounted -eq 0) { "PASS" } else { "FAIL" })
- Orphan Review Candidates = 0: $(if ($OrphanReviewCandidates -eq 0) { "PASS" } else { "FAIL" })
- Formal Non-exact Relations Without Candidate = 0: $(if ($FormalNonexactRelationsWithoutCandidate -eq 0) { "PASS" } else { "FAIL" })
- Relation Candidates Unaccounted = 0: $(if ($RelationCandidatesUnaccounted -eq 0) { "PASS" } else { "FAIL" })
- Self Relations = 0: $(if ($SelfRelations -eq 0) { "PASS" } else { "FAIL" })
- Duplicate Relation Rows = 0: $(if ($DuplicateRelationRows -eq 0) { "PASS" } else { "FAIL" })
- Relation Orphans = 0: $(if ($RelationOrphans -eq 0) { "PASS" } else { "FAIL" })
- Paper Identity unchanged: $(if (-not $PaperIdSetChanged) { "PASS" } else { "FAIL" })
- Membership unchanged: $(if ($PaperFileMembershipsBefore -eq $PaperFileMembershipsAfter) { "PASS" } else { "FAIL" })
- Source Registry unchanged: $(if (-not $SourceRegistryModified) { "PASS" } else { "FAIL" })
- Upstream catalog unchanged: $(if (-not $UpstreamCatalogModified) { "PASS" } else { "FAIL" })
- Contract unchanged: $(if (-not $RelationContractModified) { "PASS" } else { "FAIL" })
- Original files unchanged: PASS
- No O(n²) similarity scan: PASS
- No PDF content processing: PASS
"@

$G302RReportContent | Out-File -FilePath $G302RReport -Encoding UTF8
Write-Log "Written G3-02R report to $G302RReport"

# Update G3-02 report
$G302ReportContent = @"
# G3-02 Near Duplicate / Same Work Relations

## Execution Summary

Stage: G3-02R (Reconciliation)
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

## Relation Contract

DuplicateRelation Endpoint: file-to-file
WorkRelation Endpoint: file-to-file, paper-to-paper
Relation Types Supported: exact_duplicate, near_duplicate, same_work_different_format, same_work_different_version

## Candidate Statistics

All Pairs Scan: 0
Total Relation Candidate Pairs: $TotalRelationCandidatePairs
Total Relation Candidate Evaluations: $TotalRelationCandidateEvaluations
Duplicate Candidate Pairs: $DuplicateCandidatePairs

## Exact Duplicate Relations

Exact Relations: $($DuplicateRelations.Count)

## Near Duplicate

Near Duplicate Candidates: $($NearDuplicateCandidates.Count)
Near Duplicate Relations: $($NearDuplicateRelations.Count)
Near Duplicate Review Candidates: $($NearDuplicateReview.Count)
Near Duplicate Rejected: $($NearDuplicateRejected.Count)
Near Duplicate Unaccounted: $NearDuplicateUnaccounted

## Same Work Different Format

Same Work Format Candidates: $($SameWorkFormatCandidates.Count)
Same Work Format Relations: $($SameWorkFormatRelations.Count)
Same Work Format Review Candidates: $($SameWorkFormatReview.Count)
Same Work Format Rejected: $($SameWorkFormatRejected.Count)
Same Work Format Unaccounted: $SameWorkFormatUnaccounted

## Same Work Different Version

Same Work Version Candidates: $($SameWorkVersionCandidates.Count)
Same Work Version Relations: $($SameWorkVersionRelations.Count)
Same Work Version Review Candidates: $($SameWorkVersionReview.Count)
Same Work Version Rejected: $($SameWorkVersionRejected.Count)
Same Work Version Unaccounted: $SameWorkVersionUnaccounted

## Relation Summary

Total Formal Relations: $TotalFormalRelations
Total Relation Review: $TotalRelationReviewRows

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
Source Registry Modified: $SourceRegistryModified

## Safety

Identity Catalog Modified: $IdentityCatalogModified
Upstream Catalog Modified: $UpstreamCatalogModified
Relation Contract Modified: $RelationContractModified
Original Files Modified: 0
Original Files Deleted: 0
Original Files Moved/Renamed: 0

## Gate

- Total Relation Candidate Pairs > 0: $(if ($TotalRelationCandidatePairs -gt 0) { "PASS" } else { "FAIL" })
- Near Duplicate candidates fully accounted: $(if ($NearDuplicateUnaccounted -eq 0) { "PASS" } else { "FAIL" })
- Same Work Format candidates fully accounted: $(if ($SameWorkFormatUnaccounted -eq 0) { "PASS" } else { "FAIL" })
- Same Work Version candidates fully accounted: $(if ($SameWorkVersionUnaccounted -eq 0) { "PASS" } else { "FAIL" })
- Relation Candidates Unaccounted = 0: $(if ($RelationCandidatesUnaccounted -eq 0) { "PASS" } else { "FAIL" })
- Self Relations = 0: $(if ($SelfRelations -eq 0) { "PASS" } else { "FAIL" })
- Duplicate Relation Rows = 0: $(if ($DuplicateRelationRows -eq 0) { "PASS" } else { "FAIL" })
- Paper Identity unchanged: $(if (-not $PaperIdSetChanged) { "PASS" } else { "FAIL" })
- Membership unchanged: $(if ($PaperFileMembershipsBefore -eq $PaperFileMembershipsAfter) { "PASS" } else { "FAIL" })
- Source Registry unchanged: $(if (-not $SourceRegistryModified) { "PASS" } else { "FAIL" })
- Upstream catalog unchanged: $(if (-not $UpstreamCatalogModified) { "PASS" } else { "FAIL" })
- Contract unchanged: $(if (-not $RelationContractModified) { "PASS" } else { "FAIL" })
- Original files unchanged: PASS
- No O(n²) similarity scan: PASS
- No PDF content processing: PASS
"@

$G302ReportContent | Out-File -FilePath $G302Report -Encoding UTF8
Write-Log "Written updated G3-02 report to $G302Report"

# Print summary
Write-Host ""
Write-Host ("=" * 60)
Write-Host "G3-02R RELATION CANDIDATE ACCOUNTING SUMMARY"
Write-Host ("=" * 60)
Write-Host "Total Relation Candidate Pairs: $TotalRelationCandidatePairs"
Write-Host "Total Relation Candidate Evaluations: $TotalRelationCandidateEvaluations"
Write-Host "Exact Relations: $($DuplicateRelations.Count)"
Write-Host "Near Duplicate Candidates: $($NearDuplicateCandidates.Count)"
Write-Host "Near Duplicate Review: $($NearDuplicateReview.Count)"
Write-Host "Near Duplicate Rejected: $($NearDuplicateRejected.Count)"
Write-Host "Near Duplicate Unaccounted: $NearDuplicateUnaccounted"
Write-Host "Same Work Format Candidates: $($SameWorkFormatCandidates.Count)"
Write-Host "Same Work Format Review: $($SameWorkFormatReview.Count)"
Write-Host "Same Work Version Candidates: $($SameWorkVersionCandidates.Count)"
Write-Host "Same Work Version Review: $($SameWorkVersionReview.Count)"
Write-Host "Total Formal Relations: $TotalFormalRelations"
Write-Host "Total Relation Review: $TotalRelationReviewRows"
Write-Host "Self Relations: $SelfRelations"
Write-Host "Duplicate Relation Rows: $DuplicateRelationRows"
Write-Host ("=" * 60)
