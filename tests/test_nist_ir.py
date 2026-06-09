from src.ir.containment_strategy import (
    build_containment_strategy,
)
from src.ir.nist_lifecycle import (
    build_nist_incident_report,
)
from src.ir.response_metrics import (
    build_response_metrics,
)
from src.ir.root_cause_analysis import (
    build_root_cause_analysis,
)


def sample_forensic_evidence():
    return {
        "summary": {
            "first_seen": "2020-10-01 00:00:00.000000",
            "last_seen": "2020-12-31 23:58:00.000000",
        },
        "top_attackers": [
            {
                "ip": "1.1.1.1",
            }
        ],
    }


def sample_agent_investigation():
    return {
        "dry_run": True,
        "triage": {
            "incident_classification": "Potential IDOR exploitation",
            "severity": "critical",
            "priority": "P1",
        },
        "forensic_analysis": {
            "patient_zero_candidate": "1.1.1.1",
            "attack_window": {
                "first_seen": "2020-10-01 00:00:00.000000",
                "last_seen": "2020-12-31 23:58:00.000000",
            },
            "automation_assessment": {
                "is_likely_automated": True,
            },
            "idor_evidence_assessment": {
                "clear_idor_evidence": True,
            },
            "estimated_impact": {
                "unique_invoices_accessed_by_top_attackers": 10221,
                "unique_tokens_seen": 35,
                "total_attack_events": 96829,
            },
            "mitre_attack_mapping": [
                {
                    "tactic": "Collection",
                }
            ],
        },
        "response_recommendation": {
            "generated_at_utc": "2026-06-09T12:00:00+00:00",
            "mini_playbook": [
                "Apply dry-run containment",
            ],
        },
        "human_approval_response": {
            "generated_at_utc": "2026-06-09T12:00:01+00:00",
        },
    }


def test_build_response_metrics():
    metrics = build_response_metrics(
        forensic_evidence=sample_forensic_evidence(),
        agent_investigation=sample_agent_investigation(),
    )

    assert metrics["time_to_detect"]["metric"] == "TTD"
    assert metrics["time_to_respond"]["metric"] == "TTR"
    assert metrics["time_to_contain"]["metric"] == "TTC"


def test_build_containment_strategy():
    strategy = build_containment_strategy(
        forensic_evidence=sample_forensic_evidence(),
        agent_investigation=sample_agent_investigation(),
    )

    assert "immediate_containment" in strategy
    assert "strategic_containment" in strategy


def test_build_root_cause_analysis():
    analysis = build_root_cause_analysis(
        forensic_evidence=sample_forensic_evidence(),
        agent_investigation=sample_agent_investigation(),
    )

    assert analysis["root_cause"]["category"] == "Broken Access Control / IDOR"
    assert len(analysis["eradication_plan"]) >= 1


def test_build_nist_incident_report():
    forensic = sample_forensic_evidence()
    investigation = sample_agent_investigation()

    metrics = build_response_metrics(
        forensic_evidence=forensic,
        agent_investigation=investigation,
    )

    containment = build_containment_strategy(
        forensic_evidence=forensic,
        agent_investigation=investigation,
    )

    root_cause = build_root_cause_analysis(
        forensic_evidence=forensic,
        agent_investigation=investigation,
    )

    report = build_nist_incident_report(
        forensic_evidence=forensic,
        agent_investigation=investigation,
        response_metrics=metrics,
        containment_strategy=containment,
        root_cause_analysis=root_cause,
    )

    assert report["incident_summary"]["severity"] == "critical"
    assert "nist_lifecycle" in report
    assert "questions_answered" in report