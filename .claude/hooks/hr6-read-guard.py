#!/usr/bin/env python3
"""HR6: Block cache reads when invalidation is pending.

PreToolUse hook for cache_get_issue.
If a key has pending cache invalidation, blocks the read and forces
cache_invalidate first.

Exit codes: 0 = allow, 2 = deny
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hooks_state import hr6_get_pending

LOG_DIR = Path.home() / ".claude" / "hooks-logs"


def log_event(level: str, data: dict) -> None:
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        now = datetime.now(timezone.utc)
        entry = {"ts": now.isoformat(), "hook": "hr6-read-guard", "level": level, **data}
        with open(LOG_DIR / f"{now.strftime('%Y-%m-%d')}.jsonl", "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass


def main() -> None:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print("{}")
        return

    session_id = data.get("session_id", "")
    tool_input = data.get("tool_input", {})

    # Extract issue key from read request
    issue_key = None
    for field in ("issue_key", "issue_key_or_id", "key"):
        if field in tool_input:
            issue_key = str(tool_input[field])
            break

    if not issue_key:
        print("{}")
        return

    pending = hr6_get_pending(session_id)
    if issue_key in pending:
        reason = (
            f"HR6 BLOCKED: Cannot read {issue_key} — cache invalidation pending.\n"
            f"Run: cache_invalidate(issue_key='{issue_key}') first, then retry."
        )
        log_event("BLOCKED", {"issue_key": issue_key, "session_id": session_id})
        print(reason, file=sys.stderr)
        sys.exit(2)

    log_event("ALLOWED", {"issue_key": issue_key, "session_id": session_id})
    print("{}")


if __name__ == "__main__":
    main()
