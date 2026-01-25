---
name: update-subtask
description: |
  แก้ไข Sub-task ที่มีอยู่ ด้วย 5-phase update workflow

  Phases: Fetch Current → Identify Changes → Preserve Intent → Generate Update → Apply Update

  รองรับ: format migration, add details, language fix, add AC

  Triggers: "update subtask", "แก้ไข subtask", "ปรับ subtask"
argument-hint: "[issue-key] [changes]"
---

# /update-subtask

**Role:** Senior Technical Analyst
**Output:** Updated Sub-task

## Phases

### 1. Fetch Current State

- `MCP: jira_get_issue(issue_key: "BEP-XXX")`
- Fetch parent story for context
- อ่าน: Description, Summary, Status
- **Gate:** User confirms what to update

### 2. Identify Changes

| Type | Description | Example |
| --- | --- | --- |
| **Format** | ปรับ format | wiki → ADF |
| **Content** | เพิ่ม/แก้ไข | เพิ่ม AC |
| **Language** | ปรับภาษา | EN → Thai + ทับศัพท์ |
| **Codebase** | Update paths | generic → actual |

**Gate:** User approves change scope

### 3. Preserve Intent

- ✅ ปรับ format ได้
- ✅ เพิ่ม details ได้
- ✅ แปลภาษาได้
- ❌ ห้ามเปลี่ยน objective
- ❌ ห้ามลบ AC ที่มีอยู่

### 4. Generate Update

- ถ้าต้อง update file paths → `Task(Explore)`
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
| Add file paths | `/update-subtask BEP-XXX "เพิ่ม file paths"` |
| Fix language | `/update-subtask BEP-XXX "แก้เป็นไทย"` |
| Add AC | `/update-subtask BEP-XXX "เพิ่ม AC error handling"` |

---

## References

- [ADF Templates](../shared-references/templates.md) - Sub-task structure
- [Workflows](../shared-references/workflows.md) - Update phase pattern
