from datetime import datetime, timezone
from typing import Any


def build_soc_dashboard_data(
    *,
    platform_metrics: dict[str, Any],
    agent_metrics: dict[str, Any],
    healthcheck: dict[str, Any],
    nist_report: dict[str, Any],
    evaluation_report: dict[str, Any],
) -> dict[str, Any]:

    incident_summary = nist_report.get(
        "incident_summary",
        {},
    )

    evaluation_summary = evaluation_report.get(
        "summary",
        {},
    )

    return {
        "dashboard_type": "soc_dashboard_data",
        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "topline": {
            "health": healthcheck.get(
                "overall_status"
            ),
            "severity": incident_summary.get(
                "severity"
            ),
            "priority": incident_summary.get(
                "priority"
            ),
            "dry_run": incident_summary.get(
                "dry_run"
            ),
            "agent_evaluation_coverage": evaluation_summary.get(
                "overall_coverage_percent"
            ),
        },
        "pipeline": platform_metrics.get(
            "pipeline_metrics",
            {},
        ),
        "agents": {
            "n_agent_decisions": agent_metrics.get(
                "n_agent_decisions"
            ),
            "n_workflow_events": agent_metrics.get(
                "n_workflow_events"
            ),
            "n_human_approvals": agent_metrics.get(
                "n_human_approvals"
            ),
            "human_approval_status": agent_metrics.get(
                "human_approval_status"
            ),
            "human_loop_count": agent_metrics.get(
                "human_loop_count"
            ),
            "n_llm_calls": agent_metrics.get(
                "n_llm_calls"
            ),
            "n_tool_calls": agent_metrics.get(
                "n_tool_calls"
            ),
            "n_dry_run_actions": agent_metrics.get(
                "n_dry_run_actions"
            ),
        },
        "healthcheck": healthcheck,
    }