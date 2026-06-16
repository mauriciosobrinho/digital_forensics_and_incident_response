#!/usr/bin/env bash
set -euo pipefail

OUTPUT_FILE=".env.deterministic"

cat > "$OUTPUT_FILE" <<'EOF'
AGENTS_USE_LLM=false
AGENTS_DRY_RUN=true
HUMAN_APPROVAL_MODE=simulated
HUMAN_DECISION_SCENARIO=approve
LANGGRAPH_CHECKPOINT_BACKEND=memory
EOF

echo "[set_env_deterministic] Created $OUTPUT_FILE."
echo "[set_env_deterministic] This script does NOT overwrite .env."
echo "[set_env_deterministic] To use it manually, copy it yourself:"
echo "cp $OUTPUT_FILE .env"