import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_conversation_memory(
    memory_file: Path,
) -> list[dict[str, Any]]:
    if not memory_file.exists():
        return []

    with memory_file.open("r", encoding="utf-8") as f:
        return json.load(f)


def append_conversation_turn(
    memory_file: Path,
    question: str,
    response: dict[str, Any],
) -> list[dict[str, Any]]:
    memory = load_conversation_memory(memory_file)

    memory.append(
        {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "question": question,
            "answer": response.get("answer"),
            "mode": response.get("mode"),
            "used_llm": response.get("used_llm", False),
        }
    )

    memory_file.parent.mkdir(parents=True, exist_ok=True)

    with memory_file.open("w", encoding="utf-8") as f:
        json.dump(memory[-100:], f, indent=2, ensure_ascii=False)

    return memory[-100:]