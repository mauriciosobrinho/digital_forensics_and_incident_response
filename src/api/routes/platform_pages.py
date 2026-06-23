from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["platform-navigation"])


def platform_nav(active: str = "") -> str:
    items = [
        ("Home", "/home"),
        ("Streamlit UI", "http://127.0.0.1:8501"),
        ("API Docs", "/docs"),
        ("Health", "/health/ui"),
        ("Metrics", "/metrics/ui"),
        ("Prometheus", "/prometheus/ui"),
        ("Grafana", "/grafana/ui"),
        ("Alertmanager", "/alertmanager/ui"),
    ]

    return "".join(
        f'<a class="{"active" if label == active else ""}" href="{href}">{label}</a>'
        for label, href in items
    )


def page_template(title: str, subtitle: str, active: str, body: str) -> str:
    return f"""
    <!doctype html>
    <html>
    <head>
        <meta charset="utf-8"/>
        <title>{title}</title>
        <style>
            body {{
                margin: 0;
                background: #0f1117;
                color: #f0f6fc;
                font-family: Inter, Segoe UI, Arial, sans-serif;
            }}
            main {{
                max-width: 1440px;
                margin: auto;
                padding: 48px;
            }}
            nav {{
                display: flex;
                gap: 18px;
                margin-bottom: 28px;
                font-weight: 800;
            }}
            nav a {{
                color: #fff159;
                text-decoration: none;
            }}
            nav a.active {{
                color: #ffffff;
                border-bottom: 3px solid #fff159;
            }}
            nav a:hover {{
                text-decoration: underline;
            }}
            .hero {{
                background: linear-gradient(135deg, #fff159, #ffe600);
                color: #2d3277;
                padding: 36px;
                border-radius: 24px;
                margin-bottom: 32px;
            }}
            .hero h1 {{
                font-size: 44px;
                margin: 0 0 16px 0;
            }}
            .hero p {{
                font-size: 19px;
                margin: 0;
            }}
            .grid {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
            }}
            .card {{
                background: #161b22;
                border: 1px solid #30363d;
                border-radius: 18px;
                padding: 24px;
            }}
            .card h2 {{
                margin-top: 0;
                color: #fff159;
            }}
            .card strong {{
                font-size: 34px;
                display: block;
                margin-top: 10px;
            }}
            .button {{
                display: inline-block;
                background: #fff159;
                color: #2d3277;
                padding: 12px 18px;
                border-radius: 12px;
                font-weight: 900;
                text-decoration: none;
                margin-top: 12px;
            }}
            code {{
                color: #fff159;
            }}
        </style>
    </head>
    <body>
        <main>
            <nav>{platform_nav(active)}</nav>
            <section class="hero">
                <h1>{title}</h1>
                <p>{subtitle}</p>
            </section>
            {body}
        </main>
    </body>
    </html>
    """


@router.get("/prometheus/ui", response_class=HTMLResponse)
def prometheus_ui() -> str:
    body = """
    <section class="grid">
        <div class="card">
            <h2>Purpose</h2>
            <p>Prometheus is the technical monitoring engine used to scrape DFIR platform metrics and evaluate alert rules.</p>
        </div>
        <div class="card">
            <h2>Raw Service</h2>
            <p>Use the native UI for PromQL queries, targets, rules and alert status.</p>
            <a class="button" href="http://127.0.0.1:9090">Open Prometheus</a>
        </div>
        <div class="card">
            <h2>Main Scrape Target</h2>
            <p><code>dfir-api:8000/metrics</code></p>
            <p>Raw metrics remain available at <code>/metrics</code>.</p>
        </div>
    </section>
    """
    return page_template(
        "Mercado Livre · Prometheus",
        "Human-readable navigation page for Prometheus monitoring and alert rule validation.",
        "Prometheus",
        body,
    )


@router.get("/grafana/ui", response_class=HTMLResponse)
def grafana_ui() -> str:
    body = """
    <section class="grid">
        <div class="card">
            <h2>Executive Dashboard</h2>
            <p>Severity, business impact, affected invoices, SLI/SLO and containment readiness.</p>
            <a class="button" href="http://127.0.0.1:3000/d/dfir-executive/dfir-executive-dashboard?orgId=1">Open</a>
        </div>
        <div class="card">
            <h2>Investigation Dashboard</h2>
            <p>IDOR findings, anomalous IPs, forensic correlation and affected objects.</p>
            <a class="button" href="http://127.0.0.1:3000/d/dfir-investigation/dfir-investigation-dashboard?orgId=1">Open</a>
        </div>
        <div class="card">
            <h2>SOC Agents Dashboard</h2>
            <p>LLM, RAG, MCP, approval latency, fallback rate and answer quality.</p>
            <a class="button" href="http://127.0.0.1:3000/d/dfir-agents/soc-agents-dashboard?orgId=1">Open</a>
        </div>
    </section>
    """
    return page_template(
        "Mercado Livre · Grafana",
        "Human-readable entrypoint for DFIR analytical dashboards.",
        "Grafana",
        body,
    )


@router.get("/alertmanager/ui", response_class=HTMLResponse)
def alertmanager_ui() -> str:
    body = """
    <section class="grid">
        <div class="card">
            <h2>Purpose</h2>
            <p>Alertmanager receives Prometheus alerts and manages grouping, routing, silencing and notification status.</p>
        </div>
        <div class="card">
            <h2>Operations</h2>
            <p>Use it to inspect firing alerts, silence controlled test alerts and validate alert routing.</p>
            <a class="button" href="http://127.0.0.1:9093">Open Alertmanager</a>
        </div>
        <div class="card">
            <h2>Expected Critical Alerts</h2>
            <p><code>CriticalIDORFindings</code>, <code>HighIDORFindings</code> and readiness-related rules.</p>
        </div>
    </section>
    """
    return page_template(
        "Mercado Livre · Alertmanager",
        "Human-readable operational guide for alert triage and notification routing.",
        "Alertmanager",
        body,
    )