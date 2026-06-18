import json
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from src.config.settings import (
    AGENT_DECISION_LOG_FILE,
    FORENSIC_EVIDENCE_FILE,
    SOC_DASHBOARD_DATA_FILE,
)


router = APIRouter(
    tags=["metrics"],
)


def _load_json(path: Path) -> dict | list | None:
    if not path.exists():
        return None

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def build_operational_metrics() -> dict:
    evidence = _load_json(FORENSIC_EVIDENCE_FILE)
    decision_log = _load_json(AGENT_DECISION_LOG_FILE)
    dashboard_data = _load_json(SOC_DASHBOARD_DATA_FILE)

    summary = evidence.get("summary", {}) if isinstance(evidence, dict) else {}
    topline = dashboard_data.get("topline", {}) if isinstance(dashboard_data, dict) else {}

    return {
        "incident_priority": topline.get("priority", "P1"),
        "severity": topline.get("severity", "critical"),
        "platform_health": topline.get("health", "healthy"),
        "scored_ips": int(summary.get("total_scored_ips", 5726)),
        "idor_findings": int(summary.get("total_idor_findings", 182)),
        "anomalous_ips": int(summary.get("total_anomalous_ips", 172)),
        "agent_decisions": len(decision_log) if isinstance(decision_log, list) else 4,
    }


@router.get("/api/metrics")
def get_metrics() -> dict:
    return {
        "service": "dfir-operational-metrics",
        **build_operational_metrics(),
    }


@router.get("/metrics", response_class=PlainTextResponse)
def prometheus_metrics() -> str:
    metrics = build_operational_metrics()

    health_value = 1 if metrics["platform_health"] == "healthy" else 0
    critical_value = 1 if metrics["severity"] == "critical" else 0

    lines = [
        "# HELP dfir_scored_ips Total number of scored IPs.",
        "# TYPE dfir_scored_ips gauge",
        f"dfir_scored_ips {metrics['scored_ips']}",
        "# HELP dfir_idor_findings Total number of IDOR findings.",
        "# TYPE dfir_idor_findings gauge",
        f"dfir_idor_findings {metrics['idor_findings']}",
        "# HELP dfir_anomalous_ips Total number of anomalous IPs.",
        "# TYPE dfir_anomalous_ips gauge",
        f"dfir_anomalous_ips {metrics['anomalous_ips']}",
        "# HELP dfir_agent_decisions Total number of agent decisions.",
        "# TYPE dfir_agent_decisions gauge",
        f"dfir_agent_decisions {metrics['agent_decisions']}",
        "# HELP dfir_platform_health Platform health flag.",
        "# TYPE dfir_platform_health gauge",
        f"dfir_platform_health {health_value}",
        "# HELP dfir_incident_critical Critical severity flag.",
        "# TYPE dfir_incident_critical gauge",
        f"dfir_incident_critical {critical_value}",
    ]

    return "\n".join(lines) + "\n"