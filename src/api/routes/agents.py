import json
from pathlib import Path

from fastapi import APIRouter

from src.config.settings import (
    AGENT_DECISION_LOG_FILE,
    AGENT_EVAL_REPORT_FILE,
    AGENT_EVAL_RESULTS_FILE,
    AGENT_INVESTIGATION_FILE,
    AGENT_RESPONSE_PLAYBOOK_FILE,
    HUMAN_APPROVAL_DECISION_FILE,
    HUMAN_APPROVAL_REQUEST_FILE,
)


router = APIRouter(
    prefix="/api",
    tags=["agents"],
)


def _load_json(path: Path) -> dict | list | None:
    if not path.exists():
        return None

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


@router.get("/agents")
def get_agents() -> dict:
    investigation = _load_json(AGENT_INVESTIGATION_FILE)
    decision_log = _load_json(AGENT_DECISION_LOG_FILE)
    evaluation_report = _load_json(AGENT_EVAL_REPORT_FILE)

    return {
        "service": "dfir-agents",
        "dry_run": True,
        "agent_investigation_available": investigation is not None,
        "decision_count": len(decision_log) if isinstance(decision_log, list) else 0,
        "evaluation_available": evaluation_report is not None,
        "human_approval": {
            "request_file_exists": HUMAN_APPROVAL_REQUEST_FILE.exists(),
            "decision_file_exists": HUMAN_APPROVAL_DECISION_FILE.exists(),
        },
        "source_files": {
            "agent_investigation": str(AGENT_INVESTIGATION_FILE),
            "agent_decision_log": str(AGENT_DECISION_LOG_FILE),
            "agent_response_playbook": str(AGENT_RESPONSE_PLAYBOOK_FILE),
            "human_approval_request": str(HUMAN_APPROVAL_REQUEST_FILE),
            "human_approval_decision": str(HUMAN_APPROVAL_DECISION_FILE),
            "agent_eval_results": str(AGENT_EVAL_RESULTS_FILE),
            "agent_eval_report": str(AGENT_EVAL_REPORT_FILE),
        },
    }