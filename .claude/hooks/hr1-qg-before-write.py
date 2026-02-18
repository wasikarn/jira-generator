#!/usr/bin/env python3
"""HR1: Quality Gate >= 90% before Atlassian writes.

PreToolUse hook for Bash tool. Intercepts acli commands that write
ADF JSON to Jira and validates the JSON file against quality gate.

Only matches:
  acli jira workitem create --from-json <path>
  acli jira workitem edit --from-json <path>

Exit codes: 0 = allow (or not an acli command), 2 = deny (QG < 90%)
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── Paths ──────────────────────────────────────────────
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "skills" / "atlassian-scripts"
LOG_DIR = Path.home() / ".claude" / "hooks-logs"

# ── Regex: match acli write commands ───────────────────
ACLI_FROM_JSON_RE = re.compile(
    r"acli\s+jira\s+workitem\s+(?:create|edit)\s+"
    r"(?:.*\s)?--from-json\s+[\"']?([^\s\"']+)[\"']?"
)

# ── Issue type inference from filename ─────────────────
TYPE_PATTERNS = [
    ("story", re.compile(r"story", re.I)),
    ("subtask", re.compile(r"subtask|sub[-_]", re.I)),
    ("epic", re.compile(r"epic", re.I)),
    ("qa", re.compile(r"qa|testplan|test[-_]plan", re.I)),
    ("task", re.compile(r"task|migration|spike|chore|tech[-_]debt", re.I)),
]


def log_event(level: str, data: dict) -> None:
    """Append JSON log entry."""
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        now = datetime.now(timezone.utc)
        log_file = LOG_DIR / f"{now.strftime('%Y-%m-%d')}.jsonl"
        entry = {
            "ts": now.isoformat(),
            "hook": "hr1-qg-before-write",
            "level": level,
            **data,
        }
        with open(log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass


def detect_issue_type(file_path: Path, data: dict) -> str:
    """Detect issue type from CREATE format type field or filename."""
    # 1. Try CREATE format explicit type field
    type_val = str(data.get("type", "")).lower()
    if "story" in type_val:
        return "story"
    if "sub" in type_val:
        return "subtask"
    if "epic" in type_val:
        return "epic"
    if "task" in type_val and "sub" not in type_val:
        return "task"  # Task has its own checks (no narrative required)

    # 2. Try filename inference
    name = file_path.stem.lower()
    for issue_type, pattern in TYPE_PATTERNS:
        if pattern.search(name):
            return issue_type

    # 3. Default to subtask (most common, strictest checks)
    return "subtask"


def main() -> None:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print("{}")
        return

    # Only process Bash tool
    if data.get("tool_name") != "Bash":
        print("{}")
        return

    cmd = data.get("tool_input", {}).get("command", "")

    # Check if this is an acli write command with --from-json
    match = ACLI_FROM_JSON_RE.search(cmd)
    if not match:
        print("{}")
        return

    json_path = Path(match.group(1))
    # Resolve relative paths against cwd
    if not json_path.is_absolute():
        json_path = Path(data.get("cwd", ".")) / json_path

    if not json_path.exists():
        # File not found — let acli handle the error
        log_event("SKIP", {"reason": "file_not_found", "file": str(json_path)})
        print("{}")
        return

    # Load the ADF JSON file
    try:
        with open(json_path) as f:
            adf_data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        log_event("ERROR", {"reason": str(e), "file": str(json_path)})
        print("{}")
        return

    # Import validator (lazy — only when we actually need it)
    try:
        sys.path.insert(0, str(SCRIPTS_DIR))
        from lib.adf_validator import AdfValidator, detect_format
    except ImportError as e:
        log_event("ERROR", {"reason": f"import_failed: {e}"})
        print("{}")
        return

    # Detect format and extract ADF
    fmt, adf = detect_format(adf_data)
    if not adf or not isinstance(adf, dict):
        log_event("SKIP", {"reason": "no_adf", "format": fmt, "file": str(json_path)})
        print("{}")
        return

    wrapper = adf_data if fmt in ("create", "edit") else None
    issue_type = detect_issue_type(json_path, adf_data)

    # Validate
    validator = AdfValidator()
    report = validator.validate(adf, issue_type, wrapper)

    log_data = {
        "file": json_path.name,
        "type": issue_type,
        "format": fmt,
        "score": round(report.score, 1),
        "passed": report.passed,
        "session_id": data.get("session_id", ""),
    }

    if report.passed:
        log_event("ALLOWED", log_data)
        print("{}")
    else:
        # Build failure details
        issues = [
            f"  {c.check_id}: {c.message}"
            for c in report.checks
            if c.status.value == "fail"
        ]
        issues_text = "\n".join(issues[:5])  # Top 5 failures
        reason = (
            f"HR1 BLOCKED: Quality Gate {report.score:.1f}% < 90% "
            f"(type: {issue_type}, file: {json_path.name})\n"
            f"Top issues:\n{issues_text}\n"
            f"Fix the ADF JSON and re-validate before writing to Jira."
        )
        log_event("BLOCKED", log_data)
        print(reason, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
