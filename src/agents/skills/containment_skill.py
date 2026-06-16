from typing import Any


def run_containment_skill(
    artifacts: dict[str, Any],
) -> dict[str, Any]:
    strategy = artifacts.get(
        "containment_strategy",
        {},
    )

    return {
        "skill": "containment",
        "dry_run": True,
        "strategy": strategy,
        "note": "No external containment action is executed automatically.",
    }