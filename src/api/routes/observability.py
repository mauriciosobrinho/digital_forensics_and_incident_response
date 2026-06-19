from fastapi import APIRouter

from src.observability.alert_rules import AlertRuleRegistry
from src.observability.dashboard_registry import DashboardRegistry
from src.observability.health_registry import HealthRegistry
from src.observability.observability_service import ObservabilityService
from src.observability.enterprise.enterprise_observability_service import (
    EnterpriseObservabilityService,
    build_enterprise_observability_contract,
)

router = APIRouter(
    prefix="/api",
    tags=["observability"],
)

observability_service = ObservabilityService()
dashboard_registry = DashboardRegistry()
alert_registry = AlertRuleRegistry()
health_registry = HealthRegistry()
enterprise_service = EnterpriseObservabilityService()


@router.get("/observability")
def get_observability() -> dict:
    return {
        **observability_service.build_observability_status(),
        "health": health_registry.build_health_contract(),
        "dashboards": dashboard_registry.list_dashboards(),
        "alert_rules": alert_registry.list_rules(),
        "enterprise": build_enterprise_observability_contract(),
    }


@router.get("/observability/sli-slo")
def get_sli_slo() -> dict:
    return enterprise_service.get_sli_slo()


@router.get("/observability/promql")
def get_promql_catalog() -> list[dict]:
    return enterprise_service.get_promql_catalog()


@router.get("/observability/alerts")
def get_alert_rules() -> dict:
    return enterprise_service.get_alert_rules()


@router.get("/observability/dashboards")
def get_enterprise_dashboards() -> dict:
    return enterprise_service.get_dashboards()


@router.get("/observability/bigquery-readiness")
def get_bigquery_readiness() -> dict:
    return enterprise_service.get_bigquery_readiness()


@router.get("/observability/forensic-correlation")
def get_forensic_correlation() -> dict:
    return enterprise_service.get_forensic_correlation()