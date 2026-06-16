@echo off
setlocal

echo [validate_static] Compiling critical modules...
python -m py_compile src/app.py src/ui/streamlit_app.py src/reporting/pdf_exporter.py scripts/generate_final_delivery_package.py
if errorlevel 1 exit /b 1

echo [validate_static] Compiling Sprint 4.1 evidence-grounded copilot modules...
python -m py_compile src/agents/evidence_router.py src/agents/evidence_answer_templates.py src/agents/evidence_grounded_copilot.py src/agents/conversation_agent.py
if errorlevel 1 exit /b 1

echo [validate_static] Compiling Sprint 4.2 vector RAG modules...
python -m py_compile src/config/embedding_settings.py
if errorlevel 1 exit /b 1

python -m py_compile src/rag/vector/artifact_loader.py
if errorlevel 1 exit /b 1

python -m py_compile src/rag/vector/hash_embeddings.py
if errorlevel 1 exit /b 1

python -m py_compile src/rag/vector/chroma_store.py
if errorlevel 1 exit /b 1

python -m py_compile src/rag/vector/build_vector_store.py
if errorlevel 1 exit /b 1

echo [validate_static] Compiling Sprint 4.2 memory, prompts and professional copilot modules...
python -m py_compile src/agents/context/session_context.py
if errorlevel 1 exit /b 1

python -m py_compile src/agents/llm_intent_classifier.py
if errorlevel 1 exit /b 1

python -m py_compile src/agents/professional_soc_copilot.py
if errorlevel 1 exit /b 1

echo [validate_static] Compiling Sprint 4.2 prompt library...
python -m py_compile src/agents/prompts/base.py
if errorlevel 1 exit /b 1

python -m py_compile src/agents/prompts/triage_prompt.py
if errorlevel 1 exit /b 1

python -m py_compile src/agents/prompts/forensic_prompt.py
if errorlevel 1 exit /b 1

python -m py_compile src/agents/prompts/response_prompt.py
if errorlevel 1 exit /b 1

python -m py_compile src/agents/prompts/soc_copilot_prompt.py
if errorlevel 1 exit /b 1

python -m py_compile src/agents/prompts/intent_classifier_prompt.py
if errorlevel 1 exit /b 1

python -m py_compile src/agents/prompts/human_approval_prompt.py
if errorlevel 1 exit /b 1

python -m py_compile src/agents/prompts/evidence_synthesis_prompt.py
if errorlevel 1 exit /b 1

echo [validate_static] Compiling Sprint 4.2 DFIR skills...
python -m py_compile src/agents/skills/patient_zero_skill.py
if errorlevel 1 exit /b 1

python -m py_compile src/agents/skills/timeline_skill.py
if errorlevel 1 exit /b 1

python -m py_compile src/agents/skills/containment_skill.py
if errorlevel 1 exit /b 1

python -m py_compile src/agents/skills/impact_skill.py
if errorlevel 1 exit /b 1

python -m py_compile src/agents/skills/mitre_skill.py
if errorlevel 1 exit /b 1

python -m py_compile src/agents/skills/root_cause_skill.py
if errorlevel 1 exit /b 1

python -m py_compile src/agents/skills/metrics_skill.py
if errorlevel 1 exit /b 1

python -m py_compile src/agents/skills/skill_registry.py
if errorlevel 1 exit /b 1

echo [validate_static] Compiling Sprint 4.2 MCP gateway modules...
python -m py_compile src/mcp_gateway/tool_registry.py
if errorlevel 1 exit /b 1

python -m py_compile src/mcp_gateway/server/stdio_server.py
if errorlevel 1 exit /b 1

echo [validate_static] Compiling Sprint 4.2 evaluation modules...

python -m py_compile src/evaluation/soc_copilot_semantic_quality.py
if errorlevel 1 exit /b 1

python -m py_compile src/evaluation/llm_metrics.py
if errorlevel 1 exit /b 1

python -m py_compile scripts/run_copilot_question_batch.py
if errorlevel 1 exit /b 1

python -m py_compile tests/test_soc_copilot_llm_quality.py
if errorlevel 1 exit /b 1

python -m py_compile tests/test_soc_copilot_semantic_quality.py
if errorlevel 1 exit /b 1

echo [validate_static] Static validation completed.

endlocal