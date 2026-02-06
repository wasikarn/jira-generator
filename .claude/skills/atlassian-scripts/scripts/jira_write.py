#!/usr/bin/env python3
"""Jira write wrapper with HR1/HR3/HR5/HR6 enforcement.

Unified write pipeline: validate ADF → create/update → verify → assign → report.
Ensures HARD RULES are enforced at every step.

Usage:
    # Create subtask (two-step: REST create + acli edit)
    python jira_write.py create-subtask --parent BEP-1200 --adf tasks/sub.json --assignee email

    # Update description (validate first)
    python jira_write.py update-description --issue BEP-1234 --adf tasks/fixed.json

    # Dry run (validate + report, no writes)
    python jira_write.py create-subtask --parent BEP-1200 --adf tasks/sub.json --dry-run

Exit codes:
    0 = success
    1 = validation/write failed
    2 = error (input/credentials)
"""

import argparse
import json
import logging
import subprocess
import sys
from pathlib import Path

# Add parent directory to path for lib imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib import (
    APIError,
    CredentialsError,
    IssueNotFoundError,
    JiraAPI,
    create_ssl_context,
    derive_jira_url,
    get_auth_header,
    load_credentials,
)
from lib.adf_validator import AdfValidator, detect_format

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


def create_api() -> JiraAPI:
    """Create configured Jira API client."""
    creds = load_credentials()
    jira_url = derive_jira_url(creds["CONFLUENCE_URL"])
    return JiraAPI(
        base_url=jira_url,
        auth_header=get_auth_header(creds["CONFLUENCE_USERNAME"], creds["CONFLUENCE_API_TOKEN"]),
        ssl_context=create_ssl_context(),
    )


def validate_adf(file_path: Path, issue_type: str) -> tuple[dict, dict, bool]:
    """Validate ADF file and return (wrapper, adf, passed).

    HR1: Quality Gate >= 90% before Atlassian writes.
    """
    with open(file_path) as f:
        data = json.load(f)

    fmt, adf = detect_format(data)
    wrapper = data if fmt in ("create", "edit") else None

    validator = AdfValidator()
    report = validator.validate(adf, issue_type, wrapper)

    result = report.to_dict()
    score = result["score"]
    status = "\u2705" if report.passed else "\u274c"
    print(f"  HR1 Quality Gate: {score:.1f}% {status}")

    if not report.passed:
        print(f"  Issues:")
        for issue in result["issues"]:
            print(f"    - {issue['id']}: {issue['message']}")

    return data, adf, report.passed


def run_acli(args_list: list[str]) -> tuple[int, str]:
    """Run acli command and return (exit_code, output)."""
    cmd = ["acli"] + args_list
    logger.debug("Running: %s", " ".join(cmd))
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        output = result.stdout + result.stderr
        return result.returncode, output.strip()
    except FileNotFoundError:
        return 1, "acli command not found — install Atlassian CLI"
    except subprocess.TimeoutExpired:
        return 1, "acli command timed out (30s)"


def assign_issue(issue_key: str, assignee: str) -> bool:
    """Assign issue using acli (HR3: MCP assignee broken)."""
    code, output = run_acli([
        "jira", "workitem", "assign",
        "-k", issue_key,
        "-a", assignee,
        "-y",
    ])
    if code == 0:
        print(f"  HR3 Assign: {assignee} \u2705")
        return True
    else:
        print(f"  HR3 Assign: FAILED — {output}")
        return False


def verify_parent(api: JiraAPI, issue_key: str, expected_parent: str) -> bool:
    """Verify parent link (HR5)."""
    issue = api.get_issue(issue_key, fields="parent,summary")
    parent = issue["fields"].get("parent")
    parent_key = parent.get("key") if parent else None

    if parent_key == expected_parent:
        print(f"  HR5 Parent: {parent_key} \u2705")
        return True
    else:
        print(f"  HR5 Parent: {parent_key} (expected {expected_parent}) \u274c")
        return False


def cmd_create_subtask(args: argparse.Namespace) -> int:
    """Create subtask: validate → REST create → verify parent → acli edit → assign."""
    file_path = Path(args.adf)
    if not file_path.exists():
        logger.error("File not found: %s", file_path)
        return 2

    print(f"{'=' * 60}")
    print(f"Create Subtask (parent: {args.parent})")
    print(f"{'=' * 60}")

    # Step 1: Validate ADF (HR1)
    print("\n[1/5] Validating ADF...")
    data, adf, passed = validate_adf(file_path, "subtask")
    if not passed:
        print("\n\u274c Aborted — fix ADF quality issues first")
        return 1

    if args.dry_run:
        print("\n\u2705 DRY RUN — validation passed, no writes")
        return 0

    # Step 2: REST create subtask shell (with parent)
    print("\n[2/5] Creating subtask shell (REST API)...")
    try:
        api = create_api()
    except CredentialsError as e:
        logger.error("Credentials error: %s", e)
        return 2

    summary = data.get("summary", "")
    if not summary:
        # Extract from ADF or use placeholder
        summary = f"Subtask of {args.parent}"

    create_data = {
        "fields": {
            "project": {"key": "BEP"},
            "issuetype": {"name": "Subtask"},
            "summary": summary,
            "parent": {"key": args.parent},
        }
    }

    try:
        result = api._request("POST", "/rest/api/3/issue", create_data)
        new_key = result.get("key", "")
        print(f"  Created: {new_key} \u2705")
    except APIError as e:
        print(f"  Create FAILED: {e.status_code} {e.reason}")
        return 1

    # Step 3: Verify parent link (HR5)
    print(f"\n[3/5] Verifying parent link (HR5)...")
    if not verify_parent(api, new_key, args.parent):
        print(f"  \u26a0\ufe0f Parent link verification failed — may need manual fix")

    # Step 4: Update description via acli (ADF)
    print(f"\n[4/5] Updating description (acli)...")
    # Create EDIT format JSON
    edit_data = {"issues": [new_key], "description": adf}
    edit_path = file_path.with_stem(file_path.stem + "-edit-tmp")
    with open(edit_path, "w") as f:
        json.dump(edit_data, f, ensure_ascii=False)

    code, output = run_acli([
        "jira", "workitem", "edit",
        "--from-json", str(edit_path),
        "--yes",
    ])
    edit_path.unlink(missing_ok=True)  # cleanup

    if code == 0:
        print(f"  Description updated \u2705")
    else:
        print(f"  Description update FAILED: {output}")

    # Step 5: Assign (HR3)
    if args.assignee:
        print(f"\n[5/5] Assigning (HR3)...")
        assign_issue(new_key, args.assignee)
    else:
        print(f"\n[5/5] No assignee specified — skipping")

    # HR6: Report cache invalidation needed
    print(f"\n{'=' * 60}")
    print(f"\u2705 Created: {new_key}")
    print(f"HR6 Action: cache_invalidate('{new_key}')")
    print(f"{'=' * 60}")

    return 0


def cmd_update_description(args: argparse.Namespace) -> int:
    """Update description: validate → acli edit."""
    file_path = Path(args.adf)
    if not file_path.exists():
        logger.error("File not found: %s", file_path)
        return 2

    print(f"{'=' * 60}")
    print(f"Update Description: {args.issue}")
    print(f"{'=' * 60}")

    # Step 1: Validate ADF (HR1)
    print("\n[1/3] Validating ADF...")
    issue_type = args.type or "subtask"
    data, adf, passed = validate_adf(file_path, issue_type)
    if not passed:
        print("\n\u274c Aborted — fix ADF quality issues first")
        return 1

    if args.dry_run:
        print("\n\u2705 DRY RUN — validation passed, no writes")
        return 0

    # Step 2: Update via acli
    print(f"\n[2/3] Updating description (acli)...")
    edit_data = {"issues": [args.issue], "description": adf}
    edit_path = file_path.with_stem(file_path.stem + "-edit-tmp")
    with open(edit_path, "w") as f:
        json.dump(edit_data, f, ensure_ascii=False)

    code, output = run_acli([
        "jira", "workitem", "edit",
        "--from-json", str(edit_path),
        "--yes",
    ])
    edit_path.unlink(missing_ok=True)

    if code == 0:
        print(f"  Description updated \u2705")
    else:
        print(f"  Description update FAILED: {output}")
        return 1

    # Step 3: Report
    print(f"\n[3/3] Done")
    print(f"\n{'=' * 60}")
    print(f"\u2705 Updated: {args.issue}")
    print(f"HR6 Action: cache_invalidate('{args.issue}')")
    print(f"{'=' * 60}")

    return 0


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Jira write wrapper with HARD RULES enforcement",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # create-subtask
    sub = subparsers.add_parser("create-subtask", help="Create subtask with parent")
    sub.add_argument("--parent", required=True, help="Parent story key (e.g., BEP-1200)")
    sub.add_argument("--adf", required=True, help="Path to ADF JSON file")
    sub.add_argument("--assignee", help="Assignee email (uses acli for HR3)")
    sub.add_argument("--dry-run", action="store_true", help="Validate only, no writes")
    sub.add_argument("--verbose", "-v", action="store_true")

    # update-description
    upd = subparsers.add_parser("update-description", help="Update issue description")
    upd.add_argument("--issue", required=True, help="Issue key (e.g., BEP-1234)")
    upd.add_argument("--adf", required=True, help="Path to ADF JSON file")
    upd.add_argument("--type", "-t", choices=["story", "subtask", "epic", "qa"],
                      help="Issue type for validation (default: subtask)")
    upd.add_argument("--dry-run", action="store_true", help="Validate only, no writes")
    upd.add_argument("--verbose", "-v", action="store_true")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 2

    if hasattr(args, "verbose") and args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.command == "create-subtask":
        return cmd_create_subtask(args)
    elif args.command == "update-description":
        return cmd_update_description(args)

    return 2


if __name__ == "__main__":
    sys.exit(main())
