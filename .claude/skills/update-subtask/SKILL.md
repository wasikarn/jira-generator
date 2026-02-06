---
name: update-subtask
description: |
  Update an existing Sub-task with a 6-phase update workflow

  Phases: Fetch Current → Identify Changes → Preserve Intent → Generate Update → Quality Gate → Apply Update

  Supports: format migration, add details, language fix, add AC

  Triggers: "update subtask", "edit subtask", "adjust subtask"
argument-hint: "[issue-key] [changes]"
---

# /update-subtask

**Role:** Senior Technical Analyst
**Output:** Updated Sub-task

## Phases

### 1. Fetch Current State

- `MCP: jira_get_issue(issue_key: "{{PROJECT_KEY}}-XXX")`
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

### 5. Quality Gate (MANDATORY)

Before sending to Atlassian, score against `shared-references/verification-checklist.md`:

1. Report: `Technical X/5 | Quality X/6 | Overall X%`
2. If < 90% → auto-fix issues → re-score (max 2 attempts)
3. If >= 90% → proceed to create/edit
4. If still < 90% after fix → ask user before proceeding
5. After Atlassian write → `cache_invalidate(issue_key)` if cache server available

### 6. Apply Update

```bash
acli jira workitem edit --from-json tasks/bep-xxx-update.json --yes
```

---

## Common Scenarios

| Scenario | Command |
| --- | --- |
| Format migrate | `/update-subtask {{PROJECT_KEY}}-XXX "migrate ADF"` |
| Add file paths | `/update-subtask {{PROJECT_KEY}}-XXX "add file paths"` |
| Fix language | `/update-subtask {{PROJECT_KEY}}-XXX "fix to Thai"` |
| Add AC | `/update-subtask {{PROJECT_KEY}}-XXX "add AC error handling"` |

---

## References

- [ADF Core Rules](../shared-references/templates.md) - CREATE/EDIT rules, panels, styling
- [Templates](../shared-references/templates.md) - ADF templates (Sub-task section)
- [Tool Selection](../shared-references/tools.md) - Tool selection
