import json
from pathlib import Path
from typing import Any

from src.agents.artifact_loader import (
    build_anomaly_summary,
    build_risk_summary,
    load_json_file,
)

from src.agents.graph import (
    build_investigation_graph,
)

from src.config.settings import (
    AGENT_DECISION_LOG_FILE,
    AGENT_INVESTIGATION_FILE,
    AGENT_RESPONSE_PLAYBOOK_FILE,
    ANOMALY_SCORES_FILE,
    ATTACK_TIMELINE_FILE,
    FORENSIC_EVIDENCE_FILE,
    IOCS_FILE,
    RISK_SCORES_FILE,
    HUMAN_APPROVAL_REQUEST_FILE,
    HUMAN_APPROVAL_DECISION_FILE,
    INVESTIGATION_MEMORY_FILE,
    LLM_AGENT_REASONING_FILE,
    TOOL_EXECUTION_LOG_FILE,
    AGENT_WORKFLOW_TIMELINE_FILE,
)

from src.config.llm_settings import (
    load_agent_runtime_settings,
)

from src.agents.memory import (
    load_investigation_memory,
    save_investigation_memory,
    update_investigation_memory,
)

# from src.config.settings import (
#     HUMAN_APPROVAL_REQUEST_FILE,
#     HUMAN_APPROVAL_DECISION_FILE,
#     INVESTIGATION_MEMORY_FILE,
#     LLM_AGENT_REASONING_FILE,
#     TOOL_EXECUTION_LOG_FILE,
#     AGENT_WORKFLOW_TIMELINE_FILE,
# )

# from src.config.settings import (
#     AGENT_WORKFLOW_TIMELINE_FILE,
# )


def save_json(
    payload: dict[str, Any] | list[dict[str, Any]],
    output_file: Path,
) -> None:
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_file.open(
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            payload,
            f,
            indent=2,
            ensure_ascii=False,
        )


def run_agent_investigation(
    dry_run: bool = True,
    human_approval_status: str = "pending",
) -> dict[str, Any]:
    
    settings = load_agent_runtime_settings()
    memory = load_investigation_memory(
        INVESTIGATION_MEMORY_FILE
    )

    forensic_evidence = load_json_file(
        FORENSIC_EVIDENCE_FILE
    )

    attack_timeline = load_json_file(
        ATTACK_TIMELINE_FILE
    )

    iocs = load_json_file(
        IOCS_FILE
    )

    risk_summary = build_risk_summary(
        RISK_SCORES_FILE
    )

    anomaly_summary = build_anomaly_summary(
        ANOMALY_SCORES_FILE
    )

    graph = build_investigation_graph()

    initial_state = {
        "forensic_evidence": forensic_evidence,
        "attack_timeline": attack_timeline,
        "iocs": iocs,
        "risk_summary": risk_summary,
        "anomaly_summary": anomaly_summary,
        "dry_run": dry_run,
        "human_approval_status": human_approval_status,
        "decision_log": [],
        "human_approval_mode": settings.human_approval_mode,
        "agents_use_llm": settings.agents_use_llm,
        "memory": memory,
        "tool_execution_log": [],
        "llm_agent_reasoning": [],
        "workflow_stage": "initialized",
        "workflow_timeline": [],
        "human_loop_count": 0,
        "human_decision_scenario": settings.human_decision_scenario,
    }

    final_state = graph.invoke(
        initial_state
    )

    investigation = {
        "triage": final_state["triage_result"],
        "forensic_analysis": final_state["forensic_analysis"],
        "response_recommendation": final_state["response_recommendation"],
        "human_approval_required": final_state.get(
            "human_approval_required",
            True,
        ),
        "dry_run": dry_run,
        "human_approval_request": final_state["human_approval_request"],
        "human_approval_response": final_state["human_approval_response"],
        "approved_actions": final_state.get(
            "approved_actions",
            [],
        ),
        "rejected_actions": final_state.get(
            "rejected_actions",
            [],
        ),

        "workflow_stage": final_state.get("workflow_stage"),
        "workflow_timeline": final_state.get("workflow_timeline", []),
        "modified_action_plan": final_state.get("modified_action_plan", {}),
    }

    save_json(
        investigation,
        AGENT_INVESTIGATION_FILE,
    )

    save_json(
        final_state.get(
            "decision_log",
            [],
        ),
        AGENT_DECISION_LOG_FILE,
    )

    save_json(
        final_state["response_recommendation"],
        AGENT_RESPONSE_PLAYBOOK_FILE,
    )

    save_json(
        final_state["human_approval_request"],
        HUMAN_APPROVAL_REQUEST_FILE,
    )

    save_json(
        final_state["human_approval_response"],
        HUMAN_APPROVAL_DECISION_FILE,
    )

    save_json(
        final_state.get(
            "llm_agent_reasoning",
            [],
        ),
        LLM_AGENT_REASONING_FILE,
    )

    save_json(
        final_state.get(
            "tool_execution_log",
            [],
        ),
        TOOL_EXECUTION_LOG_FILE,
    )

    updated_memory = update_investigation_memory(
        memory=memory,
        investigation_summary=investigation,
    )

    save_investigation_memory(
        updated_memory,
        INVESTIGATION_MEMORY_FILE,
    )

    save_json(
        final_state.get(
            "workflow_timeline",
            [],
        ),
        AGENT_WORKFLOW_TIMELINE_FILE,
    )

    return investigation