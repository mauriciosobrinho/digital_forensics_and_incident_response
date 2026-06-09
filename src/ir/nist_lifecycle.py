from datetime import datetime, timezone
from typing import Any


def build_nist_incident_report(
    *,
    forensic_evidence: dict[str, Any],
    agent_investigation: dict[str, Any],
    response_metrics: dict[str, Any],
    containment_strategy: dict[str, Any],
    root_cause_analysis: dict[str, Any],
) -> dict[str, Any]:

    forensic = agent_investigation.get(
        "forensic_analysis",
        {},
    )

    triage = agent_investigation.get(
        "triage",
        {},
    )

    response = agent_investigation.get(
        "response_recommendation",
        {},
    )

    estimated_impact = forensic.get(
        "estimated_impact",
        {},
    )

    return {
        "report_type": "nist_incident_response_report",
        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "incident_summary": {
            "incident_type": "Insecure Direct Object Reference",
            "classification": triage.get(
                "incident_classification"
            ),
            "severity": triage.get(
                "severity"
            ),
            "priority": triage.get(
                "priority"
            ),
            "dry_run": agent_investigation.get(
                "dry_run",
                True,
            ),
        },
        "questions_answered": {
            "when_did_it_start": forensic.get(
                "attack_window",
                {},
            ).get("first_seen"),
            "when_did_it_end": forensic.get(
                "attack_window",
                {},
            ).get("last_seen"),
            "how_many_invoices": estimated_impact.get(
                "unique_invoices_accessed_by_top_attackers"
            ),
            "how_many_attack_events": estimated_impact.get(
                "total_attack_events"
            ),
            "how_many_tokens": estimated_impact.get(
                "unique_tokens_seen"
            ),
            "was_it_automated": forensic.get(
                "automation_assessment",
                {},
            ).get("is_likely_automated"),
            "patient_zero_candidate": forensic.get(
                "patient_zero_candidate"
            ),
            "mitre_mapping": forensic.get(
                "mitre_attack_mapping",
                [],
            ),
        },
        "nist_lifecycle": {
            "analysis": {
                "status": "completed",
                "evidence": [
                    "forensic_evidence.json",
                    "attack_timeline.json",
                    "iocs.json",
                    "risk_scores.parquet",
                    "anomaly_scores.parquet",
                ],
                "summary": (
                    "The platform classified the event as likely IDOR exploitation "
                    "through invoice enumeration and generated forensic evidence."
                ),
            },
            "containment": {
                "status": "proposed_dry_run",
                "strategy_file": "containment_strategy.json",
                "summary": (
                    "Immediate and strategic containment actions were generated. "
                    "Disruptive actions require human approval."
                ),
            },
            "eradication": {
                "status": "recommended",
                "root_cause_file": "root_cause_analysis.json",
                "summary": (
                    "Primary remediation requires fixing object-level authorization "
                    "and reducing enumeration feasibility."
                ),
            },
            "recovery": {
                "status": "future_operational_phase",
                "summary": (
                    "Recovery would include monitoring after remediation, token "
                    "rotation validation and false-positive review."
                ),
            },
            "lessons_learned": {
                "status": "documented",
                "summary": (
                    "The incident highlights the need for authorization hardening, "
                    "enumeration detection, token monitoring and SOC automation."
                ),
            },
        },
        "response_metrics": response_metrics,
        "containment_strategy": containment_strategy,
        "root_cause_analysis": root_cause_analysis,
        "response_playbook_reference": response.get(
            "mini_playbook",
            [],
        ),
    }