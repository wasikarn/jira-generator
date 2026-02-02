# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Overview

Agile Documentation System for **Tathep Platform** - Create Epics, User Stories, and Sub-tasks via Jira/Confluence

## Project Settings

| Setting | Value |
| --- | --- |
| Jira Site | `100-stars.atlassian.net` |
| Project Key | `BEP` |
| Confluence Space | `BEP` |

## Quick Start (5 min)

1. **ต้องการสร้าง feature ใหม่?** → `/story-full` (สร้าง Story + Sub-tasks ครบ)
2. **มี Epic แล้ว ต้องการสร้าง Story?** → `/create-story`
3. **มี Story แล้ว ต้องการวิเคราะห์?** → `/analyze-story BEP-XXX`
4. **ต้องการสร้าง Task?** → `/create-task` (tech-debt, bug, chore, spike)

> ⚡ **หลังสร้างเสร็จ:** ใช้ `/verify-issue BEP-XXX` ตรวจสอบคุณภาพเสมอ

## Skill Commands

### Create (สร้างใหม่)

| Command | Description | Output |
| --- | --- | --- |
| `/create-epic` | สร้าง Epic จาก product vision | Epic + Epic Doc |
| `/create-story` | สร้าง User Story จาก requirements | User Story |
| `/create-task` | สร้าง Task (tech-debt, bug, chore, spike) | Task |
| `/analyze-story BEP-XXX` | วิเคราะห์ Story → Sub-tasks | Sub-tasks + Technical Note |
| `/create-testplan BEP-XXX` | สร้าง Test Plan จาก Story | Test Plan + [QA] Sub-tasks |
| `/create-doc` | สร้าง Confluence page (tech-spec, adr, parent) | Confluence Page |
| `/update-doc` | Update/Move Confluence page | Updated/Moved Page |

### Update (แก้ไข/ปรับปรุง)

| Command | Description | Output |
| --- | --- | --- |
| `/update-epic BEP-XXX` | แก้ไข Epic - ปรับ scope, RICE, metrics | Updated Epic |
| `/update-story BEP-XXX` | แก้ไข User Story - เพิ่ม/แก้ AC, scope | Updated Story |
| `/update-task BEP-XXX` | แก้ไข Task - migrate format, add details | Updated Task |
| `/update-subtask BEP-XXX` | แก้ไข Sub-task - format, content | Updated Sub-task |

### Composite (End-to-End Workflow) ⭐

| Command | Description | Output |
| --- | --- | --- |
| `/story-full` | สร้าง Story + Sub-tasks ครบ workflow ในครั้งเดียว | Story + Sub-tasks |
| `/story-cascade BEP-XXX` | Update Story + cascade ไป Sub-tasks ที่เกี่ยวข้อง | Updated Story + Sub-tasks |
| `/sync-alignment BEP-XXX` | Sync artifacts ทั้งหมด (Jira + Confluence) bidirectional | Updated issues + pages |

> **เมื่อไหร่ควรใช้ Composite:**
>
> - `/story-full` - เมื่อต้องการสร้าง feature ใหม่ครบ workflow (ไม่ต้อง copy-paste issue keys)
> - `/story-cascade` - เมื่อ update Story แล้วต้องการ cascade เฉพาะ Jira sub-tasks (เร็ว)
> - `/sync-alignment` - เมื่อต้องการ sync ทุกอย่างรวม Confluence (ครบ, bidirectional)

### Utility (เครื่องมือช่วย)

| Command | Description | Output |
| --- | --- | --- |
| `/search-issues` | ค้นหา issues ก่อนสร้างใหม่ (ป้องกันสร้างซ้ำ) | List of matching issues |
| `/verify-issue BEP-XXX` | ตรวจสอบ + ปรับปรุงคุณภาพ issue (ADF, INVEST, language) | Verification report / Improved issue(s) |
| `/optimize-context` | Audit shared-refs → compress ลง passive context | Updated CLAUDE.md / Report (`--dry-run`) |

> **เมื่อไหร่ควรใช้ Verify:**
>
> - หลังสร้าง issue ใหม่ → ตรวจสอบคุณภาพก่อน handoff
> - หลัง update → ยืนยันว่า format ถูกต้อง
> - `--with-subtasks` → ตรวจสอบ Story + Sub-tasks ทั้งหมด
> - `--fix` → auto-fix + batch format migration (แทน `/improve-issue` เดิม)

**Skill Location:** `.claude/skills/` (แต่ละ command = 1 skill directory)

**How Skill Commands Work:**

1. Load skill from `.claude/skills/[command-name]/SKILL.md` (e.g., `.claude/skills/create-story/SKILL.md`)
2. Execute phases in order (ห้ามข้ามขั้นตอน)
3. Reference `.claude/skills/shared-references/` for templates and tools

## Workflow Chain

```text
Stakeholder → PM → PO → TA → QA
              │     │     │     │
              ↓     ↓     ↓     ↓
           Epic   Story  Sub-tasks  Test Cases
              ↓     ↓     ↓     ↓
         [/verify-issue หลังสร้างเสร็จ]
```

Each role uses **Handoff Protocol** to pass context to next:

1. PM creates Epic → hands off to PO
2. PO creates User Stories → hands off to TA
3. TA creates Sub-tasks → hands off to QA
4. QA creates Test Plan + [QA] Sub-tasks (terminal)

## Service Tags

| Tag | Service | Local Path |
| --- | --- | --- |
| `[BE]` | Backend | `~/Codes/Works/tathep/tathep-platform-api` |
| `[FE-Admin]` | Admin | `~/Codes/Works/tathep/tathep-admin` |
| `[FE-Web]` | Website | `~/Codes/Works/tathep/tathep-website` |

## Passive Context (Always Loaded)

> **Design principle:** ข้อมูลด้านล่างนี้ compress จาก shared-references เพื่อให้ agent มี context พร้อมใช้ตลอด
> ไม่ต้อง load file เพิ่ม ลด latency + ลดโอกาสผิด (inspired by Vercel's AGENTS.md approach)
>
> **Full references:** โหลดเพิ่มเมื่อต้องการ template เต็ม → `.claude/skills/shared-references/`

### Tool Selection

> **IMPORTANT:** Jira descriptions ต้องใช้ ADF format via `acli --from-json` เสมอ (MCP แปลงเป็น wiki format ไม่สวย)

| Operation | Tool | Note |
| --- | --- | --- |
| **Create/Update Jira description** | `acli --from-json` (ADF) | สร้าง JSON file → `acli jira workitem create/edit` |
| **Update fields (ไม่ใช่ description)** | MCP `jira_update_issue` | summary, status, labels, etc. |
| **Read issue** | MCP `jira_get_issue` | **ต้องใช้ `fields` parameter เสมอ** ป้องกัน token limit |
| **Search Jira** | MCP `jira_search` | JQL query |
| **Confluence read** | MCP `confluence_get_page` | |
| **Confluence create/update (มี code)** | Python scripts | `.claude/skills/atlassian-scripts/scripts/` |
| **Confluence (move/macros)** | Python scripts | move, ToC, Children macros |

**jira_get_issue — ต้องระบุ fields:**

```python
# ❌ token limit error
jira_get_issue(issue_key="BEP-XXX")
# ✅ ระบุ fields
jira_get_issue(issue_key="BEP-XXX", fields="summary,status,description,issuetype,parent", comment_limit=5)
```

| Use Case | Fields |
| --- | --- |
| Quick check | `summary,status,assignee` |
| Read description | `summary,status,description` |
| Full analysis | `summary,status,description,issuetype,parent,labels` |

### ADF Quick Reference

**CREATE vs EDIT — JSON format ต่างกัน (ห้ามใช้สลับ!):**

| Operation | Required | Forbidden |
| --- | --- | --- |
| **CREATE** `acli jira workitem create` | `projectKey`, `type`, `summary`, `description` | `issues` |
| **EDIT** `acli jira workitem edit` | `issues`, `description` | `projectKey`, `type`, `summary`, `parent` |

```json
// CREATE
{"projectKey":"BEP","type":"Story","summary":"...","description":{"type":"doc","version":1,"content":[...]}}
// EDIT
{"issues":["BEP-XXX"],"description":{"type":"doc","version":1,"content":[...]}}
```

**Subtask — Two-Step Workflow** (acli ไม่รองรับ `parent` field):

1. MCP create shell: `jira_create_issue({project_key:"BEP", summary:"...", issue_type:"Subtask", additional_fields:{parent:{key:"BEP-XXX"}}})`
2. acli edit description: `acli jira workitem edit --from-json subtask.json --yes`

**Panel Types:**

| Type | Color | Usage |
| --- | --- | --- |
| `info` | Blue | Story narrative, objective |
| `success` | Green | Happy path AC |
| `warning` | Yellow | Edge cases, validation |
| `error` | Red | Error handling |
| `note` | Purple | Notes, dependencies |

**Table Header Colors (semantic):**

| Category | Hex |
| --- | --- |
| Default/header | `#f4f5f7` |
| New files | `#e3fcef` (green) |
| Modify files | `#fffae6` (yellow) |
| Delete files | `#ffebe6` (red) |
| Reference | `#eae6ff` (purple) |
| Requirements | `#deebff` (blue) |

**AC Format:** panels + Given/When/Then (ต้องมีเสมอ) → Happy=`success`, Edge=`warning`, Error=`error`

**Inline code:** `{"type":"text","text":"path/file.ts","marks":[{"type":"code"}]}`

### Common Mistakes & Quick Fixes

| Mistake | Fix |
| --- | --- |
| `unknown field "projectKey"` ใน edit | ใช้ CREATE format กับ EDIT → ลบ projectKey ใช้ `issues` แทน |
| `unknown field "issues"` ใน create | ใช้ EDIT format กับ CREATE → ลบ issues ใช้ `projectKey` แทน |
| `unknown field "parent"` | acli ไม่รองรับ parent → ใช้ Two-Step Workflow |
| Nested bulletList → `INVALID_INPUT` | listItem > bulletList ไม่ได้ → flatten หรือ comma-separated |
| Nested tables | Tables ซ้อน tables ไม่ได้ → ใช้ bullets แทน |
| Table inside panel | ❌ → ใช้ bulletList inside panel |
| Description ugly wiki format | ใช้ `acli --from-json` ไม่ใช่ MCP |
| Token limit exceeded | ใช้ `fields` parameter กับ `jira_get_issue` |
| Missing `version: 1` | ADF root ต้องมี `{"type":"doc","version":1,"content":[]}` |
| Code blocks ไม่ syntax highlight (Confluence) | Run `fix_confluence_code_blocks.py --page-id` หลัง MCP |
| Confluence macros เป็น text | ใช้ `update_page_storage.py` แทน MCP |

### Agent Decision Rules

> **หลักการ:** ยิ่งมี decision points น้อย ยิ่งลดโอกาสผิด — ทำให้ rules explicit ที่สุด

| Decision Point | Rule |
| --- | --- |
| **สร้าง Technical Note?** | สร้างเมื่อ: (1) มี architecture decisions, (2) มี code patterns ที่ซับซ้อน, (3) user บอกให้สร้าง → ถ้าไม่แน่ใจ ถาม user |
| **Confluence: MCP หรือ Script?** | มี code blocks/macros → Script เสมอ, ไม่มี → MCP ได้ |
| **ADF mapping ไม่ชัด?** | Flag "unclear mapping" → ห้ามเดา |
| **Issue type ไม่แน่ใจ?** | ถาม user → อย่าเดา type |
| **Scope ใหญ่เกินไป?** | Sub-task > 5 days → แนะนำ split, ไม่ auto-split |

> **Full references:** templates → `templates.md` | tools → `tools.md` | errors → `troubleshooting.md`

## File Structure

```text
.claude/skills/            # Skill commands (each dir = 1 slash command)
├── create-epic/           → /create-epic (5-phase PM workflow)
│   └── SKILL.md
├── create-story/          → /create-story (5-phase PO workflow)
│   └── SKILL.md
├── analyze-story/         → /analyze-story (7-phase TA workflow)
│   └── SKILL.md
├── create-testplan/       → /create-testplan (6-phase QA workflow)
│   └── SKILL.md
├── create-task/           → /create-task (5-phase task workflow)
│   └── SKILL.md
├── create-doc/            → /create-doc (4-phase Confluence workflow)
│   └── SKILL.md
├── update-doc/            → /update-doc (5-phase Confluence update)
│   └── SKILL.md
├── update-epic/           → /update-epic (5-phase update)
│   └── SKILL.md
├── update-story/          → /update-story (5-phase update)
│   └── SKILL.md
├── update-task/           → /update-task (5-phase update)
│   └── SKILL.md
├── update-subtask/        → /update-subtask (5-phase update)
│   └── SKILL.md
├── story-full/            → /story-full (10-phase composite) ⭐
│   └── SKILL.md
├── story-cascade/         → /story-cascade (8-phase cascade) ⭐
│   └── SKILL.md
├── sync-alignment/        → /sync-alignment (8-phase bidirectional sync) ⭐
│   └── SKILL.md
├── search-issues/         → /search-issues (3-phase search)
│   └── SKILL.md
├── verify-issue/          → /verify-issue (5-phase verify + fix)
│   └── SKILL.md
├── atlassian-scripts/    # Python scripts for Confluence + Jira via REST API
│   ├── SKILL.md
│   ├── lib/                             → Shared library (auth, API clients, exceptions)
│   └── scripts/
│       ├── create_confluence_page.py    → Create/update with code blocks
│       ├── update_confluence_page.py    → Find/replace text in Confluence
│       ├── move_confluence_page.py      → Move page(s) to new parent
│       ├── update_page_storage.py       → Add macros (ToC, Children)
│       ├── fix_confluence_code_blocks.py → Fix broken code blocks
│       ├── audit_confluence_pages.py    → Verify content alignment
│       └── update_jira_description.py   → Fix Jira descriptions (ADF)
└── shared-references/     # Shared resources for all skills
    ├── templates.md       → ADF core rules (CREATE/EDIT, panels, styling)
    ├── templates-epic.md  → Epic ADF template
    ├── templates-story.md → Story ADF template
    ├── templates-subtask.md → Sub-task + QA ADF template
    ├── templates-task.md  → Task ADF template (4 types)
    ├── writing-style.md   → Language guidelines
    ├── tools.md           → Tool selection guide
    ├── jql-quick-ref.md   → JQL patterns
    ├── troubleshooting.md → Error recovery
    └── verification-checklist.md → Quality checks

tasks/                     # Generated outputs (gitignored)
```

## References (load when needed)

| Need | File |
| --- | --- |
| All templates (ADF) | `.claude/skills/shared-references/templates.md` |
| Tool selection + effort sizing | `.claude/skills/shared-references/tools.md` |
| Quality checklists | `.claude/skills/shared-references/verification-checklist.md` |
| Writing style guide | `.claude/skills/shared-references/writing-style.md` |
| JQL patterns | `.claude/skills/shared-references/jql-quick-ref.md` |
| Troubleshooting | `.claude/skills/shared-references/troubleshooting.md` |
| Atlassian scripts | `.claude/skills/atlassian-scripts/SKILL.md` |

## Core Principles

1. **Phase-based workflows** - ทำตาม phases เรียงลำดับ ห้ามข้ามขั้นตอน
2. **Explore before design** - ต้อง explore codebase ก่อนสร้าง Sub-tasks เสมอ
3. **ADF via acli** - ใช้ `acli --from-json` สำหรับ Jira descriptions
4. **Thai + ทับศัพท์** - เนื้อหาภาษาไทย, technical terms ภาษาอังกฤษ
5. **Clear handoffs** - Each role passes structured context to next
6. **INVEST compliance** - All items pass INVEST criteria
7. **Traceability** - Everything links back to parent (Story→Epic, Sub-task→Story)

---

## ⚠️ Critical: Explore Codebase First

> **ไม่มี Explore = ไม่มี Design**
>
> ก่อนสร้าง Sub-tasks ต้อง explore codebase เสมอ ไม่งั้นจะออกแบบผิด

### Why Explore is Mandatory

| ถ้าไม่ Explore | ผลที่ตามมา |
| --- | --- |
| ไม่รู้ file paths จริง | Subtask มี path generic ไม่มีประโยชน์ |
| ไม่รู้ว่ามีอะไรอยู่แล้ว | สร้างงานซ้ำ, reinvent the wheel |
| ไม่รู้ patterns ที่ใช้ | Dev ต้องหาเอง หรือทำผิด convention |
| ไม่รู้ dependencies | ประเมิน scope ผิด, พัง existing features |

### TA Workflow (Correct Order)

```text
1. รับ User Story
2. Impact Analysis (คิดว่ากระทบ services ไหน)
3. 🔍 EXPLORE CODEBASE ← ห้ามข้าม!
   • หา actual file paths
   • ดู existing patterns
   • เช็คว่ามีอะไรอยู่แล้ว
   • เข้าใจ architecture
4. Design Sub-tasks (ด้วยข้อมูลจริง)
5. Create Sub-tasks
```

### How to Explore

| Service | Path | Tool |
| --- | --- | --- |
| Backend | `~/Codes/Works/tathep/tathep-platform-api` | Task (Explore agent) |
| Admin | `~/Codes/Works/tathep/tathep-admin` | Task (Explore agent) |
| Website | `~/Codes/Works/tathep/tathep-website` | Task (Explore agent) |

**Example prompts for Explore agent:**

- "Find credit top-up page and related components"
- "Find API endpoint for creating orders"
- "Find existing billing form patterns"

## Troubleshooting

> Quick fixes อยู่ใน **Passive Context > Common Mistakes & Quick Fixes** ด้านบน
> Full recovery procedures → `.claude/skills/shared-references/troubleshooting.md`

| Issue | Solution |
| --- | --- |
| Wrong project key | ใช้ `BEP` เสมอ |
| "Issue not found" | ตรวจ format: `BEP-XXX` |
| "Permission denied" | Re-authenticate MCP |
| Workflow interrupted | Note phase → search Jira → resume from last completed |
