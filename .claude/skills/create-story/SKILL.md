---
name: create-story
description: |
  Create a new User Story from requirements with a 5-phase PO workflow
  Use when creating a new story, have a feature request, or need to convert requirements into a story
argument-hint: "[story-description]"
---

# /create-story

**Role:** Senior Product Owner
**Output:** User Story in Jira with ADF format

## Context Object (accumulated across phases)

| Phase | Adds to Context |
|-------|----------------|
| 1. Discovery | `epic_data`, `vs_assignment`, `user_requirements` |
| 2. Write Story | `story_narrative`, `acs[]`, `scope`, `dod` |
| 3. INVEST | `invest_score`, `vs_validated` |
| 4. QG | `qg_score`, `passed_qg` |
| 5. Create | `story_key` ({{PROJECT_KEY}}-XXX) |

## Gate Levels

| Level | Symbol | Behavior |
| --- | --- | --- |
| **AUTO** | 🟢 | Validate automatically. Pass → proceed. Fail → auto-fix (max 2). Still fail → escalate to user. |
| **REVIEW** | 🟡 | Present results to user, wait for quick confirmation. Default: proceed unless user objects. |
| **APPROVAL** | ⛔ | STOP. Wait for explicit user approval before proceeding. |

## Phases

> **Phase Tracking:** Use TodoWrite to mark each phase `in_progress` → `completed` as you work.

### 1. Discovery

- If Epic exists → `MCP: jira_get_issue` to read context + VS plan
- Ask user: Who? What? Why? Constraints?
- **VS Assignment:** Which vertical slice does this story belong to? (`vs1-skeleton`, `vs2-*`, `vs-enabler`)
- **⛔ GATE — DO NOT PROCEED** without user confirmation of requirements + VS assignment.

### 2. Write Story

```text
As a [persona],
I want to [action],
So that [benefit].
```

- Define ACs: Given/When/Then format
- Specify Scope (affected services) and DoD
- **VS Check:** Story delivers end-to-end value? All layers touched? (not shell-only or layer-split)
- Use Thai + transliteration
- **🟡 REVIEW** — Present story narrative, ACs, scope to user. Proceed unless user objects.

### 3. INVEST + VS Validation

| ✓ | Criteria | Question |
| --- | --- | --- |
| | Independent | Not dependent on other stories? |
| | Negotiable | Room for discussion? |
| | Valuable | Clear business value? |
| | Estimable | Can estimate effort? |
| | **Small + Vertical** | Completable in 1 sprint? **End-to-end slice?** |
| | Testable | All ACs verifiable in isolation? |

**VS Anti-pattern Check:**

- ❌ Shell-only (UI ไม่มี logic) → เพิ่ม minimal happy path
- ❌ Layer-split (BE แยกจาก FE) → รวมเป็น story เดียว
- ❌ Tab-split → split ตาม business rule แทน

**🟢 AUTO** — Validate all criteria. If any fail or VS anti-pattern detected → auto-fix and re-validate. Escalate to user only if unfixable.

### 4. Quality Gate (MANDATORY)

> **🟢 AUTO** — Score → auto-fix → re-score. Escalate only if still < 90% after 2 attempts.
> HR1: DO NOT send Story to Atlassian without QG ≥ 90%.

Score against `shared-references/verification-checklist.md`:

1. Score each check with confidence (0-100%). Only report issues with confidence ≥ 80%.
2. Report: `Technical X/5 | Story Quality X/6 | Overall X%`
3. If < 90% → auto-fix → re-score (max 2 attempts)
4. If ≥ 90% → proceed to Phase 5 automatically
5. If still < 90% after 2 fixes → escalate to user
6. Low-confidence items (< 80%) → flag as "needs review" but don't fail QG

### 5. Create in Jira

> **🟢 AUTO** — If QG passed → create automatically. No user interaction needed.

```bash
acli jira workitem create --from-json tasks/story.json
```

- ADF: Info panel (narrative) + Success panels (ACs)
- **Labels (MANDATORY):**
  - Feature label: `coupon-web`, `credit-topup`, etc.
  - VS label: `vs1-skeleton`, `vs2-credit-e2e`, `vs-enabler`, etc.
  - ดู convention: [Vertical Slice Guide](../shared-references/vertical-slice-guide.md)

> **🟢 AUTO** — HR6: `cache_invalidate(story_key)` after create.

### 6. Handoff

```text
## Story Created: [Title] ({{PROJECT_KEY}}-XXX)
ACs: N | Scope: [services]
→ Use /analyze-story {{PROJECT_KEY}}-XXX to continue
```

---

## References

- [ADF Core Rules](../shared-references/templates.md) - CREATE/EDIT rules, panels, styling
- [Templates](../shared-references/templates.md) - ADF templates (Story section)
- [Vertical Slice Guide](../shared-references/vertical-slice-guide.md) - VS patterns, labels, DoD
- [Verification Checklist](../shared-references/verification-checklist.md) - INVEST, AC quality
- After creation: `/verify-issue {{PROJECT_KEY}}-XXX`
