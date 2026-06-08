import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_json_artifact(
    file_path: Path,
) -> dict[str, Any]:
    with file_path.open(
        "r",
        encoding="utf-8",
    ) as f:
        return json.load(f)


def get_top_attackers(
    forensic_evidence: dict[str, Any],
    top_n: int = 10,
) -> list[dict[str, Any]]:
    return forensic_evidence.get(
        "top_attackers",
        [],
    )[:top_n]


def get_attack_window(
    attack_timeline: dict[str, Any],
) -> dict[str, Any]:
    return attack_timeline.get(
        "summary",
        {},
    )


def log_tool_call(
    tool_execution_log: list[dict[str, Any]],
    tool_name: str,
    inputs: dict[str, Any],
    output_summary: str,
) -> list[dict[str, Any]]:
    return [
        *tool_execution_log,
        {
            "tool": tool_name,
            "timestamp_utc": datetime.now(
                timezone.utc
            ).isoformat(),
            "inputs": inputs,
            "output_summary": output_summary,
        },
    ]