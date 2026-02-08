---
name: atlassian-scripts
description: |
  Python scripts for updating Confluence pages and Jira issues via REST API directly.
  Use when MCP tools have limitations (e.g., code macro formatting, ADF manipulation).

  Triggers: "fix confluence", "update confluence page", "confluence script", "fix jira description", "atlassian script"
argument-hint: "[script-name] [args]"
---

# Atlassian Scripts

**Role:** Developer / Tech Lead
**Output:** Created/Updated Confluence Pages & Jira Issues
**Version:** 4.0.0 (+ ADF validator, write wrapper, verify, workflow state)

## Architecture

```text
atlassian-scripts/
├── __init__.py              # Package marker
├── lib/                     # Shared library modules
│   ├── __init__.py          # Public exports
│   ├── exceptions.py        # Custom exceptions (Confluence + Jira + Validation)
│   ├── auth.py              # SSL, credentials, auth
│   ├── api.py               # ConfluenceAPI class
│   ├── jira_api.py          # JiraAPI class (REST v3, ADF)
│   ├── converters.py        # Content converters
│   ├── adf_validator.py     # ADF quality gate engine (HR1)
│   └── workflow_state.py    # Workflow state + prerequisites
└── scripts/                 # CLI scripts
    ├── create_confluence_page.py
    ├── update_confluence_page.py
    ├── move_confluence_page.py
    ├── update_page_storage.py
    ├── fix_confluence_code_blocks.py
    ├── audit_confluence_pages.py
    ├── update_jira_description.py
    ├── validate_adf.py          # Script 8: ADF validator (HR1)
    ├── verify_write.py          # Script 9: Post-write verifier (HR3/HR5/HR6)
    ├── jira_write.py            # Script 10: Write wrapper (HR1/HR3/HR5/HR6)
    └── workflow_checkpoint.py   # Script 11: Workflow state CLI
```

### Module Responsibilities (SRP)

| Module | Responsibility |
| --- | --- |
| `exceptions.py` | Domain-specific exceptions (Confluence + Jira + Validation) |
| `auth.py` | Authentication (SSL, credentials, auth header) |
| `api.py` | HTTP/API operations via ConfluenceAPI class |
| `jira_api.py` | Jira REST API v3 client (ADF manipulation) |
| `converters.py` | Content transformation (markdown, code blocks) |
| `adf_validator.py` | ADF quality gate engine — 25+ checks, scoring, auto-fix (HR1) |
| `workflow_state.py` | Workflow state management — phase tracking, prerequisites |

---

## Available Scripts

| Script | Description | Use Case |
| --- | --- | --- |
| `create_confluence_page.py` | Create/Update page with proper code blocks | Create or update pages containing code |
| `update_confluence_page.py` | Find/Replace text in a page | Batch text replacement |
| `move_confluence_page.py` | Move page(s) to new parent | Reorganize page hierarchy |
| `update_page_storage.py` | Update page with raw storage format | Pages requiring macros (ToC, Children) |
| `fix_confluence_code_blocks.py` | Fix code blocks that render incorrectly | Fix broken code formatting |
| `audit_confluence_pages.py` | Verify content across multiple pages | Alignment verification |
| `update_jira_description.py` | Find/Replace text in Jira ADF descriptions | Fix Jira issue descriptions |
| `validate_adf.py` | Validate ADF JSON against quality gate (HR1) | Before creating/updating issues |
| `verify_write.py` | Verify Jira writes took effect (HR3/HR5/HR6) | After creating subtasks, assigning |
| `jira_write.py` | Write wrapper: validate → create → verify → assign | Create subtask, update description |
| `workflow_checkpoint.py` | Track workflow phases + prerequisite enforcement | Multi-step skill workflows |

---

## Prerequisites

**Credentials:** `~/.config/atlassian/.env`

```env
CONFLUENCE_URL=https://{{JIRA_SITE}}/wiki
CONFLUENCE_USERNAME=your-email@example.com
CONFLUENCE_API_TOKEN=your-api-token
```

---

## Script Selection Guide

```text
What do you need to do?
    │
    ├─ Create a new page
    │     └─ create_confluence_page.py --space --title
    │
    ├─ Update entire content
    │     └─ create_confluence_page.py --page-id --content-file
    │
    ├─ Find/Replace text
    │     └─ update_confluence_page.py --find --replace
    │
    ├─ Move page(s) to new parent
    │     └─ move_confluence_page.py --page-id(s) --parent-id
    │
    ├─ Add macros (ToC, Children, Status)
    │     └─ update_page_storage.py --page-id --content-file
    │
    ├─ Fix broken code blocks
    │     └─ fix_confluence_code_blocks.py --page-id(s)
    │
    ├─ Verify content alignment
    │     └─ audit_confluence_pages.py --config audit.json
    │
    ├─ Fix Jira issue descriptions (ADF)
    │     └─ update_jira_description.py --config fixes.json
    │
    ├─ Validate ADF before Jira write (HR1)
    │     └─ validate_adf.py tasks/story.json --type story [--fix]
    │
    ├─ Verify writes took effect (HR3/HR5/HR6)
    │     └─ verify_write.py BEP-1234 --check parent,assignee
    │
    ├─ Create subtask (full pipeline)
    │     └─ jira_write.py create-subtask --parent BEP-1200 --adf tasks/sub.json
    │
    └─ Track workflow state
          └─ workflow_checkpoint.py start story-full BEP-1200
```

---

## When to Use Scripts vs MCP

> **🚨 CRITICAL:** MCP Confluence tools have TWO limitations that cause macros to fail:
>
> 1. **Storage format** → MCP HTML-escapes `<ac:` tags, macros render as raw text
> 2. **Code blocks** → MCP renders as `<pre>` instead of Confluence macro
>
> **Rule:** If your page contains ANY macros (Jira, expand, info panel, ToC, children) → **ALWAYS use Python scripts**

| Scenario | Tool | Why |
| --- | --- | --- |
| Simple page read | MCP `confluence_get_page` | Fast, no script needed |
| Page create/update (no code, no macros) | MCP `confluence_create_page` / `update_page` | Markdown works fine |
| Page create/update (with code) | MCP + `fix_confluence_code_blocks.py` | MCP renders code as `<pre>`, fix script converts |
| **Page with Jira macros / panels** | **Script** `update_page_storage.py` | ⚠️ MCP escapes XML → macros render as text |
| **Page with expand / ToC / children** | **Script** `update_page_storage.py` | ⚠️ MCP escapes XML → macros render as text |
| Batch text replacement | **Script** `update_confluence_page.py` | More reliable |
| Fix broken code blocks | **Script** `fix_confluence_code_blocks.py` | Post-step after MCP create/update |
| Issue linking (Blocks/Relates) | MCP `jira_create_issue_link` | Bidirectional links between issues |
| Web links (Figma/Confluence) | MCP `jira_create_remote_issue_link` | Add external links to issue Links section |
| Move issues to backlog / sprint mgmt | **Script** via `JiraAPI._request()` | MCP not supported — use Agile REST API + **numeric IDs** |

> **⚠️ Known Issue (Code Blocks):** MCP `confluence_create_page` / `confluence_update_page` with `content_format: 'markdown'`
> renders code blocks as `<pre class="highlight">` instead of Confluence `<ac:structured-macro>`.
> **You must always run `fix_confluence_code_blocks.py --page-id` after any MCP create/update that contains code blocks.**
>
> **⚠️ Known Issue (Storage Format/Macros):** MCP with `content_format: 'storage'` HTML-escapes the content.
> `<ac:structured-macro>` becomes `&lt;ac:structured-macro&gt;` and renders as plain text instead of a macro.
> **For ANY page with macros (Jira tables, panels, expand, ToC), use `update_page_storage.py` directly.**

---

---

## Supporting Files

> Load only when needed -- no need to load everything on invoke.

| File | Content | Load When |
| --- | --- | --- |
| [script-reference.md](script-reference.md) | Script 1-11 usage, arguments, examples | After selecting a script, when you need full docs |
| [library-api.md](library-api.md) | ConfluenceAPI, JiraAPI, Converters, Exceptions | When creating a custom script |
| [technical-notes.md](technical-notes.md) | SSL, Storage Format, Mermaid, History | Troubleshooting |

---

## References

- Confluence REST API: <https://developer.atlassian.com/cloud/confluence/rest/v1/intro/>
- Jira REST API v3: <https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/>
- Credentials: `~/.config/atlassian/.env`
- Storage Format: <https://developer.atlassian.com/cloud/confluence/confluence-storage-format/>
- ADF (Atlassian Document Format): <https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/>

---

## Related Skills

| Skill | Description |
| --- | --- |
| `/create-doc` | Create new Confluence page (uses MCP) |
| `/update-doc` | Update existing Confluence page (uses scripts when needed) |
