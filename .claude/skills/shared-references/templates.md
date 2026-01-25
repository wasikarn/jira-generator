# ADF Templates Reference

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

## Epic Template (ADF)

**Structure:**

- 🎯 Epic Overview (panel: info)
- 💰 Business Value (panel: success)
- 📦 Scope (panel: info + table)
- 📊 RICE Score (table)
- 🎯 Success Metrics (table)
- 📋 User Stories (panels by group)
- 📈 Progress (panel: note)
- 🔗 Links (table)

```json
{
  "projectKey": "BEP",
  "type": "Epic",
  "summary": "[Epic Name] Phase X",
  "description": {
    "type": "doc",
    "version": 1,
    "content": [
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "🎯 Epic Overview"}]},
      {
        "type": "panel",
        "attrs": {"panelType": "info"},
        "content": [
          {"type": "paragraph", "content": [
            {"type": "text", "text": "[พัฒนาระบบ X เพื่อ Y]", "marks": [{"type": "strong"}]}
          ]},
          {"type": "paragraph", "content": [
            {"type": "text", "text": "[รองรับ: feature1, feature2, feature3]"}
          ]}
        ]
      },
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "💰 Business Value"}]},
      {
        "type": "panel",
        "attrs": {"panelType": "success"},
        "content": [
          {"type": "paragraph", "content": [
            {"type": "text", "text": "Revenue: ", "marks": [{"type": "strong"}]},
            {"type": "text", "text": "[benefit 1]"}
          ]},
          {"type": "paragraph", "content": [
            {"type": "text", "text": "Retention: ", "marks": [{"type": "strong"}]},
            {"type": "text", "text": "[benefit 2]"}
          ]},
          {"type": "paragraph", "content": [
            {"type": "text", "text": "Operations: ", "marks": [{"type": "strong"}]},
            {"type": "text", "text": "[benefit 3]"}
          ]}
        ]
      },
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "📦 Scope"}]},
      {
        "type": "panel",
        "attrs": {"panelType": "info"},
        "content": [
          {"type": "paragraph", "content": [
            {"type": "text", "text": "1. [Feature/Module 1]", "marks": [{"type": "strong"}]},
            {"type": "text", "text": " - [description]"}
          ]},
          {"type": "paragraph", "content": [
            {"type": "text", "text": "2. [Feature/Module 2]", "marks": [{"type": "strong"}]},
            {"type": "text", "text": " - [description]"}
          ]}
        ]
      },
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "📊 RICE Score"}]},
      {
        "type": "table",
        "attrs": {"isNumberColumnEnabled": false, "layout": "default"},
        "content": [
          {"type": "tableRow", "content": [
            {"type": "tableHeader", "attrs": {"background": "#f4f5f7"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Factor"}]}]},
            {"type": "tableHeader", "attrs": {"background": "#f4f5f7"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Score"}]}]},
            {"type": "tableHeader", "attrs": {"background": "#f4f5f7"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Rationale"}]}]}
          ]},
          {"type": "tableRow", "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Reach"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[number]"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[rationale]"}]}]}
          ]},
          {"type": "tableRow", "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Impact"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[1-3]"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[rationale]"}]}]}
          ]},
          {"type": "tableRow", "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Confidence"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[%]"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[rationale]"}]}]}
          ]},
          {"type": "tableRow", "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Effort"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[weeks]"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[stories count]"}]}]}
          ]},
          {"type": "tableRow", "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "RICE Score", "marks": [{"type": "strong"}]}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[score]", "marks": [{"type": "strong"}]}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "(R × I × C) / E"}]}]}
          ]}
        ]
      },
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "🎯 Success Metrics"}]},
      {
        "type": "table",
        "attrs": {"isNumberColumnEnabled": false, "layout": "default"},
        "content": [
          {"type": "tableRow", "content": [
            {"type": "tableHeader", "attrs": {"background": "#f4f5f7"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Metric"}]}]},
            {"type": "tableHeader", "attrs": {"background": "#f4f5f7"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Target"}]}]},
            {"type": "tableHeader", "attrs": {"background": "#f4f5f7"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Measurement"}]}]}
          ]},
          {"type": "tableRow", "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[Metric 1]"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[target]"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[how to measure]"}]}]}
          ]}
        ]
      },
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "📋 User Stories"}]},
      {"type": "heading", "attrs": {"level": 3}, "content": [{"type": "text", "text": "🔨 [Group 1]"}]},
      {
        "type": "panel",
        "attrs": {"panelType": "info"},
        "content": [
          {"type": "paragraph", "content": [
            {"type": "text", "text": "BEP-XXX", "marks": [{"type": "strong"}]},
            {"type": "text", "text": " - [Story title]"}
          ]}
        ]
      },
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "📈 Progress"}]},
      {
        "type": "panel",
        "attrs": {"panelType": "note"},
        "content": [
          {"type": "paragraph", "content": [
            {"type": "text", "text": "✅ Done: ", "marks": [{"type": "strong"}]},
            {"type": "text", "text": "X (Y%)"}
          ]},
          {"type": "paragraph", "content": [
            {"type": "text", "text": "🟡 In Progress: ", "marks": [{"type": "strong"}]},
            {"type": "text", "text": "X (Y%)"}
          ]},
          {"type": "paragraph", "content": [
            {"type": "text", "text": "⚪ To Do: ", "marks": [{"type": "strong"}]},
            {"type": "text", "text": "X (Y%)"}
          ]},
          {"type": "paragraph", "content": [
            {"type": "text", "text": "Total: X stories", "marks": [{"type": "strong"}]}
          ]}
        ]
      },
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "🔗 Links"}]},
      {
        "type": "table",
        "attrs": {"isNumberColumnEnabled": false, "layout": "default"},
        "content": [
          {"type": "tableRow", "content": [
            {"type": "tableHeader", "attrs": {"background": "#f4f5f7"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Type"}]}]},
            {"type": "tableHeader", "attrs": {"background": "#f4f5f7"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Link"}]}]}
          ]},
          {"type": "tableRow", "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Epic Doc"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [
              {"type": "text", "text": "Confluence", "marks": [{"type": "link", "attrs": {"href": "[URL]"}}]}
            ]}]}
          ]}
        ]
      }
    ]
  }
}
```

**Panel Usage in Epic:**

| Section | Panel Type | Purpose |
| --- | --- | --- |
| Overview | `info` | Summary of what epic delivers |
| Business Value | `success` | Benefits/outcomes |
| Scope | `info` | Features/modules included |
| Progress | `note` | Status tracking |
| Canceled | `warning` | Out of scope items |

---

## User Story Template (ADF)

**Note:** สำหรับ Stories ที่มี AC ≥ 5 ตัว อาจเพิ่ม AC Summary table ก่อน panels (ดู Important Rules)

```json
{
  "projectKey": "BEP",
  "type": "Story",
  "summary": "[Feature Name] - Thai Description",
  "description": {
    "type": "doc",
    "version": 1,
    "content": [
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "User Story"}]},
      {
        "type": "panel",
        "attrs": {"panelType": "info"},
        "content": [
          {"type": "paragraph", "content": [
            {"type": "text", "text": "As a ", "marks": [{"type": "strong"}]},
            {"type": "text", "text": "[persona]"},
            {"type": "text", "text": ","}
          ]},
          {"type": "paragraph", "content": [
            {"type": "text", "text": "I want to ", "marks": [{"type": "strong"}]},
            {"type": "text", "text": "[action]"},
            {"type": "text", "text": ","}
          ]},
          {"type": "paragraph", "content": [
            {"type": "text", "text": "So that ", "marks": [{"type": "strong"}]},
            {"type": "text", "text": "[benefit]"}
          ]}
        ]
      },
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "Acceptance Criteria"}]},
      {
        "type": "panel",
        "attrs": {"panelType": "success"},
        "content": [
          {"type": "paragraph", "content": [{"type": "text", "text": "AC1: [Title]", "marks": [{"type": "strong"}]}]},
          {"type": "bulletList", "content": [
            {"type": "listItem", "content": [{"type": "paragraph", "content": [
              {"type": "text", "text": "Given: ", "marks": [{"type": "strong"}]},
              {"type": "text", "text": "[precondition]"}
            ]}]},
            {"type": "listItem", "content": [{"type": "paragraph", "content": [
              {"type": "text", "text": "When: ", "marks": [{"type": "strong"}]},
              {"type": "text", "text": "[action]"}
            ]}]},
            {"type": "listItem", "content": [{"type": "paragraph", "content": [
              {"type": "text", "text": "Then: ", "marks": [{"type": "strong"}]},
              {"type": "text", "text": "[result]"}
            ]}]}
          ]}
        ]
      }
    ]
  }
}
```

---

## Sub-task Template (ADF)

```json
{
  "projectKey": "BEP",
  "type": "Subtask",
  "parent": "BEP-XXX",
  "summary": "[TAG] - Description",
  "description": {
    "type": "doc",
    "version": 1,
    "content": [
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "📖 Story Narrative"}]},
      {
        "type": "panel",
        "attrs": {"panelType": "info"},
        "content": [
          {"type": "paragraph", "content": [
            {"type": "text", "text": "As a ", "marks": [{"type": "strong"}]},
            {"type": "text", "text": "[persona], "},
            {"type": "text", "text": "I want to ", "marks": [{"type": "strong"}]},
            {"type": "text", "text": "[action], "},
            {"type": "text", "text": "So that ", "marks": [{"type": "strong"}]},
            {"type": "text", "text": "[benefit]."}
          ]}
        ]
      },
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "🎯 Objective"}]},
      {"type": "paragraph", "content": [{"type": "text", "text": "[What and why - 1-2 sentences]"}]},
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "📁 Scope"}]},
      {
        "type": "table",
        "attrs": {"isNumberColumnEnabled": false, "layout": "default"},
        "content": [
          {"type": "tableRow", "content": [
            {"type": "tableHeader", "attrs": {"background": "#f4f5f7"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Category"}]}]},
            {"type": "tableHeader", "attrs": {"background": "#f4f5f7"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Details"}]}]}
          ]},
          {"type": "tableRow", "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Files"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [
              {"type": "text", "text": "src/pages/feature/index.tsx", "marks": [{"type": "code"}]}
            ]}]}
          ]}
        ]
      },
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "✅ Acceptance Criteria"}]},
      {
        "type": "panel",
        "attrs": {"panelType": "success"},
        "content": [
          {"type": "paragraph", "content": [{"type": "text", "text": "AC1: [Happy Path]", "marks": [{"type": "strong"}]}]},
          {"type": "bulletList", "content": [
            {"type": "listItem", "content": [{"type": "paragraph", "content": [
              {"type": "text", "text": "Given: ", "marks": [{"type": "strong"}]},
              {"type": "text", "text": "[precondition]"}
            ]}]},
            {"type": "listItem", "content": [{"type": "paragraph", "content": [
              {"type": "text", "text": "When: ", "marks": [{"type": "strong"}]},
              {"type": "text", "text": "[action]"}
            ]}]},
            {"type": "listItem", "content": [{"type": "paragraph", "content": [
              {"type": "text", "text": "Then: ", "marks": [{"type": "strong"}]},
              {"type": "text", "text": "[result]"}
            ]}]}
          ]}
        ]
      }
    ]
  }
}
```

---

## QA Test Case Template (ADF)

**Important:** ใช้ bulletList ใน panel (ไม่ใช้ nested table)

```json
{
  "projectKey": "BEP",
  "type": "Subtask",
  "parent": "BEP-XXX",
  "summary": "[QA] - Test: [Feature Name]",
  "description": {
    "type": "doc",
    "version": 1,
    "content": [
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "🎯 Test Objective"}]},
      {
        "type": "panel",
        "attrs": {"panelType": "info"},
        "content": [
          {"type": "paragraph", "content": [{"type": "text", "text": "[What this test validates]"}]}
        ]
      },
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "📊 AC Coverage"}]},
      {
        "type": "table",
        "attrs": {"isNumberColumnEnabled": false, "layout": "default"},
        "content": [
          {"type": "tableRow", "content": [
            {"type": "tableHeader", "attrs": {"background": "#f4f5f7"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "#"}]}]},
            {"type": "tableHeader", "attrs": {"background": "#f4f5f7"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "AC"}]}]},
            {"type": "tableHeader", "attrs": {"background": "#f4f5f7"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Scenarios"}]}]}
          ]},
          {"type": "tableRow", "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "1"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[AC1 desc]"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "TC1, TC2"}]}]}
          ]}
        ]
      },
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "🧪 Test Cases"}]},
      {
        "type": "panel",
        "attrs": {"panelType": "success"},
        "content": [
          {"type": "paragraph", "content": [{"type": "text", "text": "TC1: [Happy Path Test]", "marks": [{"type": "strong"}]}]},
          {"type": "bulletList", "content": [
            {"type": "listItem", "content": [{"type": "paragraph", "content": [
              {"type": "text", "text": "AC: 1 | Priority: 🟠 High"}
            ]}]},
            {"type": "listItem", "content": [{"type": "paragraph", "content": [
              {"type": "text", "text": "Given: ", "marks": [{"type": "strong"}]},
              {"type": "text", "text": "[precondition]"}
            ]}]},
            {"type": "listItem", "content": [{"type": "paragraph", "content": [
              {"type": "text", "text": "When: ", "marks": [{"type": "strong"}]},
              {"type": "text", "text": "[action]"}
            ]}]},
            {"type": "listItem", "content": [{"type": "paragraph", "content": [
              {"type": "text", "text": "Then: ", "marks": [{"type": "strong"}]},
              {"type": "text", "text": "[expected result]"}
            ]}]}
          ]}
        ]
      },
      {
        "type": "panel",
        "attrs": {"panelType": "warning"},
        "content": [
          {"type": "paragraph", "content": [{"type": "text", "text": "TC2: [Edge Case Test]", "marks": [{"type": "strong"}]}]},
          {"type": "bulletList", "content": [
            {"type": "listItem", "content": [{"type": "paragraph", "content": [
              {"type": "text", "text": "AC: 2 | Priority: 🟡 Medium"}
            ]}]},
            {"type": "listItem", "content": [{"type": "paragraph", "content": [
              {"type": "text", "text": "Given: ", "marks": [{"type": "strong"}]},
              {"type": "text", "text": "[edge condition]"}
            ]}]},
            {"type": "listItem", "content": [{"type": "paragraph", "content": [
              {"type": "text", "text": "When: ", "marks": [{"type": "strong"}]},
              {"type": "text", "text": "[action]"}
            ]}]},
            {"type": "listItem", "content": [{"type": "paragraph", "content": [
              {"type": "text", "text": "Then: ", "marks": [{"type": "strong"}]},
              {"type": "text", "text": "[expected result]"}
            ]}]}
          ]}
        ]
      }
    ]
  }
}
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
| Missing `version: 1` | Always include in doc root |
| Using wiki format | Use ADF JSON with acli |
| Nested tables | Flatten or use lists |
| Missing marks array | Use `[{"type": "code"}]` not `"code"` |
