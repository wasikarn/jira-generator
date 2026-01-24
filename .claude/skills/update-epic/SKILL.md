---
name: update-epic
description: |
  แก้ไข Epic ที่มีอยู่ ด้วย 5-phase update workflow

  Phases: Fetch Current → Impact Analysis → Preserve Intent → Generate Update → Apply Update

  รองรับ: ปรับ scope, update RICE, เพิ่ม success metrics, format migration

  Triggers: "update epic", "แก้ไข epic", "ปรับ epic"
argument-hint: "[issue-key] [changes]"
---

# /update-epic Command

> **Role:** Senior Product Manager
> **Input:** Existing Epic (BEP-XXX)
> **Output:** Updated Epic

---

## Usage

```
/update-epic BEP-XXX
/update-epic BEP-XXX "ปรับ scope ลด feature Y ออก"
/update-epic BEP-XXX "update RICE score"
```

---

## Five Phases

### Phase 1: Fetch Current State

**Goal:** ดึง epic ปัจจุบันและ context

**Actions:**
1. Fetch Epic:
   ```
   MCP: jira_get_issue(issue_key: "BEP-XXX")
   ```
2. Fetch child stories:
   ```
   MCP: jira_search(jql: "parent = BEP-XXX OR 'Epic Link' = BEP-XXX")
   ```
3. Fetch Epic Doc (ถ้ามี):
   ```
   MCP: confluence_search(query: "Epic: [title]")
   ```
4. อ่าน:
   - Epic title/summary
   - Description/objectives
   - RICE prioritization
   - Success metrics
   - Child stories
   - Status

**Output:** Current state summary

```markdown
## Epic: [Title] (BEP-XXX)

### Overview
[Current description]

### RICE Score
| Factor | Score | Notes |
|--------|-------|-------|
| Reach | X | ... |
| Impact | X | ... |
| Confidence | X% | ... |
| Effort | X | ... |
| **Total** | XX | ... |

### Child Stories
| Key | Summary | Status |
|-----|---------|--------|
| BEP-YYY | Story 1 | In Progress |
| BEP-ZZZ | Story 2 | To Do |

### Epic Doc
[Link if exists]
```

**Gate:** User confirms what to update

---

### Phase 2: Impact Analysis

**Goal:** วิเคราะห์ผลกระทบของ changes

**Actions:**
1. ถ้าเปลี่ยน scope:
   - Stories ไหนกระทบ?
   - Stories ไหนต้องเพิ่ม/ลบ?
2. ถ้าเปลี่ยน timeline:
   - Sprint planning กระทบ?
3. ถ้าเปลี่ยน priority (RICE):
   - อาจกระทบ backlog prioritization

**Impact Matrix:**

| Change Type | Impact on Stories | Impact on Planning |
|-------------|------------------:|-------------------:|
| Add scope | ต้องสร้าง story ใหม่ | Re-estimate timeline |
| Remove scope | ต้อง close/remove stories | Timeline shorter |
| Modify objectives | ต้อง review stories | May need re-planning |
| RICE update | ❌ No impact | May reprioritize backlog |
| Format only | ❌ No impact | ❌ No impact |

**Output:** Impact analysis

**Gate:** User acknowledges impact

---

### Phase 3: Preserve Intent

**Goal:** รักษา core intent ของ epic

**Critical Rules:**
- ✅ ปรับ wording/clarify ได้
- ✅ Update RICE ได้ (based on new data)
- ✅ เพิ่ม success metrics ได้
- ⚠️ ระวังเปลี่ยน scope (กระทบ stories)
- ❌ ห้ามเปลี่ยน core business value โดยไม่บอก

**Actions:**
1. Document original:
   - Business objective
   - Target outcome
   - Success criteria
2. Compare with requested changes
3. Flag significant scope changes for explicit approval

**Output:** Intent preservation checklist

---

### Phase 4: Generate Update

**Goal:** สร้าง description ใหม่

**Actions:**
1. Generate ADF JSON:
   - Follow `jira-templates/01-epic.md` (if exists)
   - Use Thai + ทับศัพท์
   - Preserve original content (unless explicitly changed)

2. แสดง comparison:
   ```markdown
   ## Summary
   [No change / Changed: ...]

   ## Objectives
   | Objective | Status | Change |
   |-----------|--------|--------|
   | Obj1 | ✅ Kept | - |
   | Obj2 | ✏️ Modified | [what changed] |
   | Obj3 | ➕ New | [new objective] |

   ## RICE
   | Factor | Before | After | Change |
   |--------|--------|-------|--------|
   | Reach | 5 | 7 | ⬆️ +2 |
   | Impact | 3 | 3 | - |
   | Confidence | 80% | 90% | ⬆️ +10% |
   | Effort | 8 | 6 | ⬇️ -2 |

   ## Scope
   [No change / Added: ... / Removed: ...]
   ```

**Output:** Draft update for review

**Gate:** User approves changes

---

### Phase 5: Apply Update

**Goal:** Update ใน Jira

**Actions:**
1. Save ADF JSON:
   ```
   File: tasks/bep-xxx-epic-update.json
   ```

2. Update via acli:
   ```bash
   acli jira workitem edit --from-json tasks/bep-xxx-epic-update.json --yes
   ```

3. ถ้า scope เปลี่ยน:
   - List stories ที่ต้อง update
   - Suggest actions for each

4. ถ้ามี Epic Doc:
   - Remind to update Confluence page

5. Verify update

**Output:**
```markdown
## Epic Updated: [Title] (BEP-XXX)

### Changes Applied
- [List of changes]

### Follow-up Actions
- [ ] Update Epic Doc in Confluence
- [ ] Review affected stories: BEP-YYY, BEP-ZZZ
- [ ] Update sprint planning if needed
```

---

## Quality Checklist

Before updating:
- [ ] Original business objective preserved (unless explicitly changed)
- [ ] Impact on child stories analyzed
- [ ] No silent scope changes
- [ ] RICE scores justified
- [ ] ADF format via acli
- [ ] User approved all changes

---

## Error Recovery

| Error | Solution |
|-------|----------|
| Lost original content | Re-fetch epic before retry |
| Scope changed silently | Roll back, re-analyze impact |
| acli update fails | Check JSON structure, verify issue key format |
| Stories orphaned | Link stories back to epic |

---

## Common Update Scenarios

### 1. Adjust Scope
```
/update-epic BEP-XXX "ลด scope: ยังไม่ทำ feature X ใน phase นี้"
```
- ⚠️ High impact
- ต้อง review child stories
- Update timeline

### 2. Update RICE Score
```
/update-epic BEP-XXX "update RICE: Reach เพิ่มเป็น 8 เพราะมี data ใหม่"
```
- Low impact
- เป็น re-prioritization

### 3. Add Success Metrics
```
/update-epic BEP-XXX "เพิ่ม success metric: conversion rate +5%"
```
- Low impact
- เพิ่ม measurable outcome

### 4. Format Migration
```
/update-epic BEP-XXX "migrate to ADF format"
```
- No content change
- ปรับ format + panels

### 5. Clarify Objectives
```
/update-epic BEP-XXX "objective ไม่ชัด ช่วยเขียนใหม่"
```
- Rewrite ให้ชัดเจนขึ้น
- รักษา meaning เดิม

---

## Cascading Updates

เมื่อ epic เปลี่ยน อาจต้อง update:

| Item | When to Update |
|------|----------------|
| Epic Doc | Scope/objectives เปลี่ยน |
| Child Stories | Scope เปลี่ยน, requirements เปลี่ยน |
| Sprint Planning | Timeline/priority เปลี่ยน |
| Roadmap | Major scope changes |

**Suggest follow-up:**
```
Epic updated. Related items that may need updating:
- Confluence: Epic Doc (link)
- Stories: BEP-YYY (scope removed), BEP-ZZZ (new requirement)

Use `/update-story BEP-YYY` to cascade changes
```

---

## RICE Score Guide

| Factor | Scale | Description |
|--------|-------|-------------|
| **Reach** | 1-10 | จำนวน users ที่ได้ประโยชน์ |
| **Impact** | 0.25-3 | ระดับ impact ต่อ user (0.25=minimal, 3=massive) |
| **Confidence** | 0-100% | ความมั่นใจใน estimates |
| **Effort** | 1-10 | Person-weeks needed |

**Formula:** `(Reach × Impact × Confidence) / Effort`

---

## References

- [ADF Templates](../shared-references/templates.md)
- [Writing Style](../shared-references/writing-style.md)
- [Tool Selection](../shared-references/tools.md)
