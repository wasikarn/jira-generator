---
name: story-full
description: |
  สร้าง User Story + Sub-tasks ครบ workflow ในครั้งเดียว (PO + TA combined) ด้วย 10-phase workflow

  Phases: Discovery → Write Story → INVEST → Create Story → Impact → Explore Codebase → Design → Alignment → Create Sub-tasks → Summary

  ⭐ Composite: ไม่ต้อง copy-paste issue keys, context preserved ตลอด workflow

  Triggers: "story full", "create story + subtasks", "full workflow"
disable-model-invocation: true
argument-hint: "[story-description]"
---

# /story-full Command

> **Role:** PO + TA Combined
> **Input:** Feature requirements
> **Output:** User Story + Sub-tasks + Technical Note (ครบ workflow)

---

## Usage

```
/story-full
/story-full "ผู้ใช้ต้องการดูประวัติการใช้เครดิต"
```

---

## Ten Phases (Combined Workflow)

### Part A: Create Story (Phases 1-4)

#### Phase 1: Discovery

**Goal:** ทำความเข้าใจ requirements

**Actions:**
1. ถาม user เกี่ยวกับ:
   - Who is the user? (persona)
   - What do they want to do?
   - Why? (business value)
   - Constraints/dependencies?

2. ถ้ามี Epic → Fetch context:
   ```
   MCP: jira_get_issue(issue_key: "BEP-XXX")
   ```

**Output:** Requirements summary

**Gate:** User confirms understanding

---

#### Phase 2: Write User Story

**Goal:** เขียน User Story ตาม format

**Actions:**
1. เขียน narrative:
   ```
   As a [persona],
   I want to [action],
   So that [benefit].
   ```

2. กำหนด Acceptance Criteria (ACs)
3. ระบุ Scope และ DoD

**Template:** `jira-templates/02-user-story.md`

**Output:** Draft User Story

**Gate:** User reviews story

---

#### Phase 3: INVEST Validation

**Goal:** ตรวจสอบคุณภาพ User Story

**Checklist:**
- [ ] **I**ndependent - ไม่พึ่งพา story อื่น
- [ ] **N**egotiable - มี room สำหรับ discussion
- [ ] **V**aluable - มี business value ชัดเจน
- [ ] **E**stimable - ประเมิน effort ได้
- [ ] **S**mall - ทำเสร็จใน 1 sprint
- [ ] **T**estable - ทุก AC verify ได้

**Gate:** All criteria pass

---

#### Phase 4: Create Story in Jira

**Goal:** สร้าง User Story ใน Jira

**Actions:**
1. Generate ADF JSON
2. Create via acli:
   ```bash
   acli jira workitem create --from-json tasks/story.json
   ```
3. **Capture new story key (BEP-XXX)** ← สำคัญ!

**Output:** Story URL + Key

**Gate:** Story created, continue to analysis

---

### Part B: Analyze & Create Sub-tasks (Phases 5-10)

#### Phase 5: Impact Analysis

**Goal:** ระบุ services ที่กระทบ

**Actions:**
1. วิเคราะห์ ACs → services ที่เกี่ยวข้อง
2. ระบุ impact:

| Service | Impact | Reason |
|---------|--------|--------|
| Backend | ✅/❌ | [why] |
| Admin | ✅/❌ | [why] |
| Website | ✅/❌ | [why] |

**Output:** Impact summary

**Gate:** User confirms scope

---

#### Phase 6: Codebase Exploration ⚠️ MANDATORY

**Goal:** หา actual file paths และ patterns

> **ห้ามข้าม Phase นี้!**

**Actions:**
1. สำหรับแต่ละ service ที่กระทบ:
   ```
   Task(subagent_type: "Explore", prompt: "Find [feature] in [path]")
   ```

2. รวบรวม:
   - Actual file paths
   - Existing patterns
   - Dependencies

**Output:** Codebase findings

**Gate:** มี actual file paths

---

#### Phase 7: Design Sub-tasks

**Goal:** ออกแบบ Sub-tasks จากข้อมูลจริง

**Actions:**
1. แบ่ง Sub-tasks ตาม service
2. สำหรับแต่ละ Sub-task:
   - Summary: `[TAG] - Description`
   - Scope: Files จาก exploration
   - ACs: Given/When/Then

**Template:** `jira-templates/03-sub-task.md`

**Output:** Draft sub-tasks

**Gate:** User approves design

---

#### Phase 8: Alignment Check

**Goal:** ตรวจสอบความครบถ้วน

**Checklist:**
- [ ] Sum of sub-tasks = Complete Story?
- [ ] No gaps?
- [ ] No scope creep?
- [ ] INVEST compliant?

**Gate:** All checks pass

---

#### Phase 9: Create Sub-tasks in Jira

**Goal:** สร้าง Sub-tasks ทั้งหมด

**Actions:**
1. Generate ADF JSON for each sub-task
2. Create via acli (with parent = story from Phase 4):
   ```bash
   acli jira workitem create --from-json tasks/subtask-be.json
   acli jira workitem create --from-json tasks/subtask-fe.json
   ```

**Output:** Sub-task URLs

---

#### Phase 10: Summary & Handoff

**Goal:** สรุปทุกอย่างที่สร้าง

**Output Format:**

```markdown
## Story Full Workflow Complete

### User Story
| Key | Summary |
|-----|---------|
| BEP-XXX | [Story title] |

### Sub-tasks Created
| Key | Tag | Summary | Effort |
|-----|-----|---------|--------|
| BEP-YYY | [BE] | ... | M |
| BEP-ZZZ | [FE-Admin] | ... | S |

### Next Steps
- [ ] TA: Create Technical Note (optional)
- [ ] QA: Use `/create-testplan BEP-XXX` for test coverage
- [ ] Dev: Start implementation

### Links
- Story: [BEP-XXX](jira-link)
- Sub-tasks: BEP-YYY, BEP-ZZZ
```

---

## Quality Checklist

Before completing:
- [ ] Story passes INVEST
- [ ] Codebase explored (Phase 6 not skipped)
- [ ] File paths are real
- [ ] All artifacts use ADF via acli
- [ ] Content is Thai + ทับศัพท์
- [ ] Sub-tasks link to parent story
- [ ] Summary provided

---

## Error Recovery

| Error | Solution |
|-------|----------|
| Story create fails | Fix JSON, retry Phase 4 |
| Sub-task create fails | Story exists, retry Phase 9 only |
| File paths not found | Re-run Explore (Phase 6) with different terms |
| INVEST fails | Re-work story before creating sub-tasks |
| Interrupted mid-workflow | Note last phase, check Jira for created items, resume |

---

## Comparison with Separate Commands

| Approach | Commands | Context |
|----------|----------|---------|
| **Separate** | `/create-story` + `/analyze-story BEP-XXX` | Lost between commands |
| **Combined** | `/story-full` | Preserved throughout |

**Benefits of /story-full:**
- ไม่ต้อง copy-paste issue keys
- Context preserved ตลอด workflow
- Faster overall execution
- Consistent quality checks

---

## Verification

หลังสร้าง Story + Sub-tasks แล้ว ให้ verify ทั้งหมด:

```
/verify-issue BEP-XXX --with-subtasks
```

**Checks:**
- ✅ Story: INVEST, ADF, narrative, ACs
- ✅ Sub-tasks: File paths, ACs, parent links
- ✅ All: Language เป็น Thai + ทับศัพท์

See `shared-references/verification-checklist.md` for full checklist.

---

## References

- [ADF Templates](../shared-references/templates.md)
- [Writing Style](../shared-references/writing-style.md)
- [Tool Selection](../shared-references/tools.md)
