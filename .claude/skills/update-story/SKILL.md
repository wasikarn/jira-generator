---
name: update-story
description: |
  Update an existing User Story with a 5-phase update workflow

  Phases: Fetch Current → Impact Analysis → Preserve Intent → Generate Update → Apply Update

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
- `MCP: jira_search(jql: "parent = BEP-XXX")` → Sub-tasks (**⚠️ NEVER add ORDER BY to parent queries — causes JQL parse error**)
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

### 5. Apply Update

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
- [Story Template](../shared-references/templates-story.md) - Story ADF structure
- [Verification Checklist](../shared-references/verification-checklist.md) - INVEST, AC quality
