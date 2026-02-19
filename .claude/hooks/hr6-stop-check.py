#!/usr/bin/env python3
"""HR6 Stop Hook: Check for pending cache invalidations at session end.

Replaces the prompt-based stop hook with a deterministic Python check.
Reads session state file and reports any pending cache invalidations.

Output: {"ok": true} or {"ok": false, "reason": "..."}
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hooks_state import hr6_get_pending


def main() -> None:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print(json.dumps({"ok": True}))
        return

    session_id = data.get("session_id", "")
    pending = hr6_get_pending(session_id)

    if pending:
        keys = ", ".join(sorted(pending))
        print(
            json.dumps(
                {
                    "ok": False,
                    "reason": (
                        f"HR6: cache_invalidate missing for: {keys}. "
                        f"Run cache_invalidate for each before ending session."
                    ),
                }
            )
        )
    else:
        print(json.dumps({"ok": True}))


if __name__ == "__main__":
    main()
