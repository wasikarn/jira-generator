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

- If Epic exists → `MCP: jira_get_issue` to read context
- Ask user: Who? What? Why? Constraints?
- **Gate:** User confirms understanding

### 2. Write Story

```text
As a [persona],
I want to [action],
So that [benefit].
```

- Define ACs: Given/When/Then format
- Specify Scope (affected services) and DoD
- Use Thai + transliteration
- **Gate:** User reviews draft

### 3. INVEST Validation

| ✓ | Criteria | Question |
| --- | --- | --- |
| | Independent | Not dependent on other stories? |
| | Negotiable | Room for discussion? |
| | Valuable | Clear business value? |
| | Estimable | Can estimate effort? |
| | Small | Completable in 1 sprint? |
| | Testable | All ACs verifiable? |

**Gate:** All criteria pass

### 4. Create in Jira

```bash
acli jira workitem create --from-json tasks/story.json
```

- ADF: Info panel (narrative) + Success panels (ACs)

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
- [Verification Checklist](../shared-references/verification-checklist.md) - INVEST, AC quality
- After creation: `/verify-issue BEP-XXX`
