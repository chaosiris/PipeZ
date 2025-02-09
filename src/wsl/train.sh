#!/bin/bash
set -e

cd "$(dirname "$0")"

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

# Ensure SETTINGS.txt is in LF EoL encoding sequence
dos2unix SETTINGS.txt

# Read the settings from SETTINGS.txt
while IFS="=" read -r key value; do
    if [ "$key" == "CHECKPOINT_FILE" ]; then
        checkpoint_file="$value"
    fi
done < SETTINGS.txt

# Ensure both settings are read
if [ -z "$checkpoint_file" ]; then
    echo "CHECKPOINT_FILE not found in SETTINGS.txt. Please restart the process by redownloading the checkpoint file."
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

echo "Current directory: $(pwd)"
echo "Using checkpoint file: downloaded_checkpoint/$checkpoint_file"
echo "Starting the training process..."

# Preprocess the 'final' folder into Piper's ljspeech format
python -m piper_train \
    --dataset-dir preprocessed_data \
    --accelerator gpu \
    --devices 1 \
    --batch-size 10 \
    --validation-split 0.0 \
    --num-test-examples 0 \
    --max_epochs 30000 \
    --resume_from_checkpoint "$(pwd)/downloaded_checkpoint/$checkpoint_file" \
    --checkpoint-epochs 25 \
    --precision 32

echo "Process completed"
