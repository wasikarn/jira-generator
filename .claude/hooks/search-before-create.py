#!/usr/bin/env python3
"""Search-before-create: Remind to search for duplicates before creating issues.

PostToolUse hook for jira_create_issue.
Checks if jira_search was called in this session. If not, injects reminder.

Exit codes: 0 (always — PostToolUse cannot block)
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hooks_state import search_is_done

LOG_DIR = Path.home() / ".claude" / "hooks-logs"


def log_event(level: str, data: dict) -> None:
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        now = datetime.now(timezone.utc)
        entry = {"ts": now.isoformat(), "hook": "search-before-create", "level": level, **data}
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

    if search_is_done(session_id):
        print("{}")
        return

    # Extract created issue info
    resp = data.get("tool_response", {})
    if isinstance(resp, str):
        try:
            resp = json.loads(resp)
        except (json.JSONDecodeError, TypeError):
            resp = {}
    issue_key = resp.get("key", "?") if isinstance(resp, dict) else "?"

    log_event("WARN", {"issue_key": issue_key, "session_id": session_id})

    output = {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": (
                f"DEDUP WARNING: {issue_key} created without prior search in this session. "
                f"Verify no duplicates exist. Use /search-issues or "
                f"jira_search(jql='project = BEP AND summary ~ \"keyword\"') "
                f"before creating issues."
            ),
        }
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
