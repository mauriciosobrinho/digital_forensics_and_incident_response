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
    HUMAN_APPROVAL_REQUEST_FILE,
    HUMAN_APPROVAL_DECISION_FILE,
    LLM_AGENT_REASONING_FILE,
    TOOL_EXECUTION_LOG_FILE,
    INVESTIGATION_MEMORY_FILE,
    LANGGRAPH_WORKFLOW_FILE,
    LANGGRAPH_WORKFLOW_MERMAID_FILE,
    AGENT_QUESTION_BANK_FILE,
    AGENT_EVAL_RESULTS_FILE,
    AGENT_EVAL_REPORT_FILE,
    AGENT_EVAL_SUMMARY_FILE,
    NIST_INCIDENT_REPORT_FILE,
    RESPONSE_METRICS_FILE,
    CONTAINMENT_STRATEGY_FILE,
    ROOT_CAUSE_ANALYSIS_FILE,
)

from src.agents.export_graph import (
    export_langgraph_workflow,
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

from src.evaluation.runner import (
    run_agent_evaluation,
)

from src.ir.runner import (
    run_nist_incident_response,
)


def run_pipeline() -> None:

    print("\n[1/22] Creating directories...")
    ensure_project_directories()

    print("[2/22] Generating chain of custody...")
    generate_chain_of_custody(
        INPUT_CSV,
        CHAIN_OF_CUSTODY_FILE,
    )

    print("[3/22] Loading CSV...")
    logs = load_logs(INPUT_CSV)

    print("[4/22] Parsing events...")

    if PARSED_EVENTS_FILE.exists():

        print(f"      Reusing existing parsed events: {PARSED_EVENTS_FILE}")

    else:

        parsed_events = extract_uri_fields(logs)

        print("[5/22] Persisting parsed_events.parquet...")
        persist_parsed_events(
            parsed_events,
            PARSED_EVENTS_FILE,
        )

    print("[6/22] Building IP features...")

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

        print("[7/22] Persisting ip_features.parquet...")
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

        print("[8/22] Detecting IDOR findings...")
        idor_findings = detect_idor_findings(
            ip_features
        )

        print("[9/22] Detecting bot signals...")
        bot_signals = detect_bot_signals(
            ip_features
        )

        print("[10/22] Building risk scores...")
        risk_scores = build_risk_scores(
            ip_features=ip_features,
            bot_signals=bot_signals,
            idor_findings=idor_findings,
        )

        suspicious_ips = build_suspicious_ips(
            risk_scores
        )

        print("[11/22] Persisting detection outputs...")
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

        print("[12/22] Detecting anomalies...")
        anomaly_scores = detect_anomalies(
            risk_scores
        )

        anomalous_ips = build_anomalous_ips(
            anomaly_scores
        )

        print("[13/22] Persisting anomaly outputs...")
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

        print("[14/22] Building attack timeline...")
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

        print("[15/22] Generating IOCs...")
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

        print("[16/22] Building forensic evidence package...")
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

        print("[17/22] Persisting forensic evidence package...")
        save_forensic_evidence(
            forensic_evidence,
            FORENSIC_EVIDENCE_FILE,
        )

    print("[18/22] Running LangGraph investigation agents...")
    run_agent_investigation(
        dry_run=True,
        human_approval_status="pending",
    )

    print("[19/22] Persisting agent investigation outputs...")

    print("[20/22] Exporting LangGraph workflow visualization...")
    workflow_export = export_langgraph_workflow()

    if workflow_export["png_generated"]:
        print(
            f"LangGraph workflow PNG : {workflow_export['png_file']}"
        )
    else:
        print(
            "LangGraph workflow PNG rendering unavailable. "
            f"Mermaid artifact generated: {workflow_export['mermaid_file']}"
        )

    print("[21/22] Running agent evaluation suite...")
    evaluation_report = run_agent_evaluation()

    print(
        "Agent evaluation coverage : "
        f"{evaluation_report['summary']['overall_coverage_percent']}%"
    )

    print("[22/22] Running NIST incident response metrics...")
    nist_report = run_nist_incident_response()

    print(
        "NIST incident report : "
        f"{nist_report['incident_summary']['classification']}"
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
    print(f"Agent investigation : {AGENT_INVESTIGATION_FILE}")
    print(f"Agent decision log  : {AGENT_DECISION_LOG_FILE}")
    print(f"Agent playbook      : {AGENT_RESPONSE_PLAYBOOK_FILE}")
    print(f"Human approval request : {HUMAN_APPROVAL_REQUEST_FILE}")
    print(f"Human approval decision: {HUMAN_APPROVAL_DECISION_FILE}")
    print(f"LLM reasoning          : {LLM_AGENT_REASONING_FILE}")
    print(f"Tool execution log     : {TOOL_EXECUTION_LOG_FILE}")
    print(f"Investigation memory   : {INVESTIGATION_MEMORY_FILE}")
    print(f"LangGraph workflow PNG    : {LANGGRAPH_WORKFLOW_FILE}")
    print(f"LangGraph workflow Mermaid: {LANGGRAPH_WORKFLOW_MERMAID_FILE}")
    print(f"Agent question bank : {AGENT_QUESTION_BANK_FILE}")
    print(f"Agent eval results  : {AGENT_EVAL_RESULTS_FILE}")
    print(f"Agent eval report   : {AGENT_EVAL_REPORT_FILE}")
    print(f"Agent eval summary  : {AGENT_EVAL_SUMMARY_FILE}")
    print(f"NIST report          : {NIST_INCIDENT_REPORT_FILE}")
    print(f"Response metrics     : {RESPONSE_METRICS_FILE}")
    print(f"Containment strategy : {CONTAINMENT_STRATEGY_FILE}")
    print(f"Root cause analysis  : {ROOT_CAUSE_ANALYSIS_FILE}")


if __name__ == "__main__":
    run_pipeline()