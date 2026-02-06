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

## Context Object (accumulated across phases)

| Phase | Adds to Context |
|-------|----------------|
| 1. Discovery | `story_data`, `subtask_inventory[]`, `test_scope` |
| 2. Test Scope | `ac_coverage_map[]`, `test_types[]` |
| 3. Design | `test_cases[]`, `coverage_matrix` |
| 4. QG | `qg_score`, `passed_qg` |
| 5. Create | `qa_subtask_key` |

## Gate Levels

| Level | Symbol | Behavior |
| --- | --- | --- |
| **AUTO** | 🟢 | Validate automatically. Pass → proceed. Fail → auto-fix (max 2). Still fail → escalate to user. |
| **REVIEW** | 🟡 | Present results to user, wait for quick confirmation. Default: proceed unless user objects. |
| **APPROVAL** | ⛔ | STOP. Wait for explicit user approval before proceeding. |

> **Note:** Test Plan is embedded in [QA] Sub-task description instead of creating a separate Confluence page

## Phases

> **Phase Tracking:** Use TodoWrite to mark each phase `in_progress` → `completed` as you work.

### 1. Discovery

- `MCP: jira_get_issue(issue_key: "{{PROJECT_KEY}}-XXX")`
- `MCP: jira_search(jql: "parent = {{PROJECT_KEY}}-XXX", fields: "summary,status,assignee,issuetype")` → Sub-tasks (**⚠️ NEVER add ORDER BY to parent queries**)
- Read: Narrative, ACs, Technical Note (if available)
- **⛔ GATE — DO NOT PROCEED** without user confirmation of test scope.

### 2. Test Scope Analysis

- Map ACs → Test scenarios
- 100% AC coverage required
- Test types: ✅ Happy / ⚠️ Edge / ❌ Error / 📱 UI

| AC | Description | Test Scenarios |
| --- | --- | --- |
| 1 | [AC1 desc] | TC1, TC2 |

**🟡 REVIEW** — Present AC coverage matrix to user. Proceed unless user objects.

### 3. Design Test Cases

- ID, AC coverage, Priority (🔴/🟠/🟡/🟢)
- Type: ✅ Happy / ⚠️ Edge / ❌ Error
- Given/When/Then format
- Test data requirements
- **🟡 REVIEW** — Present test cases to user. Proceed unless user objects.

### 4. Quality Gate (MANDATORY)

> **🟢 AUTO** — Score → auto-fix → re-score. Escalate only if still < 90% after 2 attempts.
> HR1: DO NOT create QA subtask in Jira without QG ≥ 90%.

Score against `shared-references/verification-checklist.md`:

1. Score each check with confidence (0-100%). Only report issues with confidence ≥ 80%.
2. Report: `Technical X/5 | QA Quality X/5 | Overall X%`
3. If < 90% → auto-fix → re-score (max 2 attempts)
4. If ≥ 90% → proceed to Phase 5 automatically
5. If still < 90% after 2 fixes → escalate to user
6. Low-confidence items (< 80%) → flag as "needs review" but don't fail QG

### 5. Create [QA] Sub-task

> **🟢 AUTO** — Create → verify parent → edit description. All automated. Escalate only if parent verify fails.
> HR5: Two-Step + Verify Parent.

> **Principle:** 1 Story = 1 [QA] Sub-task (Test Plan embedded in description)
>
> ⚠️ Use **Two-Step Workflow** (see [Templates](../shared-references/templates.md) - Sub-task section):
>
> **Step 1:** MCP `jira_create_issue` → summary: `[QA] - Test: [Feature Name]`, parent: `{{PROJECT_KEY}}-XXX`
> **Step 2:** `acli jira workitem edit --from-json tasks/bep-xxx-qa.json --yes`
>
> ⚠️ EDIT JSON uses `"issues": ["BEP-QQQ"]` (not `"parent"` or `"parentKey"`)

Panel colors: see [ADF Core Rules](../shared-references/templates.md) — success=happy, warning=edge, error=error

> **🟢 AUTO** — HR6: `cache_invalidate(qa_subtask_key)` after create.
> **🟢 AUTO** — HR3: If assignee needed, use `acli jira workitem assign -k "KEY" -a "email" -y` (never MCP).

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
