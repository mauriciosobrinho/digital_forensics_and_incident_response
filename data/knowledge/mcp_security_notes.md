# MCP Security Notes

MCP tools must be allowlisted.

Every tool execution must:
- Run in dry-run mode by default.
- Be logged.
- Avoid shell execution.
- Avoid arbitrary file writes.
- Require approval for production-impacting actions.

External MCP servers should be treated as untrusted unless reviewed.