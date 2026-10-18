@echo off
cd /d "%~dp0"
title Get shot by shot data
echo ============================================================
echo   Shot-by-shot capture
echo.
echo   A browser opens on the leaderboard. Click the player, open
echo   the Scorecard, expand AI SHOT COMMENTARY and step through
echo   the holes. Close the browser when you are done - the
echo   spreadsheet then builds itself.
echo ============================================================
echo.

rem Set up on first use, so a fresh copy of the folder on any PC needs
rem nothing but this file. Skipped once the environment is in place.
rem The marker is written only after the browser installs, so a setup cut
rem off halfway runs again rather than leaving a capture that cannot start.
if not exist ".venv\setup-complete" goto setup
goto run

:setup
echo First time on this PC - setting things up. This takes a few minutes.
echo.
set PY=
py -3 --version >nul 2>&1
if not errorlevel 1 set PY=py -3
if defined PY goto havepy
python --version >nul 2>&1
if not errorlevel 1 set PY=python
if not defined PY goto nopython

:havepy
echo [1/3] Creating the Python environment...
if not exist ".venv\Scripts\python.exe" %PY% -m venv .venv
if not exist ".venv\Scripts\python.exe" goto venvfail

echo [2/3] Installing components...
".venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
".venv\Scripts\python.exe" -m pip install -r requirements.txt --quiet
if errorlevel 1 goto pipfail

echo [3/3] Installing the browser it drives...
".venv\Scripts\python.exe" -m playwright install chromium
if errorlevel 1 goto pipfail
echo done> ".venv\setup-complete"
echo.
echo Setup done.
echo.

:run
".venv\Scripts\python.exe" capture_shots.py
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
echo If this folder is in Program Files, move it to Documents and try again.
pause
exit /b 1

:pipfail
echo A download failed - check your internet connection and try again.
pause
exit /b 1
