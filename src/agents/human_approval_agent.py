from datetime import datetime, timezone

from src.agents.human_decision_simulator import (
    simulate_human_decision,
)
from src.agents.state import InvestigationState
from src.agents.workflow import (
    append_workflow_event,
)
from src.tools.response_tools import (
    simulate_block_ip,
    simulate_rate_limit,
)


def human_approval_agent(
    state: InvestigationState,
) -> InvestigationState:

    response = state["response_recommendation"]

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
        "dry_run": dry_run,
        "workflow_stage": "awaiting_human_approval",
        "actions_waiting_approval": approval_required_actions,
        "allowed_decisions": [
            "approved_for_dry_run_only",
            "rejected",
            "modified",
            "request_more_evidence",
        ],
    }

    human_decision = simulate_human_decision(
        state
    )

    decision_status = human_decision["decision"]

    approved_actions = []
    rejected_actions = []
    modified_action_plan = {}

    if decision_status == "approved_for_dry_run_only":

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

        workflow_stage = "approved"

    elif decision_status == "rejected":

        rejected_actions = approval_required_actions
        workflow_stage = "rejected"

    elif decision_status == "modified":

        modified_action_plan = {
            "strategy": "rate_limit_first_block_later",
            "reason": (
                "Human reviewer requested lower-risk containment first."
            ),
            "approved_steps": [
                "dynamic_rate_limiting_invoice_search",
                "increase_monitoring_for_high_risk_ips",
            ],
            "deferred_steps": [
                "block_or_challenge_critical_ips",
            ],
        }

        for action in immediate_actions:
            if action["action"] == "dynamic_rate_limiting_invoice_search":
                for endpoint in action.get("targets", []):
                    approved_actions.append(
                        simulate_rate_limit(
                            endpoint=endpoint,
                            dry_run=True,
                        )
                    )

        workflow_stage = "approved_with_modifications"

    elif decision_status == "request_more_evidence":

        workflow_stage = "requesting_more_evidence"

    else:

        workflow_stage = "pending"

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
        "workflow_stage": workflow_stage,
        "rationale": human_decision["rationale"],
    }

    new_state = {
        **state,
        "human_approval_request": request,
        "human_approval_response": decision,
        "approved_actions": approved_actions,
        "rejected_actions": rejected_actions,
        "modified_action_plan": modified_action_plan,
        "human_approval_status": decision_status,
        "workflow_stage": workflow_stage,
        "human_loop_count": state.get(
            "human_loop_count",
            0,
        ) + (
            1
            if decision_status == "request_more_evidence"
            else 0
        ),
        "decision_log": [
            *state.get("decision_log", []),
            {
                "agent": "human_approval_agent",
                "decision": decision_status,
                "workflow_stage": workflow_stage,
                "reason": human_decision["rationale"],
            },
        ],
    }

    return {
        **new_state,
        "workflow_timeline": append_workflow_event(
            new_state,
            stage="human_approval",
            decision=decision_status,
            details={
                "workflow_stage": workflow_stage,
                "approved_actions_count": len(
                    approved_actions
                ),
                "rejected_actions_count": len(
                    rejected_actions
                ),
            },
        ),
    }