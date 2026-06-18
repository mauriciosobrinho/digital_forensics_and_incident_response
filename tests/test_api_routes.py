from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_root_contract():
    response = client.get("/")

    assert response.status_code == 200

    payload = response.json()

    assert payload["service"] == "DFIR IDOR Response Platform"
    assert payload["home"] == "/home"
    assert payload["health"] == "/health"
    assert payload["tabs"] == "/api/tabs"
    assert payload["metrics_prometheus"] == "/metrics"


def test_home_contract():
    response = client.get("/home")

    assert response.status_code == 200
    assert "Mercado Livre · DFIR Platform" in response.text
    assert "Digital Forensics and Incident Response" in response.text
    assert "Streamlit UI" in response.text
    assert "API Contracts" in response.text
    assert "Executive Metrics" in response.text
    assert "Platform Flow" in response.text
    assert "/api/dashboard" in response.text
    assert "/metrics" in response.text


def test_health_contract():
    response = client.get("/health")

    assert response.status_code == 200

    payload = response.json()

    assert payload["status"] == "ok"
    assert payload["service"] == "dfir-api"


def test_version_contract():
    response = client.get("/version")

    assert response.status_code == 200

    payload = response.json()

    assert payload["service"] == "dfir-platform"
    assert payload["sprint"] == "4.4"


def test_dashboard_contract():
    response = client.get("/api/dashboard")

    assert response.status_code == 200

    payload = response.json()

    assert payload["service"] == "dfir-dashboard"
    assert "scored_ips" in payload
    assert "idor_findings" in payload
    assert "anomalous_ips" in payload


def test_evidence_contract():
    response = client.get("/api/evidence")

    assert response.status_code == 200

    payload = response.json()

    assert payload["service"] == "dfir-evidence"
    assert "available" in payload
    assert "source_files" in payload


def test_agents_contract():
    response = client.get("/api/agents")

    assert response.status_code == 200

    payload = response.json()

    assert payload["service"] == "dfir-agents"
    assert "decision_count" in payload
    assert "human_approval" in payload


def test_metrics_contract():
    response = client.get("/api/metrics")

    assert response.status_code == 200

    payload = response.json()

    assert payload["service"] == "dfir-operational-metrics"
    assert "scored_ips" in payload
    assert "platform_health" in payload


def test_prometheus_metrics_contract():
    response = client.get("/metrics")

    assert response.status_code == 200

    body = response.text

    assert "dfir_scored_ips" in body
    assert "dfir_idor_findings" in body
    assert "dfir_anomalous_ips" in body
    assert "dfir_platform_health" in body


def test_observability_contract():
    response = client.get("/api/observability")

    assert response.status_code == 200

    payload = response.json()

    assert payload["service"] == "dfir-observability"
    assert payload["prometheus_ready_endpoint"] == "/metrics"
    assert "platform_health" in payload


def test_tabs_contract():
    response = client.get("/api/tabs")

    assert response.status_code == 200

    payload = response.json()

    tab_labels = [tab["label"] for tab in payload["tabs"]]

    assert "SOC Chat" in tab_labels
    assert "Investigation" in tab_labels
    assert "Human Approval" in tab_labels
    assert "Forensic Evidence" in tab_labels
    assert "Observability" in tab_labels