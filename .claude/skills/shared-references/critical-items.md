# Critical Items Checklist

> Items that **must remain** in Passive Context at all times after optimization
> Used by Phase 5 of `/optimize-context` to verify that compression does not lose important data

## Format

```text
pattern | description | source
```

- **pattern**: regex for grepping the Passive Context section
- **description**: explains what is being checked
- **source**: the shared-ref file that is the source of truth

---

## Critical (skill will fail if missing)

```text
CREATE.*EDIT | CREATE vs EDIT JSON format distinction | templates.md
issues.*BEP | EDIT requires "issues" array | templates.md
acli.*from-json | acli for description create/update | tools.md
Two-Step|MCP create.*acli edit | Subtask two-step workflow | tools.md
panelType | Panel types reference exists | templates.md
info.*success.*warning.*error.*note | All 5 panel types listed | templates.md
fields.*parameter|fields.*jira_get_issue | fields parameter required for get_issue | tools.md
```

## Important (quality will degrade if missing)

```text
Thai.*loanword|loanword | Language rule: Thai + loanwords (transliteration) | writing-style.md
Given.*When.*Then | AC format: Given/When/Then | verification-checklist.md
INVEST | Story quality criteria | verification-checklist.md
\[BE\].*\[FE | Service tags reference | writing-style.md
panels.*not.*table|table.*not.*panel | AC must use panels not tables | templates.md
Confluence.*script|Python.*script | Confluence operations need scripts | tools.md
```

---

## Maintenance

When adding a new rule to shared-refs:

1. Ask yourself: "If this rule disappears from passive context, will the skill fail?"
2. If yes → add to Critical
3. If it won't fail but quality drops → add to Important
4. If it's just a detail → don't add (keep in the original shared-ref file)
