---
name: search-issues
context: fork
model: haiku
description: |
  Search for existing issues before creating new ones (prevent duplicates) with a 3-phase workflow

  Supports: keyword search, JQL query, filters (sprint, assignee, status, type)

  Triggers: "search", "find", "find issue", "does it already exist"
argument-hint: "[keyword] [--filters]"
---

# /search-issues

**Role:** Any
**Output:** List of matching issues

## Phases

### 1. Parse Search Criteria

| Input | Generated JQL |
| --- | --- |
| `"credit"` | `project = BEP AND summary ~ "credit"` |
| `BEP-123` | `key = BEP-123` |
| `BEP-123 --children` | `parent = BEP-123` |
| `--sprint current` | `sprint IN openSprints()` |
| `--assignee me` | `assignee = currentUser()` |
| `--status "In Progress"` | `status = "In Progress"` |
| `--type Story` | `type = Story` |

### 2. Execute Search

```text
MCP: jira_search(jql: "[generated JQL]", fields: "summary,status,assignee,issuetype,priority", limit: 20)
```

### 2.5 Semantic Similarity Check (keyword search only)

**Skip if:** input is issue key (`BEP-123`), uses `--jql`, or uses `--children` flag.

```text
cache_similar_issues(query: "<keyword>", limit: 5, exclude_keys: [<keys from Phase 2>])
```

Filter results by distance (cosine distance, 0 = identical):

| Distance | Label | Action |
| --- | --- | --- |
| < 0.25 | ⚠️ Likely duplicate | แจ้งเตือนชัดเจน |
| 0.25–0.45 | 🔍 Possibly related | แสดงไว้อ้างอิง |
| > 0.45 | (skip) | noise — ไม่แสดง |

Similarity % = `(1 - distance/2) × 100`

If embeddings not available (sqlite-vec not installed) → skip gracefully, no error.

### 3. Display Results

```text
## Search Results
Query: `project = BEP AND summary ~ "credit"`
Found: 5 issues

| Key | Type | Summary | Status |
|-----|------|---------|--------|
| BEP-123 | Story | Credit feature | In Progress |
| BEP-124 | Sub-task | [BE] Credit API | To Do |

## 🔍 Semantic Matches (BERT similarity)
| Key | Summary | Similarity |
|-----|---------|------------|
| BEP-120 | [BE] เติมเครดิต wallet | ⚠️ 94% (likely duplicate) |
| BEP-118 | Credit payment flow | 🔍 72% (possibly related) |

💡 พบ likely duplicate → ยืนยันก่อนสร้าง issue ใหม่
```

If no semantic matches above threshold → omit the section entirely.

---

## Filter Options

| Flag | Example |
| --- | --- |
| `--sprint` | `--sprint current`, `--sprint "Sprint 5"` |
| `--assignee` | `--assignee me` |
| `--status` | `--status "In Progress"` |
| `--type` | `--type Story` |
| `--label` | `--label BE` |
| `--children` | `{{PROJECT_KEY}}-XXX --children` |
| `--jql` | `--jql "custom query"` |

---

## Use Cases

| Purpose | Command |
| --- | --- |
| Before creating | `/search-issues "credit top-up"` |
| View sub-tasks | `/search-issues BEP-123 --children` |
| My sprint work | `/search-issues --sprint current --assignee me` |

---

## References

- [JQL Quick Reference](../shared-references/jql-quick-ref.md)
