---
name: update-story
description: |
  Update an existing User Story with a 6-phase update workflow

  Phases: Fetch Current → Impact Analysis → Preserve Intent → Generate Update → Quality Gate → Apply Update

  Supports: add AC, modify AC, adjust scope, format migration

  Triggers: "update story", "edit story", "add AC"
argument-hint: "[issue-key] [changes]"
---

# /update-story

**Role:** Senior Product Owner
**Output:** Updated User Story

## Phases

### 1. Fetch Current State

- `MCP: jira_get_issue(issue_key: "BEP-XXX")`
- `MCP: jira_search(jql: "parent = BEP-XXX", fields: "summary,status,assignee,issuetype")` → Sub-tasks (**⚠️ NEVER add ORDER BY to parent queries**)
- Read: Narrative, ACs, Scope, Status
- **Gate:** User confirms what to update

### 2. Impact Analysis

| Change Type | Impact on Sub-tasks | Impact on QA |
| --- | --- | --- |
| Add AC | Need to create sub-task? | Need to add test? |
| Remove AC | Need to delete sub-task? | Need to delete test? |
| Modify AC | Need to update sub-task? | Need to update test? |
| Format only | ❌ No impact | ❌ No impact |

**Gate:** User acknowledges impact

### 3. Preserve Intent

- ✅ Adding ACs is allowed
- ✅ Adjusting wording is allowed
- ⚠️ Be careful changing scope (requires re-analysis)
- ❌ Do not change core value proposition without informing

### 4. Generate Update

- Generate ADF JSON → `tasks/bep-xxx-update.json`
- Show comparison:
  - Narrative: [No change / Changed]
  - ACs: ✅ Kept / ✏️ Modified / ➕ New
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

**Output:**

```text
## Story Updated: [Title] (BEP-XXX)
Changes: [list]
→ May need: /update-subtask BEP-YYY
→ May need: /story-cascade BEP-XXX (for auto cascade)
```

---

## Common Scenarios

| Scenario | Command | Impact |
| --- | --- | --- |
| Add AC | `/update-story BEP-XXX "add mobile AC"` | 🟡 Medium |
| Format migrate | `/update-story BEP-XXX "migrate ADF"` | 🟢 Low |
| Clarify AC | `/update-story BEP-XXX "AC2 is unclear"` | 🟢 Low |
| Reduce scope | `/update-story BEP-XXX "reduce scope"` | 🔴 High |

---

## References

- [ADF Core Rules](../shared-references/templates.md) - CREATE/EDIT rules, panels, styling
- [Templates](../shared-references/templates.md) - ADF templates (Story section)
- [Verification Checklist](../shared-references/verification-checklist.md) - INVEST, AC quality
