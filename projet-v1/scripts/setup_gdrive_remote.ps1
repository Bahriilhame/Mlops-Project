$ErrorActionPreference = "Stop"

if ($args.Count -lt 1) {
    Write-Error "Usage: .\scripts\setup_gdrive_remote.ps1 <google-drive-folder-id>"
}

& (Join-Path $PSScriptRoot "dvc.ps1") remote add -d gdrive "gdrive://$($args[0])" --force
& (Join-Path $PSScriptRoot "dvc.ps1") remote list
