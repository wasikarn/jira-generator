---
name: plan-sprint
disable-model-invocation: true
context: fork
description: |
  Sprint Planning using an 8-phase workflow

  Phases: Discovery → Capacity → Carry-over → Prioritize → Distribute → Risk → Review → Execute

  Triggers: "plan sprint", "sprint planning"
argument-hint: "[--sprint <id>] [--carry-over-only]"
---

# /plan-sprint

**Role:** Scrum Master + Sprint Planner
**Output:** Sprint plan with assignments executed in Jira

## Dynamic Context

- **Today:** !`date +%Y-%m-%d`
- **Recent commits:** !`git -C /Users/kobig/Codes/Works/tathep/tathep-platform-api log --oneline -5 2>/dev/null || echo "N/A"`

## Pre-Meeting Checklist

> See [Sprint Frameworks](../shared-references/sprint-frameworks.md) for full details

- [ ] **Timebox set:** 45 min × weeks (e.g., 2-week sprint = 90 min)
- [ ] **PO prepared:** Backlog refined, top items have ACs
- [ ] **Team prepared:** Capacity conflicts identified, carry-over updated
- [ ] **Sprint goal draft:** SMART format ready

## ⚠️ Critical: Capacity Before Assignment

> **Always calculate team capacity BEFORE assigning individual tasks.**
> This prevents over-committing sprints and ensures balanced workload distribution.

**Order of Operations:**

1. Calculate team velocity + individual productive hours (Phase 2)
2. Prioritize backlog items (Phase 4)
3. THEN assign to individuals using skill matrix (Phase 5)

**Anti-Pattern:** Assigning work to individuals first → leads to unbalanced sprints, burnout, missed commitments
**Anti-Pattern:** Using fixed "items/sprint" per person → ignores task complexity and skill fit

## Context Object (accumulated across phases)

| Phase | Adds to Context |
|-------|----------------|
| 1. Discovery | `source_sprint`, `target_sprint`, `sprint_items[]` |
| 2. Capacity | `capacity_table[]`, `available_slots[]` |
| 3. Carry-over | `carry_over_items[]`, `probability_scores[]` |
| 4. Prioritize | `prioritized_items[]`, `vs_validated` |
| 5. Distribute | `assignment_map[]`, `workload_table` |
| 6. Risk | `risk_flags[]`, `mitigations[]` |
| 7. Review | `approved_plan` |
| 8. Execute | `execution_log[]`, `assigned_keys[]` |

> **Workflow Patterns:** See [workflow-patterns.md](../shared-references/workflow-patterns.md) for Gate Levels (AUTO/REVIEW/ITERATE/APPROVAL), QG Scoring, Two-Step, and Explore patterns.

---

## Part A: Data Collection (Phases 1-2) — Execution Layer

> **Phase Tracking:** Use TodoWrite to mark each phase `in_progress` → `completed` as you work.

### 1. Sprint Discovery

Ask the user:

- Which target sprint? (if not specified → find the next future sprint)
- Which source sprint for carry-over? (if not specified → current active sprint)

```text
MCP: jira_get_sprint_issues(sprint_id="<source>", fields="summary,status,assignee,priority,issuetype,customfield_10016,timetracking,{{START_DATE_FIELD}},duedate")
MCP: jira_get_sprint_issues(sprint_id="<target>", fields="summary,status,assignee,priority,issuetype,customfield_10016,timetracking,{{START_DATE_FIELD}},duedate")
```

**Collect:**

- Source sprint: items + statuses + assignees (carry-over candidates)
- Target sprint: existing items (already planned)
- Sprint dates + goals

**🟡 REVIEW** — Present data summary to user. Proceed unless user objects.

### 2. Team Capacity

```text
Read: .claude/skills/shared-references/team-capacity.md
Read: .claude/project-config.json → team.members[], team.velocity
```

**Step 2a: Team Velocity (SP-based)**

```text
If velocity.story_points.avg_velocity exists:
  Sprint Capacity = avg_velocity × 0.8 (safety buffer)
Else (bootstrap phase):
  Sprint Capacity = avg_throughput_per_sprint (ticket count as proxy)

Also: sum(customfield_10016) of sprint stories → compare with Sprint Capacity to detect over-commitment
```

**Step 2b: Individual Productive Hours**

```text
Per person:
  Productive Hours = sprint_length_days × 8h × focus_factor - (leave_days × 8h × focus_factor)
  Review Load = count(reviewees) × review_cost.hours_per_junior_per_sprint  (from config)
  Already Assigned = sum(timetracking.originalEstimate) of current sprint subtasks (from Phase 1 data)
  Net Available = Productive Hours - Review Load - Already Assigned
```

> **Review Cost:** Tech Lead reviews 4 people (~15h/sprint), Senior reviews 2 (~4h/sprint).
> Read `team.review_cost` from project-config.json.

**Step 2c: Skill Profile + Complexity**

Read each member's `skill_profile` + `growth_tracks` + `bus_factor` from config.
Use **complexity-adjusted throughput** (from team-capacity.md) instead of raw throughput for item count limits.

**Output:** Capacity table

| Member | Role | Productive Hrs | Review Load | Net Available | Complexity-Adj Throughput |
| ------ | ---- | -------------- | ----------- | ------------- | ------------------------ |
| ...    | ...  | ...            | ...         | ...           | ...                      |

**🟡 REVIEW** — Present capacity table to user. Proceed unless user objects.

---

## Part B: Strategy Analysis (Phases 3-6)

> **Phase Tracking:** Use TodoWrite to mark each phase `in_progress` → `completed` as you work.
> **🟢 AUTO** — Phases 3-6 run via Task agent. All automated. Escalate only on incomplete data.

```text
Task(subagent_type: "general-purpose", prompt: """
You are a sprint planning strategist. Read and apply the frameworks from:
- .claude/skills/shared-references/sprint-frameworks.md (RICE, Impact/Effort, carry-over model)
- .claude/skills/shared-references/team-capacity.md (capacity model, skill matrix, focus factor, throughput)
- .claude/project-config.json → team.members[] (skill_profile, focus_factor, avg_throughput)

## Sprint Data
[Insert Phase 1 data: source sprint items, target sprint items, statuses, assignees]
[Insert Phase 2 data: capacity table with productive hours per person]

## Tasks
1. **Carry-over Analysis:** Calculate carry-over probability using the status-based model
2. **Prioritization:** Rank items using the Impact/Effort matrix (skip RICE if insufficient data)
3. **Workload Distribution:** Match items → team members using skill_profile match scores + hours capacity
4. **Risk Assessment:** Flag overloads (>95% utilization), skill gaps, dependencies, blockers

## Output Format
### Carry-over Summary
| Key | Summary | Status | Probability | Assignee | Est. Hours |
### Prioritized Items
| Priority | Key | Summary | Quadrant | Required Skill | Reason |
### Recommended Assignments
| Member | Productive Hrs | Carry-over Hrs | New Hrs | Total Hrs | Utilization% | Risk Flag |
### Risk Flags
| Risk | Severity | Mitigation |
""")
```

### 3. Carry-over Analysis

**Input:** Source sprint items with statuses
**Method:** Status-based probability model (from sprint-frameworks.md)

**Output:**

- Estimated carry-over count per person
- High-probability items (>80%) → auto-include in target sprint
- Medium-probability items (45-80%) → flag for user decision

### 4. Prioritization + Story Structure Validation

**Validate stories are vertical slices** (see [Sprint Frameworks](../shared-references/sprint-frameworks.md#vertical-slicing)):

- [ ] Each story delivers end-to-end user value (not just one layer)
- [ ] Shell-only stories reframed as Walking Skeleton
- [ ] VS labels assigned (`vs{N}-{name}`, `vs-enabler`, `{feature}-{scope}`)

**Input:** Target sprint items + new items to add
**Method:** Impact vs Effort matrix

**Output:**

- P1 (DO FIRST): High impact, low effort
- P2 (PLAN CAREFULLY): High impact, high effort
- P3 (QUICK WINS): Low impact, low effort
- P4 (DEFER): Low impact, high effort

### 5. Workload Distribution

**Input:** Prioritized items + team capacity (hours) + carry-over + skill profiles
**Method:** Skill matrix match → existing context → hours capacity check → grouping

**Assignment Algorithm:**

1. For each item, determine required skill area (from service tag: [BE]→backend, [FE-Admin]→frontend_admin, etc.)
2. Score each team member: `Match Score = skill_level × (1 + context_bonus)`
   - expert=1.0, intermediate=0.8, basic=0.6
   - context_bonus=0.2 if member has related carry-over items
3. Check hours capacity: `Available Hours ≥ Estimated Hours` for the item (read from `timetracking.originalEstimate` if set, else estimate from ADF panel)
4. Assign to highest score member with available capacity

**Rules:**

- Related items → same person (reduce context switching)
- Blockers → prioritize (unblock others)
- Critical path → expert-level skill match required
- Never exceed productive hours ceiling
- Track cumulative assigned hours vs available hours (not just item count)

**Output:** Assignment recommendation table with hours tracking

### 6. Risk Assessment

**Check:**

- [ ] No one exceeds capacity ceiling (utilization >95%)
- [ ] Dependencies identified
- [ ] Critical path items have an owner
- [ ] Junior devs have mentor support
- [ ] No one has >3 sticky carry-over items
- [ ] Bus factor areas covered (Video Processing, DevOps, Mobile → check if sole owner is overloaded or on leave)
- [ ] Review load validated (reviewer not >40% of productive hours on reviews)
- [ ] Cross-training opportunity flagged (if sprint items touch bus-factor=1 areas → suggest pairing)

**Output:** Risk flags with severity + mitigation

---

## Part C: Approval & Execution (Phases 7-8) — Execution Layer

> **Phase Tracking:** Use TodoWrite to mark each phase `in_progress` → `completed` as you work.

### 7. Sprint Plan Review ⚠️ GATE

Present the complete sprint plan to the user:

```text
## Sprint Plan: [Sprint Name]
📅 [Start Date] → [End Date]
🎯 Sprint Goal: [goal]
📊 Team Velocity: [X SP or Y tickets] (based on last 3-5 sprints)

### Team Workload (Hours-Based)
| Member | Role | Productive Hrs | Carry-over Hrs | New Hrs | Total Hrs | Utilization | Status |
| ... | ... | ... | ... | ... | ... | ...% | 🟢/⚠️/🔴 |

Status: 🟢 ≤80% | ⚠️ 80-95% | 🔴 >95%

### Items to Assign (sorted by Due Date ↑ then Priority ↑)
| # | Key | Summary | Assignee | Skill Match | Est. Hours | Due Date | Priority | Action |
| 1 | {{PROJECT_KEY}}-XXX | ... | Name | expert | 4h | Feb 10 | Highest | assign + move |

### Risk Summary
| Risk | Severity | Mitigation |

### Deferred Items (not included in this sprint)
| Key | Summary | Reason |
```

**🔄 ITERATE** — Present complete sprint plan as structured cards (workload per member, item assignments, risk flags). Ask: Approve / Annotate / Major rework.

- Annotate → user specifies items to reassign, adjust hours, swap priorities → revise ONLY annotated items → re-present (max 3 rounds)
- Approve → proceed to Execute Assignments
- Major rework → back to Prioritization (Phase 4)
- See [Annotation Cycle](../shared-references/workflow-patterns.md#annotation-cycle-iterate-gate)

### 8. Execute Assignments

> **🟢 AUTO** — If Phase 7 approved → execute all assignments automatically. Escalate only on failure.
> HR7: Sprint ID must be looked up dynamically. NEVER hardcode sprint IDs.

**Execution Order:** Sort items by due date (ascending) then priority (Highest→Low). This ensures critical early-due items are assigned first.

Execute according to the user-approved plan (in due date + priority order):

```text
# Move items to target sprint + set estimation fields (⚠️ sprint field = plain number, NOT object)
# Story/Task: set sprint + story_points + size + dates
MCP: jira_update_issue(issue_key="{{PROJECT_KEY}}-XXX", additional_fields={
  "{{SPRINT_FIELD}}": 123,
  "customfield_10016": 3,                        # Story Points
  "customfield_10107": {"value": "M"},            # Size
  "{{START_DATE_FIELD}}": "YYYY-MM-DD",              # Start Date
  "duedate": "YYYY-MM-DD"                         # Due Date
})

# Subtask: set original_estimate + dates (⚠️ HR10: NEVER set sprint on subtasks)
MCP: jira_update_issue(issue_key="{{PROJECT_KEY}}-YYY", additional_fields={
  "timetracking": {"originalEstimate": "4h"},     # Original Estimate
  "{{START_DATE_FIELD}}": "YYYY-MM-DD",              # Start Date
  "duedate": "YYYY-MM-DD"                         # Due Date
})

# Assign items (⚠️ MCP assignee silent fail — use acli instead)
Bash: acli jira workitem assign -k "{{PROJECT_KEY}}-XXX" -a "email@domain.com" -y
```

> ⚠️ Sprint field uses `{{SPRINT_FIELD}}` with plain number (e.g. `123`) — do not use `{"id": 123}`
> **🟢 AUTO** — HR3: NEVER set assignee via MCP. Use `acli jira workitem assign -k "KEY" -a "email" -y`.
> **🟢 AUTO** — HR6: `cache_invalidate(issue_key)` after EVERY sprint assignment.

**HR8 — Post-assignment alignment check (MANDATORY):**

```text
# After all assignments complete, run subtask alignment validation:
Bash: python3 scripts/sprint-subtask-alignment.py --sprint <target_sprint_id>

# Reviews: dates within parent range, missing OE, missing dates
# If violations found → run with --apply to auto-fix
# Then cache_invalidate(sprint_id=<id>) to refresh cache
```

> **🟢 AUTO** — Always run alignment check after Phase 8. This is the safety net for HR8.

**Output:**

```text
## Sprint Planning Complete ✅
Sprint: [Name] (ID: XXX)
Items assigned: XX
Team members: XX
Subtask alignment: [X checked, Y fixed]

### Execution Log (ordered by Due Date ↑ then Priority ↑)
| # | Key | Due | Priority | Action | Status |
| 1 | {{PROJECT_KEY}}-XXX | Feb 10 | Highest | Assigned to Name + moved to sprint | ✅ |

→ To verify: /verify-issue {{PROJECT_KEY}}-XXX
→ To update a story: /update-story {{PROJECT_KEY}}-XXX
```

---

## Options

| Flag | Description |
| ------ | ------------- |
| `--sprint <id>` | Specify target sprint ID (if not specified → find the next future sprint) |
| `--carry-over-only` | Carry-over analysis only (no assign/move) — Phase 1-3 only |

---

## References

- [Team Capacity](../shared-references/team-capacity.md) - Team roster, capacity model, skill mapping
- [Sprint Frameworks](../shared-references/sprint-frameworks.md) - RICE, Impact/Effort, carry-over model
- [Tool Selection](../shared-references/tools.md) - MCP vs acli decision rules
