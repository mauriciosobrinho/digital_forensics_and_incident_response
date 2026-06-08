from datetime import datetime, timezone

from src.agents.state import InvestigationState
from src.tools.response_tools import (
    simulate_block_ip,
    simulate_rate_limit,
)


def human_approval_agent(
    state: InvestigationState,
) -> InvestigationState:
    response = state["response_recommendation"]
    mode = state.get(
        "human_approval_mode",
        "simulated",
    )
    dry_run = state.get(
        "dry_run",
        True,
    )

    immediate_actions = (
        response
        .get("recommended_containment", {})
        .get("immediate", [])
    )

    approval_required_actions = [
        action
        for action in immediate_actions
        if action.get("requires_human_approval")
    ]

    request = {
        "agent": "human_approval_agent",
        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "approval_required": len(
            approval_required_actions
        ) > 0,
        "mode": mode,
        "dry_run": dry_run,
        "actions_waiting_approval": approval_required_actions,
        "allowed_decisions": [
            "approved_for_dry_run_only",
            "approved",
            "rejected",
            "requires_more_context",
        ],
    }

    if mode == "simulated":
        decision_status = "approved_for_dry_run_only"
    else:
        decision_status = state.get(
            "human_approval_status",
            "pending",
        )

    approved_actions = []
    rejected_actions = []

    if decision_status in {
        "approved_for_dry_run_only",
        "approved",
    }:
        for action in approval_required_actions:
            if action["action"] == "block_or_challenge_critical_ips":
                for ip in action.get("targets", []):
                    approved_actions.append(
                        simulate_block_ip(
                            ip=ip,
                            dry_run=True,
                        )
                    )

    for action in immediate_actions:
        if not action.get("requires_human_approval"):
            if action["action"] == "dynamic_rate_limiting_invoice_search":
                for endpoint in action.get("targets", []):
                    approved_actions.append(
                        simulate_rate_limit(
                            endpoint=endpoint,
                            dry_run=True,
                        )
                    )

    decision = {
        "agent": "human_approval_agent",
        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "decision": decision_status,
        "dry_run": dry_run,
        "approved_actions_count": len(
            approved_actions
        ),
        "rejected_actions_count": len(
            rejected_actions
        ),
    }

    return {
        **state,
        "human_approval_request": request,
        "human_approval_response": decision,
        "approved_actions": approved_actions,
        "rejected_actions": rejected_actions,
        "human_approval_status": decision_status,
        "decision_log": [
            *state.get("decision_log", []),
            {
                "agent": "human_approval_agent",
                "decision": decision_status,
                "reason": "Simulated approval gate produced dry-run-only action approval.",
            },
        ],
    }