# ADF Templates Reference

## Panel Types & Colors

| Panel Type | Color | Usage |
|------------|-------|-------|
| `info` | 🔵 Blue | Story narrative, objective, summary |
| `success` | 🟢 Green | Happy path AC, completed items |
| `warning` | 🟡 Yellow | Edge cases, validation, UI tests |
| `error` | 🔴 Red | Error handling, negative tests |
| `note` | 🟣 Purple | Notes, dependencies, important info |

---

## User Story Template (ADF)

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
            {"type": "tableHeader", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Category"}]}]},
            {"type": "tableHeader", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Details"}]}]}
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
            {"type": "tableHeader", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "#"}]}]},
            {"type": "tableHeader", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "AC"}]}]},
            {"type": "tableHeader", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Scenarios"}]}]}
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
|---------|---------|
| Table inside panel | Use bulletList inside panel |
| Missing `version: 1` | Always include in doc root |
| Using wiki format | Use ADF JSON with acli |
| Nested tables | Flatten or use lists |
| Missing marks array | Use `[{"type": "code"}]` not `"code"` |
