---
name: sync-alignment
description: |
  Sync all related artifacts (Epic, Story, Sub-tasks, QA, Confluence) using an 8-phase workflow

  Phases: Identify Origin → Build Graph → Detect Changes → Impact Analysis → Explore (if needed) → Generate Updates → Execute Sync → Verify & Report

  ⭐ Composite: bidirectional sync from any artifact, covering both Jira + Confluence

  Triggers: "sync alignment", "sync all", "update related", "cascade all", "align artifacts"
argument-hint: "[issue-key-or-page-id] [changes]"
---

# /sync-alignment

**Role:** PO + TA + Tech Lead Combined
**Output:** Updated Jira issues + Confluence pages (all related artifacts)

---

## Artifact Graph

```text
Epic (Jira)
├── Epic Doc (Confluence parent page) — story list, status summary
├── Story 1 (Jira) — ACs, scope
│   ├── Tech Note (Confluence child page) — technical details, API, DB
│   ├── Sub-task [BE] (Jira)
│   ├── Sub-task [FE-Admin] (Jira)
│   └── Sub-task [QA] (Jira)
├── Story 2 (Jira)
│   ├── Tech Note (Confluence)
│   └── Sub-tasks ...
└── ...
```

---

## Phases

### 1. Identify Origin

- Receive input: `BEP-XXX` (Jira key) or Confluence page ID
- `MCP: jira_get_issue(issue_key, fields="summary,status,issuetype,parent")`
- Determine artifact type: Epic / Story / Sub-task
- If Confluence page ID → `MCP: confluence_get_page(page_id)` → extract BEP keys → pivot to Jira
- **Gate:** User confirms starting artifact + describes what changed

### 2. Build Artifact Graph

Discovery algorithm:

```text
1. jira_get_issue(origin, fields="summary,status,issuetype,parent")
2. Walk UP:
   - if Sub-task → parent_story = issue.parent
   - if Story → parent_epic = issue.parent
   - if Sub-task → parent_epic = story.parent
3. Walk DOWN:
   - jira_search("parent = EPIC_KEY AND issuetype = Story") → stories
   - per story: jira_search("parent = STORY_KEY") → sub-tasks
   ⚠️ NEVER add ORDER BY to parent queries — causes JQL parse error
4. Walk SIDEWAYS (Jira → Confluence):
   - per story: confluence_search("BEP-XXX") → Tech Note
   - epic: confluence_search(epic_title) → Epic Doc
```

**Token optimization:** fetch only `fields="summary,status,issuetype,parent"` (no description)

Output: inventory table (Type, Key/ID, Title, Status) for all discovered artifacts.

**Gate:** User selects scope: Full (Jira+Confluence) / Jira-only / Confluence-only / Selective

### 3. Detect Changes

User describes changes, then classify:

| Change Type | Impact Level |
| --- | --- |
| Format only | LOW |
| Clarify wording | LOW |
| Add AC | MEDIUM |
| Modify AC | MEDIUM |
| Remove AC | HIGH |
| Change scope | HIGH |
| Technical detail change | MEDIUM |
| Business value change | HIGH |

**Gate:** User confirms changes

### 4. Impact Analysis

Map changes → affected artifacts table (Artifact, Impact, Reason).

Impact types: `ORIGIN` (starting point) / `UPDATE` (will sync) / `FLAG` (review only) / `NO CHANGE`
Directions: DOWN (parent→child) / UP (child→parent) / SIDEWAYS (Jira↔Confluence)

**Gate:** User approves sync plan

### 5. Codebase Exploration (conditional)

- Run only when: scope changed / need new file paths / new sub-task needed
- `Task(subagent_type: "Explore")`
- **Skip** if format-only / wording-only / technical detail change

### 6. Generate Sync Updates

Fetch full description only for artifacts with impact = UPDATE:

**Per Jira issue:**

- `MCP: jira_get_issue(issue_key, fields="summary,description")`
- Generate ADF JSON → `tasks/sync-bep-xxx.json`
- Show before/after comparison

**Per Confluence page:**

- `MCP: confluence_get_page(page_id)`
- If surgical (text replace) → prepare find/replace pairs
- If section update → generate new markdown section
- If full rewrite → generate full content → `tasks/sync-page-xxx.md`

**Gate:** User approves ALL updates before execution

### 7. Execute Sync

Order: Parents first → Children → Confluence

**Tool selection:**

| Change Type | Jira Tool | Confluence Tool |
| --- | --- | --- |
| Rewrite description | `acli --from-json` (ADF) | `create_confluence_page.py --page-id` |
| Text replacement | `update_jira_description.py` (surgical) | `update_confluence_page.py --find --replace` |
| Fields only | MCP `jira_update_issue` | — |
| Code blocks/macros | — | `update_page_storage.py` |

File pattern: `tasks/sync-bep-{type}.json` (Jira) / `tasks/sync-page-xxx.md` (Confluence)

### 8. Verify & Report

Verify with `audit_confluence_pages.py --config tasks/sync-audit.json`

Output: Summary table (Artifact, Action, Status) + flagged items for review.

Post-sync: `rm tasks/sync-*.json tasks/sync-*.md` → `/verify-issue BEP-XXX --with-subtasks`

---

## Edge Cases

| Case | Handling |
| --- | --- |
| Confluence page does not exist | Flag + recommend `/create-doc` (no auto-create) |
| No sub-tasks exist | Sync only Story <-> Epic/Confluence |
| Multiple Confluence pages match | List all and let user choose |
| Artifact graph > 20 items | Recommend breaking into multiple runs |
| Partial failure | Continue remaining + report failures |
| Issue DONE/CLOSED | Warning but allow sync (doc alignment) |
| No changes detected | Report "already aligned" + skip |
| QA sub-task affected | FLAG for QA review (no auto-rewrite of test plan) |
| Epic Doc affected | Update story status table + summary only |

---

## sync-alignment vs story-cascade

| Feature | `/story-cascade` | `/sync-alignment` |
| --- | --- | --- |
| Scope | Jira only | Jira + Confluence |
| Direction | Story → Sub-tasks (down) | Bidirectional (any → all) |
| Starting point | Story only | Epic / Story / Sub-task / Confluence |
| Confluence sync | No | Yes (Tech Notes + Epic Doc) |
| Use case | Quick Jira-only cascade | Full artifact alignment |
| Phases | 8 | 8 |

> **When to use which:**
>
> - `/story-cascade` — After editing a Story, cascade only to Jira sub-tasks (fast)
> - `/sync-alignment` — Need to sync everything including Confluence (comprehensive)

---

## References

- [ADF Core Rules](../shared-references/templates.md) - CREATE/EDIT rules, panels, styling
- [Epic Template](../shared-references/templates-epic.md)
- [Story Template](../shared-references/templates-story.md)
- [Sub-task Template](../shared-references/templates-subtask.md)
- [Task Template](../shared-references/templates-task.md)
- [Tool Selection](../shared-references/tools.md)
- [Verification Checklist](../shared-references/verification-checklist.md)
- [Atlassian Scripts](../atlassian-scripts/SKILL.md)
