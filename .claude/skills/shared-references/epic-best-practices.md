# Epic Best Practices — Quick Reference

## Naming Conventions

- ตั้งชื่อรอบ **deliverable** ไม่ใช่ category กว้างๆ
- ห้ามใส่ version/phase ในชื่อ (เช่น "Phase 1", "v2")
- สั้น กระชับ อ่านแล้วรู้เลยว่าจะได้อะไร
- Format: `[Domain] — [Deliverable Description]`
- ตัวอย่าง: `ระบบคูปอง — Admin CRUD & Usage History`

## Ideal Epic Size

- **8-15 stories** ต่อ Epic (recommended range)
- **ระยะเวลา 2-6 months** — ยาวกว่านี้ควร split
- ถ้า Epic ข้าม 3+ sprints และมี scope หลาย layer → split

## When to Split

- Children > 15 active tickets
- ทีมหลายคนทำงานคนละ domain ใน Epic เดียวกัน
- ไม่สามารถ track progress ได้ชัดเจน
- Epic มี mixed concerns (Admin + BE + FE)

## How to Split

- แตกตาม **user persona** (Admin vs Customer)
- แตกตาม **delivery layer** (Frontend, Backend, Infrastructure)
- แตกตาม **ordered process** (VS1→VS2→VS3)
- ห้ามแตกจน Epic มี < 5 tickets (too granular)

## Epic Lifecycle

- Close Epics when done → create new Epic for next phase
- ไม่ต้อง keep "Phase 1" open ถ้า done แล้ว
- Review Epic scope ทุก sprint planning

## Sources

- Atlassian Epics Guide: <https://www.atlassian.com/agile/project-management/epics>
- Praecipio Best Practices: <https://www.praecipio.com/resources/articles/best-practices-for-jira-epics>
- Atlassian Community Guide: <https://community.atlassian.com/forums/App-Central-articles/The-Complete-Guide-to-Jira-Epics-From-Definition-to-Execution/ba-p/3173776>
