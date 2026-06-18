from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from src.api.routes.agents import router as agents_router
from src.api.routes.dashboard import router as dashboard_router
from src.api.routes.evidence import router as evidence_router
from src.api.routes.metrics import (
    build_operational_metrics,
    router as metrics_router,
)
from src.api.routes.observability import router as observability_router
from src.api.routes.ui import router as ui_router


API_VERSION = "1.2.1"
SPRINT = "4.4"
CODENAME = "Interface Contracts & API Routes"


app = FastAPI(
    title="DFIR IDOR Response Platform API",
    description=(
        "Digital Forensics and Incident Response Platform API "
        "for IDOR investigation, evidence, agents, metrics and observability."
    ),
    version=API_VERSION,
)


app.include_router(dashboard_router)
app.include_router(evidence_router)
app.include_router(agents_router)
app.include_router(metrics_router)
app.include_router(observability_router)
app.include_router(ui_router)


@app.get("/")
def root() -> dict:
    return {
        "service": "DFIR IDOR Response Platform",
        "version": API_VERSION,
        "sprint": SPRINT,
        "codename": CODENAME,
        "home": "/home",
        "health": "/health",
        "docs": "/docs",
        "tabs": "/api/tabs",
        "metrics_json": "/api/metrics",
        "metrics_prometheus": "/metrics",
    }


@app.get("/home", response_class=HTMLResponse)
def home() -> str:
    metrics = build_operational_metrics()

    return f"""
    <!doctype html>
    <html lang="en">
        <head>
            <meta charset="utf-8" />
            <title>Mercado Livre · DFIR Platform</title>
            <style>
                :root {{
                    --meli-yellow: #fff159;
                    --meli-yellow-strong: #ffe600;
                    --meli-blue: #2d3277;
                    --bg: #0f1117;
                    --card: #161b22;
                    --border: #30363d;
                    --text: #f5f5f5;
                    --muted: #9ca3af;
                    --green: #3fb950;
                }}

                * {{
                    box-sizing: border-box;
                }}

                body {{
                    margin: 0;
                    padding: 40px;
                    background: var(--bg);
                    color: var(--text);
                    font-family: Arial, Helvetica, sans-serif;
                }}

                .container {{
                    max-width: 1180px;
                    margin: 0 auto;
                }}

                .hero {{
                    background: linear-gradient(
                        135deg,
                        var(--meli-yellow-strong) 0%,
                        var(--meli-yellow) 100%
                    );
                    color: var(--meli-blue);
                    border-radius: 18px;
                    padding: 32px;
                    border: 1px solid #d8c900;
                    box-shadow: 0 16px 48px rgba(0, 0, 0, 0.28);
                }}

                .hero h1 {{
                    margin: 0 0 10px 0;
                    font-size: 38px;
                    letter-spacing: -0.8px;
                }}

                .hero p {{
                    margin: 0 0 22px 0;
                    font-size: 17px;
                    color: #1f245f;
                }}

                .actions {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 12px;
                }}

                .button {{
                    display: inline-block;
                    background: var(--meli-blue);
                    color: #ffffff;
                    padding: 10px 16px;
                    border-radius: 999px;
                    text-decoration: none;
                    font-weight: 700;
                    font-size: 14px;
                }}

                .button.secondary {{
                    background: #ffffff;
                    color: var(--meli-blue);
                }}

                .section {{
                    margin-top: 28px;
                }}

                .section h2 {{
                    margin: 0 0 14px 0;
                    font-size: 22px;
                }}

                .metric-grid {{
                    display: grid;
                    grid-template-columns: repeat(4, minmax(0, 1fr));
                    gap: 16px;
                }}

                .metric-card {{
                    background: var(--card);
                    border: 1px solid var(--border);
                    border-radius: 14px;
                    padding: 20px;
                }}

                .metric-label {{
                    color: var(--muted);
                    font-size: 14px;
                    margin-bottom: 10px;
                }}

                .metric-value {{
                    font-size: 34px;
                    font-weight: 800;
                    color: #ffffff;
                }}

                .contract-table {{
                    width: 100%;
                    border-collapse: collapse;
                    overflow: hidden;
                    border-radius: 14px;
                    border: 1px solid var(--border);
                    background: var(--card);
                }}

                .contract-table th,
                .contract-table td {{
                    padding: 14px 16px;
                    border-bottom: 1px solid var(--border);
                    text-align: left;
                    vertical-align: top;
                }}

                .contract-table th {{
                    background: #1c212b;
                    color: var(--meli-yellow);
                    font-size: 14px;
                    text-transform: uppercase;
                    letter-spacing: 0.04em;
                }}

                .contract-table tr:last-child td {{
                    border-bottom: none;
                }}

                code {{
                    background: #22272e;
                    border: 1px solid #30363d;
                    border-radius: 6px;
                    padding: 3px 7px;
                    color: #e6edf3;
                }}

                .flow {{
                    background: var(--card);
                    border: 1px solid var(--border);
                    border-radius: 14px;
                    padding: 22px;
                    font-size: 18px;
                    line-height: 1.7;
                }}

                .flow strong {{
                    color: var(--meli-yellow);
                }}

                .badge {{
                    display: inline-block;
                    margin-top: 18px;
                    background: var(--meli-blue);
                    color: #ffffff;
                    border-radius: 999px;
                    padding: 8px 14px;
                    font-size: 13px;
                    font-weight: 700;
                }}

                .status {{
                    color: var(--green);
                    font-weight: 700;
                }}

                @media (max-width: 900px) {{
                    body {{
                        padding: 20px;
                    }}

                    .metric-grid {{
                        grid-template-columns: repeat(2, minmax(0, 1fr));
                    }}
                }}

                @media (max-width: 560px) {{
                    .metric-grid {{
                        grid-template-columns: 1fr;
                    }}

                    .hero h1 {{
                        font-size: 30px;
                    }}
                }}
            </style>
        </head>
        <body>
            <main class="container">
                <section class="hero">
                    <h1>Mercado Livre · DFIR Platform</h1>
                    <p>
                        Digital Forensics and Incident Response · IDOR Investigation Case
                    </p>

                    <div class="actions">
                        <a class="button" href="http://localhost:8501">Streamlit UI</a>
                        <a class="button" href="http://localhost:8000/docs">API Docs</a>
                        <a class="button" href="http://localhost:8000/health">Health</a>
                        <a class="button secondary" href="http://localhost:8000/api/metrics">Metrics</a>
                    </div>

                    <span class="badge">
                        Release {API_VERSION} · Sprint {SPRINT} · {CODENAME}
                    </span>
                </section>

                <section class="section">
                    <h2>Executive Metrics</h2>
                    <div class="metric-grid">
                        <div class="metric-card">
                            <div class="metric-label">Scored IPs</div>
                            <div class="metric-value">{metrics["scored_ips"]}</div>
                        </div>

                        <div class="metric-card">
                            <div class="metric-label">IDOR Findings</div>
                            <div class="metric-value">{metrics["idor_findings"]}</div>
                        </div>

                        <div class="metric-card">
                            <div class="metric-label">Anomalous IPs</div>
                            <div class="metric-value">{metrics["anomalous_ips"]}</div>
                        </div>

                        <div class="metric-card">
                            <div class="metric-label">Agent Decisions</div>
                            <div class="metric-value">{metrics["agent_decisions"]}</div>
                        </div>
                    </div>
                </section>

                <section class="section">
                    <h2>API Contracts</h2>
                    <table class="contract-table">
                        <thead>
                            <tr>
                                <th>Endpoint</th>
                                <th>Contract</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code>/api/dashboard</code></td>
                                <td>Executive SOC dashboard contract.</td>
                            </tr>
                            <tr>
                                <td><code>/api/evidence</code></td>
                                <td>Forensic evidence contract.</td>
                            </tr>
                            <tr>
                                <td><code>/api/agents</code></td>
                                <td>Agent orchestration and human approval contract.</td>
                            </tr>
                            <tr>
                                <td><code>/api/metrics</code></td>
                                <td>Operational metrics JSON contract.</td>
                            </tr>
                            <tr>
                                <td><code>/api/observability</code></td>
                                <td>Observability readiness contract.</td>
                            </tr>
                            <tr>
                                <td><code>/api/tabs</code></td>
                                <td>Streamlit tabs functional mapping.</td>
                            </tr>
                            <tr>
                                <td><code>/metrics</code></td>
                                <td>Prometheus text exposition endpoint.</td>
                            </tr>
                        </tbody>
                    </table>
                </section>

                <section class="section">
                    <h2>Platform Flow</h2>
                    <div class="flow">
                        <strong>Streamlit UI</strong>
                        →
                        <strong>FastAPI Contracts</strong>
                        →
                        <strong>Evidence / Agents / Metrics</strong>
                        →
                        <strong>Prometheus / Grafana</strong>
                    </div>
                </section>

                <section class="section">
                    <div class="flow">
                        Platform health:
                        <span class="status">{metrics["platform_health"]}</span>
                        · Severity:
                        <strong>{metrics["severity"]}</strong>
                        · Priority:
                        <strong>{metrics["incident_priority"]}</strong>
                    </div>
                </section>
            </main>
        </body>
    </html>
    """


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": "dfir-api",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "api_version": API_VERSION,
    }


@app.get("/version")
def version() -> dict:
    return {
        "service": "dfir-platform",
        "api_version": API_VERSION,
        "sprint": SPRINT,
        "codename": CODENAME,
    }