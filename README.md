# Jira Generator

Agile Documentation System for **Tathep Platform** — Create Epics, User Stories, Sub-tasks, and plan Sprints via Claude Code

## Setup Guide

### Step 1: Install Claude Code

Install [Claude Code](https://claude.com/claude-code) — choose one method:

```bash
# CLI
npm install -g @anthropic-ai/claude-code

# Or use VSCode extension
# Search "Claude Code" in Extensions marketplace
```

### Step 2: Install Atlassian CLI (acli)

Used for creating/editing Jira descriptions in ADF (Atlassian Document Format)

```bash
# macOS (Homebrew)
brew install atlassian-cli

# Or download from https://bobswift.atlassian.net/wiki/spaces/ACLI/overview
```

Configure credentials:

```bash
acli jira login --server https://100-stars.atlassian.net --user <email> --token <api-token>
```

### Step 3: Configure MCP Servers

Add MCP servers to Claude Code settings (`~/.claude/settings.json` or VSCode settings):

**mcp-atlassian** — for Jira + Confluence:

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

> See full setup: [mcp-atlassian GitHub](https://github.com/sooperset/mcp-atlassian)

### Step 4: Configure Atlassian Credentials (for Python scripts)

Python scripts load credentials from `~/.config/atlassian/.env`:

```bash
mkdir -p ~/.config/atlassian
cat > ~/.config/atlassian/.env << 'EOF'
CONFLUENCE_URL=https://100-stars.atlassian.net/wiki
CONFLUENCE_USERNAME=<email>
CONFLUENCE_API_TOKEN=<api-token>
EOF
```

### Step 5: Install Python Dependencies

```bash
pip install requests
```

### Step 6: Run Setup Script

```bash
# Clone repo (if not already cloned)
git clone <repo-url> ~/Codes/Works/tathep/jira-generator
cd ~/Codes/Works/tathep/jira-generator

# Run setup (idempotent — safe to run multiple times)
./scripts/setup.sh
```

The setup script will:

1. Install `sync-tathep-skills` CLI to `~/.local/bin/`
2. Sync skills to `~/.claude/skills/` (via symlinks)
3. Add Tathep config to `~/.claude/CLAUDE.md`

> If `~/.local/bin` is not in your PATH, add it to your shell profile:
>
> ```bash
> export PATH="$HOME/.local/bin:$PATH"
> ```

### Step 7 (Optional): Install Tresor Agents

Required for `/plan-sprint` which uses Tresor strategy — install Product team agents:

```bash
# See details: https://github.com/alirezarezvani/claude-code-tresor
# Sprint-prioritizer agent will be installed at:
# ~/.claude/subagents/product/management/sprint-prioritizer/agent.md
```

### Verify Setup

```bash
# Check skills are synced
ls ~/.claude/skills/ | grep -E "create-story|plan-sprint|verify-issue"

# Check acli works
acli jira project list --server https://100-stars.atlassian.net

# Check MCP works — open Claude Code and type:
# "Fetch issue BEP-1"
```

### Sync Skills After Updates

When skills are added or removed from the project, re-run sync:

```bash
sync-tathep-skills
```

---

## Usage

Open Claude Code in this project and type `/command` as needed.

---

### Create Full Feature Workflow

```text
/story-full
```

Claude creates a complete User Story + Sub-tasks in one go — through 10 phases from Discovery to Verify.

**Example 1:** Type `/story-full` and say "Build a coupon system for admin — create, edit, delete coupons" → Claude asks for details, then auto-generates Story + Sub-tasks `[BE]`, `[FE-Admin]`

**Example 2:** Type `/story-full` and say "Users can view their transaction history on the website" → Generates Story + Sub-tasks `[BE]`, `[FE-Web]` with complete ACs

---

### Create Epic

```text
/create-epic
```

Creates an Epic + Epic Doc on Confluence — uses RICE scoring for prioritization.

**Example 1:** "Build a Coupon Management system — admin manages all coupon types" → Creates Epic with RICE score + Confluence doc

**Example 2:** "Create epic for Payment Gateway Integration — support PromptPay, credit card" → Creates Epic with scope, success metrics, RICE

---

### Create User Story

```text
/create-story
```

Creates a User Story from requirements — through 5-phase PO workflow.

**Example 1:** "Create a story for admin to create coupons, under Epic BEP-2800" → Story with ACs (Given/When/Then) linked to Epic

**Example 2:** "Story for users to view all orders on website — filter by status" → Story with ACs + scope + service tags

---

### Analyze Story → Sub-tasks

```text
/analyze-story BEP-XXX
```

Reads a Story then explores the codebase → creates Sub-tasks with real file paths.

**Example 1:** `/analyze-story BEP-2900` → Claude reads the story, explores Backend + Admin code, creates Sub-tasks `[BE] - Create Coupon API`, `[FE-Admin] - Build Coupon Management page`

**Example 2:** `/analyze-story BEP-3050` → Claude reads payment story, explores existing payment module, creates Sub-tasks referencing actual project files

---

### Create Test Plan

```text
/create-testplan BEP-XXX
```

Creates a Test Plan + [QA] Sub-tasks from a User Story.

**Example 1:** `/create-testplan BEP-2900` → Test cases: happy path (create coupon successfully), edge cases (duplicate name, expired date), error handling (server error)

**Example 2:** `/create-testplan BEP-3050` → Test cases for payment flow: successful payment, insufficient balance, timeout, concurrent transactions

---

### Create Task

```text
/create-task
```

Creates a Jira Task — supports 4 types: `tech-debt`, `bug`, `chore`, `spike`

**Example 1:** "Create a tech-debt task for refactoring payment module — separate service layer from controller" → Task type tech-debt with scope + ACs

**Example 2:** "Create a bug task — admin coupon list page loads too slowly, over 5 seconds" → Task type bug with steps to reproduce + expected behavior

---

### Create Confluence Doc

```text
/create-doc
```

Creates a Confluence page — supports: `tech-spec`, `adr`, `parent` (category page)

**Example 1:** "Create a tech-spec for coupon architecture — include ERD, API endpoints, sequence diagram" → Confluence page with tech-spec template

**Example 2:** "Create an ADR for choosing a payment gateway — compare Omise vs Stripe" → Confluence page with ADR (Architecture Decision Record) template

---

### Update Issue

```text
/update-story BEP-XXX
/update-epic BEP-XXX
/update-task BEP-XXX
/update-subtask BEP-XXX
```

Edit an existing issue — adjust scope, add ACs, migrate format.

**Example 1:** `/update-story BEP-2900` then say "Add AC for bulk create coupon — admin creates multiple coupons from CSV" → Claude updates Story with new AC

**Example 2:** `/update-subtask BEP-3100` then say "Change scope — use React Query instead of SWR" → Claude updates Sub-task with revised technical approach

---

### Update Story + Cascade to Sub-tasks

```text
/story-cascade BEP-XXX
```

Updates a Story then automatically cascades changes to related Sub-tasks.

**Example 1:** `/story-cascade BEP-2900` → "Change scope from single coupon to bulk create" → Story updates + Sub-tasks `[BE]`, `[FE-Admin]` adjust scope accordingly

**Example 2:** `/story-cascade BEP-3050` → "Add payment method: PromptPay" → Story + all payment-related Sub-tasks are updated

---

### Sync All Artifacts

```text
/sync-alignment BEP-XXX
```

Syncs Jira + Confluence bidirectional — Epic, Story, Sub-tasks, QA, Docs.

**Example 1:** `/sync-alignment BEP-2900` → Checks Story, Sub-tasks, Confluence tech-spec are aligned → finds Confluence not updated with new scope → updates it

**Example 2:** `/sync-alignment BEP-2800` → Syncs Epic with all child Stories → finds a new Story not in Epic doc → updates Confluence

---

### Sprint Planning

```text
/plan-sprint
/plan-sprint --sprint 640
/plan-sprint --carry-over-only
```

Sprint Planning powered by Tresor Strategy + Jira Execution — through 8 phases: Discovery → Capacity → Carry-over → Prioritize → Distribute → Risk → Review → Execute

**Example 1:** Type `/plan-sprint` → Claude will:

1. Fetch current sprint + target sprint data from Jira
2. Calculate each team member's capacity
3. Analyze carry-over items (based on status probability)
4. Prioritize items using Impact/Effort matrix
5. Match items → team members by skill + capacity
6. Check risks (overload, dependencies)
7. Present plan for review + approval
8. Execute: assign + move items in Jira

**Example 2:** `/plan-sprint --carry-over-only` → Analyzes only carry-over items from the current sprint → shows probability of each item finishing on time or carrying over, without making any assignments

Options:

- `--sprint 640` — specify target sprint ID
- `--carry-over-only` — analyze carry-over only, no assignments

---

### Search Issues

```text
/search-issues
```

Search for existing issues before creating new ones — prevents duplicates.

**Example 1:** "Find issues related to coupon" → Lists matching issues with status + assignee

**Example 2:** "Find bugs assigned to joakim in the current sprint" → Uses JQL filter to show bugs for a specific person + sprint

---

### Verify Issue Quality

```text
/verify-issue BEP-XXX
/verify-issue BEP-XXX --with-subtasks
/verify-issue BEP-XXX --fix
```

Checks ADF format, INVEST criteria, language, hierarchy alignment.

**Example 1:** `/verify-issue BEP-2900 --fix` → Checks Story, finds ACs missing Given/When/Then, all in English → auto-fixes to Thai + transliteration + adds Given/When/Then

**Example 2:** `/verify-issue BEP-2900 --with-subtasks` → Checks Story + all Sub-tasks → reports Sub-task #3 missing scope, Sub-task #5 missing ACs

Options:

- `--with-subtasks` — check all Sub-tasks as well
- `--fix` — auto-fix + format migration

---

### Update Confluence Doc

```text
/update-doc
```

Update or move a Confluence page.

**Example 1:** "Update the coupon tech-spec page to match the new design — add bulk create API" → Updates page content

**Example 2:** "Move page 'Coupon Tech Spec' under parent 'Payment Features'" → Moves page to new parent

---

### Optimize Context

```text
/optimize-context
/optimize-context --dry-run
```

Audits shared-references → compresses into passive context in CLAUDE.md.

**Example 1:** `/optimize-context --dry-run` → Shows report of which shared-references are outdated, which aren't compressed yet → no actual changes

**Example 2:** `/optimize-context` → Audits + compresses shared-references into CLAUDE.md passive context → reduces token usage for the agent

---

## Recommended Workflows

### Create a New Feature End-to-End

```text
/create-epic          → Create Epic
/story-full           → Create Story + Sub-tasks
/create-testplan      → Create Test Plan
/verify-issue BEP-XXX → Verify quality
```

### Plan a Sprint

```text
/plan-sprint          → Plan sprint (carry-over + assign)
```

### Edit + Sync

```text
/update-story BEP-XXX       → Edit Story
/story-cascade BEP-XXX      → Cascade to Sub-tasks
/sync-alignment BEP-XXX     → Sync everything
```

---

## Project Structure

```text
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

- **After creating/updating an issue:** Always run `/verify-issue` to check quality
- **Before creating a new issue:** Use `/search-issues` to prevent duplicates
- **Language:** Jira content is written in Thai + English transliteration for technical terms
- **Format:** Jira descriptions use ADF format (Claude handles this automatically)
- **Sync skills:** After adding/removing skills, run `sync-tathep-skills`
