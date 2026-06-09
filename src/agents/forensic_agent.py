from datetime import datetime, timezone

from src.agents.state import InvestigationState

from src.agents.workflow import append_workflow_event

def forensic_analyst_agent(
    state: InvestigationState,
) -> InvestigationState:
    
    # is_reentry = (
    #     state.get("workflow_stage") == "requesting_more_evidence"
    # )

    human_loop_count = state.get(
        "human_loop_count",
        0,
    )

    is_reentry = (
        state.get("workflow_stage")
        == "requesting_more_evidence"
        or human_loop_count > 0
    )

    analysis_type = (
        "additional_evidence_review"
        if is_reentry
        else "initial_forensic_review"
    )

    evidence = state["forensic_evidence"]
    timeline = state["attack_timeline"]
    iocs = state["iocs"]
    risk_summary = state["risk_summary"]
    anomaly_summary = state["anomaly_summary"]

    top_attackers = evidence.get(
        "top_attackers",
        [],
    )

    patient_zero = (
        top_attackers[0]["ip"]
        if top_attackers
        else None
    )

    timeline_summary = timeline.get(
        "summary",
        {},
    )

    first_seen = timeline_summary.get(
        "first_seen"
    )

    last_seen = timeline_summary.get(
        "last_seen"
    )

    enumeration_patterns = iocs.get(
        "enumeration_patterns",
        [],
    )

    top_pattern = (
        enumeration_patterns[0]
        if enumeration_patterns
        else {}
    )

    result = {
        "agent": "forensic_analyst_agent",
        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "patient_zero_candidate": patient_zero,
        "attack_window": {
            "first_seen": first_seen,
            "last_seen": last_seen,
        },
        "attack_pattern_explanation": (
            "The evidence shows high-volume invoice access, high invoice diversity "
            "and elevated sequential access ratio. This combination is consistent "
            "with automated enumeration of direct object identifiers."
        ),
        "automation_assessment": {
            "likely_automated": True,
            "rationale": (
                "Top IPs converge across risk scoring, bot likelihood and Isolation "
                "Forest anomaly detection."
            ),
            "total_anomalous_ips": anomaly_summary.get(
                "total_anomalous_ips"
            ),
        },
        "idor_evidence_assessment": {
            "clear_idor_evidence": True,
            "reason": (
                "Multiple IPs accessed thousands of unique invoice IDs with strong "
                "sequential patterns, suggesting enumeration of object references."
            ),
            "top_enumeration_pattern": top_pattern,
        },
        "estimated_impact": {
            "unique_invoices_accessed_by_top_attackers": timeline_summary.get(
                "unique_invoices_accessed"
            ),
            "unique_tokens_seen": timeline_summary.get(
                "unique_tokens_seen"
            ),
            "total_attack_events": timeline_summary.get(
                "total_attack_events"
            ),
        },
        "mitre_attack_mapping_high_level": [
            {
                "tactic": "Credential Access / Discovery",
                "technique": "Automated resource enumeration",
                "note": "Mapped at high level due to identifier enumeration behavior.",
            },
            {
                "tactic": "Collection",
                "technique": "Data from information repositories",
                "note": "Invoice data may represent sensitive business/user information.",
            },
            {
                "tactic": "Defense Evasion",
                "technique": "Use of distributed IPs or repeated low-rate access",
                "note": "Multiple suspicious IPs may indicate campaign distribution.",
            },
        ],
        "top_attackers_reviewed": risk_summary.get(
            "top_risk_ips",
            [],
        )[:10],

        # "analysis_iteration": (
        #     "additional_evidence_review"
        #     if is_reentry
        #     else "initial_forensic_review"
        # ),

        "analysis_iteration": analysis_type,

        "human_requested_more_evidence": is_reentry,
    }

    decision = {
        "agent": "forensic_analyst_agent",
        "decision": "confirmed_likely_idor_enumeration",
        "patient_zero_candidate": patient_zero,
        "reason": "Evidence converges across timeline, IOCs, risk and anomaly scores.",
        "analysis_iteration": analysis_type,
        "human_requested_more_evidence": is_reentry,
    }

    return {
        **state,
        "forensic_analysis": result,
        "workflow_stage": "forensic_analysis",
        "workflow_timeline": append_workflow_event(
            state,
            stage="forensic_analysis",
            decision="idor_pattern_analyzed",
            details={
                "patient_zero_candidate": patient_zero,
                "analysis_iteration": analysis_type,
                "human_requested_more_evidence": is_reentry,
            },
        ),
        "decision_log": [
            *state.get("decision_log", []),
            decision,
        ],
    }