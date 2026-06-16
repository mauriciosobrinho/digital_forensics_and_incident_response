from __future__ import annotations

import json
import sys
from typing import Any

from src.mcp_gateway.tool_registry import (
    call_registered_tool,
    list_tools,
)


def handle_request(
    request: dict[str, Any],
) -> dict[str, Any]:
    method = request.get("method")
    request_id = request.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "name": "idor-response-platform-mcp",
                "version": "0.1.0",
                "capabilities": {
                    "tools": True,
                },
            },
        }

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": list_tools(),
            },
        }

    if method == "tools/call":
        params = request.get("params", {})
        name = params.get("name")
        arguments = params.get("arguments", {})

        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": call_registered_tool(
                name,
                arguments,
            ),
        }

    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {
            "code": -32601,
            "message": f"Unknown method: {method}",
        },
    }


def main() -> None:
    for line in sys.stdin:
        if not line.strip():
            continue

        request = json.loads(line)
        response = handle_request(request)

        print(
            json.dumps(response),
            flush=True,
        )


if __name__ == "__main__":
    main()