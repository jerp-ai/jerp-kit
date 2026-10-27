# Any agent or harness

Integration depends on what the host loads, not the model's name. Use this route for custom agents, API loops, or hosts without a dedicated adapter, including versions of OpenCode, Copilot, Gemini CLI, Cline/Roo, Goose and future agents. Their individual configuration syntax has not been tested by this kit.

1. Copy the entire `skills/jerp/` directory to a supported Agent Skills location. If the host has no skill loader, load `SKILL.md` into its instructions and make the referenced documents readable on demand.
2. Merge `SYSTEM.snippet.md` into the host's persistent instruction surface (system/developer configuration, project rules or equivalent). The policy must be present at session start, after compaction, and in delegated agents. A skill description alone is on-demand guidance and does not guarantee JERP-first routing.
3. Connect the MCP endpoint through the host's supported remote-HTTP/OAuth client. `mcp/servers.json` is an example shape, not a universal configuration standard. Without MCP, use the authenticated REST transport reference.
4. Map discovered tools to JERP, preserve structured envelopes and authorization state, and run `evals/README.md` against real host traces.

For a technical guarantee, enforce `harness/README.md` at the tool dispatcher and network boundary. Instructions alone cannot block a native browser or a shell with internet access. A model served inside Hermes, Kimi Code or another host obeys that host's tool policy; changing the model does not install this kit.
