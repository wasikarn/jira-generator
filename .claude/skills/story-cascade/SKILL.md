---
name: story-cascade
description: |
  Update Story + cascade changes to related Sub-tasks with an 8-phase workflow

  Phases: Fetch → Understand Changes → Impact Analysis → Explore (if needed) → Generate Story Update → Generate Sub-task Updates → Apply All → Summary

  Composite: Automatic impact analysis, update everything in a single transaction

  Triggers: "story cascade", "update all", "cascade changes"
argument-hint: "[issue-key] [changes]"
---

# /story-cascade

**Role:** PO + TA Combined
**Output:** Updated Story + Updated/New Sub-tasks

## Phases

### 1. Fetch Current State

- `MCP: jira_get_issue(issue_key: "BEP-XXX")`
- `MCP: jira_search(jql: "parent = BEP-XXX", fields: "summary,status,assignee,issuetype")` (**⚠️ NEVER add ORDER BY to parent queries**)
- Build inventory: Story + all Sub-tasks
- **Gate:** User confirms scope

### 2. Understand Changes

| Change Type | Impact Level |
| --- | --- |
| Format only | 🟢 Low |
| Clarify AC | 🟢 Low |
| Add AC | 🟡 Medium |
| Modify AC | 🟡 Medium |
| Remove AC | 🔴 High |
| Change Scope | 🔴 High |

**Gate:** User confirms changes

### 3. Impact Analysis

| AC | Related Sub-tasks | Impact |
| --- | --- | --- |
| AC1 | BEP-YYY | ❌ No change |
| AC2 | BEP-YYY, BEP-ZZZ | ✏️ Must update |
| AC3 (new) | - | ➕ Need new |

**Gate:** User approves cascade plan

### 4. Codebase Exploration (if needed)

- Run only if: New sub-task needed OR scope changed
- `Task(subagent_type: "Explore")`
- Skip if format-only changes

### 5. Generate Story Update

- Apply changes: narrative, ACs, scope
- Generate ADF JSON → `tasks/bep-xxx-update.json`
- Show comparison table

### 6. Generate Sub-task Updates

- Preserve original intent
- Update ACs to align
- New sub-tasks: follow template
- Generate JSON files
- **Gate:** User approves all

### 7. Apply All Updates

```bash
# Story first
acli jira workitem edit --from-json tasks/bep-xxx-update.json --yes
# Then sub-tasks
acli jira workitem edit --from-json tasks/bep-yyy-update.json --yes
# New sub-tasks
acli jira workitem create --from-json tasks/new-subtask.json
```

### 8. Cleanup & Summary

```bash
rm tasks/bep-*-update.json tasks/new-*.json
```

```text
## Cascade Complete
Story: BEP-XXX (AC2 modified, AC3 added)
Updated: BEP-YYY, BEP-ZZZ
Created: BEP-NEW
→ Review QA sub-task if needed
```

---

## Cascade vs Separate

| Approach | Commands | Issues |
| --- | --- | --- |
| Separate | `/update-story` + N × `/update-subtask` | Lost context |
| Cascade | `/story-cascade BEP-XXX` | Auto impact |

---

## References

- [ADF Core Rules](../shared-references/templates.md) - CREATE/EDIT rules, panels, styling
- [Story Template](../shared-references/templates-story.md) - Story ADF structure
- [Sub-task Template](../shared-references/templates-subtask.md) - Sub-task + QA ADF structure
- [Tool Selection](../shared-references/tools.md) - Tool selection
