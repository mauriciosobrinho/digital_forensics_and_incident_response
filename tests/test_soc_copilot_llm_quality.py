import os

import pytest

from src.agents.conversation_agent import ask_soc_copilot


LLM_QUALITY_QUESTIONS = [
    "Who is the patient zero and what evidence supports that conclusion?",
    "Correlate the forensic evidence, NIST report and observability metrics into a single incident narrative.",
    "You are the lead DFIR analyst. Build a complete incident assessment covering patient zero, timeline, IDOR evidence, automation, affected assets, business impact and containment.",
]


def _llm_enabled() -> bool:
    return os.getenv(
        "AGENTS_USE_LLM",
        "",
    ).strip().lower() in {
        "1",
        "true",
        "yes",
        "y",
        "on",
    }


def _is_provider_quota_error(
    error: str | None,
) -> bool:
    if not error:
        return False

    normalized = error.lower()

    return any(
        marker in normalized
        for marker in [
            "ratelimiterror",
            "rate limit",
            "429",
            "quota",
            "tokens per day",
            "tpd",
            "insufficient_quota",
        ]
    )


@pytest.mark.skipif(
    not _llm_enabled(),
    reason="LLM quality tests require AGENTS_USE_LLM=true.",
)
def test_soc_copilot_llm_quality_contract():
    provider_quota_failures = []

    for question in LLM_QUALITY_QUESTIONS:
        response = ask_soc_copilot(question)

        assert isinstance(response, dict)
        assert response.get("llm_requested") is True

        if response.get("used_llm") is not True:
            llm_error = response.get("llm_error")

            if _is_provider_quota_error(llm_error):
                provider_quota_failures.append(
                    {
                        "question": question,
                        "llm_error": llm_error,
                    }
                )
                continue

            if llm_error == (
                "LLM answer failed minimum semantic quality gate. "
                "Falling back to deterministic evidence-grounded answer."
            ):
                assert response.get("mode") in {
                    "professional_vector_rag_deterministic",
                    "evidence_grounded",
                    "evidence_grounded_llm",
                }
                assert response.get("answer", "").strip()
                assert response.get("evidence_grounded") is True
                continue

            raise AssertionError(
                {
                    "question": question,
                    "mode": response.get("mode"),
                    "used_llm": response.get("used_llm"),
                    "llm_error": llm_error,
                }
            )

        assert "llm" in response.get("mode", "").lower()

        answer = response.get("answer", "")

        assert answer.strip()
        assert len(answer) > 200

        vector_context = response.get("vector_context", {})
        retrieved_documents = vector_context.get(
            "retrieved_documents",
            [],
        )

        assert retrieved_documents

        assert response.get("intent")
        assert response.get("skill_outputs")
        assert response.get("confidence")
        assert response.get("safety", {}).get("external_actions_executed") is False

    if provider_quota_failures:
        pytest.skip(
            "LLM provider quota/rate limit reached during quality test. "
            f"Skipped after provider errors: {provider_quota_failures[:1]}"
        )


@pytest.mark.skipif(
    not _llm_enabled(),
    reason="LLM quality tests require AGENTS_USE_LLM=true.",
)
def test_soc_copilot_llm_professional_narrative_markers():
    response = ask_soc_copilot(
        "You are the lead DFIR analyst. Build a complete incident assessment covering patient zero, timeline, IDOR evidence, automation, affected assets, business impact and containment."
    )

    assert response.get("llm_requested") is True

    if response.get("used_llm") is not True:
        llm_error = response.get("llm_error")

        if _is_provider_quota_error(llm_error):
            pytest.skip(
                f"LLM provider quota/rate limit reached during narrative test: {llm_error}"
            )

        if llm_error == (
            "LLM answer failed minimum semantic quality gate. "
            "Falling back to deterministic evidence-grounded answer."
        ):
            assert response.get("mode") in {
                "professional_vector_rag_deterministic",
                "evidence_grounded",
                "evidence_grounded_llm",
            }
            assert response.get("answer", "").strip()
            assert response.get("evidence_grounded") is True
            return

        raise AssertionError(
            {
                "mode": response.get("mode"),
                "used_llm": response.get("used_llm"),
                "llm_error": llm_error,
            }
        )

    answer = response.get("answer", "").lower()

    expected_markers = [
        "executive answer",
        "supporting evidence",
        "reasoning",
        "operational implication",
        "confidence",
        "citations",
        "containment",
        "patient zero",
        "idor",
    ]

    for marker in expected_markers:
        assert marker in answer