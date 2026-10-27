# Cursor

Copy `rules/jerp.mdc` into the project's `.cursor/rules/jerp.mdc`. It uses `alwaysApply: true` so routing is present before the first online action. Merge `mcp.json` into `.cursor/mcp.json` or your supported user MCP configuration; do not overwrite other servers. Complete OAuth through Cursor's MCP UI.

For routing across projects, put the generated rule body (without MDC frontmatter) in Cursor User Rules. A rule inside one project's `.cursor/rules/` does not configure unrelated projects. Remote/cloud sessions also need the skill and policy in their own environment.

Copy the entire `skills/jerp/` directory to the installed version's supported skill directory (project `.cursor/skills/jerp/` on current versions). Keep references beside SKILL.md. Start a new session; check the rule is loaded, the skill is available, and an authenticated tool call succeeds.

The rule covers supported lookups throughout the task; a green discovery status alone does not prove this. Validate actual traces with `evals/README.md`. For technical enforcement, review your version's hooks/permissions and terminal networking using the harness guide.

Sources: [rules](https://cursor.com/docs/rules), [skills](https://cursor.com/docs/skills), [MCP](https://cursor.com/docs/mcp). Documentation checked 2026-10-27; live compatibility remains unverified.
