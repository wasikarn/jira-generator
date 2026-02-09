# Team Capacity Reference

## Capacity Model (Evidence-Based)

> **Source of truth:** `project-config.json` → `team.members[]` + `team.velocity`
> **Sprint Length:** 2 weeks (10 working days)

**Hybrid Model:**

| Level | Metric | Purpose |
|-------|--------|---------|
| **Story** | Story Points (1,2,3,5,8,13) | Team velocity — "how much can we handle this sprint?" |
| **Subtask** | Size (XS/S/M/L) + Estimated Hours | Individual workload — "when will this be done?" |

## Focus Factor (per Level)

Focus Factor = productive dev hours / total available hours

| Level | Focus Factor | Available Hours/Sprint | Productive Hours/Sprint | Reason |
|-------|-------------|----------------------|------------------------|--------|
| Tech Lead | 0.4-0.5 | 80h | 32-40h | Code review, mentoring, architecture, meetings |
| Senior | 0.7-0.8 | 80h | 56-64h | Complex tasks, some review, mentoring |
| Mid | 0.75-0.85 | 80h | 60-68h | Feature work, some review |
| Junior | 0.6-0.7 | 80h | 48-56h | Learning curve, needs code review, pair programming |

## Skill Matrix

> Skill levels determine task assignment fitness (expert=1.0x, intermediate=0.8x, basic=0.6x)

| Skill Area | Primary (expert) | Secondary (intermediate) | Basic |
|-----------|-------------------|--------------------------|-------|
| Backend API | Sr. Backend, Tech Lead | Jr. Full Stack × 2 | Frontend Dev |
| Frontend (Admin) | Tech Lead | Jr. Full Stack × 2 | Frontend Dev |
| Frontend (Web) | Frontend Dev | Jr. Full Stack × 2 | Sr. Backend |
| Mobile (Flutter) | Frontend Dev | — | — |
| Database/Complex | Sr. Backend, Tech Lead | — | Jr. Full Stack |
| DevOps/Infra | Tech Lead | Sr. Backend, Frontend Dev | Jr. Full Stack |

## Throughput Reference (per Person)

> Source: Jira Sprint 28-31 (Nov 2025 - Feb 2026) — tickets completed per sprint

| Slot | Role | Level | Focus Factor | Avg Throughput | Data Source |
|------|------|-------|-------------|---------------|-------------|
| 1 | Tech Lead | Lead | 0.50 | ~6 tickets/sprint | S29-S31 avg |
| 2 | Sr. Backend | Senior | 0.75 | ~6 tickets/sprint | S29-S31 avg |
| 3 | Jr. Full Stack | Junior | 0.65 | ~14 tickets/sprint | S29-S31 avg |
| 4 | Jr. Full Stack | Junior | 0.65 | ~9 tickets/sprint | S29-S31 avg |
| 5 | Frontend Dev + Mobile | Mid | 0.70 | ~4 tickets/sprint | S30-S31 avg (BEP), billboard-owner-app sole dev |
| 6 | QA | — | — | — | — |
| 7 | QA | — | — | — | — |

## Capacity Calculation (Sprint Planning)

### Step 1: Team Velocity (SP-based — when data available)

```
Team Velocity = avg SP completed over last 3-5 sprints
Sprint Capacity = Team Velocity × 0.8 (safety buffer)
```

> **Bootstrap Phase:** Until 3-5 sprints of SP data collected, use throughput-based model below.

### Step 2: Individual Capacity (Hours-based)

```
Available Hours = Sprint Days × 8h × Focus Factor
Productive Hours = Available Hours - (Leave days × 8h × Focus Factor)
Max Subtask Hours = Productive Hours (sum of estimated hours must not exceed this)
```

**Example:**

```
Jr. Full Stack (no leave): 10 days × 8h × 0.65 = 52 productive hours
Sr. Backend (1 day leave): (10-1) × 8h × 0.75 = 54 productive hours
Tech Lead (no leave): 10 × 8h × 0.50 = 40 productive hours
```

### Step 3: Assignment Matching

```
Match Score = Skill Level × (1 + Context Bonus)
  where Context Bonus = 0.2 if assignee has related carry-over items
```

Priority order:

1. Expert with context → assign directly
2. Expert without context → assign
3. Intermediate with context → assign with review
4. Intermediate without context → assign with review
5. Basic → only if no better match, assign with mentoring

## Carry-over Probability (by Jira Status)

| Status | Probability | Rationale |
|--------|------------|-----------|
| To Do | 100% | Not started yet — guaranteed carry-over |
| In Progress | 85% | May finish before sprint end but most carry over |
| TO FIX | 92% | Needs fixing — usually won't finish in one sprint |
| WAITING TO TEST | 55% | Depends on QA capacity; may finish if QA is available |
| TESTING | 45% | Currently being tested; has a chance to finish in sprint |
| Done | 0% | Completed |
| CANCELED | 0% | Canceled |

## Workload Thresholds

> Based on throughput data. Yellow = at historical avg, Red = exceeds historical max.

| Level | Green (OK) | Yellow (At avg) | Red (Over) |
|-------|-----------|----------------|------------|
| Tech Lead | ≤5 items | 6 items | >6 items |
| Senior | ≤5 items | 6 items | >6 items |
| Mid (FE) | ≤3 items | 4 items | >4 items |
| Junior (FS) | varies | at avg_throughput | >avg_throughput |

> **Note:** joakim has high throughput (~14) due to mostly small fixes (XS/S). Don't use this as benchmark for complex tasks. Adjust threshold by task size mix.
