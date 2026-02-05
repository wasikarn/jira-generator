# Writing Style Guide

## Language Rules

### Thai + Transliteration

**Principle:** Main content in Thai, technical terms in English

| Content Type | Language | Example |
| --- | --- | --- |
| User Story narrative | Thai | "Admin wants to view coupon list" |
| AC descriptions | Thai | "When clicking the Submit button" |
| Technical terms | English | endpoint, payload, component |
| File paths | English | `src/pages/coupon/index.tsx` |
| Code/Routes | English | `/api/coupons`, `getCoupons()` |

### Commonly Used Transliterations

| Thai | English (keep as-is) |
| --- | --- |
| - | endpoint |
| - | payload |
| - | validate |
| - | component |
| - | service |
| - | API |
| - | route |
| - | model |
| - | schema |
| - | query |
| - | filter |
| - | response |
| - | request |

### Correct Examples

**Good:**

```text
Given: Admin enters the `/coupon` page
When: Clicks "Top-up Credit Coupon"
Then: Navigates to `/coupon/topup-credit`
```

**Bad:**

```text
Given: Admin enters the coupon page  (❌ all English - no route reference)
When: Click "Top-up Credit Coupon"
Then: Navigate to topup credit page
```

---

## Tone & Style

> **3 Principles:** Concise (cut excess words) · Casual (talk like a teammate) · Clear (specific + testable)

| ❌ Verbose | ✅ Concise |
| --- | --- |
| The system shall render and display a total of 3 card types in accordance with the approved design specifications | Display 3 card types per design |
| Upon successful completion of page loading, the user shall be able to observe 3 card items rendered on screen | AC1: Display - Page loads and shows 3 cards |
| Then: Show an appropriate error | Then: Show error "Please enter an amount" |

---

## Scan-First Principle

Team will **scan before reading** — design content to be scannable in 5 seconds

1. **Bold keywords first** — `**Given:** precondition` not long prose
2. **Bullets > Paragraphs** — no long paragraphs, use bullet points
3. **Tables > Lists** — if 2+ columns of data, use table
4. **Skip if empty** — if a section has no real data, don't add placeholder

---

## Content Budget (per section)

> Agent **must** write within this budget — if exceeded, cut or split

| Issue Type | Section | Budget |
| --- | --- | --- |
| **Epic** | Overview | 2 sentences |
| | Business Value | 3 bullets (Revenue/Retention/Ops) |
| | Scope | 1 line/item, no description needed |
| | RICE | ⚡ optional — skip if priority is already clear |
| | Success Metrics | ⚡ optional — skip if metrics not yet defined |
| | User Stories | list + link only, no description |
| | Progress | auto counts, don't write manually |
| **Story** | Narrative | 3 lines (As a / I want / So that) |
| | AC panels | max 5 panels — if >5, split story |
| | Each AC | 3 bullets (Given/When/Then) + optional And |
| | Reference | ⚡ skip if no Figma/external link |
| **Sub-task** | Objective | 1 sentence |
| | Scope table | only files that change, max 10 rows |
| | AC panels | max 3 panels |
| | Reference | ⚡ skip if parent story has all links |
| **QA** ⚡ | Test Objective | 1 sentence |
| | Test Cases | max 8 cases — if >8, split QA ticket |

**⚡ = optional** — section or issue type included only when needed (QA ticket not required for every story)

---

## ADF Formatting

### Inline Code

Use inline code for:

- File paths: `src/pages/coupon/index.tsx`
- Routes: `/coupon/topup-credit`
- Component names: `CouponCard`
- Function names: `getCoupons()`
- Config keys: `COUPON_TYPES`

**ADF Mark:**

```json
{"type": "text", "text": "/coupon/topup-credit", "marks": [{"type": "code"}]}
```

### Bold Text

Use bold for:

- Labels: **Given**, **When**, **Then**
- Emphasis: **important**
- Section headers in content

**ADF Mark:**

```json
{"type": "text", "text": "Given:", "marks": [{"type": "strong"}]}
```

---

## Summary Format

### User Story

```text
[Service Tag] - [Description] ([English feature name])
```

Examples:

- ✅ `[FE-Admin] - Create coupon menu page (Coupon Menu)`
- ✅ `[BE] - Add API filter coupons`
- ❌ `Create coupon menu page` (no tag, English only)
- ❌ `[BE] - Build API` (not specific enough)

### Sub-task

```text
[TAG] - [Brief description]
```

Tags: `[BE]`, `[FE-Admin]`, `[FE-Web]`

### QA Sub-task

```text
[QA] - Test: [Story title or feature name]
```

---

## Vertical Slice Labels

> Convention from Sprint 32 — used with Jira labels for board filtering

| Pattern | When to use | Example |
| --- | --- | --- |
| `vs{N}-{name}` | Numbered vertical slice | `vs1-skeleton`, `vs2-credit-e2e` |
| `vs-enabler` | Shared component used by multiple slices | Side Panel, Toast |
| `{feature}-{scope}` | Cross-cutting concern | `coupon-web`, `ad-integration` |

**Rules:** Every story must have a feature label (`coupon-web`) + at least 1 VS label / 1 story may have multiple VS labels

---

## Common Mistakes

| Mistake | Correct |
| --- | --- |
| All English | Thai + transliteration |
| Too long | Concise, cut verbose words |
| Ambiguous | Specific, testable |
| Missing tag | Add `[BE]`, `[FE-Admin]`, etc. |
| Generic file paths | Actual paths from codebase |
