---
name: create-doc
description: |
  สร้าง Confluence page จาก template ด้วย 4-phase workflow
  รองรับ: tech-spec, adr (Architecture Decision Record)

  Triggers: "create doc", "สร้าง doc", "technical spec", "ADR"
argument-hint: "[template] [title]"
---

# /create-doc

**Role:** Developer / Tech Lead
**Output:** Confluence Page

## Templates

| Template | Use Case | Structure |
| --- | --- | --- |
| `tech-spec` | API design, Feature spec | Overview → Requirements → Design → API → Testing |
| `adr` | Architecture Decision | Context → Decision → Consequences |

---

## Phases

### 1. Discovery

ถาม user เพื่อ gather ข้อมูล:

**ถ้าไม่ระบุ template:**

```text
ต้องการสร้าง Document ประเภทไหน?
1. tech-spec - Technical Specification
2. adr - Architecture Decision Record
```

**Gather details ตาม template:**

| Template | Required Info |
| --- | --- |
| `tech-spec` | Title, Overview, Related Jira issue |
| `adr` | Title, Context, Options considered |

**Gate:** User provides required info

---

### 2. Generate Content

สร้าง markdown content ตาม template

**tech-spec Template:**

```markdown
# [Title] - Technical Specification

## Overview
[Brief description of what this spec covers]

## Related Issues
- [BEP-XXX](https://100-stars.atlassian.net/browse/BEP-XXX)

---

## Requirements

### Functional Requirements
- FR-1: [Requirement]
- FR-2: [Requirement]

### Non-Functional Requirements
- NFR-1: [Performance/Security/etc.]

---

## Design

### Architecture
[High-level architecture description]

### Data Model
[Database changes if any]

### Sequence Diagram
[Flow description or diagram]

---

## API Specification

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/v1/resource | Create resource |
| GET | /api/v1/resource/:id | Get resource |

### Request/Response Examples
[Code examples]

---

## Testing Strategy

### Unit Tests
- [Test case 1]

### Integration Tests
- [Test case 1]

### Manual Testing
- [Test scenario 1]

---

## Rollout Plan
1. Deploy to staging
2. QA verification
3. Deploy to production

## Rollback Plan
[How to rollback if issues arise]
```

**adr Template:**

```markdown
# ADR-XXX: [Title]

## Status
Proposed | Accepted | Deprecated | Superseded

## Context
[What is the issue that we're seeing that is motivating this decision?]

## Decision
[What is the change that we're proposing and/or doing?]

## Options Considered

### Option 1: [Name]
**Pros:**
- [Pro 1]

**Cons:**
- [Con 1]

### Option 2: [Name]
**Pros:**
- [Pro 1]

**Cons:**
- [Con 1]

## Consequences

### Positive
- [Positive consequence 1]

### Negative
- [Negative consequence 1]

## Related
- [Link to related ADRs or issues]
```

**Gate:** Content generated

---

### 3. Review

แสดง preview ให้ user ตรวจสอบ:

```text
## Document Preview

**Template:** [tech-spec/adr]
**Title:** [title]
**Space:** BEP

[Show markdown content]

ต้องการปรับแก้อะไรก่อน create หรือไม่?
```

**Gate:** User approves content

---

### 4. Create

```typescript
confluence_create_page({
  space_key: "BEP",
  title: "[Title]",
  content: "[markdown content]",
  parent_id: "[optional parent page ID]"
})
```

**Output:**

```text
## ✅ Document Created: [Title]

**Template:** [type]
**Space:** BEP

🔗 [View in Confluence](URL)

→ Link to Jira: ใช้ MCP jira_create_remote_issue_link
```

---

## Common Scenarios

| Scenario | Command |
| --- | --- |
| สร้าง Tech Spec | `/create-doc tech-spec "Payment API"` |
| สร้าง ADR | `/create-doc adr "Use Redis for caching"` |

---

## References

- Space: `BEP`
- MCP Tool: `confluence_create_page`
