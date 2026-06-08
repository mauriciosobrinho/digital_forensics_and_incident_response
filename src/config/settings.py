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