from typing import Any

from src.config.settings import (
    KNOWLEDGE_DIR,
    RAG_CONTEXT_FILE,
)

from src.mcp_gateway.gateway import (
    invoke_mcp_tool,
)

from src.rag.rag_context import (
    build_rag_context,
    save_rag_context,
)


def answer_soc_question(
    question: str,
) -> dict[str, Any]:

    normalized = question.lower()

    rag_context = build_rag_context(
        knowledge_dir=KNOWLEDGE_DIR,
        query=question,
        top_k=3,
    )

    save_rag_context(
        rag_context,
        RAG_CONTEXT_FILE,
    )

    tool_result = None

    if "top" in normalized and (
        "ip" in normalized
        or "atacante" in normalized
        or "attacker" in normalized
    ):
        tool_result = invoke_mcp_tool(
            "get_top_attackers",
            {
                "top_n": 10,
            },
            approved=True,
            dry_run=True,
        )

    elif (
        "janela" in normalized
        or "window" in normalized
    ):
        tool_result = invoke_mcp_tool(
            "get_attack_window",
            {},
            approved=True,
            dry_run=True,
        )

    elif (
        "bloquear" in normalized
        or "block" in normalized
    ):
        tool_result = invoke_mcp_tool(
            "simulate_block_ip",
            {
                "ip": "requires_explicit_ip",
            },
            approved=False,
            dry_run=True,
        )

    answer = {
        "question": question,
        "answer": (
            "Resposta gerada pelo SOC Assistant com RAG local, "
            "artefatos forenses e MCP-safe tools em modo dry-run."
        ),
        "rag_context": rag_context,
        "tool_result": tool_result,
        "safety": {
            "dry_run": True,
            "external_actions_executed": False,
            "mcp_mode": "safe_allowlisted_simulation",
        },
    }

    return answer