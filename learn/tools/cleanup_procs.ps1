<#
.SYNOPSIS
  Reap stray HyperFrames render processes left behind by interrupted runs.

.DESCRIPTION
  Puppeteer browsers and npx wrappers survive their parent shell. Killing a VS Code
  terminal orphans them instead of stopping them, and an orphaned browser keeps
  spawning children — each one flashing a console window on Windows.

  Only provably-dead processes are killed:
    - chrome-headless-shell trees whose root has no living parent
    - npx wrappers older than -MinAgeMinutes that are stuck on the install prompt

  An ACTIVE render always has a living node parent, so it is never touched.

.EXAMPLE
  pwsh tools/cleanup_procs.ps1              # report only
  pwsh tools/cleanup_procs.ps1 -Kill        # reap
#>
[CmdletBinding()]
param(
    [switch]$Kill,
    [int]$MinAgeMinutes = 10
)

function Get-OrphanRoots {
    Get-CimInstance Win32_Process -Filter "Name='chrome-headless-shell.exe'" | Where-Object {
        # A root is a headless-shell whose parent is gone or is not itself a headless-shell.
        $parent = Get-Process -Id $_.ParentProcessId -ErrorAction SilentlyContinue
        -not $parent -or $parent.ProcessName -ne 'chrome-headless-shell'
    } | Where-Object {
        -not (Get-Process -Id $_.ParentProcessId -ErrorAction SilentlyContinue)
    }
}

function Get-StuckNpx {
    param([int]$MinAge)
    Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Where-Object {
        $_.CommandLine -match 'npx-cli\.js.*hyperframes'
    } | Where-Object {
        $proc = Get-Process -Id $_.ProcessId -ErrorAction SilentlyContinue
        $proc -and ((Get-Date) - $proc.StartTime).TotalMinutes -gt $MinAge
    }
}

$orphans = @(Get-OrphanRoots)
$stuck = @(Get-StuckNpx -MinAge $MinAgeMinutes)
$total = @(Get-Process chrome-headless-shell -ErrorAction SilentlyContinue).Count

if (-not $orphans -and -not $stuck) {
    Write-Host "clean - no orphaned browsers, no stuck npx ($total headless-shell running, all parented)"
    return
}

foreach ($o in $orphans) {
    $proc = Get-Process -Id $o.ProcessId -ErrorAction SilentlyContinue
    $age = if ($proc) { [math]::Round(((Get-Date) - $proc.StartTime).TotalMinutes, 1) } else { '?' }
    Write-Host "orphaned browser tree  pid $($o.ProcessId)  up ${age}m"
    if ($Kill) { taskkill /PID $o.ProcessId /T /F 2>&1 | Out-Null }
}

foreach ($s in $stuck) {
    $proc = Get-Process -Id $s.ProcessId -ErrorAction SilentlyContinue
    $age = if ($proc) { [math]::Round(((Get-Date) - $proc.StartTime).TotalMinutes, 1) } else { '?' }
    Write-Host "stuck npx wrapper      pid $($s.ProcessId)  up ${age}m"
    if ($Kill) { taskkill /PID $s.ProcessId /T /F 2>&1 | Out-Null }
}

if ($Kill) {
    Start-Sleep -Milliseconds 700
    $left = @(Get-Process chrome-headless-shell -ErrorAction SilentlyContinue).Count
    Write-Host "`nreaped. $left headless-shell remaining"
} else {
    Write-Host "`nreport only - rerun with -Kill to reap"
}
