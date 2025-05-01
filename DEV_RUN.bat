@echo off
setlocal enabledelayedexpansion

for /f "tokens=2 delims=::" %%a in ('DEV_VENV.bat ^| findstr "::RETURN::"') do (
    set VENV_DIR=%%a
)

:: ===============================================
:: Run PyForge
:: ===============================================

echo.
echo [INFO] Activating environment and running app...

call !VENV_DIR!\Scripts\activate

py ./app

call !VENV_DIR!\Scripts\deactivate

timeout /t 5
