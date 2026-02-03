---
name: plan-sprint
description: |
  Sprint Planning with Tresor Strategy + Jira Execution using an 8-phase workflow

  Phases: Discovery → Capacity → Carry-over → Prioritize → Distribute → Risk → Review → Execute

  ⭐ Hybrid: Tresor sprint-prioritizer handles strategy (Phase 3-6) + MCP handles execution (Phase 1,2,8)
  🔗 Tresor Agent: ~/.claude/subagents/product/management/sprint-prioritizer/agent.md

  Triggers: "plan sprint", "sprint planning"
argument-hint: "[--sprint <id>] [--carry-over-only]"
---

# /plan-sprint

**Role:** Scrum Master + Sprint Planner (Tresor-powered)
**Output:** Sprint plan with assignments executed in Jira

## Part A: Data Collection (Phases 1-2) — Execution Layer

### 1. Sprint Discovery

Ask the user:

- Which target sprint? (if not specified → find the next future sprint)
- Which source sprint for carry-over? (if not specified → current active sprint)

```text
MCP: jira_get_sprint_issues(sprint_id="<source>", fields="summary,status,assignee,priority,issuetype")
MCP: jira_get_sprint_issues(sprint_id="<target>", fields="summary,status,assignee,priority,issuetype")
```

**Collect:**

- Source sprint: items + statuses + assignees (carry-over candidates)
- Target sprint: existing items (already planned)
- Sprint dates + goals

**Gate:** Data collected — show summary for user confirmation

### 2. Team Capacity

```text
Read: .claude/skills/shared-references/team-capacity.md
```

**Calculate per person:**

- Max capacity (items/sprint from budget)
- Already assigned (target sprint items)
- Available slots = max - already assigned

**Output:** Capacity table

| Member | Role | Budget | Assigned | Available |
|--------|------|--------|----------|-----------|
| ... | ... | ... | ... | ... |

**Gate:** Capacity numbers confirmed

---

## Part B: Strategy Analysis (Phases 3-6) — Tresor Layer

> Phases 3-6 delegate to Tresor sprint-prioritizer via Task agent
> Agent reads: team-capacity.md + sprint-frameworks.md + sprint data from Phase 1

```text
Task(subagent_type: "general-purpose", prompt: """
You are a sprint planning strategist. Read and apply the frameworks from:
- .claude/skills/shared-references/sprint-frameworks.md (RICE, Impact/Effort, carry-over model)
- .claude/skills/shared-references/team-capacity.md (team roster, capacity, skill mapping)

Also reference Tresor sprint-prioritizer methodology from:
- ~/.claude/subagents/product/management/sprint-prioritizer/agent.md

## Sprint Data
[Insert Phase 1 data: source sprint items, target sprint items, statuses, assignees]

## Tasks
1. **Carry-over Analysis:** Calculate carry-over probability using the status-based model
2. **Prioritization:** Rank items using the Impact/Effort matrix (skip RICE if insufficient data)
3. **Workload Distribution:** Match items → team members based on skill match + capacity
4. **Risk Assessment:** Flag overloads, dependencies, blockers

## Output Format
### Carry-over Summary
| Key | Summary | Status | Probability | Assignee |
### Prioritized Items
| Priority | Key | Summary | Quadrant | Reason |
### Recommended Assignments
| Member | Carry-over | New | Total | Budget | Risk Flag |
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

### 4. Prioritization

**Input:** Target sprint items + new items to add
**Method:** Impact vs Effort matrix

**Output:**

- P1 (DO FIRST): High impact, low effort
- P2 (PLAN CAREFULLY): High impact, high effort
- P3 (QUICK WINS): Low impact, low effort
- P4 (DEFER): Low impact, high effort

### 5. Workload Distribution

**Input:** Prioritized items + team capacity + carry-over
**Method:** Skill match → existing context → capacity check → grouping

**Rules:**

- Related items → same person (reduce context switching)
- Blockers → prioritize (unblock others)
- Critical path → senior/lead
- Never exceed capacity ceiling

**Output:** Assignment recommendation table

### 6. Risk Assessment

**Check:**

- [ ] No one exceeds capacity ceiling
- [ ] Dependencies identified
- [ ] Critical path items have an owner
- [ ] Junior devs have mentor support
- [ ] No one has >3 sticky carry-over items

**Output:** Risk flags with severity + mitigation

---

## Part C: Approval & Execution (Phases 7-8) — Execution Layer

### 7. Sprint Plan Review ⚠️ GATE

Present the complete sprint plan to the user:

```text
## Sprint Plan: [Sprint Name]
📅 [Start Date] → [End Date]
🎯 Sprint Goal: [goal]

### Team Workload
| Member | Carry-over | New | Total | Budget | Status |
| ... | ... | ... | ... | ... | 🟢/⚠️/🔴 |

### Items to Assign
| # | Key | Summary | Assignee | Priority | Action |
| 1 | BEP-XXX | ... | Name | P1 | assign + move |

### Risk Summary
| Risk | Severity | Mitigation |

### Deferred Items (not included in this sprint)
| Key | Summary | Reason |
```

**Gate:** User approves the plan (may adjust assignments before approving)

### 8. Execute Assignments

Execute according to the user-approved plan:

```text
# Move items to target sprint
MCP: jira_update_issue(issue_key="BEP-XXX", additional_fields={"sprint": <target_sprint_id>})

# Assign items
MCP: jira_update_issue(issue_key="BEP-XXX", fields={"assignee": "Display Name"})
```

**Output:**

```text
## Sprint Planning Complete ✅
Sprint: [Name] (ID: XXX)
Items assigned: XX
Team members: XX

### Execution Log
| # | Key | Action | Status |
| 1 | BEP-XXX | Assigned to Name + moved to sprint | ✅ |

→ To verify: /verify-issue BEP-XXX
→ To update a story: /update-story BEP-XXX
```

---

## Options

| Flag | Description |
|------|-------------|
| `--sprint <id>` | Specify target sprint ID (if not specified → find the next future sprint) |
| `--carry-over-only` | Carry-over analysis only (no assign/move) — Phase 1-3 only |

---

## References

- [Team Capacity](../shared-references/team-capacity.md) - Team roster, capacity model, skill mapping
- [Sprint Frameworks](../shared-references/sprint-frameworks.md) - RICE, Impact/Effort, carry-over model
- [Tresor Sprint Prioritizer](~/.claude/subagents/product/management/sprint-prioritizer/agent.md) - Strategy methodology
- [Tool Selection](../shared-references/tools.md) - MCP vs acli decision rules
