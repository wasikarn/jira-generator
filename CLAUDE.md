# CLAUDE.md

## Overview

Agile Documentation System for **Tathep Platform** - Create Epics, User Stories, and Sub-tasks via Jira/Confluence

## Project Settings

| Setting | Value |
| --- | --- |
| Jira Site | `100-stars.atlassian.net` |
| Project Key | `BEP` |
| Confluence Space | `BEP` |

## Quick Start (5 min)

1. **Need to create a new feature?** → `/story-full` (creates Story + Sub-tasks end-to-end)
2. **Already have an Epic, need a Story?** → `/create-story`
3. **Already have a Story, need to analyze?** → `/analyze-story BEP-XXX`
4. **Need to create a Task?** → `/create-task` (tech-debt, bug, chore, spike)
5. **Need to plan a Sprint?** → `/plan-sprint` (Tresor strategy + Jira execution)

> ⚡ **After creation:** Always use `/verify-issue BEP-XXX` to verify quality

## Skill Commands

### Create

| Command | Description | Output |
| --- | --- | --- |
| `/create-epic` | Create Epic from product vision | Epic + Epic Doc |
| `/create-story` | Create User Story from requirements | User Story |
| `/create-task` | Create Task (tech-debt, bug, chore, spike) | Task |
| `/analyze-story BEP-XXX` | Analyze Story → Sub-tasks | Sub-tasks + Technical Note |
| `/create-testplan BEP-XXX` | Create Test Plan from Story | Test Plan + [QA] Sub-tasks |
| `/create-doc` | Create Confluence page (tech-spec, adr, parent) | Confluence Page |
| `/update-doc` | Update/Move Confluence page | Updated/Moved Page |

### Update

| Command | Description | Output |
| --- | --- | --- |
| `/update-epic BEP-XXX` | Edit Epic - adjust scope, RICE, metrics | Updated Epic |
| `/update-story BEP-XXX` | Edit User Story - add/edit AC, scope | Updated Story |
| `/update-task BEP-XXX` | Edit Task - migrate format, add details | Updated Task |
| `/update-subtask BEP-XXX` | Edit Sub-task - format, content | Updated Sub-task |

### Composite (End-to-End Workflow) ⭐

| Command | Description | Output |
| --- | --- | --- |
| `/story-full` | Create Story + Sub-tasks complete workflow in one go | Story + Sub-tasks |
| `/story-cascade BEP-XXX` | Update Story + cascade to related Sub-tasks | Updated Story + Sub-tasks |
| `/sync-alignment BEP-XXX` | Sync all artifacts (Jira + Confluence) bidirectional | Updated issues + pages |
| `/plan-sprint` | Sprint planning: carry-over + prioritize + assign (Tresor-powered) | Sprint plan + Jira assignments |

> **When to use:** `story-full` = complete new feature, `story-cascade` = cascade Jira only, `sync-alignment` = full sync + Confluence, `plan-sprint` = plan a new sprint

### Utility

| Command | Description | Output |
| --- | --- | --- |
| `/search-issues` | Search issues before creating new ones (prevent duplicates) | List of matching issues |
| `/verify-issue BEP-XXX` | Verify + improve issue quality (ADF, INVEST, language) | Verification report / Improved issue(s) |
| `/optimize-context` | Audit shared-refs → compress into passive context | Updated CLAUDE.md / Report (`--dry-run`) |

> **Verify:** After creating/updating an issue | `--with-subtasks` = batch check | `--fix` = auto-fix + format migration

**Skill Location:** `.claude/skills/` (each command = 1 skill directory)

**How Skills Work:** `.claude/skills/[command-name]/SKILL.md` → execute phases in order → reference `shared-references/`

## Workflow Chain

```text
Stakeholder → PM → PO → TA → QA
              │     │     │     │
              ↓     ↓     ↓     ↓
           Epic   Story  Sub-tasks  Test Cases
              ↓     ↓     ↓     ↓
         [/verify-issue after creation]
```

**Handoff:** PM (Epic) → PO (Story) → TA (Sub-tasks) → QA (Test Plan) — structured context passed to each role

## Service Tags

| Tag | Service | Local Path |
| --- | --- | --- |
| `[BE]` | Backend | `~/Codes/Works/tathep/tathep-platform-api` |
| `[FE-Admin]` | Admin | `~/Codes/Works/tathep/tathep-admin` |
| `[FE-Web]` | Website | `~/Codes/Works/tathep/tathep-website` |

## Passive Context (Always Loaded)

> **Design principle:** The data below is compressed from shared-references so the agent always has context ready to use.
> No need to load additional files, reducing latency + reducing chance of errors (inspired by Vercel's AGENTS.md approach)
>
> **Full references:** Load when full templates are needed → `.claude/skills/shared-references/`

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

**jira_get_issue — must specify fields:**

```python
# ❌ token limit error
jira_get_issue(issue_key="BEP-XXX")
# ✅ specify fields
jira_get_issue(issue_key="BEP-XXX", fields="summary,status,description,issuetype,parent", comment_limit=5)
```

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

## File Structure

```text
.claude/skills/            # Each dir = 1 skill (see Skill Commands above)
├── create-epic/           → 5-phase PM
├── create-story/          → 5-phase PO
├── analyze-story/         → 7-phase TA
├── create-testplan/       → 6-phase QA
├── create-task/           → 5-phase task
├── create-doc/            → 4-phase Confluence
├── update-doc/            → 5-phase Confluence update
├── update-{epic,story,task,subtask}/ → 5-phase update
├── story-full/            → 10-phase composite ⭐
├── story-cascade/         → 8-phase cascade ⭐
├── sync-alignment/        → 8-phase bidirectional ⭐
├── plan-sprint/           → 8-phase Tresor strategy + execution ⭐
├── search-issues/         → 3-phase search
├── verify-issue/          → 5-phase verify + fix
├── atlassian-scripts/     → Python REST API scripts
│   ├── lib/               → auth, api, jira_api, converters, exceptions
│   └── scripts/           → 7 scripts (see Tool Selection)
└── shared-references/     → Templates, tools, style, checklists
    └── critical-items.md  → Passive context validation checklist

tasks/                     # Generated outputs (gitignored)
```

## References (load when needed)

| Need | File |
| --- | --- |
| **Skills Index (full catalog)** | **`.claude/SKILLS-INDEX.md`** |
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
2. **Explore before design** - Must always explore codebase before creating Sub-tasks
3. **ADF via acli** - Use `acli --from-json` for Jira descriptions
4. **Thai + loanwords** - Content in Thai, technical terms in English
5. **Clear handoffs** - Each role passes structured context to next
6. **INVEST compliance** - All items pass INVEST criteria
7. **Traceability** - Everything links back to parent (Story→Epic, Sub-task→Story)

---

## ⚠️ Critical: Explore Codebase First

> **No Explore = No Design**
>
> Must always explore codebase before creating Sub-tasks, otherwise the design will be wrong

**Without Exploring:** generic paths (useless), duplicate work, wrong conventions, incorrect scope estimates

**TA Workflow:** Story → Impact Analysis → 🔍 **EXPLORE** (paths, patterns, existing code, architecture) → Design → Create Sub-tasks

**How to Explore:** Use `Task (Explore agent)` with paths from **Service Tags** above

**Explore prompts:** "Find credit top-up page", "Find API endpoint for orders", "Find existing billing patterns"

## Troubleshooting

> Quick fixes are in **Passive Context > Common Mistakes & Quick Fixes** above
> Full recovery procedures → `.claude/skills/shared-references/troubleshooting.md`

| Issue | Solution |
| --- | --- |
| Wrong project key | Always use `BEP` |
| "Issue not found" | Check format: `BEP-XXX` |
| "Permission denied" | Re-authenticate MCP |
| Workflow interrupted | Note phase → search Jira → resume from last completed |
