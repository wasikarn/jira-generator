#!/usr/bin/env python3
"""Create Confluence page: Backend-Driven Player Architecture — Design Proposal.

Creates under BEP space as a child of 'Player Doc' (page 81592324).
Idempotent: checks if page already exists by title.
"""

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


def code_block(code: str, language: str = "text", title: str = "") -> str:
    parts = [
        '<ac:structured-macro ac:name="code" ac:schema-version="1">',
        f'<ac:parameter ac:name="language">{language}</ac:parameter>',
    ]
    if title:
        parts.append(f'<ac:parameter ac:name="title">{title}</ac:parameter>')
    parts.append(f"<ac:plain-text-body><![CDATA[{code}]]></ac:plain-text-body>")
    parts.append("</ac:structured-macro>")
    return "".join(parts)


def tracked_code_block(code: str, language: str = "text", title: str = "") -> str:
    """code_block() with global counter for Forge index tracking."""
    global _code_block_count
    result = code_block(code, language, title)
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


def build_content(page_id: str = "165019751") -> str:
    global _code_block_count
    _code_block_count = 0
    sections = []

    # ToC
    sections.append(toc())

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

    # ─── Section 1: Problem Statement ───
    sections.append("<h2>1. Problem Statement</h2>")
    sections.append(error_panel(
        "<p><strong>Smart Player</strong></p>"
        "<ul>"
        "<li>Player round-robin ads locally (SchedulePlay, TimeSlot, Playlist components)</li>"
        "<li>Exclusive interrupt logic (preempt + resume <code>pausePlayData</code>)</li>"
        "<li>Retry queue (max 3 attempts), frequency count tracking, operating hours gate</li>"
        "<li>Player complexity: <strong>3,500+ lines</strong> scheduling logic in <code>src/components/screen/device/schedule/</code></li>"
        "</ul>"
        "<p><strong>Offline Handling (Current)</strong></p>"
        "<ul>"
        "<li>Detect offline: <code>fetch</code> error where <code>err?.message === 'Load failed'</code></li>"
        "<li>Play from <code>localStorage</code> cache (schedules + playlists)</li>"
        "<li>No graceful fallback: fresh boot + no internet = <strong>black screen</strong></li>"
        "<li>No checksum validation on downloaded media</li>"
        "</ul>"
    ))

    # ─── Section 2: Current Architecture ───
    sections.append("<h2>2. Current Architecture</h2>")
    sections.append("<h3>2.1 Backend (tathep-platform-api)</h3>")

    sections.append(mermaid_diagram(
        "flowchart TD\n"
        "    A[\"Cron (every 10 min)\"] --> B[\"PlayScheduleCalculate\\njob (BullMQ)\"]\n"
        "    B --> C[\"PlayScheduleCalculatePerScreen\\n(per billboard)\"]\n"
        "    C --> D[\"PlayScheduleFrequencyService\\n(owner ads)\"]\n"
        "    C --> E[\"PlaySchedulePeriodService\\n(paid customer ads)\"]\n"
        "    D & E --> F[\"Create PlaySchedule rows in DB\"]\n"
        "    F --> G[\"Pusher 'update-play-schedule'\\n→ Player\"]",
        page_id=page_id,
    ))

    sections.append(
        '<table>'
        '<tr><th>Component</th><th>File</th><th>Purpose</th></tr>'
        '<tr><td>PlaySchedule model</td><td><code>app/Models/PlaySchedule.ts</code></td><td>Status: WAITING&rarr;PLAYING&rarr;PLAYED, Types: exclusive/continuous/frequency</td></tr>'
        '<tr><td>Billboard model</td><td><code>app/Models/Billboard.ts</code></td><td>ownerTime/platformTime budget (seconds/hour)</td></tr>'
        '<tr><td>Cron orchestrator</td><td><code>app/Jobs/PlayScheduleCalculate.ts</code></td><td>Enqueue per-screen jobs every N minutes</td></tr>'
        '<tr><td>Per-screen calc</td><td><code>app/Jobs/PlayScheduleCalculatePerScreen.ts</code></td><td>Generate PlaySchedule rows for 1 billboard</td></tr>'
        '<tr><td>Player-pull mode</td><td><code>app/Jobs/PlayScheduleRoundCreate.ts</code></td><td>POST /v2/play-schedules/request {amount: N}</td></tr>'
        '<tr><td>Owner frequency</td><td><code>app/Services/PlayScheduleFrequencyService.ts</code></td><td>Owner ads rotation + random jitter</td></tr>'
        '<tr><td>Customer period</td><td><code>app/Services/PlaySchedulePeriodService.ts</code></td><td>Paid ads: PER_HOUR/PER_DAY/custom slots</td></tr>'
        '<tr><td>Pusher service</td><td><code>app/Services/PusherPlayScheduleService.ts</code></td><td>Channel: play-schedule-{deviceCode}</td></tr>'
        '</table>'
    )

    sections.append("<h3>2.2 Player (bd-vision-player)</h3>")
    sections.append(mermaid_diagram(
        "flowchart TD\n"
        "    subgraph T1[\"Track 1: Schedule Ads - paid\"]\n"
        "        direction TB\n"
        "        S1[\"Round-robin + exclusive interrupts\"]\n"
        "        S2[\"ScreenDeviceSchedulePlayComponent\"]\n"
        "        S3[\"ScreenDeviceSchedulePlayTimeSlotComponent\"]\n"
        "        S1 --> S2 --> S3\n"
        "    end\n"
        "    subgraph T2[\"Track 2: Playlist Ads - owner\"]\n"
        "        direction TB\n"
        "        P1[\"Sequential, plays when no schedule ad\"]\n"
        "        P2[\"ScreenDeviceSchedulePlaylistComponent\"]\n"
        "        P1 --> P2\n"
        "    end\n"
        "    subgraph DF[\"Data Flow\"]\n"
        "        D1[\"Pusher events → re-fetch schedules\"]\n"
        "        D2[\"Poll 10 min → re-fetch playlists\"]\n"
        "        D3[\"localStorage → schedules, playlists, retryQueue\"]\n"
        "        D4[\"Tauri plugin → download media → appDataDir\"]\n"
        "    end",
        page_id=page_id,
    ))

    sections.append(
        '<table>'
        '<tr><th>Feature</th><th>Implementation</th><th>File</th></tr>'
        '<tr><td>Schedule types</td><td><code>exclusive</code> (time-block interrupt), <code>continuous</code> (date range), <code>frequency</code> (count)</td><td><code>src/constants/schedule.constant.ts</code></td></tr>'
        '<tr><td>Round-robin</td><td><code>(currentIndex + 1) % activeSchedules.length</code></td><td><code>screen.device.schedule.play.timeslot.component.tsx</code></td></tr>'
        '<tr><td>Exclusive preempt</td><td>CalculatePlaySchedules query (1s interval) checks <code>isBetween(start, end)</code></td><td><code>screen.device.schedule.play.component.tsx</code></td></tr>'
        '<tr><td>Retry queue</td><td>Max 3 attempts, stored in localStorage</td><td><code>screen.device.schedule.play.timeslot.component.tsx</code></td></tr>'
        '<tr><td>Media download</td><td>Tauri <code>plugin-upload</code> (native HTTP), sequential</td><td><code>screen.device.schedule.setup.schedule-download.tsx</code></td></tr>'
        '<tr><td>File cleanup</td><td>Every 24h during off-hours, LRU-based</td><td><code>src/services/file-cleanup.service.ts</code></td></tr>'
        '<tr><td>Offline detect</td><td><code>err?.message === "Load failed"</code></td><td><code>screen.device.schedule.component.tsx</code></td></tr>'
        '<tr><td>Play history retry</td><td>Tauri Store (<code>player.history.json</code>), batch 10, every 1 min</td><td><code>player-history.store.ts</code></td></tr>'
        '</table>'
    )

    sections.append("<h3>2.3 Pusher Events</h3>")
    sections.append(
        '<table>'
        '<tr><th>Event</th><th>Trigger</th><th>Player Action</th></tr>'
        '<tr><td><code>update-play-schedule</code></td><td>Cron round complete</td><td>Re-fetch <code>GET /v2/play-schedules</code></td></tr>'
        '<tr><td><code>created-play-schedule</code></td><td>Player-pull job complete</td><td>Re-fetch schedules</td></tr>'
        '<tr><td><code>approved-advertisement-exclusive</code></td><td>Exclusive ad approved</td><td>Inject immediately (no re-fetch)</td></tr>'
        '<tr><td><code>stop-advertisement</code></td><td>Ad cancelled</td><td>Remove from local schedule</td></tr>'
        '<tr><td><code>new/update/delete-play-schedule</code></td><td>Schedule CRUD</td><td>Re-fetch schedules</td></tr>'
        '<tr><td><code>un-pair-screen</code></td><td>Device unpaired</td><td>Clear all, back to pair screen</td></tr>'
        '</table>'
    )

    # ─── Section 3: Proposed Architecture ───
    sections.append("<hr/>")
    sections.append("<h2>3. Proposed Architecture: Backend-Driven Player</h2>")
    sections.append(info_panel(
        "<p><strong>Core Idea:</strong> Backend sends <strong>ordered playlist sequence</strong> instead of a bag of ads + rules. "
        "Player just plays <code>sequence[i++]</code>.</p>"
    ))

    sections.append("<h3>3.1 Proposed Architecture Flow (on existing infrastructure)</h3>")
    sections.append(mermaid_diagram(
        "flowchart TD\n"
        "    subgraph BE[\"BACKEND (AdonisJS + BullMQ + Redis)\"]\n"
        "        Cron[\"Cron Job\\n(BullMQ) every 10m\"] --> Calc[\"PlayScheduleCalculate\\nNO CHANGE\"]\n"
        "        Calc --> Per[\"PerScreen calc\\nNO CHANGE\"]\n"
        "        Per -->|\"PlaySchedule rows\"| PB[\"⭐ PlaylistBuilder Service\\nNEW\\n1. Sort paid\\n2. Interleave owner\\n3. Insert exclusives\\n4. Assign sequence_no\\n5. Version++\"]\n"
        "        PB --> DB[(\"PostgreSQL NO CHANGE\\nPlaySchedule / Billboard\\nAdvertisement\")]\n"
        "        PB --> DPL[(\"⭐ DevicePlaylist NEW\\nDevicePlaylistItem\")]\n"
        "        PB --> Push[\"Pusher +evt\\nplaylist-updated\"]\n"
        "        API1[\"⭐ GET /v2/device-playlist NEW\\ntier=live, since_version=N\\nordered items + manifest\"]\n"
        "        API2[\"POST /v2/play-history ENHANCED\\nX-Idempotency-Key\\nRedis dedup\"]\n"
        "    end\n"
        "    subgraph PL[\"PLAYER (Tauri Desktop App)\"]\n"
        "        Push -->|\"WebSocket\"| INB[\"⭐ Inbox Handler NEW\\nevent_id dedup\\nversion gap check\"]\n"
        "        INB -->|\"fetch playlist\"| CACHE[\"⭐ 3-Tier Local Cache NEW\\nTier 1: LIVE (current round)\\nTier 2: BUFFER (next 2-4h)\\nTier 3: FALLBACK (owner ads)\"]\n"
        "        CACHE --> SM[\"⭐ State Machine NEW\\nBOOT → CACHED → SYNC\\n→ ONLINE → OFFLINE → FALLBACK\"]\n"
        "        SM --> REN[\"Dumb Renderer\\nplay sequence[i++]\\nSIMPLIFIED from 3,500+ lines\"]\n"
        "        OUT[\"⭐ Outbox Store NEW\\n(Tauri Store)\\npending → sent → ack\"]\n"
        "    end\n"
        "    PL -->|\"GET\"| API1\n"
        "    OUT -->|\"flush every 1 min\"| API2\n"
        "    style PB fill:#ffd700,stroke:#333\n"
        "    style DPL fill:#ffd700,stroke:#333\n"
        "    style INB fill:#ffd700,stroke:#333\n"
        "    style CACHE fill:#ffd700,stroke:#333\n"
        "    style SM fill:#ffd700,stroke:#333\n"
        "    style OUT fill:#ffd700,stroke:#333\n"
        "    style API1 fill:#ffd700,stroke:#333",
        page_id=page_id,
    ))

    sections.append("<h3>3.2 Infrastructure Mapping: Existing → Proposed</h3>")
    sections.append(
        '<table>'
        '<tr><th>Existing Infrastructure</th><th>Role Today</th><th>Role in Proposed</th><th>Change</th></tr>'
        '<tr><td><strong>BullMQ + Redis</strong></td><td>Cron job queue (PlayScheduleCalculate)</td><td>Same + enqueue PlaylistBuilder after schedule calc</td><td>' + status_macro("REUSE", "Green") + '</td></tr>'
        '<tr><td><strong>PostgreSQL</strong></td><td>PlaySchedule, Billboard, Advertisement models</td><td>Same + NEW DevicePlaylist, DevicePlaylistItem tables</td><td>' + status_macro("ADD TABLES", "Yellow") + '</td></tr>'
        '<tr><td><strong>Redis (cache)</strong></td><td>GET/SET string cache (Bentocache)</td><td>Same + idempotency keys (SET with TTL 24h)</td><td>' + status_macro("REUSE", "Green") + '</td></tr>'
        '<tr><td><strong>Pusher (WebSocket)</strong></td><td>6 event types, channel per device</td><td>Same channel + 2 new typed events</td><td>' + status_macro("ADD EVENTS", "Yellow") + '</td></tr>'
        '<tr><td><strong>AdonisJS routes</strong></td><td>Player V2 routes (/play-schedules, /playlist-advertisements)</td><td>Keep existing + add GET /v2/device-playlist</td><td>' + status_macro("ADD ENDPOINT", "Yellow") + '</td></tr>'
        '<tr><td><strong>Tauri plugin-upload</strong></td><td>Native HTTP media download</td><td>Same (sequential download with resume)</td><td>' + status_macro("NO CHANGE", "Green") + '</td></tr>'
        '<tr><td><strong>localStorage</strong></td><td>Schedules, playlists, playData</td><td>Migrate heavy data to Tauri Store; localStorage for small state only</td><td>' + status_macro("MIGRATE", "Yellow") + '</td></tr>'
        '<tr><td><strong>Tauri Store</strong></td><td>player.history.json (play history retry)</td><td>+ outbox.json, playlist-cache.json, inbox-state.json</td><td>' + status_macro("EXPAND", "Yellow") + '</td></tr>'
        '<tr><td><strong>Pusher client (player)</strong></td><td>Subscribe, re-fetch on event</td><td>Same + inbox dedup layer (event_id + version check)</td><td>' + status_macro("WRAP", "Yellow") + '</td></tr>'
        '<tr><td><strong>x-device-code auth</strong></td><td>Player auth header</td><td>Same</td><td>' + status_macro("NO CHANGE", "Green") + '</td></tr>'
        '</table>'
    )

    sections.append("<h3>3.3 Sequence Diagrams: Key Flows</h3>")

    sections.append("<h4>Flow A: Normal Online Play (Happy Path)</h4>")
    sections.append(mermaid_diagram(
        "sequenceDiagram\n"
        "    participant BE as Backend\n"
        "    participant PU as Pusher\n"
        "    participant PL as Player\n"
        "    BE->>BE: Cron fires (every 10m)\n"
        "    BE->>BE: PlayScheduleCalculate PerScreen\n"
        "    BE->>BE: Create PlaySchedule rows\n"
        "    BE->>BE: PlaylistBuilder: sort + interleave + version++\n"
        "    BE->>BE: Save DevicePlaylist (v42)\n"
        "    BE->>PU: Push: playlist-updated\n"
        "    PU->>PL: {version:42, tier:live}\n"
        "    Note over PL: Inbox check:<br/>42 > 41? YES<br/>event_id new? YES\n"
        "    PL->>BE: GET /v2/device-playlist?since_version=41\n"
        "    BE->>PL: {version:42, items:[...], manifest:[...]}\n"
        "    Note over PL: Save to Tier 1<br/>Download new media<br/>local_version = 42\n"
        "    Note over PL: Play sequence[0], [1], ...\n"
        "    PL->>BE: POST /v2/play-history (Outbox flush)\n"
        "    Note over PL: X-Idempotency-Key: uuid-123\n"
        "    BE->>PL: {status: 'created', ack_id: 'PH-xxx'}\n"
        "    Note over PL: Mark outbox: acked",
        page_id=page_id,
    ))

    sections.append("<h4>Flow B: Network Drop → Offline → Reconnect</h4>")
    sections.append(mermaid_diagram(
        "sequenceDiagram\n"
        "    participant BE as Backend\n"
        "    participant PU as Pusher\n"
        "    participant PL as Player\n"
        "    Note over PL: Playing Tier 1, version = 42\n"
        "    rect rgb(255, 200, 200)\n"
        "        Note over BE,PL: NETWORK DROPS\n"
        "        BE->>BE: Cron: v43\n"
        "        BE->>BE: Cron: v44\n"
        "        BE->>BE: Cron: v45\n"
        "        PU--xPL: (not delivered)\n"
        "    end\n"
        "    Note over PL: Tier 1 exhausted → OFFLINE_PLAYBACK<br/>Switch to Tier 2 (buffer)\n"
        "    Note over PL: Tier 2 expired → FALLBACK<br/>Switch to Tier 3 (owner loop)\n"
        "    rect rgb(200, 255, 200)\n"
        "        Note over BE,PL: NETWORK RETURNS\n"
        "        PU->>PL: Pusher reconnect\n"
        "        Note over PL: Debounce: wait 10s stable\n"
        "    end\n"
        "    PL->>BE: GET /v2/device-playlist?since_version=42\n"
        "    Note over BE: gap = 45-42 = 3 → FULL playlist\n"
        "    BE->>PL: {version:45, full:true, items:[...]}\n"
        "    Note over PL: Replace Tier 1+2<br/>Download new media<br/>local_version = 45<br/>State: ONLINE_PLAYBACK\n"
        "    PL->>BE: POST /v2/play-history (flush backlog)\n"
        "    Note over BE: Dedup via idempotency keys",
        page_id=page_id,
    ))

    sections.append("<h4>Flow C: Exclusive Ad Interrupt (Online)</h4>")
    sections.append(mermaid_diagram(
        "sequenceDiagram\n"
        "    participant AD as Admin\n"
        "    participant BE as Backend\n"
        "    participant PL as Player\n"
        "    AD->>BE: Approve exclusive ad\n"
        "    BE->>BE: PlaylistBuilder: inject at play_at, version++\n"
        "    BE->>PL: Push: approved-advertisement-exclusive\n"
        "    Note over PL: {version:43, ad_code,<br/>play_at, media_url, checksum}\n"
        "    Note over PL: Download media immediately<br/>Wait for play_at time<br/>Pause current ad<br/>Play exclusive ad<br/>Resume sequence",
        page_id=page_id,
    ))

    sections.append("<h4>Flow D: Fresh Boot (No Cache)</h4>")
    sections.append(mermaid_diagram(
        "sequenceDiagram\n"
        "    participant PL as Player\n"
        "    participant BE as Backend\n"
        "    Note over PL: BOOT (app start)<br/>Check Tauri Store...<br/>No cached playlist<br/>State: SPLASH (logo + loading)\n"
        "    Note over PL: Check internet... OK<br/>State: SYNCING (first)\n"
        "    PL->>BE: GET /v2/device-playlist (full fetch)\n"
        "    BE->>PL: Tier 1 (live) + Tier 2 + Tier 3 + manifest\n"
        "    Note over PL: Download ALL media<br/>Save to Tauri Store<br/>local_version = latest\n"
        "    Note over PL: Subscribe Pusher channel<br/>State: ONLINE_PLAYBACK<br/>Play Tier 1: sequence[0], [1]...\n"
        "    rect rgb(255, 255, 200)\n"
        "        Note over PL,BE: Fresh boot + NO internet:<br/>State stays SPLASH<br/>Show logo + 'connect wifi'<br/>Retry every 5s\n"
        "    end",
        page_id=page_id,
    ))

    sections.append("<h3>3.4 Backend Scheduling Logic: How PlaylistBuilder Works</h3>")
    sections.append(note_panel(
        "<p><strong>Key insight:</strong> PlaylistBuilder runs <em>after</em> existing PlayScheduleCalculatePerScreen. "
        "It takes the PlaySchedule rows (already calculated) and converts them into an <strong>ordered sequence</strong>.</p>"
    ))
    sections.append(tracked_code_block(
        "// PlaylistBuilder Algorithm (simplified)\n\n"
        "Input:\n"
        "  - playSchedules[]: PlaySchedule rows from current round\n"
        "    (already has: ad_code, media, duration, type, priority, time_slot)\n"
        "  - ownerPlaylist[]: Owner's default ads from PlaylistAdvertisement\n"
        "  - billboard: { ownerTime, platformTime }  // seconds per hour budget\n\n"
        "Step 1: Separate by type\n"
        "  exclusive[] = playSchedules.filter(s => s.type === 'exclusive')\n"
        "  frequency[] = playSchedules.filter(s => s.type === 'frequency')\n"
        "  continuous[] = playSchedules.filter(s => s.type === 'continuous')\n\n"
        "Step 2: Calculate interleave ratio\n"
        "  // Example: ownerTime=1800s, platformTime=1800s → 50/50\n"
        "  ownerRatio = billboard.ownerTime / (ownerTime + platformTime)\n"
        "  // Every N paid ads, insert 1 owner ad\n"
        "  interleaveEvery = Math.round(1 / ownerRatio)\n\n"
        "Step 3: Build ordered sequence\n"
        "  sequence = []\n"
        "  ownerIndex = 0\n\n"
        "  // 3a. Continuous ads first (they fill time blocks)\n"
        "  for (const ad of continuous) {\n"
        "    sequence.push({ ...ad, type: 'paid' })\n"
        "    if (sequence.length % interleaveEvery === 0) {\n"
        "      sequence.push(ownerPlaylist[ownerIndex++ % ownerPlaylist.length])\n"
        "    }\n"
        "  }\n\n"
        "  // 3b. Frequency ads (count-based)\n"
        "  for (const ad of frequency) {\n"
        "    sequence.push({ ...ad, type: 'paid' })\n"
        "    if (sequence.length % interleaveEvery === 0) {\n"
        "      sequence.push(ownerPlaylist[ownerIndex++ % ownerPlaylist.length])\n"
        "    }\n"
        "  }\n\n"
        "  // 3c. Fill remaining time with owner ads\n"
        "  while (totalDuration(sequence) < roundDuration) {\n"
        "    sequence.push(ownerPlaylist[ownerIndex++ % ownerPlaylist.length])\n"
        "  }\n\n"
        "Step 4: Inject exclusives at their exact play_at position\n"
        "  for (const ex of exclusive) {\n"
        "    // Find position in sequence where play_at falls\n"
        "    insertAt = findTimePosition(sequence, ex.play_at)\n"
        "    sequence.splice(insertAt, 0, { ...ex, priority: 'exclusive' })\n"
        "  }\n\n"
        "Step 5: Assign sequence_no (1, 2, 3, ...)\n"
        "  sequence.forEach((item, i) => item.sequence_no = i + 1)\n\n"
        "Step 6: Version + persist\n"
        "  version = (lastVersion for this device) + 1\n"
        "  Save DevicePlaylist { version, tier: 'live', items: sequence }\n"
        "  Mark previous 'live' playlist as 'replaced'\n\n"
        "Output:\n"
        "  DevicePlaylist v42 with ordered items[]\n"
        "  Player just plays: items[0] → items[1] → items[2] → ...",
        "typescript", "PlaylistBuilder Algorithm"
    ))

    sections.append("<h3>3.5 3-Tier Playlist Architecture</h3>")
    sections.append(mermaid_diagram(
        "flowchart TD\n"
        "    subgraph LOCAL[\"Player Local Storage\"]\n"
        "        T1[\"🟢 Tier 1: LIVE\\n(current round, ordered by backend)\\n① ② ③ ④ ⑤ ⑥\"]\n"
        "        T2[\"🟡 Tier 2: BUFFER\\n(next 2-4 hours, pre-fetched)\\nPre-generated playlist + media\"]\n"
        "        T3[\"🔴 Tier 3: FALLBACK\\n(owner ads, always cached)\\nLoop forever\"]\n"
        "        T1 -->|exhausted| T2\n"
        "        T2 -->|expired| T3\n"
        "    end\n"
        "    BE[\"Backend push\"] -->|\"playlist-updated\"| T1\n"
        "    T3 -->|\"Reconnect\"| BE\n"
        "    style T1 fill:#d4edda,stroke:#333\n"
        "    style T2 fill:#fff3cd,stroke:#333\n"
        "    style T3 fill:#f8d7da,stroke:#333",
        page_id=page_id,
    ))

    sections.append("<h3>3.2 What Changes vs What Stays</h3>")
    sections.append(
        '<table>'
        '<tr><th>Component</th><th>Current</th><th>Proposed</th><th>Change Type</th></tr>'
        '<tr><td>Cron job</td><td>PlayScheduleCalculate every 10 min</td><td>Same</td><td>' + status_macro("NO CHANGE", "Green") + '</td></tr>'
        '<tr><td>Per-screen job</td><td>Create PlaySchedule rows</td><td>Create PlaySchedule + <strong>ordered DevicePlaylist</strong></td><td>' + status_macro("ADD STEP", "Yellow") + '</td></tr>'
        '<tr><td>Pusher</td><td>Channel per device</td><td>Same channel + new event <code>playlist-updated</code></td><td>' + status_macro("ADD EVENT", "Yellow") + '</td></tr>'
        '<tr><td>Player API</td><td>GET /v2/play-schedules + /playlist-advertisements</td><td><strong>GET /v2/device-playlist</strong> (unified)</td><td>' + status_macro("NEW ENDPOINT", "Blue") + '</td></tr>'
        '<tr><td>Player scheduling</td><td>Round-robin + exclusive interrupt (complex)</td><td><strong>play sequence[i++]</strong> (simple)</td><td>' + status_macro("SIMPLIFY", "Green") + '</td></tr>'
        '<tr><td>Player storage</td><td>localStorage (separate schedules + playlists)</td><td>Tauri Store (3-tier playlist)</td><td>' + status_macro("MIGRATE", "Yellow") + '</td></tr>'
        '<tr><td>Media download</td><td>Tauri plugin-upload</td><td>Same</td><td>' + status_macro("NO CHANGE", "Green") + '</td></tr>'
        '<tr><td>BullMQ</td><td>Redis queue</td><td>Same</td><td>' + status_macro("NO CHANGE", "Green") + '</td></tr>'
        '<tr><td>Auth</td><td>x-device-code header</td><td>Same</td><td>' + status_macro("NO CHANGE", "Green") + '</td></tr>'
        '<tr><td>Play history</td><td>POST /v2/play-history + retry</td><td>Same + <strong>Outbox pattern</strong></td><td>' + status_macro("ENHANCE", "Yellow") + '</td></tr>'
        '</table>'
    )

    sections.append("<h3>3.3 New Backend Components</h3>")
    sections.append(tracked_code_block(
        "// NEW: DevicePlaylist model (app/Models/DevicePlaylist.ts)\n"
        "interface DevicePlaylist {\n"
        "  id: number\n"
        "  device_code: string\n"
        "  tier: 'live' | 'buffer' | 'fallback'\n"
        "  version: number          // monotonically increasing per device\n"
        "  valid_from: DateTime\n"
        "  valid_until: DateTime\n"
        "  status: 'active' | 'expired' | 'replaced'\n"
        "  created_at: DateTime\n"
        "}\n\n"
        "// NEW: DevicePlaylistItem model (app/Models/DevicePlaylistItem.ts)\n"
        "interface DevicePlaylistItem {\n"
        "  id: number\n"
        "  device_playlist_id: number\n"
        "  sequence_no: number      // ordered by backend\n"
        "  play_schedule_code: string | null  // link to existing PlaySchedule\n"
        "  advertisement_code: string\n"
        "  media_code: string\n"
        "  duration_seconds: number\n"
        "  type: 'paid' | 'owner'\n"
        "  priority: 'normal' | 'exclusive'\n"
        "  play_at: DateTime | null  // for exclusive: exact time\n"
        "}",
        "typescript", "New Models"
    ))

    sections.append(tracked_code_block(
        "// NEW: PlaylistBuilder service (app/Services/PlaylistBuilderService.ts)\n"
        "// Called AFTER PlayScheduleCalculatePerScreen generates PlaySchedule rows\n\n"
        "class PlaylistBuilderService {\n"
        "  async buildPlaylist(\n"
        "    screenCode: string,\n"
        "    playSchedules: PlaySchedule[],   // from cron calculation\n"
        "    ownerPlaylist: PlaylistAdvertisement[],\n"
        "    billboard: Billboard\n"
        "  ): Promise<DevicePlaylist> {\n"
        "    // 1. Sort paid ads by priority/time\n"
        "    // 2. Interleave owner ads based on ownerTime/platformTime ratio\n"
        "    // 3. Insert exclusive ads at their exact play_at position\n"
        "    // 4. Assign sequence_no (1, 2, 3, ...)\n"
        "    // 5. Set valid_from/valid_until from round window\n"
        "    // 6. Increment version (per device)\n"
        "    // 7. Create DevicePlaylist + DevicePlaylistItem rows\n"
        "    // 8. Mark previous 'live' playlist as 'replaced'\n"
        "  }\n\n"
        "  async buildBufferPlaylist(\n"
        "    screenCode: string,\n"
        "    hoursAhead: number = 4\n"
        "  ): Promise<DevicePlaylist> {\n"
        "    // Pre-generate next N hours of playlist for offline buffer\n"
        "  }\n\n"
        "  async buildFallbackPlaylist(\n"
        "    billboardCode: string\n"
        "  ): Promise<DevicePlaylist> {\n"
        "    // Owner ads only, loopable, rarely changes\n"
        "  }\n"
        "}",
        "typescript", "PlaylistBuilder Service"
    ))

    sections.append("<h3>3.4 New API Endpoint</h3>")
    sections.append(tracked_code_block(
        "// GET /v2/device-playlist?tier=live&since_version=41\n"
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
        '      "media_code": "MD-xxx",\n'
        '      "media_url": "https://cdn.../video.mp4",\n'
        '      "media_checksum": "a1b2c3d4...",  // MD5 for validation\n'
        '      "duration_seconds": 15,\n'
        '      "type": "paid",\n'
        '      "priority": "normal"\n'
        "    },\n"
        "    ...\n"
        "  ],\n"
        '  "media_manifest": [\n'
        '    { "media_code": "MD-xxx", "url": "...", "checksum": "...", "size_bytes": 12345 }\n'
        "  ]\n"
        "}",
        "json", "API Response Format"
    ))

    # ─── Section 4: Outbox/Inbox Pattern ───
    sections.append("<hr/>")
    sections.append("<h2>4. Outbox/Inbox Pattern</h2>")

    # 4.0 Problems to solve
    sections.append("<h3>4.0 ปัญหาที่ต้องแก้</h3>")
    sections.append(error_panel(
        "<p><strong>ปัญหา 1 (Player &rarr; Backend): Play History ซ้ำ</strong><br/>"
        "Player POST <code>/v2/play-history</code> &rarr; timeout &rarr; retry &rarr; backend ได้ 2 รายการ สำหรับ ad เดียวกัน</p>"
        "<p><strong>ปัญหา 2 (Backend &rarr; Player): Missed Pusher Events</strong><br/>"
        "Pusher disconnect 30 วิ &rarr; reconnect &rarr; events ระหว่างนั้นหายไป &rarr; Player ไม่รู้ว่ามี playlist ใหม่</p>"
        "<p><strong>ปัญหา 3 (Backend &rarr; Player): Duplicate Pusher Events</strong><br/>"
        "Pusher ส่ง event ซ้ำ (at-least-once) &rarr; player process ซ้ำ &rarr; fetch ซ้ำ &rarr; เสีย bandwidth</p>"
    ))
    sections.append(info_panel(
        "<p><strong>Solution:</strong> Outbox (Player&rarr;Backend) + Inbox (Backend&rarr;Player)</p>"
    ))

    # 4.1 Player Outbox
    sections.append("<h3>4.1 Player Outbox (Play History)</h3>")
    sections.append(mermaid_diagram(
        "flowchart TD\n"
        "    EV[\"Event occurs\\n(ad played)\"] --> OB[\"Outbox Store\\n(Tauri Store)\"]\n"
        "    OB -.->|\"Format\"| FMT[\"id: uuid\\ntype, payload\\nstatus: pending/sent/acked\\nretry: 0, created_at\"]\n"
        "    OB -->|\"Flush ทุก 1 นาที\"| API[\"POST /v2/play-history\\nX-Idempotency-Key: uuid\"]\n"
        "    API -->|\"200 OK + ack_id\"| ACK[\"Mark status = acked\\nCleanup acked items >24h\"]\n"
        "    API -->|\"timeout/error\"| RETRY[\"Keep pending\\nretry_count++\"]\n"
        "    RETRY -->|\"retry < 10\"| OB\n"
        "    RETRY -->|\"retry >= 10\"| FAIL[\"Mark failed\\nLog diagnostic\"]",
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
        "typescript", "Outbox Interface"
    ))

    # 4.2 Backend Idempotency
    sections.append("<h3>4.2 Backend Idempotency</h3>")
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
        "typescript", "Backend Idempotency Check"
    ))

    # 4.3 Player Inbox
    sections.append("<h3>4.3 Player Inbox (Schedule Commands)</h3>")
    sections.append(mermaid_diagram(
        "flowchart TD\n"
        "    EV[\"Pusher event arrives\\n{event_id, version, ...}\"] --> CHK{\"Check:\\nevent_id already in inbox?\\nversion ≤ local?\"}\n"
        "    CHK -->|\"YES\"| SKIP[\"SKIP\\n(duplicate)\"]\n"
        "    CHK -->|\"NO\"| PROC[\"PROCESS\\nfetch new playlist\\nupdate local cache\\nstore event_id (last 100)\"]\n"
        "    REC[\"On reconnect\"] --> FETCH[\"GET /v2/device-playlist\\n?since_version=local_ver\"]\n"
        "    FETCH --> DELTA[\"Delta or full playlist\\n(if gap too large)\"]",
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
        "typescript", "Inbox Deduplication Code"
    ))

    # 4.4 Version Protocol
    sections.append("<h3>4.4 Version Protocol</h3>")
    sections.append(mermaid_diagram(
        "sequenceDiagram\n"
        "    participant BE as Backend\n"
        "    participant PL as Player\n"
        "    BE->>BE: Cron → calculate → playlist v42\n"
        "    BE->>PL: Pusher: {version: 42}\n"
        "    Note over PL: inbox: 42 > 41? YES\n"
        "    PL->>BE: GET /device-playlist?since=41\n"
        "    BE->>PL: {version: 42, items}\n"
        "    Note over PL: save Tier 1<br/>local_version = 42\n"
        "    rect rgb(255, 200, 200)\n"
        "        Note over BE,PL: Internet drops\n"
        "        BE->>BE: Cron → v43, v44, v45\n"
        "    end\n"
        "    rect rgb(200, 255, 200)\n"
        "        Note over BE,PL: Internet returns + Pusher reconnect\n"
        "    end\n"
        "    PL->>BE: GET /device-playlist?since=42\n"
        "    Note over BE: gap=3 → return FULL playlist\n"
        "    BE->>PL: {version: 45, full: true}\n"
        "    Note over PL: replace Tier 1+2<br/>local_version = 45",
        page_id=page_id,
    ))

    # ─── Section 5: Player State Machine ───
    sections.append("<hr/>")
    sections.append("<h2>5. Player State Machine</h2>")
    sections.append(mermaid_diagram(
        "stateDiagram-v2\n"
        "    [*] --> BOOT\n"
        "\n"
        "    BOOT --> SPLASH : No localStorage\n"
        "    BOOT --> CACHED_PLAYBACK : Has localStorage\n"
        "\n"
        "    SPLASH --> SYNCING_FIRST : Connected\n"
        "    SPLASH --> SPLASH : No internet (retry 5s)\n"
        "\n"
        "    CACHED_PLAYBACK --> OFFLINE_PLAYBACK : Not online\n"
        "    CACHED_PLAYBACK --> SYNCING_DELTA : Online\n"
        "\n"
        "    SYNCING_FIRST --> ONLINE_PLAYBACK : Playlist fetched\n"
        "    SYNCING_DELTA --> ONLINE_PLAYBACK : Delta applied\n"
        "\n"
        "    ONLINE_PLAYBACK --> OFFLINE_PLAYBACK : Network drop\n"
        "\n"
        "    OFFLINE_PLAYBACK --> ONLINE_PLAYBACK : Reconnect + sync\n"
        "    OFFLINE_PLAYBACK --> FALLBACK : Tier 1+2 exhausted\n"
        "\n"
        "    FALLBACK --> ONLINE_PLAYBACK : Reconnect + sync\n"
        "    FALLBACK --> SPLASH_LAST : Tier 3 empty\n"
        "\n"
        "    note right of CACHED_PLAYBACK : Play from cache immediately\n"
        "    note right of OFFLINE_PLAYBACK : Tier 1 then 2 then 3\n"
        "    note right of SPLASH_LAST : Logo + contact admin",
        page_id=page_id,
    ))

    sections.append(warning_panel(
        "<p><strong>Rule:</strong> Every state MUST have something to display. <strong>Black screen is NEVER acceptable.</strong></p>"
    ))

    # ─── Section 6: Edge Cases ───
    sections.append("<hr/>")
    sections.append("<h2>6. Edge Cases Analysis (ละเอียด)</h2>")

    sections.append("<h3>Category 1: Network Issues</h3>")
    sections.append(
        '<table>'
        '<tr><th>#</th><th>Edge Case</th><th>สิ่งที่เกิดขึ้น</th><th>Solution</th></tr>'
        '<tr><td>E1</td><td><strong>Network flapping</strong> (on/off ทุก 30 วิ)</td>'
        '<td>Player fetch ค้าง, Pusher reconnect วนซ้ำ, media download incomplete</td>'
        '<td><strong>Debounce reconnect:</strong> ต้อง online ต่อเนื่อง 10 วิ ก่อน trigger sync. Media download ต้อง resume-able (Tauri download รองรับอยู่แล้ว)</td></tr>'
        '<tr><td>E2</td><td><strong>Pusher disconnect 5 นาที</strong> &rarr; missed events</td>'
        '<td>Player ไม่รู้ว่ามี playlist ใหม่</td>'
        '<td><strong>Version check on reconnect:</strong> Player เก็บ <code>last_version</code>. Reconnect &rarr; <code>GET /v2/device-playlist?since_version=N</code> &rarr; ได้ delta</td></tr>'
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

    sections.append("<h3>Category 2: Schedule/Playlist Issues</h3>")
    sections.append(
        '<table>'
        '<tr><th>#</th><th>Edge Case</th><th>สิ่งที่เกิดขึ้น</th><th>Solution</th></tr>'
        '<tr><td>E7</td><td><strong>Schedule gap</strong> &mdash; ไม่มี ad สำหรับช่วงเวลานี้</td>'
        '<td>Tier 1 ว่างเปล่า</td>'
        '<td>Auto-switch Tier 3 (owner fallback). <strong>ห้ามจอดำเด็ดขาด</strong></td></tr>'
        '<tr><td>E8</td><td><strong>Exclusive ad ขณะ offline</strong></td>'
        '<td>Backend approve exclusive แต่ push ไม่ถึง player</td>'
        '<td><strong>Buffer tier:</strong> Exclusive ที่ approved ล่วงหน้า ถูกใส่ใน Tier 2 ด้วย <code>priority: exclusive</code> + <code>play_at: exact_time</code>. Player check Tier 2 ทุก 1 วิ ว่ามี exclusive <code>CalculatePlaySchedules</code> query ทำอยู่แล้ว)</td></tr>'
        '<tr><td>E9</td><td><strong>Tier 1 หมด แต่ Tier 2 ยังไม่พร้อม</strong> (media กำลัง download)</td>'
        '<td>ช่วงว่างระหว่าง tier</td>'
        '<td>Play Tier 3 ขณะรอ. เมื่อ Tier 2 media download ครบ &rarr; switch ขึ้นไป</td></tr>'
        '<tr><td>E10</td><td><strong>Billboard time budget overflow</strong> &mdash; ads มากกว่า time slots</td>'
        '<td>PlaylistBuilder สร้าง playlist ยาวเกินรอบ</td>'
        '<td>Backend cap ที่ <code>roundDuration</code>. ส่วนที่เกิน &rarr; ไม่ใส่ playlist (เหมือนเดิมที่ cron ทำ). Player ไม่ต้องคิด</td></tr>'
        '<tr><td>E11</td><td><strong>Owner playlist ว่าง</strong> &mdash; billboard owner ไม่ได้ตั้งค่า</td>'
        '<td>Tier 3 ไม่มี content</td>'
        '<td><strong>First boot check:</strong> ถ้า Tier 3 ว่าง &rarr; แสดง <strong>system splash</strong> (logo + "กำลังเตรียมระบบ"). Admin UI แจ้งเตือน owner ให้ upload content. บังคับ: Device register สำเร็จต่อเมื่อ billboard มีอย่างน้อย 1 รายการ</td></tr>'
        '<tr><td>E12</td><td><strong>Stale schedule</strong> &mdash; offline นานจน Tier 2 expired</td>'
        '<td><code>valid_until</code> ผ่านไปแล้ว</td>'
        '<td>Player check <code>valid_until</code> ก่อนเล่น. ถ้า expired &rarr; switch Tier 3. <strong>ไม่เล่น ad expired</strong> เพราะอาจเป็น campaign ที่หมดแล้ว (billing issue)</td></tr>'
        '<tr><td>E13</td><td><strong>Concurrent Pusher events</strong> &mdash; 3 events มาพร้อมกัน</td>'
        '<td>Race condition ใน playlist update</td>'
        '<td><strong>Version monotonic:</strong> Player เก็บ <code>current_version</code>. ถ้า <code>event.version</code> &le; current &rarr; skip. ถ้า &gt; current &rarr; process. ถ้า &gt; current+1 (gap) &rarr; full re-fetch</td></tr>'
        '</table>'
    )

    sections.append("<h3>Category 3: Device/Storage Issues</h3>")
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

    sections.append("<h3>Category 4: Business Logic Issues</h3>")
    sections.append(
        '<table>'
        '<tr><th>#</th><th>Edge Case</th><th>สิ่งที่เกิดขึ้น</th><th>Solution</th></tr>'
        '<tr><td>E20</td><td><strong>Ad cancelled ขณะ offline</strong></td>'
        '<td>Backend cancel ad แต่ player ยังเล่นอยู่</td>'
        '<td><strong>Acceptable tradeoff:</strong> player จะเล่น ad ต่อจน reconnect. เมื่อ reconnect &rarr; sync playlist ใหม่ &rarr; ad หายไป. Play history records ยังถูกต้อง (ส่งทีหลัง reconnect)</td></tr>'
        '<tr><td>E21</td><td><strong>Campaign budget exhausted ขณะเล่น</strong></td>'
        '<td>Player กำลังเล่น ad ของ campaign ที่หมด budget</td>'
        '<td>Backend ไม่ใส่ ad นี้ใน round ถัดไป. Player round ปัจจุบันเล่นจบปกติ (ยอมรับได้ &mdash; เป็น 1 round = 10 นาที max)</td></tr>'
        '<tr><td>E22</td><td><strong>Play history ส่งไม่ได้</strong> &rarr; billing คลาดเคลื่อน</td>'
        '<td>Offline นาน &rarr; play history queue สะสม</td>'
        '<td><strong>Outbox guarantee:</strong> ไม่มี play event หาย (persisted ใน Tauri Store). เมื่อ reconnect &rarr; flush ทั้งหมดตามลำดับ. Backend reconcile by timestamp</td></tr>'
        '<tr><td>E23</td><td><strong>Billboard unpair ขณะ offline</strong></td>'
        '<td>Admin unpair device แต่ player ไม่รู้</td>'
        '<td>Player ยังเล่นต่อจาก cache. เมื่อ reconnect &rarr; Pusher <code>un-pair-screen</code> &rarr; clear all + back to pair screen. หรือ: API call fail &rarr; 401 &rarr; trigger unpair locally</td></tr>'
        '<tr><td>E24</td><td><strong>Multiple devices ใช้ device code เดียวกัน</strong></td>'
        '<td>Clone device &rarr; 2 players same code</td>'
        '<td>Backend: POST <code>/v2/play-history</code> ส่ง <code>device_fingerprint</code> (MAC + hostname). ถ้าไม่ตรง &rarr; reject + alert</td></tr>'
        '</table>'
    )

    # ─── Section 7: Migration Plan ───
    sections.append("<hr/>")
    sections.append("<h2>7. Migration Plan (Incremental)</h2>")
    sections.append(info_panel(
        "<p><strong>Feature flag:</strong> <code>billboard.player_mode: 'smart' | 'dumb'</code> &mdash; roll out per billboard, no big bang</p>"
    ))
    sections.append(
        '<table>'
        '<tr><th>Phase</th><th>Backend</th><th>Player</th><th>Risk</th></tr>'
        '<tr><td><strong>Phase 0</strong></td><td>Add <code>version</code> field to Pusher payload</td><td>Store version (don\'t use yet)</td><td>' + status_macro("Zero risk", "Green") + '</td></tr>'
        '<tr><td><strong>Phase 1</strong></td><td>Add PlaylistBuilder service + DevicePlaylist models + <code>GET /v2/device-playlist</code></td><td>Read-only testing (no behavior change)</td><td>' + status_macro("Backend only", "Green") + '</td></tr>'
        '<tr><td><strong>Phase 2</strong></td><td>Add Idempotency Key check in play-history</td><td>Send <code>X-Idempotency-Key</code> header</td><td>' + status_macro("Backward compat", "Green") + '</td></tr>'
        '<tr><td><strong>Phase 3</strong></td><td>&mdash;</td><td>Player V2: read ordered playlist. <strong>Feature flag per device</strong></td><td>' + status_macro("Gradual rollout", "Yellow") + '</td></tr>'
        '<tr><td><strong>Phase 4</strong></td><td>&mdash;</td><td>3-Tier cache + state machine + checksum validation</td><td>' + status_macro("Full new behavior", "Yellow") + '</td></tr>'
        '<tr><td><strong>Phase 5</strong></td><td>Remove old schedule endpoints (v1)</td><td>Remove old scheduling code</td><td>' + status_macro("Cleanup", "Grey") + '</td></tr>'
        '</table>'
    )

    # ─── Section 8: Industry Reference ───
    sections.append("<hr/>")
    sections.append("<h2>8. Industry Reference</h2>")
    sections.append("<h3>8.1 How Commercial Solutions Handle Offline</h3>")
    sections.append(
        '<table>'
        '<tr><th>Platform</th><th>Approach</th><th>Buffer</th></tr>'
        '<tr><td>Xibo</td><td>RequiredFiles manifest + MD5 per file + 50MB chunk download</td><td>48h ahead (configurable)</td></tr>'
        '<tr><td>piSignage</td><td>Default playlist fallback + local media folder + delta sync</td><td>Full campaign window</td></tr>'
        '<tr><td>BrightSign BSN.Cloud</td><td>Local-first: all media cached, network = sync only</td><td>Content-dependent</td></tr>'
        '<tr><td>info-beamer</td><td>3-state degradation (Online/Degraded/Offline) + RTC fallback</td><td>All scheduled content</td></tr>'
        '</table>'
    )

    sections.append("<h3>8.2 Open Source References</h3>")
    sections.append(
        '<table>'
        '<tr><th>Project</th><th>Repository</th><th>Relevant Pattern</th></tr>'
        '<tr><td>Xibo Player SDK</td><td><a href="https://github.com/xibo-players/xiboplayer">xibo-players/xiboplayer</a></td><td>Cache API + IndexedDB, XMR WebSocket, chunk downloads with MD5, 2-layout preload pool</td></tr>'
        '<tr><td>Xibo .NET Client</td><td><a href="https://github.com/xibosignage/xibo-dotnetclient">xibosignage/xibo-dotnetclient</a></td><td>ScheduleManager.cs: thread polling, priority resolution, disk-resident schedule, Splash fallback</td></tr>'
        '<tr><td>piSignage</td><td><a href="https://github.com/colloqi/piSignage">colloqi/piSignage</a></td><td>Node.js + WebSocket, default playlist fallback, local filesystem media</td></tr>'
        '<tr><td>Anthias (Screenly OSE)</td><td><a href="https://github.com/Screenly/Anthias">Screenly/Anthias</a></td><td>Docker microservices, Redis + SQLite, Celery queue, Qt viewer</td></tr>'
        '</table>'
    )

    sections.append("<h3>8.3 Protocol Recommendation</h3>")
    sections.append(note_panel(
        "<p><strong>Keep Pusher</strong> (existing) for real-time push. Add <strong>version-based checkpoint</strong> on reconnect via REST. "
        "Never depend on push for playback &mdash; it only triggers early sync.</p>"
        "<p><strong>Key insight (from RxDB):</strong> Client can miss events during disconnect. "
        "Solution: checkpoint mode on reconnect (full schedule compare via REST) + event mode once synced (Pusher for incremental).</p>"
    ))

    # ─── Section 9: Formalized Event-Driven Architecture ───
    sections.append("<hr/>")
    sections.append("<h2>9. Formalized Event-Driven Architecture</h2>")
    sections.append(info_panel(
        "<p><strong>Decision:</strong> Formalize existing event-driven patterns (Pusher + BullMQ) with typed contracts, "
        "domain events, and clear ownership. <strong>NOT</strong> Event-Sourcing &mdash; scale + team doesn't justify the complexity.</p>"
    ))

    sections.append("<h3>9.1 What We Already Have (De Facto Event-Driven)</h3>")
    sections.append(
        '<table>'
        '<tr><th>Component</th><th>Pattern</th><th>Status</th></tr>'
        '<tr><td>BullMQ cron &rarr; per-screen jobs</td><td>Job queue as event bus</td><td>' + status_macro("EXISTS", "Green") + '</td></tr>'
        '<tr><td>Pusher events &rarr; Player</td><td>Real-time event delivery</td><td>' + status_macro("EXISTS", "Green") + '</td></tr>'
        '<tr><td>Play history retry queue</td><td>Outbox-like (player.history.json)</td><td>' + status_macro("EXISTS", "Green") + '</td></tr>'
        '<tr><td>Typed event contracts</td><td>Explicit interface per event</td><td>' + status_macro("MISSING", "Red") + '</td></tr>'
        '<tr><td>Domain events in code</td><td>Named events for traceability</td><td>' + status_macro("MISSING", "Red") + '</td></tr>'
        '<tr><td>Idempotency keys</td><td>Dedup on retry</td><td>' + status_macro("MISSING", "Red") + '</td></tr>'
        '<tr><td>Version protocol</td><td>Monotonic version per device</td><td>' + status_macro("MISSING", "Red") + '</td></tr>'
        '</table>'
    )

    sections.append("<h3>9.2 Typed Pusher Event Contracts</h3>")
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
        "interface PlaylistUpdatedEvent extends PusherEventBase {\n"
        "  type: 'playlist-updated'\n"
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
        "// ─── Union Type ───\n"
        "type PusherEvent =\n"
        "  | UpdatePlayScheduleEvent\n"
        "  | CreatedPlayScheduleEvent\n"
        "  | ApprovedExclusiveEvent\n"
        "  | StopAdvertisementEvent\n"
        "  | UnPairScreenEvent\n"
        "  | PlaylistUpdatedEvent\n"
        "  | DeviceConfigUpdatedEvent",
        "typescript", "Typed Pusher Event Contracts"
    ))

    sections.append("<h3>9.3 Domain Events (Internal Code-Level)</h3>")
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
        "/** Emitted: PlaylistBuilderService completes */\n"
        "interface DevicePlaylistBuilt {\n"
        "  type: 'DevicePlaylistBuilt'\n"
        "  device_code: string\n"
        "  playlist_id: number\n"
        "  version: number\n"
        "  tier: 'live' | 'buffer' | 'fallback'\n"
        "  item_count: number\n"
        "  timestamp: DateTime\n"
        "}\n\n"
        "/** Emitted: Player confirms media downloaded */\n"
        "interface MediaDownloadConfirmed {\n"
        "  type: 'MediaDownloadConfirmed'\n"
        "  device_code: string\n"
        "  media_codes: string[]\n"
        "  total_bytes: number\n"
        "  timestamp: DateTime\n"
        "}\n\n"
        "/** Emitted: Player sends play history batch */\n"
        "interface PlayHistoryReceived {\n"
        "  type: 'PlayHistoryReceived'\n"
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
        "}",
        "typescript", "Domain Events"
    ))

    sections.append("<h3>9.4 Event Flow Diagram</h3>")
    sections.append(mermaid_diagram(
        "flowchart TD\n"
        "    subgraph BE[\"BACKEND (AdonisJS)\"]\n"
        "        CRON[\"Cron\\n(BullMQ)\"] --> CALC[\"PlayScheduleCalc\\nPerScreen (BullMQ)\"]\n"
        "        CALC -->|\"PlayScheduleCalculated\\n(domain event)\"| PB[\"PlaylistBuilder\\nService\"]\n"
        "        PB --> DB[\"DB Write\\n(PG)\"]\n"
        "        PB -->|\"DevicePlaylistBuilt\\n(domain event)\"| PUSH[\"Pusher Push\\n(typed event)\"]\n"
        "        PH[\"Play History Endpoint\\n+ Idempotency Check (Redis)\\nPlayHistoryReceived event\"]\n"
        "    end\n"
        "    subgraph PL[\"PLAYER (Tauri)\"]\n"
        "        INB[\"Inbox Handler\\n+ event_id dedup\\n+ version check\"] --> FETCH[\"GET /v2/\\ndevice-playlist\"]\n"
        "        FETCH --> CACHE[\"3-Tier Cache\\n(local)\"]\n"
        "        CACHE --> SM[\"State Machine\\nBOOT→SYNC→PLAY\\n→OFFLINE→FALL\"]\n"
        "        OUT[\"Outbox Store\\n(Tauri Store)\\npending → sent → ack\"]\n"
        "    end\n"
        "    PUSH -->|\"Pusher WebSocket\\n(typed contract)\"| INB\n"
        "    OUT -->|\"Outbox flush (1 min)\\n+ X-Idempotency-Key\"| PH",
        page_id=page_id,
    ))

    sections.append("<h3>9.5 Decision Record: Why NOT Event-Sourcing</h3>")
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

    sections.append("<h3>9.6 Implementation Checklist</h3>")
    sections.append(success_panel(
        "<p><strong>What to formalize (ordered by priority):</strong></p>"
        "<ol>"
        "<li><strong>Typed Pusher event contracts</strong> &mdash; shared interfaces (backend + player)</li>"
        "<li><strong>Version protocol</strong> &mdash; monotonic <code>version</code> per device on every Pusher event</li>"
        "<li><strong>Outbox pattern</strong> &mdash; Tauri Store with UUID idempotency key + flush cycle</li>"
        "<li><strong>Inbox dedup</strong> &mdash; <code>event_id</code> tracking (last 100) + version gap detection</li>"
        "<li><strong>Backend idempotency</strong> &mdash; Redis <code>idem:{uuid}</code> check on play-history endpoint</li>"
        "<li><strong>Domain events (in-code)</strong> &mdash; named typed objects, passed between services, logged for observability</li>"
        "</ol>"
    ))

    return "\n".join(sections)


def main():
    dry_run = "--dry-run" in sys.argv

    # Parse --update PAGE_ID
    update_page_id = None
    if "--update" in sys.argv:
        idx = sys.argv.index("--update")
        if idx + 1 < len(sys.argv):
            update_page_id = sys.argv[idx + 1]
        else:
            print("Error: --update requires PAGE_ID argument")
            sys.exit(1)

    creds = load_credentials()
    api = ConfluenceAPI(
        base_url=creds["CONFLUENCE_URL"],
        auth_header=get_auth_header(
            creds["CONFLUENCE_USERNAME"], creds["CONFLUENCE_API_TOKEN"]
        ),
        ssl_context=create_ssl_context(),
    )

    pid = update_page_id or "165019751"
    content = build_content(page_id=pid)

    if dry_run:
        out = Path(__file__).parent.parent / "tasks" / "player-architecture-preview.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(content, encoding="utf-8")
        print(f"  DRY RUN — Preview saved to {out}")
        print(f"  Content length: {len(content)} chars")
        return

    if update_page_id:
        print(f"=== Updating Confluence page: {update_page_id} ===")
        page = api.get_page(update_page_id)
        version = page["version"]["number"]
        title = page["title"]
        api.update_page(
            page_id=update_page_id,
            title=title,
            content=content,
            version=version,
        )
        print(f"  Updated: {title} (v{version} -> v{version + 1})")
        print(f"  URL: https://{{JIRA_SITE}}/wiki/spaces/{SPACE_KEY}/pages/{update_page_id}")
    else:
        print(f"=== Creating Confluence page: {PAGE_TITLE} ===")
        result = api.create_page(
            space_key=SPACE_KEY,
            title=PAGE_TITLE,
            content=content,
            parent_id=PARENT_PAGE_ID,
        )
        page_id = result.get("id", "unknown")
        print(f"  Created page: {page_id}")
        print(f"  URL: https://{{JIRA_SITE}}/wiki/spaces/{SPACE_KEY}/pages/{page_id}")


if __name__ == "__main__":
    main()
