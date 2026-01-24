---
name: update-epic
description: |
  แก้ไข Epic ที่มีอยู่ ด้วย 5-phase update workflow

  Phases: Fetch Current → Impact Analysis → Preserve Intent → Generate Update → Apply Update

  รองรับ: ปรับ scope, update RICE, เพิ่ม success metrics, format migration

  Triggers: "update epic", "แก้ไข epic", "ปรับ epic"
argument-hint: "[issue-key] [changes]"
---

# /update-epic

**Role:** Senior Product Manager
**Output:** Updated Epic

## Phases

### 1. Fetch Current State
- `MCP: jira_get_issue(issue_key: "BEP-XXX")`
- `MCP: jira_search(jql: "parent = BEP-XXX OR 'Epic Link' = BEP-XXX")`
- `MCP: confluence_search(query: "Epic: [title]")`
- อ่าน: RICE, objectives, success metrics, child stories
- **Gate:** User confirms what to update

### 2. Impact Analysis

| Change Type | Impact on Stories | Impact on Planning |
|-------------|-------------------|-------------------|
| Add scope | ต้องสร้าง story ใหม่ | Re-estimate |
| Remove scope | ต้อง close stories | Timeline shorter |
| RICE update | ❌ No impact | May reprioritize |
| Format only | ❌ No impact | ❌ No impact |

**Gate:** User acknowledges impact

### 3. Preserve Intent
- ✅ ปรับ wording/clarify ได้
- ✅ Update RICE ได้
- ✅ เพิ่ม success metrics ได้
- ⚠️ ระวังเปลี่ยน scope (กระทบ stories)
- ❌ ห้ามเปลี่ยน core business value โดยไม่บอก

### 4. Generate Update
- Generate ADF JSON → `tasks/bep-xxx-epic-update.json`
- Show comparison: Before/After for RICE, objectives, scope
- **Gate:** User approves changes

### 5. Apply Update
```bash
acli jira workitem edit --from-json tasks/bep-xxx-epic-update.json --yes
```

**Output:**
```
## Epic Updated: [Title] (BEP-XXX)
Changes: [list]
→ Update Epic Doc if needed
→ Review stories: BEP-YYY, BEP-ZZZ
```

---

## Common Scenarios

| Scenario | Command | Impact |
|----------|---------|--------|
| Adjust scope | `/update-epic BEP-XXX "ลด scope"` | ⚠️ High |
| Update RICE | `/update-epic BEP-XXX "RICE update"` | 🟢 Low |
| Add metrics | `/update-epic BEP-XXX "เพิ่ม metric"` | 🟢 Low |
| Format migrate | `/update-epic BEP-XXX "migrate ADF"` | 🟢 Low |

---

## Epic Structure (ADF)

| Section | Panel Type | Content |
|---------|------------|---------|
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

- [ADF Templates](../shared-references/templates.md) - Epic ADF structure
- [Workflows](../shared-references/workflows.md) - Update phase pattern
