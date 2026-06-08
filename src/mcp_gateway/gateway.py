import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.config.settings import (
    FORENSIC_EVIDENCE_FILE,
    MCP_TOOL_EXECUTION_LOG_FILE,
    MCP_TOOL_REGISTRY_FILE,
)

from src.mcp_gateway.registry import (
    build_mcp_tool_registry,
)

from src.tools.evidence_tools import (
    get_attack_window,
    get_top_attackers,
    load_json_artifact,
)

from src.tools.response_tools import (
    simulate_block_ip,
    simulate_rate_limit,
)


def save_mcp_tool_registry(
    output_file: Path = MCP_TOOL_REGISTRY_FILE,
) -> list[dict[str, Any]]:
    registry = build_mcp_tool_registry()

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_file.open(
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            registry,
            f,
            indent=2,
            ensure_ascii=False,
        )

    return registry


def _load_execution_log() -> list[dict[str, Any]]:
    if not MCP_TOOL_EXECUTION_LOG_FILE.exists():
        return []

    with MCP_TOOL_EXECUTION_LOG_FILE.open(
        "r",
        encoding="utf-8",
    ) as f:
        return json.load(f)


def _save_execution_log(
    log: list[dict[str, Any]],
) -> None:
    MCP_TOOL_EXECUTION_LOG_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with MCP_TOOL_EXECUTION_LOG_FILE.open(
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            log,
            f,
            indent=2,
            ensure_ascii=False,
        )


def invoke_mcp_tool(
    tool_name: str,
    payload: dict[str, Any] | None = None,
    *,
    approved: bool = False,
    dry_run: bool = True,
) -> dict[str, Any]:
    payload = payload or {}

    registry = {
        tool["name"]: tool
        for tool in build_mcp_tool_registry()
    }

    if tool_name not in registry:
        result = {
            "status": "rejected",
            "reason": "Tool is not allowlisted.",
        }
    else:
        spec = registry[tool_name]

        if spec["requires_human_approval"] and not approved:
            result = {
                "status": "approval_required",
                "reason": "Tool requires human approval.",
                "tool_name": tool_name,
            }

        elif tool_name == "get_top_attackers":
            evidence = load_json_artifact(
                FORENSIC_EVIDENCE_FILE
            )
            result = {
                "status": "ok",
                "result": get_top_attackers(
                    evidence,
                    top_n=int(
                        payload.get(
                            "top_n",
                            10,
                        )
                    ),
                ),
            }

        elif tool_name == "get_attack_window":
            evidence = load_json_artifact(
                FORENSIC_EVIDENCE_FILE
            )
            result = {
                "status": "ok",
                "result": get_attack_window(
                    evidence.get(
                        "attack_timeline",
                        {},
                    )
                ),
            }

        elif tool_name == "simulate_block_ip":
            result = {
                "status": "ok",
                "result": simulate_block_ip(
                    ip=payload["ip"],
                    dry_run=dry_run,
                ),
            }

        elif tool_name == "simulate_rate_limit":
            result = {
                "status": "ok",
                "result": simulate_rate_limit(
                    endpoint=payload.get(
                        "endpoint",
                        "/invoices/search",
                    ),
                    dry_run=dry_run,
                ),
            }

        else:
            result = {
                "status": "not_implemented",
                "tool_name": tool_name,
            }

    log = _load_execution_log()

    log.append(
        {
            "timestamp_utc": datetime.now(
                timezone.utc
            ).isoformat(),
            "tool_name": tool_name,
            "payload": payload,
            "approved": approved,
            "dry_run": dry_run,
            "result": result,
        }
    )

    _save_execution_log(
        log
    )

    return result