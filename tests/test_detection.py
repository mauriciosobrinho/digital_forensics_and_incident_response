import polars as pl

from src.detection.idor_detector import (
    detect_idor_findings,
)

from src.detection.bot_detector import (
    detect_bot_signals,
)

from src.detection.risk_scoring import (
    build_risk_scores,
    build_suspicious_ips,
)


def sample_ip_features() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "ip": [
                "10.0.0.1",
                "10.0.0.2",
            ],
            "total_requests": [
                5000,
                10,
            ],
            "unique_invoice_ids": [
                3000,
                3,
            ],
            "successful_requests": [
                4500,
                9,
            ],
            "failed_requests": [
                500,
                1,
            ],
            "success_rate": [
                0.90,
                0.90,
            ],
            "error_rate": [
                0.10,
                0.10,
            ],
            "unique_tokens": [
                2,
                1,
            ],
            "unique_user_agents": [
                1,
                2,
            ],
            "first_seen": [
                "2020-10-01",
                "2020-10-01",
            ],
            "last_seen": [
                "2020-10-02",
                "2020-10-02",
            ],
            "active_minutes": [
                1440.0,
                1440.0,
            ],
            "requests_per_minute": [
                3.47,
                0.006,
            ],
            "min_invoice_id": [
                1000,
                1000,
            ],
            "max_invoice_id": [
                5000,
                1003,
            ],
            "invoice_span": [
                4000,
                3,
            ],
            "sequential_access_ratio": [
                0.80,
                0.01,
            ],
        }
    )


def test_detect_idor_findings():
    features = sample_ip_features()

    findings = detect_idor_findings(
        features
    )

    assert findings.height == 1
    assert findings["ip"][0] == "10.0.0.1"
    assert findings["is_idor_suspect"][0] is True


def test_detect_bot_signals():
    features = sample_ip_features()

    bot_signals = detect_bot_signals(
        features
    )

    assert bot_signals.height == 2
    assert "bot_likelihood_score" in bot_signals.columns


def test_build_risk_scores():
    features = sample_ip_features()
    findings = detect_idor_findings(features)
    bot_signals = detect_bot_signals(features)

    risk_scores = build_risk_scores(
        ip_features=features,
        bot_signals=bot_signals,
        idor_findings=findings,
    )

    assert risk_scores.height == 2
    assert "risk_score" in risk_scores.columns
    assert "risk_level" in risk_scores.columns


def test_build_suspicious_ips():
    features = sample_ip_features()
    findings = detect_idor_findings(features)
    bot_signals = detect_bot_signals(features)

    risk_scores = build_risk_scores(
        ip_features=features,
        bot_signals=bot_signals,
        idor_findings=findings,
    )

    suspicious_ips = build_suspicious_ips(
        risk_scores
    )

    assert suspicious_ips.height >= 1