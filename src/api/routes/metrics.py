from __future__ import annotations

import json
from datetime import UTC, datetime
from html import escape

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, PlainTextResponse

from src.observability.observability_service import ObservabilityService
from src.observability.enterprise.enterprise_observability_service import (
    build_enterprise_metrics,
)

router = APIRouter(tags=["metrics"])
observability_service = ObservabilityService()


NAV = """
<nav class="nav">
  <a href="/home">Home</a>
  <a href="http://127.0.0.1:8501">Streamlit UI</a>
  <a href="/docs">API Docs</a>
  <a href="/health/ui">Health</a>
  <a href="/metrics/ui">Metrics</a>
  <a href="http://127.0.0.1:9090">Prometheus</a>
  <a href="http://127.0.0.1:3000">Grafana</a>
  <a href="http://127.0.0.1:9093">Alertmanager</a>
</nav>
"""


def build_operational_metrics() -> dict:
    payload = observability_service.build_api_metrics()
    payload.update(build_enterprise_metrics())
    return payload


def render_page(title: str, subtitle: str, body: str) -> str:
    return f"""
    <!doctype html>
    <html>
    <head>
      <meta charset="utf-8"/>
      <title>{escape(title)}</title>
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
          padding: 40px;
        }}
        .nav {{
          display: flex;
          gap: 16px;
          flex-wrap: wrap;
          margin-bottom: 24px;
        }}
        .nav a {{
          color: #fff159;
          text-decoration: none;
          font-weight: 700;
        }}
        .hero {{
          background: linear-gradient(135deg, #fff159, #ffe600);
          color: #2d3277;
          padding: 30px;
          border-radius: 22px;
          margin-bottom: 28px;
        }}
        .grid {{
          display: grid;
          grid-template-columns: repeat(4, minmax(0, 1fr));
          gap: 18px;
        }}
        .card {{
          background: #161b22;
          border: 1px solid #30363d;
          border-radius: 16px;
          padding: 20px;
        }}
        .card span {{
          color: #a9b7c6;
          display: block;
          font-size: 13px;
          margin-bottom: 10px;
        }}
        .card strong {{
          font-size: 32px;
        }}
        pre {{
          background: #080b10;
          border: 1px solid #30363d;
          border-radius: 16px;
          padding: 20px;
          overflow: auto;
        }}
      </style>
    </head>
    <body>
      <main>
        {NAV}
        <section class="hero">
          <h1>{escape(title)}</h1>
          <p>{escape(subtitle)}</p>
        </section>
        {body}
      </main>
    </body>
    </html>
    """


@router.get("/api/metrics")
def get_metrics() -> dict:
    return build_operational_metrics()


@router.get("/metrics", response_class=PlainTextResponse)
def prometheus_metrics() -> str:
    return observability_service.render_prometheus_metrics()


@router.get("/health/ui", response_class=HTMLResponse)
@router.get("/health-view", response_class=HTMLResponse)
def health_ui() -> str:
    payload = {
        "status": "ok",
        "service": "dfir-api",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "api_version": "1.2.1",
        "streamlit": "http://127.0.0.1:8501",
        "prometheus": "http://127.0.0.1:9090",
        "grafana": "http://127.0.0.1:3000",
        "alertmanager": "http://127.0.0.1:9093",
    }

    cards = "".join(
        f'<div class="card"><span>{escape(k)}</span><strong>{escape(str(v))}</strong></div>'
        for k, v in payload.items()
    )

    return render_page(
        "Mercado Livre · DFIR Health",
        "Human-readable platform health page. Raw machine endpoint remains available at /health.",
        f'<section class="grid">{cards}</section><h2>Raw contract</h2><pre>{escape(json.dumps(payload, indent=2))}</pre>',
    )


@router.get("/metrics/ui", response_class=HTMLResponse)
@router.get("/metrics-view", response_class=HTMLResponse)
def metrics_ui() -> str:
    metrics = build_operational_metrics()

    cards = "".join(
        f'<div class="card"><span>{escape(k)}</span><strong>{escape(str(v))}</strong></div>'
        for k, v in metrics.items()
        if isinstance(v, (int, float, str))
    )

    return render_page(
        "Mercado Livre · DFIR Metrics",
        "Human-readable operational metrics page. Raw Prometheus scrape remains available at /metrics.",
        f'<section class="grid">{cards}</section><h2>Raw contract</h2><pre>{escape(json.dumps(metrics, indent=2))}</pre>',
    )