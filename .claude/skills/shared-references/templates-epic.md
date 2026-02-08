# Epic Template (ADF)

> **Prerequisite:** Read [templates-core.md](templates-core.md) for CREATE/EDIT rules, panel types, styling

## Epic Best Practices

**Naming:** `[Domain] — [Deliverable]` (never include version/phase e.g. "Phase 1", "v2")

**Size:** 8-15 stories, 2-6 months — if spanning 3+ sprints + multi-layer scope → split

**When to Split:** >15 tickets | multiple domains in one epic | can't track progress | mixed concerns

**How to Split:** By user persona | By delivery layer | By ordered process (VS1→VS2) | min 5 tickets per epic

**Lifecycle:** Close when done → create new Epic | Review scope every sprint planning

## Epic Template (ADF) - CREATE

> Used with `acli jira workitem create --from-json`
>
> **Content Budget** → see [writing-style.md](writing-style.md#content-budget-per-section)

**Structure:** (⚡ = optional, include only when real data exists)

- 🎯 Epic Overview (info) — **3 lines max** (Problem → Summary → Supports)
- 💰 Business Value (success) — **3 bullets max**
- 📦 Scope (info) — **1 line/item, no description needed**
- 📊 RICE Score (table) — ⚡ skip if priority is already clear
- 🎯 Success Metrics (table) — ⚡ skip if metrics not yet defined
- 📋 User Stories (panels) — **list + link only**
- 📈 Progress (note) — auto counts
- 🔗 Links (table)

```json
{
  "projectKey": "{{PROJECT_KEY}}",
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
            {"type": "text", "text": "Problem: ", "marks": [{"type": "strong"}]},
            {"type": "text", "text": "[สถานการณ์ปัจจุบัน] → [ปัญหา] → [Epic นี้แก้ปัญหาโดย...]"}
          ]},
          {"type": "paragraph", "content": [
            {"type": "text", "text": "[Develop system X for Y]", "marks": [{"type": "strong"}]}
          ]},
          {"type": "paragraph", "content": [
            {"type": "text", "text": "[Supports: feature1, feature2, feature3]"}
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
            {"type": "text", "text": "{{PROJECT_KEY}}-XXX", "marks": [{"type": "strong"}]},
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
            {"type": "tableHeader", "attrs": {"background": "#eae6ff"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Type"}]}]},
            {"type": "tableHeader", "attrs": {"background": "#eae6ff"}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Link"}]}]}
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

**Panels:** Overview/Scope=`info`, Business Value=`success`, Progress=`note`, Canceled=`warning`
