# Jira Generator - Claude Project Instructions

> **Version:** 2.3 | **Updated:** 2026-01-22

---

## Overview

Agile Documentation System สำหรับ **Tathep Platform** - สร้าง Epics, User Stories, และ Sub-tasks ผ่าน Jira/Confluence

---

## Quick Start

| ต้องการ | Prompt | Output |
| --- | --- | --- |
| สร้าง Epic | `prompts/01-senior-product-manager.md` | Epic + Epic Doc |
| สร้าง User Story | `prompts/02-senior-product-owner.md` | User Story |
| วิเคราะห์ Story | `prompts/03-senior-technical-analyst.md` | Sub-tasks + Technical Note |
| Update Sub-task | `prompts/04-update-subtask.md` | Updated Sub-task |
| สร้าง Test Plan | `prompts/05-senior-qa-analyst.md` | Test Plan + [QA] Sub-tasks |

---

## Workflow Chain

```
Stakeholder → PM → PO → TA → QA
              │     │     │     │
              ↓     ↓     ↓     ↓
           Epic   Story  Sub-tasks  Test Cases
```

### Handoff Flow

```
1. PM creates Epic → hands off to PO
2. PO creates User Stories → hands off to TA
3. TA creates Sub-tasks → hands off to QA
4. QA creates Test Plan + [QA] Sub-tasks (terminal)
```

Each role uses **Handoff Protocol** to pass context clearly.

---

## Project Settings

| Setting | Value |
| --- | --- |
| Jira Site | `100-stars.atlassian.net` |
| Project Key | `BEP` |
| Confluence Space | `BEP` |

See `references/shared-config.md` for complete settings.

---

## File Structure

```
jira-generator/
├── CLAUDE.md                    ← You are here
├── prompts/
│   ├── 01-senior-product-manager.md    ← Epic (PM)
│   ├── 02-senior-product-owner.md      ← User Story (PO)
│   ├── 03-senior-technical-analyst.md  ← Sub-task (TA)
│   ├── 04-update-subtask.md            ← Update existing sub-tasks
│   └── 05-senior-qa-analyst.md         ← Test Plan (QA)
├── references/                  ← Load when needed
│   ├── shared-config.md        ← Project settings, tools
│   ├── templates.md            ← All templates
│   └── checklists.md           ← All quality checklists
├── confluence-templates/
│   ├── 01-epic-doc.md
│   ├── 02-technical-note.md
│   └── 03-test-plan.md
├── jira-templates/
│   ├── 01-epic.md
│   ├── 02-user-story.md
│   ├── 03-sub-task.md
│   └── 04-qa-test-case.md
└── tasks/                       ← Task outputs
```

---

## Role Selection

| Trigger | Role | Prompt |
| --- | --- | --- |
| "สร้าง epic", "product vision", "RICE", "PRD" | PM | `01-senior-product-manager.md` |
| "สร้าง user story", "sprint planning", "backlog" | PO | `02-senior-product-owner.md` |
| "วิเคราะห์ story", "สร้าง sub-task", "BEP-XXX" | TA | `03-senior-technical-analyst.md` |
| "update sub-task", "แก้ sub-task" | TA | `04-update-subtask.md` |
| "สร้าง test plan", "QA", "test coverage", "test case" | QA | `05-senior-qa-analyst.md` |

---

## References

โหลดเมื่อต้องการ detail:

| Need | File |
| --- | --- |
| Project settings, tools | `references/shared-config.md` |
| Templates (PM/PO/TA/QA) | `references/templates.md` |
| Quality checklists | `references/checklists.md` |

---

## Core Principles

1. **Slim prompts** - Core instructions only, details in references
2. **Clear handoffs** - Each role passes structured context to next
3. **INVEST compliance** - All items pass INVEST criteria
4. **Traceability** - Everything links back to parent (Story→Epic, Sub-task→Story)

---

## Usage Examples

### Create Epic
```
User: สร้าง epic สำหรับ User Authentication
Claude: [Loads prompts/01-senior-product-manager.md]
        → Creates Epic in Jira (BEP-xxx)
        → Creates Epic Doc in Confluence
        → Hands off context to PO
```

### Create User Story
```
User: สร้าง user story จาก BEP-123
Claude: [Loads prompts/02-senior-product-owner.md]
        → Reads Epic from Jira
        → Creates User Stories (BEP-124, BEP-125, ...)
        → Hands off context to TA
```

### Create Sub-tasks
```
User: วิเคราะห์ BEP-124
Claude: [Loads prompts/03-senior-technical-analyst.md]
        → Analyzes User Story
        → Creates Sub-tasks with [BE]/[FE] tags
        → Creates Technical Note in Confluence
```

### Create Test Plan
```
User: สร้าง test plan จาก BEP-124
Claude: [Loads prompts/05-senior-qa-analyst.md]
        → Analyzes User Story ACs
        → Creates Test Plan in Confluence
        → Creates [QA] Sub-tasks in Jira
```

---

## Troubleshooting

| Issue | Solution |
| --- | --- |
| MCP tool not found | Check `references/shared-config.md` for correct tool names |
| Wrong project key | Ensure using `BEP` project key |
| Missing parent link | Always specify parent Epic/Story when creating |
| Template mismatch | Reference `jira-templates/` for current formats |
| AC format wrong | Use Given-When-Then format per checklist |

### Common Errors

| Error | Cause | Fix |
| --- | --- | --- |
| "Issue not found" | Wrong issue key | Verify key format: `BEP-XXX` |
| "Permission denied" | Atlassian auth | Re-authenticate MCP |
| "Invalid field" | Wrong issue type | Check issue type in project |

---

## MCP Tools

| Tool | Use |
| --- | --- |
| Atlassian | Jira/Confluence operations |
| Repomix | Local codebase (primary) |
| Github | Remote codebase (fallback) |

See `references/shared-config.md` for details.


<claude-mem-context>
# Recent Activity

<!-- This section is auto-generated by claude-mem. Edit content outside the tags. -->

*No recent activity*
</claude-mem-context>