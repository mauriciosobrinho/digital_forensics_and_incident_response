#!/usr/bin/env bash
set -euo pipefail

if [ ! -f "data/raw/three_months.csv" ]; then
  echo "[run_pipeline] Missing required dataset: data/raw/three_months.csv"
  echo "Copy the original challenge CSV to data/raw/three_months.csv before running the pipeline."
  exit 1
fi

echo "[run_pipeline] Running full DFIR pipeline..."
python -m src.app