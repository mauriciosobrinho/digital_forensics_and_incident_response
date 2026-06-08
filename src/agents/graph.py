from langgraph.graph import END, START, StateGraph

from src.agents.state import InvestigationState

from src.agents.triage_agent import (
    triage_agent,
)

from src.agents.forensic_agent import (
    forensic_analyst_agent,
)

from src.agents.response_agent import (
    response_advisor_agent,
)

from src.agents.human_approval_agent import (
    human_approval_agent,
)


def build_investigation_graph():
    graph = StateGraph(
        InvestigationState
    )

    graph.add_node(
        "triage",
        triage_agent,
    )

    graph.add_node(
        "forensic_analysis",
        forensic_analyst_agent,
    )

    graph.add_node(
        "response_advice",
        response_advisor_agent,
    )

    graph.add_node(
        "human_approval",
        human_approval_agent,
    )

    graph.add_edge(
        START,
        "triage",
    )

    graph.add_edge(
        "triage",
        "forensic_analysis",
    )

    graph.add_edge(
        "forensic_analysis",
        "response_advice",
    )

    graph.add_edge(
        "response_advice",
        "human_approval",
    )

    graph.add_edge(
        "human_approval",
        END,
    )

    
    return graph.compile()