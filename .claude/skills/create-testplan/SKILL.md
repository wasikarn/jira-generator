---
name: create-testplan
description: |
  สร้าง Test Plan + [QA] Sub-task จาก User Story ด้วย 5-phase QA workflow

  Phases: Discovery → Test Scope Analysis → Design Test Cases → Create [QA] Sub-task → Summary

  Output: [QA] Sub-task in Jira (รวม Test Plan ไว้ใน description)

  Triggers: "create test plan", "QA", "test case", "testing"
argument-hint: "[issue-key]"
---

# /create-testplan

**Role:** Senior QA Analyst
**Output:** [QA] Sub-task (with embedded Test Plan)

> **Note:** Test Plan รวมไว้ใน [QA] Sub-task description แทนการสร้าง Confluence page แยก

## Phases

### 1. Discovery

- `MCP: jira_get_issue(issue_key: "BEP-XXX")`
- `MCP: jira_search(jql: "parent = BEP-XXX")` → Sub-tasks
- อ่าน: Narrative, ACs, Technical Note (ถ้ามี)
- **Gate:** User confirms scope

### 2. Test Scope Analysis

- Map ACs → Test scenarios
- 100% AC coverage required
- Test types: ✅ Happy / ⚠️ Edge / ❌ Error / 📱 UI

| AC | Description | Test Scenarios |
| --- | --- | --- |
| 1 | [AC1 desc] | TC1, TC2 |

**Gate:** Coverage matrix approved

### 3. Design Test Cases

- ID, AC coverage, Priority (🔴/🟠/🟡/🟢)
- Type: ✅ Happy / ⚠️ Edge / ❌ Error
- Given/When/Then format
- Test data requirements
- **Gate:** User reviews test coverage

### 4. Create [QA] Sub-task

> **หลักการ:** 1 Story = 1 [QA] Sub-task (รวม Test Plan ไว้ใน description)

#### Step 1: Create Subtask Shell

```text
MCP: jira_create_issue(
  project_key: "BEP",
  summary: "[QA] - Test: [Feature Name]",
  issue_type: "Subtask",
  additional_fields: {"parent": "BEP-XXX"}
)
```

→ ได้ issue key: BEP-QQQ

#### Step 2: Update with Full Description

1. สร้างไฟล์ `tasks/bep-xxx-qa.json`:

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

> ⚠️ **สำคัญ:** ใช้ `"issues": ["BEP-QQQ"]` ไม่ใช่ `"parent"` หรือ `"parentKey"` หรือ `"parentIssueId"`
> acli edit ต้องการ issues array สำหรับระบุ issue ที่จะแก้ไข

1. Run acli:

```bash
acli jira workitem edit --from-json tasks/bep-xxx-qa.json --yes
```

1. ลบไฟล์ temp:

```bash
rm tasks/bep-xxx-qa.json
```

#### ADF Panel Colors

| Panel Type | Color | Usage |
| --- | --- | --- |
| `info` | 🔵 Blue | Test objective, summary |
| `success` | 🟢 Green | Happy path tests |
| `warning` | 🟡 Yellow | Edge cases, validation |
| `error` | 🔴 Red | Error handling tests |
| `note` | 🟣 Purple | Notes, dependencies |

### 5. Summary

```text
## QA Complete: [Title] (BEP-XXX)

[QA] Sub-task: BEP-QQQ (N scenarios)
Coverage: X ACs → Y test scenarios (100%)

→ /verify-issue BEP-QQQ to verify
```

---

## Common Errors & Fixes

| Error | Cause | Fix |
| --- | --- | --- |
| `json: unknown field "parent"` | ใช้ field ผิดใน JSON | ใช้ MCP สร้างก่อน แล้ว acli edit |
| `json: unknown field "parentKey"` | ใช้ field ผิดใน JSON | ใช้ MCP สร้างก่อน แล้ว acli edit |
| `Could not find issue by id or key` | parentIssueId ไม่ถูกต้อง | ใช้ MCP สร้างก่อน แล้ว acli edit |

**Recommended Workflow:**

1. **Create** ด้วย MCP `jira_create_issue` (รองรับ parent ผ่าน additional_fields)
2. **Edit** ด้วย `acli --from-json` (ใส่ ADF description)

---

## References

- [ADF Core Rules](../shared-references/templates.md) - CREATE/EDIT rules, panels, styling
- [Sub-task Template](../shared-references/templates-subtask.md) - Sub-task + QA ADF structure
- [Verification](../shared-references/verification-checklist.md) - QA checklist
