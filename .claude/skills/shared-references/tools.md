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
          ├─ Create (no code) → MCP confluence_create_page
          ├─ Create (with code) → Python script
          ├─ Update content → Python script
          ├─ Move page → Python script
          └─ Add macros (ToC, Children) → Python script
```

---

## Tool Reference

### Jira Operations

| Operation | Tool | Command/Syntax |
| --- | --- | --- |
| **Search issues** | MCP | `jira_search(jql: "project = BEP AND ...")` |
| **Get issue details** | MCP | `jira_get_issue(issue_key: "BEP-XXX", fields: "summary,status,description")` |

> ⚠️ **IMPORTANT:** ใช้ `fields` parameter เสมอเพื่อป้องกัน token limit error!
>
> ```python
> # ❌ Bad - อาจเกิน token limit ถ้า issue มีข้อมูลเยอะ
> jira_get_issue(issue_key="BEP-XXX")
>
> # ✅ Good - ระบุ fields ที่ต้องการ
> jira_get_issue(
>     issue_key="BEP-XXX",
>     fields="summary,status,description,issuetype,parent",
>     comment_limit=5
> )
> ```

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
| **Create page (simple)** | MCP | `confluence_create_page(space_key: "BEP", ...)` |
| **Create page (code blocks)** | Script | `python3 .claude/skills/atlassian-scripts/scripts/create_confluence_page.py` |
| **Update content** | Script | `python3 .claude/skills/atlassian-scripts/scripts/create_confluence_page.py --page-id` |
| **Find/Replace text** | Script | `python3 .claude/skills/atlassian-scripts/scripts/update_confluence_page.py` |
| **Move page** | Script | `python3 .claude/skills/atlassian-scripts/scripts/move_confluence_page.py` |
| **Add macros (ToC, Children)** | Script | `python3 .claude/skills/atlassian-scripts/scripts/update_page_storage.py` |

> ⚠️ **IMPORTANT:** MCP `confluence_create_page` และ `confluence_update_page` มีข้อจำกัด:
>
> - Code blocks จะ render ผิด (ไม่เป็น syntax highlight)
> - Macros (ToC, Children, Status) จะ render เป็น text แทน
> - ใช้ Python scripts ใน `.claude/skills/atlassian-scripts/scripts/` แทน

### Confluence Scripts Decision Flow

```text
ต้องการทำอะไร?
    │
    ├─ สร้าง page ใหม่ (ไม่มี code)
    │     └─ MCP confluence_create_page
    │
    ├─ สร้าง page ใหม่ (มี code blocks)
    │     └─ create_confluence_page.py --space --title
    │
    ├─ Update content ทั้งหมด
    │     └─ create_confluence_page.py --page-id --content-file
    │
    ├─ Find/Replace text
    │     └─ update_confluence_page.py --find --replace
    │
    ├─ Move page(s) to new parent
    │     └─ move_confluence_page.py --page-id(s) --parent-id
    │
    └─ Add macros (ToC, Children, Status)
          └─ update_page_storage.py --page-id --content-file
```

**Script Location:** `.claude/skills/atlassian-scripts/scripts/`

**Full Documentation:** `.claude/skills/atlassian-scripts/SKILL.md`

### Codebase Exploration

| Operation | Tool | Syntax |
| --- | --- | --- |
| **Deep exploration** | Task | `Task(subagent_type: "Explore", prompt: "...")` |
| **Quick file search** | Glob | `Glob(pattern: "**/*.tsx")` |
| **Code search** | Grep | `Grep(pattern: "functionName")` |
| **Read file** | Read | `Read(file_path: "/path/to/file")` |

---

## ADF JSON Structure

> ⚠️ **CRITICAL:** CREATE และ EDIT ใช้ JSON format ที่ต่างกัน - ห้ามใช้สลับกัน!

### Create New Issue (`acli jira workitem create`)

| Field | Required | Notes |
| --- | --- | --- |
| `projectKey` | ✅ | เช่น `"BEP"` |
| `type` | ✅ | `"Epic"`, `"Story"` (ไม่รวม Subtask - ดูด้านล่าง) |
| `summary` | ✅ | Issue title |
| `description` | ✅ | ADF content |
| ~~`issues`~~ | ❌ | ห้ามใช้! |
| ~~`parent`~~ | ❌ | ไม่รองรับ! ใช้ Two-Step Workflow แทน |

> ⚠️ **CRITICAL: Subtask Creation**
>
> `acli jira workitem create` **ไม่รองรับ `parent` field!**
>
> ต้องใช้ **Two-Step Workflow** สำหรับ Subtask:
>
> 1. สร้าง shell ด้วย MCP: `jira_create_issue(issue_type="Subtask", additional_fields={parent:{key:"BEP-XXX"}})`
> 2. Update description ด้วย: `acli jira workitem edit --from-json ... --yes`

**Epic/Story CREATE Example:**

```json
{
  "projectKey": "BEP",
  "type": "Story",
  "summary": "[Feature] - Title",
  "description": {
    "type": "doc",
    "version": 1,
    "content": [...]
  }
}
```

### Update Existing Issue (`acli jira workitem edit`)

| Field | Required | Notes |
| --- | --- | --- |
| `issues` | ✅ | Array of issue keys เช่น `["BEP-XXX"]` |
| `description` | ✅ | ADF content |
| ~~`projectKey`~~ | ❌ | ห้ามใช้! Error: unknown field |
| ~~`type`~~ | ❌ | ห้ามใช้! |
| ~~`summary`~~ | ❌ | ห้ามใช้! (ใช้ MCP แทนถ้าต้องการ update) |

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

# Sub-tasks of a story (without ORDER BY)
parent = BEP-XXX

# Sub-tasks of a story (with ORDER BY - use "Parent Link")
"Parent Link" = BEP-XXX ORDER BY created DESC

# Recently updated
project = BEP AND updated >= -7d ORDER BY updated DESC

# By status
project = BEP AND status = "In Progress"

# By assignee
project = BEP AND assignee = currentUser()

# Epics only
project = BEP AND issuetype = Epic
```

> ⚠️ **JQL Gotcha:** `parent = BEP-XXX ORDER BY...` จะเกิด error!
> ใช้ `"Parent Link" = BEP-XXX ORDER BY...` แทน
