import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_investigation_memory(
    memory_file: Path,
) -> dict[str, Any]:
    if not memory_file.exists():
        return {
            "prior_runs": [],
            "known_iocs": [],
            "notes": [],
        }

    with memory_file.open(
        "r",
        encoding="utf-8",
    ) as f:
        return json.load(f)


def update_investigation_memory(
    memory: dict[str, Any],
    investigation_summary: dict[str, Any],
) -> dict[str, Any]:
    prior_runs = memory.get(
        "prior_runs",
        [],
    )

    prior_runs.append(
        {
            "generated_at_utc": datetime.now(
                timezone.utc
            ).isoformat(),
            "summary": investigation_summary,
        }
    )

    memory["prior_runs"] = prior_runs[-20:]

    return memory


def save_investigation_memory(
    memory: dict[str, Any],
    memory_file: Path,
) -> None:
    memory_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with memory_file.open(
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            memory,
            f,
            indent=2,
            ensure_ascii=False,
        )