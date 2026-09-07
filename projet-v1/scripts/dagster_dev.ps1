$ErrorActionPreference = "Stop"

$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$env:DAGSTER_HOME = Join-Path $projectRoot ".dagster_home"
New-Item -ItemType Directory -Force -Path $env:DAGSTER_HOME | Out-Null

& (Join-Path $projectRoot ".venv\Scripts\dagster.exe") dev -f (Join-Path $projectRoot "pipelines\dagster_pipeline.py")
