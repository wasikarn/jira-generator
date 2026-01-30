#!/bin/bash
# Setup jira-generator: skills, CLI tools, and global Claude config
# Safe to run multiple times (idempotent)

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== jira-generator setup ==="
echo "Project: $PROJECT_DIR"
echo ""

# --- 1. Install sync-tathep-skills CLI ---
echo "[1/3] Installing sync-tathep-skills CLI..."
mkdir -p "$HOME/.local/bin"

SYNC_SRC="$SCRIPT_DIR/sync-tathep-skills"
SYNC_DST="$HOME/.local/bin/sync-tathep-skills"

if [ -L "$SYNC_DST" ]; then
  existing=$(readlink "$SYNC_DST")
  if [ "$existing" = "$SYNC_SRC" ]; then
    echo "  already installed"
  else
    rm "$SYNC_DST"
    ln -s "$SYNC_SRC" "$SYNC_DST"
    echo "  updated (was: $existing)"
  fi
elif [ -f "$SYNC_DST" ]; then
  rm "$SYNC_DST"
  ln -s "$SYNC_SRC" "$SYNC_DST"
  echo "  replaced file with symlink"
else
  ln -s "$SYNC_SRC" "$SYNC_DST"
  echo "  installed"
fi

# --- 2. Sync skills to ~/.claude/skills/ ---
echo ""
echo "[2/3] Syncing skills to ~/.claude/skills/..."
"$SYNC_SRC"

# --- 3. Add Tathep config to ~/.claude/CLAUDE.md ---
echo ""
echo "[3/3] Configuring ~/.claude/CLAUDE.md..."
mkdir -p "$HOME/.claude"
CLAUDE_MD="$HOME/.claude/CLAUDE.md"

if [ -f "$CLAUDE_MD" ] && grep -q "Tathep Atlassian Settings" "$CLAUDE_MD"; then
  echo "  Tathep settings already present"
else
  # Append Tathep config block
  cat >> "$CLAUDE_MD" << 'TATHEP_CONFIG'

## Tathep Atlassian Settings

| Setting | Value |
| --- | --- |
| Jira Site | `100-stars.atlassian.net` |
| Project Key | `BEP` |
| Confluence Space | `BEP` |

### Service Tags

| Tag | Service | Path |
| --- | --- | --- |
| `[BE]` | Backend | `~/Codes/Works/tathep/tathep-platform-api` |
| `[FE-Admin]` | Admin | `~/Codes/Works/tathep/tathep-admin` |
| `[FE-Web]` | Website | `~/Codes/Works/tathep/tathep-website` |
| `[Video]` | Video Processing | `~/Codes/Works/tathep/tathep-video-processing` |
| `[Player]` | Vision Player | `~/Codes/Works/tathep/bd-vision-player` |
| `[Jira-Gen]` | Jira Generator | `~/Codes/Works/tathep/jira-generator` |

## Tathep Development Workflow

### เมื่อ user อ้างถึง Jira issue (BEP-XXX)

**ก่อน implement:**
1. อ่าน issue ด้วย MCP `jira_get_issue` — เข้าใจ AC, scope, technical notes
2. ถ้ามี sub-tasks ให้อ่านด้วยเพื่อดู implementation details

**หลัง implement เสร็จ:**
1. Add comment ใน Jira ด้วย MCP `jira_add_comment` สรุป:
   - สิ่งที่ implement/เปลี่ยนแปลง
   - Files ที่แก้ไข
   - สิ่งที่เบี่ยงเบนจาก AC (ถ้ามี)

### Code Review

เมื่อ review code ที่เกี่ยวกับ Jira issue:
1. อ่าน issue ก่อน — เทียบ implementation กับ AC
2. ตรวจว่าทุก AC ถูก address ในโค้ด
3. Flag gaps ระหว่างโค้ดกับ requirements

### Confluence Updates

Update Confluence เมื่อ implementation กระทบ:
- Architecture decisions
- API contracts / data models
- Technical specifications

### Daily Ops Tool Selection

| Operation | Tool |
| --- | --- |
| Read issue | MCP `jira_get_issue` |
| Search issues | MCP `jira_search` |
| Add comment | MCP `jira_add_comment` |
| Update issue fields | MCP `jira_update_issue` |
| Read Confluence | MCP `confluence_get_page` |
| Update Confluence | MCP `confluence_update_page` |
| Complex formatting | `/atlassian-scripts` |
| Create/manage issues | Skill commands (`/create-story`, `/verify-issue`, etc.) |
TATHEP_CONFIG
  echo "  added Tathep settings and workflow"
fi

# --- Check PATH ---
echo ""
if echo "$PATH" | tr ':' '\n' | grep -q "$HOME/.local/bin"; then
  echo "=== Setup complete ==="
else
  echo "=== Setup complete ==="
  echo ""
  echo "WARNING: ~/.local/bin is not in PATH. Add to your shell profile:"
  echo '  export PATH="$HOME/.local/bin:$PATH"'
fi
