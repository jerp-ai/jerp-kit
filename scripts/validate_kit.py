#!/usr/bin/env python3
"""Offline package/link/config checks; optionally compare examples with JERP OpenAPI."""
import argparse
import json
import re
from pathlib import Path
from sync_adapters import rendered

ROOT = Path(__file__).resolve().parents[1]


def public_content_errors(root):
    errors = []
    patterns = {
        "private key": r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        "GitHub credential": r"\b(?:ghp_|github_pat_)[A-Za-z0-9_]{20,}\b",
        "AWS access key": r"\bAKIA[0-9A-Z]{16}\b",
        "JERP credential": r"\bjerp_[A-Za-z0-9_]{32,}\b",
        "live guard token": r"\bjgt_[A-Za-z0-9]{20,}\b",
        "personal filesystem path": r"/(?:Users|home)/[A-Za-z0-9_.-]+/",
        "credential in connection URL": r"\b(?:postgres|mysql|mongodb|redis)://[^\s/:]+:[^\s@]+@",
    }
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(part in (".git", "__pycache__") for part in relative.parts) or not path.is_file():
            continue
        name = str(relative)
        private_path = any(part in (".private", "internal", "reports") for part in relative.parts)
        private_path |= bool(re.match(r"evals/.*(?:review|report).*\.md$", name, re.I))
        private_path |= path.suffix in (".pem", ".key", ".p12", ".pfx", ".sarif")
        private_path |= path.name.startswith(".env") and not path.name.endswith(".example")
        if private_path:
            errors.append(name + ": private artifact does not belong in public kit")
        if not path.resolve().is_relative_to(root.resolve()):
            errors.append(name + ": symlink points outside public kit")
            continue
        try:
            content = path.read_text()
        except UnicodeDecodeError:
            continue
        for label, pattern in patterns.items():
            if re.search(pattern, content):
                errors.append(name + ": possible " + label + " (value withheld)")
    return errors


def validate(openapi=None):
    errors = public_content_errors(ROOT)
    for path in ROOT.rglob("*.json"):
        if ".git" not in path.parts:
            try:
                json.loads(path.read_text())
            except (ValueError, OSError) as error:
                errors.append(str(path.relative_to(ROOT)) + ": " + str(error))
    index = json.loads((ROOT / "index.json").read_text())
    for host, files in index["agents"].items():
        for name in files:
            if not (ROOT / name).is_file():
                errors.append(host + ": missing " + name)
    for name, content in rendered().items():
        path = ROOT / name
        if not path.exists() or path.read_text() != content:
            errors.append("stale generated adapter: " + name)
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if "://" in target or target.startswith("#"):
                continue
            target = target.split("#", 1)[0]
            if target and not (path.parent / target).exists():
                errors.append(str(path.relative_to(ROOT)) + ": broken link " + target)
    skill = (ROOT / "skills/jerp/SKILL.md").read_text()
    if not skill.startswith("---\n") or "name: jerp\n" not in skill.split("---", 2)[1]:
        errors.append("invalid skill metadata")
    if len((ROOT / "gpt/INSTRUCTIONS.md").read_text()) > 8000:
        errors.append("Custom GPT instructions exceed 8000 characters")
    if "alwaysApply: true" not in (ROOT / "cursor/rules/jerp.mdc").read_text().split("---", 2)[1]:
        errors.append("Cursor policy is not always applied")
    if openapi:
        document = json.loads(Path(openapi).read_text())
        for tool in ("guard", "verdict", "speaker", "support"):
            if "/api/v1/" + tool not in document["paths"]:
                errors.append("live schema missing " + tool)
        for path in (ROOT / "skills/jerp").rglob("*.md"):
            for raw in re.findall(r"```json\s*\n(.*?)\n```", path.read_text(), re.S):
                value = json.loads(raw)
                tool = "verdict" if "form" in value else "speaker" if "need" in value else "guard" if "kind" in value else None
                if not tool:
                    errors.append("unmapped request example: " + str(path))
                    continue
                schema = document["paths"]["/api/v1/" + tool]["post"]["requestBody"]["content"]["application/json"]["schema"]
                if set(value) - set(schema["properties"]) or set(schema.get("required", [])) - set(value):
                    errors.append("example fields disagree with live schema: " + str(path))
                for key, field in value.items():
                    enum = schema["properties"].get(key, {}).get("enum")
                    if enum and field not in enum:
                        errors.append("example enum disagrees with live schema: " + key)
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--openapi", type=Path)
    args = parser.parse_args()
    errors = validate(args.openapi)
    print(json.dumps({"ok": not errors, "errors": errors}, indent=2))
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
