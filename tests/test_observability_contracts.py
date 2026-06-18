from pathlib import Path

from src.observability.alert_rules import AlertRuleRegistry
from src.observability.dashboard_registry import DashboardRegistry
from src.observability.health_registry import HealthRegistry
from src.observability.metrics_registry import ObservabilityMetrics
from src.observability.observability_service import ObservabilityService
from src.observability.prometheus_exporter import PrometheusExporter


def test_observability_metrics_contract():
    metrics = ObservabilityMetrics()

    payload = metrics.to_dict()

    assert payload["incident_priority"] == "P1"
    assert payload["severity"] == "critical"
    assert payload["scored_ips"] == 5726
    assert payload["idor_findings"] == 182
    assert payload["evaluation_score"] >= 0.80


def test_prometheus_exporter_contract():
    metrics = ObservabilityMetrics()
    exporter = PrometheusExporter()

    text = exporter.render(metrics)

    assert "dfir_scored_ips 5726" in text
    assert "dfir_idor_findings 182" in text
    assert "dfir_evaluation_score" in text
    assert "dfir_rag_hit_rate" in text


def test_observability_service_contract():
    service = ObservabilityService()

    payload = service.build_observability_status()

    assert payload["service"] == "dfir-observability"
    assert payload["prometheus_ready_endpoint"] == "/metrics"
    assert payload["prometheus_scrape_target"] == "http://dfir-api:8000/metrics"
    assert payload["promql_endpoint"] == "http://localhost:9090/api/v1/query"


def test_dashboard_registry_contract():
    dashboards = DashboardRegistry().list_dashboards()

    ids = [dashboard["id"] for dashboard in dashboards]

    assert "executive" in ids
    assert "dfir" in ids
    assert "agents" in ids


def test_alert_rule_registry_contract():
    rules = AlertRuleRegistry().list_rules()

    alerts = [rule["alert"] for rule in rules]

    assert "DFIRPlatformDown" in alerts
    assert "HighIDORFindings" in alerts
    assert "LowEvaluationScore" in alerts


def test_health_registry_contract():
    payload = HealthRegistry().build_health_contract()

    assert payload["platform_health"] == "healthy"
    assert payload["promql"] == "available_through_prometheus"


def test_observability_config_files_exist():
    expected_files = [
        "docker/compose/observability.yml",
        "docker/prometheus/prometheus.yml",
        "docker/prometheus/alert_rules.yml",
        "docker/grafana/provisioning/datasources/datasource.yml",
        "docker/grafana/provisioning/dashboards/dashboards.yml",
        "docker/grafana/dashboards/executive.json",
        "docker/grafana/dashboards/dfir.json",
        "docker/grafana/dashboards/agents.json",
    ]

    for file_path in expected_files:
        assert Path(file_path).exists(), file_path