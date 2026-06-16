from typing import Any


def run_root_cause_skill(
    artifacts: dict[str, Any],
) -> dict[str, Any]:
    return {
        "skill": "root_cause",
        "root_cause_analysis": artifacts.get("root_cause_analysis", {}),
    }