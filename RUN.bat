@echo off

:: Setup Python ==============================================
:: Check and update Windows
:: No 'upgrade' available
:: Manually install python3...
:: No need to install pip (is default)
:: No need to install venv (is default)
py -m pip install --upgrade pip

set VENV_DIR=.venv

:run

if exist %VENV_DIR% (
    echo Virtual environment present.

    call %VENV_DIR%\Scripts\activate

    py ./buildpy --project ./project --json ./build.json

    call %VENV_DIR%\Scripts\deactivate

) else (
    echo Creating new virtual environment...

    py -m venv %VENV_DIR%

    call %VENV_DIR%\Scripts\activate

    echo Upgrading pip...
    py -m pip install --upgrade pip

    echo Installing buildpy dependencies...
    py -m pip install -r requirements.txt

    call %VENV_DIR%\Scripts\deactivate

    goto run
)

cmd /k