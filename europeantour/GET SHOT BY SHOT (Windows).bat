@echo off
cd /d "%~dp0"
title Get shot by shot data
echo ============================================================
echo   Opening the Shot Tracker to capture shot-by-shot data.
echo.
echo   A browser will open and click through to the Shots view
echo   by itself. Accept cookies if asked, then leave it alone.
echo   It takes about a minute.
echo ============================================================
echo.
if not exist ".venv\Scripts\python.exe" (
  echo Run "START HERE (Windows).bat" first to set things up.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" capture_shots.py
