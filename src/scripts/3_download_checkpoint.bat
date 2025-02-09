@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

REM Check if Python 3.10 is installed
echo Checking for python3.10...
where python3.10 >nul 2>nul
if errorlevel 1 (
    echo python3.10 not found, checking for py...
    where py >nul 2>nul
    if errorlevel 1 (
        echo py command not found, checking for python...
        where python >nul 2>nul
        if errorlevel 1 (
            echo Python is not installed. Please install Python 3.10 to proceed.
            pause
            exit /b 1
        ) else (
            set PYTHON_CMD=python
            echo Using 'python' instead of 'py' or 'python3.10'.
        )
    ) else (
        set PYTHON_CMD=py -3.10
        echo Using 'py -3.10' instead of 'python3.10'.
    )
) else (
    set PYTHON_CMD=python3.10
    echo Using 'python3.10'.
)

REM Ensure PYTHON_CMD is set correctly
if not defined PYTHON_CMD (
    echo ERROR: PYTHON_CMD is not set correctly.
    pause
    exit /b 1
)

REM Activate the virtual environment
set "venv_path=..\piper\src\python\.venv"
echo Activating virtual environment
if not exist "%venv_path%\bin\activate" (
    echo Virtual environment not found. Is piper correctly installed?
    pause
    exit /b 1
)
call "%venv_path%\bin\activate"

REM Install requests in the virtual environment
echo Installing requests
%PYTHON_CMD% -m pip install requests

REM Call the Python script to download the checkpoint file
echo Initializing checkpoint file download...
%PYTHON_CMD% download_checkpoint.py

