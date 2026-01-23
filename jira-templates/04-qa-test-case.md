# Jira QA Test Case Template

> **Version:** 1.1 | **Updated:** 2026-01-22

---

## หลักการสำคัญ

**1 User Story = 1 [QA] Sub-task** (รวมทุก test scenario ไว้ใน sub-task เดียว)

---

## Summary Format

```
[QA] - Test: [Story title หรือ feature name]
```

**Tag:** `[QA]` เท่านั้น

**Examples:**
- ✅ `[QA] - Test: หน้าเมนูคูปอง (Coupon Menu)`
- ✅ `[QA] - Test: User Authentication Flow`
- ✅ `[QA] - Test: Product Search & Filter`
- ❌ `[QA] - Test: Display cards` (เฉพาะเจาะจงเกินไป - ควรรวมทั้ง story)
- ❌ `Test login` (ไม่มี tag)

---

## Description Template (Copy ไปใช้เลย)

```markdown
## Story Narrative

> As a [persona], I want to [action] so that [benefit]

---

## Test Objective

[What this test validates - อธิบาย scope ทั้งหมดของ story]

---

## AC Coverage

| AC | Description | Test Scenarios |
| --- | --- | --- |
| AC1 | [desc] | TC1, TC2 |
| AC2 | [desc] | TC3 |
| AC3 | [desc] | TC4, TC5 |

**Coverage:** [X] scenarios / [Y] ACs

---

## Test Scenarios Summary

| ID | Scenario | AC | Type | Priority |
| --- | --- | --- | --- | --- |
| TC1 | [Happy path scenario] | AC1 | Happy | High |
| TC2 | [Alternative path] | AC1 | Happy | Medium |
| TC3 | [Error scenario] | AC2 | Error | High |
| TC4 | [Edge case] | AC3 | Edge | Medium |
| TC5 | [UI/Responsive] | AC3 | UI | Low |

---

## Test Steps Detail

### TC1: [Scenario Name]

**AC:** AC1
**Type:** Happy Path
**Priority:** High

**Preconditions:**
- [Setup required]

**Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Result:**
- [Expected outcome - specific, measurable]

---

### TC2: [Scenario Name]

**AC:** AC1
**Type:** Happy Path
**Priority:** Medium

**Preconditions:**
- [Setup required]

**Steps:**
1. [Step 1]
2. [Step 2]

**Expected Result:**
- [Expected outcome]

---

(เพิ่ม TC3, TC4, ... ตามจำนวน scenario)

---

## Test Data Requirements

| Data | Description | Source |
| --- | --- | --- |
| [Data type] | [Description] | [Manual/Seed/API] |

---

## Notes

- [Edge case to watch]
- [Dependencies]
- [Risks]

---

## Reference

📋 User Story: [BEP-XXX](link)
📄 Test Plan: [Confluence link]
```

---

## Other Fields

| Field | Value |
| --- | --- |
| Issue Type | Subtask |
| Project | BEP |
| Parent | [User Story] |
| Priority | Critical/High/Medium/Low |

---

## Effort Size

| Size | Scenarios | When |
| --- | --- | --- |
| S | 1-3 | Simple story, few ACs |
| M | 4-6 | Moderate story |
| L | 7-10 | Complex story, many ACs |

**Note:** ไม่ต้อง split - รวมทุก scenario ไว้ใน sub-task เดียว

---

## Priority Guide

| Priority | When | Example |
| --- | --- | --- |
| 🔴 Critical | Core flow, data integrity | Payment, authentication |
| 🟠 High | Primary features | CRUD operations |
| 🟡 Medium | Secondary features | Filters, sorting |
| 🟢 Low | Nice-to-have | UI feedback |

---

## Test Type Reference

| Type | Focus | Example |
| --- | --- | --- |
| Happy | Normal flow succeeds | Login with valid creds |
| Validation | Input rules enforced | Invalid email rejected |
| Error | Failure handled | Network error shows message |
| Edge | Boundary cases | Max 100 items limit |
| Security | Access control | Unauthorized returns 403 |

---

## Quality Check

Before submit:
- [ ] **1 sub-task per story** - รวมทุก scenario ไว้ใน sub-task เดียว
- [ ] **Clear objective** - อธิบาย test scope ของทั้ง story
- [ ] **AC coverage table** - map ทุก AC กับ scenarios
- [ ] **All scenarios included** - Happy, Error, Edge, UI
- [ ] **Specific steps** - steps ละเอียด reproducible
- [ ] **Expected results** - ผลลัพธ์ชัดเจน verifiable
- [ ] **Test data defined** - ข้อมูล test ระบุครบ

---

_See `references/checklists.md` for QA checklist_
