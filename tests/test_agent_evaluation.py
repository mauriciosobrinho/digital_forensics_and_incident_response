from src.evaluation.agent_evaluator import (
    evaluate_agents,
)
from src.evaluation.evaluation_report import (
    build_evaluation_report,
)
from src.evaluation.question_bank import (
    build_agent_question_bank,
)


def sample_investigation():
    return {
        "triage": {
            "severity": "critical",
            "priority": "P1",
            "incident_classification": "Potential IDOR exploitation",
            "initial_hypotheses": [
                "Automated invoice enumeration",
            ],
            "investigation_plan": [
                "Review top risk IPs",
            ],
        },
        "forensic_analysis": {
            "patient_zero_candidate": "1.1.1.1",
            "attack_window": {
                "first_seen": "2020-10-01",
            },
            "first_seen": "2020-10-01",
            "automation_assessment": "likely automated",
            "attack_pattern": "sequential invoice enumeration",
            "mitre_attack_mapping": [
                "Collection",
                "Discovery",
            ],
        },
        "response_recommendation": {
            "human_approval_required": True,
            "recommended_containment": {
                "immediate": [
                    {
                        "action": "block_or_challenge_critical_ips",
                        "requires_human_approval": True,
                    }
                ]
            },
            "mini_playbook": [
                "Validate evidence",
                "Apply dry-run containment",
            ],
        },
        "human_approval_request": {
            "approval_required": True,
        },
        "human_approval_response": {
            "decision": "approved_for_dry_run_only",
        },
        "approved_actions": [],
        "rejected_actions": [],
        "modified_action_plan": {},
        "workflow_stage": "approved",
        "workflow_timeline": [
            {
                "stage": "human_approval",
                "decision": "approved_for_dry_run_only",
            }
        ],
        "human_loop_count": 1,
    }


def test_question_bank_has_requirements():
    questions = build_agent_question_bank()

    assert len(questions) >= 10
    assert all(
        "challenge_requirement" in question
        for question in questions
    )


def test_evaluate_agents():
    results = evaluate_agents(
        investigation=sample_investigation(),
        decision_log=[
            {
                "agent": "triage_agent",
                "decision": "classified_incident",
            }
        ],
    )

    assert results["total_questions"] >= 10
    assert len(results["results"]) >= 10


def test_build_evaluation_report():
    results = evaluate_agents(
        investigation=sample_investigation(),
        decision_log=[
            {
                "agent": "triage_agent",
                "decision": "classified_incident",
            }
        ],
    )

    report = build_evaluation_report(
        results
    )

    assert "summary" in report
    assert "agent_scores" in report
    assert report["summary"]["overall_coverage_percent"] > 0