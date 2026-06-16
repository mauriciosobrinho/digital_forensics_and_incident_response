from __future__ import annotations

from typing import Any

from src.agents.context.session_context import build_session_context
from src.agents.evidence_answer_templates import format_grounded_answer
from src.agents.evidence_grounded_copilot import (
    answer_from_structured_evidence,
    load_structured_evidence,
)
from src.agents.llm_client import build_llm_client
from src.agents.llm_intent_classifier import classify_question_with_llm
from src.agents.prompts.soc_copilot_prompt import build_soc_copilot_prompt
from src.agents.skills.skill_registry import run_all_skills
from src.rag.vector.chroma_store import query_vector_store


def _llm_answer_passes_minimum_quality_gate(
    llm_answer: str | None,
    structured_answer: dict[str, Any],
) -> bool:
    if not llm_answer:
        return False

    answer = llm_answer.lower()
    intent = structured_answer.get("intent")

    required_terms_by_intent = {
        "patient_zero": [
            "204.210.158.207",
        ],
        "attack_start": [
            "2020-10-01",
        ],
        "attack_end": [
            "2020-12-31",
        ],
        "affected_invoices": [
            "10221",
        ],
        "automation": [
            "automated",
        ],
        "response_metrics": [
            "ttd",
            "ttr",
            "ttc",
        ],
        "idor_evidence": [
            "idor",
            "invoice",
            "enumeration",
        ],
        "business_impact": [
            "critical",
            "p1",
        ],
        "containment": [
            "containment",
        ],
    }

    required_terms = required_terms_by_intent.get(
        intent,
        [],
    )

    broad_assessment_markers = [
        "timeline",
        "idor",
        "automation",
        "business impact",
        "containment",
    ]

    if any(
        marker in structured_answer.get("question", "").lower()
        for marker in [
            "complete incident assessment",
            "lead dfir analyst",
            "correlate",
            "ciso",
        ]
    ):
        return all(
            marker in answer
            for marker in broad_assessment_markers
        )

    return all(
        term.lower() in answer
        for term in required_terms
    )


def answer_professional_soc_question(
    question: str,
    tool_outputs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    llm_client = build_llm_client()

    intent = classify_question_with_llm(question)
    structured_answer = answer_from_structured_evidence(question)

    effective_intent = intent

    if structured_answer.get("is_answered") and structured_answer.get("intent"):
        effective_intent = {
            "intent": structured_answer.get("intent"),
            "confidence": structured_answer.get("intent_confidence"),
            "rationale": structured_answer.get("intent_rationale"),
            "classifier": "structured_evidence_router",
        }

    structured_artifacts = load_structured_evidence()
    session_context = build_session_context()
    skill_outputs = run_all_skills(structured_artifacts)

    try:
        vector_context = query_vector_store(question, top_k=6)
    except Exception as exc:
        vector_context = {
            "query": question,
            "retrieved_documents": [],
            "error": str(exc),
        }

    deterministic_answer = None

    if structured_answer.get("is_answered"):
        deterministic_answer = format_grounded_answer(
            structured_answer,
        )

    llm_answer = None
    llm_error = None

    if llm_client.is_enabled():
        prompt = build_soc_copilot_prompt(
            question=question,
            intent=effective_intent,
            structured_answer=structured_answer,
            structured_artifacts=structured_artifacts,
            vector_context=vector_context,
            session_context=session_context,
            skill_outputs=skill_outputs,
            tool_outputs=tool_outputs or {},
        )

        llm_answer = llm_client.generate_text(prompt)

        if not llm_answer:
            llm_error = (
                llm_client.last_error
                or "LLM generation returned no content. Falling back to deterministic evidence-grounded answer."
            )
        elif not _llm_answer_passes_minimum_quality_gate(
            llm_answer,
            structured_answer,
        ):
            llm_error = (
                "LLM answer failed minimum semantic quality gate. "
                "Falling back to deterministic evidence-grounded answer."
            )
            llm_answer = None

    final_answer = (
        llm_answer
        if llm_answer
        else deterministic_answer
    )

    if final_answer:
        return {
            "question": question,
            "answer": final_answer,
            "mode": (
                "professional_vector_rag_llm"
                if llm_answer
                else "professional_vector_rag_deterministic"
            ),
            "used_llm": bool(llm_answer),
            "llm_requested": llm_client.is_enabled(),
            "llm_error": llm_error,
            "intent": effective_intent,
            "evidence_grounded": bool(
                structured_answer.get("is_answered")
            ),
            "structured_answer": structured_answer,
            "vector_context": vector_context,
            "session_context": session_context,
            "skill_outputs": skill_outputs,
            "tool_outputs": tool_outputs or {},
            "confidence": structured_answer.get(
                "confidence",
                "medium",
            ),
            "source_artifacts": structured_answer.get(
                "source_artifacts",
                [],
            ),
            "safety": {
                "dry_run": True,
                "external_actions_executed": False,
                "mcp_mode": "safe_allowlisted_simulation",
            },
        }

    return {
        "question": question,
        "answer": (
            "I could not find a direct structured answer, but retrieved relevant "
            "DFIR context from the vector store for analyst review."
        ),
        "mode": "professional_vector_rag_fallback",
        "used_llm": False,
        "llm_requested": llm_client.is_enabled(),
        "llm_error": llm_error,
        "intent": effective_intent,
        "evidence_grounded": False,
        "structured_answer": structured_answer,
        "vector_context": vector_context,
        "session_context": session_context,
        "skill_outputs": skill_outputs,
        "tool_outputs": tool_outputs or {},
        "confidence": "low",
        "source_artifacts": [],
        "safety": {
            "dry_run": True,
            "external_actions_executed": False,
            "mcp_mode": "safe_allowlisted_simulation",
        },
    }