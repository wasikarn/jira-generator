# Subtask Best Practices — Quick Reference

## When to Use Subtasks vs Split Story

| Situation | Action | เหตุผล |
| --- | --- | --- |
| Story ซับซ้อน แต่ scope ถูกต้อง | ใช้ Subtask | แตก task tracking ภายใน story |
| Story scope ใหญ่เกินไป (>4 วัน) | Split Story (SPIDR) | แต่ละ story ต้องส่ง value ได้เอง |
| ต้องการ parallel work | ใช้ Subtask | assign คนละคนได้ |
| แต่ละส่วนมี independent value | Split Story | ไม่ควรซ่อน value ไว้ใน subtask |

## SMART Criteria (ตัวตรวจสอบคุณภาพ Subtask)

| Criteria | ความหมาย | Red Flag |
| --- | --- | --- |
| **S**pecific | ชัดเจนว่าทำอะไร | "ทำส่วน backend" (vague) |
| **M**easurable | วัดได้ว่าเสร็จหรือยัง | ไม่มี AC หรือ definition of done |
| **A**chievable | คนเดียวทำเสร็จได้ | ต้องรอคนอื่น 3 คน |
| **R**elevant | ตรงกับ parent story | ไม่เกี่ยวกับ story เลย |
| **T**ime-boxed | ≤ 1 วัน (4-8 ชม.) | ใช้เวลา 3 วัน |

## Subtask Size Guide

| Size | Duration | Guideline |
| --- | --- | --- |
| XS | < 2 hours | อาจเล็กเกินไป — รวมกับ subtask อื่นได้ |
| S | 2-4 hours | เหมาะสม |
| M | 4-8 hours (1 day) | เหมาะสม — ขอบเขตบน |
| L | > 1 day | ต้อง split — ใหญ่เกินไปสำหรับ subtask |

## Ideal Count

- **3-10 subtasks** ต่อ story (ขึ้นกับ complexity)
- < 3 subtasks → story อาจเล็กพอที่ไม่ต้องแตก
- > 10 subtasks → story ใหญ่เกินไป ควร split story ก่อน (ใช้ SPIDR)
- เป้าหมาย: **5-7 subtasks** ต่อ story (sweet spot)

## Subtask Content Requirements

### ต้องมี (Required)

- **Objective**: 1 ประโยค — ทำอะไร ทำไม
- **Scope**: file paths จริงจาก codebase (ห้าม generic)
- **Acceptance Criteria**: Given/When/Then (อย่างน้อย 1 AC)
- **Service Tag**: `[BE]`, `[FE-Admin]`, `[FE-Web]`, `[QA]`

### ควรมี (Recommended)

- Dependencies: ต้องรอ subtask ไหนก่อน
- Technical Notes: implementation hints, API contracts
- Test approach: unit test, integration test, manual test
- **Start/End Dates**: `{{START_DATE_FIELD}}` — ช่วย dependency-chain analysis

## Subtask Date Fields

**⚠️ Important:** ตั้ง Start Date เมื่อ assign subtask — ช่วย dependency-chain คำนวณ critical path

| Field | Custom Field | Use Case |
| --- | --- | --- |
| Start Date | `{{START_DATE_FIELD}}` | วันที่เริ่มทำ subtask |
| Due Date | `duedate` (standard) | deadline ของ subtask |

**MCP Example:**

```python
jira_update_issue(
    issue_key="{{PROJECT_KEY}}-XXX",
    additional_fields={
        "{{START_DATE_FIELD}}": "2026-02-06",  # Start Date
        "duedate": "2026-02-08"              # Due Date
    }
)
```

**Why Dates Matter:**

- `/dependency-chain` skill ใช้ dates คำนวณ critical path
- Sprint planning ใช้ dates เพื่อ detect overflow (dates นอก sprint range)
- Team capacity planning ใช้ dates เพื่อ balance workload per day

## Decomposition Techniques

| Technique | วิธี | ตัวอย่าง |
| --- | --- | --- |
| **By Layer** | แยกตาม service tag | [BE] API + [FE-Admin] UI + [QA] Test |
| **By Step** | แยกตามขั้นตอน | DB migration → API endpoint → UI form → Integration test |
| **By Scenario** | แยกตาม AC ของ parent | Happy path → Edge case → Error handling |
| **By Component** | แยกตาม component/module | Form component → List component → Filter component |

### Decomposition Rules

- **Vertical Slice เมื่อเป็นไปได้** — subtask ที่ deliver observable change ดีกว่า layer-only
- แต่ละ subtask ต้อง **independently completable** โดยคนเดียว
- ทุก subtask ต้องมี **clear definition of done**
- ห้าม subtask ที่เป็น "leftover" หรือ "miscellaneous"

## Anti-Patterns

| Anti-Pattern | ปัญหา | แก้ไข |
| --- | --- | --- |
| Over-layering | hierarchy ลึกเกิน = admin overhead | ใช้แค่ Epic → Story → Subtask |
| Subtask ไม่มี AC | ไม่รู้ว่าเสร็จเมื่อไหร่ | เขียน Given/When/Then เสมอ |
| Subtask แทน story split | ซ่อน value ไว้ใน subtask | ถ้า subtask ส่ง independent value → ควรเป็น story |
| Generic paths | "แก้ไขไฟล์ backend" | Explore codebase → ใช้ real file paths |
| One-person subtask | แตกให้ตัวเอง track | ถ้าคนเดียวทำทั้ง story → อาจไม่ต้องแตก |
| Copy-paste AC | AC ซ้ำกับ parent story | Subtask AC ควร specific กว่า parent |

## Sources

- Atlassian Subtasks: <https://support.atlassian.com/jira-software-cloud/docs/what-is-a-sub-task/>
- Story Decomposition: <https://www.mountaingoatsoftware.com/blog/why-i-dont-use-sub-tasks>
- Agile Alliance: <https://www.agilealliance.org/glossary/decomposition/>
