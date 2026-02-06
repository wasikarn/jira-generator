---
name: create-testplan
description: |
  Create Test Plan + [QA] Sub-task from User Story with a 5-phase QA workflow

  Phases: Discovery → Test Scope Analysis → Design Test Cases → Create [QA] Sub-task → Summary

  Output: [QA] Sub-task in Jira (Test Plan embedded in description)

  Triggers: "create test plan", "QA", "test case", "testing"
argument-hint: "[issue-key]"
---

# /create-testplan

**Role:** Senior QA Analyst
**Output:** [QA] Sub-task (with embedded Test Plan)

> **Note:** Test Plan is embedded in [QA] Sub-task description instead of creating a separate Confluence page

## Phases

### 1. Discovery

- `MCP: jira_get_issue(issue_key: "{{PROJECT_KEY}}-XXX")`
- `MCP: jira_search(jql: "parent = {{PROJECT_KEY}}-XXX", fields: "summary,status,assignee,issuetype")` → Sub-tasks (**⚠️ NEVER add ORDER BY to parent queries**)
- Read: Narrative, ACs, Technical Note (if available)
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

### 4. Quality Gate (MANDATORY)

Before sending to Atlassian, score against `shared-references/verification-checklist.md`:

1. Report: `Technical X/5 | Quality X/6 | Overall X%`
2. If < 90% → auto-fix issues → re-score (max 2 attempts)
3. If >= 90% → proceed to create/edit
4. If still < 90% after fix → ask user before proceeding
5. After Atlassian write → `cache_invalidate(issue_key)` if cache server available

### 5. Create [QA] Sub-task

> **Principle:** 1 Story = 1 [QA] Sub-task (Test Plan embedded in description)
>
> ⚠️ Use **Two-Step Workflow** (see [Templates](../shared-references/templates.md) - Sub-task section):
>
> **Step 1:** MCP `jira_create_issue` → summary: `[QA] - Test: [Feature Name]`, parent: `{{PROJECT_KEY}}-XXX`
> **Step 2:** `acli jira workitem edit --from-json tasks/bep-xxx-qa.json --yes`
>
> ⚠️ EDIT JSON uses `"issues": ["BEP-QQQ"]` (not `"parent"` or `"parentKey"`)

Panel colors: see [ADF Core Rules](../shared-references/templates.md) — success=happy, warning=edge, error=error

### 6. Summary

```text
## QA Complete: [Title] ({{PROJECT_KEY}}-XXX)

[QA] Sub-task: BEP-QQQ (N scenarios)
Coverage: X ACs → Y test scenarios (100%)

→ /verify-issue BEP-QQQ to verify
```

---

## Common Errors & Fixes

| Error | Cause | Fix |
| --- | --- | --- |
| `json: unknown field "parent"` | Wrong field in JSON | Use MCP to create first, then acli edit |
| `json: unknown field "parentKey"` | Wrong field in JSON | Use MCP to create first, then acli edit |
| `Could not find issue by id or key` | Invalid parentIssueId | Use MCP to create first, then acli edit |

**Recommended Workflow:**

1. **Create** with MCP `jira_create_issue` (supports parent via additional_fields)
2. **Edit** with `acli --from-json` (add ADF description)

---

## References

- [ADF Core Rules](../shared-references/templates.md) - CREATE/EDIT rules, panels, styling
- [Templates](../shared-references/templates.md) - ADF templates (Sub-task section)
- [Verification](../shared-references/verification-checklist.md) - QA checklist
