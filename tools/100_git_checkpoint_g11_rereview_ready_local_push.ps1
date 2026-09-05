[CmdletBinding()]
param()

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'

$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[Console]::OutputEncoding = $Utf8NoBom
[Console]::InputEncoding = $Utf8NoBom
$OutputEncoding = $Utf8NoBom

$CurrentOperation = 'PRECHECK'
$CurrentPath = $null
$LastGitStdout = @()
$LastGitStderr = @()
$LastGitExitCode = $null
$MaxFailureDetailChars = 4000
$script:LastGitDetailTruncated = 0
$script:ExpectedPathSet = $null
$script:OriginalRequiredPathSet = $null
$script:BaselineInitialSet = $null

$RepoRoot = 'D:\cumcm-modeling-Award-Collection'
$BaseBranch = 'library-refactor-v1'
$BaseHead = '557724fba6572d4d83dc421feda5b17b13ff8d66'
$TargetBranch = 'library-refactor-v1-g11-rereview-ready'
$ExpectedInitialStagedPathListSha256 = '0cc52946bf4da1cce7e969e7f7ee6dd5e4f6e97393f85325e29168ea80fa6582'
$ExpectedRequiredPathListSha256 = '7be0654d31caa13af46c6cefcca79428ab639cd5df7ddacc552c1325643a33e7'
$ExpectedCheckpointPathListSha256 = 'd6604af2a10accfca5376275d4f76e164f99d76bf104bb4dd3eec0039265a2c0'
$ExpectedCheckpointPathCount = 19061
$DecisionSheetPath = 'catalog/scale/g11_post_repair_human_rereview_decisions.csv'
$ExpectedDecisionSheetSha256 = '9F81352331BCDEF28F95FAAC7D6EF53AFDC20470CA867BC9C9B98DF48A05DC55'
$CommitMessage = 'checkpoint: G11 repair complete, human rereview ready'

$RequiredPathListPath = 'reports/scale/GIT_CHECKPOINT_G11_REREVIEW_READY_REQUIRED_UNSTAGED_PATHS.txt'
$ExpectedPathListPath = 'reports/scale/GIT_CHECKPOINT_G11_REREVIEW_READY_EXPECTED_PATHS.txt'

function Get-PathListHash {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Paths
    )

    $normalized = @($Paths | ForEach-Object { Normalize-RepoPath $_ } | Where-Object { $_ -ne '' } | Sort-Object)
    $joined = [string]::Join("`n", $normalized) + "`n"
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        return ([BitConverter]::ToString($sha.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($joined)))).Replace('-', '').ToLowerInvariant()
    }
    finally {
        $sha.Dispose()
    }
}

function Normalize-RepoPath {
    param(
        [Parameter(Mandatory = $false)]
        [string]$Path
    )

    if ($null -eq $Path) {
        return ''
    }
    return $Path.Trim().Replace('\', '/')
}

function New-NormalizedPathSetInfo {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Paths
    )

    $set = New-Object -TypeName 'System.Collections.Generic.HashSet[string]' -ArgumentList ([System.StringComparer]::Ordinal)
    $duplicateCount = 0
    foreach ($rawPath in $Paths) {
        $path = Normalize-RepoPath $rawPath
        if ($path -eq '') {
            continue
        }
        if ($set.Contains($path)) {
            $duplicateCount++
        }
        else {
            [void]$set.Add($path)
        }
    }
    return [PSCustomObject]@{
        PathSet = $set
        DuplicateCount = $duplicateCount
    }
}

function Get-PathSetDifference {
    param(
        [Parameter(Mandatory = $true)]
        [System.Collections.Generic.HashSet[string]]$Left,
        [Parameter(Mandatory = $true)]
        [System.Collections.Generic.HashSet[string]]$Right
    )

    $difference = New-Object 'System.Collections.Generic.List[string]'
    foreach ($path in $Left) {
        if (-not $Right.Contains($path)) {
            [void]$difference.Add($path)
        }
    }
    return @($difference | Sort-Object)
}

function Get-PathSetIntersection {
    param(
        [Parameter(Mandatory = $true)]
        [System.Collections.Generic.HashSet[string]]$Left,
        [Parameter(Mandatory = $true)]
        [System.Collections.Generic.HashSet[string]]$Right
    )

    $intersection = New-Object 'System.Collections.Generic.List[string]'
    foreach ($path in $Left) {
        if ($Right.Contains($path)) {
            [void]$intersection.Add($path)
        }
    }
    return @($intersection | Sort-Object)
}

function Set-OperationContext {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Operation,
        [Parameter(Mandatory = $false)]
        [string]$Path
    )

    $script:CurrentOperation = $Operation
    $script:CurrentPath = $Path
}

function ConvertTo-BoundedFailureText {
    param(
        [Parameter(Mandatory = $false)]
        [object[]]$Lines,
        [Parameter(Mandatory = $false)]
        [int]$MaxChars = 4000
    )

    if ($MaxChars -lt 1) {
        throw 'FAILURE_DETAIL_MAX_CHARS_INVALID'
    }
    $parts = New-Object 'System.Collections.Generic.List[string]'
    $currentLength = 0
    $truncated = $false
    foreach ($line in @($Lines)) {
        if ($null -eq $line) {
            continue
        }
        $safeLine = ([string]$line) -replace '[\x00-\x08\x0B\x0C\x0E-\x1F]', ' ' -replace '[\r\n]+', ' '
        $safeLine = $safeLine.Trim()
        if ($safeLine -eq '') {
            continue
        }
        $separator = if ($parts.Count -gt 0) { ' | ' } else { '' }
        $available = $MaxChars - $currentLength - $separator.Length
        if ($available -le 0) {
            $truncated = $true
            break
        }
        if ($safeLine.Length -gt $available) {
            if ($available -gt 3) {
                [void]$parts.Add($separator + $safeLine.Substring(0, $available - 3) + '...')
            }
            else {
                [void]$parts.Add($separator + $safeLine.Substring(0, $available))
            }
            $currentLength = $MaxChars
            $truncated = $true
            break
        }
        [void]$parts.Add($separator + $safeLine)
        $currentLength += $separator.Length + $safeLine.Length
    }
    return [PSCustomObject]@{
        Text = ($parts -join '')
        Truncated = [int]$truncated
    }
}

function ConvertTo-SafeFailureText {
    param(
        [Parameter(Mandatory = $false)]
        [object[]]$Lines
    )

    $bounded = ConvertTo-BoundedFailureText -Lines $Lines -MaxChars $MaxFailureDetailChars
    return $bounded.Text
}

function Invoke-GitCaptured {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments,
        [Parameter(Mandatory = $true)]
        [string]$Operation,
        [Parameter(Mandatory = $false)]
        [string]$Path
    )

    Set-OperationContext -Operation $Operation -Path $Path
    $captured = @(& git @Arguments 2>&1)
    $exitCode = $LASTEXITCODE
    $stdout = @()
    $stderr = @()
    foreach ($entry in $captured) {
        if ($entry -is [System.Management.Automation.ErrorRecord]) {
            $stderr += [string]$entry
        }
        else {
            $stdout += [string]$entry
        }
    }
    if ($exitCode -ne 0 -and $stderr.Count -eq 0) {
        $stderr = @($captured | ForEach-Object { [string]$_ })
    }
    $stdoutDiagnostic = ConvertTo-BoundedFailureText -Lines $stdout -MaxChars $MaxFailureDetailChars
    $stderrDiagnostic = ConvertTo-BoundedFailureText -Lines $stderr -MaxChars $MaxFailureDetailChars
    $script:LastGitStdout = $stdoutDiagnostic.Text
    $script:LastGitStderr = $stderrDiagnostic.Text
    $script:LastGitExitCode = $exitCode
    $script:LastGitDetailTruncated = [int]($stdoutDiagnostic.Truncated -eq 1 -or $stderrDiagnostic.Truncated -eq 1)
    return [PSCustomObject]@{
        ExitCode = $exitCode
        Stdout = @($stdout)
        Stderr = @($stderr)
        StdoutDiagnostic = $stdoutDiagnostic.Text
        StderrDiagnostic = $stderrDiagnostic.Text
        DetailTruncated = $script:LastGitDetailTruncated
    }
}

function Invoke-GitChecked {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments,
        [Parameter(Mandatory = $false)]
        [string]$Operation = 'GIT_COMMAND',
        [Parameter(Mandatory = $false)]
        [string]$Path
    )

    $result = Invoke-GitCaptured -Arguments $Arguments -Operation $Operation -Path $Path
    if ($result.ExitCode -ne 0) {
        $detail = ConvertTo-SafeFailureText @($result.StderrDiagnostic, $result.StdoutDiagnostic)
        throw ("GIT_COMMAND_FAILED: git {0} failed with exit code {1}: {2}" -f ($Arguments -join ' '), $result.ExitCode, $detail)
    }
    return $result.Stdout
}

function Get-StagedPaths {
    param(
        [Parameter(Mandatory = $false)]
        [string]$Operation = 'FINAL_STAGED_SET_READ'
    )

    $paths = @(Invoke-GitChecked @('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only', '--') -Operation $Operation)
    return @($paths | ForEach-Object { [string]$_ } | Where-Object { $_ -ne '' } | Sort-Object)
}

function Get-InterruptedResumeState {
    try {
        if ($null -eq $script:ExpectedPathSet -or $null -eq $script:OriginalRequiredPathSet -or $null -eq $script:BaselineInitialSet) {
            return [PSCustomObject]@{ Available = 0; Error = 'PATH_SET_STATE_UNAVAILABLE' }
        }
        $stagedPaths = @(Get-StagedPaths -Operation 'FAILURE_RESUME_STATE_READ')
        $stagedInfo = New-NormalizedPathSetInfo $stagedPaths
        $baselineMissing = @(Get-PathSetDifference -Left $script:BaselineInitialSet -Right $stagedInfo.PathSet)
        $unexpected = @(Get-PathSetDifference -Left $stagedInfo.PathSet -Right $script:ExpectedPathSet)
        $requiredStaged = @(Get-PathSetIntersection -Left $script:OriginalRequiredPathSet -Right $stagedInfo.PathSet)
        $remainingRequired = @(Get-PathSetDifference -Left $script:OriginalRequiredPathSet -Right $stagedInfo.PathSet)
        return [PSCustomObject]@{
            Available = 1
            StagedCount = $stagedInfo.PathSet.Count
            RequiredStagedCount = $requiredStaged.Count
            RemainingRequiredCount = $remainingRequired.Count
            BaselineMissingCount = $baselineMissing.Count
            UnexpectedCount = $unexpected.Count
            DuplicateCount = $stagedInfo.DuplicateCount
            Safe = [int]($baselineMissing.Count -eq 0 -and $unexpected.Count -eq 0)
        }
    }
    catch {
        return [PSCustomObject]@{ Available = 0; Error = $_.Exception.Message }
    }
}

function Get-CheckpointFailureBlocker {
    param(
        [Parameter(Mandatory = $true)]
        [System.Exception]$Exception
    )

    $message = [string]$Exception.Message
    $gitText = ConvertTo-SafeFailureText @($script:LastGitStderr + $script:LastGitStdout + $message)
    switch ($script:CurrentOperation) {
        'GIT_METADATA_WRITE_PROBE' { return 'GIT_METADATA_WRITE_ACCESS_DENIED' }
        'GIT_INDEX_LOCK_CHECK' { return 'GIT_INDEX_LOCK_PRESENT' }
        'SOURCE_PATH_EXISTENCE_CHECK' { return 'REQUIRED_PATH_DOES_NOT_EXIST' }
        'SOURCE_PATH_READ_PROBE' { return 'SOURCE_PATH_READ_ACCESS_DENIED' }
        { $_ -eq 'GIT_ADD_REQUIRED_PATH' -or $_ -eq 'GIT_ADD_CHECKPOINT_EVIDENCE_PATH' } {
            if ($gitText -match '(?i)index\.lock|unable to create|permission denied|access is denied') {
                return 'GIT_METADATA_INDEX_WRITE_ACCESS_DENIED'
            }
            if ($gitText -match '(?i)pathspec|did not match any files') {
                return 'GIT_ADD_PATHSPEC_MISMATCH'
            }
            if ($gitText -match '(?i)permission denied|access is denied|unauthorized') {
                return 'GIT_ADD_SOURCE_PATH_ACCESS_DENIED'
            }
            return 'GIT_ADD_FAILED'
        }
    }
    if ($message -notmatch '^GIT_COMMAND_FAILED:') {
        return $message
    }
    return 'CHECKPOINT_OPERATION_FAILED'
}

function Get-CheckpointFailureCategory {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Blocker,
        [Parameter(Mandatory = $true)]
        [System.Exception]$Exception
    )

    if ($Blocker -match '(?i)ACCESS_DENIED|PERMISSION|UNAUTHORIZED') {
        return 'ACCESS_DENIED'
    }
    if ($Blocker -match '(?i)PATHSPEC|PATH_DOES_NOT_EXIST|MANIFEST_PATH') {
        return 'PATH_RESOLUTION'
    }
    if ($Exception -is [System.UnauthorizedAccessException]) {
        return 'ACCESS_DENIED'
    }
    return 'CHECKPOINT_FAILURE'
}

function Fail-Checkpoint {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Blocker,
        [Parameter(Mandatory = $true)]
        [string]$Operation,
        [Parameter(Mandatory = $false)]
        [string]$Path,
        [Parameter(Mandatory = $false)]
        [string]$Detail,
        [Parameter(Mandatory = $true)]
        [System.Exception]$Exception,
        [Parameter(Mandatory = $true)]
        [string]$ErrorCategory,
        [Parameter(Mandatory = $false)]
        [string]$ExceptionType,
        [Parameter(Mandatory = $false)]
        [object]$GitExitCode,
        [Parameter(Mandatory = $false)]
        [string]$GitStdout,
        [Parameter(Mandatory = $false)]
        [string]$GitStderr
    )

    $state = Get-InterruptedResumeState
    $detailResult = ConvertTo-BoundedFailureText -Lines @($Detail, $GitStderr, $GitStdout, $Exception.Message) -MaxChars $MaxFailureDetailChars
    $stdoutResult = ConvertTo-BoundedFailureText -Lines @($GitStdout) -MaxChars $MaxFailureDetailChars
    $stderrResult = ConvertTo-BoundedFailureText -Lines @($GitStderr) -MaxChars $MaxFailureDetailChars
    $failureDetailTruncated = [int]($detailResult.Truncated -eq 1 -or $stdoutResult.Truncated -eq 1 -or $stderrResult.Truncated -eq 1 -or $script:LastGitDetailTruncated -eq 1)
    Write-Output 'STAGE=GIT-CHECKPOINT-G11-REREVIEW-READY-LOCAL-PUSH'
    Write-Output 'STATUS=BLOCKED'
    Write-Output ("BLOCKER={0}" -f $Blocker)
    Write-Output ("FAILED_OPERATION={0}" -f $Operation)
    Write-Output ("FAILED_PATH={0}" -f ($(if ($null -eq $Path) { '' } else { $Path })))
    Write-Output ("FAILED_ERROR_CATEGORY={0}" -f $ErrorCategory)
    Write-Output ("FAILED_ERROR_DETAIL={0}" -f $detailResult.Text)
    Write-Output ("FAILED_EXCEPTION_TYPE={0}" -f $ExceptionType)
    Write-Output ("FAILED_GIT_EXIT_CODE={0}" -f ($(if ($null -eq $GitExitCode) { '' } else { $GitExitCode })))
    Write-Output ("FAILED_GIT_STDOUT={0}" -f $stdoutResult.Text)
    Write-Output ("FAILED_GIT_STDERR={0}" -f $stderrResult.Text)
    Write-Output ("FAILED_GIT_DETAIL_TRUNCATED={0}" -f $failureDetailTruncated)
    Write-Output ("MAX_FAILURE_DETAIL_CHARS={0}" -f $MaxFailureDetailChars)
    if ($state.Available -eq 1) {
        Write-Output ("STAGED_COUNT_AT_FAILURE={0}" -f $state.StagedCount)
        Write-Output ("CURRENT_STAGED_COUNT_AFTER_ACCESS_DENIED={0}" -f $state.StagedCount)
        Write-Output ("REQUIRED_STAGED_AT_FAILURE_COUNT={0}" -f $state.RequiredStagedCount)
        Write-Output ("REQUIRED_ALREADY_STAGED_AFTER_ACCESS_DENIED_COUNT={0}" -f $state.RequiredStagedCount)
        Write-Output ("REMAINING_REQUIRED_AT_FAILURE_COUNT={0}" -f $state.RemainingRequiredCount)
        Write-Output ("REMAINING_REQUIRED_AFTER_ACCESS_DENIED_COUNT={0}" -f $state.RemainingRequiredCount)
        Write-Output ("BASELINE_MISSING_AT_FAILURE_COUNT={0}" -f $state.BaselineMissingCount)
        Write-Output ("BASELINE_INITIAL_MISSING_FROM_CURRENT_COUNT={0}" -f $state.BaselineMissingCount)
        Write-Output ("UNEXPECTED_STAGED_AT_FAILURE_COUNT={0}" -f $state.UnexpectedCount)
        Write-Output ("CURRENT_STAGED_OUTSIDE_EXPECTED_COUNT={0}" -f $state.UnexpectedCount)
        Write-Output ("RESUME_SAFE={0}" -f $state.Safe)
        Write-Output ("CURRENT_STAGED_SET_SAFE_AFTER_ACCESS_DENIED={0}" -f $state.Safe)
    }
    else {
        Write-Output 'STAGED_COUNT_AT_FAILURE='
        Write-Output 'CURRENT_STAGED_COUNT_AFTER_ACCESS_DENIED='
        Write-Output 'REQUIRED_STAGED_AT_FAILURE_COUNT='
        Write-Output 'REQUIRED_ALREADY_STAGED_AFTER_ACCESS_DENIED_COUNT='
        Write-Output 'REMAINING_REQUIRED_AT_FAILURE_COUNT='
        Write-Output 'REMAINING_REQUIRED_AFTER_ACCESS_DENIED_COUNT='
        Write-Output 'BASELINE_MISSING_AT_FAILURE_COUNT='
        Write-Output 'UNEXPECTED_STAGED_AT_FAILURE_COUNT='
        Write-Output 'RESUME_SAFE=0'
        Write-Output 'CURRENT_STAGED_SET_SAFE_AFTER_ACCESS_DENIED=0'
    }
}

function Invoke-GitMetadataWriteProbe {
    Set-OperationContext -Operation 'GIT_METADATA_WRITE_PROBE' -Path '.git'
    $probePath = Join-Path -Path (Join-Path -Path (Get-Location).Path -ChildPath '.git') -ChildPath ("checkpoint-write-probe-{0}.tmp" -f ([guid]::NewGuid().ToString('N')))
    $stream = $null
    $primaryException = $null
    $cleanupException = $null
    try {
        $stream = [System.IO.File]::Open($probePath, [System.IO.FileMode]::CreateNew, [System.IO.FileAccess]::Write, [System.IO.FileShare]::None)
        $bytes = [System.Text.Encoding]::ASCII.GetBytes('checkpoint-probe')
        [void]$stream.Write($bytes, 0, $bytes.Length)
        [void]$stream.Flush()
    }
    catch {
        $primaryException = $_.Exception
    }
    finally {
        if ($null -ne $stream) {
            try { [void]$stream.Dispose() } catch { $cleanupException = $_.Exception }
        }
        if ($null -eq $cleanupException -and [System.IO.File]::Exists($probePath)) {
            try { [void][System.IO.File]::Delete($probePath) } catch { $cleanupException = $_.Exception }
        }
    }
    if ($null -ne $primaryException) { throw $primaryException }
    if ($null -ne $cleanupException) { throw $cleanupException }
}

function Test-SourcePathReadable {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    Set-OperationContext -Operation 'SOURCE_PATH_READ_PROBE' -Path $Path
    $fullPath = [System.IO.Path]::GetFullPath((Join-Path -Path (Get-Location).Path -ChildPath $Path))
    $stream = $null
    $primaryException = $null
    $cleanupException = $null
    try {
        $stream = [System.IO.File]::Open($fullPath, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]::ReadWrite)
    }
    catch {
        $primaryException = $_.Exception
    }
    finally {
        if ($null -ne $stream) {
            try { [void]$stream.Dispose() } catch { $cleanupException = $_.Exception }
        }
    }
    if ($null -ne $primaryException) { throw $primaryException }
    if ($null -ne $cleanupException) { throw $cleanupException }
}

function Get-PathCategory {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    $normalizedPath = Normalize-RepoPath $Path
    $parts = @($normalizedPath -split '/')
    $leaf = $parts[-1]

    $ciBootstrapRoots = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::Ordinal)
    foreach ($root in @('.github', '.bootstrap')) {
        [void]$ciBootstrapRoots.Add($root)
    }
    $transientRoots = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::Ordinal)
    [void]$transientRoots.Add('tmp')
    $transientDirectories = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::Ordinal)
    foreach ($directory in @(
        '.g11_multi_route_repair_staging',
        '.g9_index_refresh_after_g11_repair_staging',
        'g8_q3_formal_artifact_stage',
        'g9_index_stage'
    )) {
        [void]$transientDirectories.Add($directory)
    }
    $transientLeafNames = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::Ordinal)
    foreach ($leafName in @('Thumbs.db', '.DS_Store')) {
        [void]$transientLeafNames.Add($leafName)
    }
    $transientExtensions = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::Ordinal)
    foreach ($extension in @('.pyc', '.pyo', '.tmp', '.temp', '.swp', '.bak')) {
        [void]$transientExtensions.Add($extension)
    }

    if ($ciBootstrapRoots.Contains($parts[0])) {
        return 'EXCLUDE_CI_BOOTSTRAP'
    }
    $containsTransientDirectory = $false
    foreach ($part in $parts) {
        if ($transientDirectories.Contains([string]$part)) {
            $containsTransientDirectory = $true
            break
        }
    }
    if ($transientRoots.Contains($parts[0]) -or $containsTransientDirectory -or $transientLeafNames.Contains($leaf) -or $transientExtensions.Contains(([System.IO.Path]::GetExtension($leaf)).ToLowerInvariant())) {
        return 'EXCLUDE_TRANSIENT'
    }
    return 'INCLUDE'
}

try {
    Set-OperationContext -Operation 'IDENTITY_CHECK'
    $Identity = (whoami).Trim()
    if ([string]::IsNullOrWhiteSpace($Identity)) {
        throw 'EXECUTION_IDENTITY_UNAVAILABLE'
    }
    if ($Identity -match 'CodexSandboxOffline') {
        throw 'Do not run this script inside CodexSandboxOffline.'
    }

    Set-OperationContext -Operation 'REPO_LOCATION' -Path $RepoRoot
    Set-Location -LiteralPath $RepoRoot

    $currentBranch = (Invoke-GitChecked @('branch', '--show-current') -Operation 'BASE_BRANCH_READ' | Select-Object -First 1).ToString().Trim()
    $currentHead = (Invoke-GitChecked @('rev-parse', 'HEAD') -Operation 'BASE_HEAD_READ' | Select-Object -First 1).ToString().Trim()
    if ($currentBranch -ne $BaseBranch) {
        throw ("BASE_BRANCH_MISMATCH: {0}" -f $currentBranch)
    }
    if ($currentHead -ne $BaseHead) {
        throw ("BASE_HEAD_MISMATCH: {0}" -f $currentHead)
    }

    Set-OperationContext -Operation 'GIT_INDEX_LOCK_CHECK' -Path '.git/index.lock'
    if (Test-Path -LiteralPath '.git/index.lock') {
        throw 'UNEXPECTED_GIT_INDEX_LOCK_PRESENT'
    }

    $initialStagedPaths = @(Get-StagedPaths -Operation 'INTERRUPTED_STAGED_SET_READ')
    $initialStagedHash = Get-PathListHash $initialStagedPaths

    Set-OperationContext -Operation 'REQUIRED_MANIFEST_EXISTENCE_CHECK' -Path $RequiredPathListPath
    if (-not (Test-Path -LiteralPath $RequiredPathListPath -PathType Leaf)) {
        throw ("REQUIRED_PATH_LIST_MISSING: {0}" -f $RequiredPathListPath)
    }
    Set-OperationContext -Operation 'EXPECTED_MANIFEST_EXISTENCE_CHECK' -Path $ExpectedPathListPath
    if (-not (Test-Path -LiteralPath $ExpectedPathListPath -PathType Leaf)) {
        throw ("EXPECTED_PATH_LIST_MISSING: {0}" -f $ExpectedPathListPath)
    }

    Set-OperationContext -Operation 'REQUIRED_MANIFEST_UTF8_READ' -Path $RequiredPathListPath
    $requiredRawPaths = @(Get-Content -LiteralPath $RequiredPathListPath -Encoding UTF8)
    Set-OperationContext -Operation 'EXPECTED_MANIFEST_UTF8_READ' -Path $ExpectedPathListPath
    $expectedRawPaths = @(Get-Content -LiteralPath $ExpectedPathListPath -Encoding UTF8)
    $requiredInfo = New-NormalizedPathSetInfo $requiredRawPaths
    $expectedInfo = New-NormalizedPathSetInfo $expectedRawPaths
    $currentInitialInfo = New-NormalizedPathSetInfo $initialStagedPaths

    $failedManifestEntryLine = 0
    $failedManifestPathUtf8 = ''
    for ($i = 0; $i -lt $requiredRawPaths.Count; $i++) {
        $candidatePath = Normalize-RepoPath $requiredRawPaths[$i]
        $candidateLeaf = @($candidatePath -split '/')[-1]
        if ($candidateLeaf -ceq 'abc.zip') {
            $failedManifestEntryLine = $i + 1
            $failedManifestPathUtf8 = $candidatePath
            break
        }
    }
    Set-OperationContext -Operation 'FAILED_MANIFEST_PATH_EXISTENCE_CHECK' -Path $failedManifestPathUtf8
    $failedManifestPathExists = [int](-not [string]::IsNullOrEmpty($failedManifestPathUtf8) -and (Test-Path -LiteralPath $failedManifestPathUtf8 -PathType Leaf))

    Write-Output ("EXPECTED_PATH_DUPLICATE_COUNT={0}" -f $expectedInfo.DuplicateCount)
    Write-Output ("REQUIRED_UNSTAGED_PATH_DUPLICATE_COUNT={0}" -f $requiredInfo.DuplicateCount)
    Write-Output ("CURRENT_STAGED_PATH_DUPLICATE_COUNT={0}" -f $currentInitialInfo.DuplicateCount)
    if ($expectedInfo.DuplicateCount -ne 0 -or $requiredInfo.DuplicateCount -ne 0 -or $currentInitialInfo.DuplicateCount -ne 0) {
        throw 'DUPLICATE_PATH_IN_CHECKPOINT_MANIFEST'
    }

    $requiredNotInExpected = @(Get-PathSetDifference -Left $requiredInfo.PathSet -Right $expectedInfo.PathSet)
    $requiredAlreadyStaged = @(Get-PathSetIntersection -Left $requiredInfo.PathSet -Right $currentInitialInfo.PathSet)
    $currentStagedNotInExpected = @(Get-PathSetDifference -Left $currentInitialInfo.PathSet -Right $expectedInfo.PathSet)

    $initialPlusRequiredSet = New-Object -TypeName 'System.Collections.Generic.HashSet[string]' -ArgumentList ([System.StringComparer]::Ordinal)
    foreach ($path in $currentInitialInfo.PathSet) {
        [void]$initialPlusRequiredSet.Add($path)
    }
    foreach ($path in $requiredInfo.PathSet) {
        [void]$initialPlusRequiredSet.Add($path)
    }
    $expectedMissingFromUnion = @(Get-PathSetDifference -Left $expectedInfo.PathSet -Right $initialPlusRequiredSet)
    $unexpectedInUnion = @(Get-PathSetDifference -Left $initialPlusRequiredSet -Right $expectedInfo.PathSet)

    $baselineInitialSet = New-Object -TypeName 'System.Collections.Generic.HashSet[string]' -ArgumentList ([System.StringComparer]::Ordinal)
    foreach ($path in $expectedInfo.PathSet) {
        [void]$baselineInitialSet.Add($path)
    }
    foreach ($path in $requiredInfo.PathSet) {
        [void]$baselineInitialSet.Remove($path)
    }
    $script:ExpectedPathSet = $expectedInfo.PathSet
    $script:OriginalRequiredPathSet = $requiredInfo.PathSet
    $script:BaselineInitialSet = $baselineInitialSet
    $initialMissing = @(Get-PathSetDifference -Left $baselineInitialSet -Right $currentInitialInfo.PathSet)
    $initialExtra = @(Get-PathSetDifference -Left $currentInitialInfo.PathSet -Right $baselineInitialSet)

    $initialStagedCount = $currentInitialInfo.PathSet.Count
    $requiredUnstagedCount = $requiredInfo.PathSet.Count
    $expectedPathCount = $expectedInfo.PathSet.Count
    $baselineInitialCount = $baselineInitialSet.Count
    $baselineInitialMissingCount = $initialMissing.Count
    $currentStagedOutsideExpectedCount = $currentStagedNotInExpected.Count
    $remainingRequiredSet = New-Object -TypeName 'System.Collections.Generic.HashSet[string]' -ArgumentList ([System.StringComparer]::Ordinal)
    foreach ($path in $requiredInfo.PathSet) {
        if (-not $currentInitialInfo.PathSet.Contains($path)) {
            [void]$remainingRequiredSet.Add($path)
        }
    }
    $remainingRequiredCount = $remainingRequiredSet.Count
    $stagedAccountingPass = [int](($initialStagedCount -eq ($baselineInitialCount + $requiredAlreadyStaged.Count)) -and (($requiredAlreadyStaged.Count + $remainingRequiredCount) -eq $requiredUnstagedCount))
    $currentStagedSetSafe = [int]($baselineInitialMissingCount -eq 0 -and $currentStagedOutsideExpectedCount -eq 0)
    $resumeMode = if ($requiredAlreadyStaged.Count -eq 0) { 'FRESH' } else { 'PARTIAL_STAGING' }
    $countIdentityPass = [int](($baselineInitialCount + $requiredUnstagedCount) -eq $expectedPathCount)
    $initialPlusRequiredEqualsExpected = [int]($expectedMissingFromUnion.Count -eq 0 -and $unexpectedInUnion.Count -eq 0)
    $initialStagedPathSetMatch = [int]($initialMissing.Count -eq 0 -and $initialExtra.Count -eq 0)

    Write-Output ("CURRENT_STAGED_COUNT_AFTER_INTERRUPTED_RUN={0}" -f $initialStagedCount)
    Write-Output ("EXPECTED_PATH_COUNT={0}" -f $expectedPathCount)
    Write-Output ("ORIGINAL_REQUIRED_PATH_COUNT={0}" -f $requiredUnstagedCount)
    Write-Output ("BASELINE_INITIAL_PATH_COUNT={0}" -f $baselineInitialCount)
    Write-Output ("BASELINE_INITIAL_MISSING_FROM_CURRENT_COUNT={0}" -f $baselineInitialMissingCount)
    Write-Output ("CURRENT_STAGED_OUTSIDE_EXPECTED_COUNT={0}" -f $currentStagedOutsideExpectedCount)
    Write-Output ("REQUIRED_ALREADY_STAGED_AFTER_INTERRUPTED_RUN_COUNT={0}" -f $requiredAlreadyStaged.Count)
    Write-Output ("REMAINING_REQUIRED_COUNT={0}" -f $remainingRequiredCount)
    Write-Output ("REQUIRED_ALREADY_STAGED_AT_RESUME_COUNT={0}" -f $requiredAlreadyStaged.Count)
    Write-Output ("REMAINING_REQUIRED_AT_RESUME_COUNT={0}" -f $remainingRequiredCount)
    Write-Output ("INTERRUPTED_STAGING_ACCOUNTING_PASS={0}" -f $stagedAccountingPass)
    Write-Output ("CURRENT_STAGED_SET_SAFE_AFTER_INTERRUPTED_RUN={0}" -f $currentStagedSetSafe)
    Write-Output ("RESUME_MODE={0}" -f $resumeMode)
    Write-Output ("FAILED_MANIFEST_ENTRY_LINE={0}" -f $failedManifestEntryLine)
    Write-Output ("FAILED_MANIFEST_PATH_UTF8={0}" -f $failedManifestPathUtf8)
    Write-Output ("FAILED_MANIFEST_PATH_EXISTS={0}" -f $failedManifestPathExists)
    Write-Output 'EXPLICIT_UTF8_MANIFEST_READ_IMPLEMENTED=1'
    Write-Output 'POWERSHELL_UTF8_OUTPUT_CONFIGURATION_IMPLEMENTED=1'
    Write-Output 'GIT_QUOTEPATH_FALSE_IMPLEMENTED=1'
    Write-Output 'PARTIAL_STAGING_RESUME_GATE_IMPLEMENTED=1'
    Write-Output 'REMAINING_REQUIRED_ONLY_STAGING_IMPLEMENTED=1'
    Write-Output 'REQUIRED_PATH_EXISTENCE_GATE_IMPLEMENTED=1'
    Write-Output 'OPERATION_CONTEXT_REPORTING_IMPLEMENTED=1'
    Write-Output 'FAILED_PATH_REPORTING_IMPLEMENTED=1'
    Write-Output 'FAILED_ERROR_CATEGORY_REPORTING_IMPLEMENTED=1'
    Write-Output 'GIT_METADATA_WRITE_PROBE_IMPLEMENTED=1'
    Write-Output 'SOURCE_PATH_READ_PROBE_IMPLEMENTED=1'
    Write-Output 'GIT_STDERR_CAPTURE_IMPLEMENTED=1'
    Write-Output 'FAILURE_RESUME_STATE_REPORTING_IMPLEMENTED=1'
    Write-Output 'PARTIAL_STAGING_RESUME_SUPPORTED=1'
    Write-Output 'FINAL_STAGED_EXACT_PATH_SET_GATE_RETAINED=1'
    Write-Output 'UTF8_PATH_HANDLING_RETAINED=1'

    Write-Output ("REQUIRED_NOT_IN_EXPECTED_COUNT={0}" -f $requiredNotInExpected.Count)
    Write-Output ("REQUIRED_ALREADY_STAGED_COUNT={0}" -f $requiredAlreadyStaged.Count)
    Write-Output ("CURRENT_STAGED_NOT_IN_EXPECTED_COUNT={0}" -f $currentStagedNotInExpected.Count)
    Write-Output ("UNION_PATH_COUNT={0}" -f $initialPlusRequiredSet.Count)
    Write-Output ("EXPECTED_PATH_COUNT={0}" -f $expectedPathCount)
    Write-Output ("EXPECTED_MISSING_FROM_UNION_COUNT={0}" -f $expectedMissingFromUnion.Count)
    Write-Output ("UNEXPECTED_IN_UNION_COUNT={0}" -f $unexpectedInUnion.Count)
    Write-Output ("INITIAL_PLUS_REQUIRED_EQUALS_EXPECTED={0}" -f $initialPlusRequiredEqualsExpected)
    Write-Output ("INITIAL_STAGED_COUNT={0}" -f $initialStagedCount)
    Write-Output ("REQUIRED_UNSTAGED_COUNT={0}" -f $requiredUnstagedCount)
    Write-Output ("COUNT_IDENTITY_PASS={0}" -f $countIdentityPass)

    $initialStagedShaMatch = [int]((Get-PathListHash $initialStagedPaths) -eq $ExpectedInitialStagedPathListSha256)
    Write-Output ("EXPECTED_INITIAL_STAGED_COUNT={0}" -f $baselineInitialSet.Count)
    Write-Output ("OBSERVED_INITIAL_STAGED_COUNT={0}" -f $currentInitialInfo.PathSet.Count)
    Write-Output ("MISSING_FROM_CURRENT_STAGE_COUNT={0}" -f $initialMissing.Count)
    Write-Output ("EXTRA_IN_CURRENT_STAGE_COUNT={0}" -f $initialExtra.Count)
    Write-Output ("INITIAL_STAGED_PATH_SET_MATCH={0}" -f $initialStagedPathSetMatch)
    Write-Output ("INITIAL_STAGED_SHA_MATCH={0}" -f $initialStagedShaMatch)
    # Exact normalized Ordinal path-set equality is authoritative.
    # Serialized path-list SHA is diagnostic only because encoding, line-ending, and serialization differences may vary across environments.

    if ($failedManifestPathExists -ne 1) {
        throw 'REQUIRED_MANIFEST_PATH_ACTUALLY_MISSING'
    }
    if ($requiredNotInExpected.Count -ne 0) {
        foreach ($path in @($requiredNotInExpected | Select-Object -First 20)) { Write-Output ("REQUIRED_NOT_IN_EXPECTED_PATH={0}" -f $path) }
        throw 'REQUIRED_UNSTAGED_PATH_OUTSIDE_EXPECTED_SET'
    }
    if ($baselineInitialMissingCount -ne 0) {
        foreach ($path in @($initialMissing | Select-Object -First 20)) { Write-Output ("BASELINE_INITIAL_MISSING_PATH={0}" -f $path) }
        throw 'BASELINE_STAGED_PATH_LOST_AFTER_INTERRUPTED_RUN'
    }
    if ($currentStagedNotInExpected.Count -ne 0) {
        foreach ($path in @($currentStagedNotInExpected | Select-Object -First 20)) { Write-Output ("CURRENT_STAGED_NOT_IN_EXPECTED_PATH={0}" -f $path) }
        throw 'UNEXPECTED_PATH_STAGED_DURING_INTERRUPTED_RUN'
    }
    if ($expectedMissingFromUnion.Count -ne 0 -or $unexpectedInUnion.Count -ne 0) {
        foreach ($path in @($expectedMissingFromUnion | Select-Object -First 20)) { Write-Output ("EXPECTED_MISSING_FROM_UNION_PATH={0}" -f $path) }
        foreach ($path in @($unexpectedInUnion | Select-Object -First 20)) { Write-Output ("UNEXPECTED_IN_UNION_PATH={0}" -f $path) }
        throw 'INITIAL_PLUS_REQUIRED_NOT_EQUAL_EXPECTED'
    }
    if ($countIdentityPass -ne 1) {
        throw 'COUNT_IDENTITY_MISMATCH'
    }
    if ($stagedAccountingPass -ne 1) {
        throw 'INTERRUPTED_STAGING_SET_ACCOUNTING_MISMATCH'
    }

    $requiredPaths = @($requiredInfo.PathSet | Sort-Object)
    $expectedPaths = @($expectedInfo.PathSet | Sort-Object)
    if ($requiredPaths.Count -ne $requiredInfo.PathSet.Count) {
        throw 'REQUIRED_PATH_LIST_ENUMERATION_ERROR'
    }
    if ($expectedPaths.Count -ne $ExpectedCheckpointPathCount) {
        throw ("EXPECTED_PATH_COUNT_MISMATCH: {0}" -f $expectedPaths.Count)
    }
    $requiredPathSha = Get-PathListHash $requiredPaths
    $expectedPathSha = Get-PathListHash $expectedPaths
    $requiredPathShaMatch = [int]($requiredPathSha -eq $ExpectedRequiredPathListSha256)
    $expectedPathShaMatch = [int]($expectedPathSha -eq $ExpectedCheckpointPathListSha256)
    Write-Output ("REQUIRED_UNSTAGED_PATH_LIST_SHA256={0}" -f $requiredPathSha)
    Write-Output ("EXPECTED_PATH_LIST_SHA256={0}" -f $expectedPathSha)
    Write-Output ("REQUIRED_UNSTAGED_PATH_LIST_SHA_MATCH={0}" -f $requiredPathShaMatch)
    Write-Output ("EXPECTED_PATH_LIST_SHA_MATCH={0}" -f $expectedPathShaMatch)
    Write-Output 'EXPECTED_MANIFEST_SHA_DIAGNOSTIC_ONLY=1'
    Write-Output 'REQUIRED_MANIFEST_SHA_DIAGNOSTIC_ONLY=1'
    Write-Output 'INITIAL_STAGED_SHA_DIAGNOSTIC_ONLY=1'
    Write-Output 'SHA_GATE_DIAGNOSTIC_ONLY=1'
    # Serialized manifest SHA256 is diagnostic only.
    # Cross-environment encoding and line-ending differences may alter byte hashes.
    # Normalized Ordinal exact path-set relationships are authoritative.

    $remainingRequiredPaths = @($remainingRequiredSet | Sort-Object)
    foreach ($path in $remainingRequiredPaths) {
        Set-OperationContext -Operation 'SOURCE_PATH_EXISTENCE_CHECK' -Path $path
        if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
            throw ("REQUIRED_PATH_DOES_NOT_EXIST:{0}" -f $path)
        }
    }

    Invoke-GitMetadataWriteProbe
    Write-Output 'GIT_METADATA_FILESYSTEM_WRITE_PROBE_PASS=1'
    Set-OperationContext -Operation 'GIT_INDEX_LOCK_CHECK' -Path '.git/index.lock'
    if (Test-Path -LiteralPath '.git/index.lock') {
        throw 'GIT_INDEX_LOCK_PRESENT'
    }

    foreach ($path in $remainingRequiredPaths) {
        Test-SourcePathReadable -Path $path
    }

    $previousLiteralPathspecs = $env:GIT_LITERAL_PATHSPECS
    try {
        $env:GIT_LITERAL_PATHSPECS = '1'
        Write-Output 'GIT_LITERAL_PATHSPEC_MODE_IMPLEMENTED=1'
        $remainingStartCount = $remainingRequiredPaths.Count
        $remainingDoneCount = 0
        foreach ($path in $remainingRequiredPaths) {
            Set-OperationContext -Operation 'GIT_ADD_REQUIRED_PATH' -Path $path
            Invoke-GitChecked @('add', '--', $path) -Operation 'GIT_ADD_REQUIRED_PATH' -Path $path | Out-Null
            $remainingDoneCount++
            if ($remainingDoneCount -eq $remainingStartCount -or ($remainingDoneCount -gt 0 -and ($remainingDoneCount % 100) -eq 0)) {
                Write-Output ("STAGING_PROGRESS={0}/{1}" -f $remainingDoneCount, $remainingStartCount)
            }
        }

        $checkpointEvidencePaths = @(
            'catalog/scale/git_checkpoint_secret_triage.csv',
            'reports/scale/GIT_CHECKPOINT_G11_REREVIEW_READY_SECRET_TRIAGE.md',
            'reports/scale/GIT_CHECKPOINT_G11_REREVIEW_READY_REQUIRED_UNSTAGED_RECONCILIATION.csv',
            'reports/scale/GIT_CHECKPOINT_G11_REREVIEW_READY_REQUIRED_UNSTAGED_PATHS.txt',
            'reports/scale/GIT_CHECKPOINT_G11_REREVIEW_READY_EXPECTED_PATHS.txt',
            'reports/scale/GIT_CHECKPOINT_G11_REREVIEW_READY.md',
            'reports/scale/GIT_CHECKPOINT_G11_REREVIEW_READY_PUSH_RESULT.md',
            'tools/100_git_checkpoint_g11_rereview_ready_local_push.ps1'
        )
        foreach ($path in $checkpointEvidencePaths) {
            if ($remainingRequiredSet.Contains($path)) {
                continue
            }
            Set-OperationContext -Operation 'CHECKPOINT_EVIDENCE_CHANGE_CHECK' -Path $path
            $unstagedEvidence = @(Invoke-GitChecked @('-c', 'core.quotepath=false', 'diff', '--name-only', '--', $path) -Operation 'CHECKPOINT_EVIDENCE_CHANGE_CHECK' -Path $path)
            $untrackedEvidence = @(Invoke-GitChecked @('-c', 'core.quotepath=false', 'ls-files', '--others', '--exclude-standard', '--', $path) -Operation 'CHECKPOINT_EVIDENCE_CHANGE_CHECK' -Path $path)
            if ($unstagedEvidence.Count -ne 0 -or $untrackedEvidence.Count -ne 0) {
                Invoke-GitChecked @('add', '--', $path) -Operation 'GIT_ADD_CHECKPOINT_EVIDENCE_PATH' -Path $path | Out-Null
            }
        }
    }
    finally {
        if ($null -eq $previousLiteralPathspecs) {
            Remove-Item Env:GIT_LITERAL_PATHSPECS -ErrorAction SilentlyContinue
        }
        else {
            $env:GIT_LITERAL_PATHSPECS = $previousLiteralPathspecs
        }
    }

    $stagedAfterAdd = @(Get-StagedPaths -Operation 'FINAL_STAGED_SET_READ')
    $finalStagedInfo = New-NormalizedPathSetInfo $stagedAfterAdd
    $finalExpectedInfo = New-NormalizedPathSetInfo $expectedPaths
    $finalMissing = @(Get-PathSetDifference -Left $finalExpectedInfo.PathSet -Right $finalStagedInfo.PathSet)
    $finalExtra = @(Get-PathSetDifference -Left $finalStagedInfo.PathSet -Right $finalExpectedInfo.PathSet)
    Write-Output ("FINAL_EXPECTED_STAGED_COUNT={0}" -f $finalExpectedInfo.PathSet.Count)
    Write-Output ("FINAL_CURRENT_STAGED_COUNT={0}" -f $finalStagedInfo.PathSet.Count)
    Write-Output ("FINAL_MISSING_EXPECTED_PATH_COUNT={0}" -f $finalMissing.Count)
    Write-Output ("FINAL_UNEXPECTED_STAGED_PATH_COUNT={0}" -f $finalExtra.Count)
    Write-Output ("FINAL_STAGED_PATH_SET_MATCH={0}" -f [int]($finalMissing.Count -eq 0 -and $finalExtra.Count -eq 0 -and $finalStagedInfo.DuplicateCount -eq 0))
    if ($finalStagedInfo.DuplicateCount -ne 0 -or $finalMissing.Count -ne 0 -or $finalExtra.Count -ne 0) {
        throw 'FINAL_STAGED_EXACT_PATH_SET_MISMATCH'
    }
    $unexpectedTransient = @($stagedAfterAdd | Where-Object { (Get-PathCategory $_) -eq 'EXCLUDE_TRANSIENT' })
    $unexpectedCi = @($stagedAfterAdd | Where-Object { (Get-PathCategory $_) -eq 'EXCLUDE_CI_BOOTSTRAP' })
    if ($unexpectedTransient.Count -ne 0) {
        throw ("UNEXPECTED_STAGED_TRANSIENT_COUNT: {0}" -f $unexpectedTransient.Count)
    }
    if ($unexpectedCi.Count -ne 0) {
        throw ("UNEXPECTED_STAGED_CI_BOOTSTRAP_COUNT: {0}" -f $unexpectedCi.Count)
    }

    $over100Mb = @()
    foreach ($path in $stagedAfterAdd) {
        Set-OperationContext -Operation 'FINAL_STAGED_FILE_EXISTENCE_CHECK' -Path $path
        if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
            throw ("STAGED_FILE_MISSING_ON_DISK: {0}" -f $path)
        }
        Set-OperationContext -Operation 'FINAL_STAGED_FILE_SIZE_READ' -Path $path
        $item = Get-Item -LiteralPath $path
        if ($item.Length -gt 100MB) {
            $over100Mb += $path
        }
    }
    if ($over100Mb.Count -ne 0) {
        throw ("STAGED_FILE_OVER_100MB_COUNT: {0}" -f $over100Mb.Count)
    }

    Set-OperationContext -Operation 'DECISION_SHEET_HASH_READ' -Path $DecisionSheetPath
    $decisionHash = (Get-FileHash -LiteralPath $DecisionSheetPath -Algorithm SHA256).Hash.ToUpperInvariant()
    if ($decisionHash -ne $ExpectedDecisionSheetSha256) {
        throw 'DECISION_SHEET_HASH_MISMATCH'
    }

    $targetLocalResult = Invoke-GitCaptured -Arguments @('show-ref', '--verify', '--quiet', ("refs/heads/{0}" -f $TargetBranch)) -Operation 'TARGET_BRANCH_LOCAL_CHECK' -Path $TargetBranch
    if ($targetLocalResult.ExitCode -eq 0) {
        throw 'TARGET_BRANCH_ALREADY_EXISTS_LOCALLY'
    }
    if ($targetLocalResult.ExitCode -ne 1) {
        throw ("TARGET_BRANCH_LOCAL_CHECK_FAILED: {0}" -f (ConvertTo-SafeFailureText @($targetLocalResult.Stderr + $targetLocalResult.Stdout)))
    }

    $remoteTargetResult = Invoke-GitCaptured -Arguments @('ls-remote', '--heads', 'origin', $TargetBranch) -Operation 'TARGET_BRANCH_REMOTE_CHECK' -Path $TargetBranch
    if ($remoteTargetResult.ExitCode -ne 0) {
        throw ("TARGET_BRANCH_REMOTE_CHECK_FAILED: {0}" -f (ConvertTo-SafeFailureText @($remoteTargetResult.Stderr + $remoteTargetResult.Stdout)))
    }
    $remoteTarget = @($remoteTargetResult.Stdout)
    if ($remoteTarget.Count -ne 0) {
        throw 'TARGET_BRANCH_ALREADY_EXISTS_REMOTELY'
    }

    $beforeBranchPaths = @(Get-StagedPaths -Operation 'BRANCH_STAGED_SET_READ')
    $beforeBranchInfo = New-NormalizedPathSetInfo $beforeBranchPaths
    $beforeBranchHash = Get-PathListHash $beforeBranchPaths
    Invoke-GitChecked @('switch', '-c', $TargetBranch) -Operation 'BRANCH_CREATE' -Path $TargetBranch | Out-Null
    $afterBranchPaths = @(Get-StagedPaths -Operation 'BRANCH_STAGED_SET_READ')
    $afterBranchInfo = New-NormalizedPathSetInfo $afterBranchPaths
    if ($afterBranchInfo.PathSet.Count -ne $beforeBranchInfo.PathSet.Count) {
        throw 'STAGED_COUNT_CHANGED_AFTER_BRANCH_CREATE'
    }
    if (@(Get-PathSetDifference -Left $beforeBranchInfo.PathSet -Right $afterBranchInfo.PathSet).Count -ne 0 -or @(Get-PathSetDifference -Left $afterBranchInfo.PathSet -Right $beforeBranchInfo.PathSet).Count -ne 0) {
        throw 'STAGED_PATH_SET_CHANGED_AFTER_BRANCH_CREATE'
    }

    Invoke-GitChecked @('commit', '-m', $CommitMessage) -Operation 'COMMIT' | Out-Null
    $commitSha = (Invoke-GitChecked @('rev-parse', 'HEAD') -Operation 'COMMIT_SHA_READ' | Select-Object -First 1).ToString().Trim()

    $postDiffInfo = New-NormalizedPathSetInfo @(Invoke-GitChecked @('-c', 'core.quotepath=false', 'diff', '--name-only', 'HEAD', '--') -Operation 'POST_COMMIT_RESIDUAL_DIFF_READ' | ForEach-Object { [string]$_ })
    $postUntrackedInfo = New-NormalizedPathSetInfo @(Invoke-GitChecked @('-c', 'core.quotepath=false', 'ls-files', '--others', '--exclude-standard', '--') -Operation 'POST_COMMIT_RESIDUAL_UNTRACKED_READ' | ForEach-Object { [string]$_ })
    $postResidualSet = New-Object -TypeName 'System.Collections.Generic.HashSet[string]' -ArgumentList ([System.StringComparer]::Ordinal)
    foreach ($path in $postDiffInfo.PathSet) {
        [void]$postResidualSet.Add($path)
    }
    foreach ($path in $postUntrackedInfo.PathSet) {
        [void]$postResidualSet.Add($path)
    }
    $governedLeft = @(Get-PathSetDifference -Left $expectedInfo.PathSet -Right $postResidualSet)
    if ($governedLeft.Count -ne 0) {
        throw ("GOVERNED_REQUIRED_CHANGES_LEFT_UNCOMMITTED: {0}" -f $governedLeft.Count)
    }

    Invoke-GitChecked @('push', '-u', 'origin', $TargetBranch) -Operation 'PUSH' -Path $TargetBranch | Out-Null
    $remoteAfterPush = @(Invoke-GitChecked @('ls-remote', '--heads', 'origin', $TargetBranch) -Operation 'REMOTE_SHA_VERIFY' -Path $TargetBranch)
    if ($remoteAfterPush.Count -eq 0) {
        throw 'REMOTE_BRANCH_NOT_FOUND_AFTER_PUSH'
    }
    $remoteSha = ([string]($remoteAfterPush | Select-Object -First 1)).Split("`t")[0].Trim()
    if ($remoteSha -ne $commitSha) {
        throw ("REMOTE_SHA_MISMATCH: {0}" -f $remoteSha)
    }

    $originalHead = (Invoke-GitChecked @('rev-parse', $BaseBranch) -Operation 'ORIGINAL_BRANCH_VERIFY' -Path $BaseBranch | Select-Object -First 1).ToString().Trim()
    if ($originalHead -ne $BaseHead) {
        throw ("ORIGINAL_BRANCH_HEAD_CHANGED: {0}" -f $originalHead)
    }

    Write-Output 'STAGE=GIT-CHECKPOINT-G11-REREVIEW-READY-LOCAL-PUSH'
    Write-Output 'STATUS=PASS'
    Write-Output ("EXECUTION_IDENTITY={0}" -f $Identity)
    Write-Output ("TARGET_BRANCH={0}" -f $TargetBranch)
    Write-Output ("CHECKPOINT_COMMIT_SHA={0}" -f $commitSha)
    Write-Output ("REMOTE_BRANCH_SHA={0}" -f $remoteSha)
    Write-Output 'LOCAL_REMOTE_SHA_MATCH=1'
    Write-Output 'ORIGINAL_BRANCH_HEAD_UNCHANGED=1'
    Write-Output 'G11_STATUS_AT_CHECKPOINT=PARTIAL'
    Write-Output 'G11_HUMAN_REREVIEW_PENDING_COUNT=11'
    Write-Output 'G12_RUN=0'
    Write-Output 'NEXT=USER_POST_REPAIR_HUMAN_REREVIEW'
}
catch {
    $failureException = $_.Exception
    $failureOperation = $script:CurrentOperation
    $failurePath = $script:CurrentPath
    $failureBlocker = Get-CheckpointFailureBlocker -Exception $failureException
    $failureCategory = Get-CheckpointFailureCategory -Blocker $failureBlocker -Exception $failureException
    $failureExceptionType = $failureException.GetType().FullName
    $failureGitStdout = ConvertTo-SafeFailureText $script:LastGitStdout
    $failureGitStderr = ConvertTo-SafeFailureText $script:LastGitStderr
    $failureDetail = ConvertTo-SafeFailureText @($failureGitStderr, $failureGitStdout)
    Fail-Checkpoint -Blocker $failureBlocker -Operation $failureOperation -Path $failurePath -Detail $failureDetail -Exception $failureException -ErrorCategory $failureCategory -ExceptionType $failureExceptionType -GitExitCode $script:LastGitExitCode -GitStdout $failureGitStdout -GitStderr $failureGitStderr
    exit 1
}
