# Task Templates (ADF)

> Extracted from templates.md — used with `/create-task`, `/update-task`
>
> For core rules (CREATE vs EDIT, Panel Types, Styling) → see [templates.md](templates.md)

---

## Task Templates (ADF) - CREATE

> Used with `acli jira workitem create --from-json`

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
            {"type": "text", "text": "[Origin of this task - e.g., found during PR review, code smell, etc.]"}
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
            {"type": "text", "text": "Fix: ", "marks": [{"type": "strong"}]},
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

**Use case:** Bug fixes from QA or production

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
          {"type": "paragraph", "content": [{"type": "text", "text": "[Describe the bug - symptoms, impact]"}]}
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
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[What should happen]"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[What actually happens]"}]}]}
          ]}
        ]
      },
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "🔍 Root Cause"}]},
      {
        "type": "panel",
        "attrs": {"panelType": "note"},
        "content": [
          {"type": "paragraph", "content": [{"type": "text", "text": "[Root cause of the bug - if known, or 'TBD' if not yet determined]"}]}
        ]
      },
      {"type": "rule"},
      {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "✅ Fix Criteria"}]},
      {
        "type": "panel",
        "attrs": {"panelType": "success"},
        "content": [
          {"type": "bulletList", "content": [
            {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[Criteria 1 - bug no longer occurs]"}]}]},
            {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[Criteria 2 - regression tests pass]"}]}]}
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
**Summary:** `[Chore] [Title]`

**Sections (same ADF patterns as tech-debt):**

1. `🎯 Objective` — panel(info): task objective
2. `📋 Tasks` — panel(note): bulletList with ⬜ checkboxes
3. `🔗 Reference` — purple table (same as tech-debt)

---

### spike Template

**Use case:** Research, investigation, POC
**Summary:** `[Spike] [Title]`

**Sections:**

1. `❓ Research Question` — panel(info): main question
2. `📋 Context` — paragraph: background/rationale
3. `🔍 Investigation Areas` — bulletList: topics to study
4. `📝 Findings` — panel(note): *[To be filled after research]*
5. `💡 Recommendations` — panel(success): *[To be filled after research]*
6. `🔗 Reference` — purple table (same as tech-debt)
