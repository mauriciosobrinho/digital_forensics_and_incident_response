from pathlib import Path

from src.observability.enterprise.bigquery_readiness import build_bigquery_readiness_contract
from src.observability.enterprise.enterprise_observability_service import (
    build_enterprise_metrics,
    build_enterprise_observability_contract,
    build_enterprise_prometheus_text,
)
from src.observability.enterprise.forensic_correlation import build_forensic_correlation
from src.observability.enterprise.promql_catalog import build_promql_catalog
from src.observability.enterprise.sli_slo_registry import build_sli_slo_registry


def test_enterprise_metrics_contract():
    metrics = build_enterprise_metrics()

    expected = [
        "dfir_sli_detection_success_rate",
        "dfir_sli_evidence_completeness",
        "dfir_sli_containment_readiness",
        "dfir_slo_detection_target",
        "dfir_slo_response_target",
        "dfir_agent_latency_seconds",
        "dfir_rag_latency_seconds",
        "dfir_mcp_tool_latency_seconds",
        "dfir_llm_latency_seconds",
        "dfir_human_approval_latency_seconds",
        "dfir_ioc_generation_count",
        "dfir_affected_invoice_count",
        "dfir_patient_zero_confidence",
        "dfir_forensic_correlation_score",
        "dfir_bigquery_readiness",
    ]

    for metric in expected:
        assert metric in metrics


def test_enterprise_prometheus_text_contract():
    text = build_enterprise_prometheus_text()

    assert "dfir_sli_detection_success_rate" in text
    assert "dfir_forensic_correlation_score" in text
    assert "dfir_bigquery_readiness" in text


def test_enterprise_observability_contract():
    contract = build_enterprise_observability_contract()

    assert contract["service"] == "dfir-enterprise-observability"
    assert contract["sprint"] == "5.0"
    assert "metrics" in contract
    assert "promql_catalog" in contract
    assert "forensic_correlation" in contract
    assert "bigquery_readiness" in contract


def test_sli_slo_registry_contract():
    registry = build_sli_slo_registry()

    assert registry["sli_detection_success_rate"] >= 0.95
    assert registry["sli_evidence_completeness"] >= 0.90
    assert registry["slo_detection_target"] == 0.95


def test_promql_catalog_contract():
    catalog = build_promql_catalog()

    assert len(catalog) >= 8
    assert any(item["query"] == "dfir_scored_ips" for item in catalog)
    assert any(item["query"] == "dfir_forensic_correlation_score" for item in catalog)


def test_forensic_correlation_contract():
    correlation = build_forensic_correlation()

    assert correlation["patient_zero_ip"] == "204.210.158.207"
    assert correlation["affected_invoices"] == 10221
    assert correlation["forensic_correlation_score"] >= 0.90


def test_bigquery_readiness_contract():
    contract = build_bigquery_readiness_contract()

    assert contract["provider"] == "bigquery"
    assert contract["status"] == "ready_for_integration"
    assert "raw_logs" in contract["tables"]
    assert "incident_metrics" in contract["tables"]


def test_alertmanager_files_exist():
    expected_files = [
        "docker/alertmanager/alertmanager.yml",
        "docker/alertmanager/notification_templates.tmpl",
    ]

    for file_path in expected_files:
        assert Path(file_path).exists(), file_path