#!/usr/bin/env python3
"""HR6: Track and enforce cache_invalidate after every Jira write.

PostToolUse hook for jira_create_issue, jira_update_issue, jira_transition_issue.
Records pending invalidation in session state (hr6-read-guard blocks stale reads)
and injects additionalContext reminder.

Exit codes: 0 (always — PostToolUse cannot block)
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hooks_state import hr6_add_pending

LOG_DIR = Path.home() / ".claude" / "hooks-logs"


def log_event(level: str, data: dict) -> None:
    """Append JSON log entry."""
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        now = datetime.now(timezone.utc)
        log_file = LOG_DIR / f"{now.strftime('%Y-%m-%d')}.jsonl"
        entry = {
            "ts": now.isoformat(),
            "hook": "hr6-cache-invalidate",
            "level": level,
            **data,
        }
        with open(log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass


def extract_issue_key(data: dict) -> str | None:
    """Extract issue key from tool_input or tool_response."""
    # Try tool_response first (create returns key)
    resp = data.get("tool_response", {})
    if isinstance(resp, str):
        try:
            resp = json.loads(resp)
        except (json.JSONDecodeError, TypeError):
            resp = {}
    if isinstance(resp, dict) and resp.get("key"):
        return resp["key"]

    # Try tool_input (update/transition has issue_key)
    inp = data.get("tool_input", {})
    for field in ("issue_key", "issue_key_or_id", "key"):
        if field in inp:
            return str(inp[field])

    return None


def main() -> None:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print("{}")
        return

    issue_key = extract_issue_key(data)
    if not issue_key:
        print("{}")
        return

    # Track pending invalidation in session state
    session_id = data.get("session_id", "")
    hr6_add_pending(session_id, issue_key)

    tool_name = data.get("tool_name", "unknown")
    log_event("REMIND", {
        "issue_key": issue_key,
        "tool": tool_name,
        "session_id": data.get("session_id", ""),
    })

    output = {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": (
                f"HR6 REQUIRED: Run cache_invalidate(issue_key='{issue_key}', auto_refresh=true) "
                f"before any subsequent read of {issue_key}. "
                f"auto_refresh=true fetches fresh data in the same call (saves 1 MCP round-trip). "
                f"Stale cache causes silent data corruption."
            ),
        }
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
