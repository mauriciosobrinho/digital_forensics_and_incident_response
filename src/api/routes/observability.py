from fastapi import APIRouter

from src.config.settings import (
    AGENT_METRICS_FILE,
    HEALTHCHECK_FILE,
    PLATFORM_METRICS_FILE,
    SOC_DASHBOARD_DATA_FILE,
)


router = APIRouter(
    prefix="/api",
    tags=["observability"],
)


@router.get("/observability")
def get_observability() -> dict:
    healthcheck_available = HEALTHCHECK_FILE.exists()
    platform_metrics_available = PLATFORM_METRICS_FILE.exists()
    agent_metrics_available = AGENT_METRICS_FILE.exists()
    dashboard_data_available = SOC_DASHBOARD_DATA_FILE.exists()

    platform_health = (
        "healthy"
        if all(
            [
                healthcheck_available,
                platform_metrics_available,
                agent_metrics_available,
                dashboard_data_available,
            ]
        )
        else "degraded"
    )

    return {
        "service": "dfir-observability",
        "platform_health": platform_health,
        "healthcheck_available": healthcheck_available,
        "platform_metrics_available": platform_metrics_available,
        "agent_metrics_available": agent_metrics_available,
        "dashboard_data_available": dashboard_data_available,
        "prometheus_ready_endpoint": "/metrics",
        "future_stack": {
            "prometheus": "docker/compose/observability.yml",
            "grafana": "docker/grafana/",
            "scrape_target": "http://dfir-api:8000/metrics",
        },
    }