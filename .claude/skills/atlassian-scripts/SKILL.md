---
name: atlassian-scripts
description: |
  Python scripts สำหรับ update Confluence pages และ Jira issues ผ่าน REST API โดยตรง
  ใช้เมื่อ MCP tool มีข้อจำกัด (เช่น code macro formatting, ADF manipulation)

  Triggers: "fix confluence", "update confluence page", "confluence script", "fix jira description", "atlassian script"
argument-hint: "[script-name] [args]"
---

# Atlassian Scripts

**Role:** Developer / Tech Lead
**Output:** Created/Updated Confluence Pages & Jira Issues
**Version:** 3.0.0 (Renamed from confluence-scripts, + JiraAPI)

## Architecture

```text
atlassian-scripts/
├── __init__.py              # Package marker
├── lib/                     # Shared library modules
│   ├── __init__.py          # Public exports
│   ├── exceptions.py        # Custom exceptions (Confluence + Jira)
│   ├── auth.py              # SSL, credentials, auth
│   ├── api.py               # ConfluenceAPI class
│   ├── jira_api.py          # JiraAPI class (REST v3, ADF)
│   └── converters.py        # Content converters
└── scripts/                 # CLI scripts
    ├── create_confluence_page.py
    ├── update_confluence_page.py
    ├── move_confluence_page.py
    ├── update_page_storage.py
    ├── fix_confluence_code_blocks.py
    ├── audit_confluence_pages.py
    └── update_jira_description.py
```

### Module Responsibilities (SRP)

| Module | Responsibility |
| --- | --- |
| `exceptions.py` | Domain-specific exceptions (Confluence + Jira) |
| `auth.py` | Authentication (SSL, credentials, auth header) |
| `api.py` | HTTP/API operations via ConfluenceAPI class |
| `jira_api.py` | Jira REST API v3 client (ADF manipulation) |
| `converters.py` | Content transformation (markdown, code blocks) |

---

## Available Scripts

| Script | Description | Use Case |
| --- | --- | --- |
| `create_confluence_page.py` | Create/Update page พร้อม proper code blocks | สร้างหรือ update page ที่มี code |
| `update_confluence_page.py` | Find/Replace text ใน page | Batch text replacement |
| `move_confluence_page.py` | Move page(s) to new parent | Reorganize page hierarchy |
| `update_page_storage.py` | Update page ด้วย raw storage format | Pages ที่ต้องการ macros (ToC, Children) |
| `fix_confluence_code_blocks.py` | แก้ไข code blocks ที่ render ผิด | Fix broken code formatting |
| `audit_confluence_pages.py` | ตรวจสอบ content ของหลาย pages | Alignment verification |
| `update_jira_description.py` | Find/Replace text ใน Jira ADF descriptions | Fix Jira issue descriptions |

---

## Prerequisites

**Credentials:** `~/.config/atlassian/.env`

```env
CONFLUENCE_URL=https://100-stars.atlassian.net/wiki
CONFLUENCE_USERNAME=your-email@example.com
CONFLUENCE_API_TOKEN=your-api-token
```

---

## Script Selection Guide

```text
ต้องการทำอะไร?
    │
    ├─ สร้าง page ใหม่
    │     └─ create_confluence_page.py --space --title
    │
    ├─ Update content ทั้งหมด
    │     └─ create_confluence_page.py --page-id --content-file
    │
    ├─ Find/Replace text
    │     └─ update_confluence_page.py --find --replace
    │
    ├─ Move page(s) to new parent
    │     └─ move_confluence_page.py --page-id(s) --parent-id
    │
    ├─ Add macros (ToC, Children, Status)
    │     └─ update_page_storage.py --page-id --content-file
    │
    ├─ Fix broken code blocks
    │     └─ fix_confluence_code_blocks.py --page-id(s)
    │
    ├─ Verify content alignment
    │     └─ audit_confluence_pages.py --config audit.json
    │
    └─ Fix Jira issue descriptions (ADF)
          └─ update_jira_description.py --config fixes.json
```

---

## When to Use Scripts vs MCP

| Scenario | Tool | Why |
| --- | --- | --- |
| Simple page read | MCP `confluence_get_page` | Fast, no script needed |
| Simple page create (no code) | MCP `confluence_create_page` | Markdown works fine |
| Page with code blocks | **Script** | MCP breaks code formatting |
| Batch text replacement | **Script** | More reliable |
| Fix broken formatting | **Script** | Direct storage format access |

---

---

## Supporting Files

> Load เฉพาะที่ต้องการ — ไม่ต้อง load ทั้งหมดเมื่อ invoke

| File | Content | Load When |
| --- | --- | --- |
| [script-reference.md](script-reference.md) | Script 1-7 usage, arguments, examples | เลือก script แล้ว ต้องการ full docs |
| [library-api.md](library-api.md) | ConfluenceAPI, JiraAPI, Converters, Exceptions | สร้าง custom script |
| [technical-notes.md](technical-notes.md) | SSL, Storage Format, Mermaid, History | Troubleshooting |

---

## References

- Confluence REST API: <https://developer.atlassian.com/cloud/confluence/rest/v1/intro/>
- Jira REST API v3: <https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/>
- Credentials: `~/.config/atlassian/.env`
- Storage Format: <https://developer.atlassian.com/cloud/confluence/confluence-storage-format/>
- ADF (Atlassian Document Format): <https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/>

---

## Related Skills

| Skill | Description |
| --- | --- |
| `/create-doc` | Create new Confluence page (uses MCP) |
| `/update-doc` | Update existing Confluence page (uses scripts when needed) |
