# CLAUDE.md

## Overview

Agile Documentation System for **Tathep Platform** — skills-based Jira/Confluence automation

**Structure:** `.claude/skills/` — 19 skills (`SKILL.md` → phases → `shared-references/`) + `atlassian-scripts/` (7 Python scripts) + `shared-references/` (17 docs)

```text
.claude/skills/{name}/SKILL.md   ← skill entry (reads shared-references/)
.claude/skills/shared-references/ ← 17 docs: templates, tools, best-practices
.claude/skills/atlassian-scripts/ ← 7 Python scripts + lib/ (REST API)
tasks/                            ← ADF JSON output (acli --from-json input)
scripts/                          ← setup + sync utilities
```

> Skill `CLAUDE.md` = claude-mem only (auto-generated). All skill logic lives in `SKILL.md`.

## Project Settings

| Setting | Value |
| --- | --- |
| Jira Site | `100-stars.atlassian.net` |
| Project Key | `BEP` |
| Confluence Space | `BEP` |

**Prerequisites:** `acli` CLI, MCP (Jira + Confluence + Figma + GitHub), Python 3.x (`atlassian-scripts/`)

## Skill Commands

| Command | Description | Output |
| --- | --- | --- |
| `/create-epic` | Create Epic from product vision | Epic + Epic Doc |
| `/create-story` | Create User Story from requirements | User Story |
| `/create-task` | Create Task (tech-debt, bug, chore, spike) | Task |
| `/analyze-story BEP-XXX` | Analyze Story → Sub-tasks | Sub-tasks + Technical Note |
| `/create-testplan BEP-XXX` | Create Test Plan from Story | [QA] Sub-task |
| `/create-doc` | Create Confluence page (tech-spec, adr, parent) | Confluence Page |
| `/update-epic BEP-XXX` | Edit Epic - adjust scope, RICE, metrics | Updated Epic |
| `/update-story BEP-XXX` | Edit User Story - add/edit AC, scope | Updated Story |
| `/update-task BEP-XXX` | Edit Task - migrate format, add details | Updated Task |
| `/update-subtask BEP-XXX` | Edit Sub-task - format, content | Updated Sub-task |
| `/update-doc PAGE-ID` | Update/Move Confluence page | Updated Page |
| `/story-full` | Create Story + Sub-tasks in one go ⭐ | Story + Sub-tasks |
| `/story-cascade BEP-XXX` | Update Story + cascade to Sub-tasks ⭐ | Updated Story + Sub-tasks |
| `/sync-alignment BEP-XXX` | Sync all artifacts bidirectional ⭐ | Updated issues + pages |
| `/plan-sprint` | Sprint planning: carry-over + assign ⭐ | Sprint plan + assignments |
| `/dependency-chain` | Dependency analysis, critical path, swim lanes | Mermaid + plan |
| `/search-issues` | Search before creating (dedup) | Matching issues |
| `/verify-issue BEP-XXX` | Verify quality (ADF, INVEST, language) | Report / Fixed issues |
| `/optimize-context` | Audit + compress CLAUDE.md | Updated CLAUDE.md |

> `/verify-issue` flags: `--with-subtasks` = batch | `--fix` = auto-fix | `--dry-run` = report only

**Skills:** `.claude/skills/[name]/SKILL.md` → phases in order → refs from `shared-references/`

## Workflow Chain

```text
/search-issues ← always run FIRST (prevent duplicates)
       ↓
Stakeholder → PM(/create-epic) → PO(/create-story) → TA(/analyze-story) → ⚡ QA(/create-testplan)
                                       │                     │
                                       └── /story-full ⭐ ───┘  (PO + TA combined)
⚡ QA = optional — create when requested or story has complex logic

Update flows:
  /update-{epic,story,task,subtask} ── single issue
  /story-cascade ⭐ ──────────────── Story + cascade to Sub-tasks
  /sync-alignment ⭐ ─────────────── sync all (Jira + Confluence)

Standalone: /create-task, /create-doc, /update-doc
Planning:   /plan-sprint ⭐ (reads Jira, assigns work)
Verify:     /verify-issue ← always run AFTER creating/updating
Alignment:  Epic ↔ Stories ↔ Confluence ↔ Figma (cross-layer check)
```

### Common Skill Mistakes

| Mistake | Correct |
| --- | --- |
| `/create-story` + `/analyze-story` separately | Use `/story-full` ⭐ — does both in one go |
| `/analyze-story` without Explore | Sub-tasks will have generic paths — always Explore first |
| Creating without `/search-issues` | May create duplicates — always search first |
| `/update-story` when Sub-tasks also need changes | Use `/story-cascade` ⭐ to cascade automatically |
| `/story-cascade` when Confluence also needs sync | Use `/sync-alignment` ⭐ for full bidirectional sync |

## Passive Context (Always Loaded)

> Compressed from `shared-references/` — load full templates only when needed

> Tool Selection, ADF basics (panels, colors, AC format, inline code), Writing Style, Verification, Service Tags, Common ADF/tool errors → see global `~/.claude/CLAUDE.md`

### jira_get_issue — always use `fields` param

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

1. MCP: `jira_create_issue({project_key:"BEP", summary:"...", issue_type:"Subtask", additional_fields:{parent:{key:"BEP-XXX"}}})`
2. acli: `acli jira workitem edit --from-json subtask.json --yes`

**Smart Link:** `{"type":"inlineCard","attrs":{"url":"https://...atlassian.net/browse/BEP-XXX"}}` — auto-resolves summary+status

### Content Density

**Scan-First:** bold keywords first · bullets > paragraphs · tables > lists · skip if empty
**Content Budget:** Epic overview 2 sentences · Story max 5 AC panels · Sub-task max 3 AC · QA ⚡ optional max 8 TC
**Full rules** → `shared-references/writing-style.md`

### Common Mistakes (project-specific)

> Shared ADF/tool errors → see global `~/.claude/CLAUDE.md` | Full recovery → `shared-references/troubleshooting.md`

| Mistake | Fix |
| --- | --- |
| Description via MCP → ugly wiki | Use `acli --from-json`, never MCP for descriptions |
| `unknown field "issues"` in create | Used EDIT format with CREATE → remove issues, use `projectKey` instead |
| Nested tables | Not supported → use bullets instead |
| Missing `version: 1` | ADF root must have `{"type":"doc","version":1,"content":[]}` |
| Code blocks no syntax highlight (Confluence) | Run `fix_confluence_code_blocks.py --page-id` after MCP |
| Confluence macros rendered as text | Use `update_page_storage.py` instead of MCP |
| Permission denied | Re-authenticate MCP |
| Workflow interrupted mid-phase | Note phase → search Jira → resume from last completed |
| MCP `jira_update_issue` assignee → silent fail | Use `acli jira workitem assign -k "KEY" -a "email" -y` |
| `acli jira issue update --assignee` → unknown flag | Use `acli jira workitem assign` not `acli jira issue update` |
| JQL `key in (...) ORDER BY` → parse error | Remove `ORDER BY` when using `key in (...)` syntax |
| MCP `jira_update_issue(fields=...)` → unexpected kwarg | Use `additional_fields` not `fields` for custom fields |
| MCP `jira_search` → exceeds max tokens | Always use `fields` param: `fields="summary,status,assignee"` |

## References (load when needed)

> **Shared refs** at `.claude/skills/shared-references/` (all `.md`):
> templates (index → templates-{epic,story,subtask,task}) · tools · verification-checklist · writing-style · jql-quick-ref · troubleshooting · critical-items · team-capacity · sprint-frameworks · epic-best-practices · story-best-practices · subtask-best-practices · technical-note-best-practices

> **Tresor:** `~/.claude/subagents/product/management/sprint-prioritizer/agent.md` | **Scripts:** `.claude/skills/atlassian-scripts/SKILL.md`

## Core Principles

1. **Phase-based workflows** - Follow phases in order, never skip steps
2. **Clear handoffs** - Each role passes structured context to next
3. **Traceability** - Everything links back to parent (Story→Epic, Sub-task→Story)

## Critical: Explore Codebase First

> **No Explore = No Design** — `Task(Explore)` before creating Sub-tasks, otherwise → generic paths, wrong conventions
> Example: "Find credit top-up page in `[BE]`" — uses **Service Tags** paths from global

> Run `/optimize-context` when CLAUDE.md feels outdated or context exceeds 15 KB
