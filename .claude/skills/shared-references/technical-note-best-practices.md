# Technical Note Best Practices — Quick Reference

## Technical Note คืออะไร

Technical Note (Tech Note) คือเอกสารประกอบ Jira ticket ที่อธิบาย **implementation approach** สำหรับ developer — ไม่ใช่ specification แต่เป็น **guidance** ที่ช่วยให้เริ่มงานได้เร็วขึ้น

### Technical Note vs อื่นๆ

| Document | จุดประสงค์ | ผู้อ่าน | ความละเอียด |
| --- | --- | --- | --- |
| **Technical Note** | Implementation guidance สำหรับ ticket | Developer | พอดี — เฉพาะสิ่งที่ต้องรู้ |
| Tech Spec | Full design + architecture decision | Team + stakeholders | สูง — ครบทุก section |
| ADR | บันทึก architecture decision + เหตุผล | Future team | กลาง — focus ที่ decision |
| README | Project setup + usage | New developer | กลาง — onboarding |

## When to Write

| Situation | ต้องเขียน? | เหตุผล |
| --- | --- | --- |
| Subtask มี scope ชัดเจน, dev รู้ codebase | ❌ ไม่จำเป็น | AC เพียงพอแล้ว |
| Story มี API contract ใหม่หรือ data flow ซับซ้อน | ✅ ควรเขียน | ลด ambiguity ให้ dev |
| Cross-service integration (BE↔FE, external API) | ✅ ต้องเขียน | ป้องกัน miscommunication |
| New pattern/library ที่ทีมยังไม่เคยใช้ | ✅ ต้องเขียน | ลด learning curve |
| Bug fix ที่ root cause ชัดแล้ว | ❌ ไม่จำเป็น | ใส่ root cause ใน ticket พอ |

## Sections — JBGE (Just Barely Good Enough)

> เขียนแค่ section ที่จำเป็น — ไม่ต้องครบทุก section

### Required Sections

| Section | เนื้อหา | Tips |
| --- | --- | --- |
| **Objective** | 1-2 ประโยค — ทำอะไร ทำไม | ตอบ "ทำเสร็จแล้วได้อะไร?" |
| **Scope** | file paths จริง, modules ที่แก้ | ต้อง Explore codebase ก่อน |
| **Approach** | วิธีทำ step-by-step (high-level) | ลำดับ: DB → API → UI → Test |

### Recommended Sections (ใช้เมื่อจำเป็น)

| Section | เมื่อไหร่ | เนื้อหา |
| --- | --- | --- |
| **API Contract** | endpoint ใหม่/เปลี่ยน | method, path, request/response schema |
| **Data Flow** | cross-service | diagram หรือ arrow notation (`A → B → C`) |
| **Dependencies** | ต้องรอ ticket อื่น | link + ระบุว่ารออะไร |
| **Alternatives** | มีทาง >1 ทาง | เปรียบเทียบ pros/cons สั้นๆ |
| **Risks** | มี technical risk | ระบุ risk + mitigation |
| **Open Questions** | ยังไม่แน่ใจบางส่วน | list คำถาม + ใครตอบได้ |

## Writing Style

### Do's

- ใช้ **bullet points** ไม่ใช่ paragraph ยาว
- ใส่ **code marks** สำหรับ file paths, function names, routes
- ใส่ **real file paths** จาก codebase (Explore ก่อนเสมอ)
- เขียน API contract แบบ **concrete** (method + path + schema)
- ใช้ **arrow notation** สำหรับ data flow: `Client → API → Service → DB`
- link ไป Jira ticket, Confluence, Figma เมื่ออ้างอิง

### Don'ts

- ❌ เขียน specification ซ้ำกับ AC (duplicate)
- ❌ เขียน "how to code" ทีละบรรทัด (micromanage)
- ❌ ใส่ business logic ที่ควรอยู่ใน AC
- ❌ เขียน generic path ("แก้ไฟล์ service") → ต้อง specific
- ❌ เขียนยาวเกินไป — ถ้า > 1 page ควร split เป็น Tech Spec

## Size Guide

| Size | บรรทัด | เหมาะกับ |
| --- | --- | --- |
| Minimal | 5-10 | Subtask เดียว, scope ชัด |
| Standard | 10-25 | Story ที่มี API/integration |
| Extended | 25-50 | Cross-service, new pattern |
| Too Long | > 50 | ควรเป็น Tech Spec/ADR แทน |

## Confluence Technical Note

### Page Structure

```text
Title: [{{PROJECT_KEY}}-XXX] Technical Note — [Feature Name]
├── Objective
├── Scope (files/modules)
├── Approach (step-by-step)
├── API Contract (if applicable)
├── Data Flow (if cross-service)
├── Open Questions
└── Related Links (Jira, Figma)
```

### Confluence Best Practices

- ใช้ **template** เดิมทุกครั้ง — consistency สำคัญ
- ใส่ **labels**: `tech-note`, service tag (`backend`, `frontend`), sprint
- link กลับไป **Jira ticket** เสมอ (bidirectional)
- ใช้ **Table of Contents macro** สำหรับ note ที่ยาว
- ใช้ **Code Block macro** (พร้อม syntax highlight) สำหรับ code snippets
- ใช้ **Panel macro** — `info`(context), `warning`(risks), `note`(tips)
- **Review** tech note หลัง sprint — archive หรือ update ถ้า outdated

### Naming Convention

- Jira subtask: `[TAG] - Technical Note: [Feature]`
- Confluence page: `[{{PROJECT_KEY}}-XXX] Technical Note — [Feature]`
- Label: `tech-note`, `sprint-XX`, service tag

## Architecture Decision Record (ADR)

> ใช้เมื่อต้องตัดสินใจ architecture ที่ส่งผลกระทบกว้าง

### ADR Format (MADR)

```text
Title: ADR-XXX — [Decision Title]
Status: Proposed | Accepted | Deprecated | Superseded
Date: YYYY-MM-DD

## Context
ปัญหาหรือสถานการณ์ที่ต้องตัดสินใจ

## Decision
สิ่งที่เลือกทำ + เหตุผล

## Alternatives
ทางเลือกอื่นที่พิจารณาแล้ว + เหตุผลที่ไม่เลือก

## Consequences
ผลกระทบ (ทั้ง positive + negative)
```

### When ADR vs Tech Note

| เงื่อนไข | ใช้ ADR | ใช้ Tech Note |
| --- | --- | --- |
| ตัดสินใจ architecture/technology | ✅ | |
| Implementation guidance | | ✅ |
| มี alternatives ที่ต้อง document | ✅ | |
| Scope = 1 ticket | | ✅ |
| Scope = หลาย tickets / system-wide | ✅ | |
| ต้อง review ในอนาคต (เช่น 6 เดือน) | ✅ | |

## Anti-Patterns

| Anti-Pattern | ปัญหา | แก้ไข |
| --- | --- | --- |
| Spec ซ้ำ AC | duplicate info, ยาก maintain | Tech note = HOW, AC = WHAT |
| Micromanage code | dev ไม่มี room ตัดสินใจ | เขียน approach level, ไม่ใช่ code level |
| No real paths | dev ต้องหาเอง | Explore codebase ก่อนเขียนเสมอ |
| Never update | เอกสาร outdated mislead | Review ทุก sprint, archive ถ้า done |
| Write too early | requirement ยังเปลี่ยน | เขียนหลัง story refined แล้ว |
| Write too late | dev เริ่มงานไปแล้ว | เขียนก่อน sprint planning |

## Sources

- Agile Documentation: <https://agilemodeling.com/essays/agileDocumentationBestPractices.htm>
- MADR (ADR Template): <https://adr.github.io/madr/>
- Confluence Tech Docs: <https://support.atlassian.com/confluence-cloud/docs/use-confluence-for-technical-documentation/>
- Technical Design Docs: <https://www.range.co/blog/better-tech-specs>
- Atlassian Templates: <https://www.atlassian.com/software/confluence/templates>
- JBGE Principle: <https://www.pmi.org/disciplined-agile/agile/documentation>
