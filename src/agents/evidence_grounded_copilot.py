from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.agents.evidence_answer_templates import not_enough_structured_evidence
from src.agents.evidence_router import EvidenceIntent, classify_evidence_intent


ROOT_DIR = Path(__file__).resolve().parents[2]

EVIDENCE_DIR = ROOT_DIR / "data" / "evidence"
OBSERVABILITY_DIR = ROOT_DIR / "data" / "observability"

COPILOT_GROUNDED_ANSWERS_PATH = (
    EVIDENCE_DIR / "copilot_grounded_answers.json"
)


def _load_json(
    path: Path,
    default: Any,
) -> Any:
    if not path.exists():
        return default

    try:
        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    except json.JSONDecodeError:
        broken_path = path.with_suffix(
            path.suffix + ".broken"
        )

        try:
            path.replace(
                broken_path,
            )
        except OSError:
            pass

        return default


def load_structured_evidence(
    evidence_dir: Path = EVIDENCE_DIR,
    observability_dir: Path = OBSERVABILITY_DIR,
) -> dict[str, Any]:
    return {
        "forensic_evidence": _load_json(
            evidence_dir / "forensic_evidence.json",
            {},
        ),
        "agent_investigation": _load_json(
            evidence_dir / "agent_investigation.json",
            {},
        ),
        "nist_incident_report": _load_json(
            evidence_dir / "nist_incident_report.json",
            {},
        ),
        "response_metrics": _load_json(
            evidence_dir / "response_metrics.json",
            {},
        ),
        "soc_dashboard_data": _load_json(
            observability_dir / "soc_dashboard_data.json",
            {},
        ),
    }


def _questions(artifacts: dict[str, Any]) -> dict[str, Any]:
    return artifacts.get(
        "nist_incident_report",
        {},
    ).get(
        "questions_answered",
        {},
    )


def _topline(artifacts: dict[str, Any]) -> dict[str, Any]:
    return artifacts.get(
        "soc_dashboard_data",
        {},
    ).get(
        "topline",
        {},
    )


def _pipeline_metrics(artifacts: dict[str, Any]) -> dict[str, Any]:
    return artifacts.get(
        "soc_dashboard_data",
        {},
    ).get(
        "pipeline_metrics",
        {},
    ) or artifacts.get(
        "soc_dashboard_data",
        {},
    ).get(
        "metrics",
        {},
    )


def _build_answer(
    question: str,
    answer: str,
    evidence: list[str],
    source_artifacts: list[str],
    confidence: str,
    technical_payload: dict[str, Any],
) -> dict[str, Any]:
    return {
        "question": question,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "is_answered": True,
        "answer": answer,
        "evidence": evidence,
        "source_artifacts": source_artifacts,
        "confidence": confidence,
        "technical_payload": technical_payload,
        "fallback_to_rag": False,
    }


def _answer_patient_zero(
    question: str,
    artifacts: dict[str, Any],
) -> dict[str, Any]:
    questions = _questions(artifacts)
    patient_zero = questions.get("patient_zero_candidate")

    if not patient_zero:
        return not_enough_structured_evidence(question)

    return _build_answer(
        question=question,
        answer=f"Patient zero candidate: {patient_zero}",
        evidence=[
            "The NIST incident report contains a structured patient_zero_candidate field.",
            "The candidate is correlated with the consolidated forensic investigation output.",
            "The finding is part of the structured incident questions answered by the platform.",
        ],
        source_artifacts=[
            "data/evidence/nist_incident_report.json",
            "data/evidence/forensic_evidence.json",
            "data/evidence/agent_investigation.json",
        ],
        confidence="high",
        technical_payload={
            "patient_zero_candidate": patient_zero,
        },
    )


def _answer_attack_start(
    question: str,
    artifacts: dict[str, Any],
) -> dict[str, Any]:
    questions = _questions(artifacts)

    start = questions.get("when_did_it_start")
    end = questions.get("when_did_it_end")

    if not start:
        return not_enough_structured_evidence(question)

    return _build_answer(
        question=question,
        answer=f"The observed exploitation window starts at {start}.",
        evidence=[
            "The incident report contains a structured start timestamp.",
            "The same report also records the observed end of the attack window.",
            "The value is generated from the forensic timeline and incident response layer.",
        ],
        source_artifacts=[
            "data/evidence/nist_incident_report.json",
            "data/evidence/forensic_evidence.json",
        ],
        confidence="high",
        technical_payload={
            "attack_start": start,
            "attack_end": end,
        },
    )


def _answer_attack_end(
    question: str,
    artifacts: dict[str, Any],
) -> dict[str, Any]:
    questions = _questions(artifacts)

    start = questions.get("when_did_it_start")
    end = questions.get("when_did_it_end")

    if not end:
        return not_enough_structured_evidence(question)

    return _build_answer(
        question=question,
        answer=f"The observed exploitation window ended at {end}.",
        evidence=[
            "The incident report contains a structured end timestamp.",
            "The same report also records the observed start of the attack window.",
            "The value is generated from the forensic timeline and incident response layer.",
        ],
        source_artifacts=[
            "data/evidence/nist_incident_report.json",
            "data/evidence/forensic_evidence.json",
        ],
        confidence="high",
        technical_payload={
            "attack_start": start,
            "attack_end": end,
        },
    )


def _answer_automation(
    question: str,
    artifacts: dict[str, Any],
) -> dict[str, Any]:
    questions = _questions(artifacts)

    automated = questions.get("was_it_automated")
    attack_events = questions.get("how_many_attack_events")
    invoices = questions.get("how_many_invoices")

    if automated is None:
        return not_enough_structured_evidence(question)

    answer = (
        "Yes. The incident evidence indicates automated behavior."
        if automated
        else "No. The structured evidence does not classify the behavior as automated."
    )

    return _build_answer(
        question=question,
        answer=answer,
        evidence=[
            "The NIST incident report explicitly classifies automation status.",
            "The investigation correlates request volume with invoice enumeration.",
            "High event count and invoice diversity are consistent with automated enumeration.",
        ],
        source_artifacts=[
            "data/evidence/nist_incident_report.json",
            "data/evidence/agent_investigation.json",
        ],
        confidence="high" if automated else "medium",
        technical_payload={
            "was_it_automated": automated,
            "attack_events": attack_events,
            "invoices_involved": invoices,
        },
    )


def _answer_affected_invoices(
    question: str,
    artifacts: dict[str, Any],
) -> dict[str, Any]:
    questions = _questions(artifacts)

    invoices = questions.get("how_many_invoices")
    attack_events = questions.get("how_many_attack_events")

    if invoices is None:
        return not_enough_structured_evidence(question)

    return _build_answer(
        question=question,
        answer=f"The platform identified {invoices} invoices involved in the suspicious activity.",
        evidence=[
            "The incident report exposes how_many_invoices as a structured metric.",
            "The metric is generated from the forensic aggregation layer.",
            "Attack event volume is available for contextual impact assessment.",
        ],
        source_artifacts=[
            "data/evidence/nist_incident_report.json",
            "data/evidence/forensic_evidence.json",
        ],
        confidence="high",
        technical_payload={
            "invoices_involved": invoices,
            "attack_events": attack_events,
        },
    )


def _answer_containment(
    question: str,
    artifacts: dict[str, Any],
) -> dict[str, Any]:
    investigation = artifacts.get("agent_investigation", {})

    response = (
        investigation.get("response_recommendation")
        or investigation.get("response")
        or {}
    )

    recommended_actions = (
        response.get("recommended_actions")
        or response.get("actions")
        or response.get("containment_actions")
        or []
    )

    if not recommended_actions:
        recommended_actions = [
            "Apply dynamic rate limiting to suspicious invoice access patterns.",
            "Challenge or selectively block confirmed high-risk IPs after human approval.",
            "Review and rotate suspicious tokens associated with abnormal access patterns.",
            "Update WAF rules to reduce direct object enumeration attempts.",
            "Increase monitoring on impacted invoice endpoints.",
        ]

    return _build_answer(
        question=question,
        answer="Recommended containment is selective, staged and human-approved.",
        evidence=[
            "The response advisor layer generates containment recommendations.",
            "Human approval is required before disruptive actions.",
            "The platform keeps containment in dry-run mode for safety and auditability.",
        ],
        source_artifacts=[
            "data/evidence/agent_investigation.json",
            "data/evidence/nist_incident_report.json",
        ],
        confidence="high",
        technical_payload={
            "recommended_actions": recommended_actions,
            "requires_human_approval": True,
            "execution_mode": "dry_run",
        },
    )


def _answer_business_impact(
    question: str,
    artifacts: dict[str, Any],
) -> dict[str, Any]:
    questions = _questions(artifacts)
    topline = _topline(artifacts)

    invoices = questions.get("how_many_invoices")
    attack_events = questions.get("how_many_attack_events")
    severity = topline.get("severity")
    priority = topline.get("priority")

    if invoices is None and attack_events is None:
        return not_enough_structured_evidence(question)

    return _build_answer(
        question=question,
        answer=(
            "The business impact is material because the activity involved "
            "large-scale invoice enumeration and was classified as high-priority incident evidence."
        ),
        evidence=[
            "The incident report quantifies affected invoices and attack events.",
            "SOC dashboard data provides severity and operational priority.",
            "Invoice enumeration can expose sensitive business and user-related information.",
        ],
        source_artifacts=[
            "data/evidence/nist_incident_report.json",
            "data/observability/soc_dashboard_data.json",
        ],
        confidence="high",
        technical_payload={
            "severity": severity,
            "priority": priority,
            "invoices_involved": invoices,
            "attack_events": attack_events,
        },
    )


def _answer_response_metrics(
    question: str,
    artifacts: dict[str, Any],
) -> dict[str, Any]:
    metrics = artifacts.get("response_metrics", {})

    ttd = metrics.get("time_to_detect", {})
    ttr = metrics.get("time_to_respond", {})
    ttc = metrics.get("time_to_contain", {})

    if not any([ttd, ttr, ttc]):
        return _build_answer(
            question=question,
            answer=(
                "TTD is retrospective for this historical dataset, while TTR and TTC are measured "
                "inside the automated dry-run response cycle."
            ),
            evidence=[
                "The NIST response layer defines TTD, TTR and TTC semantics.",
                "The project runs containment in dry-run mode.",
            ],
            source_artifacts=[
                "data/evidence/nist_incident_report.json",
                "data/evidence/response_metrics.json",
            ],
            confidence="medium",
            technical_payload={
                "TTD": "retrospective",
                "TTR": "dry_run_cycle",
                "TTC": "dry_run_cycle",
            },
        )

    return _build_answer(
        question=question,
        answer="The platform generated TTD, TTR and TTC metrics for the incident response workflow.",
        evidence=[
            "The response_metrics artifact contains structured incident response timing.",
            "TTD is retrospective because the dataset is historical.",
            "TTR and TTC are measured in the automated dry-run execution cycle.",
        ],
        source_artifacts=[
            "data/evidence/response_metrics.json",
        ],
        confidence="high",
        technical_payload={
            "TTD": ttd,
            "TTR": ttr,
            "TTC": ttc,
        },
    )


def _answer_idor_evidence(
    question: str,
    artifacts: dict[str, Any],
) -> dict[str, Any]:
    questions = _questions(artifacts)

    invoices = questions.get("how_many_invoices")
    attack_events = questions.get("how_many_attack_events")
    automated = questions.get("was_it_automated")

    if invoices is None and attack_events is None:
        return not_enough_structured_evidence(question)

    return _build_answer(
        question=question,
        answer="The structured evidence supports potential IDOR exploitation through invoice enumeration.",
        evidence=[
            "Large invoice diversity was observed in the suspicious activity.",
            "The incident report confirms invoice enumeration indicators.",
            "The behavior was classified as automated or automation-compatible.",
            "The NIST report names the incident as potential IDOR exploitation via invoice enumeration.",
        ],
        source_artifacts=[
            "data/evidence/nist_incident_report.json",
            "data/evidence/forensic_evidence.json",
            "data/evidence/agent_investigation.json",
        ],
        confidence="high",
        technical_payload={
            "invoices_involved": invoices,
            "attack_events": attack_events,
            "was_it_automated": automated,
        },
    )


def _answer_mitre(
    question: str,
    artifacts: dict[str, Any],
) -> dict[str, Any]:
    questions = _questions(artifacts)
    mitre = questions.get("mitre_mapping")

    if not mitre:
        return not_enough_structured_evidence(question)

    evidence = []
    for item in mitre:
        tactic = item.get("tactic")
        technique = item.get("technique")
        rationale = item.get("rationale")
        evidence.append(f"{tactic} / {technique}: {rationale}")

    return _build_answer(
        question=question,
        answer="The incident was mapped to high-level MITRE ATT&CK tactics and techniques.",
        evidence=evidence,
        source_artifacts=[
            "data/evidence/nist_incident_report.json",
        ],
        confidence="high",
        technical_payload={
            "mitre_mapping": mitre,
        },
    )


def _answer_human_escalation(
    question: str,
    artifacts: dict[str, Any],
) -> dict[str, Any]:
    topline = _topline(artifacts)

    return _build_answer(
        question=question,
        answer=(
            "Actions that may disrupt users or production traffic should be escalated for human approval."
        ),
        evidence=[
            "The platform implements human-in-the-loop governance.",
            "Supported scenarios include approve, reject, modify and request_more_evidence.",
            "Containment remains dry-run until reviewed.",
        ],
        source_artifacts=[
            "data/evidence/agent_investigation.json",
            "data/observability/soc_dashboard_data.json",
        ],
        confidence="high",
        technical_payload={
            "dry_run": topline.get("dry_run", True),
            "human_approval_required": True,
            "approval_scenarios": [
                "approve",
                "reject",
                "modify",
                "request_more_evidence",
            ],
        },
    )


def build_grounded_answer(
    question: str,
    artifacts: dict[str, Any] | None = None,
) -> dict[str, Any]:
    artifacts = artifacts or load_structured_evidence()
    routed = classify_evidence_intent(question)

    handlers = {
        EvidenceIntent.PATIENT_ZERO: _answer_patient_zero,
        EvidenceIntent.ATTACK_END: _answer_attack_end,
        EvidenceIntent.ATTACK_START: _answer_attack_start,
        EvidenceIntent.AUTOMATION: _answer_automation,
        EvidenceIntent.AFFECTED_INVOICES: _answer_affected_invoices,
        EvidenceIntent.CONTAINMENT: _answer_containment,
        EvidenceIntent.BUSINESS_IMPACT: _answer_business_impact,
        EvidenceIntent.RESPONSE_METRICS: _answer_response_metrics,
        EvidenceIntent.IDOR_EVIDENCE: _answer_idor_evidence,
        EvidenceIntent.MITRE_MAPPING: _answer_mitre,
        EvidenceIntent.HUMAN_ESCALATION: _answer_human_escalation,
    }

    handler = handlers.get(routed.intent)

    if not handler:
        answer = not_enough_structured_evidence(question)
    else:
        answer = handler(question, artifacts)

    answer["intent"] = routed.intent.value
    answer["intent_confidence"] = routed.confidence
    answer["intent_rationale"] = routed.rationale

    return answer


def persist_grounded_answer(
    answer: dict[str, Any],
    output_path: Path = COPILOT_GROUNDED_ANSWERS_PATH,
) -> None:
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    existing = _load_json(
        output_path,
        [],
    )

    if not isinstance(existing, list):
        existing = [existing]

    existing.append(answer)
    
    # Keep only the N most recent records
    # avoiding indefinite file growth.
    MAX_HISTORY = 1000

    existing = existing[-MAX_HISTORY:]

    temp_path = output_path.with_suffix(
        output_path.suffix + ".tmp"
    )

    with temp_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            existing,
            file,
            indent=2,
            ensure_ascii=False,
        )

    temp_path.replace(
        output_path
    )


def answer_from_structured_evidence(question: str) -> dict[str, Any]:
    answer = build_grounded_answer(question)
    persist_grounded_answer(answer)
    return answer