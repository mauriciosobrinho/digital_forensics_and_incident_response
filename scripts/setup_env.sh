#!/usr/bin/env bash
set -euo pipefail

echo "[setup_env] Creating virtual environment..."
python -m venv .venv

echo "[setup_env] Upgrading pip..."
if [ -f ".venv/Scripts/python.exe" ]; then
  .venv/Scripts/python.exe -m pip install --upgrade pip
  .venv/Scripts/python.exe -m pip install -r requirements.txt
else
  .venv/bin/python -m pip install --upgrade pip
  .venv/bin/python -m pip install -r requirements.txt
fi

echo "[setup_env] Creating data/raw directory..."
mkdir -p data/raw

echo "[setup_env] Done."
echo "Next step:"
echo "  - Git Bash on Windows: source .venv/Scripts/activate"
echo "  - Linux/macOS: source .venv/bin/activate"
echo "  - Place the raw dataset at: data/raw/three_months.csv"