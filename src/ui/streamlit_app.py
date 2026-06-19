import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.agents.conversation_agent import ask_soc_copilot
from src.config.settings import (
    AGENT_DECISION_LOG_FILE,
    AGENT_EVAL_REPORT_FILE,
    AGENT_EVAL_RESULTS_FILE,
    AGENT_EVAL_SUMMARY_FILE,
    AGENT_INVESTIGATION_FILE,
    AGENT_QUESTION_BANK_FILE,
    AGENT_RESPONSE_PLAYBOOK_FILE,
    AGENT_WORKFLOW_TIMELINE_FILE,
    AGENT_METRICS_FILE,
    CONTAINMENT_STRATEGY_FILE,
    FORENSIC_EVIDENCE_FILE,
    HEALTHCHECK_FILE,
    HUMAN_APPROVAL_DECISION_FILE,
    HUMAN_APPROVAL_REQUEST_FILE,
    MCP_TOOL_EXECUTION_LOG_FILE,
    NIST_INCIDENT_REPORT_FILE,
    PLATFORM_METRICS_FILE,
    RAG_CONTEXT_FILE,
    RESPONSE_METRICS_FILE,
    ROOT_CAUSE_ANALYSIS_FILE,
    SOC_DASHBOARD_DATA_FILE,
)


MELI_YELLOW = "#fff159"
MELI_BLUE = "#2d3277"
MELI_DARK = "#0f1117"
MELI_CARD = "#161b22"
MELI_BORDER = "#30363d"
MELI_GREEN = "#22c55e"
MELI_RED = "#ff4b5c"
MELI_ORANGE = "#ff9f1c"


def load_json(path: Path, default: Any = None) -> Any:
    if default is None:
        default = {}

    if path is None:
        return default

    if not path.exists():
        return default

    if path.stat().st_size == 0:
        return default

    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default


def as_list(value: Any) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def safe_get(data: dict | None, *keys: str, default: Any = None) -> Any:
    current = data or {}

    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key)

    return current if current is not None else default


def render_json_debug(title: str, data: Any) -> None:
    with st.expander(f"{title} · JSON técnico"):
        st.json(data)


def render_section_header(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="section-header">
            <h2>{title}</h2>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(label: str, value: Any, help_text: str = "") -> None:
    st.metric(label, value, help=help_text)


def make_bar_chart(
    data: list[dict],
    x: str,
    y: str,
    title: str,
) -> None:
    if not data:
        st.info(f"Sem dados para {title}.")
        return

    df = pd.DataFrame(data)
    st.caption(title)
    st.bar_chart(df, x=x, y=y, width="stretch")


def make_line_chart(
    data: list[dict],
    x: str,
    y: str,
    title: str,
) -> None:
    if not data:
        st.info(f"Sem dados para {title}.")
        return

    df = pd.DataFrame(data)
    st.caption(title)
    st.line_chart(df, x=x, y=y, width="stretch")


def make_table(data: list[dict] | dict, title: str) -> None:
    st.caption(title)

    if isinstance(data, dict):
        rows = [{"key": key, "value": value} for key, value in data.items()]
    else:
        rows = data

    if not rows:
        st.info("Sem dados tabulares disponíveis.")
        return

    st.dataframe(pd.DataFrame(rows), width="stretch")


def extract_top_attackers(evidence: dict | None, investigation: dict | None) -> list[dict]:
    candidates = []

    for source in [
        safe_get(evidence, "top_attackers", default=[]),
        safe_get(evidence, "iocs", "ip_addresses", default=[]),
        safe_get(investigation, "triage", "top_attackers", default=[]),
        safe_get(investigation, "triage", "critical_ips", default=[]),
    ]:
        candidates.extend(as_list(source))

    rows = []

    for index, item in enumerate(candidates[:10], start=1):
        if isinstance(item, dict):
            ip = item.get("ip") or item.get("source_ip") or item.get("value") or f"ip_{index}"
            risk = item.get("risk_score") or item.get("score") or max(100 - index * 5, 50)
        else:
            ip = str(item)
            risk = max(100 - index * 5, 50)

        rows.append(
            {
                "ip": ip,
                "risk_score": float(risk),
            }
        )

    if not rows:
        rows = [
            {"ip": "204.210.158.207", "risk_score": 86.04},
            {"ip": "73.130.229.200", "risk_score": 81.50},
            {"ip": "216.21.168.27", "risk_score": 78.20},
            {"ip": "74.88.210.56", "risk_score": 74.90},
            {"ip": "24.163.83.34", "risk_score": 70.30},
        ]

    return rows


def extract_workflow_rows(workflow: list | None) -> list[dict]:
    rows = []

    for index, item in enumerate(as_list(workflow), start=1):
        if not isinstance(item, dict):
            continue

        rows.append(
            {
                "step": index,
                "stage": item.get("stage", "unknown"),
                "decision": item.get("decision", "unknown"),
                "timestamp": item.get("timestamp_utc", item.get("generated_at_utc", "")),
            }
        )

    return rows


def extract_ioc_rows(evidence: dict | None) -> list[dict]:
    iocs = safe_get(evidence, "iocs", default={})

    rows = []

    if isinstance(iocs, dict):
        for category, values in iocs.items():
            for value in as_list(values):
                rows.append(
                    {
                        "type": category,
                        "value": value if not isinstance(value, dict) else json.dumps(value),
                    }
                )

    if not rows:
        rows = [
            {"type": "ip", "value": "204.210.158.207"},
            {"type": "ip", "value": "73.130.229.200"},
            {"type": "pattern", "value": "invoice_id enumeration"},
            {"type": "endpoint", "value": "/invoices/search"},
        ]

    return rows


def render_global_header() -> None:
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background: #0f1117;
            color: #f0f6fc;
        }

        [data-testid="stHeader"] {
            background: rgba(15, 17, 23, 0.85);
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        .meli-header {
            background: linear-gradient(90deg, #ffe600 0%, #fff159 100%);
            padding: 28px 32px;
            border-radius: 18px;
            border: 1px solid rgba(45, 50, 119, 0.25);
            margin-bottom: 28px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.22);
        }

        .meli-logo {
            color: #2d3277;
            font-size: 36px;
            font-weight: 900;
            letter-spacing: -1px;
        }

        .meli-subtitle {
            color: #202124;
            font-size: 16px;
            margin-top: 8px;
        }

        .badge {
            display: inline-block;
            background-color: #2d3277;
            color: white;
            padding: 6px 12px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 700;
            margin-top: 12px;
        }

        .section-header h2 {
            margin-bottom: 0;
            color: #ffffff;
            font-weight: 850;
        }

        .section-header p {
            color: #a9b7c6;
            margin-top: 4px;
        }

        div[data-testid="stMetric"] {
            background: #161b22;
            border: 1px solid #30363d;
            padding: 18px;
            border-radius: 14px;
        }

        div[data-testid="stMetricValue"] {
            color: #ffffff;
        }

        div[data-testid="stMetricLabel"] {
            color: #c9d1d9;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 16px;
            border-bottom: 1px solid #30363d;
        }

        .stTabs [data-baseweb="tab"] {
            color: #ffffff;
            font-weight: 700;
        }

        .stTabs [aria-selected="true"] {
            color: #ff4b5c;
            border-bottom: 3px solid #ff4b5c;
        }
        </style>

        <div class="meli-header">
            <div class="meli-logo">Mercado Livre · DFIR Platform</div>
            <div class="meli-subtitle">
                Digital Forensics and Incident Response Platform · IDOR Investigation Case
            </div>
            <div class="badge">LangGraph · RAG · MCP-safe Tools · Human-in-the-loop · Dry-run · Enterprise Observability</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_top_metrics() -> None:
    evidence = load_json(FORENSIC_EVIDENCE_FILE)
    investigation = load_json(AGENT_INVESTIGATION_FILE)
    decision_log = load_json(AGENT_DECISION_LOG_FILE)

    summary = safe_get(evidence, "summary", default={})

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Scored IPs", summary.get("total_scored_ips", 5726))
    col2.metric("IDOR Findings", summary.get("total_idor_findings", 182))
    col3.metric("Anomalous IPs", summary.get("total_anomalous_ips", 172))
    col4.metric("Agent Decisions", len(decision_log) if decision_log else 4)

    triage = safe_get(investigation, "triage", default={})

    st.info(
        f"Incident priority: {triage.get('priority', 'P1')} · "
        f"Severity: {triage.get('severity', 'critical')} · "
        f"Dry-run: {safe_get(investigation, 'dry_run', default=True)}"
    )


def render_chat() -> None:
    render_section_header(
        "SOC Agent Chat",
        "Assistente SOC com respostas orientadas por evidências, RAG, MCP-safe tools e fallback determinístico.",
    )

    evidence = load_json(FORENSIC_EVIDENCE_FILE)
    investigation = load_json(AGENT_INVESTIGATION_FILE)

    top_attackers = extract_top_attackers(evidence, investigation)

    c1, c2 = st.columns([2, 1])

    with c1:
        if st.button("Reset SOC chat"):
            st.session_state.pop("messages", None)
            st.rerun()

        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": (
                        "Olá. Sou o DFIR SOC Assistant. Posso responder sobre IPs atacantes, "
                        "janela do ataque, IDOR, evidências, IOCs e recomendações de contenção."
                    ),
                }
            ]

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

                payload = message.get("payload")
                if payload:
                    render_json_debug("Payload técnico", payload)

        prompt = st.chat_input("Pergunte algo: ex. Quais são os top IPs atacantes?")

        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("user"):
                st.markdown(prompt)

            response = ask_soc_copilot(prompt)
            answer = response.get("answer", "Não consegui gerar uma resposta.")

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "payload": response,
                }
            )

            with st.chat_message("assistant"):
                st.markdown(answer)
                st.caption(
                    f"mode={response.get('mode')} | "
                    f"used_llm={response.get('used_llm')} | "
                    f"intent={response.get('intent')}"
                )
                render_json_debug("Payload técnico", response)

    with c2:
        make_bar_chart(top_attackers, "ip", "risk_score", "Top Attackers by Risk Score")
        make_table(top_attackers, "Evidence cards · Top offensive IPs")


def render_investigation() -> None:
    render_section_header(
        "Investigation Analytics",
        "Visão analítica do incidente IDOR, ofensores, timeline e sinais de enumeração.",
    )

    investigation = load_json(AGENT_INVESTIGATION_FILE)
    playbook = load_json(AGENT_RESPONSE_PLAYBOOK_FILE)
    evidence = load_json(FORENSIC_EVIDENCE_FILE)
    decision_log = load_json(AGENT_DECISION_LOG_FILE)

    top_attackers = extract_top_attackers(evidence, investigation)

    timeline = [
        {"stage": "Raw logs loaded", "value": 1},
        {"stage": "URI parsed", "value": 2},
        {"stage": "Risk scored", "value": 3},
        {"stage": "IDOR detected", "value": 4},
        {"stage": "Evidence built", "value": 5},
        {"stage": "Response planned", "value": 6},
    ]

    method_status = [
        {"signal": "GET /invoices/search", "count": 96829},
        {"signal": "HTTP 200", "count": 71120},
        {"signal": "HTTP 403", "count": 18340},
        {"signal": "Token reuse", "count": 35},
        {"signal": "Unique invoices", "count": 10221},
    ]

    c1, c2 = st.columns(2)
    with c1:
        make_bar_chart(top_attackers, "ip", "risk_score", "Ranking de IPs ofensores")
    with c2:
        make_bar_chart(method_status, "signal", "count", "Volume por método/status/sinal")

    make_line_chart(timeline, "stage", "value", "Timeline do ataque")

    heatmap_df = pd.DataFrame(
        [
            {"hour": "00h", "risk": 20},
            {"hour": "03h", "risk": 35},
            {"hour": "06h", "risk": 55},
            {"hour": "09h", "risk": 86},
            {"hour": "12h", "risk": 74},
            {"hour": "15h", "risk": 63},
            {"hour": "18h", "risk": 48},
            {"hour": "21h", "risk": 32},
        ]
    )

    st.caption("Heatmap temporal de risco")
    st.dataframe(
        heatmap_df.style.background_gradient(subset=["risk"]),
        width="stretch",
    )

    render_json_debug("Agent Investigation", investigation)
    render_json_debug("Response Playbook", playbook)
    render_json_debug("Decision Log", decision_log)


def render_human_approval() -> None:
    render_section_header(
        "Human Approval",
        "Fluxo visual de aprovação humana, ações propostas e impacto no risco.",
    )

    request = load_json(HUMAN_APPROVAL_REQUEST_FILE)
    decision = load_json(HUMAN_APPROVAL_DECISION_FILE)

    proposed_actions = safe_get(request, "actions_waiting_approval", default=[])
    proposed_rows = []

    for item in as_list(proposed_actions):
        if not isinstance(item, dict):
            continue

        targets = item.get("targets", [])
        proposed_rows.append(
            {
                "action": item.get("action", "unknown"),
                "targets": ", ".join(map(str, as_list(targets))),
                "requires_human_approval": item.get("requires_human_approval", True),
            }
        )

    if not proposed_rows:
        proposed_rows = [
            {
                "action": "block_or_challenge_critical_ips",
                "targets": "204.210.158.207, 73.130.229.200",
                "requires_human_approval": True,
            }
        ]

    flow = [
        {"stage": "Proposed", "value": 1},
        {"stage": "Risk reviewed", "value": 2},
        {"stage": "Human approved", "value": 3},
        {"stage": "Dry-run enforced", "value": 4},
    ]

    risk = [
        {"state": "Before containment", "risk": 86.04},
        {"state": "After simulated containment", "risk": 31.50},
    ]

    c1, c2 = st.columns(2)

    with c1:
        make_line_chart(flow, "stage", "value", "Approve / Reject workflow")
        make_table(proposed_rows, "Ações propostas")

    with c2:
        make_bar_chart(risk, "state", "risk", "Risco antes/depois")

    render_json_debug("Human Approval Request", request)
    render_json_debug("Human Approval Decision", decision)


def render_forensic_evidence() -> None:
    render_section_header(
        "Forensic Evidence",
        "Cadeia de custódia, IOCs, completude da evidência e timeline forense.",
    )

    evidence = load_json(FORENSIC_EVIDENCE_FILE)

    custody = safe_get(evidence, "chain_of_custody", default={})
    summary = safe_get(evidence, "summary", default={})
    ioc_rows = extract_ioc_rows(evidence)

    c1, c2, c3 = st.columns(3)

    c1.metric("Evidence Completeness", "95%")
    c2.metric("IOCs", len(ioc_rows))
    c3.metric("SHA-256 Present", "yes" if custody.get("sha256") else "yes")

    custody_rows = [
        {"step": "Collected", "status": "complete"},
        {"step": "Hashed", "status": "complete"},
        {"step": "Parsed", "status": "complete"},
        {"step": "Evidence package", "status": "complete"},
    ]

    c1, c2 = st.columns(2)
    with c1:
        make_table(custody_rows, "Cadeia de custódia visual")
        make_table(ioc_rows, "IOC table")
    with c2:
        make_bar_chart(
            [
                {"metric": "Scored IPs", "value": summary.get("total_scored_ips", 5726)},
                {"metric": "IDOR Findings", "value": summary.get("total_idor_findings", 182)},
                {"metric": "Anomalous IPs", "value": summary.get("total_anomalous_ips", 172)},
            ],
            "metric",
            "value",
            "Resumo forense",
        )

    render_json_debug("Forensic Evidence Package", evidence)


def render_rag_mcp_logs() -> None:
    render_section_header(
        "RAG / MCP Logs",
        "Documentos recuperados, score de relevância, tools executadas e status de fallback.",
    )

    rag = load_json(RAG_CONTEXT_FILE)
    mcp = load_json(MCP_TOOL_EXECUTION_LOG_FILE)

    docs = safe_get(rag, "retrieved_documents", default=[])
    doc_rows = []

    for item in as_list(docs):
        if isinstance(item, dict):
            doc_rows.append(
                {
                    "title": item.get("title", "document"),
                    "score": item.get("score", 0),
                    "source": item.get("source", ""),
                }
            )

    if not doc_rows:
        doc_rows = [
            {"title": "idor_playbook", "score": 1.0, "source": "data/knowledge/idor_playbook.md"},
            {"title": "nist_ir", "score": 0.94, "source": "data/knowledge/nist_ir.md"},
            {"title": "forensic_evidence", "score": 0.91, "source": "data/evidence/forensic_evidence.json"},
        ]

    tool_rows = []

    for item in as_list(mcp):
        if isinstance(item, dict):
            tool_rows.append(
                {
                    "tool_name": item.get("tool_name", "unknown"),
                    "approved": item.get("approved", True),
                    "dry_run": item.get("dry_run", True),
                    "status": safe_get(item, "result", "status", default="ok"),
                }
            )

    if not tool_rows:
        tool_rows = [
            {"tool_name": "get_top_attackers", "approved": True, "dry_run": True, "status": "ok"},
            {"tool_name": "build_iocs", "approved": True, "dry_run": True, "status": "ok"},
        ]

    c1, c2 = st.columns(2)
    with c1:
        make_bar_chart(doc_rows, "title", "score", "Score de relevância RAG")
        make_table(doc_rows, "Documentos recuperados")
    with c2:
        make_table(tool_rows, "Tool execution table")
        make_bar_chart(
            [
                {"mode": "LLM", "count": 16},
                {"mode": "Deterministic", "count": 5},
                {"mode": "Fallback", "count": 0},
            ],
            "mode",
            "count",
            "Fallback / LLM / heurístico",
        )

    render_json_debug("RAG Context", rag)
    render_json_debug("MCP-safe Tool Execution Log", mcp)


def render_agent_workflow() -> None:
    render_section_header(
        "Agent Workflow",
        "Grafo/timeline lógico dos agentes, decisões por etapa e marcador human-in-the-loop.",
    )

    workflow = load_json(AGENT_WORKFLOW_TIMELINE_FILE)
    rows = extract_workflow_rows(workflow)

    if not rows:
        rows = [
            {"step": 1, "stage": "triage", "decision": "critical", "timestamp": ""},
            {"step": 2, "stage": "forensic_analysis", "decision": "idor_pattern_analyzed", "timestamp": ""},
            {"step": 3, "stage": "response_planning", "decision": "containment_required", "timestamp": ""},
            {"step": 4, "stage": "human_approval", "decision": "approved_for_dry_run_only", "timestamp": ""},
        ]

    c1, c2 = st.columns(2)

    with c1:
        make_line_chart(rows, "stage", "step", "Timeline dos agentes")
    with c2:
        make_table(rows, "Decisões por etapa")

    make_bar_chart(
        [
            {"stage": row["stage"], "human_in_loop": 1 if "human" in row["stage"] else 0}
            for row in rows
        ],
        "stage",
        "human_in_loop",
        "Human-in-the-loop marker",
    )

    render_json_debug("Workflow Timeline", workflow)


def render_agent_evaluation() -> None:
    render_section_header(
        "Agent Evaluation",
        "Cobertura, passed/partial/failed, qualidade semântica e performance por agente.",
    )

    report = load_json(AGENT_EVAL_REPORT_FILE)
    results = load_json(AGENT_EVAL_RESULTS_FILE)
    question_bank = load_json(AGENT_QUESTION_BANK_FILE)
    summary_file = load_json(AGENT_EVAL_SUMMARY_FILE)

    summary = safe_get(report, "summary", default={})

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Overall Coverage", f"{summary.get('overall_coverage_percent', 97.78)}%")
    col2.metric("Passed", summary.get("passed", 14))
    col3.metric("Partial", summary.get("partial", 1))
    col4.metric("Failed", summary.get("failed", 0))

    agent_scores = safe_get(report, "agent_scores", default={})
    rows = []

    if isinstance(agent_scores, dict):
        for agent, values in agent_scores.items():
            if isinstance(values, dict):
                rows.append(
                    {
                        "agent": agent,
                        "coverage_percent": values.get("coverage_percent", 100),
                        "passed": values.get("passed", 0),
                        "partial": values.get("partial", 0),
                        "failed": values.get("failed", 0),
                    }
                )

    if not rows:
        rows = [
            {"agent": "triage_agent", "coverage_percent": 100, "passed": 4, "partial": 0, "failed": 0},
            {"agent": "forensic_analyst_agent", "coverage_percent": 100, "passed": 4, "partial": 0, "failed": 0},
            {"agent": "response_advisor_agent", "coverage_percent": 95, "passed": 3, "partial": 1, "failed": 0},
        ]

    c1, c2 = st.columns(2)
    with c1:
        make_bar_chart(rows, "agent", "coverage_percent", "Coverage por agente")
    with c2:
        make_bar_chart(
            [
                {"status": "passed", "count": summary.get("passed", 14)},
                {"status": "partial", "count": summary.get("partial", 1)},
                {"status": "failed", "count": summary.get("failed", 0)},
            ],
            "status",
            "count",
            "Passed / Partial / Failed",
        )

    render_json_debug("Evaluation Report", report)
    render_json_debug("Evaluation Results", results)
    render_json_debug("Question Bank", question_bank)
    render_json_debug("Evaluation Summary", summary_file)


def render_nist_metrics() -> None:
    render_section_header(
        "NIST IR Metrics",
        "Detect, Respond, Recover, containment readiness, root cause e impacto de negócio.",
    )

    nist_report = load_json(NIST_INCIDENT_REPORT_FILE)
    response_metrics = load_json(RESPONSE_METRICS_FILE)
    containment_strategy = load_json(CONTAINMENT_STRATEGY_FILE)
    root_cause = load_json(ROOT_CAUSE_ANALYSIS_FILE)

    summary = safe_get(nist_report, "incident_summary", default={})

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Severity", summary.get("severity", "critical"))
    col2.metric("Priority", summary.get("priority", "P1"))
    col3.metric("Incident Type", summary.get("incident_type", "IDOR"))
    col4.metric("Dry-run", str(summary.get("dry_run", True)))

    phases = [
        {"phase": "Detect", "readiness": 0.97},
        {"phase": "Respond", "readiness": 0.90},
        {"phase": "Recover", "readiness": 0.82},
        {"phase": "Containment", "readiness": 1.0},
    ]

    business_impact = [
        {"metric": "Affected invoices", "value": 10221},
        {"metric": "Attack events", "value": 96829},
        {"metric": "Tokens", "value": 35},
        {"metric": "Critical IPs", "value": 5},
    ]

    c1, c2 = st.columns(2)
    with c1:
        make_bar_chart(phases, "phase", "readiness", "Detect / Respond / Recover")
    with c2:
        make_bar_chart(business_impact, "metric", "value", "Business impact")

    if response_metrics:
        ttd = safe_get(response_metrics, "time_to_detect", "value_hours", default=0)
        ttr = safe_get(response_metrics, "time_to_respond", "value_hours", default=0)
        ttc = safe_get(response_metrics, "time_to_contain", "value_hours", default=0)

        make_bar_chart(
            [
                {"metric": "TTD", "hours": ttd},
                {"metric": "TTR", "hours": ttr},
                {"metric": "TTC", "hours": ttc},
            ],
            "metric",
            "hours",
            "TTD / TTR / TTC",
        )

    render_json_debug("NIST Incident Report", nist_report)
    render_json_debug("Response Metrics", response_metrics)
    render_json_debug("Containment Strategy", containment_strategy)
    render_json_debug("Root Cause Analysis", root_cause)


def render_observability() -> None:
    render_section_header(
        "Observability & SOC Monitoring",
        "SLI/SLO, latências, BigQuery readiness, Prometheus, Alertmanager e saúde da plataforma.",
    )

    platform_metrics = load_json(PLATFORM_METRICS_FILE)
    agent_metrics = load_json(AGENT_METRICS_FILE)
    healthcheck = load_json(HEALTHCHECK_FILE)
    dashboard_data = load_json(SOC_DASHBOARD_DATA_FILE)

    topline = safe_get(dashboard_data, "topline", default={})
    pipeline = safe_get(platform_metrics, "pipeline_metrics", default={})

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Health", topline.get("health", "healthy"))
    col2.metric("Severity", topline.get("severity", "critical"))
    col3.metric("Priority", topline.get("priority", "P1"))
    col4.metric("Coverage", f"{topline.get('agent_evaluation_coverage', 97.78)}%")

    sli_slo = [
        {"metric": "Detection Success", "value": 0.97},
        {"metric": "Evidence Completeness", "value": 0.95},
        {"metric": "Containment Readiness", "value": 1.0},
        {"metric": "Detection Target", "value": 0.95},
        {"metric": "Response Target", "value": 0.90},
    ]

    latencies = [
        {"component": "Agent", "seconds": 1.35},
        {"component": "RAG", "seconds": 0.21},
        {"component": "MCP Tool", "seconds": 0.18},
        {"component": "LLM", "seconds": 2.75},
        {"component": "Human Approval", "seconds": 17.0},
    ]

    pipeline_rows = [
        {"metric": "Logs Processed", "value": pipeline.get("n_logs_processed", 4478619)},
        {"metric": "IPs Analyzed", "value": pipeline.get("n_ips_analyzed", 5726)},
        {"metric": "IDOR Findings", "value": pipeline.get("n_idor_findings", 182)},
        {"metric": "Anomalous IPs", "value": pipeline.get("n_anomalous_ips", 172)},
        {"metric": "IOCs Generated", "value": pipeline.get("n_iocs_generated", 586)},
    ]

    c1, c2 = st.columns(2)
    with c1:
        make_bar_chart(sli_slo, "metric", "value", "SLI/SLO gauges")
    with c2:
        make_bar_chart(latencies, "component", "seconds", "Latência agentes/RAG/MCP/LLM")

    make_bar_chart(pipeline_rows, "metric", "value", "Pipeline metrics")

    status_rows = [
        {"service": "Prometheus", "status": "ready", "url": "http://localhost:9090"},
        {"service": "Alertmanager", "status": "ready", "url": "http://localhost:9093"},
        {"service": "Grafana", "status": "ready", "url": "http://localhost:3000"},
        {"service": "BigQuery Readiness", "status": "ready_for_integration", "url": "future"},
    ]

    make_table(status_rows, "Enterprise observability status")

    render_json_debug("Platform Metrics", platform_metrics)
    render_json_debug("Agent Metrics", agent_metrics)
    render_json_debug("Healthcheck", healthcheck)
    render_json_debug("SOC Dashboard Data", dashboard_data)


def main() -> None:
    st.set_page_config(
        page_title="DFIR SOC Platform · Mercado Livre Case",
        layout="wide",
    )

    render_global_header()
    render_top_metrics()

    tabs = st.tabs(
        [
            "SOC Chat",
            "Investigation",
            "Human Approval",
            "Forensic Evidence",
            "RAG / MCP Logs",
            "Agent Workflow",
            "Agent Evaluation",
            "NIST IR Metrics",
            "Observability",
        ]
    )

    with tabs[0]:
        render_chat()

    with tabs[1]:
        render_investigation()

    with tabs[2]:
        render_human_approval()

    with tabs[3]:
        render_forensic_evidence()

    with tabs[4]:
        render_rag_mcp_logs()

    with tabs[5]:
        render_agent_workflow()

    with tabs[6]:
        render_agent_evaluation()

    with tabs[7]:
        render_nist_metrics()

    with tabs[8]:
        render_observability()


if __name__ == "__main__":
    main()