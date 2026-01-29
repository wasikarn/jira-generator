---
name: create-epic
description: |
  สร้าง Epic + Epic Doc จาก product vision ด้วย 5-phase PM workflow
  ใช้เมื่อต้องการสร้าง initiative ใหม่, มี product vision, หรือต้องการทำ RICE prioritization
argument-hint: "[epic-title]"
---

# /create-epic

**Role:** Senior Product Manager
**Output:** Epic in Jira + Epic Doc in Confluence

## Phases

### 1. Discovery

- สัมภาษณ์ stakeholder: Problem? Target users? Business value? Success metrics?
- ถ้ามี existing docs → อ่าน context
- **Gate:** Stakeholder confirms understanding

### 2. RICE Prioritization

- **R**each (1-10): จำนวน users ที่ได้รับผลกระทบ
- **I**mpact (0.25-3): ระดับ impact ต่อ user
- **C**onfidence (0-100%): ความมั่นใจใน estimate
- **E**ffort (person-weeks): effort ที่ต้องใช้
- Formula: `(R × I × C) / E`
- **Gate:** Stakeholder agrees with priority

### 3. Define Scope

- ระบุ high-level requirements
- แบ่งเป็น User Stories (draft): Story 1, Story 2, ...
- กำหนด MVP: Must have / Should have / Nice to have
- ระบุ Dependencies และ Risks
- **Gate:** Stakeholder approves scope

### 4. Create Artifacts

1. **Epic Doc** → `MCP: confluence_create_page(space_key: "BEP")`
2. **Epic** → `acli jira workitem create --from-json tasks/epic.json`
3. **Link** Epic to Doc

### 5. Handoff

```text
## Epic Created: [Title] (BEP-XXX)
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

**ข้อห้าม ADF:**

- ❌ ห้าม nest table ใน panel (จะ error)
- ✅ ใช้ paragraphs หรือ bulletList ใน panel แทน

---

## References

- [ADF Core Rules](../shared-references/templates.md) - CREATE/EDIT rules, panels, styling
- [Epic Template](../shared-references/templates-epic.md) - Epic ADF structure
- [Workflows](../shared-references/workflows.md) - Phase patterns, tool selection
- After creation: `/verify-issue BEP-XXX`
