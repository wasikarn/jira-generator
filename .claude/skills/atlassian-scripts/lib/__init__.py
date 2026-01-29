"""Shared library modules for Atlassian scripts.

Modules:
    exceptions: Custom exception classes (Confluence + Jira)
    auth: SSL context, credentials loading, authentication
    api: Confluence REST API client
    jira_api: Jira REST API v3 client (ADF manipulation)
    converters: Content conversion utilities
"""

from .exceptions import (
    ConfluenceError,
    CredentialsError,
    PageNotFoundError,
    APIError,
    ContentConversionError,
    JiraError,
    IssueNotFoundError,
)
from .auth import (
    create_ssl_context,
    load_credentials,
    get_auth_header,
)
from .api import ConfluenceAPI
from .jira_api import (
    JiraAPI,
    derive_jira_url,
    walk_and_replace,
)
from .converters import (
    markdown_to_storage,
    create_code_macro,
    fix_code_blocks,
    convert_inline,
)

__all__ = [
    # Exceptions
    "ConfluenceError",
    "CredentialsError",
    "PageNotFoundError",
    "APIError",
    "ContentConversionError",
    "JiraError",
    "IssueNotFoundError",
    # Auth
    "create_ssl_context",
    "load_credentials",
    "get_auth_header",
    # API - Confluence
    "ConfluenceAPI",
    # API - Jira
    "JiraAPI",
    "derive_jira_url",
    "walk_and_replace",
    # Converters
    "markdown_to_storage",
    "create_code_macro",
    "fix_code_blocks",
    "convert_inline",
]
