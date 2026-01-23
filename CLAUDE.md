# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Overview

Agile Documentation System for **Tathep Platform** - Create Epics, User Stories, and Sub-tasks via Jira/Confluence

## Project Settings

| Setting | Value |
| --- | --- |
| Jira Site | `100-stars.atlassian.net` |
| Project Key | `BEP` |
| Confluence Space | `BEP` |

## Quick Start

| Task | Prompt | Output |
| --- | --- | --- |
| Create Epic | `prompts/01-senior-product-manager.md` | Epic + Epic Doc |
| Create User Story | `prompts/02-senior-product-owner.md` | User Story |
| Analyze Story | `prompts/03-senior-technical-analyst.md` | Sub-tasks + Technical Note |
| Update Sub-task | `prompts/04-update-subtask.md` | Updated Sub-task |
| Create Test Plan | `prompts/05-senior-qa-analyst.md` | Test Plan + [QA] Sub-tasks |

## Workflow Chain

```
Stakeholder → PM → PO → TA → QA
              │     │     │     │
              ↓     ↓     ↓     ↓
           Epic   Story  Sub-tasks  Test Cases
```

Each role uses **Handoff Protocol** to pass context to next:
1. PM creates Epic → hands off to PO
2. PO creates User Stories → hands off to TA
3. TA creates Sub-tasks → hands off to QA
4. QA creates Test Plan + [QA] Sub-tasks (terminal)

## Role Selection

| Trigger | Role | Prompt |
| --- | --- | --- |
| "create epic", "product vision", "RICE", "PRD" | PM | `01-senior-product-manager.md` |
| "create user story", "sprint planning", "backlog" | PO | `02-senior-product-owner.md` |
| "analyze story", "create sub-task", "BEP-XXX" | TA | `03-senior-technical-analyst.md` |
| "update sub-task", "edit sub-task" | TA | `04-update-subtask.md` |
| "create test plan", "QA", "test coverage", "test case" | QA | `05-senior-qa-analyst.md` |

## Service Tags

| Tag | Service | Local Path |
| --- | --- | --- |
| `[BE]` | Backend | `~/Codes/Works/tathep/tathep-platform-api` |
| `[FE-Admin]` | Admin | `~/Codes/Works/tathep/tathep-admin` |
| `[FE-Web]` | Website | `~/Codes/Works/tathep/tathep-website` |

## Atlassian Tool Selection

### Jira Issue Create/Update - Always Use ADF

> **IMPORTANT:** When creating or updating Jira issues, **always use ADF format via `acli --from-json`**
>
> MCP tools (jira_create_issue, jira_update_issue) convert markdown to wiki format which doesn't render as nicely as ADF

| Operation | Command | Note |
| --- | --- | --- |
| **Create issue** | `acli jira workitem create --from-json issue.json` | ADF description |
| **Update issue** | `acli jira workitem edit --from-json issue.json --yes` | ADF description |
| **Simple field update** | MCP `jira_update_issue` | Does not touch description |

### Other Tools

| Scenario | Tool | Reason |
| --- | --- | --- |
| **Search issues/pages** | MCP `jira_search` or `confluence_search` | Fast |
| **Read issue details** | MCP `jira_get_issue` | Full data |
| **Read Confluence page** | MCP `confluence_get_page` | Returns markdown |
| **Create Confluence page** | MCP `confluence_create_page` | Accepts markdown, converts to storage format |
| **Bulk Jira operations** | `acli` + `--jql` flag | Supports bulk edit |

### Decision Flow

```
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
    └─ Confluence page
          ├─ Read  → MCP confluence_get_page
          └─ Create/Update → MCP confluence_create_page (markdown OK)
```

### ADF JSON Structure

```json
{
  "issues": ["BEP-XXX"],
  "projectKey": "BEP",
  "type": "Subtask",
  "parent": "BEP-YYY",
  "summary": "[TAG] - Title",
  "description": {
    "type": "doc",
    "version": 1,
    "content": [
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "Section"}]},
      {"type": "paragraph", "content": [{"type": "text", "text": "Normal "}, {"type": "text", "text": "bold", "marks": [{"type": "strong"}]}]},
      {"type": "rule"},
      {"type": "table", "attrs": {"isNumberColumnEnabled": false, "layout": "default"}, "content": [...]},
      {"type": "blockquote", "content": [{"type": "paragraph", "content": [...]}]},
      {"type": "bulletList", "content": [{"type": "listItem", "content": [{"type": "paragraph", "content": [...]}]}]}
    ]
  }
}
```

**Commands:**
```bash
# Create new issue
acli jira workitem create --from-json issue.json

# Update existing issue (requires "issues": ["BEP-XXX"] in JSON)
acli jira workitem edit --from-json issue.json --yes
```

See `atlassian-cli` skill for detailed ADF format reference.

## MCP Tools

| Tool | Use |
| --- | --- |
| `jira_search` | Search Jira issues with JQL |
| `jira_get_issue` | Read issue details |
| `jira_update_issue` | Update fields (excluding description) |
| `confluence_search` | Search Confluence pages |
| `confluence_get_page` | Read Confluence page |
| `confluence_create_page` | Create Confluence page (markdown OK) |

> **WARNING:** Do not use `jira_create_issue` or `jira_update_issue` for description field.
> It converts to wiki format which doesn't render nicely. Use `acli --from-json` instead.

Codebase: Local first (Repomix MCP), GitHub fallback (Github MCP)

## File Structure

```
prompts/              # Role-specific prompts (load one per task)
├── 01-senior-product-manager.md    → Epic creation
├── 02-senior-product-owner.md      → User Story creation
├── 03-senior-technical-analyst.md  → Sub-task breakdown
├── 04-update-subtask.md            → Sub-task updates
└── 05-senior-qa-analyst.md         → Test Plan + QA tasks

references/           # Shared resources (load on demand)
├── shared-config.md  → Project settings, MCP tools
├── templates.md      → All Jira/Confluence templates
└── checklists.md     → Quality validation checklists

jira-templates/       # Issue formats
confluence-templates/ # Page formats
tasks/                # Generated outputs (gitignored)
```

## References (load when needed)

| Need | File |
| --- | --- |
| Complete project settings | `references/shared-config.md` |
| All templates | `references/templates.md` |
| Quality checklists | `references/checklists.md` |

## Core Principles

1. **Slim prompts** - Core instructions only, details in references
2. **Clear handoffs** - Each role passes structured context to next
3. **INVEST compliance** - All items pass INVEST criteria
4. **Traceability** - Everything links back to parent (Story→Epic, Sub-task→Story)

## Troubleshooting

| Issue | Solution |
| --- | --- |
| Description renders as ugly wiki format | Use `acli --from-json` with ADF format instead of MCP |
| `acli` error: unknown field | Check JSON structure (use `projectKey` not `project`, use `issues` array for edit) |
| MCP tool not found | Check `references/shared-config.md` for correct tool names |
| Wrong project key | Ensure using `BEP` project key |
| Missing parent link | Always specify parent Epic/Story when creating subtask |
| "Issue not found" | Verify key format: `BEP-XXX` |
| "Permission denied" | Re-authenticate MCP |
