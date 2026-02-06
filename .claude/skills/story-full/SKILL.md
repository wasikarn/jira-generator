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
- If Epic exists → `MCP: jira_get_issue(issue_key: "BEP-XXX")` + read VS plan
- **VS Assignment:** Which vertical slice? (`vs1-skeleton`, `vs2-*`, `vs-enabler`)
- **Gate:** User confirms requirements + VS assignment

### 2. Write User Story

```text
As a [persona],
I want to [action],
So that [benefit].
```

- Define ACs, Scope, DoD
- **VS Check:** Story delivers e2e value? All layers touched? (not shell-only)
- **Gate:** User reviews story + VS integrity

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

**Gate:** All criteria pass + VS integrity

### 4. Create Story in Jira

```bash
acli jira workitem create --from-json tasks/story.json
```

**Labels (MANDATORY):** Feature label + VS label (e.g., `coupon-web`, `vs2-collect-e2e`)

**Capture story key → BEP-XXX**

---

## Part B: Create Sub-tasks (Phases 5-10)

### 5. Impact Analysis

| Service | Impact | Reason |
| --- | --- | --- |
| Backend | ✅/❌ | [why] |
| Admin | ✅/❌ | [why] |
| Website | ✅/❌ | [why] |

**VS Verification:** Story touches all layers for e2e slice? (not layer-only)

**Gate:** User confirms scope + VS integrity

### 6. Codebase Exploration ⚠️ MANDATORY

```text
Task(subagent_type: "Explore", prompt: "Find [feature] in [path]")
```

Collect: Actual file paths, patterns, dependencies

**Gate:** Must have actual file paths

### 7. Design Sub-tasks

- 1 sub-task per service
- **VS Integrity:** Each subtask contributes to VS completion (not horizontal)
- Summary: `[TAG] - Description`
- Scope: Files from Phase 6
- ACs: Given/When/Then
- **Gate:** User approves design + VS alignment

### 8. Alignment Check

- [ ] Sum of sub-tasks = Complete Story?
- [ ] No gaps? No scope creep?
- [ ] File paths exist?
- [ ] **VS integrity maintained?** (subtasks complete the slice, not horizontal)

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
- [Templates](../shared-references/templates.md) - ADF templates (Story, Sub-task sections)
- [Vertical Slice Guide](../shared-references/vertical-slice-guide.md) - VS patterns, decomposition, labels
- [Verification Checklist](../shared-references/verification-checklist.md) - INVEST, quality checks
