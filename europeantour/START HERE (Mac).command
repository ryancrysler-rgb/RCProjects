#!/bin/bash
cd "$(dirname "$0")" || exit 1
echo "============================================================"
echo "  DP World Tour shot scraper - first run takes a few minutes"
echo "============================================================"
echo

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is not installed."
  echo
  echo "  1. Go to https://www.python.org/downloads/"
  echo "  2. Download and run the installer"
  echo "  3. Then double-click this file again"
  echo
  read -r -p "Press Enter to close... "
  exit 1
fi

echo "[1/4] Setting up (one time only)..."
[ -d .venv ] || python3 -m venv .venv || {
  echo "Could not create the Python environment here."; read -r -p "Press Enter... "; exit 1; }

echo "[2/4] Installing components..."
.venv/bin/python -m pip install --upgrade pip --quiet
.venv/bin/python -m pip install -r requirements.txt --quiet || {
  echo "Download failed - check your internet connection."; read -r -p "Press Enter... "; exit 1; }

echo "[3/4] Installing the browser it drives..."
.venv/bin/python -m playwright install chromium || {
  echo "Browser download failed."; read -r -p "Press Enter... "; exit 1; }

echo "[4/4] Starting."
echo
.venv/bin/python run_all.py
echo
read -r -p "Press Enter to close... "
