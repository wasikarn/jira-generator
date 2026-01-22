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

```
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
