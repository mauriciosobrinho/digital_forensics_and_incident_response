from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import polars as pl


def _safe_parquet_height(path: Path) -> int:
    if not path.exists():
        return 0

    try:
        return pl.scan_parquet(path).select(
            pl.len()
        ).collect().item()
    except Exception:
        return 0


def _safe_json_len(
    data: Any,
    key: str | None = None,
) -> int:
    if key and isinstance(data, dict):
        value = data.get(key, [])
    else:
        value = data

    if isinstance(value, list):
        return len(value)

    if isinstance(value, dict):
        return len(value)

    return 0


def build_platform_metrics(
    *,
    paths: dict[str, Path],
    forensic_evidence: dict[str, Any],
    iocs: dict[str, Any],
) -> dict[str, Any]:

    parsed_events = _safe_parquet_height(
        paths["parsed_events"]
    )

    ip_features = _safe_parquet_height(
        paths["ip_features"]
    )

    idor_findings = _safe_parquet_height(
        paths["idor_findings"]
    )

    anomaly_scores = _safe_parquet_height(
        paths["anomaly_scores"]
    )

    anomalous_ips = _safe_parquet_height(
        paths["anomalous_ips"]
    )

    summary = forensic_evidence.get(
        "summary",
        {},
    )

    ioc_summary = iocs.get(
        "summary",
        {},
    )

    n_iocs_generated = sum(
        value
        for value in ioc_summary.values()
        if isinstance(value, int)
    )

    return {
        "metrics_type": "platform_metrics",
        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "pipeline_metrics": {
            "n_logs_processed": parsed_events,
            "n_ips_analyzed": ip_features,
            "n_idor_findings": idor_findings,
            "n_anomaly_scores": anomaly_scores,
            "n_anomalous_ips": anomalous_ips,
            "n_iocs_generated": n_iocs_generated,
        },
        "forensic_summary": summary,
        "ioc_summary": ioc_summary,
        "status": "healthy"
        if parsed_events > 0 and ip_features > 0
        else "degraded",
    }