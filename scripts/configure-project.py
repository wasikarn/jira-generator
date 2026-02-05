#!/usr/bin/env python3
"""
Configure project files from project-config.json

Replaces hardcoded values (project key, Jira site, custom fields) in skill files
with values from .claude/project-config.json

Usage:
    python scripts/configure-project.py           # Dry run (show changes)
    python scripts/configure-project.py --apply   # Apply changes
    python scripts/configure-project.py --revert  # Revert to placeholders
"""

import json
import re
import sys
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
CONFIG_PATH = PROJECT_DIR / ".claude" / "project-config.json"
SKILLS_DIR = PROJECT_DIR / ".claude" / "skills"

# Placeholder format: {{KEY}}
PLACEHOLDERS = {
    "PROJECT_KEY": "BEP",
    "JIRA_SITE": "100-stars.atlassian.net",
    "CONFLUENCE_SITE": "100-stars.atlassian.net",
    "SPACE_KEY": "BEP",
    "START_DATE_FIELD": "customfield_10015",
    "SPRINT_FIELD": "customfield_10020",
}


def load_config() -> dict:
    """Load project-config.json and extract values."""
    if not CONFIG_PATH.exists():
        print(f"Error: {CONFIG_PATH} not found")
        sys.exit(1)

    with open(CONFIG_PATH) as f:
        config = json.load(f)

    return {
        "PROJECT_KEY": config["jira"]["project_key"],
        "JIRA_SITE": config["jira"]["site"],
        "CONFLUENCE_SITE": config["confluence"]["site"],
        "SPACE_KEY": config["confluence"]["space_key"],
        "START_DATE_FIELD": config["jira"]["custom_fields"]["start_date"],
        "SPRINT_FIELD": config["jira"]["custom_fields"]["sprint"],
    }


def get_replacement_patterns(values: dict, revert: bool = False) -> list[tuple[str, str]]:
    """Generate regex patterns for replacement."""
    patterns = []

    for key, placeholder_default in PLACEHOLDERS.items():
        actual_value = values.get(key, placeholder_default)
        placeholder = f"{{{{{key}}}}}"  # {{KEY}}

        if revert:
            # Replace actual values with placeholders
            # Project key in various contexts
            if key == "PROJECT_KEY":
                patterns.extend([
                    (rf'"projectKey":\s*"{re.escape(actual_value)}"', f'"projectKey": "{placeholder}"'),
                    (rf'project_key:\s*"{re.escape(actual_value)}"', f'project_key: "{placeholder}"'),
                    (rf'project_key="{re.escape(actual_value)}"', f'project_key="{placeholder}"'),
                    (rf'space_key:\s*"{re.escape(actual_value)}"', f'space_key: "{placeholder}"'),
                    (rf'space_key="{re.escape(actual_value)}"', f'space_key="{placeholder}"'),
                    # Issue key pattern BEP-XXX (but not in URLs or smart links)
                    (rf'(?<!/browse/){re.escape(actual_value)}-XXX', f'{placeholder}-XXX'),
                ])
            elif key == "JIRA_SITE":
                patterns.append(
                    (rf'https://{re.escape(actual_value)}', f'https://{placeholder}')
                )
            elif key in ("START_DATE_FIELD", "SPRINT_FIELD"):
                patterns.append(
                    (rf'{re.escape(actual_value)}', placeholder)
                )
        else:
            # Replace placeholders with actual values
            if key == "PROJECT_KEY":
                patterns.extend([
                    (rf'"projectKey":\s*"\{{\{{PROJECT_KEY\}}\}}"', f'"projectKey": "{actual_value}"'),
                    (rf'project_key:\s*"\{{\{{PROJECT_KEY\}}\}}"', f'project_key: "{actual_value}"'),
                    (rf'project_key="\{{\{{PROJECT_KEY\}}\}}"', f'project_key="{actual_value}"'),
                    (rf'space_key:\s*"\{{\{{SPACE_KEY\}}\}}"', f'space_key: "{actual_value}"'),
                    (rf'space_key="\{{\{{SPACE_KEY\}}\}}"', f'space_key="{actual_value}"'),
                    (rf'\{{\{{PROJECT_KEY\}}\}}-XXX', f'{actual_value}-XXX'),
                ])
            elif key == "JIRA_SITE":
                patterns.append(
                    (rf'https://\{{\{{JIRA_SITE\}}\}}', f'https://{actual_value}')
                )
            elif key in ("START_DATE_FIELD", "SPRINT_FIELD"):
                patterns.append(
                    (rf'\{{\{{{key}\}}\}}', actual_value)
                )

    return patterns


def process_file(filepath: Path, patterns: list[tuple[str, str]], dry_run: bool = True) -> list[str]:
    """Process a single file and return list of changes made."""
    changes = []

    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        return [f"  Error reading: {e}"]

    new_content = content
    for pattern, replacement in patterns:
        matches = re.findall(pattern, new_content)
        if matches:
            new_content = re.sub(pattern, replacement, new_content)
            changes.append(f"  {pattern[:50]}... → {replacement[:50]}... ({len(matches)} matches)")

    if changes and not dry_run:
        filepath.write_text(new_content, encoding='utf-8')

    return changes


def main():
    # Parse args
    apply_changes = "--apply" in sys.argv
    revert_mode = "--revert" in sys.argv

    if revert_mode and apply_changes:
        print("Error: Cannot use --apply and --revert together")
        sys.exit(1)

    # Load config
    config_values = load_config()

    print("=" * 60)
    if revert_mode:
        print("REVERT MODE: Converting actual values → placeholders")
    else:
        print("CONFIGURE MODE: Converting placeholders → actual values")
    print("=" * 60)
    print(f"\nConfig: {CONFIG_PATH}")
    print(f"Values:")
    for k, v in config_values.items():
        print(f"  {k}: {v}")
    print()

    # Get patterns
    patterns = get_replacement_patterns(config_values, revert=revert_mode)

    # Find all markdown files in skills directory
    md_files = list(SKILLS_DIR.rglob("*.md"))

    # Also include root CLAUDE.md
    root_claude = PROJECT_DIR / "CLAUDE.md"
    if root_claude.exists():
        md_files.append(root_claude)

    print(f"Scanning {len(md_files)} files...\n")

    total_changes = 0
    files_changed = 0

    for filepath in sorted(md_files):
        rel_path = filepath.relative_to(PROJECT_DIR)
        changes = process_file(filepath, patterns, dry_run=not apply_changes)

        if changes:
            files_changed += 1
            total_changes += len(changes)
            print(f"📄 {rel_path}")
            for change in changes:
                print(change)
            print()

    # Summary
    print("=" * 60)
    if apply_changes:
        print(f"✅ Applied {total_changes} changes in {files_changed} files")
    else:
        print(f"🔍 Found {total_changes} potential changes in {files_changed} files")
        print("\nRun with --apply to make changes:")
        print(f"  python {Path(__file__).name} --apply")
        if not revert_mode:
            print(f"\nOr revert to placeholders:")
            print(f"  python {Path(__file__).name} --revert --apply")


if __name__ == "__main__":
    main()
