#!/usr/bin/env bash
set -euo pipefail

echo "[validate_release] Step 1/4 - Setting deterministic environment..."
scripts/set_env_deterministic.sh

echo "[validate_release] Step 2/4 - Static validation..."
scripts/validate_static.sh

echo "[validate_release] Step 3/4 - Running full pipeline..."
scripts/run_pipeline.sh

echo "[validate_release] Step 4/4 - Running test suite..."
scripts/run_tests.sh

echo "[validate_release] Release validation completed successfully."