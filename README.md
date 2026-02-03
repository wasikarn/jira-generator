# Jira Generator

Agile Documentation System สำหรับ **Tathep Platform** — สร้าง Epic, User Story, Sub-task และวางแผน Sprint ผ่าน Claude Code

## Setup Guide

### Step 1: ติดตั้ง Claude Code

ติดตั้ง [Claude Code](https://claude.com/claude-code) — เลือกวิธีใดวิธีหนึ่ง:

```bash
# CLI
npm install -g @anthropic-ai/claude-code

# หรือใช้ VSCode extension
# ค้นหา "Claude Code" ใน Extensions marketplace
```

### Step 2: ติดตั้ง Atlassian CLI (acli)

ใช้สำหรับสร้าง/แก้ไข Jira descriptions ในรูปแบบ ADF (Atlassian Document Format)

```bash
# macOS (Homebrew)
brew install atlassian-cli

# หรือดาวน์โหลดจาก https://bobswift.atlassian.net/wiki/spaces/ACLI/overview
```

ตั้งค่า credentials:

```bash
acli jira login --server https://100-stars.atlassian.net --user <email> --token <api-token>
```

### Step 3: ตั้งค่า MCP Servers

เพิ่ม MCP servers ใน Claude Code settings (`~/.claude/settings.json` หรือ VSCode settings):

**mcp-atlassian** — สำหรับ Jira + Confluence:

```json
{
  "mcpServers": {
    "mcp-atlassian": {
      "command": "uvx",
      "args": ["mcp-atlassian"],
      "env": {
        "JIRA_URL": "https://100-stars.atlassian.net",
        "JIRA_USERNAME": "<email>",
        "JIRA_API_TOKEN": "<api-token>",
        "CONFLUENCE_URL": "https://100-stars.atlassian.net/wiki",
        "CONFLUENCE_USERNAME": "<email>",
        "CONFLUENCE_API_TOKEN": "<api-token>"
      }
    }
  }
}
```

> ดู setup เพิ่มเติม: [mcp-atlassian GitHub](https://github.com/sooperset/mcp-atlassian)

### Step 4: ตั้งค่า Atlassian Credentials (สำหรับ Python scripts)

Python scripts ใช้ credentials จากไฟล์ `~/.config/atlassian/.env`:

```bash
mkdir -p ~/.config/atlassian
cat > ~/.config/atlassian/.env << 'EOF'
CONFLUENCE_URL=https://100-stars.atlassian.net/wiki
CONFLUENCE_USERNAME=<email>
CONFLUENCE_API_TOKEN=<api-token>
EOF
```

### Step 5: ติดตั้ง Python dependencies

```bash
pip install requests
```

### Step 6: รัน Setup Script

```bash
# Clone repo (ถ้ายังไม่มี)
git clone <repo-url> ~/Codes/Works/tathep/jira-generator
cd ~/Codes/Works/tathep/jira-generator

# รัน setup (idempotent — รันซ้ำได้ปลอดภัย)
./scripts/setup.sh
```

Setup script จะ:

1. ติดตั้ง `sync-tathep-skills` CLI ไปที่ `~/.local/bin/`
2. Sync skills ไป `~/.claude/skills/` (symlinks)
3. เพิ่ม Tathep config ใน `~/.claude/CLAUDE.md`

> ถ้า `~/.local/bin` ไม่อยู่ใน PATH ให้เพิ่มใน shell profile:
>
> ```bash
> export PATH="$HOME/.local/bin:$PATH"
> ```

### Step 7 (Optional): ติดตั้ง Tresor Agents

สำหรับ `/plan-sprint` ที่ใช้ Tresor strategy — ติดตั้ง Product team agents:

```bash
# ดูรายละเอียด: https://github.com/alirezarezvani/claude-code-tresor
# Sprint-prioritizer agent จะถูกติดตั้งที่:
# ~/.claude/subagents/product/management/sprint-prioritizer/agent.md
```

### ตรวจสอบว่า setup สำเร็จ

```bash
# ตรวจ skills ถูก sync
ls ~/.claude/skills/ | grep -E "create-story|plan-sprint|verify-issue"

# ตรวจ acli ใช้ได้
acli jira project list --server https://100-stars.atlassian.net

# ตรวจ MCP ใช้ได้ — เปิด Claude Code แล้วพิมพ์:
# "ดึง issue BEP-1 ให้หน่อย"
```

### Sync Skills หลังจาก update

เมื่อมีการเพิ่ม/ลบ skills ใน project ให้รัน sync ใหม่:

```bash
sync-tathep-skills
```

---

## วิธีใช้งาน

เปิด Claude Code ใน project นี้ แล้วพิมพ์ `/command` ตามต้องการ

---

### สร้าง Feature ใหม่ครบ workflow

```
/story-full
```

Claude จะสร้าง User Story + Sub-tasks ครบในครั้งเดียว — ผ่าน 10 phases ตั้งแต่ Discovery จนถึง Verify

**ตัวอย่างที่ 1:** พิมพ์ `/story-full` แล้วบอก "สร้างระบบ coupon สำหรับ admin — สร้าง, แก้ไข, ลบ coupon ได้" → Claude จะถามรายละเอียดเพิ่ม แล้วสร้าง Story + Sub-tasks `[BE]`, `[FE-Admin]` ให้อัตโนมัติ

**ตัวอย่างที่ 2:** พิมพ์ `/story-full` แล้วบอก "user สามารถดู transaction history ของตัวเองบนหน้า website" → ได้ Story + Sub-tasks `[BE]`, `[FE-Web]` พร้อม AC ครบ

---

### สร้าง Epic

```
/create-epic
```

สร้าง Epic + Epic Doc บน Confluence — ใช้ RICE scoring จัดลำดับ

**ตัวอย่างที่ 1:** "ต้องการระบบ Coupon Management — ให้ admin จัดการ coupon ทุกประเภท" → ได้ Epic พร้อม RICE score + Confluence doc

**ตัวอย่างที่ 2:** "สร้าง epic สำหรับ Payment Gateway Integration — รองรับ PromptPay, credit card" → ได้ Epic พร้อม scope, success metrics, RICE

---

### สร้าง User Story

```
/create-story
```

สร้าง User Story จาก requirements — ผ่าน 5-phase PO workflow

**ตัวอย่างที่ 1:** "สร้าง story สำหรับ admin สามารถสร้าง coupon ได้ ภายใต้ Epic BEP-2800" → ได้ Story พร้อม AC (Given/When/Then) link กับ Epic

**ตัวอย่างที่ 2:** "story สำหรับ user ดูรายการ order ทั้งหมดบน website — filter ตาม status ได้" → ได้ Story พร้อม AC + scope + service tags

---

### วิเคราะห์ Story → Sub-tasks

```
/analyze-story BEP-XXX
```

อ่าน Story แล้ว explore codebase → สร้าง Sub-tasks พร้อม file paths จริง

**ตัวอย่างที่ 1:** `/analyze-story BEP-2900` → Claude อ่าน story, explore code จาก Backend + Admin, สร้าง Sub-tasks `[BE] - สร้าง Coupon API`, `[FE-Admin] - สร้างหน้า Coupon Management`

**ตัวอย่างที่ 2:** `/analyze-story BEP-3050` → Claude อ่าน story เรื่อง payment, explore existing payment module, สร้าง Sub-tasks ที่ reference ไฟล์จริงในโปรเจค

---

### สร้าง Test Plan

```
/create-testplan BEP-XXX
```

สร้าง Test Plan + [QA] Sub-tasks จาก User Story

**ตัวอย่างที่ 1:** `/create-testplan BEP-2900` → ได้ test cases: happy path (สร้าง coupon สำเร็จ), edge cases (ชื่อซ้ำ, วันหมดอายุผ่านแล้ว), error handling (server error)

**ตัวอย่างที่ 2:** `/create-testplan BEP-3050` → ได้ test cases สำหรับ payment flow: successful payment, insufficient balance, timeout, concurrent transactions

---

### สร้าง Task

```
/create-task
```

สร้าง Jira Task — รองรับ 4 types: `tech-debt`, `bug`, `chore`, `spike`

**ตัวอย่างที่ 1:** "สร้าง tech-debt task สำหรับ refactor payment module — แยก service layer ออกจาก controller" → ได้ Task type tech-debt พร้อม scope + AC

**ตัวอย่างที่ 2:** "สร้าง bug task — หน้า admin coupon list โหลดช้ามาก เกิน 5 วินาที" → ได้ Task type bug พร้อม steps to reproduce + expected behavior

---

### สร้าง Confluence Doc

```
/create-doc
```

สร้าง Confluence page — รองรับ: `tech-spec`, `adr`, `parent` (category page)

**ตัวอย่างที่ 1:** "สร้าง tech-spec สำหรับ coupon architecture — ต้องมี ERD, API endpoints, sequence diagram" → ได้ Confluence page แบบ tech-spec พร้อม template

**ตัวอย่างที่ 2:** "สร้าง ADR สำหรับเลือก payment gateway — เปรียบเทียบ Omise vs Stripe" → ได้ Confluence page แบบ ADR (Architecture Decision Record)

---

### Update Issue

```
/update-story BEP-XXX
/update-epic BEP-XXX
/update-task BEP-XXX
/update-subtask BEP-XXX
```

แก้ไข issue ที่มีอยู่ — ปรับ scope, เพิ่ม AC, migrate format

**ตัวอย่างที่ 1:** `/update-story BEP-2900` แล้วบอกว่า "เพิ่ม AC สำหรับ bulk create coupon — admin สร้าง coupon ทีละหลายใบจาก CSV" → Claude update Story เพิ่ม AC ใหม่

**ตัวอย่างที่ 2:** `/update-subtask BEP-3100` แล้วบอกว่า "เปลี่ยน scope — ใช้ React Query แทน SWR" → Claude update Sub-task ปรับ technical approach

---

### Update Story + Cascade ไป Sub-tasks

```
/story-cascade BEP-XXX
```

Update Story แล้ว cascade changes ไปยัง Sub-tasks ที่เกี่ยวข้องอัตโนมัติ

**ตัวอย่างที่ 1:** `/story-cascade BEP-2900` → "เปลี่ยน scope จาก single coupon เป็น bulk create" → Story update + Sub-tasks `[BE]`, `[FE-Admin]` ปรับ scope ตาม

**ตัวอย่างที่ 2:** `/story-cascade BEP-3050` → "เพิ่ม payment method: PromptPay" → Story + Sub-tasks ที่เกี่ยวข้องกับ payment ถูก update ทั้งหมด

---

### Sync ทุก Artifacts

```
/sync-alignment BEP-XXX
```

Sync Jira + Confluence bidirectional — Epic, Story, Sub-tasks, QA, Docs ทั้งหมด

**ตัวอย่างที่ 1:** `/sync-alignment BEP-2900` → ตรวจว่า Story, Sub-tasks, Confluence tech-spec ตรงกัน → พบ Confluence ยังไม่ update scope ใหม่ → update ให้

**ตัวอย่างที่ 2:** `/sync-alignment BEP-2800` → sync Epic กับ Stories ทั้งหมดข้างใต้ → พบ Story ใหม่ที่ยังไม่อยู่ใน Epic doc → update Confluence

---

### วางแผน Sprint

```
/plan-sprint
/plan-sprint --sprint 640
/plan-sprint --carry-over-only
```

Sprint Planning ด้วย Tresor Strategy + Jira Execution — ผ่าน 8 phases: Discovery → Capacity → Carry-over → Prioritize → Distribute → Risk → Review → Execute

**ตัวอย่างที่ 1:** พิมพ์ `/plan-sprint` → Claude จะ:

1. ดึงข้อมูล sprint ปัจจุบัน + target sprint จาก Jira
2. คำนวณ capacity ของแต่ละคนในทีม
3. วิเคราะห์ carry-over items (ตาม status probability)
4. จัดลำดับ priority ด้วย Impact/Effort matrix
5. จับคู่ items → team members ตาม skill + capacity
6. ตรวจ risk (overload, dependencies)
7. แสดง plan ให้ review + approve
8. Execute: assign + move items ใน Jira

**ตัวอย่างที่ 2:** `/plan-sprint --carry-over-only` → วิเคราะห์เฉพาะ carry-over items จาก sprint ปัจจุบัน → แสดง probability ว่าแต่ละ item จะเสร็จทันหรือต้อง carry-over โดยไม่ assign อะไร

Options:

- `--sprint 640` — ระบุ target sprint ID
- `--carry-over-only` — วิเคราะห์ carry-over อย่างเดียว ไม่ assign

---

### ค้นหา Issue

```
/search-issues
```

ค้นหา issues ก่อนสร้างใหม่ — ป้องกันสร้างซ้ำ

**ตัวอย่างที่ 1:** "หา issues ที่เกี่ยวกับ coupon" → แสดงรายการ issues ที่ match พร้อม status + assignee

**ตัวอย่างที่ 2:** "หา bug ที่ assign ให้ joakim ใน sprint ปัจจุบัน" → ใช้ JQL filter แสดง bugs เฉพาะคน + sprint

---

### ตรวจสอบคุณภาพ Issue

```
/verify-issue BEP-XXX
/verify-issue BEP-XXX --with-subtasks
/verify-issue BEP-XXX --fix
```

ตรวจสอบ ADF format, INVEST criteria, ภาษา, hierarchy alignment

**ตัวอย่างที่ 1:** `/verify-issue BEP-2900 --fix` → ตรวจ Story พบ AC ไม่มี Given/When/Then, ภาษาอังกฤษทั้งหมด → auto-fix เป็น Thai + ทับศัพท์ + เพิ่ม Given/When/Then

**ตัวอย่างที่ 2:** `/verify-issue BEP-2900 --with-subtasks` → ตรวจ Story + Sub-tasks ทั้งหมด → report ว่า Sub-task #3 ไม่มี scope, Sub-task #5 ไม่มี AC

Options:

- `--with-subtasks` — ตรวจ Sub-tasks ทั้งหมดด้วย
- `--fix` — auto-fix + format migration

---

### Update Confluence Doc

```
/update-doc
```

Update หรือ move Confluence page

**ตัวอย่างที่ 1:** "update tech-spec page ของ coupon ให้ตรงกับ design ใหม่ — เพิ่ม bulk create API" → update เนื้อหา page

**ตัวอย่างที่ 2:** "ย้าย page 'Coupon Tech Spec' ไปอยู่ภายใต้ parent 'Payment Features'" → move page ไป parent ใหม่

---

### Optimize Context

```
/optimize-context
/optimize-context --dry-run
```

Audit shared-references → compress ลง passive context ใน CLAUDE.md

**ตัวอย่างที่ 1:** `/optimize-context --dry-run` → ดู report ว่า shared-references ตัวไหน outdated, ตัวไหนยังไม่ compress → ไม่แก้ไขจริง

**ตัวอย่างที่ 2:** `/optimize-context` → audit + compress shared-references ลง CLAUDE.md passive context → ลด token usage สำหรับ agent

---

## Workflow แนะนำ

### สร้าง Feature ใหม่ตั้งแต่ต้น

```
/create-epic          → สร้าง Epic
/story-full           → สร้าง Story + Sub-tasks ครบ
/create-testplan      → สร้าง Test Plan
/verify-issue BEP-XXX → ตรวจสอบคุณภาพ
```

### Sprint Planning

```
/plan-sprint          → วางแผน sprint (carry-over + assign)
```

### แก้ไข + Sync

```
/update-story BEP-XXX       → แก้ Story
/story-cascade BEP-XXX      → Cascade ไป Sub-tasks
/sync-alignment BEP-XXX     → Sync ทั้งหมด
```

---

## Project Structure

```
.claude/skills/              <- Skill definitions (1 dir = 1 command)
├── create-{epic,story,task,doc,testplan}/
├── update-{epic,story,task,subtask,doc}/
├── analyze-story/
├── story-full/              <- Composite workflows
├── story-cascade/
├── sync-alignment/
├── plan-sprint/
├── search-issues/
├── verify-issue/
├── optimize-context/
├── atlassian-scripts/       <- Python REST API scripts
│   ├── lib/                 <- auth, api, converters
│   └── scripts/             <- 7 utility scripts
└── shared-references/       <- Templates, style guide, checklists
    ├── templates.md
    ├── tools.md
    ├── writing-style.md
    ├── team-capacity.md
    ├── sprint-frameworks.md
    └── ...

scripts/
├── setup.sh                 <- Setup script (idempotent)
└── sync-tathep-skills       <- Sync skills to ~/.claude/skills/

tasks/                       <- Generated outputs (gitignored)
CLAUDE.md                    <- Agent instructions (passive context)
README.md                    <- This file
```

## Tips

- **หลังสร้าง/update issue:** ใช้ `/verify-issue` ตรวจสอบคุณภาพเสมอ
- **ก่อนสร้าง issue ใหม่:** ใช้ `/search-issues` ป้องกันสร้างซ้ำ
- **ภาษา:** เนื้อหาใน Jira เป็นภาษาไทย + ทับศัพท์ technical terms
- **Format:** Jira descriptions ใช้ ADF format (Claude จัดการให้อัตโนมัติ)
- **Sync skills:** หลังเพิ่ม/ลบ skills ให้รัน `sync-tathep-skills`
