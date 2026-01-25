---
name: create-story
description: |
  สร้าง User Story ใหม่จาก requirements ด้วย 5-phase PO workflow
  ใช้เมื่อต้องการสร้าง story ใหม่, มี feature request, หรือต้องการแปลง requirements เป็น story
argument-hint: "[story-description]"
---

# /create-story

**Role:** Senior Product Owner
**Output:** User Story in Jira with ADF format

## Phases

### 1. Discovery

- ถ้ามี Epic → `MCP: jira_get_issue` เพื่อดู context
- ถาม user: Who? What? Why? Constraints?
- **Gate:** User confirms understanding

### 2. Write Story

```text
As a [persona],
I want to [action],
So that [benefit].
```

- กำหนด ACs: Given/When/Then format
- ระบุ Scope (affected services) และ DoD
- ใช้ภาษาไทย + ทับศัพท์
- **Gate:** User reviews draft

### 3. INVEST Validation

| ✓ | Criteria | Question |
| --- | --- | --- |
| | Independent | ไม่พึ่งพา story อื่น? |
| | Negotiable | มี room สำหรับ discussion? |
| | Valuable | มี business value ชัดเจน? |
| | Estimable | ประเมิน effort ได้? |
| | Small | ทำเสร็จใน 1 sprint? |
| | Testable | ทุก AC verify ได้? |

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

- [ADF Templates](../shared-references/templates.md) - Story ADF structure
- [Workflows](../shared-references/workflows.md) - INVEST, AC format
- After creation: `/verify-issue BEP-XXX`
