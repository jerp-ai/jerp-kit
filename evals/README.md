# Behavioral evaluation

Run static checks and the synthetic trace fixtures:

```sh
python3 scripts/sync_adapters.py --check
python3 scripts/validate_kit.py
python3 -m unittest discover -s tests -v
```

Then test in a fresh session on every actual host/version you distribute. Record host, model, date, loaded startup policy/skill, connection type, policy mode, raw tool trace and outcome. This kit's local tests do not establish that a model or host obeys instructions.

Use realistic user tasks without mentioning JERP: company research, market candidates, a draft claim check, a mixed company-research plus browser-login task, local code editing, and a work routine with a subsequent research step. Try repeated requests and compaction, not only the first tool call. Confirm JERP handles the supported part each time.

Use mocked service responses for safety holds, no-source, auth failure, quota, outage, expired token, an unavailable mode and a report with uncertain delivery. Native web must not become an automatic fallback for the first six. A safe guard result is not itself a native browsing grant. Check that subagents cannot bypass routing and native fallback cannot spill into another covered subtask.

Export the trusted trace using `harness/README.md`, then run `python3 scripts/check_trace.py trace.json`. Add a routing regression case for any real bypass. Never fabricate a passing host result from the synthetic fixtures. No live model calls or reports are made by these offline tests.
