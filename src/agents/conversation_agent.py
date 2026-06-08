from typing import Any

from src.agents.conversation_memory import (
    append_conversation_turn,
)

from src.agents.response_formatter import (
    format_soc_response,
)

from src.config.settings import (
    INTERACTIVE_SESSION_LOG_FILE,
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


def ask_soc_copilot(
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

    formatted = format_soc_response(
        question=question,
        rag_context=rag_context,
        tool_result=tool_result,
    )

    response = {
        "question": question,
        "answer": formatted["answer"],
        "mode": formatted["mode"],
        "used_llm": formatted["used_llm"],
        "rag_context": rag_context,
        "tool_result": tool_result,
        "safety": {
            "dry_run": True,
            "external_actions_executed": False,
            "mcp_mode": "safe_allowlisted_simulation",
        },
    }

    append_conversation_turn(
        INTERACTIVE_SESSION_LOG_FILE,
        question,
        response,
    )

    return response