# Skills Index

> 18 skills | Project: BEP | Operational context → `CLAUDE.md`

## Overview

| Category | Count | Invoke |
| --- | --- | --- |
| Create | 6 | `/skill-name [description]` |
| Update | 6 | `/skill-name BEP-XXX [changes]` |
| Composite | 4 ⭐ | `/skill-name [args]` |
| Utility | 2 | `/skill-name [args]` |

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

### Common Mistakes

| Mistake | Correct |
| --- | --- |
| `/create-story` + `/analyze-story` separately | Use `/story-full` ⭐ — does both in one go |
| `/analyze-story` without Explore | Sub-tasks will have generic paths — always Explore first |
| Creating without `/search-issues` | May create duplicates — always search first |
| `/update-story` when Sub-tasks also need changes | Use `/story-cascade` ⭐ to cascade automatically |
| `/story-cascade` when Confluence also needs sync | Use `/sync-alignment` ⭐ for full bidirectional sync |

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

## Create Skills (6)

| Skill | Args | Phases | Role | Output | Triggers |
| --- | --- | --- | --- | --- | --- |
| `/create-epic` | `[title]` | 5 | Sr. Product Manager | Epic + Epic Doc | "create epic", "new initiative" |
| `/create-story` | `[description]` | 5 | Sr. Product Owner | User Story | "create story", "new feature" |
| `/create-task` | `[type] [desc]` | 5 | Developer / Tech Lead | Task | "create task", "new task" |
| `/analyze-story` | `BEP-XXX` | 7 | Sr. Technical Analyst | Sub-tasks + Tech Note | "analyze", "create subtasks" |
| `/create-testplan` | `BEP-XXX` | 5 | Sr. QA Analyst | [QA] Sub-task | "test plan", "QA" |
| `/create-doc` | `[template] [title]` | 4 | Developer / Tech Lead | Confluence Page | "create doc", "tech spec" |

### Key Details

- **`/create-epic`** — RICE prioritization + Confluence Epic Doc
- **`/create-task`** — Types: `tech-debt`, `bug`, `chore`, `spike`
- **`/analyze-story`** — **MUST explore codebase first** (`Task(Explore)`)
- **`/create-testplan`** — Test Plan embedded in [QA] Sub-task description

## Update Skills (6)

| Skill | Args | Phases | Role | Output | Triggers |
| --- | --- | --- | --- | --- | --- |
| `/update-epic` | `BEP-XXX [changes]` | 5 | Sr. Product Manager | Updated Epic | "update epic", "edit epic" |
| `/update-story` | `BEP-XXX [changes]` | 5 | Sr. Product Owner | Updated Story | "update story", "edit story" |
| `/update-task` | `BEP-XXX [changes]` | 5 | Developer / Tech Lead | Updated Task | "update task", "edit task" |
| `/update-subtask` | `BEP-XXX [changes]` | 5 | Technical Analyst | Updated Sub-task | "update subtask" |
| `/update-doc` | `PAGE-ID [changes]` | 5 | Developer / Tech Lead | Updated Page | "update doc", "move page" |
| `/search-issues` | `[keyword] [--filters]` | 3 | Any | Matching issues | "search", "find" |

### Key Details

- Update skills share 5-phase pattern: Fetch → Impact Analysis → Preserve Intent → Generate → Apply
- **`/update-doc`** — Also supports `--move parent-id`
- **`/search-issues`** — Always run before creating to prevent duplicates

## Composite Skills (4) ⭐

| Skill | Args | Phases | Role | Output | Triggers |
| --- | --- | --- | --- | --- | --- |
| `/story-full` | `[description]` | 10 | PO + TA Combined | Story + Sub-tasks | "story full", "full workflow" |
| `/story-cascade` | `BEP-XXX [changes]` | 8 | PO + TA Combined | Updated Story + Subs | "cascade", "update all" |
| `/sync-alignment` | `BEP-XXX [changes]` | 8 | PO + TA + Tech Lead | All related artifacts | "sync", "align" |
| `/plan-sprint` | `[--sprint ID]` | 8 | Scrum Master (Tresor) | Sprint plan + assignments | "plan sprint" |

### Key Details

- **`/story-full`** — Most used. Creates Story (Phase 1-4) then Sub-tasks (Phase 5-10) in one workflow
- **`/story-cascade`** — Auto-cascade changes to related Sub-tasks
- **`/sync-alignment`** — Bidirectional: any artifact → detect changes → update all (Jira + Confluence)
- **`/plan-sprint`** — Tresor handles strategy (Phase 3-6), MCP handles execution (Phase 1,2,8)

## Utility Skills (2)

| Skill | Args | Phases | Role | Output | Triggers |
| --- | --- | --- | --- | --- | --- |
| `/verify-issue` | `BEP-XXX [--fix]` | 6 | Any | Report / Fixed issues | "verify", "check quality" |
| `/optimize-context` | `[--dry-run]` | - | Meta (global) | Updated CLAUDE.md | "optimize context" |

### Key Details

- **`/verify-issue`** — `--with-subtasks` = batch check, `--fix` = auto-fix + format migration
- **`/optimize-context`** — Global skill (not in `.claude/skills/`), audits passive context

> **Tool selection, scripts, shared references** → see `CLAUDE.md` Passive Context + References sections

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
/search-issues ← always run before creating (prevent duplicates)
       ↓
/create-epic ──→ /create-story ──→ /analyze-story ──→ /create-testplan
                       │                 │
                       └─ /story-full ⭐ ┘  (combines both in one go)
                       │
                       └─ /story-cascade ⭐  (update story → cascade to subs)
                       └─ /sync-alignment ⭐ (sync all: Jira + Confluence)

/create-task, /create-doc, /update-doc ──────────── (standalone)
/plan-sprint ⭐ ─────────────────────────────────── (reads Jira, assigns work)
/verify-issue ← always run after creating/updating
```

---

*Last updated: Feb 3, 2026*
