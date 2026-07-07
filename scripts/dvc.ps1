$ErrorActionPreference = "Stop"

$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$env:DVC_GLOBAL_CONFIG_DIR = Join-Path $projectRoot ".dvc_global"
$env:DVC_SITE_CACHE_DIR = Join-Path $projectRoot ".dvc_site_cache"
$env:DVC_SYSTEM_CONFIG_DIR = Join-Path $projectRoot ".dvc_system"
$env:ITERATIVE_DO_NOT_TRACK = "do-not-track"

& (Join-Path $projectRoot ".venv\Scripts\dvc.exe") @args
