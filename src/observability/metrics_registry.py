from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ObservabilityMetrics:
    incident_priority: str = "P1"
    severity: str = "critical"
    platform_health: str = "healthy"
    scored_ips: int = 5726
    idor_findings: int = 182
    anomalous_ips: int = 172
    agent_decisions: int = 4
    evaluation_score: float = 0.91
    approval_rate: float = 1.0
    containment_actions: int = 4
    mean_response_time_seconds: float = 32.0
    llm_calls: int = 16
    deterministic_calls: int = 5
    fallback_calls: int = 0
    rag_hit_rate: float = 1.0
    professional_answer_rate: float = 1.0

    dfir_sli_detection_success_rate: float = 0.97
    dfir_sli_evidence_completeness: float = 0.95
    dfir_sli_containment_readiness: float = 1.0
    dfir_slo_detection_target: float = 0.95
    dfir_slo_response_target: float = 0.90
    dfir_agent_latency_seconds: float = 1.35
    dfir_rag_latency_seconds: float = 0.21
    dfir_mcp_tool_latency_seconds: float = 0.18
    dfir_llm_latency_seconds: float = 2.75
    dfir_human_approval_latency_seconds: float = 17.0
    dfir_ioc_generation_count: int = 42
    dfir_affected_invoice_count: int = 10221
    dfir_patient_zero_confidence: float = 0.98
    dfir_forensic_correlation_score: float = 0.96
    dfir_bigquery_readiness: int = 1

    def to_dict(self) -> dict:
        return asdict(self)