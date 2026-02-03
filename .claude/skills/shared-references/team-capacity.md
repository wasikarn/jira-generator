# Team Capacity Reference

## BEP Project Team

> ชื่อจริงจะ fetch จาก Jira ตอน runtime (Phase 1 Sprint Discovery)
> ไฟล์นี้เก็บเฉพาะ role structure + capacity model

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
| To Do | 100% | ยังไม่เริ่ม → carry-over แน่นอน |
| In Progress | 85% | อาจเสร็จก่อน sprint end แต่ส่วนใหญ่ carry-over |
| TO FIX | 92% | ต้องแก้ไข → มักไม่ทันใน sprint เดียว |
| WAITING TO TEST | 55% | อยู่ที่ QA capacity ถ้า QA ว่างอาจจบได้ |
| TESTING | 45% | กำลังทดสอบ มีโอกาสจบใน sprint |
| Done | 0% | เสร็จแล้ว |
| CANCELED | 0% | ยกเลิก |

## Workload Thresholds

| Level | Green (OK) | Yellow (At ceiling) | Red (Over) |
|-------|-----------|-------------------|------------|
| Tech Lead | ≤4 items | 5 items | >5 items |
| Senior | ≤8 items | 9 items | >9 items |
| Mid | ≤8 items | 9 items | >9 items |
| Junior | ≤7 items | 8 items | >8 items |
