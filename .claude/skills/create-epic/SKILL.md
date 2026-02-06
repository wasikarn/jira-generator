---
name: create-epic
description: |
  Create Epic + Epic Doc from product vision with a 5-phase PM workflow
  Use when creating a new initiative, have a product vision, or need RICE prioritization
argument-hint: "[epic-title]"
---

# /create-epic

**Role:** Senior Product Manager
**Output:** Epic in Jira + Epic Doc in Confluence

## Context Object (accumulated across phases)

| Phase | Adds to Context |
|-------|----------------|
| 1. Discovery | `stakeholder_input`, `vs_plan`, `user_requirements` |
| 2. RICE | `rice_score`, `priority` |
| 3. Scope | `scope_items[]`, `vs_stories[]`, `mvp_definition` |
| 4. QG | `qg_score`, `passed_qg` |
| 5. Create | `epic_key`, `epic_doc_id` |

## Gate Levels

| Level | Symbol | Behavior |
| --- | --- | --- |
| **AUTO** | 🟢 | Validate automatically. Pass → proceed. Fail → auto-fix (max 2). Still fail → escalate to user. |
| **REVIEW** | 🟡 | Present results to user, wait for quick confirmation. Default: proceed unless user objects. |
| **APPROVAL** | ⛔ | STOP. Wait for explicit user approval before proceeding. |

## Phases

> **Phase Tracking:** Use TodoWrite to mark each phase `in_progress` → `completed` as you work.

### 1. Discovery

- Interview stakeholder: Problem? Target users? Business value? Success metrics?
- If existing docs available → read context
- **VS Planning:** Identify potential vertical slices (what distinct user flows exist?)
- **⛔ GATE — DO NOT PROCEED** without stakeholder confirmation of problem understanding + VS planning.

### 2. RICE Prioritization

- **R**each (1-10): Number of users affected
- **I**mpact (0.25-3): Level of impact on user
- **C**onfidence (0-100%): Confidence in estimate
- **E**ffort (person-weeks): Effort required
- Formula: `(R × I × C) / E`
- **🟡 REVIEW** — Present RICE scoring to stakeholder. Proceed unless stakeholder objects.

### 3. Define Scope + VS Planning

- Identify high-level requirements
- **VS Pattern Selection:** (see [vertical-slice-guide.md](../shared-references/vertical-slice-guide.md))
  - Walking Skeleton? → `vs1-skeleton`
  - Enablers needed? → `vs-enabler`
  - Business rule splits? → `vs2-*`, `vs3-*`
- Break into User Stories by VS (draft):
  - vs1-skeleton: Story A, Story B
  - vs2-{rule}: Story C, Story D
- Define MVP: Which VS are must-have vs nice-to-have?
- Identify Dependencies and Risks
- **⛔ GATE — DO NOT PROCEED** without stakeholder approval of scope + VS plan + MVP definition.

### 4. Quality Gate (MANDATORY)

> **🟢 AUTO** — Score → auto-fix → re-score. Escalate only if still < 90% after 2 attempts.
> HR1: DO NOT send Epic to Atlassian without QG ≥ 90%.

Score against `shared-references/verification-checklist.md`:

1. Score each check with confidence (0-100%). Only report issues with confidence ≥ 80%.
2. Report: `Technical X/5 | Epic Quality X/4 | Overall X%`
3. If < 90% → auto-fix → re-score (max 2 attempts)
4. If ≥ 90% → proceed to Phase 5 automatically
5. If still < 90% after 2 fixes → escalate to user
6. Low-confidence items (< 80%) → flag as "needs review" but don't fail QG

### 5. Create Artifacts

> **🟢 AUTO** — If QG passed → create automatically. No user interaction needed.

1. **Epic Doc** → `MCP: confluence_create_page(space_key: "{{PROJECT_KEY}}")`
   - Include VS Map table in Epic Doc
2. **Epic** → `acli jira workitem create --from-json tasks/epic.json`
   - Add labels: feature label + `vs-planned`
3. **Link** Epic to Doc

> **🟢 AUTO** — HR6: `cache_invalidate(epic_key)` after create.

### 6. Handoff

```text
## Epic Created: [Title] ({{PROJECT_KEY}}-XXX)
RICE Score: X | Stories: N planned
Epic Doc: [link] | Epic: [link]
→ Use /create-story to continue
```

---

## Epic Structure (ADF)

| Section | Panel Type | Content |
| --- | --- | --- |
| 🎯 Epic Overview | `info` | Summary + scope statement |
| 💰 Business Value | `success` | Revenue, Retention, Operations |
| 📦 Scope | `info` + table | Features/modules breakdown |
| 📊 RICE Score | table | R/I/C/E + final score |
| 🎯 Success Metrics | table | KPIs + targets |
| 📋 User Stories | `info` panels | Grouped by feature area |
| 📈 Progress | `note` | Done/In Progress/To Do counts |
| 🔗 Links | table | Epic Doc, Technical Notes |

**ADF Restrictions:**

- ❌ Do not nest tables inside panels (will error)
- ✅ Use paragraphs or bulletList inside panels instead

---

## References

- [ADF Core Rules](../shared-references/templates.md) - CREATE/EDIT rules, panels, styling
- [Templates](../shared-references/templates.md) - ADF templates (Epic section)
- [Tool Selection](../shared-references/tools.md) - Tool selection, effort sizing
- [Vertical Slice Guide](../shared-references/vertical-slice-guide.md) - VS patterns, decomposition
- After creation: `/verify-issue {{PROJECT_KEY}}-XXX`
