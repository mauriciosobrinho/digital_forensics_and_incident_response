def build_enterprise_dashboard_registry() -> dict:
    return {
        "dashboards": [
            {
                "name": "DFIR Executive Dashboard",
                "path": "docker/grafana/dashboards/executive.json",
                "audience": "CISO, leadership, legal and business stakeholders",
                "panels": [
                    "Incident severity",
                    "Business impact",
                    "Affected invoices",
                    "Detection and response SLO",
                    "Forensic correlation score",
                ],
            },
            {
                "name": "DFIR Investigation Dashboard",
                "path": "docker/grafana/dashboards/dfir.json",
                "audience": "DFIR analysts and incident responders",
                "panels": [
                    "IDOR findings",
                    "Anomalous IPs",
                    "Patient zero confidence",
                    "IOC generation",
                    "Evidence completeness",
                ],
            },
            {
                "name": "SOC Agents Dashboard",
                "path": "docker/grafana/dashboards/agents.json",
                "audience": "SOC, AI engineering and platform operators",
                "panels": [
                    "Agent latency",
                    "RAG hit rate",
                    "MCP tool latency",
                    "LLM latency",
                    "Human approval latency",
                ],
            },
        ]
    }