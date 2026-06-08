from typing import Any


def get_critical_ips(
    risk_summary: dict[str, Any],
) -> list[str]:
    return [
        item["ip"]
        for item in risk_summary.get(
            "top_risk_ips",
            [],
        )
        if item.get("risk_level") == "critical"
    ]


def summarize_risk_distribution(
    risk_summary: dict[str, Any],
) -> dict[str, Any]:
    return {
        "total_ips": risk_summary.get(
            "total_ips",
            0,
        ),
        "risk_level_distribution": risk_summary.get(
            "risk_level_distribution",
            [],
        ),
    }