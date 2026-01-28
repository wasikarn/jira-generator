# Troubleshooting Guide

> Universal error recovery สำหรับ jira-workflow commands

---

## acli Errors

### JSON Format Errors

| Error | Cause | Solution |
| --- | --- | --- |
| `unknown field "project"` | Wrong field name | Use `projectKey` not `project` |
| `unknown field "parent"` | acli ไม่รองรับ parent field | ใช้ Two-Step Workflow: MCP create + acli edit |
| `missing required field` | Incomplete JSON | Check all required fields present |
| `invalid JSON syntax` | Malformed JSON | Validate JSON structure |
| `issues field required` | Edit without issue key | Add `"issues": ["BEP-XXX"]` for edits |

**Create vs Edit JSON:**

```json
{
  "projectKey": "BEP",
  "type": "Story",
  "summary": "..."
}
```

Note: CREATE has no "issues" field, EDIT requires `"issues": ["BEP-XXX"]`.

### Subtask Creation (Two-Step Workflow)

> ⚠️ **เจอ `unknown field "parent"`?** ใช้ workflow นี้

**Step 1: Create shell ด้วย MCP**

```typescript
jira_create_issue({
  project_key: "BEP",
  summary: "[TAG] - Description",
  issue_type: "Subtask",
  additional_fields: { parent: { key: "BEP-XXX" } }
})
// Returns: BEP-YYY (new subtask key)
```

**Step 2: Update description ด้วย acli**

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
| `INVALID_INPUT` (InvalidPayloadException) | Nested bulletList | ❌ listItem > bulletList ไม่ได้ - flatten หรือใช้ comma-separated text |

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
| `Expecting ')' but got 'ORDER'` | ORDER BY กับ parent query | ใช้ `"Parent Link" = BEP-XXX ORDER BY...` แทน `parent = BEP-XXX ORDER BY...` |
| `Field not found` | Wrong field name | Use `issuetype` not `type` for search |
| `No issues found` | Empty result | Broaden search criteria |

### Issue Errors

| Error | Cause | Solution |
| --- | --- | --- |
| `Issue not found` | Wrong key | Verify format: `BEP-XXX` |
| `Cannot read property` | Issue deleted | Issue may have been removed |
| `Rate limited` | Too many requests | Wait and retry |
| `exceeds maximum allowed tokens` | Issue มีข้อมูลเยอะเกินไป | ใช้ `fields` parameter จำกัด fields ที่ดึง |

### Large Output Error

เมื่อเจอ error นี้:

```text
Error: result (73,235 characters) exceeds maximum allowed tokens.
Output has been saved to /path/to/tool-results/...
```

**Solution:** ใช้ `fields` parameter เพื่อจำกัดข้อมูลที่ดึง:

```python
# ❌ Bad - ดึงทุก field ทำให้ข้อมูลเยอะ
jira_get_issue(issue_key="BEP-XXX")

# ✅ Good - ระบุเฉพาะ fields ที่ต้องการ
jira_get_issue(
    issue_key="BEP-XXX",
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

## Quick Fixes

| Problem | Quick Fix |
| --- | --- |
| Description ugly format | Use `acli --from-json` not MCP |
| Thai characters broken | Ensure UTF-8 encoding |
| Inline code not rendering | Use `marks: [{"type": "code"}]` |
| Panel wrong color | Check: info (blue), success (green), warning (yellow), error (red) |

---

## Related

- ADF format details: `references/templates.md`
- Tool selection: `references/tools.md`
- Full troubleshooting: `~/.claude/skills/atlassian-cli/SKILL.md`
