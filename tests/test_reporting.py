from src.reporting.markdown_builder import (
    build_architecture_doc,
    build_evidence_appendix,
    build_executive_summary,
    build_methodology_doc,
    build_technical_report,
)


def sample_nist_report():
    return {
        "incident_summary": {
            "severity": "critical",
            "priority": "P1",
            "dry_run": True,
        },
        "questions_answered": {
            "when_did_it_start": "2020-10-01",
            "when_did_it_end": "2020-12-31",
            "how_many_invoices": 10221,
            "how_many_attack_events": 96829,
            "how_many_tokens": 35,
            "patient_zero_candidate": "1.1.1.1",
            "was_it_automated": True,
        },
    }


def sample_platform_metrics():
    return {
        "pipeline_metrics": {
            "n_logs_processed": 100,
            "n_ips_analyzed": 10,
            "n_idor_findings": 5,
            "n_anomalous_ips": 2,
            "n_iocs_generated": 3,
        }
    }


def sample_agent_metrics():
    return {
        "n_agent_decisions": 4,
        "n_tool_calls": 2,
        "n_dry_run_actions": 1,
    }


def sample_eval_report():
    return {
        "summary": {
            "overall_coverage_percent": 100,
            "passed": 15,
            "partial": 0,
            "failed": 0,
        }
    }


def test_build_technical_report():
    text = build_technical_report(
        nist_report=sample_nist_report(),
        platform_metrics=sample_platform_metrics(),
        agent_metrics=sample_agent_metrics(),
        evaluation_report=sample_eval_report(),
        healthcheck={
            "overall_status": "healthy",
        },
        figures={
            "pipeline_metrics": "reports/figures/pipeline_metrics.png",
            "agent_metrics": "reports/figures/agent_metrics.png",
            "agent_coverage": "reports/figures/agent_coverage.png",
        },
    )

    assert "Technical Report" in text
    assert "IDOR" in text
    assert "NIST" in text


def test_build_executive_summary():
    text = build_executive_summary(
        nist_report=sample_nist_report(),
        platform_metrics=sample_platform_metrics(),
        evaluation_report=sample_eval_report(),
    )

    assert "Executive Summary" in text
    assert "Estimated Impact" in text


def test_static_docs():
    assert "Architecture" in build_architecture_doc()
    assert "Methodology" in build_methodology_doc()


def test_evidence_appendix():
    text = build_evidence_appendix(
        artifacts={
            "x": "path/to/x.json",
        }
    )

    assert "Evidence Appendix" in text
    assert "path/to/x.json" in text