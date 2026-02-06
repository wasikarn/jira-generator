---
name: update-task
description: |
  Update an existing Jira Task with a 6-phase update workflow

  Phases: Fetch Current → Identify Changes → Preserve Intent → Generate Update → Quality Gate → Apply Update

  Supports: format migration, add details, change type template

  Triggers: "update task", "edit task", "adjust task"
argument-hint: "{{PROJECT_KEY}}-XXX [changes]"
---

# /update-task

**Role:** Developer / Tech Lead
**Output:** Updated Jira Task

## Context Object (accumulated across phases)

| Phase | Adds to Context |
|-------|----------------|
| 1. Fetch | `task_data`, `current_format`, `task_type` |
| 2. Identify | `change_type`, `change_scope` |
| 3. Preserve | `preservation_rules` |
| 4. Generate | `update_adf_json` |
| 5. QG | `qg_score`, `passed_qg` |
| 6. Apply | `applied` |

## Gate Levels

| Level | Symbol | Behavior |
| --- | --- | --- |
| **AUTO** | 🟢 | Validate automatically. Pass → proceed. Fail → auto-fix (max 2). Still fail → escalate to user. |
| **REVIEW** | 🟡 | Present results to user, wait for quick confirmation. Default: proceed unless user objects. |
| **APPROVAL** | ⛔ | STOP. Wait for explicit user approval before proceeding. |

## Phases

> **Phase Tracking:** Use TodoWrite to mark each phase `in_progress` → `completed` as you work.

### 1. Fetch Current State

- `MCP: jira_get_issue(issue_key: "{{PROJECT_KEY}}-XXX")`
- Read: Summary, Description, Status, Priority, Labels
- Identify current format: Wiki markup or ADF
- Identify current type (if applicable): tech-debt, bug, chore, spike

**🟡 REVIEW** — Present current state to user. Proceed unless user objects.

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

**⛔ GATE — DO NOT PROCEED** without user confirmation of changes.

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

**🟢 AUTO** — Apply preservation rules programmatically. No user interaction needed.

---

### 4. Generate Update

Generate ADF JSON → `tasks/bep-xxx-update.json`

**EDIT format (do not include projectKey, type, summary):**

```json
{
  "issues": ["{{PROJECT_KEY}}-XXX"],
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

**⛔ GATE — DO NOT APPLY** without user approval of all generated changes.

---

### 5. Quality Gate (MANDATORY)

> **🟢 AUTO** — Score → auto-fix → re-score. Escalate only if still < 90% after 2 attempts.
> HR1: DO NOT send updates to Atlassian without QG ≥ 90%.

Score against `shared-references/verification-checklist.md`:

1. Score each check with confidence (0-100%). Only report issues with confidence ≥ 80%.
2. Report: `Technical X/5 | Quality X/6 | Overall X%`
3. If < 90% → auto-fix → re-score (max 2 attempts)
4. If ≥ 90% → proceed to Phase 6 automatically
5. If still < 90% after 2 fixes → escalate to user
6. Low-confidence items (< 80%) → flag as "needs review" but don't fail QG

### 6. Apply Update

> **🟢 AUTO** — If QG passed → apply automatically. No user interaction needed.

```bash
acli jira workitem edit --from-json tasks/bep-xxx-update.json --yes
```

> **🟢 AUTO** — HR6: `cache_invalidate(issue_key)` after apply.

**Output:**

```text
## ✅ Task Updated: [Title] ({{PROJECT_KEY}}-XXX)

**Changes:**
- [list of changes applied]

🔗 [View in Jira](https://{{JIRA_SITE}}/browse/BEP-XXX)

→ Use /verify-issue {{PROJECT_KEY}}-XXX to check quality
```

---

## Common Scenarios

| Scenario | Command | Impact |
| --- | --- | --- |
| Migrate Wiki → ADF | `/update-task {{PROJECT_KEY}}-XXX "migrate"` | 🟢 Low |
| Add issues | `/update-task {{PROJECT_KEY}}-XXX "add issues"` | 🟡 Medium |
| Add ACs | `/update-task {{PROJECT_KEY}}-XXX "add ACs"` | 🟡 Medium |
| Change type | `/update-task {{PROJECT_KEY}}-XXX "change to bug"` | 🟠 High |

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
- After: `/verify-issue {{PROJECT_KEY}}-XXX` to check quality
