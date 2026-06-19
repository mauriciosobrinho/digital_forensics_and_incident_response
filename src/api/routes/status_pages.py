from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["status-pages"])


@router.get("/health-view", response_class=HTMLResponse)
def health_view() -> str:
    return """
    <!doctype html>
    <html>
    <head>
        <meta charset="utf-8"/>
        <title>Mercado Livre · DFIR Health</title>
        <style>
            body {
                margin: 0;
                background: #0f1117;
                color: #f0f6fc;
                font-family: Inter, Segoe UI, Arial, sans-serif;
            }
            main {
                max-width: 1200px;
                margin: auto;
                padding: 48px;
            }
            .hero {
                background: linear-gradient(135deg, #fff159, #ffe600);
                color: #2d3277;
                padding: 32px;
                border-radius: 22px;
                margin-bottom: 32px;
            }
            .nav a {
                color: #fff159;
                text-decoration: none;
                margin-right: 16px;
                font-weight: 700;
            }
            .grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 18px;
            }
            .card {
                background: #161b22;
                border: 1px solid #30363d;
                border-radius: 16px;
                padding: 24px;
            }
            .ok {
                color: #2ea043;
                font-size: 42px;
                font-weight: 800;
            }
        </style>
    </head>
    <body>
        <main>
            <div class="nav">
                <a href="/home">← Home</a>
                <a href="/metrics-view">Metrics</a>
                <a href="/docs">API Docs</a>
                <a href="/health">Raw Health JSON</a>
            </div>

            <section class="hero">
                <h1>Mercado Livre · DFIR Platform Health</h1>
                <p>Operational readiness page for SOC analysts and technical reviewers.</p>
            </section>

            <section class="grid">
                <div class="card">
                    <h3>API Status</h3>
                    <div class="ok">OK</div>
                </div>
                <div class="card">
                    <h3>Service</h3>
                    <div class="ok">dfir-api</div>
                </div>
                <div class="card">
                    <h3>Purpose</h3>
                    <p>Confirms the DFIR backend is alive and ready to serve investigation, evidence, agents and observability contracts.</p>
                </div>
            </section>
        </main>
    </body>
    </html>
    """