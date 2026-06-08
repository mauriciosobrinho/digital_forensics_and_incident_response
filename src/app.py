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
    AGENT_INVESTIGATION_FILE,
    AGENT_DECISION_LOG_FILE,
    AGENT_RESPONSE_PLAYBOOK_FILE,
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

from src.agents.runner import (
    run_agent_investigation,
)


def run_pipeline() -> None:

    print("\n[1/19] Creating directories...")
    ensure_project_directories()

    print("[2/19] Generating chain of custody...")
    generate_chain_of_custody(
        INPUT_CSV,
        CHAIN_OF_CUSTODY_FILE,
    )

    print("[3/19] Loading CSV...")
    logs = load_logs(INPUT_CSV)

    print("[4/19] Parsing events...")

    if PARSED_EVENTS_FILE.exists():

        print(f"      Reusing existing parsed events: {PARSED_EVENTS_FILE}")

    else:

        parsed_events = extract_uri_fields(logs)

        print("[5/19] Persisting parsed_events.parquet...")
        persist_parsed_events(
            parsed_events,
            PARSED_EVENTS_FILE,
        )

    print("[6/19] Building IP features...")

    if IP_FEATURES_FILE.exists():

        print(f"      Reusing existing IP features: {IP_FEATURES_FILE}")
        ip_features = pl.read_parquet(
            IP_FEATURES_FILE
        )

    else:

        parsed_events_for_features = pl.scan_parquet(
            PARSED_EVENTS_FILE
        )

        ip_features = build_ip_features(
            parsed_events_for_features
        )

        print("[7/19] Persisting ip_features.parquet...")
        save_ip_features(
            ip_features,
            IP_FEATURES_FILE,
        )

    if RISK_SCORES_FILE.exists():

        print(
            f"Reusing existing risk scores: {RISK_SCORES_FILE}"
        )

        risk_scores = pl.read_parquet(
            RISK_SCORES_FILE
        )

        idor_findings = pl.read_parquet(
            IDOR_FINDINGS_FILE
        )

        suspicious_ips = pl.read_parquet(
            SUSPICIOUS_IPS_FILE
        )

    else:

        print("[8/19] Detecting IDOR findings...")
        idor_findings = detect_idor_findings(
            ip_features
        )

        print("[9/19] Detecting bot signals...")
        bot_signals = detect_bot_signals(
            ip_features
        )

        print("[10/19] Building risk scores...")
        risk_scores = build_risk_scores(
            ip_features=ip_features,
            bot_signals=bot_signals,
            idor_findings=idor_findings,
        )

        suspicious_ips = build_suspicious_ips(
            risk_scores
        )

        print("[11/19] Persisting detection outputs...")
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

    if ANOMALY_SCORES_FILE.exists():

        print(
            f"Reusing existing anomaly scores: {ANOMALY_SCORES_FILE}"
        )

        anomaly_scores = pl.read_parquet(
            ANOMALY_SCORES_FILE
        )

        anomalous_ips = pl.read_parquet(
            ANOMALOUS_IPS_FILE
        )

    else:

        print("[12/19] Detecting anomalies...")
        anomaly_scores = detect_anomalies(
            risk_scores
        )

        anomalous_ips = build_anomalous_ips(
            anomaly_scores
        )

        print("[13/19] Persisting anomaly outputs...")
        save_anomaly_scores(
            anomaly_scores,
            ANOMALY_SCORES_FILE,
        )

        save_anomalous_ips(
            anomalous_ips,
            ANOMALOUS_IPS_FILE,
        )

    if (
        ATTACK_TIMELINE_FILE.exists()
        and IOCS_FILE.exists()
        and FORENSIC_EVIDENCE_FILE.exists()):

        print(
            f"Reusing existing forensic evidence: {FORENSIC_EVIDENCE_FILE}"
        )

    else:

        print("[14/19] Building attack timeline...")
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

        print("[15/19] Generating IOCs...")
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

        print("[16/19] Building forensic evidence package...")
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

        print("[17/19] Persisting forensic evidence package...")
        save_forensic_evidence(
            forensic_evidence,
            FORENSIC_EVIDENCE_FILE,
        )

    print("[18/19] Running LangGraph investigation agents...")
    run_agent_investigation(
        dry_run=True,
        human_approval_status="pending",
    )

    print("[19/19] Persisting agent investigation outputs...")

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
    print(f"Agent investigation : {AGENT_INVESTIGATION_FILE}")
    print(f"Agent decision log  : {AGENT_DECISION_LOG_FILE}")
    print(f"Agent playbook      : {AGENT_RESPONSE_PLAYBOOK_FILE}")


if __name__ == "__main__":
    run_pipeline()