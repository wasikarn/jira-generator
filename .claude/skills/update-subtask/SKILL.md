---
name: update-subtask
description: |
  แก้ไข Sub-task ที่มีอยู่ ด้วย 5-phase update workflow

  Phases: Fetch Current → Identify Changes → Preserve Intent → Generate Update → Apply Update

  รองรับ: format migration, add details, language fix, add AC

  Triggers: "update subtask", "แก้ไข subtask", "ปรับ subtask"
argument-hint: "[issue-key] [changes]"
---

# /update-subtask Command

> **Role:** Senior Technical Analyst
> **Input:** Existing Sub-task (BEP-XXX)
> **Output:** Updated Sub-task

---

## Usage

```
/update-subtask BEP-XXX
/update-subtask BEP-XXX "เพิ่ม AC สำหรับ validation"
```

---

## Five Phases

### Phase 1: Fetch Current State

**Goal:** ดึง sub-task ปัจจุบันและทำความเข้าใจ

**Actions:**
1. Fetch sub-task:
   ```
   MCP: jira_get_issue(issue_key: "BEP-XXX")
   ```
2. อ่าน:
   - Current description
   - Summary
   - Parent story
   - Status
3. Fetch parent story สำหรับ context

**Output:** Current state summary

**Gate:** User confirms what to update

---

### Phase 2: Identify Changes

**Goal:** ระบุสิ่งที่ต้องเปลี่ยนแปลง

**Change Types:**

| Type | Description | Example |
|------|-------------|---------|
| **Format** | ปรับ format ตาม template | wiki → ADF |
| **Content** | เพิ่ม/แก้ไขเนื้อหา | เพิ่ม AC, แก้ scope |
| **Language** | ปรับภาษา | English → Thai + ทับศัพท์ |
| **Codebase** | Update file paths | generic → actual paths |

**Actions:**
1. เปรียบเทียบ current vs template (`jira-templates/03-sub-task.md`)
2. ระบุ gaps/issues
3. ถาม user ว่าต้องการเปลี่ยนอะไร

**Output:** Change list

**Gate:** User approves change scope

---

### Phase 3: Preserve Intent

**Goal:** รักษา original intent ไม่เปลี่ยน meaning

**Critical Rules:**
- ✅ ปรับ format ได้
- ✅ เพิ่ม details ที่ขาดได้
- ✅ แปลภาษาได้
- ❌ ห้ามเปลี่ยน objective
- ❌ ห้ามเปลี่ยน scope โดยไม่บอก
- ❌ ห้ามลบ AC ที่มีอยู่

**Actions:**
1. Document original intent
2. Map old content → new structure
3. Flag any meaning changes for approval

**Output:** Intent preservation checklist

---

### Phase 4: Generate Update

**Goal:** สร้าง description ใหม่

**Actions:**
1. ถ้าต้อง explore codebase (เช่น update file paths):
   ```
   Task(subagent_type: "Explore", prompt: "...")
   ```

2. Generate ADF JSON:
   - Apply template structure
   - Use Thai + ทับศัพท์
   - Add inline code marks for technical terms

3. แสดง Before/After comparison:
   ```markdown
   ## Before
   [สรุป description เดิม]

   ## After
   [สรุป description ใหม่]

   ## Changes
   - [Change 1]
   - [Change 2]
   ```

**Output:** Draft update for review

**Gate:** User approves changes before update

---

### Phase 5: Apply Update

**Goal:** Update ใน Jira

**Actions:**
1. Save ADF JSON:
   ```
   File: tasks/bep-xxx-update.json
   ```

2. Update via acli:
   ```bash
   acli jira workitem edit --from-json tasks/bep-xxx-update.json --yes
   ```

3. Verify update:
   ```
   MCP: jira_get_issue(issue_key: "BEP-XXX")
   ```

4. Clean up JSON file (optional)

**Output:** Confirmation + link to updated issue

---

## Quality Checklist

Before updating:
- [ ] Original intent preserved
- [ ] No AC meaning changed without approval
- [ ] Format matches template
- [ ] Thai + ทับศัพท์ applied
- [ ] ADF format via acli (not MCP)
- [ ] User approved changes
- [ ] Before/After shown

---

## Common Update Scenarios

### 1. Format Migration (wiki → ADF)
```
/update-subtask BEP-XXX "migrate to ADF format"
```
- ไม่เปลี่ยน content
- ปรับ format + panels + inline code

### 2. Add Missing Details
```
/update-subtask BEP-XXX "เพิ่ม file paths จาก codebase"
```
- Explore codebase ก่อน
- เพิ่ม actual file paths

### 3. Language Fix
```
/update-subtask BEP-XXX "แก้เป็นภาษาไทย"
```
- แปลเป็น Thai + ทับศัพท์
- รักษา technical terms เป็น English

### 4. Add AC
```
/update-subtask BEP-XXX "เพิ่ม AC สำหรับ error handling"
```
- เพิ่ม AC ใหม่
- ไม่แก้ไข AC เดิม

---

## Error Recovery

| Error | Solution |
|-------|----------|
| Lost original content | Re-fetch from Jira before retry |
| User rejects changes | Revise based on feedback |
| acli error | Check JSON structure |

---

## References

- [ADF Templates](../shared-references/templates.md)
- [Writing Style](../shared-references/writing-style.md)
- [Tool Selection](../shared-references/tools.md)
