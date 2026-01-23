---
name: jira-workflow
description: |
  Agile documentation workflow สำหรับ Tathep Platform - สร้าง, แก้ไข, ปรับปรุง Epics, User Stories, Sub-tasks, Test Plans ผ่าน Jira/Confluence

  **Create Commands:**
  - `/create-epic` - สร้าง Epic + Epic Doc จาก product vision
  - `/create-story` - สร้าง User Story ใหม่จาก requirements
  - `/analyze-story BEP-XXX` - วิเคราะห์ User Story → สร้าง Sub-tasks + Technical Note
  - `/create-testplan BEP-XXX` - สร้าง Test Plan + QA Sub-tasks

  **Update Commands:**
  - `/update-story BEP-XXX` - แก้ไข User Story ที่มีอยู่
  - `/update-subtask BEP-XXX` - แก้ไข Sub-task ที่มีอยู่
  - `/improve-issue BEP-XXX` - ปรับปรุง format/quality ของ issue(s)

  **Composite Commands (End-to-End):**
  - `/story-full` - สร้าง User Story + Sub-tasks ครบ workflow ในครั้งเดียว
  - `/story-cascade BEP-XXX` - Update Story + cascade ไปยัง Sub-tasks ที่เกี่ยวข้อง

  Triggers: "analyze story", "create subtask", "update", "improve", "migrate", "BEP-XXX", "แก้ไข", "ปรับปรุง", "story full", "cascade"
---

# Jira Workflow

Agile documentation workflow สำหรับ Tathep Platform

## Commands

### Create (สร้างใหม่)

| Command | Phases | Description |
|---------|:------:|-------------|
| `/create-epic` | 5 | สร้าง Epic + Epic Doc จาก product vision |
| `/create-story` | 5 | สร้าง User Story ใหม่จาก requirements |
| `/analyze-story BEP-XXX` | 7 | วิเคราะห์ Story → Sub-tasks + Technical Note |
| `/create-testplan BEP-XXX` | 6 | สร้าง Test Plan + QA Sub-tasks |

### Update (แก้ไข/ปรับปรุง)

| Command | Phases | Description |
|---------|:------:|-------------|
| `/update-story BEP-XXX` | 5 | แก้ไข User Story - เพิ่ม/แก้ AC, scope |
| `/update-subtask BEP-XXX` | 5 | แก้ไข Sub-task - format, content, language |
| `/improve-issue BEP-XXX` | 6 | Batch improve - migrate format, standardize |

### Composite (End-to-End Workflow)

| Command | Phases | Description |
|---------|:------:|-------------|
| `/story-full` | 10 | สร้าง Story + Sub-tasks ครบ workflow (PO+TA combined) |
| `/story-cascade BEP-XXX` | 8 | Update Story + cascade changes ไป Sub-tasks |

**Usage:** Read the command file from `commands/` directory for detailed phase instructions.

---

## Command Selection Guide

```
What do you need?
    │
    ├─ สร้างใหม่ (Create)
    │     ├─ Product vision → Epic           → /create-epic
    │     ├─ Requirements → Story            → /create-story
    │     ├─ Story → Sub-tasks               → /analyze-story BEP-XXX
    │     ├─ Story → Test Plan               → /create-testplan BEP-XXX
    │     └─ Story + Sub-tasks (ครบ workflow) → /story-full ⭐
    │
    ├─ แก้ไข/ปรับปรุง (Update)
    │     ├─ แก้ Story (เพิ่ม AC, scope)      → /update-story BEP-XXX
    │     ├─ แก้ Sub-task เดียว              → /update-subtask BEP-XXX
    │     ├─ ปรับปรุง format หลาย issues     → /improve-issue BEP-XXX --with-subtasks
    │     └─ แก้ Story + cascade Sub-tasks   → /story-cascade BEP-XXX ⭐
    │
    └─ ⭐ = Composite command (end-to-end workflow)
```

---

## Workflow Chain

```
Stakeholder → PM → PO → TA → QA
              │     │     │     │
              ↓     ↓     ↓     ↓
           Epic   Story  Sub-tasks  Test Cases
              │     │     │     │
              └─────┴─────┴─────┘
                    ↓
              Update/Improve (anytime)
```

---

## Project Settings

| Setting | Value |
|---------|-------|
| Jira Site | `100-stars.atlassian.net` |
| Project Key | `BEP` |
| Confluence Space | `BEP` |

## Service Paths

| Tag | Service | Path |
|-----|---------|------|
| `[BE]` | Backend | `~/Codes/Works/tathep/tathep-platform-api` |
| `[FE-Admin]` | Admin | `~/Codes/Works/tathep/tathep-admin` |
| `[FE-Web]` | Website | `~/Codes/Works/tathep/tathep-website` |

---

## Critical Rules

1. **Explore Before Design** - ห้ามสร้าง Sub-tasks โดยไม่ explore codebase ก่อน
2. **ADF Format** - ใช้ `acli --from-json` สำหรับ Jira descriptions (ไม่ใช่ MCP)
3. **Thai + ทับศัพท์** - เนื้อหาภาษาไทย, technical terms เป็นภาษาอังกฤษ
4. **Phase Gates** - ผ่านทุก phase ก่อนไปขั้นตอนถัดไป
5. **Preserve Intent** - Update commands ต้องรักษา original intent

---

## References

| Need | File |
|------|------|
| ADF Templates | [references/templates.md](references/templates.md) |
| Writing Style | [references/writing-style.md](references/writing-style.md) |
| Tool Selection | [references/tools.md](references/tools.md) |
