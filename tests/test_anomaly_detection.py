import polars as pl

from src.detection.anomaly_detector import (
    detect_anomalies,
    build_anomalous_ips,
)


def test_detect_anomalies():

    normal_rows = []

    for i in range(30):
        normal_rows.append(
            {
                "ip": f"10.0.0.{i}",
                "total_requests": 20,
                "unique_invoice_ids": 5,
                "success_rate": 0.90,
                "error_rate": 0.10,
                "unique_tokens": 1,
                "unique_user_agents": 2,
                "requests_per_minute": 0.01,
                "invoice_span": 10,
                "sequential_access_ratio": 0.02,
                "risk_score": 5.0,
                "risk_level": "low",
                "is_idor_suspect": False,
                "is_likely_bot": False,
            }
        )

    outlier = {
        "ip": "200.200.200.200",
        "total_requests": 15000,
        "unique_invoice_ids": 7000,
        "success_rate": 0.95,
        "error_rate": 0.05,
        "unique_tokens": 2,
        "unique_user_agents": 1,
        "requests_per_minute": 0.12,
        "invoice_span": 111111999,
        "sequential_access_ratio": 0.70,
        "risk_score": 90.0,
        "risk_level": "critical",
        "is_idor_suspect": True,
        "is_likely_bot": True,
    }

    df = pl.DataFrame(
        [*normal_rows, outlier]
    )

    anomaly_scores = detect_anomalies(
        df,
        contamination=0.05,
    )

    anomalous_ips = build_anomalous_ips(
        anomaly_scores
    )

    assert anomaly_scores.height == 31
    assert "anomaly_score" in anomaly_scores.columns
    assert "is_anomalous" in anomaly_scores.columns
    assert anomalous_ips.height >= 1

    assert (
        anomalous_ips
        .filter(
            pl.col("ip") == "200.200.200.200"
        )
        .height
        == 1
    )