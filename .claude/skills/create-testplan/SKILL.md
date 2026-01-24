---
name: create-testplan
description: |
  สร้าง Test Plan + [QA] Sub-task จาก User Story ด้วย 6-phase QA workflow

  Phases: Discovery → Test Scope Analysis → Design Test Cases → Create Test Plan Doc → Create [QA] Sub-task → Summary

  Output: Test Plan in Confluence + [QA] Sub-task in Jira

  Triggers: "create test plan", "QA", "test case", "testing"
argument-hint: "[issue-key]"
---

# /create-testplan

**Role:** Senior QA Analyst
**Output:** Test Plan + [QA] Sub-task

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
|----|-------------|----------------|
| 1 | [AC1 desc] | TC1, TC2 |

**Gate:** Coverage matrix approved

### 3. Design Test Cases
- ID, AC coverage, Priority (🔴/🟠/🟡/🟢)
- Type: ✅ Happy / ⚠️ Edge / ❌ Error
- Given/When/Then format
- Test data requirements
- **Gate:** User reviews test coverage

### 4. Create Test Plan Doc
```
MCP: confluence_create_page(
  space_key: "BEP",
  title: "Test Plan: [Story Title]",
  content: [markdown]
)
```
**Output:** Test Plan page URL

### 5. Create [QA] Sub-task
> **หลักการ:** 1 Story = 1 [QA] Sub-task

```bash
acli jira workitem create --from-json tasks/bep-xxx-qa.json
```

**ADF Panel Colors:**
- 🔵 info: objective/summary
- 🟢 success: happy path
- 🟡 warning: edge cases
- 🔴 error: error handling

### 6. Summary
```
## QA Complete: [Title] (BEP-XXX)
Test Plan: [link]
[QA] Sub-task: BEP-QQQ (N scenarios)
→ /verify-issue BEP-QQQ to verify
```

---

## References

- [ADF Templates](../shared-references/templates.md) - QA test case structure
- [Workflows](../shared-references/workflows.md) - Phase patterns, tool selection
- [Verification](../shared-references/verification-checklist.md) - QA checklist
