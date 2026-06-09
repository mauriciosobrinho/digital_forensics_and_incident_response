from datetime import datetime, timezone
from typing import Any

from src.agents.state import InvestigationState


def append_workflow_event(
    state: InvestigationState,
    *,
    stage: str,
    decision: str,
    details: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:

    return [
        *state.get("workflow_timeline", []),
        {
            "timestamp_utc": datetime.now(
                timezone.utc
            ).isoformat(),
            "stage": stage,
            "decision": decision,
            "details": details or {},
        },
    ]


def set_workflow_stage(
    state: InvestigationState,
    stage: str,
) -> InvestigationState:
    return {
        **state,
        "workflow_stage": stage,
    }