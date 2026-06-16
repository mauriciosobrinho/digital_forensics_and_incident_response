from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.config.settings import INTERACTIVE_SESSION_LOG_FILE


def _load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default

    try:
        return json.loads(
            path.read_text(encoding="utf-8")
        )
    except json.JSONDecodeError:
        return default


def load_recent_conversation_turns(
    limit: int = 6,
) -> list[dict[str, Any]]:
    data = _load_json(
        INTERACTIVE_SESSION_LOG_FILE,
        [],
    )

    if not isinstance(data, list):
        return []

    return data[-limit:]


def summarize_recent_turns(
    turns: list[dict[str, Any]],
) -> str:
    if not turns:
        return "No previous conversation turns available."

    lines: list[str] = []

    for turn in turns:
        question = turn.get("question", "")
        response = turn.get("response", {})
        answer = ""

        if isinstance(response, dict):
            answer = response.get("answer", "")

        lines.append(
            f"User asked: {question}\nAssistant answered: {answer[:800]}"
        )

    return "\n\n".join(lines)


def build_session_context() -> dict[str, Any]:
    turns = load_recent_conversation_turns()

    return {
        "recent_turns": turns,
        "summary": summarize_recent_turns(turns),
    }