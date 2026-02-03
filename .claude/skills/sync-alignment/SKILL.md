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
4. Walk SIDEWAYS (Jira → Confluence):
   - per story: confluence_search("BEP-XXX") → Tech Note
   - epic: confluence_search(epic_title) → Epic Doc
```

**Token optimization:** fetch only `fields="summary,status,issuetype,parent"` (do not fetch description)

Output: inventory table

```text
| # | Type       | Key/ID     | Title                  | Status      |
|---|------------|------------|------------------------|-------------|
| 1 | Epic       | BEP-100    | Feature X              | In Progress |
| 2 | Epic Doc   | pg:123456  | Epic: Feature X        | -           |
| 3 | Story      | BEP-101    | Story A                | To Do       |
| 4 | Tech Note  | pg:789012  | Tech Note: Story A     | -           |
| 5 | Sub-task   | BEP-102    | [BE] - API endpoint    | To Do       |
| 6 | Sub-task   | BEP-103    | [FE-Admin] - Form      | To Do       |
| 7 | Sub-task   | BEP-104    | [QA] - Test plan       | To Do       |
```

**Gate:** User selects scope:

| Scope | Description |
| --- | --- |
| Full | Sync all artifacts (Jira + Confluence) |
| Jira-only | Sync only Jira issues |
| Confluence-only | Sync only Confluence pages |
| Selective | User selects specific artifacts to sync |

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

Map changes → affected artifacts:

```text
| Artifact            | Impact    | Reason                          |
|---------------------|-----------|--------------------------------|
| BEP-101 Story       | ORIGIN    | AC2 modified                    |
| BEP-102 [BE]        | UPDATE    | AC2 maps to API endpoint        |
| BEP-103 [FE-Admin]  | UPDATE    | AC2 maps to admin form          |
| BEP-104 [QA]        | FLAG      | Test cases for AC2 (QA review)  |
| pg:789012 Tech Note | UPDATE    | API spec section needs update   |
| BEP-100 Epic        | NO CHANGE | Scope unchanged                 |
| pg:123456 Epic Doc  | NO CHANGE | Summary unchanged               |
```

Impact types:

| Impact | Action |
| --- | --- |
| ORIGIN | Starting point (already changed) |
| UPDATE | Will be updated in Phase 7 |
| FLAG | Alert for review (no auto-update) |
| NO CHANGE | No action needed |

Sync directions:

| Direction | Example |
| --- | --- |
| DOWN | Story → Sub-tasks, Epic → Stories |
| UP | Sub-task → Story, Story → Epic |
| SIDEWAYS | Jira → Confluence, Confluence → Jira |

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

```bash
# 1. Epic (if changed)
acli jira workitem edit --from-json tasks/sync-bep-epic.json --yes

# 2. Story (if changed)
acli jira workitem edit --from-json tasks/sync-bep-story.json --yes

# 3. Sub-tasks (if changed)
acli jira workitem edit --from-json tasks/sync-bep-subtask1.json --yes
acli jira workitem edit --from-json tasks/sync-bep-subtask2.json --yes

# 4. Confluence - surgical:
python3 .claude/skills/atlassian-scripts/scripts/update_confluence_page.py \
  --page-id XXX --find "old text" --replace "new text"

# 4. Confluence - full rewrite:
python3 .claude/skills/atlassian-scripts/scripts/create_confluence_page.py \
  --page-id XXX --content-file tasks/sync-page-xxx.md

# OR surgical Jira (text-only changes):
python3 .claude/skills/atlassian-scripts/scripts/update_jira_description.py \
  --config tasks/sync-jira-fixes.json
```

**Tool selection:**

| Jira Change Type | Tool |
| --- | --- |
| Rewrite description | `acli --from-json` (ADF) |
| Text replacement only | `update_jira_description.py` (surgical) |
| Fields only (no description) | MCP `jira_update_issue` |

| Confluence Change Type | Tool |
| --- | --- |
| Text replacement | `update_confluence_page.py --find --replace` |
| Section/full rewrite | `create_confluence_page.py --page-id --content-file` |
| Code blocks/macros | `update_page_storage.py --page-id --content-file` |

### 8. Verify & Report

```bash
# Verify Confluence alignment
python3 .claude/skills/atlassian-scripts/scripts/audit_confluence_pages.py \
  --config tasks/sync-audit.json
```

Output:

```text
## Sync Complete

### Origin: BEP-101 (Story - AC2 modified)

| Artifact            | Action  | Status |
|---------------------|---------|--------|
| BEP-101 Story       | ORIGIN  | -      |
| BEP-102 [BE]        | UPDATED | OK     |
| BEP-103 [FE-Admin]  | UPDATED | OK     |
| BEP-104 [QA]        | FLAGGED | Review |
| pg:789012 Tech Note | UPDATED | OK     |
| BEP-100 Epic        | SKIPPED | N/A    |

Flagged for review:
- BEP-104 [QA]: AC2 changed → test cases may need update

→ /verify-issue BEP-101 --with-subtasks
```

Cleanup:

```bash
rm tasks/sync-*.json tasks/sync-*.md
```

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
- [Verification Checklist](../shared-references/verification-checklist.md) - Quality checks
- [Atlassian Scripts](../atlassian-scripts/SKILL.md)
- [Verification Checklist](../shared-references/verification-checklist.md)
