---
name: analyze-story
context: fork
description: |
  Analyze User Story and create Sub-tasks + Technical Note with a 7-phase TA workflow
  MANDATORY: Must explore codebase before creating Sub-tasks
argument-hint: "[issue-key]"
---

# /analyze-story

**Role:** Senior Technical Analyst
**Output:** Sub-tasks + Technical Note

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

> **Workflow Patterns:** See [workflow-patterns.md](../shared-references/workflow-patterns.md) for Gate Levels (AUTO/REVIEW/APPROVAL), QG Scoring, Two-Step, and Explore patterns.

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

### 4. Design Sub-tasks

- 1 sub-task per service (typical)
- **VS Integrity:** Each subtask contributes to VS completion (not horizontal)
- Summary: `[TAG] - Description`
- Scope: Files from Phase 3
- ACs: Given/When/Then
- Use Thai + transliteration
- **⛔ GATE — DO NOT CREATE** any subtasks without user approval of design + VS alignment.

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
