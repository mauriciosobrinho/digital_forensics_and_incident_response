from src.agents.professional_soc_copilot import answer_professional_soc_question


def test_professional_soc_copilot_contract():
    response = answer_professional_soc_question(
        "Who is the patient zero?"
    )

    assert isinstance(response, dict)
    assert "question" in response
    assert "answer" in response
    assert "mode" in response
    assert "used_llm" in response
    assert "intent" in response
    assert "vector_context" in response
    assert "session_context" in response
    assert "skill_outputs" in response
    assert response["answer"].strip()