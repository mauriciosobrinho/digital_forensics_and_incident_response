from src.config.settings import (
    INPUT_CSV,
    PARSED_EVENTS_FILE,
    CHAIN_OF_CUSTODY_FILE,
    IP_FEATURES_FILE,
    SUSPICIOUS_IPS_FILE,
    IDOR_FINDINGS_FILE,
    RISK_SCORES_FILE,
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

from src.detection.idor_detector import (
    detect_idor_findings,
    save_idor_findings,
)

from src.detection.bot_detector import (
    detect_bot_signals,
)

from src.detection.risk_scoring import (
    build_risk_scores,
    build_suspicious_ips,
    save_risk_scores,
    save_suspicious_ips,
)


def run_pipeline() -> None:

    print("\n[1/11] Creating directories...")
    ensure_project_directories()

    print("[2/11] Generating chain of custody...")
    generate_chain_of_custody(
        INPUT_CSV,
        CHAIN_OF_CUSTODY_FILE,
    )

    print("[3/11] Loading CSV...")
    logs = load_logs(INPUT_CSV)

    print("[4/11] Parsing events...")
    parsed_events = extract_uri_fields(logs)

    print("[5/11] Persisting parsed_events.parquet...")
    persist_parsed_events(
        parsed_events,
        PARSED_EVENTS_FILE,
    )

    print("[6/11] Building IP features...")
    ip_features = build_ip_features(
        parsed_events
    )

    print("[7/11] Persisting ip_features.parquet...")
    save_ip_features(
        ip_features,
        IP_FEATURES_FILE,
    )

    print("[8/11] Detecting IDOR findings...")
    idor_findings = detect_idor_findings(
        ip_features
    )

    print("[9/11] Detecting bot signals...")
    bot_signals = detect_bot_signals(
        ip_features
    )

    print("[10/11] Building risk scores...")
    risk_scores = build_risk_scores(
        ip_features=ip_features,
        bot_signals=bot_signals,
        idor_findings=idor_findings,
    )

    suspicious_ips = build_suspicious_ips(
        risk_scores
    )

    print("[11/11] Persisting detection outputs...")
    save_idor_findings(
        idor_findings,
        IDOR_FINDINGS_FILE,
    )

    save_risk_scores(
        risk_scores,
        RISK_SCORES_FILE,
    )

    save_suspicious_ips(
        suspicious_ips,
        SUSPICIOUS_IPS_FILE,
    )

    print("\nPipeline completed successfully.")
    print(f"Parsed events   : {PARSED_EVENTS_FILE}")
    print(f"IP features     : {IP_FEATURES_FILE}")
    print(f"IDOR findings   : {IDOR_FINDINGS_FILE}")
    print(f"Risk scores     : {RISK_SCORES_FILE}")
    print(f"Suspicious IPs  : {SUSPICIOUS_IPS_FILE}")
    print(f"Evidence file   : {CHAIN_OF_CUSTODY_FILE}")


if __name__ == "__main__":
    run_pipeline()