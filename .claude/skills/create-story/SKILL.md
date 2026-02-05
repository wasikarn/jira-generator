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

## Phases

### 1. Discovery

- If Epic exists → `MCP: jira_get_issue` to read context + VS plan
- Ask user: Who? What? Why? Constraints?
- **VS Assignment:** Which vertical slice does this story belong to? (`vs1-skeleton`, `vs2-*`, `vs-enabler`)
- **Gate:** User confirms understanding + VS assignment

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
- **Gate:** User reviews draft + VS integrity

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

**Gate:** All criteria pass + VS integrity confirmed

### 4. Create in Jira

```bash
acli jira workitem create --from-json tasks/story.json
```

- ADF: Info panel (narrative) + Success panels (ACs)
- **Labels (MANDATORY):**
  - Feature label: `coupon-web`, `credit-topup`, etc.
  - VS label: `vs1-skeleton`, `vs2-credit-e2e`, `vs-enabler`, etc.
  - ดู convention: [Vertical Slice Guide](../shared-references/vertical-slice-guide.md)

### 5. Handoff

```text
## Story Created: [Title] (BEP-XXX)
ACs: N | Scope: [services]
→ Use /analyze-story BEP-XXX to continue
```

---

## References

- [ADF Core Rules](../shared-references/templates.md) - CREATE/EDIT rules, panels, styling
- [Story Template](../shared-references/templates-story.md) - Story ADF structure
- [Vertical Slice Guide](../shared-references/vertical-slice-guide.md) - VS patterns, labels, DoD
- [Verification Checklist](../shared-references/verification-checklist.md) - INVEST, AC quality
- After creation: `/verify-issue BEP-XXX`
