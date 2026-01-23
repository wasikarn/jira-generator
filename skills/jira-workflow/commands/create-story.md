# /create-story Command

> **Role:** Senior Product Owner
> **Input:** Feature requirements / Epic context
> **Output:** User Story in Jira

---

## Usage

```
/create-story
/create-story "ต้องการให้ผู้ใช้สามารถดูประวัติการใช้เครดิตได้"
```

---

## Five Phases

### Phase 1: Discovery

**Goal:** ทำความเข้าใจ requirements

**Actions:**
1. ถ้ามี Epic → Fetch Epic context:
   ```
   MCP: jira_get_issue(issue_key: "BEP-XXX")
   ```
2. ถาม user เกี่ยวกับ:
   - Who is the user? (persona)
   - What do they want to do?
   - Why? (business value)
   - Any constraints or dependencies?

**Output:** Requirements summary

**Gate:** User confirms understanding

---

### Phase 2: Write User Story

**Goal:** เขียน User Story ตาม format

**Actions:**
1. เขียน narrative:
   ```
   As a [persona],
   I want to [action],
   So that [benefit].
   ```

2. กำหนด Acceptance Criteria:
   - AC1: Given/When/Then
   - AC2: Given/When/Then
   - ...

3. ระบุ:
   - Scope (affected services)
   - DoD (Definition of Done)
   - Story Points (ถ้ามี)

**Template:** See `jira-templates/02-user-story.md`

**Writing Style:**
- ภาษาไทย + ทับศัพท์
- กระชับ, ชัดเจน

**Output:** Draft User Story

**Gate:** User reviews story

---

### Phase 3: INVEST Validation

**Goal:** ตรวจสอบคุณภาพ User Story

**Checklist:**

| Criteria | Check | Note |
|----------|-------|------|
| **I**ndependent | ✅/❌ | ไม่พึ่งพา story อื่น |
| **N**egotiable | ✅/❌ | มี room สำหรับ discussion |
| **V**aluable | ✅/❌ | มี business value ชัดเจน |
| **E**stimable | ✅/❌ | ประเมิน effort ได้ |
| **S**mall | ✅/❌ | ทำเสร็จใน 1 sprint |
| **T**estable | ✅/❌ | ทุก AC verify ได้ |

**Output:** INVEST validation result

**Gate:** All criteria pass

---

### Phase 4: Create in Jira

**Goal:** สร้าง User Story ใน Jira

**Actions:**
1. Generate ADF JSON:
   - File: `tasks/bep-xxx-story.json`

2. Create via acli:
   ```bash
   acli jira workitem create --from-json tasks/bep-xxx-story.json
   ```

**ADF Structure:**
- Info panel: User Story narrative
- Success panels: Each AC with Given/When/Then
- Table: Scope (Backend/Admin/Website)
- Bullet list: DoD
- Table: Links (Design, Technical Note)

**Output:** User Story URL

---

### Phase 5: Handoff

**Goal:** ส่งต่อให้ TA

**Output Format:**

```markdown
## User Story Created: [Title] (BEP-XXX)

### Summary
- **As a:** [persona]
- **I want to:** [action]
- **So that:** [benefit]

### Acceptance Criteria
1. [AC1 summary]
2. [AC2 summary]
3. [AC3 summary]

### Handoff to TA
Story: BEP-XXX
ACs: [count]
Ready for: Technical Analysis

Use `/analyze-story BEP-XXX` to continue
```

---

## Quality Checklist

Before completing:
- [ ] User Story follows As a/I want/So that format
- [ ] All ACs have Given/When/Then
- [ ] INVEST criteria pass
- [ ] Scope is clear (which services)
- [ ] DoD is defined
- [ ] ADF format via acli
- [ ] Content is Thai + ทับศัพท์
- [ ] Handoff summary provided

---

## AC Writing Tips

**Good AC:**
```
Given: ผู้ใช้อยู่หน้า Credit History
When: คลิก filter "เดือนนี้"
Then: แสดงรายการ transactions ของเดือนปัจจุบันเท่านั้น
```

**Bad AC:**
```
- ต้องมี filter (ไม่ชัดเจน)
- หน้าต้องทำงานได้ (ไม่ testable)
```

---

## Story Points Guide

| Points | Complexity |
|--------|------------|
| 1 | Simple, config only |
| 2 | Small feature, 1 service |
| 3 | Medium, 1-2 services |
| 5 | Complex, multi-service |
| 8 | Very complex, integration |
| 13+ | ❌ ต้องแตก story |
