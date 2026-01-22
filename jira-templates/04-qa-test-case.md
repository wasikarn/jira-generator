# Jira QA Test Case Template

> **Version:** 1.0 | **Updated:** 2026-01-22

---

## Summary Format

```
[QA] - Test: [brief description]
```

**Tag:** `[QA]` เท่านั้น

**Examples:**
- ✅ `[QA] - Test: User login with valid credentials`
- ✅ `[QA] - Test: Product search validation`
- ❌ `Test login` (ไม่มี tag)
- ❌ `[QA] Create test for login` (ไม่ใช่ format)

---

## Description Template (Copy ไปใช้เลย)

```markdown
## Story Narrative

> As a [persona], I want to [action] so that [benefit]

---

## Test Objective

[What this test validates - 1-2 ประโยค]

---

## Related AC

- **AC[X]:** [copy AC from User Story]

---

## Test Scenarios

| ID | Scenario | Type | Priority |
| --- | --- | --- | --- |
| TC1 | [Happy path scenario] | Happy | High |
| TC2 | [Error scenario] | Error | Medium |
| TC3 | [Edge case scenario] | Edge | Low |

---

## Test Steps

### TC1: [Scenario Name]

**Type:** Happy Path

**Preconditions:**
- [Setup required]

**Test Data:**
- [Required data]

**Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Result:**
- [Expected outcome - specific, measurable]

---

### TC2: [Scenario Name]

**Type:** Error/Validation

**Preconditions:**
- [Setup required]

**Test Data:**
- [Invalid data]

**Steps:**
1. [Step 1]
2. [Step 2]

**Expected Result:**
- [Error message/behavior]

---

## Notes

- [Edge case to watch]
- [Related test dependencies]

---

## Reference

📋 User Story: [BEP-XXX](link)
📄 Test Plan: [Confluence link]
```

---

## Other Fields

| Field | Value |
| --- | --- |
| Issue Type | Sub-task |
| Project | BEP |
| Parent | [User Story] |
| Priority | Critical/High/Medium/Low |

---

## Effort Size

| Size | Scope | When |
| --- | --- | --- |
| S | 1-3 scenarios | Simple validation |
| M | 4-6 scenarios | Moderate flow |
| ❌ L/XL | Split | ต้องแตกย่อย |

**Note:** QA test cases should be S or M only. Split larger scopes.

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
- [ ] **Clear objective** - อธิบาย test ชัดเจน
- [ ] **Linked to AC** - map กับ AC ใน Story
- [ ] **Specific steps** - steps ละเอียด reproducible
- [ ] **Expected results** - ผลลัพธ์ชัดเจน verifiable
- [ ] **Test data defined** - ข้อมูล test ระบุครบ
- [ ] **Effort S or M** - ไม่เกิน M

---

_See `references/checklists.md` for QA checklist_
