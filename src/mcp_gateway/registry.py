from src.mcp_gateway.schemas import (
    MCPToolSpec,
)


def build_mcp_tool_registry() -> list[MCPToolSpec]:
    return [
        {
            "name": "get_top_attackers",
            "description": "Return top attacker IPs from forensic evidence.",
            "requires_human_approval": False,
            "dry_run_only": True,
        },
        {
            "name": "get_attack_window",
            "description": "Return attack first_seen and last_seen.",
            "requires_human_approval": False,
            "dry_run_only": True,
        },
        {
            "name": "simulate_block_ip",
            "description": "Simulate IP blocking action.",
            "requires_human_approval": True,
            "dry_run_only": True,
        },
        {
            "name": "simulate_rate_limit",
            "description": "Simulate endpoint rate limiting.",
            "requires_human_approval": False,
            "dry_run_only": True,
        },
    ]