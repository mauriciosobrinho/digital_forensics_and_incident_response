from src.agents.prompts.base import ANSWER_CONTRACT, GROUNDING_POLICY


def build_triage_prompt(context: str) -> str:
    return f"You are a DFIR triage agent.\n\n{GROUNDING_POLICY}\n\n{ANSWER_CONTRACT}\n\nContext:\n{context}"