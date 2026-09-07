@echo off
setlocal

set "PROJECT_ROOT=%~dp0.."
set "DAGSTER_HOME=%PROJECT_ROOT%\.dagster_home"
if not exist "%DAGSTER_HOME%" mkdir "%DAGSTER_HOME%"

"%PROJECT_ROOT%\.venv\Scripts\dagster.exe" dev -f "%PROJECT_ROOT%\pipelines\dagster_pipeline.py"
