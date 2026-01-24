# Writing Style Guide

## Language Rules

### Thai + ทับศัพท์ (Transliteration)

**หลักการ:** เนื้อหาหลักเป็นภาษาไทย, technical terms เป็นภาษาอังกฤษ

| Content Type | Language | Example |
|--------------|----------|---------|
| User Story narrative | Thai | "แอดมินต้องการดูรายการคูปอง" |
| AC descriptions | Thai | "เมื่อคลิกปุ่ม Submit" |
| Technical terms | English | endpoint, payload, component |
| File paths | English | `src/pages/coupon/index.tsx` |
| Code/Routes | English | `/api/coupons`, `getCoupons()` |

### ทับศัพท์ที่ใช้บ่อย

| Thai | English (keep as-is) |
|------|----------------------|
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

### ตัวอย่างที่ถูกต้อง

**Good:**
```
Given: แอดมินเข้าหน้า `/coupon`
When: คลิก "คูปองเติมเครดิต"
Then: ไปหน้า `/coupon/topup-credit`
```

**Bad:**
```
Given: Admin enters the coupon page  (❌ ภาษาอังกฤษทั้งหมด)
When: Click "Top-up Credit Coupon"
Then: Navigate to topup credit page
```

---

## Tone & Style

### กระชับ (Concise)

- ไม่ใช้คำฟุ่มเฟือย
- ตัดคำที่ไม่จำเป็นออก
- 1 ประโยค = 1 idea

**Good:**
```
แสดงการ์ด 3 ประเภทตามดีไซน์
```

**Bad:**
```
ระบบจะต้องทำการแสดงผลการ์ดจำนวน 3 ประเภทให้ตรงตามที่ได้ออกแบบไว้
```

### เป็นกันเอง (Casual)

- เขียนเหมือนคุยกับเพื่อนร่วมทีม
- ไม่เป็นทางการเกินไป
- ใช้ภาษาที่ทีมเข้าใจ

**Good:**
```
AC1: Display - โหลดหน้าแล้วเห็นการ์ด 3 อัน
```

**Bad:**
```
AC1: การแสดงผล - เมื่อระบบโหลดหน้าเสร็จสมบูรณ์แล้ว ผู้ใช้งานจะสามารถมองเห็นการ์ดจำนวน 3 รายการ
```

### ชัดเจน (Clear)

- ไม่คลุมเครือ
- ระบุ specific value/behavior
- Testable

**Good:**
```
Then: แสดง error "กรุณากรอกจำนวนเงิน"
```

**Bad:**
```
Then: แสดง error ที่เหมาะสม
```

---

## ADF Formatting

### Inline Code

ใช้ inline code สำหรับ:
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

ใช้ bold สำหรับ:
- Labels: **Given**, **When**, **Then**
- Emphasis: **สำคัญ**
- Section headers in content

**ADF Mark:**
```json
{"type": "text", "text": "Given:", "marks": [{"type": "strong"}]}
```

---

## Summary Format

### User Story

```
[Service Tag] - [Thai description] ([English feature name])
```

Examples:
- ✅ `[FE-Admin] - สร้างหน้าเมนูคูปอง (Coupon Menu)`
- ✅ `[BE] - เพิ่ม API filter coupons`
- ❌ `Create coupon menu page` (ไม่มี tag, English only)
- ❌ `[BE] - ทำ API` (ไม่ specific)

### Sub-task

```
[TAG] - [Brief description - Thai or Thai+English]
```

Tags: `[BE]`, `[FE-Admin]`, `[FE-Web]`

### QA Sub-task

```
[QA] - Test: [Story title or feature name]
```

---

## Common Mistakes

| Mistake | Correct |
|---------|---------|
| ภาษาอังกฤษทั้งหมด | Thai + ทับศัพท์ |
| ยาวเกินไป | กระชับ, ตัดคำฟุ่มเฟือย |
| คลุมเครือ | Specific, testable |
| ไม่มี tag | ใส่ `[BE]`, `[FE-Admin]`, etc. |
| Generic file paths | Actual paths from codebase |
