# CLAUDE.md

## Overview

Agile Documentation System for **Tathep Platform** - Create Epics, User Stories, and Sub-tasks via Jira/Confluence

## Project Settings

| Setting | Value |
| --- | --- |
| Jira Site | `100-stars.atlassian.net` |
| Project Key | `BEP` |
| Confluence Space | `BEP` |

## Skill Commands

### Create

| Command | Description | Output |
| --- | --- | --- |
| `/create-epic` | Create Epic from product vision | Epic + Epic Doc |
| `/create-story` | Create User Story from requirements | User Story |
| `/create-task` | Create Task (tech-debt, bug, chore, spike) | Task |
| `/analyze-story BEP-XXX` | Analyze Story → Sub-tasks | Sub-tasks + Technical Note |
| `/create-testplan BEP-XXX` | Create Test Plan from Story | [QA] Sub-task |
| `/create-doc` | Create Confluence page (tech-spec, adr, parent) | Confluence Page |

### Update

| Command | Description | Output |
| --- | --- | --- |
| `/update-epic BEP-XXX` | Edit Epic - adjust scope, RICE, metrics | Updated Epic |
| `/update-story BEP-XXX` | Edit User Story - add/edit AC, scope | Updated Story |
| `/update-task BEP-XXX` | Edit Task - migrate format, add details | Updated Task |
| `/update-subtask BEP-XXX` | Edit Sub-task - format, content | Updated Sub-task |
| `/update-doc PAGE-ID` | Update/Move Confluence page | Updated Page |

### Composite (End-to-End Workflow) ⭐

| Command | Description | Output |
| --- | --- | --- |
| `/story-full` | Create Story + Sub-tasks complete workflow in one go | Story + Sub-tasks |
| `/story-cascade BEP-XXX` | Update Story + cascade to related Sub-tasks | Updated Story + Sub-tasks |
| `/sync-alignment BEP-XXX` | Sync all artifacts (Jira + Confluence) bidirectional | Updated issues + pages |
| `/plan-sprint` | Sprint planning: carry-over + prioritize + assign (Tresor-powered) | Sprint plan + Jira assignments |

### Utility

| Command | Description | Output |
| --- | --- | --- |
| `/search-issues` | Search before creating (prevent duplicates) | Matching issues |
| `/verify-issue BEP-XXX` | Verify + improve quality (ADF, INVEST, language) | Report / Fixed issues |
| `/optimize-context` | Audit + compress passive context (global skill) | Updated CLAUDE.md |

> `--with-subtasks` = batch | `--fix` = auto-fix | `--dry-run` = report only

**Skills:** `.claude/skills/[name]/SKILL.md` → phases in order → refs from `shared-references/`

## Workflow Chain

### Skill Selection Guide

```text
Need a new feature?
  ├─ Have nothing yet?           → /create-epic (PM)
  ├─ Have Epic, need Story?      → /create-story (PO)
  ├─ Have Epic, need full flow?  → /story-full ⭐ (PO+TA combined)
  ├─ Have Story, need Sub-tasks? → /analyze-story (TA)
  ├─ Have Story, need tests?     → /create-testplan (QA)
  ├─ Need a Task (bug/chore)?   → /create-task (Dev)
  └─ Need a Confluence page?     → /create-doc (Dev)

Need to update?
  ├─ Update one issue?           → /update-{epic,story,task,subtask}
  ├─ Update Story + Sub-tasks?   → /story-cascade ⭐
  ├─ Sync everything?            → /sync-alignment ⭐
  └─ Update Confluence page?     → /update-doc

Need to plan or verify?
  ├─ Plan a sprint?              → /plan-sprint ⭐
  ├─ Check quality?              → /verify-issue
  └─ Prevent duplicates?         → /search-issues
```

### Handoff + Dependencies

```text
Stakeholder → PM → PO → TA → QA → /verify-issue after each step
               │     │     │     │
               ↓     ↓     ↓     ↓
            Epic   Story  Sub-tasks  Test Plan
                          ↑
            /story-full ⭐ = PO + TA in one go

/search-issues ← always run before creating (prevent duplicates)
       ↓
/create-epic ──→ /create-story ──→ /analyze-story ──→ /create-testplan
                       │                 │
                       └─ /story-full ⭐ ┘  (combines both)
                       └─ /story-cascade ⭐  (update → cascade to subs)
                       └─ /sync-alignment ⭐ (sync all: Jira + Confluence)

/create-task, /create-doc, /update-doc ── (standalone)
/plan-sprint ⭐ ───────────────────────── (reads Jira, assigns work)
/verify-issue ← always run after creating/updating
```

### Common Skill Mistakes

| Mistake | Correct |
| --- | --- |
| `/create-story` + `/analyze-story` separately | Use `/story-full` ⭐ — does both in one go |
| `/analyze-story` without Explore | Sub-tasks will have generic paths — always Explore first |
| Creating without `/search-issues` | May create duplicates — always search first |
| `/update-story` when Sub-tasks also need changes | Use `/story-cascade` ⭐ to cascade automatically |
| `/story-cascade` when Confluence also needs sync | Use `/sync-alignment` ⭐ for full bidirectional sync |

### Phase Patterns

| Pattern | Phases | Used By |
| --- | --- | --- |
| 3-phase (Search) | Parse → Search → Present | search-issues |
| 4-phase (Create Simple) | Discovery → Design → Create → Summary | create-doc |
| 5-phase (Standard) | Discovery → Write → Validate → Create → Summary | create-{epic,story,task}, update-* |
| 5-phase (QA) | Discovery → Scope → Design → Create → Summary | create-testplan |
| 6-phase (Verify) | Fetch → Technical → Quality → Hierarchy → Score → Fix | verify-issue |
| 7-phase (Analyze) | Discovery → Impact → **Explore** → Design → Align → Create → Summary | analyze-story |
| 8-phase (Cascade) | Fetch → Changes → Impact → Explore → Gen Story → Gen Subs → Apply → Summary | story-cascade, sync-alignment |
| 8-phase (Sprint) | Discovery → Capacity → Carry-over → Prioritize → Distribute → Risk → Review → Execute | plan-sprint |
| 10-phase (Full) | Discovery → Write → INVEST → Create → Impact → **Explore** → Design → Align → Create Subs → Summary | story-full |

> **Bold Explore** = mandatory codebase exploration step (uses `Task(Explore)`)

## Service Tags

| Tag | Service | Local Path |
| --- | --- | --- |
| `[BE]` | Backend | `~/Codes/Works/tathep/tathep-platform-api` |
| `[FE-Admin]` | Admin | `~/Codes/Works/tathep/tathep-admin` |
| `[FE-Web]` | Website | `~/Codes/Works/tathep/tathep-website` |

## Passive Context (Always Loaded)

> Compressed from `shared-references/` — load full templates only when needed

### Tool Selection

> **IMPORTANT:** Jira descriptions must always use ADF format via `acli --from-json` (MCP converts to ugly wiki format)

| Operation | Tool | Note |
| --- | --- | --- |
| **Create/Update Jira description** | `acli --from-json` (ADF) | Create JSON file → `acli jira workitem create/edit` |
| **Update fields (not description)** | MCP `jira_update_issue` | summary, status, labels, etc. |
| **Read issue** | MCP `jira_get_issue` | **Must always use `fields` parameter** to prevent token limit |
| **Search Jira** | MCP `jira_search` | JQL query |
| **Confluence read** | MCP `confluence_get_page` | |
| **Confluence create/update (with code)** | Python scripts | `.claude/skills/atlassian-scripts/scripts/` |
| **Confluence (move/macros)** | Python scripts | move, ToC, Children macros |

**jira_get_issue — must specify `fields` param** (without → token limit error):

| Use Case | Fields |
| --- | --- |
| Quick check | `summary,status,assignee` |
| Read description | `summary,status,description` |
| Full analysis | `summary,status,description,issuetype,parent,labels` |

### ADF Quick Reference

**CREATE vs EDIT — JSON formats differ (do not interchange!):**

| Operation | Required | Forbidden |
| --- | --- | --- |
| **CREATE** `acli jira workitem create` | `projectKey`, `type`, `summary`, `description` | `issues` |
| **EDIT** `acli jira workitem edit` | `issues`, `description` | `projectKey`, `type`, `summary`, `parent` |

```json
// CREATE
{"projectKey":"BEP","type":"Story","summary":"...","description":{"type":"doc","version":1,"content":[...]}}
// EDIT
{"issues":["BEP-XXX"],"description":{"type":"doc","version":1,"content":[...]}}
```

**Subtask — Two-Step Workflow** (acli does not support `parent` field):

1. MCP create shell: `jira_create_issue({project_key:"BEP", summary:"...", issue_type:"Subtask", additional_fields:{parent:{key:"BEP-XXX"}}})`
2. acli edit description: `acli jira workitem edit --from-json subtask.json --yes`

**Panel Types:**

| Type | Color | Usage |
| --- | --- | --- |
| `info` | Blue | Story narrative, objective |
| `success` | Green | Happy path AC |
| `warning` | Yellow | Edge cases, validation |
| `error` | Red | Error handling |
| `note` | Purple | Notes, dependencies |

**Table Header Colors (semantic):**

| Category | Hex |
| --- | --- |
| Default/header | `#f4f5f7` |
| New files | `#e3fcef` (green) |
| Modify files | `#fffae6` (yellow) |
| Delete files | `#ffebe6` (red) |
| Reference | `#eae6ff` (purple) |
| Requirements | `#deebff` (blue) |

**AC Format:** panels + Given/When/Then (always required) → Happy=`success`, Edge=`warning`, Error=`error`

**Inline code:** `{"type":"text","text":"path/file.ts","marks":[{"type":"code"}]}`

### Common Mistakes & Quick Fixes

| Mistake | Fix |
| --- | --- |
| `unknown field "projectKey"` in edit | Used CREATE format with EDIT → remove projectKey, use `issues` instead |
| `unknown field "issues"` in create | Used EDIT format with CREATE → remove issues, use `projectKey` instead |
| `unknown field "parent"` | acli does not support parent → use Two-Step Workflow |
| Nested bulletList → `INVALID_INPUT` | listItem > bulletList not allowed → flatten or comma-separated |
| Nested tables | Nested tables not supported → use bullets instead |
| Table inside panel | ❌ → use bulletList inside panel |
| Description ugly wiki format | Use `acli --from-json`, not MCP |
| Token limit exceeded | Use `fields` parameter with `jira_get_issue` |
| Missing `version: 1` | ADF root must have `{"type":"doc","version":1,"content":[]}` |
| Code blocks no syntax highlight (Confluence) | Run `fix_confluence_code_blocks.py --page-id` after MCP |
| Confluence macros rendered as text | Use `update_page_storage.py` instead of MCP |

### Agent Decision Rules

> **Principle:** Fewer decision points = fewer mistakes — make rules as explicit as possible

| Decision Point | Rule |
| --- | --- |
| **Create Technical Note?** | Create when: (1) architecture decisions exist, (2) complex code patterns, (3) user requests it → if unsure, ask user |
| **Confluence: MCP or Script?** | Has code blocks/macros → always use Script, none → MCP is fine |
| **ADF mapping unclear?** | Flag "unclear mapping" → never guess |
| **Issue type uncertain?** | Ask user → never guess the type |
| **Scope too large?** | Sub-task > 5 days → recommend split, do not auto-split |

> **Full references:** templates → `templates.md` | tools → `tools.md` | errors → `troubleshooting.md`

## References (load when needed)

> **Skills location:** `.claude/skills/` — 17 skill dirs + `atlassian-scripts/` + `shared-references/`

| Need | File |
| --- | --- |
| All templates (ADF) | `.claude/skills/shared-references/templates.md` |
| Tool selection + effort sizing | `.claude/skills/shared-references/tools.md` |
| Quality checklists | `.claude/skills/shared-references/verification-checklist.md` |
| Writing style guide | `.claude/skills/shared-references/writing-style.md` |
| JQL patterns | `.claude/skills/shared-references/jql-quick-ref.md` |
| Troubleshooting | `.claude/skills/shared-references/troubleshooting.md` |
| Critical items checklist | `.claude/skills/shared-references/critical-items.md` |
| Team capacity + skill mapping | `.claude/skills/shared-references/team-capacity.md` |
| Sprint frameworks (RICE, carry-over) | `.claude/skills/shared-references/sprint-frameworks.md` |
| Tresor sprint-prioritizer | `~/.claude/subagents/product/management/sprint-prioritizer/agent.md` |
| Atlassian scripts | `.claude/skills/atlassian-scripts/SKILL.md` |

## Core Principles

1. **Phase-based workflows** - Follow phases in order, never skip steps
2. **ADF via acli** - Use `acli --from-json` for Jira descriptions (never MCP for descriptions)
3. **Thai + loanwords** - Content in Thai, technical terms in English
4. **Clear handoffs** - Each role passes structured context to next
5. **INVEST compliance** - All items pass INVEST criteria
6. **Traceability** - Everything links back to parent (Story→Epic, Sub-task→Story)

---

## ⚠️ Critical: Explore Codebase First

> **No Explore = No Design** — Must `Task(Explore)` before creating Sub-tasks

**Why:** Without exploring → generic paths (useless), duplicate work, wrong conventions

**How:** `Task(subagent_type="Explore")` with paths from **Service Tags** — e.g., "Find credit top-up page in `[BE]`"

## Troubleshooting

> ADF/tool errors → **Common Mistakes** above | Full recovery → `shared-references/troubleshooting.md`

| Issue | Solution |
| --- | --- |
| Wrong project key | Always use `BEP` |
| "Issue not found" | Check format: `BEP-XXX` |
| "Permission denied" | Re-authenticate MCP |
| Workflow interrupted | Note phase → search Jira → resume from last completed |
