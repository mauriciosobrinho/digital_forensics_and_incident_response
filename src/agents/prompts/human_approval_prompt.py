from src.agents.prompts.base import ANSWER_CONTRACT, GROUNDING_POLICY


def build_human_approval_prompt(context: str) -> str:
    return f"You are a human approval governance agent.\n\n{GROUNDING_POLICY}\n\n{ANSWER_CONTRACT}\n\nContext:\n{context}"