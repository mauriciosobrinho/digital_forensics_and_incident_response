from typing import Any


def run_metrics_skill(
    artifacts: dict[str, Any],
) -> dict[str, Any]:
    report = artifacts.get(
        "nist_incident_report",
        {},
    )

    return {
        "skill": "metrics",
        "ttd": report.get("ttd"),
        "ttr": report.get("ttr"),
        "ttc": report.get("ttc"),
        "response_metrics": artifacts.get("response_metrics", {}),
    }