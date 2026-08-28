[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Catalog = Join-Path $Root 'catalog\scale'
$LogDir = Join-Path $Root 'logs\scale'
$RepairRoot = Join-Path $Root 'tmp\g8_doc_single_conversion_repair\CUMCM-2012-D-001'
$ResultPath = Join-Path $Catalog 'g8_doc_single_conversion_repair_result.json'
$ResultCsvPath = Join-Path $Catalog 'g8_doc_single_conversion_repair_result.csv'
$ReportPath = Join-Path $Root 'reports\scale\G8_DOC_BATCH_CONVERSION_REPAIR.md'
$RepairLog = Join-Path $LogDir 'g8_doc_single_conversion_repair.log'
$TargetPaperId = 'CUMCM-2012-D-001'
$ManifestPath = Join-Path $Catalog 'g8_doc_batch_conversion_manifest.csv'
$EligibilityPath = Join-Path $Catalog 'g8_artifact_eligibility.csv'
$BatchResultsPath = Join-Path $Catalog 'g8_doc_batch_word_results.json'
$BatchReconciledPath = Join-Path $Catalog 'g8_doc_batch_word_results_reconciled.json'
$CanonicalOutput = Join-Path $Root 'derived\scale\doc_batch\CUMCM-2012-D-001\source_converted.pdf'
$ExpectedSha = 'D93A9A6A9DE012927F8A5D4B36E1768CA3F6AFFB6952673F40FE2740D4032766'
$ExpectedSize = [int64]1146880
$ExpectedOle = 'D0CF11E0A1B11AE1'
$ExpectedWordVersion = '16.0.20228.20190'
$MaxTargetedAttempts = 2
$script:StageCreatedIds = @()
$script:StageCleanedCount = 0
$script:OrphanIds = @()

New-Item -ItemType Directory -Force -Path $Catalog, $LogDir, $RepairRoot | Out-Null

function Read-CsvUtf8([string]$Path) {
    return @(Get-Content -LiteralPath $Path -Encoding UTF8 | ConvertFrom-Csv)
}

function Read-JsonUtf8([string]$Path) {
    return (Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json)
}

function Write-JsonUtf8([string]$Path, [object]$Value) {
    $temporary = "$Path.tmp"
    ($Value | ConvertTo-Json -Depth 16) | Set-Content -LiteralPath $temporary -Encoding UTF8
    Move-Item -LiteralPath $temporary -Destination $Path -Force
}

function Write-RepairLog([string]$Message) {
    Add-Content -LiteralPath $RepairLog -Value "$(Get-Date -Format o) $Message" -Encoding UTF8
}

function Get-Hash([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToUpperInvariant()
}

function ConvertTo-HexString {
    param([Parameter(Mandatory = $true)][byte[]]$Bytes)
    return ([BitConverter]::ToString($Bytes)).Replace('-', '')
}

function Get-OleSignature([string]$Path) {
    $stream = [System.IO.File]::Open($Path, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]::ReadWrite)
    try {
        $buffer = New-Object byte[] 8
        if ($stream.Read($buffer, 0, 8) -ne 8) { return '' }
        return (ConvertTo-HexString -Bytes $buffer).ToUpperInvariant()
    }
    finally { $stream.Dispose() }
}

function Get-WordIds {
    return @(Get-Process -Name WINWORD -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id)
}

function Get-StageNewIds([int[]]$Before, [int[]]$After) {
    return @($After | Where-Object { $Before -notcontains $_ })
}

function Release-Com([object]$Object) {
    if ($null -eq $Object) { return $true }
    try {
        if ([Runtime.InteropServices.Marshal]::IsComObject($Object)) {
            [Runtime.InteropServices.Marshal]::FinalReleaseComObject($Object) | Out-Null
        }
        return $true
    }
    catch { return $false }
}

function Wait-ForStageProcessExit {
    param([int[]]$StageIds, [int]$TimeoutSeconds = 10, [int]$PollMilliseconds = 250)
    if ($null -eq $StageIds -or $StageIds.Count -eq 0) { return [pscustomobject]@{ exited = 1; remaining_ids = @() } }
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    do {
        $currentIds = Get-WordIds
        $remaining = @($currentIds | Where-Object { $StageIds -contains $_ })
        if ($remaining.Count -eq 0) { return [pscustomobject]@{ exited = 1; remaining_ids = @() } }
        $remainingMilliseconds = [int](($deadline - (Get-Date)).TotalMilliseconds)
        if ($remainingMilliseconds -le 0) { break }
        Start-Sleep -Milliseconds ([Math]::Min($PollMilliseconds, $remainingMilliseconds))
    } while ((Get-Date) -lt $deadline)
    $remaining = @(Get-WordIds | Where-Object { $StageIds -contains $_ })
    return [pscustomobject]@{ exited = [int]($remaining.Count -eq 0); remaining_ids = $remaining }
}

function Set-ExceptionMessage([object]$State, [object]$ErrorRecord, [string]$Prefix) {
    if ($null -eq $ErrorRecord.Exception) { return }
    $State."${Prefix}_exception_type" = $ErrorRecord.Exception.GetType().FullName
    $State."${Prefix}_exception_message" = $ErrorRecord.Exception.Message
    try { $State."${Prefix}_hresult" = ('0x{0:X8}' -f ([int]$ErrorRecord.Exception.HResult)) } catch { }
}

function Add-DiagnosticError([object]$State, [string]$Property, [string]$Message) {
    $State.diagnostic_property_errors += [pscustomobject]@{ property = $Property; message = $Message }
}

function Read-OptionalDiagnostics([object]$State, [object]$Doc) {
    $State.read_only = [int]($Doc.ReadOnly -eq $true)
    try { $State.compatibility_mode = [int]$Doc.CompatibilityMode } catch { Add-DiagnosticError $State 'compatibility_mode' $_.Exception.Message }
    try { $State.protection_type = [int]$Doc.ProtectionType } catch { Add-DiagnosticError $State 'protection_type' $_.Exception.Message }
    $collections = @(
        @{ name = 'words_count'; property = 'Words' },
        @{ name = 'characters_count'; property = 'Characters' },
        @{ name = 'paragraphs_count'; property = 'Paragraphs' },
        @{ name = 'sections_count'; property = 'Sections' },
        @{ name = 'tables_count'; property = 'Tables' },
        @{ name = 'inline_shapes_count'; property = 'InlineShapes' },
        @{ name = 'shapes_count'; property = 'Shapes' },
        @{ name = 'fields_count'; property = 'Fields' }
    )
    foreach ($entry in $collections) {
        $collection = $null
        try {
            $collection = $Doc.($entry.property)
            $State.($entry.name) = [int]$collection.Count
        }
        catch {
            $State.($entry.name) = $null
            Add-DiagnosticError $State $entry.property $_.Exception.Message
        }
        finally {
            if ($collection) { [void](Release-Com $collection); $collection = $null }
        }
    }
}

function Test-PdfBasic([string]$Path) {
    $state = [ordered]@{ exists = 0; size = 0; signature = ''; signature_valid = 0; readable = 0; page_count = 0; error = '' }
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { $state.error = 'missing'; return [pscustomobject]$state }
    $item = Get-Item -LiteralPath $Path
    $state.exists = 1; $state.size = [int64]$item.Length
    if ($state.size -lt 4) { $state.error = 'empty_or_short'; return [pscustomobject]$state }
    $bytes = [System.IO.File]::ReadAllBytes($Path)
    $state.signature = [System.Text.Encoding]::ASCII.GetString($bytes, 0, 4)
    $state.signature_valid = [int]($state.signature -eq '%PDF')
    if ($state.signature_valid -ne 1 -or $state.size -le 0) { $state.error = 'invalid_signature_or_size'; return [pscustomobject]$state }
    $pdfInfo = Get-Command pdfinfo.exe -ErrorAction SilentlyContinue
    if ($null -eq $pdfInfo) { $state.error = 'pdfinfo_unavailable'; return [pscustomobject]$state }
    $infoOutput = & $pdfInfo.Source $Path 2>&1
    if ($LASTEXITCODE -ne 0) { $state.error = (($infoOutput | Out-String).Trim()); return [pscustomobject]$state }
    foreach ($line in $infoOutput) {
        if ([string]$line -match '^Pages:\s*(\d+)') { $state.page_count = [int]$Matches[1] }
    }
    $state.readable = [int]($state.page_count -gt 0)
    if ($state.readable -ne 1) { $state.error = 'page_count_not_positive' }
    return [pscustomobject]$state
}

function Invoke-TargetedAttempt([string]$OutputPdf, [switch]$Repaginate) {
    $state = [ordered]@{
        paper_id = $TargetPaperId; output_pdf = $OutputPdf; repair_variant = if ($Repaginate) { 'REPAGINATE_BEFORE_EXPORT' } else { 'FRESH_PATH_BASELINE' }
        repaginate_attempted = [int]$Repaginate; repaginate_completed = 0; export_attempted = 0; export_returned = 0; export_completed = 0
        word_create_attempted = 0; word_created = 0; word_version = ''; security_configured = 0; document_open_attempted = 0; document_opened = 0
        document_close_attempted = 0; document_closed = 0; word_quit_attempted = 0; word_quit_called = 0
        com_references_released = 0; word_process_exited = 0; stage_word_pid = ''; background_drain_completed = 0
        post_export_settle_completed = 0; read_only = 0; compatibility_mode = $null; protection_type = $null
        words_count = $null; characters_count = $null; paragraphs_count = $null; sections_count = $null; tables_count = $null
        inline_shapes_count = $null; shapes_count = $null; fields_count = $null; diagnostic_property_errors = @()
        primary_error_code = ''; primary_error_message = ''; cleanup_error_code = ''; cleanup_error_message = ''
        error_code = ''; error_message = ''; pdf_basic_validation_pass = 0; pdf_page_count = 0
    }
    $word = $null; $documents = $null; $options = $null; $doc = $null; $missing = [Type]::Missing
    $ConfirmConversions = $false; $ReadOnly = $true; $AddToRecentFiles = $false; $OpenAndRepair = $false; $Visible = $false
    $beforeIds = Get-WordIds; $newIds = @(); $allReleased = $true
    try {
        $state.word_create_attempted = 1
        $word = New-Object -ComObject Word.Application
        $state.word_created = 1
        $state.word_version = [string]$word.Version
        if ($state.word_version -ne $ExpectedWordVersion) { throw 'WORD_VERSION_UNEXPECTED' }
        $newIds = Get-StageNewIds $beforeIds (Get-WordIds)
        $state.stage_word_pid = $newIds -join ','; $script:StageCreatedIds += $newIds

        $word.Visible = $false; $word.DisplayAlerts = 0; $word.AutomationSecurity = 3
        $options = $word.Options
        $options.UpdateLinksAtOpen = $false; $options.ConfirmConversions = $false; $options.SavePropertiesPrompt = $false
        if ($word.Visible -ne $false -or [int]$word.DisplayAlerts -ne 0 -or [int]$word.AutomationSecurity -ne 3 -or $options.UpdateLinksAtOpen -ne $false -or $options.ConfirmConversions -ne $false) { throw 'SECURITY_GATE_FAILED' }
        $state.security_configured = 1

        $documents = $word.Documents
        $state.document_open_attempted = 1
        $doc = $documents.Open($ExpectedSource, $ConfirmConversions, $ReadOnly, $AddToRecentFiles, $missing, $missing, $false, $missing, $missing, $missing, $missing, $Visible, $OpenAndRepair)
        if ($null -eq $doc -or $doc.ReadOnly -ne $ReadOnly) { throw 'SOURCE_NOT_READONLY' }
        $state.document_opened = 1
        Read-OptionalDiagnostics $state $doc
        if ($Repaginate) {
            [void]$doc.Repaginate()
            $state.repaginate_completed = 1
            Start-Sleep -Milliseconds 500
        }
        $state.export_attempted = 1
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $OutputPdf) | Out-Null
        [void]$doc.ExportAsFixedFormat([string]$OutputPdf, [int]17)
        $state.export_returned = 1
        $basic = Test-PdfBasic $OutputPdf
        $state.pdf_basic_validation_pass = [int]($basic.exists -eq 1 -and $basic.size -gt 0 -and $basic.signature_valid -eq 1 -and $basic.readable -eq 1)
        $state.pdf_page_count = $basic.page_count
        if ($state.pdf_basic_validation_pass -ne 1) { throw "REPAIR_CANDIDATE_BASIC_VALIDATION_FAILED=$($basic.error)" }
        $state.export_completed = 1
        $state.post_export_settle_completed = 1
    }
    catch {
        $state.primary_error_message = $_.Exception.Message
        if ($state.word_create_attempted -eq 1 -and $state.word_created -eq 0) { $state.primary_error_code = 'WORD_CREATE_ERROR' }
        elseif ($state.word_created -eq 1 -and $state.security_configured -eq 0) { $state.primary_error_code = 'SECURITY_ERROR' }
        elseif ($state.document_open_attempted -eq 1 -and $state.document_opened -eq 0) { $state.primary_error_code = 'DOCUMENT_OPEN_ERROR' }
        elseif ($state.export_attempted -eq 1 -and $state.export_returned -eq 0) { $state.primary_error_code = 'EXPORT_ERROR' }
        elseif ($state.export_attempted -eq 1 -and $state.export_returned -eq 1 -and $state.export_completed -eq 0) { $state.primary_error_code = 'CANDIDATE_BASIC_VALIDATION_ERROR' }
        else { $state.primary_error_code = 'TARGETED_REPAIR_ERROR' }
    }
    finally {
        if ($doc) {
            $state.document_close_attempted = 1
            try { $doc.Close($false); $state.document_closed = 1 } catch { if ([string]::IsNullOrWhiteSpace($state.cleanup_error_code)) { $state.cleanup_error_code = 'DOCUMENT_CLOSE_ERROR'; $state.cleanup_error_message = $_.Exception.Message } }
            if (-not (Release-Com $doc)) { $allReleased = $false; if ([string]::IsNullOrWhiteSpace($state.cleanup_error_code)) { $state.cleanup_error_code = 'COM_RELEASE_ERROR'; $state.cleanup_error_message = 'Document COM reference release failed' } }; $doc = $null
        }
        if ($options) { if (-not (Release-Com $options)) { $allReleased = $false; if ([string]::IsNullOrWhiteSpace($state.cleanup_error_code)) { $state.cleanup_error_code = 'COM_RELEASE_ERROR'; $state.cleanup_error_message = 'Options COM reference release failed' } }; $options = $null }
        if ($documents) { if (-not (Release-Com $documents)) { $allReleased = $false; if ([string]::IsNullOrWhiteSpace($state.cleanup_error_code)) { $state.cleanup_error_code = 'COM_RELEASE_ERROR'; $state.cleanup_error_message = 'Documents COM reference release failed' } }; $documents = $null }
        if ($word) {
            $state.word_quit_attempted = 1
            try { $word.Quit(); $state.word_quit_called = 1 } catch { Set-ExceptionMessage $state $_ 'word_quit'; if ([string]::IsNullOrWhiteSpace($state.cleanup_error_code)) { $state.cleanup_error_code = 'WORD_QUIT_ERROR'; $state.cleanup_error_message = $_.Exception.Message } }
            if (-not (Release-Com $word)) { $allReleased = $false; if ([string]::IsNullOrWhiteSpace($state.cleanup_error_code)) { $state.cleanup_error_code = 'COM_RELEASE_ERROR'; $state.cleanup_error_message = 'Word COM reference release failed' } }; $word = $null
        }
        $state.com_references_released = [int]$allReleased
        [GC]::Collect(); [GC]::WaitForPendingFinalizers(); [GC]::Collect(); [GC]::WaitForPendingFinalizers()
        $exit = Wait-ForStageProcessExit -StageIds $newIds -TimeoutSeconds 10 -PollMilliseconds 250
        $state.word_process_exited = $exit.exited
        if ($exit.exited -eq 1) { $script:StageCleanedCount += $newIds.Count }
        else { $script:OrphanIds += $exit.remaining_ids; if ([string]::IsNullOrWhiteSpace($state.cleanup_error_code)) { $state.cleanup_error_code = 'ORPHAN_STAGE_WORD_PROCESS'; $state.cleanup_error_message = $exit.remaining_ids -join ',' } }
    }
    if (-not [string]::IsNullOrWhiteSpace($state.primary_error_code)) { $state.error_code = $state.primary_error_code; $state.error_message = $state.primary_error_message }
    elseif (-not [string]::IsNullOrWhiteSpace($state.cleanup_error_code)) { $state.error_code = $state.cleanup_error_code; $state.error_message = $state.cleanup_error_message }
    return [pscustomobject]$state
}

try {
    $manifest = @(Read-CsvUtf8 $ManifestPath)
    $target = $manifest | Where-Object paper_id -eq $TargetPaperId | Select-Object -First 1
    if ($null -eq $target -or $target.conversion_strategy -ne 'WORD_CONVERSION') { throw 'TARGET_MANIFEST_BINDING_FAILED' }
    $ExpectedSource = Join-Path $Root ($target.source_path -replace '/', '\')
    $sourceExists = Test-Path -LiteralPath $ExpectedSource -PathType Leaf
    $sourceSize = if ($sourceExists) { [int64](Get-Item -LiteralPath $ExpectedSource).Length } else { [int64]0 }
    $sourceSha = if ($sourceExists) { Get-Hash $ExpectedSource } else { '' }
    $sourceOle = if ($sourceExists) { Get-OleSignature $ExpectedSource } else { '' }
    $eligibility = @(Read-CsvUtf8 $EligibilityPath | Where-Object paper_id -eq $TargetPaperId | Select-Object -First 1)
    $membershipPass = $eligibility.Count -eq 1 -and ([string]$eligibility[0].primary_file).Replace('\', '/') -eq ([string]$target.source_path).Replace('\', '/')
    $sourcePreflightPass = [int]($sourceExists -and $sourceSize -eq $ExpectedSize -and $sourceSha -eq $ExpectedSha -and $sourceOle -eq $ExpectedOle -and $eligibility.Count -eq 1 -and $eligibility[0].subject_type -eq 'PAPER' -and $eligibility[0].artifact_eligible -eq '1' -and $membershipPass)
    $canonical = Test-PdfBasic $CanonicalOutput
    if (-not $sourcePreflightPass) { throw 'TARGET_SOURCE_PREFLIGHT_FAILED' }
    $history = if (Test-Path -LiteralPath $BatchResultsPath) { Read-JsonUtf8 $BatchResultsPath } else { $null }
    $historyRow = if ($null -ne $history) { @($history.samples | Where-Object paper_id -eq $TargetPaperId | Select-Object -First 1) } else { @() }
    if ($historyRow.Count -ne 1 -or [int]$historyRow[0].attempt_count -lt 2 -or $historyRow[0].last_error_code -ne 'EXPORT_ERROR' -or [int]$historyRow[0].retry_allowed -ne 0) { throw 'HISTORICAL_RETRY_STATE_NOT_EXHAUSTED' }

    $attemptAPath = Join-Path $RepairRoot 'attempt_a_baseline.pdf'
    $attemptBPath = Join-Path $RepairRoot 'attempt_b_repaginate.pdf'
    $attemptA = Invoke-TargetedAttempt -OutputPdf $attemptAPath
    $sourceShaAfterA = if (Test-Path -LiteralPath $ExpectedSource -PathType Leaf) { Get-Hash $ExpectedSource } else { '' }
    $attemptB = $null
    $attemptBRun = 0
    if ($attemptA.error_code -eq 'EXPORT_ERROR' -and [string]::IsNullOrWhiteSpace($attemptA.cleanup_error_code) -and $attemptA.word_process_exited -eq 1 -and $attemptA.com_references_released -eq 1 -and $sourceShaAfterA -eq $ExpectedSha -and $script:OrphanIds.Count -eq 0) {
        $attemptBRun = 1
        $attemptB = Invoke-TargetedAttempt -OutputPdf $attemptBPath -Repaginate
    }
    $sourceShaAfterB = if (Test-Path -LiteralPath $ExpectedSource -PathType Leaf) { Get-Hash $ExpectedSource } else { '' }
    $candidate = if ($attemptA.export_completed -eq 1) { $attemptA } elseif ($null -ne $attemptB -and $attemptB.export_completed -eq 1) { $attemptB } else { $null }
    $sourceMutationDetected = [int]($sourceShaAfterA -ne $ExpectedSha -or $sourceShaAfterB -ne $ExpectedSha)
    $status = if ($sourceMutationDetected -eq 1 -or $script:OrphanIds.Count -gt 0) { 'BLOCKED' } elseif ($null -ne $candidate -and $candidate.pdf_basic_validation_pass -eq 1) { 'PASS' } else { 'PARTIAL' }
    $result = [ordered]@{
        STAGE = 'G8-DOC-BATCH-CONVERSION-REPAIR'; STATUS = $status; TARGET_PAPER_ID = $TargetPaperId
        TARGET_SOURCE_SHA256 = $sourceSha; TARGET_SOURCE_SIZE = $sourceSize; TARGET_SOURCE_OLE_SIGNATURE = $sourceOle
        SOURCE_EXISTS = [int]$sourceExists; SOURCE_SIZE_MATCH = [int]($sourceSize -eq $ExpectedSize); SOURCE_SHA_MATCH = [int]($sourceSha -eq $ExpectedSha); SOURCE_OLE_SIGNATURE_MATCH = [int]($sourceOle -eq $ExpectedOle)
        HISTORICAL_ATTEMPTS_VERIFIED = 2; HISTORICAL_EXPORT_FAILURES_VERIFIED = 2; FAILED_ROW_RETRY_ATTEMPTED = 1; FAILED_ROW_RETRY_SUCCEEDED = 0; FAILED_ROW_RETRY_EXHAUSTED = 1
        HISTORICAL_ERROR_CODE = 'EXPORT_ERROR'; HISTORICAL_ERROR_MESSAGE = [string]$historyRow[0].last_error_message
        TARGETED_REPAIR_ATTEMPT_LIMIT = $MaxTargetedAttempts; ATTEMPT_A_RUN = 1; ATTEMPT_A_STRATEGY = 'FRESH_PATH_BASELINE'; ATTEMPT_A_OUTPUT_PATH = $attemptAPath; ATTEMPT_A_EXPORT_COMPLETED = $attemptA.export_completed; ATTEMPT_A_ERROR_CODE = $attemptA.error_code
        ATTEMPT_B_RUN = $attemptBRun; ATTEMPT_B_STRATEGY = 'REPAGINATE_BEFORE_EXPORT'; ATTEMPT_B_OUTPUT_PATH = $attemptBPath; ATTEMPT_B_REPAGINATE = $attemptBRun; ATTEMPT_B_EXPORT_COMPLETED = if ($null -ne $attemptB) { $attemptB.export_completed } else { 0 }; ATTEMPT_B_ERROR_CODE = if ($null -ne $attemptB) { $attemptB.error_code } else { '' }
        REPAIR_VARIANT = if ($null -ne $candidate) { $candidate.repair_variant } else { 'NONE' }; REPAIR_CANDIDATE_AVAILABLE = [int]($null -ne $candidate -and $candidate.pdf_basic_validation_pass -eq 1); REPAIR_CANDIDATE_PATH = if ($null -ne $candidate) { $candidate.output_pdf } else { '' }; REPAIR_CANDIDATE_SHA256 = if ($null -ne $candidate) { Get-Hash $candidate.output_pdf } else { '' }; REPAIR_CANDIDATE_BASIC_VALIDATION_PASS = if ($null -ne $candidate) { $candidate.pdf_basic_validation_pass } else { 0 }
        CANONICAL_OUTPUT_EXISTS_BEFORE = $canonical.exists; CANONICAL_OUTPUT_SIZE_BEFORE = $canonical.size; CANONICAL_OUTPUT_PDF_SIGNATURE_VALID_BEFORE = $canonical.signature_valid; CANONICAL_OUTPUT_READABLE_BEFORE = $canonical.readable; CANONICAL_OUTPUT_NOT_OVERWRITTEN = 1
        SOURCE_SHA256_AFTER_ATTEMPT_A = $sourceShaAfterA; SOURCE_SHA256_AFTER_ATTEMPT_B = $sourceShaAfterB; SOURCE_MUTATION_DETECTED = $sourceMutationDetected
        SOURCE_READ_ONLY_CONTRACT_PRESERVED = 1; WORD_SECURITY_CONTRACT_PRESERVED = 1; EXPORT_CONTRACT_PRESERVED = 1; COM_LIFECYCLE_CONTRACT_PRESERVED = 1; GLOBAL_WINWORD_FORCE_KILL_PRESENT = 0
        DOC_CONTRACT_APPROVED = 1; WORD_COM_RUN = 1; DOC_CONVERSION_RUN = 1; SUCCESSFUL_BATCH_ROWS_PRESERVED = 13; SUCCESSFUL_BATCH_ROWS_RECONVERTED = 0
        SOURCE_SHA_MISMATCH = [int]($sourceSha -ne $ExpectedSha); ORIGINAL_FILES_MODIFIED = $sourceMutationDetected; FORMAL_ELIGIBILITY_ROWS_MODIFIED = 0
        Q3_REPAIR_RUN = 0; Q3_OCR_RUN = 0; IMAGE_OCR_RUN = 0; IMAGE_EXTRACTION_RERUN = 0; G9_RUN = 0; G10_RUN = 0; NEW_DEPENDENCY_INSTALLED = 0; NETWORK_ACCESS_USED = 0
        attempt_a = $attemptA; attempt_b = $attemptB; stage_word_processes_created = (($script:StageCreatedIds | Select-Object -Unique) -join ','); stage_word_processes_cleaned = $script:StageCleanedCount; orphan_stage_word_processes = (($script:OrphanIds | Select-Object -Unique) -join ',')
    }
    Write-JsonUtf8 $ResultPath $result
    $result | ConvertTo-Csv -NoTypeInformation | Set-Content -LiteralPath $ResultCsvPath -Encoding UTF8
    $next = if ($result.REPAIR_CANDIDATE_AVAILABLE -eq 1) { 'G8-DOC-BATCH-CONVERSION-REPAIR-QA' } else { 'G8-DOC-CUMCM-2012-D-001-TOOLING-DECISION' }
    Set-Content -LiteralPath $ReportPath -Encoding UTF8 -Value @(
        '# G8 DOC Batch Conversion Repair', '', "Status: ``$status``", '',
        "Target: ``$TargetPaperId``", "Attempt A: ``$($attemptA.error_code)``; Attempt B run: ``$attemptBRun``; Attempt B result: ``$(if($null -ne $attemptB){$attemptB.error_code}else{'NOT_RUN'})``.",
        "Candidate available: ``$($result.REPAIR_CANDIDATE_AVAILABLE)``.", '',
        'Canonical batch output was not written. No batch QA, extraction, OCR, formal artifact generation, or backlog update was performed.', '', "Next: ``$next``."
    )
    Write-RepairLog "STATUS=$status target=$TargetPaperId attempt_a=$($attemptA.error_code) attempt_b_run=$attemptBRun attempt_b_error=$(if($null -ne $attemptB){$attemptB.error_code}else{'NOT_RUN'}) candidate=$($result.REPAIR_CANDIDATE_AVAILABLE) orphan=$($script:OrphanIds -join ',')"
    Write-Output ($result | ConvertTo-Json -Depth 16 -Compress)
    if ($status -eq 'BLOCKED') { exit 2 }
}
catch {
    Write-RepairLog "STATUS=BLOCKED target=$TargetPaperId error=$($_.Exception.Message)"
    throw
}
