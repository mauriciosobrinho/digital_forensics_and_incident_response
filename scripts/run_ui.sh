#!/usr/bin/env bash
set -euo pipefail

echo "[run_ui] Starting Streamlit UI..."
streamlit run src/ui/streamlit_app.py