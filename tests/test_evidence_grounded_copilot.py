from src.agents.evidence_grounded_copilot import build_grounded_answer


def sample_artifacts():
    return {
        "forensic_evidence": {},
        "agent_investigation": {
            "response_recommendation": {
                "recommended_actions": [
                    "Apply rate limiting",
                    "Review suspicious tokens",
                    "Update WAF rules",
                ]
            }
        },
        "nist_incident_report": {
            "questions_answered": {
                "when_did_it_start": "2020-10-01 00:00:00.000000",
                "when_did_it_end": "2020-12-31 23:58:00.000000",
                "how_many_invoices": 10221,
                "how_many_attack_events": 96829,
                "how_many_tokens": 35,
                "was_it_automated": True,
                "patient_zero_candidate": "204.210.158.207",
                "mitre_mapping": [
                    {
                        "tactic": "Discovery",
                        "technique": "Application endpoint and object identifier enumeration",
                        "rationale": "The attacker enumerates invoice-like objects through exposed application endpoints.",
                    }
                ],
            }
        },
        "response_metrics": {
            "time_to_detect": {
                "value_hours": 49865.12,
            },
            "time_to_respond": {
                "value_hours": 0.0,
            },
            "time_to_contain": {
                "value_hours": 0.0,
            },
        },
        "soc_dashboard_data": {
            "topline": {
                "health": "healthy",
                "severity": "critical",
                "priority": "P1",
                "dry_run": True,
                "agent_evaluation_coverage": 100.0,
            }
        },
    }


def test_patient_zero_grounded_answer():
    answer = build_grounded_answer(
        "Who is the patient zero?",
        artifacts=sample_artifacts(),
    )

    assert answer["is_answered"] is True
    assert answer["intent"] == "patient_zero"
    assert "204.210.158.207" in answer["answer"]
    assert answer["confidence"] == "high"
    assert "data/evidence/nist_incident_report.json" in answer["source_artifacts"]


def test_attack_start_grounded_answer():
    answer = build_grounded_answer(
        "When did the attack start?",
        artifacts=sample_artifacts(),
    )

    assert answer["is_answered"] is True
    assert answer["intent"] == "attack_start"
    assert "2020-10-01" in answer["answer"]


def test_automation_grounded_answer():
    answer = build_grounded_answer(
        "Was the attack automated?",
        artifacts=sample_artifacts(),
    )

    assert answer["is_answered"] is True
    assert answer["intent"] == "automation"
    assert answer["technical_payload"]["was_it_automated"] is True


def test_affected_invoices_grounded_answer():
    answer = build_grounded_answer(
        "How many invoices were affected?",
        artifacts=sample_artifacts(),
    )

    assert answer["is_answered"] is True
    assert answer["intent"] == "affected_invoices"
    assert answer["technical_payload"]["invoices_involved"] == 10221


def test_containment_grounded_answer():
    answer = build_grounded_answer(
        "What containment is recommended?",
        artifacts=sample_artifacts(),
    )

    assert answer["is_answered"] is True
    assert answer["intent"] == "containment"
    assert answer["technical_payload"]["requires_human_approval"] is True


def test_response_metrics_grounded_answer():
    answer = build_grounded_answer(
        "What are the TTD TTR TTC metrics?",
        artifacts=sample_artifacts(),
    )

    assert answer["is_answered"] is True
    assert answer["intent"] == "response_metrics"
    assert answer["technical_payload"]["TTR"]["value_hours"] == 0.0


def test_idor_evidence_grounded_answer():
    answer = build_grounded_answer(
        "What evidence supports IDOR exploitation?",
        artifacts=sample_artifacts(),
    )

    assert answer["is_answered"] is True
    assert answer["intent"] == "idor_evidence"
    assert "IDOR" in answer["answer"]


def test_mitre_grounded_answer():
    answer = build_grounded_answer(
        "Which MITRE techniques apply?",
        artifacts=sample_artifacts(),
    )

    assert answer["is_answered"] is True
    assert answer["intent"] == "mitre_mapping"
    assert "mitre_mapping" in answer["technical_payload"]


def test_human_escalation_grounded_answer():
    answer = build_grounded_answer(
        "What should be escalated to a human reviewer?",
        artifacts=sample_artifacts(),
    )

    assert answer["is_answered"] is True
    assert answer["intent"] == "human_escalation"
    assert answer["technical_payload"]["human_approval_required"] is True


def test_unknown_question_falls_back_to_rag():
    answer = build_grounded_answer(
        "Explain the general security policy.",
        artifacts=sample_artifacts(),
    )

    assert answer["is_answered"] is False
    assert answer["fallback_to_rag"] is True