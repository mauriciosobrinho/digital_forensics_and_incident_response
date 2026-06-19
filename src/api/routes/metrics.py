from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from src.observability.observability_service import ObservabilityService

from src.observability.enterprise.enterprise_observability_service import (
    build_enterprise_metrics,
    build_enterprise_prometheus_text,
)

router = APIRouter(
    tags=["metrics"],
)

observability_service = ObservabilityService()


def build_operational_metrics() -> dict:
    payload = observability_service.build_metrics().to_dict()

    payload.update(
        build_enterprise_metrics()
    )

    return payload


@router.get("/api/metrics")
def get_metrics() -> dict:

    payload = observability_service.build_api_metrics()

    payload.update(
        build_enterprise_metrics()
    )

    return payload


@router.get("/metrics", response_class=PlainTextResponse)
def prometheus_metrics() -> str:

    prometheus_text = (
        observability_service.render_prometheus_metrics()
    )

    prometheus_text += (
        build_enterprise_prometheus_text()
    )

    return prometheus_text