from pathlib import Path
import json
from datetime import datetime, timezone

import polars as pl


def build_forensic_evidence(
    chain_of_custody: dict,
    attack_timeline: dict,
    iocs: dict,
    risk_scores: pl.DataFrame,
    idor_findings: pl.DataFrame,
    anomaly_scores: pl.DataFrame,
    top_n: int = 20,
) -> dict:
    top_attackers = (
        risk_scores
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
        .to_dicts()
    )

    severity_distribution = (
        risk_scores
        .group_by("risk_level")
        .agg(
            pl.len().alias("count")
        )
        .sort("count", descending=True)
        .to_dicts()
    )

    anomaly_distribution = (
        anomaly_scores
        .group_by("anomaly_level")
        .agg(
            pl.len().alias("count")
        )
        .sort("count", descending=True)
        .to_dicts()
        if "anomaly_level" in anomaly_scores.columns
        else []
    )

    evidence = {
        "evidence_type": "forensic_evidence_package",
        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "case": {
            "incident_type": "Insecure Direct Object Reference",
            "scope": "Invoice access enumeration investigation",
            "objective": (
                "Transform raw logs, detections, risk scores and anomaly "
                "signals into structured forensic evidence."
            ),
        },
        "chain_of_custody": chain_of_custody,
        "summary": {
            "total_scored_ips": risk_scores.height,
            "total_idor_findings": idor_findings.height,
            "total_anomalous_ips": (
                anomaly_scores
                .filter(pl.col("is_anomalous"))
                .height
                if "is_anomalous" in anomaly_scores.columns
                else None
            ),
            "top_attackers_count": len(top_attackers),
        },
        "top_attackers": top_attackers,
        "severity_distribution": severity_distribution,
        "anomaly_distribution": anomaly_distribution,
        "attack_timeline": attack_timeline,
        "iocs": iocs,
        "investigative_conclusion": (
            "The evidence indicates automated invoice enumeration behavior "
            "consistent with potential IDOR exploitation. High-risk IPs show "
            "large invoice diversity, sequential access patterns, elevated "
            "risk scores and convergence with anomaly detection."
        ),
        "recommended_next_steps": [
            "Block or challenge top critical IPs after human approval.",
            "Apply dynamic rate limiting to invoice search endpoints.",
            "Review authorization checks for invoice ownership.",
            "Revoke or rotate exposed suspicious tokens.",
            "Create WAF rules for detected enumeration patterns.",
            "Continue monitoring anomalous IP behavior.",
        ],
    }

    return evidence


def load_chain_of_custody(
    chain_file: Path,
) -> dict:
    if not chain_file.exists():
        return {}

    with chain_file.open(
        "r",
        encoding="utf-8",
    ) as f:
        return json.load(f)


def save_forensic_evidence(
    evidence: dict,
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
            evidence,
            f,
            indent=2,
            ensure_ascii=False,
        )