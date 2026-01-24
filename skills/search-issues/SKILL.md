---
name: search-issues
description: |
  ค้นหา issues ก่อนสร้างใหม่ (ป้องกันสร้างซ้ำ) ด้วย 3-phase workflow

  รองรับ: keyword search, JQL query, filters (sprint, assignee, status, type)

  Triggers: "search", "find", "หา issue", "มีอยู่แล้วไหม"
argument-hint: "[keyword] [--filters]"
---

# /search-issues Command

> **Role:** Any
> **Input:** Search criteria (keyword, JQL, filters)
> **Output:** List of matching issues

---

## Usage

```
/search-issues "credit"
/search-issues BEP-XXX --children
/search-issues --sprint current --assignee me
/search-issues --jql "project = BEP AND status = 'In Progress'"
```

---

## Three Phases

### Phase 1: Parse Search Criteria

**Goal:** ทำความเข้าใจ search intent

**Actions:**
1. ตรวจสอบ input type:
   - Keyword → `summary ~ "keyword"`
   - Issue key → `key = BEP-XXX`
   - `--children` flag → `parent = BEP-XXX`
   - `--jql` → Use raw JQL
   - Filters → Build JQL

2. Build JQL query

**Common Patterns:**

| Input | Generated JQL |
|-------|---------------|
| `"credit"` | `project = BEP AND summary ~ "credit"` |
| `BEP-123` | `key = BEP-123` |
| `BEP-123 --children` | `parent = BEP-123` |
| `--sprint current` | `project = BEP AND sprint IN openSprints()` |
| `--assignee me` | `project = BEP AND assignee = currentUser()` |
| `--status "In Progress"` | `project = BEP AND status = "In Progress"` |
| `--type Story` | `project = BEP AND type = Story` |

**Output:** JQL query string

---

### Phase 2: Execute Search

**Goal:** ดึงข้อมูลจาก Jira

**Actions:**
1. Execute via MCP:
   ```
   MCP: jira_search(jql: "[generated JQL]", limit: 20)
   ```

2. Handle results:
   - Found → Continue to Phase 3
   - Empty → Suggest broader search
   - Error → Check JQL syntax

**Output:** Raw search results

---

### Phase 3: Display Results

**Goal:** แสดงผลลัพธ์

**Actions:**
1. Format results as table:

```markdown
## Search Results

**Query:** `project = BEP AND summary ~ "credit"`
**Found:** 5 issues

| Key | Type | Summary | Status | Assignee |
|-----|------|---------|--------|----------|
| BEP-123 | Story | Credit top-up feature | In Progress | @john |
| BEP-124 | Sub-task | [BE] - Credit API | To Do | - |
| BEP-125 | Sub-task | [FE-Admin] - Credit UI | In Progress | @jane |

### Quick Actions
- View issue: `MCP: jira_get_issue(issue_key: "BEP-XXX")`
- View children: `/search-issues BEP-XXX --children`
```

2. If single result → offer to show details
3. If child search → group by parent

**Output:** Formatted table

---

## Filter Options

| Flag | Description | Example |
|------|-------------|---------|
| `--sprint` | Filter by sprint | `--sprint current`, `--sprint "Sprint 5"` |
| `--assignee` | Filter by assignee | `--assignee me`, `--assignee "john@email.com"` |
| `--status` | Filter by status | `--status "In Progress"` |
| `--type` | Filter by type | `--type Story`, `--type Sub-task` |
| `--label` | Filter by label | `--label BE`, `--label "FE-Admin"` |
| `--children` | Find sub-tasks | `BEP-XXX --children` |
| `--jql` | Raw JQL query | `--jql "custom query"` |
| `--limit` | Max results | `--limit 50` (default: 20) |

---

## Use Cases

### Before Creating Story
```
/search-issues "credit top-up"
```
- ป้องกันสร้าง story ซ้ำ
- หา existing work

### Review Sub-tasks
```
/search-issues BEP-123 --children
```
- ดู sub-tasks ทั้งหมดของ story
- Check coverage

### My Sprint Work
```
/search-issues --sprint current --assignee me
```
- ดูงานที่ต้องทำ
- Track progress

### Find Blockers
```
/search-issues --jql "project = BEP AND priority = Highest AND status != Done"
```
- หางานด่วน
- Prioritize

---

## Error Recovery

| Error | Solution |
|-------|----------|
| JQL syntax error | ตรวจสอบ operators และ field names |
| No results | ลอง keyword กว้างขึ้น หรือลด filters |
| Permission denied | ตรวจสอบ project access |
| Timeout | ลด limit หรือ narrow search |

---

## Related

- JQL patterns: `shared-references/jql-quick-ref.md`
- After finding: `/analyze-story BEP-XXX`

---

## References

- [JQL Quick Reference](../shared-references/jql-quick-ref.md)
- [Tool Selection](../shared-references/tools.md)
