# Claude Code and Claude app

For Claude Code, copy the entire `skills/jerp/` directory into `.claude/skills/jerp/` or `~/.claude/skills/jerp/`. Merge `CLAUDE.snippet.md` into project `CLAUDE.md` or user-wide `~/.claude/CLAUDE.md`; preserve existing instructions. This startup policy is separate from on-demand skill discovery.

Connect MCP:

```sh
claude mcp add --transport http jerp https://getjerp.com/mcp
```

Use `/mcp` to complete OAuth. Start a fresh session and check tool execution as well as discovery.

For Claude's hosted app, use its connector UI for the URL and OAuth. Upload the **whole skill package**, including references, through the supported skills UI. Put the startup snippet into project instructions or another persistent surface; a lone SKILL.md upload can lose its references. Availability and UI names depend on the installed plan/version.

Sources: [skills](https://code.claude.com/docs/en/skills), [MCP](https://code.claude.com/docs/en/mcp). Documentation checked 2026-10-27; app/CLI live tests remain necessary.
