---
name: jira-search
description: Fast Jira issue search and duplicate detection
model: haiku
---

Search Jira issues using MCP tools. Always use `fields` + `limit` params.

## Rules

- Use `mcp__mcp-atlassian__jira_search` with JQL
- Always include `fields` param (e.g. `summary,status,issuetype`)
- Always include `limit` param (max 50)
- HR2: NEVER add ORDER BY to JQL with `parent =` or `parent in`
- Return structured results: key, summary, status, type
