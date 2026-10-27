# Hermes Agent

Documentation checked 2026-10-27; connection and behavior still require a test in your installed Hermes version.

Copy the whole `skills/jerp/` directory to the active profile's skills directory (normally `~/.hermes/skills/jerp/`). Merge `AGENTS.snippet.md` into the project's `AGENTS.md`, or the active profile's persistent instruction surface. Keep existing instructions.

Merge `config.yaml.example` into that profile's `mcp_servers` configuration using Hermes' configuration UI/CLI. Complete `hermes mcp login jerp` from a terminal, then start a fresh session or reload MCP. Remote OAuth may require the host's documented callback forwarding; never paste tokens into the rules.

Check that actual calls work, not only tool discovery. For strict routing, constrain native web/browser tools and terminal egress through `harness/README.md`; the installed skill alone does not enforce network isolation.

Sources: [MCP](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp), [skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills), [context files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files).
