@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

REM Prompt user to enter a unique folder name
:enter_folder_name
set /p folder_name=Please enter a unique folder name to create your training dataset: 

REM Check if the folder name is already taken
if exist "%folder_name%" (
    echo Folder name '%folder_name%' already exists. Please enter a different name.
    goto enter_folder_name
)

REM Create the folder and change directory to the new folder
mkdir "%folder_name%"
cd "%folder_name%"

REM Create checkpoint subfolder
mkdir "downloaded_checkpoint"

REM Create training_data subfolder
mkdir "training_data"

REM Copy required files from the template directory
copy /Y "..\src\scripts\3_download_checkpoint.bat" ".\" > nul 2>&1
copy /Y "..\src\scripts\4_preprocess_data.bat" ".\" > nul 2>&1
copy /Y "..\src\scripts\5_convert_data.bat" ".\" > nul 2>&1
copy /Y "..\src\scripts\6_train.bat" ".\" > nul 2>&1
copy /Y "..\src\scripts\download_checkpoint.py" ".\" > nul 2>&1
copy /Y "..\src\scripts\unify_sample_rate.py" ".\" > nul 2>&1
copy /Y "..\src\scripts\get_sample_rate.py" ".\" > nul 2>&1
echo %folder_name% folder has been successfully created! Please copy your audio files and metadata.csv into the training_data subfolder within and then run 3_download_checkpoint.bat.

pause