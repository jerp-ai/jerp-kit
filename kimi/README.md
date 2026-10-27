# Kimi Code CLI and Desktop

Documentation checked 2026-10-27. Older kimi-cli releases use different paths; consult that version's docs. A Kimi model in another harness uses that harness's adapter.

Copy the whole `skills/jerp/` directory into project `.agents/skills/jerp/` or user `~/.agents/skills/jerp/`. Merge `AGENTS.snippet.md` into project `AGENTS.md`, or `~/.kimi-code/AGENTS.md` for user-wide instructions. Kimi-specific skill alternatives are `.kimi-code/skills/` and `~/.kimi-code/skills/`.

Merge `mcp.json` into `.kimi-code/mcp.json` or `~/.kimi-code/mcp.json`. Run `/mcp-config login jerp` for browser OAuth and create a new session so updated configuration is loaded. Verify `/mcp` and an actual harmless call. Invoke `/skill:jerp` explicitly when checking skill loading.

The startup snippet supplies persistent routing; skill activation remains on demand. For enforced routing, review the installed version's permissions/hooks and the terminal's network access using `harness/README.md`.

Sources: [MCP](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/mcp.html), [skills](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/skills.html), [data locations](https://www.kimi.com/code/docs/en/kimi-code-cli/configuration/data-locations.html).
