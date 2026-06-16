from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.agents.conversation_agent import ask_soc_copilot

from src.evaluation.soc_copilot_semantic_quality import (
    SEMANTIC_BENCHMARK,
    evaluate_semantic_response,
    write_semantic_quality_artifacts,
)

from src.evaluation.llm_metrics import (
    build_llm_metrics,
    write_llm_metrics,
)


OUTPUT_DIR = Path("data/evaluation")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_JSON = OUTPUT_DIR / "soc_copilot_question_batch_results.json"
OUTPUT_MD = OUTPUT_DIR / "soc_copilot_question_batch_report.md"
OUTPUT_CSV = OUTPUT_DIR / "soc_copilot_question_batch_summary.csv"


# QUESTIONS = [
#     "Who is the patient zero?",
#     "What evidence supports the patient zero conclusion?",
#     "When did the attack start?",
#     "When did the attack end?",
#     "How many invoices were affected?",
#     "Was the attack automated?",
#     "What containment actions are recommended?",
#     "What is the business impact?",
#     "What are the TTD, TTR and TTC metrics?",
#     "What evidence supports IDOR exploitation?",
#     "Explain the incident using the NIST incident response framework.",
#     "What is the root cause of the incident?",
#     "Summarize the incident for a CISO in less than 10 bullet points.",
#     "Correlate the forensic evidence, NIST report and observability metrics into a single incident narrative.",
#     "You are the lead DFIR analyst. Build a complete incident assessment covering patient zero, timeline, IDOR evidence, automation, affected assets, business impact and containment.",
# ]


# ADDITIONAL_QUESTIONS = [
#     "Explain the incident using the NIST incident response framework.",
#     "What is the root cause of the incident?",
#     "Summarize the incident for a CISO in less than 10 bullet points.",
#     "Correlate the forensic evidence, NIST report and observability metrics into a single incident narrative.",
#     "You are the lead DFIR analyst. Build a complete incident assessment covering patient zero, timeline, IDOR evidence, automation, affected assets, business impact and containment.",
# ]


QUESTION_BANK_PATH = Path(
    "data/evaluation/question_banks/soc_copilot_multilingual_question_bank.json"
)

def load_question_bank(path: Path = QUESTION_BANK_PATH) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["questions"]


def _score_response(
    response: dict,
    semantic_result: dict | None = None,
) -> dict:
    answer = response.get("answer", "")
    vector_context = response.get("vector_context", {})
    retrieved = vector_context.get("retrieved_documents", [])

    checks = {
        "has_answer": bool(answer.strip()),
        "has_mode": bool(response.get("mode")),
        "has_intent": bool(response.get("intent")),
        "has_vector_context": isinstance(vector_context, dict),
        "has_retrieved_documents": bool(retrieved),
        "has_skill_outputs": bool(response.get("skill_outputs")),
        "has_confidence": bool(response.get("confidence")),
        "has_safety": bool(response.get("safety")),
    }

    score = sum(
        1
        for value in checks.values()
        if value
    )

    return {
        "score": score,
        "max_score": len(checks),
        "coverage": round(
            score / len(checks),
            3,
        ),
        "checks": checks,
        "answer_is_correct": (
            semantic_result.get("answer_is_correct")
            if semantic_result
            else None
        ),
        "semantic_accuracy": (
            semantic_result.get("semantic_accuracy")
            if semantic_result
            else None
        ),
        "lexical_overlap": (
            semantic_result.get("lexical_overlap")
            if semantic_result
            else None
        ),
    }


def load_question_bank(
    path: Path = QUESTION_BANK_PATH,
) -> list[dict[str, Any]]:
    data = json.loads(
        path.read_text(
            encoding="utf-8",
        )
    )

    if "cases" in data:
        items = []

        for case in data["cases"]:
            for language, question in case.get("questions", {}).items():
                items.append(
                    {
                        "id": case.get("id"),
                        "category": case.get("category"),
                        "language": language,
                        "question": question,
                        "expected_intent": case.get("expected_intent"),
                        "expected_facts": case.get(
                            "expected_facts",
                            [],
                        ),
                        "expected_any_terms": case.get(
                            "expected_any_terms",
                            {},
                        ),
                        "forbidden_terms": case.get(
                            "forbidden_terms",
                            {},
                        ),
                    }
                )

        return items

    return data["questions"]


def main() -> None:
    results = []
    semantic_results = []

    question_items = load_question_bank()

    for index, item in enumerate(question_items, start=1):

        question = item["question"]

        print(f"[batch] {index}/{len(question_items)} - {question}")

        response = ask_soc_copilot(question)

        semantic_result = None

        for expectation in SEMANTIC_BENCHMARK:
            if expectation.question == question:
                semantic_result = evaluate_semantic_response(
                    expectation,
                    response,
                )

                semantic_results.append(
                    semantic_result,
                )

                break

        score = _score_response(
            response,
            semantic_result,
        )

        results.append(
            {
                "id": item.get("id"),
                "category": item.get("category"),
                "question": question,
                "expected_intent": item.get(
                    "expected_intent"
                ),
                "expected_contains": item.get(
                    "expected_contains",
                    [],
                ),
                "forbidden_contains": item.get(
                    "forbidden_contains",
                    [],
                ),
                "response": response,
                "quality_score": score,
                "semantic_result": semantic_result,

                "language": item.get("language"),
                "expected_facts": item.get("expected_facts", []),
                "expected_any_terms": item.get("expected_any_terms", {}),
                "forbidden_terms": item.get("forbidden_terms", {}),
            }
        )

    semantic_artifacts = write_semantic_quality_artifacts(
        semantic_results,
    )

    llm_metrics = build_llm_metrics(
        batch_results=results,
        semantic_results=semantic_results,
    )

    write_llm_metrics(
        llm_metrics,
    )

    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "total_questions": len(question_items),
        "semantic_artifacts": semantic_artifacts,
        "results": results,
        "llm_metrics": llm_metrics,
    }

    OUTPUT_JSON.write_text(
        json.dumps(
            payload,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

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
                "question",
                "expected_intent",
                "mode",
                "used_llm",
                "confidence",
                "quality_score",
                "quality_coverage",
                "answer_is_correct",
                "semantic_accuracy",
                "lexical_overlap",
                "retrieved_documents_count",
                "answer_preview",
            ],
        )

        writer.writeheader()

        for item in results:
            response = item["response"]
            quality = item["quality_score"]
            retrieved = (
                response.get("vector_context", {})
                .get("retrieved_documents", [])
            )

            writer.writerow(
                {
                    "id": item.get("id"),
                    "category": item.get("category"),
                    "question": item["question"],
                    "expected_intent": item.get("expected_intent"),
                    "mode": response.get("mode"),
                    "used_llm": response.get("used_llm"),
                    "confidence": response.get("confidence"),
                    "quality_score": quality["score"],
                    "quality_coverage": quality["coverage"],
                    "answer_is_correct": quality["answer_is_correct"],
                    "semantic_accuracy": quality["semantic_accuracy"],
                    "lexical_overlap": quality["lexical_overlap"],
                    "retrieved_documents_count": len(retrieved),
                    "answer_preview": response.get("answer", "")[:500],
                }
            )

    markdown = [
        "# SOC Copilot Question Batch Report",
        "",
        f"Generated at: {payload['generated_at_utc']}",
        "",
        f"Total questions: {len(question_items)}",
        "",
        "## Semantic Quality Summary",
        "",
        f"- Semantic accuracy: `{semantic_artifacts['summary']['semantic_accuracy']}`",
        f"- Correct answers: `{semantic_artifacts['summary']['correct_answers']}`",
        f"- Failed answers: `{semantic_artifacts['summary']['failed_answers']}`",
        "",
    ]

    for item in results:
        response = item["response"]
        quality = item["quality_score"]

        markdown.extend(
            [
                "---",
                "",
                "## Question",
                "",
                item["question"],
                "",
                "## Question Metadata",
                "",
                f"- id: `{item.get('id')}`",
                f"- category: `{item.get('category')}`",
                f"- expected_intent: `{item.get('expected_intent')}`",
                "",
                "## Answer",
                "",
                response.get("answer", ""),
                "",
                "## Response Metadata",
                "",
                f"- mode: `{response.get('mode')}`",
                f"- used_llm: `{response.get('used_llm')}`",
                f"- confidence: `{response.get('confidence')}`",
                f"- quality coverage: `{quality['coverage']}`",
                f"- answer_is_correct: `{quality['answer_is_correct']}`",
                f"- semantic_accuracy: `{quality['semantic_accuracy']}`",
                "",
            ]
        )

    OUTPUT_MD.write_text(
        "\n".join(markdown),
        encoding="utf-8",
    )

    print(f"[batch] JSON written to: {OUTPUT_JSON}")
    print(f"[batch] CSV written to: {OUTPUT_CSV}")
    print(f"[batch] Markdown written to: {OUTPUT_MD}")
    print(f"[batch] Semantic JSON written to: {semantic_artifacts['json_path']}")
    print(f"[batch] Semantic CSV written to: {semantic_artifacts['csv_path']}")
    print(f"[batch] Semantic Markdown written to: {semantic_artifacts['markdown_path']}")
    print("[batch] LLM metrics written to: data/observability/llm_metrics.json")


if __name__ == "__main__":
    main()