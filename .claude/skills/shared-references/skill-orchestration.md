# Skill Orchestration

> Intent-to-skill mapping, Tresor team collaboration, quality gates, and decision trees.
> Read this before creating/editing Jira issues.

## Intent-to-Skill Map

| Intent | Skill Chain | Tresor Team | Gate |
| --- | --- | --- | --- |
| Create epic | `/search-issues` → `/create-epic` → verify | `product/management/product-manager` | ≥ 90% |
| Create story | `/search-issues` → `/story-full` → verify | `product/management/requirements-generator` | ≥ 90% |
| Create task | `/search-issues` → `/create-task` → verify | — | ≥ 90% |
| Analyze story | `/analyze-story` → verify `--with-subtasks` | `engineering/backend/backend-architect` | ≥ 90% |
| Test plan | `/create-testplan` → verify | `core/test-engineer` | ≥ 90% |
| Update single | `/update-{epic,story,task,subtask}` → verify | — | ≥ 90% |
| Update cascade | `/story-cascade` → verify `--with-subtasks` | — | ≥ 90% |
| Sync all | `/sync-alignment` → verify `--with-subtasks` | — | ≥ 90% |
| Plan sprint | `/plan-sprint` → `/dependency-chain` | `product/management/sprint-prioritizer` | N/A |

**Rules:**

- Always `/search-issues` before creating (dedup)
- Always `/verify-issue` after creating/editing
- Prefer `/story-full` over separate `/create-story` + `/analyze-story`

## Tresor Cross-Team Collaboration

When to invoke 2+ teams together:

| Scenario | Product | Engineering | Core | Design |
| --- | --- | --- | --- | --- |
| **Epic creation** | `product-manager` scope+RICE | `backend-architect` feasibility | — | `ui-ux-analyst` if UI |
| **Story refinement** | `requirements-generator` ACs | `backend-architect` tech approach | — | `ui-ux-analyst` if UI |
| **Technical analysis** | — | `backend-architect` design | `test-engineer` test strategy | — |
| **Sprint planning** | `sprint-prioritizer` priority | — | — | — |
| **Auth/Payment** | `product-manager` | `backend-architect` | `security-auditor` MANDATORY | — |
| **Pre-launch** | `project-shipper` | — | `security-auditor` + `performance-tuner` | — |
| **Post-launch** | `feedback-synthesizer` | `root-cause-analyzer` if issues | — | — |
| **Tech debt** | — | `backend-architect` | `refactor-expert` + `test-engineer` | — |

### Tresor Decision Rules

- **Always** for epic creation → `product-manager` + `backend-architect`
- **Always** for sprint planning → `sprint-prioritizer`
- **If** story labels include `auth`, `payment`, `security`, `sensitive-data` → MUST `security-auditor`
- **If** story has UI components → `ui-ux-analyst`
- **If** high technical complexity → `backend-architect` for analyze-story

### Subagent Invocation

Tresor agents live at `~/.claude/subagents/{team}/{sub}/{name}/agent.md`

```text
Task(subagent_type="Explore") with context from agent.md
```

Key paths:

- `product/management/sprint-prioritizer/agent.md`
- `product/management/product-manager/agent.md`
- `engineering/backend/backend-architect/agent.md`
- `core/test-engineer/agent.md` (also available as Task agent)
- `core/security-auditor/agent.md` (also available as Task agent)
- `design/ui-ux/ui-ux-analyst/agent.md`

## Quality Gate Protocol

```text
BEFORE sending to Atlassian:
1. Generate content (ADF JSON)
2. Self-check against shared-references/verification-checklist.md
3. Score: Technical X/5 | Quality X/6 | Overall X%
4. If < 90% → auto-fix → re-score (max 2 attempts)
5. If >= 90% → proceed to Atlassian
6. If still < 90% after 2 fixes → ask user
7. After Atlassian write → cache_invalidate(issue_key)
```

### Scoring Reference

| Score | Status | Action |
| --- | --- | --- |
| 90-100% | Pass | Send to Atlassian |
| 70-89% | Warning | Auto-fix, then re-score |
| < 70% | Fail | Must fix, ask user if stuck |

### What Gets Scored

| Check | Max | Applies To |
| --- | --- | --- |
| T1-T5 Technical | 5 | All types |
| S1-S5 Story Quality | 6 | Story |
| ST1-ST5 Subtask Quality | 5 | Sub-task |
| QA1-QA5 QA Quality | 5 | QA Sub-task |
| E1-E4 Epic Quality | 4 | Epic |
| A1-A6 Alignment | 6 | `--with-subtasks` only |

Full checklist: `shared-references/verification-checklist.md`

## Decision Trees

### Create or Update?

```text
New requirement?
├─ Yes → /search-issues (dedup)
│        ├─ Duplicate found → /update-* or /story-cascade
│        └─ No duplicate → /story-full (preferred)
└─ No → Edit existing
         ├─ Single issue → /update-{type}
         ├─ Story + subtasks → /story-cascade
         └─ + Confluence → /sync-alignment
```

### story-full vs Separate?

```text
/story-full (default)
├─ Combined PO+TA = less context switching
├─ Use when: new story from scratch
└─ Output: Story + Sub-tasks in one go

Separate /create-story + /analyze-story
├─ Use when: story already exists, only need subtasks
└─ Use when: story needs PO review before TA
```

## Pre/Post Conditions

| Skill | Pre-condition | Post-condition | Tresor Review |
| --- | --- | --- | --- |
| `/create-epic` | `/search-issues` | `/verify-issue` >= 90% | `product-manager` scope |
| `/create-story` | `/search-issues` | `/verify-issue` >= 90% | — |
| `/story-full` | `/search-issues` | `/verify-issue --with-subtasks` >= 90% | `backend-architect` if complex |
| `/analyze-story` | Story exists | `/verify-issue --with-subtasks` >= 90% | `test-engineer` coverage |
| `/create-testplan` | Story exists | `/verify-issue` >= 90% | `test-engineer` comprehensive |
| `/create-task` | `/search-issues` | `/verify-issue` >= 90% | — |
| `/update-{type}` | Issue exists | `/verify-issue` >= 90% | — |
| `/story-cascade` | Story changed | `/verify-issue --with-subtasks` >= 90% | — |
| `/sync-alignment` | Artifacts exist | `/verify-issue --with-subtasks` >= 90% | — |
| `/plan-sprint` | Sprint exists | — | `sprint-prioritizer` always |
| `/dependency-chain` | Sprint planned | — | — |

## Cache Hygiene

- After any MCP write (`jira_update_issue`, `jira_create_issue`) → `cache_invalidate(issue_key)`
- After sprint manipulation → `cache_invalidate(sprint_id)`
- Before sprint planning → `cache_refresh(sprint_id)` for fresh data
