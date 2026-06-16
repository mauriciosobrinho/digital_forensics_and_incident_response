from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from src.mcp_gateway.gateway import invoke_mcp_tool


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    input_schema: dict[str, Any]
    dry_run_only: bool = True


TOOL_REGISTRY = {
    "get_top_attackers": ToolDefinition(
        name="get_top_attackers",
        description="Return top suspicious attacking IPs from generated evidence.",
        input_schema={
            "type": "object",
            "properties": {
                "top_n": {"type": "integer"},
            },
            "required": ["top_n"],
        },
    ),
    "get_attack_window": ToolDefinition(
        name="get_attack_window",
        description="Return reconstructed attack start and end timestamps.",
        input_schema={
            "type": "object",
            "properties": {},
        },
    ),
    "simulate_block_ip": ToolDefinition(
        name="simulate_block_ip",
        description="Simulate IP blocking in dry-run mode.",
        input_schema={
            "type": "object",
            "properties": {
                "ip": {"type": "string"},
            },
            "required": ["ip"],
        },
    ),
}


def list_tools() -> list[dict[str, Any]]:
    return [
        {
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.input_schema,
            "dry_run_only": tool.dry_run_only,
        }
        for tool in TOOL_REGISTRY.values()
    ]


def call_registered_tool(
    name: str,
    arguments: dict[str, Any],
) -> dict[str, Any]:
    if name not in TOOL_REGISTRY:
        return {
            "error": f"Tool not registered: {name}",
        }

    return invoke_mcp_tool(
        name,
        arguments,
        approved=name != "simulate_block_ip",
        dry_run=True,
    )