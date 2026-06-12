#!/usr/bin/env bash
set -euo pipefail

echo "[run_tests] Reminder: full pytest expects HUMAN_DECISION_SCENARIO=approve."
echo "[run_tests] Running test suite..."
pytest -v