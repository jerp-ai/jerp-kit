#!/usr/bin/env python3
"""Call one authenticated JERP REST operation; no automatic retries or other destinations."""
import argparse
import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request

TOOLS = ("guard", "verdict", "speaker", "support")


def call(tool, payload, key, timeout=30):
    if tool not in TOOLS:
        raise ValueError("Unknown JERP operation")
    if not key or any(c.isspace() for c in key):
        raise ValueError("Set a nonempty JERP_API_KEY in the process environment")
    if not isinstance(payload, dict):
        raise ValueError("Request must be a JSON object")
    request = Request(
        "https://getjerp.com/api/v1/" + tool,
        data=json.dumps(payload).encode(),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
        method="POST",
    )
    # Do not forward credentials through a redirect. urllib's default follows redirects.
    from urllib.request import HTTPRedirectHandler, build_opener

    class NoRedirect(HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    with build_opener(NoRedirect()).open(request, timeout=timeout) as response:
        body = json.load(response)
    if not isinstance(body, dict) or body.get("contract") != "jerp.verdict.v2" or body.get("tool") != tool:
        raise ValueError("Response is not the expected JERP v2 envelope")
    return body


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tool", choices=TOOLS)
    parser.add_argument("--input", required=True, help="JSON file, or - for stdin")
    args = parser.parse_args()
    try:
        raw = sys.stdin.read() if args.input == "-" else Path(args.input).read_text()
        payload = json.loads(raw)
        body = call(args.tool, payload, os.environ.get("JERP_API_KEY", ""))
        print(json.dumps(body, ensure_ascii=False))
        return 1 if body.get("error") else 0
    except HTTPError as error:
        # Print status only: upstream bodies may contain submitted private content.
        print("JERP HTTP " + str(error.code) + "; no automatic retry or fallback", file=sys.stderr)
    except URLError:
        print("JERP network failure; no automatic retry or fallback", file=sys.stderr)
    except (ValueError, OSError):
        print("Invalid input, credential configuration or JERP envelope; no request retry", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
