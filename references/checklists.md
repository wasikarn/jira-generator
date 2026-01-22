# Quality Checklists

> **Purpose:** รวม checklists สำหรับ quality validation - โหลดเมื่อต้องการ verify

---

## INVEST Criteria

| Criteria | Question | Red Flags |
| --- | --- | --- |
| **I**ndependent | ทำได้โดยไม่ต้องรอ task อื่น? | "after", "depends on", "requires" |
| **N**egotiable | มีหลายวิธี implement? | Lock specific solution |
| **V**aluable | User ได้อะไร? | No clear benefit |
| **E**stimable | Estimate effort ได้? | Vague scope, >20 words |
| **S**mall | เสร็จใน sprint? | XL effort |
| **T**estable | เขียน test ได้? | "maybe", "possibly", "somehow" |

---

## Product Manager Checklist

### Epic Quality
- [ ] Clear business value articulated
- [ ] Success criteria are measurable
- [ ] User stories identified
- [ ] Risks documented with mitigations
- [ ] Dependencies mapped

### RICE Prioritization
- [ ] Reach estimated with data
- [ ] Impact scored objectively
- [ ] Confidence level honest
- [ ] Effort estimated by team

### PRD Quality
- [ ] Problem clearly defined
- [ ] Solution addresses problem
- [ ] Scope is explicit (in/out)
- [ ] Success metrics are measurable

---

## Product Owner Checklist

### User Story Quality
- [ ] Follows "As a... I want... So that..." format
- [ ] Persona is specific (not generic)
- [ ] Action is clear and specific
- [ ] Benefit is user-focused
- [ ] INVEST criteria all pass

### Acceptance Criteria Quality
- [ ] Happy path covered
- [ ] Validation rules specified
- [ ] Error handling defined
- [ ] Edge cases considered
- [ ] All AC are testable (no vague words)

### Sprint Planning
- [ ] Capacity calculated (with focus factor)
- [ ] Committed ≤ capacity
- [ ] Stretch ≤ 120% capacity
- [ ] All stories are Ready
- [ ] Dependencies identified

### Backlog Health
- [ ] Stories prioritized
- [ ] Top items refined
- [ ] No items > 13 points
- [ ] Ready items ≥ 2 sprints worth

---

## Technical Analyst Checklist

### Analysis Quality
- [ ] Domain analysis done (if complex)
- [ ] Impact analysis complete
- [ ] Codebase explored

### Sub-task Quality
- [ ] กระชับ - ไม่มีคำฟุ่มเฟือย
- [ ] ชัดเจน - ไม่มีคำคลุมเครือ
- [ ] ข้อมูลครบ - context เพียงพอ
- [ ] ถูกต้อง - file paths ตรง codebase
- [ ] เป็นกันเอง - ใช้ทับศัพท์

### Coherence & Alignment
- [ ] ทุก sub-task ตอบโจทย์ User Story
- [ ] รวมทุก sub-tasks = User Story สำเร็จ
- [ ] ไม่มี task ที่เพิ่มเองนอก scope
- [ ] Dependencies ระบุครบ

### Scope Check
- [ ] มีเฉพาะ [BE], [FE-Admin], [FE-Web]
- [ ] ไม่มี QA/Testing sub-tasks

---

## QA Analyst Checklist

### Test Plan Quality
- [ ] ทุก AC มี test case อย่างน้อย 1 case
- [ ] Happy path covered
- [ ] Error cases covered
- [ ] Edge cases identified
- [ ] Test data requirements defined
- [ ] Risk assessment completed (if applicable)

### Test Case Quality
- [ ] Clear test objective
- [ ] Preconditions defined
- [ ] Steps are specific and reproducible
- [ ] Expected results are measurable
- [ ] Linked to AC in User Story
- [ ] Effort is S or M (no L/XL)

### Coverage Check
- [ ] Coverage matrix complete (AC → Test Cases)
- [ ] All critical paths tested
- [ ] Validation rules covered
- [ ] Error handling covered

### Scope Check
- [ ] มีเฉพาะ [QA] tag
- [ ] ไม่มี dev sub-tasks

---

## Common AC Anti-patterns

| ❌ Bad | ✅ Good |
| --- | --- |
| "ระบบทำงานได้ดี" | "respond ภายใน 2 วินาที" |
| "handle error เรียบร้อย" | "return 400 พร้อม error message" |
| "รองรับข้อมูลเยอะๆ" | "รองรับได้ถึง 10,000 records" |
| "ควรจะทำงานได้" | "must return 200 เมื่อ success" |

---

## Effort Sizing Guide

| Size | Complexity | Example |
| --- | --- | --- |
| **S** | Simple | Config change, 1 component |
| **M** | Medium | Multi-component, simple API |
| **L** | Complex | Multi-service, integration |
| **XL** | ❌ Split | ต้องแตกย่อย |

---

## Priority Guide

| Priority | When | Example |
| --- | --- | --- |
| **Critical** 🔴 | Security, blocking, data loss | Auth bypass fix |
| **High** 🟠 | Core functionality, primary flows | Checkout flow |
| **Medium** 🟡 | Improvements, secondary features | Search filters |
| **Low** 🟢 | Nice-to-have, cosmetic | Button style |
