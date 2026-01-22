# Update Sub-task Prompt

> ใช้ prompt นี้เพื่อ update sub-tasks ที่สร้างไปแล้วให้ตรงตาม template ใหม่

---

## Prompt (Copy ไปใช้เลย)

```
คุณคือ Senior Technical Analyst

## Task
Update sub-task [BEP-XXX] ให้ตรงตาม template ใน `jira-templates/03-sub-task.md`

## Rules
1. **รักษา original intent** - ห้ามเปลี่ยนวัตถุประสงค์หรือ scope เดิม
2. **รักษา AC เดิม** - ปรับ format เป็น Given-When-Then แต่ไม่เปลี่ยนความหมาย
3. **กระชับ** - ตัดคำฟุ่มเฟือย แต่ข้อมูลสำคัญต้องครบ
4. **ชัดเจน** - ไม่คลุมเครือ
5. **เป็นกันเอง** - ใช้ภาษาที่คุยกับทีมเล็ก

## Workflow
1. ดึง sub-task ปัจจุบัน → Atlassian:getJiraIssue
2. อ่าน template → jira-templates/03-sub-task.md
3. เปรียบเทียบ structure เดิม vs template ใหม่
4. ร่าง description ใหม่ (รักษา intent เดิม)
5. ยืนยันกับผมก่อน update
6. Update → Atlassian:editJiraIssue

## Output Format
แสดง:
- **Before:** [description เดิม - สรุป]
- **After:** [description ใหม่ตาม template]
- **Changes:** [สิ่งที่เปลี่ยน - format only, ไม่ใช่ content]

รอผมยืนยันก่อน update จริง
```

---

## ตัวอย่างการใช้งาน

### Single Sub-task
```
Update sub-task BEP-123 ให้ตรงตาม template ใน jira-templates/03-sub-task.md

Rules: รักษา original intent, ปรับ format only
```

### Multiple Sub-tasks (ทีละตัว)
```
Update sub-tasks ทั้งหมดใน User Story BEP-100 ให้ตรงตาม template

เริ่มจาก sub-task แรก แสดง before/after ให้ผมยืนยันก่อน update แต่ละตัว
```

### Batch Update (ถ้ามั่นใจ)
```
Update sub-tasks ทั้งหมดใน User Story BEP-100 ให้ตรงตาม template

แสดง summary ของ changes ทั้งหมดก่อน แล้ว update ทีเดียว
```

---

## Template Reference (jira-templates/03-sub-task.md)

```markdown
## Story Narrative

> As a [persona], I want to [action] so that [benefit]

---

## Objective

[What and why - 1-2 ประโยค กระชับ]

---

## Scope

**Files:**
- `path/to/file1.ts`
- `path/to/file2.ts`

**Dependencies:**
- [Related component/service]

---

## Requirements

- [Requirement 1]
- [Requirement 2]

---

## Acceptance Criteria

**AC1: [Happy Path]**
Given [precondition]
When [action]
Then [result]

**AC2: [Validation]**
Given [invalid input]
When [action]
Then [validation error]

**AC3: [Error Handling]**
Given [error condition]
When [action]
Then [error response]

---

## Notes

- [Edge case to handle]
- [Pattern to follow]

---

## Reference

📄 User Story Doc: [Confluence link]
```

---

## ⚠️ Important Reminders

| ✅ Do | ❌ Don't |
| --- | --- |
| รักษา original intent | เปลี่ยน scope/objective |
| ปรับ format ให้ตรง template | เพิ่ม/ลด requirements |
| แปลง AC เป็น Given-When-Then | เปลี่ยนความหมาย AC |
| ตัดคำฟุ่มเฟือย | ตัดข้อมูลสำคัญ |
| ยืนยันก่อน update | Update โดยไม่ถาม |
