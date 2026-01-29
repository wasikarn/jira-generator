---
name: sync-alignment
description: |
  Sync artifacts ที่เกี่ยวข้องทั้งหมด (Epic, Story, Sub-tasks, QA, Confluence) ด้วย 8-phase workflow

  Phases: Identify Origin → Build Graph → Detect Changes → Impact Analysis → Explore (if needed) → Generate Updates → Execute Sync → Verify & Report

  ⭐ Composite: bidirectional sync จาก artifact ใดก็ได้ ครอบคลุมทั้ง Jira + Confluence

  Triggers: "sync alignment", "sync all", "update related", "cascade all", "align artifacts"
argument-hint: "[issue-key-or-page-id] [changes]"
---

# /sync-alignment

**Role:** PO + TA + Tech Lead Combined
**Output:** Updated Jira issues + Confluence pages (ทุก artifacts ที่เกี่ยวข้อง)

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

- รับ input: `BEP-XXX` (Jira key) หรือ Confluence page ID
- `MCP: jira_get_issue(issue_key, fields="summary,status,issuetype,parent")`
- ระบุ artifact type: Epic / Story / Sub-task
- ถ้า Confluence page ID → `MCP: confluence_get_page(page_id)` → extract BEP keys → pivot ไป Jira
- **Gate:** User ยืนยัน starting artifact + บอกว่าเปลี่ยนอะไร

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

**Token optimization:** fetch เฉพาะ `fields="summary,status,issuetype,parent"` (ไม่ fetch description)

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

**Gate:** User เลือก scope:

| Scope | Description |
| --- | --- |
| Full | Sync ทุก artifacts (Jira + Confluence) |
| Jira-only | Sync เฉพาะ Jira issues |
| Confluence-only | Sync เฉพาะ Confluence pages |
| Selective | User เลือก artifacts ที่ต้อง sync |

### 3. Detect Changes

User อธิบาย changes ที่เกิดขึ้น แล้ว classify:

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

**Gate:** User ยืนยัน changes

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
| UPDATE | จะ update ใน Phase 7 |
| FLAG | แจ้งเตือนให้ review (ไม่ auto-update) |
| NO CHANGE | ไม่ต้องทำอะไร |

Sync directions:

| Direction | Example |
| --- | --- |
| DOWN | Story → Sub-tasks, Epic → Stories |
| UP | Sub-task → Story, Story → Epic |
| SIDEWAYS | Jira → Confluence, Confluence → Jira |

**Gate:** User approves sync plan

### 5. Codebase Exploration (conditional)

- Run เฉพาะเมื่อ: scope changed / need new file paths / new sub-task needed
- `Task(subagent_type: "Explore")`
- **Skip** ถ้า format-only / wording-only / technical detail change

### 6. Generate Sync Updates

Fetch full description เฉพาะ artifacts ที่มี impact = UPDATE:

**Per Jira issue:**

- `MCP: jira_get_issue(issue_key, fields="summary,description")`
- Generate ADF JSON → `tasks/sync-bep-xxx.json`
- Show before/after comparison

**Per Confluence page:**

- `MCP: confluence_get_page(page_id)`
- ถ้า surgical (text replace) → prepare find/replace pairs
- ถ้า section update → generate new markdown section
- ถ้า full rewrite → generate full content → `tasks/sync-page-xxx.md`

**Gate:** User approves ALL updates ก่อน execute

### 7. Execute Sync

ลำดับ: Parents first → Children → Confluence

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
| Confluence page ไม่มี | Flag + แนะนำ `/create-doc` (ไม่ auto-create) |
| ไม่มี sub-tasks | Sync เฉพาะ Story ↔ Epic/Confluence |
| Multiple Confluence pages match | List ทั้งหมด ให้ user เลือก |
| Artifact graph > 20 items | แนะนำ break เป็น multiple runs |
| Partial failure | Continue remaining + report failures |
| Issue DONE/CLOSED | Warning แต่ allow sync (doc alignment) |
| No changes detected | Report "already aligned" + skip |
| QA sub-task affected | FLAG สำหรับ QA review (ไม่ auto-rewrite test plan) |
| Epic Doc affected | Update story status table + summary only |

---

## sync-alignment vs story-cascade

| Feature | `/story-cascade` | `/sync-alignment` |
| --- | --- | --- |
| Scope | Jira only | Jira + Confluence |
| Direction | Story → Sub-tasks (down) | Bidirectional (any → all) |
| Starting point | Story only | Epic / Story / Sub-task / Confluence |
| Confluence sync | ไม่มี | มี (Tech Notes + Epic Doc) |
| Use case | Quick Jira-only cascade | Full artifact alignment |
| Phases | 8 | 8 |

> **เมื่อไหร่ใช้อะไร:**
>
> - `/story-cascade` — แก้ Story แล้วต้องการ cascade เฉพาะ Jira sub-tasks (เร็ว)
> - `/sync-alignment` — ต้องการ sync ทุกอย่างรวม Confluence (ครบ)

---

## References

- [ADF Core Rules](../shared-references/templates.md) - CREATE/EDIT rules, panels, styling
- [Epic Template](../shared-references/templates-epic.md)
- [Story Template](../shared-references/templates-story.md)
- [Sub-task Template](../shared-references/templates-subtask.md)
- [Task Template](../shared-references/templates-task.md)
- [Tool Selection](../shared-references/tools.md)
- [Workflows](../shared-references/workflows.md)
- [Atlassian Scripts](../atlassian-scripts/SKILL.md)
- [Verification Checklist](../shared-references/verification-checklist.md)
