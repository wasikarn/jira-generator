---
name: update-epic
disable-model-invocation: true
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

## Context Object (accumulated across phases)

| Phase | Adds to Context |
|-------|----------------|
| 1. Fetch | `epic_data`, `child_stories[]`, `epic_doc` |
| 2. Impact | `change_type`, `impact_level` |
| 3. Preserve | `preservation_rules` |
| 4. Generate | `update_adf_json` |
| 5. QG | `qg_score`, `passed_qg` |
| 6. Apply | `applied` |

> **Workflow Patterns:** See [workflow-patterns.md](../shared-references/workflow-patterns.md) for Gate Levels (AUTO/REVIEW/APPROVAL), QG Scoring, Two-Step, and Explore patterns.

## Phases

> **Phase Tracking:** Use TodoWrite to mark each phase `in_progress` → `completed` as you work.

### 1. Fetch Current State

- `MCP: jira_get_issue(issue_key: "{{PROJECT_KEY}}-XXX")`
- `MCP: jira_search(jql: "parent = {{PROJECT_KEY}}-XXX OR 'Epic Link' = {{PROJECT_KEY}}-XXX", fields: "summary,status,assignee,issuetype,priority")` (**⚠️ NEVER add ORDER BY to parent queries**)
- `MCP: confluence_search(query: "Epic: [title]")`
- Read: RICE, objectives, success metrics, child stories
- **🟡 REVIEW** — Present current state to user. Proceed unless user objects.

### 2. Impact Analysis

| Change Type | Impact on Stories | Impact on Planning |
| --- | --- | --- |
| Add scope | Need to create new stories | Re-estimate |
| Remove scope | Need to close stories | Timeline shorter |
| RICE update | ❌ No impact | May reprioritize |
| Format only | ❌ No impact | ❌ No impact |

**⛔ GATE — DO NOT PROCEED** without user confirmation of changes.

### 3. Preserve Intent

- ✅ Adjusting wording/clarifying is allowed
- ✅ Updating RICE is allowed
- ✅ Adding success metrics is allowed
- ⚠️ Be careful changing scope (affects stories)
- ❌ Do not change core business value without informing

### 4. Generate Update

- Generate ADF JSON → `tasks/bep-xxx-epic-update.json`
- Show comparison: Before/After for RICE, objectives, scope
- **⛔ GATE — DO NOT APPLY** without user approval of all generated changes.

### 5. Quality Gate (MANDATORY)

> **🟢 AUTO** — Score → auto-fix → re-score. Escalate only if still < 90% after 2 attempts.
> HR1: DO NOT send updates to Atlassian without QG ≥ 90%.

> [QG Scoring Rules](../shared-references/workflow-patterns.md#quality-gate-scoring). Report: `Technical X/5 | Quality X/6 | Overall X%`

### 6. Apply Update

> **🟢 AUTO** — If QG passed → apply automatically. No user interaction needed.

```bash
acli jira workitem edit --from-json tasks/bep-xxx-epic-update.json --yes
```

> **🟢 AUTO** — HR6: `cache_invalidate(issue_key)` after apply.

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
| 🎯 Epic Overview | `info` | Problem statement + summary + scope statement |
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

- [ADF Core Rules](../shared-references/templates-core.md) - CREATE/EDIT rules, panels, styling
- [Epic Template](../shared-references/templates-epic.md) - Epic ADF template + best practices
- [Tool Selection](../shared-references/tools.md) - Tool selection
