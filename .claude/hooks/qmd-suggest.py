#!/usr/bin/env python3
"""L2: Suggest qmd when Glob/Grep/Read targets an indexed project.

PostToolUse hook — suggestion only, never blocks.
Triggers once per session (stops suggesting after qmd is used).

Exit 0 = always allow
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hooks_state import qmd_collection_for_path, qmd_is_used

raw = sys.stdin.read()
data = json.loads(raw)
tool_name = data.get("tool_name", "")
tool_input = data.get("tool_input", {})
session_id = data.get("session_id", "")

# Only trigger on exploration tools
if tool_name not in ("Glob", "Grep", "Read"):
    sys.exit(0)

# Already using qmd this session — stop nagging
if qmd_is_used(session_id):
    sys.exit(0)

# Extract target path
target_path = tool_input.get("file_path", "") or tool_input.get("path", "")
if not target_path:
    sys.exit(0)

# Check if path is in an indexed collection
collection = qmd_collection_for_path(target_path)
if not collection:
    sys.exit(0)

print(
    json.dumps(
        {
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": (
                    f"💡 [{collection}] is indexed by qmd. "
                    f"Use mcp__qmd__search/vsearch first → ~95% fewer tokens than {tool_name}. "
                    f"Fallback to {tool_name} only if qmd returns nothing."
                ),
            }
        }
    )
)
sys.exit(0)
