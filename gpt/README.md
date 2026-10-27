# Custom GPT / REST Actions

Paste the complete generated `INSTRUCTIONS.md` into the GPT's Instructions. It includes persistent routing and compact call/recovery rules; it does not rely on Knowledge retrieval to activate JERP-first. The kit validator checks its character budget. `ACTIONS.snippet.md` is source material for the generator, not a second installation step.

Import `https://getjerp.com/api/v1/openapi.json` into Actions. Configure account API-key Bearer authentication in the credential UI. Never put credentials in Instructions or Knowledge. Attach the skill and its references as Knowledge if the host supports it; the installed Instructions still supply the core workflow.

An Actions-only GPT uses REST, not a local MCP config or MCP browser OAuth. Do not switch to anonymous routes after a quota or authentication error. Test actual action names, fields and envelopes after importing a new schema; the live service contract is authoritative.

If the host cannot disable native web tools or apply network controls, this is instruction-level routing. Use the generic harness guide for stricter environments. Configuration file checks do not establish live GPT behavior.
