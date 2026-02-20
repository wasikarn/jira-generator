#!/usr/bin/env python3
"""Reformat BEP-3331 ADF to match writing style guide.

Fixes:
1. Remove empty headings
2. Convert blockquote-style text ("> ...") to proper ADF panels
3. Fix table headers in Expected vs Actual (was "---" data row)
4. Convert [x] checkboxes to proper ✅ bullets
5. Clean trailing spaces in table cells
6. Proper numbered section pattern (N. Emoji Title)

One-time script — idempotent (checks for existing format).
"""

import json
import sys
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).resolve().parent.parent / ".claude/skills/atlassian-scripts")
)
from lib.auth import create_ssl_context, get_auth_header, load_credentials
from lib.jira_api import JiraAPI, derive_jira_url


# --- ADF helpers ---
def bold(t):
    return {"type": "text", "text": t, "marks": [{"type": "strong"}]}


def plain(t):
    return {"type": "text", "text": t}


def code(t):
    return {"type": "text", "text": t, "marks": [{"type": "code"}]}


def link_text(t, href):
    return {"type": "text", "text": t, "marks": [{"type": "link", "attrs": {"href": href}}]}


def hardbreak():
    return {"type": "hardBreak"}


def h2(t):
    return {"type": "heading", "attrs": {"level": 2}, "content": [plain(t)]}


def para(*parts):
    return {"type": "paragraph", "content": list(parts)}


def li(*parts):
    return {"type": "listItem", "content": [para(*parts)]}


def bullet(*items):
    return {"type": "bulletList", "content": list(items)}


def ordered(*items, start=1):
    return {"type": "orderedList", "attrs": {"order": start}, "content": list(items)}


def error_panel(*content):
    return {"type": "panel", "content": list(content), "attrs": {"panelType": "error"}}


def warning_panel(*content):
    return {"type": "panel", "content": list(content), "attrs": {"panelType": "warning"}}


def note_panel(*content):
    return {"type": "panel", "content": list(content), "attrs": {"panelType": "note"}}


def info_panel(*content):
    return {"type": "panel", "content": list(content), "attrs": {"panelType": "info"}}


def success_panel(*content):
    return {"type": "panel", "content": list(content), "attrs": {"panelType": "success"}}


def th(*cells):
    return {
        "type": "tableRow",
        "content": [
            {"type": "tableHeader", "attrs": {}, "content": [para(bold(c))]}
            for c in cells
        ],
    }


def td(*cells):
    """Create a table row. Each cell: str->plain text, list->inline elements."""
    row = []
    for c in cells:
        if isinstance(c, list):
            row.append({"type": "tableCell", "attrs": {}, "content": [{"type": "paragraph", "content": c}]})
        elif isinstance(c, str):
            row.append({"type": "tableCell", "attrs": {}, "content": [para(plain(c))]})
        else:
            row.append({"type": "tableCell", "attrs": {}, "content": [c]})
    return {"type": "tableRow", "content": row}


def table(*rows):
    return {
        "type": "table",
        "attrs": {"isNumberColumnEnabled": False, "layout": "default"},
        "content": list(rows),
    }


def rule():
    return {"type": "rule"}


# --- Build corrected ADF ---
def build_adf():
    return {
        "type": "doc",
        "version": 1,
        "content": [
            # 1. Bug Description
            h2("1. 🐛 Bug Description"),
            error_panel(
                para(
                    bold("Production Incident (2026-02-20): "),
                    plain("User สามารถ redeem คูปองคนละ code ได้ไม่จำกัดจำนวนต่อวัน เนื่องจากระบบปัจจุบันมีแค่ "),
                    code("maxPerUser"),
                    plain(" (per-coupon lifetime limit) แต่ไม่มี global daily cap ข้าม coupon codes ทั้งหมด"),
                ),
                para(
                    bold("Impact: "),
                    plain("User 1 คน redeem 74 coupons (53 + 20 + 1) รวมมูลค่า 3,700 ฿ ในเครดิตฟรี โดยใช้ coupon คนละ code ผ่าน "),
                    code("maxPerUser=1"),
                    plain(" check ได้ทุกใบ"),
                ),
            ),

            # 2. Reproduction Steps
            h2("2. 🔄 Reproduction Steps"),
            ordered(
                li(plain("สมัคร account ใหม่")),
                li(plain("Redeem coupon code A (credit 50 ฿, maxPerUser=1) → สำเร็จ")),
                li(plain("Redeem coupon code B (credit 50 ฿, maxPerUser=1) → สำเร็จ")),
                li(bold("ทำซ้ำ"), plain(" กับ coupon code C, D, E, ... → สำเร็จทุกใบ "), bold("ไม่มี limit")),
            ),

            # 3. Expected vs Actual
            h2("3. 📊 Expected vs Actual"),
            table(
                th("Aspect", "Expected", "Actual"),
                td(
                    [bold("Daily limit")],
                    "User ใช้ coupon ได้ไม่เกิน N ใบ/วัน (cross-coupon, default=5)",
                    [plain("ไม่มี limit — user ใช้ได้ "), bold("ไม่จำกัด"), plain(" (20 ใบใน 5 นาที)")],
                ),
                td(
                    [bold("Error response")],
                    "Reject พร้อม error code เมื่อเกิน daily limit",
                    "ไม่มี error — redeem สำเร็จทุกครั้ง",
                ),
            ),

            # 4. Root Cause
            h2("4. 🔍 Root Cause"),
            warning_panel(
                para(
                    code("CouponService.validateCoupon()"),
                    plain(" และ "),
                    code("CouponMaxPerUserService"),
                    plain(" ตรวจสอบแค่ "),
                    code("maxPerUser"),
                    plain(" (lifetime per-coupon limit) — ไม่มี check สำหรับ total redemptions across all coupons per day"),
                ),
                para(
                    bold("ตารางที่เกี่ยวข้อง: "),
                    code("coupon_redemptions"),
                    plain(" — ต้อง count WHERE "),
                    code("account_code = ? AND status = 'successful' AND redeemed_at BETWEEN today_start AND today_end"),
                ),
            ),

            # 5. Fix Plan
            h2("5. 🛠️ Fix Plan"),
            note_panel(
                para(bold("Approach: "), plain("เก็บค่า limit ใน DB ตั้งแต่แรก เพื่อรองรับ Admin Settings UI ในอนาคต")),
            ),
            ordered(
                li(
                    bold("Migration: "),
                    plain("สร้างตาราง "),
                    code("coupon_settings"),
                    plain(" พร้อม column "),
                    code("max_redemptions_per_user_per_day INT DEFAULT 1"),
                    plain(" + seed row (value=5)"),
                ),
                li(
                    bold("Model: "),
                    plain("สร้าง "),
                    code("CouponSetting"),
                    plain(" Lucid model"),
                ),
                li(
                    bold("Service: "),
                    plain("สร้าง "),
                    code("CouponGlobalDailyLimitService"),
                    plain(" แยกจาก "),
                    code("CouponMaxPerUserService"),
                    plain(" — query "),
                    code("coupon_settings"),
                    plain(" + cache Redis (TTL 5 นาที) + count today's redemptions across all coupons"),
                ),
                li(
                    bold("Validation: "),
                    plain("เพิ่ม call "),
                    code("isWithinGlobalDailyLimit()"),
                    plain(" ใน "),
                    code("CouponService.validateCoupon()"),
                ),
                li(
                    bold("Error code: "),
                    plain("เพิ่ม "),
                    code("COUPON_GLOBAL_DAILY_LIMIT_EXCEEDED"),
                    plain(" ใน "),
                    code("ErrorCode.ts"),
                ),
                li(
                    bold("Fallback: "),
                    plain("ถ้า query "),
                    code("coupon_settings"),
                    plain(" ไม่ได้ → fallback hardcoded default = 5"),
                ),
                li(
                    bold("Error handling: "),
                    plain("Fail-closed pattern — ถ้า count query fail → return "),
                    code("Infinity"),
                    plain(" (block redemption)"),
                ),
            ),

            # 6. Evidence
            h2("6. 📊 Evidence — Production Data"),
            error_panel(
                para(
                    bold("Suspicious User: "),
                    code("AC260104YZOX4866"),
                    plain(" (tenlee lovelove)"),
                ),
                bullet(
                    li(plain("5 ม.ค. 69: redeem 53 coupons x 50 ฿ = 2,650 ฿")),
                    li(bold("20 ก.พ. 69: "), plain("redeem 20 coupons x 50 ฿ = 1,000 ฿ (ใน 5 นาที)")),
                    li(bold("รวม: "), plain("74 coupons = 3,700 ฿ เครดิตฟรี")),
                ),
                para(
                    bold("Possible Alt Account: "),
                    code("AC260220LUYM4509"),
                    plain(" (blynboo) — สมัครวันนี้ 10:06 → redeem 2 coupons ใน 1 นาที"),
                ),
            ),

            # 7. Fix Criteria
            h2("7. ✅ Fix Criteria"),
            success_panel(
                bullet(
                    li(
                        plain("User ใช้ coupon (cross-coupon) ได้ไม่เกิน limit ที่กำหนดใน DB ต่อวัน (default = 5)"),
                    ),
                    li(
                        plain("Redeem เกิน limit → reject พร้อม error code "),
                        code("COUPON_GLOBAL_DAILY_LIMIT_EXCEEDED"),
                    ),
                    li(
                        plain("ค่า limit อ่านจาก "),
                        code("coupon_settings"),
                        plain(" table + Redis cache (TTL 5 นาที)"),
                    ),
                    li(
                        plain("ถ้า "),
                        code("coupon_settings"),
                        plain(" query fail → fallback default = 5"),
                    ),
                    li(plain("Daily reset ตาม Bangkok timezone (UTC+7)")),
                    li(plain("Unit tests ครอบคลุม: under limit, at limit, null setting, timezone boundary, Redis error, malformed cache, count query error")),
                    li(
                        plain("Fail-closed: count query error → block redemption (return "),
                        code("Infinity"),
                        plain(")"),
                    ),
                ),
            ),

            # 8. Reference
            h2("8. 🔗 Reference"),
            table(
                th("Type", "Link"),
                td(
                    "Related (per-coupon daily limit)",
                    [link_text("BEP-3330", "https://{{JIRA_SITE}}/browse/BEP-3330")],
                ),
                td(
                    "Technical Note",
                    [link_text(
                        "Coupon Daily Limit — maxPerUserPerDay",
                        "https://{{JIRA_SITE}}/wiki/spaces/BEP/pages/165052419",
                    )],
                ),
                td(
                    "Epic",
                    [link_text("BEP-3197", "https://{{JIRA_SITE}}/browse/BEP-3197"),
                     plain(" — Backend APIs & Infrastructure")],
                ),
                td(
                    "PR",
                    [link_text("#1902", "https://github.com/100-Stars-Co/bd-eye-platform-api/pull/1902")],
                ),
            ),
        ],
    }


def main():
    dry_run = "--dry-run" in sys.argv
    issue_key = "BEP-3331"

    creds = load_credentials()
    api = JiraAPI(
        base_url=derive_jira_url(creds["CONFLUENCE_URL"]),
        auth_header=get_auth_header(
            creds["CONFLUENCE_USERNAME"], creds["CONFLUENCE_API_TOKEN"]
        ),
        ssl_context=create_ssl_context(),
    )

    print(f"=== Reformatting {issue_key} ===")

    # Idempotency check
    issue = api.get_issue(issue_key)
    desc = issue["fields"].get("description", {})
    desc_text = json.dumps(desc, ensure_ascii=False)
    if '"panelType": "error"' in desc_text and "1. 🐛 Bug Description" in desc_text:
        print("  Already formatted — skipping")
        return

    adf = build_adf()

    if dry_run:
        print(f"  DRY RUN — {len(adf['content'])} top-level nodes")
        out = Path(__file__).parent.parent / "tasks" / "bep-3331-format-preview.json"
        out.parent.mkdir(exist_ok=True)
        with open(out, "w") as f:
            json.dump(
                {"issues": [issue_key], "description": adf},
                f,
                indent=2,
                ensure_ascii=False,
            )
        print(f"  Preview saved to {out}")
        return

    status = api.update_description(issue_key, adf)
    if status in (200, 204):
        print(f"  {issue_key}: Updated successfully")
    else:
        print(f"  {issue_key}: Failed (HTTP {status})")
        sys.exit(1)


if __name__ == "__main__":
    main()
