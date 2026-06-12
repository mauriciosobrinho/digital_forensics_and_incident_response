from src.agents.conversation_agent import ask_soc_copilot


def test_soc_copilot_top_attackers_natural_language():
    response = ask_soc_copilot(
        "Quais são os top IPs atacantes?"
    )

    assert isinstance(response, dict)
    assert "answer" in response
    assert "mode" in response
    assert "question" in response

    assert response["answer"].strip()
    assert response["question"] == "Quais são os top IPs atacantes?"


def test_soc_copilot_idor_explanation():
    response = ask_soc_copilot(
        "Explique IDOR e Broken Access Control"
    )

    assert isinstance(response, dict)
    assert "answer" in response
    assert "mode" in response
    assert "question" in response

    answer = response["answer"].lower()

    assert response["answer"].strip()
    assert response["question"] == "Explique IDOR e Broken Access Control"
    
    assert response["mode"] in {
        "evidence_grounded",
        "evidence_grounded_llm",
    }

    assert response.get("evidence_grounded") is True

    assert "idor" in answer
    assert (
        "evidence" in answer
        or "invoice enumeration" in answer
        or "broken access control" in answer
        or "object reference" in answer
    )