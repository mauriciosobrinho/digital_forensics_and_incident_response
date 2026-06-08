from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"

RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
EVIDENCE_DIR = DATA_DIR / "evidence"

INPUT_CSV = RAW_DIR / "three_months.csv"

PARSED_EVENTS_FILE = (
    PROCESSED_DIR / "parsed_events.parquet"
)

CHAIN_OF_CUSTODY_FILE = (
    EVIDENCE_DIR / "chain_of_custody.json"
)

# Sprint 1.2
IP_FEATURES_FILE = (
    PROCESSED_DIR / "ip_features.parquet"
)

# Sprint 2.1
SUSPICIOUS_IPS_FILE = (
    PROCESSED_DIR / "suspicious_ips.parquet"
)

IDOR_FINDINGS_FILE = (
    PROCESSED_DIR / "idor_findings.parquet"
)

RISK_SCORES_FILE = (
    PROCESSED_DIR / "risk_scores.parquet"
)

# Sprint 2.2
ANOMALY_SCORES_FILE = (
    PROCESSED_DIR / "anomaly_scores.parquet"
)

ANOMALOUS_IPS_FILE = (
    PROCESSED_DIR / "anomalous_ips.parquet"
)

# Sprint 2.3
ATTACK_TIMELINE_FILE = (
    EVIDENCE_DIR / "attack_timeline.json"
)

IOCS_FILE = (
    EVIDENCE_DIR / "iocs.json"
)

FORENSIC_EVIDENCE_FILE = (
    EVIDENCE_DIR / "forensic_evidence.json"
)

# Sprint 3.1
AGENT_INVESTIGATION_FILE = (
    EVIDENCE_DIR / "agent_investigation.json"
)

AGENT_DECISION_LOG_FILE = (
    EVIDENCE_DIR / "agent_decision_log.json"
)

AGENT_RESPONSE_PLAYBOOK_FILE = (
    EVIDENCE_DIR / "agent_response_playbook.json"
)

# Sprint 3.2
HUMAN_APPROVAL_REQUEST_FILE = (
    EVIDENCE_DIR / "human_approval_request.json"
)

HUMAN_APPROVAL_DECISION_FILE = (
    EVIDENCE_DIR / "human_approval_decision.json"
)

LLM_AGENT_REASONING_FILE = (
    EVIDENCE_DIR / "llm_agent_reasoning.json"
)

TOOL_EXECUTION_LOG_FILE = (
    EVIDENCE_DIR / "tool_execution_log.json"
)

MEMORY_DIR = DATA_DIR / "memory"

INVESTIGATION_MEMORY_FILE = (
    MEMORY_DIR / "investigation_memory.json"
)