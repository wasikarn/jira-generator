# User Story Best Practices — Quick Reference

## INVEST Criteria (ตัวตรวจสอบคุณภาพ Story)

| Criteria | ความหมาย | Red Flag |
|----------|----------|----------|
| **I**ndependent | ไม่พึ่งพา story อื่น | "ต้องทำ X ก่อน" |
| **N**egotiable | เป็น invitation to conversation | AC เขียนละเอียดยิบเกินไป |
| **V**aluable | ส่งมอบ value ให้ user ได้จริง | "เตรียม DB schema" (ไม่มี value ตรง) |
| **E**stimable | estimate effort ได้ | ไม่รู้ scope ชัด |
| **S**mall | เสร็จใน 1 sprint, 6-10 stories/sprint | ใหญ่กว่า 3 วัน |
| **T**estable | มี AC ที่ test ได้ชัดเจน | "ระบบทำงานได้ดี" (vague) |

## Story Format

```
As a [persona],
I want to [goal],
So that [benefit/value].
```

## Acceptance Criteria — Given/When/Then

- **Given**: สถานะเริ่มต้นของระบบ (precondition)
- **When**: action ที่ user ทำ (trigger)
- **Then**: ผลลัพธ์ที่คาดหวัง (expected outcome)

### AC Best Practices

- ห้าม vague ("โหลดเร็ว") → ต้อง specific ("โหลดภายใน 2 วินาที")
- แยก story narrative กับ AC ออกจากกัน (อย่า duplicate)
- ครอบคลุม: happy path (`success` panel) + edge case (`warning`) + error (`error`)
- อย่าลืม non-functional requirements (performance, accessibility, security)
- แต่ละ AC ต้อง **independently testable**
- ใช้ **Three Amigos**: PO + Dev + QA ร่วมกันเขียน
- อย่าเขียน AC แคบเกินไป (ไม่เหลือ room ให้ dev) หรือกว้างเกินไป (ไม่ชัดเจน)
- เขียน AC ก่อน sprint planning — ห้ามเปลี่ยนระหว่าง sprint

## Story Splitting — SPIDR Method (Mike Cohn)

| Technique | วิธี | ตัวอย่าง |
|-----------|------|----------|
| **S**pike | วิจัยก่อน split | "Spike: ทดลอง Redlock 2 วัน" |
| **P**ath | แยกตาม user path | จ่ายบัตร vs Apple Pay |
| **I**nterface | แยกตาม device/platform | iOS vs Android vs Web |
| **D**ata | แยกตาม data type | เครดิต vs ส่วนลด vs cashback |
| **R**ules | แยกตาม business rules | คูปองหมดอายุ vs ใช้ครบ vs ยกเลิก |

### Additional Splitting Techniques

- **Workflow Steps**: แยกตามขั้นตอนการทำงาน
- **CRUD**: Create / Read / Update / Delete แยกกัน
- **User Roles**: Admin vs Customer vs Influencer
- **Complexity**: manual vs automated, simple vs advanced
- **I/O Methods**: manual entry vs file upload vs API

### Splitting Rules

- **Vertical Slice เสมอ** — ห้าม Horizontal (แยก FE/BE ไม่ส่ง value)
- เป้าหมาย: 6-10 stories/sprint, แต่ละ story 1-3 วัน
- ทุก slice ต้องส่ง end-to-end value ได้

## Story Size Guide

| Size | Duration | Guideline |
|------|----------|-----------|
| XS | < 1 day | อาจเล็กเกินไป — รวมกับ story อื่นได้ |
| S | 1-2 days | เหมาะสม |
| M | 2-3 days | เหมาะสม |
| L | 3-4 days | ขอบเขตบน — พิจารณา split |
| XL | > 4 days | ต้อง split — ใช้ SPIDR |

## Sources

- INVEST: <https://scrum-master.org/en/creating-the-perfect-user-story-with-invest-criteria/>
- Given/When/Then: <https://www.parallelhq.com/blog/given-when-then-acceptance-criteria>
- SPIDR: <https://www.mountaingoatsoftware.com/blog/five-simple-but-powerful-ways-to-split-user-stories>
- Story Splitting: <https://www.humanizingwork.com/the-humanizing-work-guide-to-splitting-user-stories/>
- Acceptance Criteria: <https://www.atlassian.com/work-management/project-management/acceptance-criteria>
