#!/usr/bin/env bash
set -euo pipefail

echo "[validate_static] Compiling critical modules..."
python -m py_compile src/app.py src/ui/streamlit_app.py src/reporting/pdf_exporter.py scripts/generate_final_delivery_package.py

echo "[validate_static] Compiling Sprint 4.1 modules..."
python -m py_compile src/agents/evidence_router.py src/agents/evidence_answer_templates.py src/agents/evidence_grounded_copilot.py src/agents/conversation_agent.py

echo "[validate_static] Static validation completed."