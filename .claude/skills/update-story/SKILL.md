---
name: update-story
description: |
  แก้ไข User Story ที่มีอยู่ ด้วย 5-phase update workflow

  Phases: Fetch Current → Impact Analysis → Preserve Intent → Generate Update → Apply Update

  รองรับ: เพิ่ม AC, แก้ไข AC, ปรับ scope, format migration

  Triggers: "update story", "แก้ไข story", "เพิ่ม AC"
argument-hint: "[issue-key] [changes]"
---

# /update-story

**Role:** Senior Product Owner
**Output:** Updated User Story

## Phases

### 1. Fetch Current State

- `MCP: jira_get_issue(issue_key: "BEP-XXX")`
- `MCP: jira_search(jql: "parent = BEP-XXX")` → Sub-tasks
- อ่าน: Narrative, ACs, Scope, Status
- **Gate:** User confirms what to update

### 2. Impact Analysis

| Change Type | Impact on Sub-tasks | Impact on QA |
| --- | --- | --- |
| Add AC | ต้องสร้าง sub-task? | ต้องเพิ่ม test? |
| Remove AC | ต้องลบ sub-task? | ต้องลบ test? |
| Modify AC | ต้อง update sub-task? | ต้อง update test? |
| Format only | ❌ No impact | ❌ No impact |

**Gate:** User acknowledges impact

### 3. Preserve Intent

- ✅ เพิ่ม AC ได้
- ✅ ปรับ wording ได้
- ⚠️ ระวังเปลี่ยน scope (ต้อง re-analyze)
- ❌ ห้ามเปลี่ยน core value proposition โดยไม่บอก

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
| Add AC | `/update-story BEP-XXX "เพิ่ม AC mobile"` | 🟡 Medium |
| Format migrate | `/update-story BEP-XXX "migrate ADF"` | 🟢 Low |
| Clarify AC | `/update-story BEP-XXX "AC2 ไม่ชัด"` | 🟢 Low |
| Reduce scope | `/update-story BEP-XXX "ลด scope"` | 🔴 High |

---

## References

- [ADF Core Rules](../shared-references/templates.md) - CREATE/EDIT rules, panels, styling
- [Story Template](../shared-references/templates-story.md) - Story ADF structure
- [Workflows](../shared-references/workflows.md) - INVEST, AC format
