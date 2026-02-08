---
name: assign
description: |
  Quick assign a Jira issue to a team member using acli (bypasses MCP silent failure)

  Triggers: "assign", "assign issue", "assign to"
argument-hint: "{{PROJECT_KEY}}-XXX [name]"
---

# /assign

**Shortcut:** Assigns issue using `acli` (HR3-safe — never MCP).

## Usage

```text
/assign {{PROJECT_KEY}}-XXX Kobi        → assign to Kobi
/assign {{PROJECT_KEY}}-XXX Natthakarn  → assign to Natthakarn
/assign {{PROJECT_KEY}}-XXX unassign    → remove assignee
```

## Team Lookup

Read team from `project-config.json` → `team.members[]`. Match by first name (case-insensitive).

## Steps

1. Parse issue key + name from argument
2. Lookup email from `project-config.json` → `team.members[].email` (match by `name` field, case-insensitive first name)
3. Run: `acli jira workitem assign -k "KEY" -a "email" -y`
4. If "unassign" → Run: `acli jira workitem assign -k "KEY" -a "" -y`
5. Confirm: `Assigned {{PROJECT_KEY}}-XXX to [name] ([email])`

## Special Cases

| Name | Note |
|------|------|
| Natthakarn | Display name: `"Natthakarn Naowasook"` — use email from config |

> HR3: NEVER use MCP `jira_update_issue` with assignee — silently fails.
> HR6: `cache_invalidate(issue_key)` after assign.
