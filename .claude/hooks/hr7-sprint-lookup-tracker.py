#!/usr/bin/env python3
"""HR7: Track sprint lookups to validate sprint ID usage.

PostToolUse hook for jira_get_sprints_from_board.
Records that a sprint lookup was done in this session.

Exit codes: 0 (always — PostToolUse cannot block)
"""

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hooks_state import hr7_mark_lookup_done

LOG_DIR = Path.home() / ".claude" / "hooks-logs"


def log_event(level: str, data: dict) -> None:
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        now = datetime.now(UTC)
        entry = {"ts": now.isoformat(), "hook": "hr7-sprint-lookup-tracker", "level": level, **data}
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
    hr7_mark_lookup_done(session_id)
    log_event("TRACKED", {"session_id": session_id})
    print("{}")


if __name__ == "__main__":
    main()
