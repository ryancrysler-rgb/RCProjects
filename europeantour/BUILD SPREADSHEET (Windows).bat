@echo off
cd /d "%~dp0"
title Build the shot-by-shot spreadsheet
echo Building SHOT_BY_SHOT.csv from everything captured so far...
echo.
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" build_shots.py
) else (
  python build_shots.py
)
