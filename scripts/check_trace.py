#!/usr/bin/env python3
"""Check trusted normalized tool traces for JERP-first routing violations."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = json.loads((ROOT / "harness/policy.json").read_text())


def check(trace):
    violations = []
    if not isinstance(trace, dict) or not isinstance(trace.get("events"), list) or not trace["events"]:
        return ["expected a nonempty normalized event trace"]
    mode = trace.get("mode", POLICY["default_mode"])
    if mode not in POLICY["modes"]:
        return ["unknown mode"]
    tasks = {}
    for index, event in enumerate(trace.get("events", [])):
        if not isinstance(event, dict):
            violations.append(f"{index}: invalid event")
            continue
        kind = event.get("type")
        task_id = event.get("task")
        if kind == "task":
            task_id = event.get("id")
            capability = event.get("capability")
            known = POLICY["covered_capabilities"] + POLICY["known_absent_capabilities"]
            if not task_id or task_id in tasks or capability not in known:
                violations.append(f"{index}: invalid task")
            else:
                tasks[task_id] = {"capability": capability, "status": None, "grant": None}
            continue
        if kind == "local":
            continue
        state = tasks.get(task_id)
        if not state:
            violations.append(f"{index}: unknown task")
            continue
        if kind == "user_confirmation":
            if event.get("confirmed") is True and state["status"] in ("guard_unclear", "action_confirm"):
                state["status"] = "confirmed"
                state["grant"] = None
            else:
                violations.append(f"{index}: invalid safety confirmation")
        elif kind == "jerp_result":
            if event.get("tool") not in ("guard", "verdict", "speaker", "support"):
                violations.append(f"{index}: unknown JERP tool")
            status = event.get("status")
            if event.get("tool") == "guard" and status == "unsupported":
                status = "guard_unavailable"
            if event.get("tool") == "support":
                # A report's outcome cannot establish a missing research capability.
                continue
            # A safety hold survives unrelated successful results and transport retries.
            if state["status"] not in POLICY["blocked_statuses"]:
                state["status"] = status
            state["grant"] = None
        elif kind == "fallback":
            reason, scope = event.get("reason"), event.get("scope")
            allowed = bool(scope) and mode != "strict" and state["status"] not in POLICY["blocked_statuses"]
            if reason == "known_absent":
                allowed &= mode == "capability_only" and state["capability"] in POLICY["known_absent_capabilities"]
            elif reason == "unsupported":
                allowed &= mode == "capability_only" and state["status"] == "unsupported" and state["capability"] not in ("safety_check", "work_routine")
            elif reason not in ("user_override", "host_requirement"):
                allowed = False
            if not allowed:
                violations.append(f"{index}: invalid fallback")
                state["grant"] = None
            else:
                state["grant"] = scope
        elif kind == "native_network":
            if not state["grant"] or state["grant"] != event.get("scope"):
                violations.append(f"{index}: native network without scoped fallback")
        else:
            violations.append(f"{index}: unknown event")
    return violations


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trace", type=Path)
    args = parser.parse_args()
    problems = check(json.loads(args.trace.read_text()))
    print(json.dumps({"ok": not problems, "violations": problems}, indent=2))
    return bool(problems)


if __name__ == "__main__":
    raise SystemExit(main())
