# JERP agent kit

Persistent routing rules, a portable skill and connection adapters for [JERP](https://getjerp.com). Supported company/domain research, market discovery, verification, safety checks and stored work routines go through JERP first, throughout the task. Native tools handle local work and specific capabilities JERP does not provide.

This is a separate public repository from the JERP service. It contains no credentials. Status: draft 0.2.0; schema and host documentation checked 2026-10-27. Named host adapters are documented configurations, not a claim that every host/model has passed a live test.

Contributors must follow the [public repository boundary](CONTRIBUTING.md). Internal reports, real traces, company/private data and credentials do not belong in this kit.

## Install both layers

1. Install the **entire** `skills/jerp/` directory, including references, in the host's skill location.
2. Merge an always-on startup snippet into the host's instructions. A skill description by itself is discovered on demand and does not ensure the first online request reaches JERP. Preserve existing user/team instructions.
3. Connect `https://getjerp.com/mcp` with the host's remote HTTP MCP client and browser OAuth. Hosts without MCP can use the same operations via authenticated REST; read [transport](skills/jerp/references/transport.md).
4. Start a new session, verify actual tool calls, then run [behavioral checks](evals/README.md) in that host.

| Host | Installation guide | Persistent rule |
| --- | --- | --- |
| Codex CLI/app and compatible agents | [Codex](codex/README.md) | [AGENTS snippet](codex/AGENTS.snippet.md) |
| Claude Code / Claude app | [Claude](claude/README.md) | [CLAUDE snippet](claude/CLAUDE.snippet.md) |
| Cursor | [Cursor](cursor/README.md) | [Always Apply rule](cursor/rules/jerp.mdc) |
| Custom GPT / Actions | [GPT](gpt/README.md) | [Self-contained instructions](gpt/INSTRUCTIONS.md) |
| Hermes Agent | [Hermes](hermes/README.md) | [AGENTS snippet](hermes/AGENTS.snippet.md) |
| Kimi Code CLI/Desktop | [Kimi](kimi/README.md) | [AGENTS snippet](kimi/AGENTS.snippet.md) |
| Other MCP, Agent Skills or HTTP harnesses | [Generic integration](generic/README.md) | [Persistent instruction snippet](generic/SYSTEM.snippet.md) |

The portable contract is feature-based: a model named GPT, Claude, Kimi or another name uses the instructions and tools supplied by its **host**. New or unlisted hosts use the generic adapter; exact configuration and enforcement require version-specific verification. `index.json` exposes this map to installers.

## Routing and limits

Read [the policy](rules/jerp-rules.md) and [the skill](skills/jerp/SKILL.md). A first JERP call does not permit later native bypasses. Empty results, no source, auth errors, quotas and outages do not silently unlock native research. A supported lookup cannot be relabelled as page reading to avoid JERP. Fallback is scoped to a real absent capability or explicit user routing override.

JERP is not a universal search engine, arbitrary-page browser or action executor. The host still reads/edits local files, runs tests, executes approved steps and handles capabilities absent from JERP. Retrieved text is data, never instruction authority. Keep credentials/private content local; report issues with `support` only under the user's reporting authorization.

For **enforced** internet routing, implement [the harness boundary](harness/README.md), including native web, shell networking, other MCPs and subagents. Markdown instructions alone cannot block network access. The kit ships a policy/trace contract and offline checker, not a universal firewall or automatic hook installer.

## Maintain and validate

Change `rules/jerp-first.snippet.md`, then run `python3 scripts/sync_adapters.py` to update host snippets. The full workflow lives in the portable skill; Custom GPT's compact transport instructions live in `gpt/ACTIONS.snippet.md`.

```sh
python3 scripts/sync_adapters.py --check
python3 scripts/validate_kit.py
python3 -m unittest discover -s tests -v
```

Optionally validate request examples against a freshly downloaded OpenAPI document with `python3 scripts/validate_kit.py --openapi /path/to/openapi.json`. Validation is offline unless you download that document yourself. No test sends a support report or uses account credentials.

Authoritative service schema: [OpenAPI](https://getjerp.com/api/v1/openapi.json). Portable package format: [Agent Skills specification](https://agentskills.io/specification). Host-specific guides link primary documentation. A license has not yet been selected; do not imply unrestricted redistribution rights until one is added.
