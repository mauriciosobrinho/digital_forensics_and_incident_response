import polars as pl

from src.config.settings import (
    INPUT_CSV,
    PARSED_EVENTS_FILE,
    CHAIN_OF_CUSTODY_FILE,
    IP_FEATURES_FILE,
    SUSPICIOUS_IPS_FILE,
    IDOR_FINDINGS_FILE,
    RISK_SCORES_FILE,
    ANOMALY_SCORES_FILE,
    ANOMALOUS_IPS_FILE,
    ATTACK_TIMELINE_FILE,
    IOCS_FILE,
    FORENSIC_EVIDENCE_FILE,
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

from src.detection.anomaly_detector import (
    detect_anomalies,
    build_anomalous_ips,
    save_anomaly_scores,
    save_anomalous_ips,
)

from src.forensic.timeline import (
    build_attack_timeline,
    save_attack_timeline,
)

from src.forensic.ioc_generator import (
    generate_iocs,
    save_iocs,
)

from src.forensic.evidence_builder import (
    build_forensic_evidence,
    load_chain_of_custody,
    save_forensic_evidence,
)


def run_pipeline() -> None:

    print("\n[1/17] Creating directories...")
    ensure_project_directories()

    print("[2/17] Generating chain of custody...")
    generate_chain_of_custody(
        INPUT_CSV,
        CHAIN_OF_CUSTODY_FILE,
    )

    print("[3/17] Loading CSV...")
    logs = load_logs(INPUT_CSV)

    print("[4/17] Parsing events...")
    parsed_events = extract_uri_fields(logs)

    print("[5/17] Persisting parsed_events.parquet...")
    persist_parsed_events(
        parsed_events,
        PARSED_EVENTS_FILE,
    )

    print("[6/17] Building IP features...")
    parsed_events_for_features = pl.scan_parquet(
        PARSED_EVENTS_FILE
    )

    ip_features = build_ip_features(
        parsed_events_for_features
    )

    print("[7/17] Persisting ip_features.parquet...")
    save_ip_features(
        ip_features,
        IP_FEATURES_FILE,
    )

    print("[8/17] Detecting IDOR findings...")
    idor_findings = detect_idor_findings(
        ip_features
    )

    print("[9/17] Detecting bot signals...")
    bot_signals = detect_bot_signals(
        ip_features
    )

    print("[10/17] Building risk scores...")
    risk_scores = build_risk_scores(
        ip_features=ip_features,
        bot_signals=bot_signals,
        idor_findings=idor_findings,
    )

    suspicious_ips = build_suspicious_ips(
        risk_scores
    )

    print("[11/17] Persisting detection outputs...")
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

    print("[12/17] Detecting anomalies...")
    anomaly_scores = detect_anomalies(
        risk_scores
    )

    anomalous_ips = build_anomalous_ips(
        anomaly_scores
    )

    print("[13/17] Persisting anomaly outputs...")
    save_anomaly_scores(
        anomaly_scores,
        ANOMALY_SCORES_FILE,
    )

    save_anomalous_ips(
        anomalous_ips,
        ANOMALOUS_IPS_FILE,
    )

    print("[14/17] Building attack timeline...")
    parsed_events_df = pl.read_parquet(
        PARSED_EVENTS_FILE
    )

    attack_timeline = build_attack_timeline(
        parsed_events=parsed_events_df,
        suspicious_ips=suspicious_ips,
    )

    save_attack_timeline(
        attack_timeline,
        ATTACK_TIMELINE_FILE,
    )

    print("[15/17] Generating IOCs...")
    iocs = generate_iocs(
        parsed_events=parsed_events_df,
        suspicious_ips=suspicious_ips,
        idor_findings=idor_findings,
        anomalous_ips=anomalous_ips,
    )

    save_iocs(
        iocs,
        IOCS_FILE,
    )

    print("[16/17] Building forensic evidence package...")
    chain_of_custody = load_chain_of_custody(
        CHAIN_OF_CUSTODY_FILE
    )

    forensic_evidence = build_forensic_evidence(
        chain_of_custody=chain_of_custody,
        attack_timeline=attack_timeline,
        iocs=iocs,
        risk_scores=risk_scores,
        idor_findings=idor_findings,
        anomaly_scores=anomaly_scores,
    )

    print("[17/17] Persisting forensic evidence package...")
    save_forensic_evidence(
        forensic_evidence,
        FORENSIC_EVIDENCE_FILE,
    )

    print("\nPipeline completed successfully.")
    print(f"Parsed events   : {PARSED_EVENTS_FILE}")
    print(f"IP features     : {IP_FEATURES_FILE}")
    print(f"IDOR findings   : {IDOR_FINDINGS_FILE}")
    print(f"Risk scores     : {RISK_SCORES_FILE}")
    print(f"Suspicious IPs  : {SUSPICIOUS_IPS_FILE}")
    print(f"Evidence file   : {CHAIN_OF_CUSTODY_FILE}")
    print(f"Anomaly scores : {ANOMALY_SCORES_FILE}")
    print(f"Anomalous IPs  : {ANOMALOUS_IPS_FILE}")
    print(f"Attack timeline : {ATTACK_TIMELINE_FILE}")
    print(f"IOCs            : {IOCS_FILE}")
    print(f"Forensic package: {FORENSIC_EVIDENCE_FILE}")


if __name__ == "__main__":
    run_pipeline()