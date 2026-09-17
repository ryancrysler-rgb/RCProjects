@echo off
cd /d "%~dp0"
title Get shot by shot data
echo ============================================================
echo   Opening the Shot Tracker to capture shot-by-shot data.
echo.
echo   It asks which tournament and round first - press Enter
echo   for this week's - then a browser opens. Click the player,
echo   open AI SHOT COMMENTARY and step through the holes.
echo   Close the browser window when you are done.
echo ============================================================
echo.
if not exist ".venv\Scripts\python.exe" (
  echo Run "START HERE (Windows).bat" first to set things up.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" capture_shots.py
