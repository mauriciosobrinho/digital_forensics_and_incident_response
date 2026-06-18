class HealthRegistry:
    def build_health_contract(self) -> dict:
        return {
            "platform_health": "healthy",
            "fastapi": "ready",
            "streamlit": "ready",
            "prometheus_endpoint": "/metrics",
            "prometheus_scrape_target": "http://dfir-api:8000/metrics",
            "grafana_dashboards": "ready",
            "promql": "available_through_prometheus",
        }