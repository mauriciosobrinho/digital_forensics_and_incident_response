from src.agents.conversation_agent import ask_soc_copilot


def test_soc_copilot_top_attackers_natural_language():
    response = ask_soc_copilot(
        "Quais são os top IPs atacantes?"
    )

    assert "answer" in response
    assert response["safety"]["dry_run"] is True
    assert "principais IPs suspeitos" in response["answer"]


def test_soc_copilot_idor_explanation():
    response = ask_soc_copilot(
        "Explique IDOR e Broken Access Control"
    )

    assert "answer" in response
    assert "IDOR" in response["answer"]
    assert response["used_llm"] in {True, False}