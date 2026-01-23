# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Overview

Agile Documentation System สำหรับ **Tathep Platform** - สร้าง Epics, User Stories, และ Sub-tasks ผ่าน Jira/Confluence

## Project Settings

| Setting | Value |
| --- | --- |
| Jira Site | `100-stars.atlassian.net` |
| Project Key | `BEP` |
| Confluence Space | `BEP` |

## Quick Start

| ต้องการ | Prompt | Output |
| --- | --- | --- |
| สร้าง Epic | `prompts/01-senior-product-manager.md` | Epic + Epic Doc |
| สร้าง User Story | `prompts/02-senior-product-owner.md` | User Story |
| วิเคราะห์ Story | `prompts/03-senior-technical-analyst.md` | Sub-tasks + Technical Note |
| Update Sub-task | `prompts/04-update-subtask.md` | Updated Sub-task |
| สร้าง Test Plan | `prompts/05-senior-qa-analyst.md` | Test Plan + [QA] Sub-tasks |

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
| "สร้าง epic", "product vision", "RICE", "PRD" | PM | `01-senior-product-manager.md` |
| "สร้าง user story", "sprint planning", "backlog" | PO | `02-senior-product-owner.md` |
| "วิเคราะห์ story", "สร้าง sub-task", "BEP-XXX" | TA | `03-senior-technical-analyst.md` |
| "update sub-task", "แก้ sub-task" | TA | `04-update-subtask.md` |
| "สร้าง test plan", "QA", "test coverage", "test case" | QA | `05-senior-qa-analyst.md` |

## Service Tags

| Tag | Service | Local Path |
| --- | --- | --- |
| `[BE]` | Backend | `~/Codes/Works/tathep/tathep-platform-api` |
| `[FE-Admin]` | Admin | `~/Codes/Works/tathep/tathep-admin` |
| `[FE-Web]` | Website | `~/Codes/Works/tathep/tathep-website` |

## Atlassian Tool Selection

เลือกใช้เครื่องมือตามความเหมาะสม:

| Scenario | Tool | Reason |
| --- | --- | --- |
| **Rich text description** (tables, panels, code blocks) | `atlassian-cli` skill + `--from-json` | ADF format ต้องใช้ JSON structure |
| **Simple text description** | Atlassian MCP หรือ `acli` | ทั้งสองทำงานได้ |
| **Search issues/pages** | `atlassian:search` MCP | Rovo Search รวดเร็ว |
| **Read Confluence page** | `getConfluencePage` MCP | ได้ content เป็น markdown |
| **Create Confluence page** | `createConfluencePage` MCP | รับ markdown แปลงเป็น storage format |
| **Bulk Jira operations** | `atlassian-cli` skill + JQL | `--jql` flag รองรับ bulk edit |
| **Complex workflows** | `atlassian-mcp` skill | Guided workflow with validation |

### Decision Flow

```
ต้องการทำอะไร?
    │
    ├─ สร้าง/แก้ไข Jira issue
    │     │
    │     ├─ Description มี table/panel/rich format?
    │     │     ├─ Yes → atlassian-cli + --from-json (ADF)
    │     │     └─ No  → Atlassian MCP หรือ acli --description
    │     │
    │     └─ Bulk operation?
    │           ├─ Yes → atlassian-cli + --jql
    │           └─ No  → Atlassian MCP
    │
    ├─ Search Jira/Confluence
    │     └─ atlassian:search MCP (Rovo Search)
    │
    └─ Confluence page
          ├─ Read  → getConfluencePage MCP
          └─ Create/Update → createConfluencePage MCP (markdown OK)
```

### ADF Format (Rich Text)

เมื่อต้องการ rich text ใน Jira description ให้ใช้:

```bash
# 1. สร้าง JSON file กับ ADF content
# 2. ใช้ --from-json flag
acli jira workitem edit --from-json workitem.json --yes
```

ดูรายละเอียด ADF format ได้ที่ `atlassian-cli` skill

## MCP Tools

| Tool | Use |
| --- | --- |
| `Atlassian:search` | ค้นหา Jira/Confluence (Rovo Search) |
| `Atlassian:getConfluencePage` | อ่าน Confluence page |
| `Atlassian:createConfluencePage` | สร้าง Confluence page |
| `Atlassian:getConfluencePageFooterComments` | อ่าน comments |

**Note:** สำหรับ Jira CRUD operations ที่ต้องการ rich text ให้ใช้ `atlassian-cli` skill แทน

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
| MCP tool not found | Check `references/shared-config.md` for correct tool names |
| Wrong project key | Ensure using `BEP` project key |
| Missing parent link | Always specify parent Epic/Story when creating |
| "Issue not found" | Verify key format: `BEP-XXX` |
| "Permission denied" | Re-authenticate MCP |
