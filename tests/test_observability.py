from pathlib import Path

import polars as pl

from src.observability.agent_metrics import (
    build_agent_metrics,
)
from src.observability.healthcheck import (
    build_healthcheck,
)
from src.observability.platform_metrics import (
    build_platform_metrics,
)
from src.observability.soc_dashboard_data import (
    build_soc_dashboard_data,
)


def test_build_platform_metrics(tmp_path: Path):
    parquet_file = tmp_path / "sample.parquet"

    pl.DataFrame(
        {
            "a": [
                1,
                2,
                3,
            ]
        }
    ).write_parquet(parquet_file)

    metrics = build_platform_metrics(
        paths={
            "parsed_events": parquet_file,
            "ip_features": parquet_file,
            "idor_findings": parquet_file,
            "anomaly_scores": parquet_file,
            "anomalous_ips": parquet_file,
        },
        forensic_evidence={
            "summary": {
                "case": "test",
            }
        },
        iocs={
            "summary": {
                "ip_indicators": 2,
                "token_indicators": 1,
            }
        },
    )

    assert metrics["pipeline_metrics"]["n_logs_processed"] == 3
    assert metrics["pipeline_metrics"]["n_iocs_generated"] == 3
    assert metrics["status"] == "healthy"


def test_build_agent_metrics():
    metrics = build_agent_metrics(
        agent_investigation={
            "dry_run": True,
            "human_loop_count": 1,
            "human_approval_response": {
                "decision": "approved_for_dry_run_only",
            },
            "approved_actions": [
                {
                    "dry_run": True,
                }
            ],
        },
        decision_log=[
            {},
            {},
            {},
            {},
        ],
        workflow_timeline=[
            {},
            {},
        ],
        tool_execution_log=[
            {},
        ],
        mcp_tool_execution_log=[
            {},
        ],
        llm_reasoning=[
            {},
        ],
    )

    assert metrics["n_agent_decisions"] == 4
    assert metrics["n_tool_calls"] == 2
    assert metrics["n_human_approvals"] == 1
    assert metrics["n_dry_run_actions"] == 1
    assert metrics["status"] == "healthy"


def test_build_healthcheck(tmp_path: Path):
    artifact = tmp_path / "artifact.json"
    artifact.write_text(
        "{}",
        encoding="utf-8",
    )

    healthcheck = build_healthcheck(
        required_artifacts={
            "artifact": artifact,
        },
        platform_metrics={
            "status": "healthy",
        },
        agent_metrics={
            "status": "healthy",
        },
    )

    assert healthcheck["overall_status"] == "healthy"
    assert healthcheck["missing_artifacts"] == []


def test_build_soc_dashboard_data():
    dashboard = build_soc_dashboard_data(
        platform_metrics={
            "pipeline_metrics": {
                "n_logs_processed": 10,
            }
        },
        agent_metrics={
            "n_agent_decisions": 4,
        },
        healthcheck={
            "overall_status": "healthy",
        },
        nist_report={
            "incident_summary": {
                "severity": "critical",
                "priority": "P1",
                "dry_run": True,
            }
        },
        evaluation_report={
            "summary": {
                "overall_coverage_percent": 100,
            }
        },
    )

    assert dashboard["topline"]["health"] == "healthy"
    assert dashboard["topline"]["severity"] == "critical"
    assert dashboard["pipeline"]["n_logs_processed"] == 10