# DEVELOPERS

## Use this to setup your project

1. `git config --global core.autocrlf input` in your cmd and clone the project again. This is to ensure the files have LF line ending.

2. Dependencies:
    - Depending on platform (Linux or Windows) download binaries for `cmake` and `ninja` from here:
        - https://cmake.org/download/
        - https://github.com/ninja-build/ninja/releases
    - Place them inside the project under `deps/cmake` and `deps/ninja/bin`

3. Install Python
    - manually for Windows (https://www.python.org/downloads/)
    - `sudo apt install python3 python3-venv python3-pip` for Linux

4. Run `DEV_WINDOWS_VENV`/`DEV_LINUX_VENV` script to prepare the virtual environment for the project

5. Run `DEV_WINDOWS_DEPLOY`/`DEV_LINUX_DEPLOY` script to build the project and prepare for deployment
