# Jira QA Test Case Template

> **Version:** 2.1 | **Updated:** 2026-01-23

---

## หลักการสำคัญ

> 📌 **1 User Story = 1 [QA] Sub-task**
>
> รวมทุก test scenario ไว้ใน sub-task เดียว

---

## 🎨 ADF Cosmetic Features

| Feature | Usage | Visual |
| :--- | :--- | :---: |
| **Info Panel** | Test objective, coverage summary | 🔵 Blue |
| **Success Panel** | Happy path test cases | 🟢 Green |
| **Warning Panel** | Edge case test cases | 🟡 Yellow |
| **Error Panel** | Error handling test cases | 🔴 Red |
| **Note Panel** | Important notes, dependencies | 🟣 Purple |

> 💡 **Tip:** ใช้ ADF panels เพื่อแยก test case types ด้วยสี ช่วยให้อ่านง่ายขึ้น

---

## Summary Format

```
[QA] - Test: [Story title หรือ feature name]
```

**Tag:** `[QA]` เท่านั้น

**Examples:**
- ✅ `[QA] - Test: หน้าเมนูคูปอง (Coupon Menu)`
- ✅ `[QA] - Test: Credit Transaction History`
- ❌ `[QA] - Test: Display cards` (เจาะจงเกินไป)
- ❌ `Test login` (ไม่มี tag)

---

## Description Template (Copy ไปใช้เลย)

```markdown
## 📖 Story Narrative

> **As a** [persona],
> **I want to** [action],
> **So that** [benefit].

---

## 🎯 Test Objective

[What this test validates - อธิบาย scope ทั้งหมดของ story]

---

## 📊 AC Coverage

| # | Acceptance Criteria | Scenarios | Status |
| :---: | :--- | :---: | :---: |
| 1 | [AC description] | TC1, TC2 | ✅ |
| 2 | [AC description] | TC3 | ✅ |
| 3 | [AC description] | TC4, TC5 | ✅ |

> 📈 **Coverage:** 5 scenarios → 3 ACs (100%)

---

## 🧪 Test Scenarios

| ID | Scenario | AC | Type |
| :---: | :--- | :---: | :---: |
| 🟠 TC1 | [Happy path scenario] | 1 | ✅ Happy |
| 🟡 TC2 | [Alternative path] | 1 | ✅ Happy |
| 🟠 TC3 | [Error scenario] | 2 | ❌ Error |
| 🟡 TC4 | [Edge case] | 3 | ⚠️ Edge |
| 🟢 TC5 | [UI/Responsive] | 3 | 📱 UI |

> **Priority:** 🔴 Critical | 🟠 High | 🟡 Medium | 🟢 Low

---

## 📝 Test Cases

> 💡 **ADF Panel Guide:** ใช้ `success` panel สำหรับ Happy Path, `error` panel สำหรับ Error Cases, `warning` panel สำหรับ Edge Cases

---

### ✅ Happy Path Tests

> **🟢 TC1: [Happy Path Scenario Name]** `[panel: success]`
>
> | | |
> | --- | --- |
> | **AC** | 1 |
> | **Priority** | 🟠 High |
> | **Given** | [preconditions/setup] |
> | **When** | [action steps] |
> | **Then** | [expected result - specific, measurable] |

> **🟢 TC2: [Alternative Happy Path]** `[panel: success]`
>
> | | |
> | --- | --- |
> | **AC** | 1 |
> | **Priority** | 🟡 Medium |
> | **Given** | [preconditions/setup] |
> | **When** | [action steps] |
> | **Then** | [expected result] |

---

### ❌ Error Handling Tests

> **🔴 TC3: [Error Handling Scenario]** `[panel: error]`
>
> | | |
> | --- | --- |
> | **AC** | 2 |
> | **Priority** | 🟠 High |
> | **Given** | [error condition setup] |
> | **When** | [action that triggers error] |
> | **Then** | [error handling response] |

---

### ⚠️ Edge Case Tests

> **🟡 TC4: [Edge Case / Validation]** `[panel: warning]`
>
> | | |
> | --- | --- |
> | **AC** | 3 |
> | **Priority** | 🟡 Medium |
> | **Given** | [boundary/edge condition] |
> | **When** | [action at boundary] |
> | **Then** | [expected boundary behavior] |

---

## 📦 Test Data

| Data | Description | Source |
| :--- | :--- | :---: |
| [Data type] | [What it contains] | 🌱 Seed |
| [Data type] | [What it contains] | 🔧 Manual |
| [Data type] | [What it contains] | 🔌 API |

---

## 💡 Notes

- [Edge case to watch]
- [Dependencies]
- [Environment requirements]

---

## 🔗 Reference

| Type | Link |
| :--- | :--- |
| 📋 User Story | [BEP-XXX](link) |
| 📄 Test Plan | [Confluence URL] |
| 📝 Technical Note | [Confluence URL] |
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

| Size | Icon | Scenarios | Typical Story |
| :---: | :---: | :---: | :--- |
| **S** | 🟢 | 1-3 | Simple story, 1-2 ACs |
| **M** | 🟡 | 4-6 | Moderate story, 3-4 ACs |
| **L** | 🟠 | 7-10 | Complex story, 5+ ACs |

> 💡 **Note:** ไม่ต้อง split - รวมทุก scenario ไว้ใน sub-task เดียว

---

## 🚨 Priority Guide

| Level | Icon | When to Use | Example |
| :--- | :---: | :--- | :--- |
| **Critical** | 🔴 | Core flow, data integrity | Payment, authentication |
| **High** | 🟠 | Primary features | CRUD operations |
| **Medium** | 🟡 | Secondary features | Filters, sorting |
| **Low** | 🟢 | Nice-to-have | UI polish |

---

## 🏷️ Test Type Reference

| Icon | Type | Focus | Example |
| :---: | :--- | :--- | :--- |
| ✅ | Happy | Normal flow succeeds | Login with valid creds |
| ⚠️ | Edge | Boundary/validation | Max 100 items, invalid email |
| ❌ | Error | Failure handled | Network timeout message |
| 🔒 | Security | Access control | Unauthorized returns 403 |
| 📱 | UI | Display/responsive | Mobile layout |

---

## Quality Checklist

Before submit:
- [ ] **1 sub-task per story** - รวมทุก scenario ไว้ใน sub-task เดียว
- [ ] **Clear objective** - อธิบาย test scope ของทั้ง story
- [ ] **AC coverage table** - map ทุก AC กับ scenarios
- [ ] **All scenarios included** - Happy, Error, Edge, UI
- [ ] **Specific steps** - Given/When/Then ละเอียด reproducible
- [ ] **Expected results** - ผลลัพธ์ชัดเจน verifiable
- [ ] **Test data defined** - ข้อมูล test ระบุครบ

---

## Writing Style

- **กระชับ** - test case ชัด reproducible
- **ทับศัพท์** - scenario, expected result, test data
- **เป็นกันเอง** - คุยกับทีม casual

_See `references/shared-config.md` for Language Guidelines_
_See `references/checklists.md` for QA checklist_
