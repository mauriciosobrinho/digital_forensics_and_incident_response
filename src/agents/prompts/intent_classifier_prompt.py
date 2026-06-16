VALID_INTENTS = [
    "patient_zero",
    "attack_start",
    "automation",
    "affected_invoices",
    "containment",
    "business_impact",
    "response_metrics",
    "idor_evidence",
    "mitre_mapping",
    "human_escalation",
    "timeline",
    "root_cause",
    "unknown",
]


def build_intent_classifier_prompt(question: str) -> str:
    return (
        "Classify the user question for a DFIR/SOC IDOR investigation.\n\n"
        f"Valid intents: {VALID_INTENTS}\n\n"
        "Return only valid JSON with keys:\n"
        "- intent\n"
        "- confidence\n"
        "- rationale\n\n"
        f"Question: {question}"
    )