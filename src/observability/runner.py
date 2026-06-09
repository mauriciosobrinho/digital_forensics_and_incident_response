import json
from pathlib import Path
from typing import Any

from src.config.settings import (
    AGENT_DECISION_LOG_FILE,
    AGENT_EVAL_REPORT_FILE,
    AGENT_INVESTIGATION_FILE,
    AGENT_METRICS_FILE,
    AGENT_WORKFLOW_TIMELINE_FILE,
    ANOMALOUS_IPS_FILE,
    ANOMALY_SCORES_FILE,
    FORENSIC_EVIDENCE_FILE,
    HEALTHCHECK_FILE,
    IDOR_FINDINGS_FILE,
    IOCS_FILE,
    IP_FEATURES_FILE,
    LLM_AGENT_REASONING_FILE,
    MCP_TOOL_EXECUTION_LOG_FILE,
    NIST_INCIDENT_REPORT_FILE,
    PARSED_EVENTS_FILE,
    PLATFORM_METRICS_FILE,
    SOC_DASHBOARD_DATA_FILE,
    TOOL_EXECUTION_LOG_FILE,
)
from src.observability.agent_metrics import (
    build_agent_metrics,
)
from src.observability.healthcheck import (
    build_healthcheck,
)
from src.observability.platform_metrics import (
    build_platform_metrics,
)
from src.observability.soc_dashboard_data import (
    build_soc_dashboard_data,
)


def _load_json(
    path: Path,
    default: Any,
) -> Any:
    if not path.exists():
        return default

    with path.open(
        "r",
        encoding="utf-8",
    ) as f:
        return json.load(f)


def _save_json(
    data: dict[str, Any],
    path: Path,
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False,
            default=str,
        )


def run_observability() -> dict[str, Any]:

    forensic_evidence = _load_json(
        FORENSIC_EVIDENCE_FILE,
        {},
    )

    iocs = _load_json(
        IOCS_FILE,
        {},
    )

    agent_investigation = _load_json(
        AGENT_INVESTIGATION_FILE,
        {},
    )

    decision_log = _load_json(
        AGENT_DECISION_LOG_FILE,
        [],
    )

    workflow_timeline = _load_json(
        AGENT_WORKFLOW_TIMELINE_FILE,
        [],
    )

    tool_execution_log = _load_json(
        TOOL_EXECUTION_LOG_FILE,
        [],
    )

    mcp_tool_execution_log = _load_json(
        MCP_TOOL_EXECUTION_LOG_FILE,
        [],
    )

    llm_reasoning = _load_json(
        LLM_AGENT_REASONING_FILE,
        [],
    )

    nist_report = _load_json(
        NIST_INCIDENT_REPORT_FILE,
        {},
    )

    evaluation_report = _load_json(
        AGENT_EVAL_REPORT_FILE,
        {},
    )

    platform_metrics = build_platform_metrics(
        paths={
            "parsed_events": PARSED_EVENTS_FILE,
            "ip_features": IP_FEATURES_FILE,
            "idor_findings": IDOR_FINDINGS_FILE,
            "anomaly_scores": ANOMALY_SCORES_FILE,
            "anomalous_ips": ANOMALOUS_IPS_FILE,
        },
        forensic_evidence=forensic_evidence,
        iocs=iocs,
    )

    agent_metrics = build_agent_metrics(
        agent_investigation=agent_investigation,
        decision_log=decision_log,
        workflow_timeline=workflow_timeline,
        tool_execution_log=tool_execution_log,
        mcp_tool_execution_log=mcp_tool_execution_log,
        llm_reasoning=llm_reasoning,
    )

    required_artifacts = {
        "forensic_evidence": FORENSIC_EVIDENCE_FILE,
        "attack_iocs": IOCS_FILE,
        "agent_investigation": AGENT_INVESTIGATION_FILE,
        "agent_decision_log": AGENT_DECISION_LOG_FILE,
        "workflow_timeline": AGENT_WORKFLOW_TIMELINE_FILE,
        "nist_incident_report": NIST_INCIDENT_REPORT_FILE,
        "agent_eval_report": AGENT_EVAL_REPORT_FILE,
    }

    healthcheck = build_healthcheck(
        required_artifacts=required_artifacts,
        platform_metrics=platform_metrics,
        agent_metrics=agent_metrics,
    )

    dashboard_data = build_soc_dashboard_data(
        platform_metrics=platform_metrics,
        agent_metrics=agent_metrics,
        healthcheck=healthcheck,
        nist_report=nist_report,
        evaluation_report=evaluation_report,
    )

    _save_json(
        platform_metrics,
        PLATFORM_METRICS_FILE,
    )

    _save_json(
        agent_metrics,
        AGENT_METRICS_FILE,
    )

    _save_json(
        healthcheck,
        HEALTHCHECK_FILE,
    )

    _save_json(
        dashboard_data,
        SOC_DASHBOARD_DATA_FILE,
    )

    return dashboard_data


def main() -> None:
    dashboard = run_observability()

    topline = dashboard.get(
        "topline",
        {},
    )

    print("\nObservability artifacts generated.")
    print(
        f"Health: {topline.get('health')} | "
        f"Severity: {topline.get('severity')} | "
        f"Coverage: {topline.get('agent_evaluation_coverage')}%"
    )


if __name__ == "__main__":
    main()