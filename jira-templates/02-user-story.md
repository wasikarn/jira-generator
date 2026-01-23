# Jira User Story Template

> **Version:** 3.1 | **Updated:** 2026-01-23

---

## 🎨 ADF Cosmetic Features

| Feature | Usage | Visual |
| :--- | :--- | :---: |
| **Info Panel** | User story narrative | 🔵 Blue |
| **Success Panel** | Happy path AC | 🟢 Green |
| **Warning Panel** | Validation AC | 🟡 Yellow |
| **Error Panel** | Error handling AC | 🔴 Red |
| **Note Panel** | Business rules, important notes | 🟣 Purple |

> 💡 **Tip:** ใช้ ADF panels เพื่อแยก AC types ด้วยสี ช่วยให้ทีมอ่านและเข้าใจได้ง่ายขึ้น

---

## Summary Format

```
[Feature Name]
```

**Examples:**
- ✅ สร้างคูปองเติมเครดิต
- ✅ หน้า Coupon List
- ❌ ทำหน้า (ไม่ชัดเจน)

---

## Description Template (Copy ไปใช้เลย)

```markdown
## 📖 User Story

> **As a** [persona],
> **I want to** [action],
> **So that** [benefit].

---

## ✅ Acceptance Criteria

> 💡 **ADF Panel Guide:** ใช้ `success` panel สำหรับ Happy Path, `warning` panel สำหรับ Validation, `error` panel สำหรับ Error Case

---

> **🟢 AC1: [Happy Path - ชื่อ scenario]** `[panel: success]`
>
> | | |
> | --- | --- |
> | **Given** | [precondition - สถานะเริ่มต้น] |
> | **When** | [action - การกระทำของ user] |
> | **Then** | [outcome - ผลลัพธ์ที่คาดหวัง] |

> **🟡 AC2: [Validation - ชื่อ scenario]** `[panel: warning]`
>
> | | |
> | --- | --- |
> | **Given** | [invalid input condition] |
> | **When** | [user action] |
> | **Then** | [validation message/behavior] |

> **🔴 AC3: [Error Case - ชื่อ scenario]** `[panel: error]`
>
> | | |
> | --- | --- |
> | **Given** | [error condition] |
> | **When** | [user action] |
> | **Then** | [error handling response] |

---

## 🎯 Scope

| Service | Impact | Notes |
| :--- | :---: | :--- |
| 🔧 Backend | ✅ | [brief note] |
| 🖥️ Admin | ❌ | - |
| 🌐 Website | ✅ | [brief note] |

---

## 📋 Business Rules

| # | Rule | Description |
| :---: | :--- | :--- |
| 1 | **[Rule Name]** | [What the rule enforces] |
| 2 | **[Rule Name]** | [What the rule enforces] |

---

## 🔗 Links

| Type | Link |
| :--- | :--- |
| 🎨 Design | [Figma URL] |
| 📄 Story Doc | [Confluence URL] |
| 📊 Analytics | [Dashboard URL] |
```

---

## Other Fields

| Field | Value |
| :--- | :---: |
| **Issue Type** | Story |
| **Project** | BEP |
| **Epic Link** | [Parent Epic] |
| **Story Points** | [See guide below] |
| **Priority** | [See guide below] |

---

## 📊 Story Points Guide

| Points | Level | Complexity | Typical Work |
| :---: | :---: | :--- | :--- |
| **1** | 🟢 | Very Simple | Config change, copy update |
| **2** | 🟢 | Simple | Single component, clear scope |
| **3** | 🟡 | Medium | Multi-component, some unknowns |
| **5** | 🟡 | Complex | Cross-service, integration |
| **8** | 🟠 | Very Complex | Major feature, high risk |
| **13** | 🔴 | Epic-level | ❌ Consider splitting |

---

## 🚨 Priority Guide

| Level | Icon | When to Use |
| :--- | :---: | :--- |
| **Highest** | 🔴 | Blocker, production issue |
| **High** | 🟠 | Core feature, deadline |
| **Medium** | 🟡 | Standard priority |
| **Low** | 🟢 | Nice-to-have, backlog |

---

## AC Format Options

**Option 1: ADF Panel + Bullet List** (แนะนำ - สวยงามใน Jira)
```json
{
  "type": "panel",
  "attrs": {"panelType": "success"},
  "content": [
    {"type": "paragraph", "content": [{"type": "text", "text": "🟢 AC1: Happy Path", "marks": [{"type": "strong"}]}]},
    {"type": "bulletList", "content": [
      {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Given: [context]"}]}]},
      {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "When: [action]"}]}]},
      {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Then: [outcome]"}]}]}
    ]}
  ]
}
```

**Option 2: Markdown Table Format** (ใช้กับ markdown)
```markdown
> **AC1: [Scenario Name]**
>
> | | |
> | --- | --- |
> | **Given** | [context] |
> | **When** | [action] |
> | **Then** | [outcome] |
```

**Option 3: Inline Format** (กระชับ)
```markdown
> **AC1: [Scenario Name]**
> - **Given** [context]
> - **When** [action]
> - **Then** [outcome]
```

---

## 🎨 ADF Panel Types Reference

| Panel Type | Color | Use Case |
| :--- | :---: | :--- |
| `success` | 🟢 Green | Happy path, positive scenarios |
| `warning` | 🟡 Yellow | Validation, edge cases |
| `error` | 🔴 Red | Error handling, negative scenarios |
| `info` | 🔵 Blue | Informational, context |
| `note` | 🟣 Purple | Important notes, references |

---

## Quality Checklist

Before submit:
- [ ] **INVEST compliant** - Independent, Negotiable, Valuable, Estimable, Small, Testable
- [ ] **Clear user benefit** - "So that" explains value
- [ ] **Testable ACs** - Each AC can be verified
- [ ] **Right size** - 3-8 story points
- [ ] **Links attached** - Design, docs referenced

---

## Writing Style

- **กระชับ** - AC ชัด ไม่เยิ่นเย้อ
- **ทับศัพท์** - scope, validate, response, component
- **เป็นกันเอง** - คุยกับทีม casual

_See `references/shared-config.md` for Language Guidelines_
_See `references/checklists.md` for INVEST criteria_
