# /create-epic Command

> **Role:** Senior Product Manager
> **Input:** Product vision / Feature request
> **Output:** Epic + Epic Doc

---

## Usage

```
/create-epic
/create-epic "Coupon Management System"
```

---

## Five Phases

### Phase 1: Discovery

**Goal:** ทำความเข้าใจ product vision

**Actions:**
1. สัมภาษณ์ stakeholder เกี่ยวกับ:
   - Problem statement: ปัญหาอะไร?
   - Target users: ใครใช้?
   - Business value: ทำไมต้องทำ?
   - Success metrics: วัดผลอย่างไร?
   - Constraints: มีข้อจำกัดอะไร?

2. ถ้ามี existing docs → อ่าน context

**Output:** Vision summary

**Gate:** Stakeholder confirms understanding

---

### Phase 2: RICE Prioritization

**Goal:** ประเมินความสำคัญของ Epic

**RICE Score:**

| Factor | Score | Note |
|--------|-------|------|
| **R**each | 1-10 | จำนวน users ที่ได้รับผลกระทบ |
| **I**mpact | 0.25-3 | ระดับ impact ต่อ user (0.25=minimal, 3=massive) |
| **C**onfidence | 0-100% | ความมั่นใจใน estimate |
| **E**ffort | person-weeks | effort ที่ต้องใช้ |

```
RICE Score = (Reach × Impact × Confidence) / Effort
```

**Output:** RICE analysis

**Gate:** Stakeholder agrees with priority

---

### Phase 3: Define Epic Scope

**Goal:** กำหนดขอบเขตและแบ่ง User Stories

**Actions:**
1. ระบุ high-level requirements
2. แบ่งเป็น User Stories (draft):
   - Story 1: [title]
   - Story 2: [title]
   - ...

3. กำหนด MVP scope:
   - Must have: ...
   - Should have: ...
   - Nice to have: ...

4. ระบุ Dependencies และ Risks

**Output:** Epic scope document

**Gate:** Stakeholder approves scope

---

### Phase 4: Create Artifacts

**Goal:** สร้าง Epic และ Epic Doc

**Actions:**

1. **Create Epic Doc in Confluence:**
   ```
   MCP: confluence_create_page(
     space_key: "BEP",
     title: "[Epic Name] - Epic Document",
     content: [markdown content]
   )
   ```

   Content includes:
   - Executive Summary
   - Problem Statement
   - Proposed Solution
   - User Stories (list)
   - Success Metrics
   - Timeline
   - RICE Score

   **Template:** `confluence-templates/01-epic-doc.md`

2. **Create Epic in Jira:**
   ```bash
   acli jira workitem create --from-json tasks/bep-xxx-epic.json
   ```

   ADF Structure:
   - Info panel: Executive summary
   - Bullet list: High-level requirements
   - Table: User Stories (draft)
   - Link: Epic Doc

3. **Link Epic to Doc:**
   ```
   MCP: jira_update_issue - add Epic Doc link
   ```

**Output:** Epic URL + Epic Doc URL

---

### Phase 5: Handoff

**Goal:** ส่งต่อให้ PO

**Output Format:**

```markdown
## Epic Created: [Title] (BEP-XXX)

### Summary
[1-2 sentence summary]

### RICE Score
- Reach: X
- Impact: X
- Confidence: X%
- Effort: X weeks
- **Score:** X

### Planned User Stories
1. [Story 1 title]
2. [Story 2 title]
3. [Story 3 title]

### Documents
- Epic: [BEP-XXX](jira-link)
- Epic Doc: [Title](confluence-link)

### Handoff to PO
Epic: BEP-XXX
Stories to create: [count]
Ready for: User Story creation

Use `/create-story` to continue
```

---

## Quality Checklist

Before completing:
- [ ] Problem statement ชัดเจน
- [ ] RICE score calculated
- [ ] Scope defined (must/should/nice-to-have)
- [ ] User Stories identified (draft)
- [ ] Epic Doc created in Confluence
- [ ] Epic created in Jira with ADF format
- [ ] Epic linked to Epic Doc
- [ ] Handoff summary provided

---

## Error Recovery

| Error | Solution |
|-------|----------|
| Confluence create fails | Check space key (BEP), verify permissions |
| acli JSON error | Validate ADF structure, check field names |
| Epic Doc link fails | Manually add link via MCP jira_update_issue |
| RICE score unclear | Re-interview stakeholder for estimates |

---

## Epic vs User Story

| | Epic | User Story |
|---|------|------------|
| **Size** | Large, multi-sprint | Small, 1 sprint |
| **Detail** | High-level | Detailed ACs |
| **Deliverable** | Multiple features | 1 shippable feature |
| **Owner** | PM | PO |

---

## RICE Score Interpretation

| Score | Priority |
|-------|----------|
| > 10 | 🔴 Critical - Do now |
| 5-10 | 🟠 High - Do soon |
| 2-5 | 🟡 Medium - Plan for |
| < 2 | 🟢 Low - Maybe later |
