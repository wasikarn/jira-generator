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

## Context Object (accumulated across phases)

| Phase | Adds to Context |
|-------|----------------|
| 1. Fetch | `story_data`, `subtask_inventory[]` |
| 2. Impact | `change_type`, `impact_on_subtasks` |
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
- `MCP: jira_search(jql: "parent = {{PROJECT_KEY}}-XXX", fields: "summary,status,assignee,issuetype")` → Sub-tasks (**⚠️ NEVER add ORDER BY to parent queries**)
- Read: Narrative, ACs, Scope, Status
- **🟡 REVIEW** — Present current state to user. Proceed unless user objects.

### 2. Impact Analysis

| Change Type | Impact on Sub-tasks | Impact on QA |
| --- | --- | --- |
| Add AC | Need to create sub-task? | Need to add test? |
| Remove AC | Need to delete sub-task? | Need to delete test? |
| Modify AC | Need to update sub-task? | Need to update test? |
| Format only | ❌ No impact | ❌ No impact |

**⛔ GATE — DO NOT PROCEED** without user confirmation of changes.

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
- **⛔ GATE — DO NOT APPLY** without user approval of all generated changes.

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
## Story Updated: [Title] ({{PROJECT_KEY}}-XXX)
Changes: [list]
→ May need: /update-subtask BEP-YYY
→ May need: /story-cascade {{PROJECT_KEY}}-XXX (for auto cascade)
```

---

## Common Scenarios

| Scenario | Command | Impact |
| --- | --- | --- |
| Add AC | `/update-story {{PROJECT_KEY}}-XXX "add mobile AC"` | 🟡 Medium |
| Format migrate | `/update-story {{PROJECT_KEY}}-XXX "migrate ADF"` | 🟢 Low |
| Clarify AC | `/update-story {{PROJECT_KEY}}-XXX "AC2 is unclear"` | 🟢 Low |
| Reduce scope | `/update-story {{PROJECT_KEY}}-XXX "reduce scope"` | 🔴 High |

---

## References

- [ADF Core Rules](../shared-references/templates.md) - CREATE/EDIT rules, panels, styling
- [Templates](../shared-references/templates.md) - ADF templates (Story section)
- [Verification Checklist](../shared-references/verification-checklist.md) - INVEST, AC quality
