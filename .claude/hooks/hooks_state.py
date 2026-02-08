"""Shared session state for Claude hooks.

Single state file per session at /tmp/claude-hooks-state/{session_id}.json.
Used by HR6 (cache invalidation), HR7 (sprint lookup), and search tracking.
"""
import json
from pathlib import Path

STATE_DIR = Path("/tmp/claude-hooks-state")


def _state_file(session_id: str) -> Path:
    return STATE_DIR / f"{session_id or 'default'}.json"


def _load(session_id: str) -> dict:
    f = _state_file(session_id)
    try:
        return json.loads(f.read_text()) if f.exists() else {}
    except Exception:
        return {}


def _save(session_id: str, state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    _state_file(session_id).write_text(json.dumps(state))


# ── HR6: Cache invalidation tracking ──────────────────

def hr6_add_pending(session_id: str, key: str) -> None:
    state = _load(session_id)
    pending = set(state.get("hr6_pending", []))
    pending.add(key)
    state["hr6_pending"] = sorted(pending)
    _save(session_id, state)


def hr6_remove_pending(session_id: str, key: str) -> None:
    state = _load(session_id)
    pending = set(state.get("hr6_pending", []))
    pending.discard(key)
    state["hr6_pending"] = sorted(pending)
    _save(session_id, state)


def hr6_get_pending(session_id: str) -> set[str]:
    return set(_load(session_id).get("hr6_pending", []))


# ── HR7: Sprint lookup tracking ───────────────────────

def hr7_mark_lookup_done(session_id: str) -> None:
    state = _load(session_id)
    state["hr7_lookup_done"] = True
    _save(session_id, state)


def hr7_is_lookup_done(session_id: str) -> bool:
    return _load(session_id).get("hr7_lookup_done", False)


# ── Search tracking ───────────────────────────────────

def search_mark_done(session_id: str) -> None:
    state = _load(session_id)
    state["search_done"] = True
    _save(session_id, state)


def search_is_done(session_id: str) -> bool:
    return _load(session_id).get("search_done", False)
