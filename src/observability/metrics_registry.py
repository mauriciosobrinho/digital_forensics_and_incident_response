from dataclasses import dataclass, asdict


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

    def to_dict(self) -> dict:
        return asdict(self)