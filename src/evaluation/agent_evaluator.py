from typing import Any

from src.agents.soc_assistant import answer_soc_question
from src.evaluation.question_bank import (
    build_agent_question_bank,
)
from src.evaluation.scoring import (
    score_requirement,
)


def _select_agent_payload(
    *,
    question: dict[str, Any],
    investigation: dict[str, Any],
    decision_log: list[dict[str, Any]],
) -> dict[str, Any]:

    agent = question["agent"]

    if agent == "triage_agent":
        return investigation.get(
            "triage",
            {},
        )

    if agent == "forensic_analyst_agent":
        return investigation.get(
            "forensic_analysis",
            {},
        )

    if agent == "response_advisor_agent":
        return investigation.get(
            "response_recommendation",
            {},
        )

    if agent == "human_approval_agent":
        return {
            "human_approval_request": investigation.get(
                "human_approval_request",
                {},
            ),
            "human_approval_response": investigation.get(
                "human_approval_response",
                {},
            ),
            "human_approval_status": investigation.get(
                "human_approval_response",
                {},
            ).get("decision"),
            "approved_actions": investigation.get(
                "approved_actions",
                [],
            ),
            "rejected_actions": investigation.get(
                "rejected_actions",
                [],
            ),
            "modified_action_plan": investigation.get(
                "modified_action_plan",
                {},
            ),
        }

    if agent == "langgraph_workflow":
        return {
            "workflow_stage": investigation.get(
                "workflow_stage",
            ),
            "workflow_timeline": investigation.get(
                "workflow_timeline",
                [],
            ),
            "human_loop_count": investigation.get(
                "human_loop_count",
                0,
            ),
            "decision_log": decision_log,
        }

    if agent == "soc_copilot":
        return answer_soc_question(
            question["question"]
        )

    return {}


def evaluate_agents(
    *,
    investigation: dict[str, Any],
    decision_log: list[dict[str, Any]],
) -> dict[str, Any]:

    question_bank = build_agent_question_bank()

    results = []

    for question in question_bank:
        payload = _select_agent_payload(
            question=question,
            investigation=investigation,
            decision_log=decision_log,
        )

        score = score_requirement(
            payload=payload,
            required_evidence=question["required_evidence"],
        )

        results.append(
            {
                **question,
                "score": score["score"],
                "status": score["status"],
                "passed_checks": score["passed_checks"],
                "total_checks": score["total_checks"],
                "checks": score["checks"],
                "evidence_payload_preview": payload,
            }
        )

    return {
        "evaluation_type": "agent_validation_suite",
        "total_questions": len(results),
        "results": results,
    }