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

    echo Installing buildpy dependencies...
    py -m pip install -r requirements.txt

    call %VENV_DIR%\Scripts\deactivate
)

:: Work while venv is active =================================
call %VENV_DIR%\Scripts\activate

:menu

echo ==========================
echo        PyForge Menu       
echo ==========================
echo 1. Generate CMakeLists
echo 2. Build Project
echo 3. Clear Setup and Build
echo 4. Exit
echo ==========================
set /p choice=Choose an option (1-4): 


if "%choice%"=="1" (
    echo Running CMakeLists Generation...
    call :run_python g
    pause
    goto menu
) else if "%choice%"=="2" (
    echo Running CMake Build...
    call :run_python b
    pause
    goto menu
) else if "%choice%"=="3" (
    echo Running Setup Clear...
    call :run_python c
    pause
    goto menu
) else if "%choice%"=="4" (
    echo Exiting...
    goto end
) else (
    echo Invalid choice, please choose between 1-4.
    pause
    goto menu
)

:: Function to call Python script
:run_python
py ./buildpy --action %1 --project ./project --json ./build.json
exit /b

:end
call %VENV_DIR%\Scripts\deactivate

cmd /k