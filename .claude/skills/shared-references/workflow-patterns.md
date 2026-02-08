# Workflow Patterns (Shared Reference)

> Referenced by SKILL.md files — single source of truth for common workflow patterns.

---

## Gate Levels

| Level | Symbol | Behavior |
| --- | --- | --- |
| **AUTO** | 🟢 | Validate automatically. Pass → proceed. Fail → auto-fix (max 2). Still fail → escalate to user. |
| **REVIEW** | 🟡 | Present results to user, wait for quick confirmation. Default: proceed unless user objects. |
| **APPROVAL** | ⛔ | STOP. Wait for explicit user approval before proceeding. |

---

## Phase Tracking

> **Phase Tracking:** Use TodoWrite to mark each phase `in_progress` → `completed` as you work.

---

## Quality Gate Scoring

> HR1: NEVER create/edit issues on Jira/Confluence before QG ≥ 90%.

Score against `verification-checklist.md`:

1. Score each check with confidence (0-100%). Only report issues with confidence ≥ 80%.
2. Report: `Technical X/5 | [Domain] Quality X/N | Overall X%`
3. If < 90% → auto-fix → re-score (max 2 attempts)
4. If ≥ 90% → proceed to next phase automatically
5. If still < 90% after 2 fixes → escalate to user
6. Low-confidence items (< 80%) → flag as "needs review" but don't fail QG

### Report Format by Type

| Skill Type | Report Format |
|-----------|-------------|
| Epic | `Technical X/5 \| Epic Quality X/4 \| Overall X%` |
| Story | `Technical X/5 \| Story Quality X/6 \| Overall X%` |
| Subtask | `Technical X/5 \| Subtask Quality X/5 \| Overall X%` |
| Task | `Technical X/5 \| Quality X/6 \| Overall X%` |
| QA | `Technical X/5 \| QA Quality X/5 \| Overall X%` |

---

## Two-Step Subtask Creation

> HR5: MCP `jira_create_issue` may silently ignore parent field → orphan subtask.

**Step 1:** MCP `jira_create_issue` (create shell + parent link) — parallel calls OK

```text
MCP: jira_create_issue({
  project_key: "{{PROJECT_KEY}}",
  summary: "[TAG] - Description",
  issue_type: "Subtask",
  additional_fields: {parent: {key: "{{PROJECT_KEY}}-XXX"}}
})
```

**Step 2:** Verify parent — `jira_get_issue(issue_key, fields: "parent")` → confirm `parent.key`

- If parent missing → fix via REST API or re-create

**Step 3:** `acli jira workitem edit --from-json tasks/subtask-xxx.json --yes`

**Batch (≥3 subtasks):** Create all shells → verify all parents → batch edit descriptions

---

## Parallel Explore

> MANDATORY before creating subtasks — ensures real file paths, not generic guesses.

Launch 2-3 Explore agents **IN PARALLEL** (single message, multiple Task calls):

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

**Validation:** Validate file paths with Glob. If zero real paths found → re-explore (max 2 attempts). Generic paths like `/src/` are REJECTED.

**Conditional:** Skip if format-only changes (no new scope).

---

## HR Quick Reference

| HR | Rule | Enforcement |
|----|------|-------------|
| HR1 | QG ≥ 90% before Atlassian writes | Hook: `hr1-qg-before-write.py` |
| HR3 | Assignee via `acli` only (never MCP) | Hook: `hr3-block-mcp-assignee.py` |
| HR5 | Two-Step + Verify Parent | Hook: `hr5-verify-parent-reminder.py` |
| HR6 | `cache_invalidate(key)` after every write | Hook: `hr6-cache-invalidate.py` |
| HR7 | Sprint ID lookup, never hardcode | Hook: `hr7-sprint-id-guard.py` |
