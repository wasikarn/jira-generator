"""SQLite-based cache for Jira data with FTS5 full-text search.

Provides structured caching with TTL expiration, full-text search on
issue summaries/descriptions, and ADF text extraction for indexing.

Usage:
    from lib.cache import JiraCache

    cache = JiraCache()  # Uses ~/.cache/jira-generator/jira.db
    cache.put_issue("BEP-123", issue_data)
    cached = cache.get_issue("BEP-123", max_age_hours=24)
    results = cache.text_search("coupon payment", limit=10)
"""

import hashlib
import json
import logging
import sqlite3
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

DEFAULT_DB_PATH = Path.home() / ".cache" / "jira-generator" / "jira.db"

SCHEMA_SQL = """
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;

CREATE TABLE IF NOT EXISTS issues (
    issue_key TEXT PRIMARY KEY,
    summary TEXT NOT NULL,
    status TEXT,
    assignee TEXT,
    issue_type TEXT,
    sprint_id INTEGER,
    parent_key TEXT,
    priority TEXT,
    labels TEXT,
    start_date TEXT,
    due_date TEXT,
    description_text TEXT,
    data TEXT NOT NULL,
    cached_at TEXT NOT NULL,
    accessed_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_issues_sprint ON issues(sprint_id);
CREATE INDEX IF NOT EXISTS idx_issues_parent ON issues(parent_key);
CREATE INDEX IF NOT EXISTS idx_issues_cached ON issues(cached_at);
CREATE INDEX IF NOT EXISTS idx_issues_status ON issues(status);
CREATE INDEX IF NOT EXISTS idx_issues_assignee ON issues(assignee);

CREATE TABLE IF NOT EXISTS sprints (
    sprint_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    state TEXT,
    start_date TEXT,
    end_date TEXT,
    goal TEXT,
    data TEXT NOT NULL,
    cached_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS searches (
    cache_key TEXT PRIMARY KEY,
    jql TEXT NOT NULL,
    fields TEXT NOT NULL,
    result_keys TEXT NOT NULL,
    total INTEGER,
    data TEXT NOT NULL,
    cached_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_searches_cached ON searches(cached_at);

CREATE TABLE IF NOT EXISTS cache_stats (
    key TEXT PRIMARY KEY,
    value INTEGER DEFAULT 0
);

INSERT OR IGNORE INTO cache_stats (key, value) VALUES ('hits', 0);
INSERT OR IGNORE INTO cache_stats (key, value) VALUES ('misses', 0);
"""

FTS_SCHEMA_SQL = """
CREATE VIRTUAL TABLE IF NOT EXISTS issues_fts USING fts5(
    issue_key UNINDEXED,
    summary,
    description_text,
    content=issues,
    content_rowid=rowid,
    tokenize='unicode61'
);

CREATE TRIGGER IF NOT EXISTS issues_fts_insert AFTER INSERT ON issues BEGIN
    INSERT INTO issues_fts(rowid, issue_key, summary, description_text)
    VALUES (new.rowid, new.issue_key, new.summary, new.description_text);
END;

CREATE TRIGGER IF NOT EXISTS issues_fts_delete AFTER DELETE ON issues BEGIN
    INSERT INTO issues_fts(issues_fts, rowid, issue_key, summary, description_text)
    VALUES ('delete', old.rowid, old.issue_key, old.summary, old.description_text);
END;

CREATE TRIGGER IF NOT EXISTS issues_fts_update AFTER UPDATE ON issues BEGIN
    INSERT INTO issues_fts(issues_fts, rowid, issue_key, summary, description_text)
    VALUES ('delete', old.rowid, old.issue_key, old.summary, old.description_text);
    INSERT INTO issues_fts(rowid, issue_key, summary, description_text)
    VALUES (new.rowid, new.issue_key, new.summary, new.description_text);
END;
"""


def extract_adf_text(adf: Any) -> str | None:
    """Extract plain text from ADF (Atlassian Document Format) JSON.

    Recursively walks the ADF tree, collecting text from text nodes.

    Args:
        adf: ADF document (dict) or None

    Returns:
        Concatenated text content, or None if no text found.
    """
    if not adf or not isinstance(adf, dict):
        return None

    parts: list[str] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            if node.get("type") == "text" and "text" in node:
                parts.append(node["text"])
            for key in ("content",):
                if key in node and isinstance(node[key], list):
                    for child in node[key]:
                        walk(child)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(adf)
    text = " ".join(parts).strip()
    return text if text else None


def _extract_field(data: dict, *path: str, default: Any = None) -> Any:
    """Safely extract a nested field from issue data."""
    current = data
    for key in path:
        if not isinstance(current, dict):
            return default
        current = current.get(key, default)
    return current


class JiraCache:
    """SQLite cache for Jira issues with FTS5 full-text search.

    Attributes:
        db_path: Path to SQLite database file.
        conn: SQLite connection.
    """

    def __init__(self, db_path: Path | str | None = None) -> None:
        self.db_path = Path(db_path) if db_path else DEFAULT_DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._lock = threading.Lock()
        self._init_schema()
        logger.debug("JiraCache initialized at %s", self.db_path)

    def _init_schema(self) -> None:
        """Create tables and indexes."""
        self.conn.executescript(SCHEMA_SQL)
        try:
            self.conn.executescript(FTS_SCHEMA_SQL)
        except sqlite3.OperationalError as e:
            # FTS5 triggers may already exist — safe to ignore
            if "already exists" not in str(e):
                logger.warning("FTS5 setup warning: %s", e)
        self.conn.commit()

    # --- Issue Operations ---

    def get_issue(self, issue_key: str, max_age_hours: float = 24.0) -> dict | None:
        """Get cached issue if fresh enough.

        Args:
            issue_key: Jira issue key (e.g., 'BEP-123')
            max_age_hours: Maximum age in hours before considered stale

        Returns:
            Full issue JSON data, or None if not cached or stale.
        """
        row = self.conn.execute(
            "SELECT data, cached_at FROM issues WHERE issue_key = ?",
            (issue_key,),
        ).fetchone()

        if not row:
            self._incr_stat("misses")
            return None

        cached_at = datetime.fromisoformat(row["cached_at"])
        if datetime.now() - cached_at > timedelta(hours=max_age_hours):
            self._incr_stat("misses")
            return None

        # Update access time
        self.conn.execute(
            "UPDATE issues SET accessed_at = ? WHERE issue_key = ?",
            (datetime.now().isoformat(), issue_key),
        )
        self.conn.commit()
        self._incr_stat("hits")
        return json.loads(row["data"])

    def put_issue(self, issue_key: str, data: dict) -> None:
        """Store issue in cache, updating FTS5 index automatically.

        Args:
            issue_key: Jira issue key
            data: Full issue JSON from Jira API
        """
        fields = data.get("fields", {})
        description_text = extract_adf_text(fields.get("description"))

        # Extract sprint_id from custom field (can be list or dict)
        sprint_id = None
        sprint_data = fields.get("customfield_10020")
        if isinstance(sprint_data, list) and sprint_data:
            first = sprint_data[0]
            sprint_id = first.get("id") if isinstance(first, dict) else first
        elif isinstance(sprint_data, dict):
            sprint_id = sprint_data.get("id")

        now = datetime.now().isoformat()
        with self._lock:
            self.conn.execute(
                """INSERT OR REPLACE INTO issues
                (issue_key, summary, status, assignee, issue_type, sprint_id,
                 parent_key, priority, labels, start_date, due_date,
                 description_text, data, cached_at, accessed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    issue_key,
                    fields.get("summary", ""),
                    _extract_field(fields, "status", "name"),
                    _extract_field(fields, "assignee", "displayName"),
                    _extract_field(fields, "issuetype", "name"),
                    sprint_id,
                    _extract_field(fields, "parent", "key"),
                    _extract_field(fields, "priority", "name"),
                    json.dumps(fields.get("labels", [])),
                    fields.get("customfield_10015"),
                    fields.get("duedate"),
                    description_text,
                    json.dumps(data),
                    now,
                    now,
                ),
            )
            self.conn.commit()
        logger.debug("Cached issue %s", issue_key)

    def put_issues_batch(self, issues: list[dict]) -> int:
        """Bulk insert issues for cache warming.

        Args:
            issues: List of issue dicts from Jira API

        Returns:
            Number of issues cached.
        """
        count = 0
        for issue_data in issues:
            key = issue_data.get("key")
            if key:
                self.put_issue(key, issue_data)
                count += 1
        return count

    # --- Sprint Operations ---

    def get_sprint(self, sprint_id: int, max_age_hours: float = 4.0) -> dict | None:
        """Get cached sprint metadata."""
        row = self.conn.execute(
            "SELECT data, cached_at FROM sprints WHERE sprint_id = ?",
            (sprint_id,),
        ).fetchone()

        if not row:
            return None

        cached_at = datetime.fromisoformat(row["cached_at"])
        if datetime.now() - cached_at > timedelta(hours=max_age_hours):
            return None

        return json.loads(row["data"])

    def put_sprint(self, sprint_id: int, data: dict) -> None:
        """Store sprint metadata in cache."""
        with self._lock:
            self.conn.execute(
                """INSERT OR REPLACE INTO sprints
                (sprint_id, name, state, start_date, end_date, goal, data, cached_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    sprint_id,
                    data.get("name", ""),
                    data.get("state"),
                    data.get("startDate"),
                    data.get("endDate"),
                    data.get("goal"),
                    json.dumps(data),
                    datetime.now().isoformat(),
                ),
            )
            self.conn.commit()

    # --- Search Cache ---

    def get_search(self, jql: str, fields: str, limit: int, max_age_hours: float = 2.0) -> dict | None:
        """Get cached search results."""
        cache_key = self._search_key(jql, fields, limit)
        row = self.conn.execute(
            "SELECT data, cached_at FROM searches WHERE cache_key = ?",
            (cache_key,),
        ).fetchone()

        if not row:
            return None

        cached_at = datetime.fromisoformat(row["cached_at"])
        if datetime.now() - cached_at > timedelta(hours=max_age_hours):
            return None

        self._incr_stat("hits")
        return json.loads(row["data"])

    def put_search(self, jql: str, fields: str, limit: int, data: dict) -> None:
        """Store search results and cache individual issues."""
        cache_key = self._search_key(jql, fields, limit)
        issues = data.get("issues", [])
        result_keys = [i.get("key", "") for i in issues]

        with self._lock:
            self.conn.execute(
                """INSERT OR REPLACE INTO searches
                (cache_key, jql, fields, result_keys, total, data, cached_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    cache_key,
                    jql,
                    fields,
                    json.dumps(result_keys),
                    data.get("total", len(issues)),
                    json.dumps(data),
                    datetime.now().isoformat(),
                ),
            )
            self.conn.commit()

        # Also cache individual issues
        self.put_issues_batch(issues)

    # --- Full-Text Search ---

    def text_search(self, query: str, limit: int = 10) -> list[dict]:
        """FTS5 keyword search on cached issues.

        Args:
            query: Search query (supports FTS5 syntax like "coupon AND payment")
            limit: Maximum results

        Returns:
            List of matching issue data dicts, or empty list on FTS5 syntax error.
        """
        try:
            rows = self.conn.execute(
                """SELECT i.data FROM issues i
                JOIN issues_fts fts ON i.rowid = fts.rowid
                WHERE issues_fts MATCH ?
                ORDER BY rank
                LIMIT ?""",
                (query, limit),
            ).fetchall()
            return [json.loads(row["data"]) for row in rows]
        except sqlite3.OperationalError as e:
            logger.warning("FTS5 query error for '%s': %s", query[:50], e)
            return []

    # --- Invalidation ---

    def invalidate_issue(self, issue_key: str) -> bool:
        """Remove an issue from cache."""
        with self._lock:
            cursor = self.conn.execute(
                "DELETE FROM issues WHERE issue_key = ?", (issue_key,)
            )
            self.conn.commit()
        return cursor.rowcount > 0

    def invalidate_sprint(self, sprint_id: int) -> int:
        """Remove all issues for a sprint and the sprint itself."""
        with self._lock:
            cursor = self.conn.execute(
                "DELETE FROM issues WHERE sprint_id = ?", (sprint_id,)
            )
            self.conn.execute(
                "DELETE FROM sprints WHERE sprint_id = ?", (sprint_id,)
            )
            self.conn.commit()
        return cursor.rowcount

    def invalidate_all(self) -> None:
        """Clear entire cache."""
        with self._lock:
            self.conn.execute("DELETE FROM issues")
            self.conn.execute("DELETE FROM sprints")
            self.conn.execute("DELETE FROM searches")
            self.conn.commit()
        logger.info("Cache cleared")

    # --- Statistics ---

    def get_stats(self) -> dict:
        """Cache statistics: counts, size, hit rate."""
        issue_count = self.conn.execute(
            "SELECT COUNT(*) FROM issues"
        ).fetchone()[0]
        sprint_count = self.conn.execute(
            "SELECT COUNT(*) FROM sprints"
        ).fetchone()[0]
        search_count = self.conn.execute(
            "SELECT COUNT(*) FROM searches"
        ).fetchone()[0]

        oldest = self.conn.execute(
            "SELECT MIN(cached_at) FROM issues"
        ).fetchone()[0]
        newest = self.conn.execute(
            "SELECT MAX(cached_at) FROM issues"
        ).fetchone()[0]

        hits = self._get_stat("hits")
        misses = self._get_stat("misses")
        total = hits + misses

        db_size_mb = self.db_path.stat().st_size / (1024 * 1024) if self.db_path.exists() else 0

        return {
            "issues_cached": issue_count,
            "sprints_cached": sprint_count,
            "searches_cached": search_count,
            "hits": hits,
            "misses": misses,
            "hit_rate": f"{hits / total * 100:.1f}%" if total > 0 else "N/A",
            "db_size_mb": round(db_size_mb, 2),
            "oldest_entry": oldest,
            "newest_entry": newest,
            "db_path": str(self.db_path),
        }

    def vacuum(self) -> None:
        """Optimize database (reclaim space)."""
        self.conn.execute("VACUUM")
        self.conn.execute("ANALYZE")

    # --- Internal ---

    def _search_key(self, jql: str, fields: str, limit: int) -> str:
        raw = f"{jql}|{fields}|{limit}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def _incr_stat(self, key: str) -> None:
        self.conn.execute(
            "UPDATE cache_stats SET value = value + 1 WHERE key = ?", (key,)
        )
        self.conn.commit()

    def _get_stat(self, key: str) -> int:
        row = self.conn.execute(
            "SELECT value FROM cache_stats WHERE key = ?", (key,)
        ).fetchone()
        return row[0] if row else 0

    def close(self) -> None:
        """Close database connection."""
        self.conn.close()
