# Jira User Story Template

> **Version:** 3.0 | **Updated:** 2026-01-23

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

> **AC1: [Happy Path - ชื่อ scenario]**
>
> | | |
> | --- | --- |
> | **Given** | [precondition - สถานะเริ่มต้น] |
> | **When** | [action - การกระทำของ user] |
> | **Then** | [outcome - ผลลัพธ์ที่คาดหวัง] |

> **AC2: [Validation - ชื่อ scenario]**
>
> | | |
> | --- | --- |
> | **Given** | [invalid input condition] |
> | **When** | [user action] |
> | **Then** | [validation message/behavior] |

> **AC3: [Error Case - ชื่อ scenario]**
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

**Option 1: Table Format** (แนะนำ - อ่านง่าย)
```markdown
> **AC1: [Scenario Name]**
>
> | | |
> | --- | --- |
> | **Given** | [context] |
> | **When** | [action] |
> | **Then** | [outcome] |
```

**Option 2: Inline Format** (กระชับ)
```markdown
> **AC1: [Scenario Name]**
> - **Given** [context]
> - **When** [action]
> - **Then** [outcome]
```

**Option 3: Checklist** (simple cases)
```markdown
- [ ] [Criterion 1]
- [ ] [Criterion 2]
```

---

## Quality Checklist

Before submit:
- [ ] **INVEST compliant** - Independent, Negotiable, Valuable, Estimable, Small, Testable
- [ ] **Clear user benefit** - "So that" explains value
- [ ] **Testable ACs** - Each AC can be verified
- [ ] **Right size** - 3-8 story points
- [ ] **Links attached** - Design, docs referenced

---

_See `references/checklists.md` for INVEST criteria_
