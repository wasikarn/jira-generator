# Jira Generator

Agile Documentation System for **Tathep Platform** — Create Epics, User Stories, Sub-tasks, and plan Sprints via Claude Code skills.

## Architecture

```text
Claude Code ──skills──> acli (ADF JSON) ──> Jira Cloud
    │                                         ↑
    ├──MCP──> mcp-atlassian ─────────────────┘
    │                                   ↑
    ├──MCP──> jira-cache-server ───SQLite+FTS5 (local cache)
    │                              └─> Jira REST API v3
    ├──MCP──> Confluence, Figma, GitHub
    │
    ├──Python──> atlassian-scripts/lib/ (REST API)
    │
    └──subagents──> Tresor Teams (133 agents: product, eng, core, design)
```

**Key design decisions:**

- **Descriptions** always via `acli --from-json` (ADF format) — MCP produces ugly output
- **Fields** (assignee, sprint, labels) via MCP `jira_update_issue`
- **Sub-tasks** use two-step: MCP create (with parent) → acli edit (description)
- **Heavy ML deps** (PyTorch, sentence-transformers) isolated in venv outside project tree

## Prerequisites

| Tool | Purpose | Install |
| ---- | ------- | ------- |
| [Claude Code](https://claude.com/claude-code) | AI agent runtime | `npm i -g @anthropic-ai/claude-code` or VSCode extension |
| [acli](https://bobswift.atlassian.net/wiki/spaces/ACLI/overview) | Jira ADF descriptions | `brew install atlassian-cli` |
| [mcp-atlassian](https://github.com/sooperset/mcp-atlassian) | Jira/Confluence MCP | `uvx mcp-atlassian` (auto-installed) |
| Python 3.x | REST API scripts | Pre-installed on macOS |

## Setup

### 1. Configure acli

```bash
acli jira login --server https://100-stars.atlassian.net --user <email> --token <api-token>
```

### 2. Configure MCP Servers

Add to Claude Code settings (`~/.claude/settings.json` or VSCode settings):

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

### 3. Configure Atlassian Credentials (Python scripts)

Python scripts (`atlassian-scripts/`) load credentials from `~/.config/atlassian/.env`:

```bash
mkdir -p ~/.config/atlassian
cat > ~/.config/atlassian/.env << 'EOF'
CONFLUENCE_URL=https://100-stars.atlassian.net/wiki
CONFLUENCE_USERNAME=<email>
CONFLUENCE_API_TOKEN=<api-token>
JIRA_URL=https://100-stars.atlassian.net
JIRA_USERNAME=<email>
JIRA_API_TOKEN=<api-token>
EOF
```

### 4. Run Setup Script

```bash
git clone <repo-url> ~/Codes/Works/tathep/jira-generator
cd ~/Codes/Works/tathep/jira-generator

# Idempotent — safe to run multiple times
./scripts/setup.sh
```

This will:

1. Install `sync-tathep-skills` CLI to `~/.local/bin/`
2. Sync skills to `~/.claude/skills/` (via symlinks)
3. Add Tathep config to `~/.claude/CLAUDE.md`

> If `~/.local/bin` is not in your PATH: `export PATH="$HOME/.local/bin:$PATH"`

### 5. Setup Jira Cache Server (Optional)

Local SQLite cache for Jira data — reduces token consumption by 80-90% for repeated queries.

```bash
# Create venv in cache directory (not in project tree)
python3 -m venv ~/.cache/jira-generator/jira-cache-server/.venv
source ~/.cache/jira-generator/jira-cache-server/.venv/bin/activate
pip install -r .claude/skills/jira-cache-server/requirements.txt
```

Then add to MCP settings:

```json
{
  "mcpServers": {
    "jira-cache-server": {
      "command": "~/.cache/jira-generator/jira-cache-server/.venv/bin/python",
      "args": [".claude/skills/jira-cache-server/server.py"]
    }
  }
}
```

### 6. Install Tresor Agents (Recommended)

133 specialized subagents for cross-team review and collaboration at each workflow stage.

| Team | Key Agents | Used In |
| ---- | ---------- | ------- |
| Product (9) | `sprint-prioritizer`, `product-manager` | Sprint planning, Epic creation |
| Engineering (54) | `backend-architect`, `frontend-developer` | Story analysis, Technical review |
| Core (8) | `test-engineer`, `security-auditor` | Test plans, Security review |
| Design (7) | `ui-ux-analyst` | UI story review |

**Full install:**

```bash
git clone https://github.com/alirezarezvani/claude-code-tresor ~/.claude/subagents
cd ~/.claude/subagents && ./scripts/install.sh
```

**Minimum for Jira workflow:**

```bash
cd ~/.claude/subagents
./scripts/install.sh --category product     # sprint-prioritizer, product-manager
./scripts/install.sh --core                 # test-engineer, security-auditor
./scripts/install.sh --category engineering # backend-architect
```

Agents are auto-invoked per `shared-references/skill-orchestration.md` orchestration rules.

### Verify Setup

```bash
# Check skills synced
ls ~/.claude/skills/ | grep -E "create-story|plan-sprint|verify-issue"

# Check acli
acli jira project list --server https://100-stars.atlassian.net

# Check MCP — open Claude Code and type: "Fetch issue BEP-1"
```

### Sync Skills After Updates

```bash
sync-tathep-skills
```

---

## Commands

Open Claude Code in this project and type `/command`.

### Issue Creation

| Command | Description |
| ------- | ----------- |
| `/story-full` | Create Story + Sub-tasks in one go (PO + TA combined) |
| `/create-epic` | Create Epic + Confluence Epic Doc with RICE scoring |
| `/create-story` | Create User Story from requirements (5-phase PO workflow) |
| `/create-task` | Create Task: `tech-debt`, `bug`, `chore`, or `spike` |
| `/analyze-story BEP-XXX` | Read Story → explore codebase → create Sub-tasks |
| `/create-testplan BEP-XXX` | Create Test Plan + [QA] Sub-tasks from Story |

### Issue Updates

| Command | Description |
| ------- | ----------- |
| `/update-story BEP-XXX` | Edit Story — add/edit ACs, scope |
| `/update-epic BEP-XXX` | Edit Epic — adjust scope, RICE, metrics |
| `/update-task BEP-XXX` | Edit Task — migrate format, add details |
| `/update-subtask BEP-XXX` | Edit Sub-task — format, content |
| `/story-cascade BEP-XXX` | Update Story + cascade to all Sub-tasks |

### Sync & Quality

| Command | Description |
| ------- | ----------- |
| `/sync-alignment BEP-XXX` | Sync all artifacts bidirectional (Jira + Confluence) |
| `/verify-issue BEP-XXX` | Check ADF format, INVEST criteria, language |
| `/search-issues` | Search before creating (prevent duplicates) |

`/verify-issue` flags: `--with-subtasks` (batch check), `--fix` (auto-fix), `--dry-run` (report only)

### Planning & Analysis

| Command | Description |
| ------- | ----------- |
| `/plan-sprint` | Sprint planning: carry-over + capacity + assign |
| `/dependency-chain` | Dependency graph, critical path, swim lanes |
| `/activity-report` | Generate work activity report from claude-mem |

`/plan-sprint` options: `--sprint 640` (target sprint), `--carry-over-only` (analysis only)

### Documentation

| Command | Description |
| ------- | ----------- |
| `/create-doc` | Create Confluence page: `tech-spec`, `adr`, `parent` |
| `/update-doc` | Update or move a Confluence page |
| `/optimize-context` | Audit + compress CLAUDE.md passive context |

---

## Usage Examples

### Create a Full Feature (End-to-End)

```text
/search-issues          → Check no duplicates exist
/create-epic            → Create Epic + Confluence doc
/story-full             → Create Story + Sub-tasks in one go
/create-testplan        → Create [QA] Sub-tasks (optional)
/verify-issue BEP-XXX  → Verify quality
```

**Example:** `/story-full` → "Build a coupon system for admin — create, edit, delete coupons" → Claude asks for details, then auto-generates Story + Sub-tasks `[BE]`, `[FE-Admin]`

### Plan a Sprint

```text
/plan-sprint            → 8 phases: Discovery → Capacity → Carry-over →
                          Prioritize → Distribute → Risk → Review → Execute
```

Claude will fetch sprint data, calculate capacity, analyze carry-over, prioritize items, match to team members, check risks, present plan for approval, then execute assignments in Jira.

### Update + Cascade Changes

```text
/update-story BEP-XXX       → Edit Story only
/story-cascade BEP-XXX      → + cascade to Sub-tasks
/sync-alignment BEP-XXX     → + sync Confluence docs
```

### Analyze Dependencies

```text
/dependency-chain            → Build dependency graph from sprint
                               Identify critical path + parallel execution plan
                               Generate Mermaid diagrams + swim lanes per member
```

---

## Project Structure

```text
.claude/skills/                     <- Skill definitions (1 dir = 1 command)
├── create-{epic,story,task,doc,testplan}/
├── update-{epic,story,task,subtask,doc}/
├── analyze-story/
├── story-full/                     <- Composite: PO + TA in one workflow
├── story-cascade/                  <- Update + cascade to sub-tasks
├── sync-alignment/                 <- Bidirectional sync (Jira + Confluence)
├── plan-sprint/                    <- Tresor strategy + Jira execution
├── dependency-chain/               <- Critical path + swim lane analysis
├── search-issues/
├── verify-issue/
├── optimize-context/
├── activity-report/                <- claude-mem activity report generator
├── jira-cache-server/              <- MCP server: local Jira cache (SQLite+FTS5)
│   ├── server.py                   <- MCP entry point + 8 tool handlers
│   └── jira_cache/                 <- cache.py + embeddings.py
├── atlassian-scripts/              <- Python REST API scripts
│   ├── lib/                        <- auth, jira_api, converters, exceptions
│   └── scripts/                    <- 7 utility scripts
└── shared-references/              <- Reusable docs loaded by skills (16 files)
    ├── templates.md                <- All ADF templates (Epic, Story, Sub-task, Task)
    ├── dependency-frameworks.md    <- CPM, swim lane rules, risk scoring
    ├── tools.md                    <- Tool selection guide
    ├── writing-style.md            <- Thai + transliteration rules
    ├── verification-checklist.md   <- INVEST + quality scoring
    ├── troubleshooting.md          <- MCP errors, acli, ADF, Confluence fixes
    └── ...                         <- 12 more reference docs

scripts/
├── setup.sh                        <- Setup script (idempotent)
├── configure-project.py            <- Portable config (clone to other projects)
├── fix-table-format.py             <- Markdown table formatter
├── update-sprint-goals.py          <- Sprint goals updater
└── sync-tathep-skills              <- Sync skills to ~/.claude/skills/

tasks/                              <- Generated ADF JSON outputs (gitignored)
CLAUDE.md                           <- Agent instructions (passive context)
```

> **Note:** jira-cache-server venv is stored at `~/.cache/jira-generator/jira-cache-server/.venv/` (not in project tree) to keep the repo lightweight (~643MB of ML dependencies).

## Cloning to Another Project

This system is portable — update config and re-apply:

```bash
# 1. Edit project config
vi .claude/project-config.json
# → Update: jira.site, jira.project_key, team.members, services.tags

# 2. Revert current placeholders
python scripts/configure-project.py --revert --apply

# 3. Apply new config values
python scripts/configure-project.py --apply
```

See `.claude/project-config.json` for full team, services, and environment settings.

## Tips

- **Always search first:** `/search-issues` before creating to prevent duplicates
- **Always verify after:** `/verify-issue BEP-XXX` after creating/updating
- **Language:** Thai + English transliteration for technical terms (endpoint, API, component)
- **Format:** Jira descriptions use ADF format — Claude handles this via `acli --from-json`
- **Codebase first:** `/analyze-story` always explores codebase before creating Sub-tasks
- **Sync skills:** After adding/removing skills, run `sync-tathep-skills`
- **Cache server:** Use `cache_sprint_issues` before sprint planning for 80%+ token savings
- **Tresor teams:** Install subagents for auto-review at each workflow stage (see Setup step 6)
