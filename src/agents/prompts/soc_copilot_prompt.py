from __future__ import annotations

import json
from typing import Any


def _compact_documents(
    vector_context: dict[str, Any],
    max_docs: int = 4,
    max_chars_per_doc: int = 900,
) -> list[dict[str, Any]]:
    documents = vector_context.get(
        "retrieved_documents",
        [],
    )

    compacted = []

    for document in documents[:max_docs]:
        compacted.append(
            {
                "source_path": document.get("source_path"),
                "artifact_type": document.get("artifact_type"),
                "chunk_index": document.get("chunk_index"),
                "content": str(
                    document.get("content", "")
                )[:max_chars_per_doc],
            }
        )

    return compacted


def _compact_session_context(
    session_context: dict[str, Any],
) -> dict[str, Any]:
    return {
        "summary": str(
            session_context.get("summary", "")
        )[:1200],
        "recent_turns": session_context.get(
            "recent_turns",
            [],
        )[-3:],
    }


def _compact_structured_artifacts(
    structured_artifacts: dict[str, Any],
) -> dict[str, Any]:
    nist = structured_artifacts.get(
        "nist_incident_report",
        {},
    )

    forensic = structured_artifacts.get(
        "forensic_evidence",
        {},
    )

    observability = structured_artifacts.get(
        "soc_dashboard_data",
        {},
    )

    return {
        "nist_questions_answered": nist.get(
            "questions_answered",
            {},
        ),
        "nist_incident": {
            "severity": nist.get("severity"),
            "priority": nist.get("priority"),
            "incident_name": nist.get("incident_name"),
        },
        "forensic_summary": forensic.get(
            "summary",
            forensic.get("forensic_summary", {}),
        ),
        "observability_topline": observability.get(
            "topline",
            {},
        ),
    }


def _compact_skill_outputs(
    skill_outputs: dict[str, Any],
) -> dict[str, Any]:
    return {
        key: value
        for key, value in skill_outputs.items()
        if key
        in {
            "patient_zero",
            "timeline",
            "containment",
            "impact",
            "metrics",
            "root_cause",
            "mitre",
        }
    }


def build_soc_copilot_prompt(
    question: str,
    intent: dict[str, Any],
    structured_answer: dict[str, Any],
    structured_artifacts: dict[str, Any],
    vector_context: dict[str, Any],
    session_context: dict[str, Any],
    skill_outputs: dict[str, Any],
    tool_outputs: dict[str, Any],
) -> str:
    compact_payload = {
        "question": question,
        "intent": intent,
        "structured_answer": structured_answer,
        "structured_artifacts": _compact_structured_artifacts(
            structured_artifacts,
        ),
        "vector_documents": _compact_documents(
            vector_context,
        ),
        "session_context": _compact_session_context(
            session_context,
        ),
        "skill_outputs": _compact_skill_outputs(
            skill_outputs,
        ),
        "tool_outputs": tool_outputs,
    }

    return (
        "You are a senior SOC and Digital Forensics & Incident Response analyst.\n"
        "You are investigating an IDOR incident using structured evidence, "
        "vector-retrieved artifacts, DFIR skills and safe tool outputs.\n\n"
        "Grounding rules:\n"
        "- Answer in the same language used by the user, unless the user explicitly asks otherwise.\n"
        "- Use the structured answer as the source of truth.\n"
        "- Use vector documents only to enrich and explain the conclusion.\n"
        "- Do not invent IPs, timestamps, counts, severity, or containment actions.\n"
        "- Do not claim production containment; this platform is dry-run.\n"
        "- If evidence is insufficient, say what is missing.\n"
        "- Answer the exact question asked.\n\n"
        "Required answer format:\n"
        "Executive answer:\n"
        "<direct conclusion>\n\n"
        "Supporting evidence:\n"
        "1. <evidence item>\n"
        "2. <evidence item>\n"
        "3. <evidence item>\n\n"
        "Reasoning:\n"
        "<explain why the evidence supports the conclusion>\n\n"
        "Operational implication:\n"
        "<what the SOC/DFIR team should understand or do>\n\n"
        "Confidence level: <High|Medium|Low>\n\n"
        "Citations:\n"
        "- <source artifact path>\n\n"
        "Evidence package:\n"
        f"{json.dumps(compact_payload, indent=2, ensure_ascii=False)}"
    )