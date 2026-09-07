@echo off
setlocal

if "%~3"=="" (
  echo Usage: scripts\setup_gdrive_oauth.cmd ^<google-drive-folder-id^> ^<google-client-id^> ^<google-client-secret^>
  exit /b 1
)

call "%~dp0setup_gdrive_remote.cmd" "%~1"
call "%~dp0dvc.cmd" remote modify --local gdrive gdrive_client_id "%~2"
call "%~dp0dvc.cmd" remote modify --local gdrive gdrive_client_secret "%~3"
call "%~dp0dvc.cmd" remote list
