<#
.SYNOPSIS
  Preflight the Learn video pipeline. Run BEFORE a render, not after it fails.

.DESCRIPTION
  Every check here corresponds to a trap that actually cost a run:

    ffmpeg/ffprobe   installed by WinGet but the Links shim is empty, so they
                     are NOT on PATH. `hyperframes render` dies AFTER capturing
                     every frame - the most expensive possible moment to fail.
    azure_tts        --ssml is a FLAG, not positional. Passing the file
                     positionally feeds raw XML through the plain-text path,
                     which speaks the tags and runs ~16% faster.
    hyperframes      bare `npx hyperframes` prompts and hangs. Pin the version.

  Emits the PATH fix-up line when ffmpeg is missing but installed.
#>
[CmdletBinding()]
param(
    [switch]$FixPath,    # patch $env:PATH - only reaches the caller if this script is DOT-SOURCED
    [switch]$PathOnly,   # print just the ffmpeg bin dir, nothing else, for capture
    [switch]$Persist,    # add ffmpeg to the USER PATH permanently (survives restarts)
    [switch]$Json        # machine-readable result, for platform-setup-check to consume
)

function Find-FfmpegBin {
    $cmd = Get-Command ffmpeg -ErrorAction SilentlyContinue
    if ($cmd) { return Split-Path $cmd.Source }
    $found = Get-ChildItem "$env:LOCALAPPDATA\Microsoft\WinGet\Packages" -Recurse -Filter 'ffmpeg.exe' `
        -ErrorAction SilentlyContinue -Depth 4 | Select-Object -First 1
    if ($found) { return Split-Path $found.FullName }
    return $null
}

# Capture mode:  $env:PATH = (pwsh -NoProfile -File preflight.ps1 -PathOnly) + ';' + $env:PATH
if ($PathOnly) {
    $bin = Find-FfmpegBin
    if ($bin) { Write-Output $bin; exit 0 }
    exit 1
}

# A script run with -File gets its own process, so $env:PATH changes die with it.
# Dot-sourcing (`. .\preflight.ps1 -FixPath`) runs in the CALLER's session instead.
$dotSourced = $MyInvocation.InvocationName -eq '.'

$ok = $true
$results = [System.Collections.Generic.List[object]]::new()

function Report($name, $good, $detail, [string]$severity = 'required') {
    $script:results.Add([pscustomobject]@{ check = $name; ok = [bool]$good; severity = $severity; detail = "$detail" })
    if (-not $Json) {
        $mark = if ($good) { 'OK  ' } elseif ($severity -eq 'optional') { 'WARN' } else { 'FAIL' }
        Write-Host ("  [{0}] {1,-16} {2}" -f $mark, $name, $detail)
    }
    if (-not $good -and $severity -ne 'optional') { $script:ok = $false }
}

if (-not $Json) { Write-Host "=== Learn video pipeline preflight ===" }

# This script resolves Windows install locations (WinGet package paths). On macOS
# or Linux the tool checks still run, but the ffmpeg auto-discovery will not.
if (-not $IsWindows -and $null -ne $IsWindows) {
    Report 'platform' $true "$([System.Environment]::OSVersion.Platform) - ffmpeg auto-discovery is Windows-only; install via your package manager" 'optional'
}

# --- ffmpeg / ffprobe -------------------------------------------------------
$ffmpeg = Get-Command ffmpeg -ErrorAction SilentlyContinue
$ffprobe = Get-Command ffprobe -ErrorAction SilentlyContinue
$bin = Find-FfmpegBin

# -Persist makes the fix permanent. Ensure the bin is in the PERSISTENT user PATH regardless of
# whether THIS session already sees ffmpeg - a temporary session entry must not skip persistence.
# Also drops malformed provider-qualified entries ('...FileSystem::C:\...') that silently break PATH.
if ($Persist -and $bin) {
    $userPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
    $entries = @($userPath -split ';' | Where-Object { $_ -and ($_ -notmatch 'FileSystem::') })
    if ($entries -notcontains $bin) {
        [Environment]::SetEnvironmentVariable('PATH', ((@($bin) + $entries) -join ';'), 'User')
        Report 'ffmpeg persist' $true "added to persistent USER PATH -> $bin"
    }
    else {
        Report 'ffmpeg persist' $true 'already in persistent USER PATH'
    }
    if (($env:PATH -split ';') -notcontains $bin) { $env:PATH = "$bin;" + $env:PATH }
}

if ($ffmpeg -and $ffprobe) {
    Report 'ffmpeg' $true $ffmpeg.Source
}
elseif ($bin) {
    if ($Persist) {
        Report 'ffmpeg' $true "persisted; new shells resolve it -> $bin"
        $script:ok = $true
    }
    elseif ($FixPath) {
        $env:PATH = "$bin;" + $env:PATH
        if ($dotSourced) {
            Report 'ffmpeg' $true 'PATH patched in YOUR session (dot-sourced)'
            $script:ok = $true
        }
        else {
            Report 'ffmpeg' $false "installed but NOT on PATH -> $bin"
            Write-Host "         -FixPath patched only THIS process, which is about to exit." -ForegroundColor Yellow
            Write-Host "         Use one of:" -ForegroundColor Yellow
            Write-Host "           . '$PSCommandPath' -FixPath          # dot-source into your session" -ForegroundColor Yellow
            Write-Host "           pwsh -File '$PSCommandPath' -Persist  # permanent, user scope" -ForegroundColor Yellow
        }
    }
    else {
        Report 'ffmpeg' $false "installed but NOT on PATH -> $bin"
        Write-Host "         Fix for this session:" -ForegroundColor Yellow
        Write-Host "         `$env:PATH = '$bin;' + `$env:PATH" -ForegroundColor Yellow
        Write-Host "         Or make it permanent:  pwsh -File '$PSCommandPath' -Persist" -ForegroundColor Yellow
    }
}
else {
    Report 'ffmpeg' $false 'not installed - winget install Gyan.FFmpeg'
}

# --- azure_tts (vendored) + credentials --------------------------------------
$ttsPy = Join-Path $PSScriptRoot 'azure_tts.py'
$ttsOk = Test-Path $ttsPy
$sdkOk = $false
if ($ttsOk) {
    & py -c "import azure.cognitiveservices.speech" 2>$null
    $sdkOk = ($LASTEXITCODE -eq 0)
}
Report 'azure_tts' ($ttsOk -and $sdkOk) $(
    if (-not $ttsOk) { 'missing tools/azure_tts.py' }
    elseif (-not $sdkOk) { 'run: pip install azure-cognitiveservices-speech' }
    else { 'py tools/azure_tts.py --ssml <file>  (--ssml is a flag, NOT positional)' }
)

# Validate the Speech config by KEY NAME only - values are never read into a
# variable, printed, or logged. The vendored tool resolves config from (in order):
# ./azure-speech.env, ~/.config/azure-speech/config.env, or the AZURE_SPEECH_* env vars.
$requiredKeys = @('AZURE_SPEECH_REGION', 'AZURE_SPEECH_RESOURCE_ID',
    'AZURE_SPEECH_TENANT_ID', 'AZURE_SPEECH_SUBSCRIPTION_ID')
$cfgFile = @((Join-Path (Get-Location) 'azure-speech.env'),
    (Join-Path $HOME '.config/azure-speech/config.env')) |
    Where-Object { Test-Path $_ } | Select-Object -First 1
if ($cfgFile) {
    $present = Get-Content $cfgFile |
        Where-Object { $_ -match '^\s*[A-Za-z_]+\s*=' } |
        ForEach-Object { ($_ -split '=', 2)[0].Trim() }
    $missing = $requiredKeys | Where-Object { $present -notcontains $_ }
    if ($missing) {
        Report 'speech config' $false "missing key(s): $($missing -join ', ')  in $cfgFile"
    }
    else {
        Report 'speech config' $true "$($present.Count) keys in $cfgFile"
    }
}
elseif ($env:AZURE_SPEECH_RESOURCE_ID -and $env:AZURE_SPEECH_REGION) {
    Report 'speech config' $true 'from AZURE_SPEECH_* environment variables'
}
else {
    Report 'speech config' $false 'no azure-speech.env, ~/.config/azure-speech/config.env, or AZURE_SPEECH_* env vars'
}

# Speech uses Entra (there is no API key in the config), so narration depends on
# an active az login - a valid config file alone is not enough.
$az = Get-Command az -ErrorAction SilentlyContinue
if ($az) {
    $acct = & az account show --query 'user.name' -o tsv 2>$null
    if ($LASTEXITCODE -eq 0 -and $acct) {
        Report 'entra login' $true "signed in as $acct"
    }
    else {
        Report 'entra login' $false 'az installed but NOT signed in - run: az login'
    }
}
else {
    Report 'entra login' $false 'Azure CLI not installed - winget install Microsoft.AzureCLI, then az login'
}

# --- node / npx -------------------------------------------------------------
$npx = Get-Command npx -ErrorAction SilentlyContinue
# The pinned published version is the single source of truth in config.json.
$configPath = Join-Path (Split-Path $PSScriptRoot -Parent) 'config.json'
$pinned = if (Test-Path $configPath) { (Get-Content $configPath -Raw | ConvertFrom-Json).cli.published_version } else { $null }
$npxMsg = if ($npx) {
    if ($pinned) { "use: npx --yes hyperframes@$pinned  (pinned in config.json; never bare, never piped)" }
    else { 'use: npx --yes hyperframes@<pinned>  (never bare, never piped)' }
}
else { 'not found - install Node.js LTS' }
Report 'npx' ([bool]$npx) $npxMsg

# --- python -----------------------------------------------------------------
$py = Get-Command py -ErrorAction SilentlyContinue
if (-not $py) { $py = Get-Command python3 -ErrorAction SilentlyContinue }
Report 'python' ([bool]$py) $(if ($py) { (& $py.Source --version 2>&1) } else { 'not found' })

# --- brand assets -----------------------------------------------------------
$fontDir = Join-Path (Split-Path $PSScriptRoot -Parent) 'assets/fonts'
if (-not (Test-Path $fontDir)) { $fontDir = Join-Path (Split-Path $PSScriptRoot -Parent) 'fonts' }
$fonts = @(Get-ChildItem $fontDir -Filter '*.woff2' -ErrorAction SilentlyContinue)
Report 'brand fonts' ($fonts.Count -ge 3) $(if ($fonts.Count) { "$($fonts.Count) woff2 in $fontDir" } else { 'no embedded woff2 found - fonts must ship with each project, never fetched at render time' }) 'optional'

$endcard = Join-Path (Split-Path $PSScriptRoot -Parent) 'assets/AI_End_Card.mp4'
if (Test-Path $endcard) {
    $len = (Get-Item $endcard).Length
    Report 'AI end card' ($len -gt 5MB) "$([math]::Round($len/1MB,1)) MB $(if($len -lt 5MB){'<- looks like the NORMALIZED copy, use the original'})"
}
else {
    Report 'AI end card' $false "missing: $endcard"
}

if ($Json) {
    [pscustomobject]@{
        pass    = $ok
        checks  = $results
        failed  = @($results | Where-Object { -not $_.ok -and $_.severity -ne 'optional' } | ForEach-Object { $_.check })
        skipped = @($results | Where-Object { -not $_.ok -and $_.severity -eq 'optional' } | ForEach-Object { $_.check })
    } | ConvertTo-Json -Depth 5
    if (-not $dotSourced) { exit ([int](-not $ok)) }
    return
}

Write-Host ""
if ($ok) {
    Write-Host "PREFLIGHT PASS" -ForegroundColor Green
    if (-not $dotSourced) { exit 0 }
}
else {
    Write-Host "PREFLIGHT FAIL - fix the above before rendering" -ForegroundColor Red
    if (-not $dotSourced) { exit 1 }
}
