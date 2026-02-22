#!/usr/bin/env python3
"""Create Confluence page: Backend-Driven Player Architecture — Design Proposal.

Creates under BEP space as a child of 'Player Doc' (page 81592324).
Idempotent: checks if page already exists by title.
"""

import json
import sys
import uuid
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).resolve().parent.parent / ".claude/skills/atlassian-scripts")
)
from lib.auth import create_ssl_context, get_auth_header, load_credentials
from lib import ConfluenceAPI

SPACE_KEY = "BEP"
PARENT_PAGE_ID = "81592324"  # Player Doc
PAGE_TITLE = "Architecture Proposal: Backend-Driven Player — Dumb Renderer + Offline Resilience"
ARCH_PAGE_ID = "165019751"  # The architecture page itself

# ─── Sub-Page Config ───
PAGE_IDS_FILE = Path(__file__).parent / "architecture-page-ids.json"

SUB_PAGE_TITLES = {
    "1_problem_current": "1. ปัญหาปัจจุบันและสถาปัตยกรรมเดิม (Problem Statement)",
    "2_proposed": "2. สถาปัตยกรรมที่เสนอ (Proposed Architecture)",
    "3_key_flows": "3. Flow หลัก (Key Flows)",
    "4_tech_algorithm": "4. Technical Design: Algorithm และ Models",
    "5_tech_player": "5. Technical Design: Player Components",
    "6_interrupt_makegood": "6. Interrupt Controller และระบบ Make-Good",
    "7_events": "7. สถาปัตยกรรม Event-Driven",
    "8_edge_migration": "8. Edge Cases, แผนการ Migration และ Appendix",
    "9_es_big_picture": "9. Event Storming: ภาพรวม (Big Picture)",
    "10_es_process": "10. Event Storming: Process Modelling",
    "11_es_design": "11. Event Storming: Software Design",
}


def load_page_ids() -> dict:
    if PAGE_IDS_FILE.exists():
        return json.loads(PAGE_IDS_FILE.read_text(encoding="utf-8"))
    return {"parent": ARCH_PAGE_ID, "pages": {k: None for k in SUB_PAGE_TITLES}}


def save_page_ids(data: dict):
    PAGE_IDS_FILE.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

# ─── Mermaid Forge App Constants ───
MERMAID_APP_ID = "23392b90-4271-4239-98ca-a3e96c663cbb"
MERMAID_ENV_ID = "63d4d207-ac2f-4273-865c-0240d37f044a"
MERMAID_INSTALL_ID = "5c245bad-32e8-4c74-aa1c-6d227f18fa22"
CLOUD_ID = "85ad5bd2-ef9c-477e-b000-062f1421d0c0"
RESOURCE_UPLOAD_ID = "9f9d6c69-f97f-4e32-b336-cca6d907aa0b"
ACCOUNT_ID = "712020:64219948-720a-4925-a48c-d7a53557993c"
BEP_SPACE_ID = "1081347"
WORKSPACE_ID = "2f960cad-efff-4621-bb36-aa7f65cf74df"
ICON_URL = (
    f"https://icon.cdn.prod.atlassian-dev.net/"
    f"{MERMAID_APP_ID}/{MERMAID_ENV_ID}/{RESOURCE_UPLOAD_ID}/icons/app-icon.png"
)

# ─── Diagram Files ───
DIAGRAMS_DIR = Path(__file__).parent / "diagrams"


def load_diagram(name: str) -> str:
    """Load .mmd file from diagrams/ directory."""
    return (DIAGRAMS_DIR / name).read_text(encoding="utf-8").strip()


# Global code block counter (Forge index counts ALL code blocks on page)
_code_block_count = 0


def toc():
    return (
        '<ac:structured-macro ac:name="toc" ac:schema-version="1">'
        '<ac:parameter ac:name="minLevel">2</ac:parameter>'
        '<ac:parameter ac:name="maxLevel">3</ac:parameter>'
        "</ac:structured-macro>\n"
    )


def info_panel(content: str) -> str:
    return (
        '<ac:structured-macro ac:name="info" ac:schema-version="1">'
        f"<ac:rich-text-body>{content}</ac:rich-text-body>"
        "</ac:structured-macro>"
    )


def note_panel(content: str) -> str:
    return (
        '<ac:structured-macro ac:name="note" ac:schema-version="1">'
        f"<ac:rich-text-body>{content}</ac:rich-text-body>"
        "</ac:structured-macro>"
    )


def warning_panel(content: str) -> str:
    return (
        '<ac:structured-macro ac:name="warning" ac:schema-version="1">'
        f"<ac:rich-text-body>{content}</ac:rich-text-body>"
        "</ac:structured-macro>"
    )


def success_panel(content: str) -> str:
    return (
        '<ac:structured-macro ac:name="success" ac:schema-version="1">'
        f"<ac:rich-text-body>{content}</ac:rich-text-body>"
        "</ac:structured-macro>"
    )


def error_panel(content: str) -> str:
    return (
        '<ac:structured-macro ac:name="error" ac:schema-version="1">'
        f"<ac:rich-text-body>{content}</ac:rich-text-body>"
        "</ac:structured-macro>"
    )


def code_block(code: str, language: str = "text", title: str = "",
               collapse: bool = False) -> str:
    parts = [
        '<ac:structured-macro ac:name="code" ac:schema-version="1">',
        f'<ac:parameter ac:name="language">{language}</ac:parameter>',
    ]
    if title:
        parts.append(f'<ac:parameter ac:name="title">{title}</ac:parameter>')
    if collapse:
        parts.append('<ac:parameter ac:name="collapse">true</ac:parameter>')
    parts.append(f"<ac:plain-text-body><![CDATA[{code}]]></ac:plain-text-body>")
    parts.append("</ac:structured-macro>")
    return "".join(parts)


def tracked_code_block(code: str, language: str = "text", title: str = "",
                       collapse: bool = False) -> str:
    """code_block() with global counter for Forge index tracking."""
    global _code_block_count
    result = code_block(code, language, title, collapse=collapse)
    _code_block_count += 1
    return result


def mermaid_diagram(code: str, page_id: str) -> str:
    """Generate mermaid code block + Forge renderer macro.

    Uses global _code_block_count as the Forge index, then increments it.
    """
    global _code_block_count
    index = _code_block_count
    _code_block_count += 1

    local_id = str(uuid.uuid4())
    code_local_id = str(uuid.uuid4())
    ext_id = (
        f"ari:cloud:ecosystem::extension/"
        f"{MERMAID_APP_ID}/{MERMAID_ENV_ID}/static/mermaid-diagram"
    )
    ext_key = f"{MERMAID_APP_ID}/{MERMAID_ENV_ID}/static/mermaid-diagram"
    consent_url = (
        f"https://id.atlassian.com/outboundAuth/start?"
        f"containerId={MERMAID_APP_ID}_{MERMAID_ENV_ID}"
        f"&amp;serviceKey=atlassian-token-service-key"
        f"&amp;cloudId={CLOUD_ID}"
        f"&amp;isAccountBased=true"
        f"&amp;scopes=read%3Apage%3Aconfluence+offline_access"
    )
    context_ari = f"ari:cloud:confluence:{CLOUD_ID}:workspace/{WORKSPACE_ID}"

    params = (
        f'<ac:adf-parameter key="local-id">{local_id}</ac:adf-parameter>'
        f'<ac:adf-parameter key="extension-id">{ext_id}</ac:adf-parameter>'
        f'<ac:adf-parameter key="extension-title">Mermaid diagram</ac:adf-parameter>'
        f'<ac:adf-parameter key="layout">extension</ac:adf-parameter>'
        f'<ac:adf-parameter key="forge-environment">PRODUCTION</ac:adf-parameter>'
        f'<ac:adf-parameter key="extension-properties">'
        f'<ac:adf-parameter key="extension">'
        f'<ac:adf-parameter key="id">{ext_id}</ac:adf-parameter>'
        f'<ac:adf-parameter key="app-id">{MERMAID_APP_ID}</ac:adf-parameter>'
        f'<ac:adf-parameter key="key">mermaid-diagram</ac:adf-parameter>'
        f'<ac:adf-parameter key="environment-id">{MERMAID_ENV_ID}</ac:adf-parameter>'
        f'<ac:adf-parameter key="environment-type">PRODUCTION</ac:adf-parameter>'
        f'<ac:adf-parameter key="environment-key">production</ac:adf-parameter>'
        f'<ac:adf-parameter key="properties">'
        f'<ac:adf-parameter key="resource-upload-id">{RESOURCE_UPLOAD_ID}</ac:adf-parameter>'
        f'<ac:adf-parameter key="resource">custom-ui</ac:adf-parameter>'
        f'<ac:adf-parameter key="icon">{ICON_URL}</ac:adf-parameter>'
        f'<ac:adf-parameter key="description">Render a Mermaid diagram from a code block on a page</ac:adf-parameter>'
        f'<ac:adf-parameter key="categories">'
        f'<ac:adf-parameter-value>confluence-content</ac:adf-parameter-value>'
        f'<ac:adf-parameter-value>development</ac:adf-parameter-value>'
        f'<ac:adf-parameter-value>formatting</ac:adf-parameter-value>'
        f'<ac:adf-parameter-value>visuals</ac:adf-parameter-value>'
        f'</ac:adf-parameter>'
        f'<ac:adf-parameter key="title">Mermaid diagram</ac:adf-parameter>'
        f'<ac:adf-parameter key="type">xen:macro</ac:adf-parameter>'
        f'<ac:adf-parameter key="config">'
        f'<ac:adf-parameter key="render">native</ac:adf-parameter>'
        f'<ac:adf-parameter key="resource">macro-config</ac:adf-parameter>'
        f'<ac:adf-parameter key="title">Mermaid diagram configuration</ac:adf-parameter>'
        f'<ac:adf-parameter key="viewport-size">small</ac:adf-parameter>'
        f'</ac:adf-parameter>'
        f'<ac:adf-parameter key="key">mermaid-diagram</ac:adf-parameter>'
        f'</ac:adf-parameter>'
        f'<ac:adf-parameter key="type">xen:macro</ac:adf-parameter>'
        f'<ac:adf-parameter key="installation-id">{MERMAID_INSTALL_ID}</ac:adf-parameter>'
        f'<ac:adf-parameter key="app-version">2.45.0</ac:adf-parameter>'
        f'<ac:adf-parameter key="consent-url">{consent_url}</ac:adf-parameter>'
        f'<ac:adf-parameter key="egress"><ac:adf-parameter-value></ac:adf-parameter-value></ac:adf-parameter>'
        f'<ac:adf-parameter key="scopes"><ac:adf-parameter-value>read:page:confluence</ac:adf-parameter-value></ac:adf-parameter>'
        f'<ac:adf-parameter key="data-classification-policy-decision">'
        f'<ac:adf-parameter key="status">ALLOWED</ac:adf-parameter>'
        f'</ac:adf-parameter>'
        f'</ac:adf-parameter>'
        f'<ac:adf-parameter key="extension-data">'
        f'<ac:adf-parameter key="type">macro</ac:adf-parameter>'
        f'<ac:adf-parameter key="content">'
        f'<ac:adf-parameter key="id">{page_id}</ac:adf-parameter>'
        f'<ac:adf-parameter key="type">page</ac:adf-parameter>'
        f'</ac:adf-parameter>'
        f'<ac:adf-parameter key="space">'
        f'<ac:adf-parameter key="key">BEP</ac:adf-parameter>'
        f'<ac:adf-parameter key="id">{BEP_SPACE_ID}</ac:adf-parameter>'
        f'</ac:adf-parameter>'
        f'</ac:adf-parameter>'
        f'<ac:adf-parameter key="account-id">{ACCOUNT_ID}</ac:adf-parameter>'
        f'<ac:adf-parameter key="cloud-id">{CLOUD_ID}</ac:adf-parameter>'
        f'<ac:adf-parameter key="context-ids">'
        f'<ac:adf-parameter-value>{context_ari}</ac:adf-parameter-value>'
        f'</ac:adf-parameter>'
        f'</ac:adf-parameter>'
        f'<ac:adf-parameter key="guest-params">'
        f'<ac:adf-parameter key="index" type="integer">{index}</ac:adf-parameter>'
        f'</ac:adf-parameter>'
    )

    def adf_node():
        return (
            f'<ac:adf-node type="extension">'
            f'<ac:adf-attribute key="extension-key">{ext_key}</ac:adf-attribute>'
            f'<ac:adf-attribute key="extension-type">com.atlassian.ecosystem</ac:adf-attribute>'
            f'<ac:adf-attribute key="parameters">{params}</ac:adf-attribute>'
            f'<ac:adf-attribute key="text">Mermaid diagram</ac:adf-attribute>'
            f'<ac:adf-attribute key="layout">default</ac:adf-attribute>'
            f'<ac:adf-attribute key="local-id">{local_id}</ac:adf-attribute>'
            f'</ac:adf-node>'
        )

    expand_local_id = str(uuid.uuid4())
    code_html = (
        f'<ac:structured-macro ac:local-id="{code_local_id}" '
        f'ac:name="code" ac:schema-version="1">'
        f'<ac:parameter ac:name="language">mermaid</ac:parameter>'
        f'<ac:plain-text-body><![CDATA[{code}]]></ac:plain-text-body>'
        f'</ac:structured-macro>'
    )
    # Wrap code block in Expand macro — hides source code by default
    expand_html = (
        f'<ac:structured-macro ac:local-id="{expand_local_id}" '
        f'ac:name="expand" ac:schema-version="1">'
        f'<ac:parameter ac:name="title">Mermaid Source</ac:parameter>'
        f'<ac:rich-text-body>{code_html}</ac:rich-text-body>'
        f'</ac:structured-macro>'
    )
    forge_html = (
        f'<ac:adf-extension>'
        f'{adf_node()}'
        f'<ac:adf-fallback>{adf_node()}</ac:adf-fallback>'
        f'</ac:adf-extension>'
    )
    # Expand (collapsed source) + Forge renderer (always visible diagram)
    return expand_html + forge_html


def expand_section(title: str, content: str) -> str:
    """Wrap content in an Expand macro (collapsed by default)."""
    local_id = str(uuid.uuid4())
    return (
        f'<ac:structured-macro ac:local-id="{local_id}" '
        f'ac:name="expand" ac:schema-version="1">'
        f'<ac:parameter ac:name="title">{title}</ac:parameter>'
        f'<ac:rich-text-body>{content}</ac:rich-text-body>'
        f'</ac:structured-macro>'
    )


def status_macro(text: str, colour: str = "Grey") -> str:
    return (
        f'<ac:structured-macro ac:name="status" ac:schema-version="1">'
        f'<ac:parameter ac:name="title">{text}</ac:parameter>'
        f'<ac:parameter ac:name="colour">{colour}</ac:parameter>'
        f"</ac:structured-macro>"
    )


def children_macro() -> str:
    """Confluence Children macro — lists child pages automatically."""
    return (
        '<ac:structured-macro ac:name="children" ac:schema-version="2">'
        '<ac:parameter ac:name="all">true</ac:parameter>'
        '<ac:parameter ac:name="sort">creation</ac:parameter>'
        "</ac:structured-macro>"
    )


def build_parent_content(page_id: str = ARCH_PAGE_ID) -> str:
    """Parent page: Executive Summary text + Children macro (0 mermaid, 0 code blocks)."""
    sections = []

    # Header metadata
    sections.append(info_panel(
        "<p>"
        "<strong>Status:</strong> " + status_macro("DRAFT", "Yellow") + "<br/>"
        "<strong>Author:</strong> {{SLOT_1}}<br/>"
        "<strong>Date:</strong> 2026-02-20<br/>"
        "<strong>Related:</strong> "
        '<a href="https://{{JIRA_SITE}}/wiki/spaces/BEP/pages/81592324">Player Doc</a>'
        " | "
        '<a href="https://{{JIRA_SITE}}/browse/BEP-3335">BEP-3335 Redis Optimization Epic</a>'
        "</p>"
    ))

    # Executive Summary (TEXT ONLY — diagrams moved to page 2)
    sections.append("<h2>Executive Summary</h2>")
    sections.append(success_panel(
        "<p><strong>Problem:</strong> Player มี scheduling logic <strong>3,500+ บรรทัด</strong> "
        "ที่จัดลำดับ ad เอง + ไม่มี offline resilience (fresh boot + no internet = <strong>จอดำ</strong>) "
        "+ ไม่รองรับ premium products (Daypart Takeover, Exact-Time Spot)</p>"
        "<p><strong>Solution:</strong> Backend ส่ง <strong>ordered screen schedule (loop sequence)</strong> แทนที่จะส่ง bag of creatives + rules. "
        "Player แค่เล่น <code>sequence[i++]</code> (Dumb Renderer) + <strong>Interrupt Controller</strong> สำหรับ P0/P1 premium เท่านั้น</p>"
        "<p><strong>Impact:</strong> Player complexity <strong>&darr;80%</strong>, "
        "offline support ผ่าน 3-tier cache (Live &rarr; Buffer &rarr; Fallback), "
        "idempotent sync ป้องกัน duplicate PoP, "
        "<strong>+ premium products:</strong> Daypart Takeover (เหมา time block) + Exact-Time Spot (เล่นตรงเวลา) "
        "with make-good compensation</p>"
    ))

    # Children macro — auto-lists sub-pages
    sections.append("<h2>Contents</h2>")
    sections.append(children_macro())

    return "\n".join(sections)


def build_content(page_id: str = ARCH_PAGE_ID) -> str:
    """LEGACY — original monolithic build. Kept for reference."""
    return build_parent_content(page_id)


# ═══════════════════════════════════════════════════════════════
# Sub-Page Builders
# ═══════════════════════════════════════════════════════════════


def build_page_1(page_id: str) -> str:
    """Page 1: Problem Statement & Current Architecture (2 mermaid, 0 code blocks)."""
    global _code_block_count
    _code_block_count = 0
    sections = []

    sections.append(toc())

    # ── Problem Statement ──
    sections.append("<h2>1. ปัญหาปัจจุบัน (Problem Statement)</h2>")
    sections.append(error_panel(
        "<p><strong>Smart Player (ความซับซ้อนของ Scheduling)</strong></p>"
        "<ul>"
        "<li>Player จัดลำดับ creatives เองใน local (SchedulePlay, TimeSlot, Playlist components)</li>"
        "<li>Guaranteed spot interrupt logic: <code>calculatePlaySchedules</code> poll ทุก <strong>1 วินาที</strong> ผ่าน <code>useQuery</code>, "
        "เช็ค <code>dayjs().isBetween(start, end)</code> &mdash; ความแม่นยำ ±2 วินาที</li>"
        "<li><code>pausePlayData</code> เป็น <strong>ตัวแปรตัวเดียว</strong> &mdash; กรณี nested guaranteed interrupts จะทำให้ creative เดิมหาย "
        "(SMIL standard ใช้ pause <em>queue/stack</em>)</li>"
        "<li>Guaranteed spot media หาย &rarr; <strong>silent failure</strong>: creative ที่โดน interrupt ค้าง pause ตลอด ไม่มี recovery</li>"
        "<li>Guaranteed spots ซ้อนกัน &rarr; <code>find()</code> เลือกตัวแรกเจอ ไม่มี priority logic</li>"
        "<li>มี 2 path แยกกันสร้าง guaranteed PlaySchedules (approval push + loop injection) &mdash; logic ซ้ำซ้อน</li>"
        "<li>Retry queue (สูงสุด 3 ครั้ง), spot rotation tracking, daypart gate</li>"
        "<li>ความซับซ้อนของ Player: scheduling logic <strong>3,500+ บรรทัด</strong> ใน <code>src/components/screen/device/schedule/</code></li>"
        "</ul>"
        "<p><strong>การจัดการ Offline (ปัจจุบัน)</strong></p>"
        "<ul>"
        "<li>ตรวจจับ offline: <code>fetch</code> error ที่ <code>err?.message === 'Load failed'</code></li>"
        "<li>เล่นจาก <code>localStorage</code> cache (schedules + playlists)</li>"
        "<li>ไม่มี graceful fallback: fresh boot + ไม่มี internet = <strong>จอดำ</strong></li>"
        "<li>ไม่มี checksum validation สำหรับ creative assets ที่ download</li>"
        "<li>Guaranteed spot ได้รับ approve ขณะ offline &rarr; Pusher push หาย ไม่มี buffer mechanism</li>"
        "</ul>"
    ))

    # BEP-2998: Impression Delivery Accuracy
    sections.append(warning_panel(
        "<p><strong>Impression Delivery Accuracy (Under-Delivery Problem)</strong> "
        '&mdash; <a href="https://{{JIRA_SITE}}/browse/BEP-2998">BEP-2998</a> '
        '(Epic: <a href="https://{{JIRA_SITE}}/browse/BEP-2134">BEP-2134</a>)</p>'
        "<ul>"
        "<li>กำหนด impression target 15 plays/hr &rarr; ระบบเล่น ~13-15 (<strong>under-delivery up to 13%</strong>)</li>"
        "<li>กำหนด 100 plays/day &rarr; ระบบเล่น ~90-100 (<strong>under-delivery up to 10%</strong>)</li>"
        "<li>สาเหตุ: <code>calculateAdDisplayCount</code> rounding + proportional allocation (<code>Math.ceil(adsAmount * ratio)</code>) ไม่สม่ำเสมอ</li>"
        "<li>Player-side: <code>decrementSchedulePlayCount</code> ใช้ mutex lock + PlayKey idempotency แต่ยัง race condition ได้</li>"
        "<li>DOOH industry เรียกปัญหานี้ว่า <strong>impression shortfall</strong> &mdash; "
        "แก้ด้วย <strong>campaign pacing algorithm</strong> + <strong>SOV (Share of Voice) allocation</strong></li>"
        "</ul>"
    ))

    # ── Current Architecture ──
    sections.append("<hr/>")
    sections.append("<h2>2. สถาปัตยกรรมปัจจุบัน (Current Architecture)</h2>")
    sections.append("<h3>2.1 Backend (tathep-platform-api)</h3>")

    sections.append(mermaid_diagram(
        load_diagram("03-1-backend-pipeline.mmd"),
        page_id=page_id,
    ))

    sections.append(expand_section("Backend Components (13 ไฟล์)",
        '<table>'
        '<tr><th>Component</th><th>File</th><th>Purpose</th></tr>'
        '<tr><td>PlaySchedule model</td><td><code>app/Models/PlaySchedule.ts</code></td><td>Status: WAITING&rarr;PLAYING&rarr;PLAYED, ประเภท: guaranteed/ROS/spot-rotation</td></tr>'
        '<tr><td>Screen model</td><td><code>app/Models/Billboard.ts</code></td><td>ownerTime/platformTime = SOV (Share of Voice) budget (วินาที/ชั่วโมง)</td></tr>'
        '<tr><td>Scheduling Engine</td><td><code>app/Jobs/PlayScheduleCalculate.ts</code></td><td>สร้าง per-screen jobs ทุก N นาที</td></tr>'
        '<tr><td>Per-screen calc</td><td><code>app/Jobs/PlayScheduleCalculatePerScreen.ts</code></td><td>สร้าง PlaySchedule rows สำหรับ 1 จอ</td></tr>'
        '<tr><td>Player-pull mode</td><td><code>app/Jobs/PlayScheduleRoundCreate.ts</code></td><td>POST /v2/play-schedules/request {amount: N}</td></tr>'
        '<tr><td>House content rotation</td><td><code>app/Services/PlayScheduleFrequencyService.ts</code></td><td>หมุนเวียน creative ของเจ้าของจอ + random jitter</td></tr>'
        '<tr><td>Campaign period</td><td><code>app/Services/PlaySchedulePeriodService.ts</code></td><td>Campaign ขายตรง: PER_HOUR/PER_DAY/custom avails</td></tr>'
        '<tr><td>Guaranteed service</td><td><code>app/Services/v2/PlayScheduleExclusiveService.ts</code></td><td>แทรก guaranteed spots ที่ทับ loop window ปัจจุบัน</td></tr>'
        '<tr><td>Guaranteed job</td><td><code>app/Jobs/PlayScheduleCreateByExclusive.ts</code></td><td>On-demand: BullMQ job ทำงานเมื่อ owner approve &rarr; สร้าง PlaySchedule + push ผ่าน Pusher</td></tr>'
        '<tr><td>Guaranteed model</td><td><code>app/Models/AdvertisementDisplayExclusive.ts</code></td><td>จองเวลาต่อจอ (startDateTime/endDateTime/timePerSlot)</td></tr>'
        '<tr><td>Guaranteed time window</td><td><code>app/Models/AdGroupDisplayTimeExclusive.ts</code></td><td>ช่วงเวลา guaranteed ระดับ AdGroup สำหรับแทรกใน loop</td></tr>'
        '<tr><td>Reservation check</td><td><code>app/Services/ServiceHelpers/checkIsBillboardsReserved.ts</code></td><td>ป้องกัน double-booking: ตรวจ overlap ก่อนสร้าง guaranteed avails</td></tr>'
        '<tr><td>Pusher service</td><td><code>app/Services/PusherPlayScheduleService.ts</code></td><td>Channel: play-schedule-{deviceCode}</td></tr>'
        '</table>'
    ))

    sections.append("<h3>2.2 Player (bd-vision-player)</h3>")
    sections.append(mermaid_diagram(
        load_diagram("03-2-player-architecture.mmd"),
        page_id=page_id,
    ))

    sections.append(expand_section("Player Features (8 รายการ)",
        '<table>'
        '<tr><th>Feature</th><th>Implementation</th><th>File</th></tr>'
        '<tr><td>ประเภท Schedule</td><td><code>exclusive</code> (guaranteed spot), <code>continuous</code> (ขายตรง ROS), <code>frequency</code> (หมุนเวียน spot)</td><td><code>src/constants/schedule.constant.ts</code></td></tr>'
        '<tr><td>Loop rotation</td><td><code>(currentIndex + 1) % activeSchedules.length</code></td><td><code>screen.device.schedule.play.timeslot.component.tsx</code></td></tr>'
        '<tr><td>Guaranteed preempt</td><td><code>calculatePlaySchedules</code> (poll ทุก 1 วิ ผ่าน <code>useQuery</code>): '
        '<code>dayjs().isBetween(start, end)</code> &rarr; <code>setPausePlayData(current)</code> &rarr; เล่น guaranteed spot &rarr; '
        'จบแล้ว restore <code>pausePlayData</code>. ตัวแปรเดียว = ไม่รองรับ nested interrupt</td>'
        '<td><code>screen.device.schedule.play.component.tsx</code></td></tr>'
        '<tr><td>Retry queue</td><td>สูงสุด 3 ครั้ง, เก็บใน localStorage</td><td><code>screen.device.schedule.play.timeslot.component.tsx</code></td></tr>'
        '<tr><td>Media download</td><td>Tauri <code>plugin-upload</code> (native HTTP), ดาวน์โหลดทีละไฟล์</td><td><code>screen.device.schedule.setup.schedule-download.tsx</code></td></tr>'
        '<tr><td>File cleanup</td><td>ทุก 24 ชม. ช่วง off-hours, ลบแบบ LRU</td><td><code>src/services/file-cleanup.service.ts</code></td></tr>'
        '<tr><td>ตรวจจับ Offline</td><td><code>err?.message === "Load failed"</code></td><td><code>screen.device.schedule.component.tsx</code></td></tr>'
        '<tr><td>PoP (Proof of Play) retry</td><td>Tauri Store (<code>player.history.json</code>), batch 10 รายการ, ทุก 1 นาที</td><td><code>player-history.store.ts</code></td></tr>'
        '</table>'
    ))

    sections.append("<h3>2.3 Pusher Events</h3>")
    sections.append(expand_section("Pusher Events (6 events)",
        '<table>'
        '<tr><th>Event</th><th>Trigger</th><th>Player Action</th></tr>'
        '<tr><td><code>update-play-schedule</code></td><td>Scheduling engine loop เสร็จ</td><td>ดึง <code>GET /v2/play-schedules</code> ใหม่</td></tr>'
        '<tr><td><code>created-play-schedule</code></td><td>Player-pull job เสร็จ</td><td>ดึง schedules ใหม่</td></tr>'
        '<tr><td><code>approved-advertisement-exclusive</code></td><td>Guaranteed spot ได้รับ approve</td><td>แทรกทันที (ไม่ต้อง re-fetch)</td></tr>'
        '<tr><td><code>stop-advertisement</code></td><td>Creative ถูกยกเลิก</td><td>ลบออกจาก local schedule</td></tr>'
        '<tr><td><code>new/update/delete-play-schedule</code></td><td>Schedule CRUD</td><td>ดึง schedules ใหม่</td></tr>'
        '<tr><td><code>un-pair-screen</code></td><td>Device ถูก unpair</td><td>ล้างทั้งหมด กลับหน้า pair</td></tr>'
        '</table>'
    ))

    return "\n".join(sections)


def build_page_2(page_id: str) -> str:
    """Page 2: Proposed Architecture (3 mermaid — overview + daily schedule + proposed flow)."""
    global _code_block_count
    _code_block_count = 0
    sections = []

    sections.append(toc())

    # Architecture overview diagram (moved from Executive Summary)
    sections.append("<h2>ภาพรวมสถาปัตยกรรม (Architecture Overview)</h2>")
    sections.append(mermaid_diagram(
        load_diagram("01-proposed-architecture.mmd"),
        page_id=page_id,
    ))

    sections.append("<h3>ตัวอย่าง Daily Schedule</h3>")
    sections.append(info_panel(
        "<p>ตัวอย่าง billboard 1 จอ ตลอดวัน — แสดงสัดส่วนเวลาจริงระหว่าง priority levels ต่างๆ. "
        "<strong>P1-TK</strong> (แดง) กินเวลา 1 ชั่วโมงเต็ม, <strong>P1-ET</strong> (แดง) เป็น exact-time spot ที่เล่นตรงเวลา, "
        "<strong>P1-G</strong> (ฟ้า) กระจายตลอดวัน, <strong>P2-P4</strong> เติมช่วงที่เหลือ</p>"
    ))
    sections.append(mermaid_diagram(
        load_diagram("01-2-daily-schedule.mmd"),
        page_id=page_id,
    ))

    sections.append("<hr/>")
    sections.append("<h2>สถาปัตยกรรมที่เสนอ: Backend-Driven Player</h2>")
    sections.append(info_panel(
        "<p><strong>แนวคิดหลัก:</strong> Backend ส่ง <strong>ordered screen schedule (loop sequence)</strong> แทนที่จะส่ง bag of creatives + rules. "
        "Player แค่เล่น <code>sequence[i++]</code> (Dumb Renderer pattern &mdash; มาตรฐาน DOOH)</p>"
    ))

    sections.append("<h3>สิ่งที่เปลี่ยน vs สิ่งที่คงเดิม</h3>")
    sections.append(
        '<table>'
        '<tr><th>Component</th><th>Current</th><th>Proposed</th><th>Change Type</th></tr>'
        '<tr><td>Cron job</td><td>PlayScheduleCalculate ทุก 10 นาที</td><td>เหมือนเดิม</td><td>' + status_macro("NO CHANGE", "Green") + '</td></tr>'
        '<tr><td>Per-screen job</td><td>สร้าง PlaySchedule rows</td><td>สร้าง PlaySchedule + <strong>ordered ScreenSchedule</strong></td><td>' + status_macro("ADD STEP", "Yellow") + '</td></tr>'
        '<tr><td>Pusher</td><td>Channel per device</td><td>Channel เดิม + event ใหม่ <code>schedule-updated</code></td><td>' + status_macro("ADD EVENT", "Yellow") + '</td></tr>'
        '<tr><td>Player API</td><td>GET /v2/play-schedules + /playlist-advertisements</td><td><strong>GET /v2/screen-schedule</strong> (รวมเป็นอันเดียว)</td><td>' + status_macro("NEW ENDPOINT", "Blue") + '</td></tr>'
        '<tr><td>Player scheduling</td><td>Loop rotation + guaranteed interrupt (ซับซ้อน)</td><td><strong>play sequence[i++]</strong> (Dumb Renderer)</td><td>' + status_macro("SIMPLIFY", "Green") + '</td></tr>'
        '<tr><td>Player storage</td><td>localStorage (แยก schedules + playlists)</td><td>Tauri Store (3-tier playlist)</td><td>' + status_macro("MIGRATE", "Yellow") + '</td></tr>'
        '<tr><td>Media download</td><td>Tauri plugin-upload</td><td>เหมือนเดิม</td><td>' + status_macro("NO CHANGE", "Green") + '</td></tr>'
        '<tr><td>BullMQ</td><td>Redis queue</td><td>เหมือนเดิม</td><td>' + status_macro("NO CHANGE", "Green") + '</td></tr>'
        '<tr><td>Auth</td><td>x-device-code header</td><td>เหมือนเดิม</td><td>' + status_macro("NO CHANGE", "Green") + '</td></tr>'
        '<tr><td>Proof of Play (PoP)</td><td>POST /v2/play-history + retry</td><td>เหมือนเดิม + <strong>Outbox pattern</strong> + interrupt fields</td><td>' + status_macro("ENHANCE", "Yellow") + '</td></tr>'
        '<tr><td><strong>Interrupt Controller</strong></td><td>N/A</td><td><strong>ใหม่:</strong> Lightweight IC สำหรับ P0/P1-TK/P1-ET เท่านั้น. P2-P4 รอ creative เล่นจบ</td><td>' + status_macro("NEW", "Blue") + '</td></tr>'
        '<tr><td><strong>TK Booking API</strong></td><td>N/A</td><td><strong>ใหม่:</strong> Daypart Takeover booking + ตรวจ overlap + lead time check</td><td>' + status_macro("NEW", "Blue") + '</td></tr>'
        '<tr><td><strong>Make-Good System</strong></td><td>N/A</td><td><strong>ใหม่:</strong> Ad ที่โดน interrupt ได้ slot ชดเชยใน cycle ถัดไป</td><td>' + status_macro("NEW", "Blue") + '</td></tr>'
        '</table>'
    )

    sections.append("<h3>การ Map Infrastructure</h3>")
    sections.append(
        '<table>'
        '<tr><th>Existing Infrastructure</th><th>Role Today</th><th>Role in Proposed</th><th>Change</th></tr>'
        '<tr><td><strong>BullMQ + Redis</strong></td><td>Cron job queue (PlayScheduleCalculate)</td><td>เหมือนเดิม + เพิ่ม Ad Decisioning Engine หลัง schedule calc</td><td>' + status_macro("REUSE", "Green") + '</td></tr>'
        '<tr><td><strong>MySQL</strong></td><td>PlaySchedule, Billboard, Advertisement models</td><td>เหมือนเดิม + ตาราง ScreenSchedule, ScreenScheduleItem ใหม่</td><td>' + status_macro("ADD TABLES", "Yellow") + '</td></tr>'
        '<tr><td><strong>Redis (cache)</strong></td><td>GET/SET string cache (Bentocache)</td><td>เหมือนเดิม + idempotency keys (SET TTL 24 ชม.)</td><td>' + status_macro("REUSE", "Green") + '</td></tr>'
        '<tr><td><strong>Pusher (WebSocket)</strong></td><td>6 event types, channel per device</td><td>Channel เดิม + 5 typed events ใหม่ (schedule-updated, device-config-updated, takeover-start, takeover-end, p0-emergency)</td><td>' + status_macro("ADD EVENTS", "Yellow") + '</td></tr>'
        '<tr><td><strong>AdonisJS routes</strong></td><td>Player V2 routes (/play-schedules, /playlist-advertisements)</td><td>คง route เดิม + เพิ่ม GET /v2/screen-schedule</td><td>' + status_macro("ADD ENDPOINT", "Yellow") + '</td></tr>'
        '<tr><td><strong>Tauri plugin-upload</strong></td><td>Native HTTP media download</td><td>เหมือนเดิม (ดาวน์โหลดทีละไฟล์ + resume)</td><td>' + status_macro("NO CHANGE", "Green") + '</td></tr>'
        '<tr><td><strong>localStorage</strong></td><td>Schedules, playlists, playData</td><td>ย้ายข้อมูลหนักไป Tauri Store; localStorage เก็บแค่ small state</td><td>' + status_macro("MIGRATE", "Yellow") + '</td></tr>'
        '<tr><td><strong>Tauri Store</strong></td><td>player.history.json (play history retry)</td><td>+ outbox.json, playlist-cache.json, inbox-state.json</td><td>' + status_macro("EXPAND", "Yellow") + '</td></tr>'
        '<tr><td><strong>Pusher client (player)</strong></td><td>Subscribe, re-fetch on event</td><td>เหมือนเดิม + inbox dedup layer (event_id + version check)</td><td>' + status_macro("WRAP", "Yellow") + '</td></tr>'
        '<tr><td><strong>x-device-code auth</strong></td><td>Player auth header</td><td>เหมือนเดิม</td><td>' + status_macro("NO CHANGE", "Green") + '</td></tr>'
        '</table>'
    )

    return "\n".join(sections)


def build_page_3(page_id: str) -> str:
    """Page 3: Key Flows (6 mermaid, 0 code blocks)."""
    global _code_block_count
    _code_block_count = 0
    sections = []

    sections.append(toc())
    sections.append("<h2>Flow หลัก (Key Flows)</h2>")

    sections.append("<h3>Flow A: เล่นปกติ Online (Happy Path)</h3>")
    sections.append(mermaid_diagram(
        load_diagram("05-1-flow-normal.mmd"),
        page_id=page_id,
    ))

    sections.append("<h3>Flow B: เน็ตหลุด &rarr; Offline &rarr; เชื่อมต่อใหม่</h3>")
    sections.append(mermaid_diagram(
        load_diagram("05-2-flow-network-drop.mmd"),
        page_id=page_id,
    ))

    sections.append("<h3>Flow C: Interrupt แบบ Guaranteed Spot (Online)</h3>")
    sections.append(warning_panel(
        "<p><strong>ระบบเดิมมี 2 เส้นทางสำหรับ guaranteed spots (เดิมเรียก exclusive):</strong></p>"
        "<ul>"
        "<li><strong>เส้นทาง 1 (ตอน approve):</strong> Owner approve &rarr; BullMQ <code>PlayScheduleCreateByExclusive</code> job &rarr; "
        "สร้าง PlaySchedule rows (type=EXCLUSIVE, createdBy=EXCLUSIVE_APPROVED) &rarr; "
        "Pusher <code>approved-advertisement-exclusive</code> พร้อม payload เต็ม &rarr; Player inject ทันที</li>"
        "<li><strong>เส้นทาง 2 (ระหว่าง loop):</strong> <code>PlayScheduleExclusiveService</code> เช็ค <code>AdGroupDisplayTimeExclusive</code> "
        "ที่ overlap กับ loop window ปัจจุบัน &rarr; สร้าง PlaySchedule rows (createdBy=PLAYER_REQUEST)</li>"
        "</ul>"
        "<p><strong>ที่เสนอให้ปรับ:</strong> Ad Decisioning Engine จัดการทั้ง 2 เส้นทาง &mdash; "
        "guaranteed spots ถูก inject เข้า ordered sequence ที่ตำแหน่ง <code>play_at</code> ที่แน่นอนตั้งแต่แรก. "
        "Player ไม่ต้องมี guaranteed interrupt logic อีกต่อไป.</p>"
    ))
    sections.append(mermaid_diagram(
        load_diagram("05-3-flow-exclusive.mmd"),
        page_id=page_id,
    ))

    sections.append("<h3>Flow D: เปิดเครื่องใหม่ ไม่มี Cache (Fresh Boot)</h3>")
    sections.append(mermaid_diagram(
        load_diagram("05-4-flow-fresh-boot.mmd"),
        page_id=page_id,
    ))

    sections.append("<h3>Flow E: เหมาช่วงเวลา (Daypart Takeover)</h3>")
    sections.append(info_panel(
        "<p><strong>Daypart Takeover (เหมา time block):</strong> ลูกค้าซื้อช่วงเวลาทั้งหมด (เช่น 08:00-09:00) "
        "วน ad เดียวไม่หยุด ไม่มี ad อื่นแทรกได้ยกเว้น P0 Emergency. "
        "Billing: <strong>CPT (Cost Per Time)</strong> — flat rate ต่อ time block. "
        'ใช้แนวคิดจาก <a href="https://docs.broadsign.com/broadsign-control/latest/en/settings-section.html">'
        "Broadsign Day Part Switch Behavior</a> (configurable interrupt at boundaries).</p>"
    ))
    sections.append(mermaid_diagram(
        load_diagram("05-5-flow-takeover.mmd"),
        page_id=page_id,
    ))

    sections.append("<h3>Flow F: เล่นตรงเวลา (Exact-Time Spot)</h3>")
    sections.append(info_panel(
        "<p><strong>Exact-Time Spot:</strong> Ad ต้องเล่นตรงเวลาที่กำหนด (±5 วินาที). "
        "Interrupt Controller จะหยุด creative ที่กำลังเล่น (P2-P4 เท่านั้น) แล้วเล่น ET spot ทันที. "
        "Billing: <strong>Flat per spot</strong>. "
        "Ad ที่โดน interrupt จะได้ <strong>make-good</strong> compensation ใน cycle ถัดไป.</p>"
    ))
    sections.append(mermaid_diagram(
        load_diagram("05-6-flow-exact-time.mmd"),
        page_id=page_id,
    ))

    return "\n".join(sections)


def build_page_4(page_id: str) -> str:
    """Page 4: Technical Design — Algorithm & Models (0 mermaid, 4 code blocks)."""
    global _code_block_count
    _code_block_count = 0
    sections = []

    sections.append(toc())
    sections.append("<h2>Technical Design: Algorithm และ Models</h2>")

    # Ad Decisioning Algorithm
    sections.append("<h3>Ad Decisioning Algorithm (ขั้นตอนจัดลำดับ Ad)</h3>")
    sections.append(note_panel(
        "<p><strong>หลักการสำคัญ:</strong> Ad Decisioning Engine ทำงาน <em>หลัง</em> PlayScheduleCalculatePerScreen ที่มีอยู่เดิม. "
        "รับ PlaySchedule rows (คำนวณไว้แล้ว) แล้วแปลงเป็น <strong>ordered loop sequence</strong>.</p>"
        "<p><strong>Guaranteed spots (เดิมเรียก exclusive):</strong> ปัจจุบันจัดการด้วย 2 เส้นทางแยกกัน "
        "(<code>PlayScheduleCreateByExclusive</code> ตอน approve + <code>PlayScheduleExclusiveService</code> ระหว่าง loop). "
        "Ad Decisioning Engine <strong>รวมทั้ง 2 เส้นทาง</strong> &mdash; guaranteed spots ถูก inject ที่ตำแหน่ง <code>play_at</code> "
        "ตรงจุดใน sequence. ตรวจสอบการจองซ้ำด้วย <code>checkIsBillboardsReserved</code>. "
        "Billing ใช้ <code>exclusiveMultiplier</code> (env: <code>ADVERTISEMENT_EXCLUSIVE_MULTIPLIER</code>).</p>"
    ))
    sections.append(
        '<table>'
        '<tr><th>Priority</th><th>DOOH Type</th><th>Interrupt?</th><th>Scheduling</th><th>Billing</th></tr>'
        '<tr><td><strong>P0</strong></td><td>Emergency</td><td>' + status_macro("YES — all", "Red") + '</td><td>แจ้งเตือนระบบ, unpair, maintenance</td><td>N/A</td></tr>'
        '<tr><td><strong>P1-TK</strong></td><td>Daypart Takeover</td><td>' + status_macro("YES — boundaries", "Red") + '</td><td>เหมา time block วน ad เดียว (TK_START → loop → TK_END)</td><td>CPT (flat/time block)</td></tr>'
        '<tr><td><strong>P1-ET</strong></td><td>Exact-Time Spot</td><td>' + status_macro("YES — P2-P4", "Red") + '</td><td>เล่นตรงเวลา ±5s tolerance</td><td>Flat per spot</td></tr>'
        '<tr><td><strong>P1-G</strong></td><td>Guaranteed Spot</td><td>' + status_macro("NO — pre-positioned", "Green") + '</td><td>จอง time slot เล่นตรงตำแหน่ง <code>play_at</code> ใน sequence</td><td><code>exclusiveMultiplier</code></td></tr>'
        '<tr><td><strong>P2</strong></td><td>Direct-Sold ROS</td><td>' + status_macro("NO", "Green") + '</td><td>Campaign creatives ตาม date-range (run-of-schedule)</td><td>Standard rate</td></tr>'
        '<tr><td><strong>P3</strong></td><td>Spot Buy / Programmatic</td><td>' + status_macro("NO", "Green") + '</td><td>Campaign ตาม impression target (อนาคต: RTB ผ่าน SSP)</td><td>Standard / CPM</td></tr>'
        '<tr><td><strong>P4</strong></td><td>House / Filler</td><td>' + status_macro("NO", "Green") + '</td><td>Content default ของเจ้าของจอ (house loop)</td><td>N/A</td></tr>'
        '</table>'
    )
    sections.append(note_panel(
        "<p><strong>กฎการ Interrupt:</strong></p>"
        "<ul>"
        "<li><strong>P0/P1-TK/P1-ET:</strong> Interrupt creative ปัจจุบันทันที → <strong>stop</strong> (ไม่ pause/resume) "
        '— แนวคิดจาก <a href="https://xibosignage.com/manual/en/layouts_interrupt">Xibo Interrupt Layout</a></li>'
        "<li><strong>P1-G/P2/P3/P4:</strong> รอ creative ปัจจุบันจบก่อน (no interrupt)</li>"
        "<li>หลัง interrupt: resume จาก <strong>next item</strong> ใน schedule (ไม่ restart creative ที่โดน interrupt)</li>"
        "<li>Ad ที่โดน interrupt ได้ <strong>make-good</strong> compensation ใน cycle ถัดไป (partial play ไม่นับ impression)</li>"
        "<li>Takeover ซ้อนกันไม่ได้ (1 time block = 1 owner)</li>"
        "</ul>"
    ))

    sections.append(tracked_code_block(
        "// Ad Decisioning Algorithm v3 (Timeline-Based + Interrupt-Capable)\n"
        "// Inspired by: SMIL <excl> + Broadsign Day Part Switch + Xibo Interrupt Layout\n"
        "// Addresses: BEP-2998 under-delivery + Daypart Takeover + Exact-Time Spot + Make-Good\n\n"
        "Input:\n"
        "  - playSchedules[]: from PerScreen calc (direct-sold ROS + spot buy)\n"
        "  - guaranteedSchedules[]: from AdGroupDisplayTimeExclusive (overlapping this loop)\n"
        "  - takeoverSchedules[]: from TakeoverSchedule (overlapping this loop)\n"
        "  - exactTimeSpots[]: from ExactTimeSpot (overlapping this loop)\n"
        "  - pendingMakeGoods[]: from MakeGoodRecord where compensated=false\n"
        "  - housePlaylist[]: from PlaylistAdvertisement (owner/filler content)\n"
        "  - screen: { ownerTime, platformTime }  // SOV budget (seconds/hour)\n"
        "  - loopDuration: 600  // seconds (10 min)\n\n"
        "Step 0 (NEW): Reserve Exact-Time Spots (P1-ET)\n"
        "  for (const et of exactTimeSpots.sortBy('play_at')) {\n"
        "    timeline.reserveExact(et.play_at, et.tolerance_seconds, {\n"
        "      priority: 'P1-ET', interruptIfNeeded: true\n"
        "    })\n"
        "  }\n\n"
        "Step 1: Reserve Guaranteed Slots FIRST (P1-G)\n"
        "  timeline = createTimeline(loopStart, loopDuration)  // 600s\n"
        "  for (const g of guaranteedSchedules.sortBy('startDateTime')) {\n"
        "    if (!g.media?.file_url) { alertAdmin(g); continue }\n"
        "    timeline.reserve(g.play_at, g.duration, { priority: 'P1-G', ...g })\n"
        "  }\n\n"
        "Step 1.5 (NEW): Reserve Takeover Blocks (P1-TK)\n"
        "  for (const tk of takeoverSchedules.sortBy('start_time')) {\n"
        "    validate: no overlap with other TK (checkIsBillboardsReserved extended)\n"
        "    timeline.reserveTakeover(tk.start_time, tk.end_time, {\n"
        "      priority: 'P1-TK', loop: true, billing: 'CPT',\n"
        "      creative_code: tk.creative_code\n"
        "    })\n"
        "  }\n\n"
        "Step 2: Calculate SOV (Share of Voice) ratio for remaining avails\n"
        "  houseSOV = screen.ownerTime / (ownerTime + platformTime)\n"
        "  interleaveEvery = Math.round(1 / houseSOV)\n\n"
        "Step 2.5: Campaign Pacing (addresses BEP-2998 under-delivery)\n"
        "  for (const campaign of [...directSold, ...spotBuy]) {\n"
        "    target = campaign.impression_target\n"
        "    delivered = campaign.delivered_today\n"
        "    remaining = target - delivered\n"
        "    pacing_rate = remaining / remaining_loops_today\n"
        "  }\n\n"
        "Step 3: Fill unreserved avails with campaign + house creatives\n"
        "  availableAvails = timeline.getUnreservedSlots()\n"
        "  campaignAds = [...directSold, ...spotBuy]  // P2 before P3\n"
        "  houseIndex = 0\n\n"
        "  for (const avail of availableAvails) {\n"
        "    while (avail.hasCapacity() && campaignAds.length > 0) {\n"
        "      avail.push(campaignAds.shift())  // campaign creative\n"
        "      if (avail.count % interleaveEvery === 0) {\n"
        "        avail.push(housePlaylist[houseIndex++ % housePlaylist.length])\n"
        "      }\n"
        "    }\n"
        "  }\n\n"
        "Step 4: Fill remaining gaps with house content (P4 filler)\n"
        "  for (const emptyAvail of timeline.getEmptySlots()) {\n"
        "    emptyAvail.push(housePlaylist[houseIndex++ % housePlaylist.length])\n"
        "  }\n\n"
        "Step 5: Flatten timeline → ordered loop sequence\n"
        "  sequence = timeline.flatten()  // chronological order\n"
        "  sequence.forEach((item, i) => item.sequence_no = i + 1)\n\n"
        "Step 5.5 (NEW): Insert Make-Good Items\n"
        "  for (const mg of pendingMakeGoods) {\n"
        "    if (!mg.campaign.isValid()) { mg.skip(); continue }  // expired → log for reconcile\n"
        "    // Insert as first item after guaranteed/takeover slots\n"
        "    sequence.insertAfterReserved(mg.toScheduleItem())\n"
        "    mg.markCompensated()\n"
        "  }\n\n"
        "Step 6: Version + persist\n"
        "  version = (lastVersion for this device) + 1\n"
        "  Save ScreenSchedule { version, tier: 'live', items: sequence }\n"
        "  Mark previous 'live' schedule as 'replaced'\n\n"
        "Output:\n"
        "  ScreenSchedule v42 with ordered items[]\n"
        "  Player plays: items[0] → items[1] → items[2] → ...\n"
        "  P1-G items are pre-positioned in sequence (no interrupt needed)\n"
        "  P1-TK/P1-ET items trigger Interrupt Controller (real-time interrupt)\n"
        "  Make-good items compensate interrupted ads",
        "typescript", "Ad Decisioning Algorithm v3",
        collapse=True,
    ))

    # New Data Models
    sections.append("<h3>Data Models ใหม่</h3>")
    sections.append(tracked_code_block(
        "// NEW: ScreenSchedule model (app/Models/ScreenSchedule.ts)\n"
        "interface ScreenSchedule {\n"
        "  id: number\n"
        "  device_code: string\n"
        "  tier: 'live' | 'buffer' | 'fallback'\n"
        "  version: number          // monotonically increasing per device\n"
        "  valid_from: DateTime\n"
        "  valid_until: DateTime\n"
        "  status: 'active' | 'expired' | 'replaced'\n"
        "  created_at: DateTime\n"
        "}\n\n"
        "// NEW: ScreenScheduleItem model (app/Models/ScreenScheduleItem.ts)\n"
        "interface ScreenScheduleItem {\n"
        "  id: number\n"
        "  screen_schedule_id: number\n"
        "  sequence_no: number      // ordered by backend\n"
        "  play_schedule_code: string | null  // link to existing PlaySchedule\n"
        "  advertisement_code: string\n"
        "  creative_code: string    // creative asset identifier\n"
        "  duration_seconds: number\n"
        "  type: 'campaign' | 'house'  // campaign = sold inventory, house = filler\n"
        "  priority: 'guaranteed' | 'direct' | 'spot' | 'house'\n"
        "  play_at: DateTime | null  // for guaranteed/exact-time: exact time\n"
        "  interrupt_capable: boolean  // P1-TK/P1-ET = true, others = false\n"
        "}\n\n"
        "// NEW: TakeoverSchedule model (app/Models/TakeoverSchedule.ts)\n"
        "interface TakeoverSchedule {\n"
        "  id: number\n"
        "  device_code: string\n"
        "  advertisement_code: string\n"
        "  creative_code: string\n"
        "  start_time: DateTime      // e.g. 08:00:00\n"
        "  end_time: DateTime        // e.g. 09:00:00\n"
        "  status: 'booked' | 'active' | 'completed' | 'cancelled'\n"
        "  billing_type: 'CPT'       // Cost Per Time — flat rate per block\n"
        "  created_at: DateTime\n"
        "}\n\n"
        "// NEW: ExactTimeSpot model (app/Models/ExactTimeSpot.ts)\n"
        "interface ExactTimeSpot {\n"
        "  id: number\n"
        "  device_code: string\n"
        "  play_schedule_code: string\n"
        "  play_at: DateTime          // exact time to play\n"
        "  tolerance_seconds: number  // default: 5\n"
        "  billing_type: 'flat'       // flat per spot\n"
        "}\n\n"
        "// NEW: MakeGoodRecord model (app/Models/MakeGoodRecord.ts)\n"
        "interface MakeGoodRecord {\n"
        "  id: number\n"
        "  device_code: string\n"
        "  advertisement_code: string\n"
        "  interrupted_at: DateTime\n"
        "  play_duration_seconds: number  // how much played before interrupt\n"
        "  interrupt_reason: 'P0_emergency' | 'TK_start' | 'TK_end' | 'P1_exact_time'\n"
        "  compensated: boolean\n"
        "  compensated_at: DateTime | null\n"
        "}",
        "typescript", "New Models",
        collapse=True,
    ))

    sections.append(tracked_code_block(
        "// NEW: Ad Decisioning Engine (app/Services/AdDecisioningService.ts)\n"
        "// Called AFTER PlayScheduleCalculatePerScreen generates PlaySchedule rows\n\n"
        "class AdDecisioningService {\n"
        "  async buildSchedule(\n"
        "    screenCode: string,\n"
        "    playSchedules: PlaySchedule[],   // from cron calculation\n"
        "    housePlaylist: PlaylistAdvertisement[],  // house/filler content\n"
        "    screen: Billboard\n"
        "  ): Promise<ScreenSchedule> {\n"
        "    // 1. Sort campaign creatives by priority/time (P1 > P2 > P3)\n"
        "    // 2. Interleave house content based on SOV ratio (ownerTime/platformTime)\n"
        "    // 3. Insert guaranteed spots at their exact play_at position\n"
        "    // 4. Apply campaign pacing (BEP-2998: even impression distribution)\n"
        "    // 5. Assign sequence_no (1, 2, 3, ...)\n"
        "    // 6. Set valid_from/valid_until from loop window\n"
        "    // 7. Increment version (per device)\n"
        "    // 8. Create ScreenSchedule + ScreenScheduleItem rows\n"
        "    // 9. Mark previous 'live' schedule as 'replaced'\n"
        "  }\n\n"
        "  async buildBufferSchedule(\n"
        "    screenCode: string,\n"
        "    hoursAhead: number = 4\n"
        "  ): Promise<ScreenSchedule> {\n"
        "    // Pre-generate next N hours of schedule for offline buffer\n"
        "  }\n\n"
        "  async buildFallbackSchedule(\n"
        "    screenCode: string\n"
        "  ): Promise<ScreenSchedule> {\n"
        "    // House content only, loopable, rarely changes\n"
        "  }\n"
        "}",
        "typescript", "Ad Decisioning Engine Service",
        collapse=True,
    ))

    # New API Endpoint
    sections.append("<h3>API Endpoint ใหม่</h3>")
    sections.append(tracked_code_block(
        "// GET /v2/screen-schedule?tier=live&since_version=41\n"
        "// Response:\n"
        "{\n"
        '  "version": 42,\n'
        '  "tier": "live",\n'
        '  "full": false,             // true if gap > 3 versions (full replace)\n'
        '  "valid_from": "2026-02-20T14:00:00+07:00",\n'
        '  "valid_until": "2026-02-20T14:10:00+07:00",\n'
        '  "items": [\n'
        "    {\n"
        '      "sequence_no": 1,\n'
        '      "advertisement_code": "AD-xxx",\n'
        '      "creative_code": "CR-xxx",\n'
        '      "creative_url": "https://cdn.../video.mp4",\n'
        '      "creative_checksum": "a1b2c3d4...",  // MD5 for validation\n'
        '      "duration_seconds": 15,\n'
        '      "type": "campaign",\n'
        '      "priority": "direct",\n'
        '      "interrupt_capable": false\n'
        "    },\n"
        "    {\n"
        '      "sequence_no": 5,\n'
        '      "advertisement_code": "AD-tk-001",\n'
        '      "creative_code": "CR-tk-001",\n'
        '      "creative_url": "https://cdn.../takeover.mp4",\n'
        '      "duration_seconds": 30,\n'
        '      "type": "takeover",\n'
        '      "priority": "P1-TK",\n'
        '      "interrupt_capable": true,\n'
        '      "takeover_id": 42,\n'
        '      "takeover_start": "2026-02-20T08:00:00+07:00",\n'
        '      "takeover_end": "2026-02-20T09:00:00+07:00"\n'
        "    },\n"
        "    ...\n"
        "  ],\n"
        '  "creative_manifest": [\n'
        '    { "creative_code": "CR-xxx", "url": "...", "checksum": "...", "size_bytes": 12345 }\n'
        "  ],\n"
        '  "pending_takeovers": [\n'
        '    { "takeover_id": 42, "start": "08:00:00", "end": "09:00:00", "creative_code": "CR-tk-001" }\n'
        "  ],\n"
        '  "exact_time_spots": [\n'
        '    { "play_at": "2026-02-20T14:30:00+07:00", "tolerance_seconds": 5, "creative_code": "CR-et-001" }\n'
        "  ]\n"
        "}",
        "json", "API Response Format",
        collapse=True,
    ))

    return "\n".join(sections)


def build_page_5(page_id: str) -> str:
    """Page 5: Technical Design — Player Components (5 mermaid, 4 code blocks)."""
    global _code_block_count
    _code_block_count = 0
    sections = []

    sections.append(toc())
    sections.append("<h2>Technical Design: Player Components</h2>")

    # 3-Tier Playlist Cache
    sections.append("<h3>ระบบ Cache 3 ชั้น (3-Tier Playlist Cache)</h3>")
    sections.append(mermaid_diagram(
        load_diagram("06-4-three-tier-cache.mmd"),
        page_id=page_id,
    ))

    # Player State Machine
    sections.append("<h3>Player State Machine</h3>")
    sections.append(mermaid_diagram(
        load_diagram("06-5-state-machine.mmd"),
        page_id=page_id,
    ))
    sections.append(warning_panel(
        "<p><strong>กฎสำคัญ:</strong></p>"
        "<ul>"
        "<li>ทุก state ต้องมีอะไรแสดงเสมอ. <strong>จอดำ (black screen) ยอมรับไม่ได้เด็ดขาด.</strong></li>"
        "<li><strong>INTERRUPTED</strong> เป็น transient state — หยุด creative ปัจจุบัน → เล่น interrupt content → resume item ถัดไป. "
        "Trigger: P0 emergency, P1-TK boundary, P1-ET ±5s. ดู §6.10 Interrupt Controller</li>"
        "</ul>"
    ))

    # PoP Reporting (Outbox/Inbox)
    sections.append("<h3>ระบบรายงาน PoP (Outbox/Inbox)</h3>")
    sections.append(error_panel(
        "<p><strong>ปัญหา 1 (Player &rarr; Backend): Duplicate PoP (Proof of Play)</strong><br/>"
        "Player POST <code>/v2/play-history</code> &rarr; timeout &rarr; retry &rarr; backend ได้ 2 รายการ สำหรับ creative เดียวกัน</p>"
        "<p><strong>ปัญหา 2 (Backend &rarr; Player): Missed Pusher Events</strong><br/>"
        "Pusher disconnect 30 วิ &rarr; reconnect &rarr; events ระหว่างนั้นหายไป &rarr; Player ไม่รู้ว่ามี schedule ใหม่</p>"
        "<p><strong>ปัญหา 3 (Backend &rarr; Player): Duplicate Pusher Events</strong><br/>"
        "Pusher ส่ง event ซ้ำ (at-least-once) &rarr; player process ซ้ำ &rarr; fetch ซ้ำ &rarr; เสีย bandwidth</p>"
    ))
    sections.append(info_panel(
        "<p><strong>แนวทางแก้:</strong> Outbox (Player&rarr;Backend) + Inbox (Backend&rarr;Player)</p>"
    ))

    sections.append("<h4>Player Outbox (PoP Reporting)</h4>")
    sections.append(mermaid_diagram(
        load_diagram("06-6a-outbox.mmd"),
        page_id=page_id,
    ))
    sections.append(tracked_code_block(
        "// TypeScript interface\n"
        "interface OutboxItem {\n"
        "  id: string              // UUID — idempotency key\n"
        "  type: 'play_history' | 'diagnostic'\n"
        "  payload: PlayHistoryPayload | DiagnosticPayload\n"
        "  status: 'pending' | 'sent' | 'acked'\n"
        "  retry_count: number\n"
        "  created_at: string      // ISO 8601\n"
        "}\n\n"
        "// Flush cycle (existing 1-min interval):\n"
        "// 1. Read all 'pending' items from Tauri Store\n"
        "// 2. Batch POST /v2/play-history with X-Idempotency-Key header\n"
        "// 3. On 200 OK → mark 'acked', store ack_id\n"
        "// 4. On timeout/error → keep 'pending', retry_count++\n"
        "// 5. retry_count > 10 → mark 'failed', log diagnostic (increased from current 3)\n"
        "// 6. Cleanup: remove 'acked' items older than 24h",
        "typescript", "Outbox Interface",
        collapse=True,
    ))

    sections.append("<h4>Player Inbox (Schedule Sync)</h4>")
    sections.append(mermaid_diagram(
        load_diagram("06-6b-inbox.mmd"),
        page_id=page_id,
    ))
    sections.append(tracked_code_block(
        "// TypeScript implementation\n"
        "function handlePlaylistUpdated(event: PusherEvent) {\n"
        "  const { event_id, version } = event\n\n"
        "  // Dedup: check if already processed\n"
        "  if (inbox.has(event_id) || version <= localVersion) {\n"
        "    return // skip duplicate\n"
        "  }\n\n"
        "  // Gap detection\n"
        "  if (version > localVersion + 3) {\n"
        "    // Too many missed events → full re-fetch\n"
        "    fetchFullPlaylist()\n"
        "  } else if (version > localVersion + 1) {\n"
        "    // Small gap → delta fetch\n"
        "    fetchDeltaPlaylist(localVersion)\n"
        "  } else {\n"
        "    // Normal: version = localVersion + 1\n"
        "    fetchDeltaPlaylist(localVersion)\n"
        "  }\n\n"
        "  inbox.add(event_id) // keep last 100\n"
        "}",
        "typescript", "Inbox Deduplication Code",
        collapse=True,
    ))

    # Version Protocol
    sections.append("<h3>Version Protocol</h3>")
    sections.append(mermaid_diagram(
        load_diagram("06-7-version-protocol.mmd"),
        page_id=page_id,
    ))

    # PoP Deduplication
    sections.append("<h3>PoP Deduplication (Idempotency ฝั่ง Backend)</h3>")
    sections.append(tracked_code_block(
        "// Backend: PlayHistoryController\n"
        "async store({ request }: HttpContextContract) {\n"
        "  const idempotencyKey = request.header('X-Idempotency-Key')\n\n"
        "  if (idempotencyKey) {\n"
        "    // Check Redis first (fast path, TTL 24h)\n"
        "    const existing = await Redis.get(`play_history:idem:${idempotencyKey}`)\n"
        "    if (existing) {\n"
        "      return { status: 'already_processed', ack_id: existing }\n"
        "    }\n"
        "  }\n\n"
        "  const history = await PlayHistory.create(payload)\n\n"
        "  if (idempotencyKey) {\n"
        "    await Redis.setex(`play_history:idem:${idempotencyKey}`, 86400, history.code)\n"
        "  }\n\n"
        "  return { status: 'created', ack_id: history.code }\n"
        "}",
        "typescript", "Backend Idempotency Check",
        collapse=True,
    ))

    # Programmatic Integration Points
    sections.append("<h3>จุดเชื่อมต่อ Programmatic (pDOOH Roadmap)</h3>")
    sections.append(info_panel(
        "<p><strong>Scale 100-500 จอ:</strong> ยังไม่ต้อง SSP/DSP เต็มรูปแบบ แต่เตรียม integration points ไว้ "
        "ให้ pluggable เมื่อขยาย scale ในอนาคต. ไม่เพิ่ม tech stack ใหม่ &mdash; ใช้ AdonisJS + Redis + BullMQ เดิม.</p>"
    ))
    sections.append(mermaid_diagram(
        load_diagram("06-9-pdooh-integration.mmd"),
        page_id=page_id,
    ))
    sections.append(
        '<table>'
        '<tr><th>Integration Point</th><th>Current</th><th>pDOOH Extension (Future)</th></tr>'
        '<tr><td><strong>P3 slot fill</strong></td><td>หมุนเวียน spot ภายใน (count-based)</td><td>SSP ad request &rarr; RTB auction &rarr; winning creative หรือ fallback</td></tr>'
        '<tr><td><strong>PoP reporting</strong></td><td>POST /v2/play-history</td><td>เพิ่ม: <code>impression_id</code>, <code>campaign_id</code>, <code>creative_id</code>, <code>viewability_score</code></td></tr>'
        '<tr><td><strong>Inventory avails</strong></td><td>N/A</td><td><code>GET /v2/avails?screen_id=X&amp;daypart=Y</code> &mdash; เปิด slot ว่างให้ SSP เห็น</td></tr>'
        '<tr><td><strong>Campaign pacing</strong></td><td>BEP-2998 fix (proportional พื้นฐาน)</td><td>กระจาย impression ให้สม่ำเสมอตลอด flight + จัดสรรตาม SOV</td></tr>'
        '<tr><td><strong>Fill rate tracking</strong></td><td>N/A</td><td>% ของ P3 avails ที่เติมด้วย programmatic vs house content</td></tr>'
        '<tr><td><strong>Audience estimation</strong></td><td>N/A</td><td>ส่ง <code>audience_est</code> (foot traffic / ช่วงเวลา) ใน ad request</td></tr>'
        '</table>'
    )

    return "\n".join(sections)


def build_page_6(page_id: str) -> str:
    """Page 6: Interrupt Controller & Make-Good (2 mermaid, 0 code blocks)."""
    global _code_block_count
    _code_block_count = 0
    sections = []

    sections.append(toc())
    sections.append("<h2>Interrupt Controller และระบบ Make-Good</h2>")

    # Interrupt Controller
    sections.append("<h3>Interrupt Controller (ตัวควบคุมการ Interrupt)</h3>")
    sections.append(warning_panel(
        "<p><strong>การตัดสินใจออกแบบ: Selective Interrupt.</strong> "
        "Player ยังเป็น Dumb Renderer สำหรับ P1-G/P2/P3/P4 (รอ creative จบก่อน). "
        "แต่มี <strong>lightweight Interrupt Controller (IC)</strong> สำหรับ P0/P1-TK/P1-ET เท่านั้น.</p>"
        "<p><strong>อ้างอิงจาก Industry:</strong></p>"
        "<ul>"
        '<li><a href="https://docs.broadsign.com/broadsign-control/latest/en/settings-section.html">'
        "Broadsign Day Part Switch</a>: configurable interrupt vs wait-for-completion — "
        "เรา map priority level เป็นตัวตัดสิน (P0/P1 = interrupt, P2-P4 = wait)</li>"
        '<li><a href="https://xibosignage.com/manual/en/layouts_interrupt">'
        "Xibo Interrupt Layout</a>: priority system + Share of Voice — "
        "เรา adopt priority concept แต่ใช้ timeline reservation แทน SOV %</li>"
        "</ul>"
    ))
    sections.append(mermaid_diagram(
        load_diagram("06-10-interrupt-controller.mmd"),
        page_id=page_id,
    ))
    sections.append(
        '<table>'
        '<tr><th>Trigger</th><th>Action</th><th>Resume</th></tr>'
        '<tr><td><strong>P0 Emergency</strong><br/>(Pusher: p0-emergency)</td>'
        '<td>หยุดทันที → เล่น emergency creative</td>'
        '<td>Resume item ถัดไปหลัง emergency จบ. เวลา TK ที่เสียไป log ไว้สำหรับ billing manual</td></tr>'
        '<tr><td><strong>P1-TK Start</strong><br/>(Pusher: takeover-start หรือ local clock)</td>'
        '<td>หยุด creative ปัจจุบัน → สลับไป TK creative → วน loop จนถึง TK_END</td>'
        '<td>TK_END → resume item ถัดไปใน schedule ปกติ + make-good สำหรับ ad ที่โดน interrupt</td></tr>'
        '<tr><td><strong>P1-ET Trigger</strong><br/>(local clock ±5s)</td>'
        '<td>หยุด P2-P4 ปัจจุบัน → เล่น ET spot (เล่นครั้งเดียว)</td>'
        '<td>ET เสร็จ → resume item ถัดไป + make-good สำหรับ ad ที่โดน interrupt</td></tr>'
        '</table>'
    )

    # Make-Good System
    sections.append("<h3>ระบบ Make-Good (ชดเชย Ad ที่โดน Interrupt)</h3>")
    sections.append(info_panel(
        "<p><strong>Make-Good</strong> คือ industry standard สำหรับชดเชย ad ที่โดน interrupt "
        '(<a href="https://www.cjadvertising.com/blog/industry-trends/preempts-makegoods-money-move/">'
        "CJ Advertising: Preempts, Make-Goods, and the Money Move</a>). "
        "Ad ที่เล่นไม่จบ (partial play) <strong>ไม่นับเป็น impression</strong> — "
        "ระบบจะชดเชยด้วย slot ฟรีใน cycle ถัดไป.</p>"
    ))
    sections.append(mermaid_diagram(
        load_diagram("06-11-make-good.mmd"),
        page_id=page_id,
    ))
    sections.append(
        '<table>'
        '<tr><th>Field</th><th>Description</th></tr>'
        '<tr><td><code>interrupted</code></td><td>boolean — PoP flag: ad ถูก interrupt กลางคัน</td></tr>'
        '<tr><td><code>play_duration_seconds</code></td><td>เวลาที่เล่นจริงก่อนถูก interrupt (เช่น 8s จาก 15s)</td></tr>'
        '<tr><td><code>interrupt_reason</code></td><td><code>P0_emergency</code> / <code>TK_start</code> / <code>TK_end</code> / <code>P1_exact_time</code></td></tr>'
        '<tr><td><code>make_good</code></td><td>boolean — PoP flag: ad นี้เป็น make-good compensation (เล่นซ้ำเพื่อชดเชย)</td></tr>'
        '<tr><td><code>compensated</code></td><td>MakeGoodRecord: ชดเชยแล้วหรือยัง</td></tr>'
        '<tr><td><code>compensated_at</code></td><td>เวลาที่ชดเชยสำเร็จ</td></tr>'
        '</table>'
    )

    return "\n".join(sections)


def build_page_7(page_id: str) -> str:
    """Page 7: Event-Driven Architecture (1 mermaid, 2 code blocks)."""
    global _code_block_count
    _code_block_count = 0
    sections = []

    sections.append(toc())
    sections.append("<h2>สถาปัตยกรรม Event-Driven</h2>")
    sections.append(info_panel(
        "<p><strong>การตัดสินใจ:</strong> ทำให้ event-driven patterns ที่มีอยู่ (Pusher + BullMQ) ชัดเจนขึ้นด้วย typed contracts, "
        "domain events, และ ownership ที่ชัดเจน. <strong>ไม่ใช่</strong> Event-Sourcing &mdash; scale + ทีมยังไม่จำเป็นต้อง complex ขนาดนั้น.</p>"
    ))

    sections.append("<h3>สิ่งที่มีอยู่แล้ว (De Facto Event-Driven)</h3>")

    sections.append(
        '<table>'
        '<tr><th>Component</th><th>Pattern</th><th>Status</th></tr>'
        '<tr><td>BullMQ cron &rarr; per-screen jobs</td><td>Job queue เป็น event bus</td><td>' + status_macro("EXISTS", "Green") + '</td></tr>'
        '<tr><td>Pusher events &rarr; Player</td><td>ส่ง event แบบ real-time</td><td>' + status_macro("EXISTS", "Green") + '</td></tr>'
        '<tr><td>PoP retry queue</td><td>คล้าย Outbox (player.history.json)</td><td>' + status_macro("EXISTS", "Green") + '</td></tr>'
        '<tr><td>Typed event contracts</td><td>Interface ชัดเจนต่อ event</td><td>' + status_macro("MISSING", "Red") + '</td></tr>'
        '<tr><td>Domain events ใน code</td><td>ตั้งชื่อ event เพื่อ traceability</td><td>' + status_macro("MISSING", "Red") + '</td></tr>'
        '<tr><td>Idempotency keys</td><td>ป้องกัน duplicate ตอน retry</td><td>' + status_macro("MISSING", "Red") + '</td></tr>'
        '<tr><td>Version protocol</td><td>เลข version เพิ่มขึ้นเรื่อยๆ ต่อ device</td><td>' + status_macro("MISSING", "Red") + '</td></tr>'
        '</table>'
    )

    sections.append("<h3>Typed Pusher Event Contracts</h3>")
    sections.append(note_panel(
        "<p><strong>เป้าหมาย:</strong> ทุก Pusher event มี TypeScript interface ที่ใช้ร่วมกันระหว่าง backend และ player. "
        "ไม่มี <code>any</code> types หรือ implicit contracts อีกต่อไป.</p>"
    ))

    sections.append(tracked_code_block(
        "// ─── Shared Event Types ───\n"
        "// File: packages/shared/events/pusher-events.ts\n"
        "// (or inline in both projects until monorepo)\n\n"
        "/** Base for all Pusher events */\n"
        "interface PusherEventBase {\n"
        "  event_id: string       // UUID, for inbox dedup\n"
        "  timestamp: string      // ISO 8601\n"
        "  device_code: string\n"
        "}\n\n"
        "// ─── Existing Events (formalized) ───\n\n"
        "interface UpdatePlayScheduleEvent extends PusherEventBase {\n"
        "  type: 'update-play-schedule'\n"
        "  version: number        // NEW: monotonic per-device\n"
        "  round_id: string\n"
        "  schedule_count: number\n"
        "}\n\n"
        "interface CreatedPlayScheduleEvent extends PusherEventBase {\n"
        "  type: 'created-play-schedule'\n"
        "  version: number\n"
        "  round_id: string\n"
        "  source: 'cron' | 'player-pull'\n"
        "}\n\n"
        "/** @deprecated Phase 1+ — absorbed into schedule-updated\n"
        " *  ADE pre-positions guaranteed spots in ordered sequence,\n"
        " *  so direct inject via this event is no longer needed.\n"
        " *  Kept during migration (Phase 0-3) for backward compat. */\n"
        "interface ApprovedExclusiveEvent extends PusherEventBase {\n"
        "  type: 'approved-advertisement-exclusive'\n"
        "  version: number\n"
        "  advertisement_code: string\n"
        "  play_at: string        // ISO 8601\n"
        "  duration_seconds: number\n"
        "  media_url: string\n"
        "  media_checksum: string\n"
        "}\n\n"
        "interface StopAdvertisementEvent extends PusherEventBase {\n"
        "  type: 'stop-advertisement'\n"
        "  version: number\n"
        "  advertisement_code: string\n"
        "  reason: 'cancelled' | 'budget_exhausted' | 'expired'\n"
        "}\n\n"
        "interface UnPairScreenEvent extends PusherEventBase {\n"
        "  type: 'un-pair-screen'\n"
        "  reason: 'admin' | 'replaced'\n"
        "}\n\n"
        "// ─── New Events (Proposed) ───\n\n"
        "interface ScheduleUpdatedEvent extends PusherEventBase {\n"
        "  type: 'schedule-updated'\n"
        "  version: number\n"
        "  tier: 'live' | 'buffer' | 'fallback'\n"
        "  item_count: number\n"
        "  valid_from: string\n"
        "  valid_until: string\n"
        "  /** Media codes that player should pre-download */\n"
        "  new_media_codes: string[]\n"
        "}\n\n"
        "interface DeviceConfigUpdatedEvent extends PusherEventBase {\n"
        "  type: 'device-config-updated'\n"
        "  changes: ('operating_hours' | 'player_mode' | 'fallback_playlist')[]\n"
        "}\n\n"
        "// ─── New Events: Interrupt/Takeover (v24) ───\n\n"
        "interface TakeoverStartEvent extends PusherEventBase {\n"
        "  type: 'takeover-start'\n"
        "  version: number\n"
        "  takeover_id: number\n"
        "  creative_code: string\n"
        "  end_time: string          // ISO 8601 — when TK ends\n"
        "}\n\n"
        "interface TakeoverEndEvent extends PusherEventBase {\n"
        "  type: 'takeover-end'\n"
        "  version: number\n"
        "  takeover_id: number\n"
        "}\n\n"
        "interface P0EmergencyEvent extends PusherEventBase {\n"
        "  type: 'p0-emergency'\n"
        "  version: number\n"
        "  message: string\n"
        "  creative_url: string\n"
        "  duration_seconds: number\n"
        "}\n\n"
        "// ─── Union Type ───\n"
        "type PusherEvent =\n"
        "  | UpdatePlayScheduleEvent\n"
        "  | CreatedPlayScheduleEvent\n"
        "  | ApprovedExclusiveEvent   // @deprecated — migration only\n"
        "  | StopAdvertisementEvent\n"
        "  | UnPairScreenEvent\n"
        "  | ScheduleUpdatedEvent\n"
        "  | DeviceConfigUpdatedEvent\n"
        "  | TakeoverStartEvent      // v24\n"
        "  | TakeoverEndEvent         // v24\n"
        "  | P0EmergencyEvent         // v24",
        "typescript", "Typed Pusher Event Contracts",
        collapse=True,
    ))

    sections.append("<h3>Domain Events (ระดับ Code ภายใน)</h3>")
    sections.append(note_panel(
        "<p><strong>เป้าหมาย:</strong> ตั้งชื่อ domain events ใน backend code เพื่อ traceability. "
        "ไม่ได้เก็บเป็น event-sourcing log &mdash; แค่ typed objects ที่ส่งระหว่าง services.</p>"
    ))

    sections.append(tracked_code_block(
        "// File: app/Events/PlaySchedule/PlayScheduleEvents.ts\n\n"
        "/** Emitted: PlayScheduleCalculatePerScreen completes */\n"
        "interface PlayScheduleCalculated {\n"
        "  type: 'PlayScheduleCalculated'\n"
        "  screen_code: string\n"
        "  round_id: string\n"
        "  schedule_codes: string[]\n"
        "  timestamp: DateTime\n"
        "}\n\n"
        "/** Emitted: AdDecisioningService completes */\n"
        "interface ScreenScheduleBuilt {\n"
        "  type: 'ScreenScheduleBuilt'\n"
        "  device_code: string\n"
        "  schedule_id: number\n"
        "  version: number\n"
        "  tier: 'live' | 'buffer' | 'fallback'\n"
        "  item_count: number\n"
        "  timestamp: DateTime\n"
        "}\n\n"
        "/** Emitted: Player confirms creative assets downloaded */\n"
        "interface CreativeDownloadConfirmed {\n"
        "  type: 'CreativeDownloadConfirmed'\n"
        "  device_code: string\n"
        "  creative_codes: string[]\n"
        "  total_bytes: number\n"
        "  timestamp: DateTime\n"
        "}\n\n"
        "/** Emitted: Player sends PoP (Proof of Play) batch */\n"
        "interface PoPReceived {\n"
        "  type: 'PoPReceived'\n"
        "  device_code: string\n"
        "  batch_size: number\n"
        "  idempotency_keys: string[]\n"
        "  new_entries: number  // after dedup\n"
        "  timestamp: DateTime\n"
        "}\n\n"
        "/** Emitted: Device reconnects after gap */\n"
        "interface DeviceResynced {\n"
        "  type: 'DeviceResynced'\n"
        "  device_code: string\n"
        "  from_version: number\n"
        "  to_version: number\n"
        "  sync_type: 'delta' | 'full'\n"
        "  gap_duration_seconds: number\n"
        "  timestamp: DateTime\n"
        "}\n\n"
        "// ─── New Domain Events (v24: Interrupt/Takeover) ───\n\n"
        "/** Emitted: Ad interrupted by P0/P1-TK/P1-ET */\n"
        "interface AdInterrupted {\n"
        "  type: 'AdInterrupted'\n"
        "  device_code: string\n"
        "  advertisement_code: string\n"
        "  play_duration_seconds: number\n"
        "  interrupt_reason: 'P0_emergency' | 'TK_start' | 'TK_end' | 'P1_exact_time'\n"
        "  timestamp: DateTime\n"
        "}\n\n"
        "/** Emitted: Make-good compensation scheduled for next cycle */\n"
        "interface MakeGoodScheduled {\n"
        "  type: 'MakeGoodScheduled'\n"
        "  device_code: string\n"
        "  advertisement_code: string\n"
        "  make_good_id: number\n"
        "  original_interrupt_reason: string\n"
        "  timestamp: DateTime\n"
        "}\n\n"
        "/** Emitted: Takeover block starts/ends */\n"
        "interface TakeoverStateChanged {\n"
        "  type: 'TakeoverStateChanged'\n"
        "  device_code: string\n"
        "  takeover_id: number\n"
        "  state: 'active' | 'completed'\n"
        "  timestamp: DateTime\n"
        "}",
        "typescript", "Domain Events",
        collapse=True,
    ))

    sections.append("<h3>แผนภาพ Event Flow</h3>")
    sections.append(mermaid_diagram(
        load_diagram("07-4-event-flow.mmd"),
        page_id=page_id,
    ))

    return "\n".join(sections)


def build_page_8(page_id: str) -> str:
    """Page 8: Edge Cases, Migration & Appendix (2 mermaid, 0 code blocks)."""
    global _code_block_count
    _code_block_count = 0
    sections = []

    sections.append(toc())
    sections.append("<h2>Edge Cases และความทนทาน (Resilience)</h2>")

    sections.append("<h3>ปัญหาเครือข่าย (Network Issues)</h3>")
    sections.append(expand_section("E1-E6: Network Edge Cases",
        '<table>'
        '<tr><th>#</th><th>Edge Case</th><th>สิ่งที่เกิดขึ้น</th><th>Solution</th></tr>'
        '<tr><td>E1</td><td><strong>Network flapping</strong> (on/off ทุก 30 วิ)</td>'
        '<td>Player fetch ค้าง, Pusher reconnect วนซ้ำ, media download incomplete</td>'
        '<td><strong>Debounce reconnect:</strong> ต้อง online ต่อเนื่อง 10 วิ ก่อน trigger sync. Media download ต้อง resume-able (Tauri download รองรับอยู่แล้ว)</td></tr>'
        '<tr><td>E2</td><td><strong>Pusher disconnect 5 นาที</strong> &rarr; missed events</td>'
        '<td>Player ไม่รู้ว่ามี playlist ใหม่</td>'
        '<td><strong>Version check on reconnect:</strong> Player เก็บ <code>last_version</code>. Reconnect &rarr; <code>GET /v2/screen-schedule?since_version=N</code> &rarr; ได้ delta</td></tr>'
        '<tr><td>E3</td><td><strong>Pusher duplicate events</strong></td>'
        '<td>Player process playlist update ซ้ำ 2 ครั้ง</td>'
        '<td><strong>Inbox dedup:</strong> เก็บ <code>event_id</code> ล่าสุด 100 รายการ. ถ้าซ้ำ &rarr; skip</td></tr>'
        '<tr><td>E4</td><td><strong>API timeout &rarr; player retry &rarr; duplicate play history</strong></td>'
        '<td>Backend บันทึก 2 records สำหรับ ad เดียวกัน</td>'
        '<td><strong>Outbox + Idempotency Key:</strong> Player สร้าง UUID per play event. Backend check Redis <code>idem:{uuid}</code> ก่อน insert</td></tr>'
        '<tr><td>E5</td><td><strong>Partial media download</strong> (internet หลุดกลาง download)</td>'
        '<td>ไฟล์ media ไม่สมบูรณ์</td>'
        '<td>เดิมมีอยู่แล้ว: <code>fileCleanupService.markDownloading()</code> ป้องกัน cleanup. เพิ่ม: <strong>checksum validation</strong> &mdash; backend ส่ง <code>media.checksum</code> &rarr; ตรวจสอบ + re-download ถ้าไม่ตรง</td></tr>'
        '<tr><td>E6</td><td><strong>SSL certificate expired / DNS failure</strong></td>'
        '<td>fetch fail แต่ internet ยังใช้ได้</td>'
        '<td>Treat เหมือน offline. Player มี Tier 2/3 รองรับ. เพิ่ม <strong>diagnostic log</strong> แยก SSL error จาก network error</td></tr>'
        '</table>'
    ))

    sections.append("<h3>ปัญหา Schedule/Playlist</h3>")
    sections.append(expand_section("E7-E13: Schedule/Playlist Edge Cases",
        '<table>'
        '<tr><th>#</th><th>Edge Case</th><th>สิ่งที่เกิดขึ้น</th><th>Solution</th></tr>'
        '<tr><td>E7</td><td><strong>Schedule gap</strong> &mdash; ไม่มี ad สำหรับช่วงเวลานี้</td>'
        '<td>Tier 1 ว่างเปล่า</td>'
        '<td>Auto-switch Tier 3 (owner fallback). <strong>ห้ามจอดำเด็ดขาด</strong></td></tr>'
        '<tr><td>E8</td><td><strong>Guaranteed spot ขณะ offline</strong></td>'
        '<td>Backend approve guaranteed แต่ push ไม่ถึง player</td>'
        '<td><strong>Buffer tier:</strong> Guaranteed ที่ approved ล่วงหน้า ถูกใส่ใน Tier 2 ด้วย <code>priority: guaranteed</code> + <code>play_at: exact_time</code>. Player check Tier 2 ทุก 1 วิ ว่ามี guaranteed <code>CalculatePlaySchedules</code> query ทำอยู่แล้ว)</td></tr>'
        '<tr><td>E9</td><td><strong>Tier 1 หมด แต่ Tier 2 ยังไม่พร้อม</strong> (media กำลัง download)</td>'
        '<td>ช่วงว่างระหว่าง tier</td>'
        '<td>Play Tier 3 ขณะรอ. เมื่อ Tier 2 media download ครบ &rarr; switch ขึ้นไป</td></tr>'
        '<tr><td>E10</td><td><strong>Screen time budget overflow</strong> &mdash; creatives มากกว่า avails</td>'
        '<td>Ad Decisioning Engine สร้าง schedule ยาวเกิน loop</td>'
        '<td>Backend cap ที่ <code>loopDuration</code>. ส่วนที่เกิน &rarr; ไม่ใส่ schedule (เหมือนเดิมที่ cron ทำ). Player ไม่ต้องคิด</td></tr>'
        '<tr><td>E11</td><td><strong>House content ว่าง</strong> &mdash; screen owner ไม่ได้ตั้งค่า</td>'
        '<td>Tier 3 ไม่มี content</td>'
        '<td><strong>First boot check:</strong> ถ้า Tier 3 ว่าง &rarr; แสดง <strong>system splash</strong> (logo + "กำลังเตรียมระบบ"). Admin UI แจ้งเตือน owner ให้ upload content. บังคับ: Device register สำเร็จต่อเมื่อ screen มีอย่างน้อย 1 house creative</td></tr>'
        '<tr><td>E12</td><td><strong>Stale schedule</strong> &mdash; offline นานจน Tier 2 expired</td>'
        '<td><code>valid_until</code> ผ่านไปแล้ว</td>'
        '<td>Player check <code>valid_until</code> ก่อนเล่น. ถ้า expired &rarr; switch Tier 3. <strong>ไม่เล่น ad expired</strong> เพราะอาจเป็น campaign ที่หมดแล้ว (billing issue)</td></tr>'
        '<tr><td>E13</td><td><strong>Concurrent Pusher events</strong> &mdash; 3 events มาพร้อมกัน</td>'
        '<td>Race condition ใน playlist update</td>'
        '<td><strong>Version monotonic:</strong> Player เก็บ <code>current_version</code>. ถ้า <code>event.version</code> &le; current &rarr; skip. ถ้า &gt; current &rarr; process. ถ้า &gt; current+1 (gap) &rarr; full re-fetch</td></tr>'
        '</table>'
    ))

    sections.append("<h3>ปัญหา Device/Storage</h3>")
    sections.append(expand_section("E14-E19: Device/Storage Edge Cases",
        '<table>'
        '<tr><th>#</th><th>Edge Case</th><th>สิ่งที่เกิดขึ้น</th><th>Solution</th></tr>'
        '<tr><td>E14</td><td><strong>Player restart ขณะ offline</strong></td>'
        '<td>App crash &rarr; relaunch ไม่มี internet</td>'
        '<td>localStorage persist ข้าม restart (เดิมทำอยู่แล้ว). Boot &rarr; read localStorage &rarr; resume from last <code>sequence_no</code>. ถ้า Tier 1/2 expired &rarr; Tier 3</td></tr>'
        '<tr><td>E15</td><td><strong>First boot ไม่มี internet</strong></td>'
        '<td>Device ใหม่ ยังไม่เคย pair</td>'
        '<td>ไม่สามารถ pair ได้ (ต้องมี internet สำหรับ register). แสดง splash + "กรุณาเชื่อมต่อ internet". Poll ทุก 5 วิ (เดิม)</td></tr>'
        '<tr><td>E16</td><td><strong>Clock drift</strong> &mdash; offline นาน, NTP ไม่ sync</td>'
        '<td><code>valid_until</code> check ผิดพลาด</td>'
        '<td>Tauri บน Windows/macOS/Linux มี RTC ที่แม่นยำกว่า RPi. เก็บ <code>last_ntp_sync</code> timestamp. ถ้า drift &gt; 1 ชม. &rarr; log warning แต่ยังเล่นต่อ (เล่นผิดเวลาดีกว่าจอดำ)</td></tr>'
        '<tr><td>E17</td><td><strong>Disk full</strong> &mdash; media เต็ม storage</td>'
        '<td>Download ใหม่ไม่ได้</td>'
        '<td>เดิมมี cleanup อยู่แล้ว (file-cleanup.service.ts ทุก 24h). เพิ่ม: check disk ก่อน download. ถ้า &lt; 500MB &rarr; trigger emergency cleanup (ลบ media ที่ไม่อยู่ใน Tier 1+2+3). ถ้ายังไม่พอ &rarr; skip download, เล่น ad ถัดไป (ไม่หยุด)</td></tr>'
        '<tr><td>E18</td><td><strong>Media file corrupt</strong></td>'
        '<td>Video file เสีย &rarr; playback error</td>'
        '<td>เดิมมี <strong>retry queue</strong> (max 3 attempts). เพิ่ม: ถ้า retry ครบ 3 ครั้ง &rarr; mark file dirty &rarr; re-download next sync. Player skip ไป ad ถัดไป (ไม่หยุด)</td></tr>'
        '<tr><td>E19</td><td><strong>localStorage quota exceeded</strong> (5-10MB limit)</td>'
        '<td>เก็บ playlist data ไม่พอ</td>'
        '<td>Migrate heavy data &rarr; <strong>Tauri Store</strong> (JSON file, ไม่มี quota). เก็บเฉพาะ small state ใน localStorage. Playlist data &rarr; Tauri Store</td></tr>'
        '</table>'
    ))

    sections.append("<h3>ปัญหา Business Logic</h3>")
    sections.append(expand_section("E20-E24: Business Logic Edge Cases",
        '<table>'
        '<tr><th>#</th><th>Edge Case</th><th>สิ่งที่เกิดขึ้น</th><th>Solution</th></tr>'
        '<tr><td>E20</td><td><strong>Ad cancelled ขณะ offline</strong></td>'
        '<td>Backend cancel ad แต่ player ยังเล่นอยู่</td>'
        '<td><strong>Acceptable tradeoff:</strong> player จะเล่น creative ต่อจน reconnect. เมื่อ reconnect &rarr; sync schedule ใหม่ &rarr; creative หายไป. PoP records ยังถูกต้อง (ส่งทีหลัง reconnect)</td></tr>'
        '<tr><td>E21</td><td><strong>Campaign budget exhausted ขณะเล่น</strong></td>'
        '<td>Player กำลังเล่น ad ของ campaign ที่หมด budget</td>'
        '<td>Backend ไม่ใส่ ad นี้ใน round ถัดไป. Player round ปัจจุบันเล่นจบปกติ (ยอมรับได้ &mdash; เป็น 1 round = 10 นาที max)</td></tr>'
        '<tr><td>E22</td><td><strong>PoP ส่งไม่ได้</strong> &rarr; billing คลาดเคลื่อน</td>'
        '<td>Offline นาน &rarr; PoP outbox queue สะสม</td>'
        '<td><strong>Outbox guarantee:</strong> ไม่มี PoP event หาย (persisted ใน Tauri Store). เมื่อ reconnect &rarr; flush ทั้งหมดตามลำดับ. Backend reconcile by timestamp</td></tr>'
        '<tr><td>E23</td><td><strong>Billboard unpair ขณะ offline</strong></td>'
        '<td>Admin unpair device แต่ player ไม่รู้</td>'
        '<td>Player ยังเล่นต่อจาก cache. เมื่อ reconnect &rarr; Pusher <code>un-pair-screen</code> &rarr; clear all + back to pair screen. หรือ: API call fail &rarr; 401 &rarr; trigger unpair locally</td></tr>'
        '<tr><td>E24</td><td><strong>Multiple devices ใช้ device code เดียวกัน</strong></td>'
        '<td>Clone device &rarr; 2 players same code</td>'
        '<td>Backend: POST <code>/v2/play-history</code> ส่ง <code>device_fingerprint</code> (MAC + hostname). ถ้าไม่ตรง &rarr; reject + alert</td></tr>'
        '</table>'
    ))

    sections.append("<h3>Edge Cases ของ Guaranteed Spot (P1-G — ไม่ Interrupt)</h3>")
    sections.append(warning_panel(
        "<p><strong>Edge cases เฉพาะ P1-G guaranteed spots</strong> (เดิมเรียก exclusive). "
        "P1-G ยังคง <strong>ไม่ interrupt</strong> — pre-positioned ใน sequence โดย Ad Decisioning Engine. "
        "สำหรับ edge cases ของ P1-TK (Takeover) และ P1-ET (Exact-Time) ที่มี interrupt ดู §8.6</p>"
    ))
    sections.append(expand_section("EX1-EX7: Guaranteed Spot Edge Cases",
        '<table>'
        '<tr><th>#</th><th>Edge Case</th><th>สิ่งที่เกิดขึ้น (ปัจจุบัน)</th><th>Proposed Solution</th></tr>'
        '<tr><td>EX1</td><td><strong>Overlapping guaranteed spots</strong> &mdash; 2 guaranteed spots ที่เวลาทับกัน</td>'
        '<td>ปัจจุบัน: <code>find()</code> picks first match, ไม่มี priority logic ระหว่าง guaranteed spots</td>'
        '<td><strong>Priority queue:</strong> Guaranteed ที่ <code>play_at</code> ตรงกัน &rarr; sort by <code>created_at</code> (FIFO). '
        'Ad Decisioning Engine ตรวจ overlap ตอน build &rarr; reject ตัวหลังที่ทับ (SMIL <code>peers=&quot;stop&quot;</code> semantic). '
        'Admin UI: แสดง warning ก่อน approve ถ้าช่วงเวลาซ้อน</td></tr>'
        '<tr><td>EX2</td><td><strong>Guaranteed creative asset missing/corrupt</strong></td>'
        '<td>ปัจจุบัน: <strong>silent failure</strong> &mdash; interrupted creative stays paused, ไม่มี recovery</td>'
        '<td><strong>Creative validation at booking:</strong> Ad Decisioning Engine checks creative existence + checksum ตอน build. '
        'ถ้า creative ไม่พร้อม &rarr; mark <code>status=PENDING_CREATIVE</code>, alert admin. '
        'Player-side: ถ้า creative download fail &rarr; skip guaranteed, resume normal sequence (ไม่ pause ค้าง)</td></tr>'
        '<tr><td>EX3</td><td><strong>Guaranteed spot approved while player offline</strong></td>'
        '<td>ปัจจุบัน: Pusher push lost, no buffer mechanism &rarr; guaranteed spot ไม่เล่น</td>'
        '<td><strong>Tier 2 pre-staging:</strong> Guaranteed ที่ approved ล่วงหน้า &rarr; ใส่ใน Tier 2 (buffer) ด้วย <code>play_at</code> exact time. '
        'Player check Tier 2 locally ทุก sync cycle. Reconnect &rarr; version-based full sync จะ include guaranteed</td></tr>'
        '<tr><td>EX4</td><td><strong>Guaranteed spot cancelled after schedule built</strong></td>'
        '<td>ปัจจุบัน: ไม่มี cancel mechanism สำหรับ guaranteed ที่ถูก push ไปแล้ว</td>'
        '<td><strong>Cancel event:</strong> Backend push <code>guaranteed-cancelled {ad_code, version++}</code>. '
        'Player receives &rarr; remove from Tier 1/2 + version bump. ถ้า offline &rarr; ยอมรับ tradeoff (เล่นจบแล้ว cancel ตอน sync)</td></tr>'
        '<tr><td>EX5</td><td><strong>Clock drift + guaranteed timing</strong> &mdash; player clock off by &gt;5s</td>'
        '<td>ปัจจุบัน: <code>dayjs().isBetween(start, end)</code> ±2s precision &mdash; clock drift ทำให้ miss window</td>'
        '<td><strong>Server-relative timing:</strong> Guaranteed <code>play_at</code> stored as <code>sequence_no</code> position (not wall-clock). '
        'Player plays by sequence order, ไม่ต้องพึ่ง local clock. '
        'Fallback: NTP sync on reconnect, <code>last_ntp_offset</code> adjustment</td></tr>'
        '<tr><td>EX6</td><td><strong>Nested guaranteed interrupts</strong></td>'
        '<td>ปัจจุบัน: <code>pausePlayData</code> is <strong>single variable</strong> &mdash; nested interrupt loses original paused creative</td>'
        '<td><strong>Eliminated by design:</strong> Ad Decisioning Engine resolves all guaranteed positions at build time. '
        'Player sees flat sequence &mdash; guaranteed spot is just another item at the right position. '
        'No interrupt/pause mechanism needed (SMIL <code>pauseQueue</code> approach unnecessary)</td></tr>'
        '<tr><td>EX7</td><td><strong>Guaranteed spans loop boundary</strong> &mdash; 30s guaranteed at minute 9:50 of 10-min loop</td>'
        '<td>ปัจจุบัน: loop boundary cuts off guaranteed mid-play</td>'
        '<td><strong>Loop extension:</strong> Ad Decisioning Engine extends loop duration to fit guaranteed completely. '
        'Or: guaranteed <code>play_at</code> adjusted to start earlier so it fits within loop. '
        'Config: <code>guaranteed_loop_policy: &quot;extend&quot; | &quot;shift_earlier&quot;</code></td></tr>'
        '</table>'
    ))

    sections.append("<h4>Edge Cases ของ Flow ผสม (Regular + Exclusive)</h4>")
    sections.append(expand_section("CF1-CF5: Combined Flow Edge Cases",
        '<table>'
        '<tr><th>#</th><th>Edge Case</th><th>สิ่งที่เกิดขึ้น</th><th>Solution</th></tr>'
        '<tr><td>CF1</td><td><strong>Guaranteed during Tier 2/3 fallback</strong></td>'
        '<td>Player offline, playing house content &rarr; guaranteed <code>play_at</code> time arrives</td>'
        '<td>Tier 2 pre-staged guaranteed: Player checks Tier 2 locally. ถ้า guaranteed อยู่ใน Tier 2 + creative cached &rarr; play at position. '
        'ถ้าไม่มี (approved after last sync) &rarr; miss (acceptable &mdash; offline = degraded mode)</td></tr>'
        '<tr><td>CF2</td><td><strong>Budget exhausted mid-guaranteed</strong></td>'
        '<td>Guaranteed spot ราคาสูง, campaign budget หมดขณะ guaranteed ยังไม่ถึงเวลา</td>'
        '<td>Guaranteed = <strong>pre-paid delivery commitment</strong>. Budget check at booking time, not play time. '
        'ถ้า budget deplete after booking &rarr; ยังเล่นตาม contract (billing reconcile separately)</td></tr>'
        '<tr><td>CF3</td><td><strong>Multiple guaranteed + campaign creatives &rarr; time overflow</strong></td>'
        '<td>Guaranteed avails กิน time budget เกือบหมด &rarr; campaign creatives ไม่มีที่เล่น</td>'
        '<td>Ad Decisioning Engine: reserve guaranteed FIRST &rarr; remaining time for campaigns. '
        'ถ้า remaining &lt; min_avail_duration &rarr; skip lowest-priority campaigns. '
        'Admin UI: show time utilization preview before approve</td></tr>'
        '<tr><td>CF4</td><td><strong>Hot-swap guaranteed</strong> &mdash; owner cancels guaranteed A, immediately books guaranteed B at same avail</td>'
        '<td>Race condition: cancel event + new booking event may arrive out of order</td>'
        '<td><strong>Version monotonic:</strong> Both cancel and new booking increment version. '
        'Player applies in version order. Ad Decisioning Engine atomic: cancel A + insert B in single build cycle</td></tr>'
        '<tr><td>CF5</td><td><strong>Guaranteed + house content conflict</strong> &mdash; guaranteed books time where only house content was playing</td>'
        '<td>House loop interrupted by guaranteed</td>'
        '<td><strong>Priority model:</strong> P1 (Guaranteed) &gt; P4 (House). Ad Decisioning Engine replaces house avail with guaranteed. '
        'House content resumes after guaranteed completes (next sequence item)</td></tr>'
        '</table>'
    ))

    sections.append("<h3>Edge Cases ของ Takeover และ Exact-Time (P1-TK / P1-ET)</h3>")
    sections.append(mermaid_diagram(
        load_diagram("08-2-takeover-timeline.mmd"),
        page_id=page_id,
    ))
    sections.append("<h4>Timeline การ Interrupt ของ Takeover (Gantt View)</h4>")
    sections.append(info_panel(
        "<p>มุมมองเวลาจริง — เห็นสัดส่วนว่า <strong>TK block 60 นาที</strong> กว้างกว่า normal schedule มาก. "
        "<strong>Milestone</strong> = TK_START / TK_END boundary. "
        "<strong>Make-good</strong> (ฟ้า) เล่นชดเชย Ad A ที่โดน interrupt ทันทีหลัง TK จบ</p>"
    ))
    sections.append(mermaid_diagram(
        load_diagram("08-3-takeover-gantt.mmd"),
        page_id=page_id,
    ))
    sections.append(expand_section("TK1-TK8: Takeover & Exact-Time Edge Cases",
        '<table>'
        '<tr><th>#</th><th>Edge Case</th><th>Solution</th></tr>'
        '<tr><td>TK1</td><td><strong>TK booking ทับกัน</strong> &mdash; 2 เจ้าของจองช่วงเวลาเดียวกัน</td>'
        '<td>Reject ตอนจอง — <code>checkIsBillboardsReserved</code> ขยายรองรับ TK. 1 time block = 1 เจ้าของเท่านั้น</td></tr>'
        '<tr><td>TK2</td><td><strong>TK creative ยังไม่ cache ตอน TK_START</strong></td>'
        '<td>ข้าม TK → resume schedule ปกติ → แจ้ง admin. Pre-stage creative ผ่าน <code>device-config-updated</code> event ตอนจอง</td></tr>'
        '<tr><td>TK3</td><td><strong>P0 Emergency ระหว่าง TK</strong></td>'
        '<td>P0 ชนะเสมอ (priority สูงสุด). เวลา TK ที่เสียไป — log สำหรับ billing reconcile manual</td></tr>'
        '<tr><td>TK4</td><td><strong>Player offline ตอน TK_START</strong></td>'
        '<td>ใช้ local clock: TK schedule อยู่ใน Tier 2 พร้อม <code>takeover_id</code>. IC เช็ค local clock กับ TK boundary ที่รอ</td></tr>'
        '<tr><td>TK5</td><td><strong>จอง TK กระชั้นเกินไป (lead time ไม่พอ)</strong></td>'
        '<td>Reject — ใช้ lead time เดียวกับ guaranteed spots (exclusive validation เดิม)</td></tr>'
        '<tr><td>TK6</td><td><strong>TK creative เปลี่ยนหลังจอง</strong></td>'
        '<td>Push <code>device-config-updated</code> ใหม่พร้อม <code>creative_code</code> ใหม่. Player download ก่อน TK_START</td></tr>'
        '<tr><td>TK7</td><td><strong>หลาย ET spots ในวินาทีเดียวกัน</strong></td>'
        '<td>FIFO ตาม <code>created_at</code> — ตัวแรกได้เล่น, ตัวถัดไปขยับ <code>+duration</code> (เรียงต่อกัน ไม่พร้อมกัน)</td></tr>'
        '<tr><td>TK8</td><td><strong>Make-good creative หมดอายุ</strong></td>'
        '<td>ข้ามการชดเชย — log สำหรับ reconcile manual. ตรวจ <code>valid_until</code> ป้องกันเล่น ad ที่หมดอายุ</td></tr>'
        '</table>'
    ))

    sections.append("<hr/>")
    sections.append("<h2>แผนการ Migration (ทำทีละ Phase)</h2>")
    sections.append(info_panel(
        "<p><strong>Feature flags:</strong></p>"
        "<ul>"
        "<li><code>billboard.player_mode: 'smart' | 'dumb'</code> &mdash; roll out Dumb Renderer per billboard, no big bang</li>"
        "<li><code>billboard.interrupt_capable: boolean</code> &mdash; Phase 3.5: enable Interrupt Controller (แยกจาก player_mode)</li>"
        "</ul>"
    ))
    sections.append(
        '<table>'
        '<tr><th>Phase</th><th>Backend</th><th>Player</th><th>Risk</th></tr>'
        '<tr><td><strong>Phase 0</strong></td><td>Add <code>version</code> field to Pusher payload</td><td>Store version (don\'t use yet)</td><td>' + status_macro("Zero risk", "Green") + '</td></tr>'
        '<tr><td><strong>Phase 1</strong></td><td>Add Ad Decisioning Engine + ScreenSchedule models + <code>GET /v2/screen-schedule</code></td><td>Read-only testing (no behavior change)</td><td>' + status_macro("Backend only", "Green") + '</td></tr>'
        '<tr><td><strong>Phase 2</strong></td><td>Add Idempotency Key check in PoP endpoint</td><td>Send <code>X-Idempotency-Key</code> header</td><td>' + status_macro("Backward compat", "Green") + '</td></tr>'
        '<tr><td><strong>Phase 3</strong></td><td>&mdash;</td><td>Player V2: read ordered screen schedule. <strong>Feature flag per device</strong></td><td>' + status_macro("Gradual rollout", "Yellow") + '</td></tr>'
        '<tr><td><strong>Phase 3.5</strong></td>'
        '<td>TakeoverSchedule + ExactTimeSpot models, TK Booking API + overlap validation, '
        'Pusher: takeover-start/end + p0-emergency, MakeGoodRecord + PoP interrupt fields, '
        'Ad Decisioning v3 (Step 0 + 1.5 + 5.5)</td>'
        '<td>Interrupt Controller component, local clock TK boundary detection, '
        'PoP: interrupted + play_duration + make_good</td>'
        '<td>' + status_macro("Medium risk", "Yellow") + '</td></tr>'
        '<tr><td><strong>Phase 4</strong></td><td>&mdash;</td><td>3-Tier cache + state machine + checksum validation</td><td>' + status_macro("Full new behavior", "Yellow") + '</td></tr>'
        '<tr><td><strong>Phase 5</strong></td><td>Remove old schedule endpoints (v1)</td><td>Remove old scheduling code</td><td>' + status_macro("Cleanup", "Grey") + '</td></tr>'
        '<tr><td><strong>Phase 6</strong></td><td>SSP integration: ad request for P3 avails, impression tracking (IAB fields), <code>GET /v2/avails</code> API</td><td>No change (backend-only pDOOH)</td><td>' + status_macro("Backend only", "Yellow") + '</td></tr>'
        '<tr><td><strong>Phase 7</strong></td><td>Mediation layer: multi-SSP, floor price, preferred deals</td><td>PoP format upgrade (IAB DOOH standard)</td><td>' + status_macro("Revenue impact", "Red") + '</td></tr>'
        '</table>'
    )

    sections.append("<hr/>")
    sections.append("<h2>ภาคผนวก (Appendix)</h2>")

    sections.append("<h3>อ้างอิงจาก Industry</h3>")

    sections.append("<h4>มาตรฐาน Priority Scheduling (SMIL + DOOH)</h4>")
    sections.append(expand_section("SMIL, Xibo, Broadsign, DOOH Billing — มาตรฐาน Priority",
        info_panel(
            "<p><strong>Priority model 5 ระดับ (P0-P4)</strong> ที่เราเสนอ ได้แรงบันดาลใจจากมาตรฐาน industry เหล่านี้. "
            "หลักการสำคัญ: exclusive/priority scheduling เป็น <em>โจทย์ที่วงการ digital signage แก้ไปแล้ว</em> &mdash; "
            "เรา adapt pattern ที่พิสูจน์แล้วแทนที่จะคิดใหม่ตั้งแต่ต้น.</p>"
        ) +
        '<table>'
        '<tr><th>Standard/Platform</th><th>Priority Mechanism</th><th>What We Adopt</th></tr>'
        '<tr><td><strong>W3C SMIL 3.0</strong><br/><code>&lt;excl&gt;</code> + <code>&lt;priorityClass&gt;</code></td>'
        '<td><ul>'
        '<li><code>&lt;excl&gt;</code>: only one child plays at a time (mutual exclusion)</li>'
        '<li><code>&lt;priorityClass&gt;</code>: assigns priority levels with <code>peers</code> + <code>higher</code> + <code>lower</code> policies</li>'
        '<li>Policies: <code>stop</code> (kill lower), <code>pause</code> (pause queue/stack), <code>defer</code> (queue for later), <code>never</code> (reject)</li>'
        '<li>Pause queue: nested interrupts push onto stack &rarr; resume in LIFO order</li>'
        '</ul></td>'
        '<td><ul>'
        '<li><strong>P0-P4 levels</strong> = simplified priorityClass</li>'
        '<li><strong>Exclusive = P1</strong> with guaranteed slot reservation</li>'
        '<li>No pause queue needed &mdash; Ad Decisioning Engine resolves at build time (player sees flat sequence)</li>'
        '<li>SMIL <code>peers=&quot;stop&quot;</code> semantic for overlapping exclusives</li>'
        '</ul></td></tr>'
        '<tr><td><strong>Xibo CMS</strong><br/>Interrupt Layout + Priority</td>'
        '<td><ul>'
        '<li>Priority number (0 = lowest) per scheduled event</li>'
        '<li>Interrupt Layout: higher priority event preempts current layout</li>'
        '<li>Share of Voice: percentage-based time allocation</li>'
        '<li>Schedule reassessment on criteria change (geo-fence, daypart, priority)</li>'
        '</ul></td>'
        '<td><ul>'
        '<li><strong>Priority number</strong> concept &rarr; our P0-P4 model</li>'
        '<li><strong>Time allocation</strong> &rarr; Ad Decisioning Engine timeline reservation</li>'
        '<li>Share of Voice concept applicable for future frequency-based billing</li>'
        '</ul></td></tr>'
        '<tr><td><strong>Broadsign Control</strong><br/>'
        '<a href="https://docs.broadsign.com/broadsign-control/latest/en/settings-section.html">Day Part Switch (verified)</a></td>'
        '<td><ul>'
        '<li><strong>Configurable interrupt:</strong> Day Part Switch can interrupt mid-play or wait for completion</li>'
        '<li>Trigger system: serial/network/XML/touch triggers interrupt current content</li>'
        '<li>Default: interrupted content restarts after trigger (<code>--truncate_current</code> to skip)</li>'
        '<li>Revenue-based priority: guaranteed &gt; programmatic</li>'
        '</ul></td>'
        '<td><ul>'
        '<li><strong>Configurable interrupt → our P0/P1 interrupt vs P2-P4 wait</strong></li>'
        '<li>Day Part Switch → P1-TK Takeover boundary handling</li>'
        '<li>Restart after interrupt → we chose "resume next" (skip interrupted) + make-good</li>'
        '</ul></td></tr>'
        '<tr><td><strong>DOOH Billing Models</strong><br/>'
        '<a href="https://www.themediaant.com/blog/understanding-dooh-pricing-models/">The Media Ant (verified)</a> + '
        '<a href="https://www.cjadvertising.com/blog/industry-trends/preempts-makegoods-money-move/">CJ Advertising (verified)</a></td>'
        '<td><ul>'
        '<li><strong>CPT (Cost Per Time):</strong> flat rate for time block ownership</li>'
        '<li><strong>Make-Good:</strong> free replacement slot for preempted ads — industry standard</li>'
        '<li>CPM, Flat per spot, SOV-based pricing models</li>'
        '</ul></td>'
        '<td><ul>'
        '<li><strong>CPT → P1-TK Takeover billing</strong></li>'
        '<li><strong>Make-Good → MakeGoodRecord compensation system</strong></li>'
        '<li>Partial play ≠ impression (ไม่นับ billing)</li>'
        '</ul></td></tr>'
        '</table>'
    ))

    sections.append("<h4>สถาปัตยกรรมเรา vs มาตรฐาน DOOH</h4>")
    sections.append(expand_section("เปรียบเทียบกับมาตรฐาน DOOH (14 concepts)",
        '<table>'
        '<tr><th>DOOH Concept</th><th>Our Implementation</th><th>Gap</th></tr>'
        '<tr><td><strong>Ad Server</strong></td><td>Ad Decisioning Engine อยู่ใน Backend (AdonisJS)</td><td>ไม่แยก — OK สำหรับ 100-500 จอ</td></tr>'
        '<tr><td><strong>CMS</strong></td><td>Admin panel + owner dashboard</td><td>มาตรฐาน</td></tr>'
        '<tr><td><strong>SSP (Supply-Side Platform)</strong></td><td>ยังไม่มี — P3 = SSP avail ในอนาคต</td><td>Phase 6 roadmap</td></tr>'
        '<tr><td><strong>Impression tracking</strong></td><td>PoP ผ่าน Outbox pattern</td><td>เพิ่ม IAB fields (Phase 6)</td></tr>'
        '<tr><td><strong>Campaign pacing</strong></td><td>BEP-2998 fix + Ad Decisioning Engine</td><td>พื้นฐาน — ปรับปรุงใน Phase 6</td></tr>'
        '<tr><td><strong>SOV allocation</strong></td><td>สัดส่วน ownerTime/platformTime</td><td>เปลี่ยนชื่อเป็น SOV, logic เดิม</td></tr>'
        '<tr><td><strong>Guaranteed delivery</strong></td><td>P1-G guaranteed spots พร้อม reservation check (ไม่ interrupt)</td><td>มาตรฐาน</td></tr>'
        '<tr><td><strong>Daypart Takeover</strong></td><td>P1-TK จอง time block + Interrupt Controller</td><td>Implement แล้ว (Phase 3.5)</td></tr>'
        '<tr><td><strong>Exact-Time Spot</strong></td><td>P1-ET ±5s tolerance + IC trigger</td><td>Implement แล้ว (Phase 3.5)</td></tr>'
        '<tr><td><strong>Make-Good</strong></td><td>MakeGoodRecord: โดน interrupt → ชดเชย cycle ถัดไป</td><td>Implement แล้ว (Phase 3.5)</td></tr>'
        '<tr><td><strong>Interrupt handling</strong></td><td>เลือก interrupt: P0/P1-TK/P1-ET interrupt, P2-P4 รอ</td><td>มาตรฐาน (แบบ Broadsign configurable)</td></tr>'
        '<tr><td><strong>Creative management</strong></td><td>Upload media + CDN + checksum validation</td><td>มาตรฐาน</td></tr>'
        '<tr><td><strong>Offline resilience</strong></td><td>Cache 3 ชั้น (Live/Buffer/Fallback)</td><td>มาตรฐาน (เทียบเท่า Xibo/BrightSign)</td></tr>'
        '<tr><td><strong>Loop scheduling</strong></td><td>Loop 10 นาที ผ่าน Scheduling Engine (BullMQ)</td><td>มาตรฐาน</td></tr>'
        '</table>'
    ))

    sections.append("<h4>วิธีจัดการ Offline ของ Platform ชั้นนำ</h4>")
    sections.append(expand_section("Xibo, piSignage, BrightSign, info-beamer — แนวทาง Offline",
        '<table>'
        '<tr><th>Platform</th><th>Approach</th><th>Buffer</th></tr>'
        '<tr><td>Xibo</td><td>RequiredFiles manifest + MD5 per file + 50MB chunk download</td><td>48h ahead (configurable)</td></tr>'
        '<tr><td>piSignage</td><td>Default playlist fallback + local media folder + delta sync</td><td>Full campaign window</td></tr>'
        '<tr><td>BrightSign BSN.Cloud</td><td>Local-first: all media cached, network = sync only</td><td>Content-dependent</td></tr>'
        '<tr><td>info-beamer</td><td>3-state degradation (Online/Degraded/Offline) + RTC fallback</td><td>All scheduled content</td></tr>'
        '</table>'
    ))

    sections.append("<h4>อ้างอิง Open Source</h4>")
    sections.append(expand_section("Xibo, piSignage, Anthias — อ้างอิง Open Source",
        '<table>'
        '<tr><th>Project</th><th>Repository</th><th>Relevant Pattern</th></tr>'
        '<tr><td>Xibo Player SDK</td><td><a href="https://github.com/xibo-players/xiboplayer">xibo-players/xiboplayer</a></td><td>Cache API + IndexedDB, XMR WebSocket, chunk downloads with MD5, 2-layout preload pool</td></tr>'
        '<tr><td>Xibo .NET Client</td><td><a href="https://github.com/xibosignage/xibo-dotnetclient">xibosignage/xibo-dotnetclient</a></td><td>ScheduleManager.cs: thread polling, priority resolution, disk-resident schedule, Splash fallback</td></tr>'
        '<tr><td>piSignage</td><td><a href="https://github.com/colloqi/piSignage">colloqi/piSignage</a></td><td>Node.js + WebSocket, default playlist fallback, local filesystem media</td></tr>'
        '<tr><td>Anthias (Screenly OSE)</td><td><a href="https://github.com/Screenly/Anthias">Screenly/Anthias</a></td><td>Docker microservices, Redis + SQLite, Celery queue, Qt viewer</td></tr>'
        '</table>'
    ))

    sections.append("<h4>คำแนะนำเรื่อง Protocol</h4>")
    sections.append(note_panel(
        "<p><strong>ใช้ Pusher ต่อ</strong> (มีอยู่แล้ว) สำหรับ real-time push. เพิ่ม <strong>version-based checkpoint</strong> ตอน reconnect ผ่าน REST. "
        "อย่าพึ่ง push สำหรับ playback &mdash; push แค่ trigger sync ให้เร็วขึ้น.</p>"
        "<p><strong>หลักการสำคัญ (จาก RxDB):</strong> Client อาจพลาด event ตอน disconnect. "
        "วิธีแก้: checkpoint mode ตอน reconnect (เทียบ schedule ทั้งหมดผ่าน REST) + event mode หลัง sync แล้ว (Pusher สำหรับ incremental).</p>"
    ))

    # ─── Terminology Mapping (Old System ↔ DOOH Industry) ───
    sections.append("<h3>ตาราง Mapping คำศัพท์: Tathep &harr; DOOH Industry</h3>")

    # Build all terminology content, then wrap in a single Expand
    _term_content = (
        info_panel(
            "<p>ตารางด้านล่างเชื่อมโยง<strong>คำศัพท์เดิมในระบบ</strong> (codebase + Jira) กับ<strong>คำใหม่</strong> "
            "ที่ใช้ใน architecture proposal นี้ ซึ่ง align กับมาตรฐาน DOOH industry<br/>"
            "เพื่อให้คนที่ทำระบบเดิมอยู่ กับคนที่จะทำ version ใหม่ เข้าใจตรงกัน</p>"
        )
    )

    _term_content += "<h4>Core Concepts</h4>"
    _term_content += (
        '<table>'
        '<tr><th>หมวด</th><th>คำเดิม (Current System)</th><th>คำใหม่ (DOOH Standard)</th><th>หมายเหตุ</th></tr>'
        '<tr><td rowspan="3"><strong>Ad Types</strong></td>'
        '<td><code>exclusive</code></td><td><strong>Guaranteed Spot (P1-G)</strong></td>'
        '<td>ชื่อใน code: <code>schedule.constant.ts</code> ยังเป็น <code>exclusive</code></td></tr>'
        '<tr><td><code>continuous</code> (date-range)</td><td><strong>Direct-Sold ROS (P2)</strong></td>'
        '<td>Run-of-Schedule &mdash; campaign ที่ขายตรง</td></tr>'
        '<tr><td><code>frequency</code> (count-based)</td><td><strong>Spot Buy (P3)</strong></td>'
        '<td>อนาคต: Programmatic via SSP/RTB</td></tr>'
        '<tr><td rowspan="2"><strong>Content</strong></td>'
        '<td>owner ads / owner playlist</td><td><strong>House Content (P4)</strong></td>'
        '<td>เจ้าของจอเลือกเอง เล่นตอนว่าง</td></tr>'
        '<tr><td>ads / media</td><td><strong>Creative (asset)</strong></td>'
        '<td><code>media_code</code> &rarr; <code>creative_code</code></td></tr>'
        '<tr><td rowspan="2"><strong>Screen</strong></td>'
        '<td>billboard</td><td><strong>Screen</strong></td>'
        '<td>DOOH standard &mdash; model ยังชื่อ <code>Billboard.ts</code></td></tr>'
        '<tr><td><code>ownerTime</code> / <code>platformTime</code></td><td><strong>SOV (Share of Voice)</strong></td>'
        '<td>สัดส่วนเวลา owner vs platform &mdash; logic เดิม rename</td></tr>'
        '<tr><td rowspan="2"><strong>Scheduling</strong></td>'
        '<td>round (10 min)</td><td><strong>Loop</strong></td>'
        '<td>DOOH เรียก loop cycle</td></tr>'
        '<tr><td>round-robin</td><td><strong>Loop Rotation</strong></td>'
        '<td>การหมุนเวียน creative ใน loop</td></tr>'
        '<tr><td><strong>Reporting</strong></td>'
        '<td>play history</td><td><strong>Proof of Play (PoP)</strong></td>'
        '<td>DOOH standard &mdash; endpoint ยังเป็น <code>/v2/play-history</code></td></tr>'
        '</table>'
    )

    _term_content += "<h4>Backend Components</h4>"
    _term_content += (
        '<table>'
        '<tr><th>คำเดิม (Current Code)</th><th>คำใหม่ (Proposed)</th><th>File Path</th></tr>'
        '<tr><td><code>PlaylistBuilderService</code></td><td><strong>AdDecisioningService</strong> (Ad Decisioning Engine)</td>'
        '<td><code>app/Services/AdDecisioningService.ts</code> (NEW)</td></tr>'
        '<tr><td><code>DevicePlaylist</code> model</td><td><strong>ScreenSchedule</strong></td>'
        '<td><code>app/Models/ScreenSchedule.ts</code> (NEW)</td></tr>'
        '<tr><td><code>DevicePlaylistItem</code> model</td><td><strong>ScreenScheduleItem</strong></td>'
        '<td><code>app/Models/ScreenScheduleItem.ts</code> (NEW)</td></tr>'
        '<tr><td><code>PlayScheduleExclusiveService</code></td><td>Absorbed into <strong>AdDecisioningService</strong></td>'
        '<td><code>app/Services/v2/PlayScheduleExclusiveService.ts</code></td></tr>'
        '<tr><td><code>PlayScheduleCreateByExclusive</code> (job)</td><td>Absorbed into <strong>AdDecisioningService</strong></td>'
        '<td><code>app/Jobs/PlayScheduleCreateByExclusive.ts</code></td></tr>'
        '<tr><td><code>PlayScheduleFrequencyService</code></td><td><strong>House content rotation</strong> (input to ADE)</td>'
        '<td><code>app/Services/PlayScheduleFrequencyService.ts</code></td></tr>'
        '<tr><td><code>PlaySchedulePeriodService</code></td><td><strong>Campaign period</strong> (input to ADE)</td>'
        '<td><code>app/Services/PlaySchedulePeriodService.ts</code></td></tr>'
        '<tr><td><code>GET /v2/play-schedules</code> + <code>/playlist-advertisements</code></td>'
        '<td><strong><code>GET /v2/screen-schedule</code></strong> (unified)</td>'
        '<td>NEW endpoint</td></tr>'
        '<tr><td><code>AdvertisementDisplayExclusive</code></td><td>Remains (data source for <strong>guaranteed spots</strong>)</td>'
        '<td><code>app/Models/AdvertisementDisplayExclusive.ts</code></td></tr>'
        '<tr><td><code>AdGroupDisplayTimeExclusive</code></td><td>Remains (data source for <strong>guaranteed time window</strong>)</td>'
        '<td><code>app/Models/AdGroupDisplayTimeExclusive.ts</code></td></tr>'
        '<tr><td colspan="3"><em>NO CHANGE:</em> <code>PlayScheduleCalculate.ts</code>, '
        '<code>PlayScheduleCalculatePerScreen.ts</code>, <code>PlaySchedule.ts</code> model, '
        '<code>checkIsBillboardsReserved.ts</code></td></tr>'
        '</table>'
    )

    _term_content += "<h4>Player Components</h4>"
    _term_content += (
        '<table>'
        '<tr><th>คำเดิม (Current Code)</th><th>คำใหม่ (Proposed)</th><th>หมายเหตุ</th></tr>'
        '<tr><td>Smart Player (schedule + render)</td><td><strong>Dumb Renderer</strong> (play <code>sequence[i++]</code>)</td>'
        '<td>Feature flag: <code>billboard.player_mode</code></td></tr>'
        '<tr><td><code>SchedulePlayComponent</code><br/><code>TimeSlotComponent</code><br/><code>PlaylistComponent</code></td>'
        '<td>Absorbed into <strong>Dumb Renderer</strong></td>'
        '<td>3,500+ lines &rarr; simple sequence player</td></tr>'
        '<tr><td><code>calculatePlaySchedules</code> (1s poll)</td><td><strong>Eliminated</strong> &mdash; backend pre-positions</td>'
        '<td>ไม่ต้อง poll ทุก 1 วินาทีอีก</td></tr>'
        '<tr><td><code>pausePlayData</code> (single var)</td><td><strong>Eliminated</strong> &mdash; no nested interrupt</td>'
        '<td>ADE resolves ที่ backend แทน</td></tr>'
        '<tr><td>(no name)</td><td><strong>Interrupt Controller (IC)</strong></td>'
        '<td>NEW: P0/P1-TK/P1-ET interrupt only</td></tr>'
        '<tr><td>(no name)</td><td><strong>Inbox Handler</strong></td>'
        '<td>NEW: event_id dedup + version check</td></tr>'
        '<tr><td><code>player.history.json</code> (retry)</td><td><strong>PoP Outbox</strong></td>'
        '<td>pending &rarr; sent &rarr; acked cycle</td></tr>'
        '<tr><td><code>localStorage</code></td><td><strong>3-Tier Cache</strong> (Tauri Store)</td>'
        '<td>Tier 1: Live, Tier 2: Buffer, Tier 3: Fallback</td></tr>'
        '<tr><td>(implicit states)</td><td><strong>State Machine</strong> (10 explicit states)</td>'
        '<td>BOOT &rarr; SPLASH &rarr; SYNC &rarr; ONLINE/OFFLINE &rarr; FALLBACK</td></tr>'
        '</table>'
    )

    _term_content += "<h4>Pusher Events</h4>"
    _term_content += (
        '<table>'
        '<tr><th>Event เดิม</th><th>Event ใหม่ / เปลี่ยนแปลง</th><th>หมายเหตุ</th></tr>'
        '<tr><td><code>update-play-schedule</code></td><td><strong><code>schedule-updated</code></strong></td>'
        '<td>Renamed + typed contract</td></tr>'
        '<tr><td><code>created-play-schedule</code></td><td>Absorbed into <strong><code>schedule-updated</code></strong></td>'
        '<td>ไม่แยก create/update อีก</td></tr>'
        '<tr><td><code>approved-advertisement-exclusive</code></td><td>Absorbed into <strong><code>schedule-updated</code></strong></td>'
        '<td>ADE pre-positions guaranteed &mdash; ไม่ inject ตรง</td></tr>'
        '<tr><td><code>stop-advertisement</code></td><td>Unchanged (+ typed contract)</td>'
        '<td>Creative cancelled</td></tr>'
        '<tr><td><code>un-pair-screen</code></td><td>Unchanged (+ typed contract)</td>'
        '<td>Device unpaired</td></tr>'
        '<tr><td>(ไม่มี)</td><td><strong><code>takeover-start</code></strong></td><td>NEW: P1-TK boundary</td></tr>'
        '<tr><td>(ไม่มี)</td><td><strong><code>takeover-end</code></strong></td><td>NEW: P1-TK boundary</td></tr>'
        '<tr><td>(ไม่มี)</td><td><strong><code>p0-emergency</code></strong></td><td>NEW: system alert</td></tr>'
        '<tr><td>(ไม่มี)</td><td><strong><code>device-config-updated</code></strong></td><td>NEW: pre-stage creative</td></tr>'
        '</table>'
    )

    _term_content += "<h4>API &amp; Data Fields</h4>"
    _term_content += (
        '<table>'
        '<tr><th>Field / API เดิม</th><th>ใหม่</th><th>หมายเหตุ</th></tr>'
        '<tr><td><code>media_code</code></td><td><strong><code>creative_code</code></strong></td>'
        '<td>DOOH: creative = ชิ้นงานโฆษณา</td></tr>'
        '<tr><td><code>media_url</code></td><td><strong><code>creative_url</code></strong></td><td></td></tr>'
        '<tr><td><code>media_checksum</code></td><td><strong><code>creative_checksum</code></strong></td><td></td></tr>'
        '<tr><td><code>media_manifest</code></td><td><strong><code>creative_manifest</code></strong></td><td></td></tr>'
        '<tr><td><code>type: "paid" | "owner"</code></td>'
        '<td><strong><code>type: "campaign" | "house"</code></strong></td>'
        '<td>campaign = sold inventory</td></tr>'
        '<tr><td><code>priority: "normal" | "exclusive"</code></td>'
        '<td><strong><code>priority: "guaranteed" | "direct" | "spot" | "house"</code></strong></td>'
        '<td>4-level แทน 2-level</td></tr>'
        '<tr><td><code>ad_display_count</code></td><td><strong><code>impression_target</code></strong></td>'
        '<td>DOOH: impression = 1 play ที่นับได้</td></tr>'
        '<tr><td><code>PlaylistUpdatedEvent</code></td><td><strong><code>ScheduleUpdatedEvent</code></strong></td>'
        '<td>Interface ใหม่</td></tr>'
        '</table>'
    )

    _term_content += note_panel(
        "<p><strong>Code ยังไม่เปลี่ยน:</strong> Mapping นี้คือ <em>terminology</em> ในเอกสาร architecture. "
        "Code refactor จะทำเป็น phase ตาม Migration Plan &mdash; "
        "ไม่ต้อง rename ทุกอย่างพร้อมกัน. "
        "Model เดิม (<code>PlaySchedule</code>, <code>AdvertisementDisplayExclusive</code>, <code>Billboard</code>) "
        "ยังใช้ชื่อเดิมใน codebase จนกว่าจะ migrate</p>"
    )

    sections.append(expand_section(
        "Terminology Mapping: 5 tables (Core, Backend, Player, Pusher, API)",
        _term_content
    ))

    sections.append("<h3>บันทึกการตัดสินใจ: ทำไมไม่ใช้ Event-Sourcing</h3>")
    sections.append(expand_section("ADR-002: Why Event-Driven, NOT Event-Sourcing",
        warning_panel(
            "<p><strong>ADR-002:</strong> Event-Driven Architecture (NOT Event-Sourcing)</p>"
        ) +
        '<table>'
        '<tr><th>Aspect</th><th>Details</th></tr>'
        '<tr><td><strong>Context</strong></td><td>'
        'ระบบใช้ Pusher + BullMQ + Play history retry ซึ่งเป็น event-driven pattern อยู่แล้ว '
        'แต่ไม่มี typed contracts, domain events, หรือ idempotency &mdash; ต้อง formalize</td></tr>'
        '<tr><td><strong>Options Considered</strong></td><td>'
        '<strong>A) Formalize Event-Driven</strong> &mdash; typed contracts, domain events (in-memory), outbox/inbox dedup<br/>'
        '<strong>B) Full Event-Sourcing</strong> &mdash; event store (Kafka/EventStoreDB), projections, snapshots, CQRS</td></tr>'
        '<tr><td><strong>Decision</strong></td><td><strong>Option A: Formalize Event-Driven</strong></td></tr>'
        '<tr><td><strong>Rationale</strong></td><td>'
        '<ul>'
        '<li><strong>Scale:</strong> ~100-500 billboards, ไม่ใช่ millions of events/sec</li>'
        '<li><strong>Team:</strong> Junior devs 3 คน (fix-heavy, need review) &mdash; event store + projections ซับซ้อนเกินไป</li>'
        '<li><strong>PlaySchedule model:</strong> CRUD + status (WAITING&rarr;PLAYING&rarr;PLAYED) ใช้งานได้ดี ไม่จำเป็นต้อง replay</li>'
        '<li><strong>No business need:</strong> ไม่ต้อง replay events ย้อนหลัง, ไม่ต้อง audit trail ระดับ event</li>'
        '<li><strong>Operational cost:</strong> Event store (Kafka/EventStoreDB) + schema versioning + eventual consistency debugging</li>'
        '</ul></td></tr>'
        '<tr><td><strong>Consequences</strong></td><td>'
        '<ul>'
        '<li>+ ง่ายต่อ team ในการ maintain</li>'
        '<li>+ ไม่ต้องเพิ่ม infrastructure (ใช้ Redis + Pusher + BullMQ เดิม)</li>'
        '<li>+ Typed contracts ป้องกัน runtime error</li>'
        '<li>+ Domain events เพิ่ม traceability ใน code</li>'
        '<li>- ไม่สามารถ replay events ได้ (ต้องมี backup/restore แบบ traditional)</li>'
        '<li>- ถ้า scale ถึง 5,000+ จอ อาจต้อง revisit</li>'
        '</ul></td></tr>'
        '<tr><td><strong>Review Date</strong></td><td>Revisit เมื่อ scale &ge; 2,000 billboards หรือ team &ge; 8 devs</td></tr>'
        '</table>'
    ))

    sections.append("<h3>Checklist การ Implement</h3>")
    sections.append(success_panel(
        "<p><strong>สิ่งที่ต้อง formalize (เรียงตาม priority):</strong></p>"
        "<ol>"
        "<li><strong>Typed Pusher event contracts</strong> &mdash; shared interfaces (backend + player)</li>"
        "<li><strong>Version protocol</strong> &mdash; monotonic <code>version</code> per device on every Pusher event</li>"
        "<li><strong>PoP Outbox pattern</strong> &mdash; Tauri Store with UUID idempotency key + flush cycle</li>"
        "<li><strong>Inbox dedup</strong> &mdash; <code>event_id</code> tracking (last 100) + version gap detection</li>"
        "<li><strong>PoP deduplication</strong> &mdash; Redis <code>idem:{uuid}</code> check on PoP endpoint</li>"
        "<li><strong>Domain events (in-code)</strong> &mdash; named typed objects, passed between services, logged for observability</li>"
        "</ol>"
    ))

    return "\n".join(sections)


# ─── Event Storming Legend (shared across pages 9-11) ───


def _es_legend() -> str:
    """Event Storming notation legend table (shape-based)."""
    return (
        '<table>'
        '<tr><th>Element</th><th>Shape</th><th>Meaning</th></tr>'
        '<tr><td><strong>Domain Event</strong></td>'
        '<td><code>[text]</code> rectangle</td><td>สิ่งที่เกิดขึ้นแล้ว (past tense) &mdash; state change ใน domain</td></tr>'
        '<tr><td><strong>Command</strong></td>'
        '<td><code>[text]</code> rectangle</td><td>Action ที่ trigger event (imperative verb)</td></tr>'
        '<tr><td><strong>Aggregate</strong></td>'
        '<td><code>[text]</code> rectangle</td><td>Entity/service ที่ประมวลผล command แล้วสร้าง event</td></tr>'
        '<tr><td><strong>Policy</strong></td>'
        '<td><code>{{text}}</code> hexagon</td><td>Business rule: &ldquo;เมื่อ X เกิดขึ้น ให้ทำ Y&rdquo;</td></tr>'
        '<tr><td><strong>Actor</strong></td>'
        '<td><code>([text])</code> stadium</td><td>คนหรือ role ในระบบที่เริ่มต้น command</td></tr>'
        '<tr><td><strong>External System</strong></td>'
        '<td><code>[(text)]</code> cylinder</td><td>ระบบภายนอกที่เราควบคุมไม่ได้ (Pusher, CDN, etc.)</td></tr>'
        '<tr><td><strong>Read Model</strong></td>'
        '<td><code>[/text/]</code> parallelogram</td><td>ข้อมูลที่ต้องดูก่อนตัดสินใจ ก่อน issue command</td></tr>'
        '</table>'
    )


def build_page_9(page_id: str) -> str:
    """Page 9: Event Storming — Big Picture (1 mermaid, 0 code blocks)."""
    global _code_block_count
    _code_block_count = 0
    sections = []

    sections.append(toc())
    sections.append("<h2>Event Storming: ภาพรวม (Big Picture)</h2>")
    sections.append(info_panel(
        "<p><strong>Event Storming Level 1 &mdash; Big Picture</strong><br/>"
        "ภาพรวม domain events ทั้งระบบ Backend-Driven Player &mdash; "
        "จัดตาม swimlane (Scheduling, Playback, Interrupt, Device Lifecycle)<br/>"
        "อ้างอิง methodology ของ Alberto Brandolini &mdash; "
        "ใช้ shape-coded nodes แทน sticky notes</p>"
    ))

    # Legend
    sections.append("<h3>สัญลักษณ์ที่ใช้ (Notation Legend)</h3>")
    sections.append(expand_section("ES Notation Legend (8 elements)", _es_legend()))

    # Big Picture Timeline
    sections.append("<h3>Timeline ของ Domain Events</h3>")
    sections.append(note_panel(
        "<p>อ่านจาก <strong>ซ้ายไปขวา</strong> ตาม timeline &mdash; "
        "แต่ละ swimlane แสดง flow ของ domain events ที่เกี่ยวข้องกัน<br/>"
        "<strong>เส้นประ</strong> = cross-swimlane event flow (Pusher/API)</p>"
    ))
    sections.append(mermaid_diagram(
        load_diagram("09-1-big-picture.mmd"),
        page_id=page_id,
    ))

    # Actors
    sections.append("<h3>ผู้กระทำ (Actors)</h3>")
    sections.append(
        '<table>'
        '<tr><th>Actor</th><th>Type</th><th>Description</th></tr>'
        '<tr><td><strong>Cron</strong></td><td>System</td>'
        '<td>BullMQ scheduled job &mdash; trigger คำนวณ schedule ทุก 10 นาที</td></tr>'
        '<tr><td><strong>Admin</strong></td><td>Human</td>'
        '<td>Admin ของ platform &mdash; approve takeover, trigger emergency, จัดการจอ</td></tr>'
        '<tr><td><strong>Player</strong></td><td>Device</td>'
        '<td>Tauri desktop app บนจอโฆษณา &mdash; รับ schedule, เล่น creative, รายงาน PoP</td></tr>'
        '</table>'
    )

    # External Systems
    sections.append("<h3>ระบบภายนอก (External Systems)</h3>")
    sections.append(
        '<table>'
        '<tr><th>System</th><th>Role</th><th>Protocol</th></tr>'
        '<tr><td><strong>Pusher</strong></td><td>ส่ง event แบบ real-time</td><td>WebSocket</td></tr>'
        '<tr><td><strong>BullMQ</strong></td><td>Job queue / cron scheduler</td><td>Redis-backed queue</td></tr>'
        '<tr><td><strong>Redis</strong></td><td>Caching + ป้องกัน duplicate</td><td>In-memory store</td></tr>'
        '<tr><td><strong>CDN</strong></td><td>ส่งไฟล์ creative</td><td>HTTPS</td></tr>'
        '<tr><td><strong>Tauri Store</strong></td><td>เก็บข้อมูลบน device</td><td>File-based (device)</td></tr>'
        '</table>'
    )

    # Hot Spots
    sections.append("<h3>จุดเสี่ยง (Hot Spots)</h3>")
    sections.append(warning_panel(
        "<p><strong>ความเสี่ยงและประเด็นที่ยังไม่ได้แก้:</strong></p>"
        "<ul>"
        "<li><s><strong>Version gap threshold</strong> &mdash; "
        "gap กี่ version ถึงจะส่ง full playlist แทน delta?</s> "
        "<strong>แก้แล้ว:</strong> gap &gt; 3 versions &rarr; full replace (ดู Section 4: Algorithm)</li>"
        "<li><strong>ระยะเวลา Offline สูงสุด</strong> &mdash; "
        "player ใช้ Tier 3 fallback ได้นานแค่ไหนก่อน content จะ stale? (วัน? สัปดาห์?)</li>"
        "<li><strong>Takeover ทับกัน</strong> &mdash; "
        "ถ้า 2 takeover จองช่วงเวลาทับกันบนจอเดียว? (ปัจจุบัน: block ตอนจอง)</li>"
        "<li><strong>การจัดลำดับ Make-good ให้เท่าเทียม</strong> &mdash; "
        "จัดลำดับ make-good ยังไงเมื่อหลาย ad โดน interrupt ใน TK block เดียว?</li>"
        "<li><strong>ความเสถียรของ Pusher</strong> &mdash; "
        "Pusher เป็น best-effort delivery &mdash; version protocol จัดการ gap ได้ แต่ latency ไม่แน่นอน</li>"
        "</ul>"
    ))

    return "\n".join(sections)


def build_page_10(page_id: str) -> str:
    """Page 10: Event Storming — Process Modelling (5 mermaid, 0 code blocks)."""
    global _code_block_count
    _code_block_count = 0
    sections = []

    sections.append(toc())
    sections.append("<h2>Event Storming: Process Modelling</h2>")
    sections.append(info_panel(
        "<p><strong>Event Storming Level 2 &mdash; Process Modelling</strong><br/>"
        "แต่ละ process แสดง flow ตาม grammar: "
        "<strong>Actor &rarr; Command &rarr; Aggregate &rarr; Event &rarr; Policy &rarr; ...</strong><br/>"
        "Read Models (green) แสดงข้อมูลที่ต้องใช้ก่อนตัดสินใจ</p>"
    ))

    # Legend
    sections.append("<h3>สัญลักษณ์ที่ใช้ (Notation Legend)</h3>")
    sections.append(expand_section("ES Notation Legend (8 elements)", _es_legend()))

    # Process A: Schedule Calculation
    sections.append("<hr/>")
    sections.append("<h3>Process A: คำนวณ Schedule</h3>")
    sections.append(note_panel(
        "<p><strong>Trigger:</strong> Cron ทำงานทุก 10 นาที<br/>"
        "<strong>ผลลัพธ์:</strong> Ordered screen schedule ถูก push ไปยัง player ผ่าน Pusher<br/>"
        "<strong>Grammar:</strong> Cron &rarr; CalculateSchedule &rarr; PlaySchedule &rarr; "
        "ScheduleCalculated &rarr; <em>BuildScreenSchedule</em> &rarr; AdDecisioningService &rarr; "
        "ScreenScheduleBuilt &rarr; <em>PushToPlayer</em> &rarr; Pusher</p>"
    ))
    sections.append(mermaid_diagram(
        load_diagram("10-1-process-schedule-calc.mmd"),
        page_id=page_id,
    ))

    # Process B: Normal Playback
    sections.append("<hr/>")
    sections.append("<h3>Process B: เล่นปกติ (Normal Playback)</h3>")
    sections.append(note_panel(
        "<p><strong>Trigger:</strong> Player ได้รับ schedule-updated event จาก Pusher<br/>"
        "<strong>ผลลัพธ์:</strong> Creative เล่นบนจอ + PoP (Proof of Play) รายงานกลับ backend<br/>"
        "<strong>Policy สำคัญ:</strong> Inbox dedup ด้วย event_id + ตรวจ version ก่อน fetch</p>"
    ))
    sections.append(mermaid_diagram(
        load_diagram("10-2-process-normal-play.mmd"),
        page_id=page_id,
    ))

    # Process C: Takeover Interrupt
    sections.append("<hr/>")
    sections.append("<h3>Process C: Interrupt จาก Takeover (P1-TK)</h3>")
    sections.append(note_panel(
        "<p><strong>Trigger:</strong> Admin approve daypart takeover (เช่น brand ซื้อ 08:00-09:00)<br/>"
        "<strong>ผลลัพธ์:</strong> Ad ปัจจุบันโดน interrupt, takeover creative เล่นตลอด block, "
        "ad ที่โดน interrupt ได้ make-good compensation<br/>"
        "<strong>ข้ามขอบเขต:</strong> Backend (approve + schedule) &rarr; Pusher &rarr; Player (interrupt + เล่น)</p>"
    ))
    sections.append(mermaid_diagram(
        load_diagram("10-3-process-takeover.mmd"),
        page_id=page_id,
    ))

    # Process D: Offline & Reconnect
    sections.append("<hr/>")
    sections.append("<h3>Process D: Offline และเชื่อมต่อใหม่</h3>")
    sections.append(note_panel(
        "<p><strong>Trigger:</strong> เน็ตหลุด (Pusher disconnect)<br/>"
        "<strong>ผลลัพธ์:</strong> ลดระดับอย่างค่อยเป็นค่อยไป (graceful degradation) ผ่าน 3-tier cache แล้ว delta sync ตอนกลับมา online<br/>"
        "<strong>Policy สำคัญ:</strong> State Machine transitions: ONLINE &rarr; OFFLINE &rarr; FALLBACK &rarr; ONLINE</p>"
    ))
    sections.append(mermaid_diagram(
        load_diagram("10-4-process-offline.mmd"),
        page_id=page_id,
    ))

    # Process E: Emergency (P0)
    sections.append("<hr/>")
    sections.append("<h3>Process E: Emergency Override (P0)</h3>")
    sections.append(note_panel(
        "<p><strong>Trigger:</strong> Admin trigger P0 emergency (ประกาศราชการ, วิกฤต, ฯลฯ)<br/>"
        "<strong>ผลลัพธ์:</strong> Interrupt content ใดๆ ทันที, เล่น emergency creative, schedule make-good<br/>"
        "<strong>Priority:</strong> P0 ชนะทุกอย่าง &mdash; รวมถึง takeover ที่กำลังทำงานอยู่</p>"
    ))
    sections.append(mermaid_diagram(
        load_diagram("10-5-process-emergency.mmd"),
        page_id=page_id,
    ))

    return "\n".join(sections)


def build_page_11(page_id: str) -> str:
    """Page 11: Event Storming — Software Design (2 mermaid, 0 code blocks)."""
    global _code_block_count
    _code_block_count = 0
    sections = []

    sections.append(toc())
    sections.append("<h2>Event Storming: การออกแบบ Software</h2>")
    sections.append(info_panel(
        "<p><strong>Event Storming Level 3 &mdash; Software Design</strong><br/>"
        "Bounded Contexts, Aggregates, and Context Mapping &mdash; "
        "จาก Process Modelling (Level 2) มาจัดกลุ่มเป็น architectural boundaries</p>"
    ))

    # Legend
    sections.append("<h3>สัญลักษณ์ที่ใช้ (Notation Legend)</h3>")
    sections.append(expand_section("ES Notation Legend (8 elements)", _es_legend()))

    # Bounded Context Map
    sections.append("<hr/>")
    sections.append("<h3>แผนที่ Bounded Context</h3>")
    sections.append(note_panel(
        "<p>4 Bounded Contexts &mdash; แต่ละ context มี aggregates ที่ทำงานร่วมกัน<br/>"
        "ลูกศรระหว่าง context = event ที่ส่งข้ามขอบเขต (via Pusher หรือ API call)</p>"
    ))
    sections.append(mermaid_diagram(
        load_diagram("11-1-context-map.mmd"),
        page_id=page_id,
    ))

    # Aggregates per Context
    sections.append("<h3>Aggregate แยกตาม Context</h3>")

    # Scheduling Context
    sections.append("<h4>Scheduling Context (Backend)</h4>")
    sections.append(
        '<table>'
        '<tr><th>Aggregate</th><th>Responsibility</th><th>Key Invariants</th><th>Events Owned</th></tr>'
        '<tr><td><strong>PlaySchedule</strong></td>'
        '<td>ผลลัพธ์จากการคำนวณ schedule (ต่อจอ ต่อรอบ cron)</td>'
        '<td>1 active schedule ต่อจอต่อรอบ</td>'
        '<td>ScheduleCalculated</td></tr>'
        '<tr><td><strong>AdDecisioningService</strong></td>'
        '<td>จัดลำดับตาม priority, สลับ house content, กำหนด sequence_no, version++</td>'
        '<td>P1-G pre-positioned, P2/P3 ตาม SOV ratio, P4 เติมช่องว่าง</td>'
        '<td>ScreenScheduleBuilt</td></tr>'
        '<tr><td><strong>ScreenSchedule</strong></td>'
        '<td>Ordered playlist พร้อม versioning (เพิ่มขึ้นเรื่อยๆ ต่อ device)</td>'
        '<td>version เพิ่มขึ้นเสมอ, schedule เก่าถูก mark &ldquo;replaced&rdquo;</td>'
        '<td>(persisted state)</td></tr>'
        '</table>'
    )

    # Interrupt Context
    sections.append("<h4>Interrupt Context (Backend + Player)</h4>")
    sections.append(
        '<table>'
        '<tr><th>Aggregate</th><th>Responsibility</th><th>Key Invariants</th><th>Events Owned</th></tr>'
        '<tr><td><strong>TakeoverSchedule</strong></td>'
        '<td>จอง daypart takeover (P1-TK: brand ซื้อ time block)</td>'
        '<td>TK ซ้อนกันบนจอเดียวไม่ได้, lifecycle: booked &rarr; active &rarr; completed</td>'
        '<td>TakeoverApproved, TakeoverStateChanged</td></tr>'
        '<tr><td><strong>ExactTimeSpot</strong></td>'
        '<td>P1-ET: เล่นตรงเวลาพร้อม tolerance window</td>'
        '<td>tolerance default 5s, 1 spot ต่อ play_at ต่อจอ</td>'
        '<td>(triggers InterruptController)</td></tr>'
        '<tr><td><strong>InterruptController</strong></td>'
        '<td>หยุด ad ปัจจุบัน, เล่น interrupt creative, resume หลังจบ</td>'
        '<td>ลำดับ priority: P0 > P1-TK > P1-ET, nested interrupt เข้าคิว</td>'
        '<td>AdInterrupted</td></tr>'
        '<tr><td><strong>MakeGoodRecord</strong></td>'
        '<td>ชดเชย ad ที่โดน interrupt &mdash; ใส่คืนใน cycle ถัดไป</td>'
        '<td>1 make-good ต่อ 1 interruption, ข้ามถ้า campaign หมดอายุ</td>'
        '<td>MakeGoodScheduled</td></tr>'
        '</table>'
    )

    # Playback Context
    sections.append("<h4>Playback Context (Player)</h4>")
    sections.append(
        '<table>'
        '<tr><th>Aggregate</th><th>Responsibility</th><th>Key Invariants</th><th>Events Owned</th></tr>'
        '<tr><td><strong>InboxHandler</strong></td>'
        '<td>รับ Pusher event, dedup ด้วย event_id, ตรวจ version</td>'
        '<td>ประมวลผลเฉพาะ version > local_version และ event_id ใหม่</td>'
        '<td>ScheduleReceived</td></tr>'
        '<tr><td><strong>3-Tier Cache</strong></td>'
        '<td>เก็บบน device: Tier 1 (live) &rarr; Tier 2 (buffer) &rarr; Tier 3 (fallback/house)</td>'
        '<td>Tier 1 ต้องเป็น version ล่าสุด, Tier 3 พร้อมเสมอ (house loop)</td>'
        '<td>CacheUpdated</td></tr>'
        '<tr><td><strong>StateMachine</strong></td>'
        '<td>BOOT &rarr; CACHED &rarr; SYNC &rarr; ONLINE &rarr; OFFLINE &rarr; FALLBACK</td>'
        '<td>อยู่ได้ 1 state พร้อมกัน, log ทุก transition, กำหนดทาง recovery ไว้</td>'
        '<td>DeviceResynced</td></tr>'
        '<tr><td><strong>Renderer</strong></td>'
        '<td>Dumb Renderer: เล่น sequence[i++], ไม่มี logic จัดลำดับ</td>'
        '<td>เล่นตาม cache ให้มา, ไม่ข้าม, ไม่สลับลำดับ</td>'
        '<td>CreativePlayed</td></tr>'
        '</table>'
    )

    # Reporting Context
    sections.append("<h4>Reporting Context (Player &rarr; Backend)</h4>")
    sections.append(
        '<table>'
        '<tr><th>Aggregate</th><th>Responsibility</th><th>Key Invariants</th><th>Events Owned</th></tr>'
        '<tr><td><strong>PoP Outbox</strong></td>'
        '<td>เก็บ play event บน device, flush ไป backend ทุก 1 นาที</td>'
        '<td>lifecycle: pending &rarr; sent &rarr; acked, retry &lt; 10 ครั้ง</td>'
        '<td>PoPRecorded</td></tr>'
        '<tr><td><strong>PlayHistory</strong></td>'
        '<td>เก็บ PoP records ฝั่ง backend</td>'
        '<td>ป้องกัน duplicate ด้วย X-Idempotency-Key (UUID)</td>'
        '<td>PoPReceived</td></tr>'
        '<tr><td><strong>Idempotency</strong></td>'
        '<td>ป้องกัน duplicate ผ่าน Redis สำหรับ PoP endpoint</td>'
        '<td>Key หมดอายุ 24 ชม. (TTL-based), ป้องกันข้อมูลซ้ำ</td>'
        '<td>(guard, ไม่สร้าง event)</td></tr>'
        '</table>'
    )

    # Context Relationships
    sections.append("<hr/>")
    sections.append("<h3>ความสัมพันธ์ระหว่าง Context</h3>")
    sections.append(
        '<table>'
        '<tr><th>From</th><th>To</th><th>Event</th><th>Mechanism</th><th>Relationship Type</th></tr>'
        '<tr><td>Scheduling</td><td>Playback</td>'
        '<td>ScreenScheduleBuilt</td><td>Pusher WebSocket</td><td>Published Language</td></tr>'
        '<tr><td>Interrupt</td><td>Playback</td>'
        '<td>TakeoverStart / TakeoverEnd</td><td>Pusher WebSocket</td><td>Published Language</td></tr>'
        '<tr><td>Playback</td><td>Reporting</td>'
        '<td>PoPRecorded</td><td>HTTP (Outbox flush)</td><td>Conformist</td></tr>'
        '<tr><td>Interrupt</td><td>Scheduling</td>'
        '<td>MakeGoodScheduled</td><td>Internal (same backend)</td><td>Shared Kernel</td></tr>'
        '<tr><td>Reporting</td><td>Scheduling</td>'
        '<td>(future: analytics feedback)</td><td>TBD</td><td>TBD</td></tr>'
        '</table>'
    )

    # ACL Diagram
    sections.append("<hr/>")
    sections.append("<h3>Anti-Corruption Layer: ระบบเดิมสู่ระบบใหม่</h3>")
    sections.append(note_panel(
        "<p>ACL (Anti-Corruption Layer) &mdash; translation boundary ระหว่างระบบเดิมกับ architecture ใหม่<br/>"
        "Legacy code จะยังทำงานเหมือนเดิม แต่ output ถูก translate เป็น new domain model ผ่าน ACL<br/>"
        "เมื่อ migration เสร็จ ACL จะถูกถอดออก</p>"
    ))
    sections.append(mermaid_diagram(
        load_diagram("11-2-acl-translation.mmd"),
        page_id=page_id,
    ))

    return "\n".join(sections)


SECTION_BUILDERS = {
    "parent": ("parent", build_parent_content),
    "1": ("1_problem_current", build_page_1),
    "2": ("2_proposed", build_page_2),
    "3": ("3_key_flows", build_page_3),
    "4": ("4_tech_algorithm", build_page_4),
    "5": ("5_tech_player", build_page_5),
    "6": ("6_interrupt_makegood", build_page_6),
    "7": ("7_events", build_page_7),
    "8": ("8_edge_migration", build_page_8),
    "9": ("9_es_big_picture", build_page_9),
    "10": ("10_es_process", build_page_10),
    "11": ("11_es_design", build_page_11),
}


def _get_api():
    creds = load_credentials()
    return ConfluenceAPI(
        base_url=creds["CONFLUENCE_URL"],
        auth_header=get_auth_header(
            creds["CONFLUENCE_USERNAME"], creds["CONFLUENCE_API_TOKEN"]
        ),
        ssl_context=create_ssl_context(),
    )


def _update_page(api, page_id: str, content: str, title: str | None = None):
    page = api.get_page(page_id)
    version = page["version"]["number"]
    t = title or page["title"]
    api.update_page(page_id=page_id, title=t, content=content, version=version)
    new_ver = version + 1
    print(f"  Updated: {t} (v{version} -> v{new_ver})")
    print(f"  URL: https://{{JIRA_SITE}}/wiki/spaces/{SPACE_KEY}/pages/{page_id}")
    # Fix Confluence ADF panel bug: storage→ADF conversion sometimes creates
    # bodiedExtension instead of native panel for success/error/warning macros.
    # This causes "Error loading the extension!" in view mode.
    fixed = _fix_page_panels(api, page_id, t, new_ver)
    if fixed:
        print(f"  Fixed {fixed} ADF panel(s) (bodiedExtension → native panel)")


# Panel macro keys that Confluence should render as native ADF panels
_PANEL_TYPES = {"info", "note", "warning", "error", "success", "tip"}


def _fix_page_panels(api, page_id: str, title: str, current_ver: int) -> int:
    """Fix Confluence bug: bodiedExtension with panel-type key → native panel.

    Returns number of nodes fixed (0 if no fix needed).
    """
    # Fetch ADF via v2 API
    v2_data = api._request("GET", f"/api/v2/pages/{page_id}?body-format=atlas_doc_format")
    adf = json.loads(v2_data["body"]["atlas_doc_format"]["value"])
    ver = v2_data["version"]["number"]

    fixed_count = 0

    def fix_node(node):
        nonlocal fixed_count
        if not isinstance(node, dict):
            return node
        if (
            node.get("type") == "bodiedExtension"
            and node.get("attrs", {}).get("extensionKey", "") in _PANEL_TYPES
            and "macro.core" in node.get("attrs", {}).get("extensionType", "")
        ):
            fixed_count += 1
            return {
                "type": "panel",
                "attrs": {"panelType": node["attrs"]["extensionKey"]},
                "content": [fix_node(c) for c in node.get("content", [])],
            }
        if "content" in node and isinstance(node["content"], list):
            node["content"] = [fix_node(c) for c in node["content"]]
        return node

    adf = fix_node(adf)

    if fixed_count == 0:
        return 0

    # Update via v2 API with fixed ADF
    api._request(
        "PUT",
        f"/api/v2/pages/{page_id}",
        data={
            "id": page_id,
            "status": "current",
            "title": title,
            "body": {
                "representation": "atlas_doc_format",
                "value": json.dumps(adf),
            },
            "version": {"number": ver + 1},
        },
    )
    return fixed_count


def main():
    dry_run = "--dry-run" in sys.argv
    create_all = "--create-all" in sys.argv

    # Parse --section N
    section = None
    if "--section" in sys.argv:
        idx = sys.argv.index("--section")
        if idx + 1 < len(sys.argv):
            section = sys.argv[idx + 1]
        else:
            print("Error: --section requires argument (parent, 1-11)")
            sys.exit(1)

    # Parse --update PAGE_ID (legacy)
    update_page_id = None
    if "--update" in sys.argv:
        idx = sys.argv.index("--update")
        if idx + 1 < len(sys.argv):
            update_page_id = sys.argv[idx + 1]

    page_ids = load_page_ids()
    parent_id = page_ids["parent"]

    # ── Dry-run single section ──
    if dry_run and section:
        if section not in SECTION_BUILDERS:
            print(f"Error: unknown section '{section}'. Valid: {list(SECTION_BUILDERS.keys())}")
            sys.exit(1)
        key, builder = SECTION_BUILDERS[section]
        pid = parent_id if section == "parent" else (page_ids["pages"].get(key) or "DRAFT")
        content = builder(page_id=pid)
        out = Path(__file__).parent.parent / "tasks" / f"arch-page-{section}-preview.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(content, encoding="utf-8")
        print(f"  DRY RUN section {section} — {out}")
        print(f"  Content length: {len(content)} chars, code blocks: {_code_block_count}")
        return

    # ── Dry-run all sections ──
    if dry_run and not section:
        out_dir = Path(__file__).parent.parent / "tasks"
        out_dir.mkdir(exist_ok=True)
        for sec, (key, builder) in SECTION_BUILDERS.items():
            pid = parent_id if sec == "parent" else (page_ids["pages"].get(key) or "DRAFT")
            content = builder(page_id=pid)
            out = out_dir / f"arch-page-{sec}-preview.html"
            out.write_text(content, encoding="utf-8")
            print(f"  [{sec:>6}] {len(content):>6} chars, {_code_block_count} code blocks → {out.name}")
        return

    api = _get_api()

    # ── Create all sub-pages ──
    if create_all:
        # Update parent first
        print("=== Updating parent page ===")
        content = build_parent_content(page_id=parent_id)
        _update_page(api, parent_id, content)

        # Create sub-pages
        for sec in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]:
            key, builder = SECTION_BUILDERS[sec]
            title = SUB_PAGE_TITLES[key]
            existing_id = page_ids["pages"].get(key)

            if existing_id:
                print(f"\n=== Updating sub-page {sec}: {title} ===")
                content = builder(page_id=existing_id)
                _update_page(api, existing_id, content, title)
            else:
                print(f"\n=== Creating sub-page {sec}: {title} ===")
                # Create with placeholder, then update with real content
                result = api.create_page(
                    space_key=SPACE_KEY,
                    title=title,
                    content="<p>Loading...</p>",
                    parent_id=parent_id,
                )
                new_id = result.get("id", "unknown")
                page_ids["pages"][key] = new_id
                save_page_ids(page_ids)
                print(f"  Created: {new_id}")

                # Now update with real content (needs page_id for Forge macros)
                content = builder(page_id=new_id)
                _update_page(api, new_id, content, title)

        print(f"\n=== Done! Page IDs saved to {PAGE_IDS_FILE} ===")
        return

    # ── Update single section ──
    if section:
        if section not in SECTION_BUILDERS:
            print(f"Error: unknown section '{section}'. Valid: {list(SECTION_BUILDERS.keys())}")
            sys.exit(1)
        key, builder = SECTION_BUILDERS[section]
        if section == "parent":
            pid = parent_id
        else:
            pid = page_ids["pages"].get(key)
            if not pid:
                # Create new sub-page (page ID is null)
                title = SUB_PAGE_TITLES[key]
                print(f"=== Creating section {section}: {title} ===")
                result = api.create_page(
                    space_key=SPACE_KEY,
                    title=title,
                    content="<p>Loading...</p>",
                    parent_id=parent_id,
                )
                pid = result.get("id", "unknown")
                page_ids["pages"][key] = pid
                save_page_ids(page_ids)
                print(f"  Created: {pid}")
        content = builder(page_id=pid)
        title = SUB_PAGE_TITLES.get(key)
        print(f"=== Updating section {section} ===")
        _update_page(api, pid, content, title)
        return

    # ── Legacy: update specific page ──
    if update_page_id:
        content = build_parent_content(page_id=update_page_id)
        print(f"=== Updating page {update_page_id} ===")
        _update_page(api, update_page_id, content)
        return

    print("Usage:")
    print("  --dry-run [--section N]     Preview HTML output")
    print("  --create-all                Create/update parent + all sub-pages")
    print("  --section N                 Update single section (parent, 1-11)")
    print("  --update PAGE_ID            Legacy: update specific page")


if __name__ == "__main__":
    main()
