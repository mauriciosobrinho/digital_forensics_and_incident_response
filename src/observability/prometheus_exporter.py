from src.observability.metrics_registry import ObservabilityMetrics


class PrometheusExporter:
    def render(self, metrics: ObservabilityMetrics) -> str:
        data = metrics.to_dict()

        health_value = 1 if data["platform_health"] == "healthy" else 0
        critical_value = 1 if data["severity"] == "critical" else 0

        lines = [
            "# HELP dfir_scored_ips Total number of scored IPs.",
            "# TYPE dfir_scored_ips gauge",
            f"dfir_scored_ips {data['scored_ips']}",
            "# HELP dfir_idor_findings Total number of IDOR findings.",
            "# TYPE dfir_idor_findings gauge",
            f"dfir_idor_findings {data['idor_findings']}",
            "# HELP dfir_anomalous_ips Total number of anomalous IPs.",
            "# TYPE dfir_anomalous_ips gauge",
            f"dfir_anomalous_ips {data['anomalous_ips']}",
            "# HELP dfir_agent_decisions Total number of agent decisions.",
            "# TYPE dfir_agent_decisions gauge",
            f"dfir_agent_decisions {data['agent_decisions']}",
            "# HELP dfir_platform_health Platform health flag.",
            "# TYPE dfir_platform_health gauge",
            f"dfir_platform_health {health_value}",
            "# HELP dfir_incident_critical Critical severity flag.",
            "# TYPE dfir_incident_critical gauge",
            f"dfir_incident_critical {critical_value}",
            "# HELP dfir_evaluation_score Agent evaluation score.",
            "# TYPE dfir_evaluation_score gauge",
            f"dfir_evaluation_score {data['evaluation_score']}",
            "# HELP dfir_approval_rate Human approval rate.",
            "# TYPE dfir_approval_rate gauge",
            f"dfir_approval_rate {data['approval_rate']}",
            "# HELP dfir_containment_actions Total containment actions.",
            "# TYPE dfir_containment_actions gauge",
            f"dfir_containment_actions {data['containment_actions']}",
            "# HELP dfir_mean_response_time_seconds Mean response time in seconds.",
            "# TYPE dfir_mean_response_time_seconds gauge",
            f"dfir_mean_response_time_seconds {data['mean_response_time_seconds']}",
            "# HELP dfir_llm_calls Total LLM calls.",
            "# TYPE dfir_llm_calls gauge",
            f"dfir_llm_calls {data['llm_calls']}",
            "# HELP dfir_deterministic_calls Total deterministic calls.",
            "# TYPE dfir_deterministic_calls gauge",
            f"dfir_deterministic_calls {data['deterministic_calls']}",
            "# HELP dfir_fallback_calls Total fallback calls.",
            "# TYPE dfir_fallback_calls gauge",
            f"dfir_fallback_calls {data['fallback_calls']}",
            "# HELP dfir_rag_hit_rate RAG hit rate.",
            "# TYPE dfir_rag_hit_rate gauge",
            f"dfir_rag_hit_rate {data['rag_hit_rate']}",
            "# HELP dfir_professional_answer_rate Professional answer rate.",
            "# TYPE dfir_professional_answer_rate gauge",
            f"dfir_professional_answer_rate {data['professional_answer_rate']}",
        ]

        return "\n".join(lines) + "\n"