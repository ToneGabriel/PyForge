@echo off

:: ===============================================
:: Build PyForge
:: ===============================================
set VENV_DIR=.venv.windows

set DEST_PATH=./.build.windows
set NAME_FLAG=--name=pyforge
set DIST_FLAG=--distpath %DEST_PATH%/dist
set WORK_FLAG=--workpath %DEST_PATH%/build
set SPEC_FLAG=--specpath %DEST_PATH%
set OTHERS_FLAG=--onedir --clean
set TARGET_PATH=./app/__main__.py

echo.
echo [INFO] Activating environment and running build...

call %VENV_DIR%\Scripts\activate

pyinstaller %NAME_FLAG% %DIST_FLAG% %WORK_FLAG% %SPEC_FLAG% %OTHERS_FLAG% %TARGET_PATH%

call %VENV_DIR%\Scripts\deactivate

timeout /t 5

:: ===============================================
:: Deploy PyForge
:: ===============================================

echo.
echo [INFO] Deploying build...

call makensis windows_install_config.nsi

timeout /t 5
