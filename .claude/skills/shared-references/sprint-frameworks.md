# Sprint Planning Frameworks

> Source: Adapted from Tresor sprint-prioritizer + BEP project experience
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

Stories ต้องส่งมอบ **end-to-end user value** ครบทุก layer (UI → API → DB) แต่ละ story = independently deployable + testable

### Vertical vs Horizontal

| | Vertical (✅) | Horizontal (❌) |
| --- | --- | --- |
| Scope | Full stack for one flow | One layer across many flows |
| Value | User ใช้งานได้จริง | ต้องรอ layer อื่นจึงจะ work |
| Testing | QA ทดสอบ flow จริงได้ | ต้องรอ integration |
| Example | "ผู้ใช้เก็บคูปองเครดิต e2e" | "สร้าง UI shell ทุกหน้า" |

### Patterns

| Pattern | When to Use | Example |
| --- | --- | --- |
| **Walking Skeleton** | ต้องการ navigation + empty states ก่อน | `vs1-skeleton`: nav + empty states |
| **Business Rule Split** | แยกตาม rule/type ที่ต่างกัน | `vs2-credit-e2e`, `vs3-discount-e2e` |
| **Enabler Story** (SAFe) | Shared component ที่หลาย slice ใช้ร่วม | `vs-enabler`: Side Panel, Toast |
| **Cross-feature** | ข้ามหลาย feature areas | `ad-integration`: coupon → ad flow |

### Anti-patterns

| Anti-pattern | Problem | Fix |
| --- | --- | --- |
| Shell-only story (UI ไม่มี logic) | ไม่มี value → INVEST fail | เพิ่ม minimal happy path หรือ reframe เป็น Walking Skeleton |
| Layer split (BE แยกจาก FE) | ต้องรอ layer อื่น → blocked | รวม BE+FE ใน story เดียว |
| Tab-split (Active tab / History tab) | Tab เดียวไม่มี context | Split ตาม business rule แทน |

### Sprint Assignment Strategy

| Sprint | Focus | Stories |
| --- | --- | --- |
| Sprint N | Skeleton + Enablers + first E2E slice | `vs1-skeleton` + `vs-enabler` + `vs2-*` |
| Sprint N+1 | Remaining E2E slices + cross-feature | `vs3-*` + `vs4-*` + `ad-integration` |

## Sprint Planning Checklist

- [ ] Carry-over items identified + counted per person
- [ ] New items prioritized (RICE or Impact/Effort)
- [ ] Items matched to team members (skill + capacity)
- [ ] No one exceeds capacity ceiling
- [ ] Dependencies identified + blockers prioritized
- [ ] Risk flags reviewed + mitigated
- [ ] Stories are vertical slices (not horizontal layers)
- [ ] Sprint goal defined (1-2 sentences)
- [ ] User approved plan before execution
