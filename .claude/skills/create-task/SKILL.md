---
name: create-task
description: |
  Create a new Jira Task with a 5-phase workflow
  Supports 4 task types: tech-debt, bug, chore, spike

  Triggers: "create task", "new task"
argument-hint: "[type] [description]"
---

# /create-task

**Role:** Developer / Tech Lead
**Output:** Jira Task with ADF format

## Task Types

| Type | Use Case | Example |
| --- | --- | --- |
| `tech-debt` | PR review issues, code improvements, refactoring | Fix issues from code review |
| `bug` | Bug fixes from QA or production | Fix bug reported by QA |
| `chore` | Maintenance, dependency updates, configs | Update dependencies |
| `spike` | Research, investigation, POC | Evaluate a new library |

---

## Phases

### 1. Discovery

Ask user to gather information:

**If type not specified:**

```text
What type of Task do you want to create?
1. tech-debt - Code improvements, PR review issues
2. bug - Bug fixes
3. chore - Maintenance tasks
4. spike - Research/Investigation
```

**Gather details by type:**

| Type | Required Info |
| --- | --- |
| `tech-debt` | Context, Issues (priority), ACs |
| `bug` | Description, Repro steps, Expected/Actual |
| `chore` | Objective, Task list |
| `spike` | Research question, Investigation areas |

**Gate:** User provides required info

---

### 2. Generate Template

Generate ADF JSON based on task type → `tasks/bep-xxx-task.json`

**tech-debt Template:**

```json
{
  "projectKey": "{{PROJECT_KEY}}",
  "type": "Task",
  "summary": "[BE/FE] [Title]",
  "description": {
    "type": "doc",
    "version": 1,
    "content": [
      // 📋 Context (panel: info)
      // 🔴 HIGH Priority (panel: error) - if any
      // 🟡 MEDIUM Priority (panel: warning) - if any
      // 🟣 LOW Priority (panel: note) - if any
      // ✅ Acceptance Criteria (table)
      // 🔗 Reference (table)
    ]
  }
}
```

**bug Template:**

```json
{
  "projectKey": "{{PROJECT_KEY}}",
  "type": "Task",
  "summary": "[Bug] [Title]",
  "description": {
    "type": "doc",
    "version": 1,
    "content": [
      // 🐛 Bug Description (panel: error)
      // 🔄 Reproduction Steps (numbered list)
      // 📊 Expected vs Actual (table)
      // 🔍 Root Cause (panel: note) - optional
      // ✅ Fix Criteria (panel: success)
      // 🔗 Reference (table)
    ]
  }
}
```

**chore Template:**

```json
{
  "projectKey": "{{PROJECT_KEY}}",
  "type": "Task",
  "summary": "[Chore] [Title]",
  "description": {
    "type": "doc",
    "version": 1,
    "content": [
      // 🎯 Objective (panel: info)
      // 📋 Tasks (checklist in panel)
      // 🔗 Reference (table)
    ]
  }
}
```

**spike Template:**

```json
{
  "projectKey": "{{PROJECT_KEY}}",
  "type": "Task",
  "summary": "[Spike] [Title]",
  "description": {
    "type": "doc",
    "version": 1,
    "content": [
      // ❓ Research Question (panel: info)
      // 📋 Context (paragraph)
      // 🔍 Investigation Areas (bullet list)
      // 📝 Findings (panel: note) - placeholder
      // 💡 Recommendations (panel: success) - placeholder
      // 🔗 Reference (table)
    ]
  }
}
```

**Gate:** JSON file created

---

### 3. Review

Show preview for user to review:

```text
## Task Preview

**Type:** [tech-debt/bug/chore/spike]
**Summary:** [summary]

**Sections:**
- [list of sections with emoji]

**Files:** tasks/bep-xxx-task.json

Any changes needed before creating?
```

**Gate:** User approves content

---

### 4. Quality Gate (MANDATORY)

Before sending to Atlassian, score against `shared-references/verification-checklist.md`:

1. Report: `Technical X/5 | Quality X/6 | Overall X%`
2. If < 90% → auto-fix issues → re-score (max 2 attempts)
3. If >= 90% → proceed to create/edit
4. If still < 90% after fix → ask user before proceeding
5. After Atlassian write → `cache_invalidate(issue_key)` if cache server available

### 5. Create

```bash
acli jira workitem create --from-json tasks/bep-xxx-task.json
```

**Capture issue key from output** for use in summary

---

### 6. Summary

```text
## ✅ Task Created: [Title] ({{PROJECT_KEY}}-XXX)

**Type:** [type]
**Priority:** [High/Medium/Low]

🔗 [View in Jira](https://{{JIRA_SITE}}/browse/BEP-XXX)

→ Use /verify-issue {{PROJECT_KEY}}-XXX to check quality
→ Use /update-task {{PROJECT_KEY}}-XXX to add details later
```

---

## Common Scenarios

| Scenario | Command | Notes |
| --- | --- | --- |
| Create task from PR review | `/create-task tech-debt "PR #1234 issues"` | Specify type directly |
| Create bug report | `/create-task bug` | Ask for details after |
| Create maintenance task | `/create-task chore "update deps"` | Simple objective |
| Create research task | `/create-task spike "evaluate X"` | Focus on question |

---

## References

- [ADF Core Rules](../shared-references/templates.md) - CREATE/EDIT rules, panels, styling
- [Templates](../shared-references/templates.md) - ADF templates (Task section)
- After: `/verify-issue {{PROJECT_KEY}}-XXX` to check quality
