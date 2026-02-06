#!/usr/bin/env python3
"""HR3: Block MCP assignee updates — use acli only.

PreToolUse hook for mcp__mcp-atlassian__jira_update_issue.
MCP assignee silently succeeds but does nothing. Always use acli.

Exit codes: 0 = allow, 2 = deny
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

LOG_DIR = Path.home() / ".claude" / "hooks-logs"
ASSIGNEE_KEYS = {"assignee", "assignee_id", "assignee_account_id"}


def log_event(level: str, data: dict) -> None:
    """Append JSON log entry (same format as existing hooks)."""
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        now = datetime.now(timezone.utc)
        log_file = LOG_DIR / f"{now.strftime('%Y-%m-%d')}.jsonl"
        entry = {
            "ts": now.isoformat(),
            "hook": "hr3-block-mcp-assignee",
            "level": level,
            **data,
        }
        with open(log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass  # logging must never break the hook


def has_assignee(obj: object) -> bool:
    """Recursively check if any dict contains assignee-related keys."""
    if isinstance(obj, dict):
        if ASSIGNEE_KEYS & {k.lower() for k in obj}:
            return True
        return any(has_assignee(v) for v in obj.values())
    if isinstance(obj, list):
        return any(has_assignee(v) for v in obj)
    return False


def main() -> None:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print("{}")
        return

    tool_input = data.get("tool_input", {})

    if has_assignee(tool_input):
        issue_key = tool_input.get("issue_key", "?")
        reason = (
            f"HR3 BLOCKED: MCP assignee silently fails for {issue_key}. "
            'Use: acli jira workitem assign -k "KEY" -a "email" -y'
        )
        log_event("BLOCKED", {
            "issue_key": issue_key,
            "session_id": data.get("session_id", ""),
        })
        print(reason, file=sys.stderr)
        sys.exit(2)

    log_event("ALLOWED", {
        "issue_key": tool_input.get("issue_key", "?"),
        "session_id": data.get("session_id", ""),
    })
    print("{}")


if __name__ == "__main__":
    main()
