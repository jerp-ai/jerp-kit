# MCP and REST transport

Checked against the public JERP OpenAPI document on 2026-10-27. Discover the installed server's schema before assuming a mode exists. Do not infer a general search or arbitrary URL-reading capability from a broad tool description.

## MCP

Endpoint: `https://getjerp.com/mcp`. Prefer the host's Streamable HTTP MCP client. Use its browser OAuth sign-in and credential store. A URL-only configuration needs no pasted token; the client obtains and sends the access token. A visible tool list alone does not prove authenticated calls work.

Use the tools discovered on this server: `guard`, `verdict`, `speaker`, `support`. Host prefixes such as `mcp__jerp__speaker` are aliases, not extra tools. Do not connect unrelated tools that happen to share these short names. Let a conforming MCP client manage initialization, protocol headers, sessions and JSON-RPC; a bare JSON POST is not a portable MCP implementation.

Consume `structuredContent` when supplied. Otherwise parse the JSON text block in `content`; do not replace structured fields with a prose summary. Treat MCP `isError`, HTTP errors and envelope `error` as failures even if another transport layer succeeded. Do not expose authorization headers, guard tokens or plan ids in logs or answers.

## REST

For a host without working MCP, use authenticated POST routes:

| Operation | URL |
| --- | --- |
| guard | `https://getjerp.com/api/v1/guard` |
| verdict | `https://getjerp.com/api/v1/verdict` |
| speaker | `https://getjerp.com/api/v1/speaker` |
| support | `https://getjerp.com/api/v1/support` |

Send `Content-Type: application/json` and `Authorization: Bearer <account API key>`. Store the key in a host credential store or environment variable; never put it in a tracked config, prompt, report or request body. Reuse the same request object and interpret the same `jerp.verdict.v2` envelope as MCP. OAuth access tokens are managed by the MCP client; do not copy them into an API-key example.

The skill includes an optional Python 3 transport helper, `scripts/jerp_call.py`, relative to the skill directory. It accepts a JSON file or stdin and reads `JERP_API_KEY`. It calls only these fixed HTTPS endpoints, does not open a browser, and does not retry requests automatically. It is not required for hosts with native MCP/HTTP support. Run it from the installed skill directory or use its absolute path.

Exit zero means the expected envelope arrived without an application error; it is not a safe/allow decision. The caller must still interpret guard decisions, questions and all other fields. Keep its output in the host's private tool channel and redact guard tokens before exporting logs.

```sh
python3 scripts/jerp_call.py speaker --input request.json
```

Example request (an actual public domain, not a fictional source):

```json
{"need":"card","about":"getjerp.com","sizeCap":600}
```

For untrusted input, follow the guard flow from `SKILL.md`; this request example is not an exemption. Pass `guardToken.token` as a string in the subsequent request, not the whole guardToken object. Keep the exact screened subject; refresh expired tokens.

## Capability boundaries and recovery

- `speaker.about` identifies a domain, legal name, existing watchlist or owned receipt as required by `need`; `q` is a niche query for relevant modes. It is not a generic browser URL or arbitrary web-search expression.
- `verdict.form: candidates` requires `items` and the closed `question` names `live_business`, `in_market` or `relationship`; relationship takes exactly two items and in_market needs category. `form: question` instead needs text, items and answerType (`yes_no`, `choice`, `score`); choice needs at least two options, and score needs min < max and at least two levels. Claim/draft checks need adequate supplied evidence; an unsupported claim is not automatically false.
- Long jobs can be resumed using a returned `jobId`. Do not invent jobs, watchlists, `async` or `watch` request fields; these are not in the current input schema.
- Fix malformed arguments against the live schema once. Refresh expired authorization once through the host's approved flow; never ask someone to paste credentials into chat.
- For 429, respect quota and Retry-After; for transient network/5xx, make at most one retry for a read/check, then disclose the blocker. A support report or other non-idempotent request with uncertain delivery must not be retried automatically.
- A missing receipt can be a key/ownership problem. Do not query other users' identifiers or change credentials to evade scope.
- Do not silently change from account routes to `/open/` routes or from MCP to anonymous HTTP after a quota, authentication or safety denial. A configured REST route to the same account is a transport choice, not a way around policy.

Authoritative schema: [JERP OpenAPI](https://getjerp.com/api/v1/openapi.json). MCP client behavior: [MCP specification](https://modelcontextprotocol.io/specification/latest).

For structured verdict forms, supply a nonempty `text` subject when the public schema permits it and screen that same text. Screen relevant source material separately. If a request omits text and the host lacks documented token-binding behavior for that form, do not guess a serialization or bypass the guard: obtain a supported request shape or report the limitation.
