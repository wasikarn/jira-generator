# Sprint Planning Frameworks

> Source: Adapted from Tresor sprint-prioritizer + BEP project experience
> Used by: `/plan-sprint` skill (Phase 3-6 strategy analysis)

## RICE Scoring

**Reach × Impact × Confidence ÷ Effort = RICE Score**

| Factor | Scale | Description |
|--------|-------|-------------|
| Reach | 1-10 | Number of users affected (10=everyone) |
| Impact | 0.25-3 | Impact on user (3=massive, 2=high, 1=medium, 0.5=low, 0.25=minimal) |
| Confidence | 10-100% | Confidence in data (100%=certain, 80%=high, 50%=medium, 20%=low) |
| Effort | person-sprints | Number of person-sprints required (lower is better) |

**Interpretation:** Higher = should be done first

## Impact vs Effort Matrix

```
High Impact
    │
    │  PLAN CAREFULLY    DO FIRST ⭐
    │  (High/High)       (High/Low)
    │
    ├──────────────────────────────────
    │
    │  AVOID/DEFER       QUICK WINS
    │  (Low/High)        (Low/Low)
    │
    └─────────────────────────── High Effort
```

| Quadrant | Action | Sprint Priority |
|----------|--------|----------------|
| DO FIRST | High impact, low effort — do immediately | P1 |
| PLAN CAREFULLY | High impact, high effort — plan thoroughly | P2 |
| QUICK WINS | Low impact, low effort — do when capacity is available | P3 |
| AVOID/DEFER | Low impact, high effort — defer | P4 |

## Carry-over Analysis Model

### Status-based Probability

| Status | Carry-over % | Action |
|--------|-------------|--------|
| To Do | 100% | Not started yet — guaranteed carry-over |
| In Progress | 85% | May finish, but most won't make it in time |
| TO FIX | 92% | Needs fixing — usually must carry over |
| WAITING TO TEST | 55% | Depends on QA capacity |
| TESTING | 45% | Currently being tested; has a chance to finish |
| Done / CANCELED | 0% | No carry-over |

### Carry-over Calculation

```
Expected carry-over = Σ (items × probability per status)
```

## Workload Balancing Rules

### Assignment Criteria (Priority Order)

1. **Skill match** — assign based on primary skill first
2. **Existing context** — person already working on the item should continue (reduce context switching)
3. **Capacity available** — check if slots remain (carry-over + new items ≤ budget)
4. **Growth opportunity** — juniors can take new work when a mentor is available

### Grouping Strategy

- **Related items → same person** — reduce context switching
- **Blocking dependencies → prioritize blocker** — unblock others
- **Critical path → senior/lead** — reduce risk

### Risk Flags

| Condition | Flag | Action |
|-----------|------|--------|
| Total items > budget ceiling | 🔴 Overloaded | Move items to someone else or defer |
| Total items = budget ceiling | ⚠️ At ceiling | Monitor; do not add more items |
| Total items < 70% budget | 🟢 Has capacity | Can take on additional work |
| Junior holds critical path | ⚠️ Risk | Add reviewer/mentor support |
| >3 carry-over items (same person) | ⚠️ Sticky | Review what's blocking them |

## Sprint Planning Checklist

- [ ] Carry-over items identified + counted per person
- [ ] New items prioritized (RICE or Impact/Effort)
- [ ] Items matched to team members (skill + capacity)
- [ ] No one exceeds capacity ceiling
- [ ] Dependencies identified + blockers prioritized
- [ ] Risk flags reviewed + mitigated
- [ ] Sprint goal defined (1-2 sentences)
- [ ] User approved plan before execution
