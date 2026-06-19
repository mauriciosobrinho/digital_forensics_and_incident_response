from fastapi import APIRouter
from fastapi.responses import HTMLResponse


router = APIRouter(tags=["ui"])


STREAMLIT_TABS = [
    {
        "id": "soc_chat",
        "label": "SOC Chat",
        "description": "Interactive SOC copilot for analyst questions, evidence-grounded answers and technical payload inspection.",
        "contract_endpoint": "/api/agents",
        "primary_artifacts": [
            "agent_investigation",
            "agent_decision_log",
            "rag_context",
            "mcp_tool_execution_log",
        ],
    },
    {
        "id": "investigation",
        "label": "Investigation",
        "description": "Incident triage, forensic investigation summary and attack characterization.",
        "contract_endpoint": "/api/evidence",
        "primary_artifacts": [
            "forensic_evidence",
            "attack_timeline",
            "nist_incident_report",
        ],
    },
    {
        "id": "human_approval",
        "label": "Human Approval",
        "description": "Human-in-the-loop approval request and decision contract for simulated containment actions.",
        "contract_endpoint": "/api/agents",
        "primary_artifacts": [
            "human_approval_request",
            "human_approval_decision",
        ],
    },
    {
        "id": "forensic_evidence",
        "label": "Forensic Evidence",
        "description": "Evidence package, chain of custody, IOCs and attack timeline.",
        "contract_endpoint": "/api/evidence",
        "primary_artifacts": [
            "chain_of_custody",
            "forensic_evidence",
            "iocs",
            "attack_timeline",
        ],
    },
    {
        "id": "rag_mcp_logs",
        "label": "RAG / MCP Logs",
        "description": "Vector RAG context and MCP-safe tool execution logs.",
        "contract_endpoint": "/api/agents",
        "primary_artifacts": [
            "rag_context",
            "mcp_tool_execution_log",
        ],
    },
    {
        "id": "agent_workflow",
        "label": "Agent Workflow",
        "description": "LangGraph workflow, agent orchestration and decision timeline.",
        "contract_endpoint": "/api/agents",
        "primary_artifacts": [
            "agent_workflow_timeline",
            "agent_decision_log",
        ],
    },
    {
        "id": "agent_evaluation",
        "label": "Agent Evaluation",
        "description": "Agent benchmark results, evaluation report and semantic quality indicators.",
        "contract_endpoint": "/api/agents",
        "primary_artifacts": [
            "agent_eval_results",
            "agent_eval_report",
            "agent_eval_summary",
        ],
    },
    {
        "id": "nist_ir_metrics",
        "label": "NIST IR Metrics",
        "description": "Incident response metrics aligned to NIST identify, protect, detect, respond and recover phases.",
        "contract_endpoint": "/api/metrics",
        "primary_artifacts": [
            "response_metrics",
            "containment_strategy",
            "root_cause_analysis",
            "nist_incident_report",
        ],
    },
    {
        "id": "observability",
        "label": "Observability",
        "description": "Platform health, operational metrics and Prometheus-ready surface.",
        "contract_endpoint": "/api/observability",
        "primary_artifacts": [
            "platform_metrics",
            "agent_metrics",
            "healthcheck",
            "soc_dashboard_data",
        ],
    },
]


def _home_html() -> str:
    return """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <title>Mercado Livre · DFIR Platform</title>
</head>
<body style="margin:0;background:#0f1117;color:#f0f6fc;font-family:Inter,Segoe UI,Roboto,Arial,sans-serif;">
<main style="max-width:1480px;margin:0 auto;padding:56px 48px 80px;">
    <section style="background:linear-gradient(135deg,#fff159,#ffe600);color:#2d3277;border-radius:22px;padding:42px;">
        <h1 style="margin:0;font-size:44px;">Mercado Livre · DFIR Platform</h1>
        <p style="font-size:18px;color:#111827;">Digital Forensics and Incident Response · IDOR Investigation Case</p>
        <p><strong>Release 1.3.0 · Sprint 5.0 · Enterprise Observability</strong></p>
        <p>
            <a href="http://localhost:8501">Streamlit UI</a> |
            <a href="/docs">API Docs</a> |
            <a href="/health">Health</a> |
            <a href="/metrics">Metrics</a> |
            <a href="http://localhost:9090">Prometheus</a> |
            <a href="http://localhost:3000">Grafana</a> |
            <a href="http://localhost:9093">Alertmanager</a>
        </p>
    </section>

    <section>
        <h2>Runtime Access</h2>
        <ul>
            <li>Streamlit UI</li>
            <li>FastAPI Docs</li>
            <li>Prometheus</li>
            <li>Grafana</li>
            <li>Alertmanager</li>
        </ul>
    </section>

    <section>
        <h2>API Contracts</h2>
        <ul>
            <li><code>/api/dashboard</code> — Executive Metrics and SOC dashboard contract.</li>
            <li><code>/api/evidence</code> — Forensic evidence and incident summary contract.</li>
            <li><code>/api/agents</code> — Agent orchestration, RAG, MCP and human approval contract.</li>
            <li><code>/api/metrics</code> — Operational and enterprise metrics JSON contract.</li>
            <li><code>/api/observability</code> — Enterprise observability readiness and dashboard contract.</li>
            <li><code>/api/tabs</code> — Streamlit functional tab mapping.</li>
            <li><code>/metrics</code> — Prometheus text exposition endpoint.</li>
        </ul>
    </section>

    <section>
        <h2>Enterprise Observability</h2>
        <ul>
            <li><a href="/api/observability/sli-slo">SLI / SLO</a></li>
            <li><a href="/api/observability/promql">PromQL Catalog</a></li>
            <li><a href="/api/observability/alerts">Alert Rules</a></li>
            <li><a href="/api/observability/dashboards">Grafana Dashboards</a></li>
            <li><a href="/api/observability/bigquery-readiness">BigQuery Readiness</a></li>
            <li><a href="/api/observability/forensic-correlation">Forensic Correlation</a></li>
        </ul>
    </section>

    <section>
        <h2>Forensic Use Cases</h2>
        <p>Patient Zero · Timeline · Automation · IDOR Evidence · Business Impact · Containment · NIST · MITRE · IOC · Root Cause · Correlation</p>
    </section>

    <section>
        <h2>Platform Flow</h2>
        <p>Streamlit UI → FastAPI Contracts → Evidence / Agents / Metrics → Prometheus / PromQL → Alertmanager → Grafana Dashboards → SOC Decision Layer</p>
    </section>
</main>
</body>
</html>
"""


@router.get("/home", response_class=HTMLResponse)
def get_home() -> HTMLResponse:
    return HTMLResponse(content=_home_html())


@router.get("/api/tabs")
def get_tabs() -> dict:
    return {
        "service": "dfir-ui-contracts",
        "ui": "streamlit",
        "tabs": STREAMLIT_TABS,
        "streamlit_url": "http://localhost:8501",
        "api_home": "http://localhost:8000/home",
    }