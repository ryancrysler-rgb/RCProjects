@echo off
cd /d "%~dp0"
title DP World Tour - fetch player data
echo ============================================================
echo   Fetching Laurie Canter's data from the tour's own API
echo   (no browser needed - this is the quick one)
echo ============================================================
echo.

if exist ".venv\Scripts\python.exe" goto run

echo First-time setup...
set PY=
py -3 --version >nul 2>&1
if %errorlevel%==0 set PY=py -3
if not defined PY python --version >nul 2>&1
if %errorlevel%==0 if not defined PY set PY=python
if not defined PY goto nopython
%PY% -m venv .venv
".venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
".venv\Scripts\python.exe" -m pip install requests --quiet

:run
".venv\Scripts\python.exe" fetch_event.py
exit /b 0

:nopython
echo Python is not installed. Get it from https://www.python.org/downloads/
echo and tick "Add python.exe to PATH" during the install.
pause
exit /b 1
