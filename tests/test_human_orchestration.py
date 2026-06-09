from src.agents.graph import (
    build_investigation_graph,
)


def sample_state(
    scenario: str,
):
    return {
        "forensic_evidence": {
            "top_attackers": [
                {
                    "ip": "1.1.1.1",
                    "risk_score": 90.0,
                    "risk_level": "critical",
                    "is_idor_suspect": True,
                    "is_likely_bot": True,
                    "sequential_access_ratio": 0.9,
                    "unique_invoice_ids": 1000,
                    "total_requests": 2000,
                }
            ],
        },
        "attack_timeline": {
            "summary": {
                "first_seen": "2020-12-01T00:00:00",
                "last_seen": "2020-12-01T01:00:00",
                "unique_invoices_accessed": 1000,
                "unique_tokens_seen": 2,
                "total_attack_events": 2000,
            }
        },
        "iocs": {
            "summary": {
                "total_suspicious_ips": 1,
            },
            "ip_indicators": [
                {
                    "ip": "1.1.1.1",
                    "risk_level": "critical",
                }
            ],
            "enumeration_patterns": [
                {
                    "ip": "1.1.1.1",
                    "sequential_access_ratio": 0.9,
                }
            ],
        },
        "risk_summary": {
            "total_ips": 10,
            "top_risk_ips": [
                {
                    "ip": "1.1.1.1",
                    "risk_score": 90.0,
                    "risk_level": "critical",
                    "is_idor_suspect": True,
                    "is_likely_bot": True,
                    "sequential_access_ratio": 0.9,
                    "unique_invoice_ids": 1000,
                    "total_requests": 2000,
                }
            ],
            "risk_level_distribution": [],
        },
        "anomaly_summary": {
            "total_ips": 10,
            "total_anomalous_ips": 1,
            "top_anomalies": [],
        },
        "dry_run": True,
        "human_approval_mode": "simulated",
        "human_approval_status": "pending",
        "human_decision_scenario": scenario,
        "decision_log": [],
        "workflow_timeline": [],
        "workflow_stage": "initialized",
        "human_loop_count": 0,
        "llm_agent_reasoning": [],
    }


def test_human_approval_approve_scenario():
    graph = build_investigation_graph()

    result = graph.invoke(
        sample_state("approve")
    )

    assert result["workflow_stage"] == "approved"
    assert len(result["approved_actions"]) > 0
    assert result["human_approval_status"] == "approved_for_dry_run_only"


def test_human_approval_reject_scenario():
    graph = build_investigation_graph()

    result = graph.invoke(
        sample_state("reject")
    )

    assert result["workflow_stage"] == "rejected"
    assert len(result["rejected_actions"]) > 0
    assert result["human_approval_status"] == "rejected"


def test_human_approval_modify_scenario():
    graph = build_investigation_graph()

    result = graph.invoke(
        sample_state("modify")
    )

    assert result["workflow_stage"] == "approved_with_modifications"
    assert result["modified_action_plan"]["strategy"] == "rate_limit_first_block_later"


def test_human_approval_request_more_evidence_reentry():
    graph = build_investigation_graph()

    result = graph.invoke(
        sample_state("request_more_evidence")
    )

    forensic_events = [
        event
        for event in result["workflow_timeline"]
        if event["stage"] == "forensic_analysis"
    ]

    assert len(forensic_events) >= 2
    assert result["human_loop_count"] == 1
    assert result["workflow_stage"] == "approved"