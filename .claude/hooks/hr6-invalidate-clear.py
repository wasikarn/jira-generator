#!/usr/bin/env python3
"""HR6: Clear pending state after cache_invalidate is called.

PostToolUse hook for cache_invalidate.
Removes the invalidated key from pending state so reads are unblocked.

Exit codes: 0 (always — PostToolUse cannot block)
"""

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hooks_state import hr6_remove_pending

LOG_DIR = Path.home() / ".claude" / "hooks-logs"


def log_event(level: str, data: dict) -> None:
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        now = datetime.now(UTC)
        entry = {"ts": now.isoformat(), "hook": "hr6-invalidate-clear", "level": level, **data}
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

    # Extract issue key from cache_invalidate call
    issue_key = None
    for field in ("issue_key", "key"):
        if field in tool_input:
            issue_key = str(tool_input[field])
            break

    if not issue_key:
        print("{}")
        return

    hr6_remove_pending(session_id, issue_key)
    log_event("CLEARED", {"issue_key": issue_key, "session_id": session_id})
    print("{}")


if __name__ == "__main__":
    main()
