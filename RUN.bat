@echo off

:: Setup Python ==============================================
:: Check and update Windows
:: No 'upgrade' available
:: Manually install python3...
:: No need to install pip (is default)
:: No need to install venv (is default)
py -m pip install --upgrade pip

:: Setup VENV ================================================
:: Set the virtual environment directory name
set VENV_DIR=.venv

:: Create a new virtual environment and upgrade pip
if exist %VENV_DIR% (
    echo Virtual environment present.
) else (
    echo Creating new virtual environment...
    py -m venv %VENV_DIR%

    call %VENV_DIR%\Scripts\activate

    echo Upgrading pip...
    py -m pip install --upgrade pip

    echo Installing requirements...
    py -m pip install -r requirements.txt

    call %VENV_DIR%\Scripts\deactivate
)

:: Work while venv is active =================================
call %VENV_DIR%\Scripts\activate

:menu

echo 1. Generate CMakeLists
echo 2. Build Project
echo 3. Exit
set /p choice=Choose an option (1-3): 

if "%choice%"=="1" (
    echo Running CMakeLists Generation...
    py ./.build_app_py --action g --json ./generate.json
    pause
    goto menu
) else if "%choice%"=="2" (
    echo Running CMake Build...
    py ./.build_app_py --action b --json ./build.json
    pause
    goto menu
) else if "%choice%"=="3" (
    echo Exiting...
) else (
    echo Invalid choice, please choose between 1-3.
    pause
    goto menu
)

call %VENV_DIR%\Scripts\deactivate

cmd /k