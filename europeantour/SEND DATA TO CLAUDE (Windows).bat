@echo off
cd /d "%~dp0"
title Collect captured data
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" share.py
) else (
  python share.py
)
