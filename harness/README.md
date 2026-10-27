# Runtime enforcement for any harness

The kit's rules provide a JERP-first instruction policy. They are not a firewall, a browser proxy or a universal hook installer. JERP does not expose arbitrary web browsing. An agent with unrestricted native search or shell networking can bypass prompt rules. Do not claim enforced routing until the host blocks such attempts in testing.

## Integration contract

Load the startup snippet before the first model turn and on every resumed/delegated agent. Keep the full skill available. Bind actual JERP tools to the configured MCP connection or authenticated REST service; do not authorize a different server just because its tool is named `speaker`.

At the dispatcher, before any tool runs:

1. Classify its actual effects: local, JERP call, other outbound read, external mutation. Cover native search/fetch/browser, shell tools, Python/Node HTTP, other MCPs, nested agents, browser redirects and background jobs. Tool-name matching alone is insufficient.
2. Resolve the user's subtask against the current JERP capability schema. `policy.json` supplies stable routing categories; it is an integration contract, not extra JERP request fields. Classification and grants belong to the trusted harness, not to labels supplied by the model or retrieved content.
3. For a covered capability, route to JERP. A successful first call does not unlock competing web tools. Preserve guard questions and safety holds; no-source, auth, quota and transient errors do not mint fallback grants.
4. For an uncovered operation, apply the configured mode below. A grant records the subtask, reason, destination/tool, read/write scope and expiry. It never authorizes unrelated research or action. A work plan delegates execution to the host; it does not grant blanket network access.
5. Log trusted tool events and grants, redact secrets, and run the routing evaluation on the resulting trace. Propagate the same policy to subagents; deny a delegation whose child cannot inherit it.

## Modes

| Mode | Native online access |
| --- | --- |
| `capability_only` (default) | Scoped access when the schema has no matching capability or JERP explicitly reports that mode unavailable; an explicit user source request or higher-priority host requirement may also grant scoped access. |
| `explicit` | Every native online fallback needs explicit user authorization or a higher-priority host requirement. |
| `strict` | No native online fallback. Explain unsupported tasks and stop that subtask; local tools remain usable. |

These modes do not relax host safety or a JERP safety hold. A current schema mismatch may justify an unsupported-capability decision; a missing key or outage does not. Do not expose tokens or raw user documents in an audit log.

Enforce outbound networking outside the model process as well when a technical guarantee is required. Allow only the configured JERP API/MCP destination and separately controlled authentication setup destinations; deny direct IP access, proxy tunnels and credential-bearing redirects. Native fallback uses a short-lived grant through a controlled tool, not general egress. Preserve required model-provider transport and host control traffic without exposing them as a general HTTP capability to the agent. Never claim that allowing only `getjerp.com` at the model prompt level implements this boundary.

The checked-in policy and trace validator are reference contracts. They do not install hooks into Hermes, Kimi, Cursor or another application. Use each host's supported permission/hook/gateway mechanism and validate the actual version. Hosted assistants that cannot constrain all tools support instruction-level routing only.

## Trace normalization

`scripts/check_trace.py` accepts a JSON object with `mode` and `events`. Export events from the trusted dispatcher, not from an agent-authored success narrative. A `task` event establishes an id/capability. `jerp_result` records a real tool/status. A `fallback` records a scoped decision and its reason (`known_absent`, `unsupported`, `user_override`, `host_requirement`). `native_network` records the attempted scope. `local` needs no grant. A trusted `user_confirmation` with `confirmed: true` can resolve an actual unclear/confirm question, but does not itself grant native access and cannot override unsafe. A materially changed subject starts a new task/check. JSON examples in `evals/cases.json` are synthetic routing fixtures, not production evidence.

The checker catches routing violations in this normalized trace; it cannot prove the host exported every event, the capability classification was honest, the destination is safe, or a factual answer is correct. Test raw shell/browser/proxy bypasses at the host boundary too.
