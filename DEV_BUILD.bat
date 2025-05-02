@echo off
setlocal enabledelayedexpansion

for /f "tokens=2 delims=::" %%a in ('DEV_VENV.bat ^| findstr "::RETURN::"') do (
    set VENV_DIR=%%a
)

:: ===============================================
:: Build PyForge
:: ===============================================

echo.
echo [INFO] Activating environment and running build...

call !VENV_DIR!\Scripts\activate

pyinstaller --onefile --name=pyforge ./app/__main__.py

call !VENV_DIR!\Scripts\deactivate

timeout /t 5
