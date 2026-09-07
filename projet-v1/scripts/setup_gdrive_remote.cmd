@echo off
setlocal

if "%~1"=="" (
  echo Usage: scripts\setup_gdrive_remote.cmd ^<google-drive-folder-id^>
  exit /b 1
)

call "%~dp0dvc.cmd" remote add -d gdrive "gdrive://%~1" --force
call "%~dp0dvc.cmd" remote list
