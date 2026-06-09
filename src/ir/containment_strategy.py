from datetime import datetime, timezone
from typing import Any


def build_containment_strategy(
    *,
    agent_investigation: dict[str, Any],
    forensic_evidence: dict[str, Any],
) -> dict[str, Any]:

    response = agent_investigation.get(
        "response_recommendation",
        {},
    )

    recommended = response.get(
        "recommended_containment",
        {},
    )

    top_attackers = forensic_evidence.get(
        "top_attackers",
        [],
    )

    critical_targets = [
        item.get("ip")
        for item in top_attackers[:5]
        if item.get("ip")
    ]

    return {
        "strategy_type": "nist_containment_strategy",
        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "dry_run": agent_investigation.get(
            "dry_run",
            True,
        ),
        "immediate_containment": [
            {
                "action": "block_or_challenge_critical_ips",
                "targets": critical_targets,
                "order": 1,
                "requires_human_approval": True,
                "rationale": (
                    "Critical IPs show the highest convergence of risk score, "
                    "IDOR indicators and automation signals."
                ),
                "false_positive_risk": "medium",
                "business_impact": (
                    "Possible friction for legitimate clients behind shared IPs. "
                    "Human approval is required before production execution."
                ),
                "automation_policy": "human_approval_required",
            },
            {
                "action": "dynamic_rate_limiting_invoice_search",
                "targets": [
                    "/invoices/search",
                    "/invoice",
                ],
                "order": 2,
                "requires_human_approval": False,
                "rationale": (
                    "Rate limiting reduces enumeration velocity without fully "
                    "blocking access."
                ),
                "false_positive_risk": "low_to_medium",
                "business_impact": (
                    "May increase latency for high-volume legitimate clients."
                ),
                "automation_policy": "safe_for_dry_run_automation",
            },
            {
                "action": "increase_monitoring_for_high_risk_ips",
                "targets": critical_targets,
                "order": 3,
                "requires_human_approval": False,
                "rationale": (
                    "Enhanced monitoring improves investigation visibility while "
                    "avoiding disruptive action."
                ),
                "false_positive_risk": "low",
                "business_impact": "minimal",
                "automation_policy": "safe_to_automate",
            },
        ],
        "strategic_containment": [
            {
                "action": "fix_idor_object_level_authorization",
                "order": 1,
                "requires_human_approval": False,
                "rationale": (
                    "The root control failure is missing or insufficient "
                    "object-level authorization."
                ),
                "business_impact": (
                    "Requires engineering remediation and regression testing."
                ),
            },
            {
                "action": "rotate_or_revoke_suspicious_tokens",
                "order": 2,
                "requires_human_approval": True,
                "rationale": (
                    "Suspicious tokens were observed during attack activity."
                ),
                "business_impact": (
                    "May force re-authentication or interrupt legitimate sessions."
                ),
            },
            {
                "action": "update_waf_rules",
                "order": 3,
                "requires_human_approval": True,
                "rationale": (
                    "WAF rules can reduce repeated enumeration attempts."
                ),
                "business_impact": (
                    "Incorrect rules may block legitimate traffic patterns."
                ),
            },
        ],
        "source_recommendation": recommended,
    }