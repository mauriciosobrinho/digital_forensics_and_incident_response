#!/usr/bin/env bash
set -euo pipefail

cat > .env.example.llm <<'EOF'
AGENTS_USE_LLM=true
AGENTS_DRY_RUN=true
HUMAN_APPROVAL_MODE=simulated
HUMAN_DECISION_SCENARIO=approve
LANGGRAPH_CHECKPOINT_BACKEND=memory

LLM_PROVIDER=groq
LLM_API_KEY=replace_me
LLM_MODEL=llama-3.3-70b-versatile
LLM_BASE_URL=https://api.groq.com/openai/v1
EOF

echo "[set_env_llm_example] .env.example.llm created."
echo "Copy it to .env only after replacing LLM_API_KEY."