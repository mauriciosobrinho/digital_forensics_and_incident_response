from src.agents.conversation_agent import ask_soc_copilot
from src.evaluation.soc_copilot_semantic_quality import (
    SEMANTIC_BENCHMARK,
    evaluate_semantic_response,
)


def test_soc_copilot_semantic_quality_benchmark():
    failures = []

    for expectation in SEMANTIC_BENCHMARK:
        response = ask_soc_copilot(
            expectation.question,
        )

        result = evaluate_semantic_response(
            expectation,
            response,
        )

        if not result["answer_is_correct"]:
            failures.append(
                {
                    "id": expectation.id,
                    "category": expectation.category,
                    "language": expectation.language,
                    "question": expectation.question,
                    "expected_facts": expectation.expected_facts,
                    "expected_any_terms": expectation.expected_any_terms,
                    "forbidden_terms": expectation.forbidden_terms,
                    "expected_intent": expectation.expected_intent,
                    "actual_intent": result["actual_intent"],
                    "expected_hits": result["expected_hits"],
                    "term_group_hits": result["term_group_hits"],
                    "forbidden_hits": result["forbidden_hits"],
                    "answer": result["answer"],
                }
            )

    assert not failures, failures