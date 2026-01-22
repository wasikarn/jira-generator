# Test Plan Template

> **Version:** 1.0 | **Updated:** 2026-01-22

---

## Usage

**Naming:** `Test Plan: [Feature Name] (BEP-XXX)`

**Location:** Confluence → Under Epic Doc (child page)

**Owner:** QA Analyst

**When:** Story มี multiple ACs, complex flows, หรือต้องการ track test coverage

---

## Template (Copy ไปใช้เลย)

```markdown
# Test Plan: [Feature Name]

> **Story:** [BEP-XXX](https://100-stars.atlassian.net/browse/BEP-XXX)
> **Epic:** [BEP-YYY](link) - [Epic Name]
> **Status:** Draft / Ready / In Progress / Complete
> **Updated:** YYYY-MM-DD

---

## Overview

[อธิบาย 2-3 ประโยค: test อะไร, ทำไม, scope กว้างแค่ไหน]

**Story:**
> As a [persona],
> I want to [action],
> So that [benefit].

---

## Test Scope

### In Scope
- [Feature/area ที่ test]
- [Feature/area ที่ test]

### Out of Scope
- [Feature/area ที่ไม่ test ใน plan นี้]

---

## AC Coverage Matrix

| AC | Description | Test Cases | Priority | Status |
| --- | --- | --- | --- | --- |
| AC1 | [description] | TC1, TC2 | High | ⬜ |
| AC2 | [description] | TC3 | Medium | ⬜ |
| AC3 | [description] | TC4, TC5 | High | ⬜ |

**Coverage:** [X] test cases / [Y] ACs = 100%

---

## Test Scenarios

### Happy Path
| ID | Scenario | AC | Priority |
| --- | --- | --- | --- |
| TC1 | [Normal flow succeeds] | AC1 | High |
| TC2 | [Alternative success path] | AC1 | Medium |

### Error Cases
| ID | Scenario | AC | Priority |
| --- | --- | --- | --- |
| TC3 | [Invalid input rejected] | AC2 | High |
| TC4 | [System error handled] | AC3 | Medium |

### Edge Cases
| ID | Scenario | AC | Priority |
| --- | --- | --- | --- |
| TC5 | [Boundary condition] | AC3 | Low |

---

## Test Data Requirements

| Data | Description | Source |
| --- | --- | --- |
| [Data type] | [Description] | [Manual/Seed/API] |
| Test user | User with specific role | Seed data |
| Test product | Product with specific attributes | Manual setup |

---

## Environment

| Environment | URL | Notes |
| --- | --- | --- |
| Staging | [URL] | Primary test env |
| Dev | [URL] | If staging unavailable |

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
| --- | --- | --- | --- |
| [Risk description] | High/Med/Low | High/Med/Low | [Action] |
| Data dependency | Medium | Medium | Prepare seed data |
| Third-party API | High | Low | Mock responses |

---

## Test Cases (Jira Links)

| Key | Summary | Priority | Status |
| --- | --- | --- | --- |
| [BEP-XXX](link) | [QA] - Test: [desc] | High | ⬜ |
| [BEP-YYY](link) | [QA] - Test: [desc] | Medium | ⬜ |

---

## Links

- 📋 User Story: [BEP-XXX](link)
- 📁 Epic Doc: [link]
- 📄 Technical Note: [link]
- 🎨 Design: [Figma link]

---

_Updated: YYYY-MM-DD_
```

---

## Section Guide

| Section | When |
| --- | --- |
| Overview | ✅ Always |
| Test Scope | ✅ Always |
| AC Coverage Matrix | ✅ Always |
| Test Scenarios | ✅ Always |
| Test Data | ⚠️ If specific data needed |
| Environment | ⚠️ If multiple envs |
| Risk Assessment | ⚠️ If risks identified |
| Test Cases | ✅ Always (after creating Jira) |
| Links | ✅ Always |

---

## Variants

**Simple (1-2 ACs):** Overview + AC Coverage + Test Scenarios + Links

**Standard (3-5 ACs):** + Test Data + Test Cases

**Complex (5+ ACs):** Full template + Risk Assessment + Environment

---

## Status Legend

| Symbol | Meaning |
| --- | --- |
| ⬜ | Not started |
| 🔄 | In progress |
| ✅ | Complete |
| ❌ | Blocked/Failed |

---

_For QA checklists, see `references/checklists.md`_
