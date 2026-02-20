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
    "1_problem_current": "1. Problem Statement & Current Architecture",
    "2_proposed": "2. Proposed Architecture",
    "3_key_flows": "3. Key Flows",
    "4_tech_algorithm": "4. Technical Design: Algorithm & Models",
    "5_tech_player": "5. Technical Design: Player Components",
    "6_interrupt_makegood": "6. Interrupt Controller & Make-Good",
    "7_events": "7. Event-Driven Architecture",
    "8_edge_migration": "8. Edge Cases, Migration & Appendix",
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

    code_html = (
        f'<ac:structured-macro ac:local-id="{code_local_id}" '
        f'ac:name="code" ac:schema-version="1">'
        f'<ac:parameter ac:name="language">mermaid</ac:parameter>'
        f'<ac:plain-text-body><![CDATA[{code}]]></ac:plain-text-body>'
        f'</ac:structured-macro>'
    )
    forge_html = (
        f'<ac:adf-extension>'
        f'{adf_node()}'
        f'<ac:adf-fallback>{adf_node()}</ac:adf-fallback>'
        f'</ac:adf-extension>'
    )
    return code_html + forge_html


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
    sections.append("<h2>1. Problem Statement</h2>")
    sections.append(error_panel(
        "<p><strong>Smart Player (Scheduling Complexity)</strong></p>"
        "<ul>"
        "<li>Player loop-rotates creatives locally (SchedulePlay, TimeSlot, Playlist components)</li>"
        "<li>Guaranteed spot interrupt logic: <code>calculatePlaySchedules</code> polls every <strong>1 second</strong> via <code>useQuery</code>, "
        "checks <code>dayjs().isBetween(start, end)</code> &mdash; ±2s timing precision</li>"
        "<li><code>pausePlayData</code> is a <strong>single variable</strong> &mdash; nested guaranteed interrupts lose the original paused creative "
        "(SMIL standard uses a pause <em>queue/stack</em> for this)</li>"
        "<li>Guaranteed spot media missing &rarr; <strong>silent failure</strong>: interrupted creative stays paused indefinitely, no recovery</li>"
        "<li>Multiple overlapping guaranteed spots &rarr; <code>find()</code> picks first match, no priority logic between them</li>"
        "<li>2 separate paths create guaranteed PlaySchedules (approval push + loop injection) &mdash; duplicated logic</li>"
        "<li>Retry queue (max 3 attempts), spot rotation tracking, daypart gate</li>"
        "<li>Player complexity: <strong>3,500+ lines</strong> scheduling logic in <code>src/components/screen/device/schedule/</code></li>"
        "</ul>"
        "<p><strong>Offline Handling (Current)</strong></p>"
        "<ul>"
        "<li>Detect offline: <code>fetch</code> error where <code>err?.message === 'Load failed'</code></li>"
        "<li>Play from <code>localStorage</code> cache (schedules + playlists)</li>"
        "<li>No graceful fallback: fresh boot + no internet = <strong>black screen</strong></li>"
        "<li>No checksum validation on downloaded creative assets</li>"
        "<li>Guaranteed spot approved while offline &rarr; Pusher push lost, no buffer mechanism</li>"
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
    sections.append("<h2>2. Current Architecture</h2>")
    sections.append("<h3>2.1 Backend (tathep-platform-api)</h3>")

    sections.append(mermaid_diagram(
        load_diagram("03-1-backend-pipeline.mmd"),
        page_id=page_id,
    ))

    sections.append(
        '<table>'
        '<tr><th>Component</th><th>File</th><th>Purpose</th></tr>'
        '<tr><td>PlaySchedule model</td><td><code>app/Models/PlaySchedule.ts</code></td><td>Status: WAITING&rarr;PLAYING&rarr;PLAYED, Types: guaranteed/ROS/spot-rotation</td></tr>'
        '<tr><td>Screen model</td><td><code>app/Models/Billboard.ts</code></td><td>ownerTime/platformTime = SOV (Share of Voice) budget (seconds/hour)</td></tr>'
        '<tr><td>Scheduling Engine</td><td><code>app/Jobs/PlayScheduleCalculate.ts</code></td><td>Enqueue per-screen jobs every N minutes</td></tr>'
        '<tr><td>Per-screen calc</td><td><code>app/Jobs/PlayScheduleCalculatePerScreen.ts</code></td><td>Generate PlaySchedule rows for 1 screen</td></tr>'
        '<tr><td>Player-pull mode</td><td><code>app/Jobs/PlayScheduleRoundCreate.ts</code></td><td>POST /v2/play-schedules/request {amount: N}</td></tr>'
        '<tr><td>House content rotation</td><td><code>app/Services/PlayScheduleFrequencyService.ts</code></td><td>House (owner) creative rotation + random jitter</td></tr>'
        '<tr><td>Campaign period</td><td><code>app/Services/PlaySchedulePeriodService.ts</code></td><td>Direct-sold campaigns: PER_HOUR/PER_DAY/custom avails</td></tr>'
        '<tr><td>Guaranteed service</td><td><code>app/Services/v2/PlayScheduleExclusiveService.ts</code></td><td>Loop-based: inject guaranteed spots overlapping current loop window</td></tr>'
        '<tr><td>Guaranteed job</td><td><code>app/Jobs/PlayScheduleCreateByExclusive.ts</code></td><td>On-demand: BullMQ job triggered on owner approval &rarr; create PlaySchedule + Pusher push</td></tr>'
        '<tr><td>Guaranteed model</td><td><code>app/Models/AdvertisementDisplayExclusive.ts</code></td><td>Avail reservation per screen (startDateTime/endDateTime/timePerSlot)</td></tr>'
        '<tr><td>Guaranteed time window</td><td><code>app/Models/AdGroupDisplayTimeExclusive.ts</code></td><td>AdGroup-level guaranteed window (start/end/duration) for loop injection</td></tr>'
        '<tr><td>Reservation check</td><td><code>app/Services/ServiceHelpers/checkIsBillboardsReserved.ts</code></td><td>Prevent double-booking: validate time overlap before creating guaranteed avails</td></tr>'
        '<tr><td>Pusher service</td><td><code>app/Services/PusherPlayScheduleService.ts</code></td><td>Channel: play-schedule-{deviceCode}</td></tr>'
        '</table>'
    )

    sections.append("<h3>2.2 Player (bd-vision-player)</h3>")
    sections.append(mermaid_diagram(
        load_diagram("03-2-player-architecture.mmd"),
        page_id=page_id,
    ))

    sections.append(
        '<table>'
        '<tr><th>Feature</th><th>Implementation</th><th>File</th></tr>'
        '<tr><td>Schedule types</td><td><code>exclusive</code> (guaranteed spot), <code>continuous</code> (direct-sold ROS), <code>frequency</code> (spot rotation)</td><td><code>src/constants/schedule.constant.ts</code></td></tr>'
        '<tr><td>Loop rotation</td><td><code>(currentIndex + 1) % activeSchedules.length</code></td><td><code>screen.device.schedule.play.timeslot.component.tsx</code></td></tr>'
        '<tr><td>Guaranteed preempt</td><td><code>calculatePlaySchedules</code> (1s <code>useQuery</code> interval): '
        '<code>dayjs().isBetween(start, end)</code> &rarr; <code>setPausePlayData(current)</code> &rarr; play guaranteed spot &rarr; '
        'on finish: restore <code>pausePlayData</code>. Single variable = no nested interrupt support</td>'
        '<td><code>screen.device.schedule.play.component.tsx</code></td></tr>'
        '<tr><td>Retry queue</td><td>Max 3 attempts, stored in localStorage</td><td><code>screen.device.schedule.play.timeslot.component.tsx</code></td></tr>'
        '<tr><td>Media download</td><td>Tauri <code>plugin-upload</code> (native HTTP), sequential</td><td><code>screen.device.schedule.setup.schedule-download.tsx</code></td></tr>'
        '<tr><td>File cleanup</td><td>Every 24h during off-hours, LRU-based</td><td><code>src/services/file-cleanup.service.ts</code></td></tr>'
        '<tr><td>Offline detect</td><td><code>err?.message === "Load failed"</code></td><td><code>screen.device.schedule.component.tsx</code></td></tr>'
        '<tr><td>PoP (Proof of Play) retry</td><td>Tauri Store (<code>player.history.json</code>), batch 10, every 1 min</td><td><code>player-history.store.ts</code></td></tr>'
        '</table>'
    )

    sections.append("<h3>2.3 Pusher Events</h3>")
    sections.append(
        '<table>'
        '<tr><th>Event</th><th>Trigger</th><th>Player Action</th></tr>'
        '<tr><td><code>update-play-schedule</code></td><td>Scheduling engine loop complete</td><td>Re-fetch <code>GET /v2/play-schedules</code></td></tr>'
        '<tr><td><code>created-play-schedule</code></td><td>Player-pull job complete</td><td>Re-fetch schedules</td></tr>'
        '<tr><td><code>approved-advertisement-exclusive</code></td><td>Guaranteed spot approved</td><td>Inject immediately (no re-fetch)</td></tr>'
        '<tr><td><code>stop-advertisement</code></td><td>Creative cancelled</td><td>Remove from local schedule</td></tr>'
        '<tr><td><code>new/update/delete-play-schedule</code></td><td>Schedule CRUD</td><td>Re-fetch schedules</td></tr>'
        '<tr><td><code>un-pair-screen</code></td><td>Device unpaired</td><td>Clear all, back to pair screen</td></tr>'
        '</table>'
    )

    return "\n".join(sections)


def build_page_2(page_id: str) -> str:
    """Page 2: Proposed Architecture (3 mermaid — overview + daily schedule + proposed flow)."""
    global _code_block_count
    _code_block_count = 0
    sections = []

    sections.append(toc())

    # Architecture overview diagram (moved from Executive Summary)
    sections.append("<h2>Architecture Overview</h2>")
    sections.append(mermaid_diagram(
        load_diagram("01-proposed-architecture.mmd"),
        page_id=page_id,
    ))

    sections.append("<h3>Daily Schedule Example</h3>")
    sections.append(info_panel(
        "<p>ตัวอย่าง billboard 1 จอ ตลอดวัน — แสดงสัดส่วนเวลาจริงระหว่าง priority levels ต่างๆ. "
        "<strong>P1-TK</strong> (แดง) กินเวลา 1 ชั่วโมงเต็ม, <strong>P1-ET</strong> (แดง) เป็น pin-point ตรงเวลา, "
        "<strong>P1-G</strong> (ฟ้า) กระจายตลอดวัน, <strong>P2-P4</strong> เติมช่วงที่เหลือ</p>"
    ))
    sections.append(mermaid_diagram(
        load_diagram("01-2-daily-schedule.mmd"),
        page_id=page_id,
    ))

    sections.append("<hr/>")
    sections.append("<h2>Proposed Architecture: Backend-Driven Player</h2>")
    sections.append(info_panel(
        "<p><strong>Core Idea:</strong> Backend sends <strong>ordered screen schedule (loop sequence)</strong> instead of a bag of creatives + rules. "
        "Player just plays <code>sequence[i++]</code> (Dumb Renderer pattern &mdash; standard in DOOH).</p>"
    ))

    sections.append("<h3>What Changes vs What Stays</h3>")
    sections.append(
        '<table>'
        '<tr><th>Component</th><th>Current</th><th>Proposed</th><th>Change Type</th></tr>'
        '<tr><td>Cron job</td><td>PlayScheduleCalculate every 10 min</td><td>Same</td><td>' + status_macro("NO CHANGE", "Green") + '</td></tr>'
        '<tr><td>Per-screen job</td><td>Create PlaySchedule rows</td><td>Create PlaySchedule + <strong>ordered ScreenSchedule</strong></td><td>' + status_macro("ADD STEP", "Yellow") + '</td></tr>'
        '<tr><td>Pusher</td><td>Channel per device</td><td>Same channel + new event <code>schedule-updated</code></td><td>' + status_macro("ADD EVENT", "Yellow") + '</td></tr>'
        '<tr><td>Player API</td><td>GET /v2/play-schedules + /playlist-advertisements</td><td><strong>GET /v2/screen-schedule</strong> (unified)</td><td>' + status_macro("NEW ENDPOINT", "Blue") + '</td></tr>'
        '<tr><td>Player scheduling</td><td>Loop rotation + guaranteed interrupt (complex)</td><td><strong>play sequence[i++]</strong> (Dumb Renderer)</td><td>' + status_macro("SIMPLIFY", "Green") + '</td></tr>'
        '<tr><td>Player storage</td><td>localStorage (separate schedules + playlists)</td><td>Tauri Store (3-tier playlist)</td><td>' + status_macro("MIGRATE", "Yellow") + '</td></tr>'
        '<tr><td>Media download</td><td>Tauri plugin-upload</td><td>Same</td><td>' + status_macro("NO CHANGE", "Green") + '</td></tr>'
        '<tr><td>BullMQ</td><td>Redis queue</td><td>Same</td><td>' + status_macro("NO CHANGE", "Green") + '</td></tr>'
        '<tr><td>Auth</td><td>x-device-code header</td><td>Same</td><td>' + status_macro("NO CHANGE", "Green") + '</td></tr>'
        '<tr><td>Proof of Play (PoP)</td><td>POST /v2/play-history + retry</td><td>Same + <strong>Outbox pattern</strong> + interrupt fields</td><td>' + status_macro("ENHANCE", "Yellow") + '</td></tr>'
        '<tr><td><strong>Interrupt Controller</strong></td><td>N/A</td><td><strong>NEW:</strong> Lightweight IC for P0/P1-TK/P1-ET only. P2-P4 wait for creative to finish</td><td>' + status_macro("NEW", "Blue") + '</td></tr>'
        '<tr><td><strong>TK Booking API</strong></td><td>N/A</td><td><strong>NEW:</strong> Daypart Takeover booking + overlap validation + lead time check</td><td>' + status_macro("NEW", "Blue") + '</td></tr>'
        '<tr><td><strong>Make-Good System</strong></td><td>N/A</td><td><strong>NEW:</strong> Interrupted ads get compensation slot in next cycle</td><td>' + status_macro("NEW", "Blue") + '</td></tr>'
        '</table>'
    )

    sections.append("<h3>Infrastructure Mapping</h3>")
    sections.append(
        '<table>'
        '<tr><th>Existing Infrastructure</th><th>Role Today</th><th>Role in Proposed</th><th>Change</th></tr>'
        '<tr><td><strong>BullMQ + Redis</strong></td><td>Cron job queue (PlayScheduleCalculate)</td><td>Same + enqueue Ad Decisioning Engine after schedule calc</td><td>' + status_macro("REUSE", "Green") + '</td></tr>'
        '<tr><td><strong>MySQL</strong></td><td>PlaySchedule, Billboard, Advertisement models</td><td>Same + NEW ScreenSchedule, ScreenScheduleItem tables</td><td>' + status_macro("ADD TABLES", "Yellow") + '</td></tr>'
        '<tr><td><strong>Redis (cache)</strong></td><td>GET/SET string cache (Bentocache)</td><td>Same + idempotency keys (SET with TTL 24h)</td><td>' + status_macro("REUSE", "Green") + '</td></tr>'
        '<tr><td><strong>Pusher (WebSocket)</strong></td><td>6 event types, channel per device</td><td>Same channel + 5 new typed events (schedule-updated, device-config-updated, takeover-start, takeover-end, p0-emergency)</td><td>' + status_macro("ADD EVENTS", "Yellow") + '</td></tr>'
        '<tr><td><strong>AdonisJS routes</strong></td><td>Player V2 routes (/play-schedules, /playlist-advertisements)</td><td>Keep existing + add GET /v2/screen-schedule</td><td>' + status_macro("ADD ENDPOINT", "Yellow") + '</td></tr>'
        '<tr><td><strong>Tauri plugin-upload</strong></td><td>Native HTTP media download</td><td>Same (sequential download with resume)</td><td>' + status_macro("NO CHANGE", "Green") + '</td></tr>'
        '<tr><td><strong>localStorage</strong></td><td>Schedules, playlists, playData</td><td>Migrate heavy data to Tauri Store; localStorage for small state only</td><td>' + status_macro("MIGRATE", "Yellow") + '</td></tr>'
        '<tr><td><strong>Tauri Store</strong></td><td>player.history.json (play history retry)</td><td>+ outbox.json, playlist-cache.json, inbox-state.json</td><td>' + status_macro("EXPAND", "Yellow") + '</td></tr>'
        '<tr><td><strong>Pusher client (player)</strong></td><td>Subscribe, re-fetch on event</td><td>Same + inbox dedup layer (event_id + version check)</td><td>' + status_macro("WRAP", "Yellow") + '</td></tr>'
        '<tr><td><strong>x-device-code auth</strong></td><td>Player auth header</td><td>Same</td><td>' + status_macro("NO CHANGE", "Green") + '</td></tr>'
        '</table>'
    )

    return "\n".join(sections)


def build_page_3(page_id: str) -> str:
    """Page 3: Key Flows (6 mermaid, 0 code blocks)."""
    global _code_block_count
    _code_block_count = 0
    sections = []

    sections.append(toc())
    sections.append("<h2>Key Flows</h2>")

    sections.append("<h3>Flow A: Normal Online Play (Happy Path)</h3>")
    sections.append(mermaid_diagram(
        load_diagram("05-1-flow-normal.mmd"),
        page_id=page_id,
    ))

    sections.append("<h3>Flow B: Network Drop &rarr; Offline &rarr; Reconnect</h3>")
    sections.append(mermaid_diagram(
        load_diagram("05-2-flow-network-drop.mmd"),
        page_id=page_id,
    ))

    sections.append("<h3>Flow C: Guaranteed Spot Interrupt (Online)</h3>")
    sections.append(warning_panel(
        "<p><strong>Current system has 2 paths for guaranteed spots (เดิมเรียก exclusive):</strong></p>"
        "<ul>"
        "<li><strong>Path 1 (On approval):</strong> Owner approves &rarr; BullMQ <code>PlayScheduleCreateByExclusive</code> job &rarr; "
        "creates PlaySchedule rows (type=EXCLUSIVE, createdBy=EXCLUSIVE_APPROVED) &rarr; "
        "Pusher <code>approved-advertisement-exclusive</code> with full payload &rarr; Player injects immediately</li>"
        "<li><strong>Path 2 (During loop):</strong> <code>PlayScheduleExclusiveService</code> checks <code>AdGroupDisplayTimeExclusive</code> "
        "overlapping current loop window &rarr; creates PlaySchedule rows (createdBy=PLAYER_REQUEST)</li>"
        "</ul>"
        "<p><strong>Proposed simplification:</strong> Ad Decisioning Engine handles both paths &mdash; "
        "guaranteed spots are pre-injected into the ordered sequence at their exact <code>play_at</code> position. "
        "Player no longer needs guaranteed interrupt logic.</p>"
    ))
    sections.append(mermaid_diagram(
        load_diagram("05-3-flow-exclusive.mmd"),
        page_id=page_id,
    ))

    sections.append("<h3>Flow D: Fresh Boot (No Cache)</h3>")
    sections.append(mermaid_diagram(
        load_diagram("05-4-flow-fresh-boot.mmd"),
        page_id=page_id,
    ))

    sections.append("<h3>Flow E: Daypart Takeover</h3>")
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

    sections.append("<h3>Flow F: Exact-Time Spot</h3>")
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
    sections.append("<h2>Technical Design: Algorithm &amp; Models</h2>")

    # Ad Decisioning Algorithm
    sections.append("<h3>Ad Decisioning Algorithm</h3>")
    sections.append(note_panel(
        "<p><strong>Key insight:</strong> Ad Decisioning Engine runs <em>after</em> existing PlayScheduleCalculatePerScreen. "
        "It takes the PlaySchedule rows (already calculated) and converts them into an <strong>ordered loop sequence</strong>.</p>"
        "<p><strong>Guaranteed spots (เดิมเรียก exclusive):</strong> Currently handled by 2 separate paths "
        "(<code>PlayScheduleCreateByExclusive</code> on approval + <code>PlayScheduleExclusiveService</code> during loops). "
        "Ad Decisioning Engine <strong>unifies both</strong> &mdash; guaranteed spots are injected at their exact <code>play_at</code> "
        "position in the sequence. Reservation check (<code>checkIsBillboardsReserved</code>) prevents double-booking. "
        "Billing uses <code>exclusiveMultiplier</code> (env: <code>ADVERTISEMENT_EXCLUSIVE_MULTIPLIER</code>).</p>"
    ))
    sections.append(
        '<table>'
        '<tr><th>Priority</th><th>DOOH Type</th><th>Interrupt?</th><th>Scheduling</th><th>Billing</th></tr>'
        '<tr><td><strong>P0</strong></td><td>Emergency</td><td>' + status_macro("YES — all", "Red") + '</td><td>System alerts, unpair, maintenance</td><td>N/A</td></tr>'
        '<tr><td><strong>P1-TK</strong></td><td>Daypart Takeover</td><td>' + status_macro("YES — boundaries", "Red") + '</td><td>เหมา time block วน ad เดียว (TK_START → loop → TK_END)</td><td>CPT (flat/time block)</td></tr>'
        '<tr><td><strong>P1-ET</strong></td><td>Exact-Time Spot</td><td>' + status_macro("YES — P2-P4", "Red") + '</td><td>เล่นตรงเวลา ±5s tolerance</td><td>Flat per spot</td></tr>'
        '<tr><td><strong>P1-G</strong></td><td>Guaranteed Spot</td><td>' + status_macro("NO — pre-positioned", "Green") + '</td><td>Time-reserved guaranteed spots (<code>play_at</code> exact position in sequence)</td><td><code>exclusiveMultiplier</code></td></tr>'
        '<tr><td><strong>P2</strong></td><td>Direct-Sold ROS</td><td>' + status_macro("NO", "Green") + '</td><td>Date-range campaign creatives (run-of-schedule)</td><td>Standard rate</td></tr>'
        '<tr><td><strong>P3</strong></td><td>Spot Buy / Programmatic</td><td>' + status_macro("NO", "Green") + '</td><td>Impression-target creatives (future: RTB via SSP)</td><td>Standard / CPM</td></tr>'
        '<tr><td><strong>P4</strong></td><td>House / Filler</td><td>' + status_macro("NO", "Green") + '</td><td>Screen owner default content (house loop)</td><td>N/A</td></tr>'
        '</table>'
    )
    sections.append(note_panel(
        "<p><strong>Interrupt Rules:</strong></p>"
        "<ul>"
        "<li><strong>P0/P1-TK/P1-ET:</strong> Interrupt current creative ทันที → <strong>stop</strong> (ไม่ pause/resume) "
        '— แนวคิดจาก <a href="https://xibosignage.com/manual/en/layouts_interrupt">Xibo Interrupt Layout</a></li>'
        "<li><strong>P1-G/P2/P3/P4:</strong> รอ creative ปัจจุบันจบก่อน (no interrupt)</li>"
        "<li>After interrupt: resume จาก <strong>next item</strong> ใน schedule (ไม่ restart creative ที่โดน interrupt)</li>"
        "<li>Interrupted ad ได้ <strong>make-good</strong> compensation ใน cycle ถัดไป (partial play ไม่นับ impression)</li>"
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
    sections.append("<h3>New Data Models</h3>")
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
    sections.append("<h3>New API Endpoint</h3>")
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
    sections.append("<h3>3-Tier Playlist Cache</h3>")
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
        "<p><strong>Rules:</strong></p>"
        "<ul>"
        "<li>Every state MUST have something to display. <strong>Black screen is NEVER acceptable.</strong></li>"
        "<li><strong>INTERRUPTED</strong> is a transient state — stop current → play interrupt content → resume next item. "
        "Triggers: P0 emergency, P1-TK boundary, P1-ET ±5s. ดู §6.10 Interrupt Controller</li>"
        "</ul>"
    ))

    # PoP Reporting (Outbox/Inbox)
    sections.append("<h3>PoP Reporting (Outbox/Inbox)</h3>")
    sections.append(error_panel(
        "<p><strong>ปัญหา 1 (Player &rarr; Backend): Duplicate PoP (Proof of Play)</strong><br/>"
        "Player POST <code>/v2/play-history</code> &rarr; timeout &rarr; retry &rarr; backend ได้ 2 รายการ สำหรับ creative เดียวกัน</p>"
        "<p><strong>ปัญหา 2 (Backend &rarr; Player): Missed Pusher Events</strong><br/>"
        "Pusher disconnect 30 วิ &rarr; reconnect &rarr; events ระหว่างนั้นหายไป &rarr; Player ไม่รู้ว่ามี schedule ใหม่</p>"
        "<p><strong>ปัญหา 3 (Backend &rarr; Player): Duplicate Pusher Events</strong><br/>"
        "Pusher ส่ง event ซ้ำ (at-least-once) &rarr; player process ซ้ำ &rarr; fetch ซ้ำ &rarr; เสีย bandwidth</p>"
    ))
    sections.append(info_panel(
        "<p><strong>Solution:</strong> Outbox (Player&rarr;Backend) + Inbox (Backend&rarr;Player)</p>"
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
        "// 5. retry_count > 10 → mark 'failed', log diagnostic\n"
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
    sections.append("<h3>PoP Deduplication (Backend Idempotency)</h3>")
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
    sections.append("<h3>Programmatic Integration Points (pDOOH Roadmap)</h3>")
    sections.append(info_panel(
        "<p><strong>Scale 100-500 screens:</strong> ยังไม่ต้อง SSP/DSP เต็มรูปแบบ แต่วาง integration points ไว้ "
        "เพื่อให้ pluggable เมื่อ scale ถึง. ไม่เพิ่ม tech stack ใหม่ &mdash; ใช้ AdonisJS + Redis + BullMQ เดิม.</p>"
    ))
    sections.append(mermaid_diagram(
        load_diagram("06-9-pdooh-integration.mmd"),
        page_id=page_id,
    ))
    sections.append(
        '<table>'
        '<tr><th>Integration Point</th><th>Current</th><th>pDOOH Extension (Future)</th></tr>'
        '<tr><td><strong>P3 slot fill</strong></td><td>Internal spot rotation (count-based)</td><td>SSP ad request &rarr; RTB auction &rarr; winning creative or fallback</td></tr>'
        '<tr><td><strong>PoP reporting</strong></td><td>POST /v2/play-history</td><td>Add: <code>impression_id</code>, <code>campaign_id</code>, <code>creative_id</code>, <code>viewability_score</code></td></tr>'
        '<tr><td><strong>Inventory avails</strong></td><td>N/A</td><td><code>GET /v2/avails?screen_id=X&amp;daypart=Y</code> &mdash; expose available slots to SSP</td></tr>'
        '<tr><td><strong>Campaign pacing</strong></td><td>BEP-2998 fix (basic proportional)</td><td>Even distribution across flight + SOV-based allocation</td></tr>'
        '<tr><td><strong>Fill rate tracking</strong></td><td>N/A</td><td>% of P3 avails filled programmatic vs house content</td></tr>'
        '<tr><td><strong>Audience estimation</strong></td><td>N/A</td><td>Pass <code>audience_est</code> (foot traffic / time-of-day) in ad request</td></tr>'
        '</table>'
    )

    return "\n".join(sections)


def build_page_6(page_id: str) -> str:
    """Page 6: Interrupt Controller & Make-Good (2 mermaid, 0 code blocks)."""
    global _code_block_count
    _code_block_count = 0
    sections = []

    sections.append(toc())
    sections.append("<h2>Interrupt Controller &amp; Make-Good</h2>")

    # Interrupt Controller
    sections.append("<h3>Interrupt Controller</h3>")
    sections.append(warning_panel(
        "<p><strong>Design decision: Selective Interrupt.</strong> "
        "Player ยังเป็น Dumb Renderer สำหรับ P1-G/P2/P3/P4 (รอ creative จบก่อน). "
        "แต่มี <strong>lightweight Interrupt Controller (IC)</strong> สำหรับ P0/P1-TK/P1-ET เท่านั้น.</p>"
        "<p><strong>Industry reference:</strong></p>"
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
        '<td>Stop immediately → play emergency creative</td>'
        '<td>Resume next item after emergency duration. TK time lost (log for manual billing)</td></tr>'
        '<tr><td><strong>P1-TK Start</strong><br/>(Pusher: takeover-start OR local clock)</td>'
        '<td>Stop current → switch to TK creative → loop until TK_END</td>'
        '<td>TK_END → resume next item in normal schedule + make-good for interrupted ad</td></tr>'
        '<tr><td><strong>P1-ET Trigger</strong><br/>(local clock ±5s)</td>'
        '<td>Stop current P2-P4 → play ET spot (single play)</td>'
        '<td>ET done → resume next item + make-good for interrupted ad</td></tr>'
        '</table>'
    )

    # Make-Good System
    sections.append("<h3>Make-Good System</h3>")
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
    sections.append("<h2>Event-Driven Architecture</h2>")
    sections.append(info_panel(
        "<p><strong>Decision:</strong> Formalize existing event-driven patterns (Pusher + BullMQ) with typed contracts, "
        "domain events, and clear ownership. <strong>NOT</strong> Event-Sourcing &mdash; scale + team doesn't justify the complexity.</p>"
    ))

    sections.append("<h3>What We Already Have (De Facto Event-Driven)</h3>")

    sections.append(
        '<table>'
        '<tr><th>Component</th><th>Pattern</th><th>Status</th></tr>'
        '<tr><td>BullMQ cron &rarr; per-screen jobs</td><td>Job queue as event bus</td><td>' + status_macro("EXISTS", "Green") + '</td></tr>'
        '<tr><td>Pusher events &rarr; Player</td><td>Real-time event delivery</td><td>' + status_macro("EXISTS", "Green") + '</td></tr>'
        '<tr><td>PoP retry queue</td><td>Outbox-like (player.history.json)</td><td>' + status_macro("EXISTS", "Green") + '</td></tr>'
        '<tr><td>Typed event contracts</td><td>Explicit interface per event</td><td>' + status_macro("MISSING", "Red") + '</td></tr>'
        '<tr><td>Domain events in code</td><td>Named events for traceability</td><td>' + status_macro("MISSING", "Red") + '</td></tr>'
        '<tr><td>Idempotency keys</td><td>Dedup on retry</td><td>' + status_macro("MISSING", "Red") + '</td></tr>'
        '<tr><td>Version protocol</td><td>Monotonic version per device</td><td>' + status_macro("MISSING", "Red") + '</td></tr>'
        '</table>'
    )

    sections.append("<h3>Typed Pusher Event Contracts</h3>")
    sections.append(note_panel(
        "<p><strong>Goal:</strong> Every Pusher event has a TypeScript interface shared between backend and player. "
        "No more <code>any</code> types or implicit contracts.</p>"
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
        "  | ApprovedExclusiveEvent\n"
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

    sections.append("<h3>Domain Events (Internal Code-Level)</h3>")
    sections.append(note_panel(
        "<p><strong>Goal:</strong> Named domain events inside backend code for traceability. "
        "NOT persisted as event-sourcing log &mdash; just typed objects passed between services.</p>"
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

    sections.append("<h3>Event Flow Diagram</h3>")
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
    sections.append("<h2>Edge Cases &amp; Resilience</h2>")

    sections.append("<h3>Network Issues</h3>")
    sections.append(
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
        '<td>เดิมมีอยู่แล้ว: <code>fileCleanupService.markDownloading()</code> ป้องกัน cleanup. เพิ่ม: <strong>checksum validation</strong> &mdash; backend ส่ง <code>media.checksum</code> &rarr; สน + re-download</td></tr>'
        '<tr><td>E6</td><td><strong>SSL certificate expired / DNS failure</strong></td>'
        '<td>fetch fail แต่ internet ยังใช้ได้</td>'
        '<td>Treat เหมือน offline. Player มี Tier 2/3 รองรับ. เพิ่ม <strong>diagnostic log</strong> แยก SSL error จาก network error</td></tr>'
        '</table>'
    )

    sections.append("<h3>Schedule/Playlist Issues</h3>")
    sections.append(
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
    )

    sections.append("<h3>Device/Storage Issues</h3>")
    sections.append(
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
        '<td>Tauri บน Windows/macOS/Linux มี RTC ที่แม่นยำกว่า RPi. เก็บ <code>last_ntp_sync</code> timestamp. ถ้า drift &gt; 1 ชม. &rarr; log warning แต่ยังเล่น play (better than black screen). <strong>Exclusive</strong> tradeoff</td></tr>'
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
    )

    sections.append("<h3>Business Logic Issues</h3>")
    sections.append(
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
    )

    sections.append("<h3>Guaranteed Spot Edge Cases (P1-G — No Interrupt)</h3>")
    sections.append(warning_panel(
        "<p><strong>Edge cases specific to P1-G guaranteed spots</strong> (เดิมเรียก exclusive). "
        "P1-G ยังคง <strong>ไม่ interrupt</strong> — pre-positioned ใน sequence โดย Ad Decisioning Engine. "
        "สำหรับ edge cases ของ P1-TK (Takeover) และ P1-ET (Exact-Time) ที่มี interrupt ดู §8.6</p>"
    ))
    sections.append(
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
    )

    sections.append("<h4>Combined Flow Edge Cases (Regular + Exclusive)</h4>")
    sections.append(
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
    )

    sections.append("<h3>Takeover &amp; Exact-Time Edge Cases (P1-TK / P1-ET)</h3>")
    sections.append(mermaid_diagram(
        load_diagram("08-2-takeover-timeline.mmd"),
        page_id=page_id,
    ))
    sections.append("<h4>Takeover Interrupt Timeline (Gantt View)</h4>")
    sections.append(info_panel(
        "<p>มุมมองเวลาจริง — เห็นสัดส่วนว่า <strong>TK block 60 นาที</strong> กว้างกว่า normal schedule มาก. "
        "<strong>Milestone</strong> = TK_START / TK_END boundary. "
        "<strong>Make-good</strong> (ฟ้า) เล่นชดเชย Ad A ที่โดน interrupt ทันทีหลัง TK จบ</p>"
    ))
    sections.append(mermaid_diagram(
        load_diagram("08-3-takeover-gantt.mmd"),
        page_id=page_id,
    ))
    sections.append(
        '<table>'
        '<tr><th>#</th><th>Edge Case</th><th>Solution</th></tr>'
        '<tr><td>TK1</td><td><strong>Overlapping TK booking</strong> &mdash; 2 owners want same time block</td>'
        '<td>Reject at booking time — <code>checkIsBillboardsReserved</code> extended for TK. 1 time block = 1 owner only</td></tr>'
        '<tr><td>TK2</td><td><strong>TK creative not cached at TK_START</strong></td>'
        '<td>Skip TK → resume normal schedule → alert admin. Pre-stage creative via <code>device-config-updated</code> event at booking time</td></tr>'
        '<tr><td>TK3</td><td><strong>P0 Emergency during TK</strong></td>'
        '<td>P0 wins (always highest priority). TK time lost during emergency — log for manual billing reconciliation</td></tr>'
        '<tr><td>TK4</td><td><strong>Player offline at TK_START</strong></td>'
        '<td>Local clock fallback: TK schedule pre-staged in Tier 2 with <code>takeover_id</code>. IC checks local clock against pending TK boundaries</td></tr>'
        '<tr><td>TK5</td><td><strong>TK booking &lt; lead time</strong></td>'
        '<td>Reject — same lead time constraint as guaranteed spots (existing exclusive validation)</td></tr>'
        '<tr><td>TK6</td><td><strong>TK creative changes after booking</strong></td>'
        '<td>Re-push <code>device-config-updated</code> with new <code>creative_code</code>. Player re-downloads before TK_START</td></tr>'
        '<tr><td>TK7</td><td><strong>Multiple ET spots at same second</strong></td>'
        '<td>FIFO by <code>created_at</code> — first wins, second gets <code>+duration</code> offset (sequential, not parallel)</td></tr>'
        '<tr><td>TK8</td><td><strong>Make-good creative expired</strong></td>'
        '<td>Skip compensation — log for manual reconcile. Campaign <code>valid_until</code> check prevents playing expired ads</td></tr>'
        '</table>'
    )

    sections.append("<hr/>")
    sections.append("<h2>Migration Plan (Incremental)</h2>")
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
    sections.append("<h2>Appendix</h2>")

    sections.append("<h3>Industry Reference</h3>")

    sections.append("<h4>Priority Scheduling Standards (SMIL + DOOH)</h4>")
    sections.append(info_panel(
        "<p>Our proposed <strong>5-level priority model (P0-P4)</strong> is inspired by these industry standards. "
        "The key insight: exclusive/priority scheduling is a <em>solved problem</em> in digital signage &mdash; "
        "we adapt proven patterns rather than inventing from scratch.</p>"
    ))
    sections.append(
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
    )

    sections.append("<h4>Our Architecture vs DOOH Standard</h4>")
    sections.append(
        '<table>'
        '<tr><th>DOOH Concept</th><th>Our Implementation</th><th>Gap</th></tr>'
        '<tr><td><strong>Ad Server</strong></td><td>Ad Decisioning Engine within Backend (AdonisJS)</td><td>Not separated &mdash; OK for 100-500 screens</td></tr>'
        '<tr><td><strong>CMS</strong></td><td>Admin panel + owner dashboard</td><td>Standard</td></tr>'
        '<tr><td><strong>SSP (Supply-Side Platform)</strong></td><td>Not yet &mdash; P3 = future SSP avail</td><td>Phase 6 roadmap</td></tr>'
        '<tr><td><strong>Impression tracking</strong></td><td>PoP via Outbox pattern</td><td>Add IAB fields (Phase 6)</td></tr>'
        '<tr><td><strong>Campaign pacing</strong></td><td>BEP-2998 fix + Ad Decisioning Engine</td><td>Basic &mdash; enhance in Phase 6</td></tr>'
        '<tr><td><strong>SOV allocation</strong></td><td>ownerTime/platformTime ratio</td><td>Renamed to SOV, same logic</td></tr>'
        '<tr><td><strong>Guaranteed delivery</strong></td><td>P1-G guaranteed spots with reservation check (no interrupt)</td><td>Standard</td></tr>'
        '<tr><td><strong>Daypart Takeover</strong></td><td>P1-TK time block reservation + Interrupt Controller</td><td>Implemented (Phase 3.5)</td></tr>'
        '<tr><td><strong>Exact-Time Spot</strong></td><td>P1-ET ±5s tolerance + IC trigger</td><td>Implemented (Phase 3.5)</td></tr>'
        '<tr><td><strong>Make-Good</strong></td><td>MakeGoodRecord: interrupted → compensate next cycle</td><td>Implemented (Phase 3.5)</td></tr>'
        '<tr><td><strong>Interrupt handling</strong></td><td>Selective: P0/P1-TK/P1-ET interrupt, P2-P4 wait</td><td>Standard (Broadsign-style configurable)</td></tr>'
        '<tr><td><strong>Creative management</strong></td><td>Media upload + CDN + checksum validation</td><td>Standard</td></tr>'
        '<tr><td><strong>Offline resilience</strong></td><td>3-Tier cache (Live/Buffer/Fallback)</td><td>Standard (comparable to Xibo/BrightSign)</td></tr>'
        '<tr><td><strong>Loop scheduling</strong></td><td>10-min loop via Scheduling Engine (BullMQ)</td><td>Standard</td></tr>'
        '</table>'
    )

    sections.append("<h4>How Commercial Solutions Handle Offline</h4>")
    sections.append(
        '<table>'
        '<tr><th>Platform</th><th>Approach</th><th>Buffer</th></tr>'
        '<tr><td>Xibo</td><td>RequiredFiles manifest + MD5 per file + 50MB chunk download</td><td>48h ahead (configurable)</td></tr>'
        '<tr><td>piSignage</td><td>Default playlist fallback + local media folder + delta sync</td><td>Full campaign window</td></tr>'
        '<tr><td>BrightSign BSN.Cloud</td><td>Local-first: all media cached, network = sync only</td><td>Content-dependent</td></tr>'
        '<tr><td>info-beamer</td><td>3-state degradation (Online/Degraded/Offline) + RTC fallback</td><td>All scheduled content</td></tr>'
        '</table>'
    )

    sections.append("<h4>Open Source References</h4>")
    sections.append(
        '<table>'
        '<tr><th>Project</th><th>Repository</th><th>Relevant Pattern</th></tr>'
        '<tr><td>Xibo Player SDK</td><td><a href="https://github.com/xibo-players/xiboplayer">xibo-players/xiboplayer</a></td><td>Cache API + IndexedDB, XMR WebSocket, chunk downloads with MD5, 2-layout preload pool</td></tr>'
        '<tr><td>Xibo .NET Client</td><td><a href="https://github.com/xibosignage/xibo-dotnetclient">xibosignage/xibo-dotnetclient</a></td><td>ScheduleManager.cs: thread polling, priority resolution, disk-resident schedule, Splash fallback</td></tr>'
        '<tr><td>piSignage</td><td><a href="https://github.com/colloqi/piSignage">colloqi/piSignage</a></td><td>Node.js + WebSocket, default playlist fallback, local filesystem media</td></tr>'
        '<tr><td>Anthias (Screenly OSE)</td><td><a href="https://github.com/Screenly/Anthias">Screenly/Anthias</a></td><td>Docker microservices, Redis + SQLite, Celery queue, Qt viewer</td></tr>'
        '</table>'
    )

    sections.append("<h4>Protocol Recommendation</h4>")
    sections.append(note_panel(
        "<p><strong>Keep Pusher</strong> (existing) for real-time push. Add <strong>version-based checkpoint</strong> on reconnect via REST. "
        "Never depend on push for playback &mdash; it only triggers early sync.</p>"
        "<p><strong>Key insight (from RxDB):</strong> Client can miss events during disconnect. "
        "Solution: checkpoint mode on reconnect (full schedule compare via REST) + event mode once synced (Pusher for incremental).</p>"
    ))

    sections.append("<h3>Decision Record: Why NOT Event-Sourcing</h3>")
    sections.append(warning_panel(
        "<p><strong>ADR-002:</strong> Event-Driven Architecture (NOT Event-Sourcing)</p>"
    ))
    sections.append(
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
    )

    sections.append("<h3>Implementation Checklist</h3>")
    sections.append(success_panel(
        "<p><strong>What to formalize (ordered by priority):</strong></p>"
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
    print(f"  Updated: {t} (v{version} -> v{version + 1})")
    print(f"  URL: https://{{JIRA_SITE}}/wiki/spaces/{SPACE_KEY}/pages/{page_id}")


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
            print("Error: --section requires argument (parent, 1-8)")
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
        for sec in ["1", "2", "3", "4", "5", "6", "7", "8"]:
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
                print(f"Error: no page ID for section {section}. Run --create-all first.")
                sys.exit(1)
        content = builder(page_id=pid)
        print(f"=== Updating section {section} ===")
        _update_page(api, pid, content)
        return

    # ── Legacy: update specific page ──
    if update_page_id:
        content = build_parent_content(page_id=update_page_id)
        print(f"=== Updating page {update_page_id} ===")
        _update_page(api, update_page_id, content)
        return

    print("Usage:")
    print("  --dry-run [--section N]     Preview HTML output")
    print("  --create-all                Create/update parent + 8 sub-pages")
    print("  --section N                 Update single section (parent, 1-8)")
    print("  --update PAGE_ID            Legacy: update specific page")


if __name__ == "__main__":
    main()
