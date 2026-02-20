# Troubleshooting Guide

> Universal error recovery for jira-workflow commands

---

## acli Errors

### JSON Format Errors

| Error | Cause | Solution |
| --- | --- | --- |
| `unknown field "project"` | Wrong field name | Use `projectKey` not `project` |
| `unknown field "parent"` | acli does not support the parent field | Use Two-Step Workflow: MCP create + acli edit |
| `missing required field` | Incomplete JSON | Check all required fields present |
| `invalid JSON syntax` | Malformed JSON | Validate JSON structure |
| `issues field required` | Edit without issue key | Add `"issues": ["{{PROJECT_KEY}}-XXX"]` for edits |

**Create vs Edit JSON:**

```json
{
  "projectKey": "{{PROJECT_KEY}}",
  "type": "Story",
  "summary": "..."
}
```

Note: CREATE has no "issues" field, EDIT requires `"issues": ["{{PROJECT_KEY}}-XXX"]`.

### Subtask Creation (Two-Step Workflow)

> ⚠️ **Getting `unknown field "parent"`?** Use this workflow

**Step 1: Create shell with MCP**

```typescript
// Subtask — parent is an object
jira_create_issue({
  project_key: "{{PROJECT_KEY}}",
  summary: "[TAG] - Description",
  issue_type: "Subtask",
  additional_fields: { parent: { key: "{{PROJECT_KEY}}-XXX" } }
})

// Epic child (Story/Task) — parent is a string
jira_create_issue({
  project_key: "{{PROJECT_KEY}}",
  summary: "Story title",
  issue_type: "Story",
  additional_fields: { parent: "BEP-2883" }
})
```

> ⚠️ **Parent format:** Subtask = `{parent: {key: "{{PROJECT_KEY}}-XXX"}}` (object) / Epic child = `{parent: "BEP-2883"}` (string)

**Step 2: Update description with acli**

```json
{
  "issues": ["BEP-YYY"],
  "description": { "type": "doc", "version": 1, "content": [...] }
}
```

```bash
acli jira workitem edit --from-json tasks/subtask.json --yes
```

### Authentication Errors

| Error | Cause | Solution |
| --- | --- | --- |
| `401 Unauthorized` | Invalid token | Re-authenticate: `acli auth login` |
| `403 Forbidden` | No permission | Check project permissions |
| `Token expired` | Session timeout | Re-run `acli auth login` |

### ADF Validation Errors

| Error | Cause | Solution |
| --- | --- | --- |
| `Invalid document structure` | Malformed ADF | Check `type: "doc"` at root |
| `Unknown node type` | Typo in type name | Verify: heading, paragraph, bulletList, etc. |
| `Invalid attrs` | Wrong attributes | Check panel: `panelType`, heading: `level` |
| `Nested table error` | Tables in tables | ❌ Tables cannot contain tables - use bullets |
| `INVALID_INPUT` (InvalidPayloadException) | Nested bulletList | listItem > bulletList is not allowed - flatten or use comma-separated text |

**ADF Structure Must Have:**

```json
{
  "description": {
    "type": "doc",
    "version": 1,
    "content": []
  }
}
```

---

## MCP Tool Errors

### Search Errors

| Error | Cause | Solution |
| --- | --- | --- |
| `JQL syntax error` | Invalid query | Check JQL operators and field names |
| `Expecting ')' but got 'ORDER'` | ORDER BY with parent query | Use `"Parent Link" = {{PROJECT_KEY}}-XXX ORDER BY...` instead of `parent = {{PROJECT_KEY}}-XXX ORDER BY...` |
| `Field not found` | Wrong field name | Use `issuetype` not `type` for search |
| `No issues found` | Empty result | Broaden search criteria |

### Issue Errors

| Error | Cause | Solution |
| --- | --- | --- |
| `Issue not found` | Wrong key | Verify format: `{{PROJECT_KEY}}-XXX` |
| `Cannot read property` | Issue deleted | Issue may have been removed |
| `Rate limited` | Too many requests | Wait and retry |
| `exceeds maximum allowed tokens` | Issue has too much data | Use `fields` parameter to limit fetched fields |
| `jira_update_issue` parent → silent fail | MCP doesn't set parent on Bug/Story | Use REST API v3: `api._request('PUT', '/rest/api/3/issue/KEY', {'fields': {'parent': {'key': 'EPIC-KEY'}}})` |
| `jira_create_issue` parent → silent fail | MCP may silently ignore parent | Verify after create, use REST API if needed |
| `jira_update_issue(fields=...)` → unexpected kwarg | Wrong parameter name | Use `additional_fields` not `fields` for custom fields |

### MCP Parameter Errors

| Error | Cause | Solution |
| --- | --- | --- |
| `jira_get_agile_boards(project_key_or_id=...)` → unexpected kwarg | Wrong parameter name | Use `project_key` not `project_key_or_id` |
| `jira_get_sprint_issues` limit > 50 → validation error | Limit exceeds max | Max `limit=50` — use pagination with `start_at` for more |

### Assignment Errors

| Error | Cause | Solution |
| --- | --- | --- |
| `jira_update_issue` assignee → silent fail | MCP doesn't set assignee | Use `acli jira workitem assign -k "KEY" -a "email" -y` |
| `acli workitem assign -a ""` → failed to resolve | Empty string not valid | Use `--remove-assignee` flag: `acli jira workitem assign -k "KEY" --remove-assignee -y` |
| `acli jira issue update --assignee` → unknown flag | Wrong command | Use `acli jira workitem assign` not `acli jira issue update` |

### Subtask Errors

| Error | Cause | Solution |
| --- | --- | --- |
| `expected 'key' to be string` / `parent not specified` | Parent format wrong | Use `additional_fields={"parent": {"key": "{{PROJECT_KEY}}-XXX"}}` — object, not string |
| Subtask + sprint field → `cannot be associated to a sprint` | Subtasks inherit sprint from parent | Remove sprint field from subtask — inherits automatically |

### Agile API Errors

| Error | Cause | Solution |
| --- | --- | --- |
| MCP `sprint: null` doesn't work | MCP can't remove sprint | Use Agile REST API: `POST /rest/agile/1.0/backlog/issue` + numeric IDs |
| Agile API issue key → 204 but no move | Issue key not accepted | Must use numeric ID from `issue["id"]` |
| Sprint field `{"id": N}` → error | Wrong format for sprint field | `{{SPRINT_FIELD}}` accepts plain number: `{"{{SPRINT_FIELD}}": 123}` |

### Issue Link Errors

| Error | Cause | Solution |
| --- | --- | --- |
| Issue link "Relates to" → error | Wrong link type name | Correct name is `"Relates"` / valid: `Blocks`, `Duplicate`, `Cloners` |

### JQL Errors

| Error | Cause | Solution |
| --- | --- | --- |
| `Expecting ')' but got 'ORDER'` | ORDER BY with `parent =` query | Use `parent = {{PROJECT_KEY}}-XXX` without ORDER BY, or `"Parent Link" = {{PROJECT_KEY}}-XXX ORDER BY...` |
| `key in (...) ORDER BY` → parse error | ORDER BY not allowed with key in | Remove `ORDER BY` when using `key in (...)` syntax |

> 🚨 **NEVER add ORDER BY to `parent =` or `key in (...)` queries — they always cause parse errors**

### Parallel MCP Call Errors

| Error | Cause | Solution |
| --- | --- | --- |
| `Sibling tool call errored` | One parallel MCP call failed → all others cancelled | Fix the failing call first; consider making dependent calls sequential instead of parallel |

> **Tip:** When making multiple `jira_search` / `jira_get_issue` calls in parallel, if one has bad JQL syntax, ALL sibling calls get cancelled. Validate JQL syntax before parallel execution.

### Large Output Error

When encountering this error:

```text
Error: result (73,235 characters) exceeds maximum allowed tokens.
Output has been saved to /path/to/tool-results/...
```

**Solution:** Use the `fields` parameter to limit fetched data:

```python
# ❌ Bad - fetches all fields, causing excessive data
jira_get_issue(issue_key="{{PROJECT_KEY}}-XXX")

# ✅ Good - specify only the fields you need
jira_get_issue(
    issue_key="{{PROJECT_KEY}}-XXX",
    fields="summary,status,description,issuetype,parent",
    comment_limit=5
)
```

**Recommended fields for common operations:**

| Use Case | Fields |
| --- | --- |
| Quick status check | `summary,status,assignee` |
| Read description | `summary,status,description` |
| Check parent/links | `summary,status,issuetype,parent` |
| Full analysis | `summary,status,description,issuetype,parent,labels` |

---

## Common Workflow Errors

### Phase 1: Discovery

| Issue | Solution |
| --- | --- |
| Can't find parent Epic | Search: `project = BEP AND type = Epic` |
| Story not found | Verify issue key, check permissions |

### Phase 2: Design

| Issue | Solution |
| --- | --- |
| Generic file paths | **MUST explore codebase first** - use Task(Explore) |
| Wrong service tag | Check tags: `[BE]`, `[FE-Admin]`, `[FE-Web]` |

### Phase 3: Create

| Issue | Solution |
| --- | --- |
| acli create fails | Check JSON format, validate ADF structure |
| Missing parent link | Add `parent` field for sub-tasks |
| Wrong issue type | Use: `Story`, `Sub-task`, `Epic` (exact case) |

### Phase 4: Update

| Issue | Solution |
| --- | --- |
| Edit overwrites content | Always fetch current first, then merge |
| Lost original intent | Compare before/after, preserve core meaning |

---

## Recovery Procedures

### If Create Fails

1. Check error message
2. Validate JSON structure
3. Verify ADF format
4. Retry with fixed JSON
5. If still fails, try simpler description

### If Update Fails

1. Re-fetch current issue state
2. Compare with your changes
3. Check for concurrent edits
4. Retry update

### If Workflow Interrupted

1. Note which phase completed
2. Check if issue was created (search Jira)
3. Resume from last completed phase
4. If duplicate created, delete and restart

---

## Validation Commands

```bash
# Validate JSON syntax
cat tasks/issue.json | jq .

# Test acli connection
acli jira issue get BEP-1
```

For MCP: Use `jira_get_issue(issue_key: "BEP-1")`

---

## Confluence Scripts Errors

### Python Script Errors

| Error | Cause | Solution |
| --- | --- | --- |
| `SSL: CERTIFICATE_VERIFY_FAILED` | macOS SSL cert issue | Scripts already have SSL bypass built in - if still encountering, check Python version |
| `401 Unauthorized` | Invalid credentials | Check `~/.config/atlassian/.env` |
| `404 Not Found` | Wrong page ID | Verify page ID from URL |
| `ModuleNotFoundError` | Missing module | Scripts use stdlib only (no pip install needed) |

### MCP Confluence Limitations

| Issue | Cause | Solution |
| --- | --- | --- |
| Code blocks not syntax highlighted | MCP renders as `<pre class="highlight">` | Run `fix_confluence_code_blocks.py --page-id` after MCP create/update |
| Macros displayed as text | MCP doesn't understand storage format | Use `update_page_storage.py` |
| Cannot move page | MCP has no move API | Use `move_confluence_page.py` |
| Mermaid diagram not rendering | Code block alone won't render | Need BOTH: code block (`language=mermaid`) + Forge `ac:adf-extension` macro — see below |
| Page font-size 16px instead of 13px | Forge macros force standard renderer | Pages with Forge extensions (Mermaid, etc.) render at 16px (`is-full-width`/`is-full-page`). Simple pages render at 13px (`is-max`). Cannot override via API — content complexity determines renderer mode |
| `content-appearance-published` doesn't change font | Property controls width only | `"full-width"` = wider content area. Font-size is separate: determined by Confluence's internal renderer selection based on page content |

### Page Appearance Properties

**`content-appearance-published`** — controls content width via v2 API.

| Value | Renderer Class | Content Width | Font (body) |
| --- | --- | --- | --- |
| not set | `is-full-page` (complex) or `is-max` (simple) | default | 16px or 13px |
| `"full-width"` | `is-full-width` (complex) or `is-max` (simple) | 100% viewport | 16px or 13px |
| `"fixed-width"` | same as not set | default | 16px or 13px |

> **Font-size is NOT controlled by this property.** Confluence selects `is-max` (compact, 13px) for simple pages and `is-full-page`/`is-full-width` (standard, 16px) for pages with Forge extensions.

**API:**

```bash
# Set full-width
POST /wiki/api/v2/pages/{page_id}/properties
{"key": "content-appearance-published", "value": "full-width"}

# Remove (revert to default)
DELETE /wiki/api/v2/pages/{page_id}/properties/{prop_id}

# List properties
GET /wiki/api/v2/pages/{page_id}/properties
```

### Mermaid Diagrams (Confluence)

The Mermaid plugin is a **Forge app** (`mermaid-diagram`). It requires **two elements** to render:

1. **Code block** (`language=mermaid`) — the diagram source text
2. **Forge `ac:adf-extension` macro** — the renderer (placed after code block)

> **Code block alone does NOT render.** The Forge macro reads the code block via `guest-params > index`. **CRITICAL:** index counts ALL code blocks on the page (not just mermaid ones).

**Step 1: Code block (source)**

```xml
<ac:structured-macro ac:name="code" ac:schema-version="1">
  <ac:parameter ac:name="language">mermaid</ac:parameter>
  <ac:parameter ac:name="title">Diagram Title</ac:parameter>
  <ac:plain-text-body><![CDATA[flowchart TD
    A --> B
    B --> C]]></ac:plain-text-body>
</ac:structured-macro>
```

**Step 2: Forge extension (renderer)** — can be constructed programmatically using `mermaid_diagram()`.

**Reference implementation:** `scripts/create-player-architecture-page.py`

- `mermaid_diagram(code, page_id)` — generates code block + Forge `ac:adf-extension` macro
- `tracked_code_block()` — wrapper for non-mermaid code blocks that increments global counter
- Global `_code_block_count` tracks position for Forge `guest-params > index`

**Two workflows for Mermaid diagrams:**

**A) Programmatic (preferred for scripts with multiple diagrams):**

1. Use `mermaid_diagram(code, page_id)` — generates code block + Forge macro with correct index
2. Use `tracked_code_block()` for ALL non-mermaid code blocks (maintains index counter)
3. Counter resets at start of `build_content()` — indices are sequential across all code blocks

**B) Manual (for one-off edits):**

1. User inserts `/mermaid` macro in Confluence editor with dummy content → Save
2. Script updates the code block's `CDATA` content with actual diagram text
3. Forge macro auto-reads updated code block on next page view

**Instance IDs ({{JIRA_SITE}}):**

| Parameter | Value |
| --- | --- |
| app-id | `23392b90-4271-4239-98ca-a3e96c663cbb` |
| environment-id | `63d4d207-ac2f-4273-865c-0240d37f044a` |
| installation-id | `5c245bad-32e8-4c74-aa1c-6d227f18fa22` |
| cloud-id | `85ad5bd2-ef9c-477e-b000-062f1421d0c0` |

**Common mistakes:**

| Mistake | Why it fails |
| --- | --- |
| Code block only (no Forge macro) | Displays as raw code text, not a rendered diagram |
| `ac:name="mermaid-cloud"` | Not a valid macro — renders as unknown macro error |
| `ac:name="mermaid-diagram"` as `ac:structured-macro` | This is the Forge `ac:adf-extension` key — cannot be constructed as `ac:structured-macro` |
| Wrong Forge `guest-params > index` | Index must count ALL code blocks on page, not just mermaid — use `tracked_code_block()` counter |

### Script Locations

```text
.claude/skills/atlassian-scripts/scripts/
├── create_confluence_page.py   → Create/update with code blocks
├── update_confluence_page.py   → Find/replace text
├── move_confluence_page.py     → Move page(s) to new parent
├── update_page_storage.py      → Add macros (ToC, Children)
└── fix_confluence_code_blocks.py → Fix broken code blocks
```

### Credentials File

```bash
# Check credentials
cat ~/.config/atlassian/.env

# Expected format:
CONFLUENCE_URL=https://{{JIRA_SITE}}/wiki
CONFLUENCE_USERNAME=your-email@example.com
CONFLUENCE_API_TOKEN=your-api-token
```

---

## Quick Fixes

| Problem | Quick Fix |
| --- | --- |
| Description ugly format | Use `acli --from-json` not MCP |
| Thai characters broken | Ensure UTF-8 encoding |
| Inline code not rendering | Use `marks: [{"type": "code"}]` |
| Panel wrong color | Check: info (blue), success (green), warning (yellow), error (red) |

---

## Related

- ADF format details: `templates.md`
- Tool selection: `tools.md`
- Atlassian scripts: `../atlassian-scripts/SKILL.md`
