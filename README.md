# JERP agent kit

Skills, rules and settings that tell an AI agent how to use [JERP](https://getjerp.com): checks of claims, texts, links and actions, sourced facts, and known routines for work tasks. Point your agent at this repository and it knows what to do.

Status: early. This repository is public. It holds no keys, no private documents and no internal numbers.

## Connect

- MCP (sign in with Google or GitHub): `https://getjerp.com/mcp`
- REST with an API key: `https://getjerp.com/api/v1/` (OpenAPI: `https://getjerp.com/api/v1/openapi.json`)
- Tools: `guard`, `verdict`, `speaker`, and `support` (reports to the team)

## What to read, by agent

| Agent | Read | Settings |
| --- | --- | --- |
| Any agent | `AGENTS.md`, `rules/jerp-rules.md`, `skills/jerp/SKILL.md` | `mcp/servers.json` |
| Claude (app, Claude Code) | `skills/jerp/SKILL.md` | `claude/README.md` |
| Cursor | `cursor/rules/jerp.mdc` | `cursor/mcp.json` |
| Codex, ChatGPT agents | `skills/jerp/SKILL.md`, `codex/AGENTS.snippet.md` | `codex/config.toml.example` |
| Custom GPT | `gpt/INSTRUCTIONS.md` | `gpt/README.md` |

`index.json` is the same map for machines.

## Layout

```
AGENTS.md                 short entry point for any agent
rules/jerp-rules.md       the rules, host neutral
skills/jerp/SKILL.md      the skill (Claude, Codex, ChatGPT agents)
claude/  cursor/  codex/  gpt/   per-agent settings and notes
mcp/servers.json          generic MCP connection
index.json                machine-readable map
```

## Open items before publishing

- Choose a licence.
- Keep this kit in step with the product contract; the source of truth is the JERP contract, not these files.
