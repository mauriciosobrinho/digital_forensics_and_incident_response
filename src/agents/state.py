from typing import Any, TypedDict


class InvestigationState(TypedDict, total=False):
    forensic_evidence: dict[str, Any]
    attack_timeline: dict[str, Any]
    iocs: dict[str, Any]
    risk_summary: dict[str, Any]
    anomaly_summary: dict[str, Any]

    triage_result: dict[str, Any]
    forensic_analysis: dict[str, Any]
    response_recommendation: dict[str, Any]

    decision_log: list[dict[str, Any]]
    dry_run: bool
    human_approval_required: bool
    human_approval_status: str