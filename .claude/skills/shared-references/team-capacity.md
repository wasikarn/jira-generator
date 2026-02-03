# Team Capacity Reference

## BEP Project Team

> Real names are fetched from Jira at runtime (Phase 1 Sprint Discovery)
> This file only stores the role structure + capacity model

| Slot | Role | Level | Focus | Capacity | Items/Sprint |
|------|------|-------|-------|----------|-------------|
| 1 | Tech Lead | Lead | Full Stack + code review + mentoring | 40-50% | 4-5 |
| 2 | Sr. Backend | Senior | Backend, complex systems | 80-90% | 8-9 |
| 3 | Jr. Full Stack | Junior | Frontend + Backend | 70-80% | 7-8 |
| 4 | Jr. Full Stack | Junior | Frontend + Backend | 70-80% | 7-8 |
| 5 | Frontend Dev | Mid | Frontend | 85-90% | 8-9 |
| 6 | QA | — | Testing | — | — |
| 7 | QA | — | Testing | — | — |
| 8 | UX/UI | — | Design | — | — |

## Capacity Model

**Sprint Length:** 2 weeks (10 working days)

**Capacity = Level Budget:**

| Level | Dev Capacity | Reason |
|-------|-------------|--------|
| Tech Lead | 40-50% | Code review, mentoring, architecture decisions |
| Senior | 80-90% | Complex tasks, some review |
| Mid | 85-90% | Feature work, some review |
| Junior | 70-80% | Learning curve, needs review |

## Skill Mapping (by Role)

| Skill Area | Primary | Secondary |
|------------|---------|-----------|
| Backend API | Sr. Backend, Tech Lead | Jr. Full Stack |
| Frontend (Admin) | Jr. Full Stack, Tech Lead | Frontend Dev |
| Frontend (Web) | Frontend Dev, Tech Lead | Jr. Full Stack |
| Database/Complex | Sr. Backend | Tech Lead |
| DevOps/Infra | Tech Lead | Sr. Backend |

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

| Level | Green (OK) | Yellow (At ceiling) | Red (Over) |
|-------|-----------|-------------------|------------|
| Tech Lead | ≤4 items | 5 items | >5 items |
| Senior | ≤8 items | 9 items | >9 items |
| Mid | ≤8 items | 9 items | >9 items |
| Junior | ≤7 items | 8 items | >8 items |
