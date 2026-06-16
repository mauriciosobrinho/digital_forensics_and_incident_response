from typing import Any


def run_impact_skill(
    artifacts: dict[str, Any],
) -> dict[str, Any]:
    dashboard = artifacts.get(
        "soc_dashboard_data",
        {},
    )

    return {
        "skill": "impact",
        "topline": dashboard.get("topline", {}),
        "pipeline_metrics": dashboard.get("pipeline_metrics", {}),
    }