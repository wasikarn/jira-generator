# Shared Configuration

> **Purpose:** Project settings และ MCP tools ที่ใช้ร่วมกันทุก roles

---

## Project Settings

| Setting | Value |
| --- | --- |
| **Jira Site** | `100-stars.atlassian.net` |
| **Jira Project Key** | `BEP` |
| **Confluence Space** | `BEP` |
| **Sprint Duration** | 2 weeks |
| **Default Capacity** | 30-40 points/sprint |

### Naming Conventions

| Type | Format | Example |
| --- | --- | --- |
| Epic | `[Epic Name]` | `User Authentication` |
| User Story | `As a [persona]...` | `As a customer, I want to...` |
| Sub-task | `[TAG] - Description` | `[BE] - Create login API` |

### Service Tags

| Tag | Service | Local Path | GitHub |
| --- | --- | --- | --- |
| `[BE]` | Backend | `~/Codes/Works/tathep/tathep-platform-api` | `100-Stars-Co/bd-eye-platform-api` |
| `[FE-Admin]` | Admin | `~/Codes/Works/tathep/tathep-admin` | `100-Stars-Co/bluedragon-eye-admin` |
| `[FE-Web]` | Website | `~/Codes/Works/tathep/tathep-website` | `100-Stars-Co/bluedragon-eye-website` |

---

## MCP Tools Reference

### Atlassian MCP

| Tool | Purpose |
| --- | --- |
| `Atlassian:search` | Search issues/pages |
| `Atlassian:getJiraIssue` | Get issue details |
| `Atlassian:createJiraIssue` | Create Epic/Story/Sub-task |
| `Atlassian:editJiraIssue` | Update issue |
| `Atlassian:createConfluencePage` | Create doc page |
| `Atlassian:getConfluencePage` | Get page content |
| `Atlassian:searchJiraIssuesUsingJql` | JQL search |

### Codebase Access

1. **Local first** (Repomix MCP)
2. **GitHub fallback** (Github MCP)
3. **Report if both fail**

---

## Documentation Hierarchy

```text
Epic (BEP-XXX)
├── Epic Doc (Confluence)
└── User Stories (BEP-YYY)
    ├── User Story Doc (Confluence)
    └── Sub-tasks (BEP-ZZZ)
```

### Confluence Page Titles

| Type | Title Format |
| --- | --- |
| Epic Doc | `Epic: [Name] (BEP-XXX)` |
| User Story Doc | `User Story: [Name] (BEP-XXX)` |

---

## Language Guidelines

### โทนการเขียน

| ✅ ทำ | ❌ ไม่ทำ |
| --- | --- |
| เป็นกันเอง คุยกับทีม casual | ใช้สำนวนราชการ/ทางการเกินไป |
| กระชับ ตรงประเด็น | เยิ่นเย้อ ใช้คำฟุ่มเฟือย |
| ชัดเจน ไม่คลุมเครือ | ใช้คำคลุมเครือ "ควรจะ", "น่าจะ" |

### Technical Terms (ใช้ทับศัพท์)

| หมวด | ใช้ทับศัพท์ |
| --- | --- |
| **Process** | deploy, merge, sprint, release, commit |
| **Architecture** | API, endpoint, payload, component, service |
| **Development** | debug, refactor, validate, implement |
| **Agile** | backlog, velocity, story point, estimate |
| **Data** | schema, migration, query, cache |

> 💡 **Tip:** ทีมคุ้นเคยกับคำเหล่านี้อยู่แล้ว การแปลเป็นไทยอาจทำให้สับสนมากกว่า

### Editing Guidelines

เมื่อแก้ไขเนื้อหาที่มีอยู่:

1. **รักษา core message** - ไม่เปลี่ยนวัตถุประสงค์เดิม
2. **ปรับแค่ภาษา/flow** - ไม่เปลี่ยน meaning หรือ intent
3. **ถามก่อนแก้** - หากไม่แน่ใจว่าจะกระทบความหมายเดิม
