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

### Concise

- No verbose wording
- Cut unnecessary words
- 1 sentence = 1 idea

**Good:**

```text
Display 3 card types per design
```

**Bad:**

```text
The system shall render and display a total of 3 card types in accordance with the approved design specifications
```

### Casual

- Write as if talking to a teammate
- Not overly formal
- Use language the team understands

**Good:**

```text
AC1: Display - Page loads and shows 3 cards
```

**Bad:**

```text
AC1: Display - Upon successful completion of page loading, the user shall be able to observe 3 card items rendered on screen
```

### Clear

- Not ambiguous
- Specify exact values/behavior
- Testable

**Good:**

```text
Then: Show error "Please enter an amount"
```

**Bad:**

```text
Then: Show an appropriate error
```

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
