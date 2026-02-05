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

> ⚠️ **IMPORTANT:** Always use the `fields` parameter to prevent token limit errors!
>
> ```python
> # ❌ Bad - may exceed token limit if the issue has too much data
> jira_get_issue(issue_key="BEP-XXX")
>
> # ✅ Good - specify only the fields you need
> jira_get_issue(
>     issue_key="BEP-XXX",
>     fields="summary,status,description,issuetype,parent",
>     comment_limit=5
> )
> ```

| **Create issue** | acli | `acli jira workitem create --from-json file.json` |
| **Update description** | acli | `acli jira workitem edit --from-json file.json --yes` |
| **Update other fields** | MCP | `jira_update_issue(issue_key: "BEP-XXX", fields: {...})` |
| **Assign issue** | acli | `acli jira workitem assign -k "BEP-XXX" -a "email@..." -y` |
| **Create issue link** | MCP | `jira_create_issue_link(link_type: "Relates", inward_issue: "BEP-X", outward_issue: "BEP-Y")` |
| **Get transitions** | MCP | `jira_get_transitions(issue_key: "BEP-XXX")` |
| **Transition issue** | MCP | `jira_transition_issue(issue_key: "BEP-XXX", ...)` |
| **Set dates** | MCP | `jira_update_issue(issue_key: "BEP-XXX", additional_fields: {"customfield_10015": "YYYY-MM-DD", "duedate": "YYYY-MM-DD"})` |
| **Move to sprint** | MCP | `jira_update_issue(issue_key: "BEP-XXX", additional_fields: {"customfield_10020": 640})` |
| **Get sprints** | MCP | `jira_get_sprints_from_board(board_id: "2", state: "future")` |

> **BEP Board/Sprint Info:**
> Board ID: `2` · Sprint IDs: `640` (S32), `673` (S33), `706` (S34), `707` (S35), `708` (S36)
> Date fields: `customfield_10015` (Start date), `duedate` (Due date) · Sprint field: `customfield_10020` (plain number)

> **Issue Link Types (BEP):** `Relates` · `Blocks` · `Duplicate` · `Cloners` · `Test Case`
> ⚠️ ใช้ `"Relates"` ไม่ใช่ `"Relates to"` — ชื่อต้องตรงกับ Jira config
>
> ⚠️ **MCP assignee bug:** `jira_update_issue` assignee field reports success but doesn't update.
> Use `acli jira workitem assign -k "KEY" -a "email" -y` instead.

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

> ⚠️ **IMPORTANT:** MCP `confluence_create_page` and `confluence_update_page` have limitations:
>
> - Code blocks will render incorrectly (no syntax highlighting)
> - Macros (ToC, Children, Status) will render as plain text instead
> - Use the Python scripts in `.claude/skills/atlassian-scripts/scripts/` instead

### Confluence Scripts Decision Flow

```text
What do you need to do?
    │
    ├─ Create new page (no code)
    │     └─ MCP confluence_create_page
    │
    ├─ Create new page (with code blocks)
    │     └─ create_confluence_page.py --space --title
    │
    ├─ Update all content
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

## Effort Sizing

| Size | Description | Action |
| --- | --- | --- |
| S | < 2 days | Single sub-task |
| M | 2-5 days | Single sub-task |
| L | 5-10 days | Consider splitting |
| XL | > 10 days | Must split |

---

## See Also

> Detailed references are in separate files — load when needed

- **ADF format** (CREATE vs EDIT, panels, tables, inline code) → [templates.md](templates.md)
- **JQL patterns** (search, filter, operators) → [jql-quick-ref.md](jql-quick-ref.md)
- **Error recovery** (workflow errors, validation) → [troubleshooting.md](troubleshooting.md)
