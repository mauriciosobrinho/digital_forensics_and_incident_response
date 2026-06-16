from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


OBSERVABILITY_DIR = Path("data/observability")
LLM_METRICS_PATH = OBSERVABILITY_DIR / "llm_metrics.json"


def _safe_ratio(
    numerator: int | float,
    denominator: int | float,
) -> float:
    if denominator == 0:
        return 0.0

    return round(
        numerator / denominator,
        4,
    )


def build_llm_metrics(
    batch_results: list[dict[str, Any]],
    semantic_results: list[dict[str, Any]],
) -> dict[str, Any]:
    total_questions = len(batch_results)

    llm_calls = sum(
        1
        for item in batch_results
        if item.get("response", {}).get("used_llm") is True
    )

    deterministic_calls = total_questions - llm_calls

    fallback_calls = sum(
        1
        for item in batch_results
        if "fallback" in str(item.get("response", {}).get("mode", "")).lower()
    )

    vector_hits = 0
    total_context_chunks = 0

    for item in batch_results:
        vector_context = (
            item.get("response", {})
            .get("vector_context", {})
        )

        retrieved_documents = vector_context.get(
            "retrieved_documents",
            [],
        )

        if retrieved_documents:
            vector_hits += 1
            total_context_chunks += len(retrieved_documents)

    semantic_total = len(semantic_results)

    semantic_correct = sum(
        1
        for item in semantic_results
        if item.get("answer_is_correct") is True
    )

    intent_correct = sum(
        1
        for item in semantic_results
        if item.get("intent_pass") is True
    )

    professional_answer_hits = 0

    required_markers = [
        "executive answer",
        "supporting evidence",
        "reasoning",
        "operational implication",
        "confidence",
    ]

    for item in batch_results:
        answer = (
            item.get("response", {})
            .get("answer", "")
            .lower()
        )

        if any(marker in answer for marker in required_markers):
            professional_answer_hits += 1

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "total_questions": total_questions,
        "llm_calls": llm_calls,
        "deterministic_calls": deterministic_calls,
        "fallback_calls": fallback_calls,
        "semantic_accuracy": _safe_ratio(
            semantic_correct,
            semantic_total,
        ),
        "intent_accuracy": _safe_ratio(
            intent_correct,
            semantic_total,
        ),
        "rag_hit_rate": _safe_ratio(
            vector_hits,
            total_questions,
        ),
        "avg_context_chunks": round(
            total_context_chunks / vector_hits,
            2,
        )
        if vector_hits
        else 0.0,
        "professional_answer_rate": _safe_ratio(
            professional_answer_hits,
            total_questions,
        ),
        "observability_ready": True,
        "notes": {
            "semantic_accuracy": "Ratio of benchmark answers that matched expected semantic criteria.",
            "intent_accuracy": "Ratio of benchmark questions routed to the expected intent.",
            "rag_hit_rate": "Ratio of questions with at least one vector-retrieved document.",
            "avg_context_chunks": "Average number of retrieved vector chunks when retrieval succeeds.",
            "professional_answer_rate": "Ratio of answers following the expected analyst-grade narrative structure.",
            "llm_calls": "Number of answers generated with LLM assistance.",
            "fallback_calls": "Number of fallback-mode answers.",
        },
    }


def write_llm_metrics(
    metrics: dict[str, Any],
    output_path: Path = LLM_METRICS_PATH,
) -> None:
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        json.dumps(
            metrics,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )