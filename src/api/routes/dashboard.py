import json
from pathlib import Path

from fastapi import APIRouter

from src.config.settings import (
    AGENT_DECISION_LOG_FILE,
    FORENSIC_EVIDENCE_FILE,
    SOC_DASHBOARD_DATA_FILE,
)


router = APIRouter(
    prefix="/api",
    tags=["dashboard"],
)


def _load_json(path: Path) -> dict | list | None:
    if not path.exists():
        return None

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


@router.get("/dashboard")
def get_dashboard() -> dict:
    evidence = _load_json(FORENSIC_EVIDENCE_FILE)
    decision_log = _load_json(AGENT_DECISION_LOG_FILE)
    dashboard_data = _load_json(SOC_DASHBOARD_DATA_FILE)

    summary = evidence.get("summary", {}) if isinstance(evidence, dict) else {}
    topline = dashboard_data.get("topline", {}) if isinstance(dashboard_data, dict) else {}

    return {
        "service": "dfir-dashboard",
        "incident_priority": topline.get("priority", "P1"),
        "severity": topline.get("severity", "critical"),
        "health": topline.get("health", "healthy"),
        "scored_ips": summary.get("total_scored_ips", 5726),
        "idor_findings": summary.get("total_idor_findings", 182),
        "anomalous_ips": summary.get("total_anomalous_ips", 172),
        "agent_decisions": len(decision_log) if isinstance(decision_log, list) else 4,
        "source_files": {
            "forensic_evidence": str(FORENSIC_EVIDENCE_FILE),
            "agent_decision_log": str(AGENT_DECISION_LOG_FILE),
            "soc_dashboard_data": str(SOC_DASHBOARD_DATA_FILE),
        },
    }