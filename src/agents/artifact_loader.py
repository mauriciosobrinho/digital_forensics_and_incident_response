import json
from pathlib import Path
from typing import Any

import polars as pl


def load_json_file(
    file_path: Path,
) -> dict[str, Any]:
    if not file_path.exists():
        raise FileNotFoundError(
            f"Required evidence file not found: {file_path}"
        )

    with file_path.open(
        "r",
        encoding="utf-8",
    ) as f:
        return json.load(f)


def build_risk_summary(
    risk_scores_file: Path,
    top_n: int = 20,
) -> dict[str, Any]:
    risk_scores = pl.read_parquet(
        risk_scores_file
    )

    top_risk = (
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

    distribution = (
        risk_scores
        .group_by("risk_level")
        .agg(
            pl.len().alias("count")
        )
        .sort("count", descending=True)
        .to_dicts()
    )

    return {
        "total_ips": risk_scores.height,
        "top_risk_ips": top_risk,
        "risk_level_distribution": distribution,
    }


def build_anomaly_summary(
    anomaly_scores_file: Path,
    top_n: int = 20,
) -> dict[str, Any]:
    anomaly_scores = pl.read_parquet(
        anomaly_scores_file
    )

    top_anomalies = (
        anomaly_scores
        .sort("anomaly_score", descending=True)
        .select(
            [
                "ip",
                "anomaly_score",
                "anomaly_level",
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

    total_anomalous = (
        anomaly_scores
        .filter(
            pl.col("is_anomalous")
        )
        .height
    )

    return {
        "total_ips": anomaly_scores.height,
        "total_anomalous_ips": total_anomalous,
        "top_anomalies": top_anomalies,
    }