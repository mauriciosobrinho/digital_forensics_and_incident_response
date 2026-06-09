from datetime import datetime, timezone
from typing import Any

from src.agents.state import InvestigationState
from src.config.llm_settings import (
    load_agent_runtime_settings,
)


def simulate_human_decision(
    state: InvestigationState,
) -> dict[str, Any]:

    settings = load_agent_runtime_settings()

    scenario = state.get(
        "human_decision_scenario",
        settings.human_decision_scenario,
    )

    loop_count = state.get(
        "human_loop_count",
        0,
    )

    if scenario == "request_more_evidence" and loop_count == 0:
        decision = "request_more_evidence"
        rationale = (
            "Human reviewer requested additional forensic evidence "
            "before approving containment."
        )

    elif scenario == "reject":
        decision = "rejected"
        rationale = (
            "Human reviewer rejected containment due to possible "
            "false-positive or insufficient business context."
        )

    elif scenario == "modify":
        decision = "modified"
        rationale = (
            "Human reviewer approved only a modified dry-run plan, "
            "prioritizing rate limiting before IP blocking."
        )

    else:
        decision = "approved_for_dry_run_only"
        rationale = (
            "Human reviewer approved containment simulation only. "
            "No production action is authorized."
        )

    return {
        "agent": "human_decision_simulator",
        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "scenario": scenario,
        "decision": decision,
        "rationale": rationale,
        "loop_count": loop_count,
        "dry_run": state.get(
            "dry_run",
            True,
        ),
    }