from typing import Any

from src.config.llm_settings import (
    AgentRuntimeSettings,
)


class DeterministicLLMClient:
    def generate_json(
        self,
        *,
        agent_name: str,
        prompt: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "agent": agent_name,
            "mode": "deterministic_stub",
            "used_llm": False,
            "summary": (
                "LLM disabled. Deterministic reasoning generated "
                "from structured evidence."
            ),
            "prompt_preview": prompt[:500],
            "context_keys": list(context.keys()),
        }


class OpenAILLMClient:
    def __init__(
        self,
        settings: AgentRuntimeSettings,
    ) -> None:
        self.settings = settings

    def generate_json(
        self,
        *,
        agent_name: str,
        prompt: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        if not self.settings.openai_api_key:
            return {
                "agent": agent_name,
                "mode": "openai_not_configured",
                "used_llm": False,
                "summary": (
                    "AGENTS_USE_LLM=true but OPENAI_API_KEY is missing. "
                    "Falling back to deterministic behavior."
                ),
            }

        try:
            from langchain_openai import ChatOpenAI
        except ImportError:
            return {
                "agent": agent_name,
                "mode": "langchain_openai_missing",
                "used_llm": False,
                "summary": (
                    "langchain-openai is not installed. "
                    "Falling back to deterministic behavior."
                ),
            }

        llm = ChatOpenAI(
            model=self.settings.openai_model,
            api_key=self.settings.openai_api_key,
            temperature=0,
        )

        message = (
            f"{prompt}\n\n"
            "Return a concise JSON-like investigation reasoning summary.\n\n"
            f"Context:\n{context}"
        )

        response = llm.invoke(
            message
        )

        return {
            "agent": agent_name,
            "mode": "openai",
            "used_llm": True,
            "model": self.settings.openai_model,
            "summary": response.content,
        }


def build_llm_client(
    settings: AgentRuntimeSettings,
):
    if settings.agents_use_llm:
        return OpenAILLMClient(
            settings
        )

    return DeterministicLLMClient()