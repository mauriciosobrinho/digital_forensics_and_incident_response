from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _artifact_status(path: Path) -> dict[str, Any]:
    exists = path.exists()

    return {
        "path": str(path),
        "exists": exists,
        "size_bytes": path.stat().st_size
        if exists
        else 0,
    }


def build_healthcheck(
    *,
    required_artifacts: dict[str, Path],
    platform_metrics: dict[str, Any],
    agent_metrics: dict[str, Any],
) -> dict[str, Any]:

    artifacts = {
        name: _artifact_status(path)
        for name, path in required_artifacts.items()
    }

    missing = [
        name
        for name, item in artifacts.items()
        if not item["exists"]
    ]

    degraded = []

    if platform_metrics.get("status") != "healthy":
        degraded.append("platform_metrics")

    if agent_metrics.get("status") != "healthy":
        degraded.append("agent_metrics")

    overall_status = (
        "healthy"
        if not missing and not degraded
        else "degraded"
    )

    return {
        "healthcheck_type": "platform_healthcheck",
        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "overall_status": overall_status,
        "missing_artifacts": missing,
        "degraded_components": degraded,
        "artifact_status": artifacts,
    }