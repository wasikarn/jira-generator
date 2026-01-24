---
name: improve-issue
description: |
  ปรับปรุง format/quality ของ issue(s) แบบ batch ด้วย 6-phase workflow

  Phases: Discovery → Analyze Quality → Load Templates → Generate Improvements → Apply Updates → Cleanup

  รองรับ: batch format migration, language standardization, template compliance

  Triggers: "improve", "migrate", "ปรับปรุง format", "standardize"
argument-hint: "[issue-key] [--with-subtasks]"
---

# /improve-issue

**Role:** Technical Analyst
**Output:** Improved issues with better format/content

## Phases

### 1. Discovery
- `MCP: jira_get_issue(issue_key: "BEP-XXX")`
- ถ้า `--with-subtasks` → `MCP: jira_search(jql: "parent = BEP-XXX")`
- Build inventory: Key, Type, Current Format
- **Gate:** User confirms scope

### 2. Analyze Quality

| Dimension | Check |
|-----------|-------|
| Format | ADF with panels? Inline code marks? |
| Language | Thai + ทับศัพท์? |
| Structure | Follows template? |
| Completeness | All sections present? |
| Clarity | ACs testable? Given/When/Then? |

Score: ⭐⭐⭐☆☆ (3/5) per dimension

**Gate:** User approves improvement scope

### 3. Load Templates
- Story → `jira-templates/02-user-story.md`
- Sub-task → `jira-templates/03-sub-task.md`
- QA → `jira-templates/04-qa-test-case.md`
- Load: `shared-references/writing-style.md`, `shared-references/templates.md`

### 4. Generate Improvements
- Preserve original intent/content
- Apply template structure
- Convert to ADF format
- Apply Thai + ทับศัพท์
- Add inline code marks
- Generate JSON files → `tasks/bep-xxx-improved.json`
- **Gate:** User reviews and approves

### 5. Apply Updates
```bash
acli jira workitem edit --from-json tasks/bep-xxx-improved.json --yes
```
Track: ✅ Updated / ❌ Failed (retry)

### 6. Cleanup & Summary
```bash
rm tasks/bep-*-improved.json
```

```
## Improvement Complete
Updated: BEP-XXX, BEP-YYY, BEP-ZZZ
Quality: wiki → ADF, EN → Thai
```

---

## Common Scenarios

| Scenario | Command |
|----------|---------|
| Batch format | `/improve-issue BEP-XXX --with-subtasks` |
| Single polish | `/improve-issue BEP-YYY "add panels"` |
| Language fix | `/improve-issue BEP-XXX "standardize Thai"` |
| Template align | `/improve-issue BEP-XXX "align templates"` |

---

## References

- [ADF Templates](../shared-references/templates.md)
- [Writing Style](../shared-references/writing-style.md)
