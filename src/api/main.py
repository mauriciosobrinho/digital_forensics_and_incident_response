from __future__ import annotations

from datetime import datetime, timezone

from fastapi import FastAPI

from src.config.settings import (
    HEALTHCHECK_FILE,
    SOC_DASHBOARD_DATA_FILE,
)


app = FastAPI(
    title="DFIR IDOR Response Platform API",
    version="1.2.0",
    description=(
        "Digital Forensics and Incident Response Platform API "
        "for IDOR investigation, evidence, agents and metrics."
    ),
)


@app.get("/")
def root():
    return {
        "service": "DFIR IDOR Response Platform",
        "version": "1.2.0",
        "health": "/health",
        "docs": "/docs",
    }


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": "dfir-api",
        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "healthcheck_file_exists": HEALTHCHECK_FILE.exists(),
        "soc_dashboard_file_exists": SOC_DASHBOARD_DATA_FILE.exists(),
    }


@app.get("/version")
def version() -> dict:
    return {
        "service": "dfir-platform",
        "api_version": "1.2.0",
        "sprint": "4.3",
        "codename": "Platform Reliability & Quality Engineering",
    }