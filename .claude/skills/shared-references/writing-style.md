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

> **หลัก 3 ข้อ:** Concise (ตัดคำเกิน) · Casual (คุยกับเพื่อนร่วมทีม) · Clear (specific + testable)

| ❌ Verbose | ✅ Concise |
| --- | --- |
| The system shall render and display a total of 3 card types in accordance with the approved design specifications | Display 3 card types per design |
| Upon successful completion of page loading, the user shall be able to observe 3 card items rendered on screen | AC1: Display - Page loads and shows 3 cards |
| Then: Show an appropriate error | Then: Show error "Please enter an amount" |

---

## Scan-First Principle

ทีมจะ **scan ก่อนอ่าน** — ออกแบบ content ให้ scan ได้ใน 5 วินาที

1. **Bold keywords first** — `**Given:** precondition` ไม่ใช่ prose ยาว
2. **Bullets > Paragraphs** — ห้ามเขียนย่อหน้ายาว, ใช้ bullet points
3. **Tables > Lists** — ถ้ามี 2+ columns ของข้อมูล ใช้ table
4. **Skip if empty** — ถ้า section ไม่มีข้อมูลจริง ไม่ต้องใส่ placeholder

---

## Content Budget (ต่อ section)

> Agent **ต้อง** เขียนไม่เกิน budget นี้ — ถ้าเกิน ให้ตัดหรือ split

| Issue Type | Section | Budget |
| --- | --- | --- |
| **Epic** | Overview | 2 ประโยค |
| | Business Value | 3 bullets (Revenue/Retention/Ops) |
| | Scope | 1 บรรทัด/item, ไม่ต้องอธิบาย |
| | RICE | ⚡ optional — skip ถ้า priority ชัดอยู่แล้ว |
| | Success Metrics | ⚡ optional — skip ถ้า metrics ยังไม่ define |
| | User Stories | list + link เท่านั้น, ไม่ต้อง description |
| | Progress | auto counts, ไม่ต้องเขียนเอง |
| **Story** | Narrative | 3 บรรทัด (As a / I want / So that) |
| | AC panels | max 5 panels — ถ้า >5 ให้ split story |
| | Each AC | 3 bullets (Given/When/Then) + optional And |
| | Reference | ⚡ skip ถ้าไม่มี Figma/external link |
| **Sub-task** | Objective | 1 ประโยค |
| | Scope table | เฉพาะ files ที่เปลี่ยน, max 10 rows |
| | AC panels | max 3 panels |
| | Reference | ⚡ skip ถ้า parent story มี link ครบ |
| **QA** | Test Objective | 1 ประโยค |
| | Test Cases | max 8 cases — ถ้า >8 ให้ split QA ticket |

**⚡ = optional section** — ใส่เฉพาะเมื่อมีข้อมูลจริง

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

> Convention จาก Sprint 32 — ใช้กับ Jira labels สำหรับ board filtering

| Pattern | ใช้เมื่อ | Example |
| --- | --- | --- |
| `vs{N}-{name}` | Numbered vertical slice | `vs1-skeleton`, `vs2-credit-e2e` |
| `vs-enabler` | Shared component ที่หลาย slice ใช้ | Side Panel, Toast |
| `{feature}-{scope}` | Cross-cutting concern | `coupon-web`, `ad-integration` |

**Rules:** ทุก story ต้องมี feature label (`coupon-web`) + VS label อย่างน้อย 1 ตัว / 1 story อาจมีหลาย VS labels

---

## Common Mistakes

| Mistake | Correct |
| --- | --- |
| All English | Thai + transliteration |
| Too long | Concise, cut verbose words |
| Ambiguous | Specific, testable |
| Missing tag | Add `[BE]`, `[FE-Admin]`, etc. |
| Generic file paths | Actual paths from codebase |
