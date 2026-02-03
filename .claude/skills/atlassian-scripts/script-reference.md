# Script Reference

> Details for all scripts in `atlassian-scripts/scripts/`
>
> For overview and script selection guide, see [SKILL.md](SKILL.md)

---

## Script 1: Create/Update Page

Create or update a Confluence page with proper code block formatting.

**Location:** `.claude/skills/atlassian-scripts/scripts/create_confluence_page.py`

### Create New Page

```bash
# Basic create
python3 .claude/skills/atlassian-scripts/scripts/create_confluence_page.py \
  --space BEP \
  --title "Technical Spec: Feature X" \
  --content-file content.md

# Create as child of parent page
python3 .claude/skills/atlassian-scripts/scripts/create_confluence_page.py \
  --space BEP \
  --title "Sub Page" \
  --parent-id 123456789 \
  --content-file content.md
```

### Update Existing Page

```bash
# Update from file
python3 .claude/skills/atlassian-scripts/scripts/create_confluence_page.py \
  --page-id 144244902 \
  --content-file updated-content.md

# Update with inline content
python3 .claude/skills/atlassian-scripts/scripts/create_confluence_page.py \
  --page-id 144244902 \
  --content "# Updated Title\n\nNew content here"

# Dry run (preview storage format)
python3 .claude/skills/atlassian-scripts/scripts/create_confluence_page.py \
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

*Must specify either `--content` or `--content-file`.

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
| Tables | `\| col \|` | ✅ |
| Blockquotes | `> quote` | ✅ |
| HR | `---` | ✅ |

---

## Script 2: Find/Replace

Generic script for find/replace content in Confluence pages.

**Location:** `.claude/skills/atlassian-scripts/scripts/update_confluence_page.py`

### Usage

```bash
# Simple replacement
python3 .claude/skills/atlassian-scripts/scripts/update_confluence_page.py \
  --page-id 154730498 \
  --find "5 minutes" \
  --replace "3 minutes"

# Multiple replacements
python3 .claude/skills/atlassian-scripts/scripts/update_confluence_page.py \
  --page-id 154730498 \
  --find "5 minutes" --replace "3 minutes" \
  --find "300" --replace "180"

# Dry run (preview only)
python3 .claude/skills/atlassian-scripts/scripts/update_confluence_page.py \
  --page-id 154730498 \
  --find "old text" --replace "new text" \
  --dry-run

# Regex replacement
python3 .claude/skills/atlassian-scripts/scripts/update_confluence_page.py \
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

Move page(s) under a different parent page without modifying content.

**Location:** `.claude/skills/atlassian-scripts/scripts/move_confluence_page.py`

### Usage

```bash
# Move single page
python3 .claude/skills/atlassian-scripts/scripts/move_confluence_page.py \
  --page-id 144244902 \
  --parent-id 153518083

# Batch move multiple pages
python3 .claude/skills/atlassian-scripts/scripts/move_confluence_page.py \
  --page-ids 144244902,144015541,144015575 \
  --parent-id 153518083

# Dry run (preview only)
python3 .claude/skills/atlassian-scripts/scripts/move_confluence_page.py \
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

*Must specify either `--page-id` or `--page-ids`.

### Why Use This Script

MCP `confluence_update_page` cannot move a page without overwriting its content.
This script uses the Confluence REST API directly:

```text
PUT /rest/api/content/{pageId}/move/append/{parentId}
```

---

## Script 4: Update with Storage Format

Update a page with raw storage format for macros (ToC, Children, Status).

**Location:** `.claude/skills/atlassian-scripts/scripts/update_page_storage.py`

### Usage

```bash
# Update from HTML file with macros
python3 .claude/skills/atlassian-scripts/scripts/update_page_storage.py \
  --page-id 156598299 \
  --content-file content.html

# Update with inline storage content
python3 .claude/skills/atlassian-scripts/scripts/update_page_storage.py \
  --page-id 156598299 \
  --content "<h1>Title</h1><ac:structured-macro ac:name=\"toc\"/>"

# Dry run (preview only)
python3 .claude/skills/atlassian-scripts/scripts/update_page_storage.py \
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

*Must specify either `--content` or `--content-file`.

### Common Macros

| Macro | Storage Format |
| --- | --- |
| Table of Contents | `<ac:structured-macro ac:name="toc"><ac:parameter ac:name="maxLevel">2</ac:parameter></ac:structured-macro>` |
| Children Display | `<ac:structured-macro ac:name="children"><ac:parameter ac:name="all">true</ac:parameter><ac:parameter ac:name="sort">title</ac:parameter></ac:structured-macro>` |
| Status | `<ac:structured-macro ac:name="status"><ac:parameter ac:name="colour">Green</ac:parameter><ac:parameter ac:name="title">Complete</ac:parameter></ac:structured-macro>` |
| Info Panel | `<ac:structured-macro ac:name="info"><ac:rich-text-body><p>Info text</p></ac:rich-text-body></ac:structured-macro>` |
| Warning Panel | `<ac:structured-macro ac:name="warning"><ac:rich-text-body><p>Warning text</p></ac:rich-text-body></ac:structured-macro>` |

### Why Use This Script

MCP tools do not convert storage format correctly -- macros will render as plain text instead.
This script sends raw storage format directly to the API.

---

## Script 5: Fix Code Blocks

Fix code blocks from `<pre class="highlight"><code>` to `<ac:structured-macro ac:name="code">`.

**Location:** `.claude/skills/atlassian-scripts/scripts/fix_confluence_code_blocks.py`

### Usage

```bash
# Fix single page
python3 .claude/skills/atlassian-scripts/scripts/fix_confluence_code_blocks.py \
  --page-id 144244902

# Fix multiple pages
python3 .claude/skills/atlassian-scripts/scripts/fix_confluence_code_blocks.py \
  --page-ids 144244902,144015541,144015575,143720672

# Dry run (preview only)
python3 .claude/skills/atlassian-scripts/scripts/fix_confluence_code_blocks.py \
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

*Must specify either `--page-id` or `--page-ids`.

### What it does

1. Fetch the current page content
2. Find `<pre class="highlight"><code class="language-xxx">` patterns
3. Convert to `<ac:structured-macro ac:name="code">` format
4. Update the page via REST API

---

## Script 6: Audit Pages

Verify content across multiple Confluence pages for presence/absence of specified strings.

**Location:** `.claude/skills/atlassian-scripts/scripts/audit_confluence_pages.py`

### Usage

```bash
# Audit single page
python3 .claude/skills/atlassian-scripts/scripts/audit_confluence_pages.py \
  --page-id 153518083 \
  --label "Epic Parent" \
  --should-have "BEP-2883" "2026" \
  --should-not-have "2025-01-21"

# Audit multiple pages from JSON config
python3 .claude/skills/atlassian-scripts/scripts/audit_confluence_pages.py \
  --config audit.json
```

### Config JSON Format

```json
[
  {
    "page_id": "153518083",
    "label": "Epic Parent Page",
    "should_have": ["BEP-2883", "2026-01-21", "15 stories"],
    "should_not_have": ["2025-01-21"]
  },
  {
    "page_id": "144244902",
    "label": "BEP-2755 Credit",
    "should_have": ["billboard_codes", "IN STAGING"],
    "should_not_have": ["billboard_ids"]
  }
]
```

### Arguments

| Argument | Required | Description |
| --- | --- | --- |
| `--config` | ✅* | Path to JSON config file |
| `--page-id` | ✅* | Single page ID to audit |
| `--label` | ❌ | Label for the page (with --page-id) |
| `--should-have` | ❌ | Strings that MUST be present |
| `--should-not-have` | ❌ | Strings that MUST NOT be present |
| `--verbose` | ❌ | Enable debug logging |

*Must specify either `--config` or `--page-id`.

---

## Script 7: Update Jira Description

Fix Jira issue descriptions via REST API v3 (ADF format) directly.
Preserves all formatting (panels, tables, marks, code blocks).

**Location:** `.claude/skills/atlassian-scripts/scripts/update_jira_description.py`

### Usage

```bash
# Single issue with inline replacements
python3 .claude/skills/atlassian-scripts/scripts/update_jira_description.py \
  --issue BEP-2819 \
  --find "billboard_ids" --replace "billboard_codes"

# Multiple replacements for single issue
python3 .claude/skills/atlassian-scripts/scripts/update_jira_description.py \
  --issue BEP-2819 \
  --find "old1" --replace "new1" \
  --find "old2" --replace "new2"

# Batch from JSON config
python3 .claude/skills/atlassian-scripts/scripts/update_jira_description.py \
  --config fixes.json

# Dry run (preview only)
python3 .claude/skills/atlassian-scripts/scripts/update_jira_description.py \
  --config fixes.json --dry-run
```

### Config JSON Format (Jira)

```json
{
  "BEP-2819": [
    ["billboard_ids", "billboard_codes"]
  ],
  "BEP-2755": [
    ["old text 1", "new text 1"],
    ["old text 2", "new text 2"]
  ]
}
```

### Arguments

| Argument | Required | Description |
| --- | --- | --- |
| `--config` | ✅* | Path to JSON config file |
| `--issue` | ✅* | Single issue key (e.g., BEP-2819) |
| `--find` | ❌ | Text to find (repeatable, with --issue) |
| `--replace` | ❌ | Replacement text (repeatable, with --issue) |
| `--dry-run` | ❌ | Preview changes only |
| `--verbose` | ❌ | Enable debug logging |

*Must specify either `--config` or `--issue`.

### How It Works

1. GET issue via Jira REST API v3 (returns ADF format)
2. Deep copy ADF description
3. Walk ADF tree recursively, replace text in text nodes
4. PUT modified ADF back via REST API v3
5. All formatting (panels, tables, marks) preserved

### Key Difference from MCP

| Approach | Format | Preserves Formatting |
| --- | --- | --- |
| MCP `jira_update_issue` | Wiki markup | ❌ Converts to wiki |
| `acli --from-json` | ADF (must build from scratch) | ⚠️ Replaces entire description |
| **This script** | ADF (surgical edit) | ✅ Modifies only text nodes |

---

## Script Selection Guide

```text
What do you need to do?
    │
    ├─ Create a new page
    │     └─ create_confluence_page.py --space --title
    │
    ├─ Update entire content
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
    ├─ Fix broken code blocks
    │     └─ fix_confluence_code_blocks.py --page-id(s)
    │
    ├─ Verify content alignment
    │     └─ audit_confluence_pages.py --config audit.json
    │
    └─ Fix Jira issue descriptions (ADF)
          └─ update_jira_description.py --config fixes.json
```
