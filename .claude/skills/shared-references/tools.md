# Tool Selection Guide

## Decision Flow

```text
What do you need?
    │
    ├─ Create/Update Jira issue description
    │     │
    │     └─ Always use acli + --from-json (ADF)
    │           • Create JSON file with ADF content
    │           • acli jira workitem create --from-json issue.json
    │           • acli jira workitem edit --from-json issue.json --yes
    │
    ├─ Update other fields (not description)
    │     └─ MCP jira_update_issue is OK
    │
    ├─ Search Jira/Confluence
    │     └─ MCP jira_search / confluence_search
    │
    ├─ Read Jira issue
    │     └─ MCP jira_get_issue
    │
    ├─ Explore codebase
    │     └─ Task tool with Explore agent
    │
    └─ Confluence page
          ├─ Read  → MCP confluence_get_page
          └─ Create/Update → MCP confluence_create_page (markdown OK)
```

---

## Tool Reference

### Jira Operations

| Operation | Tool | Command/Syntax |
| --- | --- | --- |
| **Search issues** | MCP | `jira_search(jql: "project = BEP AND ...")` |
| **Get issue details** | MCP | `jira_get_issue(issue_key: "BEP-XXX")` |
| **Create issue** | acli | `acli jira workitem create --from-json file.json` |
| **Update description** | acli | `acli jira workitem edit --from-json file.json --yes` |
| **Update other fields** | MCP | `jira_update_issue(issue_key: "BEP-XXX", fields: {...})` |
| **Get transitions** | MCP | `jira_get_transitions(issue_key: "BEP-XXX")` |
| **Transition issue** | MCP | `jira_transition_issue(issue_key: "BEP-XXX", ...)` |

### Confluence Operations

| Operation | Tool | Command/Syntax |
| --- | --- | --- |
| **Search pages** | MCP | `confluence_search(query: "...")` |
| **Get page** | MCP | `confluence_get_page(page_id: "...")` |
| **Create page** | MCP | `confluence_create_page(space_key: "BEP", ...)` |
| **Update page** | MCP | `confluence_update_page(page_id: "...", ...)` |

### Codebase Exploration

| Operation | Tool | Syntax |
| --- | --- | --- |
| **Deep exploration** | Task | `Task(subagent_type: "Explore", prompt: "...")` |
| **Quick file search** | Glob | `Glob(pattern: "**/*.tsx")` |
| **Code search** | Grep | `Grep(pattern: "functionName")` |
| **Read file** | Read | `Read(file_path: "/path/to/file")` |

---

## ADF JSON Structure

### Create New Issue

```json
{
  "projectKey": "BEP",
  "type": "Subtask",
  "parent": "BEP-XXX",
  "summary": "[TAG] - Title",
  "description": {
    "type": "doc",
    "version": 1,
    "content": [...]
  }
}
```

### Update Existing Issue

```json
{
  "issues": ["BEP-XXX"],
  "description": {
    "type": "doc",
    "version": 1,
    "content": [...]
  }
}
```

### Common ADF Elements

**Heading:**

```json
{"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "Title"}]}
```

**Paragraph:**

```json
{"type": "paragraph", "content": [{"type": "text", "text": "Content"}]}
```

**Bold text:**

```json
{"type": "text", "text": "Bold", "marks": [{"type": "strong"}]}
```

**Inline code:**

```json
{"type": "text", "text": "/api/endpoint", "marks": [{"type": "code"}]}
```

**Panel (info/success/warning/error/note):**

```json
{
  "type": "panel",
  "attrs": {"panelType": "success"},
  "content": [
    {"type": "paragraph", "content": [...]}
  ]
}
```

**Bullet list:**

```json
{
  "type": "bulletList",
  "content": [
    {"type": "listItem", "content": [{"type": "paragraph", "content": [...]}]}
  ]
}
```

**Table:**

```json
{
  "type": "table",
  "attrs": {"isNumberColumnEnabled": false, "layout": "default"},
  "content": [
    {"type": "tableRow", "content": [
      {"type": "tableHeader", "content": [{"type": "paragraph", "content": [...]}]},
      {"type": "tableHeader", "content": [{"type": "paragraph", "content": [...]}]}
    ]},
    {"type": "tableRow", "content": [
      {"type": "tableCell", "content": [{"type": "paragraph", "content": [...]}]},
      {"type": "tableCell", "content": [{"type": "paragraph", "content": [...]}]}
    ]}
  ]
}
```

**Rule (horizontal line):**

```json
{"type": "rule"}
```

---

## Common Errors & Solutions

| Error | Cause | Solution |
| --- | --- | --- |
| `INVALID_INPUT` | Nested tables in panels | Use bulletList instead of table in panels |
| `Unknown field` | Wrong JSON field name | Use `projectKey` not `project`, use `issues` array for edit |
| Description renders as wiki | Used MCP for description | Use `acli --from-json` with ADF |
| Issue not found | Wrong key format | Check format is `BEP-XXX` |
| Confluence timeout | Large page content | Split into smaller pages |

---

## acli Commands

```bash
# Create new issue
acli jira workitem create --from-json tasks/bep-xxx.json

# Update existing issue (requires "issues": ["BEP-XXX"] in JSON)
acli jira workitem edit --from-json tasks/bep-xxx.json --yes

# List issues
acli jira workitem list --project BEP --limit 10

# Get issue details
acli jira workitem get BEP-XXX
```

---

## MCP JQL Examples

```text
# All stories in project
project = BEP AND issuetype = Story

# Sub-tasks of a story
parent = BEP-XXX

# Recently updated
project = BEP AND updated >= -7d

# By status
project = BEP AND status = "In Progress"

# By assignee
project = BEP AND assignee = currentUser()

# Epics only
project = BEP AND issuetype = Epic
```
