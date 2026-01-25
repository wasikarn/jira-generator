# Jira QA Test Case Template

> **Version:** 2.2 | **Updated:** 2026-01-25

---

## หลักการสำคัญ

> **1 User Story = 1 [QA] Sub-task**
>
> รวมทุก test scenario + Test Plan ไว้ใน sub-task เดียว (ไม่ต้องสร้าง Confluence page แยก)

---

## Creating [QA] Sub-task (2-Step Process)

### Step 1: Create Subtask Shell via MCP

```text
MCP: jira_create_issue(
  project_key: "BEP",
  summary: "[QA] - Test: [Feature Name]",
  issue_type: "Subtask",
  additional_fields: {"parent": "BEP-XXX"}
)
```

→ ได้ issue key: BEP-QQQ

### Step 2: Update with ADF Description via acli

สร้างไฟล์ `tasks/bep-xxx-qa.json`:

```json
{
  "issues": ["BEP-QQQ"],
  "description": {
    "type": "doc",
    "version": 1,
    "content": [...]
  }
}
```

> ⚠️ **สำคัญ:** ใช้ `"issues": ["BEP-QQQ"]` ไม่ใช่ `"parent"`, `"parentKey"`, หรือ `"parentIssueId"`

Run acli:

```bash
acli jira workitem edit --from-json tasks/bep-xxx-qa.json --yes
```

ลบไฟล์ temp:

```bash
rm tasks/bep-xxx-qa.json
```

---

## Common Errors & Fixes

| Error | Cause | Fix |
| --- | --- | --- |
| `json: unknown field "parent"` | ใช้ field ผิดใน JSON | ใช้ MCP สร้างก่อน แล้ว acli edit |
| `json: unknown field "parentKey"` | ใช้ field ผิดใน JSON | ใช้ MCP สร้างก่อน แล้ว acli edit |
| `Could not find issue by id or key` | parentIssueId ไม่ถูกต้อง | ใช้ MCP สร้างก่อน แล้ว acli edit |

---

## ADF Cosmetic Features

| Feature | Usage | Visual |
| --- | --- | --- |
| **Info Panel** | Test objective, coverage summary | 🔵 Blue |
| **Success Panel** | Happy path test cases | 🟢 Green |
| **Warning Panel** | Edge case test cases | 🟡 Yellow |
| **Error Panel** | Error handling test cases | 🔴 Red |
| **Note Panel** | Important notes, dependencies | 🟣 Purple |

**Inline Code Marks:**

| Markdown | ADF Mark |
| --- | --- |
| `` `code` `` | `{"type": "code"}` |
| `**bold**` | `{"type": "strong"}` |

> **Tip:** ใช้ ADF panels เพื่อแยก test case types ด้วยสี ช่วยให้อ่านง่ายขึ้น
>
> _See `.claude/skills/shared-references/templates.md` for full ADF format reference_

---

## Summary Format

```text
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
## 🎯 Test Objective

> [What this test validates - อธิบาย scope ทั้งหมดของ story]
> Flow: [step1 → step2 → step3]
> Total: X Test Scenarios (Y Happy / Z Edge / W Error)

---

## 📊 AC Coverage

| AC | Description | Type | Scenarios |
| --- | --- | --- | --- |
| AC1 | [AC description] | ✅ Happy | TC1, TC2 |
| AC2 | [AC description] | ⚠️ Edge | TC3 |
| AC3 | [AC description] | ❌ Error | TC4, TC5 |

---

## 🧪 Test Cases

### AC1: [AC Title]

> **🟢 TC1: [Happy Path Scenario Name]**
>
> - Priority: 🔴 High | Type: ✅ Happy
> - **Given:** [preconditions/setup]
> - **When:** [action steps]
> - **Then:** [expected result - specific, measurable]

> **🟢 TC2: [Alternative Happy Path]**
>
> - Priority: 🟡 Medium | Type: ✅ Happy
> - **Given:** [preconditions/setup]
> - **When:** [action steps]
> - **Then:** [expected result]

### AC2: [AC Title]

> **🟡 TC3: [Edge Case / Validation]**
>
> - Priority: 🟠 High | Type: ⚠️ Edge
> - **Given:** [boundary/edge condition]
> - **When:** [action at boundary]
> - **Then:** [expected boundary behavior]
> - **Test Data:** `value1`, `value2`, `value3`

### Error Handling

> **🔴 TC4: [Error Handling Scenario]**
>
> - Priority: 🔴 High | Type: ❌ Error
> - **Given:** [error condition setup]
> - **When:** [action that triggers error]
> - **Then:** [error handling response]

---

## 📝 Notes

> **Environment:** Staging
> **Related:** [BEP-XXX](link) (related story/feature)
> **Figma:** [Design Link](url)

---

## 🔗 Reference

| Type | Link |
| --- | --- |
| User Story | [BEP-XXX](link) |
| Backend | [BEP-YYY](link) |
| Frontend | [BEP-ZZZ](link) |
```

---

## Other Fields

| Field | Value |
| --- | --- |
| **Issue Type** | Subtask |
| **Project** | BEP |
| **Parent** | [User Story] |
| **Priority** | [See guide below] |

---

## Effort Size

| Size | Icon | Scenarios | Typical Story |
| --- | --- | --- | --- |
| **S** | 🟢 | 1-3 | Simple story, 1-2 ACs |
| **M** | 🟡 | 4-6 | Moderate story, 3-4 ACs |
| **L** | 🟠 | 7-10 | Complex story, 5+ ACs |

> **Note:** ไม่ต้อง split - รวมทุก scenario ไว้ใน sub-task เดียว

---

## Priority Guide

| Level | Icon | When to Use | Example |
| --- | --- | --- | --- |
| **Critical** | 🔴 | Core flow, data integrity | Payment, authentication |
| **High** | 🟠 | Primary features | CRUD operations |
| **Medium** | 🟡 | Secondary features | Filters, sorting |
| **Low** | 🟢 | Nice-to-have | UI polish |

---

## Test Type Reference

| Icon | Type | Focus | Example |
| --- | --- | --- | --- |
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
- [ ] **Panel colors correct** - success=happy, warning=edge, error=error

---

## Writing Style

- **กระชับ** - test case ชัด reproducible
- **ทับศัพท์** - scenario, expected result, test data
- **เป็นกันเอง** - คุยกับทีม casual

_See `.claude/skills/shared-references/templates.md` for ADF format_
_See `references/checklists.md` for QA checklist_
