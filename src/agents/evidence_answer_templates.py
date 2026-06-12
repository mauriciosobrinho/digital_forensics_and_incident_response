from __future__ import annotations

from typing import Any


def format_grounded_answer(answer: dict[str, Any]) -> str:
    if not answer.get("is_answered"):
        return ""

    lines: list[str] = []

    lines.append(answer["answer"])
    lines.append("")

    evidence = answer.get("evidence", [])
    if evidence:
        lines.append("Evidence:")
        for item in evidence:
            lines.append(f"- {item}")
        lines.append("")

    sources = answer.get("source_artifacts", [])
    if sources:
        lines.append("Source artifacts:")
        for source in sources:
            lines.append(f"- `{source}`")
        lines.append("")

    confidence = answer.get("confidence")
    if confidence:
        lines.append(f"Confidence: {confidence}")

    technical_payload = answer.get("technical_payload", {})
    if technical_payload:
        lines.append("")
        lines.append("Technical payload:")
        for key, value in technical_payload.items():
            lines.append(f"- {key}: {value}")

    return "\n".join(lines)


def not_enough_structured_evidence(question: str) -> dict[str, Any]:
    return {
        "question": question,
        "is_answered": False,
        "answer": "No structured evidence answer was generated for this question.",
        "evidence": [],
        "source_artifacts": [],
        "confidence": "low",
        "technical_payload": {},
        "fallback_to_rag": True,
    }