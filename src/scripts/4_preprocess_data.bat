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

REM Read the settings from SETTINGS.txt
for /f "tokens=1,2 delims==" %%a in (SETTINGS.txt) do (
    if "%%a"=="ESPEAK_LANGUAGE_CODE" set "language_code=%%b"
    if "%%a"=="CHECKPOINT_SAMPLE_RATE" set "sample_rate=%%b"
)

REM Ensure both settings are read
if not defined language_code (
    echo ESPEAK_LANGUAGE_CODE not found in SETTINGS.txt. Please restart the process by redownloading the checkpoint.
    exit /b 1
)

if not defined sample_rate (
    echo SAMPLE_RATE not found in SETTINGS.txt. Please restart the process by redownloading the checkpoint.
    exit /b 1
)

REM Set the path to the training_data folder
set "training_data=training_data"
set "metadata_file=%training_data%\metadata.csv"
set "preprocess_script=get_sample_rate.py"
set "unify_script=unify_sample_rate.py"
set "venv_path=..\piper\src\python\.venv"
set "backup_folder=%training_data%\backup"

REM Install ffmpeg-python in the virtual environment
echo Installing ffmpeg-python
%PYTHON_CMD% -m pip install ffmpeg-python

REM Check if metadata.csv exists
if not exist "%metadata_file%" (
    echo metadata.csv not found in %training_data% folder.
    pause
    exit /b 1
)

REM Create backup folder and copy existing WAV files
echo Creating backup folder and copying WAV files
if not exist "%backup_folder%" (
    mkdir "%backup_folder%"
)
for %%f in (%training_data%) do (
    copy /Y "%%f" "%backup_folder%" > nul 2>&1
)
echo Completed file backup

REM Initialize variables
set "sample_rates="
echo Initialized sample_rates

REM Read the metadata.csv and check for existence of listed files
for /f "tokens=1* delims=|" %%a in ('type "%metadata_file%"') do (
    REM Append .wav extension if not present
    if /i "%%~xa" neq ".wav" (
        set "filename=%%a.wav"
    ) else (
        set "filename=%%a"
    )

    if exist "%training_data%\!filename!" (
        REM Get the sample rate of the audio file using the Python script
        echo Getting sample rate for !filename!
        for /f %%b in ('%PYTHON_CMD% "%preprocess_script%" "%training_data%\!filename!"') do (
            set "sample_rate=%%b"
            REM Add sample rate to the list
            if "!sample_rates!" neq "" set "sample_rates=!sample_rates!,"
            set "sample_rates=!sample_rates!%%b"
            REM Create the directory for the sample rate if it doesn't exist
            if not exist "%training_data%\wav_%%b" (
                mkdir "%training_data%\wav_%%b"
            )
            REM Move the file to the appropriate directory
            move "%training_data%\!filename!" "%training_data%\wav_%%b\"
            echo !filename! has been moved to wav_%%b folder.
        )
    ) else (
        echo File !filename! listed in metadata.csv not found.
    )
)

echo Sorting completed.

REM Call the Python script to unify sample rates
%PYTHON_CMD% "%unify_script%" "%sample_rate%"

pause
