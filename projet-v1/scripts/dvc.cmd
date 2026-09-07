@echo off
setlocal

set "PROJECT_ROOT=%~dp0.."
set "DVC_GLOBAL_CONFIG_DIR=%PROJECT_ROOT%\.dvc_global"
set "DVC_SITE_CACHE_DIR=%PROJECT_ROOT%\.dvc_site_cache"
set "DVC_SYSTEM_CONFIG_DIR=%PROJECT_ROOT%\.dvc_system"
set "ITERATIVE_DO_NOT_TRACK=do-not-track"

"%PROJECT_ROOT%\.venv\Scripts\dvc.exe" %*
