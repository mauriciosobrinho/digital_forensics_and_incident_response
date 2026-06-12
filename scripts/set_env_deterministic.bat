@echo off
setlocal

(
echo AGENTS_USE_LLM=false
echo AGENTS_DRY_RUN=true
echo HUMAN_APPROVAL_MODE=simulated
echo HUMAN_DECISION_SCENARIO=approve
echo LANGGRAPH_CHECKPOINT_BACKEND=memory
) > .env

echo [set_env_deterministic] .env created:
type .env

endlocal