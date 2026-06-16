from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


QUESTION_BANK_PATH = Path(
    "data/evaluation/question_banks/soc_copilot_multilingual_question_bank.json"
)

OUTPUT_JSON = Path(
    "data/evaluation/soc_copilot_semantic_quality_results.json"
)

OUTPUT_CSV = Path(
    "data/evaluation/soc_copilot_semantic_quality_results.csv"
)

OUTPUT_MD = Path(
    "data/evaluation/soc_copilot_semantic_quality_report.md"
)

INTENT_ALIASES = {
    "attack_start": {
        "attack_start",
        "timeline",
    },
    "attack_end": {
        "attack_end",
        "timeline",
        "attack_start",
    },
    "affected_invoices": {
        "affected_invoices",
        "business_impact",
        "unknown",
    },
}

@dataclass(frozen=True)
class SemanticExpectation:
    id: str
    category: str
    language: str
    question: str
    expected_intent: str | None
    expected_facts: tuple[str, ...]
    expected_any_terms: tuple[tuple[str, ...], ...]
    forbidden_terms: tuple[str, ...]


def _remove_accents(value: str) -> str:
    return "".join(
        char
        for char in unicodedata.normalize("NFKD", value)
        if not unicodedata.combining(char)
    )


def _normalize_number_match(match: re.Match[str]) -> str:
    value = match.group(0)

    if re.fullmatch(
        r"\d{1,3}(\.\d{1,3}){3}",
        value,
    ):
        return value

    return re.sub(
        r"[,.\s\u202f\u00a0]",
        "",
        value,
    )


def normalize_text(value: Any) -> str:
    text = str(value or "").lower()
    text = _remove_accents(text)

    text = (
        text
        .replace("\u2010", "-")
        .replace("\u2011", "-")
        .replace("\u2012", "-")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\u2212", "-")
    )

    text = re.sub(
        r"\b\d{1,3}([,.\s\u202f\u00a0]\d{3})+\b",
        _normalize_number_match,
        text,
    )

    return text


def _intent_value(response: dict[str, Any]) -> str | None:
    intent = response.get("intent")

    if isinstance(intent, dict):
        return intent.get("intent")

    return intent


def load_multilingual_question_bank(
    path: Path = QUESTION_BANK_PATH,
) -> list[SemanticExpectation]:
    data = json.loads(
        path.read_text(
            encoding="utf-8",
        )
    )

    expectations: list[SemanticExpectation] = []

    for item in data.get("cases", []):
        expected_any_terms = item.get(
            "expected_any_terms",
            {},
        ).get(
            "any",
            [],
        )

        forbidden_terms = item.get(
            "forbidden_terms",
            {},
        ).get(
            "any",
            [],
        )

        for language, question in item.get("questions", {}).items():
            expectations.append(
                SemanticExpectation(
                    id=item["id"],
                    category=item["category"],
                    language=language,
                    question=question,
                    expected_intent=item.get("expected_intent"),
                    expected_facts=tuple(
                        item.get(
                            "expected_facts",
                            [],
                        )
                    ),
                    expected_any_terms=tuple(
                        tuple(group)
                        for group in expected_any_terms
                    ),
                    forbidden_terms=tuple(
                        forbidden_terms
                    ),
                )
            )

    return expectations


SEMANTIC_BENCHMARK = load_multilingual_question_bank()


def _contains_term(
    answer: str,
    term: str,
) -> bool:
    return normalize_text(term) in answer


def evaluate_semantic_response(
    expectation: SemanticExpectation,
    response: dict[str, Any],
) -> dict[str, Any]:
    answer = normalize_text(
        response.get(
            "answer",
            "",
        )
    )

    actual_intent = _intent_value(response)

    expected_hits = [
        fact
        for fact in expectation.expected_facts
        if _contains_term(
            answer,
            fact,
        )
    ]

    fact_pass = len(expected_hits) == len(
        expectation.expected_facts
    )

    term_group_hits = []

    for group in expectation.expected_any_terms:
        matched = [
            term
            for term in group
            if _contains_term(
                answer,
                term,
            )
        ]

        if matched:
            term_group_hits.append(
                matched[0]
            )

    any_terms_pass = len(term_group_hits) == len(
        expectation.expected_any_terms
    )

    forbidden_hits = [
        term
        for term in expectation.forbidden_terms
        if _contains_term(
            answer,
            term,
        )
    ]

    forbidden_pass = not forbidden_hits

    allowed_intents = INTENT_ALIASES.get(
        expectation.expected_intent,
        {expectation.expected_intent},
    )

    intent_pass = (
        True
        if expectation.expected_intent is None
        else actual_intent in allowed_intents
    )

    answer_is_correct = (
        fact_pass
        and any_terms_pass
        and forbidden_pass
        and intent_pass
    )

    lexical_total = (
        len(expectation.expected_facts)
        + len(expectation.expected_any_terms)
    )

    lexical_hits = len(expected_hits) + len(term_group_hits)

    lexical_overlap = (
        round(
            lexical_hits / lexical_total,
            4,
        )
        if lexical_total
        else None
    )

    return {
        "id": expectation.id,
        "category": expectation.category,
        "language": expectation.language,
        "question": expectation.question,
        "expected_intent": expectation.expected_intent,
        "actual_intent": actual_intent,
        "expected_facts": list(expectation.expected_facts),
        "expected_hits": expected_hits,
        "expected_any_terms": [
            list(group)
            for group in expectation.expected_any_terms
        ],
        "term_group_hits": term_group_hits,
        "forbidden_terms": list(expectation.forbidden_terms),
        "forbidden_hits": forbidden_hits,
        "fact_pass": fact_pass,
        "any_terms_pass": any_terms_pass,
        "forbidden_pass": forbidden_pass,
        "intent_pass": intent_pass,
        "answer_is_correct": answer_is_correct,
        "semantic_accuracy": 1.0 if answer_is_correct else 0.0,
        "lexical_overlap": lexical_overlap,
        "answer": response.get(
            "answer",
            "",
        ),
        "mode": response.get("mode"),
        "used_llm": response.get("used_llm"),
        "confidence": response.get("confidence"),
    }


def write_semantic_quality_artifacts(
    results: list[dict[str, Any]],
) -> dict[str, Any]:
    OUTPUT_JSON.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    total = len(results)
    correct = sum(
        1
        for item in results
        if item.get("answer_is_correct")
    )

    summary = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "total_questions": total,
        "correct_answers": correct,
        "failed_answers": total - correct,
        "semantic_accuracy": round(
            correct / total,
            4,
        )
        if total
        else 0.0,
    }

    payload = {
        "summary": summary,
        "results": results,
    }

    OUTPUT_JSON.write_text(
        json.dumps(
            payload,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    import csv

    with OUTPUT_CSV.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "id",
                "category",
                "language",
                "question",
                "expected_intent",
                "actual_intent",
                "answer_is_correct",
                "semantic_accuracy",
                "lexical_overlap",
                "mode",
                "used_llm",
                "confidence",
            ],
        )

        writer.writeheader()

        for item in results:
            writer.writerow(
                {
                    "id": item.get("id"),
                    "category": item.get("category"),
                    "language": item.get("language"),
                    "question": item.get("question"),
                    "expected_intent": item.get("expected_intent"),
                    "actual_intent": item.get("actual_intent"),
                    "answer_is_correct": item.get("answer_is_correct"),
                    "semantic_accuracy": item.get("semantic_accuracy"),
                    "lexical_overlap": item.get("lexical_overlap"),
                    "mode": item.get("mode"),
                    "used_llm": item.get("used_llm"),
                    "confidence": item.get("confidence"),
                }
            )

    markdown = [
        "# SOC Copilot Multilingual Semantic Quality Report",
        "",
        f"Generated at: {summary['generated_at_utc']}",
        "",
        f"- Total questions: `{summary['total_questions']}`",
        f"- Correct answers: `{summary['correct_answers']}`",
        f"- Failed answers: `{summary['failed_answers']}`",
        f"- Semantic accuracy: `{summary['semantic_accuracy']}`",
        "",
    ]

    for item in results:
        markdown.extend(
            [
                "---",
                "",
                f"## {item.get('id')} [{item.get('language')}]",
                "",
                f"Question: {item.get('question')}",
                "",
                f"- category: `{item.get('category')}`",
                f"- expected_intent: `{item.get('expected_intent')}`",
                f"- actual_intent: `{item.get('actual_intent')}`",
                f"- answer_is_correct: `{item.get('answer_is_correct')}`",
                f"- semantic_accuracy: `{item.get('semantic_accuracy')}`",
                "",
            ]
        )

    OUTPUT_MD.write_text(
        "\n".join(markdown),
        encoding="utf-8",
    )

    return {
        "json_path": str(OUTPUT_JSON),
        "csv_path": str(OUTPUT_CSV),
        "markdown_path": str(OUTPUT_MD),
        "summary": summary,
    }