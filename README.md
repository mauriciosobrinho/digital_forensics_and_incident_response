# IDOR Response Platform

<p align="center">
  <strong>IDOR Response Platform</strong><br/>
  Digital Forensics & Incident Response · GenAI Agents · Human-in-the-loop · NIST IR · SOC Observability
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.12-blue">
  <img alt="Polars" src="https://img.shields.io/badge/Polars-Data%20Processing-orange">
  <img alt="LangGraph" src="https://img.shields.io/badge/LangGraph-Agent%20Orchestration-purple">
  <img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-SOC%20UI-red">
  <img alt="Pytest" src="https://img.shields.io/badge/Pytest-36%20tests%20passing-green">
  <img alt="Status" src="https://img.shields.io/badge/Project-Sprint%204.0%20in%20progress-yellow">
</p>

---

## Digital Forensics & Incident Response Platform

Technical Challenge — Technical Leader, Digital Forensics and Incident Response
Mercado Livre / Mercado Libre Cybersecurity Case

---

## Overview

The **IDOR Response Platform** is an end-to-end Digital Forensics and Incident Response platform designed to investigate, explain, validate and safely respond to **IDOR — Insecure Direct Object Reference** incidents.

The project was built as a complete DFIR/SOC investigation platform, combining:

* Forensic ingestion
* Chain of custody
* URI parsing
* Feature engineering
* IDOR detection
* Risk scoring
* Anomaly detection
* IOC generation
* Forensic evidence packaging
* LangGraph multi-agent orchestration
* Human-in-the-loop approval
* Dry-run containment simulation
* RAG-based SOC Copilot
* MCP-safe tool execution
* NIST incident response metrics
* Observability and SOC monitoring
* Automated reporting

All containment actions are executed in **dry-run mode**, ensuring safety, auditability and human oversight.

---

## Challenge Requirements Coverage

| Challenge Requirement        | Platform Capability                    | Status |
| ---------------------------- | -------------------------------------- | ------ |
| Incident classification      | Triage Agent                           | ✅      |
| Severity classification      | Risk scoring + Triage Agent            | ✅      |
| Hypothesis generation        | Triage Agent                           | ✅      |
| Investigation prioritization | Risk score + anomaly convergence       | ✅      |
| Forensic analysis            | Forensic Analyst Agent                 | ✅      |
| Patient zero identification  | Forensic evidence package              | ✅      |
| Initial exploitation window  | Attack timeline                        | ✅      |
| Automation assessment        | Bot/anomaly/sequential access analysis | ✅      |
| MITRE ATT&CK mapping         | Forensic Analyst Agent                 | ✅      |
| Immediate containment        | Response Advisor Agent                 | ✅      |
| Strategic containment        | NIST IR layer                          | ✅      |
| Human approval               | Human Approval Agent                   | ✅      |
| Dry-run execution            | Safe simulated tools                   | ✅      |
| Decision logging             | Agent decision log                     | ✅      |
| Workflow state machine       | LangGraph workflow                     | ✅      |
| Workflow re-entry            | Request more evidence scenario         | ✅      |
| Response metrics             | TTD / TTR / TTC                        | ✅      |
| Dashboards / metrics         | Streamlit + observability artifacts    | ✅      |
| Final reports                | Technical report + executive summary   | ✅      |

---

## High-Level Architecture

```text
Raw Web Logs
    │
    ▼
Evidence Integrity / Chain of Custody
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
Risk Scoring
    │
    ▼
Anomaly Detection
    │
    ▼
Forensic Evidence Package
    │
    ▼
LangGraph Investigation Agents
    │
    ├── Triage Agent
    ├── Forensic Analyst Agent
    ├── Response Advisor Agent
    └── Human Approval Agent
    │
    ▼
Human-in-the-loop Workflow
    │
    ▼
NIST Incident Response Metrics
    │
    ▼
Observability & SOC Monitoring
    │
    ▼
SOC Copilot / Streamlit UI
    │
    ▼
Technical Reports & Executive Summary
```

---

## Technology Stack

| Layer                  | Technology                          |
| ---------------------- | ----------------------------------- |
| Language               | Python 3.12                         |
| Data processing        | Polars                              |
| Storage format         | Parquet                             |
| Validation             | Pydantic v2                         |
| ML / anomaly detection | Scikit-learn / Isolation Forest     |
| Agent orchestration    | LangGraph                           |
| LLM interface          | OpenAI-compatible API via LangChain |
| UI                     | Streamlit                           |
| Testing                | Pytest                              |
| Reporting              | Markdown + Matplotlib figures       |
| Evidence format        | JSON                                |
| Workflow visualization | Mermaid / PNG                       |

---

## Dataset

Input file:

```text
data/raw/three_months.csv
```

Observed dataset size:

| Metric         |     Value |
| -------------- | --------: |
| Raw events     | 4,478,619 |
| Columns        |         8 |
| Analyzed IPs   |     5,726 |
| IDOR findings  |       182 |
| Anomalous IPs  |       172 |
| Generated IOCs |       586 |

---

## Input Schema

| Original Column   | Normalized Column |
| ----------------- | ----------------- |
| `timestamp`       | `timestamp`       |
| `http_staus`      | `status_code`     |
| `http_host`       | `host`            |
| `http_uri`        | `uri`             |
| `http_method`     | `method`          |
| `http_referer`    | `referer`         |
| `http_user_agent` | `user_agent`      |
| `source_ip`       | `source_ip`       |

Extracted URI fields:

| Field        | Description                                               |
| ------------ | --------------------------------------------------------- |
| `invoice_id` | Direct object identifier used for invoice access analysis |
| `site_id`    | Site/country/business context identifier                  |
| `auth_token` | Token-like value observed in request URI                  |

---

## Project Structure

```text
src/
├── agents/
│   ├── conversation_agent.py
│   ├── conversation_memory.py
│   ├── export_graph.py
│   ├── forensic_agent.py
│   ├── graph.py
│   ├── human_approval_agent.py
│   ├── human_decision_simulator.py
│   ├── interactive_console.py
│   ├── llm_client.py
│   ├── response_agent.py
│   ├── response_formatter.py
│   ├── runner.py
│   ├── soc_assistant.py
│   ├── state.py
│   ├── triage_agent.py
│   └── workflow.py
│
├── config/
│   ├── llm_settings.py
│   └── settings.py
│
├── detection/
│   ├── anomaly_detector.py
│   ├── bot_detector.py
│   ├── idor_detector.py
│   ├── isolation_forest.py
│   └── risk_scoring.py
│
├── evaluation/
│   ├── agent_evaluator.py
│   ├── evaluation_report.py
│   ├── question_bank.py
│   └── scoring.py
│
├── forensic/
│   ├── evidence_builder.py
│   ├── ioc_generator.py
│   └── timeline.py
│
├── ingestion/
│   ├── integrity.py
│   └── loader.py
│
├── ir/
│   ├── containment_strategy.py
│   ├── nist_lifecycle.py
│   ├── response_metrics.py
│   ├── root_cause_analysis.py
│   └── runner.py
│
├── mcp_gateway/
│   └── safe_tools.py
│
├── memory/
│   └── investigation_memory.py
│
├── models/
│   ├── events.py
│   └── features.py
│
├── observability/
│   ├── agent_metrics.py
│   ├── healthcheck.py
│   ├── platform_metrics.py
│   ├── runner.py
│   └── soc_dashboard_data.py
│
├── parsing/
│   └── uri_parser.py
│
├── rag/
│   ├── local_retriever.py
│   └── knowledge_base.py
│
├── reporting/
│   ├── figures.py
│   ├── markdown_builder.py
│   ├── pdf_exporter.py
│   ├── report_data_loader.py
│   └── runner.py
│
├── response/
│   └── playbook.py
│
├── tools/
│   └── response_tools.py
│
├── ui/
│   └── streamlit_app.py
│
├── utils/
│   └── filesystem.py
│
└── app.py

data/
├── raw/
├── processed/
├── evidence/
├── evaluation/
├── observability/
├── memory/
└── knowledge/

reports/
├── technical_report.md
├── executive_summary.md
├── architecture.md
├── methodology.md
├── evidence_appendix.md
└── figures/
    ├── agent_coverage.png
    ├── agent_metrics.png
    ├── pipeline_metrics.png
    └── streamlit_ui.png

tests/
├── test_agent_evaluation.py
├── test_agents.py
├── test_anomaly_detection.py
├── test_conversation_agent.py
├── test_detection.py
├── test_forensic.py
├── test_human_approval.py
├── test_human_orchestration.py
├── test_integrity.py
├── test_nist_ir.py
├── test_observability.py
├── test_reporting.py
└── test_uri_parser.py
```

---

## Setup and Installation

### Clone Repository

```bash
git clone <repository_url>

cd idor-response-platform
```

### Create Virtual Environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux / macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file at the project root.

### Deterministic mode for tests and final validation

Recommended for `pytest` and reproducible pipeline runs:

```env
AGENTS_USE_LLM=false
AGENTS_DRY_RUN=true
HUMAN_APPROVAL_MODE=simulated
HUMAN_DECISION_SCENARIO=approve
LANGGRAPH_CHECKPOINT_BACKEND=memory
```

### LLM-enabled mode

Used for SOC Copilot and agent reasoning experiments:

```env
AGENTS_USE_LLM=true
AGENTS_DRY_RUN=true
HUMAN_APPROVAL_MODE=simulated
HUMAN_DECISION_SCENARIO=approve
LANGGRAPH_CHECKPOINT_BACKEND=memory

LLM_PROVIDER=groq
LLM_MODEL=llama-3.3-70b-versatile
LLM_API_KEY=your_api_key_here
LLM_BASE_URL=https://api.groq.com/openai/v1
```

---

## Human Decision Scenarios

| Scenario                | Behavior                                    |
| ----------------------- | ------------------------------------------- |
| `approve`               | Human reviewer approves dry-run containment |
| `reject`                | Human reviewer rejects containment          |
| `modify`                | Human reviewer modifies the response plan   |
| `request_more_evidence` | Workflow re-enters forensic analysis        |

Example:

```env
HUMAN_DECISION_SCENARIO=request_more_evidence
```

Expected result:

```text
human_loop_count = 1
decision_log = 7
```

---

---

## Human-in-the-Loop Validation

The platform supports simulated human intervention through a LangGraph state machine. The human reviewer can approve, reject, modify or request additional evidence before containment is approved.

### Validated scenarios

| Scenario | Expected Evidence | Interpretation |
| --- | --- | --- |
| `approve` | `human_loop_count = 0`, `decision_log = 4` | Linear approval flow |
| `reject` | `workflow_stage = rejected`, `decision_log = 4` | Containment is interrupted |
| `modify` | `modified_action_plan != {}`, `decision_log = 4` | Human reviewer changes the response plan |
| `request_more_evidence` | `human_loop_count = 1`, `decision_log = 7` | Workflow re-enters forensic analysis |

### Re-entry workflow

```text
Triage
  ↓
Forensic Analysis
  ↓
Response Advice
  ↓
Human Approval
  ↓
Request More Evidence
  ↓
Forensic Re-analysis
  ↓
Response Advice
  ↓
Human Approval
  ↓
Approved
```

This validates the most important governance requirement of the challenge: the platform does not blindly execute containment. It allows a human analyst to request additional forensic evidence and resumes the investigation before approval.


## LLM Provider Examples

The platform uses an OpenAI-compatible client interface for most providers. In most cases, change only:

```env
LLM_PROVIDER
LLM_MODEL
LLM_API_KEY
LLM_BASE_URL
```

### Groq OpenAI-compatible API key and settings

```env
AGENTS_USE_LLM=true

LLM_PROVIDER=groq
LLM_API_KEY=gsk_...
LLM_MODEL=llama-3.3-70b-versatile
LLM_BASE_URL=https://api.groq.com/openai/v1
```

### OpenAI API key and settings

```env
AGENTS_USE_LLM=true

LLM_PROVIDER=openai
LLM_API_KEY=sk-proj-...
LLM_MODEL=gpt-4.1-mini
LLM_BASE_URL=
```

### OpenRouter API key and settings

```env
AGENTS_USE_LLM=true

LLM_PROVIDER=openrouter
LLM_API_KEY=sk-or-...
LLM_MODEL=openai/gpt-4.1-mini
LLM_BASE_URL=https://openrouter.ai/api/v1
```

### Anthropic Claude Sonnet via OpenRouter

```env
AGENTS_USE_LLM=true

LLM_PROVIDER=openrouter
LLM_API_KEY=sk-or-...
LLM_MODEL=anthropic/claude-3.5-sonnet
LLM_BASE_URL=https://openrouter.ai/api/v1
```

### Anthropic Claude Haiku via OpenRouter

```env
AGENTS_USE_LLM=true

LLM_PROVIDER=openrouter
LLM_API_KEY=sk-or-...
LLM_MODEL=anthropic/claude-3.5-haiku
LLM_BASE_URL=https://openrouter.ai/api/v1
```

### Anthropic Claude Opus via OpenRouter

```env
AGENTS_USE_LLM=true

LLM_PROVIDER=openrouter
LLM_API_KEY=sk-or-...
LLM_MODEL=anthropic/claude-3-opus
LLM_BASE_URL=https://openrouter.ai/api/v1
```

### Google Gemini native OpenAI-compatible endpoint

```env
AGENTS_USE_LLM=true

LLM_PROVIDER=gemini
LLM_API_KEY=your_gemini_key
LLM_MODEL=gemini-2.5-flash
LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
```

### Google Gemini via OpenRouter

```env
AGENTS_USE_LLM=true

LLM_PROVIDER=openrouter
LLM_API_KEY=sk-or-...
LLM_MODEL=google/gemini-2.5-flash
LLM_BASE_URL=https://openrouter.ai/api/v1
```

### Perplexity OpenAI-compatible API key and settings

```env
AGENTS_USE_LLM=true

LLM_PROVIDER=perplexity
LLM_API_KEY=pplx-...
LLM_MODEL=sonar-pro
LLM_BASE_URL=https://api.perplexity.ai
```

### Perplexity Sonar Reasoning

```env
AGENTS_USE_LLM=true

LLM_PROVIDER=perplexity
LLM_API_KEY=pplx-...
LLM_MODEL=sonar-reasoning-pro
LLM_BASE_URL=https://api.perplexity.ai
```

### xAI Grok

```env
AGENTS_USE_LLM=true

LLM_PROVIDER=xai
LLM_API_KEY=xai-...
LLM_MODEL=grok-3
LLM_BASE_URL=https://api.x.ai/v1
```

### xAI Grok Mini

```env
AGENTS_USE_LLM=true

LLM_PROVIDER=xai
LLM_API_KEY=xai-...
LLM_MODEL=grok-3-mini
LLM_BASE_URL=https://api.x.ai/v1
```

### Local OpenAI-compatible server

Example for local gateways such as LM Studio, Ollama-compatible proxies, LiteLLM, vLLM or local OpenAI-compatible endpoints:

```env
AGENTS_USE_LLM=true

LLM_PROVIDER=local
LLM_API_KEY=local_or_dummy_key
LLM_MODEL=local-model-name
LLM_BASE_URL=http://localhost:1234/v1
```

### Quick provider switching examples

#### OpenRouter + GPT-4.1 Mini

```env
LLM_PROVIDER=openrouter
LLM_API_KEY=sk-or-...
LLM_MODEL=openai/gpt-4.1-mini
LLM_BASE_URL=https://openrouter.ai/api/v1
```

#### OpenRouter + Claude Sonnet

```env
LLM_PROVIDER=openrouter
LLM_API_KEY=sk-or-...
LLM_MODEL=anthropic/claude-3.5-sonnet
LLM_BASE_URL=https://openrouter.ai/api/v1
```

#### OpenRouter + Gemini Flash

```env
LLM_PROVIDER=openrouter
LLM_API_KEY=sk-or-...
LLM_MODEL=google/gemini-2.5-flash
LLM_BASE_URL=https://openrouter.ai/api/v1
```

#### Groq + Llama 3.3 70B

```env
LLM_PROVIDER=groq
LLM_API_KEY=gsk_...
LLM_MODEL=llama-3.3-70b-versatile
LLM_BASE_URL=https://api.groq.com/openai/v1
```

#### Perplexity Sonar Pro

```env
LLM_PROVIDER=perplexity
LLM_API_KEY=pplx-...
LLM_MODEL=sonar-pro
LLM_BASE_URL=https://api.perplexity.ai
```

### Native Claude/Gemini note

For native Claude/Gemini SDKs, the SDK and client implementation may change. If using Claude or Gemini via OpenRouter, the existing OpenAI-compatible code path can be preserved and only the model changes:

```env
LLM_PROVIDER=openrouter
LLM_API_KEY=sk-or-...
LLM_MODEL=anthropic/claude-3.5-sonnet
LLM_BASE_URL=https://openrouter.ai/api/v1
```

or:

```env
LLM_PROVIDER=openrouter
LLM_API_KEY=sk-or-...
LLM_MODEL=google/gemini-2.5-flash
LLM_BASE_URL=https://openrouter.ai/api/v1
```

---

## Running the Full Pipeline

```bash
python -m src.app
```

The pipeline generates:

* processed Parquet datasets
* forensic evidence
* agent investigation outputs
* human approval artifacts
* LangGraph workflow visualization
* evaluation reports
* NIST incident response metrics
* observability artifacts
* final technical reports

---

## Validation Commands

### Compile critical files

```bash
python -m py_compile src/app.py
python -m py_compile src/ui/streamlit_app.py
```

### Run tests

```bash
pytest -v
```

### Run pipeline

```bash
python -m src.app
```

### Run Streamlit UI

```bash
streamlit run src/ui/streamlit_app.py
```

---

## SOC Copilot Consoles

### Analyst console

Natural language interface for investigation:

```bash
python -m src.agents.interactive_console
```

Example questions:

```text
Quais são os top IPs atacantes?
Qual foi a janela do ataque?
Explique IDOR e Broken Access Control.
O ataque apresenta automação?
Quem é o patient zero?
Quais ações de contenção são recomendadas?
Qual foi o resultado da intervenção humana?
Mostre a timeline do workflow.
Houve reentrada no agente forense?
Quais são as métricas TTD, TTR e TTC?
```

### Debug console

Shows raw JSON payloads for inspection:

```bash
python -m src.agents.interactive_console --json
```

Use this mode to validate:

* selected intent
* tool result
* RAG context
* raw structured payload
* generated answer
* evidence references

---

## Streamlit UI

![Streamlit UI](reports/figures/streamlit_ui.png)

Launch:

```bash
streamlit run src/ui/streamlit_app.py
```

### Available Tabs

| Tab                 | Purpose                      | What to Expect                                                    |
| ------------------- | ---------------------------- | ----------------------------------------------------------------- |
| `SOC Chat`          | Natural language SOC Copilot | Ask investigation questions in Portuguese or English              |
| `Investigation`     | Agent investigation output   | Triage, forensic analysis and response advisor JSON               |
| `Human Approval`    | Human-in-the-loop governance | Approval request, approval decision and dry-run status            |
| `Forensic Evidence` | Evidence package             | Chain of custody, summary, attack indicators and forensic context |
| `RAG / MCP Logs`    | Retrieval and safe tool logs | RAG context and MCP-safe tool execution history                   |
| `Agent Workflow`    | LangGraph execution trace    | Workflow timeline, current state and decision transitions         |
| `Agent Evaluation`  | Validation suite             | Overall coverage, passed/partial/failed checks and question bank  |
| `NIST IR Metrics`   | Incident response metrics    | TTD, TTR, TTC, containment strategy and root cause analysis       |
| `Observability`     | SOC monitoring               | Health, pipeline metrics, agent metrics and evidence completeness |

---

---

## Agent Evaluation Results

The platform includes an explicit validation suite that maps challenge requirements to expected evidence in each agent output.

| Agent / Component | Coverage |
| --- | ---: |
| Triage Agent | 100% |
| Forensic Analyst Agent | 100% |
| Response Advisor Agent | 100% |
| Human Approval Agent | 100% |
| LangGraph Workflow | 100% |
| SOC Copilot | 100% |

| Evaluation Metric | Value |
| --- | ---: |
| Total questions | 15 |
| Overall score | 1.0 |
| Overall coverage | 100% |
| Passed | 15 |
| Partial | 0 |
| Failed | 0 |

The validation suite proves that the agentic layer covers classification, hypothesis generation, prioritization, forensic reasoning, patient zero identification, automation assessment, MITRE mapping, containment planning, human approval and workflow re-entry.


---

## Generated Evidence Artifacts

| Artifact | Purpose |
| --- | --- |
| `data/evidence/chain_of_custody.json` | SHA-256 integrity and forensic provenance |
| `data/processed/parsed_events.parquet` | Normalized events and extracted URI fields |
| `data/processed/ip_features.parquet` | IP-level features for investigation and detection |
| `data/processed/idor_findings.parquet` | IDOR-compatible findings |
| `data/processed/anomaly_scores.parquet` | Isolation Forest anomaly scores |
| `data/evidence/attack_timeline.json` | Attack window and timeline reconstruction |
| `data/evidence/iocs.json` | Indicators of compromise |
| `data/evidence/forensic_evidence.json` | Consolidated forensic evidence package |
| `data/evidence/agent_investigation.json` | Consolidated multi-agent investigation output |
| `data/evidence/agent_decision_log.json` | Agent and human decision trail |
| `data/evidence/human_approval_decision.json` | Human approval governance evidence |
| `data/evidence/nist_incident_report.json` | NIST-style incident response report |
| `data/evaluation/agent_eval_report.json` | Agent validation and coverage report |
| `data/observability/platform_metrics.json` | Platform observability metrics |
| `data/observability/soc_dashboard_data.json` | SOC dashboard data |
| `reports/technical_report.md` | Technical report |
| `reports/executive_summary.md` | Executive summary |
| `presentation/technical_pitch.pptx` | Technical presentation deck |
| `presentation/executive_pitch.pptx` | Executive presentation deck |
| `demo/demo_script.md` | Demonstration script |
| `demo/demo_questions.md` | Demo question bank |


## Generated Artifacts

### Processed Data

```text
data/processed/
├── parsed_events.parquet
├── ip_features.parquet
├── idor_findings.parquet
├── risk_scores.parquet
├── suspicious_ips.parquet
├── anomaly_scores.parquet
└── anomalous_ips.parquet
```

### Forensic Evidence

```text
data/evidence/
├── chain_of_custody.json
├── attack_timeline.json
├── iocs.json
├── forensic_evidence.json
├── agent_investigation.json
├── agent_decision_log.json
├── agent_response_playbook.json
├── human_approval_request.json
├── human_approval_decision.json
├── agent_workflow_timeline.json
├── langgraph_workflow.mmd
├── langgraph_workflow.png
├── nist_incident_report.json
├── response_metrics.json
├── containment_strategy.json
└── root_cause_analysis.json
```

### Evaluation

```text
data/evaluation/
├── agent_question_bank.json
├── agent_eval_results.json
├── agent_eval_report.json
└── agent_eval_summary.csv
```

Latest validation:

| Metric           | Value |
| ---------------- | ----: |
| Overall coverage |  100% |
| Passed           |    15 |
| Partial          |     0 |
| Failed           |     0 |

### Observability

```text
data/observability/
├── platform_metrics.json
├── agent_metrics.json
├── healthcheck.json
└── soc_dashboard_data.json
```

Example topline:

```json
{
  "health": "healthy",
  "severity": "critical",
  "priority": "P1",
  "dry_run": true,
  "agent_evaluation_coverage": 100.0
}
```

### Reports

```text
reports/
├── technical_report.md
├── executive_summary.md
├── architecture.md
├── methodology.md
├── evidence_appendix.md
└── figures/
    ├── agent_coverage.png
    ├── agent_metrics.png
    └── pipeline_metrics.png
```

---

## Key Results

| Metric                    |     Value |
| ------------------------- | --------: |
| Logs processed            | 4,478,619 |
| IPs analyzed              |     5,726 |
| IDOR findings             |       182 |
| Anomalous IPs             |       172 |
| IOCs generated            |       586 |
| Agent evaluation coverage |      100% |
| Severity                  |  critical |
| Priority                  |        P1 |
| Dry-run                   |      true |

---

## NIST Incident Response Metrics

| Metric | Meaning         |                  Current Result |
| ------ | --------------- | ------------------------------: |
| TTD    | Time to Detect  | Historical retrospective metric |
| TTR    | Time to Respond |                            0.0h |
| TTC    | Time to Contain |                    0.0h dry-run |

Interpretation:

* TTD is high because the dataset is historical.
* TTR is zero because response recommendations are generated in the same automated pipeline cycle.
* TTC is zero because containment approval is simulated in dry-run during the same execution cycle.

---

## Roadmap

| Sprint     | Description                                          | Status |
| ---------- | ---------------------------------------------------- | ------ |
| Sprint 0   | Architecture and planning                            | ✅      |
| Sprint 1.1 | Evidence ingestion, chain of custody and URI parsing | ✅      |
| Sprint 1.2 | Feature engineering and detection base               | ✅      |
| Sprint 1.3 | Forensic evidence package                            | ✅      |
| Sprint 2.x | IDOR detection, risk scoring and anomaly detection   | ✅      |
| Sprint 3.1 | LangGraph investigation agents                       | ✅      |
| Sprint 3.2 | Human approval and dry-run response                  | ✅      |
| Sprint 3.3 | Streamlit SOC interface                              | ✅      |
| Sprint 3.4 | Natural language SOC Copilot                         | ✅      |
| Sprint 3.5 | Human-in-the-loop orchestration                      | ✅      |
| Sprint 3.6 | Agent evaluation and validation suite                | ✅      |
| Sprint 3.7 | NIST incident response metrics                       | ✅      |
| Sprint 3.8 | Observability and SOC monitoring                     | ✅      |
| Sprint 3.9 | Final technical report and executive summary         | ✅      |
| Sprint 4.0 | Demo package and presentation                        | 🚧 In Progress |

---

## Production Hardening Backlog

The MVP intentionally prioritizes investigation, evidence, agents, explainability, human approval, dry-run safety and incident response.

Production hardening items:

* Docker Compose
* Prometheus
* Grafana
* CI/CD
* Secrets management
* RBAC
* Authentication
* Cloud deployment
* Persistent vector database
* External MCP servers
* Production WAF integration
* SIEM integration
* Case management integration

---

## Recommended Final Validation

Before submitting or presenting:

```bash
python -m py_compile src/app.py
python -m py_compile src/ui/streamlit_app.py
pytest -v
python -m src.app
streamlit run src/ui/streamlit_app.py
```

Recommended deterministic `.env`:

```env
AGENTS_USE_LLM=false
AGENTS_DRY_RUN=true
HUMAN_APPROVAL_MODE=simulated
HUMAN_DECISION_SCENARIO=approve
LANGGRAPH_CHECKPOINT_BACKEND=memory
```

---

## Author

Maurício Luiz Sobrinho

Technical Challenge — Digital Forensics and Incident Response
Mercado Livre / Mercado Libre
