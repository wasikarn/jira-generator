# Task Templates (ADF)

> Extracted from templates.md — ใช้กับ `/create-task`, `/update-task`
>
> สำหรับ core rules (CREATE vs EDIT, Panel Types, Styling) → ดู [templates.md](templates.md)

---

## Task Templates (ADF) - CREATE

> ใช้กับ `acli jira workitem create --from-json`

### tech-debt Template

**Use case:** PR review issues, code improvements, refactoring

```json
{
  "projectKey": "BEP",
  "type": "Task",
  "summary": "[BE] [Title] - [Context]",
  "description": {
    "type": "doc",
    "version": 1,
    "content": [
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "📋 Context"}]},
      {
        "type": "panel",
        "attrs": {"panelType": "info"},
        "content": [
          {"type": "paragraph", "content": [
            {"type": "text", "text": "[ที่มาของ task - เช่น พบจาก PR review, code smell, etc.]"}
          ]}
        ]
      },
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "🔴 HIGH Priority"}]},
      {
        "type": "panel",
        "attrs": {"panelType": "error"},
        "content": [
          {"type": "paragraph", "content": [{"type": "text", "text": "1. [Issue title]", "marks": [{"type": "strong"}]}]},
          {"type": "paragraph", "content": [
            {"type": "text", "text": "File: ", "marks": [{"type": "strong"}]},
            {"type": "text", "text": "path/to/file.ts", "marks": [{"type": "code"}]}
          ]},
          {"type": "paragraph", "content": [{"type": "text", "text": "[Description of issue]"}]},
          {"type": "paragraph", "content": [
            {"type": "text", "text": "แก้ไข: ", "marks": [{"type": "strong"}]},
            {"type": "text", "text": "[How to fix]"}
          ]}
        ]
      },
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "🟡 MEDIUM Priority"}]},
      {
        "type": "panel",
        "attrs": {"panelType": "warning"},
        "content": [
          {"type": "paragraph", "content": [{"type": "text", "text": "2. [Issue title]", "marks": [{"type": "strong"}]}]},
          {"type": "paragraph", "content": [{"type": "text", "text": "[Description and fix]"}]}
        ]
      },
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "🟣 LOW Priority"}]},
      {
        "type": "panel",
        "attrs": {"panelType": "note"},
        "content": [
          {"type": "paragraph", "content": [{"type": "text", "text": "3. [Issue title]", "marks": [{"type": "strong"}]}]},
          {"type": "paragraph", "content": [{"type": "text", "text": "[Description and fix]"}]}
        ]
      },
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "✅ Acceptance Criteria"}]},
      {
        "type": "table",
        "attrs": {"isNumberColumnEnabled": false, "layout": "default"},
        "content": [
          {"type": "tableRow", "content": [
            {"type": "tableHeader", "attrs": {"background": "#f4f5f7"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "#"}]}]},
            {"type": "tableHeader", "attrs": {"background": "#f4f5f7"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Priority"}]}]},
            {"type": "tableHeader", "attrs": {"background": "#f4f5f7"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Criteria"}]}]},
            {"type": "tableHeader", "attrs": {"background": "#f4f5f7"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Status"}]}]}
          ]},
          {"type": "tableRow", "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "1", "marks": [{"type": "strong"}]}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "🔴 HIGH"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[Criteria description]"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "⬜"}]}]}
          ]}
        ]
      },
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "🔗 Reference"}]},
      {
        "type": "table",
        "attrs": {"isNumberColumnEnabled": false, "layout": "default"},
        "content": [
          {"type": "tableRow", "content": [
            {"type": "tableHeader", "attrs": {"background": "#eae6ff"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Type"}]}]},
            {"type": "tableHeader", "attrs": {"background": "#eae6ff"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Link"}]}]}
          ]},
          {"type": "tableRow", "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Related Issue"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [
              {"type": "text", "text": "BEP-XXX", "marks": [{"type": "link", "attrs": {"href": "https://100-stars.atlassian.net/browse/BEP-XXX"}}]}
            ]}]}
          ]}
        ]
      }
    ]
  }
}
```

---

### bug Template

**Use case:** Bug fixes จาก QA หรือ production

```json
{
  "projectKey": "BEP",
  "type": "Task",
  "summary": "[Bug] [Title]",
  "description": {
    "type": "doc",
    "version": 1,
    "content": [
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "🐛 Bug Description"}]},
      {
        "type": "panel",
        "attrs": {"panelType": "error"},
        "content": [
          {"type": "paragraph", "content": [{"type": "text", "text": "[อธิบาย bug ที่พบ - อาการ, ผลกระทบ]"}]}
        ]
      },
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "🔄 Reproduction Steps"}]},
      {"type": "orderedList", "content": [
        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[Step 1]"}]}]},
        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[Step 2]"}]}]},
        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[Step 3]"}]}]}
      ]},
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "📊 Expected vs Actual"}]},
      {
        "type": "table",
        "attrs": {"isNumberColumnEnabled": false, "layout": "default"},
        "content": [
          {"type": "tableRow", "content": [
            {"type": "tableHeader", "attrs": {"background": "#e3fcef"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Expected"}]}]},
            {"type": "tableHeader", "attrs": {"background": "#ffebe6"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Actual"}]}]}
          ]},
          {"type": "tableRow", "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[สิ่งที่ควรเกิดขึ้น]"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[สิ่งที่เกิดขึ้นจริง]"}]}]}
          ]}
        ]
      },
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "🔍 Root Cause"}]},
      {
        "type": "panel",
        "attrs": {"panelType": "note"},
        "content": [
          {"type": "paragraph", "content": [{"type": "text", "text": "[สาเหตุของ bug - ถ้าทราบ หรือ 'TBD' ถ้ายังไม่ทราบ]"}]}
        ]
      },
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "✅ Fix Criteria"}]},
      {
        "type": "panel",
        "attrs": {"panelType": "success"},
        "content": [
          {"type": "bulletList", "content": [
            {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[Criteria 1 - bug ไม่เกิดอีก]"}]}]},
            {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[Criteria 2 - regression test ผ่าน]"}]}]}
          ]}
        ]
      },
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "🔗 Reference"}]},
      {
        "type": "table",
        "attrs": {"isNumberColumnEnabled": false, "layout": "default"},
        "content": [
          {"type": "tableRow", "content": [
            {"type": "tableHeader", "attrs": {"background": "#eae6ff"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Type"}]}]},
            {"type": "tableHeader", "attrs": {"background": "#eae6ff"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Link"}]}]}
          ]},
          {"type": "tableRow", "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "QA Report"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[Link to report/video]"}]}]}
          ]}
        ]
      }
    ]
  }
}
```

---

### chore Template

**Use case:** Maintenance, dependency updates, configs

```json
{
  "projectKey": "BEP",
  "type": "Task",
  "summary": "[Chore] [Title]",
  "description": {
    "type": "doc",
    "version": 1,
    "content": [
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "🎯 Objective"}]},
      {
        "type": "panel",
        "attrs": {"panelType": "info"},
        "content": [
          {"type": "paragraph", "content": [{"type": "text", "text": "[วัตถุประสงค์ของ task นี้]"}]}
        ]
      },
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "📋 Tasks"}]},
      {
        "type": "panel",
        "attrs": {"panelType": "note"},
        "content": [
          {"type": "bulletList", "content": [
            {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "⬜ [Task 1]"}]}]},
            {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "⬜ [Task 2]"}]}]},
            {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "⬜ [Task 3]"}]}]}
          ]}
        ]
      },
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "🔗 Reference"}]},
      {
        "type": "table",
        "attrs": {"isNumberColumnEnabled": false, "layout": "default"},
        "content": [
          {"type": "tableRow", "content": [
            {"type": "tableHeader", "attrs": {"background": "#eae6ff"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Type"}]}]},
            {"type": "tableHeader", "attrs": {"background": "#eae6ff"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Link"}]}]}
          ]},
          {"type": "tableRow", "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Docs"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[Link to relevant docs]"}]}]}
          ]}
        ]
      }
    ]
  }
}
```

---

### spike Template

**Use case:** Research, investigation, POC

```json
{
  "projectKey": "BEP",
  "type": "Task",
  "summary": "[Spike] [Title]",
  "description": {
    "type": "doc",
    "version": 1,
    "content": [
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "❓ Research Question"}]},
      {
        "type": "panel",
        "attrs": {"panelType": "info"},
        "content": [
          {"type": "paragraph", "content": [{"type": "text", "text": "[คำถามหลักที่ต้องการหาคำตอบ]"}]}
        ]
      },
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "📋 Context"}]},
      {"type": "paragraph", "content": [{"type": "text", "text": "[ที่มาและความเป็นมา ทำไมต้อง research เรื่องนี้]"}]},
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "🔍 Investigation Areas"}]},
      {"type": "bulletList", "content": [
        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[Area 1 - สิ่งที่ต้องศึกษา]"}]}]},
        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[Area 2 - สิ่งที่ต้องทดสอบ]"}]}]},
        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[Area 3 - สิ่งที่ต้องเปรียบเทียบ]"}]}]}
      ]},
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "📝 Findings"}]},
      {
        "type": "panel",
        "attrs": {"panelType": "note"},
        "content": [
          {"type": "paragraph", "content": [{"type": "text", "text": "[จะเติมหลังจาก research เสร็จ]", "marks": [{"type": "em"}]}]}
        ]
      },
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "💡 Recommendations"}]},
      {
        "type": "panel",
        "attrs": {"panelType": "success"},
        "content": [
          {"type": "paragraph", "content": [{"type": "text", "text": "[จะเติมหลังจาก research เสร็จ]", "marks": [{"type": "em"}]}]}
        ]
      },
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "🔗 Reference"}]},
      {
        "type": "table",
        "attrs": {"isNumberColumnEnabled": false, "layout": "default"},
        "content": [
          {"type": "tableRow", "content": [
            {"type": "tableHeader", "attrs": {"background": "#eae6ff"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Type"}]}]},
            {"type": "tableHeader", "attrs": {"background": "#eae6ff"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Link"}]}]}
          ]},
          {"type": "tableRow", "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Docs"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[Official documentation]"}]}]}
          ]}
        ]
      }
    ]
  }
}
```
