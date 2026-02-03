---
name: update-subtask
description: |
  Update an existing Sub-task with a 5-phase update workflow

  Phases: Fetch Current → Identify Changes → Preserve Intent → Generate Update → Apply Update

  Supports: format migration, add details, language fix, add AC

  Triggers: "update subtask", "edit subtask", "adjust subtask"
argument-hint: "[issue-key] [changes]"
---

# /update-subtask

**Role:** Senior Technical Analyst
**Output:** Updated Sub-task

## Phases

### 1. Fetch Current State

- `MCP: jira_get_issue(issue_key: "BEP-XXX")`
- Fetch parent story for context
- Read: Description, Summary, Status
- **Gate:** User confirms what to update

### 2. Identify Changes

| Type | Description | Example |
| --- | --- | --- |
| **Format** | Adjust format | wiki → ADF |
| **Content** | Add/edit content | add AC |
| **Language** | Fix language | EN → Thai + transliteration |
| **Codebase** | Update paths | generic → actual |

**Gate:** User approves change scope

### 3. Preserve Intent

- ✅ Adjusting format is allowed
- ✅ Adding details is allowed
- ✅ Translating language is allowed
- ❌ Do not change the objective
- ❌ Do not remove existing ACs

### 4. Generate Update

- If file paths need updating → `Task(Explore)`
- Generate ADF JSON → `tasks/bep-xxx-update.json`
- Show Before/After comparison
- **Gate:** User approves changes

### 5. Apply Update

```bash
acli jira workitem edit --from-json tasks/bep-xxx-update.json --yes
```

---

## Common Scenarios

| Scenario | Command |
| --- | --- |
| Format migrate | `/update-subtask BEP-XXX "migrate ADF"` |
| Add file paths | `/update-subtask BEP-XXX "add file paths"` |
| Fix language | `/update-subtask BEP-XXX "fix to Thai"` |
| Add AC | `/update-subtask BEP-XXX "add AC error handling"` |

---

## References

- [ADF Core Rules](../shared-references/templates.md) - CREATE/EDIT rules, panels, styling
- [Sub-task Template](../shared-references/templates-subtask.md) - Sub-task + QA ADF structure
- [Tool Selection](../shared-references/tools.md) - Tool selection
