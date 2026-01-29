# ADF Templates Reference

## ⚠️ CREATE vs EDIT - JSON Format ที่ต่างกัน

> **CRITICAL:** JSON สำหรับ create และ edit มี format ต่างกัน ห้ามใช้สลับกัน!

| Operation | Required Fields | Forbidden Fields |
| --- | --- | --- |
| **CREATE** (new issue) | `projectKey`, `type`, `summary`, `description` | `issues` |
| **EDIT** (existing issue) | `issues`, `description` | `projectKey`, `type`, `summary`, `parent` |

### CREATE Example

```json
{
  "projectKey": "BEP",
  "type": "Story",
  "summary": "Feature title",
  "description": { "type": "doc", "version": 1, "content": [...] }
}
```

### EDIT Example

```json
{
  "issues": ["BEP-XXX"],
  "description": { "type": "doc", "version": 1, "content": [...] }
}
```

> **Error Prevention:**
>
> - ถ้าเจอ `Error: json: unknown field "projectKey"` → กำลังใช้ CREATE format กับ EDIT command
> - ถ้าเจอ `Error: json: unknown field "issues"` → กำลังใช้ EDIT format กับ CREATE command

---

## Panel Types & Colors

| Panel Type | Color | Usage |
| --- | --- | --- |
| `info` | 🔵 Blue | Story narrative, objective, summary |
| `success` | 🟢 Green | Happy path AC, completed items |
| `warning` | 🟡 Yellow | Edge cases, validation, UI tests |
| `error` | 🔴 Red | Error handling, negative tests |
| `note` | 🟣 Purple | Notes, dependencies, important info |

---

## ⚠️ Important Rules

| Section | Format | ❌ Never Use |
| --- | --- | --- |
| **Acceptance Criteria** | panels + Given/When/Then | table alone |
| **AC Summary** | table (optional) | - |
| **Fields/Spec** | table | panels |
| **Notes/Dependencies** | panel (note) | table |

### AC Format: Hybrid Approach (Recommended)

**Primary:** panels + Given/When/Then (ต้องมีเสมอ)
**Optional:** AC Summary table (สำหรับ Stories ที่มี AC ≥ 5 ตัว)

**AC Summary Table (ADF):**

```json
{"type": "heading", "attrs": {"level": 3}, "content": [{"type": "text", "text": "📋 AC Summary"}]},
{
  "type": "table",
  "attrs": {"isNumberColumnEnabled": false, "layout": "default"},
  "content": [
    {"type": "tableRow", "content": [
      {"type": "tableHeader", "attrs": {"background": "#f4f5f7"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "ID"}]}]},
      {"type": "tableHeader", "attrs": {"background": "#f4f5f7"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Title"}]}]},
      {"type": "tableHeader", "attrs": {"background": "#f4f5f7"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Type"}]}]},
      {"type": "tableHeader", "attrs": {"background": "#f4f5f7"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Description"}]}]}
    ]},
    {"type": "tableRow", "content": [
      {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "AC-01", "marks": [{"type": "strong"}]}]}]},
      {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "แสดง Fields"}]}]},
      {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "✅ Happy"}]}]},
      {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "ระบบแสดง field ที่เกี่ยวข้องเมื่อเลือกประเภท"}]}]}
    ]},
    {"type": "tableRow", "content": [
      {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "AC-02", "marks": [{"type": "strong"}]}]}]},
      {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Validation ช่องทาง"}]}]},
      {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "⚠️ Edge"}]}]},
      {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "ต้องเลือกช่องทางอย่างน้อย 1 ช่องทาง"}]}]}
    ]}
  ]
},
{"type": "rule"},
{"type": "heading", "attrs": {"level": 3}, "content": [{"type": "text", "text": "📝 AC Details"}]}
```

**Table Design Tips:**

- **ID column:** ใช้ `strong` mark เพื่อเน้น
- **Type column:** ใช้ emoji (✅/⚠️/❌) บอก AC type
- **Description column:** สรุปสั้นๆ 1 บรรทัด
- ตามด้วย `rule` แล้วค่อย panels

> **Rule:** AC Details (panels) ต้องมีเสมอ - Summary table เป็น optional
>
> แม้ข้อมูลเดิม (wiki markup) จะเป็น table ก็ต้องแปลงเป็น panels + Given/When/Then format
>
> - Happy path → `panelType: "success"`
> - Validation/Edge cases → `panelType: "warning"`
> - Error handling → `panelType: "error"`

---

## Table Styling

### Header Background Colors

ใช้ `attrs.background` attribute กับ `tableHeader` เพื่อเพิ่มสีพื้นหลัง:

```json
{"type": "tableHeader", "attrs": {"background": "#f4f5f7"}, "content": [...]}
```

### Atlassian Color Palette

| Color | Hex Code | Usage |
| --- | --- | --- |
| Grey light | `#f4f5f7` | Header rows (default) |
| Blue light | `#e6fcff` | Information highlight |
| Green light | `#e3fcef` | Success/Happy path |
| Yellow light | `#fffae6` | Warning/Edge cases |
| Red light | `#ffebe6` | Error/Critical |
| Purple light | `#eae6ff` | Notes/Special |

### Row Highlighting Example

สำหรับ highlight row สำคัญ (เช่น Total row):

```json
{"type": "tableRow", "content": [
  {"type": "tableCell", "attrs": {"background": "#f4f5f7"}, "content": [...]},
  {"type": "tableCell", "attrs": {"background": "#f4f5f7"}, "content": [...]}
]}
```

---

## Semantic Table Headers (Colored by Category)

> **Concept:** ใช้สี header แยก semantic meaning - มองปุ๊บรู้ประเภททันที

### Color Scheme by Category

| Category | Color | Hex Code | Usage |
| --- | --- | --- | --- |
| **New / Create** | 🟢 Green | `#e3fcef` | Files ที่ต้องสร้างใหม่ |
| **Modify / Change** | 🟡 Yellow | `#fffae6` | Files ที่ต้องแก้ไข |
| **Delete / Remove** | 🔴 Red | `#ffebe6` | Files ที่ต้องลบ |
| **Reference / Info** | 🟣 Purple | `#eae6ff` | Links, dependencies, notes |
| **Requirements** | 🔵 Blue | `#deebff` | Specs, requirements |
| **Default** | ⚪ Grey | `#f4f5f7` | Generic tables |

### ADF Example: Scope Tables with Semantic Colors

**Files (New) - Green Header:**

```json
{"type": "heading", "attrs": {"level": 3}, "content": [{"type": "text", "text": "Files (New)"}]},
{
  "type": "table",
  "attrs": {"isNumberColumnEnabled": false, "layout": "default"},
  "content": [
    {"type": "tableRow", "content": [
      {"type": "tableHeader", "attrs": {"background": "#e3fcef"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "File Path"}]}]},
      {"type": "tableHeader", "attrs": {"background": "#e3fcef"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Description"}]}]}
    ]},
    {"type": "tableRow", "content": [
      {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "src/pages/feature/index.tsx", "marks": [{"type": "code"}]}]}]},
      {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "หน้าหลักของ feature"}]}]}
    ]}
  ]
}
```

**Files (Modify) - Yellow Header:**

```json
{"type": "heading", "attrs": {"level": 3}, "content": [{"type": "text", "text": "Files (Modify)"}]},
{
  "type": "table",
  "attrs": {"isNumberColumnEnabled": false, "layout": "default"},
  "content": [
    {"type": "tableRow", "content": [
      {"type": "tableHeader", "attrs": {"background": "#fffae6"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "File Path"}]}]},
      {"type": "tableHeader", "attrs": {"background": "#fffae6"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Changes"}]}]}
    ]},
    {"type": "tableRow", "content": [
      {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "src/services/auth.service.ts", "marks": [{"type": "code"}]}]}]},
      {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "เพิ่ม API calls สำหรับ feature"}]}]}
    ]}
  ]
}
```

**Reference - Purple Header:**

```json
{
  "type": "table",
  "attrs": {"isNumberColumnEnabled": false, "layout": "default"},
  "content": [
    {"type": "tableRow", "content": [
      {"type": "tableHeader", "attrs": {"background": "#eae6ff"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Type"}]}]},
      {"type": "tableHeader", "attrs": {"background": "#eae6ff"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Link"}]}]}
    ]},
    {"type": "tableRow", "content": [
      {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "User Story"}]}]},
      {"type": "tableCell", "content": [{"type": "paragraph", "content": [
        {"type": "text", "text": "BEP-XXX", "marks": [{"type": "link", "attrs": {"href": "https://100-stars.atlassian.net/browse/BEP-XXX"}}]}
      ]}]}
    ]}
  ]
}
```

### When to Use Semantic Colors

| Section | Recommended Color |
| --- | --- |
| 📁 Scope > Files (New) | 🟢 `#e3fcef` |
| 📁 Scope > Files (Modify) | 🟡 `#fffae6` |
| 📁 Scope > Files (Delete) | 🔴 `#ffebe6` |
| 🔗 Reference | 🟣 `#eae6ff` |
| 📋 Requirements | 🔵 `#deebff` |
| 📊 RICE Score, Metrics | ⚪ `#f4f5f7` (default) |
| 📊 AC Coverage | ⚪ `#f4f5f7` (default) |

> **Tip:** ใช้สี header เดียวกันทั้ง row - ไม่ mix สีใน header row เดียวกัน

---

---

## EDIT Template (All Issue Types)

> ใช้กับ `acli jira workitem edit --from-json ... --yes`

**สำหรับ update description ของ issue ที่มีอยู่แล้ว** - ใช้ format เดียวกันทุก issue type

```json
{
  "issues": ["BEP-XXX"],
  "description": {
    "type": "doc",
    "version": 1,
    "content": [
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "Section Title"}]},
      {
        "type": "panel",
        "attrs": {"panelType": "info"},
        "content": [
          {"type": "paragraph", "content": [{"type": "text", "text": "Content here..."}]}
        ]
      }
    ]
  }
}
```

**⚠️ สิ่งที่ห้ามใส่ใน EDIT JSON:**

- ❌ `projectKey` - Error: unknown field
- ❌ `type` - Error: unknown field
- ❌ `summary` - Error: unknown field (ใช้ MCP `jira_update_issue` แทน)
- ❌ `parent` - Error: unknown field

**Update summary/fields อื่นๆ (ไม่ใช่ description):**

```typescript
// ใช้ MCP แทน acli
jira_update_issue({
  issue_key: "BEP-XXX",
  fields: { summary: "New Summary" }
})
```

---

## Inline Code Examples

**File path:**

```json
{"type": "text", "text": "src/pages/coupon/index.tsx", "marks": [{"type": "code"}]}
```

**Route:**

```json
{"type": "text", "text": "/coupon/topup-credit", "marks": [{"type": "code"}]}
```

**Component:**

```json
{"type": "text", "text": "CouponCard", "marks": [{"type": "code"}]}
```

**Combined text:**

```json
{"type": "paragraph", "content": [
  {"type": "text", "text": "Navigate to "},
  {"type": "text", "text": "/coupon", "marks": [{"type": "code"}]},
  {"type": "text", "text": " page"}
]}
```

---

## Common Mistakes

| Mistake | Correct |
| --- | --- |
| Table inside panel | Use bulletList inside panel |
| Using `projectKey` in EDIT JSON | Remove - only use `issues` array |
| Using `issues` in CREATE JSON | Remove - use `projectKey`, `type`, `summary` |
| `Error: unknown field "projectKey"` | You're using CREATE format with EDIT command |
| Missing `version: 1` | Always include in doc root |
| Using wiki format | Use ADF JSON with acli |
| Nested tables | Flatten or use lists |
| Nested bulletList (listItem > bulletList) | Flatten to single list or use comma-separated text |
| Missing marks array | Use `[{"type": "code"}]` not `"code"` |

---

## Issue Type Templates (Separate Files)

> Full ADF JSON templates แยกตาม issue type — load เฉพาะที่ต้องการ

| Template File | Content | Used By |
| --- | --- | --- |
| [templates-epic.md](templates-epic.md) | Epic ADF (CREATE) | `/create-epic`, `/update-epic` |
| [templates-story.md](templates-story.md) | Story ADF (CREATE) | `/create-story`, `/update-story`, `/story-full` |
| [templates-subtask.md](templates-subtask.md) | Sub-task + QA ADF (TWO-STEP) | `/analyze-story`, `/update-subtask`, `/create-testplan`, `/story-full` |
| [templates-task.md](templates-task.md) | Task ADF: tech-debt, bug, chore, spike (CREATE) | `/create-task`, `/update-task` |
