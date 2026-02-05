# Story Template (ADF)

> Extracted from templates.md — used with `/create-story`, `/update-story`, `/story-full`
>
> For core rules (CREATE vs EDIT, Panel Types, Styling) → see [templates.md](templates.md)
>
> **Content Budget** → see [writing-style.md](writing-style.md#content-budget-per-section)

---

## User Story Template (ADF) - CREATE

> Used with `acli jira workitem create --from-json`

**Density rules:**

- Narrative: **3 lines** (As a / I want / So that) — no additional explanatory paragraphs
- AC: **max 5 panels** — if >5, split story (SPIDR)
- Each AC: **3 bullets** (Given/When/Then) + optional And — no prose
- Reference: ⚡ **skip** if no Figma/external link

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
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Epic"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [
              {"type": "text", "text": "BEP-XXX", "marks": [{"type": "link", "attrs": {"href": "https://100-stars.atlassian.net/browse/BEP-XXX"}}]}
            ]}]}
          ]},
          {"type": "tableRow", "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Figma"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [
              {"type": "text", "text": "Design", "marks": [{"type": "link", "attrs": {"href": "[Figma URL]"}}]}
            ]}]}
          ]}
        ]
      }
    ]
  }
}
```
