---
name: story-cascade
description: |
  Update Story + cascade changes ไปยัง Sub-tasks ที่เกี่ยวข้อง ด้วย 8-phase workflow

  Phases: Fetch → Understand Changes → Impact Analysis → Explore (if needed) → Generate Story Update → Generate Sub-task Updates → Apply All → Summary

  ⭐ Composite: วิเคราะห์ impact อัตโนมัติ, update ทุกอย่างใน transaction เดียว

  Triggers: "story cascade", "update all", "cascade changes"
argument-hint: "[issue-key] [changes]"
---

# /story-cascade Command

> **Role:** PO + TA Combined
> **Input:** Existing User Story (BEP-XXX) + Changes
> **Output:** Updated Story + Updated/New Sub-tasks (cascade changes)

---

## Usage

```
/story-cascade BEP-XXX
/story-cascade BEP-XXX "เพิ่ม AC สำหรับ mobile responsive"
/story-cascade BEP-XXX "ลด scope: ยังไม่ต้องทำ feature X"
```

---

## Eight Phases (Cascade Update Workflow)

### Phase 1: Fetch Current State

**Goal:** ดึงข้อมูล Story และ Sub-tasks ทั้งหมด

**Actions:**
1. Fetch User Story:
   ```
   MCP: jira_get_issue(issue_key: "BEP-XXX")
   ```

2. Fetch all Sub-tasks:
   ```
   MCP: jira_search(jql: "parent = BEP-XXX")
   ```

3. Build inventory:

| Key | Type | Tag | Summary | Status |
|-----|------|-----|---------|--------|
| BEP-XXX | Story | - | [title] | In Progress |
| BEP-YYY | Sub-task | [BE] | ... | To Do |
| BEP-ZZZ | Sub-task | [FE-Admin] | ... | In Progress |
| BEP-QQQ | [QA] | [QA] | ... | To Do |

**Output:** Complete inventory

**Gate:** User confirms scope

---

### Phase 2: Understand Changes

**Goal:** ทำความเข้าใจสิ่งที่ต้องเปลี่ยน

**Actions:**
1. ถ้าไม่ระบุ changes → ถามว่าต้องการเปลี่ยนอะไร
2. Categorize changes:

| Change Type | Impact Level | Example |
|-------------|--------------|---------|
| **Format only** | 🟢 Low | wiki → ADF, language fix |
| **Clarify AC** | 🟢 Low | Reword for clarity |
| **Add AC** | 🟡 Medium | New requirement |
| **Modify AC** | 🟡 Medium | Change existing requirement |
| **Remove AC** | 🔴 High | Remove requirement |
| **Change Scope** | 🔴 High | Add/remove features |

**Output:** Change summary with impact level

**Gate:** User confirms changes

---

### Phase 3: Impact Analysis

**Goal:** วิเคราะห์ผลกระทบต่อ Sub-tasks

**Actions:**
1. Map Story ACs → Sub-tasks:

| AC | Related Sub-tasks | Impact |
|----|-------------------|--------|
| AC1 | BEP-YYY | ❌ No change |
| AC2 | BEP-YYY, BEP-ZZZ | ✏️ Must update |
| AC3 (new) | - | ➕ Need new sub-task |
| AC4 (removed) | BEP-QQQ | ⚠️ May need removal |

2. Determine actions for each sub-task:

| Sub-task | Action | Reason |
|----------|--------|--------|
| BEP-YYY | UPDATE | AC2 changed |
| BEP-ZZZ | UPDATE | AC2 changed |
| BEP-QQQ | REVIEW | Related AC removed |
| NEW | CREATE | AC3 needs implementation |

**Output:** Impact matrix

**Gate:** User approves cascade plan

---

### Phase 4: Codebase Exploration (if needed)

**Goal:** Update file paths ถ้ามี scope changes

**Condition:** Run only if:
- New sub-task needed
- Scope changed significantly

**Actions:**
1. Explore affected services:
   ```
   Task(subagent_type: "Explore", prompt: "Find [feature] in [path]")
   ```

2. Update file paths for affected sub-tasks

**Output:** Updated codebase findings (if applicable)

**Gate:** Skip if format-only changes

---

### Phase 5: Generate Story Update

**Goal:** สร้าง updated Story

**Actions:**
1. Apply changes to Story:
   - Update narrative (if needed)
   - Add/modify/remove ACs
   - Update scope section

2. Generate ADF JSON:
   ```
   File: tasks/bep-xxx-update.json
   ```

3. Show comparison:
   ```markdown
   ## Story Changes

   | Section | Change |
   |---------|--------|
   | Narrative | No change |
   | AC1 | No change |
   | AC2 | ✏️ Modified: [what] |
   | AC3 | ➕ Added |
   | Scope | Updated |
   ```

**Output:** Draft Story update

---

### Phase 6: Generate Sub-task Updates

**Goal:** สร้าง updates สำหรับ Sub-tasks ทั้งหมด

**Actions:**
1. For each sub-task that needs update:
   - Preserve original intent
   - Update ACs to align with Story
   - Update scope/files if needed

2. Generate ADF JSON files:
   ```
   tasks/bep-yyy-update.json
   tasks/bep-zzz-update.json
   ```

3. For new sub-tasks:
   - Follow template `jira-templates/03-sub-task.md`
   - Link to parent Story

4. Show summary:
   ```markdown
   ## Sub-task Changes

   | Key | Action | Changes |
   |-----|--------|---------|
   | BEP-YYY | UPDATE | AC alignment |
   | BEP-ZZZ | UPDATE | Format + AC |
   | NEW | CREATE | For AC3 |
   ```

**Output:** Draft sub-task updates

**Gate:** User approves all changes

---

### Phase 7: Apply All Updates

**Goal:** Update ทุกอย่างใน Jira

**Actions:**
1. Update Story first:
   ```bash
   acli jira workitem edit --from-json tasks/bep-xxx-update.json --yes
   ```

2. Update existing Sub-tasks:
   ```bash
   acli jira workitem edit --from-json tasks/bep-yyy-update.json --yes
   acli jira workitem edit --from-json tasks/bep-zzz-update.json --yes
   ```

3. Create new Sub-tasks (if any):
   ```bash
   acli jira workitem create --from-json tasks/new-subtask.json
   ```

4. Track status:
   ```
   ✅ BEP-XXX (Story) updated
   ✅ BEP-YYY updated
   ✅ BEP-ZZZ updated
   ✅ BEP-NEW created
   ```

**Output:** Update status

---

### Phase 8: Cleanup & Summary

**Goal:** สรุปและ cleanup

**Actions:**
1. Delete JSON files:
   ```bash
   rm tasks/bep-*-update.json tasks/new-*.json
   ```

2. Generate summary:
   ```markdown
   ## Cascade Update Complete

   ### Story
   | Key | Changes |
   |-----|---------|
   | BEP-XXX | AC2 modified, AC3 added |

   ### Sub-tasks Updated
   | Key | Tag | Changes |
   |-----|-----|---------|
   | BEP-YYY | [BE] | AC alignment |
   | BEP-ZZZ | [FE-Admin] | Format + AC |

   ### Sub-tasks Created
   | Key | Tag | Summary |
   |-----|-----|---------|
   | BEP-NEW | [BE] | For AC3 |

   ### Next Steps
   - [ ] Review QA sub-task (BEP-QQQ) - may need update
   - [ ] Notify Dev team of changes

   ### Links
   - Story: [BEP-XXX](jira-link)
   - Updated: BEP-YYY, BEP-ZZZ
   - Created: BEP-NEW
   ```

**Output:** Final summary

---

## Quality Checklist

Before completing:
- [ ] Story changes applied correctly
- [ ] All affected sub-tasks updated
- [ ] New sub-tasks created (if needed)
- [ ] Original intent preserved
- [ ] No orphaned sub-tasks
- [ ] ADF format via acli
- [ ] Thai + ทับศัพท์ consistent
- [ ] JSON files cleaned up

---

## Cascade Scenarios

### 1. Add New AC
```
/story-cascade BEP-XXX "เพิ่ม AC: รองรับ mobile"
```
- เพิ่ม AC ใน Story
- สร้าง Sub-task ใหม่สำหรับ AC นั้น

### 2. Modify Existing AC
```
/story-cascade BEP-XXX "AC2: เปลี่ยนจาก 3 วัน เป็น 7 วัน"
```
- แก้ AC ใน Story
- Update Sub-tasks ที่เกี่ยวข้อง

### 3. Format Migration (Batch)
```
/story-cascade BEP-XXX "migrate to ADF + Thai"
```
- Convert Story to ADF
- Convert all Sub-tasks to ADF
- Apply Thai + ทับศัพท์

### 4. Scope Reduction
```
/story-cascade BEP-XXX "ลด scope: ยังไม่ต้องทำ export"
```
- ⚠️ High impact
- Remove AC จาก Story
- Flag Sub-tasks ที่อาจต้องลบ (ไม่ลบอัตโนมัติ)

---

## Comparison: Separate vs Cascade

| Approach | Commands | Issues |
|----------|----------|--------|
| **Separate** | `/update-story` + `/update-subtask` × N | Lost context, manual tracking |
| **Cascade** | `/story-cascade BEP-XXX` | Automatic impact analysis |

**Benefits of /story-cascade:**
- วิเคราะห์ impact อัตโนมัติ
- Update ทุกอย่างใน transaction เดียว
- ไม่มี orphaned sub-tasks
- Consistent quality
- Summary ครบถ้วน

---

## Error Recovery

| Situation | Recovery |
|-----------|----------|
| Story update failed | Re-fetch and retry |
| Sub-task update failed | Story OK, retry sub-task only |
| User rejects changes | Revise based on feedback |
| Conflict with in-progress work | Warn and ask for confirmation |

---

## References

- [ADF Templates](../shared-references/templates.md)
- [Writing Style](../shared-references/writing-style.md)
- [Tool Selection](../shared-references/tools.md)
