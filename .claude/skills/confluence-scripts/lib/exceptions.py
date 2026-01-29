"""Custom exceptions for Confluence scripts.

This module provides a hierarchy of exceptions for better error handling:
- ConfluenceError: Base exception for all Confluence-related errors
- CredentialsError: Raised when credentials loading fails
- PageNotFoundError: Raised when a page ID doesn't exist
- APIError: Raised when an API call fails
- ContentConversionError: Raised when content conversion fails
"""


class ConfluenceError(Exception):
    """Base exception for all Confluence operations."""

    pass


class CredentialsError(ConfluenceError):
    """Raised when credentials loading fails.

    Examples:
        - Credentials file not found
        - Missing required keys (CONFLUENCE_URL, USERNAME, API_TOKEN)
        - Invalid credentials format
    """

    pass


class PageNotFoundError(ConfluenceError):
    """Raised when a page ID doesn't exist.

    Attributes:
        page_id: The page ID that was not found
    """

    def __init__(self, page_id: str, message: str | None = None):
        self.page_id = page_id
        super().__init__(message or f"Page not found: {page_id}")


class APIError(ConfluenceError):
    """Raised when a Confluence API call fails.

    Attributes:
        status_code: HTTP status code
        reason: HTTP reason phrase
        details: Response body or additional details
    """

    def __init__(self, status_code: int, reason: str, details: str = ""):
        self.status_code = status_code
        self.reason = reason
        self.details = details
        super().__init__(f"API Error {status_code}: {reason}")


class ContentConversionError(ConfluenceError):
    """Raised when content conversion fails.

    Examples:
        - Invalid markdown syntax
        - Unsupported content elements
        - Malformed HTML in code blocks
    """

    pass


# --- Jira Exceptions ---


class JiraError(Exception):
    """Base exception for all Jira operations."""

    pass


class IssueNotFoundError(JiraError):
    """Raised when a Jira issue key doesn't exist.

    Attributes:
        issue_key: The issue key that was not found
    """

    def __init__(self, issue_key: str, message: str | None = None):
        self.issue_key = issue_key
        super().__init__(message or f"Issue not found: {issue_key}")
