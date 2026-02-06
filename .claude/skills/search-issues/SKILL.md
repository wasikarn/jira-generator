---
name: search-issues
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

### 3. Display Results

```text
## Search Results
Query: `project = BEP AND summary ~ "credit"`
Found: 5 issues

| Key | Type | Summary | Status |
|-----|------|---------|--------|
| BEP-123 | Story | Credit feature | In Progress |
| BEP-124 | Sub-task | [BE] Credit API | To Do |
```

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
