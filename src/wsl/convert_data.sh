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
    if [ "$key" == "ESPEAK_LANGUAGE_CODE" ]; then
        language_code="$value"
    elif [ "$key" == "CHECKPOINT_SAMPLE_RATE" ]; then
        sample_rate="$value"
    fi
done < SETTINGS.txt

# Ensure both settings are read
if [ -z "$language_code" ]; then
    echo "ESPEAK_LANGUAGE_CODE not found in SETTINGS.txt. Please restart the process by redownloading the checkpoint file."
    exit 1
fi

if [ -z "$sample_rate" ]; then
    echo "SAMPLE_RATE not found in SETTINGS.txt. Please restart the process by redownloading the checkpoint file."
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

final_dir="$(pwd)/training_data/final"
echo "Obtaining dataset file from $final_dir"
echo "ESpeak-NG Language Code: $language_code"
echo "Dataset Sample Rate: $sample_rate"

echo "Starting the conversion to Piper's ljspeech format..."
# Preprocess the 'final' folder into Piper's ljspeech format
$PYTHON_CMD -m piper_train.preprocess \
--language en \
--input-dir $final_dir \
--output-dir preprocessed_data \
--dataset-format ljspeech \
--single-speaker \
--sample-rate $sample_rate \
--max-workers 8

echo "Process completed"
