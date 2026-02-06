---
name: update-task
description: |
  Update an existing Jira Task with a 6-phase update workflow

  Phases: Fetch Current → Identify Changes → Preserve Intent → Generate Update → Quality Gate → Apply Update

  Supports: format migration, add details, change type template

  Triggers: "update task", "edit task", "adjust task"
argument-hint: "BEP-XXX [changes]"
---

# /update-task

**Role:** Developer / Tech Lead
**Output:** Updated Jira Task

## Phases

### 1. Fetch Current State

- `MCP: jira_get_issue(issue_key: "BEP-XXX")`
- Read: Summary, Description, Status, Priority, Labels
- Identify current format: Wiki markup or ADF
- Identify current type (if applicable): tech-debt, bug, chore, spike

**Gate:** User confirms what to update

---

### 2. Identify Changes

Ask the user what they want to update:

| Change Type | Description |
| --- | --- |
| `migrate` | Convert Wiki → ADF format |
| `add-details` | Add more details (issues, ACs, etc.) |
| `change-type` | Change template type |
| `update-content` | Edit existing content |

**Common scenarios:**

```text
1. Migrate format (Wiki → ADF)
2. Add issues/ACs
3. Change priority
4. Add reference links
5. Other (specify)
```

**Gate:** User specifies changes

---

### 3. Preserve Intent

| Change Type | Preserve | Allow Change |
| --- | --- | --- |
| Format migrate | ✅ All content | Format only |
| Add details | ✅ Existing content | ➕ New sections |
| Change type | ⚠️ Core info | Template structure |
| Update content | ✅ Other sections | Specified sections |

**Rules:**

- ✅ Adding content is allowed
- ✅ Adjusting format/wording is allowed
- ⚠️ Be careful changing scope
- ❌ Do not delete content without informing

**Gate:** User acknowledges what will change

---

### 4. Generate Update

Generate ADF JSON → `tasks/bep-xxx-update.json`

**EDIT format (do not include projectKey, type, summary):**

```json
{
  "issues": ["BEP-XXX"],
  "description": {
    "type": "doc",
    "version": 1,
    "content": [...]
  }
}
```

**Show comparison:**

```text
## Changes Preview

| Section | Before | After |
|---------|--------|-------|
| Format | Wiki | ADF |
| Context | ✅ Kept | ✅ Kept |
| Issues | 3 items | 5 items (➕2) |
| ACs | ❌ None | ➕ 5 items |

Would you like to apply these changes?
```

**Gate:** User approves changes

---

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
## ✅ Task Updated: [Title] (BEP-XXX)

**Changes:**
- [list of changes applied]

🔗 [View in Jira](https://100-stars.atlassian.net/browse/BEP-XXX)

→ Use /verify-issue BEP-XXX to check quality
```

---

## Common Scenarios

| Scenario | Command | Impact |
| --- | --- | --- |
| Migrate Wiki → ADF | `/update-task BEP-XXX "migrate"` | 🟢 Low |
| Add issues | `/update-task BEP-XXX "add issues"` | 🟡 Medium |
| Add ACs | `/update-task BEP-XXX "add ACs"` | 🟡 Medium |
| Change type | `/update-task BEP-XXX "change to bug"` | 🟠 High |

---

## Task Type Detection

**Auto-detect from content:**

| Pattern | Detected Type |
| --- | --- |
| Priority sections (HIGH/MEDIUM/LOW) | `tech-debt` |
| Repro steps, Expected/Actual | `bug` |
| Task checklist, simple objective | `chore` |
| Research question, Investigation | `spike` |
| No clear pattern | `generic` |

**Type impacts which template structure is used**

---

## References

- [ADF Core Rules](../shared-references/templates.md) - CREATE/EDIT rules, panels, styling
- [Templates](../shared-references/templates.md) - ADF templates (Task section)
- After: `/verify-issue BEP-XXX` to check quality
