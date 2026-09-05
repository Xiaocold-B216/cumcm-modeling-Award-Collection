[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Catalog = Join-Path $Root 'catalog\scale'
$LogDir = Join-Path $Root 'logs\scale'
$ReportDir = Join-Path $Root 'reports\scale'
$VersionDriftRoot = Join-Path $Root 'tmp\g8_doc_converter_version_drift\16.0.20326.20112'
$ManifestPath = Join-Path $Catalog 'g8_doc_converter_version_drift_manifest.csv'
$ResultPath = Join-Path $Catalog 'g8_doc_converter_version_drift_results.json'
$ResultCsvPath = Join-Path $Catalog 'g8_doc_converter_version_drift_results.csv'
$PdfAuditPath = Join-Path $Catalog 'g8_doc_converter_version_drift_pdf_audit.csv'
$PageAuditPath = Join-Path $Catalog 'g8_doc_converter_version_drift_page_audit.csv'
$SemanticPath = Join-Path $Catalog 'g8_doc_converter_version_drift_semantic_comparison.csv'
$ReportPath = Join-Path $ReportDir 'G8_DOC_CONVERTER_VERSION_DRIFT_COMPATIBILITY.md'
$LogPath = Join-Path $LogDir 'g8_doc_converter_version_drift.log'
$ExpectedComMajor = '16.0'
$ExpectedCandidateProductVersion = '16.0.20326.20112'
$FrozenBaselineProductVersion = '16.0.20228.20190'
$WordExecutable = 'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE'
$ExpectedOle = 'D0CF11E0A1B11AE1'
$script:StageCreatedIds = @()
$script:StageOrphanIds = @()
$script:StageCleanedIds = @()

New-Item -ItemType Directory -Force -Path $Catalog, $LogDir, $ReportDir, $VersionDriftRoot | Out-Null

function Read-CsvUtf8([string]$Path) {
    return @(Get-Content -LiteralPath $Path -Encoding UTF8 | ConvertFrom-Csv)
}

function Test-FixedSampleManifest {
    param([object[]]$Rows)
    $expectedIds = @(
        'CUMCM-2011-C-002'
        'CUMCM-2013-D-001'
        'CUMCM-2014-D-003'
    )
    $headers = if ($null -ne $Rows -and @($Rows).Count -gt 0) { @($Rows[0].PSObject.Properties.Name) } else { @() }
    $readerFieldPass = [int]($headers -contains 'paper_id')
    $manifestIds = @()
    if ($readerFieldPass -eq 1) {
        $manifestIds = @(
            @($Rows) |
                ForEach-Object { [string]$_.paper_id } |
                ForEach-Object { $_.Trim() } |
                Where-Object { $_ -ne '' }
        )
    }
    $uniqueIds = @($manifestIds | Sort-Object -Unique)
    $duplicateCount = [int]($manifestIds.Count - $uniqueIds.Count)
    $countPass = [int]($manifestIds.Count -eq 3)
    $setEqualityPass = 0
    if ($countPass -eq 1 -and $duplicateCount -eq 0 -and $uniqueIds.Count -eq $expectedIds.Count) {
        $expectedSet = @($expectedIds | Sort-Object -Unique)
        $setEqualityPass = [int](
            (($uniqueIds | Where-Object { $expectedSet -contains $_ }).Count -eq $expectedSet.Count) -and
            (($expectedSet | Where-Object { $uniqueIds -contains $_ }).Count -eq $uniqueIds.Count)
        )
    }
    $forbiddenIncluded = [int]($manifestIds -contains 'CUMCM-2014-A-006')
    return [pscustomobject]@{
        headers = $headers
        manifest_ids = $manifestIds
        expected_ids = $expectedIds
        manifest_row_count = @($Rows).Count
        manifest_id_count = $manifestIds.Count
        duplicate_count = $duplicateCount
        fixed_sample_count_pass = $countPass
        set_equality_pass = $setEqualityPass
        forbidden_sample_included = $forbiddenIncluded
        reader_field = 'paper_id'
        reader_field_pass = $readerFieldPass
        normalization_pass = [int]($readerFieldPass -eq 1 -and $manifestIds.Count -eq @($Rows).Count -and @($manifestIds | Where-Object { $_ -ne $_.Trim() }).Count -eq 0)
    }
}

function Write-JsonUtf8([string]$Path, [object]$Value) {
    $temporary = "$Path.tmp"
    ($Value | ConvertTo-Json -Depth 20) | Set-Content -LiteralPath $temporary -Encoding UTF8
    Move-Item -LiteralPath $temporary -Destination $Path -Force
}

function Write-Log([string]$Message) {
    Add-Content -LiteralPath $LogPath -Value "$(Get-Date -Format o) $Message" -Encoding UTF8
}

function Get-Hash([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToUpperInvariant()
}

function ConvertTo-HexString {
    param([Parameter(Mandatory = $true)][byte[]]$Bytes)
    return ([BitConverter]::ToString($Bytes)).Replace('-', '').ToUpperInvariant()
}

function Get-OleSignature([string]$Path) {
    $stream = [System.IO.File]::Open($Path, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]::ReadWrite)
    try {
        $buffer = New-Object byte[] 8
        if ($stream.Read($buffer, 0, 8) -ne 8) { return '' }
        return (ConvertTo-HexString -Bytes $buffer)
    }
    finally { $stream.Dispose() }
}

function Get-Sha256Text([string]$Text) {
    $sha = New-Object System.Security.Cryptography.SHA256Managed
    try { return (ConvertTo-HexString -Bytes ($sha.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($Text)))) }
    finally { $sha.Dispose() }
}

function Normalize-Text([string]$Text) {
    if ($null -eq $Text) { return '' }
    $withoutNull = $Text.Replace(([char]0).ToString(), [string]::Empty)
    return ([regex]::Replace($withoutNull, '\s+', ' ')).Trim()
}

function Get-WordProductVersion {
    if (-not (Test-Path -LiteralPath $WordExecutable -PathType Leaf)) { return '' }
    try { return [string](Get-Item -LiteralPath $WordExecutable).VersionInfo.FileVersion } catch { return '' }
}

function Get-WordIds {
    return @(Get-Process -Name WINWORD -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id)
}

function Get-StageNewIds([int[]]$Before, [int[]]$After) {
    return @($After | Where-Object { $Before -notcontains $_ })
}

function Capture-StageNewIds([int[]]$Before) {
    $newIds = @(Get-StageNewIds $Before (Get-WordIds))
    if ($newIds.Count -eq 0) {
        for ($i = 0; $i -lt 4; $i++) {
            Start-Sleep -Milliseconds 250
            $newIds = @(Get-StageNewIds $Before (Get-WordIds))
            if ($newIds.Count -gt 0) { break }
        }
    }
    return $newIds
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
    param([int[]]$StageIds, [int]$TimeoutSeconds = 30, [int]$PollMilliseconds = 250)
    if ($null -eq $StageIds -or $StageIds.Count -eq 0) { return [pscustomobject]@{ exited = 1; remaining_ids = @() } }
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    do {
        $remaining = @(Get-WordIds | Where-Object { $StageIds -contains $_ })
        if ($remaining.Count -eq 0) { return [pscustomobject]@{ exited = 1; remaining_ids = @() } }
        $remainingMilliseconds = [int](($deadline - (Get-Date)).TotalMilliseconds)
        if ($remainingMilliseconds -le 0) { break }
        Start-Sleep -Milliseconds ([Math]::Min($PollMilliseconds, $remainingMilliseconds))
    } while ((Get-Date) -lt $deadline)
    $remaining = @(Get-WordIds | Where-Object { $StageIds -contains $_ })
    return [pscustomobject]@{ exited = [int]($remaining.Count -eq 0); remaining_ids = $remaining }
}

function Set-PrimaryError([object]$State, [string]$Code, [string]$Message) {
    if ([string]::IsNullOrWhiteSpace([string]$State.primary_error_code)) {
        $State.primary_error_code = $Code
        $State.primary_error_message = $Message
    }
}

function Set-CleanupError([object]$State, [string]$Code, [string]$Message) {
    if ([string]::IsNullOrWhiteSpace([string]$State.cleanup_error_code)) {
        $State.cleanup_error_code = $Code
        $State.cleanup_error_message = $Message
    }
}

function Get-PdfBasic([string]$Path) {
    $state = [ordered]@{ exists = 0; size = 0; signature_valid = 0; readable = 0; page_count = 0; encrypted = ''; error = '' }
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { $state.error = 'missing'; return [pscustomobject]$state }
    $item = Get-Item -LiteralPath $Path
    $state.exists = 1; $state.size = [int64]$item.Length
    if ($state.size -lt 4) { $state.error = 'empty_or_short'; return [pscustomobject]$state }
    $stream = [System.IO.File]::Open($Path, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]::ReadWrite)
    try {
        $header = New-Object byte[] 4
        if ($stream.Read($header, 0, 4) -eq 4) { $state.signature_valid = [int]([System.Text.Encoding]::ASCII.GetString($header) -eq '%PDF') }
    }
    finally { $stream.Dispose() }
    if ($state.signature_valid -ne 1) { $state.error = 'invalid_signature'; return [pscustomobject]$state }
    $pdfInfo = Get-Command pdfinfo.exe -ErrorAction SilentlyContinue
    if ($null -eq $pdfInfo) { $state.error = 'pdfinfo_unavailable'; return [pscustomobject]$state }
    $infoOutput = & $pdfInfo.Source $Path 2>&1
    if ($LASTEXITCODE -ne 0) { $state.error = (($infoOutput | Out-String).Trim()); return [pscustomobject]$state }
    foreach ($line in $infoOutput) {
        if ([string]$line -match '^Pages:\s*(\d+)') { $state.page_count = [int]$Matches[1] }
        elseif ([string]$line -match '^Encrypted:\s*(.*)$') { $state.encrypted = $Matches[1].Trim() }
    }
    $state.readable = [int]($state.page_count -gt 0 -and $state.encrypted -notmatch 'yes|encrypted')
    if ($state.readable -ne 1) { $state.error = 'unreadable_or_encrypted' }
    return [pscustomobject]$state
}

function Get-PdfPageText([string]$Path, [int]$Page) {
    $pdftotext = Get-Command pdftotext.exe -ErrorAction SilentlyContinue
    if ($null -eq $pdftotext) { throw 'PDFTOTEXT_UNAVAILABLE' }
    $raw = & $pdftotext.Source '-f' $Page '-l' $Page '-layout' $Path '-' 2>$null | Out-String
    return (Normalize-Text $raw)
}

function Get-CandidatePageAudit([string]$Path, [string]$PaperId, [object]$PdfInfo) {
    $pages = @(); $normalizedPages = @(); $classes = @(); $routes = @()
    for ($page = 1; $page -le $PdfInfo.page_count; $page++) {
        $text = Get-PdfPageText $Path $page
        $pageClass = if ($text.Length -gt 0) { 'TEXT_PAGE' } else { 'UNEXPLAINED_PAGE' }
        $route = [int]($pageClass -eq 'IMAGE_ONLY_CONTENT_PAGE')
        $textSha = Get-Sha256Text $text
        $normalizedPages += $text; $classes += $pageClass; $routes += $route
        $pages += [pscustomobject]@{
            paper_id = $PaperId; logical_page_number = $page; page_class = $pageClass
            text_layer_present = [int]($text.Length -gt 0); ocr_route_required = $route
            text_chars = $text.Length; text_sha256 = $textSha; rendered_for_classification = 0; nonwhite_ratio = ''
        }
    }
    return [pscustomobject]@{ rows = $pages; pages = $normalizedPages; classes = $classes; routes = $routes }
}

function Get-ReferenceAudit([object]$Sample) {
    $rows = @(Read-CsvUtf8 (Join-Path $Root ($Sample.reference_page_audit_path -replace '/', '\')) | Where-Object { $_.paper_id -eq $Sample.paper_id -and $_.attempt -eq 'PRIMARY' } | Sort-Object { [int]$_.logical_page_number })
    if ($rows.Count -eq 0) { throw "REFERENCE_PAGE_AUDIT_MISSING=$($Sample.paper_id)" }
    return $rows
}

function Compare-Semantics([object]$Sample, [object]$CandidatePages, [object]$PdfInfo) {
    $reference = @(Get-ReferenceAudit $Sample)
    $refClasses = @($reference | ForEach-Object { [string]$_.page_class })
    $refRoutes = @($reference | ForEach-Object { [int]$_.ocr_route_required })
    $refTextHashes = @($reference | ForEach-Object { [string]$_.text_sha256 })
    $candidateText = (($CandidatePages.pages) -join ' ')
    $candidateOverallSha = Get-Sha256Text $candidateText
    $classesMatch = [int](@($CandidatePages.classes) -join ';' -eq ($refClasses -join ';'))
    $routesMatch = [int](@($CandidatePages.routes) -join ';' -eq ($refRoutes -join ';'))
    $pageTextMatch = [int](@($CandidatePages.rows | ForEach-Object { [string]$_.text_sha256 }) -join ';' -eq ($refTextHashes -join ';'))
    $pageCountMatch = [int]($PdfInfo.page_count -eq $reference.Count)
    $overallMatch = [int]($candidateOverallSha -eq [string]$Sample.reference_normalized_text_sha256)
    $semanticPass = [int]($pageCountMatch -eq 1 -and $classesMatch -eq 1 -and $routesMatch -eq 1 -and $pageTextMatch -eq 1 -and $overallMatch -eq 1)
    return [pscustomobject]@{
        paper_id = $Sample.paper_id; candidate_page_count = $PdfInfo.page_count; reference_page_count = $reference.Count
        page_count_match = $pageCountMatch; page_class_match = $classesMatch; ocr_route_match = $routesMatch
        page_text_sha256_match = $pageTextMatch; candidate_normalized_text_sha256 = $candidateOverallSha
        reference_normalized_text_sha256 = $Sample.reference_normalized_text_sha256; normalized_text_match = $overallMatch
        reference_semantic_sha256 = $Sample.reference_semantic_sha256; binary_pdf_sha_equality_required = 0
        semantic_compatibility = if ($semanticPass -eq 1) { 'PASS' } else { 'FAIL' }
    }
}

function Invoke-CandidateConversion([object]$Sample) {
    $outputPdf = Join-Path $VersionDriftRoot (Join-Path $Sample.paper_id 'source_converted.pdf')
    $state = [ordered]@{
        paper_id = $Sample.paper_id; source_path = $Sample.source_path; source_absolute = $Sample.source_absolute
        candidate_output_path = $outputPdf; source_preflight_pass = 0; source_sha_before = ''; source_sha_after = ''
        current_conversion_status = 'PENDING'; skip_word_conversion = 0; candidate_pdf_sha256_before_audit = ''; candidate_pdf_hash_stable = 0
        word_create_attempted = 0; word_created = 0; word_com_version = ''; word_product_version = ''
        word_com_major_version_pass = 0; word_product_version_pass = 0; candidate_version_drift_during_test = 0; version_gate_pass = 0
        security_configured = 0; document_open_attempted = 0; document_opened = 0
        conversion_attempted = 0; export_returned = 0; conversion_completed = 0
        document_close_attempted = 0; document_closed = 0; word_quit_attempted = 0; word_quit_called = 0
        com_references_released = 0; word_process_exited = 0; stage_word_pid = ''
        primary_error_code = ''; primary_error_message = ''; cleanup_error_code = ''; cleanup_error_message = ''
        error_code = ''; error_message = ''; candidate_pdf_size = 0; candidate_pdf_sha256 = ''
        pdf_basic_validation_pass = 0; semantic_compatibility = 'NOT_RUN'
    }
    $sourceExists = Test-Path -LiteralPath $Sample.source_absolute -PathType Leaf
    if ($sourceExists) {
        $item = Get-Item -LiteralPath $Sample.source_absolute
        $state.source_sha_before = Get-Hash $Sample.source_absolute
        $sourceOle = Get-OleSignature $Sample.source_absolute
        $state.source_preflight_pass = [int]($item.Length -eq [int64]$Sample.source_size -and $state.source_sha_before -eq $Sample.source_sha256 -and $sourceOle -eq $ExpectedOle)
    }
    if ($state.source_preflight_pass -ne 1) {
        Set-PrimaryError $state 'SOURCE_PREFLIGHT_ERROR' 'Source path, size, SHA256, or OLE signature mismatch'
        $state.error_code = $state.primary_error_code; $state.error_message = $state.primary_error_message
        return [pscustomobject]$state
    }

    # A validated, version-isolated candidate is reusable.  Do not create a
    # new Word session or overwrite it during a resume.
    $existingPdf = Get-PdfBasic $outputPdf
    if ($existingPdf.exists -eq 1 -and $existingPdf.size -gt 0 -and $existingPdf.signature_valid -eq 1 -and $existingPdf.readable -eq 1) {
        $state.current_conversion_status = 'COMPLETE'
        $state.skip_word_conversion = 1
        $state.candidate_pdf_size = $existingPdf.size
        $state.pdf_basic_validation_pass = 1
        $state.candidate_pdf_sha256 = Get-Hash $outputPdf
        $state.candidate_pdf_sha256_before_audit = $state.candidate_pdf_sha256
        $state.candidate_pdf_hash_stable = 1
        $state.conversion_completed = 1
        $state.source_sha_after = $state.source_sha_before
        return [pscustomobject]$state
    }
    if ($existingPdf.exists -eq 1) { $state.current_conversion_status = 'INVALID' }

    $word = $null; $documents = $null; $options = $null; $doc = $null; $missing = [Type]::Missing
    $beforeIds = @(Get-WordIds); $newIds = @(); $allReleased = $true
    try {
        $state.word_create_attempted = 1
        $word = New-Object -ComObject Word.Application
        $state.word_created = 1
        $newIds = @(Capture-StageNewIds $beforeIds)
        $state.stage_word_pid = $newIds -join ','
        foreach ($id in $newIds) { if ($script:StageCreatedIds -notcontains $id) { $script:StageCreatedIds += $id } }
        if ($newIds.Count -ne 1) { throw 'PROCESS_OWNERSHIP_AMBIGUOUS' }

        $state.word_com_version = [string]$word.Version
        $state.word_com_major_version_pass = [int]($state.word_com_version -eq $ExpectedComMajor)
        if ($state.word_com_major_version_pass -ne 1) { throw 'WORD_COM_VERSION_UNEXPECTED' }
        $state.word_product_version = Get-WordProductVersion
        $state.word_product_version_pass = [int]($state.word_product_version -eq $ExpectedCandidateProductVersion)
        $state.candidate_version_drift_during_test = [int]($state.word_product_version_pass -ne 1)
        if ($state.candidate_version_drift_during_test -eq 1) { throw 'CANDIDATE_VERSION_DRIFT_DURING_TEST' }
        $state.version_gate_pass = 1

        $word.Visible = $false; $word.DisplayAlerts = 0; $word.AutomationSecurity = 3
        $options = $word.Options
        $options.UpdateLinksAtOpen = $false; $options.ConfirmConversions = $false; $options.SavePropertiesPrompt = $false
        if ($word.Visible -ne $false -or [int]$word.DisplayAlerts -ne 0 -or [int]$word.AutomationSecurity -ne 3 -or $options.UpdateLinksAtOpen -ne $false -or $options.ConfirmConversions -ne $false) { throw 'SECURITY_GATE_FAILED' }
        $state.security_configured = 1

        $documents = $word.Documents
        $state.document_open_attempted = 1
        $doc = $documents.Open([string]$Sample.source_absolute, $false, $true, $false, $missing, $missing, $false, $missing, $missing, $missing, $missing, $false, $false)
        if ($null -eq $doc -or $doc.ReadOnly -ne $true) { throw 'SOURCE_NOT_READONLY' }
        $state.document_opened = 1

        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $outputPdf) | Out-Null
        $state.conversion_attempted = 1
        [void]$doc.ExportAsFixedFormat([string]$outputPdf, [int]17)
        $state.export_returned = 1
        Start-Sleep -Milliseconds 500
        $pdf = Get-PdfBasic $outputPdf
        $state.candidate_pdf_size = $pdf.size
        $state.pdf_basic_validation_pass = [int]($pdf.exists -eq 1 -and $pdf.size -gt 0 -and $pdf.signature_valid -eq 1 -and $pdf.readable -eq 1)
        if ($state.pdf_basic_validation_pass -ne 1) { throw "CANDIDATE_PDF_BASIC_VALIDATION_FAILED=$($pdf.error)" }
        $state.candidate_pdf_sha256 = Get-Hash $outputPdf
        $state.candidate_pdf_sha256_before_audit = $state.candidate_pdf_sha256
        $state.candidate_pdf_hash_stable = 1
        $state.conversion_completed = 1
        $state.current_conversion_status = 'COMPLETE'
    }
    catch {
        $message = $_.Exception.Message
        if ($state.word_create_attempted -eq 1 -and $state.word_created -eq 0) { Set-PrimaryError $state 'WORD_CREATE_ERROR' $message }
        elseif ($state.word_created -eq 1 -and $state.version_gate_pass -eq 0) { Set-PrimaryError $state 'VERSION_GATE_ERROR' $message }
        elseif ($state.security_configured -eq 0) { Set-PrimaryError $state 'SECURITY_ERROR' $message }
        elseif ($state.document_open_attempted -eq 1 -and $state.document_opened -eq 0) { Set-PrimaryError $state 'DOCUMENT_OPEN_ERROR' $message }
        elseif ($state.conversion_attempted -eq 1 -and $state.export_returned -eq 0) { Set-PrimaryError $state 'EXPORT_ERROR' $message }
        elseif ($state.conversion_attempted -eq 1 -and $state.conversion_completed -eq 0) { Set-PrimaryError $state 'CANDIDATE_PDF_VALIDATION_ERROR' $message }
        else { Set-PrimaryError $state 'CANDIDATE_RUN_ERROR' $message }
    }
    finally {
        if ($doc) {
            $state.document_close_attempted = 1
            try { $doc.Close($false); $state.document_closed = 1 } catch { Set-CleanupError $state 'DOCUMENT_CLOSE_ERROR' $_.Exception.Message }
        }
        if ($word) {
            $state.word_quit_attempted = 1
            try { $word.Quit(); $state.word_quit_called = 1 } catch { Set-CleanupError $state 'WORD_QUIT_ERROR' $_.Exception.Message }
        }
        if ($doc) { if (-not (Release-Com $doc)) { $allReleased = $false; Set-CleanupError $state 'COM_RELEASE_ERROR' 'Document COM release failed' }; $doc = $null }
        if ($options) { if (-not (Release-Com $options)) { $allReleased = $false; Set-CleanupError $state 'COM_RELEASE_ERROR' 'Options COM release failed' }; $options = $null }
        if ($documents) { if (-not (Release-Com $documents)) { $allReleased = $false; Set-CleanupError $state 'COM_RELEASE_ERROR' 'Documents COM release failed' }; $documents = $null }
        if ($word) { if (-not (Release-Com $word)) { $allReleased = $false; Set-CleanupError $state 'COM_RELEASE_ERROR' 'Word COM release failed' }; $word = $null }
        $state.com_references_released = [int]$allReleased
        [GC]::Collect(); [GC]::WaitForPendingFinalizers(); [GC]::Collect(); [GC]::WaitForPendingFinalizers()
        $exit = Wait-ForStageProcessExit -StageIds $newIds -TimeoutSeconds 30 -PollMilliseconds 250
        $state.word_process_exited = $exit.exited
        if ($exit.exited -eq 1) { foreach ($id in $newIds) { if ($script:StageCleanedIds -notcontains $id) { $script:StageCleanedIds += $id } } }
        else { foreach ($id in $exit.remaining_ids) { if ($script:StageOrphanIds -notcontains $id) { $script:StageOrphanIds += $id } }; Set-CleanupError $state 'ORPHAN_STAGE_WORD_PROCESS' ($exit.remaining_ids -join ',') }
    }
    $state.source_sha_after = if (Test-Path -LiteralPath $Sample.source_absolute -PathType Leaf) { Get-Hash $Sample.source_absolute } else { '' }
    if ($state.source_sha_after -ne $state.source_sha_before) { Set-PrimaryError $state 'SOURCE_MUTATION' 'Source SHA256 changed during candidate run' }
    if (-not [string]::IsNullOrWhiteSpace([string]$state.primary_error_code)) { $state.error_code = $state.primary_error_code; $state.error_message = $state.primary_error_message }
    elseif (-not [string]::IsNullOrWhiteSpace([string]$state.cleanup_error_code)) { $state.error_code = $state.cleanup_error_code; $state.error_message = $state.cleanup_error_message }
    return [pscustomobject]$state
}

try {
    $manifest = @(Read-CsvUtf8 $ManifestPath)
    $manifestGate = Test-FixedSampleManifest -Rows $manifest
    if ($manifestGate.reader_field_pass -ne 1) { throw 'FIXED_SAMPLE_MANIFEST_FIELD_MISSING' }
    if ($manifestGate.fixed_sample_count_pass -ne 1 -or $manifestGate.duplicate_count -ne 0 -or $manifestGate.set_equality_pass -ne 1) { throw 'FIXED_SAMPLE_MANIFEST_FAILED' }
    if ($manifestGate.forbidden_sample_included -eq 1) { throw 'FORBIDDEN_SUPPORTING_MATERIAL_SAMPLE_PRESENT' }
    $expectedIds = @($manifestGate.expected_ids)
    $results = @(); $pdfRows = @(); $pageRows = @(); $semanticRows = @()
    foreach ($sample in $manifest) {
        $result = Invoke-CandidateConversion $sample
        if ($result.conversion_completed -eq 1) {
            $pdf = Get-PdfBasic $result.candidate_output_path
            $pages = Get-CandidatePageAudit $result.candidate_output_path $sample.paper_id $pdf
            $semantic = Compare-Semantics $sample $pages $pdf
            $candidateHashAfterAudit = Get-Hash $result.candidate_output_path
            $result | Add-Member -NotePropertyName candidate_pdf_sha256_after_audit -NotePropertyValue $candidateHashAfterAudit -Force
            $result | Add-Member -NotePropertyName candidate_pdf_hash_stable -NotePropertyValue ([int]($candidateHashAfterAudit -eq $result.candidate_pdf_sha256_before_audit)) -Force
            if ($result.candidate_pdf_hash_stable -ne 1) {
                Set-PrimaryError $result 'CANDIDATE_PDF_HASH_DRIFT_ERROR' 'Candidate PDF SHA256 changed during semantic audit'
                $result.error_code = $result.primary_error_code; $result.error_message = $result.primary_error_message
            }
            $result | Add-Member -NotePropertyName semantic_compatibility -NotePropertyValue $semantic.semantic_compatibility -Force
            $result | Add-Member -NotePropertyName candidate_page_count -NotePropertyValue $pdf.page_count -Force
            $result | Add-Member -NotePropertyName candidate_normalized_text_sha256 -NotePropertyValue $semantic.candidate_normalized_text_sha256 -Force
            $pdfRows += [pscustomobject]@{ paper_id = $sample.paper_id; candidate_pdf_path = $result.candidate_output_path; pdf_exists = $pdf.exists; pdf_size = $pdf.size; pdf_sha256 = $result.candidate_pdf_sha256; pdf_readable = $pdf.readable; page_count = $pdf.page_count; encrypted = $pdf.encrypted; pdf_class = if (@($pages.classes | Where-Object { $_ -eq 'TEXT_PAGE' }).Count -eq $pdf.page_count) { 'TEXT' } else { 'MIXED_OR_UNEXPLAINED' }; audit_status = if ($pdf.readable -eq 1) { 'PASS' } else { 'FAIL' } }
            $pageRows += @($pages.rows)
            $semanticRows += $semantic
        }
        else { $semanticRows += [pscustomobject]@{ paper_id = $sample.paper_id; semantic_compatibility = 'NOT_RUN'; candidate_page_count = 0; reference_page_count = ''; page_count_match = 0; page_class_match = 0; ocr_route_match = 0; page_text_sha256_match = 0; candidate_normalized_text_sha256 = ''; reference_normalized_text_sha256 = $sample.reference_normalized_text_sha256; normalized_text_match = 0; reference_semantic_sha256 = $sample.reference_semantic_sha256; binary_pdf_sha_equality_required = 0 } }
        $results += $result
    }
    $wordRun = @($results | Where-Object { $_.word_created -eq 1 }).Count
    $conversionRun = @($results | Where-Object { $_.conversion_attempted -eq 1 }).Count
    $semanticPass = @($semanticRows | Where-Object { $_.semantic_compatibility -eq 'PASS' }).Count
    $sourceMutation = @($results | Where-Object { $_.source_sha_after -ne '' -and $_.source_sha_after -ne $_.source_sha_before }).Count
    $resumeComplete = @($results | Where-Object { $_.current_conversion_status -eq 'COMPLETE' -and $_.skip_word_conversion -eq 1 }).Count
    $resumePending = @($results | Where-Object { $_.current_conversion_status -ne 'COMPLETE' }).Count
    $status = if ($script:StageOrphanIds.Count -gt 0 -or $sourceMutation -gt 0) { 'BLOCKED' } elseif ($semanticPass -eq 3) { 'PASS' } elseif ($wordRun -gt 0 -or $resumeComplete -gt 0) { 'PARTIAL' } else { 'BLOCKED' }
    $summary = [ordered]@{
        STAGE = 'G8-DOC-CONVERTER-VERSION-DRIFT-COMPATIBILITY'; STATUS = $status
        BASELINE_WORD_PRODUCT_VERSION = $FrozenBaselineProductVersion; CANDIDATE_WORD_PRODUCT_VERSION = $ExpectedCandidateProductVersion; EXPECTED_WORD_COM_MAJOR_VERSION = $ExpectedComMajor
        VERSION_DRIFT_CONFIRMED = 1; FIXED_SAMPLE_COUNT = 3; FIXED_SAMPLE_IDS = ($expectedIds -join ','); BINARY_PDF_SHA_EQUALITY_REQUIRED = 0
        MANIFEST_HEADERS = ($manifestGate.headers -join '|'); MANIFEST_ROW_COUNT = $manifestGate.manifest_row_count; MANIFEST_PAPER_IDS = ($manifestGate.manifest_ids -join ','); MANIFEST_ID_COUNT = $manifestGate.manifest_id_count; MANIFEST_DUPLICATE_ID_COUNT = $manifestGate.duplicate_count; MANIFEST_FIXED_SAMPLE_COUNT_PASS = $manifestGate.fixed_sample_count_pass; MANIFEST_FIXED_SAMPLE_SET_EQUALITY_PASS = $manifestGate.set_equality_pass; MANIFEST_READER_FIELD = $manifestGate.reader_field; MANIFEST_READER_FIELD_PASS = $manifestGate.reader_field_pass; MANIFEST_NORMALIZATION_PASS = $manifestGate.normalization_pass; FORBIDDEN_SAMPLE_INCLUDED = $manifestGate.forbidden_sample_included
        WORD_COM_RUN = $wordRun; DOC_CONVERSION_RUN = $conversionRun; SEMANTIC_COMPATIBILITY_PASS_COUNT = $semanticPass
        RESUME_COMPLETE_CANDIDATE_COUNT = $resumeComplete; RESUME_PENDING_CANDIDATE_COUNT = $resumePending; VALID_CANDIDATE_RECONVERSION_PROHIBITED = 1
        SOURCE_SHA_MISMATCH = $sourceMutation; ORIGINAL_FILES_MODIFIED = $sourceMutation; FORMAL_ARTIFACTS_MODIFIED = 0; FORMAL_ELIGIBILITY_MODIFIED = 0
        DOC_BATCH_RUN = 0; Q3_REPAIR_RUN = 0; Q3_OCR_RUN = 0; IMAGE_OCR_RUN = 0; IMAGE_EXTRACTION_RERUN = 0; G9_RUN = 0; G10_RUN = 0
        NEW_DEPENDENCY_INSTALLED = 0; NETWORK_ACCESS_USED = 0; GLOBAL_WINWORD_FORCE_KILL_PRESENT = 0
        STAGE_WORD_PROCESSES_CREATED = (($script:StageCreatedIds | Select-Object -Unique) -join ','); STAGE_WORD_PROCESSES_CLEANED = $script:StageCleanedIds.Count; ORPHAN_STAGE_WORD_PROCESSES = (($script:StageOrphanIds | Select-Object -Unique) -join ',')
        samples = $results; pdf_audit = $pdfRows; page_audit = $pageRows; semantic_comparison = $semanticRows
    }
    Write-JsonUtf8 $ResultPath $summary
    if ($results.Count -gt 0) { $results | ConvertTo-Csv -NoTypeInformation | Set-Content -LiteralPath $ResultCsvPath -Encoding UTF8 }
    if ($pdfRows.Count -gt 0) { $pdfRows | ConvertTo-Csv -NoTypeInformation | Set-Content -LiteralPath $PdfAuditPath -Encoding UTF8 }
    if ($pageRows.Count -gt 0) { $pageRows | ConvertTo-Csv -NoTypeInformation | Set-Content -LiteralPath $PageAuditPath -Encoding UTF8 }
    if ($semanticRows.Count -gt 0) { $semanticRows | ConvertTo-Csv -NoTypeInformation | Set-Content -LiteralPath $SemanticPath -Encoding UTF8 }
    Set-Content -LiteralPath $ReportPath -Encoding UTF8 -Value @('# G8 DOC Converter Version Drift Compatibility', '', "Status: ``$status``", '', "Candidate build: ``$ExpectedCandidateProductVersion``; frozen baseline: ``$FrozenBaselineProductVersion``.", "Word sessions: ``$wordRun``; conversion attempts: ``$conversionRun``; semantic passes: ``$semanticPass/3``.", '', 'Candidate PDFs are isolated under `tmp/g8_doc_converter_version_drift/16.0.20326.20112/`; governed production outputs were not written.', '', 'Binary PDF SHA equality is not required; semantic equivalence is evaluated from page count, page class, OCR route, page text hashes, and normalized text hash.', '', 'This runner must be executed only by the user in a normal Windows desktop Word session.')
    Write-Log "STATUS=$status word_run=$wordRun conversion_run=$conversionRun semantic_pass=$semanticPass orphan=$($script:StageOrphanIds -join ',')"
    Write-Output ($summary | ConvertTo-Json -Depth 20 -Compress)
    if ($status -eq 'BLOCKED') { exit 2 }
}
catch {
    Write-Log "STATUS=BLOCKED error=$($_.Exception.Message)"
    throw
}
