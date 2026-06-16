@echo off
setlocal

set OUTPUT_FILE=.env.deterministic

(
echo AGENTS_USE_LLM=false
echo AGENTS_DRY_RUN=true
echo HUMAN_APPROVAL_MODE=simulated
echo HUMAN_DECISION_SCENARIO=approve
echo LANGGRAPH_CHECKPOINT_BACKEND=memory
) > %OUTPUT_FILE%

echo [set_env_deterministic] Created %OUTPUT_FILE%.
echo [set_env_deterministic] This script does NOT overwrite .env.
echo [set_env_deterministic] To use it manually, copy it yourself:
echo copy %OUTPUT_FILE% .env

endlocal