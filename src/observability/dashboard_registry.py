class DashboardRegistry:
    def list_dashboards(self) -> list[dict]:
        return [
            {
                "id": "executive",
                "title": "DFIR Executive Dashboard",
                "path": "docker/grafana/dashboards/executive.json",
                "panels": [
                    "Scored IPs",
                    "IDOR Findings",
                    "Anomalous IPs",
                    "Agent Decisions",
                    "Platform Health",
                ],
            },
            {
                "id": "dfir",
                "title": "DFIR Investigation Dashboard",
                "path": "docker/grafana/dashboards/dfir.json",
                "panels": [
                    "Attack Surface",
                    "IDOR Findings",
                    "Anomaly Distribution",
                    "Containment Actions",
                ],
            },
            {
                "id": "agents",
                "title": "SOC Agents Dashboard",
                "path": "docker/grafana/dashboards/agents.json",
                "panels": [
                    "LLM Calls",
                    "Deterministic Calls",
                    "Fallback Calls",
                    "RAG Hit Rate",
                    "Professional Answer Rate",
                ],
            },
        ]