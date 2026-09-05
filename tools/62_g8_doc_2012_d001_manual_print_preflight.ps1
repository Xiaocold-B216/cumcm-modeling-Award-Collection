param(
    [switch]$SelfTest,
    [string]$ResultPath
)

$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
$TargetPaperId = 'CUMCM-2012-D-001'
$MembershipCsv = Join-Path $Root 'catalog\paper_files.csv'
$SourceRows = @(Import-Csv -LiteralPath $MembershipCsv -Encoding UTF8 | Where-Object { $_.paper_id -eq $TargetPaperId })
if ($SourceRows.Count -ne 1) { throw "Expected exactly one paper-file membership for $TargetPaperId." }
$SourcePath = Join-Path $Root ($SourceRows[0].path -replace '/', '\\')
$DocxPath = Join-Path $Root 'tmp\g8_doc_2012_d001_docx_intermediate\CUMCM-2012-D-001\source_rebuilt.docx'
$OutputDirectory = Join-Path $Root 'tmp\g8_doc_2012_d001_manual_print_to_pdf\CUMCM-2012-D-001'
$PdfOutputPath = Join-Path $OutputDirectory 'manual_print_candidate.pdf'
$ExpectedSourceSha = 'D93A9A6A9DE012927F8A5D4B36E1768CA3F6AFFB6952673F40FE2740D4032766'
$ExpectedDocxSha = 'B948CA41387ABC408724B1D64286830B54B12198A33C54D8BE684661CA8937DC'

function Get-Sha256Hex {
    param([Parameter(Mandatory = $true)][string]$Path)
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToUpperInvariant()
}

function Get-PreflightStatus {
    param([Parameter(Mandatory = $true)][hashtable]$State)
    if (-not $State.source_sha_match -or -not $State.docx_sha_match -or -not $State.docx_zip_readable -or -not $State.printer_present -or -not $State.printer_driver_match) { return 'FAIL' }
    if ($State.output_exists_before -or -not $State.spooler_running -or $State.tracked_insertions_present -or $State.tracked_deletions_present -or $State.comments_present) { return 'BLOCKED' }
    return 'PASS'
}

function Get-PrinterInventoryReadOnly {
    $keyPath = 'HKLM:\SYSTEM\CurrentControlSet\Control\Print\Printers'
    $rows = @()
    Get-ChildItem -LiteralPath $keyPath | ForEach-Object {
        $props = Get-ItemProperty -LiteralPath $_.PSPath
        $rows += [PSCustomObject]@{
            Name = $_.PSChildName
            DriverName = if ($null -eq $props.'Printer Driver') { 'UNAVAILABLE' } else { [string]$props.'Printer Driver' }
            PortName = if ($null -eq $props.Port) { 'UNAVAILABLE' } else { [string]$props.Port }
        }
    }
    return $rows
}

function Get-DocxMarkupState {
    param([Parameter(Mandatory = $true)][string]$Path)
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $archive = [System.IO.Compression.ZipFile]::OpenRead($Path)
    try {
        $documentEntry = $archive.GetEntry('word/document.xml')
        if ($null -eq $documentEntry) { throw 'word/document.xml is missing.' }
        $reader = New-Object System.IO.StreamReader($documentEntry.Open())
        try { $xml = $reader.ReadToEnd() } finally { $reader.Dispose() }
        return [PSCustomObject]@{
            ZipReadable = 1
            TrackedInsertionsPresent = [int]($xml -match '<w:ins(?:\s|>)')
            TrackedDeletionsPresent = [int]($xml -match '<w:del(?:\s|>)')
            CommentsPresent = [int]($null -ne $archive.GetEntry('word/comments.xml'))
        }
    }
    finally { $archive.Dispose() }
}

if ($SelfTest) {
    $base = @{ source_sha_match=$true; docx_sha_match=$true; docx_zip_readable=$true; printer_present=$true; printer_driver_match=$true; output_exists_before=$false; spooler_running=$true; tracked_insertions_present=$false; tracked_deletions_present=$false; comments_present=$false }
    $cases = @{
        A = @{ State=$base; Expected='PASS' }
        B = @{ State=($base.Clone()); Expected='FAIL' }
        C = @{ State=($base.Clone()); Expected='FAIL' }
        D = @{ State=($base.Clone()); Expected='FAIL' }
        E = @{ State=($base.Clone()); Expected='BLOCKED' }
        F = @{ State=($base.Clone()); Expected='BLOCKED' }
        G = @{ State=($base.Clone()); Expected='BLOCKED' }
        H = @{ State=($base.Clone()); Expected='BLOCKED' }
    }
    $cases.B.State.source_sha_match = $false; $cases.C.State.docx_sha_match = $false; $cases.D.State.printer_present = $false
    $cases.E.State.output_exists_before = $true; $cases.F.State.tracked_insertions_present = $true; $cases.G.State.comments_present = $true; $cases.H.State.spooler_running = $false
    $pass = $true
    foreach ($case in $cases.Values) { if ((Get-PreflightStatus -State $case.State) -ne $case.Expected) { $pass = $false } }
    "PREFLIGHT_REGRESSION_PASS=$([int]$pass)"
    exit $(if ($pass) { 0 } else { 1 })
}

if ([string]::IsNullOrWhiteSpace($ResultPath)) { $ResultPath = Join-Path $OutputDirectory 'preflight_result.json' }
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
$sourceSha = Get-Sha256Hex -Path $SourcePath
$docxSha = Get-Sha256Hex -Path $DocxPath
$markup = Get-DocxMarkupState -Path $DocxPath
$printers = Get-PrinterInventoryReadOnly
$printer = @($printers | Where-Object { $_.Name -eq 'Microsoft Print to PDF' }) | Select-Object -First 1
$spoolerRunning = [int]((Get-Service -Name Spooler).Status.ToString() -eq 'Running')
$state = @{
    source_sha_match = ($sourceSha -eq $ExpectedSourceSha)
    docx_sha_match = ($docxSha -eq $ExpectedDocxSha)
    docx_zip_readable = ($markup.ZipReadable -eq 1)
    printer_present = ($null -ne $printer)
    printer_driver_match = ($null -ne $printer -and $printer.DriverName -eq 'Microsoft Print To PDF')
    output_exists_before = (Test-Path -LiteralPath $PdfOutputPath)
    spooler_running = ($spoolerRunning -eq 1)
    tracked_insertions_present = ($markup.TrackedInsertionsPresent -eq 1)
    tracked_deletions_present = ($markup.TrackedDeletionsPresent -eq 1)
    comments_present = ($markup.CommentsPresent -eq 1)
}
$status = Get-PreflightStatus -State $state
$result = [ordered]@{
    STAGE = 'G8-DOC-CUMCM-2012-D-001-MANUAL-PRINT-TO-PDF-PREFLIGHT'
    STATUS = $status
    TARGET_PAPER_ID = $TargetPaperId
    ORIGINAL_SOURCE_SHA_MATCH = [int]$state.source_sha_match
    REBUILT_DOCX_SHA_MATCH = [int]$state.docx_sha_match
    DOCX_EXISTS = [int](Test-Path -LiteralPath $DocxPath)
    DOCX_SIZE = (Get-Item -LiteralPath $DocxPath).Length
    DOCX_SHA256 = $docxSha
    DOCX_ZIP_READABLE = [int]$state.docx_zip_readable
    MICROSOFT_PRINT_TO_PDF_PRESENT = [int]$state.printer_present
    MICROSOFT_PRINT_TO_PDF_DRIVER_MATCH = [int]$state.printer_driver_match
    MICROSOFT_PRINT_TO_PDF_PORT_MATCH = [int]($null -ne $printer -and $printer.PortName -eq 'PORTPROMPT:')
    PRINT_SPOOLER_RUNNING = $spoolerRunning
    PDF_OUTPUT_PATH = $PdfOutputPath
    PDF_OUTPUT_EXISTS_BEFORE = [int]$state.output_exists_before
    TRACKED_INSERTIONS_PRESENT = [int]$state.tracked_insertions_present
    TRACKED_DELETIONS_PRESENT = [int]$state.tracked_deletions_present
    COMMENTS_PRESENT = [int]$state.comments_present
    MANUAL_PRINT_MARKUP_STATE_REQUIRES_DECISION = [int]($state.tracked_insertions_present -or $state.tracked_deletions_present -or $state.comments_present)
    PREFLIGHT_PASS = [int]($status -eq 'PASS')
    WORD_RUN = 0
    PRINT_JOB_RUN = 0
    PDF_GENERATION_RUN = 0
    NETWORK_ACCESS_USED = 0
    NEW_DEPENDENCY_INSTALLED = 0
    PREFLIGHT_TIMESTAMP = (Get-Date).ToString('o')
}
$json = $result | ConvertTo-Json -Depth 4
[System.IO.File]::WriteAllText($ResultPath, $json + [Environment]::NewLine, [System.Text.Encoding]::UTF8)
$result | ConvertTo-Json -Depth 4
exit $(if ($status -eq 'PASS') { 0 } elseif ($status -eq 'BLOCKED') { 2 } else { 1 })
