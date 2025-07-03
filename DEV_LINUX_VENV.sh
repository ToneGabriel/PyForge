#!/bin/bash

# ===============================================
# Python Virtual Environment Setup
# ===============================================

# Set virtual environment directory name
VENV_DIR=".venv.linux"

# Check if the virtual environment already exists
if [ -d "$VENV_DIR" ]; then
    echo
    echo "[INFO] Virtual environment detected."
else
    echo
    echo "[INFO] Creating virtual environment..."
    python3 -m venv "$VENV_DIR"

    echo
    echo "[INFO] Activating and configuring environment..."
    source "$VENV_DIR/bin/activate"

    echo "[INFO] Upgrading pip and installing requirements..."
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt

    deactivate
fi
