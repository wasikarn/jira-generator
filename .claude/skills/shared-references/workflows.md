# Workflow Patterns

## Phase Gate Pattern

ทุก phase ต้องผ่าน gate ก่อนไป phase ถัดไป:

```text
Phase N: [Goal]
  Actions → Output → Gate (user confirms) → Phase N+1
```

## Standard Phase Types

### Discovery Phase

1. Fetch data from Jira/Confluence
2. อ่านและสรุป context
3. **Gate:** User confirms understanding

### Analysis Phase

1. วิเคราะห์ requirements/impact
2. สร้าง analysis output (table, matrix)
3. **Gate:** User approves scope

### Design Phase

1. Draft content/structure
2. Apply templates and style
3. **Gate:** User reviews draft

### Create Phase

1. Generate ADF JSON → `tasks/` folder
2. Execute via `acli jira workitem create --from-json`
3. Verify creation

### Update Phase

1. Generate ADF JSON with `"issues": ["BEP-XXX"]`
2. Execute via `acli jira workitem edit --from-json --yes`
3. Verify update

### Handoff Phase

1. สรุปผลลัพธ์
2. List follow-up actions
3. Suggest next command

---

## Tool Selection

| Task | Tool | Why |
| --- | --- | --- |
| Create/Update Jira description | `acli --from-json` | ADF renders correctly |
| Update fields only | MCP `jira_update_issue` | Simple, fast |
| Search Jira | MCP `jira_search` | JQL support |
| Read issue | MCP `jira_get_issue` | Full details |
| Create Confluence (simple) | MCP `confluence_create_page` | Accepts markdown |
| Confluence with code/macros | Python scripts | MCP breaks formatting |

> **Note:** สำหรับ Confluence pages ที่มี code blocks, macros (ToC, Children), หรือต้องการ move
> ให้ใช้ Python scripts ใน `.claude/skills/atlassian-scripts/scripts/`

---

## Effort Sizing

| Size | Description | Action |
| --- | --- | --- |
| S | < 2 days | Single sub-task |
| M | 2-5 days | Single sub-task |
| L | 5-10 days | Consider splitting |
| XL | > 10 days | Must split |

---

## Service Tags

| Tag | Service | Path |
| --- | --- | --- |
| `[BE]` | Backend | `~/Codes/Works/tathep/tathep-platform-api` |
| `[FE-Admin]` | Admin | `~/Codes/Works/tathep/tathep-admin` |
| `[FE-Web]` | Website | `~/Codes/Works/tathep/tathep-website` |
| `[QA]` | QA Test | N/A |

---

## INVEST Criteria

| Criteria | Question |
| --- | --- |
| **I**ndependent | ไม่พึ่งพา story อื่น? |
| **N**egotiable | มี room สำหรับ discussion? |
| **V**aluable | มี business value ชัดเจน? |
| **E**stimable | ประเมิน effort ได้? |
| **S**mall | ทำเสร็จใน 1 sprint? |
| **T**estable | ทุก AC verify ได้? |

---

## AC Format

```text
Given: [precondition]
When: [action]
Then: [expected result]
```

**Good:** specific, measurable, testable
**Bad:** vague, subjective, untestable
