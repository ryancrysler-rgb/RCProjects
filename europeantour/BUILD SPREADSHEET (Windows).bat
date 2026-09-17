@echo off
cd /d "%~dp0"
title Build the shot-by-shot spreadsheet
echo Building the spreadsheet from everything captured for this
echo tournament so far. It is saved as SHOT_BY_SHOT_<tournament>.csv
echo.
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" build_shots.py
) else (
  python build_shots.py
)
