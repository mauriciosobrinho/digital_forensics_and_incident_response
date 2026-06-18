from fastapi import APIRouter

from src.observability.alert_rules import AlertRuleRegistry
from src.observability.dashboard_registry import DashboardRegistry
from src.observability.health_registry import HealthRegistry
from src.observability.observability_service import ObservabilityService


router = APIRouter(
    prefix="/api",
    tags=["observability"],
)


observability_service = ObservabilityService()
dashboard_registry = DashboardRegistry()
alert_registry = AlertRuleRegistry()
health_registry = HealthRegistry()


@router.get("/observability")
def get_observability() -> dict:
    return {
        **observability_service.build_observability_status(),
        "health": health_registry.build_health_contract(),
        "dashboards": dashboard_registry.list_dashboards(),
        "alert_rules": alert_registry.list_rules(),
    }