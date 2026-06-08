from src.agents.human_approval_agent import (
    human_approval_agent,
)


def test_human_approval_agent_simulated():
    state = {
        "dry_run": True,
        "human_approval_mode": "simulated",
        "human_approval_status": "pending",
        "response_recommendation": {
            "recommended_containment": {
                "immediate": [
                    {
                        "action": "block_or_challenge_critical_ips",
                        "targets": [
                            "1.1.1.1",
                        ],
                        "requires_human_approval": True,
                        "priority": "P1",
                    },
                    {
                        "action": "dynamic_rate_limiting_invoice_search",
                        "targets": [
                            "/invoices/search",
                        ],
                        "requires_human_approval": False,
                        "priority": "P1",
                    },
                ]
            }
        },
        "decision_log": [],
    }

    result = human_approval_agent(
        state
    )

    assert result["human_approval_request"]["approval_required"] is True
    assert result["human_approval_response"]["decision"] == "approved_for_dry_run_only"
    assert result["human_approval_status"] == "approved_for_dry_run_only"
    assert len(result["approved_actions"]) >= 1