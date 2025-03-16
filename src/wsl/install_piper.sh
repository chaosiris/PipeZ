#!/bin/bash
# Known to work with Piper commit: a0f09cdf9155010a45c243bc8a4286b94f286ef4

# Navigate to the script directory
cd "$(dirname "$0")"
# Print the current directory
echo "Current directory: $(pwd)"

# Check if Piper is already installed
if [ -d "piper" ]; then
    read -p "Piper is already installed. Do you want to re-install it? (y/n): " choice
    if [ "$choice" != "y" ]; then
        echo "You chose not to reinstall. Proceeding with the installation process..."
    else
        echo "You chose to reinstall. Removing existing Piper installation..."
        rm -rf piper
        echo "Continuing with the installation..."
    fi
else
    echo "Piper is not installed. Proceeding with installation..."
fi

# Clone Piper repository if not already installed
if [ ! -d "piper" ]; then
    git clone https://github.com/rhasspy/piper.git
    if [ $? -ne 0 ]; then
        echo "Failed to clone Piper repository."
        exit 1
    fi
fi

echo "Proceeding with installation..."

# Check if the piper directory exists after cloning
if [ ! -d "piper" ]; then
    echo "Piper directory does not exist after cloning."
    exit 1
fi

echo "Piper repository cloned successfully."
cd piper/src/python
if [ $? -ne 0 ]; then
    echo "Failed to change directory to piper/src/python."
    exit 1
fi

# Print the current directory again to ensure we're in the correct place
echo "Current directory: $(pwd)"

# Check if Python 3.10 is installed
echo "Checking for python3.10..."
if ! command -v python3.10 &> /dev/null; then
    echo "python3.10 not found. Checking for other Python versions..."
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

# Create and activate virtual environment
echo "Creating Python 3.10 virtual environment..."
$PYTHON_CMD -m venv .venv

# Activate virtual environment
source .venv/bin/activate
sudo apt update
sudo apt install dos2unix
sudo apt install python3-dev
sudo apt install build-essential

# Update pip and install packages
echo "Enforcing pip==24.0 and installing dependency packages..."
$PYTHON_CMD -m pip install --upgrade pip==24.0 wheel setuptools
$PYTHON_CMD -m pip install "torch<2.6.0" torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
$PYTHON_CMD -m pip install -r requirements.txt
$PYTHON_CMD -m pip install numpy==1.24.4
$PYTHON_CMD -m pip install torchmetrics==0.11.4
$PYTHON_CMD -m pip install build
$PYTHON_CMD -m python -m build
$PYTHON_CMD -m pip install -e .

echo "Running build_monotonic_align..."

# Now go into the correct directory, relative to the root of the repository
cd piper_train/vits/monotonic_align
if [ $? -ne 0 ]; then
    echo "Failed to change directory to piper/src/python/piper_train/vits/monotonic_align."
    exit 1
fi

# Check if the 'monotonic_align' directory exists, create if not
if [ ! -d "monotonic_align" ]; then
    mkdir monotonic_align
fi

echo "Directory change successful and required directory created if not already present."

# Cythonize core.pyx (this is equivalent to the bash cythonize command)
echo "Cythonizing core.pyx..."
cythonize -i core.pyx

# Move the generated .so file to the monotonic_align directory
mv core*.so monotonic_align/

echo "Build completed for monotonic_align!"

echo "Piper installation complete!"
