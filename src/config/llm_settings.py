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
    llm_api_key: str | None
    llm_model: str
    llm_base_url: str | None

    agents_use_llm: bool
    agents_dry_run: bool

    human_approval_mode: str
    checkpoint_backend: str
    
    human_decision_scenario: str


def load_agent_runtime_settings() -> AgentRuntimeSettings:
    return AgentRuntimeSettings(
        llm_provider=os.getenv(
            "LLM_PROVIDER",
            "openrouter",
        ),
        llm_api_key=os.getenv(
            "LLM_API_KEY",
        ),
        llm_model=os.getenv(
            "LLM_MODEL",
            "openai/gpt-4.1-mini",
        ),
        llm_base_url=os.getenv(
            "LLM_BASE_URL",
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
        human_decision_scenario=os.getenv(
        "HUMAN_DECISION_SCENARIO",
        "approve",
        ),
    )