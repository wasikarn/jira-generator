---
name: update-task
description: |
  แก้ไข Jira Task ที่มีอยู่ด้วย 5-phase update workflow

  Phases: Fetch Current → Identify Changes → Preserve Intent → Generate Update → Apply Update

  รองรับ: format migration, add details, change type template

  Triggers: "update task", "แก้ไข task", "ปรับ task"
argument-hint: "BEP-XXX [changes]"
---

# /update-task

**Role:** Developer / Tech Lead
**Output:** Updated Jira Task

## Phases

### 1. Fetch Current State

- `MCP: jira_get_issue(issue_key: "BEP-XXX")`
- อ่าน: Summary, Description, Status, Priority, Labels
- ระบุ current format: Wiki markup หรือ ADF
- ระบุ current type (ถ้ามี): tech-debt, bug, chore, spike

**Gate:** User confirms what to update

---

### 2. Identify Changes

ถาม user ว่าต้องการ update อะไร:

| Change Type | Description |
| --- | --- |
| `migrate` | แปลง Wiki → ADF format |
| `add-details` | เพิ่มรายละเอียด (issues, ACs, etc.) |
| `change-type` | เปลี่ยน template type |
| `update-content` | แก้ไข content ที่มีอยู่ |

**Common scenarios:**

```text
1. Migrate format (Wiki → ADF)
2. เพิ่ม issues/ACs
3. เปลี่ยน priority
4. เพิ่ม reference links
5. อื่นๆ (ระบุ)
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

- ✅ เพิ่ม content ได้
- ✅ ปรับ format/wording ได้
- ⚠️ ระวังเปลี่ยน scope
- ❌ ห้ามลบ content โดยไม่บอก

**Gate:** User acknowledges what will change

---

### 4. Generate Update

สร้าง ADF JSON → `tasks/bep-xxx-update.json`

**EDIT format (ห้ามใส่ projectKey, type, summary):**

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

ต้องการ apply changes หรือไม่?
```

**Gate:** User approves changes

---

### 5. Apply Update

```bash
acli jira workitem edit --from-json tasks/bep-xxx-update.json --yes
```

**Output:**

```text
## ✅ Task Updated: [Title] (BEP-XXX)

**Changes:**
- [list of changes applied]

🔗 [View in Jira](https://100-stars.atlassian.net/browse/BEP-XXX)

→ ใช้ /verify-issue BEP-XXX ตรวจสอบคุณภาพ
```

---

## Common Scenarios

| Scenario | Command | Impact |
| --- | --- | --- |
| Migrate Wiki → ADF | `/update-task BEP-XXX "migrate"` | 🟢 Low |
| เพิ่ม issues | `/update-task BEP-XXX "add issues"` | 🟡 Medium |
| เพิ่ม ACs | `/update-task BEP-XXX "add ACs"` | 🟡 Medium |
| เปลี่ยน type | `/update-task BEP-XXX "change to bug"` | 🟠 High |

---

## Task Type Detection

**Auto-detect จาก content:**

| Pattern | Detected Type |
| --- | --- |
| Priority sections (HIGH/MEDIUM/LOW) | `tech-debt` |
| Repro steps, Expected/Actual | `bug` |
| Task checklist, simple objective | `chore` |
| Research question, Investigation | `spike` |
| No clear pattern | `generic` |

**Type มี impact กับ template structure ที่ใช้**

---

## References

- [ADF Core Rules](../shared-references/templates.md) - CREATE/EDIT rules, panels, styling
- [Task Template](../shared-references/templates-task.md) - Task ADF (tech-debt, bug, chore, spike)
- After: `/verify-issue BEP-XXX` ตรวจสอบคุณภาพ
