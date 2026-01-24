---
name: update-story
description: |
  แก้ไข User Story ที่มีอยู่ ด้วย 5-phase update workflow

  Phases: Fetch Current → Impact Analysis → Preserve Intent → Generate Update → Apply Update

  รองรับ: เพิ่ม AC, แก้ไข AC, ปรับ scope, format migration

  Triggers: "update story", "แก้ไข story", "เพิ่ม AC"
argument-hint: "[issue-key] [changes]"
---

# /update-story Command

> **Role:** Senior Product Owner
> **Input:** Existing User Story (BEP-XXX)
> **Output:** Updated User Story

---

## Usage

```
/update-story BEP-XXX
/update-story BEP-XXX "เพิ่ม AC สำหรับ mobile responsive"
```

---

## Five Phases

### Phase 1: Fetch Current State

**Goal:** ดึง story ปัจจุบันและ context

**Actions:**
1. Fetch User Story:
   ```
   MCP: jira_get_issue(issue_key: "BEP-XXX")
   ```
2. Fetch related items:
   ```
   MCP: jira_search(jql: "parent = BEP-XXX")  # Sub-tasks
   ```
3. อ่าน:
   - Current narrative
   - Acceptance Criteria
   - Scope
   - Linked Sub-tasks
   - Status

**Output:** Current state summary

**Gate:** User confirms what to update

---

### Phase 2: Impact Analysis

**Goal:** วิเคราะห์ผลกระทบของ changes

**Actions:**
1. ถ้าเปลี่ยน AC:
   - Sub-tasks ไหนกระทบ?
   - QA test cases ต้อง update?
2. ถ้าเปลี่ยน scope:
   - ต้องสร้าง sub-task ใหม่?
   - ต้องลบ sub-task เก่า?

**Impact Matrix:**

| Change Type | Impact on Sub-tasks | Impact on QA |
|-------------|--------------------:|-------------:|
| Add AC | ต้องสร้าง sub-task? | ต้องเพิ่ม test? |
| Remove AC | ต้องลบ sub-task? | ต้องลบ test? |
| Modify AC | ต้อง update sub-task? | ต้อง update test? |
| Format only | ❌ No impact | ❌ No impact |

**Output:** Impact analysis

**Gate:** User acknowledges impact

---

### Phase 3: Preserve Intent

**Goal:** รักษา core intent ของ story

**Critical Rules:**
- ✅ เพิ่ม AC ได้ (ถ้า scope ยังเหมาะสม)
- ✅ ปรับ wording ได้
- ✅ แปลภาษาได้
- ⚠️ ระวังเปลี่ยน scope (ต้อง re-analyze)
- ❌ ห้ามเปลี่ยน core value proposition โดยไม่บอก

**Actions:**
1. Document original:
   - As a [who]
   - I want to [what]
   - So that [why]
2. Compare with requested changes
3. Flag scope changes for explicit approval

**Output:** Intent preservation checklist

---

### Phase 4: Generate Update

**Goal:** สร้าง description ใหม่

**Actions:**
1. Generate ADF JSON:
   - Follow `jira-templates/02-user-story.md`
   - Use Thai + ทับศัพท์
   - Preserve original ACs (unless explicitly changed)
   - Add new ACs (if requested)

2. แสดง comparison:
   ```markdown
   ## Narrative
   [No change / Changed: ...]

   ## Acceptance Criteria
   | AC | Status | Change |
   |----|--------|--------|
   | AC1 | ✅ Kept | - |
   | AC2 | ✏️ Modified | [what changed] |
   | AC3 | ➕ New | [new AC] |

   ## Scope
   [No change / Added: ... / Removed: ...]
   ```

**Output:** Draft update for review

**Gate:** User approves changes

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

3. ถ้ามี cascading updates needed:
   - Notify user about sub-tasks that need updating
   - Suggest: `/update-subtask BEP-YYY`

4. Verify update

**Output:**
- Confirmation + link
- List of related items that may need updating

---

## Quality Checklist

Before updating:
- [ ] Original narrative preserved (unless explicitly changed)
- [ ] Impact on sub-tasks analyzed
- [ ] No silent scope changes
- [ ] INVEST still valid
- [ ] ADF format via acli
- [ ] User approved all changes

---

## Error Recovery

| Error | Solution |
|-------|----------|
| Lost original content | Re-fetch story before retry |
| Scope changed silently | Roll back, re-analyze impact |
| acli update fails | Check JSON structure, verify issue key format |
| Cascading changes missed | Use `/story-cascade` instead for automatic handling |

---

## Common Update Scenarios

### 1. Add New AC
```
/update-story BEP-XXX "เพิ่ม AC: mobile responsive"
```
- เพิ่ม AC ใหม่
- Flag: อาจต้องสร้าง sub-task ใหม่

### 2. Format Migration
```
/update-story BEP-XXX "migrate to ADF format"
```
- ไม่เปลี่ยน content
- ปรับ format + panels

### 3. Clarify AC
```
/update-story BEP-XXX "AC2 ไม่ชัด ช่วยเขียนใหม่"
```
- Rewrite AC ให้ชัดเจนขึ้น
- รักษา meaning เดิม

### 4. Scope Adjustment
```
/update-story BEP-XXX "ลด scope: ยังไม่ต้องทำ feature X"
```
- ⚠️ High impact
- ต้อง review sub-tasks ที่กระทบ

---

## Cascading Updates

เมื่อ story เปลี่ยน อาจต้อง update:

| Item | When to Update |
|------|----------------|
| Sub-tasks | AC เปลี่ยน, scope เปลี่ยน |
| QA Sub-task | AC เปลี่ยน |
| Technical Note | Scope/architecture เปลี่ยน |

**Suggest follow-up commands:**
```
Story updated. Related items that may need updating:
- BEP-YYY (Sub-task) - AC2 changed
- BEP-ZZZ ([QA]) - New AC added

Use `/update-subtask BEP-YYY` to update
```

---

## References

- [ADF Templates](../shared-references/templates.md)
- [Writing Style](../shared-references/writing-style.md)
- [Tool Selection](../shared-references/tools.md)
