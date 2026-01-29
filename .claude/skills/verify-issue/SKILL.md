---
name: verify-issue
description: |
  ตรวจสอบและปรับปรุงคุณภาพ issue (ADF format, INVEST, language) ด้วย 5-phase workflow

  Checks: ADF render, panel structure, links, inline code, INVEST criteria, Given/When/Then, file paths, language consistency

  รองรับ: --with-subtasks (batch), --fix (auto-fix + format migration)

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

### 4. Report

```text
## Verification: BEP-XXX

| Category | Score | Status |
|----------|-------|--------|
| Technical | 5/5 | ✅ Pass |
| Quality | 4/6 | ⚠️ Warning |
| **Overall** | 9/11 | ⚠️ |

Issues:
1. ⚠️ AC3 missing "Then"
2. ❌ Language mixed

→ /verify-issue BEP-XXX --fix
```

### 5. Fix (--fix flag only)

ถ้ามี `--fix` → ดำเนินการแก้ไขทั้งหมดที่พบใน Phase 2-3:

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

| Key | Technical | Quality | Overall |
| --- | --- | --- | --- |
| BEP-XXX | 5/5 ✅ | 4/6 ⚠️ | ⚠️ |
| BEP-YYY | 5/5 ✅ | 6/6 ✅ | ✅ |

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
