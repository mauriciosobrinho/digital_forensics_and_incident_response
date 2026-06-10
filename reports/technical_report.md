# IDOR Response Platform — Technical Report

Generated at: 2026-06-10T16:03:23.551126+00:00

## 1. Context and Objective

This project implements a Digital Forensics and Incident Response platform for investigating IDOR incidents.

The objective is to detect suspicious access patterns, produce forensic evidence, classify the incident, identify patient zero, recommend containment and support human-in-the-loop response.

## 2. Architecture

The platform follows an end-to-end DFIR pipeline:

Raw logs → Evidence integrity → Parsing → Feature engineering → IDOR detection → Anomaly detection → Forensic package → LangGraph agents → Human approval → NIST response → Observability.

## 3. Investigation Methodology

The methodology combines deterministic detection, anomaly detection, forensic evidence generation and agentic reasoning.

## 4. Data Pipeline

Processed logs: **4478619**

Analyzed IPs: **5726**

IDOR findings: **182**

Anomalous IPs: **172**

IOCs generated: **586**

![Pipeline Metrics](C:\Users\mlsob\Developer\idor-response-platform\reports\figures\pipeline_metrics.png)

## 5. IDOR Detection

The platform detects high-volume invoice enumeration, sequential object access, token reuse and behavioral indicators compatible with Broken Access Control.

## 6. Anomaly Detection

Isolation Forest is used to identify anomalous IP behavior and support prioritization.

## 7. Forensic Evidence

Attack start: **2020-10-01 00:00:00.000000**

Attack end: **2020-12-31 23:58:00.000000**

Invoices involved: **10221**

Attack events: **96829**

Patient zero candidate: **204.210.158.207**

Automated: **True**

## 8. GenAI Agents and LangGraph

The platform includes Triage, Forensic Analyst, Response Advisor and Human Approval agents orchestrated through LangGraph.

Human-in-the-loop supports approve, reject, modify and request_more_evidence scenarios.

![Agent Metrics](C:\Users\mlsob\Developer\idor-response-platform\reports\figures\agent_metrics.png)

## 9. NIST Incident Response

Severity: **critical**

Priority: **P1**

Dry-run: **True**

The NIST response layer generates TTD, TTR, TTC, containment strategy and root cause analysis.

## 10. Observability

Platform health: **healthy**

Agent decisions: **4**

Tool calls: **65**

Dry-run actions: **6**

## 11. Evaluation

Overall evaluation coverage: **100.0%**

Passed: **15**

Partial: **0**

Failed: **0**

![Agent Coverage](C:\Users\mlsob\Developer\idor-response-platform\reports\figures\agent_coverage.png)

## 12. Limitations

The platform runs in dry-run mode and does not execute destructive production actions.

External MCP servers, production authentication, RBAC, Prometheus/Grafana and Docker Compose are documented as production hardening backlog.

## 13. Next Steps

Recommended next steps include containerization, production observability, RBAC, secrets management, CI/CD, persistent vector database and cloud deployment.
