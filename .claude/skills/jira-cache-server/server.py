# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "mcp>=1.0.0",
#     "sqlite-vec>=0.1.1",
#     "sentence-transformers>=2.2.0",
# ]
# ///
"""MCP server for Jira data caching with FTS5 and vector search.

Provides 8 tools for cached Jira data access:
- cache_get_issue: Get issue (cache-first, upstream fallback)
- cache_search: JQL search with caching
- cache_sprint_issues: Sprint issues with caching
- cache_text_search: FTS5 keyword search on cached issues
- cache_similar_issues: Semantic similarity via embeddings
- cache_refresh: Force-refresh from upstream
- cache_stats: Cache statistics
- cache_invalidate: Clear cache entries

Runs as stdio MCP server for Claude Code integration.

Usage:
    uv run server.py
"""

import json
import logging
import sys
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

# Add atlassian-scripts to path for JiraAPI + auth reuse
_scripts_dir = Path(__file__).resolve().parent.parent / "atlassian-scripts"
if str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))

from lib.auth import create_ssl_context, get_auth_header, load_credentials
from lib.jira_api import JiraAPI, derive_jira_url

# Local imports (jira_cache to avoid namespace collision with atlassian-scripts/lib)
from jira_cache.cache import JiraCache
from jira_cache.embeddings import EmbeddingStore

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("jira-cache-server")

# Claude Code MCP token limit is ~30K chars; keep well under
MAX_RESPONSE_CHARS = 25_000

# --- Globals (initialized on startup) ---
cache: JiraCache | None = None
embeddings: EmbeddingStore | None = None
jira_api: JiraAPI | None = None

TOOLS = [
    Tool(
        name="cache_get_issue",
        description="Get a Jira issue by key. Returns cached data if fresh, otherwise fetches from Jira REST API and caches the result. Specify fields to control which Jira fields are returned from upstream.",
        inputSchema={
            "type": "object",
            "properties": {
                "issue_key": {"type": "string", "description": "Jira issue key (e.g., BEP-123)"},
                "fields": {"type": "string", "description": "Comma-separated fields for upstream fetch (default: summary,status,assignee,issuetype,priority,labels,parent,description)", "default": "summary,status,assignee,issuetype,priority,labels,parent,description"},
                "max_age_hours": {"type": "number", "description": "Max cache age in hours (default: 24)", "default": 24},
                "force_refresh": {"type": "boolean", "description": "Skip cache and fetch from Jira upstream, then update cache (default: false)", "default": False},
            },
            "required": ["issue_key"],
        },
    ),
    Tool(
        name="cache_search",
        description="Search Jira issues via JQL. Returns cached results if same query was recently run, otherwise fetches from Jira REST API. Always use fields and limit params to control response size.",
        inputSchema={
            "type": "object",
            "properties": {
                "jql": {"type": "string", "description": "JQL query string"},
                "fields": {"type": "string", "description": "Comma-separated fields (default: summary,status,assignee,issuetype,priority)", "default": "summary,status,assignee,issuetype,priority"},
                "limit": {"type": "integer", "description": "Max results (default: 30, max: 50)", "default": 30},
                "max_age_hours": {"type": "number", "description": "Max cache age in hours (default: 2)", "default": 2},
                "force_refresh": {"type": "boolean", "description": "Skip cache and fetch from Jira upstream, then update cache (default: false)", "default": False},
                "start_at": {"type": "integer", "description": "Response offset for pagination. Use when previous response had has_more=true (default: 0)", "default": 0},
            },
            "required": ["jql"],
        },
    ),
    Tool(
        name="cache_sprint_issues",
        description="Get all issues in a sprint. Uses Jira Agile API with caching. Good for sprint overviews and capacity planning.",
        inputSchema={
            "type": "object",
            "properties": {
                "sprint_id": {"type": ["integer", "string"], "description": "Jira sprint ID (e.g., 123)"},
                "fields": {"type": "string", "description": "Comma-separated fields (default: summary,status,assignee,issuetype,priority,labels)", "default": "summary,status,assignee,issuetype,priority,labels"},
                "max_age_hours": {"type": "number", "description": "Max cache age in hours (default: 2)", "default": 2},
                "force_refresh": {"type": "boolean", "description": "Skip cache and fetch from Jira upstream, then update cache (default: false)", "default": False},
                "start_at": {"type": "integer", "description": "Response offset for pagination. Use when previous response had has_more=true (default: 0)", "default": 0},
            },
            "required": ["sprint_id"],
        },
    ),
    Tool(
        name="cache_text_search",
        description="Full-text keyword search on cached Jira issues using FTS5. Searches summary and description text. No upstream call — only returns previously cached issues.",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search keywords (supports FTS5 syntax: AND, OR, NOT, quotes for phrases)"},
                "limit": {"type": "integer", "description": "Max results (default: 10)", "default": 10},
            },
            "required": ["query"],
        },
    ),
    Tool(
        name="cache_similar_issues",
        description="Find semantically similar issues using vector embeddings. Requires sqlite-vec and sentence-transformers. Returns issues ranked by cosine similarity.",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Text to find similar issues for"},
                "limit": {"type": "integer", "description": "Max results (default: 5)", "default": 5},
                "exclude_keys": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Issue keys to exclude from results",
                    "default": [],
                },
            },
            "required": ["query"],
        },
    ),
    Tool(
        name="cache_refresh",
        description="Force-refresh issue(s) from Jira upstream, ignoring cache. Use after making changes to issues or when cache is stale.",
        inputSchema={
            "type": "object",
            "properties": {
                "issue_keys": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Issue keys to refresh (e.g., ['BEP-123', 'BEP-456'])",
                },
                "sprint_id": {"type": "integer", "description": "Refresh all issues in this sprint (alternative to issue_keys)"},
            },
        },
    ),
    Tool(
        name="cache_stats",
        description="Get cache statistics: issue count, hit/miss rate, database size, oldest/newest entries.",
        inputSchema={
            "type": "object",
            "properties": {},
        },
    ),
    Tool(
        name="cache_invalidate",
        description="Clear cache entries. Can invalidate specific issues, a sprint, or the entire cache.",
        inputSchema={
            "type": "object",
            "properties": {
                "issue_key": {"type": "string", "description": "Invalidate a specific issue"},
                "sprint_id": {"type": "integer", "description": "Invalidate all issues in a sprint"},
                "all": {"type": "boolean", "description": "Clear entire cache", "default": False},
            },
        },
    ),
]


def _init() -> None:
    """Initialize cache, embeddings, and upstream API client."""
    global cache, embeddings, jira_api

    cache = JiraCache()
    embeddings = EmbeddingStore(cache.conn)

    try:
        creds = load_credentials()
        jira_url = derive_jira_url(creds["CONFLUENCE_URL"])
        auth_header = get_auth_header(creds["CONFLUENCE_USERNAME"], creds["CONFLUENCE_API_TOKEN"])
        ssl_ctx = create_ssl_context()
        jira_api = JiraAPI(base_url=jira_url, auth_header=auth_header, ssl_context=ssl_ctx)
        logger.info("Initialized: cache=%s, embeddings=%s, upstream=%s", cache.db_path, embeddings.available, jira_url)
    except Exception as e:
        logger.error("Failed to init upstream API (cache-only mode): %s", e)
        jira_api = None


def _format_issue_summary(issue: dict) -> str:
    """Format issue data for compact MCP response."""
    fields = issue.get("fields", {})
    key = issue.get("key", "?")
    summary = fields.get("summary", "")
    status = fields.get("status", {})
    status_name = status.get("name", "") if isinstance(status, dict) else str(status)
    assignee = fields.get("assignee", {})
    assignee_name = assignee.get("displayName", "Unassigned") if isinstance(assignee, dict) else str(assignee or "Unassigned")
    issue_type = fields.get("issuetype", {})
    type_name = issue_type.get("name", "") if isinstance(issue_type, dict) else str(issue_type)

    return f"[{key}] ({type_name}) {summary} | {status_name} | {assignee_name}"


# --- Response size management (tiered: strip → paginate → compact) ---

# Level 1: Fields that are never useful to Claude (API URLs, avatars, internal IDs)
_NOISE_FIELDS = frozenset({
    "self",            # REST API URL on every object
    "avatarUrls",      # 4 avatar size URLs per user
    "accountId",       # Internal Jira account ID
    "accountType",     # "atlassian" etc
    "emailAddress",    # Privacy; use displayName instead
    "timeZone",        # User timezone
    "active",          # User active status
    "iconUrl",         # Status/priority icon URLs
    "statusCategory",  # Redundant (use status.name)
    "expand",          # Jira API metadata
    "hierarchyLevel",  # Redundant issuetype metadata
    "subtask",         # Redundant boolean (use issuetype)
    "entityId",        # Internal entity ID
    "scope",           # Project scope details
})


def _strip_noise(obj: Any) -> Any:
    """Recursively strip noise fields from Jira response objects."""
    if isinstance(obj, dict):
        return {k: _strip_noise(v) for k, v in obj.items() if k not in _NOISE_FIELDS}
    if isinstance(obj, list):
        return [_strip_noise(item) for item in obj]
    return obj


def _strip_response_noise(result_json: str) -> str:
    """Level 1: Strip Jira metadata noise from JSON response."""
    try:
        data = json.loads(result_json)
    except (json.JSONDecodeError, TypeError):
        return result_json
    stripped = _strip_noise(data)
    return json.dumps(stripped, ensure_ascii=False)


def _find_issues_list(data: dict) -> tuple[list | None, dict | None, str | None]:
    """Find the issues array in common response shapes."""
    for parent_key in ("results", None):
        container = data.get(parent_key) if parent_key else data
        if isinstance(container, dict):
            for k in ("issues", "data"):
                if isinstance(container.get(k), list):
                    return container[k], container, k
    return None, None, None


def _paginate_response(result_json: str) -> str:
    """Level 2: Return a subset of issues that fits within MAX_RESPONSE_CHARS."""
    try:
        data = json.loads(result_json)
    except (json.JSONDecodeError, TypeError):
        return result_json[:MAX_RESPONSE_CHARS] + "\n... (truncated)"

    issues, parent, key = _find_issues_list(data)
    if issues is None:
        return result_json[:MAX_RESPONSE_CHARS] + "\n... (truncated)"

    total = len(issues)
    # Estimate how many issues fit based on average size
    avg_size = len(result_json) / max(total, 1)
    fits = max(1, int((MAX_RESPONSE_CHARS - 500) / avg_size))  # 500 for metadata overhead
    fits = min(fits, total)

    parent[key] = issues[:fits]
    data["_pagination"] = {
        "total": total,
        "returned": fits,
        "has_more": fits < total,
        "next_offset": fits,
        "hint": f"Call again with start_at={fits} to get next page",
    }

    result = json.dumps(data, ensure_ascii=False)
    # Safety: halve if still too large
    while len(result) > MAX_RESPONSE_CHARS and fits > 1:
        fits = fits // 2
        parent[key] = issues[:fits]
        data["_pagination"].update({"returned": fits, "next_offset": fits, "has_more": True})
        result = json.dumps(data, ensure_ascii=False)

    return result


def _compact_response(result_json: str) -> str:
    """Level 3 (last resort): Replace full issues with minimal summaries."""
    try:
        data = json.loads(result_json)
    except (json.JSONDecodeError, TypeError):
        return result_json[:MAX_RESPONSE_CHARS] + "\n... (truncated)"

    issues, parent, key = _find_issues_list(data)
    if issues is None:
        return result_json[:MAX_RESPONSE_CHARS] + "\n... (truncated)"

    compact_issues = []
    for issue in issues:
        if isinstance(issue, dict) and "fields" in issue:
            fields = issue["fields"]
            compact = {
                "key": issue.get("key", "?"),
                "summary": fields.get("summary", ""),
                "status": fields.get("status", {}).get("name", "") if isinstance(fields.get("status"), dict) else str(fields.get("status", "")),
                "assignee": fields.get("assignee", {}).get("displayName", "Unassigned") if isinstance(fields.get("assignee"), dict) else str(fields.get("assignee") or "Unassigned"),
                "issuetype": fields.get("issuetype", {}).get("name", "") if isinstance(fields.get("issuetype"), dict) else str(fields.get("issuetype", "")),
            }
            if "priority" in fields:
                p = fields["priority"]
                compact["priority"] = p.get("name", "") if isinstance(p, dict) else str(p)
            if "labels" in fields:
                compact["labels"] = fields["labels"]
            if "parent" in fields:
                p = fields["parent"]
                compact["parent"] = p.get("key", "") if isinstance(p, dict) else str(p)
            compact_issues.append(compact)
        else:
            compact_issues.append(issue)

    parent[key] = compact_issues
    data["_compacted"] = True
    data["_original_chars"] = len(result_json)
    return json.dumps(data, ensure_ascii=False)


# --- Tool Handlers ---


async def handle_cache_get_issue(args: dict) -> str:
    """Get issue: cache-first with upstream fallback."""
    issue_key = args["issue_key"]
    fields = args.get("fields", "summary,status,assignee,issuetype,priority,labels,parent,description")
    max_age = args.get("max_age_hours") or cache.get_adaptive_ttl(issue_key)
    force_refresh = args.get("force_refresh", False)

    # Try cache first (skip if force_refresh)
    if not force_refresh:
        cached = cache.get_issue(issue_key, max_age_hours=max_age)
        if cached:
            logger.info("Cache HIT: %s", issue_key)
            return json.dumps({"source": "cache", "issue": cached}, ensure_ascii=False)

    # Cache miss or force_refresh — fetch upstream
    if not jira_api:
        return json.dumps({"error": "Issue not in cache and upstream API not available"})

    logger.info("Cache %s: %s — fetching upstream", "REFRESH" if force_refresh else "MISS", issue_key)
    try:
        issue = jira_api.get_issue(issue_key, fields=fields)
        cache.put_issue(issue_key, issue)
        if embeddings and embeddings.available:
            f = issue.get("fields", {})
            text = f"{f.get('summary', '')} {f.get('description', '') if isinstance(f.get('description'), str) else ''}"
            embeddings.store_embedding(issue_key, text[:500])
        return json.dumps({"source": "upstream", "issue": issue}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"Failed to fetch {issue_key}: {e}"})


async def handle_cache_search(args: dict) -> str:
    """JQL search with caching."""
    jql = args["jql"]
    fields = args.get("fields", "summary,status,assignee,issuetype,priority")
    limit = min(int(args.get("limit", 30)), 50)
    max_age = args.get("max_age_hours", 2)
    force_refresh = args.get("force_refresh", False)
    start_at = int(args.get("start_at", 0))

    source = "cache"
    results = None

    # Try cache (skip if force_refresh)
    if not force_refresh:
        cached = cache.get_search(jql, fields, limit, max_age_hours=max_age)
        if cached:
            logger.info("Search cache HIT: %s", jql[:60])
            results = cached

    # Cache miss or force_refresh — fetch upstream
    if results is None:
        if not jira_api:
            return json.dumps({"error": "Search not in cache and upstream API not available"})

        logger.info("Search cache MISS: %s — fetching upstream", jql[:60])
        try:
            results = jira_api.search_issues(jql, fields=fields, max_results=limit)
            cache.put_search(jql, fields, limit, results)
            if embeddings and embeddings.available:
                embeddings.store_batch(results.get("issues", []))
            source = "upstream"
        except Exception as e:
            return json.dumps({"error": f"Search failed: {e}"})

    # Apply response-level offset (pagination page 2+)
    if start_at > 0:
        issues = results.get("issues", [])
        results = {**results, "issues": issues[start_at:], "startAt": start_at}

    return json.dumps({"source": source, "results": results}, ensure_ascii=False)


async def handle_cache_sprint_issues(args: dict) -> str:
    """Get sprint issues with caching."""
    sprint_id = int(args["sprint_id"])
    fields = args.get("fields", "summary,status,assignee,issuetype,priority,labels")
    max_age = args.get("max_age_hours", 2)
    force_refresh = args.get("force_refresh", False)
    response_offset = int(args.get("start_at", 0))

    source = "cache"
    results = None

    # Use JQL-based search cache (sprint issues = search query)
    jql = f"sprint = {sprint_id}"
    if not force_refresh:
        cached = cache.get_search(jql, fields, 50, max_age_hours=max_age)
        if cached:
            logger.info("Sprint cache HIT: %d", sprint_id)
            results = cached

    if results is None:
        if not jira_api:
            return json.dumps({"error": "Sprint not in cache and upstream API not available"})

        logger.info("Sprint cache MISS: %d — fetching upstream", sprint_id)
        try:
            all_issues: list[dict] = []
            upstream_offset = 0
            while True:
                page = jira_api.get_sprint_issues(sprint_id, fields=fields, max_results=50, start_at=upstream_offset)
                issues = page.get("issues", [])
                all_issues.extend(issues)
                if upstream_offset + len(issues) >= page.get("total", 0):
                    break
                upstream_offset += len(issues)

            results = {"issues": all_issues, "total": len(all_issues)}
            cache.put_search(jql, fields, 50, results)
            if embeddings and embeddings.available:
                embeddings.store_batch(all_issues)
            source = "upstream"
        except Exception as e:
            return json.dumps({"error": f"Sprint fetch failed: {e}"})

    # Apply response-level offset (pagination page 2+)
    if response_offset > 0:
        issues = results.get("issues", [])
        results = {**results, "issues": issues[response_offset:], "startAt": response_offset}

    return json.dumps({"source": source, "results": results}, ensure_ascii=False)


async def handle_cache_text_search(args: dict) -> str:
    """FTS5 keyword search on cached issues."""
    query = args["query"]
    limit = args.get("limit", 10)

    results = cache.text_search(query, limit=limit)
    summaries = [_format_issue_summary(r) for r in results]

    return json.dumps({
        "source": "fts5",
        "count": len(results),
        "issues": summaries,
        "data": results,
    }, ensure_ascii=False)


async def handle_cache_similar_issues(args: dict) -> str:
    """Semantic similarity search via embeddings."""
    if not embeddings or not embeddings.available:
        return json.dumps({"error": "Embeddings not available (install sqlite-vec and sentence-transformers)"})

    query = args["query"]
    limit = args.get("limit", 5)
    exclude = args.get("exclude_keys", [])

    similar = embeddings.find_similar(query, limit=limit, exclude_keys=exclude)

    # Enrich with issue data from cache
    enriched = []
    for item in similar:
        issue = cache.get_issue(item["issue_key"], max_age_hours=9999)
        if issue:
            enriched.append({
                **item,
                "summary": _format_issue_summary(issue),
            })
        else:
            enriched.append(item)

    return json.dumps({
        "source": "embeddings",
        "count": len(enriched),
        "results": enriched,
    }, ensure_ascii=False)


async def handle_cache_refresh(args: dict) -> str:
    """Force-refresh from upstream."""
    if not jira_api:
        return json.dumps({"error": "Upstream API not available"})

    refreshed = []

    # Refresh specific issues
    issue_keys = args.get("issue_keys", [])
    for key in issue_keys:
        try:
            issue = jira_api.get_issue(key)
            cache.put_issue(key, issue)
            if embeddings and embeddings.available:
                f = issue.get("fields", {})
                text = f"{f.get('summary', '')}"[:500]
                embeddings.store_embedding(key, text)
            refreshed.append(key)
        except Exception as e:
            logger.error("Failed to refresh %s: %s", key, e)

    # Refresh sprint
    sprint_id = args.get("sprint_id")
    if sprint_id:
        try:
            cache.invalidate_sprint(sprint_id)
            start_at = 0
            while True:
                page = jira_api.get_sprint_issues(sprint_id, max_results=50, start_at=start_at)
                issues = page.get("issues", [])
                cache.put_issues_batch(issues)
                if embeddings and embeddings.available:
                    embeddings.store_batch(issues)
                refreshed.extend(i.get("key", "") for i in issues)
                if start_at + len(issues) >= page.get("total", 0):
                    break
                start_at += len(issues)
        except Exception as e:
            logger.error("Failed to refresh sprint %d: %s", sprint_id, e)

    return json.dumps({"refreshed": len(refreshed), "keys": refreshed})


async def handle_cache_stats(args: dict) -> str:
    """Cache statistics."""
    stats = cache.get_stats()
    if embeddings:
        stats["embeddings_count"] = embeddings.count()
        stats["embeddings_available"] = embeddings.available
    return json.dumps(stats, ensure_ascii=False)


async def handle_cache_invalidate(args: dict) -> str:
    """Cache invalidation."""
    if args.get("all"):
        cache.invalidate_all()
        return json.dumps({"invalidated": "all"})

    issue_key = args.get("issue_key")
    if issue_key:
        removed = cache.invalidate_issue(issue_key)
        if embeddings:
            embeddings.remove_embedding(issue_key)
        return json.dumps({"invalidated": issue_key, "found": removed})

    sprint_id = args.get("sprint_id")
    if sprint_id:
        count = cache.invalidate_sprint(sprint_id)
        return json.dumps({"invalidated_sprint": sprint_id, "issues_removed": count})

    return json.dumps({"error": "Specify issue_key, sprint_id, or all=true"})


# --- Handler dispatch ---

HANDLERS = {
    "cache_get_issue": handle_cache_get_issue,
    "cache_search": handle_cache_search,
    "cache_sprint_issues": handle_cache_sprint_issues,
    "cache_text_search": handle_cache_text_search,
    "cache_similar_issues": handle_cache_similar_issues,
    "cache_refresh": handle_cache_refresh,
    "cache_stats": handle_cache_stats,
    "cache_invalidate": handle_cache_invalidate,
}


async def main() -> None:
    """Run MCP server over stdio."""
    _init()

    server = Server("jira-cache-server")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return TOOLS

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
        handler = HANDLERS.get(name)
        if not handler:
            return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]

        try:
            result = await handler(arguments)

            # Tiered response size management
            if len(result) > MAX_RESPONSE_CHARS:
                # Level 1: Strip Jira metadata noise
                result = _strip_response_noise(result)
                logger.info("L1 strip: %d chars for %s", len(result), name)

            if len(result) > MAX_RESPONSE_CHARS:
                # Level 2: Paginate (return subset with has_more)
                logger.warning("L2 paginate: %d chars for %s", len(result), name)
                result = _paginate_response(result)

            if len(result) > MAX_RESPONSE_CHARS:
                # Level 3: Compact (replace issues with minimal summaries)
                logger.warning("L3 compact: %d chars for %s", len(result), name)
                result = _compact_response(result)

            return [TextContent(type="text", text=result)]
        except Exception as e:
            logger.exception("Tool %s failed", name)
            return [TextContent(type="text", text=json.dumps({"error": str(e)}))]

    logger.info("Starting jira-cache-server (stdio)")
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
