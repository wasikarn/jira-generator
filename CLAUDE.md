# CLAUDE.md

## Overview

Agile Documentation System for **{{COMPANY}} Platform** — skills-based Jira/Confluence automation

**Structure:** `.claude/skills/` — 19 skills (`SKILL.md` → phases → `shared-references/`) + `atlassian-scripts/` (7 Python scripts) + `jira-cache-server/` (MCP) + `shared-references/` (11 docs)

```text
.claude/skills/{name}/SKILL.md     ← skill entry (reads shared-references/)
.claude/skills/shared-references/  ← 11 docs: templates, tools, verification, orchestration
.claude/skills/atlassian-scripts/  ← 7 Python scripts + lib/ (REST API)
.claude/skills/jira-cache-server/  ← MCP server (SQLite + FTS5, local Jira cache)
tasks/                             ← ADF JSON output (acli --from-json input)
scripts/                           ← setup + sync utilities
```

## Project Settings

Config: `.claude/project-config.json` (single source of truth) — Jira/Confluence, team, services, environments

| Setting | Config Key |
| --- | --- |
| Jira/Confluence | `jira.*`, `confluence.*` |
| Team + Capacity | `team.members[]` |
| Service Tags | `services.tags[]` |
| Environments | `environments.*` |

**Dynamic lookup:** Board → `jira_get_agile_boards(project_key="{{PROJECT_KEY}}")` · Sprint → `jira_get_sprints_from_board(board_id, state="future")`
**Prerequisites:** `acli` CLI, MCP (Jira + Confluence + Figma + GitHub), Python 3.x

**Configuration:** Git smudge/clean filters auto-convert placeholders↔real values (setup.sh configures). Repo always stores placeholders; working tree shows real values. Pre-commit hook as safety net.

**Cloning:** `cp .template .json` → edit values → `./scripts/setup.sh`

## Skill Commands

| Command | Description |
| --- | --- |
| `/create-epic` | Create Epic from product vision + Epic Doc |
| `/create-story` | Create User Story from requirements |
| `/create-task` | Create Task (tech-debt, bug, chore, spike) |
| `/analyze-story {{PROJECT_KEY}}-XXX` | Analyze Story → Sub-tasks + Technical Note |
| `/create-testplan {{PROJECT_KEY}}-XXX` | Create Test Plan → [QA] Sub-task |
| `/create-doc` | Create Confluence page (tech-spec, adr, parent) |
| `/update-{epic,story,task,subtask}` | Edit single issue — scope, AC, format |
| `/update-doc PAGE-ID` | Update/Move Confluence page |
| `/story-full` | Create Story + Sub-tasks in one go (preferred) |
| `/story-cascade {{PROJECT_KEY}}-XXX` | Update Story + cascade to Sub-tasks |
| `/sync-alignment {{PROJECT_KEY}}-XXX` | Sync all artifacts bidirectional |
| `/plan-sprint` | Sprint planning: carry-over + capacity + assign |
| `/dependency-chain` | Dependency analysis, critical path, swim lanes |
| `/search-issues` | Search before creating (dedup) |
| `/verify-issue {{PROJECT_KEY}}-XXX` | Verify quality (ADF, INVEST, language) |
| `/activity-report` | Generate activity report from claude-mem |
| `/optimize-context` | Audit + compress CLAUDE.md |

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

**Full orchestration + Tresor teams:** `shared-references/skill-orchestration.md`

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
- **Cache:** MCP `jira-cache-server` — local SQLite cache for fast search/similarity (8 tools: `cache_get_issue`, `cache_search`, `cache_text_search`, etc.)

### jira_get_issue — always use `fields` param

| Use Case | Fields |
| --- | --- |
| Quick check | `summary,status,assignee` |
| Read description | `summary,status,description` |
| Full analysis | `summary,status,description,issuetype,parent,labels` |

### jira_search — always use `fields` + `limit` params

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

**Subtask Two-Step:** MCP `jira_create_issue` (with `parent:{key:"{{PROJECT_KEY}}-XXX"}`) → acli `workitem edit --from-json`
**Smart Link:** `{"type":"inlineCard","attrs":{"url":"https://...atlassian.net/browse/BEP-XXX"}}`

## Common Mistakes (unified)

> Full troubleshooting: `shared-references/troubleshooting.md`

| Category | Quick Fix |
| --- | --- |
| MCP assignee → silent fail | Use `acli jira workitem assign` |
| Subtask parent → error | `additional_fields={"parent": {"key": "{{PROJECT_KEY}}-XXX"}}` |
| Subtask + sprint → error | Remove sprint field — inherits from parent |
| `fields` param → error | Use `additional_fields` not `fields` |
| `project_key_or_id` → error | Use `project_key` |
| `limit > 50` → error | Max 50, use pagination `start_at` |
| Sibling tool call errored | One parallel MCP call failed → all cancelled. Fix failing call first |
| Confluence macros → raw XML | Use `update_page_storage.py`, never MCP for macros |
| Prefer `/story-full` over separate create+analyze | `/search-issues` before creating · `/story-cascade` to cascade · `/sync-alignment` for Confluence |
| After Jira write → stale cache | `cache_invalidate(issue_key)` before next read |

## References

Shared refs at `.claude/skills/shared-references/` (all `.md`):
templates (epic·story·subtask·task sections) · tools · verification-checklist · writing-style · jql-quick-ref · troubleshooting · team-capacity · sprint-frameworks · dependency-frameworks · vertical-slice-guide · skill-orchestration

**Templates:** `shared-references/templates.md` | **Writing style:** `shared-references/writing-style.md`
**Orchestration:** `shared-references/skill-orchestration.md` | **Scripts:** `.claude/skills/atlassian-scripts/SKILL.md`
**Tresor:** `~/.claude/subagents/` (133 agents: product, engineering, core, design)

## Core Principles

1. **Quality Gate before Atlassian** — NEVER create/edit issues on Jira/Confluence before QG ≥ 90%
2. **Phase-based workflows** — follow phases in order, never skip steps
3. **Clear handoffs** — each role passes structured context to next
4. **Traceability** — everything links back to parent (Story→Epic, Sub-task→Story)
5. **Explore first** — prefer `Task(Explore)` before creating Sub-tasks (no explore = generic paths)

### HARD RULES

Rules that if violated cause **silent failures**, **data corruption**, or **irreversible damage**. No exceptions.

#### HR1. Quality Gate ≥ 90% Before Atlassian Writes

**NEVER** create or edit issues on Jira/Confluence before passing QG ≥ 90%.

```text
1. Explore codebase (real file paths — no generic paths)
2. Generate ADF (template-compliant, panels, Given/When/Then)
3. QG verify (≥ 90% → proceed, < 90% → fix first, max 2 retries)
4. MCP create shell (summary + parent only — NO description)
5. acli edit --from-json (ADF description)
```

Applies to ALL skills: create-epic, create-story, story-full, analyze-story, create-task, update-\*, story-cascade, sync-alignment.

#### HR2. JQL `parent` — No ORDER BY

**NEVER** add `ORDER BY` to JQL with `parent =`, `parent in`, or `key in (...)`. Parser error, no results.

#### HR3. MCP Assignee — Use acli Only

MCP `jira_update_issue` with assignee **silently succeeds but does nothing**. Always use `acli jira workitem assign -k "KEY" -a "email" -y`.

#### HR4. Confluence Macros — Use Script Only

MCP HTML-escapes `<ac:structured-macro>` → page renders raw XML. Use `update_page_storage.py` for ANY page with macros (ToC, Children, Code blocks).

#### HR5. Subtask = Two-Step + Verify Parent

MCP `jira_create_issue` may **silently ignore parent field** → orphan subtask. Always: (1) MCP create with parent, (2) `jira_get_issue` to verify parent link set, (3) acli edit for ADF description.

#### HR6. Cache Invalidate After Every Write

After any MCP write → `cache_invalidate(issue_key)`. Without this, subsequent reads return **stale data silently** — affects verify, cascade, and sprint planning.

#### HR7. Sprint ID — Always Lookup, Never Hardcode

Sprint IDs change every sprint. **Always** use `jira_get_sprints_from_board()` to get current ID. Hardcoding causes tickets to land in **wrong sprint silently** (no error from API).

#### HR8. Subtask Size + Dates Must Align with Parent

Subtask dates must fall within parent date range. Story points sum must be reasonable vs parent estimate. Misalignment → capacity calculation wrong, burndown chart inaccurate.

#### HR9. Related Ticket Descriptions Must Align

Story ACs must be covered by subtask objectives. Epic scope must reflect in child Stories. Blocked/blocking tickets must reference each other. Run `/verify-issue --with-subtasks` to check alignment (A1-A6).
Run `/optimize-context` when CLAUDE.md feels outdated or context exceeds 15 KB.
