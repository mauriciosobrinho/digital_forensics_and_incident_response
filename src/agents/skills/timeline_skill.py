from typing import Any


def run_timeline_skill(
    artifacts: dict[str, Any],
) -> dict[str, Any]:
    questions = artifacts.get(
        "nist_incident_report",
        {},
    ).get(
        "questions_answered",
        {},
    )

    return {
        "skill": "timeline",
        "attack_start": questions.get("when_did_it_start"),
        "attack_end": questions.get("when_did_it_end"),
    }