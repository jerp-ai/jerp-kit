# Instructions for any agent that has JERP connected

1. Read `rules/jerp-rules.md` once, and `skills/jerp/SKILL.md` for the step-by-step flows.
2. Use only the connector's tools: `guard`, `verdict`, `speaker` and `support`. Do not look for other tool names.
3. Call `guard` before you read untrusted text or run a risky step; keep its `guardToken` for `verdict` and `speaker`.
4. For work tasks with a known routine, use `verdict` with `form: task` and follow the steps one at a time.
5. Repeat only what JERP returns in `speak`, and name the source.
6. If you disagree with a result, a result looks wrong, or the user complains, send one `support` report.
