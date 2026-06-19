from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class PromqlQuery:
    name: str
    query: str
    description: str
    audience: str


def build_promql_catalog() -> list[dict]:
    queries = [
        PromqlQuery("Scored IPs", "dfir_scored_ips", "Total scored IPs.", "SOC"),
        PromqlQuery("IDOR Findings", "dfir_idor_findings", "Detected IDOR findings.", "DFIR"),
        PromqlQuery("Anomalous IPs", "dfir_anomalous_ips", "Suspicious anomalous IPs.", "SOC"),
        PromqlQuery("Agent Decisions", "dfir_agent_decisions", "Agent orchestration decisions.", "AI Engineering"),
        PromqlQuery("Detection SLI", "dfir_sli_detection_success_rate", "Detection success SLI.", "Leadership"),
        PromqlQuery("Evidence Completeness", "dfir_sli_evidence_completeness", "Forensic evidence completeness.", "DFIR"),
        PromqlQuery("RAG Hit Rate", "dfir_rag_hit_rate", "RAG retrieval success rate.", "AI Engineering"),
        PromqlQuery("LLM Latency", "dfir_llm_latency_seconds", "LLM response latency.", "AI Engineering"),
        PromqlQuery("Human Approval Latency", "dfir_human_approval_latency_seconds", "Human approval loop latency.", "SOC"),
        PromqlQuery("Forensic Correlation", "dfir_forensic_correlation_score", "Correlation between DFIR, evidence and metrics.", "Leadership"),
    ]
    return [asdict(query) for query in queries]