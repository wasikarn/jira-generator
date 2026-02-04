---
name: analyze-story
description: |
  Analyze User Story and create Sub-tasks + Technical Note with a 7-phase TA workflow
  MANDATORY: Must explore codebase before creating Sub-tasks
argument-hint: "[issue-key]"
---

# /analyze-story

**Role:** Senior Technical Analyst
**Output:** Sub-tasks + Technical Note

## Phases

### 1. Discovery

- `MCP: jira_get_issue(issue_key: "BEP-XXX")`
- Read: Narrative, ACs, Links, Epic context
- **Gate:** User confirms understanding

### 2. Impact Analysis

| Service | Impact | Reason |
| --- | --- | --- |
| Backend | ✅/❌ | [why] |
| Admin | ✅/❌ | [why] |
| Website | ✅/❌ | [why] |

**Gate:** User confirms scope

### 3. Codebase Exploration ⚠️ MANDATORY

```text
Task(subagent_type: "Explore", prompt: "Find [feature] in [service path]")
```

| Service | Path |
| --- | --- |
| Backend | `~/Codes/Works/tathep/tathep-platform-api` |
| Admin | `~/Codes/Works/tathep/tathep-admin` |
| Website | `~/Codes/Works/tathep/tathep-website` |

Collect: File paths, existing patterns, dependencies

**Gate:** Must have actual file paths before design

### 4. Design Sub-tasks

- 1 sub-task per service (typical)
- Summary: `[TAG] - Description`
- Scope: Files from Phase 3
- ACs: Given/When/Then
- Use Thai + transliteration
- **Gate:** User approves design

### 5. Alignment Check

- [ ] Sum of sub-tasks = Complete Story?
- [ ] No gaps? No scope creep?
- [ ] File paths exist in codebase?

### 6. Create Artifacts

> ⚠️ **CRITICAL:** Sub-tasks must use Two-Step Workflow (acli does not support `parent`)
>
> **Step 1:** MCP `jira_create_issue` (create shell + parent link)
> **Step 2:** `acli --from-json` (update ADF description)
>
> See full pattern: [Sub-task Template](../shared-references/templates-subtask.md)

- Technical Note (if needed):
  - Simple text → `MCP: confluence_create_page`
  - With code blocks → Python script (see `.claude/skills/atlassian-scripts/SKILL.md`)

### 7. Handoff

```text
## TA Complete: [Title] (BEP-XXX)
Sub-tasks: BEP-YYY, BEP-ZZZ
→ Use /create-testplan BEP-XXX to continue
```

---

## Batch Sub-task Creation

> เมื่อต้องสร้าง sub-tasks ≥3 ตัว ใช้ batch pattern ประหยัด tokens:
>
> 1. สร้าง shells ทั้งหมดด้วย MCP (parallel calls)
> 2. เขียน ADF JSON ทั้งหมดเป็น files ใน `tasks/`
> 3. Run `acli edit --from-json` ต่อเนื่อง (หรือ Python script สำหรับ batch >5)

---

## References

- [ADF Core Rules](../shared-references/templates.md) - CREATE/EDIT rules, panels, styling
- [Sub-task Template](../shared-references/templates-subtask.md) - Sub-task + QA ADF structure
- [Tool Selection](../shared-references/tools.md) - Tools, service tags, effort sizing
- After creation: `/verify-issue BEP-XXX --with-subtasks`
