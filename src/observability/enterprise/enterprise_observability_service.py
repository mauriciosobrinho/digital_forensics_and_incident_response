from src.observability.metrics_registry import ObservabilityMetrics


class EnterpriseObservabilityService:
    release = "1.3.0"
    sprint = "5.0"
    service = "dfir-enterprise-observability"

    def get_metrics(self) -> dict:
        return ObservabilityMetrics().to_dict()

    def get_sli_slo(self) -> dict:
        return {
            "service": "dfir-enterprise-sli-slo",
            "release": self.release,
            "sprint": self.sprint,
            "sli": {
                "detection_success_rate": 0.97,
                "evidence_completeness": 0.95,
                "containment_readiness": 1.0,
            },
            "slo": {
                "detection_target": 0.95,
                "response_target": 0.90,
            },
        }

    def get_promql_catalog(self) -> list[dict]:
        return [
            {
                "name": "Detection Success Rate",
                "query": "dfir_sli_detection_success_rate",
                "purpose": "Monitor whether IDOR detection is meeting enterprise SLI expectations.",
            },
            {
                "name": "Evidence Completeness",
                "query": "dfir_sli_evidence_completeness",
                "purpose": "Track forensic evidence completeness for investigation readiness.",
            },
            {
                "name": "Agent Latency",
                "query": "dfir_agent_latency_seconds",
                "purpose": "Monitor multi-agent orchestration latency.",
            },
            {
                "name": "RAG Latency",
                "query": "dfir_rag_latency_seconds",
                "purpose": "Monitor retrieval latency for evidence-grounded answers.",
            },
            {
                "name": "LLM Latency",
                "query": "dfir_llm_latency_seconds",
                "purpose": "Monitor LLM response latency.",
            },
            {
                "name": "Human Approval Latency",
                "query": "dfir_human_approval_latency_seconds",
                "purpose": "Monitor human-in-the-loop approval latency.",
            },
            {
                "name": "Forensic Correlation Score",
                "query": "dfir_forensic_correlation_score",
                "purpose": "Measure correlation quality across DFIR, investigation and evidence artifacts.",
            },
            {
                "name": "BigQuery Readiness",
                "query": "dfir_bigquery_readiness",
                "purpose": "Check whether the platform is ready for BigQuery forensic analytics integration.",
            },
        ]

    def get_alert_rules(self) -> dict:
        return {
            "service": "dfir-enterprise-alert-rules",
            "alertmanager_url": "http://localhost:9093",
            "rules": [
                {
                    "alert": "LowEvidenceCompleteness",
                    "expr": "dfir_sli_evidence_completeness < 0.90",
                    "severity": "warning",
                },
                {
                    "alert": "AgentLatencyHigh",
                    "expr": "dfir_agent_latency_seconds > 5",
                    "severity": "warning",
                },
                {
                    "alert": "ForensicCorrelationLow",
                    "expr": "dfir_forensic_correlation_score < 0.90",
                    "severity": "critical",
                },
                {
                    "alert": "BigQueryReadinessMissing",
                    "expr": "dfir_bigquery_readiness == 0",
                    "severity": "warning",
                },
            ],
        }

    def get_dashboards(self) -> dict:
        return {
            "service": "dfir-enterprise-dashboards",
            "grafana_url": "http://localhost:3000",
            "dashboards": [
                {
                    "id": "executive",
                    "title": "DFIR Executive Dashboard",
                    "path": "docker/grafana/dashboards/executive.json",
                },
                {
                    "id": "dfir",
                    "title": "DFIR Investigation Dashboard",
                    "path": "docker/grafana/dashboards/dfir.json",
                },
                {
                    "id": "agents",
                    "title": "SOC Agents Dashboard",
                    "path": "docker/grafana/dashboards/agents.json",
                },
            ],
        }

    def get_bigquery_readiness(self) -> dict:
        return {
            "provider": "bigquery",
            "status": "ready_for_integration",
            "readiness": 1,
            "dataset_strategy": "forensic_analytics",
            "tables": [
                "raw_logs",
                "parsed_events",
                "risk_scores",
                "idor_findings",
                "forensic_evidence",
                "agent_decisions",
                "incident_metrics",
            ],
        }

    def get_forensic_correlation(self) -> dict:
        return {
            "service": "dfir-forensic-correlation",
            "score": 0.96,
            "correlation_layers": [
                "raw_logs",
                "parsed_events",
                "risk_scores",
                "idor_findings",
                "forensic_evidence",
                "agent_decisions",
                "response_metrics",
            ],
            "use_cases": [
                "patient_zero",
                "timeline",
                "automation",
                "idor_evidence",
                "business_impact",
                "containment",
                "nist",
                "mitre",
                "ioc",
                "root_cause",
            ],
        }

    def build_enterprise_contract(self) -> dict:
        return {
            "service": self.service,
            "release": self.release,
            "sprint": self.sprint,
            "metrics": self.get_metrics(),
            "sli_slo": self.get_sli_slo(),
            "promql_catalog": self.get_promql_catalog(),
            "alerts": self.get_alert_rules(),
            "forensic_correlation": self.get_forensic_correlation(),
            "dashboards": self.get_dashboards(),
            "bigquery_readiness": self.get_bigquery_readiness(),
        }

def build_enterprise_metrics() -> dict:
    return ObservabilityMetrics().to_dict()


def build_enterprise_prometheus_text() -> str:
    metrics = ObservabilityMetrics().to_dict()

    enterprise_metric_names = [
        "dfir_sli_detection_success_rate",
        "dfir_sli_evidence_completeness",
        "dfir_sli_containment_readiness",
        "dfir_slo_detection_target",
        "dfir_slo_response_target",
        "dfir_agent_latency_seconds",
        "dfir_rag_latency_seconds",
        "dfir_mcp_tool_latency_seconds",
        "dfir_llm_latency_seconds",
        "dfir_human_approval_latency_seconds",
        "dfir_ioc_generation_count",
        "dfir_affected_invoice_count",
        "dfir_patient_zero_confidence",
        "dfir_forensic_correlation_score",
        "dfir_bigquery_readiness",
    ]

    lines = []

    for metric_name in enterprise_metric_names:
        lines.append(f"# HELP {metric_name} Enterprise observability metric.")
        lines.append(f"# TYPE {metric_name} gauge")
        lines.append(f"{metric_name} {metrics[metric_name]}")

    return "\n".join(lines) + "\n"


def build_enterprise_observability_contract() -> dict:
    return EnterpriseObservabilityService().build_enterprise_contract()