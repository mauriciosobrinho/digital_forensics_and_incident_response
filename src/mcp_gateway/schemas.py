from typing import Any, TypedDict


class MCPToolSpec(TypedDict):
    name: str
    description: str
    requires_human_approval: bool
    dry_run_only: bool


class MCPToolExecution(TypedDict, total=False):
    tool_name: str
    input: dict[str, Any]
    output: dict[str, Any]
    dry_run: bool
    approved: bool
    status: str