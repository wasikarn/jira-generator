---
name: story-full
context: fork
description: |
  Create User Story + Sub-tasks in one complete workflow (PO + TA combined) with a 10-phase workflow

  Phases: Discovery → Write Story → INVEST → Create Story → Impact → Explore Codebase → Design → Alignment → Create Sub-tasks → Summary

  Composite: No need to copy-paste issue keys, context preserved throughout workflow

  Triggers: "story full", "create story + subtasks", "full workflow"
argument-hint: "[story-description]"
---

# /story-full

**Role:** PO + TA Combined
**Output:** User Story + Sub-tasks (complete workflow)

## Context Object (accumulated across phases)

| Phase | Adds to Context |
|-------|----------------|
| 1. Discovery | `epic_data`, `vs_assignment`, `user_requirements` |
| 2. Write Story | `story_narrative`, `acs[]`, `scope`, `dod` |
| 3. INVEST | `invest_score`, `vs_validated` |
| 3b. QG Story | `story_adf_json`, `story_qg_score` |
| 4. Create Story | `story_key` ({{PROJECT_KEY}}-XXX) |
| 5. Impact | `services_impacted[]`, `vs_verified` |
| 6. Explore | `file_paths[]`, `patterns[]`, `dependencies[]` |
| 7. Design | `subtask_designs[]` |
| 8. Alignment | `alignment_checklist` |
| 9. QG Subtasks | `qg_score`, `passed_qg` |
| 10. Create | `subtask_keys[]` |

## Part A: Create Story (Phases 1-4)

> **Phase Tracking:** Use TodoWrite to mark each phase `in_progress` → `completed` as you work.

### 1. Discovery

- Ask: Who? What? Why? Constraints?
- If Epic exists → `MCP: jira_get_issue(issue_key: "{{PROJECT_KEY}}-XXX")` + read VS plan
- **VS Assignment:** Which vertical slice? (`vs1-skeleton`, `vs2-*`, `vs-enabler`)
- **⛔ GATE — DO NOT PROCEED** without user confirmation of requirements + VS assignment.

### 2. Write User Story

```text
As a [persona],
I want to [action],
So that [benefit].
```

- Define ACs, Scope, DoD
- **VS Check:** Story delivers e2e value? All layers touched? (not shell-only)
- **⛔ GATE — DO NOT PROCEED** without user approval of story narrative, ACs, and VS integrity.

### 3. INVEST + VS Validation

- [ ] **I**ndependent - Not dependent on other stories
- [ ] **N**egotiable - Room for discussion
- [ ] **V**aluable - Clear business value
- [ ] **E**stimable - Can estimate effort
- [ ] **S**mall + **Vertical** - Completable in 1 sprint? **End-to-end slice?**
- [ ] **T**estable - All ACs verifiable in isolation

**VS Anti-pattern Check:**

- ❌ Shell-only (UI ไม่มี logic) → เพิ่ม minimal happy path
- ❌ Layer-split (BE แยกจาก FE) → รวมเป็น story เดียว

**⛔ GATE — If any INVEST criterion fails or VS anti-pattern detected → STOP. Fix before proceeding.**

### 3b. Quality Gate — Story (HR1)

> **⛔ HR1 — DO NOT send Story to Atlassian without QG ≥ 90%.**

1. Generate ADF JSON → `tasks/story.json`
2. Score against `shared-references/verification-checklist.md` (Technical + Story Quality)
3. If < 90% → auto-fix → re-score (max 2 attempts)
4. If ≥ 90% → proceed to Phase 4
5. If still < 90% after 2 fixes → ask user before proceeding

### 4. Create Story in Jira

> **⛔ HR1 — Phase 3b QG must have passed before this step.**

```bash
acli jira workitem create --from-json tasks/story.json
```

**Labels (MANDATORY):** Feature label + VS label (e.g., `coupon-web`, `vs2-collect-e2e`)

**Capture story key → {{PROJECT_KEY}}-XXX**

> **⛔ HR6 — `cache_invalidate(story_key)` after create.**

---

## Part B: Create Sub-tasks (Phases 5-10)

> **Phase Tracking:** Use TodoWrite to mark each phase `in_progress` → `completed` as you work.

### 5. Impact Analysis

| Service | Impact | Reason |
| --- | --- | --- |
| Backend | ✅/❌ | [why] |
| Admin | ✅/❌ | [why] |
| Website | ✅/❌ | [why] |

**VS Verification:** Story touches all layers for e2e slice? (not layer-only)

**⛔ GATE — DO NOT PROCEED** without user confirmation of scope + VS integrity.

### 6. Codebase Exploration ⚠️ MANDATORY

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

**⛔ GATE — If zero real file paths found → DO NOT PROCEED to Phase 7.** Re-explore or ask user. Paths must be real files (verify with Glob). Generic paths like `/src/` are REJECTED.

### 7. Design Sub-tasks

- 1 sub-task per service
- **VS Integrity:** Each subtask contributes to VS completion (not horizontal)
- Summary: `[TAG] - Description`
- Scope: Files from Phase 6
- ACs: Given/When/Then
- **⛔ GATE — DO NOT CREATE** any subtasks without user approval of design + VS alignment.

### 8. Alignment Check

- [ ] Sum of sub-tasks = Complete Story?
- [ ] No gaps? No scope creep?
- [ ] File paths exist?
- [ ] **VS integrity maintained?** (subtasks complete the slice, not horizontal)

### 9. Quality Gate — Subtasks (MANDATORY)

> **⛔ HR1 — DO NOT create subtasks in Jira without QG ≥ 90%. No exceptions.**

Score each subtask ADF against `shared-references/verification-checklist.md`:

1. Score each check with confidence (0-100%). Only report issues with confidence ≥ 80%.
2. Report: `Technical X/5 | Subtask Quality X/5 | Overall X%`
3. If < 90% → auto-fix → re-score (max 2 attempts)
4. If ≥ 90% → proceed to Phase 10
5. If still < 90% after 2 fixes → STOP and ask user
6. Low-confidence items (< 80%) → flag as "needs review" but don't fail QG

### 10. Create Sub-tasks

> **⛔ HR5 — Two-Step + Verify Parent.** acli ไม่รองรับ `parent` field. MCP may silently ignore parent.

**Step 1:** MCP `jira_create_issue` (create shell + parent link) — parallel calls ได้
**Step 2:** Verify parent — `jira_get_issue` each subtask → check `parent.key` = story_key
**Step 3:** `acli --from-json` (update ADF description)

เมื่อ sub-tasks ≥3 ตัว: สร้าง shells ทั้งหมดก่อน → verify all → batch edit descriptions

```text
# Step 1: Create shells (parallel)
MCP: jira_create_issue({project_key: "{{PROJECT_KEY}}", summary:"[BE] - ...", issue_type:"Subtask", additional_fields:{parent:{key:"{{PROJECT_KEY}}-XXX"}}})
MCP: jira_create_issue({project_key: "{{PROJECT_KEY}}", summary:"[FE-Web] - ...", issue_type:"Subtask", additional_fields:{parent:{key:"{{PROJECT_KEY}}-XXX"}}})

# Step 2: Verify parent (HR5) — DO NOT SKIP
MCP: jira_get_issue(issue_key: "BEP-YYY", fields: "parent") → confirm parent.key = "{{PROJECT_KEY}}-XXX"
MCP: jira_get_issue(issue_key: "BEP-ZZZ", fields: "parent") → confirm parent.key = "{{PROJECT_KEY}}-XXX"
# If parent missing → fix via REST API before continuing

# Step 3: Update descriptions
acli jira workitem edit --from-json tasks/subtask-be.json --yes
acli jira workitem edit --from-json tasks/subtask-fe.json --yes
```

> **⛔ HR6 — `cache_invalidate(subtask_key)` after EVERY Atlassian write.**
> **⛔ HR3 — If assignee needed: NEVER use MCP. Use `acli jira workitem assign -k "KEY" -a "email" -y`.**

### 11. Summary

```text
## Story Full Complete
Story: {{PROJECT_KEY}}-XXX
Sub-tasks: BEP-YYY [BE], BEP-ZZZ [FE-Admin]
→ /create-testplan {{PROJECT_KEY}}-XXX for QA
→ /verify-issue {{PROJECT_KEY}}-XXX --with-subtasks
```

---

## Benefits vs Separate Commands

| Approach | Commands | Context |
| --- | --- | --- |
| Separate | `/create-story` + `/analyze-story` | Lost between |
| Combined | `/story-full` | Preserved |

---

## References

- [ADF Core Rules](../shared-references/templates.md) - CREATE/EDIT rules, panels, styling
- [Templates](../shared-references/templates.md) - ADF templates (Story, Sub-task sections)
- [Vertical Slice Guide](../shared-references/vertical-slice-guide.md) - VS patterns, decomposition, labels
- [Verification Checklist](../shared-references/verification-checklist.md) - INVEST, quality checks
