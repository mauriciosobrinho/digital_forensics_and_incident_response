from datetime import datetime, timezone

from src.agents.state import InvestigationState

from src.agents.llm_client import build_llm_client
from src.agents.prompt_loader import load_prompt
from src.config.llm_settings import load_agent_runtime_settings


def triage_agent(
    state: InvestigationState,
) -> InvestigationState:
    risk_summary = state["risk_summary"]
    anomaly_summary = state["anomaly_summary"]
    iocs = state["iocs"]

    top_risk = risk_summary.get(
        "top_risk_ips",
        [],
    )

    top_score = (
        top_risk[0]["risk_score"]
        if top_risk
        else 0.0
    )

    total_suspicious_ips = (
        iocs
        .get("summary", {})
        .get("total_suspicious_ips", 0)
    )

    total_anomalous_ips = anomaly_summary.get(
        "total_anomalous_ips",
        0,
    )

    if top_score >= 80:
        severity = "critical"
        priority = "P1"
    elif top_score >= 60:
        severity = "high"
        priority = "P2"
    elif top_score >= 40:
        severity = "medium"
        priority = "P3"
    else:
        severity = "low"
        priority = "P4"

    result = {
        "agent": "triage_agent",
        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "incident_classification": "Potential IDOR exploitation via invoice enumeration",
        "severity": severity,
        "priority": priority,
        "top_risk_score": top_score,
        "total_suspicious_ips": total_suspicious_ips,
        "total_anomalous_ips": total_anomalous_ips,
        "initial_hypotheses": [
            "Automated invoice enumeration against invoice search endpoint.",
            "Possible IDOR exploitation due to high invoice diversity per IP.",
            "Likely bot-driven activity due to convergence of heuristic and anomaly signals.",
        ],
        "investigation_plan": [
            "Review top risk IPs and their invoice enumeration pattern.",
            "Validate whether accessed invoices belong to different users.",
            "Review auth token reuse and suspicious user-agent patterns.",
            "Correlate risk scoring with Isolation Forest anomaly results.",
            "Prioritize containment for critical IPs with confirmed high-risk behavior.",
        ],
    }

    decision = {
        "agent": "triage_agent",
        "decision": "classified_incident",
        "severity": severity,
        "priority": priority,
        "reason": "Severity derived from top risk score, IOC count and anomaly convergence.",
    }

    
    settings = load_agent_runtime_settings()
    llm_client = build_llm_client(settings)
    prompt = load_prompt("triage_prompt.md")

    reasoning = llm_client.generate_json(
        agent_name="triage_agent",
        prompt=prompt,
        context={
            "risk_summary": risk_summary,
            "anomaly_summary": anomaly_summary,
            "iocs_summary": iocs.get("summary", {}),
            "triage_result": result,
        },
    )

    return {
        **state,
        "triage_result": result,

        "decision_log": [
            *state.get("decision_log", []),
            decision,
        ],

        "llm_agent_reasoning": [
            *state.get("llm_agent_reasoning", []),
            reasoning,
        ],
    }