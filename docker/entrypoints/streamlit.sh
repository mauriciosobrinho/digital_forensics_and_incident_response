#!/usr/bin/env bash
set -euo pipefail

echo "[streamlit] Starting DFIR Streamlit UI..."

streamlit run src/ui/streamlit_app.py \
  --server.address=0.0.0.0 \
  --server.port=8501 \
  --browser.gatherUsageStats=false