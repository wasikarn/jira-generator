---
name: verify-issue
description: |
  ตรวจสอบคุณภาพ issue (ADF format, INVEST, language) ด้วย 4-phase workflow

  Checks: ADF render, panel structure, links, inline code, INVEST criteria, Given/When/Then, file paths, language consistency

  รองรับ: --with-subtasks (batch verify), --fix (auto-fix)

  Triggers: "verify", "validate", "ตรวจสอบ", "check quality"
argument-hint: "[issue-key] [--with-subtasks] [--fix]"
---

# /verify-issue

**Role:** Any
**Output:** Verification report with pass/fail status

## Phases

### 1. Fetch & Identify
- `MCP: jira_get_issue(issue_key: "BEP-XXX")`
- ถ้า `--with-subtasks` → `MCP: jira_search(jql: "parent = BEP-XXX")`
- Identify type → Select checklist

### 2. Technical Verification

| Check | Pass Criteria |
|-------|---------------|
| ADF Format | Has `type: "doc"` |
| Panels | Correct `panelType` |
| Inline Code | Technical terms marked |
| Links | Parent/child exist |
| Fields | Required fields filled |

### 3. Quality Verification

**Story Checks:**
- INVEST criteria (6 points)
- Narrative format
- AC Given/When/Then
- Language Thai + ทับศัพท์

**Sub-task Checks:**
- Objective clear
- File paths real (not generic)
- AC format correct

**QA Checks:**
- All Story ACs covered
- Test scenarios clear
- Priority assigned

### 4. Report & Fix

```
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

---

## Batch Verification

```
/verify-issue BEP-XXX --with-subtasks
```

| Key | Technical | Quality | Overall |
|-----|-----------|---------|---------|
| BEP-XXX | 5/5 ✅ | 4/6 ⚠️ | ⚠️ |
| BEP-YYY | 5/5 ✅ | 6/6 ✅ | ✅ |

---

## Integration

| After Command | Verify With |
|---------------|-------------|
| `/create-story` | `/verify-issue BEP-XXX` |
| `/analyze-story` | `/verify-issue BEP-XXX --with-subtasks` |
| `/story-full` | `/verify-issue BEP-XXX --with-subtasks` |

---

## References

- [Verification Checklist](../shared-references/verification-checklist.md)
- [ADF Templates](../shared-references/templates.md)
