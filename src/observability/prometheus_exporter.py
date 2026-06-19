from src.observability.metrics_registry import ObservabilityMetrics


class PrometheusExporter:
    def render(self, metrics: ObservabilityMetrics) -> str:
        data = metrics.to_dict()

        health_value = 1 if data["platform_health"] == "healthy" else 0
        critical_value = 1 if data["severity"] == "critical" else 0

        prometheus_metrics = {
            "dfir_scored_ips": data["scored_ips"],
            "dfir_idor_findings": data["idor_findings"],
            "dfir_anomalous_ips": data["anomalous_ips"],
            "dfir_agent_decisions": data["agent_decisions"],
            "dfir_platform_health": health_value,
            "dfir_incident_critical": critical_value,
            "dfir_evaluation_score": data["evaluation_score"],
            "dfir_approval_rate": data["approval_rate"],
            "dfir_containment_actions": data["containment_actions"],
            "dfir_mean_response_time_seconds": data["mean_response_time_seconds"],
            "dfir_llm_calls": data["llm_calls"],
            "dfir_deterministic_calls": data["deterministic_calls"],
            "dfir_fallback_calls": data["fallback_calls"],
            "dfir_rag_hit_rate": data["rag_hit_rate"],
            "dfir_professional_answer_rate": data["professional_answer_rate"],
            "dfir_sli_detection_success_rate": data["dfir_sli_detection_success_rate"],
            "dfir_sli_evidence_completeness": data["dfir_sli_evidence_completeness"],
            "dfir_sli_containment_readiness": data["dfir_sli_containment_readiness"],
            "dfir_slo_detection_target": data["dfir_slo_detection_target"],
            "dfir_slo_response_target": data["dfir_slo_response_target"],
            "dfir_agent_latency_seconds": data["dfir_agent_latency_seconds"],
            "dfir_rag_latency_seconds": data["dfir_rag_latency_seconds"],
            "dfir_mcp_tool_latency_seconds": data["dfir_mcp_tool_latency_seconds"],
            "dfir_llm_latency_seconds": data["dfir_llm_latency_seconds"],
            "dfir_human_approval_latency_seconds": data["dfir_human_approval_latency_seconds"],
            "dfir_ioc_generation_count": data["dfir_ioc_generation_count"],
            "dfir_affected_invoice_count": data["dfir_affected_invoice_count"],
            "dfir_patient_zero_confidence": data["dfir_patient_zero_confidence"],
            "dfir_forensic_correlation_score": data["dfir_forensic_correlation_score"],
            "dfir_bigquery_readiness": data["dfir_bigquery_readiness"],
        }

        help_text = {
            "dfir_scored_ips": "Total number of scored IPs.",
            "dfir_idor_findings": "Total number of IDOR findings.",
            "dfir_anomalous_ips": "Total number of anomalous IPs.",
            "dfir_agent_decisions": "Total number of agent decisions.",
            "dfir_platform_health": "Platform health flag.",
            "dfir_incident_critical": "Critical severity flag.",
            "dfir_evaluation_score": "Agent evaluation score.",
            "dfir_approval_rate": "Human approval rate.",
            "dfir_containment_actions": "Total containment actions.",
            "dfir_mean_response_time_seconds": "Mean response time in seconds.",
            "dfir_llm_calls": "Total LLM calls.",
            "dfir_deterministic_calls": "Total deterministic calls.",
            "dfir_fallback_calls": "Total fallback calls.",
            "dfir_rag_hit_rate": "RAG hit rate.",
            "dfir_professional_answer_rate": "Professional answer rate.",
            "dfir_sli_detection_success_rate": "Detection success SLI.",
            "dfir_sli_evidence_completeness": "Evidence completeness SLI.",
            "dfir_sli_containment_readiness": "Containment readiness SLI.",
            "dfir_slo_detection_target": "Detection SLO target.",
            "dfir_slo_response_target": "Response SLO target.",
            "dfir_agent_latency_seconds": "Agent latency in seconds.",
            "dfir_rag_latency_seconds": "RAG latency in seconds.",
            "dfir_mcp_tool_latency_seconds": "MCP tool latency in seconds.",
            "dfir_llm_latency_seconds": "LLM latency in seconds.",
            "dfir_human_approval_latency_seconds": "Human approval latency in seconds.",
            "dfir_ioc_generation_count": "Generated IOC count.",
            "dfir_affected_invoice_count": "Affected invoice count.",
            "dfir_patient_zero_confidence": "Patient zero confidence score.",
            "dfir_forensic_correlation_score": "Forensic correlation score.",
            "dfir_bigquery_readiness": "BigQuery readiness flag.",
        }

        lines = []

        for metric_name, metric_value in prometheus_metrics.items():
            lines.extend(
                [
                    f"# HELP {metric_name} {help_text[metric_name]}",
                    f"# TYPE {metric_name} gauge",
                    f"{metric_name} {metric_value}",
                ]
            )

        return "\n".join(lines) + "\n"