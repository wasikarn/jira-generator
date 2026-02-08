#!/usr/bin/env python3
"""L3: Block Glob/Grep on indexed projects until qmd is used first.

PreToolUse hook — blocks exploration tools if:
1. Target path is in a qmd collection
2. qmd hasn't been used yet this session
3. Tool is Glob or Grep (Read is always allowed for editing)

Safeguards:
- Read is never blocked (needed for file editing)
- Passes through if qmd was already used this session
- Only activates for known indexed project paths

Exit 0 = allow, Exit 2 = block
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

# Only block Glob and Grep — never block Read (needed for editing)
if tool_name not in ("Glob", "Grep"):
    sys.exit(0)

# Already used qmd this session — allow everything
if qmd_is_used(session_id):
    sys.exit(0)

# Extract target path
target_path = tool_input.get("path", "") or tool_input.get("pattern", "")
if not target_path:
    sys.exit(0)

# Check if path is in an indexed collection
collection = qmd_collection_for_path(target_path)
if not collection:
    sys.exit(0)

# Block with helpful message
print(json.dumps({
    "error": (
        f"⚠️ [{collection}] is indexed by qmd — use qmd search first to save ~95% tokens.\n"
        f"→ mcp__qmd__search(query=\"...\", collection=\"{collection}\") for keyword search\n"
        f"→ mcp__qmd__vsearch(query=\"...\", collection=\"{collection}\") for semantic search\n"
        f"After using qmd, Glob/Grep will be unblocked for this session."
    )
}))
sys.exit(2)
