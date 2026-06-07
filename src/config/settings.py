from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"

RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
EVIDENCE_DIR = DATA_DIR / "evidence"

INPUT_CSV = RAW_DIR / "three_months.csv"

PARSED_EVENTS_FILE = PROCESSED_DIR / "parsed_events.parquet"

CHAIN_OF_CUSTODY_FILE = (
    EVIDENCE_DIR / "chain_of_custody.json"
)
