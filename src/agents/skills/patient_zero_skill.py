from typing import Any


def run_patient_zero_skill(
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
        "skill": "patient_zero",
        "patient_zero_candidate": questions.get("patient_zero_candidate"),
        "evidence": [
            "NIST incident report questions_answered.patient_zero_candidate",
            "forensic evidence correlation",
            "agent investigation output",
        ],
    }