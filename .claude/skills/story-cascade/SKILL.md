---
name: story-cascade
context: fork
description: |
  Update Story + cascade changes to related Sub-tasks with a 9-phase workflow

  Phases: Fetch → Understand Changes → Impact Analysis → Explore (if needed) → Generate Story Update → Generate Sub-task Updates → Quality Gate → Apply All → Summary

  Composite: Automatic impact analysis, update everything in a single transaction

  Triggers: "story cascade", "update all", "cascade changes"
argument-hint: "[issue-key] [changes]"
---

# /story-cascade

**Role:** PO + TA Combined
**Output:** Updated Story + Updated/New Sub-tasks

## Context Object (accumulated across phases)

| Phase | Adds to Context |
|-------|----------------|
| 1. Fetch | `story_data`, `subtask_inventory[]`, `current_state` |
| 2. Understand | `change_type`, `impact_level` |
| 3. Impact | `impact_map[]`, `cascade_plan` |
| 4. Explore | `file_paths[]`, `patterns[]` (conditional) |
| 5. Story Update | `story_adf_json` |
| 6. Subtask Updates | `subtask_adf_jsons[]` |
| 7. QG | `qg_score`, `passed_qg` |
| 8. Apply | `applied_keys[]` |

## Gate Levels

| Level | Symbol | Behavior |
| --- | --- | --- |
| **AUTO** | 🟢 | Validate automatically. Pass → proceed. Fail → auto-fix (max 2). Still fail → escalate to user. |
| **REVIEW** | 🟡 | Present results to user, wait for quick confirmation. Default: proceed unless user objects. |
| **APPROVAL** | ⛔ | STOP. Wait for explicit user approval before proceeding. |

## Phases

> **Phase Tracking:** Use TodoWrite to mark each phase `in_progress` → `completed` as you work.

### 1. Fetch Current State

- `MCP: jira_get_issue(issue_key: "{{PROJECT_KEY}}-XXX")`
- `MCP: jira_search(jql: "parent = {{PROJECT_KEY}}-XXX", fields: "summary,status,assignee,issuetype")` (**⚠️ NEVER add ORDER BY to parent queries**)
- Build inventory: Story + all Sub-tasks
- **🟡 REVIEW** — Present inventory summary to user. Proceed unless user objects.

### 2. Understand Changes

| Change Type | Impact Level |
| --- | --- |
| Format only | 🟢 Low |
| Clarify AC | 🟢 Low |
| Add AC | 🟡 Medium |
| Modify AC | 🟡 Medium |
| Remove AC | 🔴 High |
| Change Scope | 🔴 High |

**⛔ GATE — DO NOT PROCEED** without user confirmation of change type + impact level.

### 3. Impact Analysis

| AC | Related Sub-tasks | Impact |
| --- | --- | --- |
| AC1 | BEP-YYY | ❌ No change |
| AC2 | BEP-YYY, BEP-ZZZ | ✏️ Must update |
| AC3 (new) | - | ➕ Need new |

**🟡 REVIEW** — Present impact table + cascade plan to user. Proceed unless user objects.

### 4. Codebase Exploration (if needed)

> **🟢 AUTO** — Run only if scope changed or new sub-task needed. Skip if format-only. Validate paths with Glob.

- Run only if: New sub-task needed OR scope changed
- Launch 2-3 Explore agents **IN PARALLEL** (single message, multiple Task calls):

```text
# Agent 1: Backend (models, controllers, routes, services)
Task(subagent_type: "Explore", prompt: "Find [feature] in backend: models, controllers, routes, services")

# Agent 2: Frontend (pages, components, hooks, stores)
Task(subagent_type: "Explore", prompt: "Find [feature] in frontend: pages, components, hooks")

# Agent 3 (if needed): Shared/infra (config, middleware, types, utils)
Task(subagent_type: "Explore", prompt: "Find [feature] in shared: config, middleware, types")
```

Each agent returns: `file_paths[]`, `patterns[]`, `dependencies[]`
Merge results into context.

- Skip if format-only changes
- Validate file paths with Glob. Generic paths like `/src/` are REJECTED.

### 5. Generate Story Update

> **🟢 AUTO** — Generate automatically from change analysis. No user interaction needed.

- Apply changes: narrative, ACs, scope
- Generate ADF JSON → `tasks/bep-xxx-update.json`
- Show comparison table

### 6. Generate Sub-task Updates

- Preserve original intent
- Update ACs to align
- New sub-tasks: follow template
- Generate JSON files
- **⛔ GATE — DO NOT APPLY** any updates without user approval of all generated changes.

### 7. Quality Gate (MANDATORY)

> **🟢 AUTO** — Score → auto-fix → re-score. Escalate only if still < 90% after 2 attempts.
> HR1: DO NOT send updates to Atlassian without QG ≥ 90%.

Score against `shared-references/verification-checklist.md`:

1. Score each check with confidence (0-100%). Only report issues with confidence ≥ 80%.
2. Report: `Technical X/5 | Quality X/6 | Overall X%`
3. If < 90% → auto-fix → re-score (max 2 attempts)
4. If ≥ 90% → proceed to Phase 8 automatically
5. If still < 90% after 2 fixes → escalate to user
6. Low-confidence items (< 80%) → flag as "needs review" but don't fail QG

### 8. Apply All Updates

> **🟢 AUTO** — If QG passed → apply all automatically. Escalate only if parent verify fails.
> HR5: New subtasks must use Two-Step + Verify Parent.

```bash
# Story first
acli jira workitem edit --from-json tasks/bep-xxx-update.json --yes
# Then sub-tasks
acli jira workitem edit --from-json tasks/bep-yyy-update.json --yes
# New sub-tasks: Two-Step (MCP create shell → verify parent → acli edit)
```

> **🟢 AUTO** — HR6: `cache_invalidate(issue_key)` after EVERY Atlassian write.
> **🟢 AUTO** — HR3: If assignee needed, use `acli jira workitem assign -k "KEY" -a "email" -y` (never MCP).

### 9. Cleanup & Summary

```bash
rm tasks/bep-*-update.json tasks/new-*.json
```

```text
## Cascade Complete
Story: {{PROJECT_KEY}}-XXX (AC2 modified, AC3 added)
Updated: BEP-YYY, BEP-ZZZ
Created: BEP-NEW
→ Review QA sub-task if needed
```

---

## Cascade vs Separate

| Approach | Commands | Issues |
| --- | --- | --- |
| Separate | `/update-story` + N × `/update-subtask` | Lost context |
| Cascade | `/story-cascade {{PROJECT_KEY}}-XXX` | Auto impact |

---

## References

- [ADF Core Rules](../shared-references/templates.md) - CREATE/EDIT rules, panels, styling
- [Templates](../shared-references/templates.md) - ADF templates (Story, Sub-task sections)
- [Tool Selection](../shared-references/tools.md) - Tool selection
