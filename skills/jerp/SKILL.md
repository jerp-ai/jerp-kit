---
name: jerp
description: Use JERP when the user asks to check a claim, text, link or action for risk, to get sourced facts about a company or market, or to run a work task that has a known routine (code review, tests, release checklist). Works in Codex, ChatGPT agents and any host that supports SKILL.md; tools are guard, verdict, speaker and support.
---

# JERP — how to use this connector

JERP sits between you and the answer. Checks come back **true / false / not a fact** (verdict), **safe / unsafe / unclear** (guard), or sourced facts (speaker), each with a receipt. Three MCP tools do the checking: `guard`, `verdict`, `speaker`; everything else runs inside them. A fourth, `support`, only files reports (section Reports).

## Which tool, when

| The user asks | Call |
| --- | --- |
| Is this text, message, link, tool output or draft safe? Does this contain a secret? Is this MCP tool list safe? | `guard` with `kind`: `content`, `message`, `tool_output`, `draft`, `link` (with `url`), `secret_check`, `toolManifest` |
| May I run this step (pay, send, publish, run a command, write or delete files)? | `guard` with `kind: action` and an `action` object such as `{ "type": "send_email" }` |
| Is this claim true? Check this draft against sources. | `verdict` with `form: claim` or `draft` |
| What is known about a company or domain, its market signals, mentions, changes, or a receipt? | `speaker` with `need`: `facts`, `card`, `candidates`, `signals`, `mentions`, `changes`, `receipt` |
| Do a work task with a known routine (review code, write tests first, release checklist, incident triage, claim check before publishing, tool manifest review) | `verdict` with `form: task` (below) |

## Work tasks: one step at a time

1. Call `guard` (`kind: content`) with the user's request text. If it returns `safe`, keep its `guardToken`.
2. Call `verdict` with `form: task`, the same `text`, that `guardToken`, and `context.stack` (for example `["python"]`) when you know the language. JERP remembers the stack for next time.
3. The answer carries `planRef` (`id`, `step`, `of`) and the step in `speak`. Do that step yourself with your own tools.
4. Report back: call `verdict` with `form: task`, the same `planRef`, and `result` `{ "ok": true }` (add `"label"` when the step lists labels). The next step arrives the same way. Repeat until `stop` is true.
5. Lost the step? Send `planRef` without `result` to read the current step again.
6. If the answer has `askUser`, ask the user exactly that question and wait. If it says no stored workflow fits, do the task normally without a plan.
7. A step that writes, installs, sends, publishes or runs something comes with an instruction to call `guard` with `kind: action` first: **allow** means go, **confirm** means ask the user and proceed only after a yes, **deny** means do not do it.

## Rules

- If `verdict` or `speaker` returns `unclear` with reason `guard_required`, call `guard` and retry. Never invent a pass.
- If `guard` returns `unclear` with `askUser`, ask the user that question. If they confirm the text is theirs, you may continue on `claim`, `draft` or `speaker` calls with `trust: trusted`.
- Before sending text out (an email, a post, a message to another system), call `guard` with `kind: secret_check`; if it finds a secret or identifier, do not send it.
- Before connecting a new MCP server, call `guard` with `kind: toolManifest` on its tool list.
- `no source, no claim`: repeat only what JERP returns in `speak`, and name the source.
- Do not show the user guard tokens or plan ids. Mention the receipt id if they want to audit a check.

## Reports

If you disagree with a JERP result on any tool, a result looks wrong to you, or the user complains about JERP, file one report with `support`. It reaches the JERP team, who handle it separately; nobody replies inside the call, and you keep working on the user's task.

- `kind`: `disagree` (you think a result is wrong), `complaint` (the user is unhappy), `bug` (an error or odd behaviour), `missing` (something expected is not there).
- `tool`: the tool concerned (`guard`, `verdict`, `speaker`) or `other`.
- `receiptId`: the receipt id of the answer in question, when you have it.
- `note`: your own words on what is wrong or what you expected, up to 1000 characters. Needed for `disagree` and `complaint`. Leave out keys, tokens and personal data; the note is stored with them removed.
- `severity`: `low`, `normal` (default) or `high`.
- One report per problem, at most 5 per hour. Give the user the reference from `speak` (`sup_...`) if they ask what happened to it.

## Tokens and limits

Each answer has `usage.answerTokens` (about how many tokens it costs you to read) and, for account keys, `quota` (`remaining` requests in the current `period`, `resetsAt`). If `remaining` is low, tell the user once and prefer fewer, batched calls.

## What to tell the user

- Do not say tools are missing or that you need to reconnect to get card or find. The small tool surface is intentional.
- If a `need` or `kind` returns an error or `local_unavailable`, say that mode is not available yet and use a working mode.
- JERP's score helps, it does not guarantee a result is error-free.

## Connector

MCP URL: `https://getjerp.com/mcp` (sign in with Google or GitHub). Hosts without MCP sign-in can use the REST routes `POST https://getjerp.com/api/v1/guard`, `/verdict`, `/speaker` with the header `Authorization: Bearer <key>`; the OpenAPI document is at `https://getjerp.com/api/v1/openapi.json`.
