# Public repository boundary

This repository distributes user-facing JERP integration instructions, configuration examples, helpers and synthetic acceptance tests. Every committed file is public.

Keep internal review reports, agent/model execution notes, raw conversations and tool traces, incident details, production receipts, customer/employee data, company plans, infrastructure details, provider implementation details and financial information outside this repository. Never copy service source code or private documents into this kit. Describe only the public client contract needed for integration.

Credentials, cookies, private keys, connection strings and personal machine paths must not appear in examples, fixtures, reports or logs. Use clearly nonfunctional test values and public documentation endpoints. Test output and local security-scan reports stay outside the checkout. Do not upload sensitive material to a remote checker to decide whether it is sensitive.

Before committing or publishing, inspect the full diff and every new file, run `python3 scripts/validate_kit.py`, and use an approved secret scanner when available. The validator catches selected high-confidence credential patterns, personal filesystem paths and disallowed private-artifact names. It cannot establish that prose contains no confidential information; human content review remains necessary. Never print matched secret values while reporting a finding.

`.gitignore` is a convenience, not a security boundary: tracked files and forced additions can still be published. Do not add internal reports under another name to bypass the public-content check. If a secret was already published, remove it from use and follow the owner's incident process; deleting the latest file does not revoke a credential or remove Git history.
