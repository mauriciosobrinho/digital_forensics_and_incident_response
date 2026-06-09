import json
from typing import Any

from src.config.llm_settings import (
    AgentRuntimeSettings,
    load_agent_runtime_settings,
)


class LLMClient:
    def __init__(
        self,
        settings: AgentRuntimeSettings | None = None,
    ) -> None:
        self.settings = (
            settings
            if settings is not None
            else load_agent_runtime_settings()
        )

    def is_enabled(self) -> bool:
        return (
            self.settings.agents_use_llm
            and self.settings.llm_api_key is not None
        )

    def generate_text(
        self,
        prompt: str,
    ) -> str | None:

        if not self.is_enabled():
            return None

        try:
            from langchain_openai import ChatOpenAI
        except ImportError:
            return None

        llm_kwargs = {
            "model": self.settings.llm_model,
            "api_key": self.settings.llm_api_key,
            "temperature": 0,
        }

        if self.settings.llm_base_url:
            llm_kwargs["base_url"] = (
                self.settings.llm_base_url
            )

        try:
            llm = ChatOpenAI(
                **llm_kwargs
            )

            response = llm.invoke(
                prompt
            )

            return response.content

        except Exception:
            return None

    def generate_json(
        self,
        prompt: str,
        agent_name: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:

        enriched_prompt = prompt

        if agent_name or context:
            enriched_prompt = (
                f"{prompt}\n\n"
                "Return only valid JSON.\n\n"
                f"agent_name: {agent_name}\n\n"
                f"context:\n{json.dumps(context or {}, ensure_ascii=False, indent=2)}"
            )

        content = self.generate_text(
            enriched_prompt
        )

        if not content:
            return None

        try:
            return json.loads(
                content
            )

        except json.JSONDecodeError:
            return {
                "raw_response": content,
                "json_parse_error": True,
            }


def build_llm_client(
    settings: AgentRuntimeSettings | None = None,
) -> LLMClient:
    return LLMClient(
        settings
    )