---
name: create-doc
description: |
  สร้าง Confluence page จาก template ด้วย 4-phase workflow
  รองรับ: tech-spec, adr, parent (category page)

  Triggers: "create doc", "สร้าง doc", "technical spec", "ADR"
argument-hint: "[template] [title] [--parent page-id]"
---

# /create-doc

**Role:** Developer / Tech Lead
**Output:** Confluence Page

## Templates

| Template | Use Case | Structure |
| --- | --- | --- |
| `tech-spec` | API design, Feature spec | Overview → Requirements → Design → API → Testing |
| `adr` | Architecture Decision | Context → Decision → Consequences |
| `parent` | Category/Parent page | Title → Description → Sub-pages table |

---

## Phases

### 1. Discovery

ถาม user เพื่อ gather ข้อมูล:

**ถ้าไม่ระบุ template:**

```text
ต้องการสร้าง Document ประเภทไหน?
1. tech-spec - Technical Specification
2. adr - Architecture Decision Record
3. parent - Category/Parent page (จัดกลุ่ม pages)
```

**Gather details ตาม template:**

| Template | Required Info |
| --- | --- |
| `tech-spec` | Title, Overview, Related Jira issue |
| `adr` | Title, Context, Options considered |
| `parent` | Title, Description, Category type |

**ถ้าต้องการสร้างเป็น child ของ page อื่น:**

```text
ต้องการสร้างภายใต้ parent page ไหน?
1. Root (ไม่มี parent)
2. ระบุ Page ID
3. ค้นหาจาก title
```

**ค้นหา parent page:**

```python
confluence_search(query="title ~ \"[search term]\"", limit=5)
```

**Gate:** User provides required info + Parent page identified (if specified)

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

**parent Template:**

```markdown
# [Title]

[Brief description of what this category contains]

{toc:maxLevel=2}

---

## 📄 Sub-pages

{children:all=true|sort=title}

---

## 🏷️ Topics Covered

| Topic | Description |
| --- | --- |
| [Topic 1] | [Description] |
| [Topic 2] | [Description] |

---

## 🔗 Related

- [Link to related pages or issues]

---

*Last updated: [date]*
```

> **Note:** `{toc}` และ `{children}` macros จะแสดงผลเฉพาะใน Confluence
> สำหรับ parent pages ที่ต้องการ macros ให้ใช้ `update_page_storage.py` script

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

สร้าง page ด้วย MCP tool:

```python
confluence_create_page(
  space_key="BEP",
  title="[Title]",
  content="[markdown content]",
  parent_id="[optional parent page ID]"
)
```

**⚠️ IMPORTANT: Fix Code Blocks (mandatory if content has code blocks)**

MCP markdown → Confluence จะ render code blocks เป็น `<pre class="highlight">` ซึ่งไม่ถูกต้อง
**ต้อง run fix script ทันทีหลัง create/update เสมอ:**

```bash
python3 .claude/skills/atlassian-scripts/scripts/fix_confluence_code_blocks.py \
  --page-id [created_page_id]
```

Script จะแปลงจาก `<pre class="highlight">` → `<ac:structured-macro ac:name="code">` ให้อัตโนมัติ

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
| สร้าง Parent page | `/create-doc parent "Documentation: Ads System"` |
| สร้างเป็น child | `/create-doc tech-spec "API Spec" --parent 153518083` |

---

## References

- Space: `BEP`
- MCP Tool: `confluence_create_page`
- Scripts: `.claude/skills/atlassian-scripts/scripts/`
- Related: `/update-doc` for updating existing pages
