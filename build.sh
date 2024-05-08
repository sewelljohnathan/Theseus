#!/bin/bash

PROGRAM_NAME="THESEUS"
BUILD_DIR="build"
DIST_DIR="dist"

# Set up the virtual environment
VENV_PATH="${BUILD_DIR}/.venv"
python -m venv $VENV_PATH

PYTHON_PATH="${VENV_PATH}/bin/python"
PYINSTALLER_PATH="${VENV_PATH}/bin/pyinstaller"

$PYTHON_PATH -m pip install --upgrade pip
$PYTHON_PATH -m pip install -r requirements.txt
$PYTHON_PATH -m pip install pyinstaller==6.3.0

# PyInstaller
$PYINSTALLER_PATH -F -w --clean --name "${PROGRAM_NAME}" src/main.py
