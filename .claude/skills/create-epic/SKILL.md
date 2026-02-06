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

## Phases

### 1. Discovery

- Interview stakeholder: Problem? Target users? Business value? Success metrics?
- If existing docs available → read context
- **VS Planning:** Identify potential vertical slices (what distinct user flows exist?)
- **Gate:** Stakeholder confirms understanding

### 2. RICE Prioritization

- **R**each (1-10): Number of users affected
- **I**mpact (0.25-3): Level of impact on user
- **C**onfidence (0-100%): Confidence in estimate
- **E**ffort (person-weeks): Effort required
- Formula: `(R × I × C) / E`
- **Gate:** Stakeholder agrees with priority

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
- **Gate:** Stakeholder approves scope + VS plan

### 4. Create Artifacts

1. **Epic Doc** → `MCP: confluence_create_page(space_key: "BEP")`
   - Include VS Map table in Epic Doc
2. **Epic** → `acli jira workitem create --from-json tasks/epic.json`
   - Add labels: feature label + `vs-planned`
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

**ADF Restrictions:**

- ❌ Do not nest tables inside panels (will error)
- ✅ Use paragraphs or bulletList inside panels instead

---

## References

- [ADF Core Rules](../shared-references/templates.md) - CREATE/EDIT rules, panels, styling
- [Templates](../shared-references/templates.md) - ADF templates (Epic section)
- [Tool Selection](../shared-references/tools.md) - Tool selection, effort sizing
- [Vertical Slice Guide](../shared-references/vertical-slice-guide.md) - VS patterns, decomposition
- After creation: `/verify-issue BEP-XXX`
