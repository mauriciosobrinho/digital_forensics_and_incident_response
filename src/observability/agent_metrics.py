from datetime import datetime, timezone
from typing import Any


def _count_tool_calls(
    tool_log: Any,
) -> int:
    if isinstance(tool_log, list):
        return len(tool_log)

    if isinstance(tool_log, dict):
        return len(
            tool_log.get(
                "executions",
                [],
            )
        )

    return 0


def build_agent_metrics(
    *,
    agent_investigation: dict[str, Any],
    decision_log: list[dict[str, Any]],
    workflow_timeline: list[dict[str, Any]],
    tool_execution_log: Any,
    mcp_tool_execution_log: Any,
    llm_reasoning: Any,
) -> dict[str, Any]:

    human_response = agent_investigation.get(
        "human_approval_response",
        {},
    )

    approved_actions = agent_investigation.get(
        "approved_actions",
        [],
    )

    dry_run_actions = [
        action
        for action in approved_actions
        if action.get("dry_run") is True
    ]

    return {
        "metrics_type": "agent_metrics",
        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "n_agent_decisions": len(
            decision_log
        ),
        "n_workflow_events": len(
            workflow_timeline
        ),
        "n_human_approvals": (
            1
            if human_response
            else 0
        ),
        "human_approval_status": human_response.get(
            "decision"
        ),
        "human_loop_count": agent_investigation.get(
            "human_loop_count",
            0,
        ),
        "n_tool_calls": (
            _count_tool_calls(tool_execution_log)
            + _count_tool_calls(mcp_tool_execution_log)
        ),
        "n_llm_calls": len(
            llm_reasoning
        )
        if isinstance(llm_reasoning, list)
        else 0,
        "n_dry_run_actions": len(
            dry_run_actions
        ),
        "dry_run": agent_investigation.get(
            "dry_run",
            True,
        ),
        "status": "healthy"
        if len(decision_log) >= 4
        else "degraded",
    }