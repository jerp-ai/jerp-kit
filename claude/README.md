# Claude

## Claude app (Claude.ai)
1. Customize -> Connectors -> Add custom connector -> name `JERP` -> URL `https://getjerp.com/mcp` -> sign in with Google or GitHub.
2. Customize -> Skills -> upload `skills/jerp/SKILL.md`.

## Claude Code
```bash
claude mcp add --transport http jerp https://getjerp.com/mcp
mkdir -p ~/.claude/skills/jerp && cp skills/jerp/SKILL.md ~/.claude/skills/jerp/SKILL.md
```
Then run `/mcp` in Claude Code and sign in to JERP.

Optional chat-sync hooks for people who opted in are part of the pack at `https://getjerp.com/lab/connect`; they are not in this repository.
