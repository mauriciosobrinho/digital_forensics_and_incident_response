from pathlib import Path


PROMPTS_DIR = Path(__file__).resolve().parents[1] / "prompts"


def load_prompt(
    prompt_name: str,
) -> str:
    prompt_file = PROMPTS_DIR / prompt_name

    if not prompt_file.exists():
        raise FileNotFoundError(
            f"Prompt file not found: {prompt_file}"
        )

    return prompt_file.read_text(
        encoding="utf-8",
    )