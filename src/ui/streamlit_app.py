import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT),
    )

import streamlit as st

from src.agents.soc_assistant import answer_soc_question
from src.config.settings import (
    AGENT_DECISION_LOG_FILE,
    AGENT_INVESTIGATION_FILE,
    AGENT_RESPONSE_PLAYBOOK_FILE,
    AGENT_WORKFLOW_TIMELINE_FILE,
    FORENSIC_EVIDENCE_FILE,
    HUMAN_APPROVAL_DECISION_FILE,
    HUMAN_APPROVAL_REQUEST_FILE,
    MCP_TOOL_EXECUTION_LOG_FILE,
    RAG_CONTEXT_FILE,
    AGENT_QUESTION_BANK_FILE,
    AGENT_EVAL_RESULTS_FILE,
    AGENT_EVAL_REPORT_FILE,
    AGENT_EVAL_SUMMARY_FILE,
)


def load_json(path: Path):
    if not path.exists():
        return None

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def render_top_metrics():
    evidence = load_json(FORENSIC_EVIDENCE_FILE)
    investigation = load_json(AGENT_INVESTIGATION_FILE)
    decision_log = load_json(AGENT_DECISION_LOG_FILE)

    summary = evidence.get("summary", {}) if evidence else {}

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Scored IPs",
        summary.get("total_scored_ips", "-"),
    )

    col2.metric(
        "IDOR Findings",
        summary.get("total_idor_findings", "-"),
    )

    col3.metric(
        "Anomalous IPs",
        summary.get("total_anomalous_ips", "-"),
    )

    col4.metric(
        "Agent Decisions",
        len(decision_log) if decision_log else "-",
    )

    if investigation:
        triage = investigation.get("triage", {})
        st.info(
            f"Incident priority: {triage.get('priority', 'N/A')} · "
            f"Severity: {triage.get('severity', 'N/A')} · "
            f"Dry-run: {investigation.get('dry_run', True)}"
        )


def render_chat():
    st.subheader("SOC Agent Chat")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Olá. Sou o DFIR SOC Assistant. "
                    "Posso responder sobre IPs atacantes, janela do ataque, "
                    "IDOR, evidências, IOCs e recomendações de contenção."
                ),
            }
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input(
        "Pergunte algo: ex. Quais são os top IPs atacantes?"
    )

    if prompt:
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        response = answer_soc_question(
            prompt
        )

        answer = response.get(
            "answer",
            "Não consegui gerar uma resposta.",
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        with st.chat_message("assistant"):
            st.markdown(answer)

            with st.expander("Ver payload técnico"):
                st.json(response)


def render_json_section(title: str, path: Path):
    st.subheader(title)

    data = load_json(path)

    if data is None:
        st.warning(f"Arquivo não encontrado: {path}")
        return

    st.json(data)


def main():
    st.set_page_config(
        page_title="DFIR SOC Platform · Mercado Livre Case",
        layout="wide",
    )

    st.markdown(
        """
        <style>
        .main {
            background-color: #f5f5f5;
        }
        .meli-header {
            background: linear-gradient(90deg, #FFE600 0%, #FFF159 100%);
            padding: 24px;
            border-radius: 16px;
            border: 1px solid #e0c800;
            margin-bottom: 20px;
        }
        .meli-logo {
            color: #2D3277;
            font-size: 34px;
            font-weight: 800;
            letter-spacing: -1px;
        }
        .meli-subtitle {
            color: #333333;
            font-size: 16px;
            margin-top: 4px;
        }
        .badge {
            display: inline-block;
            background-color: #2D3277;
            color: white;
            padding: 4px 10px;
            border-radius: 999px;
            font-size: 12px;
            margin-top: 8px;
        }
        </style>

        <div class="meli-header">
            <div class="meli-logo">Mercado Livre · DFIR Platform</div>
            <div class="meli-subtitle">
                Digital Forensics and Incident Response Platform · IDOR Investigation Case
            </div>
            <div class="badge">LangGraph · RAG · MCP-safe Tools · Human-in-the-loop · Dry-run</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

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
        ]
    )

    with tabs[0]:
        render_chat()

    with tabs[1]:
        col1, col2 = st.columns(2)

        with col1:
            render_json_section(
                "Agent Investigation",
                AGENT_INVESTIGATION_FILE,
            )

        with col2:
            render_json_section(
                "Response Playbook",
                AGENT_RESPONSE_PLAYBOOK_FILE,
            )

        render_json_section(
            "Decision Log",
            AGENT_DECISION_LOG_FILE,
        )

    with tabs[2]:
        col1, col2 = st.columns(2)

        with col1:
            render_json_section(
                "Human Approval Request",
                HUMAN_APPROVAL_REQUEST_FILE,
            )

        with col2:
            render_json_section(
                "Human Approval Decision",
                HUMAN_APPROVAL_DECISION_FILE,
            )

    with tabs[3]:
        render_json_section(
            "Forensic Evidence Package",
            FORENSIC_EVIDENCE_FILE,
        )

    with tabs[4]:
        col1, col2 = st.columns(2)

        with col1:
            render_json_section(
                "RAG Context",
                RAG_CONTEXT_FILE,
            )

        with col2:
            render_json_section(
                "MCP-safe Tool Execution Log",
                MCP_TOOL_EXECUTION_LOG_FILE,
            )

    with tabs[5]:
        st.subheader("Agent Workflow & Human-in-the-loop")

        workflow = load_json(
            AGENT_WORKFLOW_TIMELINE_FILE
        )

        if workflow:
            st.write("Workflow Timeline")
            st.json(workflow)

            latest = workflow[-1]
            st.metric(
                "Current Stage",
                latest.get("stage", "unknown"),
            )

            st.metric(
                "Latest Decision",
                latest.get("decision", "unknown"),
            )
        else:
            st.warning(
                "Workflow timeline not generated yet."
            )

    with tabs[6]:
        st.subheader("Agent Evaluation & Validation Suite")

        report = load_json(
            AGENT_EVAL_REPORT_FILE
        )

        results = load_json(
            AGENT_EVAL_RESULTS_FILE
        )

        question_bank = load_json(
            AGENT_QUESTION_BANK_FILE
        )

        if report:
            summary = report.get(
                "summary",
                {},
            )

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Overall Coverage",
                f"{summary.get('overall_coverage_percent', 0)}%",
            )

            col2.metric(
                "Passed",
                summary.get("passed", 0),
            )

            col3.metric(
                "Partial",
                summary.get("partial", 0),
            )

            col4.metric(
                "Failed",
                summary.get("failed", 0),
            )

            st.subheader("Agent Coverage")
            st.json(
                report.get(
                    "agent_scores",
                    {},
                )
            )

        else:
            st.warning(
                "Agent evaluation report not generated yet."
            )

        if results:
            st.subheader("Evaluation Results")
            st.json(results)

        if question_bank:
            st.subheader("Question Bank")
            st.json(question_bank)    


if __name__ == "__main__":
    main()