# Script Reference

> Details for all scripts in `atlassian-scripts/scripts/`
>
> For overview and script selection guide, see [SKILL.md](SKILL.md)

---

## Script 1: Create/Update Page

Create or update a Confluence page with proper code block formatting.

**Location:** `.claude/skills/atlassian-scripts/scripts/create_confluence_page.py`

### Usage

```bash
# Create new page
python3 .claude/skills/atlassian-scripts/scripts/create_confluence_page.py \
  --space BEP --title "Technical Spec: Feature X" --content-file content.md

# Create as child page
# Add: --parent-id 123456789

# Update existing page
python3 .claude/skills/atlassian-scripts/scripts/create_confluence_page.py \
  --page-id 144244902 --content-file updated-content.md

# Options: --content "inline" | --dry-run | --verbose
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
python3 .claude/skills/atlassian-scripts/scripts/update_confluence_page.py \
  --page-id 154730498 --find "old" --replace "new"

# Multiple: repeat --find/--replace pairs | --regex | --dry-run | --verbose
```

### Arguments

| Argument | Required | Description |
| --- | --- | --- |
| `--page-id` | ✅ | Confluence page ID |
| `--find` | ✅ | Text to find (repeatable) |
| `--replace` | ✅ | Replacement (must match --find count) |
| `--regex` | ❌ | Regex mode |
| `--dry-run` | ❌ | Preview only |

---

## Script 3: Move Page

Move page(s) under a different parent page without modifying content.

**Location:** `.claude/skills/atlassian-scripts/scripts/move_confluence_page.py`

### Usage

```bash
python3 .claude/skills/atlassian-scripts/scripts/move_confluence_page.py \
  --page-id 144244902 --parent-id 153518083

# Batch: --page-ids 123,456,789 | --dry-run | --verbose
```

| Argument | Required | Description |
| --- | --- | --- |
| `--page-id` / `--page-ids` | ✅ | Single or comma-separated page IDs |
| `--parent-id` | ✅ | Target parent page ID |

> **Why:** MCP can't move pages without overwriting content. Uses `PUT /rest/api/content/{pageId}/move/append/{parentId}`

---

## Script 4: Update with Storage Format

Update a page with raw storage format for macros (ToC, Children, Status).

**Location:** `.claude/skills/atlassian-scripts/scripts/update_page_storage.py`

### Usage

```bash
python3 .claude/skills/atlassian-scripts/scripts/update_page_storage.py \
  --page-id 156598299 --content-file content.html

# Options: --content "inline" | --title "New Title" | --dry-run | --verbose
```

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
python3 .claude/skills/atlassian-scripts/scripts/fix_confluence_code_blocks.py \
  --page-id 144244902
# Batch: --page-ids 123,456,789 | --dry-run | --verbose
```

Converts `<pre class="highlight"><code>` → `<ac:structured-macro ac:name="code">` via REST API.

---

## Script 6: Audit Pages

Verify content across multiple Confluence pages for presence/absence of specified strings.

**Location:** `.claude/skills/atlassian-scripts/scripts/audit_confluence_pages.py`

### Usage

```bash
# Single page
python3 .claude/skills/atlassian-scripts/scripts/audit_confluence_pages.py \
  --page-id 153518083 --should-have "BEP-2883" --should-not-have "2025-01-21"

# Batch from JSON config
python3 .claude/skills/atlassian-scripts/scripts/audit_confluence_pages.py --config audit.json
```

Config: `[{"page_id":"123","label":"Name","should_have":["X"],"should_not_have":["Y"]}]`

| Argument | Description |
| --- | --- |
| `--config` / `--page-id` | JSON config or single page (one required) |
| `--should-have` / `--should-not-have` | Presence/absence checks (with --page-id) |
| `--label`, `--verbose` | Display label, debug logging |

---

## Script 7: Update Jira Description

Fix Jira issue descriptions via REST API v3 (ADF format) directly.
Preserves all formatting (panels, tables, marks, code blocks).

**Location:** `.claude/skills/atlassian-scripts/scripts/update_jira_description.py`

### Usage

```bash
# Single issue
python3 .claude/skills/atlassian-scripts/scripts/update_jira_description.py \
  --issue BEP-2819 --find "old" --replace "new"

# Batch: --config fixes.json | --dry-run | --verbose
```

Config: `{"BEP-2819": [["old","new"]], "BEP-2755": [["old1","new1"],["old2","new2"]]}`

| Argument | Description |
| --- | --- |
| `--config` / `--issue` | JSON config or single issue key (one required) |
| `--find`, `--replace` | Text pairs (repeatable, with --issue) |

**How:** GET ADF via REST v3 → walk tree → replace text nodes → PUT back. Preserves all formatting (panels, tables, marks).

**vs MCP:** MCP converts to wiki markup (loses formatting). `acli` replaces entire description. This script does **surgical text-only edits**.

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
