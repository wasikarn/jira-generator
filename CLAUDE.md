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

> **Portable config:** `.claude/project-config.json` — update when cloning to another project/instance

| Setting | Source | Config Key |
| --- | --- | --- |
| Jira/Confluence | `project-config.json` | `jira.*`, `confluence.*` |
| Team + Capacity | `project-config.json` | `team.members[]` |
| Service Tags | `project-config.json` | `services.tags[]` |
| Environments | `project-config.json` | `environments.*` |

**Dynamic lookup:** Board ID → `jira_get_agile_boards(project_key="BEP")` · Sprint IDs → `jira_get_sprints_from_board(board_id, state="future")`

**Prerequisites:** `acli` CLI, MCP (Jira + Confluence + Figma + GitHub), Python 3.x (`atlassian-scripts/`)

### Cloning to Another Project

```bash
# 1. Edit config
vi .claude/project-config.json
# → Update: jira.site, jira.project_key, confluence.space_key, team.members, services.tags

# 2. Preview changes (dry-run)
python scripts/configure-project.py --revert

# 3. Apply placeholder conversion
python scripts/configure-project.py --revert --apply

# 4. Re-apply with new config values
python scripts/configure-project.py --apply
```

**What gets replaced:** `projectKey`, `project_key`, `space_key`, Jira URLs, custom field IDs

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
| `/activity-report` | Generate activity report from claude-mem | Markdown report |
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

### jira_search — always use `fields` + `limit` params

**Without `fields`, results regularly exceed 70K+ chars → token limit error.**

```text
❌ jira_search(jql="sprint = 640")                              → 73K+ chars, exceeds limit
❌ jira_search(jql="sprint = 640", fields="summary,status")     → still 70K+ if 100 issues
✅ jira_search(jql="sprint = 640", fields="summary,status,assignee", limit=30)  → safe
```

| Use Case | Fields | Limit |
| --- | --- | --- |
| Sprint overview | `summary,status,assignee,issuetype,priority` | 30 |
| Sub-task list | `summary,status,assignee` | 20 |
| Search duplicates | `summary,status,issuetype` | 10 |
| Full with links | `summary,status,assignee,issuetype,issuelinks,priority,labels` | 20 |

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

### Common Mistakes (quick ref)

> **Full troubleshooting:** `shared-references/troubleshooting.md` — MCP errors, Agile API, acli, ADF, Confluence

| Category | Quick Fix |
| --- | --- |
| Description via MCP → ugly | Use `acli --from-json`, never MCP |
| MCP assignee → silent fail | Use `acli jira workitem assign` |
| Subtask parent → error | `additional_fields={"parent": {"key": "BEP-XXX"}}` |
| Subtask + sprint → error | Remove sprint field — inherits from parent |
| `fields` param → error | Use `additional_fields` not `fields` |
| `project_key_or_id` → error | Use `project_key` |
| `limit > 50` → error | Use pagination with `start_at` |
| **Confluence macros → raw XML** | **Use `update_page_storage.py`, never MCP for macros** |

### 🚨 JQL `parent` Field — HARD RULE

**NEVER add `ORDER BY` to ANY JQL query that uses `parent =` or `parent in`.**
This includes compound queries: `project = BEP AND parent = BEP-XXX ORDER BY ...` also fails.

```text
❌ parent = BEP-XXX ORDER BY rank
❌ project = BEP AND parent = BEP-XXX AND issuetype = Story ORDER BY created
❌ parent in (BEP-123, BEP-456) ORDER BY priority
✅ parent = BEP-XXX                         → use results as-is
✅ "Parent Link" = BEP-XXX ORDER BY created → if sorting needed
```

**Also:** `key in (...) ORDER BY` causes same error — remove ORDER BY.

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
