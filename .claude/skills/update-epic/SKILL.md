---
name: update-epic
description: |
  Update an existing Epic with a 6-phase update workflow

  Phases: Fetch Current → Impact Analysis → Preserve Intent → Generate Update → Quality Gate → Apply Update

  Supports: adjust scope, update RICE, add success metrics, format migration

  Triggers: "update epic", "edit epic", "adjust epic"
argument-hint: "[issue-key] [changes]"
---

# /update-epic

**Role:** Senior Product Manager
**Output:** Updated Epic

## Phases

### 1. Fetch Current State

- `MCP: jira_get_issue(issue_key: "{{PROJECT_KEY}}-XXX")`
- `MCP: jira_search(jql: "parent = {{PROJECT_KEY}}-XXX OR 'Epic Link' = {{PROJECT_KEY}}-XXX", fields: "summary,status,assignee,issuetype,priority")` (**⚠️ NEVER add ORDER BY to parent queries**)
- `MCP: confluence_search(query: "Epic: [title]")`
- Read: RICE, objectives, success metrics, child stories
- **Gate:** User confirms what to update

### 2. Impact Analysis

| Change Type | Impact on Stories | Impact on Planning |
| --- | --- | --- |
| Add scope | Need to create new stories | Re-estimate |
| Remove scope | Need to close stories | Timeline shorter |
| RICE update | ❌ No impact | May reprioritize |
| Format only | ❌ No impact | ❌ No impact |

**Gate:** User acknowledges impact

### 3. Preserve Intent

- ✅ Adjusting wording/clarifying is allowed
- ✅ Updating RICE is allowed
- ✅ Adding success metrics is allowed
- ⚠️ Be careful changing scope (affects stories)
- ❌ Do not change core business value without informing

### 4. Generate Update

- Generate ADF JSON → `tasks/bep-xxx-epic-update.json`
- Show comparison: Before/After for RICE, objectives, scope
- **Gate:** User approves changes

### 5. Quality Gate (MANDATORY)

Before sending to Atlassian, score against `shared-references/verification-checklist.md`:

1. Report: `Technical X/5 | Quality X/6 | Overall X%`
2. If < 90% → auto-fix issues → re-score (max 2 attempts)
3. If >= 90% → proceed to create/edit
4. If still < 90% after fix → ask user before proceeding
5. After Atlassian write → `cache_invalidate(issue_key)` if cache server available

### 6. Apply Update

```bash
acli jira workitem edit --from-json tasks/bep-xxx-epic-update.json --yes
```

**Output:**

```text
## Epic Updated: [Title] ({{PROJECT_KEY}}-XXX)
Changes: [list]
→ Update Epic Doc if needed
→ Review stories: BEP-YYY, BEP-ZZZ
```

---

## Common Scenarios

| Scenario | Command | Impact |
| --- | --- | --- |
| Adjust scope | `/update-epic {{PROJECT_KEY}}-XXX "reduce scope"` | ⚠️ High |
| Update RICE | `/update-epic {{PROJECT_KEY}}-XXX "RICE update"` | 🟢 Low |
| Add metrics | `/update-epic {{PROJECT_KEY}}-XXX "add metric"` | 🟢 Low |
| Format migrate | `/update-epic {{PROJECT_KEY}}-XXX "migrate ADF"` | 🟢 Low |

---

## Epic Structure (ADF)

| Section | Panel Type | Content |
| --- | --- | --- |
| 🎯 Epic Overview | `info` | Summary + scope statement |
| 💰 Business Value | `success` | Revenue, Retention, Operations |
| 📦 Scope | `info` + table | Features/modules breakdown |
| 📊 RICE Score | table | R/I/C/E + final score |
| 🎯 Success Metrics | table | KPIs + targets |
| 📋 User Stories | `info` panels | Grouped by feature area |
| 📈 Progress | `note` | Done/In Progress/To Do counts |
| 🔗 Links | table | Epic Doc, Technical Notes |

**ADF restrictions:**

- ❌ Do not nest tables inside panels (will cause an error)
- ✅ Use paragraphs or bulletList inside panels instead

---

## References

- [ADF Core Rules](../shared-references/templates.md) - CREATE/EDIT rules, panels, styling
- [Templates](../shared-references/templates.md) - ADF templates (Epic section)
- [Tool Selection](../shared-references/tools.md) - Tool selection
