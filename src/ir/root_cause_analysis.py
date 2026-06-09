from datetime import datetime, timezone
from typing import Any


def build_root_cause_analysis(
    *,
    forensic_evidence: dict[str, Any],
    agent_investigation: dict[str, Any],
) -> dict[str, Any]:

    forensic = agent_investigation.get(
        "forensic_analysis",
        {},
    )

    return {
        "analysis_type": "root_cause_analysis",
        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "root_cause": {
            "primary": (
                "Broken object-level authorization enabling direct access to "
                "invoice-like objects through predictable identifiers."
            ),
            "category": "Broken Access Control / IDOR",
            "confidence": "high",
        },
        "supporting_evidence": {
            "patient_zero_candidate": forensic.get(
                "patient_zero_candidate"
            ),
            "attack_window": forensic.get(
                "attack_window"
            ),
            "automation_assessment": forensic.get(
                "automation_assessment"
            ),
            "idor_evidence_assessment": forensic.get(
                "idor_evidence_assessment"
            ),
            "mitre_attack_mapping": forensic.get(
                "mitre_attack_mapping"
            ),
        },
        "failed_controls": [
            {
                "control": "object_level_authorization",
                "assessment": (
                    "Application endpoints appear to allow enumeration of "
                    "invoice identifiers without sufficient ownership validation."
                ),
            },
            {
                "control": "anti_enumeration_rate_limiting",
                "assessment": (
                    "Observed request volume and invoice diversity indicate that "
                    "enumeration was not sufficiently throttled."
                ),
            },
            {
                "control": "token_abuse_monitoring",
                "assessment": (
                    "Suspicious token patterns require validation and potential "
                    "rotation."
                ),
            },
        ],
        "eradication_plan": [
            {
                "step": 1,
                "action": "enforce_server_side_object_ownership_checks",
                "expected_result": (
                    "Only authorized users can access their own invoice objects."
                ),
            },
            {
                "step": 2,
                "action": "replace_predictable_object_access_patterns",
                "expected_result": (
                    "Reduce feasibility of direct object enumeration."
                ),
            },
            {
                "step": 3,
                "action": "implement_enumeration_detection_controls",
                "expected_result": (
                    "Detect and slow down repeated invoice probing behavior."
                ),
            },
            {
                "step": 4,
                "action": "rotate_or_revoke_suspicious_tokens",
                "expected_result": (
                    "Reduce risk from potentially abused credentials or tokens."
                ),
            },
        ],
    }