import json
from pathlib import Path

from src.observability.metrics_registry import ObservabilityMetrics
from src.observability.prometheus_exporter import PrometheusExporter


class ObservabilityService:
    def __init__(self) -> None:
        self.exporter = PrometheusExporter()

    def build_metrics(self) -> ObservabilityMetrics:
        return ObservabilityMetrics()

    def build_api_metrics(self) -> dict:
        return {
            "service": "dfir-operational-metrics",
            **self.build_metrics().to_dict(),
        }

    def build_observability_status(self) -> dict:
        return {
            "service": "dfir-observability",
            "platform_health": "healthy",
            "prometheus_ready_endpoint": "/metrics",
            "prometheus_scrape_target": "http://dfir-api:8000/metrics",
            "promql_endpoint": "http://localhost:9090/api/v1/query",
            "grafana_url": "http://localhost:3000",
            "dashboards": [
                "executive",
                "dfir",
                "agents",
            ],
            "stack": {
                "prometheus": "docker/prometheus/prometheus.yml",
                "alert_rules": "docker/prometheus/alert_rules.yml",
                "grafana": "docker/grafana/",
            },
        }

    def render_prometheus_metrics(self) -> str:
        return self.exporter.render(self.build_metrics())

    def write_executive_dashboard_data(
        self,
        output_path: Path = Path("data/observability/executive_dashboard_data.json"),
    ) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "service": "dfir-executive-dashboard",
            "metrics": self.build_metrics().to_dict(),
            "prometheus": {
                "scrape_target": "http://dfir-api:8000/metrics",
                "promql_examples": [
                    "dfir_scored_ips",
                    "dfir_idor_findings",
                    "dfir_platform_health",
                    "dfir_evaluation_score",
                ],
            },
        }
        output_path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )