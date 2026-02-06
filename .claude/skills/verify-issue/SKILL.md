---
name: verify-issue
description: |
  Verify and improve issue quality (ADF format, INVEST, language, hierarchy alignment) with a 6-phase workflow

  Checks: ADF render, panel structure, links, inline code, INVEST criteria, Given/When/Then, file paths, language consistency, hierarchy alignment (Epic↔Story↔Subtasks↔Docs)

  Supports: --with-subtasks (batch + alignment check), --fix (auto-fix + format migration)

  Triggers: "verify", "validate", "check quality", "improve", "migrate format"
argument-hint: "[issue-key] [--with-subtasks] [--fix]"
---

# /verify-issue

**Role:** Any
**Output:** Verification report (default) or Improved issues (with `--fix`)

## Phases

### 1. Fetch & Identify

- `MCP: jira_get_issue(issue_key: "BEP-XXX")`
- If `--with-subtasks` → `MCP: jira_search(jql: "parent = BEP-XXX", fields: "summary,status,assignee,issuetype")` (**⚠️ NEVER add ORDER BY to parent queries**)
- Identify type → Select checklist
- Build inventory: Key, Type, Current Format
- **Gate (--fix only):** User confirms scope

### 2. Technical Verification

| Check | Pass Criteria |
| --- | --- |
| ADF Format | Has `type: "doc"` |
| Panels | Correct `panelType` |
| Inline Code | Technical terms marked |
| Links | Parent/child exist |
| Fields | Required fields filled |

### 3. Quality Verification

| Dimension | Check |
| --- | --- |
| Format | ADF with panels? Inline code marks? |
| Language | Thai + transliterated loanwords? |
| Structure | Follows template? |
| Completeness | All sections present? |
| Clarity | ACs testable? Given/When/Then? |

Score: ⭐⭐⭐☆☆ (per dimension, 5-point scale)

**Type-specific checks:**

- **Story:** INVEST criteria (6 points), Narrative format, AC Given/When/Then
- **Sub-task:** Objective clear, File paths real (not generic), AC format correct
- **QA:** All Story ACs covered, Test scenarios clear, Priority assigned

### 4. Hierarchy Alignment (`--with-subtasks` only)

> **Principle:** Use only real data fetched from Jira/Confluence — never guess.
> If unsure which AC maps to which subtask → flag as "unclear mapping"

**Data fetching:**

```text
1. Story → jira_get_issue(story_key) — ACs, scope, services impacted
2. Epic → jira_get_issue(story.parent) — scope, must-have list (skip if none)
3. Subtasks → already fetched in Phase 1
4. Confluence → confluence_search("BEP-XXX") — Tech Note (skip if none)
```

**Alignment checks:**

| ID | Check | How to Verify | Pass Criteria |
| --- | --- | --- | --- |
| A1 | AC ↔ Subtask Coverage | Map each Story AC → subtask(s) that implement it | Every AC has ≥1 subtask covering it |
| A2 | Service Tag Match | Story "Services Impacted" → Subtask tags `[BE]`/`[FE-*]` | Every service has a subtask |
| A3 | Scope Consistency | Story in-scope items → Subtask objectives cover them | No scope gaps |
| A4 | Epic ↔ Story Fit | Story scope falls within Epic must-have/should-have | Story does not exceed Epic scope |
| A5 | Parent-Child Links | Subtask.parent = Story, Story.parent = Epic | Links are correct |
| A6 | Confluence Alignment | Tech Note content aligns with Story ACs (if exists) | No conflicts |

**Rules:**

- If no Epic (standalone Story) → skip A4
- If no Confluence page → skip A6, flag as info
- If mapping is unclear → flag "unclear mapping" (never guess)
- Report only what can be verified from actual data

### 5. Report

```text
## Verification: BEP-XXX

| Category | Score | Status |
|----------|-------|--------|
| Technical | 5/5 | ✅ Pass |
| Quality | 4/6 | ⚠️ Warning |
| Alignment | 5/6 | ⚠️ Warning |  ← (--with-subtasks only)
| **Overall** | 14/17 | ⚠️ |

Issues:
1. ⚠️ AC3 missing "Then"
2. ❌ Language mixed

Alignment Issues (--with-subtasks):
1. ⚠️ AC3 has no subtask covering it
2. ⚠️ Story specifies [FE-Web] but no subtask has [FE-Web] tag

→ /verify-issue BEP-XXX --fix
```

### 6. Fix (--fix flag only)

If `--fix` is present → apply all fixes found in Phases 2-4:

1. **Load Templates** — Fetch template for the issue type from `shared-references/`
2. **Generate** — Preserve original intent, apply template + ADF + Thai + inline code → `tasks/bep-xxx-fixed.json`
3. **Gate:** User reviews and approves
4. **Apply** — `acli jira workitem edit --from-json tasks/bep-xxx-fixed.json --yes`
5. **Cleanup** — `rm tasks/bep-*-fixed.json`

```text
## Fix Complete
Updated: BEP-XXX, BEP-YYY, BEP-ZZZ
Quality: wiki → ADF, EN → Thai
```

---

## Batch Mode

```text
/verify-issue BEP-XXX --with-subtasks
/verify-issue BEP-XXX --with-subtasks --fix
```

| Key | Technical | Quality | Alignment | Overall |
| --- | --- | --- | --- | --- |
| BEP-XXX (Story) | 5/5 ✅ | 4/6 ⚠️ | 5/6 ⚠️ | ⚠️ |
| BEP-YYY [BE] | 5/5 ✅ | 6/6 ✅ | — | ✅ |
| BEP-ZZZ [FE-Web] | 5/5 ✅ | 5/6 ⚠️ | — | ⚠️ |

---

## Common Scenarios

| Scenario | Command |
| --- | --- |
| Quick check | `/verify-issue BEP-XXX` |
| Check story + subtasks | `/verify-issue BEP-XXX --with-subtasks` |
| Auto-fix single issue | `/verify-issue BEP-XXX --fix` |
| Batch format migration | `/verify-issue BEP-XXX --with-subtasks --fix` |
| Language standardization | `/verify-issue BEP-XXX --fix "standardize Thai"` |

---

## Integration

| After Command | Verify With |
| --- | --- |
| `/create-story` | `/verify-issue BEP-XXX` |
| `/analyze-story` | `/verify-issue BEP-XXX --with-subtasks` |
| `/story-full` | `/verify-issue BEP-XXX --with-subtasks` |
| `/improve-issue` (legacy) | → Use `/verify-issue BEP-XXX --with-subtasks --fix` instead |

---

## References

- [Verification Checklist](../shared-references/verification-checklist.md)
- [ADF Core Rules](../shared-references/templates.md) - CREATE/EDIT rules, panels, styling
- [Templates](../shared-references/templates.md) - ADF templates (Epic, Story, Sub-task, Task)
- [Writing Style](../shared-references/writing-style.md)
