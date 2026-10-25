# Codex and ChatGPT agents

1. Skill: copy `skills/jerp/SKILL.md` to `~/.codex/skills/jerp/SKILL.md` (or your host's skills folder).
2. Instructions: append `codex/AGENTS.snippet.md` to the project `AGENTS.md`.
3. Connector: add the MCP server from `codex/config.toml.example` (check your host's documentation for the exact keys of remote MCP servers) and sign in at `https://getjerp.com/mcp`.
4. Hosts without MCP sign-in can call the REST routes with an API key: see `skills/jerp/SKILL.md`, section Connector.
