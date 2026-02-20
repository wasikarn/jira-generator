#!/usr/bin/env python3
"""Reformat BEP-3330 ADF to match writing style guide.

Fixes:
1. Add numbered section pattern (N. Emoji Title)
2. Remove empty headings
3. Wrap ACs in info panels with proper naming (AC1: [Verb] — [Scenario])
4. Fix broken table cell (Coupon.ts row: 3 cells → 2)

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


def h3(t):
    return {"type": "heading", "attrs": {"level": 3}, "content": [plain(t)]}


def para(*parts):
    return {"type": "paragraph", "content": list(parts)}


def li(*parts):
    return {"type": "listItem", "content": [para(*parts)]}


def bullet(*items):
    return {"type": "bulletList", "content": list(items)}


def info_panel(*content):
    return {"type": "panel", "content": list(content), "attrs": {"panelType": "info"}}


def th(*cells):
    return {
        "type": "tableRow",
        "content": [
            {"type": "tableHeader", "attrs": {}, "content": [para(bold(c))]}
            for c in cells
        ],
    }


def td(*cells):
    """Create a table row. Each cell: str→plain text, list→inline elements."""
    row = []
    for c in cells:
        if isinstance(c, list):
            row.append(
                {
                    "type": "tableCell",
                    "attrs": {},
                    "content": [{"type": "paragraph", "content": c}],
                }
            )
        elif isinstance(c, str):
            row.append(
                {
                    "type": "tableCell",
                    "attrs": {},
                    "content": [para(plain(c))],
                }
            )
        else:
            row.append({"type": "tableCell", "attrs": {}, "content": [c]})
    return {"type": "tableRow", "content": row}


def table(*rows):
    return {
        "type": "table",
        "attrs": {"isNumberColumnEnabled": False, "layout": "default"},
        "content": list(rows),
    }


# --- Build corrected ADF ---
def build_adf():
    return {
        "type": "doc",
        "version": 1,
        "content": [
            # 1. Overview
            h2("1. 🎯 Overview"),
            info_panel(
                para(
                    plain(
                        "เพิ่มความสามารถจำกัดการใช้คูปองต่อคนต่อวัน (daily limit) โดย admin สามารถตั้งค่า "
                    ),
                    code("max_per_user_per_day"),
                    plain(" ต่อคูปองได้"),
                    hardbreak(),
                    bold("ตัวอย่าง:"),
                    plain(
                        " คูปองไม่จำกัดจำนวนครั้งตลอด campaign แต่ใช้ได้ไม่เกินวันละ 1 ครั้งต่อคน"
                    ),
                ),
            ),
            # 2. Requirements
            h2("2. 📋 Requirements"),
            bullet(
                li(
                    plain("เพิ่ม field "),
                    code("max_per_user_per_day"),
                    plain(" (nullable integer) ใน "),
                    code("coupons"),
                    plain(" table"),
                ),
                li(
                    code("null"),
                    plain(
                        " = ไม่จำกัดต่อวัน, ตัวเลข = จำนวนครั้งสูงสุดต่อคนต่อวัน"
                    ),
                ),
                li(
                    plain("Apply เฉพาะ "),
                    bold("redeem flow"),
                    plain(" (useCoupon) — ไม่กระทบ collect flow"),
                ),
                li(
                    plain("นับวันตาม "),
                    bold("Asia/Bangkok"),
                    plain(" timezone (GMT+7)"),
                ),
                li(
                    plain(
                        "Admin สามารถตั้งค่าได้ตอน create/update coupon (range: 1-100)"
                    )
                ),
            ),
            # 3. Scope
            h2("3. 📐 Scope"),
            table(
                th("Service", "ต้องแก้ไข", "เหตุผล"),
                td(
                    "Backend API",
                    "✅ ใช่",
                    "เพิ่ม field, validation logic, error handling",
                ),
                td(
                    "Admin Frontend",
                    "✅ ใช่",
                    "เพิ่ม input field ใน create/update coupon form",
                ),
                td("Website Frontend", "❌ ไม่", "canUse logic อยู่ฝั่ง BE"),
            ),
            # 4. Acceptance Criteria
            h2("4. ✅ Acceptance Criteria"),
            # AC1
            info_panel(
                para(bold("AC1: Validate — Daily Limit Block")),
                bullet(
                    li(
                        bold("Given: "),
                        plain("คูปองมี "),
                        code("max_per_user_per_day = 1"),
                        plain(" และ user ใช้คูปองนี้ไปแล้ว 1 ครั้งวันนี้"),
                    ),
                    li(
                        bold("When: "),
                        plain("user พยายามใช้คูปองเดิมอีกครั้งในวันเดียวกัน"),
                    ),
                    li(
                        bold("Then: "),
                        plain("API reject ด้วย error "),
                        code("COUPON_CANNOT_USE_MAX_PER_USER_PER_DAY"),
                        plain(" พร้อม message ภาษาไทย"),
                    ),
                ),
            ),
            # AC2
            info_panel(
                para(bold("AC2: Reset — วันใหม่นับใหม่")),
                bullet(
                    li(
                        bold("Given: "),
                        plain("คูปองมี "),
                        code("max_per_user_per_day = 1"),
                        plain(" และ user ใช้ไปแล้ว 1 ครั้งเมื่อวาน"),
                    ),
                    li(
                        bold("When: "),
                        plain("วันใหม่ (00:00 Asia/Bangkok) user ใช้คูปองอีกครั้ง"),
                    ),
                    li(bold("Then: "), plain("ใช้ได้สำเร็จ (นับใหม่ทุกวัน)")),
                ),
            ),
            # AC3
            info_panel(
                para(bold("AC3: Skip — null ไม่จำกัด")),
                bullet(
                    li(
                        bold("Given: "),
                        plain("คูปองมี "),
                        code("max_per_user_per_day = null"),
                    ),
                    li(
                        bold("When: "),
                        plain("user ใช้คูปองหลายครั้งในวันเดียวกัน"),
                    ),
                    li(
                        bold("Then: "),
                        plain("ใช้ได้ไม่จำกัด (เท่าที่ lifetime limit อนุญาต)"),
                    ),
                ),
            ),
            # AC4
            info_panel(
                para(bold("AC4: Configure — Admin ตั้งค่า")),
                bullet(
                    li(bold("Given: "), plain("Admin สร้าง/แก้ไขคูปอง")),
                    li(
                        bold("When: "),
                        plain("กรอกค่า "),
                        code("max_per_user_per_day"),
                    ),
                    li(
                        bold("Then: "),
                        plain(
                            "ค่าถูกบันทึกและ enforce ตามที่ตั้งไว้ (range: 1-100, nullable)"
                        ),
                    ),
                ),
            ),
            # AC5
            info_panel(
                para(bold("AC5: Display — canUse reflect limit")),
                bullet(
                    li(
                        bold("Given: "),
                        plain("User ดูรายละเอียดคูปอง (GetCouponByCode)"),
                    ),
                    li(bold("When: "), plain("ใช้ครบ daily limit แล้ว")),
                    li(bold("Then: "), code("can_use = false")),
                ),
            ),
            # AC6
            info_panel(
                para(bold("AC6: Isolate — Collect ไม่กระทบ")),
                bullet(
                    li(bold("Given: "), plain("คูปองมี daily limit")),
                    li(bold("When: "), plain("user collect คูปอง")),
                    li(
                        bold("Then: "),
                        plain("collect ได้ปกติ ไม่ถูก block โดย daily limit"),
                    ),
                ),
            ),
            # 5. Technical Approach
            h2("5. 🔧 Technical Approach"),
            h3("Files to Modify"),
            table(
                th("File", "Change"),
                td(
                    [
                        code(
                            "database/migrations/{ts}_alter_coupons_add_max_per_user_per_day.ts"
                        )
                    ],
                    "NEW — add nullable int column",
                ),
                td(
                    [code("app/Models/Coupon.ts")],
                    [plain("Add "), code("maxPerUserPerDay: number | null")],
                ),
                td(
                    [code("app/Constants/Coupon/ErrorCode.ts")],
                    [
                        plain("Add "),
                        code("COUPON_CANNOT_USE_MAX_PER_USER_PER_DAY"),
                    ],
                ),
                td(
                    [code("app/Services/Coupon/CouponMaxPerUserService.ts")],
                    [
                        plain("Add "),
                        code("checkCouponMaxPerUserPerDay()"),
                        plain(" + "),
                        code("countTodayRedemptions()"),
                    ],
                ),
                td(
                    [code("app/Services/CouponService.ts")],
                    [plain("Call daily check in "), code("validateCoupon")],
                ),
                td(
                    [code("app/Validators/Admin/Coupon/CreateCouponValidator.ts")],
                    [plain("Add "), code("max_per_user_per_day"), plain(" field")],
                ),
                td(
                    [code("app/Validators/Admin/Coupon/UpdateCouponValidator.ts")],
                    [plain("Add "), code("max_per_user_per_day"), plain(" field")],
                ),
                td(
                    [code("app/UseCases/Admin/V1/Coupon/CreateCoupon.ts")],
                    [plain("Persist "), code("maxPerUserPerDay")],
                ),
                td(
                    [code("app/UseCases/Admin/V1/Coupon/UpdateCoupon.ts")],
                    [plain("Persist "), code("maxPerUserPerDay")],
                ),
                td(
                    [
                        code(
                            "app/Modules/Coupon/Admin/UseCases/UpdateCouponUseCase.ts"
                        )
                    ],
                    "Add to merge map",
                ),
                td(
                    [
                        code(
                            "app/Modules/Coupon/Admin/UseCases/DuplicateCouponUseCase.ts"
                        )
                    ],
                    "Copy field",
                ),
                td(
                    [code("app/UseCases/Public/V2/Coupon/GetCouponByCode.ts")],
                    [plain("Add daily check to "), code("canUse")],
                ),
                td(
                    [
                        code(
                            "tests/unit/Services/Coupon/CouponMaxPerUserService.spec.ts"
                        )
                    ],
                    "Add daily limit test group",
                ),
            ),
            h3("Key Design Decisions"),
            bullet(
                li(
                    plain("Reuse "),
                    code("CouponMaxPerUserService"),
                    plain(" — co-locate daily limit with lifetime limit"),
                ),
                li(
                    plain("Use Luxon "),
                    code("DateTime.now().setZone('Asia/Bangkok')"),
                    plain(" for UTC day bounds"),
                ),
                li(
                    plain("Count "),
                    code("CouponRedemption"),
                    plain(" (redeem flow only) with date range filter"),
                ),
                li(code("findCoupon()"), plain(" reused from existing code")),
            ),
            # 6. Links
            h2("6. 🔗 Links"),
            table(
                th("Type", "Link"),
                td(
                    "Epic",
                    [
                        link_text(
                            "BEP-3197",
                            "https://{{JIRA_SITE}}/browse/BEP-3197",
                        ),
                        plain(" — Backend APIs & Infrastructure"),
                    ],
                ),
                td(
                    "Related",
                    [
                        link_text(
                            "BEP-3165",
                            "https://{{JIRA_SITE}}/browse/BEP-3165",
                        ),
                        plain(" — Fix checkCoupon() maxPerUser Bug"),
                    ],
                ),
            ),
        ],
    }


def main():
    dry_run = "--dry-run" in sys.argv
    issue_key = "BEP-3330"

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
    if "1. 🎯 Overview" in desc_text and '"panelType": "info"' in desc_text:
        # Check if ACs are already in panels
        ac_panel_count = desc_text.count("AC1: Validate")
        if ac_panel_count > 0:
            print("  Already formatted — skipping")
            return

    adf = build_adf()

    if dry_run:
        print(f"  DRY RUN — {len(adf['content'])} top-level nodes")
        # Save to file for inspection
        out = Path(__file__).parent.parent / "tasks" / "bep-3330-format-preview.json"
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
