# Jira Sub-task Template

> **Version:** 4.1 | **Updated:** 2026-01-23

---

## 🎨 ADF Cosmetic Features

| Feature | Usage | Visual |
| :--- | :--- | :---: |
| **Info Panel** | Story narrative, objective | 🔵 Blue |
| **Success Panel** | Happy path AC | 🟢 Green |
| **Warning Panel** | Validation AC | 🟡 Yellow |
| **Error Panel** | Error handling AC | 🔴 Red |
| **Note Panel** | Important notes, references | 🟣 Purple |

**Inline Code Marks:**

| Markdown | ADF Mark |
| :--- | :--- |
| `` `code` `` | `{"type": "code"}` |
| `**bold**` | `{"type": "strong"}` |

> 💡 **Tip:** ใช้ ADF panels เพื่อแยก AC types ด้วยสี ช่วยให้ Developer อ่านง่ายขึ้น
>
> _See `references/templates.md` for full ADF format reference_

---

## Summary Format

```
[SERVICE_TAG] - Brief description
```

**Tags:** `[BE]` | `[FE-Admin]` | `[FE-Web]`

**Examples:**
- ✅ `[BE] - เพิ่ม API filter products ตาม category`
- ✅ `[FE-Admin] - สร้างหน้า Credit Transaction History`
- ❌ `Backend task` (ไม่มี tag)
- ❌ `[BE] - ทำ API` (ไม่ชัดเจน)

---

## Description Template (Copy ไปใช้เลย)

```markdown
## 📖 Story Narrative

> **As a** [persona],
> **I want to** [action],
> **So that** [benefit].

---

## 🎯 Objective

[What and why - 1-2 ประโยค กระชับ ชัดเจน]

---

## 📁 Scope

| Category | Details |
| :--- | :--- |
| **Files** | `path/to/file1.ts`, `path/to/file2.ts` |
| **Dependencies** | [Related components/services] |
| **Database** | [Tables affected, if any] |

---

## 📋 Requirements

- [Requirement 1 - what, not how]
- [Requirement 2 - what, not how]
- [Requirement 3 - what, not how]

---

## ✅ Acceptance Criteria

> 💡 **ADF Panel Guide:** ใช้ `success` panel สำหรับ Happy Path, `warning` panel สำหรับ Validation, `error` panel สำหรับ Error Handling

---

> **🟢 AC1: [Happy Path]** `[panel: success]`
>
> | | |
> | --- | --- |
> | **Given** | [precondition] |
> | **When** | [action/API call] |
> | **Then** | [expected response/behavior] |

> **🟡 AC2: [Validation]** `[panel: warning]`
>
> | | |
> | --- | --- |
> | **Given** | [invalid input] |
> | **When** | [action/API call] |
> | **Then** | [validation error/response] |

> **🔴 AC3: [Error Handling]** `[panel: error]`
>
> | | |
> | --- | --- |
> | **Given** | [error condition] |
> | **When** | [action/API call] |
> | **Then** | [error response/status code] |

---

## 💡 Notes

- [Edge case to handle]
- [Pattern to follow from existing code]
- [Performance consideration]

---

## 🔗 Reference

| Type | Link |
| :--- | :--- |
| 📄 User Story | [BEP-XXX](link) |
| 📝 Technical Doc | [Confluence URL] |
| 🎨 Design | [Figma URL] |
```

---

## Other Fields

| Field | Value |
| :--- | :---: |
| **Issue Type** | Subtask |
| **Project** | BEP |
| **Parent** | [User Story] |
| **Priority** | [See guide below] |

---

## ⏱️ Effort Size

| Size | Icon | Duration | When to Use |
| :---: | :---: | :---: | :--- |
| **S** | 🟢 | 0.5-1 day | Simple, 1 component, clear scope |
| **M** | 🟡 | 1-2 days | Multi-component, some complexity |
| **L** | 🟠 | 2-3 days | Complex logic, integration needed |
| **XL** | 🔴 | > 3 days | ❌ ต้องแตกย่อย |

---

## 🚨 Priority Guide

| Level | Icon | When to Use |
| :--- | :---: | :--- |
| **Critical** | 🔴 | Security fix, blocker, data loss risk |
| **High** | 🟠 | Core functionality, deadline |
| **Medium** | 🟡 | Standard development work |
| **Low** | 🟢 | Nice-to-have, improvements |

---

## Quality Checklist

Before submit:
- [ ] **กระชับ** - Developer อ่านเข้าใจใน 30 วินาที
- [ ] **ชัดเจน** - ไม่คลุมเครือ, scope ชัด
- [ ] **ถูกต้อง** - File paths ตรงกับ codebase จริง
- [ ] **Testable** - ทุก AC verify ได้
- [ ] **Right size** - S/M/L (ไม่ใช่ XL)

---

## 📝 Note

> **ไม่ต้องสร้าง Confluence doc** สำหรับ sub-tasks ส่วนใหญ่
>
> Technical details อยู่ใน User Story Doc แล้ว

---

## Writing Style

- **กระชับ** - dev อ่านเข้าใจใน 30 วินาที
- **ทับศัพท์** - endpoint, payload, validate, component
- **เป็นกันเอง** - คุยกับทีม casual

_See `references/shared-config.md` for Language Guidelines_
_See `references/checklists.md` for INVEST criteria_
