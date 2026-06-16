from src.mcp_gateway.server.stdio_server import handle_request


def test_mcp_tools_list():
    response = handle_request(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
        }
    )

    assert response["id"] == 1
    assert "tools" in response["result"]
    assert response["result"]["tools"]


def test_mcp_initialize():
    response = handle_request(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
        }
    )

    assert response["result"]["capabilities"]["tools"] is True