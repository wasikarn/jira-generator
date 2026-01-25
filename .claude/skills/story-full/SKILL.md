---
name: story-full
description: |
  สร้าง User Story + Sub-tasks ครบ workflow ในครั้งเดียว (PO + TA combined) ด้วย 10-phase workflow

  Phases: Discovery → Write Story → INVEST → Create Story → Impact → Explore Codebase → Design → Alignment → Create Sub-tasks → Summary

  ⭐ Composite: ไม่ต้อง copy-paste issue keys, context preserved ตลอด workflow

  Triggers: "story full", "create story + subtasks", "full workflow"
argument-hint: "[story-description]"
---

# /story-full

**Role:** PO + TA Combined
**Output:** User Story + Sub-tasks (ครบ workflow)

## Part A: Create Story (Phases 1-4)

### 1. Discovery

- ถาม: Who? What? Why? Constraints?
- ถ้ามี Epic → `MCP: jira_get_issue(issue_key: "BEP-XXX")`
- **Gate:** User confirms requirements

### 2. Write User Story

```text
As a [persona],
I want to [action],
So that [benefit].
```

- กำหนด ACs, Scope, DoD
- **Gate:** User reviews story

### 3. INVEST Validation

- [ ] **I**ndependent - ไม่พึ่งพา story อื่น
- [ ] **N**egotiable - มี room สำหรับ discussion
- [ ] **V**aluable - มี business value ชัดเจน
- [ ] **E**stimable - ประเมิน effort ได้
- [ ] **S**mall - ทำเสร็จใน 1 sprint
- [ ] **T**estable - ทุก AC verify ได้

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

รวบรวม: Actual file paths, patterns, dependencies

**Gate:** มี actual file paths

### 7. Design Sub-tasks

- 1 sub-task per service
- Summary: `[TAG] - Description`
- Scope: Files จาก Phase 6
- ACs: Given/When/Then
- **Gate:** User approves design

### 8. Alignment Check

- [ ] Sum of sub-tasks = Complete Story?
- [ ] No gaps? No scope creep?
- [ ] File paths exist?

### 9. Create Sub-tasks

```bash
acli jira workitem create --from-json tasks/subtask-be.json
acli jira workitem create --from-json tasks/subtask-fe.json
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

- [ADF Templates](../shared-references/templates.md)
- [Workflows](../shared-references/workflows.md) - INVEST, service tags
