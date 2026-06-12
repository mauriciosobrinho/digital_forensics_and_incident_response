#!/usr/bin/env bash
set -euo pipefail

cat > .env <<'EOF'
AGENTS_USE_LLM=false
AGENTS_DRY_RUN=true
HUMAN_APPROVAL_MODE=simulated
HUMAN_DECISION_SCENARIO=approve
LANGGRAPH_CHECKPOINT_BACKEND=memory
EOF

echo "[set_env_deterministic] .env created:"
cat .env