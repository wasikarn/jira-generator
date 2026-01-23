# /improve-issue Command

> **Role:** Technical Analyst
> **Input:** Existing Issue(s) (BEP-XXX or Story with sub-tasks)
> **Output:** Improved issues with better format/content

---

## Usage

```
/improve-issue BEP-XXX
/improve-issue BEP-XXX --with-subtasks
/improve-issue BEP-XXX "apply new ADF templates"
```

---

## Six Phases

### Phase 1: Discovery

**Goal:** เข้าใจ issue(s) ที่ต้อง improve

**Actions:**
1. Fetch target issue:
   ```
   MCP: jira_get_issue(issue_key: "BEP-XXX")
   ```

2. ถ้า `--with-subtasks` หรือ issue type = Story:
   ```
   MCP: jira_search(jql: "parent = BEP-XXX")
   ```

3. ระบุ issue types:
   - Story
   - Sub-task (Dev)
   - Sub-task (QA)
   - Epic

**Output:** Issue inventory

| Key | Type | Current Format |
|-----|------|----------------|
| BEP-XXX | Story | wiki/ADF |
| BEP-YYY | Sub-task | wiki/ADF |
| BEP-ZZZ | [QA] | wiki/ADF |

**Gate:** User confirms scope

---

### Phase 2: Analyze Quality

**Goal:** ประเมินคุณภาพปัจจุบัน

**Quality Dimensions:**

| Dimension | Check |
|-----------|-------|
| **Format** | ADF with panels? Inline code marks? |
| **Language** | Thai + ทับศัพท์? |
| **Structure** | Follows template? |
| **Completeness** | All sections present? |
| **Clarity** | ACs testable? Given/When/Then? |

**Actions:**
1. สำหรับแต่ละ issue → Score quality:
   ```
   Format:       ⭐⭐⭐☆☆ (3/5)
   Language:     ⭐⭐☆☆☆ (2/5)
   Structure:    ⭐⭐⭐⭐☆ (4/5)
   Completeness: ⭐⭐⭐☆☆ (3/5)
   Clarity:      ⭐⭐⭐⭐☆ (4/5)
   ```

2. Identify improvement areas

**Output:** Quality assessment report

**Gate:** User approves improvement scope

---

### Phase 3: Load Templates

**Goal:** อ่าน templates ที่เกี่ยวข้อง

**Actions:**
1. Based on issue types → Load templates:

| Issue Type | Template |
|------------|----------|
| Story | `jira-templates/02-user-story.md` |
| Sub-task (Dev) | `jira-templates/03-sub-task.md` |
| Sub-task (QA) | `jira-templates/04-qa-test-case.md` |

2. Load style guide:
   - `skills/jira-workflow/references/writing-style.md`

3. Load ADF templates:
   - `skills/jira-workflow/references/templates.md`

**Output:** Templates loaded

---

### Phase 4: Generate Improvements

**Goal:** สร้าง improved versions

**Actions:**
1. สำหรับแต่ละ issue:
   - Preserve original intent/content
   - Apply template structure
   - Convert to ADF format
   - Apply Thai + ทับศัพท์
   - Add inline code marks

2. Generate ADF JSON files:
   ```
   tasks/bep-xxx-improved.json
   tasks/bep-yyy-improved.json
   tasks/bep-zzz-improved.json
   ```

3. แสดง summary:
   ```markdown
   ## Improvements Summary

   | Key | Type | Changes |
   |-----|------|---------|
   | BEP-XXX | Story | Format: wiki→ADF, Language: EN→TH |
   | BEP-YYY | Sub-task | Added panels, inline code marks |
   | BEP-ZZZ | [QA] | Restructured test cases |
   ```

**Output:** Draft improvements

**Gate:** User reviews and approves

---

### Phase 5: Apply Updates

**Goal:** Update ทุก issues ใน Jira

**Actions:**
1. Update ทีละ issue:
   ```bash
   acli jira workitem edit --from-json tasks/bep-xxx-improved.json --yes
   acli jira workitem edit --from-json tasks/bep-yyy-improved.json --yes
   acli jira workitem edit --from-json tasks/bep-zzz-improved.json --yes
   ```

2. Track status:
   ```
   ✅ BEP-XXX updated
   ✅ BEP-YYY updated
   ❌ BEP-ZZZ failed (retry...)
   ```

3. Handle errors:
   - ADF validation error → Simplify structure
   - API error → Retry

**Output:** Update status

---

### Phase 6: Cleanup & Summary

**Goal:** สรุปและ cleanup

**Actions:**
1. Delete JSON files:
   ```bash
   rm tasks/bep-*-improved.json
   ```

2. Generate summary:
   ```markdown
   ## Improvement Complete

   ### Updated Issues
   | Key | Type | Status |
   |-----|------|--------|
   | BEP-XXX | Story | ✅ |
   | BEP-YYY | Sub-task | ✅ |
   | BEP-ZZZ | [QA] | ✅ |

   ### Quality Improvement
   - Format: wiki → ADF with colored panels
   - Language: English → Thai + ทับศัพท์
   - Structure: Applied standard templates
   ```

**Output:** Final summary

---

## Quality Checklist

Before applying:
- [ ] Original content preserved
- [ ] No meaning changes
- [ ] Templates applied correctly
- [ ] Thai + ทับศัพท์ consistent
- [ ] ADF format valid
- [ ] User approved all changes

---

## Common Improvement Scenarios

### 1. Batch Format Migration
```
/improve-issue BEP-XXX --with-subtasks
```
- Convert story + all sub-tasks to ADF
- Apply consistent templates

### 2. Single Issue Polish
```
/improve-issue BEP-YYY "add panels and inline code"
```
- Enhance single issue
- Keep content, improve format

### 3. Language Standardization
```
/improve-issue BEP-XXX --with-subtasks "standardize to Thai"
```
- Convert all to Thai + ทับศัพท์
- Keep technical terms in English

### 4. Template Compliance
```
/improve-issue BEP-XXX "align with new templates"
```
- Restructure to match current templates
- Add missing sections

---

## ADF Improvement Patterns

### Before (wiki format)
```
h2. Objective
Do something

h2. AC
* Given x
* When y
* Then z
```

### After (ADF format)
```json
{
  "type": "panel",
  "attrs": {"panelType": "info"},
  "content": [...]
}
```

**Key Improvements:**
- Color-coded panels (info, success, warning, error)
- Inline code marks for paths, routes, components
- Structured tables
- Proper Given/When/Then formatting
