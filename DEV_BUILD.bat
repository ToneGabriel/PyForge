@echo off
setlocal enabledelayedexpansion

for /f "tokens=2 delims=::" %%a in ('DEV_VENV.bat ^| findstr "::RETURN::"') do (
    set VENV_DIR=%%a
)

:: ===============================================
:: Build PyForge
:: ===============================================

set DEST_PATH=./.build
set NAME_FLAG=--name=pyforge
set DIST_FLAG=--distpath %DEST_PATH%/dist
set WORK_FLAG=--workpath %DEST_PATH%/build
set SPEC_FLAG=--specpath %DEST_PATH%
set TARGET_PATH=./app/__main__.py

echo.
echo [INFO] Activating environment and running build...

call !VENV_DIR!\Scripts\activate

pyinstaller --onedir %NAME_FLAG% %DIST_FLAG% %WORK_FLAG% %SPEC_FLAG% %TARGET_PATH%

call !VENV_DIR!\Scripts\deactivate

timeout /t 5
