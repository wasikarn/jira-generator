#!/usr/bin/env python3
"""Q: ADF Template Structure Validator.

PreToolUse hook for Bash. Validates ADF JSON structure matches
template requirements before acli writes to Jira.

Checks required headings by issue type, panel presence, non-empty content.
Complements HR1 QG scoring with fast structural pre-check.

Exit codes: 0 = allow, 2 = block (structure invalid)
"""
import json
import re
import sys
from pathlib import Path

ACLI_RE = re.compile(
    r"acli\s+jira\s+workitem\s+(?:create|edit)\s+"
    r"(?:.*\s)?--from-json\s+[\"']?([^\s\"']+)[\"']?"
)

# Required headings by issue type (normalized lowercase, emoji-stripped)
REQUIRED_HEADINGS = {
    "epic": ["epic overview"],
    "story": ["user story", "acceptance criteria"],
    "subtask": ["objective"],
    "qa": ["test objective", "test cases"],
    "task": [],
}

TYPE_KEYWORDS = {
    "epic": re.compile(r"epic", re.I),
    "story": re.compile(r"story", re.I),
    "subtask": re.compile(r"subtask|sub[-_]", re.I),
    "qa": re.compile(r"qa|testplan|test[-_]plan", re.I),
    "task": re.compile(r"task|migration|spike|chore|tech[-_]debt", re.I),
}


def extract_headings(content: list) -> list[str]:
    headings = []
    for node in content:
        if node.get("type") == "heading":
            texts = []
            for child in node.get("content", []):
                if child.get("type") == "text":
                    texts.append(child.get("text", ""))
            headings.append("".join(texts))
    return headings


def normalize(h: str) -> str:
    return re.sub(r"^[^\w]*", "", h).strip().lower()


def has_panel(content: list) -> bool:
    return any(node.get("type") == "panel" for node in content)


def detect_type(file_path: Path, data: dict) -> str:
    type_val = str(data.get("type", "")).lower()
    for itype, pattern in TYPE_KEYWORDS.items():
        if pattern.search(type_val):
            return itype
    name = file_path.stem.lower()
    for itype, pattern in TYPE_KEYWORDS.items():
        if pattern.search(name):
            return itype
    return "subtask"


raw = sys.stdin.read()
data = json.loads(raw)

if data.get("tool_name") != "Bash":
    sys.exit(0)

cmd = data.get("tool_input", {}).get("command", "")
match = ACLI_RE.search(cmd)
if not match:
    sys.exit(0)

json_path = Path(match.group(1))
if not json_path.is_absolute():
    json_path = Path(data.get("cwd", ".")) / json_path

if not json_path.exists():
    sys.exit(0)

try:
    adf_data = json.loads(json_path.read_text())
except (json.JSONDecodeError, OSError):
    sys.exit(0)

desc = adf_data.get("description", {})
if not isinstance(desc, dict) or desc.get("type") != "doc":
    print(
        'ADF STRUCTURE ERROR: description must be {"type": "doc", "version": 1, "content": [...]}',
        file=sys.stderr,
    )
    sys.exit(2)

content = desc.get("content", [])
if not content:
    print("ADF STRUCTURE ERROR: description.content is empty", file=sys.stderr)
    sys.exit(2)

issue_type = detect_type(json_path, adf_data)
headings = extract_headings(content)
heading_normalized = [normalize(h) for h in headings]

required = REQUIRED_HEADINGS.get(issue_type, [])
missing = [r for r in required if not any(r in h for h in heading_normalized)]

if missing:
    print(
        f"ADF STRUCTURE ERROR ({issue_type}): Missing required headings: {', '.join(missing)}\n"
        f"Found: {headings}\n"
        f"Fix the ADF JSON template structure before writing.",
        file=sys.stderr,
    )
    sys.exit(2)

if issue_type != "task" and not has_panel(content):
    # Warning only — print to stdout, exit 0
    print(
        f"⚠️ ADF structure ({issue_type}): No panel found. "
        f"Templates require panels (info/success/warning/error)."
    )

sys.exit(0)
