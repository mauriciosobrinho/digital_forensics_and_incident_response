from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class EvidenceIntent(StrEnum):
    PATIENT_ZERO = "patient_zero"
    ATTACK_START = "attack_start"
    AUTOMATION = "automation"
    AFFECTED_INVOICES = "affected_invoices"
    CONTAINMENT = "containment"
    BUSINESS_IMPACT = "business_impact"
    RESPONSE_METRICS = "response_metrics"
    IDOR_EVIDENCE = "idor_evidence"
    MITRE_MAPPING = "mitre_mapping"
    HUMAN_ESCALATION = "human_escalation"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class RoutedQuestion:
    question: str
    intent: EvidenceIntent
    confidence: float
    rationale: str


def classify_evidence_intent(question: str) -> RoutedQuestion:
    normalized = question.lower().strip()

    rules: list[tuple[EvidenceIntent, list[str], str]] = [
        (
            EvidenceIntent.PATIENT_ZERO,
            ["patient zero", "first attacker", "initial attacker", "primeiro atacante"],
            "The question asks who initiated or first appeared in the suspicious activity.",
        ),
        (
            EvidenceIntent.ATTACK_START,
            ["when did", "start", "began", "begin", "quando começou", "inicio", "início"],
            "The question asks about the beginning of the exploitation window.",
        ),
        (
            EvidenceIntent.AUTOMATION,
            ["automated", "automation", "bot", "automatizado", "automação"],
            "The question asks whether the behavior was automated.",
        ),
        (
            EvidenceIntent.AFFECTED_INVOICES,
            ["how many invoices", "affected invoices", "invoices affected", "quantas invoices"],
            "The question asks about affected invoice volume.",
        ),
        (
            EvidenceIntent.CONTAINMENT,
            ["containment", "mitigation", "block", "waf", "rate limit", "contenção", "mitigar"],
            "The question asks about containment or mitigation actions.",
        ),
        (
            EvidenceIntent.BUSINESS_IMPACT,
            ["impact", "business", "risk", "regulatory", "impacto", "negócio"],
            "The question asks about business or operational impact.",
        ),
        (
            EvidenceIntent.RESPONSE_METRICS,
            ["ttd", "ttr", "ttc", "time to detect", "time to respond", "time to contain"],
            "The question asks about incident response metrics.",
        ),
        (
            EvidenceIntent.IDOR_EVIDENCE,
            ["idor", "evidence", "proves", "sustenta", "evidência", "evidencia"],
            "The question asks what evidence supports IDOR exploitation.",
        ),
        (
            EvidenceIntent.MITRE_MAPPING,
            ["mitre", "att&ck", "ttp", "technique", "tactic"],
            "The question asks about MITRE ATT&CK mapping.",
        ),
        (
            EvidenceIntent.HUMAN_ESCALATION,
            ["human", "approval", "escalate", "reviewer", "aprovação", "humana"],
            "The question asks what requires human approval or escalation.",
        ),
    ]

    for intent, keywords, rationale in rules:
        if any(keyword in normalized for keyword in keywords):
            return RoutedQuestion(
                question=question,
                intent=intent,
                confidence=0.95,
                rationale=rationale,
            )

    return RoutedQuestion(
        question=question,
        intent=EvidenceIntent.UNKNOWN,
        confidence=0.0,
        rationale="No structured evidence intent matched the question.",
    )