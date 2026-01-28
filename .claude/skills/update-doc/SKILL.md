---
name: update-doc
description: |
  Update existing Confluence page ด้วย 5-phase workflow
  รองรับ: content update, section update, status change, move

  Triggers: "update doc", "แก้ไข doc", "update confluence", "move page"
argument-hint: "[page-id or title] [--move parent-id]"
---

# /update-doc

**Role:** Developer / Tech Lead
**Output:** Updated Confluence Page

## Update Types

| Type | Description | Use Case |
| --- | --- | --- |
| `content` | Update entire content | Major revision |
| `section` | Update specific section | Add/modify section |
| `status` | Change document status | Draft → Published |
| `replace` | Find and replace text | Batch text changes |
| `move` | Move to different parent | Reorganize hierarchy |

---

## Phases

### 1. Discovery

ถาม user เพื่อ identify page:

**ถ้าไม่ระบุ page:**

```text
ต้องการ update page ไหน?
1. ระบุ Page ID (เช่น 144244902)
2. ค้นหาจาก title
```

**ถ้าค้นหาจาก title:**

```python
confluence_search(query="title ~ \"[search term]\"", limit=5)
```

**Gather update details:**

| Update Type | Required Info |
| --- | --- |
| `content` | New content (markdown) |
| `section` | Section name, New content |
| `status` | New status value |
| `replace` | Find text, Replace text |
| `move` | Target parent page ID |

**ถ้าต้องการ move:**

```text
ต้องการย้ายไปอยู่ภายใต้ parent page ไหน?
1. ระบุ Page ID
2. ค้นหาจาก title
```

**Gate:** Page identified + Update type determined

---

### 2. Fetch Current

ดึง content ปัจจุบัน:

```python
confluence_get_page(
  page_id="[page_id]",
  convert_to_markdown=true,
  include_metadata=true
)
```

**Output:**

- Current content (markdown)
- Page title
- Version number
- Last updated

**Gate:** Current content retrieved

---

### 3. Generate Updates

สร้าง updated content ตาม update type:

**Content Update:**

- แทนที่ content ทั้งหมด
- รักษา structure และ formatting

**Section Update:**

- หา section ที่ต้องการแก้ไข
- แทนที่เฉพาะ section นั้น
- รักษา sections อื่น

**Status Update:**

- หา status field
- เปลี่ยนค่า (Draft/In Review/Published)

**Replace:**

- Find all occurrences
- Replace with new text
- Report count

**Move:**

- ไม่แก้ไข content
- เปลี่ยนเฉพาะ parent page
- รักษา page metadata

**Gate:** Updated content generated (or move target identified)

---

### 4. Review

แสดง preview ให้ user ตรวจสอบ:

```text
## Update Preview

**Page:** [Title]
**Page ID:** [page_id]
**Current Version:** [version]
**Update Type:** [type]

### Changes:
[Show diff or summary of changes]

ต้องการดำเนินการหรือไม่?
```

**Gate:** User approves changes

---

### 5. Update

**Option A: Simple update (no code blocks)**

```python
confluence_update_page(
  page_id="[page_id]",
  title="[title]",
  content="[updated markdown]"
)
```

**Option B: With code blocks (use Python script)**

ถ้า content มี code blocks ให้ใช้ Python script:

```bash
python3 .claude/skills/confluence-scripts/scripts/update_confluence_page.py \
  --page-id [page_id] \
  --find "[old text]" \
  --replace "[new text]"
```

หรือสำหรับ full content update:

```bash
python3 .claude/skills/confluence-scripts/scripts/create_confluence_page.py \
  --page-id [page_id] \
  --content-file tasks/temp-content.md
```

**Option C: Move page (use Python script)**

ย้าย page ไปอยู่ภายใต้ parent อื่น:

```bash
python3 .claude/skills/confluence-scripts/scripts/move_confluence_page.py \
  --page-id [page_id] \
  --parent-id [target_parent_id]
```

Batch move หลาย pages:

```bash
python3 .claude/skills/confluence-scripts/scripts/move_confluence_page.py \
  --page-ids [page_id1],[page_id2],[page_id3] \
  --parent-id [target_parent_id]
```

**Output:**

```text
## ✅ Document Updated: [Title]

**Page ID:** [page_id]
**New Version:** [version + 1]
**Update Type:** [type]

🔗 [View in Confluence](URL)
```

---

## Decision Flow

```text
Update type?
    │
    ├─ Move → move_confluence_page.py --page-id --parent-id
    │
    └─ Content/Section/Status/Replace
          │
          └─ มี code blocks?
                │
                ├─ No → ใช้ MCP confluence_update_page
                │
                └─ Yes → ใช้ Python script
                          │
                          ├─ Find/Replace → update_confluence_page.py
                          │
                          └─ Full content → create_confluence_page.py --page-id
```

---

## Common Scenarios

| Scenario | Command | Tool |
| --- | --- | --- |
| Update status | `/update-doc 144244902 --status Published` | MCP |
| Replace text | `/update-doc 144244902 --find "v1" --replace "v2"` | Script |
| Update section | `/update-doc 144244902 --section "API Spec"` | MCP or Script |
| Full rewrite | `/update-doc 144244902` | Script |
| Move page | `/update-doc 144244902 --move 153518083` | Script |
| Batch move | `/update-doc --move 153518083 --pages 144244902,144015541` | Script |

---

## Error Handling

| Error | Cause | Solution |
| --- | --- | --- |
| Page not found | Wrong page ID | ค้นหา page ใหม่ |
| Version conflict | Someone else updated | Fetch latest version แล้ว retry |
| Permission denied | No edit access | ติดต่อ admin |
| Code blocks broken | Used MCP for code | ใช้ Python script แทน |

---

## References

- Space: `BEP`
- MCP Tool: `confluence_update_page`, `confluence_get_page`
- Scripts: `.claude/skills/confluence-scripts/scripts/`
