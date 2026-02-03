# Critical Items Checklist

> Items ที่ **ต้องอยู่** ใน Passive Context เสมอหลัง optimize
> ใช้โดย Phase 5 ของ `/optimize-context` เพื่อ verify ว่า compression ไม่ทำให้ข้อมูลสำคัญหาย

## Format

```text
pattern | description | source
```

- **pattern**: regex สำหรับ grep ใน Passive Context section
- **description**: อธิบายว่า check อะไร
- **source**: shared-ref file ที่เป็นต้นทาง

---

## Critical (skill จะ fail ถ้าหาย)

```text
CREATE.*EDIT | CREATE vs EDIT JSON format distinction | templates.md
issues.*BEP | EDIT requires "issues" array | templates.md
acli.*from-json | acli for description create/update | tools.md
Two-Step|MCP create.*acli edit | Subtask two-step workflow | tools.md
panelType | Panel types reference exists | templates.md
info.*success.*warning.*error.*note | All 5 panel types listed | templates.md
fields.*parameter|fields.*jira_get_issue | fields parameter required for get_issue | tools.md
```

## Important (quality จะลดลงถ้าหาย)

```text
Thai.*ทับศัพท์|ทับศัพท์ | Language rule: Thai + transliteration | writing-style.md
Given.*When.*Then | AC format: Given/When/Then | verification-checklist.md
INVEST | Story quality criteria | verification-checklist.md
\[BE\].*\[FE | Service tags reference | writing-style.md
panels.*not.*table|table.*not.*panel | AC must use panels not tables | templates.md
Confluence.*script|Python.*script | Confluence operations need scripts | tools.md
```

---

## Maintenance

เมื่อเพิ่ม rule ใหม่ใน shared-refs:

1. ถามตัวเอง: "ถ้า rule นี้หายจาก passive context, skill จะ fail มั้ย?"
2. ถ้าใช่ → เพิ่มใน Critical
3. ถ้าไม่ fail แต่ quality ลด → เพิ่มใน Important
4. ถ้าเป็นแค่ detail → ไม่ต้องเพิ่ม (ไว้ใน shared-ref เดิม)
