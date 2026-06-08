from src.agents.forensic_agent import (
    forensic_analyst_agent,
)

from src.agents.response_agent import (
    response_advisor_agent,
)

from src.agents.triage_agent import (
    triage_agent,
)

from src.agents.graph import (
    build_investigation_graph,
)


def sample_state():
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
            "summary": {
                "total_scored_ips": 10,
                "total_idor_findings": 1,
                "total_anomalous_ips": 1,
            },
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
                "total_idor_findings": 1,
                "total_anomalous_ips": 1,
            },
            "ip_indicators": [
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
            "enumeration_patterns": [
                {
                    "ip": "1.1.1.1",
                    "sequential_access_ratio": 0.9,
                    "unique_invoice_ids": 1000,
                    "idor_severity": "critical",
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
            "risk_level_distribution": [
                {
                    "risk_level": "critical",
                    "count": 1,
                }
            ],
        },
        "anomaly_summary": {
            "total_ips": 10,
            "total_anomalous_ips": 1,
            "top_anomalies": [
                {
                    "ip": "1.1.1.1",
                    "anomaly_score": 99.0,
                    "anomaly_level": "critical",
                }
            ],
        },
        "dry_run": True,
        "human_approval_status": "pending",
        "decision_log": [],
    }


def test_triage_agent():
    result = triage_agent(
        sample_state()
    )

    assert result["triage_result"]["severity"] == "critical"
    assert result["triage_result"]["priority"] == "P1"
    assert len(result["decision_log"]) == 1


def test_forensic_agent():
    state = triage_agent(
        sample_state()
    )

    result = forensic_analyst_agent(
        state
    )

    assert result["forensic_analysis"]["patient_zero_candidate"] == "1.1.1.1"
    assert result["forensic_analysis"]["idor_evidence_assessment"]["clear_idor_evidence"] is True


def test_response_agent():
    state = triage_agent(
        sample_state()
    )

    state = forensic_analyst_agent(
        state
    )

    result = response_advisor_agent(
        state
    )

    assert result["response_recommendation"]["dry_run"] is True
    assert result["human_approval_required"] is True
    assert len(result["decision_log"]) == 3


def test_langgraph_investigation_graph():
    graph = build_investigation_graph()

    result = graph.invoke(
        sample_state()
    )

    assert "triage_result" in result
    assert "forensic_analysis" in result
    assert "response_recommendation" in result
    assert len(result["decision_log"]) == 3