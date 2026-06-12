@echo off
setlocal

(
echo AGENTS_USE_LLM=true
echo AGENTS_DRY_RUN=true
echo HUMAN_APPROVAL_MODE=simulated
echo HUMAN_DECISION_SCENARIO=approve
echo LANGGRAPH_CHECKPOINT_BACKEND=memory
echo.
echo LLM_PROVIDER=groq
echo LLM_API_KEY=replace_me
echo LLM_MODEL=llama-3.3-70b-versatile
echo LLM_BASE_URL=https://api.groq.com/openai/v1
) > .env.example.llm

echo [set_env_llm_example] .env.example.llm created.
echo Copy it to .env only after replacing LLM_API_KEY.

endlocal