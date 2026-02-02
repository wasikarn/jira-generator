---
name: verify-issue
description: |
  ตรวจสอบและปรับปรุงคุณภาพ issue (ADF format, INVEST, language, hierarchy alignment) ด้วย 6-phase workflow

  Checks: ADF render, panel structure, links, inline code, INVEST criteria, Given/When/Then, file paths, language consistency, hierarchy alignment (Epic↔Story↔Subtasks↔Docs)

  รองรับ: --with-subtasks (batch + alignment check), --fix (auto-fix + format migration)

  Triggers: "verify", "validate", "ตรวจสอบ", "check quality", "improve", "migrate format"
argument-hint: "[issue-key] [--with-subtasks] [--fix]"
---

# /verify-issue

**Role:** Any
**Output:** Verification report (default) หรือ Improved issues (with `--fix`)

## Phases

### 1. Fetch & Identify

- `MCP: jira_get_issue(issue_key: "BEP-XXX")`
- ถ้า `--with-subtasks` → `MCP: jira_search(jql: "parent = BEP-XXX")`
- Identify type → Select checklist
- Build inventory: Key, Type, Current Format
- **Gate (--fix only):** User confirms scope

### 2. Technical Verification

| Check | Pass Criteria |
| --- | --- |
| ADF Format | Has `type: "doc"` |
| Panels | Correct `panelType` |
| Inline Code | Technical terms marked |
| Links | Parent/child exist |
| Fields | Required fields filled |

### 3. Quality Verification

| Dimension | Check |
| --- | --- |
| Format | ADF with panels? Inline code marks? |
| Language | Thai + ทับศัพท์? |
| Structure | Follows template? |
| Completeness | All sections present? |
| Clarity | ACs testable? Given/When/Then? |

Score: ⭐⭐⭐☆☆ (per dimension, 5-point scale)

**Type-specific checks:**

- **Story:** INVEST criteria (6 points), Narrative format, AC Given/When/Then
- **Sub-task:** Objective clear, File paths real (not generic), AC format correct
- **QA:** All Story ACs covered, Test scenarios clear, Priority assigned

### 4. Hierarchy Alignment (`--with-subtasks` only)

> **หลักการ:** ใช้เฉพาะข้อมูลจริงที่ fetch มาจาก Jira/Confluence เท่านั้น — ห้ามเดาอย่างเด็ดขาด
> ถ้าไม่แน่ใจว่า AC ไหน map กับ subtask ไหน → flag เป็น "unclear mapping"

**Data fetching:**

```text
1. Story → jira_get_issue(story_key) — ACs, scope, services impacted
2. Epic → jira_get_issue(story.parent) — scope, must-have list (skip ถ้าไม่มี)
3. Subtasks → fetched แล้วจาก Phase 1
4. Confluence → confluence_search("BEP-XXX") — Tech Note (skip ถ้าไม่มี)
```

**Alignment checks:**

| ID | Check | วิธีตรวจ | Pass Criteria |
| --- | --- | --- | --- |
| A1 | AC ↔ Subtask Coverage | map แต่ละ Story AC → subtask(s) ที่ implement | ทุก AC มี ≥1 subtask รองรับ |
| A2 | Service Tag Match | Story "Services Impacted" → Subtask tags `[BE]`/`[FE-*]` | ทุก service มี subtask |
| A3 | Scope Consistency | Story in-scope items → Subtask objectives cover them | ไม่มี scope gap |
| A4 | Epic ↔ Story Fit | Story scope อยู่ใน Epic must-have/should-have | Story ไม่หลุด Epic scope |
| A5 | Parent-Child Links | Subtask.parent = Story, Story.parent = Epic | links ถูกต้อง |
| A6 | Confluence Alignment | Tech Note content สอดคล้องกับ Story ACs (ถ้ามี) | ไม่ขัดแย้ง |

**Rules:**

- ถ้า Epic ไม่มี (standalone Story) → skip A4
- ถ้า Confluence ไม่มี → skip A6, flag เป็น info
- ถ้า mapping ไม่ชัด → flag "unclear mapping" (ห้ามเดา)
- Report เฉพาะสิ่งที่ verify ได้จากข้อมูลจริง

### 5. Report

```text
## Verification: BEP-XXX

| Category | Score | Status |
|----------|-------|--------|
| Technical | 5/5 | ✅ Pass |
| Quality | 4/6 | ⚠️ Warning |
| Alignment | 5/6 | ⚠️ Warning |  ← (--with-subtasks only)
| **Overall** | 14/17 | ⚠️ |

Issues:
1. ⚠️ AC3 missing "Then"
2. ❌ Language mixed

Alignment Issues (--with-subtasks):
1. ⚠️ AC3 ไม่มี subtask รองรับ
2. ⚠️ Story ระบุ [FE-Web] แต่ไม่มี subtask tag [FE-Web]

→ /verify-issue BEP-XXX --fix
```

### 6. Fix (--fix flag only)

ถ้ามี `--fix` → ดำเนินการแก้ไขทั้งหมดที่พบใน Phase 2-4:

1. **Load Templates** — ดึง template ตาม issue type จาก `shared-references/`
2. **Generate** — Preserve original intent, apply template + ADF + Thai + inline code → `tasks/bep-xxx-fixed.json`
3. **Gate:** User reviews and approves
4. **Apply** — `acli jira workitem edit --from-json tasks/bep-xxx-fixed.json --yes`
5. **Cleanup** — `rm tasks/bep-*-fixed.json`

```text
## Fix Complete
Updated: BEP-XXX, BEP-YYY, BEP-ZZZ
Quality: wiki → ADF, EN → Thai
```

---

## Batch Mode

```text
/verify-issue BEP-XXX --with-subtasks
/verify-issue BEP-XXX --with-subtasks --fix
```

| Key | Technical | Quality | Alignment | Overall |
| --- | --- | --- | --- | --- |
| BEP-XXX (Story) | 5/5 ✅ | 4/6 ⚠️ | 5/6 ⚠️ | ⚠️ |
| BEP-YYY [BE] | 5/5 ✅ | 6/6 ✅ | — | ✅ |
| BEP-ZZZ [FE-Web] | 5/5 ✅ | 5/6 ⚠️ | — | ⚠️ |

---

## Common Scenarios

| Scenario | Command |
| --- | --- |
| Quick check | `/verify-issue BEP-XXX` |
| Check story + subtasks | `/verify-issue BEP-XXX --with-subtasks` |
| Auto-fix single issue | `/verify-issue BEP-XXX --fix` |
| Batch format migration | `/verify-issue BEP-XXX --with-subtasks --fix` |
| Language standardization | `/verify-issue BEP-XXX --fix "standardize Thai"` |

---

## Integration

| After Command | Verify With |
| --- | --- |
| `/create-story` | `/verify-issue BEP-XXX` |
| `/analyze-story` | `/verify-issue BEP-XXX --with-subtasks` |
| `/story-full` | `/verify-issue BEP-XXX --with-subtasks` |
| `/improve-issue` (legacy) | → ใช้ `/verify-issue BEP-XXX --with-subtasks --fix` แทน |

---

## References

- [Verification Checklist](../shared-references/verification-checklist.md)
- [ADF Core Rules](../shared-references/templates.md) - CREATE/EDIT rules, panels, styling
- [Epic Template](../shared-references/templates-epic.md)
- [Story Template](../shared-references/templates-story.md)
- [Sub-task Template](../shared-references/templates-subtask.md)
- [Task Template](../shared-references/templates-task.md)
- [Writing Style](../shared-references/writing-style.md)
