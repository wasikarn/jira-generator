# Sprint Planning Frameworks

> Source: BEP project experience
> Used by: `/plan-sprint` skill (Phase 3-6 strategy analysis)

## RICE Scoring

**Reach × Impact × Confidence ÷ Effort = RICE Score**

| Factor | Scale | Description |
| -------- | ------- | ------------- |
| Reach | 1-10 | Number of users affected (10=everyone) |
| Impact | 0.25-3 | Impact on user (3=massive, 2=high, 1=medium, 0.5=low, 0.25=minimal) |
| Confidence | 10-100% | Confidence in data (100%=certain, 80%=high, 50%=medium, 20%=low) |
| Effort | person-sprints | Number of person-sprints required (lower is better) |

**Interpretation:** Higher = should be done first

## Impact vs Effort Matrix

```text
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
| ---------- | -------- | ---------------- |
| DO FIRST | High impact, low effort — do immediately | P1 |
| PLAN CAREFULLY | High impact, high effort — plan thoroughly | P2 |
| QUICK WINS | Low impact, low effort — do when capacity is available | P3 |
| AVOID/DEFER | Low impact, high effort — defer | P4 |

## Carry-over Analysis Model

### Status-based Probability

| Status | Carry-over % | Action |
| -------- | ------------- | -------- |
| To Do | 100% | Not started yet — guaranteed carry-over |
| In Progress | 85% | May finish, but most won't make it in time |
| TO FIX | 92% | Needs fixing — usually must carry over |
| WAITING TO TEST | 55% | Depends on QA capacity |
| TESTING | 45% | Currently being tested; has a chance to finish |
| Done / CANCELED | 0% | No carry-over |

### Carry-over Calculation

```text
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
| ----------- | ------ | -------- |
| Total items > budget ceiling | 🔴 Overloaded | Move items to someone else or defer |
| Total items = budget ceiling | ⚠️ At ceiling | Monitor; do not add more items |
| Total items < 70% budget | 🟢 Has capacity | Can take on additional work |
| Junior holds critical path | ⚠️ Risk | Add reviewer/mentor support |
| >3 carry-over items (same person) | ⚠️ Sticky | Review what's blocking them |

## Vertical Slicing

> Source: Scrum Guide, StoriesOnBoard, SAFe — applied in Sprint 32 coupon system

### Principle

Stories must deliver **end-to-end user value** across all layers (UI → API → DB) — each story = independently deployable + testable

### Vertical vs Horizontal

| | Vertical (✅) | Horizontal (❌) |
| --- | --- | --- |
| Scope | Full stack for one flow | One layer across many flows |
| Value | User can actually use it | Must wait for other layers to work |
| Testing | QA can test real flows | Must wait for integration |
| Example | "User collects credit coupon e2e" | "Build UI shell for all pages" |

### Patterns

| Pattern | When to Use | Example |
| --- | --- | --- |
| **Walking Skeleton** | Need navigation + empty states first | `vs1-skeleton`: nav + empty states |
| **Business Rule Split** | Split by different rules/types | `vs2-credit-e2e`, `vs3-discount-e2e` |
| **Enabler Story** (SAFe) | Shared component used by multiple slices | `vs-enabler`: Side Panel, Toast |
| **Cross-feature** | Spans multiple feature areas | `ad-integration`: coupon → ad flow |

### Anti-patterns

| Anti-pattern | Problem | Fix |
| --- | --- | --- |
| Shell-only story (UI has no logic) | No value → INVEST fail | Add minimal happy path or reframe as Walking Skeleton |
| Layer split (BE separated from FE) | Must wait for other layers → blocked | Combine BE+FE in single story |
| Tab-split (Active tab / History tab) | Single tab has no context | Split by business rule instead |

### Sprint Assignment Strategy

| Sprint | Focus | Stories |
| --- | --- | --- |
| Sprint N | Skeleton + Enablers + first E2E slice | `vs1-skeleton` + `vs-enabler` + `vs2-*` |
| Sprint N+1 | Remaining E2E slices + cross-feature | `vs3-*` + `vs4-*` + `ad-integration` |

## Sprint Meeting Best Practices

> Source: [Easy Agile](https://www.easyagile.com/blog/2026-sprint-planning-team-alignment-challenges-best-practices), [Mountain Goat Software](https://www.mountaingoatsoftware.com/agile/scrum/meetings/sprint-planning-meeting)

### Timebox Formula

| Sprint Length | Meeting Timebox |
| --- | --- |
| 1 week | 45 min |
| 2 weeks | 90 min |
| 3 weeks | 2h 15min |
| 4 weeks | 3h |

**Formula:** `45 min × weeks in sprint`

### Meeting Preparation Checklist

**Product Owner:**

- [ ] Review past sprint retrospective + stakeholder feedback
- [ ] Backlog refined + prioritized (top items ready)
- [ ] Acceptance criteria defined for top items
- [ ] Dependencies identified

**Development Team:**

- [ ] Capacity conflicts identified (leave, meetings)
- [ ] Technical concerns surfaced
- [ ] Carry-over items status updated

**Scrum Master:**

- [ ] Meeting scheduled consistently (same day/time)
- [ ] Sprint goal draft prepared
- [ ] Previous sprint metrics available

---

## Sprint Goal Best Practices

> Source: [Atlassian](https://www.atlassian.com/agile/scrum/sprint-planning), [DevDynamics](https://devdynamics.ai/blog/the-ultimate-guide-to-agile-sprint-planning/)

### SMART Sprint Goal

| Criteria | Question | Example |
| --- | --- | --- |
| **S**pecific | What outcome? | "Users can collect credit coupons" |
| **M**easurable | How to verify? | "QA passes 3 main test cases" |
| **A**chievable | Within capacity? | ≤80% of capacity |
| **R**elevant | Aligns with product? | Aligns with Epic objective |
| **T**ime-bound | End of sprint? | "Within Sprint 33" |

### Sprint Goal Template

```text
By the end of this Sprint, [target users] will be able to [do something valuable]
```

**Example:**
> By the end of Sprint 33, coupon system users will be able to collect credit coupons and view coupon history

### Anti-patterns

| Anti-pattern | Problem | Fix |
| --- | --- | --- |
| "Just finish it" | No clear outcome | Specify user outcome |
| No goal | Team has no direction | Define goal before selecting items |
| Goal doesn't align with items | Completing items but not reaching goal | Review items vs goal |

---

## "Just Enough" Planning

> Source: [DevDynamics](https://devdynamics.ai/blog/the-ultimate-guide-to-agile-sprint-planning/), [Premier Agile](https://premieragile.com/sprint-planning-best-practices)

### Principle

**Focus on goal, not complete plan** — Plan should be guardrails, not a monkey on the team's back

### Guidelines

| Do | Don't |
| --- | --- |
| Define sprint goal first | Start with task assignment |
| Build backlog to get started | Create complete task breakdown |
| Allow self-organization | Pre-assign all tasks |
| Use lightweight estimation | Spend hours on estimation |
| Leave room for discovery | Plan every hour of the sprint |

### Real-time Sign-up Strategy

```text
❌ Bad: Before sprint starts → assign all tasks to everyone
✅ Good: Assign only Day 1-2 → rest is self sign-up
```

**Benefits:**

- Reduce context switching
- Whoever is free first picks up work first
- Flexibility when blockers arise

---

## Task Decomposition

> Source: [monday.com](https://monday.com/blog/rnd/sprint-backlog/)

### Rule: Subtask ≤ 1 day

| Size | Duration | Action |
| --- | --- | --- |
| XS | < 4h | Appropriate |
| S | 4-8h (1 day) | Appropriate |
| M | 1-2 days | Should split |
| L | > 2 days | Must split |

### Decomposition Checklist

- [ ] Subtask has clear deliverable
- [ ] Can be demo'd/verified
- [ ] No dependency on other subtasks completing first (if possible)
- [ ] Single assignee (no sharing)

---

## Sustainable Pace

> Source: [Wrike](https://www.wrike.com/scrum-guide/faq/what-is-a-sprint-backlog/), Agile Manifesto

### Core Principle

> "Agile processes promote sustainable development. The sponsors, developers, and users should be able to maintain a constant pace indefinitely."

### Capacity Buffer

| Scenario | Buffer | Reason |
| --- | --- | --- |
| Normal sprint | 10-15% | Unexpected issues |
| New team member | 20% | Onboarding overhead |
| Tech debt sprint | 25% | Discovery during refactor |
| Holiday period | 30% | Reduced availability |

### Overcommitment Signs

- [ ] Team consistently misses sprint goals
- [ ] High carry-over rate (>30%)
- [ ] Quality issues / bugs increase
- [ ] Team morale decreasing
- [ ] Overtime becoming normal

**Fix:** Reduce scope, not quality

---

## Backlog Grooming Integration

> Source: [Premier Agile](https://premieragile.com/prioritize-work-and-manage-sprint-backlog/), [Scrum Study](https://www.scrumstudy.com/article/agile-scrum-sprint-backlog)

### 10% Rule

> Development teams should spend **no more than 10%** of their capacity on backlog grooming

| Sprint Length | Grooming Budget |
| --- | --- |
| 2 weeks | ~1 day |
| 4 weeks | ~2 days |

### Pre-Sprint Refinement Checklist

- [ ] Top 2 sprints worth of items refined
- [ ] Acceptance criteria written
- [ ] Dependencies identified
- [ ] Estimates assigned (if using points)
- [ ] Items small enough (≤3 days)

---

## Sprint Planning Checklist

- [ ] **Meeting:** Timeboxed, all roles present, prepared
- [ ] **Goal:** SMART sprint goal defined + agreed
- [ ] Carry-over items identified + counted per person
- [ ] New items prioritized (RICE or Impact/Effort)
- [ ] Items matched to team members (skill + capacity)
- [ ] No one exceeds capacity ceiling (sustainable pace)
- [ ] Dependencies identified + blockers prioritized
- [ ] Risk flags reviewed + mitigated
- [ ] Stories are vertical slices (not horizontal layers)
- [ ] **Buffer:** 10-15% capacity reserved
- [ ] User approved plan before execution

---

## Sources

- Meeting Timebox: [Mountain Goat Software](https://www.mountaingoatsoftware.com/agile/scrum/meetings/sprint-planning-meeting)
- Sprint Planning Best Practices: [Easy Agile](https://www.easyagile.com/blog/2026-sprint-planning-team-alignment-challenges-best-practices)
- Sprint Goal: [Atlassian Sprint Planning](https://www.atlassian.com/agile/scrum/sprint-planning)
- Just Enough Planning: [DevDynamics](https://devdynamics.ai/blog/the-ultimate-guide-to-agile-sprint-planning/)
- Sprint Backlog: [monday.com](https://monday.com/blog/rnd/sprint-backlog/), [Wrike](https://www.wrike.com/scrum-guide/faq/what-is-a-sprint-backlog/)
- Backlog Grooming: [Premier Agile](https://premieragile.com/prioritize-work-and-manage-sprint-backlog/)
