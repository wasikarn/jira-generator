---
name: analyze-story
disable-model-invocation: true
context: fork
description: |
  Analyze User Story and create Sub-tasks + Technical Note with a 7-phase TA workflow
  MANDATORY: Must explore codebase before creating Sub-tasks
argument-hint: "[issue-key]"
---

# /analyze-story

**Role:** Senior Technical Analyst
**Output:** Sub-tasks + Technical Note

## Dynamic Context

- **Today:** !`date +%Y-%m-%d`

## Context Object (accumulated across phases)

| Phase | Adds to Context |
|-------|----------------|
| 1. Discovery | `story_data`, `epic_context`, `vs_assignment` |
| 2. Impact | `services_impacted[]`, `vs_verified` |
| 3. Explore | `file_paths[]`, `patterns[]`, `dependencies[]` |
| 4. Design | `subtask_designs[]` |
| 5. Alignment | `alignment_checklist` |
| 5b. QG | `qg_score`, `passed_qg` |
| 6. Create | `subtask_keys[]` |

> **Workflow Patterns:** See [workflow-patterns.md](../shared-references/workflow-patterns.md) for Gate Levels (AUTO/REVIEW/ITERATE/APPROVAL), QG Scoring, Two-Step, and Explore patterns.

## Phases

> **Phase Tracking:** Use TodoWrite to mark each phase `in_progress` → `completed` as you work.

### 1. Discovery

- `MCP: jira_get_issue(issue_key: "{{PROJECT_KEY}}-XXX")`
- Read: Narrative, ACs, Links, Epic context
- **⛔ GATE — DO NOT PROCEED** without user confirmation of story understanding.

### 2. Impact Analysis

| Service | Impact | Reason |
| --- | --- | --- |
| Backend | ✅/❌ | [why] |
| Admin | ✅/❌ | [why] |
| Website | ✅/❌ | [why] |

**⚡ Event Flow (optional — include for complex domains):**

| Command | Event Emitted | Consumer(s) | Side Effect |
| --- | --- | --- | --- |
| [user action] | [DomainEvent] | [service/policy] | [state change] |

> Use when story has cross-service event flow or policy trigger — helps Phase 4 subtask design be more accurate

**VS Verification:** Story touches all layers for e2e slice? (not layer-only)

**🟡 REVIEW** — Present impact table + VS verification to user. Proceed unless user objects.

### 3. Codebase Exploration ⚠️ MANDATORY

> [Parallel Explore](../shared-references/workflow-patterns.md#parallel-explore): Launch 2-3 agents (Backend/Frontend/Shared) IN PARALLEL.
> Validate paths with Glob. Generic paths REJECTED. Re-explore max 2 attempts.

**What each agent MUST discover:**

| Agent | Must Find |
|-------|-----------|
| Backend | Models/Migrations path, Controllers pattern, Routes file, Config enums (any enum to extend?), Auth middleware on similar routes, Existing similar implementation as REF |
| Frontend | Page dir structure, Service base pattern (`ApiBaseService`?), OAuth/auth lib, Shared UI components (dialogs, icons, layouts) with exact filenames |
| Shared/Config | `.env` variables consumed by feature, Types/interfaces, Error handling patterns |

**Critical validation:**

- Validate every filename with Glob — don't assume (typos exist in real codebases, e.g., `account-layoyt.component.tsx`)
- Config enums that need new values → include as MODIFY in scope
- Auth middleware: which routes require `auth:publicApi`? Which are public?
- Find at least 1 REF pattern per subtask to guide developer

### 4. Design Sub-tasks

**Tech Lead Decomposition — dependency ordering:**

```
1. Data layer (migration + model)   ← foundation, blocks everything
2. Auth/OAuth (if new auth flow)    ← must exist before API validates identity
3. Backend API (endpoints + routes) ← FE service contract depends on this
4. Backend service/channel          ← business logic, depends on model
5. FE service layer                 ← depends on BE API contract
6. FE component/page                ← depends on FE service
7. FE interactions/events           ← depends on FE component + FE service
```

**Scope table format per subtask** (single Action | File table):

- `CREATE` — new file to create from scratch
- `MODIFY` — existing file to add/change code
- `REF` — existing file developer reads as pattern guide (no changes — just follow the pattern)
- **Minimum 1 REF row per subtask** — never leave developer without a pattern reference

**AC specificity requirements (Tech Lead level):**

- Reference actual method names from Phase 3: `LineAuthStrategy.handleCallback()`
- Specify exact HTTP endpoints + status codes: `POST /v2/notification/line-accounts → 201 or 409`
- Specify data contracts: `{ line_uid, display_name, avatar_url, access_token }`
- Specify error UI: toast color + exact error message text
- Specify env vars if consumed by new code: `LINE_MESSAGING_API_CHANNEL_ACCESS_TOKEN`

**Config/enum awareness:**

- New feature type → check if config enum needs a new value (add as MODIFY to scope)
- New unique constraint → specify explicitly in migration AC
- Middleware → document which middleware applies to each new route in AC

- 1 sub-task per service boundary (split only if complexity warrants)
- **VS Integrity:** Each subtask contributes to VS completion (not horizontal layer)
- Summary: `[TAG] - Description`
- ACs: Thai narrative + English technical terms

- **🔄 ITERATE** — Present subtask design as plan cards (tag, scope files, ACs, OE per subtask). Ask: Approve all / Annotate (specify subtask #) / Major rework.
  - Annotate → user specifies subtask + notes → revise ONLY annotated subtasks → re-present (max 3 rounds)
  - Approve → proceed to Alignment Check
  - Major rework → back to Codebase Exploration
  - See [Annotation Cycle](../shared-references/workflow-patterns.md#annotation-cycle-iterate-gate)

### 5. Alignment Check

> **🟢 AUTO** — Verify programmatically. Auto-fix misalignment. Escalate only if unfixable.

- [ ] Sum of sub-tasks = Complete Story?
- [ ] No gaps? No scope creep?
- [ ] File paths exist? (validate with Glob)
- [ ] **VS integrity maintained?** (subtasks complete the slice, not horizontal split)

If any check fails → auto-adjust subtask scope/design → re-check. Escalate to user only if gap cannot be resolved automatically.

### 5b. Quality Gate — Subtasks (MANDATORY)

> **🟢 AUTO** — Score → auto-fix → re-score. Escalate only if still < 90% after 2 attempts.
> HR1: DO NOT create subtasks in Jira without QG ≥ 90%.

> [QG Scoring Rules](../shared-references/workflow-patterns.md#quality-gate-scoring). Report: `Technical X/5 | Subtask Quality X/5 | Overall X%`

### 6. Create Artifacts

> **🟢 AUTO** — Create → verify parent → edit descriptions. All automated. Escalate only if parent verify fails after retry.
> HR5: Two-Step + Verify Parent. acli does not support the `parent` field. MCP may silently ignore parent.

> [Two-Step Subtask](../shared-references/workflow-patterns.md#two-step-subtask-creation): MCP create shell → verify parent → acli edit. Batch ≥3: create all → verify all → edit all.

> **🟢 AUTO** — HR6: `cache_invalidate(subtask_key)` after EVERY Atlassian write.
> **🟢 AUTO** — HR3: If assignee needed, use `acli jira workitem assign -k "KEY" -a "email" -y` (never MCP).

**Set subtask estimation (after verify parent, before acli edit):**

```text
MCP: jira_update_issue(issue_key="BEP-YYY", additional_fields={
  "timetracking": {"originalEstimate": "<N>h"},  # Original Estimate (from ⏱️ panel)
  "{{START_DATE_FIELD}}": "YYYY-MM-DD",             # Start Date (within parent range — HR8)
  "duedate": "YYYY-MM-DD"                        # Due Date (within parent range — HR8)
})
# ⚠️ HR10: NEVER set sprint on subtasks — inherits from parent
```

- Technical Note (if needed):
  - Simple text → `MCP: confluence_create_page`
  - With code blocks → Python script (see `.claude/skills/atlassian-scripts/SKILL.md`)

### 7. Handoff

```text
## TA Complete: [Title] ({{PROJECT_KEY}}-XXX)
Sub-tasks: BEP-YYY, BEP-ZZZ
→ Use /create-testplan {{PROJECT_KEY}}-XXX to continue
```

---

## Batch Sub-task Creation

> When creating ≥3 sub-tasks, use batch pattern to save tokens:
>
> 1. Create all shells with MCP (parallel calls)
> 2. Write all ADF JSON as files in `tasks/`
> 3. Run `acli edit --from-json` sequentially (or Python script for batch >5)

---

## References

- [ADF Core Rules](../shared-references/templates-core.md) - CREATE/EDIT rules, panels, styling
- [Subtask Template](../shared-references/templates-subtask.md) - Subtask ADF template + best practices
- [Vertical Slice Guide](../shared-references/vertical-slice-guide.md) - VS decomposition, patterns
- [Tool Selection](../shared-references/tools.md) - Tools, service tags, effort sizing
- After creation: `/verify-issue {{PROJECT_KEY}}-XXX --with-subtasks`
