---
name: story-full
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

## Part A: Create Story (Phases 1-4)

### 1. Discovery

- Ask: Who? What? Why? Constraints?
- If Epic exists → `MCP: jira_get_issue(issue_key: "BEP-XXX")`
- **Gate:** User confirms requirements

### 2. Write User Story

```text
As a [persona],
I want to [action],
So that [benefit].
```

- Define ACs, Scope, DoD
- **Gate:** User reviews story

### 3. INVEST Validation

- [ ] **I**ndependent - Not dependent on other stories
- [ ] **N**egotiable - Room for discussion
- [ ] **V**aluable - Clear business value
- [ ] **E**stimable - Can estimate effort
- [ ] **S**mall - Completable in 1 sprint
- [ ] **T**estable - All ACs verifiable

**Gate:** All criteria pass

### 4. Create Story in Jira

```bash
acli jira workitem create --from-json tasks/story.json
```

**Capture story key → BEP-XXX**

---

## Part B: Create Sub-tasks (Phases 5-10)

### 5. Impact Analysis

| Service | Impact | Reason |
| --- | --- | --- |
| Backend | ✅/❌ | [why] |
| Admin | ✅/❌ | [why] |
| Website | ✅/❌ | [why] |

**Gate:** User confirms scope

### 6. Codebase Exploration ⚠️ MANDATORY

```text
Task(subagent_type: "Explore", prompt: "Find [feature] in [path]")
```

Collect: Actual file paths, patterns, dependencies

**Gate:** Must have actual file paths

### 7. Design Sub-tasks

- 1 sub-task per service
- Summary: `[TAG] - Description`
- Scope: Files from Phase 6
- ACs: Given/When/Then
- **Gate:** User approves design

### 8. Alignment Check

- [ ] Sum of sub-tasks = Complete Story?
- [ ] No gaps? No scope creep?
- [ ] File paths exist?

### 9. Create Sub-tasks

> ⚠️ **Two-Step Workflow** — acli ไม่รองรับ `parent` field
>
> **Step 1:** MCP `jira_create_issue` (create shell + parent link) — parallel calls ได้
> **Step 2:** `acli --from-json` (update ADF description)
>
> เมื่อ sub-tasks ≥3 ตัว: สร้าง shells ทั้งหมดก่อน → batch edit descriptions

```text
# Step 1: Create shells (parallel)
MCP: jira_create_issue({project_key:"BEP", summary:"[BE] - ...", issue_type:"Subtask", additional_fields:{parent:{key:"BEP-XXX"}}})
MCP: jira_create_issue({project_key:"BEP", summary:"[FE-Web] - ...", issue_type:"Subtask", additional_fields:{parent:{key:"BEP-XXX"}}})

# Step 2: Update descriptions
acli jira workitem edit --from-json tasks/subtask-be.json --yes
acli jira workitem edit --from-json tasks/subtask-fe.json --yes
```

### 10. Summary

```text
## Story Full Complete
Story: BEP-XXX
Sub-tasks: BEP-YYY [BE], BEP-ZZZ [FE-Admin]
→ /create-testplan BEP-XXX for QA
→ /verify-issue BEP-XXX --with-subtasks
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
- [Story Template](../shared-references/templates-story.md) - Story ADF structure
- [Sub-task Template](../shared-references/templates-subtask.md) - Sub-task + QA ADF structure
- [Verification Checklist](../shared-references/verification-checklist.md) - INVEST, quality checks
