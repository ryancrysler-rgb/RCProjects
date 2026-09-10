@echo off
cd /d "%~dp0"
title DP World Tour shot scraper
echo ============================================================
echo   DP World Tour shot scraper - first run takes a few minutes
echo ============================================================
echo.

set PY=
py -3 --version >nul 2>&1
if %errorlevel%==0 set PY=py -3
if not defined PY python --version >nul 2>&1
if %errorlevel%==0 if not defined PY set PY=python
if not defined PY goto nopython

echo [1/4] Setting up (one time only)...
if not exist ".venv" %PY% -m venv .venv
if not exist ".venv\Scripts\python.exe" goto venvfail

echo [2/4] Installing components...
".venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
".venv\Scripts\python.exe" -m pip install -r requirements.txt --quiet
if errorlevel 1 goto pipfail

echo [3/4] Installing the browser it drives...
".venv\Scripts\python.exe" -m playwright install chromium
if errorlevel 1 goto pipfail

echo [4/4] Starting.
echo.
".venv\Scripts\python.exe" run_all.py
echo.
pause
exit /b 0

:nopython
echo Python is not installed on this PC.
echo.
echo   1. Go to https://www.python.org/downloads/
echo   2. Download and run the installer
echo   3. IMPORTANT - tick "Add python.exe to PATH" on the first screen
echo   4. Then double-click this file again
echo.
pause
exit /b 1

:venvfail
echo Could not create the Python environment in this folder.
echo If this folder is in OneDrive or Program Files, try moving it to your Desktop.
pause
exit /b 1

:pipfail
echo Download failed - check your internet connection and try again.
pause
exit /b 1
