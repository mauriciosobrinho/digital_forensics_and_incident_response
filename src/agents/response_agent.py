from datetime import datetime, timezone

from src.agents.state import InvestigationState


def response_advisor_agent(
    state: InvestigationState,
) -> InvestigationState:
    triage = state["triage_result"]
    forensic = state["forensic_analysis"]
    iocs = state["iocs"]
    dry_run = state.get(
        "dry_run",
        True,
    )

    ip_indicators = iocs.get(
        "ip_indicators",
        [],
    )

    critical_ips = [
        item["ip"]
        for item in ip_indicators
        if item.get("risk_level") == "critical"
    ]

    high_ips = [
        item["ip"]
        for item in ip_indicators
        if item.get("risk_level") == "high"
    ]

    response = {
        "agent": "response_advisor_agent",
        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "dry_run": dry_run,
        "human_approval_required": True,
        "human_approval_status": state.get(
            "human_approval_status",
            "pending",
        ),
        "recommended_containment": {
            "immediate": [
                {
                    "action": "block_or_challenge_critical_ips",
                    "targets": critical_ips,
                    "requires_human_approval": True,
                    "business_risk": "Possible false positives may impact legitimate users behind shared IPs.",
                    "priority": "P1",
                },
                {
                    "action": "dynamic_rate_limiting_invoice_search",
                    "targets": [
                        "/invoices/search"
                    ],
                    "requires_human_approval": False,
                    "business_risk": "Low to medium; may affect heavy legitimate usage.",
                    "priority": "P1",
                },
                {
                    "action": "increase_monitoring_for_high_risk_ips",
                    "targets": high_ips,
                    "requires_human_approval": False,
                    "business_risk": "Low.",
                    "priority": "P2",
                },
            ],
            "strategic": [
                {
                    "action": "fix_object_level_authorization",
                    "description": "Ensure invoice access checks validate ownership/authorization server-side.",
                    "requires_human_approval": True,
                    "priority": "P1",
                },
                {
                    "action": "rotate_or_revoke_suspicious_tokens",
                    "description": "Review tokens observed in suspicious access patterns.",
                    "requires_human_approval": True,
                    "priority": "P2",
                },
                {
                    "action": "update_waf_rules",
                    "description": "Add rules for sequential invoice enumeration patterns.",
                    "requires_human_approval": True,
                    "priority": "P2",
                },
            ],
        },
        "mini_playbook": [
            "Validate critical IPs against customer support and internal allowlists.",
            "Apply dry-run blocklist simulation.",
            "Enable rate limiting for invoice search endpoint.",
            "Escalate object-level authorization fix to application security owners.",
            "Review token exposure and revoke suspicious tokens if confirmed.",
            "Monitor anomaly score and risk score deltas after containment.",
        ],
        "executive_summary": (
            f"Incident classified as {triage['severity']} / {triage['priority']}. "
            f"Likely IDOR enumeration confirmed by forensic analysis. "
            f"Patient-zero candidate: {forensic.get('patient_zero_candidate')}."
        ),
    }

    decision = {
        "agent": "response_advisor_agent",
        "decision": "recommended_dry_run_containment",
        "dry_run": dry_run,
        "human_approval_required": True,
        "reason": "Blocking actions can affect users and require human approval.",
    }

    return {
        **state,
        "response_recommendation": response,
        "human_approval_required": True,
        "decision_log": [
            *state.get("decision_log", []),
            decision,
        ],
    }