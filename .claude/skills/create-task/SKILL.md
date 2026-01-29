---
name: create-task
description: |
  สร้าง Jira Task ใหม่ด้วย 5-phase workflow
  รองรับ 4 task types: tech-debt, bug, chore, spike

  Triggers: "create task", "สร้าง task", "new task"
argument-hint: "[type] [description]"
---

# /create-task

**Role:** Developer / Tech Lead
**Output:** Jira Task with ADF format

## Task Types

| Type | Use Case | Example |
| --- | --- | --- |
| `tech-debt` | PR review issues, code improvements, refactoring | แก้ไข issues จาก code review |
| `bug` | Bug fixes จาก QA หรือ production | แก้ไข bug ที่ QA report |
| `chore` | Maintenance, dependency updates, configs | Update dependencies |
| `spike` | Research, investigation, POC | ศึกษา library ใหม่ |

---

## Phases

### 1. Discovery

ถาม user เพื่อ gather ข้อมูล:

**ถ้าไม่ระบุ type:**

```text
ต้องการสร้าง Task ประเภทไหน?
1. tech-debt - Code improvements, PR review issues
2. bug - Bug fixes
3. chore - Maintenance tasks
4. spike - Research/Investigation
```

**Gather details ตาม type:**

| Type | Required Info |
| --- | --- |
| `tech-debt` | Context, Issues (priority), ACs |
| `bug` | Description, Repro steps, Expected/Actual |
| `chore` | Objective, Task list |
| `spike` | Research question, Investigation areas |

**Gate:** User provides required info

---

### 2. Generate Template

สร้าง ADF JSON ตาม task type → `tasks/bep-xxx-task.json`

**tech-debt Template:**

```json
{
  "projectKey": "BEP",
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
  "projectKey": "BEP",
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
  "projectKey": "BEP",
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
  "projectKey": "BEP",
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

แสดง preview ให้ user ตรวจสอบ:

```text
## Task Preview

**Type:** [tech-debt/bug/chore/spike]
**Summary:** [summary]

**Sections:**
- [list of sections with emoji]

**Files:** tasks/bep-xxx-task.json

ต้องการปรับแก้อะไรก่อน create หรือไม่?
```

**Gate:** User approves content

---

### 4. Create

```bash
acli jira workitem create --from-json tasks/bep-xxx-task.json
```

**จับ issue key จาก output** เพื่อใช้ใน summary

---

### 5. Summary

```text
## ✅ Task Created: [Title] (BEP-XXX)

**Type:** [type]
**Priority:** [High/Medium/Low]

🔗 [View in Jira](https://100-stars.atlassian.net/browse/BEP-XXX)

→ ใช้ /verify-issue BEP-XXX ตรวจสอบคุณภาพ
→ ใช้ /update-task BEP-XXX เพิ่มรายละเอียดภายหลัง
```

---

## Common Scenarios

| Scenario | Command | Notes |
| --- | --- | --- |
| สร้าง task จาก PR review | `/create-task tech-debt "PR #1234 issues"` | ระบุ type ตรง |
| สร้าง bug report | `/create-task bug` | ถามรายละเอียดทีหลัง |
| สร้าง maintenance task | `/create-task chore "update deps"` | Simple objective |
| สร้าง research task | `/create-task spike "evaluate X"` | Focus on question |

---

## References

- [ADF Core Rules](../shared-references/templates.md) - CREATE/EDIT rules, panels, styling
- [Task Template](../shared-references/templates-task.md) - Task ADF (tech-debt, bug, chore, spike)
- After: `/verify-issue BEP-XXX` ตรวจสอบคุณภาพ
