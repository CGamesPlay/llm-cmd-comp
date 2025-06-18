#!/bin/bash

# Integration test for llm-cmd-comp package
# This test:
# 1. Builds the package to a wheel
# 2. Installs the wheel in a clean virtual environment  
# 3. Tests that `llm cmdcomp --init bash` works correctly

set -eux

TEMP_DIR=$(mktemp -d)
cleanup() {
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

rm -rf dist
python -m pip install build
python -m build --wheel

# Locate the wheel file
WHEEL_FILE=$(find dist -name "*.whl" | head -1)
[[ -n "$WHEEL_FILE" ]]

# Set up a venv
VENV_PATH="$TEMP_DIR/test_venv"
python -m venv "$VENV_PATH"
source "$VENV_PATH/bin/activate"
pip install llm
llm install "$WHEEL_FILE"

llm cmdcomp --init bash
