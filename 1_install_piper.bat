@echo off

cd /d "%~dp0"

REM Start WSL and run the commands in a bash script
wsl bash -c "cd $(wslpath '%~dp0') && bash -s" < "%~dp0\src\wsl\install_piper.sh"
pause