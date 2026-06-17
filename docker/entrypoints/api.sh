#!/usr/bin/env bash
set -euo pipefail

echo "[api] Starting DFIR FastAPI service..."

uvicorn src.api.main:app \
  --host 0.0.0.0 \
  --port 8000