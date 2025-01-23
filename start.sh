#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source "$SCRIPT_DIR/venv/bin/activate"
python3 "$SCRIPT_DIR/src/create_background.py"

# Deactivate the virtual environment
deactivate
