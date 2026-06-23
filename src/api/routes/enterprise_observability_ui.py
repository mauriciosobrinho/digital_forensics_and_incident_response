# src/api/routes/enterprise_observability_ui.py

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from src.observability.enterprise.enterprise_observability_service import (
    EnterpriseObservabilityService,
)

router = APIRouter(tags=["enterprise-observability-ui"])

enterprise_service = EnterpriseObservabilityService()

def render_platform_nav() -> str:
    return """
    <nav class="platform-nav">
        <a href="/home">Home</a>
        <a href="http://127.0.0.1:8501/?platform_nav=1">Streamlit UI</a>
        <a href="/docs">API Docs</a>
        <a href="/health/ui">Health</a>
        <a href="/metrics/ui">Metrics</a>
        <a href="/observability/ui">Observability</a>
        <a href="/prometheus/ui">Prometheus</a>
        <a href="/grafana/ui">Grafana</a>
        <a href="/alertmanager/ui">Alertmanager</a>
    </nav>
    """

def render_breadcrumb(current: str) -> str:
    return f"""
    <div class="breadcrumb">
        <a href="/home">Home</a>
        <span>/</span>
        <a href="/observability/ui">Observability</a>
        <span>/</span>
        <strong>{current}</strong>
    </div>
    """

# def page(title: str, subtitle: str, body: str) -> str:
def page(
        title: str,
        subtitle: str,
        body: str,
        breadcrumb: str = ""
        ) -> str:
    return f"""
    <!doctype html>
    <html>
    <head>
        <meta charset="utf-8"/>
        <title>Mercado Livre · {title}</title>
        <style>
            body {{
                margin: 0;
                background: #0f1117;
                color: #f0f6fc;
                font-family: Inter, Segoe UI, Roboto, Arial, sans-serif;
            }}
            main {{
                max-width: 1480px;
                margin: 0 auto;
                padding: 48px;
            }}
            .platform-nav {{
                display: flex;
                gap: 18px;
                margin-bottom: 28px;
                font-weight: 800;
            }}
            .platform-nav a {{
                color: #fff159;
                text-decoration: none;
            }}
            .platform-nav a:hover {{
                text-decoration: underline;
            }}
            .hero {{
                background: linear-gradient(135deg, #fff159, #ffe600);
                color: #2d3277;
                border-radius: 22px;
                padding: 42px;
                margin-bottom: 34px;
            }}
            .hero h1 {{
                margin: 0;
                font-size: 44px;
            }}
            .hero p {{
                color: #111827;
                font-size: 18px;
            }}
            .grid {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 22px;
            }}
            .card {{
                background: #161b22;
                border: 1px solid #30363d;
                border-radius: 18px;
                padding: 26px;
            }}
            .card h2 {{
                color: #fff159;
                margin-top: 0;
            }}
            .value {{
                font-size: 42px;
                font-weight: 900;
                color: #ffffff;
            }}
            .muted {{
                color: #a9b7c6;
            }}
            .ok {{
                color: #7ee787;
            }}
            .warn {{
                color: #ffcc00;
            }}
            .critical {{
                color: #ff4b5c;
            }}
            code {{
                color: #fff159;
            }}
            .button {{
                display: inline-block;
                margin-top: 16px;
                background: #fff159;
                color: #2d3277;
                padding: 12px 18px;
                border-radius: 12px;
                font-weight: 900;
                text-decoration: none;
            }}


            .breadcrumb {{
                display: flex;
                gap: 10px;
                align-items: center;
                margin-bottom: 26px;
                font-weight: 800;
            }}

            .breadcrumb a {{
                color: #fff159;
                text-decoration: none;
            }}

            .breadcrumb a:hover {{
                text-decoration: underline;
            }}

            .breadcrumb span {{
                color: #9ca3af;
            }}

            .breadcrumb strong {{
                color: #ffffff;
            }}


        </style>
    </head>
    <body>
        <main>
            {render_platform_nav()}
            {breadcrumb}

            <section class="hero">
                <h1>Mercado Livre · {title}</h1>
                <p>{subtitle}</p>
            </section>

            {body}
        </main>
    </body>
    </html>
    """


@router.get("/observability/ui", response_class=HTMLResponse)
def observability_overview_ui() -> str:
    slo = enterprise_service.get_sli_slo()
    correlation = enterprise_service.get_forensic_correlation()
    bigquery = enterprise_service.get_bigquery_readiness()
    alerts = enterprise_service.get_alert_rules()

    body = f"""
    <section class="grid">
        <div class="card">
            <h2>Detection SLI</h2>
            <div class="value">{slo["sli"]["detection_success_rate"]:.0%}</div>
            <p class="muted">Target: {slo["slo"]["detection_target"]:.0%}</p>
            <a class="button" href="/observability/slo/ui">Open SLO Dashboard</a>
        </div>

        <div class="card">
            <h2>Evidence Completeness</h2>
            <div class="value">{slo["sli"]["evidence_completeness"]:.0%}</div>
            <p class="muted">Forensic readiness indicator.</p>
            <a class="button" href="/observability/correlation/ui">Open Correlation</a>
        </div>

        <div class="card">
            <h2>Containment Readiness</h2>
            <div class="value">{slo["sli"]["containment_readiness"]:.0%}</div>
            <p class="muted">Human-in-the-loop safe response readiness.</p>
        </div>

        <div class="card">
            <h2>Forensic Correlation</h2>
            <div class="value">{correlation["score"]:.0%}</div>
            <p class="muted">Correlation across evidence, agents and response artifacts.</p>
        </div>

        <div class="card">
            <h2>Data Platform</h2>
            <div class="value">{bigquery["readiness"]}</div>
            <p class="muted">{bigquery["status"]}</p>
            <a class="button" href="/observability/data-platform/ui">Open Data Platform</a>
        </div>

        <div class="card">
            <h2>Alert Rules</h2>
            <div class="value">{len(alerts["rules"])}</div>
            <p class="muted">Enterprise alerting rules registered.</p>
            <a class="button" href="/observability/alerts/ui">Open Alert Operations</a>
        </div>
    </section>
    """

    return page(
        "Enterprise Observability",
        "Human-readable operational observability layer for SOC, DFIR, SLI/SLO, alerting and data readiness.",
        body,
        breadcrumb="""
        <div class="breadcrumb">
            <a href="/home">Home</a>
            <span>/</span>
            <strong>Observability</strong>
        </div>
        """,
    )


@router.get("/observability/slo/ui", response_class=HTMLResponse)
def slo_dashboard_ui() -> str:
    data = enterprise_service.get_sli_slo()
    sli = data["sli"]
    slo = data["slo"]

    body = f"""
    <section class="grid">
        <div class="card">
            <h2>Detection Success Rate</h2>
            <div class="value">{sli["detection_success_rate"]:.0%}</div>
            <p class="muted">Target: {slo["detection_target"]:.0%}</p>
        </div>

        <div class="card">
            <h2>Evidence Completeness</h2>
            <div class="value">{sli["evidence_completeness"]:.0%}</div>
            <p class="muted">Required for forensic-grade investigation.</p>
        </div>

        <div class="card">
            <h2>Containment Readiness</h2>
            <div class="value">{sli["containment_readiness"]:.0%}</div>
            <p class="muted">Target response readiness: {slo["response_target"]:.0%}</p>
        </div>
    </section>
    """

    return page(
        "Detection SLO Dashboard",
        "SLI/SLO dashboard for detection quality, evidence completeness and containment readiness.",
        body,
        breadcrumb=render_breadcrumb("SLI / SLO"),
    )


@router.get("/observability/alerts/ui", response_class=HTMLResponse)
def alert_operations_ui() -> str:
    data = enterprise_service.get_alert_rules()
    rules = data["rules"]

    cards = "".join(
        f"""
        <div class="card">
            <h2>{rule["alert"]}</h2>
            <p><code>{rule["expr"]}</code></p>
            <p class="{rule["severity"]}">Severity: {rule["severity"]}</p>
        </div>
        """
        for rule in rules
    )

    body = f"""
    <section class="grid">
        {cards}
    </section>
    """

    return page(
        "Alert Operations Dashboard",
        "...",
        body,
        breadcrumb=render_breadcrumb("Alert Rules"),
    )


@router.get("/observability/promql/ui", response_class=HTMLResponse)
def promql_explorer_ui() -> str:
    queries = enterprise_service.get_promql_catalog()

    cards = "".join(
        f"""
        <div class="card">
            <h2>{item["name"]}</h2>
            <p><code>{item["query"]}</code></p>
            <p class="muted">{item["purpose"]}</p>
        </div>
        """
        for item in queries
    )

    body = f"""
    <section class="grid">
        {cards}
    </section>
    """

    return page(
        "Prometheus Metrics Explorer",
        "Catalog of operational PromQL expressions used by dashboards, alerts and automation.",
        body,
        breadcrumb=render_breadcrumb("PromQL Catalog"),
    )


@router.get("/observability/correlation/ui", response_class=HTMLResponse)
def forensic_correlation_ui() -> str:
    data = enterprise_service.get_forensic_correlation()

    layers = "".join(f"<li>{layer}</li>" for layer in data["correlation_layers"])
    use_cases = "".join(f"<li>{case}</li>" for case in data["use_cases"])

    body = f"""
    <section class="grid">
        <div class="card">
            <h2>Correlation Score</h2>
            <div class="value">{data["score"]:.0%}</div>
            <p class="muted">Cross-artifact forensic consistency.</p>
        </div>

        <div class="card">
            <h2>Correlation Layers</h2>
            <ul>{layers}</ul>
        </div>

        <div class="card">
            <h2>Use Cases</h2>
            <ul>{use_cases}</ul>
        </div>
    </section>
    """

    return page(
        "Forensic Correlation Dashboard",
        "Forensic correlation across raw logs, parsed events, risk scores, evidence and response metrics.",
        body,
        breadcrumb=render_breadcrumb("Forensic Correlation"),
    )


@router.get("/observability/data-platform/ui", response_class=HTMLResponse)
def data_platform_ui() -> str:
    data = enterprise_service.get_bigquery_readiness()

    tables = "".join(f"<li>{table}</li>" for table in data["tables"])

    body = f"""
    <section class="grid">
        <div class="card">
            <h2>Provider</h2>
            <div class="value">{data["provider"]}</div>
        </div>

        <div class="card">
            <h2>Readiness</h2>
            <div class="value">{data["readiness"]}</div>
            <p class="muted">{data["status"]}</p>
        </div>

        <div class="card">
            <h2>Dataset Strategy</h2>
            <div class="value">{data["dataset_strategy"]}</div>
        </div>

        <div class="card">
            <h2>Analytical Tables</h2>
            <ul>{tables}</ul>
        </div>
    </section>
    """

    return page(
        "Data Platform Readiness",
        "Human-readable readiness page for BigQuery forensic analytics integration.",
        body,
        breadcrumb=render_breadcrumb("Data Platform"),
    )