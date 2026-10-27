# Codex and compatible ChatGPT agents

Copy the whole `skills/jerp/` directory to `.agents/skills/jerp/` in a project or `~/.agents/skills/jerp/` for the user. Older hosts may use another path; preserve any host-specific configuration.

Merge `AGENTS.snippet.md` into project `AGENTS.md`, or `~/.codex/AGENTS.md` for user-wide Codex sessions. Keep the routing rule always present; automatic skill discovery alone does not guarantee routing. Do not replace unrelated instructions.

Add the remote MCP server using the host's supported command/UI or merge `config.toml.example` into its MCP configuration. Complete OAuth using the host's login flow and test a real call. Copy no token into the example. Hosted ChatGPT integrations use their plugin/connector UI; a local TOML file does not configure them. REST-only hosts use the transport reference.

Sources: [OpenAI Docs: skills](https://learn.chatgpt.com/docs/build-skills), [MCP configuration](https://developers.openai.com/learn/docs-mcp). Documentation checked 2026-10-27; live host compatibility is not established by file validation.
