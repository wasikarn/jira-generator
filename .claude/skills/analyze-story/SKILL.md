---
name: analyze-story
description: |
  วิเคราะห์ User Story และสร้าง Sub-tasks + Technical Note ด้วย 7-phase TA workflow
  ⚠️ MANDATORY: ต้อง explore codebase ก่อนสร้าง Sub-tasks เสมอ
argument-hint: "[issue-key]"
---

# /analyze-story

**Role:** Senior Technical Analyst
**Output:** Sub-tasks + Technical Note

## Phases

### 1. Discovery

- `MCP: jira_get_issue(issue_key: "BEP-XXX")`
- อ่าน: Narrative, ACs, Links, Epic context
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

รวบรวม: File paths, existing patterns, dependencies

**Gate:** มี actual file paths ก่อน design

### 4. Design Sub-tasks

- 1 sub-task per service (ปกติ)
- Summary: `[TAG] - Description`
- Scope: Files จาก Phase 3
- ACs: Given/When/Then
- ใช้ภาษาไทย + ทับศัพท์
- **Gate:** User approves design

### 5. Alignment Check

- [ ] Sum of sub-tasks = Complete Story?
- [ ] No gaps? No scope creep?
- [ ] File paths exist in codebase?

### 6. Create Artifacts

> ⚠️ **CRITICAL:** ต้องใช้ Two-Step Workflow สำหรับ Subtask (acli ไม่รองรับ `parent` field)

**Step 1: สร้าง Sub-task shell ด้วย MCP**

```typescript
jira_create_issue({
  project_key: "BEP",
  summary: "[TAG] - Description",
  issue_type: "Subtask",
  additional_fields: { parent: { key: "BEP-XXX" } }  // Parent Story key
})
// Returns: BEP-YYY (new subtask key)
```

**Step 2: Update description ด้วย acli + ADF**

```bash
acli jira workitem edit --from-json tasks/subtask-bep-yyy.json --yes
```

> JSON file ต้องใช้ format: `{"issues": ["BEP-YYY"], "description": {...}}`

- Technical Note (ถ้าจำเป็น):
  - Simple text → `MCP: confluence_create_page`
  - With code blocks → Python script (see `.claude/skills/atlassian-scripts/SKILL.md`)

### 7. Handoff

```text
## TA Complete: [Title] (BEP-XXX)
Sub-tasks: BEP-YYY, BEP-ZZZ
→ Use /create-testplan BEP-XXX to continue
```

---

## References

- [ADF Templates](../shared-references/templates.md) - Sub-task structure
- [Workflows](../shared-references/workflows.md) - Service tags, effort sizing
- After creation: `/verify-issue BEP-XXX --with-subtasks`
