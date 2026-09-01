# Signet7 company-computer setup. Recipients should not run this.
# Live check (no install): https://verify.signet7.io/email/verify
$ErrorActionPreference = "Stop"
$setup = [string]$env:SIGNET7_SETUP
if ([string]::IsNullOrWhiteSpace($setup)) { $setup = "help" }
$setup = $setup.Trim().ToLowerInvariant()

$verify = "https://verify.signet7.io/email/verify"
$watchUrl = "https://signet7.io/files/signet7-watch-windows.zip"
$manifestUrl = "https://signet7.io/outlook/manifest.xml"
$root = Join-Path $env:LOCALAPPDATA "Signet7"

function Show-Help {
  Write-Host "Signet7 setup (Windows)"
  Write-Host "Recipients install nothing. $verify"
  Write-Host ""
  Write-Host "This script is for one company computer. Unsigned preview. Not a store listing."
  Write-Host "Set SIGNET7_SETUP then re-run:"
  Write-Host "  watch     download Watch zip for this PC (one company inbox)"
  Write-Host "  desktop   pip install signet7 if Python is present"
  Write-Host "  outlook   save Outlook manifest (Add from File, not AppSource)"
  Write-Host "  help      this list (default)"
  Write-Host ""
  Write-Host "There is no Uninstall command and no Check for update. To remove Watch, delete $root by hand."
  Write-Host "files/latest.json names the current unsigned preview. This script does not upgrade you."
  Write-Host ""
  Write-Host "Example:"
  Write-Host "  `$env:SIGNET7_SETUP='watch'; irm https://signet7.io/install.ps1 | iex"
}

function Install-Watch {
  New-Item -ItemType Directory -Force -Path $root | Out-Null
  $zip = Join-Path $root "signet7-watch-windows.zip"
  Write-Host "Downloading unsigned Watch. SmartScreen may warn. Recipients should not install."
  Invoke-WebRequest -Uri $watchUrl -OutFile $zip -UseBasicParsing
  $dest = Join-Path $root "watch"
  Expand-Archive -Path $zip -DestinationPath $dest -Force
  Write-Host "Unpacked to $dest"
  Write-Host "One company inbox only. Checkout is not live."
}

function Install-Desktop {
  $pip = Get-Command pip -ErrorAction SilentlyContinue
  if (-not $pip) {
    Write-Host "Python/pip not found. Use Watch on https://signet7.io/download or install Python first."
    Write-Host "Recipients still use $verify"
    return
  }
  Write-Host "Installing company desktop (pip). Recipients do not need this."
  & pip install --upgrade signet7
  Write-Host "Run: signet7"
  Write-Host "Or: signet7-setup --list"
}

function Install-Outlook {
  $downloads = [Environment]::GetFolderPath("UserProfile")
  if ($env:USERPROFILE) { $downloads = Join-Path $env:USERPROFILE "Downloads" }
  New-Item -ItemType Directory -Force -Path $downloads | Out-Null
  $out = Join-Path $downloads "signet7-outlook-manifest.xml"
  Invoke-WebRequest -Uri $manifestUrl -OutFile $out -UseBasicParsing
  Write-Host "Saved $out"
  Write-Host "In cloud Outlook: Add from File. Not AppSource. Not Add from URL."
  Write-Host "Recipients who never sideload: $verify"
}

switch ($setup) {
  "watch" { Install-Watch }
  "desktop" { Install-Desktop }
  "outlook" { Install-Outlook }
  default { Show-Help }
}
