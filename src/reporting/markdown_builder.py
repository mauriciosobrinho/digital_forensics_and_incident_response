from datetime import datetime, timezone


def build_technical_report(
    *,
    nist_report: dict,
    platform_metrics: dict,
    agent_metrics: dict,
    evaluation_report: dict,
    healthcheck: dict,
    figures: dict,
) -> str:

    incident = nist_report.get("incident_summary", {})
    questions = nist_report.get("questions_answered", {})
    pipeline = platform_metrics.get("pipeline_metrics", {})
    eval_summary = evaluation_report.get("summary", {})

    return f"""# IDOR Response Platform — Technical Report

Generated at: {datetime.now(timezone.utc).isoformat()}

## 1. Context and Objective

This project implements a Digital Forensics and Incident Response platform for investigating IDOR incidents.

The objective is to detect suspicious access patterns, produce forensic evidence, classify the incident, identify patient zero, recommend containment and support human-in-the-loop response.

## 2. Architecture

The platform follows an end-to-end DFIR pipeline:

Raw logs → Evidence integrity → Parsing → Feature engineering → IDOR detection → Anomaly detection → Forensic package → LangGraph agents → Human approval → NIST response → Observability.

## 3. Investigation Methodology

The methodology combines deterministic detection, anomaly detection, forensic evidence generation and agentic reasoning.

## 4. Data Pipeline

Processed logs: **{pipeline.get("n_logs_processed")}**

Analyzed IPs: **{pipeline.get("n_ips_analyzed")}**

IDOR findings: **{pipeline.get("n_idor_findings")}**

Anomalous IPs: **{pipeline.get("n_anomalous_ips")}**

IOCs generated: **{pipeline.get("n_iocs_generated")}**

![Pipeline Metrics]({figures.get("pipeline_metrics")})

## 5. IDOR Detection

The platform detects high-volume invoice enumeration, sequential object access, token reuse and behavioral indicators compatible with Broken Access Control.

## 6. Anomaly Detection

Isolation Forest is used to identify anomalous IP behavior and support prioritization.

## 7. Forensic Evidence

Attack start: **{questions.get("when_did_it_start")}**

Attack end: **{questions.get("when_did_it_end")}**

Invoices involved: **{questions.get("how_many_invoices")}**

Attack events: **{questions.get("how_many_attack_events")}**

Patient zero candidate: **{questions.get("patient_zero_candidate")}**

Automated: **{questions.get("was_it_automated")}**

## 8. GenAI Agents and LangGraph

The platform includes Triage, Forensic Analyst, Response Advisor and Human Approval agents orchestrated through LangGraph.

Human-in-the-loop supports approve, reject, modify and request_more_evidence scenarios.

![Agent Metrics]({figures.get("agent_metrics")})

## 9. NIST Incident Response

Severity: **{incident.get("severity")}**

Priority: **{incident.get("priority")}**

Dry-run: **{incident.get("dry_run")}**

The NIST response layer generates TTD, TTR, TTC, containment strategy and root cause analysis.

## 10. Observability

Platform health: **{healthcheck.get("overall_status")}**

Agent decisions: **{agent_metrics.get("n_agent_decisions")}**

Tool calls: **{agent_metrics.get("n_tool_calls")}**

Dry-run actions: **{agent_metrics.get("n_dry_run_actions")}**

## 11. Evaluation

Overall evaluation coverage: **{eval_summary.get("overall_coverage_percent")}%**

Passed: **{eval_summary.get("passed")}**

Partial: **{eval_summary.get("partial")}**

Failed: **{eval_summary.get("failed")}**

![Agent Coverage]({figures.get("agent_coverage")})

## 12. Limitations

The platform runs in dry-run mode and does not execute destructive production actions.

External MCP servers, production authentication, RBAC, Prometheus/Grafana and Docker Compose are documented as production hardening backlog.

## 13. Next Steps

Recommended next steps include containerization, production observability, RBAC, secrets management, CI/CD, persistent vector database and cloud deployment.
"""


def build_executive_summary(
    *,
    nist_report: dict,
    platform_metrics: dict,
    evaluation_report: dict,
) -> str:

    incident = nist_report.get("incident_summary", {})
    questions = nist_report.get("questions_answered", {})
    pipeline = platform_metrics.get("pipeline_metrics", {})
    eval_summary = evaluation_report.get("summary", {})

    return f"""# Executive Summary — IDOR Incident Response Platform

## What Happened

The platform identified behavior compatible with IDOR exploitation through invoice enumeration.

Severity: **{incident.get("severity")}**

Priority: **{incident.get("priority")}**

## Estimated Impact

Attack window:

- Start: **{questions.get("when_did_it_start")}**
- End: **{questions.get("when_did_it_end")}**

Observed impact:

- Invoices involved: **{questions.get("how_many_invoices")}**
- Attack events: **{questions.get("how_many_attack_events")}**
- Tokens observed: **{questions.get("how_many_tokens")}**
- Patient zero candidate: **{questions.get("patient_zero_candidate")}**

## Operational Results

- Logs processed: **{pipeline.get("n_logs_processed")}**
- IPs analyzed: **{pipeline.get("n_ips_analyzed")}**
- IDOR findings: **{pipeline.get("n_idor_findings")}**
- IOCs generated: **{pipeline.get("n_iocs_generated")}**

## Response

The platform generated a dry-run containment strategy including selective IP challenge/blocking, rate limiting, token review and WAF rule recommendations.

## Governance

Destructive actions require human approval. The system supports approve, reject, modify and request_more_evidence workflows.

## Validation

Evaluation coverage: **{eval_summary.get("overall_coverage_percent")}%**

Passed: **{eval_summary.get("passed")}**

Failed: **{eval_summary.get("failed")}**

## Recommendation

Proceed with object-level authorization fixes, suspicious token rotation, rate limiting and enhanced monitoring.
"""


def build_architecture_doc() -> str:
    return """# Architecture

The platform is organized as a modular DFIR pipeline.

Raw logs are transformed into structured events, features, detections, forensic evidence, agent outputs, response metrics and observability artifacts.

Main modules:

- ingestion
- parsing
- features
- detection
- forensic
- agents
- rag
- mcp_gateway
- ir
- observability
- reporting
"""


def build_methodology_doc() -> str:
    return """# Methodology

The investigation methodology combines:

1. Forensic evidence preservation
2. Structured event parsing
3. Feature engineering
4. IDOR detection
5. Anomaly detection
6. Timeline reconstruction
7. IOC generation
8. Agentic investigation
9. Human approval
10. NIST response analysis
11. Observability and validation
"""


def build_evidence_appendix(
    *,
    artifacts: dict[str, str],
) -> str:
    lines = [
        "# Evidence Appendix",
        "",
        "The following artifacts were generated by the platform:",
        "",
    ]

    for name, path in artifacts.items():
        lines.append(f"- **{name}**: `{path}`")

    return "\n".join(lines)