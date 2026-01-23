# /verify-issue Command

> **Role:** Any
> **Input:** Issue key (BEP-XXX) or Story with sub-tasks
> **Output:** Verification report with pass/fail status

---

## Usage

```
/verify-issue BEP-XXX
/verify-issue BEP-XXX --with-subtasks
/verify-issue BEP-XXX --fix
```

---

## Four Phases

### Phase 1: Fetch & Identify

**Goal:** ดึงข้อมูลและระบุ issue type

**Actions:**
1. Fetch issue:
   ```
   MCP: jira_get_issue(issue_key: "BEP-XXX")
   ```

2. ถ้า `--with-subtasks`:
   ```
   MCP: jira_search(jql: "parent = BEP-XXX")
   ```

3. Identify issue type → Select checklist:
   - Epic → Epic checklist
   - Story → Story checklist
   - Sub-task → Sub-task checklist
   - [QA] Sub-task → QA checklist

**Output:** Issue inventory with types

---

### Phase 2: Technical Verification

**Goal:** ตรวจสอบ technical aspects

**Checks:**

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| **ADF Format** | Check description structure | Has `type: "doc"` with content |
| **Panels Render** | Look for panel nodes | Panels have correct `panelType` |
| **Inline Code** | Check for code marks | Technical terms have code marks |
| **Links Valid** | Check issue links | Parent/child links exist |
| **Fields Complete** | Check required fields | Summary, description, type filled |

**Actions:**
1. Parse description → Check for ADF structure
2. Verify panel types (info, success, warning, error)
3. Check for inline code marks on:
   - File paths
   - Routes/endpoints
   - Component names
4. Verify parent link (for sub-tasks)
5. Verify child links (for stories)

**Output:** Technical verification results

```markdown
## Technical Verification

| Check | Status | Details |
|-------|--------|---------|
| ADF Format | ✅ Pass | Valid doc structure |
| Panels | ✅ Pass | 3 panels (info, success, warning) |
| Inline Code | ⚠️ Warning | Missing code marks on 2 paths |
| Links | ✅ Pass | Parent: BEP-100, 3 sub-tasks |
| Fields | ✅ Pass | All required fields present |
```

---

### Phase 3: Quality Verification

**Goal:** ตรวจสอบ content quality

**Checks by Issue Type:**

#### Story Checks
| Check | Pass Criteria |
|-------|---------------|
| **INVEST** | All 6 criteria pass |
| **Narrative** | Has As a/I want/So that |
| **AC Format** | All ACs have Given/When/Then |
| **AC Testable** | ACs are specific, measurable |
| **Scope Clear** | Services/impact defined |
| **Language** | Thai + ทับศัพท์ consistent |

#### Sub-task Checks
| Check | Pass Criteria |
|-------|---------------|
| **Objective** | Clear 1-2 sentence goal |
| **File Paths** | Real paths (not generic) |
| **AC Format** | Given/When/Then format |
| **Dependencies** | Listed if any |
| **Language** | Thai + ทับศัพท์ consistent |

#### QA Sub-task Checks
| Check | Pass Criteria |
|-------|---------------|
| **Coverage** | All Story ACs covered |
| **Test Format** | Clear expected results |
| **Scenarios** | Happy, edge, error paths |
| **Priority** | Tests prioritized |
| **Language** | Thai + ทับศัพท์ consistent |

**Actions:**
1. Run INVEST validation (for stories)
2. Check narrative format
3. Validate AC structure
4. Verify file paths exist (for sub-tasks)
5. Check language consistency

**Output:** Quality verification results

```markdown
## Quality Verification

| Check | Status | Details |
|-------|--------|---------|
| INVEST | ✅ Pass | All criteria met |
| Narrative | ✅ Pass | Complete format |
| AC Format | ⚠️ Warning | AC3 missing "Then" |
| AC Testable | ✅ Pass | All specific |
| Scope | ✅ Pass | 2 services defined |
| Language | ❌ Fail | Mixed EN/TH in section 2 |
```

---

### Phase 4: Report & Fix

**Goal:** สรุปผลและเสนอ fixes

**Actions:**
1. Generate summary report
2. ถ้า `--fix` flag:
   - Generate fixed ADF JSON
   - Offer to apply fixes
3. List recommended actions

**Output Format:**

```markdown
## Verification Report: BEP-XXX

### Summary
| Category | Score | Status |
|----------|-------|--------|
| Technical | 5/5 | ✅ Pass |
| Quality | 4/6 | ⚠️ Warning |
| **Overall** | 9/11 | ⚠️ Needs Attention |

### Issues Found
1. ⚠️ AC3 missing "Then" clause
2. ❌ Language inconsistent in section 2
3. ⚠️ Missing inline code marks (2 paths)

### Recommended Actions
- [ ] Add "Then" to AC3
- [ ] Fix language to Thai + ทับศัพท์
- [ ] Add code marks to file paths

### Quick Fix
Use `/verify-issue BEP-XXX --fix` to auto-generate fixes
```

**If --fix flag:**
```markdown
### Auto-Fix Available

| Issue | Fix |
|-------|-----|
| AC3 missing Then | Added: `Then ระบบแสดง...` |
| Language mixed | Converted to Thai |
| Missing code marks | Added marks to 2 paths |

Apply fixes? (yes/no)
```

---

## Verification Checklist Reference

See `references/verification-checklist.md` for complete checklist by issue type.

---

## Batch Verification

```
/verify-issue BEP-XXX --with-subtasks
```

**Output:**
```markdown
## Batch Verification: BEP-XXX + Sub-tasks

| Key | Type | Technical | Quality | Overall |
|-----|------|-----------|---------|---------|
| BEP-XXX | Story | 5/5 ✅ | 4/6 ⚠️ | ⚠️ |
| BEP-YYY | [BE] | 5/5 ✅ | 6/6 ✅ | ✅ |
| BEP-ZZZ | [FE] | 4/5 ⚠️ | 5/6 ⚠️ | ⚠️ |
| BEP-QQQ | [QA] | 5/5 ✅ | 5/5 ✅ | ✅ |

### Issues Summary
- BEP-XXX: 2 issues (AC format, language)
- BEP-ZZZ: 2 issues (inline code, file path)

### Quick Fix All
Use `/verify-issue BEP-XXX --with-subtasks --fix`
```

---

## Error Recovery

| Error | Solution |
|-------|----------|
| Issue not found | Check key format (BEP-XXX) |
| Can't parse description | Issue may use wiki format, not ADF |
| File path check fails | Need codebase access, use Task(Explore) |
| Fix rejected | Manual fix required |

---

## Integration with Other Commands

| After Command | Verify With |
|---------------|-------------|
| `/create-story` | `/verify-issue BEP-XXX` |
| `/analyze-story` | `/verify-issue BEP-XXX --with-subtasks` |
| `/create-testplan` | `/verify-issue BEP-QQQ` |
| `/story-full` | `/verify-issue BEP-XXX --with-subtasks` |
| `/improve-issue` | `/verify-issue BEP-XXX` |
