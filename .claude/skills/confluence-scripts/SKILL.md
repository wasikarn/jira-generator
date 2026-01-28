---
name: confluence-scripts
description: |
  Python scripts สำหรับ update Confluence pages ผ่าน REST API โดยตรง
  ใช้เมื่อ MCP tool มีข้อจำกัด (เช่น code macro formatting)

  Triggers: "fix confluence", "update confluence page", "confluence script"
argument-hint: "[script-name] [args]"
---

# Confluence Scripts

**Role:** Developer / Tech Lead
**Output:** Created/Updated Confluence Pages

## Available Scripts

| Script | Description | Use Case |
| --- | --- | --- |
| `create_confluence_page.py` | Create/Update page พร้อม proper code blocks | สร้างหรือ update page ที่มี code |
| `update_confluence_page.py` | Find/Replace text ใน page | Batch text replacement |
| `move_confluence_page.py` | Move page(s) to new parent | Reorganize page hierarchy |
| `fix_confluence_code_blocks.py` | แก้ไข code blocks ที่ render ผิด | Fix broken code formatting |

---

## Prerequisites

**Credentials:** `~/.config/atlassian/.env`

```env
CONFLUENCE_URL=https://100-stars.atlassian.net/wiki
CONFLUENCE_USERNAME=your-email@example.com
CONFLUENCE_API_TOKEN=your-api-token
```

---

## Script 1: Create/Update Page

สร้างหรือ update Confluence page พร้อม proper code block formatting

**Location:** `.claude/skills/confluence-scripts/scripts/create_confluence_page.py`

### Create New Page

```bash
# Basic create
python3 .claude/skills/confluence-scripts/scripts/create_confluence_page.py \
  --space BEP \
  --title "Technical Spec: Feature X" \
  --content-file content.md

# Create as child of parent page
python3 .claude/skills/confluence-scripts/scripts/create_confluence_page.py \
  --space BEP \
  --title "Sub Page" \
  --parent-id 123456789 \
  --content-file content.md
```

### Update Existing Page

```bash
# Update from file
python3 .claude/skills/confluence-scripts/scripts/create_confluence_page.py \
  --page-id 144244902 \
  --content-file updated-content.md

# Update with inline content
python3 .claude/skills/confluence-scripts/scripts/create_confluence_page.py \
  --page-id 144244902 \
  --content "# Updated Title\n\nNew content here"

# Dry run (preview storage format)
python3 .claude/skills/confluence-scripts/scripts/create_confluence_page.py \
  --space BEP \
  --title "Test" \
  --content "# Hello World" \
  --dry-run
```

### Arguments

| Argument | Mode | Required | Description |
| --- | --- | --- | --- |
| `--space` | Create | ✅ | Space key (e.g., BEP) |
| `--title` | Create | ✅ | Page title |
| `--parent-id` | Create | ❌ | Parent page ID |
| `--page-id` | Update | ✅ | Page ID to update |
| `--content` | Both | ✅* | Inline markdown content |
| `--content-file` | Both | ✅* | Path to markdown file |
| `--dry-run` | Both | ❌ | Preview without saving |

*ต้องระบุ `--content` หรือ `--content-file` อย่างใดอย่างหนึ่ง

### Supported Markdown

| Element | Syntax | Supported |
| --- | --- | --- |
| Headings | `# ## ###` | ✅ |
| Bold | `**text**` | ✅ |
| Italic | `*text*` | ✅ |
| Code blocks | ` ```lang ` | ✅ (as ac:structured-macro) |
| Inline code | `` `code` `` | ✅ |
| Links | `[text](url)` | ✅ |
| Lists | `- item` | ✅ |
| Tables | `| col |` | ✅ |
| Blockquotes | `> quote` | ✅ |
| HR | `---` | ✅ |

---

## Script 2: Find/Replace

Generic script สำหรับ find/replace content ใน Confluence pages

**Location:** `.claude/skills/confluence-scripts/scripts/update_confluence_page.py`

### Usage

```bash
# Simple replacement
python3 .claude/skills/confluence-scripts/scripts/update_confluence_page.py \
  --page-id 154730498 \
  --find "5 นาที" \
  --replace "3 นาที"

# Multiple replacements
python3 .claude/skills/confluence-scripts/scripts/update_confluence_page.py \
  --page-id 154730498 \
  --find "5 minutes" --replace "3 minutes" \
  --find "300" --replace "180"

# Dry run (preview only)
python3 .claude/skills/confluence-scripts/scripts/update_confluence_page.py \
  --page-id 154730498 \
  --find "old text" --replace "new text" \
  --dry-run

# Regex replacement
python3 .claude/skills/confluence-scripts/scripts/update_confluence_page.py \
  --page-id 154730498 \
  --find "v\\d+\\.\\d+" --replace "v2.0" \
  --regex
```

### Arguments

| Argument | Required | Description |
| --- | --- | --- |
| `--page-id` | ✅ | Confluence page ID |
| `--find` | ✅ | Text to find (can repeat) |
| `--replace` | ✅ | Replacement text (must match --find count) |
| `--regex` | ❌ | Treat find as regex pattern |
| `--dry-run` | ❌ | Preview changes without applying |

---

## Script 3: Move Page

ย้าย page(s) ไปอยู่ภายใต้ parent page อื่น โดยไม่แก้ไข content

**Location:** `.claude/skills/confluence-scripts/scripts/move_confluence_page.py`

### Usage

```bash
# Move single page
python3 .claude/skills/confluence-scripts/scripts/move_confluence_page.py \
  --page-id 144244902 \
  --parent-id 153518083

# Batch move multiple pages
python3 .claude/skills/confluence-scripts/scripts/move_confluence_page.py \
  --page-ids 144244902,144015541,144015575 \
  --parent-id 153518083

# Dry run (preview only)
python3 .claude/skills/confluence-scripts/scripts/move_confluence_page.py \
  --page-id 144244902 \
  --parent-id 153518083 \
  --dry-run
```

### Arguments

| Argument | Required | Description |
| --- | --- | --- |
| `--page-id` | ✅* | Single page ID to move |
| `--page-ids` | ✅* | Comma-separated list of page IDs to move |
| `--parent-id` | ✅ | Target parent page ID |
| `--dry-run` | ❌ | Preview changes without applying |

*ต้องระบุ `--page-id` หรือ `--page-ids` อย่างใดอย่างหนึ่ง

### Why Use This Script

MCP `confluence_update_page` ไม่สามารถย้าย page ได้โดยไม่ overwrite content
Script นี้ใช้ Confluence REST API โดยตรง:

```text
PUT /rest/api/content/{pageId}/move/append/{parentId}
```

---

## Script 4: Fix Code Blocks

แก้ไข code blocks จาก `<pre class="highlight"><code>` เป็น `<ac:structured-macro ac:name="code">`

**Location:** `.claude/skills/confluence-scripts/scripts/fix_confluence_code_blocks.py`

### Usage

```bash
python3 .claude/skills/confluence-scripts/scripts/fix_confluence_code_blocks.py
```

### Default Pages (แก้ไขใน script)

```python
pages = [
    ("144244902", "Credit Coupon"),
    ("144015541", "Discount Coupon"),
    ("144015575", "Cashback Coupon"),
    ("143720672", "Coupon Menu"),
]
```

### What it does

1. ดึง page content ปัจจุบัน
2. หา `<pre class="highlight"><code class="language-xxx">` patterns
3. แปลงเป็น `<ac:structured-macro ac:name="code">` format
4. Update page ผ่าน REST API

---

## Decision Flow

```text
ต้องการทำอะไร?
    │
    ├─ สร้าง page ใหม่
    │     └─ create_confluence_page.py --space --title
    │
    ├─ Update content ทั้งหมด
    │     └─ create_confluence_page.py --page-id --content-file
    │
    ├─ Find/Replace text
    │     └─ update_confluence_page.py --find --replace
    │
    ├─ Move page(s) to new parent
    │     └─ move_confluence_page.py --page-id(s) --parent-id
    │
    └─ Fix broken code blocks
          └─ fix_confluence_code_blocks.py
```

---

## When to Use Scripts vs MCP

| Scenario | Tool | Why |
| --- | --- | --- |
| Simple page read | MCP `confluence_get_page` | Fast, no script needed |
| Simple page create (no code) | MCP `confluence_create_page` | Markdown works fine |
| Page with code blocks | **Script** | MCP breaks code formatting |
| Batch text replacement | **Script** | More reliable |
| Fix broken formatting | **Script** | Direct storage format access |

---

## Technical Notes

### SSL Certificate Issue (macOS)

Scripts ใช้ SSL context ที่ไม่ verify certificate:

```python
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
```

### Confluence Storage Format

**Code blocks ต้องใช้ format นี้:**

```xml
<ac:structured-macro ac:name="code" ac:schema-version="1">
  <ac:parameter ac:name="language">json</ac:parameter>
  <ac:plain-text-body><![CDATA[
    {"key": "value"}
  ]]></ac:plain-text-body>
</ac:structured-macro>
```

**ไม่ใช่:**

```html
<pre class="highlight"><code class="language-json">...</code></pre>
```

### Mermaid Diagrams

Scripts สร้าง code blocks สำหรับ mermaid แต่ไม่ render เป็น diagram

ถ้าต้องการให้แสดงเป็น flowchart:

1. ไปที่ Confluence page
2. Edit → พิมพ์ `/mermaid`
3. Paste mermaid code

---

## History

| Date | Script | Purpose |
| --- | --- | --- |
| 2026-01-27 | `update_confluence_page.py` | Update OTP validity 5min → 3min |
| 2026-01-29 | `fix_confluence_code_blocks.py` | Fix code block formatting |
| 2026-01-29 | `create_confluence_page.py` | Create/update with proper code formatting |
| 2026-01-29 | `move_confluence_page.py` | Move pages to reorganize hierarchy |

---

## Related Skills

| Skill | Description |
| --- | --- |
| `/create-doc` | Create new Confluence page (uses MCP) |
| `/update-doc` | Update existing Confluence page (uses scripts when needed) |

---

## References

- Confluence REST API: <https://developer.atlassian.com/cloud/confluence/rest/v1/intro/>
- Credentials: `~/.config/atlassian/.env`
- Storage Format: <https://developer.atlassian.com/cloud/confluence/confluence-storage-format/>
