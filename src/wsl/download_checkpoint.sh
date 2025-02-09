#!/bin/bash
set -e

cd "$(dirname "$0")"
echo "Current directory: $(pwd)"

# Check if Python 3.10 is installed
echo "Checking for python3.10..."
if ! command -v python3.10 &> /dev/null; then
    echo "python3.10 not found, checking for python3..."
    if ! command -v python3 &> /dev/null; then
        echo "Python is not installed. Please install Python 3.10 to proceed."
        exit 1
    else
        PYTHON_CMD=python3
        echo "Using 'python3' instead of 'python3.10'."
    fi
else
    PYTHON_CMD=python3.10
    echo "Using 'python3.10'."
fi

# Ensure PYTHON_CMD is set correctly
if [ -z "$PYTHON_CMD" ]; then
    echo "ERROR: PYTHON_CMD is not set correctly."
    exit 1
fi

# Activate the virtual environment
venv_path="../piper/src/python/.venv"
echo "Activating virtual environment"
if [ ! -f "$venv_path/bin/activate" ]; then
    echo "Virtual environment not found. Is piper correctly installed?"
    exit 1
fi
source "$venv_path/bin/activate"

# Install requests in the virtual environment
echo "Installing requests"
$PYTHON_CMD -m pip install requests

# Call the Python script to download the checkpoint file
echo "Initializing checkpoint file download..."
$PYTHON_CMD download_checkpoint.py

echo "Checkpoint file completed successfully"
