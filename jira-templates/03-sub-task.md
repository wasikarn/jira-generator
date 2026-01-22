# Jira Sub-task Template

> **Version:** 3.0 | **Updated:** 2025-01-22

---

## Summary Format

```
[SERVICE_TAG] - Brief description
```

**Tags:** `[BE]`, `[FE-Admin]`, `[FE-Web]`

**Examples:**
- ✅ `[BE] - เพิ่ม API filter products ตาม category`
- ✅ `[FE-Web] - เพิ่ม category dropdown`
- ❌ `Backend task` (ไม่มี tag)

---

## Description Template (Copy ไปใช้เลย)

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

## Other Fields

| Field | Value |
| --- | --- |
| Issue Type | Sub-task |
| Project | BEP |
| Parent | [User Story] |
| Priority | Critical/High/Medium/Low |

---

## Effort Size

| Size | Duration | When |
| --- | --- | --- |
| S | 0.5-1 day | Simple, 1 component |
| M | 1-2 days | Multi-component |
| L | 2-3 days | Complex, integration |
| XL | ❌ Split | ต้องแตกย่อย |

---

## Priority Guide

| Priority | When |
| --- | --- |
| 🔴 Critical | Security, blocking, data loss |
| 🟠 High | Core functionality |
| 🟡 Medium | Improvements |
| 🟢 Low | Nice-to-have |

---

## Quality Check

Before submit:
- [ ] **กระชับ** - อ่านเข้าใจใน 30 วินาที
- [ ] **ชัดเจน** - ไม่คลุมเครือ
- [ ] **ครบถ้วน** - Developer เข้าใจ scope
- [ ] **ถูกต้อง** - File paths ตรง codebase
- [ ] **Testable** - ทุก AC verify ได้

---

## Note

**ไม่ต้องสร้าง Confluence doc** สำหรับ sub-tasks ส่วนใหญ่

Technical details อยู่ใน User Story Doc แล้ว

---

_See `references/checklists.md` for INVEST criteria_
