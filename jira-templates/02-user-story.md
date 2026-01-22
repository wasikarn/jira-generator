# Jira User Story Template

> **Version:** 2.0 | **Updated:** 2025-01-22

---

## Summary Format

```
[Feature Name]
```

**Examples:**
- สร้างคูปองเติมเครดิต
- หน้า Coupon List
- แก้ไขคูปอง

---

## Description Template (Copy ไปใช้เลย)

```markdown
## User Story

> **As a** [persona],  
> **I want to** [action],  
> **So that** [benefit].

---

## Acceptance Criteria

**AC1: [Happy Path]**
Given [precondition]  
When [action]  
Then [result]

**AC2: [Validation]**
Given [invalid input]  
When [action]  
Then [validation error]

**AC3: [Error Case]**
Given [error condition]  
When [action]  
Then [error handling]

---

## Scope

| Service | Affected |
| --- | --- |
| Backend | ✅/❌ |
| Admin | ✅/❌ |
| Website | ✅/❌ |

---

## Business Rules (ถ้ามี)

| Rule | Description |
| --- | --- |
| BR-1 | [Rule] |

---

## Links

- 🎨 Design: [Figma]
- 📄 Story Doc: [Confluence]
```

---

## Other Fields

| Field | Value |
| --- | --- |
| Issue Type | Story |
| Project | BEP |
| Epic Link | [Parent Epic] |
| Story Points | 1, 2, 3, 5, 8, 13 |
| Priority | Highest/High/Medium/Low |

---

## Story Points Guide

| Points | Complexity | Duration |
| --- | --- | --- |
| 1 | Very Simple | < 0.5 day |
| 2 | Simple | 0.5-1 day |
| 3 | Medium | 1-2 days |
| 5 | Complex | 2-3 days |
| 8 | Very Complex | 3-5 days |
| 13 | ❌ Consider split | > 5 days |

---

## AC Format Options

**Option 1: Given-When-Then** (แนะนำ)
```
Given [context]
When [action]
Then [outcome]
```

**Option 2: Checklist**
```
- [ ] [Criterion]
```

**Option 3: Should-When**
```
Should [behavior] when [condition]
```

---

_See `references/checklists.md` for INVEST criteria_
