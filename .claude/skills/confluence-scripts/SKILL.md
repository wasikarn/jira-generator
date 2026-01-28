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
**Version:** 2.0.0 (Refactored with SRP/OCP)

## Architecture

```text
confluence-scripts/
├── __init__.py              # Package marker
├── lib/                     # Shared library modules
│   ├── __init__.py          # Public exports
│   ├── exceptions.py        # Custom exceptions
│   ├── auth.py              # SSL, credentials, auth
│   ├── api.py               # ConfluenceAPI class
│   └── converters.py        # Content converters
└── scripts/                 # CLI scripts
    ├── create_confluence_page.py
    ├── update_confluence_page.py
    ├── move_confluence_page.py
    ├── update_page_storage.py
    └── fix_confluence_code_blocks.py
```

### Module Responsibilities (SRP)

| Module | Responsibility |
| --- | --- |
| `exceptions.py` | Domain-specific exceptions |
| `auth.py` | Authentication (SSL, credentials, auth header) |
| `api.py` | HTTP/API operations via ConfluenceAPI class |
| `converters.py` | Content transformation (markdown, code blocks) |

---

## Available Scripts

| Script | Description | Use Case |
| --- | --- | --- |
| `create_confluence_page.py` | Create/Update page พร้อม proper code blocks | สร้างหรือ update page ที่มี code |
| `update_confluence_page.py` | Find/Replace text ใน page | Batch text replacement |
| `move_confluence_page.py` | Move page(s) to new parent | Reorganize page hierarchy |
| `update_page_storage.py` | Update page ด้วย raw storage format | Pages ที่ต้องการ macros (ToC, Children) |
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
| `--verbose` | Both | ❌ | Enable debug logging |

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
| `--verbose` | ❌ | Enable debug logging |

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
| `--verbose` | ❌ | Enable debug logging |

*ต้องระบุ `--page-id` หรือ `--page-ids` อย่างใดอย่างหนึ่ง

### Why Use This Script

MCP `confluence_update_page` ไม่สามารถย้าย page ได้โดยไม่ overwrite content
Script นี้ใช้ Confluence REST API โดยตรง:

```text
PUT /rest/api/content/{pageId}/move/append/{parentId}
```

---

## Script 4: Update with Storage Format

Update page ด้วย raw storage format สำหรับ macros (ToC, Children, Status)

**Location:** `.claude/skills/confluence-scripts/scripts/update_page_storage.py`

### Usage

```bash
# Update from HTML file with macros
python3 .claude/skills/confluence-scripts/scripts/update_page_storage.py \
  --page-id 156598299 \
  --content-file content.html

# Update with inline storage content
python3 .claude/skills/confluence-scripts/scripts/update_page_storage.py \
  --page-id 156598299 \
  --content "<h1>Title</h1><ac:structured-macro ac:name=\"toc\"/>"

# Dry run (preview only)
python3 .claude/skills/confluence-scripts/scripts/update_page_storage.py \
  --page-id 156598299 \
  --content-file content.html \
  --dry-run
```

### Arguments

| Argument | Required | Description |
| --- | --- | --- |
| `--page-id` | ✅ | Confluence page ID |
| `--content` | ✅* | Raw storage format content (inline) |
| `--content-file` | ✅* | Path to file with storage content |
| `--title` | ❌ | New title (optional) |
| `--dry-run` | ❌ | Preview changes without applying |
| `--verbose` | ❌ | Enable debug logging |

*ต้องระบุ `--content` หรือ `--content-file` อย่างใดอย่างหนึ่ง

### Common Macros

| Macro | Storage Format |
| --- | --- |
| Table of Contents | `<ac:structured-macro ac:name="toc"><ac:parameter ac:name="maxLevel">2</ac:parameter></ac:structured-macro>` |
| Children Display | `<ac:structured-macro ac:name="children"><ac:parameter ac:name="all">true</ac:parameter><ac:parameter ac:name="sort">title</ac:parameter></ac:structured-macro>` |
| Status | `<ac:structured-macro ac:name="status"><ac:parameter ac:name="colour">Green</ac:parameter><ac:parameter ac:name="title">Complete</ac:parameter></ac:structured-macro>` |
| Info Panel | `<ac:structured-macro ac:name="info"><ac:rich-text-body><p>Info text</p></ac:rich-text-body></ac:structured-macro>` |
| Warning Panel | `<ac:structured-macro ac:name="warning"><ac:rich-text-body><p>Warning text</p></ac:rich-text-body></ac:structured-macro>` |

### Why Use This Script

MCP tools แปลง storage format ไม่ถูกต้อง - macros จะ render เป็น text แทน
Script นี้ส่ง raw storage format ไปที่ API โดยตรง

---

## Script 5: Fix Code Blocks

แก้ไข code blocks จาก `<pre class="highlight"><code>` เป็น `<ac:structured-macro ac:name="code">`

**Location:** `.claude/skills/confluence-scripts/scripts/fix_confluence_code_blocks.py`

### Usage

```bash
# Fix single page
python3 .claude/skills/confluence-scripts/scripts/fix_confluence_code_blocks.py \
  --page-id 144244902

# Fix multiple pages
python3 .claude/skills/confluence-scripts/scripts/fix_confluence_code_blocks.py \
  --page-ids 144244902,144015541,144015575,143720672

# Dry run (preview only)
python3 .claude/skills/confluence-scripts/scripts/fix_confluence_code_blocks.py \
  --page-ids 144244902,144015541 \
  --dry-run
```

### Arguments

| Argument | Required | Description |
| --- | --- | --- |
| `--page-id` | ✅* | Single page ID to fix |
| `--page-ids` | ✅* | Comma-separated list of page IDs to fix |
| `--dry-run` | ❌ | Preview changes without applying |
| `--verbose` | ❌ | Enable debug logging |

*ต้องระบุ `--page-id` หรือ `--page-ids` อย่างใดอย่างหนึ่ง

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
    ├─ Add macros (ToC, Children, Status)
    │     └─ update_page_storage.py --page-id --content-file
    │
    └─ Fix broken code blocks
          └─ fix_confluence_code_blocks.py --page-id(s)
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

## Library API (for developers)

### Using ConfluenceAPI

```python
from lib import (
    ConfluenceAPI,
    create_ssl_context,
    load_credentials,
    get_auth_header,
)

creds = load_credentials()
api = ConfluenceAPI(
    base_url=creds["CONFLUENCE_URL"],
    auth_header=get_auth_header(creds["CONFLUENCE_USERNAME"], creds["CONFLUENCE_API_TOKEN"]),
    ssl_context=create_ssl_context(),
)

# Get page
page = api.get_page("123456")
print(page["title"])

# Create page
result = api.create_page("BEP", "My Page", "<p>Content</p>", parent_id="123")

# Update page
result = api.update_page("123456", "Title", "<p>New content</p>", version=2)

# Move page
result = api.move_page("123456", "789012")
```

### Using Converters

```python
from lib import markdown_to_storage, create_code_macro, fix_code_blocks

# Convert markdown to storage format
storage_html = markdown_to_storage("# Hello\\n**Bold** text")

# Create code macro
macro = create_code_macro("python", "print('hello')")

# Fix broken code blocks in HTML
fixed_html = fix_code_blocks(broken_html)
```

### Custom Exceptions

```python
from lib import ConfluenceError, CredentialsError, PageNotFoundError, APIError

try:
    page = api.get_page("invalid")
except PageNotFoundError as e:
    print(f"Page not found: {e.page_id}")
except APIError as e:
    print(f"API error {e.status_code}: {e.reason}")
except CredentialsError as e:
    print(f"Credentials error: {e}")
```

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

| Date | Version | Changes |
| --- | --- | --- |
| 2026-01-27 | 1.0.0 | Initial scripts: update_confluence_page.py |
| 2026-01-29 | 1.1.0 | Added create, move, fix scripts |
| 2026-01-29 | 2.0.0 | Refactored with SRP/OCP: lib/ modules, type hints, logging, custom exceptions |

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
