@echo off
cd /d "%~dp0"
title Find shot-by-shot data
echo ============================================================
echo   Searching everything already captured for shot-by-shot
echo   data. Nothing is downloaded - this reads your own files.
echo ============================================================
echo.
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" find_shots.py
) else (
  python find_shots.py
)
