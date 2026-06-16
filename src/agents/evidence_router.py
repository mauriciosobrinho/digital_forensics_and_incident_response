from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class EvidenceIntent(StrEnum):
    PATIENT_ZERO = "patient_zero"
    ATTACK_START = "attack_start"
    ATTACK_END = "attack_end"
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
            EvidenceIntent.CONTAINMENT,
            [
                "containment",
                "containment action",
                "containment actions",
                "recommended containment",
                "what containment actions are recommended",
                "response action",
                "response actions",
                "mitigation",
                "mitigations",
                "block",
                "blocking",
                "rate limiting",
                "rate-limit",
                "waf",
                "token rotation",
                "recommended actions",
                "ações de contenção",
                "acoes de contencao",
                "ação de contenção",
                "acao de contencao",
                "contenção",
                "contencao",
                "quais ações de contenção são recomendadas",
                "quais acoes de contencao sao recomendadas",
                "mitigação",
                "mitigacao",
                "bloqueio",
                "limitação de taxa",
                "limitacao de taxa",
                "ações recomendadas",
                "acoes recomendadas",
                "acciones de contención",
                "acciones de contencion",
                "acción de contención",
                "accion de contencion",
                "qué acciones de contención se recomiendan",
                "que acciones de contencion se recomiendan",
                "mitigación",
                "mitigacion",
                "bloqueo",
                "limitación de tasa",
                "limitacion de tasa",
                "acciones recomendadas",
            ],
            "The question asks about recommended containment or mitigation actions.",
        ),
        (
            EvidenceIntent.ATTACK_END,
            [
                "when did the attack end",
                "when did it end",
                "attack end",
                "attack ended",
                "end of the attack",
                "last seen",
                "quando terminou",
                "fim do ataque",
                "terminou",
                "ended",
                "quando o ataque terminou",
                "término do ataque",
                "termino do ataque",
                "cuándo terminó el ataque",
                "cuando termino el ataque",
                "fin del ataque",
                "terminación del ataque",
                "terminacion del ataque",
            ],
            "The question asks about the end of the exploitation window.",
        ),
        (
            EvidenceIntent.PATIENT_ZERO,
            [
                "patient zero",
                "paciente zero",
                "paciente cero",
                "first attacker",
                "initial attacker",
                "primeiro atacante",
                "primer atacante",
            ],
            "The question asks who initiated or first appeared in the suspicious activity.",
        ),
        (
            EvidenceIntent.ATTACK_START,
            [
                "when did the attack start",
                "when did it start",
                "attack start",
                "started",
                "began",
                "begin",
                "first seen",
                "quando começou",
                "quando comecou",
                "inicio",
                "início",
                "start of the attack",
                "quando o ataque começou",
                "quando o ataque comecou",
                "início do ataque",
                "inicio do ataque",
                "cuándo comenzó el ataque",
                "cuando comenzo el ataque",
                "inicio del ataque",
                "comienzo del ataque",
            ],
            "The question asks about the beginning of the exploitation window.",
        ),
        (
            EvidenceIntent.AUTOMATION,
            [
                "automated",
                "automation",
                "bot",
                "automatizado",
                "automatizada",
                "automação",
                "automacao",
                "automatización",
                "automatizacion",
            ],
            "The question asks whether the behavior was automated.",
        ),
        (
            EvidenceIntent.AFFECTED_INVOICES,
            [
                "how many invoices",
                "affected invoices",
                "invoices affected",
                "invoices were affected",
                "quantas faturas",
                "quantas invoices",
                "facturas afectadas",
                "cuántas facturas",
                "cuantas facturas",
            ],
            "The question asks about affected invoice volume.",
        ),
        (
            EvidenceIntent.BUSINESS_IMPACT,
            [
                "impact",
                "business",
                "risk",
                "regulatory",
                "impacto",
                "negócio",
                "negocio",
                "riesgo",
                "regulatorio",
            ],
            "The question asks about business or operational impact.",
        ),
        (
            EvidenceIntent.RESPONSE_METRICS,
            [
                "ttd",
                "ttr",
                "ttc",
                "time to detect",
                "time to respond",
                "time to contain",
            ],
            "The question asks about incident response metrics.",
        ),
        (
            EvidenceIntent.IDOR_EVIDENCE,
            [
                "idor",
                "evidence",
                "proves",
                "sustenta",
                "evidência",
                "evidencia",
                "evidências",
                "evidencias",
            ],
            "The question asks what evidence supports IDOR exploitation.",
        ),
        (
            EvidenceIntent.MITRE_MAPPING,
            [
                "mitre",
                "att&ck",
                "ttp",
                "technique",
                "tactic",
                "técnica",
                "tecnica",
                "táctica",
                "tactica",
            ],
            "The question asks about MITRE ATT&CK mapping.",
        ),
        (
            EvidenceIntent.HUMAN_ESCALATION,
            [
                "human",
                "approval",
                "escalate",
                "reviewer",
                "aprovação",
                "aprovacao",
                "humana",
                "aprobación",
                "aprobacion",
                "escalamiento",
            ],
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