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
)


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

    return investigation