from typing import Any

from src.agents.evidence_answer_templates import format_grounded_answer

from src.agents.evidence_grounded_copilot import (
    answer_from_structured_evidence,
    load_structured_evidence,
)

from src.agents.llm_client import build_llm_client

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


def _build_grounded_llm_prompt(
    question: str,
    grounded_answer: dict[str, Any],
    deterministic_answer: str,
) -> str:
    return (
        "You are a senior Digital Forensics and Incident Response analyst. "
        "Answer the user's question using only the structured evidence below. "
        "Do not invent facts. If something is uncertain, say it is uncertain. "
        "Keep the answer practical, executive-ready and useful for a SOC/DFIR review.\n\n"
        f"User question:\n{question}\n\n"
        f"Deterministic evidence-grounded answer:\n{deterministic_answer}\n\n"
        "Structured evidence payload:\n"
        f"{grounded_answer}\n\n"
        "Required answer format:\n"
        "1. Direct answer\n"
        "2. Evidence\n"
        "3. Confidence\n"
        "4. Recommended next action\n"
    )


def _build_general_dfir_llm_prompt(
    question: str,
    artifacts: dict[str, Any],
    rag_context: dict[str, Any],
    tool_result: dict[str, Any] | None,
) -> str:
    return (
        "You are a senior Digital Forensics and Incident Response analyst "
        "supporting an IDOR incident investigation for a SOC/DFIR team.\n\n"
        "Answer the user's question using the structured investigation artifacts, "
        "RAG context and tool result below.\n\n"
        "Rules:\n"
        "- Do not invent facts.\n"
        "- Prefer structured evidence over generic playbook text.\n"
        "- If the question is not directly mapped to a predefined intent, infer the best answer from the available evidence.\n"
        "- If evidence is incomplete, say exactly what is missing.\n"
        "- Keep the answer practical, technical and useful for an incident review.\n"
        "- Include direct answer, evidence, confidence and recommended next action.\n\n"
        f"User question:\n{question}\n\n"
        f"Structured artifacts:\n{artifacts}\n\n"
        f"RAG context:\n{rag_context}\n\n"
        f"Tool result:\n{tool_result}\n"
    )



def ask_soc_copilot(
    question: str,
) -> dict[str, Any]:

    normalized = question.lower()

    grounded_answer = answer_from_structured_evidence(question)

    if grounded_answer.get("is_answered"):
        deterministic_answer = format_grounded_answer(
            grounded_answer,
        )

        llm_client = build_llm_client()
        llm_answer = None

        if llm_client.is_enabled():
            llm_answer = llm_client.generate_text(
                _build_grounded_llm_prompt(
                    question=question,
                    grounded_answer=grounded_answer,
                    deterministic_answer=deterministic_answer,
                )
            )

        final_answer = (
            llm_answer
            if llm_answer
            else deterministic_answer
        )

        response = {
            "question": question,
            "answer": final_answer,
            "mode": (
                "evidence_grounded_llm"
                if llm_answer
                else "evidence_grounded"
            ),
            "used_llm": bool(llm_answer),
            "evidence_grounded": True,
            "intent": grounded_answer.get("intent"),
            "confidence": grounded_answer.get("confidence"),
            "evidence": grounded_answer.get("evidence", []),
            "source_artifacts": grounded_answer.get("source_artifacts", []),
            "technical_payload": grounded_answer.get("technical_payload", {}),
            "deterministic_answer": deterministic_answer,
            "rag_context": None,
            "tool_result": None,
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

    llm_client = build_llm_client()

    if llm_client.is_enabled():
        artifacts = load_structured_evidence()

        generalized_answer = llm_client.generate_text(
            _build_general_dfir_llm_prompt(
                question=question,
                artifacts=artifacts,
                rag_context=rag_context,
                tool_result=tool_result,
            )
        )

        if generalized_answer:
            response = {
                "question": question,
                "answer": generalized_answer,
                "mode": "evidence_grounded_llm_generalized",
                "used_llm": True,
                "evidence_grounded": True,
                "intent": "generalized_dfir_question",
                "confidence": "medium",
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