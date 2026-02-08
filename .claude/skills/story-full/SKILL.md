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
| 1. Discovery | `epic_data`, `vs_assignment`, `user_requirements`, `user_context` |
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

> **Workflow Patterns:** See [workflow-patterns.md](../shared-references/workflow-patterns.md) for Gate Levels (AUTO/REVIEW/APPROVAL), QG Scoring, Two-Step, and Explore patterns.

## Part A: Create Story (Phases 1-4)

> **Phase Tracking:** Use TodoWrite to mark each phase `in_progress` → `completed` as you work.

### 1. Discovery

- Ask: Who? What? Why? Constraints?
  - **Story Context:** What is the user currently doing? What's difficult? (for 📍 context line)
- If Epic exists → `MCP: jira_get_issue(issue_key: "{{PROJECT_KEY}}-XXX")` + read VS plan + Problem narrative
- **VS Assignment:** Which vertical slice? (`vs1-skeleton`, `vs2-*`, `vs-enabler`)
- **⛔ GATE — DO NOT PROCEED** without user confirmation of requirements + VS assignment.

### 2. Write User Story

```text
📍 [User's current situation — what they're doing, what's difficult]  ⚡ optional
As a [persona],
I want to [action],
So that [benefit].
```

- ⚡ **Context line:** Include when persona is new or workflow is complex — not needed for every story
- Define ACs, Scope, DoD
- **AC Naming:** Use `AC{N}: [Verb] — [Scenario Name]` (not just "AC1: Title")
- **VS Check:** Story delivers e2e value? All layers touched? (not shell-only)
- **🟡 REVIEW** — Present story narrative, ACs, scope to user. Proceed unless user objects.

### 3. INVEST + VS Validation

- [ ] **I**ndependent - Not dependent on other stories
- [ ] **N**egotiable - Room for discussion
- [ ] **V**aluable - Clear business value
- [ ] **E**stimable - Can estimate effort
- [ ] **S**mall + **Vertical** - Completable in 1 sprint? **End-to-end slice?**
- [ ] **T**estable - All ACs verifiable in isolation

**VS Anti-pattern Check:**

- ❌ Shell-only (UI has no logic) → Add minimal happy path
- ❌ Layer-split (BE separated from FE) → Combine into single story

**🟢 AUTO** — Validate all criteria. If any fail or VS anti-pattern detected → auto-fix and re-validate. Escalate to user only if unfixable.

### 3b. Quality Gate — Story (HR1)

> **🟢 AUTO** — Score → auto-fix → re-score. Escalate to user only if still < 90% after 2 attempts.
> HR1: DO NOT send Story to Atlassian without QG ≥ 90%.

1. Generate ADF JSON → `tasks/story.json`
2. Score against `shared-references/verification-checklist.md` (Technical + Story Quality)
3. If < 90% → auto-fix → re-score (max 2 attempts)
4. If ≥ 90% → proceed to Phase 4 automatically
5. If still < 90% after 2 fixes → escalate to user

### 4. Create Story in Jira

> **🟢 AUTO** — If Phase 3b QG passed → create automatically. No user interaction needed.

```bash
acli jira workitem create --from-json tasks/story.json
```

**Labels (MANDATORY):** Feature label + VS label (e.g., `coupon-web`, `vs2-collect-e2e`)

**Capture story key → {{PROJECT_KEY}}-XXX**

> **🟢 AUTO** — HR6: `cache_invalidate(story_key)` after create.

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

**🟡 REVIEW** — Present impact table + VS verification to user. Proceed unless user objects.

### 6. Codebase Exploration ⚠️ MANDATORY

> [Parallel Explore](../shared-references/workflow-patterns.md#parallel-explore): Launch 2-3 agents (Backend/Frontend/Shared) IN PARALLEL.
> Validate paths with Glob. Generic paths REJECTED. Re-explore max 2 attempts.

### 7. Design Sub-tasks

- 1 sub-task per service
- **VS Integrity:** Each subtask contributes to VS completion (not horizontal)
- Summary: `[TAG] - Description`
- Scope: Files from Phase 6
- ACs: Given/When/Then
- **⛔ GATE — DO NOT CREATE** any subtasks without user approval of design + VS alignment.

### 8. Alignment Check

> **🟢 AUTO** — Verify programmatically. Auto-fix misalignment. Escalate only if unfixable.

- [ ] Sum of sub-tasks = Complete Story?
- [ ] No gaps? No scope creep?
- [ ] File paths exist? (validate with Glob)
- [ ] **VS integrity maintained?** (subtasks complete the slice, not horizontal)

If any check fails → auto-adjust subtask scope/design → re-check. Escalate to user only if gap cannot be resolved automatically.

### 9. Quality Gate — Subtasks (MANDATORY)

> **🟢 AUTO** — Score → auto-fix → re-score. Escalate only if still < 90% after 2 attempts.
> HR1: DO NOT create subtasks in Jira without QG ≥ 90%.

> [QG Scoring Rules](../shared-references/workflow-patterns.md#quality-gate-scoring). Report: `Technical X/5 | Subtask Quality X/5 | Overall X%`

### 10. Create Sub-tasks

> **🟢 AUTO** — Create → verify parent → edit descriptions. All automated. Escalate only if parent verify fails after retry.
> HR5: Two-Step + Verify Parent. acli does not support the parent field. MCP may silently ignore parent.

> [Two-Step Subtask](../shared-references/workflow-patterns.md#two-step-subtask-creation): MCP create shell → verify parent → acli edit. Batch ≥3: create all → verify all → edit all.

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

> **🟢 AUTO** — HR6: `cache_invalidate(subtask_key)` after EVERY Atlassian write.
> **🟢 AUTO** — HR3: If assignee needed, use `acli jira workitem assign -k "KEY" -a "email" -y` (never MCP).

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

- [ADF Core Rules](../shared-references/templates-core.md) - CREATE/EDIT rules, panels, styling
- [Story Template](../shared-references/templates-story.md) - Story ADF template + best practices
- [Subtask Template](../shared-references/templates-subtask.md) - Subtask ADF template + QA
- [Vertical Slice Guide](../shared-references/vertical-slice-guide.md) - VS patterns, decomposition, labels
- [Verification Checklist](../shared-references/verification-checklist.md) - INVEST, quality checks
