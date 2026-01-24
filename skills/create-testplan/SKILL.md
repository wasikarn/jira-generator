---
name: create-testplan
description: |
  สร้าง Test Plan + [QA] Sub-task จาก User Story ด้วย 6-phase QA workflow

  Phases: Discovery → Test Scope Analysis → Design Test Cases → Create Test Plan Doc → Create [QA] Sub-task → Summary

  Output: Test Plan in Confluence + [QA] Sub-task in Jira

  Triggers: "create test plan", "QA", "test case", "testing"
argument-hint: "[issue-key]"
---

# /create-testplan Command

> **Role:** Senior QA Analyst
> **Input:** User Story (BEP-XXX)
> **Output:** Test Plan + [QA] Sub-task

---

## Usage

```
/create-testplan BEP-XXX
```

---

## Six Phases

Execute phases in order.

### Phase 1: Discovery

**Goal:** ทำความเข้าใจ User Story และ Sub-tasks

**Actions:**
1. Fetch User Story:
   ```
   MCP: jira_get_issue(issue_key: "BEP-XXX")
   ```
2. Fetch Sub-tasks:
   ```
   MCP: jira_search(jql: "parent = BEP-XXX")
   ```
3. อ่าน Technical Note (ถ้ามี)

**Output:** Story summary + Sub-tasks list

**Gate:** User confirms scope

---

### Phase 2: Test Scope Analysis

**Goal:** กำหนด test scope และ coverage

**Actions:**
1. วิเคราะห์ ACs → Test scenarios
2. Map scenarios to AC coverage:

| AC | Description | Test Scenarios |
|----|-------------|----------------|
| 1 | [AC1 desc] | TC1, TC2 |
| 2 | [AC2 desc] | TC3 |

3. ระบุ test types needed:
   - ✅ Happy path
   - ⚠️ Edge cases
   - ❌ Error handling
   - 🔒 Security (if applicable)
   - 📱 UI/Responsive

**Output:** AC coverage matrix

**Gate:** 100% AC coverage

---

### Phase 3: Design Test Cases

**Goal:** ออกแบบ test cases ละเอียด

**Actions:**
1. สำหรับแต่ละ scenario → Create test case:

| Field | Content |
|-------|---------|
| ID | TC1, TC2, ... |
| AC | Which AC it covers |
| Priority | 🔴 Critical / 🟠 High / 🟡 Medium / 🟢 Low |
| Type | ✅ Happy / ⚠️ Edge / ❌ Error |
| Given | Preconditions |
| When | Actions |
| Then | Expected results (specific, measurable) |

2. กำหนด Test Data requirements
3. ระบุ Dependencies และ Environment needs

**Template:** See `jira-templates/04-qa-test-case.md`

**Output:** Draft test cases

**Gate:** User reviews test coverage

---

### Phase 4: Create Test Plan Doc

**Goal:** สร้าง Test Plan ใน Confluence

**Actions:**
1. Create Confluence page:
   ```
   MCP: confluence_create_page(
     space_key: "BEP",
     title: "Test Plan: [Story Title]",
     parent_id: [Epic page ID],
     content: [markdown content]
   )
   ```

2. Content includes:
   - Test objectives
   - Scope (in/out)
   - Test scenarios summary
   - Environment requirements
   - Test data requirements

**Template:** `confluence-templates/03-test-plan.md`

**Output:** Test Plan page URL

---

### Phase 5: Create [QA] Sub-task

**Goal:** สร้าง QA sub-task ใน Jira

> **หลักการ:** 1 User Story = 1 [QA] Sub-task
> รวมทุก test scenarios ไว้ใน sub-task เดียว

**Actions:**
1. Generate ADF JSON:
   - Summary: `[QA] - Test: [Story title]`
   - Parent: User Story
   - Description: All test cases in ADF format

2. Create via acli:
   ```bash
   acli jira workitem create --from-json tasks/bep-xxx-qa.json
   ```

**ADF Structure:**
- Info panel: Test objective, coverage summary
- Success panels: Happy path test cases (🟢)
- Warning panels: Edge cases (🟡)
- Error panels: Error handling (🔴)

**Important:**
- ใช้ bulletList ใน panel (ไม่ใช่ nested table)
- ภาษาไทย + ทับศัพท์

**Output:** QA sub-task URL

---

### Phase 6: Summary

**Goal:** สรุปและ link artifacts

**Actions:**
1. Update User Story - add Test Plan link
2. Provide summary

**Output Format:**

```markdown
## QA Analysis Complete: [Story Title] (BEP-XXX)

### Test Plan
- [Test Plan: Title](confluence-link)

### QA Sub-task
| Key | Summary | Scenarios |
|-----|---------|-----------|
| BEP-QQQ | [QA] - Test: ... | 6 |

### Coverage Summary
- Total Scenarios: X
- ACs Covered: Y/Y (100%)
- Test Types: Happy (N), Edge (N), Error (N)

### Next Steps
- [ ] Execute test cases
- [ ] Report results
- [ ] Update test status
```

---

## Quality Checklist

Before completing:
- [ ] All ACs have test coverage
- [ ] Test cases have specific expected results
- [ ] 1 [QA] sub-task per story (not multiple)
- [ ] Test Plan in Confluence
- [ ] ADF format via acli (not MCP)
- [ ] Content is Thai + ทับศัพท์
- [ ] Panels use bulletList (not nested tables)

---

## Error Recovery

| Error | Solution |
|-------|----------|
| Confluence create fails | Check space key, verify parent page exists |
| Nested table error | Use bulletList inside panels instead of tables |
| Missing AC coverage | Review Story ACs, add missing test scenarios |
| acli JSON error | Simplify ADF structure, validate JSON |

---

## ADF Panel Color Guide

| Panel Type | Color | Use For |
|------------|-------|---------|
| `info` | 🔵 Blue | Objective, summary |
| `success` | 🟢 Green | Happy path tests |
| `warning` | 🟡 Yellow | Edge cases, UI tests |
| `error` | 🔴 Red | Error handling tests |
| `note` | 🟣 Purple | Notes, dependencies |

---

## Test Priority Guide

| Priority | When to Use |
|----------|-------------|
| 🔴 Critical | Core flow, data integrity, payment |
| 🟠 High | Primary features, CRUD operations |
| 🟡 Medium | Secondary features, filters |
| 🟢 Low | Nice-to-have, UI polish |

---

## Verification

หลังสร้าง [QA] Sub-task แล้ว ให้ verify:

```
/verify-issue BEP-QQQ
```

**Checks:**
- ✅ ADF format ถูกต้อง
- ✅ ครอบคลุมทุก Story ACs
- ✅ Panel colors ตรงกับ test type
- ✅ Test scenarios ชัดเจน
- ✅ Language เป็น Thai + ทับศัพท์

See `shared-references/verification-checklist.md` for full checklist.

---

## References

- [ADF Templates](../shared-references/templates.md)
- [Writing Style](../shared-references/writing-style.md)
- [Tool Selection](../shared-references/tools.md)
