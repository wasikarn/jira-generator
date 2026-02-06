#!/usr/bin/env python3
"""Fix markdown table formatting for MD060 compliance.

Ensures consistent "leading_and_trailing" style:
  | cell | cell | cell |
  | --- | --- | --- |

Skips tables inside fenced code blocks.
"""

import re
import sys
from pathlib import Path


def fix_table_line(line: str) -> str:
    """Normalize pipe spacing in a single table line."""
    stripped = line.rstrip("\n")
    if not stripped.strip().startswith("|"):
        return line

    # Split by pipe, but respect escaped pipes and inline code
    # Simple approach: split on unescaped pipes
    raw = stripped.strip()

    # Remove leading and trailing pipes
    if raw.startswith("|"):
        raw = raw[1:]
    if raw.endswith("|"):
        raw = raw[:-1]

    cells = raw.split("|")

    fixed_cells = []
    for cell in cells:
        content = cell.strip()
        if content:
            fixed_cells.append(f" {content} ")
        else:
            fixed_cells.append("  ")

    return "|" + "|".join(fixed_cells) + "|"


def fix_file(filepath: str) -> int:
    """Fix all tables in a markdown file. Returns number of lines changed."""
    text = Path(filepath).read_text(encoding="utf-8")
    lines = text.split("\n")

    in_code_block = False
    changes = 0
    result = []

    for line in lines:
        # Track fenced code blocks
        if re.match(r"^\s*```", line):
            in_code_block = not in_code_block
            result.append(line)
            continue

        # Only fix table lines outside code blocks
        if not in_code_block and "|" in line and line.strip().startswith("|"):
            fixed = fix_table_line(line)
            if fixed != line:
                changes += 1
            result.append(fixed)
        else:
            result.append(line)

    if changes > 0:
        Path(filepath).write_text("\n".join(result), encoding="utf-8")

    return changes


def main():
    if len(sys.argv) < 2:
        print("Usage: python fix-table-format.py <file1.md> [file2.md ...]")
        sys.exit(1)

    total_changes = 0
    for filepath in sys.argv[1:]:
        changes = fix_file(filepath)
        if changes > 0:
            print(f"  Fixed {changes} lines: {filepath}")
            total_changes += changes

    print(f"\nTotal: {total_changes} lines fixed")


if __name__ == "__main__":
    main()
