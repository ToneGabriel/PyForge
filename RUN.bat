@echo off
setlocal enabledelayedexpansion

:: ===============================================
:: Python Virtual Environment Setup
:: ===============================================

:: Manually install python3...
:: No need to install pip (is default)
:: No need to install venv (is default)

:: Set virtual environment directory name
set VENV_DIR=.venv

:: Check if the virtual environment already exists
if exist %VENV_DIR% (
    echo.
    echo [INFO] Virtual environment detected.

) else (
    echo.
    echo [INFO] Upgrading pip...
    py -m pip install --upgrade pip

    echo.
    echo [INFO] Creating virtual environment...
    py -m venv %VENV_DIR%

    echo.
    echo [INFO] Activating and configuring environment...
    call %VENV_DIR%\Scripts\activate

    echo [INFO] Installing requirements...
    py -m pip install --upgrade pip
    py -m pip install -r requirements.txt

    call %VENV_DIR%\Scripts\deactivate
)

:: ===============================================
:: Run PyForge
:: ===============================================

echo.
echo [INFO] Activating environment and running build...

call %VENV_DIR%\Scripts\activate

py ./pyforgemain --json ./setup.json --structure ./structure.zip

call %VENV_DIR%\Scripts\deactivate

:: Keep terminal open
cmd /k
