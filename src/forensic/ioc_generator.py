from pathlib import Path
import json

import polars as pl


def generate_iocs(
    parsed_events: pl.DataFrame,
    suspicious_ips: pl.DataFrame,
    idor_findings: pl.DataFrame,
    anomalous_ips: pl.DataFrame,
    top_n: int = 50,
) -> dict:
    top_suspicious_ips = (
        suspicious_ips
        .sort("risk_score", descending=True)
        .select(
            [
                "ip",
                "risk_score",
                "risk_level",
                "is_idor_suspect",
                "is_likely_bot",
                "sequential_access_ratio",
                "unique_invoice_ids",
                "total_requests",
            ]
        )
        .head(top_n)
    )

    ip_list = (
        top_suspicious_ips
        .select("ip")
        .to_series()
        .to_list()
    )

    suspicious_events = (
        parsed_events
        .filter(
            pl.col("source_ip").is_in(ip_list)
        )
    )

    user_agents = (
        suspicious_events
        .group_by("user_agent")
        .agg(
            [
                pl.len().alias("requests"),
                pl.col("source_ip").n_unique().alias("unique_ips"),
            ]
        )
        .sort("requests", descending=True)
        .head(top_n)
    )

    enumeration_patterns = (
        idor_findings
        .sort("sequential_access_ratio", descending=True)
        .select(
            [
                "ip",
                "sequential_access_ratio",
                "unique_invoice_ids",
                "invoice_span",
                "min_invoice_id",
                "max_invoice_id",
                "idor_severity",
                "idor_evidence",
            ]
        )
        .head(top_n)
    )

    anomalous = (
        anomalous_ips
        .sort("anomaly_score", descending=True)
        .select(
            [
                "ip",
                "anomaly_score",
                "anomaly_level",
                "risk_score",
                "risk_level",
            ]
        )
        .head(top_n)
        if anomalous_ips.height > 0
        else pl.DataFrame()
    )

    return {
        "ioc_type": "idor_investigation_iocs",
        "summary": {
            "total_suspicious_ips": suspicious_ips.height,
            "total_idor_findings": idor_findings.height,
            "total_anomalous_ips": anomalous_ips.height,
            "top_n": top_n,
        },
        "ip_indicators": top_suspicious_ips.to_dicts(),
        "user_agent_indicators": user_agents.to_dicts(),
        "enumeration_patterns": enumeration_patterns.to_dicts(),
        "anomaly_indicators": anomalous.to_dicts(),
    }


def save_iocs(
    iocs: dict,
    output_file: Path,
) -> None:
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_file.open(
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            iocs,
            f,
            indent=2,
            ensure_ascii=False,
        )