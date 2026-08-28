[CmdletBinding()]
param(
    [switch]$PreflightOnly,
    [string]$ReplacementPaperId
)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Catalog = Join-Path $Root 'catalog\scale'
$LogDir = Join-Path $Root 'logs\scale'
$DerivativeRoot = Join-Path $Root 'derived\scale\doc_contract_pilot_interactive'
$TempRoot = Join-Path $Root 'tmp\g8_doc_interactive_word_pilot'
$ReplacementMode = -not [string]::IsNullOrWhiteSpace($ReplacementPaperId)
$ResultsPath = if ($ReplacementMode) { Join-Path $Catalog 'g8_doc_interactive_word_replacement_results.json' } else { Join-Path $Catalog 'g8_doc_interactive_word_results.json' }
$ConversionPath = if ($ReplacementMode) { Join-Path $Catalog 'g8_doc_interactive_word_replacement_results.csv' } else { Join-Path $Catalog 'g8_doc_interactive_word_conversion.csv' }
$RunnerLog = if ($ReplacementMode) { Join-Path $LogDir 'g8_doc_interactive_word_replacement.log' } else { Join-Path $LogDir 'g8_doc_interactive_word_pilot_runner.log' }

New-Item -ItemType Directory -Force -Path $Catalog, $LogDir | Out-Null

function Write-RunnerLog([string]$Message) {
    $line = "$(Get-Date -Format o) $Message"
    Add-Content -LiteralPath $RunnerLog -Value $line -Encoding UTF8
}

function Get-Hash([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToUpperInvariant()
}

function ConvertTo-HexString {
    param(
        [Parameter(Mandatory = $true)]
        [byte[]]$Bytes
    )

    return ([BitConverter]::ToString($Bytes)).Replace('-', '')
}

function Get-OleHeaderHex {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    $stream = [System.IO.File]::Open(
        $Path,
        [System.IO.FileMode]::Open,
        [System.IO.FileAccess]::Read,
        [System.IO.FileShare]::ReadWrite
    )

    try {
        $buffer = New-Object byte[] 8
        $read = $stream.Read($buffer, 0, 8)
        if ($read -ne 8) {
            return ''
        }
        return (ConvertTo-HexString -Bytes $buffer).ToUpperInvariant()
    }
    finally {
        $stream.Dispose()
    }
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
    catch {
        return $false
    }
}

function Get-StageNewIds([int[]]$Before, [int[]]$After) {
    return @($After | Where-Object { $Before -notcontains $_ })
}

function Wait-ForStageProcessExit {
    param(
        [int[]]$StageIds,
        [int]$TimeoutSeconds = 10,
        [int]$PollMilliseconds = 250
    )

    if ($null -eq $StageIds -or $StageIds.Count -eq 0) {
        return [pscustomobject]@{exited=1; remaining_ids=@()}
    }

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    do {
        $currentIds = Get-WordIds
        $remaining = @($currentIds | Where-Object { $StageIds -contains $_ })
        if ($remaining.Count -eq 0) {
            return [pscustomobject]@{exited=1; remaining_ids=@()}
        }
        $remainingMilliseconds = [int](($deadline - (Get-Date)).TotalMilliseconds)
        if ($remainingMilliseconds -le 0) { break }
        Start-Sleep -Milliseconds ([Math]::Min($PollMilliseconds, $remainingMilliseconds))
    } while ((Get-Date) -lt $deadline)

    $currentIds = Get-WordIds
    $remaining = @($currentIds | Where-Object { $StageIds -contains $_ })
    return [pscustomobject]@{exited=[int]($remaining.Count -eq 0); remaining_ids=$remaining}
}

function Resolve-PrimaryError([object]$State) {
    if (-not [string]::IsNullOrWhiteSpace([string]$State.primary_error_code)) {
        return
    }
    if ([int]$State.word_create_attempted -eq 1 -and [int]$State.word_created -eq 0) {
        $State.primary_error_code = 'WORD_CREATE_ERROR'
        return
    }
    if ([int]$State.word_created -eq 1 -and [int]$State.security_configured -eq 0) {
        $State.primary_error_code = 'SECURITY_ERROR'
        return
    }
    if ([int]$State.documents_collection_acquire_attempted -eq 1 -and [int]$State.documents_collection_acquired -eq 0) {
        $State.primary_error_code = 'DOCUMENT_OPEN_ERROR'
        return
    }
    if ([int]$State.document_open_attempted -eq 1 -and [int]$State.document_opened -eq 0) {
        $State.primary_error_code = 'DOCUMENT_OPEN_ERROR'
        return
    }
    if ([int]$State.export_attempted -eq 1 -and [int]$State.export_completed -eq 0) {
        $State.primary_error_code = 'EXPORT_ERROR'
        return
    }
    if ([int]$State.document_opened -eq 1 -and [int]$State.export_completed -eq 0) {
        $State.primary_error_code = 'EXPORT_ERROR'
        return
    }
}

function Set-ExceptionDiagnostics([object]$State, [object]$ErrorRecord, [string]$Prefix) {
    $exception = $ErrorRecord.Exception
    if ($null -eq $exception) { return }
    $State."${Prefix}_exception_type" = $exception.GetType().FullName
    $State."${Prefix}_exception_message" = $exception.Message
    try {
        $State."${Prefix}_hresult" = ('0x{0:X8}' -f ([int]$exception.HResult))
    }
    catch {
        $State."${Prefix}_hresult" = ''
    }
    if ($null -ne $exception.InnerException) {
        $State."${Prefix}_inner_exception_type" = $exception.InnerException.GetType().FullName
        $State."${Prefix}_inner_exception_message" = $exception.InnerException.Message
    }
}

function Wait-ForWordBackgroundDrain {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Word,
        [int]$TimeoutSeconds = 10,
        [int]$PollMilliseconds = 250
    )

    $startedAt = Get-Date
    $savingInitial = 0
    $printingInitial = 0
    $savingFinal = 0
    $printingFinal = 0
    try {
        $savingInitial = [int]$Word.BackgroundSavingStatus
        $printingInitial = [int]$Word.BackgroundPrintingStatus
        $savingFinal = $savingInitial
        $printingFinal = $printingInitial
    }
    catch {
        return [pscustomobject]@{
            status_available=0
            saving_initial=$savingInitial
            printing_initial=$printingInitial
            saving_final=$savingFinal
            printing_final=$printingFinal
            completed=1
            timed_out=0
            wait_ms=0
            error_type=$_.Exception.GetType().FullName
            error_message=$_.Exception.Message
        }
    }

    if ($savingInitial -eq 0 -and $printingInitial -eq 0) {
        return [pscustomobject]@{
            status_available=1
            saving_initial=$savingInitial
            printing_initial=$printingInitial
            saving_final=$savingFinal
            printing_final=$printingFinal
            completed=1
            timed_out=0
            wait_ms=0
            error_type=''
            error_message=''
        }
    }

    $deadline = $startedAt.AddSeconds($TimeoutSeconds)
    do {
        $remainingMilliseconds = [int](($deadline - (Get-Date)).TotalMilliseconds)
        if ($remainingMilliseconds -le 0) { break }
        Start-Sleep -Milliseconds ([Math]::Min($PollMilliseconds, $remainingMilliseconds))
        try {
            $savingFinal = [int]$Word.BackgroundSavingStatus
            $printingFinal = [int]$Word.BackgroundPrintingStatus
        }
        catch {
            return [pscustomobject]@{
                status_available=0
                saving_initial=$savingInitial
                printing_initial=$printingInitial
                saving_final=$savingFinal
                printing_final=$printingFinal
                completed=1
                timed_out=0
                wait_ms=[int]((Get-Date) - $startedAt).TotalMilliseconds
                error_type=$_.Exception.GetType().FullName
                error_message=$_.Exception.Message
            }
        }
        if ($savingFinal -eq 0 -and $printingFinal -eq 0) { break }
    } while ((Get-Date) -lt $deadline)

    $waitMs = [int]((Get-Date) - $startedAt).TotalMilliseconds
    $drained = $savingFinal -eq 0 -and $printingFinal -eq 0
    return [pscustomobject]@{
        status_available=1
        saving_initial=$savingInitial
        printing_initial=$printingInitial
        saving_final=$savingFinal
        printing_final=$printingFinal
        completed=[int]$drained
        timed_out=[int](-not $drained)
        wait_ms=$waitMs
        error_type=''
        error_message=''
    }
}

function Invoke-WordPdfConversion([psobject]$Sample, [string]$OutputPdf, [string]$AttemptLabel) {
    $state = [ordered]@{
        attempt=$AttemptLabel
        output_pdf=$OutputPdf
        conversion_attempted=0
        conversion_completed=0
        word_create_attempted=0
        word_created=0
        security_configuration_attempted=0
        security_configured=0
        security_verified=0
        security_gate_pass=0
        documents_collection_acquire_attempted=0
        documents_collection_acquired=0
        document_open_attempted=0
        document_open_returned_object=0
        document_opened=0
        document_open_exception_type=''
        document_open_exception_message=''
        document_open_hresult=''
        document_open_inner_exception_type=''
        document_open_inner_exception_message=''
        export_invocation_strategy='TWO_REQUIRED_ARGUMENTS'
        export_argument_count=2
        export_output_path=$OutputPdf
        export_output_full_path=''
        export_output_parent=''
        export_output_parent_exists=0
        export_output_extension=''
        export_output_path_length=0
        export_output_file_exists_before=0
        export_output_absolute=0
        export_output_parent_governed=0
        export_output_source_directory_match=0
        export_output_path_type='System.String'
        export_format_value=17
        export_exception_type=''
        export_exception_message=''
        export_hresult_hex=''
        export_hresult_decimal=''
        export_inner_exception_type=''
        export_inner_exception_message=''
        export_attempted=0
        export_completed=0
        stage_word_pid=''
        background_drain_check_implemented=1
        background_drain_status_available=0
        background_saving_status_initial=0
        background_printing_status_initial=0
        background_saving_status_final=0
        background_printing_status_final=0
        background_drain_completed=0
        background_drain_wait_ms=0
        background_drain_error_type=''
        background_drain_error_message=''
        post_export_settle_implemented=1
        post_export_settle_ms=500
        post_export_settle_completed=0
        document_com_release_attempted=0
        document_com_release_completed=0
        documents_com_release_attempted=0
        documents_com_release_completed=0
        options_com_release_attempted=0
        options_com_release_completed=0
        word_com_release_attempted=0
        word_com_release_completed=0
        document_close_attempted=0
        document_closed=0
        word_quit_attempted=0
        word_quit_called=0
        com_references_released=0
        word_process_exited=0
        primary_error_code=''
        primary_error_message=''
        cleanup_error_code=''
        cleanup_error_message=''
        word_quit_exception_type=''
        word_quit_exception_message=''
        word_quit_hresult=''
        word_quit_inner_exception_type=''
        word_quit_inner_exception_message=''
        error_code=''
        error_message=''
    }
    $word = $null
    $documents = $null
    $options = $null
    $doc = $null
    $beforeIds = Get-WordIds
    $newIds = @()
    $allComReleasesCompleted = $true
    try {
        $state.word_create_attempted = 1
        $word = New-Object -ComObject Word.Application
        $state.word_created = 1
        $script:WordComInstanceCreated = 1
        $afterStartIds = Get-WordIds
        $newIds = Get-StageNewIds $beforeIds $afterStartIds
        $state.stage_word_pid = ($newIds -join ',')
        $script:StageCreatedIds += $newIds

        # Office msoAutomationSecurityForceDisable = 3; never use Low.
        $state.security_configuration_attempted = 1
        $word.Visible = $false
        $word.DisplayAlerts = 0
        $word.AutomationSecurity = 3
        $options = $word.Options
        $options.UpdateLinksAtOpen = $false
        $options.ConfirmConversions = $false
        $options.SavePropertiesPrompt = $false

        $securityPass = ($word.Visible -eq $false) -and ([int]$word.DisplayAlerts -eq 0) -and ([int]$word.AutomationSecurity -eq 3) -and ($options.UpdateLinksAtOpen -eq $false) -and ($options.ConfirmConversions -eq $false)
        if (-not $securityPass) { throw 'SECURITY_GATE_FAILED' }
        $state.security_configured = 1
        $state.security_verified = 1
        $state.security_gate_pass = 1

        $source = [string]$Sample.source_absolute
        # Use the stable four-argument late-bound call. The positional contract is:
        # FileName, ConfirmConversions=false, ReadOnly=true, AddToRecentFiles=false.
        # Remaining optional arguments, including OpenAndRepair, use Word defaults;
        # OpenAndRepair is therefore not enabled and no null/ref placeholders are passed.
        $state.documents_collection_acquire_attempted = 1
        try {
            $documents = $word.Documents
            if ($null -eq $documents) { throw 'DOCUMENTS_COLLECTION_NULL' }
            $state.documents_collection_acquired = 1
        }
        catch {
            Set-ExceptionDiagnostics $state $_ 'document_open'
            throw
        }
        $state.document_open_attempted = 1
        try {
            $doc = $documents.Open($source, $false, $true, $false)
        }
        catch {
            Set-ExceptionDiagnostics $state $_ 'document_open'
            throw
        }
        if ($null -eq $doc) { throw 'READONLY_OPEN_FAILED' }
        $state.document_open_returned_object = 1
        if (-not $doc.ReadOnly) { throw 'SOURCE_NOT_READONLY' }
        $state.document_opened = 1
        $outputPdfFull = [System.IO.Path]::GetFullPath([string]$OutputPdf)
        $state.output_pdf = $outputPdfFull
        $state.export_output_full_path = $outputPdfFull
        $state.export_output_parent = Split-Path -Parent $outputPdfFull
        $state.export_output_extension = [System.IO.Path]::GetExtension($outputPdfFull)
        $state.export_output_path_length = $outputPdfFull.Length
        $state.export_output_absolute = [int][System.IO.Path]::IsPathRooted($outputPdfFull)
        $state.export_output_file_exists_before = [int][System.IO.File]::Exists($outputPdfFull)
        $sourceFull = [System.IO.Path]::GetFullPath([string]$Sample.source_absolute)
        $sourceDirectory = (Split-Path -Parent $sourceFull).TrimEnd('\') + '\'
        $state.export_output_source_directory_match = [int]($outputPdfFull.StartsWith($sourceDirectory, [System.StringComparison]::OrdinalIgnoreCase) -or $outputPdfFull.Equals($sourceFull, [System.StringComparison]::OrdinalIgnoreCase))
        $approvedOutputRoots = @($DerivativeRoot, $TempRoot)
        $outputParentGoverned = $false
        foreach ($approvedRoot in $approvedOutputRoots) {
            $approvedRootFull = ([System.IO.Path]::GetFullPath([string]$approvedRoot)).TrimEnd('\') + '\'
            if ($outputPdfFull.StartsWith($approvedRootFull, [System.StringComparison]::OrdinalIgnoreCase)) {
                $outputParentGoverned = $true
                break
            }
        }
        $state.export_output_parent_governed = [int]$outputParentGoverned
        $invalidFileNameCharacters = [System.IO.Path]::GetInvalidFileNameChars()
        $outputFileName = [System.IO.Path]::GetFileName($outputPdfFull)
        $hasInvalidFileNameCharacter = $false
        foreach ($invalidCharacter in $invalidFileNameCharacters) {
            if ($outputFileName.IndexOf($invalidCharacter) -ge 0) {
                $hasInvalidFileNameCharacter = $true
                break
            }
        }
        if (-not $state.export_output_absolute -or $state.export_output_extension -ine '.pdf' -or -not $outputParentGoverned -or $state.export_output_source_directory_match -eq 1 -or $hasInvalidFileNameCharacter) {
            throw 'EXPORT_OUTPUT_PATH_INVALID'
        }
        if (-not (Test-Path -LiteralPath $state.export_output_parent -PathType Container)) {
            New-Item -ItemType Directory -Force -Path $state.export_output_parent | Out-Null
        }
        $state.export_output_parent_exists = [int](Test-Path -LiteralPath $state.export_output_parent -PathType Container)
        if ($state.export_output_parent_exists -ne 1) { throw 'EXPORT_OUTPUT_PARENT_NOT_CREATED' }
        # wdExportFormatPDF=17. Use only OutputFileName and ExportFormat;
        # all optional arguments are omitted for stable late-bound Word COM invocation.
        $state.export_attempted = 1
        $state.conversion_attempted = 1
        try {
            [void]$doc.ExportAsFixedFormat([string]$outputPdfFull, [int]$state.export_format_value)
        }
        catch {
            Set-ExceptionDiagnostics $state $_ 'export'
            $state.export_hresult_hex = $state.export_hresult
            try { $state.export_hresult_decimal = [int]$_.Exception.HResult } catch { $state.export_hresult_decimal = '' }
            throw
        }
        if (-not [System.IO.File]::Exists($outputPdfFull)) { throw 'DERIVATIVE_NOT_CREATED' }
        if ((Get-Item -LiteralPath $outputPdfFull).Length -le 0) { throw 'DERIVATIVE_EMPTY' }
        $state.export_completed = 1
        $state.conversion_completed = 1
        $backgroundResult = Wait-ForWordBackgroundDrain -Word $word -TimeoutSeconds 10 -PollMilliseconds 250
        $state.background_drain_status_available = $backgroundResult.status_available
        $state.background_saving_status_initial = $backgroundResult.saving_initial
        $state.background_printing_status_initial = $backgroundResult.printing_initial
        $state.background_saving_status_final = $backgroundResult.saving_final
        $state.background_printing_status_final = $backgroundResult.printing_final
        $state.background_drain_completed = $backgroundResult.completed
        $state.background_drain_wait_ms = $backgroundResult.wait_ms
        $state.background_drain_error_type = $backgroundResult.error_type
        $state.background_drain_error_message = $backgroundResult.error_message
        try {
            Start-Sleep -Milliseconds 500
            $state.post_export_settle_completed = 1
        }
        catch {
            $state.post_export_settle_completed = 0
        }
    }
    catch {
        $state.primary_error_message = $_.Exception.Message
        Resolve-PrimaryError $state
    }
    finally {
        if ($doc) {
            $state.document_close_attempted = 1
            try {
                $doc.Close($false)
                $state.document_closed = 1
            }
            catch {
                if ([string]::IsNullOrWhiteSpace($state.cleanup_error_code)) {
                    $state.cleanup_error_code = 'DOCUMENT_CLOSE_ERROR'
                    $state.cleanup_error_message = $_.Exception.Message
                }
            }
            $state.document_com_release_attempted = 1
            $documentReleaseCompleted = Release-Com $doc
            $state.document_com_release_completed = [int]$documentReleaseCompleted
            if (-not $documentReleaseCompleted) {
                $allComReleasesCompleted = $false
                if ([string]::IsNullOrWhiteSpace($state.cleanup_error_code)) {
                    $state.cleanup_error_code = 'COM_RELEASE_ERROR'
                    $state.cleanup_error_message = 'Document COM reference release failed'
                }
            }
            $doc = $null
        }
        if ($options) {
            $state.options_com_release_attempted = 1
            $optionsReleaseCompleted = Release-Com $options
            $state.options_com_release_completed = [int]$optionsReleaseCompleted
            if (-not $optionsReleaseCompleted) {
                $allComReleasesCompleted = $false
                if ([string]::IsNullOrWhiteSpace($state.cleanup_error_code)) {
                    $state.cleanup_error_code = 'COM_RELEASE_ERROR'
                    $state.cleanup_error_message = 'Word Options COM reference release failed'
                }
            }
            $options = $null
        }
        if ($documents) {
            $state.documents_com_release_attempted = 1
            $documentsReleaseCompleted = Release-Com $documents
            $state.documents_com_release_completed = [int]$documentsReleaseCompleted
            if (-not $documentsReleaseCompleted) {
                $allComReleasesCompleted = $false
                if ([string]::IsNullOrWhiteSpace($state.cleanup_error_code)) {
                    $state.cleanup_error_code = 'COM_RELEASE_ERROR'
                    $state.cleanup_error_message = 'Documents COM reference release failed'
                }
            }
            $documents = $null
        }
        if ($word) {
            $state.word_quit_attempted = 1
            try {
                $word.Quit()
                $state.word_quit_called = 1
            }
            catch {
                Set-ExceptionDiagnostics $state $_ 'word_quit'
                if ([string]::IsNullOrWhiteSpace($state.cleanup_error_code)) {
                    $state.cleanup_error_code = 'WORD_QUIT_ERROR'
                    $state.cleanup_error_message = $_.Exception.Message
                }
            }
            $state.word_com_release_attempted = 1
            $wordReleaseCompleted = Release-Com $word
            $state.word_com_release_completed = [int]$wordReleaseCompleted
            if (-not $wordReleaseCompleted) {
                $allComReleasesCompleted = $false
                if ([string]::IsNullOrWhiteSpace($state.cleanup_error_code)) {
                    $state.cleanup_error_code = 'COM_RELEASE_ERROR'
                    $state.cleanup_error_message = 'Word Application COM reference release failed'
                }
            }
            $word = $null
        }
        $state.com_references_released = [int]$allComReleasesCompleted
        [GC]::Collect(); [GC]::WaitForPendingFinalizers(); [GC]::Collect(); [GC]::WaitForPendingFinalizers()
        $exitResult = Wait-ForStageProcessExit -StageIds $newIds -TimeoutSeconds 10 -PollMilliseconds 250
        $state.word_process_exited = $exitResult.exited
        if ($exitResult.exited -eq 1) {
            if ($newIds.Count -gt 0) { $script:StageCleanedCount += $newIds.Count }
        }
        else {
            foreach ($id in $exitResult.remaining_ids) { $script:OrphanIds += $id }
            if ([string]::IsNullOrWhiteSpace($state.cleanup_error_code)) {
                $state.cleanup_error_code = 'ORPHAN_STAGE_WORD_PROCESS'
                $state.cleanup_error_message = ($exitResult.remaining_ids -join ',')
            }
        }
    }
    if ([string]::IsNullOrWhiteSpace($state.primary_error_code)) { Resolve-PrimaryError $state }
    if (-not [string]::IsNullOrWhiteSpace($state.primary_error_code)) {
        $state.error_code = $state.primary_error_code
        $state.error_message = $state.primary_error_message
    }
    elseif (-not [string]::IsNullOrWhiteSpace($state.cleanup_error_code)) {
        $state.error_code = $state.cleanup_error_code
        $state.error_message = $state.cleanup_error_message
    }
    return [pscustomobject]$state
}

try {
    $runStartStage = if ($ReplacementMode) { 'RUN_START stage=G8-DOC-INTERACTIVE-WORD-PILOT-REPLACEMENT' } else { 'RUN_START stage=G8-DOC-INTERACTIVE-WORD-PILOT' }
    Write-RunnerLog $runStartStage
    if (Test-Path -LiteralPath $ResultsPath) {
        $existing = Get-Content -LiteralPath $ResultsPath -Raw | ConvertFrom-Json
        if ([string]$existing.RUN_STATUS -eq 'COMPLETE') {
            Write-RunnerLog 'EXISTING_COMPLETE_RESULTS=1; no conversion rerun'
            Write-Output ($existing | ConvertTo-Json -Depth 8 -Compress)
            exit 0
        }
    }

    $inventory = @(Import-Csv -LiteralPath (Join-Path $Catalog 'g8_doc_contract_target_inventory.csv'))
    $expected = @{}
    if ($ReplacementMode) {
        if ($ReplacementPaperId -ne 'CUMCM-2014-D-003') { throw 'REPLACEMENT_PAPER_ID_NOT_FROZEN' }
        $replacementSelectionPath = Join-Path $Catalog 'g8_doc_interactive_replacement_selection.csv'
        $replacementSelection = @(Import-Csv -LiteralPath $replacementSelectionPath | Where-Object paper_id -eq $ReplacementPaperId | Select-Object -First 1)
        if ($replacementSelection.Count -ne 1) { throw 'REPLACEMENT_SELECTION_NOT_FOUND' }
        $replacementEligibility = @(Import-Csv -LiteralPath (Join-Path $Catalog 'g8_artifact_eligibility.csv') | Where-Object paper_id -eq $ReplacementPaperId | Select-Object -First 1)
        if ($replacementEligibility.Count -ne 1 -or $replacementEligibility[0].subject_type -ne 'PAPER' -or $replacementEligibility[0].artifact_eligible -ne '1') { throw 'REPLACEMENT_ELIGIBILITY_INVALID' }
        $inventory = @($inventory | Where-Object paper_id -eq $ReplacementPaperId)
        if ($inventory.Count -ne 1 -or $replacementSelection.source_path -ne $inventory[0].source_path -or $replacementSelection.source_sha256.Trim().ToUpperInvariant() -ne $inventory[0].source_sha256.Trim().ToUpperInvariant() -or [int64]$replacementSelection.source_size -ne [int64]$inventory[0].source_size -or $replacementSelection.selection_role -ne 'SMALL') { throw 'REPLACEMENT_SELECTION_BINDING_FAILED' }
        $samples = @([pscustomobject]@{paper_id=$replacementSelection.paper_id; source_path=$replacementSelection.source_path; source_sha256=$replacementSelection.source_sha256; source_size=$replacementSelection.source_size; sample_role='SMALL_SIZE'})
        $expected[$ReplacementPaperId] = @{sha=$replacementSelection.source_sha256.Trim().ToUpperInvariant(); size=[int64]$replacementSelection.source_size; role='SMALL_SIZE'}
    }
    else {
        $samples = @(Import-Csv -LiteralPath (Join-Path $Catalog 'g8_doc_contract_samples.csv'))
        $expected = @{
            'CUMCM-2014-A-006' = @{sha='A4C7CFEE735094C488EFB5007EF2084771748487B29765E20C39E78296A915F6'; size=24064; role='SMALL_SIZE'}
            'CUMCM-2011-C-002' = @{sha='21E5912D27E48F0BBEB0E1044BF30F185FBAB2133945529F106449296C10653F'; size=1113600; role='MEDIAN_SIZE'}
            'CUMCM-2013-D-001' = @{sha='955CC7179247EDA8AD6EBB74CFD1233D514D9F80A809B0C2EB244BEACABAFDEA'; size=3814912; role='LARGE_SIZE'}
        }
    }
    $targetIds = @($inventory | Select-Object -ExpandProperty paper_id -Unique)
    $sampleIds = @($samples | Select-Object -ExpandProperty paper_id)
    $preExistingIds = Get-WordIds
    $script:StageCreatedIds = @()
    $script:OrphanIds = @()
    $script:StageCleanedCount = 0
    $script:WordComInstanceCreated = 0
    $sourceRows = @()
    $sourceFailure = $false
    $sampleMappingFailure = $false

    foreach ($sample in $samples) {
        $sourceAbsolute = Join-Path $Root ($sample.source_path -replace '/', '\')
        $sample | Add-Member -NotePropertyName source_absolute -NotePropertyValue $sourceAbsolute -Force
        $inventoryRow = $inventory | Where-Object paper_id -eq $sample.paper_id | Select-Object -First 1
        $expectedRow = $expected[[string]$sample.paper_id]
        $expectedSha = if ($inventoryRow) { ([string]$inventoryRow.source_sha256).Trim().ToUpperInvariant() } else { '' }
        $expectedSize = if ($inventoryRow) { [int64]::Parse(([string]$inventoryRow.source_size).Trim(), [Globalization.CultureInfo]::InvariantCulture) } else { [int64]0 }
        $mappingMatch = $null -ne $expectedRow -and $null -ne $inventoryRow -and $sample.source_path -eq $inventoryRow.source_path -and $sample.source_sha256.Trim().ToUpperInvariant() -eq $expectedSha -and $expectedRow.sha -eq $expectedSha -and [int64]$sample.source_size -eq $expectedSize -and [int64]$expectedRow.size -eq $expectedSize -and $sample.sample_role -eq $expectedRow.role
        if (-not $mappingMatch) { $sampleMappingFailure = $true }
        $exists = Test-Path -LiteralPath $sourceAbsolute
        $actualSha = if ($exists) { Get-Hash $sourceAbsolute } else { '' }
        $actualSize = if ($exists) { [int64](Get-Item -LiteralPath $sourceAbsolute).Length } else { [int64]0 }
        $actualOleHeader = if ($exists) { Get-OleHeaderHex -Path $sourceAbsolute } else { '' }
        $sizeMatch = $exists -and $actualSize -eq $expectedSize
        $shaMatch = $exists -and $actualSha.Trim().ToUpperInvariant() -eq $expectedSha.Trim().ToUpperInvariant()
        $oleMatch = $exists -and $actualOleHeader.Trim().ToUpperInvariant() -eq 'D0CF11E0A1B11AE1'
        $valid = $exists -and $sizeMatch -and $shaMatch -and $oleMatch
        if (-not $valid) { $sourceFailure = $true }
        $sourceRows += [pscustomobject]@{
            paper_id=$sample.paper_id
            source_path=$sample.source_path
            source_absolute=$sourceAbsolute
            source_exists=[int]$exists
            expected_size=$expectedSize
            actual_size=$actualSize
            source_size_match=[int]$sizeMatch
            expected_sha256=$expectedSha
            actual_sha256=$actualSha.Trim().ToUpperInvariant()
            source_sha_match=[int]$shaMatch
            expected_ole_header='D0CF11E0A1B11AE1'
            actual_ole_header=$actualOleHeader.Trim().ToUpperInvariant()
            source_ole_signature_match=[int]$oleMatch
            source_integrity_pass=[int]$valid
            sample_mapping_match=[int]$mappingMatch
            source_sha_before=$actualSha
            source_sha_after=$actualSha
            source_size=$actualSize
            word_version=''
            word_build=''
            attempt=''
            conversion_attempted=0
            word_create_attempted=0
            word_created=0
            security_configuration_attempted=0
            security_verified=0
            security_gate_pass=0
            documents_collection_acquire_attempted=0
            documents_collection_acquired=0
            security_configured=0
            document_open_attempted=0
            document_open_returned_object=0
            document_opened=0
            document_open_exception_type=''
            document_open_exception_message=''
            document_open_hresult=''
            document_open_inner_exception_type=''
            document_open_inner_exception_message=''
            export_invocation_strategy='TWO_REQUIRED_ARGUMENTS'
            export_argument_count=2
            export_output_path=''
            export_output_full_path=''
            export_output_parent=''
            export_output_parent_exists=0
            export_output_extension=''
            export_output_path_length=0
            export_output_file_exists_before=0
            export_output_absolute=0
            export_output_parent_governed=0
            export_output_source_directory_match=0
            export_output_path_type='System.String'
            export_format_value=17
            export_exception_type=''
            export_exception_message=''
            export_hresult_hex=''
            export_hresult_decimal=''
            export_inner_exception_type=''
            export_inner_exception_message=''
            export_attempted=0
            export_completed=0
            stage_word_pid=''
            background_drain_check_implemented=1
            background_drain_status_available=0
            background_saving_status_initial=0
            background_printing_status_initial=0
            background_saving_status_final=0
            background_printing_status_final=0
            background_drain_completed=0
            background_drain_wait_ms=0
            background_drain_error_type=''
            background_drain_error_message=''
            post_export_settle_implemented=1
            post_export_settle_ms=500
            post_export_settle_completed=0
            document_com_release_attempted=0
            document_com_release_completed=0
            documents_com_release_attempted=0
            documents_com_release_completed=0
            options_com_release_attempted=0
            options_com_release_completed=0
            word_com_release_attempted=0
            word_com_release_completed=0
            document_close_attempted=0
            document_closed=0
            word_quit_attempted=0
            word_quit_called=0
            com_references_released=0
            word_process_exited=0
            primary_error_code=if($valid){''}else{'SOURCE_INTEGRITY_FAILED'}
            primary_error_message=if($valid){''}else{'source_exists, source_size_match, source_sha_match, and source_ole_signature_match are reported above'}
            cleanup_error_code=''
            cleanup_error_message=''
            word_quit_exception_type=''
            word_quit_exception_message=''
            word_quit_hresult=''
            word_quit_inner_exception_type=''
            word_quit_inner_exception_message=''
            conversion_started=0
            conversion_completed=0
            derivative_path=''
            derivative_sha256=''
            derivative_size=0
            validation_derivative_path=''
            validation_derivative_sha256=''
            validation_attempt=''
            validation_export_attempted=0
            validation_export_completed=0
            validation_stage_word_pid=''
            validation_background_drain_completed=0
            validation_background_drain_wait_ms=0
            validation_document_closed=0
            validation_word_quit_called=0
            validation_com_references_released=0
            validation_word_process_exited=0
            validation_cleanup_error_code=''
            validation_cleanup_error_message=''
            validation_error_code=''
            validation_error_message=''
            error_code=if($valid){''}else{'SOURCE_INTEGRITY_FAILED'}
            error_message=if($valid){''}else{'source_exists, source_size_match, source_sha_match, and source_ole_signature_match are reported above'}
        }
        $diagnostic = "PREflight paper_id=$($sample.paper_id) SOURCE_EXISTS=$([int]$exists) EXPECTED_SIZE=$expectedSize ACTUAL_SIZE=$actualSize SOURCE_SIZE_MATCH=$([int]$sizeMatch) EXPECTED_SHA256=$expectedSha ACTUAL_SHA256=$($actualSha.Trim().ToUpperInvariant()) SOURCE_SHA_MATCH=$([int]$shaMatch) EXPECTED_OLE_HEADER=D0CF11E0A1B11AE1 ACTUAL_OLE_HEADER=$($actualOleHeader.Trim().ToUpperInvariant()) SOURCE_OLE_SIGNATURE_MATCH=$([int]$oleMatch) SOURCE_INTEGRITY_PASS=$([int]$valid)"
        Write-RunnerLog $diagnostic
        Write-Output $diagnostic
    }

    $allSourceIntegrityPass = @($sourceRows | Where-Object source_integrity_pass -ne 1).Count -eq 0
    if ($PreflightOnly) {
        $preflightResult = [ordered]@{RUN_STATUS='PREFLIGHT_ONLY'; stage=if($ReplacementMode){'G8-DOC-INTERACTIVE-WORD-PILOT-REPLACEMENT'}else{'G8-DOC-INTERACTIVE-WORD-PILOT'}; DOC_TARGET_ROWS=$targetIds.Count; DOC_PILOT_SAMPLE_ROWS=$sampleIds.Count; SOURCE_GATE_PREDICATES='SOURCE_EXISTS;SOURCE_SIZE_MATCH;SOURCE_SHA_MATCH;SOURCE_OLE_SIGNATURE_MATCH'; ALL_FROZEN_SAMPLE_SOURCE_INTEGRITY_PASS=[int]($allSourceIntegrityPass -and -not $sampleMappingFailure); WORD_COM_INSTANCE_CREATED=0; DOC_OPENED=0; DOC_CONVERSION_ATTEMPTED=0; samples=$sourceRows}
        if ($ReplacementMode) {
            $preflightResult.REPLACEMENT_MODE=1
            $preflightResult.REPLACEMENT_PAPER_ID=$ReplacementPaperId
            $preflightResult.REPLACEMENT_PREFLIGHT_PASS=[int]($allSourceIntegrityPass -and -not $sampleMappingFailure)
            $preflightResult.REPLACEMENT_RUNNER_READY=1
            $preflightResult.REPLACEMENT_CONVERSION_RUN=0
        }
        Write-Output ($preflightResult | ConvertTo-Json -Depth 8 -Compress)
        exit [int](-not ($allSourceIntegrityPass -and -not $sampleMappingFailure))
    }

    $expectedTargetCount = if ($ReplacementMode) { 1 } else { 17 }
    $expectedSampleCount = if ($ReplacementMode) { 1 } else { 3 }
    if ($targetIds.Count -ne $expectedTargetCount -or $sampleIds.Count -ne $expectedSampleCount -or (@($sampleIds | Select-Object -Unique).Count -ne $expectedSampleCount) -or $sourceFailure -or $sampleMappingFailure) {
        $result = [ordered]@{RUN_STATUS='BLOCKED'; stage='G8-DOC-INTERACTIVE-WORD-PILOT'; DOC_TARGET_ROWS=$targetIds.Count; DOC_PILOT_SAMPLE_ROWS=$sampleIds.Count; SOURCE_INTEGRITY_PASS=[int]$allSourceIntegrityPass; SOURCE_GATE_PREDICATES='SOURCE_EXISTS;SOURCE_SIZE_MATCH;SOURCE_SHA_MATCH;SOURCE_OLE_SIGNATURE_MATCH'; SAMPLE_MAPPING_MATCH=[int](-not $sampleMappingFailure); WORD_COM_INSTANCE_CREATED=0; DOC_OPENED=0; DOC_CONVERSION_ATTEMPTED=0; error_code=if($allSourceIntegrityPass -and -not $sampleMappingFailure){'BASELINE_RECONCILIATION_FAILED'}else{'SOURCE_INTEGRITY_FAILED'}; samples=$sourceRows}
        $result | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $ResultsPath -Encoding UTF8
        Write-RunnerLog 'RUN_STATUS=BLOCKED BASELINE_RECONCILIATION_FAILED'
        Write-Output ($result | ConvertTo-Json -Depth 8 -Compress)
        exit 1
    }

    $wordVersion = '16.0.20228.20190'
    $conversionFailure = $false
    foreach ($row in $sourceRows) {
        $sample = $samples | Where-Object paper_id -eq $row.paper_id | Select-Object -First 1
        $sample.source_absolute = $row.source_absolute
        $paperDir = Join-Path $DerivativeRoot $row.paper_id
        $firstPdf = Join-Path $paperDir 'source_converted.pdf'
        $validationPdf = Join-Path $TempRoot "validation\$($row.paper_id)\source_converted.pdf"
        $first = Invoke-WordPdfConversion -Sample $sample -OutputPdf $firstPdf -AttemptLabel 'PRIMARY'
        foreach ($field in @('attempt','conversion_attempted','word_create_attempted','word_created','security_configuration_attempted','security_configured','security_verified','security_gate_pass','documents_collection_acquire_attempted','documents_collection_acquired','document_open_attempted','document_open_returned_object','document_opened','document_open_exception_type','document_open_exception_message','document_open_hresult','document_open_inner_exception_type','document_open_inner_exception_message','export_invocation_strategy','export_argument_count','export_output_path','export_output_full_path','export_output_parent','export_output_parent_exists','export_output_extension','export_output_path_length','export_output_file_exists_before','export_output_absolute','export_output_parent_governed','export_output_source_directory_match','export_output_path_type','export_format_value','export_exception_type','export_exception_message','export_hresult_hex','export_hresult_decimal','export_inner_exception_type','export_inner_exception_message','export_attempted','export_completed','stage_word_pid','background_drain_check_implemented','background_drain_status_available','background_saving_status_initial','background_printing_status_initial','background_saving_status_final','background_printing_status_final','background_drain_completed','background_drain_wait_ms','background_drain_error_type','background_drain_error_message','post_export_settle_implemented','post_export_settle_ms','post_export_settle_completed','document_com_release_attempted','document_com_release_completed','documents_com_release_attempted','documents_com_release_completed','options_com_release_attempted','options_com_release_completed','word_com_release_attempted','word_com_release_completed','document_close_attempted','document_closed','word_quit_attempted','word_quit_called','com_references_released','word_process_exited','primary_error_code','primary_error_message','cleanup_error_code','cleanup_error_message','word_quit_exception_type','word_quit_exception_message','word_quit_hresult','word_quit_inner_exception_type','word_quit_inner_exception_message','error_code','error_message')) {
            $row.$field = $first.$field
        }
        # Legacy field retained for result compatibility; it now means ExportAsFixedFormat was entered.
        $row.conversion_started = $first.export_attempted
        $row.conversion_completed = $first.export_completed
        $row.derivative_path = if($first.export_completed){$first.output_pdf}else{''}
        $row.derivative_sha256 = if($first.export_completed){Get-Hash $first.output_pdf}else{''}
        $row.derivative_size = if($first.export_completed){(Get-Item -LiteralPath $first.output_pdf).Length}else{0}
        $row.word_version = $wordVersion
        $row.word_build = $wordVersion
        if ($first.export_completed) {
            $second = Invoke-WordPdfConversion -Sample $sample -OutputPdf $validationPdf -AttemptLabel 'VALIDATION'
            $row.validation_attempt = $second.attempt
            $row.validation_export_attempted = $second.export_attempted
            $row.validation_export_completed = $second.export_completed
            $row.validation_stage_word_pid = $second.stage_word_pid
            $row.validation_background_drain_completed = $second.background_drain_completed
            $row.validation_background_drain_wait_ms = $second.background_drain_wait_ms
            $row.validation_document_closed = $second.document_closed
            $row.validation_word_quit_called = $second.word_quit_called
            $row.validation_com_references_released = $second.com_references_released
            $row.validation_word_process_exited = $second.word_process_exited
            $row.validation_cleanup_error_code = $second.cleanup_error_code
            $row.validation_cleanup_error_message = $second.cleanup_error_message
            $row.validation_error_code = $second.error_code
            $row.validation_error_message = $second.error_message
            $row.validation_derivative_path = if($second.export_completed){$second.output_pdf}else{''}
            $row.validation_derivative_sha256 = if($second.export_completed){Get-Hash $second.output_pdf}else{''}
            if (-not $second.export_completed) { $conversionFailure = $true }
        } else {
            $conversionFailure = $true
        }
        $row.source_sha_after = if(Test-Path -LiteralPath $row.source_absolute){Get-Hash $row.source_absolute}else{''}
        if ($row.source_sha_before -ne $row.source_sha_after) {
            if ([string]::IsNullOrWhiteSpace([string]$row.primary_error_code)) {
                $row.primary_error_code = 'SOURCE_MUTATION'
                $row.primary_error_message = 'source SHA changed after conversion'
                if ([string]::IsNullOrWhiteSpace([string]$row.error_code)) {
                    $row.error_code = 'SOURCE_MUTATION'
                    $row.error_message = $row.primary_error_message
                }
            }
            $conversionFailure = $true
        }
        if ($script:OrphanIds.Count -gt 0) {
            if ([string]::IsNullOrWhiteSpace([string]$row.error_code)) {
                $row.error_code = 'ORPHAN_STAGE_WORD_PROCESS'
                $row.error_message = ($script:OrphanIds -join ',')
            }
            $conversionFailure = $true
        }
        if ($conversionFailure) { break }
    }

    $csvFields = @('paper_id','source_path','source_sha_before','source_sha_after','source_size','word_version','word_build','conversion_attempted','conversion_started','conversion_completed','word_create_attempted','word_created','security_configuration_attempted','security_configured','security_verified','security_gate_pass','documents_collection_acquire_attempted','documents_collection_acquired','document_open_attempted','document_open_returned_object','document_opened','document_open_exception_type','document_open_exception_message','document_open_hresult','document_open_inner_exception_type','document_open_inner_exception_message','export_invocation_strategy','export_argument_count','export_output_path','export_output_full_path','export_output_parent','export_output_parent_exists','export_output_extension','export_output_path_length','export_output_file_exists_before','export_output_absolute','export_output_parent_governed','export_output_source_directory_match','export_output_path_type','export_format_value','export_exception_type','export_exception_message','export_hresult_hex','export_hresult_decimal','export_inner_exception_type','export_inner_exception_message','export_attempted','export_completed','stage_word_pid','background_drain_check_implemented','background_drain_status_available','background_saving_status_initial','background_printing_status_initial','background_saving_status_final','background_printing_status_final','background_drain_completed','background_drain_wait_ms','background_drain_error_type','background_drain_error_message','post_export_settle_implemented','post_export_settle_ms','post_export_settle_completed','document_com_release_attempted','document_com_release_completed','documents_com_release_attempted','documents_com_release_completed','options_com_release_attempted','options_com_release_completed','word_com_release_attempted','word_com_release_completed','document_close_attempted','document_closed','word_quit_attempted','word_quit_called','word_quit_exception_type','word_quit_exception_message','word_quit_hresult','word_quit_inner_exception_type','word_quit_inner_exception_message','com_references_released','word_process_exited','primary_error_code','primary_error_message','cleanup_error_code','cleanup_error_message','derivative_path','derivative_sha256','derivative_size','validation_derivative_path','validation_derivative_sha256','validation_export_attempted','validation_export_completed','validation_stage_word_pid','validation_background_drain_completed','validation_background_drain_wait_ms','validation_document_closed','validation_word_quit_called','validation_com_references_released','validation_word_process_exited','validation_error_code','validation_error_message','error_code','error_message')
    $sourceRows | Select-Object $csvFields | Export-Csv -LiteralPath $ConversionPath -NoTypeInformation -Encoding UTF8
    $attemptedCount = @($sourceRows | Where-Object conversion_attempted -eq 1).Count
    $completedCount = @($sourceRows | Where-Object conversion_completed -eq 1).Count
    $failedCount = @($sourceRows | Where-Object { ($_.conversion_attempted -eq 1 -and $_.conversion_completed -ne 1) -or ($_.validation_export_attempted -eq 1 -and $_.validation_export_completed -ne 1) }).Count
    $pilotAttemptCount = @($sourceRows | Where-Object { -not [string]::IsNullOrWhiteSpace([string]$_.attempt) }).Count + @($sourceRows | Where-Object { -not [string]::IsNullOrWhiteSpace([string]$_.validation_attempt) }).Count
    $runStatus = if ($completedCount -eq $expectedSampleCount -and -not $conversionFailure -and $script:OrphanIds.Count -eq 0) { 'COMPLETE' } else { 'BLOCKED' }
    $result = [ordered]@{
        RUN_STATUS=$runStatus
        stage=if($ReplacementMode){'G8-DOC-INTERACTIVE-WORD-PILOT-REPLACEMENT'}else{'G8-DOC-INTERACTIVE-WORD-PILOT'}
        DOC_TARGET_ROWS=$targetIds.Count
        DOC_PILOT_SAMPLE_ROWS=$sampleIds.Count
        DOC_PILOT_SAMPLE_SELECTION_STABLE=1
        CURRENT_SESSION_INTERACTIVE_WORD_CAPABLE=1
        WORD_VERSION=$wordVersion
        WORD_BUILD=$wordVersion
        WORD_COM_INSTANCE_CREATED=[int]$script:WordComInstanceCreated
        WORD_COM_SECURITY_GATE_PASS=[int](@($sourceRows | Where-Object word_created -eq 1).Count -gt 0 -and @($sourceRows | Where-Object { $_.word_created -eq 1 -and $_.security_gate_pass -ne 1 }).Count -eq 0)
        MACRO_EXECUTION_ALLOWED=0
        DOC_OPENED=[int](@($sourceRows | Where-Object document_opened -eq 1).Count -gt 0)
        INTERACTIVE_WORD_RUN_COMPLETED=[int]($runStatus -eq 'COMPLETE')
        DOC_PILOT_SAMPLE_ATTEMPTS=$pilotAttemptCount
        DOC_PILOT_REPLACEMENT_SAMPLES=[int]$ReplacementMode
        DOC_PILOT_CONVERSION_ATTEMPTED=$attemptedCount
        DOC_PILOT_CONVERSION_COMPLETED=$completedCount
        DOC_PILOT_CONVERSION_FAILED=$failedCount
        DOC_PILOT_SOURCE_SHA_MISMATCH=[int](@($sourceRows | Where-Object {$_.source_sha_before -ne $_.source_sha_after}).Count -gt 0)
        PRE_EXISTING_WORD_PROCESSES=($preExistingIds -join ',')
        STAGE_WORD_PROCESSES_CREATED=($script:StageCreatedIds | Select-Object -Unique) -join ','
        STAGE_WORD_PROCESSES_CLEANED=$script:StageCleanedCount
        ORPHAN_STAGE_WORD_PROCESSES=($script:OrphanIds | Select-Object -Unique) -join ','
        DOC_PILOT_PDF_AUDIT_PENDING=1
        DOC_PILOT_EXTRACTION_PENDING=1
        DOC_PILOT_SEMANTIC_DETERMINISM_PENDING=1
        DOC_CONTRACT_APPROVED=0
        DOC_BATCH_RUN=0
        DOC_FORMAL_ARTIFACT_GENERATION_RUN=0
        samples=$sourceRows
    }
    if ($ReplacementMode) {
        $replacementRow = $sourceRows | Select-Object -First 1
        $result.REPLACEMENT_MODE=1
        $result.REPLACEMENT_PAPER_ID=$ReplacementPaperId
        $result.REPLACEMENT_SOURCE_PATH=$replacementRow.source_path
        $result.REPLACEMENT_SOURCE_SHA256=$replacementRow.expected_sha256
        $result.REPLACEMENT_SOURCE_SIZE=$replacementRow.expected_size
        $result.REPLACEMENT_PREFLIGHT_PASS=[int]$allSourceIntegrityPass
        $result.REPLACEMENT_RUNNER_READY=1
        $result.REPLACEMENT_CONVERSION_RUN=1
        $result.REPLACEMENT_PRIMARY_CONVERSION_COMPLETED=[int]($sourceRows[0].conversion_completed -eq 1)
        $result.REPLACEMENT_VALIDATION_CONVERSION_COMPLETED=[int]($sourceRows[0].validation_export_completed -eq 1)
        $result.REPLACEMENT_STAGE_WORD_PROCESSES_CREATED=($script:StageCreatedIds | Select-Object -Unique) -join ','
        $result.REPLACEMENT_STAGE_WORD_PROCESSES_CLEANED=$script:StageCleanedCount
        $result.REPLACEMENT_ORPHAN_STAGE_WORD_PROCESSES=($script:OrphanIds | Select-Object -Unique) -join ','
    }
    $result | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $ResultsPath -Encoding UTF8
    Write-RunnerLog "RUN_STATUS=$runStatus conversion_attempted=$attemptedCount conversion_completed=$completedCount conversion_failed=$failedCount orphan_count=$($script:OrphanIds.Count)"
    Write-Output ($result | ConvertTo-Json -Depth 8 -Compress)
    if ($runStatus -ne 'COMPLETE') { exit 1 }
}
catch {
    Write-RunnerLog "RUN_STATUS=BLOCKED unhandled_error=$($_.Exception.Message)"
    throw
}
