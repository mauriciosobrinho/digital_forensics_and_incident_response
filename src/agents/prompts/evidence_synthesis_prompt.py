from src.agents.prompts.base import ANSWER_CONTRACT, GROUNDING_POLICY


def build_evidence_synthesis_prompt(context: str) -> str:
    return f"You synthesize DFIR evidence into grounded conclusions.\n\n{GROUNDING_POLICY}\n\n{ANSWER_CONTRACT}\n\nContext:\n{context}"