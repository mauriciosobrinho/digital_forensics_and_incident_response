from __future__ import annotations

from typing import Any

from src.agents.evidence_router import classify_evidence_intent
from src.agents.llm_client import build_llm_client
from src.agents.prompts.intent_classifier_prompt import (
    build_intent_classifier_prompt,
)


def classify_question_with_llm(
    question: str,
) -> dict[str, Any]:
    fallback = classify_evidence_intent(question)
    llm_client = build_llm_client()

    if not llm_client.is_enabled():
        return {
            "intent": fallback.intent.value,
            "confidence": fallback.confidence,
            "rationale": fallback.rationale,
            "classifier": "rules",
        }

    result = llm_client.generate_json(
        prompt=build_intent_classifier_prompt(question),
        agent_name="llm_intent_classifier",
        context={"question": question},
    )

    if not result:
        return {
            "intent": fallback.intent.value,
            "confidence": fallback.confidence,
            "rationale": fallback.rationale,
            "classifier": "rules_fallback",
        }

    return {
        "intent": result.get("intent", fallback.intent.value),
        "confidence": float(result.get("confidence", fallback.confidence)),
        "rationale": result.get("rationale", fallback.rationale),
        "classifier": "llm",
    }