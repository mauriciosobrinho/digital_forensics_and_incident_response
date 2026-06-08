import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


def _as_bool(
    value: str | None,
    default: bool = False,
) -> bool:
    if value is None:
        return default

    return value.strip().lower() in {
        "1",
        "true",
        "yes",
        "y",
        "on",
    }


@dataclass(frozen=True)
class AgentRuntimeSettings:
    llm_provider: str
    openai_api_key: str | None
    openai_model: str
    agents_use_llm: bool
    agents_dry_run: bool
    human_approval_mode: str
    checkpoint_backend: str


def load_agent_runtime_settings() -> AgentRuntimeSettings:
    return AgentRuntimeSettings(
        llm_provider=os.getenv(
            "LLM_PROVIDER",
            "openai",
        ),
        openai_api_key=os.getenv(
            "OPENAI_API_KEY",
        ),
        openai_model=os.getenv(
            "OPENAI_MODEL",
            "gpt-4.1-mini",
        ),
        agents_use_llm=_as_bool(
            os.getenv("AGENTS_USE_LLM"),
            default=False,
        ),
        agents_dry_run=_as_bool(
            os.getenv("AGENTS_DRY_RUN"),
            default=True,
        ),
        human_approval_mode=os.getenv(
            "HUMAN_APPROVAL_MODE",
            "simulated",
        ),
        checkpoint_backend=os.getenv(
            "LANGGRAPH_CHECKPOINT_BACKEND",
            "memory",
        ),
    )