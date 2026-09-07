$ErrorActionPreference = "Stop"

if ($args.Count -lt 3) {
    Write-Error "Usage: .\scripts\setup_gdrive_oauth.ps1 <google-drive-folder-id> <google-client-id> <google-client-secret>"
}

& (Join-Path $PSScriptRoot "setup_gdrive_remote.ps1") $args[0]
& (Join-Path $PSScriptRoot "dvc.ps1") remote modify --local gdrive gdrive_client_id $args[1]
& (Join-Path $PSScriptRoot "dvc.ps1") remote modify --local gdrive gdrive_client_secret $args[2]
& (Join-Path $PSScriptRoot "dvc.ps1") remote list
