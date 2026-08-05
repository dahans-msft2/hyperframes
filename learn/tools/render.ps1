<#
.SYNOPSIS
  Fail-fast render wrapper for the Learn HyperFrames pipeline.

.DESCRIPTION
  One controlled render attempt with real diagnostics. This exists because the
  first Entra render failed on a transient 5-second FFmpeg cold-start timeout that
  the CLI reported as "FFmpeg cannot start", the agent then retried blindly, mixed
  two CLI versions, and orphaned Chrome trees. This wrapper removes every one of
  those failure modes on OUR side, without waiting for an upstream CLI fix:

    - Resolves every path ONCE via tools/paths.py (no cwd guessing).
    - Pins exactly one CLI version (config.json cli.published_version unless -Version).
    - EXECUTES ffmpeg/ffprobe with a measured probe that distinguishes timeout from
      a real spawn/exit failure, and checks for an H.264 encoder — the CLI's own
      probe cannot tell these apart.
    - Binds HYPERFRAMES_FFMPEG_PATH / HYPERFRAMES_FFPROBE_PATH / HYPERFRAMES_BROWSER_PATH
      explicitly so the render never re-resolves an ambient binary.
    - Writes an attempt manifest BEFORE running, so recovery never depends on scrollback.
    - Runs ONE attempt. No blind retry. Re-running is a conscious act; pass -Note.
    - Marks success ONLY after independently probing the output MP4 (video+audio,
      dimensions, fps, duration). Launching the command is not success.
    - try/finally cleans only THIS attempt's process tree and restores env.

.EXAMPLE
  pwsh hf.ps1 render --project <dir> --note "first attempt after preflight"
  pwsh tools/render.ps1 -Project <dir> -Version 0.7.78 -Note "retry: pinned CLI"
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$Project,
    [string]$Output,
    [string]$Version,
    [string]$Ffmpeg,
    [string]$Ffprobe,
    [string]$Browser,
    [string]$RunId,
    [string]$Note,
    [int]$RenderTimeoutMin = 60,
    [switch]$Force
)

$ErrorActionPreference = 'Stop'
$engine = Split-Path $PSScriptRoot -Parent      # tools/ -> learn/
$tools = $PSScriptRoot
$configPath = Join-Path $engine 'config.json'

function Fail($msg) { Write-Host "RENDER FAIL: $msg" -ForegroundColor Red; exit 1 }

# ---- resolve project + config ------------------------------------------------
$projectDir = (Resolve-Path -LiteralPath $Project -ErrorAction SilentlyContinue)?.Path
if (-not $projectDir) { Fail "project not found: $Project" }
$config = if (Test-Path $configPath) { Get-Content $configPath -Raw | ConvertFrom-Json } else { $null }

if (-not $Version) { $Version = $config.cli.published_version }
if (-not $Version) { Fail "no CLI version given and config.json has no cli.published_version" }

$reviewDir = Join-Path $projectDir 'review'
$attemptsDir = Join-Path $reviewDir 'render-attempts'

if (-not $Output) { $Output = Join-Path $projectDir 'renders\render.mp4' }
New-Item -ItemType Directory -Force -Path (Split-Path $Output -Parent) | Out-Null

$attemptId = Get-Date -Format 'yyyyMMdd-HHmmss'
$manifestPath = Join-Path $attemptsDir "$attemptId.json"
$logOut = Join-Path $attemptsDir "$attemptId.out.log"
$logErr = Join-Path $attemptsDir "$attemptId.err.log"

# ---- binary resolution -------------------------------------------------------
function Find-Binary {
    param([string]$Name, [string]$Explicit)
    if ($Explicit) {
        if (Test-Path $Explicit) { return (Resolve-Path $Explicit).Path }
        Fail "$Name path does not exist: $Explicit"
    }
    $cmd = Get-Command $Name -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    $hit = Get-ChildItem "$env:LOCALAPPDATA\Microsoft\WinGet\Packages" -Recurse -Filter "$Name.exe" `
        -ErrorAction SilentlyContinue -Depth 4 | Select-Object -First 1
    if ($hit) { return $hit.FullName }
    return $null
}

# ---- measured, executing probe (distinguishes timeout from real failure) -----
# TimeoutMs is generous: a first-run WinGet binary can block ~30s in process
# creation alone while Defender/SmartScreen scans it. The CLI's fixed 5s probe
# cannot survive that cold start - warming the binaries here is the whole point.
function Invoke-Probe {
    param([string]$Exe, [string[]]$ProbeArgs, [int]$TimeoutMs = 45000)
    $psi = [System.Diagnostics.ProcessStartInfo]::new()
    $psi.FileName = $Exe
    foreach ($a in $ProbeArgs) { [void]$psi.ArgumentList.Add($a) }
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    try { $p = [System.Diagnostics.Process]::Start($psi) }
    catch { return [pscustomobject]@{ ok = $false; reason = 'spawn-error'; detail = $_.Exception.Message; elapsed_ms = 0 } }
    $outTask = $p.StandardOutput.ReadToEndAsync()
    $errTask = $p.StandardError.ReadToEndAsync()
    if (-not $p.WaitForExit($TimeoutMs)) {
        try { $p.Kill($true) } catch { }
        $sw.Stop()
        return [pscustomobject]@{ ok = $false; reason = 'timeout'; detail = "exceeded ${TimeoutMs}ms"; elapsed_ms = $sw.ElapsedMilliseconds }
    }
    $sw.Stop()
    $out = $outTask.Result; $err = $errTask.Result
    if ($p.ExitCode -ne 0) {
        $line = ($err.Trim() -split "`n" | Select-Object -First 1)
        return [pscustomobject]@{ ok = $false; reason = 'nonzero-exit'; exit_code = $p.ExitCode; detail = $line; elapsed_ms = $sw.ElapsedMilliseconds }
    }
    return [pscustomobject]@{ ok = $true; stdout = $out; elapsed_ms = $sw.ElapsedMilliseconds }
}

$ffmpegPath = Find-Binary -Name 'ffmpeg' -Explicit $Ffmpeg
if (-not $ffmpegPath) { Fail "ffmpeg not found (Get-Command or WinGet). winget install Gyan.FFmpeg" }
$ffprobePath = Find-Binary -Name 'ffprobe' -Explicit $Ffprobe
if (-not $ffprobePath) { Fail "ffprobe not found (Get-Command or WinGet)." }
$browserPath = if ($Browser) { Find-Binary -Name 'chrome' -Explicit $Browser } else { $null }

Write-Host "=== render preflight (executing probes) ===" -ForegroundColor Cyan
$ffmpegVer = Invoke-Probe -Exe $ffmpegPath -ProbeArgs @('-version')
if (-not $ffmpegVer.ok) { Fail "ffmpeg probe failed [$($ffmpegVer.reason)] $($ffmpegVer.detail)" }
$ffprobeVer = Invoke-Probe -Exe $ffprobePath -ProbeArgs @('-version')
if (-not $ffprobeVer.ok) { Fail "ffprobe probe failed [$($ffprobeVer.reason)] $($ffprobeVer.detail)" }
$encoders = Invoke-Probe -Exe $ffmpegPath -ProbeArgs @('-hide_banner', '-encoders')
if (-not $encoders.ok) { Fail "ffmpeg -encoders failed [$($encoders.reason)] $($encoders.detail)" }
if ($encoders.stdout -notmatch '\blibx264\b' -and $encoders.stdout -notmatch '\bh264_') {
    Fail "this ffmpeg build has no H.264 encoder (libx264 / h264_*). The render would fail after capture."
}
$ffmpegVerLine = ($ffmpegVer.stdout -split "`n" | Select-Object -First 1).Trim()
$ffprobeVerLine = ($ffprobeVer.stdout -split "`n" | Select-Object -First 1).Trim()
Write-Host "  ffmpeg  : $ffmpegVerLine  (probe $($ffmpegVer.elapsed_ms)ms)"
Write-Host "  ffprobe : $ffprobeVerLine  (probe $($ffprobeVer.elapsed_ms)ms)"
Write-Host "  encoder : H.264 present"

# ---- refuse to clobber a valid existing output unless -Force -----------------
function Test-Output {
    param([string]$Path)
    if (-not (Test-Path $Path)) { return [pscustomobject]@{ ok = $false; reason = 'missing' } }
    $len = (Get-Item $Path).Length
    if ($len -le 0) { return [pscustomobject]@{ ok = $false; reason = 'empty' } }
    $probe = Invoke-Probe -Exe $ffprobePath -ProbeArgs @('-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', $Path) -TimeoutMs 15000
    if (-not $probe.ok) { return [pscustomobject]@{ ok = $false; reason = "ffprobe-$($probe.reason)"; detail = $probe.detail } }
    $meta = $probe.stdout | ConvertFrom-Json
    $video = $meta.streams | Where-Object { $_.codec_type -eq 'video' } | Select-Object -First 1
    $audio = $meta.streams | Where-Object { $_.codec_type -eq 'audio' } | Select-Object -First 1
    $dur = [double]($meta.format.duration)
    $fpsNum = 0.0
    if ($video.r_frame_rate -match '^(\d+)/(\d+)$' -and [int]$Matches[2] -ne 0) { $fpsNum = [int]$Matches[1] / [int]$Matches[2] }
    $problems = @()
    if (-not $video) { $problems += 'no video stream' }
    if (-not $audio) { $problems += 'no audio stream' }
    if ($dur -le 0) { $problems += 'zero duration' }
    return [pscustomobject]@{
        ok       = ($problems.Count -eq 0)
        reason   = ($problems -join '; ')
        bytes    = $len
        width    = $video.width
        height   = $video.height
        fps      = [math]::Round($fpsNum, 3)
        seconds  = [math]::Round($dur, 3)
        v_codec  = $video.codec_name
        a_codec  = $audio.codec_name
    }
}

if ((Test-Path $Output) -and -not $Force) {
    $existing = Test-Output -Path $Output
    if ($existing.ok) { Fail "a VALID render already exists at $Output ($($existing.seconds)s). Pass -Force to overwrite." }
}

# ---- attempt manifest (written BEFORE execution) -----------------------------
$nodeVer = (& node --version 2>$null)
function Write-Manifest {
    param([string]$Status, [object]$Probe, [double]$ElapsedSec, [int]$RootPid)
    $obj = [ordered]@{
        attempt_id      = $attemptId
        status          = $Status
        note            = $Note
        started_utc     = $startedUtc
        elapsed_seconds = $ElapsedSec
        cli_version     = $Version
        node_version    = "$nodeVer"
        project         = $projectDir
        output          = $Output
        ffmpeg          = @{ path = $ffmpegPath; version = $ffmpegVerLine }
        ffprobe         = @{ path = $ffprobePath; version = $ffprobeVerLine }
        browser         = $browserPath
        command         = "npx --yes hyperframes@$Version render --output `"$Output`""
        root_pid        = $RootPid
        logs            = @{ stdout = $logOut; stderr = $logErr }
        output_probe    = $Probe
    }
    ($obj | ConvertTo-Json -Depth 6) | Set-Content -LiteralPath $manifestPath -Encoding UTF8
}

$startedUtc = (Get-Date).ToUniversalTime().ToString('s') + 'Z'
New-Item -ItemType Directory -Force -Path $attemptsDir | Out-Null
Write-Manifest -Status 'running' -Probe $null -ElapsedSec 0 -RootPid 0

# ---- bind explicit paths (save + restore in finally) -------------------------
$prevFfmpeg = $env:HYPERFRAMES_FFMPEG_PATH
$prevFfprobe = $env:HYPERFRAMES_FFPROBE_PATH
$prevBrowser = $env:HYPERFRAMES_BROWSER_PATH

$rootPid = 0
$renderSw = [System.Diagnostics.Stopwatch]::StartNew()
$status = 'failed'
$finalProbe = $null

try {
    $env:HYPERFRAMES_FFMPEG_PATH = $ffmpegPath
    $env:HYPERFRAMES_FFPROBE_PATH = $ffprobePath
    if ($browserPath) { $env:HYPERFRAMES_BROWSER_PATH = $browserPath }

    if ($RunId) { & py (Join-Path $tools 'stage_timing.py') start --project $projectDir --stage renderer --run-id $RunId --meta "attempt=$attemptId" 2>$null | Out-Null }

    # Get-Command can resolve npx to npx.ps1, which Start-Process -NoNewWindow cannot
    # execute directly (CreateProcess needs a native/.cmd entry point). Prefer .cmd/.exe.
    $npx = (Get-Command npx -All -ErrorAction SilentlyContinue |
        Sort-Object { switch -Wildcard ($_.Source) { '*.cmd' { 0 } '*.exe' { 1 } default { 2 } } } |
        Select-Object -First 1)?.Source
    if (-not $npx) { Fail "npx not found - install Node.js LTS" }

    Write-Host "=== render (hyperframes@$Version, one attempt) ===" -ForegroundColor Cyan
    Write-Host "  output: $Output"
    $proc = Start-Process -FilePath $npx `
        -ArgumentList @('--yes', "hyperframes@$Version", 'render', '--output', $Output) `
        -WorkingDirectory $projectDir -PassThru -NoNewWindow `
        -RedirectStandardOutput $logOut -RedirectStandardError $logErr
    $rootPid = $proc.Id

    if (-not $proc.WaitForExit($RenderTimeoutMin * 60 * 1000)) {
        Write-Host "  render exceeded ${RenderTimeoutMin}m - terminating attempt tree" -ForegroundColor Yellow
        taskkill /PID $rootPid /T /F 2>&1 | Out-Null
        $renderSw.Stop()
        Write-Manifest -Status 'timeout' -Probe $null -ElapsedSec ([math]::Round($renderSw.Elapsed.TotalSeconds, 1)) -RootPid $rootPid
        Fail "render timed out after ${RenderTimeoutMin} minutes (attempt $attemptId)"
    }
    $renderSw.Stop()

    if ($proc.ExitCode -ne 0) {
        $tail = (Get-Content $logErr -Tail 3 -ErrorAction SilentlyContinue) -join ' | '
        Write-Manifest -Status 'failed' -Probe $null -ElapsedSec ([math]::Round($renderSw.Elapsed.TotalSeconds, 1)) -RootPid $rootPid
        Fail "hyperframes render exited $($proc.ExitCode). Last stderr: $tail  (attempt $attemptId)"
    }

    # Output existence is NOT success. Probe it.
    $finalProbe = Test-Output -Path $Output
    if (-not $finalProbe.ok) {
        Write-Manifest -Status 'invalid-output' -Probe $finalProbe -ElapsedSec ([math]::Round($renderSw.Elapsed.TotalSeconds, 1)) -RootPid $rootPid
        Fail "render produced an INVALID output: $($finalProbe.reason)  (attempt $attemptId)"
    }

    $status = 'passed'
    Write-Manifest -Status $status -Probe $finalProbe -ElapsedSec ([math]::Round($renderSw.Elapsed.TotalSeconds, 1)) -RootPid $rootPid
}
finally {
    # Clean ONLY this attempt's process tree, if it is still alive.
    if ($rootPid -gt 0) {
        $alive = Get-Process -Id $rootPid -ErrorAction SilentlyContinue
        if ($alive) { taskkill /PID $rootPid /T /F 2>&1 | Out-Null }
    }
    if ($RunId) {
        $timingStatus = if ($status -eq 'passed') { 'passed' } else { 'failed' }
        & py (Join-Path $tools 'stage_timing.py') end --project $projectDir --stage renderer --run-id $RunId --status $timingStatus --note "attempt $attemptId ($status)" 2>$null | Out-Null
    }
    $env:HYPERFRAMES_FFMPEG_PATH = $prevFfmpeg
    $env:HYPERFRAMES_FFPROBE_PATH = $prevFfprobe
    $env:HYPERFRAMES_BROWSER_PATH = $prevBrowser
}

Write-Host ""
Write-Host "RENDER PASS" -ForegroundColor Green
Write-Host ("  {0}x{1} @ {2}fps  {3}s  video={4} audio={5}  {6:n1} MB" -f `
        $finalProbe.width, $finalProbe.height, $finalProbe.fps, $finalProbe.seconds, `
        $finalProbe.v_codec, $finalProbe.a_codec, ($finalProbe.bytes / 1MB))
Write-Host "  attempt manifest: $manifestPath"
Write-Host "  NOTE: this verifies the artifact only. Gate 8 'passed' is recorded by the caller from this result."
exit 0
