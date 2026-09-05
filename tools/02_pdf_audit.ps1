# G4-00: PDF Audit PowerShell Wrapper
param(
    [string]$Pdf,
    [switch]$DryRun,
    [switch]$SmokeTest,
    [int]$Count = 3
)
$PythonPath = "D:\python\python.exe"
$ScriptPath = Join-Path $PSScriptRoot "02_pdf_audit.py"
if (-not (Test-Path $PythonPath)) {
    Write-Error "Python not found at $PythonPath"
    exit 1
}
$Args = @()
if ($Pdf) { $Args += "--pdf", $Pdf }
if ($DryRun) { $Args += "--dry-run" }
if ($SmokeTest) { $Args += "--smoke-test" }
if ($Count -ne 3) { $Args += "--count", $Count }
& $PythonPath $ScriptPath @Args
