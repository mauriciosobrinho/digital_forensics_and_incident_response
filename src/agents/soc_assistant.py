from typing import Any

from src.agents.conversation_agent import ask_soc_copilot


def answer_soc_question(
    question: str,
) -> dict[str, Any]:
    return ask_soc_copilot(
        question
    )