from src.config.settings import (
    INPUT_CSV,
    PARSED_EVENTS_FILE,
    CHAIN_OF_CUSTODY_FILE,
    IP_FEATURES_FILE,
)

from src.utils.filesystem import (
    ensure_project_directories,
)

from src.ingestion.loader import (
    load_logs,
)

from src.ingestion.integrity import (
    generate_chain_of_custody,
)

from src.parsing.uri_parser import (
    extract_uri_fields,
    persist_parsed_events,
)

from src.features.feature_builder import (
    build_ip_features,
    save_ip_features,
)


def run_pipeline() -> None:

    print("\n[1/7] Creating directories...")
    ensure_project_directories()

    print("[2/7] Generating chain of custody...")
    generate_chain_of_custody(
        INPUT_CSV,
        CHAIN_OF_CUSTODY_FILE,
    )

    print("[3/7] Loading CSV...")
    logs = load_logs(INPUT_CSV)

    print("[4/7] Parsing events...")
    parsed_events = extract_uri_fields(logs)

    print("[5/7] Persisting parsed_events.parquet...")
    persist_parsed_events(
        parsed_events,
        PARSED_EVENTS_FILE,
    )

    print("[6/7] Building IP features...")
    ip_features = build_ip_features(
        parsed_events
    )

    print("[7/7] Persisting ip_features.parquet...")
    save_ip_features(
        ip_features,
        IP_FEATURES_FILE,
    )

    print("\nPipeline completed successfully.")
    print(f"Parsed events : {PARSED_EVENTS_FILE}")
    print(f"IP features   : {IP_FEATURES_FILE}")
    print(f"Evidence file : {CHAIN_OF_CUSTODY_FILE}")


if __name__ == "__main__":
    run_pipeline()