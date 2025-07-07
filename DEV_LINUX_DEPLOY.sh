#!/bin/bash

# ===============================================
# Build PyForge
# ===============================================

VENV_DIR=".venv.linux"

DEST_PATH="./.build.linux"
NAME_FLAG="--name=pyforge"
DIST_FLAG="--distpath ${DEST_PATH}/dist"
WORK_FLAG="--workpath ${DEST_PATH}/build"
SPEC_FLAG="--specpath ${DEST_PATH}"
OTHERS_FLAG="--onedir --clean"
TARGET_PATH="./app/__main__.py"

echo
echo "[INFO] Activating environment and running build..."

source "${VENV_DIR}/bin/activate"

pyinstaller $NAME_FLAG $DIST_FLAG $WORK_FLAG $SPEC_FLAG $OTHERS_FLAG $TARGET_PATH

deactivate

sleep 3

# ===============================================
# Deploy PyForge
# ===============================================

echo
echo "[INFO] Deploying build..."

mkdir -p PyForge/deps

# Copy deps
cp -r deps.linux/* PyForge/deps/

# Copy PyInstaller output
cp -r .build.linux/dist/pyforge/* PyForge/

# Copy metadata files
cp manifest.json README.md PyForge/

tar czvf PyForge.tar.gz PyForge/

# To extract
# tar xzvf PyForge.tar.gz
