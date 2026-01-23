# /analyze-story Command

> **Role:** Senior Technical Analyst
> **Input:** User Story (BEP-XXX)
> **Output:** Sub-tasks + Technical Note

---

## Usage

```
/analyze-story BEP-XXX
```

---

## Seven Phases

Execute phases in order. **ห้ามข้ามขั้นตอน**

### Phase 1: Discovery

**Goal:** ทำความเข้าใจ User Story

**Actions:**
1. Fetch User Story จาก Jira
   ```
   MCP: jira_get_issue(issue_key: "BEP-XXX")
   ```
2. อ่าน:
   - User Story narrative (As a... I want... So that...)
   - Acceptance Criteria (ACs)
   - Links (Design, Epic, related stories)
3. ถ้ามี Epic - อ่าน Epic context

**Output:** สรุป Story ให้ user ยืนยันความเข้าใจ

**Gate:** User confirms understanding before proceeding

---

### Phase 2: Impact Analysis

**Goal:** ระบุ services และ scope ที่กระทบ

**Actions:**
1. วิเคราะห์ ACs → services ที่เกี่ยวข้อง
2. ระบุ impact:

| Service | Impact | Reason |
|---------|--------|--------|
| Backend | ✅/❌ | [why] |
| Admin | ✅/❌ | [why] |
| Website | ✅/❌ | [why] |

3. ถ้า complex → Domain Analysis (events, commands, actors)

**Output:** Impact summary table

**Gate:** User confirms scope before codebase exploration

---

### Phase 3: Codebase Exploration ⚠️ MANDATORY

**Goal:** หา actual file paths และ patterns จาก codebase จริง

> **ห้ามข้าม Phase นี้!**
> ไม่มี exploration = ไม่มี design ที่ถูกต้อง

**Actions:**
1. สำหรับแต่ละ service ที่กระทบ → Launch Explore agent:

```
Task(
  subagent_type: "Explore",
  prompt: "Find [feature] implementation in [service path].
           Look for: existing components, API endpoints,
           models, patterns used."
)
```

| Service | Path |
|---------|------|
| Backend | `~/Codes/Works/tathep/tathep-platform-api` |
| Admin | `~/Codes/Works/tathep/tathep-admin` |
| Website | `~/Codes/Works/tathep/tathep-website` |

2. จาก exploration results → รวบรวม:
   - [ ] Actual file paths ที่ต้องแก้ไข
   - [ ] Existing models/components ที่เกี่ยวข้อง
   - [ ] Patterns & conventions ที่ใช้ในโปรเจค
   - [ ] Dependencies & related code

**Output:** Codebase findings summary with specific file paths

**Gate:** มี actual file paths ก่อน design

---

### Phase 4: Design Sub-tasks

**Goal:** ออกแบบ Sub-tasks จากข้อมูลจริง

**Actions:**
1. แบ่ง Sub-tasks ตาม service:
   - 1 sub-task per service (ปกติ)
   - Split ถ้า XL effort

2. สำหรับแต่ละ Sub-task:
   - Summary: `[TAG] - Description`
   - Objective: What and why (1-2 ประโยค)
   - Scope: Files จาก Phase 3 exploration
   - Requirements: What to do (not how)
   - ACs: Given/When/Then

3. Apply writing style:
   - ภาษาไทย + ทับศัพท์ (technical terms)
   - กระชับ, เป็นกันเอง

**Template:** See `jira-templates/03-sub-task.md`

**Output:** Draft sub-tasks for review

**Gate:** User approves sub-task design

---

### Phase 5: Alignment Check

**Goal:** ตรวจสอบความครบถ้วน

**Checklist:**
- [ ] Sum of sub-tasks = Complete User Story?
- [ ] No gaps (missing functionality)?
- [ ] No scope creep (extra features)?
- [ ] Each sub-task is INVEST compliant?
- [ ] Only tags: `[BE]`, `[FE-Admin]`, `[FE-Web]`?
- [ ] File paths exist in codebase?

**Output:** Alignment confirmation

**Gate:** All checks pass

---

### Phase 6: Create Artifacts

**Goal:** สร้าง Sub-tasks และ Technical Note ใน Jira/Confluence

**Actions:**

1. **Create Sub-tasks** (ใช้ ADF format):
   ```bash
   # Generate ADF JSON
   # File: tasks/bep-xxx-subtask.json

   # Create via acli
   acli jira workitem create --from-json tasks/bep-xxx-subtask.json
   ```

2. **Create Technical Note** (ถ้าจำเป็น):
   - ใช้ MCP: `confluence_create_page`
   - Parent: Epic doc
   - Template: `confluence-templates/02-technical-note.md`

3. **Update User Story**:
   - Add Technical Note link
   - MCP: `jira_update_issue`

**Tool Selection:**
| Task | Tool | Reason |
|------|------|--------|
| Create/Update Jira description | `acli --from-json` | ADF renders correctly |
| Update other fields | MCP `jira_update_issue` | Simple fields |
| Create Confluence | MCP `confluence_create_page` | Accepts markdown |

**Output:** Links to created artifacts

---

### Phase 7: Summary & Handoff

**Goal:** สรุปและส่งต่อให้ QA

**Output Format:**

```markdown
## TA Analysis Complete: [Story Title] (BEP-XXX)

### Created Sub-tasks
| Key | Summary | Effort |
|-----|---------|--------|
| BEP-YYY | [BE] - ... | M |
| BEP-ZZZ | [FE-Admin] - ... | S |

### Technical Note
- [Title](confluence-link)

### Handoff to QA
Story: BEP-XXX
Sub-tasks: BEP-YYY, BEP-ZZZ
Ready for: Test Plan creation

Use `/create-testplan BEP-XXX` to continue
```

---

## Quality Checklist

Before completing:
- [ ] All 7 phases executed in order
- [ ] Codebase explored (Phase 3 not skipped)
- [ ] File paths are real (not generic)
- [ ] Sub-tasks use ADF format via acli
- [ ] Content is Thai + ทับศัพท์
- [ ] INVEST criteria met
- [ ] Technical Note created (if needed)
- [ ] Handoff summary provided

---

## Error Recovery

| Error | Solution |
|-------|----------|
| Jira API error | Check issue key format (BEP-XXX) |
| ADF validation error | Simplify structure (no nested tables in panels) |
| File paths not found | Re-run Explore agent with different search terms |
| MCP timeout | Retry or use acli alternative |
