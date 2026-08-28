[CmdletBinding()]
param(
    [switch]$PreflightOnly
)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Catalog = Join-Path $Root 'catalog\scale'
$LogDir = Join-Path $Root 'logs\scale'
$ManifestPath = Join-Path $Catalog 'g8_doc_batch_conversion_manifest.csv'
$TargetPath = Join-Path $Catalog 'g8_doc_batch_target_inventory.csv'
$ContractPath = Join-Path $Catalog 'g8_doc_extraction_contract_v1.json'
$ResultsPath = Join-Path $Catalog 'g8_doc_batch_word_results.json'
$ResultsCsvPath = Join-Path $Catalog 'g8_doc_batch_word_results.csv'
$RunnerLog = Join-Path $LogDir 'g8_doc_batch_extraction.log'
$DerivativeRoot = Join-Path $Root 'derived\scale\doc_batch'
$StageName = 'G8-DOC-BATCH-EXTRACTION'
$MaxConversionAttempts = 2
$PilotPdfSha = @{
    'CUMCM-2011-C-002' = '064CD08E45796A9ADB27BAD2DFB5CFB457DCE57FD8ACFEAF5B1C3E3B1C51F7CB'
    'CUMCM-2013-D-001' = '3C560062FFD7F9F4E855926AD051346D4FC2366C0052D80159836E1A007812A4'
    'CUMCM-2014-D-003' = '00C0D4361A59E3D5F1E97FBE7DAF28B60FCDDA9C26EBF435182C9F6961EB360C'
}
$script:StageCreatedIds = @()
$script:StageCleanedCount = 0
$script:OrphanIds = @()
$script:WordComInstanceCreated = 0

New-Item -ItemType Directory -Force -Path $Catalog, $LogDir, $DerivativeRoot | Out-Null

function Read-CsvUtf8([string]$Path) {
    return @(Get-Content -LiteralPath $Path -Encoding UTF8 | ConvertFrom-Csv)
}

function Read-JsonUtf8([string]$Path) {
    return (Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json)
}

function Write-JsonUtf8([string]$Path, [object]$Value) {
    $temporary = "$Path.tmp"
    ($Value | ConvertTo-Json -Depth 12) | Set-Content -LiteralPath $temporary -Encoding UTF8
    Move-Item -LiteralPath $temporary -Destination $Path -Force
}

function Write-RunnerLog([string]$Message) {
    Add-Content -LiteralPath $RunnerLog -Value "$(Get-Date -Format o) $Message" -Encoding UTF8
}

function Get-Hash([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToUpperInvariant()
}

function ConvertTo-HexString {
    param([Parameter(Mandatory = $true)][byte[]]$Bytes)
    return ([BitConverter]::ToString($Bytes)).Replace('-', '')
}

function Get-OleHeaderHex([string]$Path) {
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

function Get-StageNewIds([int[]]$Before, [int[]]$After) {
    return @($After | Where-Object { $Before -notcontains $_ })
}

function Wait-ForStageProcessExit {
    param([int[]]$StageIds, [int]$TimeoutSeconds = 10, [int]$PollMilliseconds = 250)
    if ($null -eq $StageIds -or $StageIds.Count -eq 0) {
        return [pscustomobject]@{ exited = 1; remaining_ids = @() }
    }
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    do {
        $currentIds = Get-WordIds
        $remaining = @($currentIds | Where-Object { $StageIds -contains $_ })
        if ($remaining.Count -eq 0) { return [pscustomobject]@{ exited = 1; remaining_ids = @() } }
        $remainingMilliseconds = [int](($deadline - (Get-Date)).TotalMilliseconds)
        if ($remainingMilliseconds -le 0) { break }
        Start-Sleep -Milliseconds ([Math]::Min($PollMilliseconds, $remainingMilliseconds))
    } while ((Get-Date) -lt $deadline)
    $currentIds = Get-WordIds
    $remaining = @($currentIds | Where-Object { $StageIds -contains $_ })
    return [pscustomobject]@{ exited = [int]($remaining.Count -eq 0); remaining_ids = $remaining }
}

function Wait-ForWordBackgroundDrain {
    param([Parameter(Mandatory = $true)][object]$Word, [int]$TimeoutSeconds = 10, [int]$PollMilliseconds = 250)
    $started = Get-Date
    $saving = 0; $printing = 0
    try {
        $saving = [int]$Word.BackgroundSavingStatus
        $printing = [int]$Word.BackgroundPrintingStatus
    }
    catch { return [pscustomobject]@{ completed = 1; wait_ms = 0; error_message = $_.Exception.Message } }
    if ($saving -eq 0 -and $printing -eq 0) { return [pscustomobject]@{ completed = 1; wait_ms = 0; error_message = '' } }
    $deadline = $started.AddSeconds($TimeoutSeconds)
    do {
        $remainingMilliseconds = [int](($deadline - (Get-Date)).TotalMilliseconds)
        if ($remainingMilliseconds -le 0) { break }
        Start-Sleep -Milliseconds ([Math]::Min($PollMilliseconds, $remainingMilliseconds))
        try {
            $saving = [int]$Word.BackgroundSavingStatus
            $printing = [int]$Word.BackgroundPrintingStatus
        }
        catch { return [pscustomobject]@{ completed = 1; wait_ms = [int]((Get-Date) - $started).TotalMilliseconds; error_message = $_.Exception.Message } }
        if ($saving -eq 0 -and $printing -eq 0) { break }
    } while ((Get-Date) -lt $deadline)
    return [pscustomobject]@{ completed = [int]($saving -eq 0 -and $printing -eq 0); wait_ms = [int]((Get-Date) - $started).TotalMilliseconds; error_message = '' }
}

function Set-ExceptionMessage([object]$State, [object]$ErrorRecord, [string]$Prefix) {
    if ($null -eq $ErrorRecord.Exception) { return }
    $State."${Prefix}_exception_type" = $ErrorRecord.Exception.GetType().FullName
    $State."${Prefix}_exception_message" = $ErrorRecord.Exception.Message
    try { $State."${Prefix}_hresult" = ('0x{0:X8}' -f ([int]$ErrorRecord.Exception.HResult)) } catch { }
}

function Set-ResultField([object]$Object, [string]$Name, [object]$Value) {
    if ($Object.PSObject.Properties.Name -contains $Name) {
        $Object.$Name = $Value
    }
    else {
        $Object | Add-Member -NotePropertyName $Name -NotePropertyValue $Value -Force
    }
}

function Invoke-WordPdfConversion([psobject]$Sample, [string]$OutputPdf) {
    $state = [ordered]@{
        paper_id = $Sample.paper_id; output_pdf = $OutputPdf; conversion_attempted = 0; conversion_completed = 0
        word_create_attempted = 0; word_created = 0; security_configured = 0; security_gate_pass = 0
        document_open_attempted = 0; document_opened = 0; export_attempted = 0; export_completed = 0
        document_close_attempted = 0; document_closed = 0; word_quit_attempted = 0; word_quit_called = 0
        com_references_released = 0; word_process_exited = 0; stage_word_pid = ''
        export_invocation_strategy = 'TWO_REQUIRED_ARGUMENTS'; export_argument_count = 2; export_format_value = 17
        background_drain_completed = 0; post_export_settle_ms = 500; post_export_settle_completed = 0
        primary_error_code = ''; primary_error_message = ''; cleanup_error_code = ''; cleanup_error_message = ''
        error_code = ''; error_message = ''
    }
    $word = $null; $documents = $null; $options = $null; $doc = $null
    $beforeIds = Get-WordIds; $newIds = @(); $allReleased = $true
    try {
        $state.word_create_attempted = 1
        $word = New-Object -ComObject Word.Application
        $state.word_created = 1; $script:WordComInstanceCreated = 1
        $newIds = Get-StageNewIds $beforeIds (Get-WordIds)
        $state.stage_word_pid = $newIds -join ','; $script:StageCreatedIds += $newIds

        $word.Visible = $false; $word.DisplayAlerts = 0; $word.AutomationSecurity = 3
        $options = $word.Options
        $options.UpdateLinksAtOpen = $false; $options.ConfirmConversions = $false; $options.SavePropertiesPrompt = $false
        if ($word.Visible -ne $false -or [int]$word.DisplayAlerts -ne 0 -or [int]$word.AutomationSecurity -ne 3 -or $options.UpdateLinksAtOpen -ne $false -or $options.ConfirmConversions -ne $false) { throw 'SECURITY_GATE_FAILED' }
        $state.security_configured = 1; $state.security_gate_pass = 1

        $documents = $word.Documents
        if ($null -eq $documents) { throw 'DOCUMENTS_COLLECTION_NULL' }
        $state.document_open_attempted = 1
        $doc = $documents.Open([string]$Sample.source_absolute, $false, $true, $false)
        if ($null -eq $doc -or $doc.ReadOnly -ne $true) { throw 'SOURCE_NOT_READONLY' }
        $state.document_opened = 1
        $outputFull = [System.IO.Path]::GetFullPath([string]$OutputPdf)
        $outputParent = Split-Path -Parent $outputFull
        $approvedRoot = ([System.IO.Path]::GetFullPath([string]$DerivativeRoot)).TrimEnd('\') + '\'
        if (-not $outputFull.StartsWith($approvedRoot, [System.StringComparison]::OrdinalIgnoreCase) -or [System.IO.Path]::GetExtension($outputFull) -ine '.pdf') { throw 'EXPORT_OUTPUT_PATH_INVALID' }
        New-Item -ItemType Directory -Force -Path $outputParent | Out-Null
        $state.export_attempted = 1; $state.conversion_attempted = 1
        [void]$doc.ExportAsFixedFormat([string]$outputFull, [int]17)
        if (-not [System.IO.File]::Exists($outputFull) -or (Get-Item -LiteralPath $outputFull).Length -le 0) { throw 'DERIVATIVE_NOT_CREATED' }
        $state.export_completed = 1; $state.conversion_completed = 1
        $drain = Wait-ForWordBackgroundDrain -Word $word
        $state.background_drain_completed = $drain.completed
        $state.background_drain_wait_ms = $drain.wait_ms
        Start-Sleep -Milliseconds 500; $state.post_export_settle_completed = 1
    }
    catch {
        $state.primary_error_message = $_.Exception.Message
        if ($state.word_create_attempted -eq 1 -and $state.word_created -eq 0) { $state.primary_error_code = 'WORD_CREATE_ERROR' }
        elseif ($state.word_created -eq 1 -and $state.security_configured -eq 0) { $state.primary_error_code = 'SECURITY_ERROR' }
        elseif ($state.document_open_attempted -eq 1 -and $state.document_opened -eq 0) { $state.primary_error_code = 'DOCUMENT_OPEN_ERROR' }
        elseif ($state.export_attempted -eq 1 -and $state.export_completed -eq 0) { $state.primary_error_code = 'EXPORT_ERROR' }
        else { $state.primary_error_code = 'CONVERSION_ERROR' }
    }
    finally {
        if ($doc) {
            $state.document_close_attempted = 1
            try { $doc.Close($false); $state.document_closed = 1 } catch { if ([string]::IsNullOrWhiteSpace($state.cleanup_error_code)) { $state.cleanup_error_code = 'DOCUMENT_CLOSE_ERROR'; $state.cleanup_error_message = $_.Exception.Message } }
            $released = Release-Com $doc; if (-not $released) { $allReleased = $false; if ([string]::IsNullOrWhiteSpace($state.cleanup_error_code)) { $state.cleanup_error_code = 'COM_RELEASE_ERROR'; $state.cleanup_error_message = 'Document COM reference release failed' } }; $doc = $null
        }
        if ($options) { $released = Release-Com $options; if (-not $released) { $allReleased = $false; if ([string]::IsNullOrWhiteSpace($state.cleanup_error_code)) { $state.cleanup_error_code = 'COM_RELEASE_ERROR'; $state.cleanup_error_message = 'Options COM reference release failed' } }; $options = $null }
        if ($documents) { $released = Release-Com $documents; if (-not $released) { $allReleased = $false; if ([string]::IsNullOrWhiteSpace($state.cleanup_error_code)) { $state.cleanup_error_code = 'COM_RELEASE_ERROR'; $state.cleanup_error_message = 'Documents COM reference release failed' } }; $documents = $null }
        if ($word) {
            $state.word_quit_attempted = 1
            try { $word.Quit(); $state.word_quit_called = 1 } catch { Set-ExceptionMessage $state $_ 'word_quit'; if ([string]::IsNullOrWhiteSpace($state.cleanup_error_code)) { $state.cleanup_error_code = 'WORD_QUIT_ERROR'; $state.cleanup_error_message = $_.Exception.Message } }
            $released = Release-Com $word; if (-not $released) { $allReleased = $false; if ([string]::IsNullOrWhiteSpace($state.cleanup_error_code)) { $state.cleanup_error_code = 'COM_RELEASE_ERROR'; $state.cleanup_error_message = 'Word COM reference release failed' } }; $word = $null
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
    if (-not (Test-Path -LiteralPath $ContractPath) -or -not (Test-Path -LiteralPath $ManifestPath) -or -not (Test-Path -LiteralPath $TargetPath)) { throw 'BATCH_INPUT_MANIFEST_MISSING' }
    $contract = Read-JsonUtf8 $ContractPath
    if ([int]$contract.approved -ne 1) { throw 'DOC_CONTRACT_NOT_APPROVED' }
    $manifest = @(Read-CsvUtf8 $ManifestPath)
    $targets = @(Read-CsvUtf8 $TargetPath)
    if ($manifest.Count -ne 17 -or $targets.Count -ne 17) { throw 'DOC_BATCH_TARGET_COUNT_NOT_17' }
    $duplicateIds = @($manifest | Group-Object paper_id | Where-Object Count -gt 1)
    if ($duplicateIds.Count -gt 0) { throw 'DOC_BATCH_DUPLICATE_PAPER_IDS' }
    $eligibility = @(Read-CsvUtf8 (Join-Path $Catalog 'g8_artifact_eligibility.csv'))
    $artifactManifest = @(Read-CsvUtf8 (Join-Path $Catalog 'g8_artifact_manifest.csv'))
    $artifactIds = @($artifactManifest | Select-Object -ExpandProperty paper_id -Unique)
    $targetRows = @()
    $preflightFailure = $false
    foreach ($row in $manifest) {
        $sourceAbsolute = Join-Path $Root ($row.source_path -replace '/', '\')
        $exists = Test-Path -LiteralPath $sourceAbsolute -PathType Leaf
        $actualSha = if ($exists) { Get-Hash $sourceAbsolute } else { '' }
        $actualSize = if ($exists) { [int64](Get-Item -LiteralPath $sourceAbsolute).Length } else { [int64]0 }
        $actualOle = if ($exists) { Get-OleHeaderHex $sourceAbsolute } else { '' }
        $governance = $eligibility | Where-Object paper_id -eq $row.paper_id | Select-Object -First 1
        $eligibleOk = $null -ne $governance -and $governance.subject_type -eq 'PAPER' -and $governance.artifact_eligible -eq '1'
        $membershipOk = $null -ne $governance -and ([string]$governance.primary_file).Replace('\', '/') -eq ([string]$row.source_path).Replace('\', '/')
        $artifactAbsent = $artifactIds -notcontains $row.paper_id
        $valid = $exists -and $actualSha -eq ([string]$row.source_sha256).ToUpperInvariant() -and $actualSize -eq [int64]$row.source_size -and $actualOle -eq 'D0CF11E0A1B11AE1' -and $eligibleOk -and $membershipOk -and $artifactAbsent
        if (-not $valid) { $preflightFailure = $true }
        $targetRows += [pscustomobject]@{ paper_id=$row.paper_id; source_path=$row.source_path; source_absolute=$sourceAbsolute; source_sha256=$row.source_sha256; source_size=$row.source_size; source_exists=[int]$exists; source_sha256_actual=$actualSha; source_size_actual=$actualSize; source_ole_signature_actual=$actualOle; subject_type=if($governance){$governance.subject_type}else{''}; artifact_eligible=if($governance){$governance.artifact_eligible}else{''}; membership_match=[int]$membershipOk; artifact_absent=[int]$artifactAbsent; conversion_strategy=$row.conversion_strategy; output_pdf=$row.output_pdf; preflight_pass=[int]$valid }
        Write-RunnerLog "PREFLIGHT paper_id=$($row.paper_id) source_exists=$([int]$exists) source_sha_match=$([int]($actualSha -eq ([string]$row.source_sha256).ToUpperInvariant())) source_size_match=$([int]($actualSize -eq [int64]$row.source_size)) source_ole_match=$([int]($actualOle -eq 'D0CF11E0A1B11AE1')) eligibility_match=$([int]$eligibleOk) membership_match=$([int]$membershipOk) artifact_absent=$([int]$artifactAbsent)"
    }
    $pilotHashDrift = 0
    foreach ($pilot in @($manifest | Where-Object conversion_strategy -eq 'PILOT_REUSE')) {
        $pilotPdf = Join-Path $Root ($pilot.output_pdf -replace '/', '\')
        if (-not (Test-Path -LiteralPath $pilotPdf) -or (Get-Hash $pilotPdf) -ne $PilotPdfSha[[string]$pilot.paper_id]) { $pilotHashDrift++ }
    }
    if ($pilotHashDrift -gt 0) { $preflightFailure = $true }
    $pilotCount = @($manifest | Where-Object conversion_strategy -eq 'PILOT_REUSE').Count
    $wordRequired = @($manifest | Where-Object conversion_strategy -eq 'WORD_CONVERSION').Count
    $preflight = [ordered]@{ RUN_STATUS='PREFLIGHT_ONLY'; stage=$StageName; DOC_CONTRACT_APPROVED=1; DOC_BATCH_TARGET_ROWS=$manifest.Count; DOC_BATCH_UNIQUE_PAPER_IDS=@($manifest | Select-Object -ExpandProperty paper_id -Unique).Count; DOC_BATCH_DUPLICATE_PAPER_IDS=$duplicateIds.Count; DOC_BATCH_UNKNOWN_IDENTITIES=@($targetRows | Where-Object subject_type -ne 'PAPER').Count; DOC_BATCH_PILOT_REUSE_COUNT=$pilotCount; DOC_BATCH_PILOT_REUSE_HASH_DRIFT=$pilotHashDrift; DOC_BATCH_WORD_CONVERSION_REQUIRED=$wordRequired; DOC_SOURCE_MISSING=@($targetRows | Where-Object source_exists -ne 1).Count; DOC_SOURCE_SHA_MISMATCH=@($targetRows | Where-Object { $_.source_sha256_actual -ne $_.source_sha256.ToUpperInvariant() }).Count; DOC_SOURCE_FORMAT_DRIFT=@($targetRows | Where-Object source_ole_signature_actual -ne 'D0CF11E0A1B11AE1').Count; DOC_ELIGIBILITY_DRIFT=@($targetRows | Where-Object artifact_eligible -ne '1').Count; DOC_MEMBERSHIP_DRIFT=@($targetRows | Where-Object membership_match -ne 1).Count; WORD_COM_RUN=0; DOC_BATCH_RUN=0; DOC_CONVERSION_ATTEMPTED=0; targets=$targetRows }
    if ($PreflightOnly) { Write-Output ($preflight | ConvertTo-Json -Depth 8 -Compress); exit [int]$preflightFailure }
    if ($preflightFailure) { throw 'DOC_BATCH_PREFLIGHT_FAILED' }

    $prior = $null
    if (Test-Path -LiteralPath $ResultsPath) { $prior = Read-JsonUtf8 $ResultsPath }
    $priorById = @{}
    if ($null -ne $prior -and $prior.samples) { foreach ($item in @($prior.samples)) { $priorById[[string]$item.paper_id] = $item } }
    $results = @()
    $wordConversionRerun = 0
    $successfulConversionRerun = 0
    $failedRowRetryCompleted = 0
    foreach ($row in @($manifest | Where-Object conversion_strategy -eq 'WORD_CONVERSION')) {
        $target = $targetRows | Where-Object paper_id -eq $row.paper_id | Select-Object -First 1
        $existing = $priorById[[string]$row.paper_id]
        $output = Join-Path $Root ($row.output_pdf -replace '/', '\')
        $canSkip = $null -ne $existing -and [int]$existing.conversion_completed -eq 1 -and (Test-Path -LiteralPath $output) -and (Get-Hash $output) -eq ([string]$existing.effective_pdf_sha256).ToUpperInvariant() -and (Get-Hash $target.source_absolute) -eq ([string]$row.source_sha256).ToUpperInvariant()
        if ($canSkip) {
            Set-ResultField $existing 'conversion_origin' 'DOC_BATCH_WORD'
            $previousAttempts = 0
            try { $previousAttempts = [int]$existing.attempt_count } catch { $previousAttempts = 0 }
            if ($previousAttempts -lt 1) { $previousAttempts = 1 }
            Set-ResultField $existing 'attempt_count' $previousAttempts
            Set-ResultField $existing 'current_status' 'SUCCESS'
            Set-ResultField $existing 'last_attempt_status' 'SUCCESS'
            Set-ResultField $existing 'retry_allowed' 0
            Set-ResultField $existing 'successful_conversion_rerun' 0
            $results += $existing
            Write-RunnerLog "SKIP_COMPLETE paper_id=$($row.paper_id) SUCCESSFUL_CONVERSION_RERUN=0"
            continue
        }
        if ($null -ne $existing -and [int]$existing.conversion_completed -eq 1) {
            throw "COMPLETED_CONVERSION_OUTPUT_INTEGRITY_DRIFT=$($row.paper_id)"
        }
        $previousAttempts = 0
        if ($null -ne $existing) {
            try { $previousAttempts = [int]$existing.attempt_count } catch { $previousAttempts = 0 }
            if ($previousAttempts -eq 0 -and [int]$existing.conversion_attempted -eq 1) { $previousAttempts = 1 }
        }
        if ($null -ne $existing -and $previousAttempts -ge $MaxConversionAttempts -and [int]$existing.conversion_completed -ne 1) {
            Set-ResultField $existing 'current_status' 'FAILED'
            Set-ResultField $existing 'last_attempt_status' 'FAILED'
            Set-ResultField $existing 'retry_allowed' 0
            Set-ResultField $existing 'successful_conversion_rerun' 0
            Set-ResultField $existing 'conversion_origin' 'DOC_BATCH_WORD'
            $results += $existing
            Write-RunnerLog "SKIP_RETRY_LIMIT paper_id=$($row.paper_id) attempt_count=$previousAttempts FAILED_ROW_MAX_ATTEMPTS=$MaxConversionAttempts"
            continue
        }
        if ($script:OrphanIds.Count -gt 0) { throw "ORPHAN_STAGE_WORD_PROCESS=$($script:OrphanIds -join ',')" }
        $converted = Invoke-WordPdfConversion -Sample $target -OutputPdf $output
        $converted | Add-Member -NotePropertyName conversion_origin -NotePropertyValue 'DOC_BATCH_WORD' -Force
        $converted | Add-Member -NotePropertyName source_sha256 -NotePropertyValue $row.source_sha256 -Force
        $converted | Add-Member -NotePropertyName source_size -NotePropertyValue $row.source_size -Force
        $converted | Add-Member -NotePropertyName effective_pdf_sha256 -NotePropertyValue $(if($converted.conversion_completed -eq 1){Get-Hash $output}else{''}) -Force
        if ($converted.error_code -eq 'ORPHAN_STAGE_WORD_PROCESS' -or $script:OrphanIds.Count -gt 0) { throw "ORPHAN_STAGE_WORD_PROCESS=$($script:OrphanIds -join ',')" }
        $attemptCount = $previousAttempts + 1
        $converted | Add-Member -NotePropertyName attempt_count -NotePropertyValue $attemptCount -Force
        $converted | Add-Member -NotePropertyName last_attempt_status -NotePropertyValue $(if($converted.conversion_completed -eq 1){'SUCCESS'}else{'FAILED'}) -Force
        $converted | Add-Member -NotePropertyName current_status -NotePropertyValue $(if($converted.conversion_completed -eq 1){'SUCCESS'}else{'FAILED'}) -Force
        $converted | Add-Member -NotePropertyName retry_allowed -NotePropertyValue ([int]($converted.conversion_completed -ne 1 -and $attemptCount -lt $MaxConversionAttempts)) -Force
        $converted | Add-Member -NotePropertyName last_error_code -NotePropertyValue ([string]$converted.error_code) -Force
        $converted | Add-Member -NotePropertyName last_error_message -NotePropertyValue ([string]$converted.error_message) -Force
        $converted | Add-Member -NotePropertyName successful_conversion_rerun -NotePropertyValue 0 -Force
        $converted | Add-Member -NotePropertyName failed_row_retry_completed -NotePropertyValue ([int]($converted.conversion_completed -eq 1 -and $previousAttempts -gt 0)) -Force
        if ($previousAttempts -gt 0) { $wordConversionRerun++ }
        if ($converted.conversion_completed -eq 1 -and $previousAttempts -gt 0) { $failedRowRetryCompleted++ }
        $results += $converted
        if ($converted.conversion_completed -ne 1) {
            Write-RunnerLog "ROW_LOCAL_FAILURE_CONTINUES paper_id=$($row.paper_id) attempt_count=$attemptCount error_code=$($converted.error_code) retry_allowed=$($converted.retry_allowed)"
            continue
        }
    }
    $completed = @($results | Where-Object current_status -eq 'SUCCESS').Count
    $failed = @($results | Where-Object current_status -eq 'FAILED').Count
    $pending = $wordRequired - $completed - $failed
    $attempted = @($results | Where-Object conversion_attempted -eq 1).Count
    $runStatus = if ($completed -eq $wordRequired -and $failed -eq 0 -and $pending -eq 0 -and $script:OrphanIds.Count -eq 0) { 'COMPLETE' } else { 'PARTIAL' }
    $result = [ordered]@{ RUN_STATUS=$runStatus; stage=$StageName; DOC_CONTRACT_APPROVED=1; DOC_BATCH_TARGET_ROWS=17; DOC_BATCH_UNIQUE_PAPER_IDS=17; DOC_BATCH_DUPLICATE_PAPER_IDS=0; DOC_BATCH_PILOT_REUSE_COUNT=3; DOC_BATCH_WORD_CONVERSION_REQUIRED=$wordRequired; DOC_BATCH_WORD_CONVERSION_ATTEMPTED=$attempted; DOC_BATCH_WORD_CONVERSION_COMPLETED=$completed; DOC_BATCH_WORD_CONVERSION_FAILED=$failed; DOC_BATCH_WORD_CONVERSION_PENDING=$pending; WORD_CONVERSION_RERUN=$wordConversionRerun; SUCCESSFUL_CONVERSION_RERUN=$successfulConversionRerun; FAILED_ROW_RETRY_COMPLETED=$failedRowRetryCompleted; FAILED_ROW_MAX_ATTEMPTS=$MaxConversionAttempts; DOC_BATCH_RUN=1; DOC_FORMAL_ARTIFACT_GENERATION_RUN=0; DOC_BATCH_RUNNER_READY=1; BATCH_RESUMABLE=1; USER_ACTION_REQUIRED=[int]($runStatus -ne 'COMPLETE'); PRE_EXISTING_WORD_PROCESSES=''; DOC_BATCH_STAGE_WORD_PROCESSES_CREATED=(($script:StageCreatedIds | Select-Object -Unique) -join ','); DOC_BATCH_STAGE_WORD_PROCESSES_CLEANED=$script:StageCleanedCount; DOC_BATCH_ORPHAN_STAGE_WORD_PROCESSES=(($script:OrphanIds | Select-Object -Unique) -join ','); samples=$results }
    Write-JsonUtf8 $ResultsPath $result
    $results | Export-Csv -LiteralPath $ResultsCsvPath -NoTypeInformation -Encoding UTF8
    Write-RunnerLog "RUN_STATUS=$runStatus DOC_BATCH_WORD_CONVERSION_ATTEMPTED=$attempted DOC_BATCH_WORD_CONVERSION_COMPLETED=$completed DOC_BATCH_WORD_CONVERSION_FAILED=$failed DOC_BATCH_WORD_CONVERSION_PENDING=$pending SUCCESSFUL_CONVERSION_RERUN=$successfulConversionRerun DOC_BATCH_STAGE_WORD_PROCESSES_CLEANED=$($script:StageCleanedCount) ORPHAN=$($script:OrphanIds -join ',')"
    Write-Output ($result | ConvertTo-Json -Depth 12 -Compress)
    if ($runStatus -ne 'COMPLETE') { exit 1 }
}
catch {
    Write-RunnerLog "RUN_STATUS=BLOCKED error=$($_.Exception.Message)"
    throw
}
