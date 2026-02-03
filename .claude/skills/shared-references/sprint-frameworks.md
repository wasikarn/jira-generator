# Sprint Planning Frameworks

> Source: Adapted from Tresor sprint-prioritizer + BEP project experience
> Used by: `/plan-sprint` skill (Phase 3-6 strategy analysis)

## RICE Scoring

**Reach × Impact × Confidence ÷ Effort = RICE Score**

| Factor | Scale | Description |
|--------|-------|-------------|
| Reach | 1-10 | จำนวน users ที่ได้รับผลกระทบ (10=ทุกคน) |
| Impact | 0.25-3 | ผลกระทบต่อ user (3=massive, 2=high, 1=medium, 0.5=low, 0.25=minimal) |
| Confidence | 10-100% | ความมั่นใจในข้อมูล (100%=แน่นอน, 80%=high, 50%=medium, 20%=low) |
| Effort | person-sprints | จำนวน person-sprint ที่ต้องใช้ (ยิ่งน้อยยิ่งดี) |

**Interpretation:** สูงกว่า = ควรทำก่อน

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
| DO FIRST | High impact, low effort → ทำทันที | P1 |
| PLAN CAREFULLY | High impact, high effort → วางแผนดี ๆ | P2 |
| QUICK WINS | Low impact, low effort → ทำเมื่อมี capacity เหลือ | P3 |
| AVOID/DEFER | Low impact, high effort → เลื่อนออก | P4 |

## Carry-over Analysis Model

### Status-based Probability

| Status | Carry-over % | Action |
|--------|-------------|--------|
| To Do | 100% | ยังไม่เริ่ม → carry-over แน่นอน |
| In Progress | 85% | อาจเสร็จ แต่ส่วนใหญ่ไม่ทัน |
| TO FIX | 92% | ต้องแก้ไข → มักต้อง carry-over |
| WAITING TO TEST | 55% | ขึ้นกับ QA capacity |
| TESTING | 45% | กำลังทดสอบ มีโอกาสจบ |
| Done / CANCELED | 0% | ไม่ carry-over |

### Carry-over Calculation

```
Expected carry-over = Σ (items × probability per status)
```

## Workload Balancing Rules

### Assignment Criteria (Priority Order)

1. **Skill match** — assign ตาม primary skill ก่อน
2. **Existing context** — คนที่ทำ item เดิมอยู่ → ให้ทำต่อ (ลด context switching)
3. **Capacity available** — ดูว่ามี slot เหลือไหม (carry-over + new items ≤ budget)
4. **Growth opportunity** — junior ทำงานใหม่ได้เมื่อ mentor available

### Grouping Strategy

- **Related items → same person** — ลด context switching
- **Blocking dependencies → prioritize blocker** — ปลดล็อคคนอื่น
- **Critical path → senior/lead** — ลดความเสี่ยง

### Risk Flags

| Condition | Flag | Action |
|-----------|------|--------|
| Total items > budget ceiling | 🔴 Overloaded | ย้าย items ให้คนอื่น หรือ defer |
| Total items = budget ceiling | ⚠️ At ceiling | Monitor ไม่เพิ่ม items |
| Total items < 70% budget | 🟢 Has capacity | สามารถรับงานเพิ่มได้ |
| Junior ถือ critical path | ⚠️ Risk | เพิ่ม reviewer/mentor support |
| >3 carry-over items (same person) | ⚠️ Sticky | Review ว่าติดอะไร |

## Sprint Planning Checklist

- [ ] Carry-over items identified + counted per person
- [ ] New items prioritized (RICE or Impact/Effort)
- [ ] Items matched to team members (skill + capacity)
- [ ] No one exceeds capacity ceiling
- [ ] Dependencies identified + blockers prioritized
- [ ] Risk flags reviewed + mitigated
- [ ] Sprint goal defined (1-2 sentences)
- [ ] User approved plan before execution
