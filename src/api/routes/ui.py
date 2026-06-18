from fastapi import APIRouter


router = APIRouter(
    prefix="/api",
    tags=["ui"],
)


STREAMLIT_TABS = [
    {
        "id": "soc_chat",
        "label": "SOC Chat",
        "description": "Interactive SOC copilot for analyst questions, evidence-grounded answers and technical payload inspection.",
        "contract_endpoint": "/api/agents",
        "primary_artifacts": [
            "agent_investigation",
            "agent_decision_log",
            "rag_context",
            "mcp_tool_execution_log",
        ],
    },
    {
        "id": "investigation",
        "label": "Investigation",
        "description": "Incident triage, forensic investigation summary and attack characterization.",
        "contract_endpoint": "/api/evidence",
        "primary_artifacts": [
            "forensic_evidence",
            "attack_timeline",
            "nist_incident_report",
        ],
    },
    {
        "id": "human_approval",
        "label": "Human Approval",
        "description": "Human-in-the-loop approval request and decision contract for simulated containment actions.",
        "contract_endpoint": "/api/agents",
        "primary_artifacts": [
            "human_approval_request",
            "human_approval_decision",
        ],
    },
    {
        "id": "forensic_evidence",
        "label": "Forensic Evidence",
        "description": "Evidence package, chain of custody, IOCs and attack timeline.",
        "contract_endpoint": "/api/evidence",
        "primary_artifacts": [
            "chain_of_custody",
            "forensic_evidence",
            "iocs",
            "attack_timeline",
        ],
    },
    {
        "id": "rag_mcp_logs",
        "label": "RAG / MCP Logs",
        "description": "Vector RAG context and MCP-safe tool execution logs.",
        "contract_endpoint": "/api/agents",
        "primary_artifacts": [
            "rag_context",
            "mcp_tool_execution_log",
        ],
    },
    {
        "id": "agent_workflow",
        "label": "Agent Workflow",
        "description": "LangGraph workflow, agent orchestration and decision timeline.",
        "contract_endpoint": "/api/agents",
        "primary_artifacts": [
            "agent_workflow_timeline",
            "agent_decision_log",
        ],
    },
    {
        "id": "agent_evaluation",
        "label": "Agent Evaluation",
        "description": "Agent benchmark results, evaluation report and semantic quality indicators.",
        "contract_endpoint": "/api/agents",
        "primary_artifacts": [
            "agent_eval_results",
            "agent_eval_report",
            "agent_eval_summary",
        ],
    },
    {
        "id": "nist_ir_metrics",
        "label": "NIST IR Metrics",
        "description": "Incident response metrics aligned to NIST identify, protect, detect, respond and recover phases.",
        "contract_endpoint": "/api/metrics",
        "primary_artifacts": [
            "response_metrics",
            "containment_strategy",
            "root_cause_analysis",
            "nist_incident_report",
        ],
    },
    {
        "id": "observability",
        "label": "Observability",
        "description": "Platform health, operational metrics and Prometheus-ready surface.",
        "contract_endpoint": "/api/observability",
        "primary_artifacts": [
            "platform_metrics",
            "agent_metrics",
            "healthcheck",
            "soc_dashboard_data",
        ],
    },
]


@router.get("/tabs")
def get_tabs() -> dict:
    return {
        "service": "dfir-ui-contracts",
        "ui": "streamlit",
        "tabs": STREAMLIT_TABS,
        "streamlit_url": "http://localhost:8501",
        "api_home": "http://localhost:8000/home",
    }