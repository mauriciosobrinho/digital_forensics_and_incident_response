from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from src.observability.observability_service import ObservabilityService


router = APIRouter(
    tags=["metrics"],
)


observability_service = ObservabilityService()


def build_operational_metrics() -> dict:
    return observability_service.build_metrics().to_dict()


@router.get("/api/metrics")
def get_metrics() -> dict:
    return observability_service.build_api_metrics()


@router.get("/metrics", response_class=PlainTextResponse)
def prometheus_metrics() -> str:
    return observability_service.render_prometheus_metrics()