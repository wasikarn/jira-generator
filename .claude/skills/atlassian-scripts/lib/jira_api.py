"""Jira REST API v3 client for ADF description manipulation.

This module provides a class-based API client for Jira operations:
- Get issue with ADF description
- Update issue description (preserving ADF formatting)
- Walk and replace text in ADF tree

Uses REST API v3 which returns/accepts ADF (Atlassian Document Format),
preserving all formatting (panels, tables, marks, etc.)

Usage:
    from lib.jira_api import JiraAPI, derive_jira_url
    from lib.auth import create_ssl_context, load_credentials, get_auth_header

    creds = load_credentials()
    api = JiraAPI(
        base_url=derive_jira_url(creds["CONFLUENCE_URL"]),
        auth_header=get_auth_header(creds["CONFLUENCE_USERNAME"], creds["CONFLUENCE_API_TOKEN"]),
        ssl_context=create_ssl_context()
    )

    issue = api.get_issue("BEP-2819")
    description = issue["fields"]["description"]
    # ... modify ADF ...
    api.update_description("BEP-2819", modified_description)
"""

import json
import logging
import ssl
import urllib.error
import urllib.request
from copy import deepcopy
from typing import Any

from .exceptions import APIError, IssueNotFoundError

logger = logging.getLogger(__name__)


def derive_jira_url(confluence_url: str) -> str:
    """Derive Jira base URL from Confluence URL.

    Strips '/wiki' suffix from Confluence URL to get the Atlassian site URL.

    Args:
        confluence_url: Confluence wiki URL (e.g., https://example.atlassian.net/wiki)

    Returns:
        Jira base URL (e.g., https://example.atlassian.net)
    """
    return confluence_url.rstrip("/").removesuffix("/wiki")


def walk_and_replace(node: Any, replacements: list[tuple[str, str]]) -> int:
    """Walk ADF tree and replace text in text nodes.

    Recursively traverses the ADF JSON structure, finding text nodes
    and applying find/replace operations.

    Args:
        node: ADF node (dict or list)
        replacements: List of (find, replace) tuples

    Returns:
        Number of text replacements made.
    """
    changes = 0
    if isinstance(node, dict):
        if node.get("type") == "text" and "text" in node:
            for old, new in replacements:
                if old in node["text"]:
                    node["text"] = node["text"].replace(old, new)
                    changes += 1
        for key in ("content", "attrs"):
            if key in node and isinstance(node[key], (list, dict)):
                changes += walk_and_replace(node[key], replacements)
    elif isinstance(node, list):
        for item in node:
            changes += walk_and_replace(item, replacements)
    return changes


class JiraAPI:
    """Jira REST API v3 client.

    Uses API v3 which works with ADF (Atlassian Document Format) for
    rich text fields like description. This preserves all formatting
    including panels, tables, marks, code blocks, etc.

    Attributes:
        base_url: Jira site URL (e.g., https://example.atlassian.net)
        auth_header: Authorization header value (Basic auth)
        ssl_context: SSL context for HTTPS requests
    """

    def __init__(
        self,
        base_url: str,
        auth_header: str,
        ssl_context: ssl.SSLContext | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.auth_header = auth_header
        self.ssl_context = ssl_context
        logger.debug("JiraAPI initialized for %s", self.base_url)

    def _request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make an HTTP request to the Jira API.

        Args:
            method: HTTP method (GET, PUT, POST)
            endpoint: API endpoint path
            data: Request body data (will be JSON encoded)

        Returns:
            Parsed JSON response, or {"_status": code} for empty responses.

        Raises:
            IssueNotFoundError: If issue not found (404)
            APIError: If API request fails
        """
        url = f"{self.base_url}{endpoint}"
        logger.debug("%s %s", method, url)

        req = urllib.request.Request(url, method=method)
        req.add_header("Authorization", self.auth_header)
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "application/json")

        if data is not None:
            req.data = json.dumps(data).encode("utf-8")

        try:
            with urllib.request.urlopen(req, context=self.ssl_context) as resp:
                body = resp.read().decode("utf-8")
                if body:
                    return json.loads(body)
                return {"_status": resp.status}

        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else ""
            logger.error("API error: %s %s - %s", e.code, e.reason, error_body[:200])

            if e.code == 404:
                raise IssueNotFoundError("unknown", f"Resource not found: {endpoint}") from e

            raise APIError(e.code, e.reason, error_body) from e

        except urllib.error.URLError as e:
            logger.error("URL error: %s", e.reason)
            raise APIError(0, str(e.reason), "") from e

    def get_issue(
        self,
        issue_key: str,
        fields: str = "description,summary",
    ) -> dict[str, Any]:
        """Get Jira issue with ADF description via REST API v3.

        Args:
            issue_key: Jira issue key (e.g., 'BEP-2819')
            fields: Comma-separated field names to return

        Returns:
            Issue data including fields with ADF description.

        Raises:
            IssueNotFoundError: If issue key doesn't exist
            APIError: If API request fails
        """
        logger.info("Getting issue %s", issue_key)

        try:
            return self._request("GET", f"/rest/api/3/issue/{issue_key}?fields={fields}")
        except IssueNotFoundError:
            raise IssueNotFoundError(issue_key)

    def update_description(
        self,
        issue_key: str,
        description_adf: dict[str, Any],
    ) -> int:
        """Update issue description with ADF via REST API v3.

        Args:
            issue_key: Jira issue key (e.g., 'BEP-2819')
            description_adf: ADF document for the new description

        Returns:
            HTTP status code (204 = success).

        Raises:
            IssueNotFoundError: If issue key doesn't exist
            APIError: If API request fails
        """
        logger.info("Updating description for %s", issue_key)

        result = self._request(
            "PUT",
            f"/rest/api/3/issue/{issue_key}",
            {"fields": {"description": description_adf}},
        )
        status = result.get("_status", 200)
        logger.info("Updated %s (HTTP %d)", issue_key, status)
        return status

    def fix_description(
        self,
        issue_key: str,
        replacements: list[tuple[str, str]],
        dry_run: bool = False,
    ) -> tuple[bool, int]:
        """Fix issue description by replacing text in ADF nodes.

        High-level convenience method that:
        1. Gets the issue's ADF description
        2. Deep copies and applies text replacements
        3. Updates the issue (unless dry_run)

        Args:
            issue_key: Jira issue key
            replacements: List of (find, replace) tuples
            dry_run: If True, only check for matches without updating

        Returns:
            Tuple of (had_changes, change_count)
        """
        issue = self.get_issue(issue_key)
        summary = issue["fields"]["summary"]
        description = issue["fields"].get("description")

        logger.info("Processing %s: %s", issue_key, summary)

        if not description:
            logger.warning("%s has no description", issue_key)
            return False, 0

        modified = deepcopy(description)
        change_count = walk_and_replace(modified, replacements)

        if change_count == 0:
            logger.info("%s: no matches found", issue_key)
            return False, 0

        logger.info("%s: found %d replacement(s)", issue_key, change_count)

        if dry_run:
            logger.info("%s: DRY RUN - no changes applied", issue_key)
            return True, change_count

        status = self.update_description(issue_key, modified)
        if status in (200, 204):
            logger.info("%s: updated successfully", issue_key)
            return True, change_count

        logger.error("%s: update failed (HTTP %d)", issue_key, status)
        return False, change_count
