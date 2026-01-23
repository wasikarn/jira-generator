# Epic Doc Template

> **Version:** 3.0 | **Updated:** 2025-01-22

---

## Usage

**Naming:** `Epic: [Epic Name] (BEP-XXX)`

**Location:** Confluence Space BEP → Root level

**When:** Epic มี 5+ stories หรือต้อง communicate กับ stakeholders

---

## Template (Copy ไปใช้เลย)

```markdown
# [Epic Name]

> **Epic:** [BEP-XXX](https://100-stars.atlassian.net/browse/BEP-XXX)  
> **Status:** 🔵 To Do / 🟡 In Progress / ✅ Done  
> **Stories:** X total (Y active, Z done)  
> **Duration:** X Sprints  
> **Updated:** YYYY-MM-DD

---

## Overview

[อธิบาย 2-3 ประโยค: ทำอะไร, ทำไม, ใครได้ประโยชน์]

**Problem:** [ปัญหาที่แก้]
**Solution:** [Solution ที่ทำ]
**Value:** [Business value]

---

## Goals & Success

| Goal | Target | Measure |
| --- | --- | --- |
| [Goal 1] | [Target] | [How] |
| [Goal 2] | [Target] | [How] |

---

## User Stories

### Phase 1: [Name] (Sprint X-Y)

| Key | Summary | Status | Points |
| --- | --- | --- | --- |
| [BEP-XXX](link) | [Name] | To Do | X |
| [BEP-YYY](link) | [Name] | Done | Y |

**Deliverable:** [สิ่งที่ user ได้เมื่อจบ Phase นี้]

### Phase 2: [Name] (Sprint Y-Z)

| Key | Summary | Status | Points |
| --- | --- | --- | --- |
| [BEP-ZZZ](link) | [Name] | To Do | X |

**Deliverable:** [สิ่งที่ user ได้]

---

## Dependencies (ถ้ามี)

```
BEP-XXX → BEP-YYY → BEP-ZZZ
```

| Story | Depends On | Status |
| --- | --- | --- |
| [BEP-YYY](link) | [BEP-XXX](link) | ✅ Done |

---

## Risks (ถ้ามี)

| Risk | Impact | Mitigation |
| --- | --- | --- |
| [Risk] | High/Med/Low | [Action] |

---

## Links

- 🎨 Design: [Figma](url)
- 📋 Jira: [Epic](url)
- 📖 PRD: [Doc](url)

---

## Child Docs

| Story | Status |
| --- | --- |
| [User Story: Name](confluence-link) | Draft/Done |

---

_Updated: YYYY-MM-DD_
```

---

## Section Guide

| Section | When to Include |
| --- | --- |
| Overview | ✅ Always |
| Goals & Success | ✅ Always |
| User Stories | ✅ Always |
| Dependencies | ⚠️ When stories มี dependencies |
| Risks | ⚠️ Complex/risky epics |
| Links | ✅ Always |
| Child Docs | ✅ Always |

---

## Variants

**Simple (< 5 stories):** Overview + Stories + Links

**Standard (5-15 stories):** Full template

**Complex (> 15 stories):** Add Timeline section, Stakeholders table

---

## Writing Style

- **กระชับ** - stakeholder อ่านเข้าใจเร็ว
- **ทับศัพท์** - milestone, deliverable, phase, sprint
- **เป็นกันเอง** - คุยกับทีม casual

_See `references/shared-config.md` for Language Guidelines_
_For detailed explanations, see `references/templates.md`_
