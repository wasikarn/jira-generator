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

## Project Settings

Config: `.claude/project-config.json` — Jira/Confluence, team, services, environments

| Setting | Config Key |
| --- | --- |
| Jira/Confluence | `jira.*`, `confluence.*` |
| Team + Capacity | `team.members[]` |
| Service Tags | `services.tags[]` |
| Environments | `environments.*` |

**Dynamic lookup:** Board → `jira_get_agile_boards(project_key="BEP")` · Sprint → `jira_get_sprints_from_board(board_id, state="future")`
**Prerequisites:** `acli` CLI, MCP (Jira + Confluence + Figma + GitHub), Python 3.x

### Cloning to Another Project

```bash
vi .claude/project-config.json                      # 1. Edit config
python scripts/configure-project.py --revert        # 2. Preview (dry-run)
python scripts/configure-project.py --revert --apply # 3. Revert placeholders
python scripts/configure-project.py --apply          # 4. Apply new values
```

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
| `/story-full` | Create Story + Sub-tasks in one go | Story + Sub-tasks |
| `/story-cascade BEP-XXX` | Update Story + cascade to Sub-tasks | Updated Story + Sub-tasks |
| `/sync-alignment BEP-XXX` | Sync all artifacts bidirectional | Updated issues + pages |
| `/plan-sprint` | Sprint planning: carry-over + assign | Sprint plan + assignments |
| `/dependency-chain` | Dependency analysis, critical path, swim lanes | Mermaid + plan |
| `/search-issues` | Search before creating (dedup) | Matching issues |
| `/verify-issue BEP-XXX` | Verify quality (ADF, INVEST, language) | Report / Fixed issues |
| `/activity-report` | Generate activity report from claude-mem | Markdown report |
| `/optimize-context` | Audit + compress CLAUDE.md | Updated CLAUDE.md |

`/verify-issue` flags: `--with-subtasks` (batch) | `--fix` (auto-fix) | `--dry-run` (report only)

## Workflow Chain

| Phase | Flow | Notes |
| --- | --- | --- |
| **Search first** | `/search-issues` | Always run before creating (dedup) |
| **Create** | PM `/create-epic` → PO `/create-story` → TA `/analyze-story` → QA `/create-testplan` | QA optional |
| **Combined** | `/story-full` = `/create-story` + `/analyze-story` in one go | Preferred |
| **Update single** | `/update-{epic,story,task,subtask}` | One issue |
| **Update cascade** | `/story-cascade` = Story + Sub-tasks | `/sync-alignment` if Confluence too |
| **Standalone** | `/create-task`, `/create-doc`, `/update-doc` | |
| **Planning** | `/plan-sprint` | Reads Jira, assigns work |
| **Verify** | `/verify-issue` | Always run after creating/updating |

## Tool Selection

- **Desc:** `acli --from-json` (ADF JSON) | **Fields:** MCP `jira_update_issue`
- **Read:** MCP `jira_get_issue` — **always use `fields` param**
- **Search:** MCP `jira_search` (JQL) — **always use `fields` + `limit` params**
- **Comment:** MCP `jira_add_comment`
- **Sub-task:** Two-Step: MCP create → acli edit (`parent` doesn't work with acli)
- **Script:** `update_jira_description.py` (REST) | **Format:** `/atlassian-scripts`
- **Confluence:** MCP (read/simple), Python scripts (code/macros), `audit_confluence_pages.py` (audit)
- **Explore:** Task(Explore) — always before creating subtasks
- **Issue Links:** MCP `jira_create_issue_link` (Blocks/Relates) | **Web Links:** MCP `jira_create_remote_issue_link`
- **Sprint Mgmt:** Agile REST API via `JiraAPI._request()` — MCP doesn't support move to backlog

### jira_get_issue — always use `fields` param

| Use Case | Fields |
| --- | --- |
| Quick check | `summary,status,assignee` |
| Read description | `summary,status,description` |
| Full analysis | `summary,status,description,issuetype,parent,labels` |

### jira_search — always use `fields` + `limit` params

Without `fields`, results exceed 70K+ chars → token limit error.

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

**Subtask — Two-Step** (acli does not support `parent` field):
1. MCP: `jira_create_issue({project_key:"BEP", summary:"...", issue_type:"Subtask", additional_fields:{parent:{key:"BEP-XXX"}}})`
2. acli: `acli jira workitem edit --from-json subtask.json --yes`

**Smart Link:** `{"type":"inlineCard","attrs":{"url":"https://...atlassian.net/browse/BEP-XXX"}}`

## Common Mistakes (unified)

> Full troubleshooting: `shared-references/troubleshooting.md`

| Category | Quick Fix |
| --- | --- |
| Description via MCP → ugly | Use `acli --from-json`, never MCP |
| MCP assignee → silent fail | Use `acli jira workitem assign` |
| Subtask parent → error | `additional_fields={"parent": {"key": "BEP-XXX"}}` |
| Subtask + sprint → error | Remove sprint field — inherits from parent |
| `fields` param → error | Use `additional_fields` not `fields` |
| `project_key_or_id` → error | Use `project_key` |
| `limit > 50` → error | Max 50, use pagination `start_at` |
| Token limit exceeded | Use `fields` + `limit` params |
| Sibling tool call errored | One parallel MCP call failed → all cancelled. Fix failing call first |
| Confluence macros → raw XML | Use `update_page_storage.py`, never MCP for macros |
| `/create-story` + `/analyze-story` separately | Use `/story-full` — does both in one go |
| `/analyze-story` without Explore | Sub-tasks get generic paths — always Explore first |
| Creating without `/search-issues` | May create duplicates — always search first |
| `/update-story` when Sub-tasks need changes | Use `/story-cascade` to cascade automatically |
| `/story-cascade` when Confluence needs sync | Use `/sync-alignment` for full bidirectional sync |

### JQL `parent` Field — HARD RULE

**NEVER add `ORDER BY` to ANY JQL with `parent =`, `parent in`, or `key in (...)`.**

```text
❌ parent = BEP-XXX ORDER BY rank
✅ parent = BEP-XXX                         → use results as-is
✅ "Parent Link" = BEP-XXX ORDER BY created → if sorting needed
```

## Decision Rules

- **Description create/update** → acli + ADF JSON (never MCP for descriptions)
- **Sub-task create** → Two-Step: MCP create shell → acli edit description
- **Before creating sub-tasks** → MUST explore codebase (Task/Explore) for real file paths
- **Full templates** → load from `shared-references/templates-{type}.md`
- **Content density** → `shared-references/writing-style.md`

## References

Shared refs at `.claude/skills/shared-references/` (all `.md`):
templates (index → templates-{epic,story,subtask,task}) · tools · verification-checklist · writing-style · jql-quick-ref · troubleshooting · critical-items · team-capacity · sprint-frameworks · epic-best-practices · story-best-practices · subtask-best-practices · technical-note-best-practices

**Tresor:** `~/.claude/subagents/product/management/sprint-prioritizer/agent.md` | **Scripts:** `.claude/skills/atlassian-scripts/SKILL.md`

## Core Principles

1. **Phase-based workflows** — follow phases in order, never skip steps
2. **Clear handoffs** — each role passes structured context to next
3. **Traceability** — everything links back to parent (Story→Epic, Sub-task→Story)
4. **Explore first** — `Task(Explore)` before creating Sub-tasks (no explore = generic paths)
Run `/optimize-context` when CLAUDE.md feels outdated or context exceeds 15 KB.
