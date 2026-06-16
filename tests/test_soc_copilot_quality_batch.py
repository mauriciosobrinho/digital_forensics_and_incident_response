from src.agents.conversation_agent import ask_soc_copilot


QUESTIONS = [
    "Who is the patient zero?",
    "What evidence supports IDOR exploitation?",
    "Was the attack automated?",
    "What containment actions are recommended?",
    "What is the business impact?",
]


def test_soc_copilot_quality_batch_contract():
    for question in QUESTIONS:
        response = ask_soc_copilot(question)

        assert isinstance(response, dict)
        assert response.get("question") == question
        assert response.get("answer", "").strip()
        assert response.get("mode")
        assert "used_llm" in response
        assert "safety" in response

        if response.get("used_llm"):
            assert response.get("vector_context") is not None
            assert response.get("skill_outputs") is not None
            assert response.get("intent") is not None


def test_soc_copilot_vector_context_has_no_runtime_error():
    response = ask_soc_copilot(
        "Who is the patient zero and what evidence supports that conclusion?"
    )

    vector_context = response.get("vector_context", {})

    if vector_context:
        assert "error" not in vector_context