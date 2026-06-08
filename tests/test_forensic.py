import polars as pl

from src.forensic.timeline import (
    build_attack_timeline,
)

from src.forensic.ioc_generator import (
    generate_iocs,
)

from src.forensic.evidence_builder import (
    build_forensic_evidence,
)


def sample_events() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "timestamp": [
                "2020-12-31T00:00:00",
                "2020-12-31T01:00:00",
                "2020-12-31T02:00:00",
            ],
            "status_code": [
                200,
                200,
                403,
            ],
            "host": [
                "mercadolibre.com",
                "mercadolibre.com",
                "mercadolibre.com",
            ],
            "method": [
                "GET",
                "GET",
                "GET",
            ],
            "source_ip": [
                "1.1.1.1",
                "1.1.1.1",
                "2.2.2.2",
            ],
            "user_agent": [
                "BotUA",
                "BotUA",
                "NormalUA",
            ],
            "invoice_id": [
                100,
                101,
                999,
            ],
            "site_id": [
                "MeliBR",
                "MeliBR",
                "MeliAR",
            ],
            "auth_token": [
                "TOKEN1",
                "TOKEN1",
                "TOKEN2",
            ],
        }
    )


def sample_suspicious_ips() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "ip": [
                "1.1.1.1",
            ],
            "risk_score": [
                90.0,
            ],
            "risk_level": [
                "critical",
            ],
            "is_idor_suspect": [
                True,
            ],
            "is_likely_bot": [
                True,
            ],
            "sequential_access_ratio": [
                1.0,
            ],
            "unique_invoice_ids": [
                2,
            ],
            "total_requests": [
                2,
            ],
        }
    )


def sample_idor_findings() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "ip": [
                "1.1.1.1",
            ],
            "sequential_access_ratio": [
                1.0,
            ],
            "unique_invoice_ids": [
                2,
            ],
            "invoice_span": [
                1,
            ],
            "min_invoice_id": [
                100,
            ],
            "max_invoice_id": [
                101,
            ],
            "idor_severity": [
                "critical",
            ],
            "idor_evidence": [
                "Sequential invoice enumeration pattern.",
            ],
        }
    )


def sample_anomalous_ips() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "ip": [
                "1.1.1.1",
            ],
            "anomaly_score": [
                99.0,
            ],
            "anomaly_level": [
                "critical",
            ],
            "risk_score": [
                90.0,
            ],
            "risk_level": [
                "critical",
            ],
        }
    )


def sample_anomaly_scores() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "ip": [
                "1.1.1.1",
            ],
            "anomaly_score": [
                99.0,
            ],
            "anomaly_level": [
                "critical",
            ],
            "is_anomalous": [
                True,
            ],
        }
    )


def test_build_attack_timeline():
    timeline = build_attack_timeline(
        parsed_events=sample_events(),
        suspicious_ips=sample_suspicious_ips(),
    )

    assert timeline["timeline_type"] == "attack_timeline"
    assert timeline["summary"]["total_attack_events"] == 2
    assert len(timeline["attacker_timelines"]) == 1


def test_generate_iocs():
    iocs = generate_iocs(
        parsed_events=sample_events(),
        suspicious_ips=sample_suspicious_ips(),
        idor_findings=sample_idor_findings(),
        anomalous_ips=sample_anomalous_ips(),
    )

    assert iocs["ioc_type"] == "idor_investigation_iocs"
    assert iocs["summary"]["total_suspicious_ips"] == 1
    assert len(iocs["ip_indicators"]) == 1


def test_build_forensic_evidence():
    timeline = build_attack_timeline(
        parsed_events=sample_events(),
        suspicious_ips=sample_suspicious_ips(),
    )

    iocs = generate_iocs(
        parsed_events=sample_events(),
        suspicious_ips=sample_suspicious_ips(),
        idor_findings=sample_idor_findings(),
        anomalous_ips=sample_anomalous_ips(),
    )

    evidence = build_forensic_evidence(
        chain_of_custody={
            "sha256": "abc123",
        },
        attack_timeline=timeline,
        iocs=iocs,
        risk_scores=sample_suspicious_ips(),
        idor_findings=sample_idor_findings(),
        anomaly_scores=sample_anomaly_scores(),
    )

    assert evidence["evidence_type"] == "forensic_evidence_package"
    assert evidence["summary"]["total_scored_ips"] == 1
    assert len(evidence["top_attackers"]) == 1