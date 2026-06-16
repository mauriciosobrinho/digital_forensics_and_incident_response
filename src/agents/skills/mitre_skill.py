from typing import Any


def run_mitre_skill(
    artifacts: dict[str, Any],
) -> dict[str, Any]:
    investigation = artifacts.get(
        "agent_investigation",
        {},
    )

    return {
        "skill": "mitre",
        "mapping": investigation.get("mitre_mapping", {}),
    }