# Verification Checklist

> Standard checklists สำหรับ verify Jira issues

---

## Technical Checks (All Issue Types)

### T1: ADF Format
```
□ Description has type: "doc"
□ Version is 1
□ Content array exists
□ No malformed nodes
```

### T2: Panel Structure
```
□ Panels have valid panelType (info, success, warning, error, note)
□ Panel content is array
□ No nested tables in panels
```

### T3: Inline Code Marks
```
□ File paths have code marks (e.g., `app/Models/User.ts`)
□ API routes have code marks (e.g., `/api/v1/credits`)
□ Component names have code marks (e.g., `CreditHistoryPage`)
□ Technical terms marked appropriately
```

### T4: Links
```
□ Parent link exists (for sub-tasks)
□ Epic link exists (for stories)
□ Child count matches (for parents)
□ External links valid (Confluence, docs)
```

### T5: Required Fields
```
□ Summary filled
□ Description not empty
□ Issue type correct
□ Project key correct (BEP)
□ Assignee/Reporter set (if required)
```

---

## Story Quality Checks

### S1: INVEST Criteria
```
□ Independent - ไม่พึ่งพา story อื่นในการ deliver value
□ Negotiable - มี room สำหรับ discussion
□ Valuable - มี business value ชัดเจน
□ Estimable - ประเมิน effort ได้
□ Small - ทำเสร็จใน 1 sprint
□ Testable - ทุก AC verify ได้
```

### S2: Narrative Format
```
□ Has "As a [persona]"
□ Has "I want to [action]"
□ Has "So that [benefit]"
□ Persona is specific (not generic "user")
□ Benefit is business value (not technical)
```

### S3: Acceptance Criteria
```
□ All ACs have Given clause
□ All ACs have When clause
□ All ACs have Then clause
□ ACs are specific (not vague)
□ ACs are measurable
□ ACs cover happy path
□ ACs cover error cases
□ ACs are independent
```

### S4: Scope Definition
```
□ Services impacted listed
□ In-scope clearly defined
□ Out-of-scope mentioned
□ Dependencies noted
```

### S5: Language
```
□ Thai language for content
□ English for technical terms (ทับศัพท์)
□ Consistent throughout
□ No machine translation artifacts
```

---

## Sub-task Quality Checks

### ST1: Objective
```
□ Clear 1-2 sentence objective
□ Answers "what" and "why"
□ Specific to this sub-task
```

### ST2: Scope & Files
```
□ File paths are real (not generic)
□ Paths verified against codebase
□ Dependencies listed
□ Related components mentioned
```

### ST3: Acceptance Criteria
```
□ Given/When/Then format
□ Specific expected behavior
□ Error handling covered
□ Edge cases mentioned
```

### ST4: Tag & Summary
```
□ Tag matches service: [BE], [FE-Admin], [FE-Web]
□ Summary is descriptive
□ Summary starts with tag
```

### ST5: Language
```
□ Thai + ทับศัพท์ consistent
□ Technical terms in English
□ Code/paths in English
```

---

## QA Sub-task Quality Checks

### QA1: Coverage
```
□ All Story ACs have test coverage
□ Happy path covered
□ Edge cases covered
□ Error handling covered
```

### QA2: Test Format
```
□ Test objective clear
□ Preconditions stated
□ Steps are specific
□ Expected results defined
□ Actual result field (for execution)
```

### QA3: Test Scenarios
```
□ Scenarios grouped by type (happy, edge, error)
□ Priority assigned to each test
□ Panel colors match type:
  - 🟢 success = Happy path
  - 🟡 warning = Edge cases
  - 🔴 error = Error handling
```

### QA4: Test Data
```
□ Test data requirements listed
□ Preconditions for tests defined
□ Environment requirements noted
```

### QA5: Language
```
□ Thai + ทับศัพท์ consistent
□ Technical terms in English
□ Clear, actionable language
```

---

## Epic Quality Checks

### E1: Vision
```
□ Problem statement clear
□ Target users defined
□ Business value articulated
□ Success metrics defined
```

### E2: RICE Score
```
□ Reach estimated
□ Impact scored (0.25-3)
□ Confidence percentage
□ Effort in weeks
□ Final score calculated
```

### E3: Scope
```
□ Must-have features listed
□ Should-have features listed
□ Nice-to-have features listed
□ Out-of-scope defined
```

### E4: User Stories
```
□ Stories identified (draft)
□ Stories cover must-have scope
□ Stories are independent
```

---

## Scoring Guide

### Per Check
| Status | Score | Meaning |
|--------|-------|---------|
| ✅ Pass | 1 | Meets criteria |
| ⚠️ Warning | 0.5 | Partially meets, needs attention |
| ❌ Fail | 0 | Does not meet criteria |

### Overall Score
| Score % | Status | Action |
|---------|--------|--------|
| 90-100% | ✅ Pass | Ready |
| 70-89% | ⚠️ Warning | Review recommended |
| < 70% | ❌ Fail | Must fix before proceeding |

---

## Auto-Fix Capabilities

| Issue | Can Auto-Fix? | How |
|-------|---------------|-----|
| Missing code marks | ✅ Yes | Detect paths, add marks |
| Language mixed | ⚠️ Partial | Basic translation |
| Missing Given/When/Then | ❌ No | Requires understanding |
| Missing panel | ✅ Yes | Wrap in appropriate panel |
| Wrong panel color | ✅ Yes | Change panelType |
| Missing parent link | ✅ Yes | Add via MCP |

---

## Quick Reference

### Verify Story + Sub-tasks
```
/verify-issue BEP-XXX --with-subtasks
```

### Verify and Auto-Fix
```
/verify-issue BEP-XXX --fix
```

### After Creating Story
```
/create-story → /verify-issue BEP-XXX
```

### After Full Workflow
```
/story-full → /verify-issue BEP-XXX --with-subtasks
```
