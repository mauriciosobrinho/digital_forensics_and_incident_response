# IDOR Response Platform

## Digital Forensics & Incident Response Platform

Technical Challenge — Technical Leader, Digital Forensics and Incident Response

---

## Overview

The IDOR Response Platform is an end-to-end DFIR solution designed to investigate, explain, validate and safely respond to IDOR (Insecure Direct Object Reference) incidents.

The platform combines:

- Forensic Data Processing
- IDOR Detection
- Anomaly Detection
- Forensic Evidence Generation
- LangGraph Multi-Agent Investigation
- Human-in-the-loop Approval
- Retrieval-Augmented Generation (RAG)
- MCP-safe Tool Execution
- SOC Copilot
- Agent Evaluation & Validation
- Streamlit Investigation Interface

All containment recommendations operate in **dry-run mode**, ensuring analyst oversight and safe execution.

---

# Architecture

```text
Raw Logs
    │
    ▼
Evidence Integrity
    │
    ▼
URI Parsing
    │
    ▼
Feature Engineering
    │
    ▼
IDOR Detection
    │
    ▼
Anomaly Detection
    │
    ▼
IOC Generation
    │
    ▼
Forensic Evidence Package
    │
    ▼
LangGraph Investigation Agents
    │
    ▼
Human Approval Workflow
    │
    ▼
SOC Copilot
    │
    ▼
Streamlit Interface
    │
    ▼
Agent Evaluation & Validation
```

---

# Challenge Requirements Coverage

| Requirement | Status |
|------------|---------|
| Incident Classification | ✅ |
| Investigation Prioritization | ✅ |
| Hypothesis Generation | ✅ |
| Forensic Analysis | ✅ |
| Patient Zero Identification | ✅ |
| Initial Exploitation Detection | ✅ |
| Automation Assessment | ✅ |
| MITRE ATT&CK Mapping | ✅ |
| Containment Recommendation | ✅ |
| Human Approval | ✅ |
| Mini Playbook | ✅ |
| Explainability | ✅ |
| Dry-run Safety | ✅ |
| RAG Investigation | ✅ |
| MCP-safe Tools | ✅ |

---

# Technology Stack

| Component | Technology |
|------------|------------|
| Language | Python 3.12 |
| Data Processing | Polars |
| Data Format | Parquet |
| Validation | Pydantic v2 |
| ML | Scikit-Learn |
| Anomaly Detection | Isolation Forest |
| Agents | LangGraph |
| LLM Integration | Groq / OpenAI Compatible |
| UI | Streamlit |
| Testing | Pytest |
| Evidence Storage | JSON |
| Workflow Visualization | Mermaid |

---

# Dataset

Input file:

```text
data/raw/three_months.csv
```

Approximate size:

| Metric | Value |
|---------|--------|
| Rows | 4,478,619 |
| Columns | 8 |
| Source | Web access logs |

---

# Input Schema

| Original Column | Normalized |
|-----------------|------------|
| timestamp | timestamp |
| http_staus | status_code |
| http_host | host |
| http_uri | uri |
| http_method | method |
| http_referer | referer |
| http_user_agent | user_agent |
| source_ip | source_ip |

Extracted fields:

- invoice_id
- site_id
- auth_token

---

# Installation

## Clone Repository

```bash
git clone <repository_url>

cd idor-response-platform
```

## Create Virtual Environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv .venv

source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Example:

```env
AGENTS_USE_LLM=true

LLM_PROVIDER=groq

LLM_MODEL=llama-3.3-70b-versatile

LLM_API_KEY=YOUR_KEY

HUMAN_DECISION_SCENARIO=approve
```

Supported approval scenarios:

| Scenario | Description |
|-----------|------------|
| approve | Analyst approves actions |
| reject | Analyst rejects actions |
| modify | Analyst modifies actions |
| request_more_evidence | Analyst requests re-analysis |

---

# Running the Pipeline

```bash
python -m src.app
```

---

# Running Tests

Complete suite:

```bash
pytest -v
```

Compile critical modules:

```bash
python -m py_compile src/app.py

python -m py_compile src/ui/streamlit_app.py
```

---

# Streamlit UI

Launch UI:

```bash
streamlit run src/ui/streamlit_app.py
```

---

# Available Tabs

| Tab | Description |
|-------|------------|
| SOC Chat | Natural language investigation |
| Investigation | Agent outputs |
| Human Approval | Approval workflow |
| Forensic Evidence | Evidence package |
| RAG / MCP Logs | Retrieval and tools |
| Agent Workflow | LangGraph timeline |
| Agent Evaluation | Validation suite |

---

# LangGraph Investigation Agents

## Triage Agent

Responsibilities:

- Severity classification
- Priority assignment
- Initial hypotheses

---

## Forensic Analyst Agent

Responsibilities:

- Patient Zero
- Attack Window
- MITRE Mapping
- Automation Assessment
- Impact Analysis

---

## Response Advisor Agent

Responsibilities:

- Containment Strategy
- False Positive Analysis
- Business Impact
- Response Playbook

---

## Human Approval Agent

Responsibilities:

- Approve
- Reject
- Modify
- Request More Evidence

---

# Human-in-the-loop Workflow

Supported execution paths:

## Approval

```text
Triage
 ↓
Forensic
 ↓
Response
 ↓
Human Approval
 ↓
Approved
```

## Rejection

```text
Triage
 ↓
Forensic
 ↓
Response
 ↓
Human Approval
 ↓
Rejected
```

## Modification

```text
Triage
 ↓
Forensic
 ↓
Response
 ↓
Human Approval
 ↓
Modified Action Plan
```

## Request More Evidence

```text
Triage
 ↓
Forensic
 ↓
Response
 ↓
Human Approval
 ↓
Request More Evidence
 ↓
Forensic
 ↓
Response
 ↓
Human Approval
 ↓
Approved
```

---

# Dry-Run Model

All response actions execute in simulation mode.

Examples:

- IP Blocking
- Token Revocation
- Rate Limiting
- WAF Rules

are generated but never executed automatically.

Benefits:

- Safe experimentation
- Auditability
- Human oversight
- Reproducibility

---

# Generated Artifacts

## Processed Data

```text
data/processed/
```

Artifacts:

| Artifact |
|----------|
| parsed_events.parquet |
| ip_features.parquet |
| risk_scores.parquet |
| anomaly_scores.parquet |
| suspicious_ips.parquet |
| anomalous_ips.parquet |

---

## Forensic Evidence

```text
data/evidence/
```

Artifacts:

| Artifact |
|----------|
| chain_of_custody.json |
| attack_timeline.json |
| iocs.json |
| forensic_evidence.json |
| agent_investigation.json |
| agent_decision_log.json |
| agent_response_playbook.json |
| human_approval_request.json |
| human_approval_decision.json |
| llm_agent_reasoning.json |
| tool_execution_log.json |
| langgraph_workflow.png |
| langgraph_workflow.mmd |

---

## Agent Evaluation

```text
data/evaluation/
```

Artifacts:

| Artifact |
|----------|
| agent_question_bank.json |
| agent_eval_results.json |
| agent_eval_report.json |
| agent_eval_summary.csv |

---

# Agent Evaluation & Validation Suite

Current validation scope:

| Agent | Coverage |
|---------|----------|
| Triage Agent | 100% |
| Forensic Analyst Agent | 100% |
| Response Advisor Agent | 100% |
| Human Approval Agent | 100% |
| LangGraph Workflow | 100% |
| SOC Copilot | 100% |

Overall Challenge Coverage:

```text
100%
```

---

# Project Structure

```text
src/
├── agents/
├── detection/
├── evaluation/
├── forensic/
├── ingestion/
├── observability/
├── parsing/
├── ui/
├── config/
└── utils/

data/
├── raw/
├── processed/
├── evidence/
├── evaluation/
├── memory/
└── knowledge/

tests/

reports/

presentation/

demo/
```

---

# Roadmap

| Sprint | Status |
|----------|--------|
| Sprint 0 | ✅ |
| Sprint 1.1 | ✅ |
| Sprint 1.2 | ✅ |
| Sprint 1.3 | ✅ |
| Sprint 2.x | ✅ |
| Sprint 3.1 | ✅ |
| Sprint 3.2 | ✅ |
| Sprint 3.3 | ✅ |
| Sprint 3.4 | ✅ |
| Sprint 3.5 | ✅ |
| Sprint 3.6 | ✅ |
| Sprint 3.7 | 🚧 |
| Sprint 3.8 | 🚧 |
| Sprint 3.9 | 🚧 |
| Sprint 4.0 | 🚧 |

---

# Future Work

Production hardening backlog:

- Docker Compose
- CI/CD
- Prometheus
- Grafana
- Secrets Management
- RBAC
- Authentication
- Cloud Deployment
- Persistent Vector Database
- External MCP Servers

---

# Author

Maurício Luiz Sobrinho

Technical Challenge

Digital Forensics and Incident Response

Mercado Livre