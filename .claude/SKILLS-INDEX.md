# Skills Index

> 18 skills + 7 scripts + 14 references | Project: BEP (Tathep Platform)

## Overview

| Category | Count | Invoke | Input |
| --- | --- | --- | --- |
| Create | 7 | `/skill-name [args]` | description or requirements |
| Update | 5 | `/skill-name BEP-XXX [changes]` | issue key + changes |
| Composite | 4 | `/skill-name [args]` | varies (end-to-end) |
| Utility | 2 | `/skill-name [args]` | issue key or keyword |

**Total:** 18 skills across 4 categories, 7 Python scripts, 14 shared reference files

## Skill Selection Guide

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

## Workflow Chain

```text
Stakeholder → PM → PO → TA → QA
               │     │     │     │
               ↓     ↓     ↓     ↓
            Epic   Story  Sub-tasks  Test Plan
                          ↑
              /story-full ⭐ = PO + TA in one go
```

**Handoff flow:** Each role passes structured context to the next via Jira issue links.

---

## Create Skills (7)

| # | Skill | Phases | Role | Output | Triggers |
| --- | --- | --- | --- | --- | --- |
| 1 | `/create-epic` | 5 | Sr. Product Manager | Epic + Epic Doc (Confluence) | "create epic", "new initiative" |
| 2 | `/create-story` | 5 | Sr. Product Owner | User Story (Jira) | "create story", "new feature" |
| 3 | `/create-task` | 5 | Developer / Tech Lead | Task (Jira) | "create task", "new task" |
| 4 | `/analyze-story` | 7 | Sr. Technical Analyst | Sub-tasks + Technical Note | "analyze", "create subtasks" |
| 5 | `/create-testplan` | 5 | Sr. QA Analyst | [QA] Sub-task (Jira) | "test plan", "QA", "testing" |
| 6 | `/create-doc` | 4 | Developer / Tech Lead | Confluence Page | "create doc", "tech spec", "ADR" |
| 7 | `/search-issues` | 3 | Any | List of matching issues | "search", "find", "duplicate check" |

### Key Details

- **`/create-epic`** — RICE prioritization, stakeholder interview, creates both Jira Epic + Confluence Epic Doc
- **`/create-task`** — Supports 4 types: `tech-debt`, `bug`, `chore`, `spike`
- **`/analyze-story`** — **MUST explore codebase** before designing Sub-tasks (uses `Task(Explore)`)
- **`/create-testplan`** — Test Plan embedded in [QA] Sub-task description (not separate Confluence page)
- **`/search-issues`** — Always run before creating to prevent duplicates

## Update Skills (5)

| # | Skill | Phases | Role | Output | Triggers |
| --- | --- | --- | --- | --- | --- |
| 8 | `/update-epic` | 5 | Sr. Product Manager | Updated Epic | "update epic", "edit epic" |
| 9 | `/update-story` | 5 | Sr. Product Owner | Updated Story | "update story", "edit story" |
| 10 | `/update-task` | 5 | Developer / Tech Lead | Updated Task | "update task", "edit task" |
| 11 | `/update-subtask` | 5 | Technical Analyst | Updated Sub-task | "update subtask", "edit subtask" |
| 12 | `/update-doc` | 5 | Developer / Tech Lead | Updated Confluence Page | "update doc", "move page" |

### Key Details

- All update skills share the same 5-phase pattern: Fetch → Impact Analysis → Preserve Intent → Generate → Apply
- **`/update-doc`** — Also supports moving pages to different parent

## Composite Skills (4) ⭐

| # | Skill | Phases | Role | Output | Triggers |
| --- | --- | --- | --- | --- | --- |
| 13 | `/story-full` | 10 | PO + TA Combined | Story + Sub-tasks (end-to-end) | "story full", "full workflow" |
| 14 | `/story-cascade` | 8 | PO + TA Combined | Updated Story + Sub-tasks | "cascade", "update all" |
| 15 | `/sync-alignment` | 8 | PO + TA + Tech Lead | Updated issues + Confluence pages | "sync", "align artifacts" |
| 16 | `/plan-sprint` | 8 | Scrum Master (Tresor) | Sprint plan + Jira assignments | "plan sprint" |

### Key Details

- **`/story-full`** — Most used skill. Creates Story (Phase 1-4) then Sub-tasks (Phase 5-10) in one workflow
- **`/story-cascade`** — Updates Story and automatically cascades changes to related Sub-tasks
- **`/sync-alignment`** — Bidirectional sync: any artifact → detect changes → update all related artifacts (Jira + Confluence)
- **`/plan-sprint`** — Hybrid: Tresor sprint-prioritizer handles strategy (Phase 3-6) + MCP handles execution (Phase 1,2,8)
  - External agent: `~/.claude/subagents/product/management/sprint-prioritizer/agent.md`

## Utility Skills (2)

| # | Skill | Phases | Role | Output | Triggers |
| --- | --- | --- | --- | --- | --- |
| 17 | `/verify-issue` | 6 | Any | Verification report or fixed issues | "verify", "check quality" |
| 18 | `/optimize-context` | - | Meta | Updated CLAUDE.md / Report | "optimize", "audit context" |

### Key Details

- **`/verify-issue`** — Options: `--with-subtasks` (batch), `--fix` (auto-fix + format migration)
- **`/optimize-context`** — Audits and compresses CLAUDE.md for agent effectiveness

---

## Tool Ecosystem

### Atlassian Scripts (7 scripts)

> Location: `.claude/skills/atlassian-scripts/`

| Script | Purpose | When to Use |
| --- | --- | --- |
| `create_confluence_page.py` | Create Confluence page | Code blocks, macros needed |
| `update_confluence_page.py` | Update Confluence page | Code blocks, macros needed |
| `move_confluence_page.py` | Move page to new parent | Reorganize Confluence structure |
| `update_page_storage.py` | Update via storage format | Complex formatting (ToC, macros) |
| `fix_confluence_code_blocks.py` | Fix code block formatting | After MCP creates broken blocks |
| `audit_confluence_pages.py` | Audit pages for quality | Validate page structure |
| `update_jira_description.py` | Update Jira description via REST | Direct ADF manipulation |

**Library modules:** `auth.py`, `api.py`, `jira_api.py`, `converters.py`, `exceptions.py`

### Shared References (14 files)

> Location: `.claude/skills/shared-references/`

| Category | Files | Purpose |
| --- | --- | --- |
| Templates | `templates.md`, `templates-{epic,story,subtask,task}.md` | ADF templates per issue type |
| Quality | `verification-checklist.md`, `critical-items.md` | INVEST compliance, validation rules |
| Tools | `tools.md` | Tool selection matrix + effort sizing |
| Style | `writing-style.md` | Thai + loanwords, tone, formatting |
| Reference | `jql-quick-ref.md`, `troubleshooting.md` | JQL patterns, error recovery |
| Planning | `sprint-frameworks.md`, `team-capacity.md` | RICE, carry-over, team budgets |

### External Tools

| Tool | Purpose | Invocation |
| --- | --- | --- |
| MCP `jira_*` | Read/update Jira fields | MCP tool calls |
| MCP `confluence_*` | Read Confluence pages | MCP tool calls |
| `acli` | Create/edit Jira descriptions (ADF) | `acli jira workitem create/edit --from-json` |
| Tresor sprint-prioritizer | Sprint strategy (RICE, distribution) | Read agent.md → use as Task prompt |

---

## Phase Pattern Reference

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

---

## Dependencies Between Skills

```text
/create-epic ─────────────────────────────────────── (standalone)
  └─→ /create-story ──→ /analyze-story ──→ /create-testplan
        │                     │
        └── /story-full ⭐ ───┘  (combines create-story + analyze-story)
        │
        └── /story-cascade ⭐     (update story + cascade to subtasks)
        └── /sync-alignment ⭐    (sync all: Jira + Confluence)

/create-task ─────────────────────────────────────── (standalone)
/create-doc ──────────────────────────────────────── (standalone)
/update-doc ──────────────────────────────────────── (standalone)

/plan-sprint ⭐ ──────────────────────────────────── (reads from Jira, assigns work)
/verify-issue ────────────────────────────────────── (post-creation quality check)
/search-issues ───────────────────────────────────── (pre-creation duplicate check)
```

---

*Last updated: Feb 3, 2026*
