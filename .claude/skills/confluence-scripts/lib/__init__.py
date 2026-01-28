"""Shared library modules for Confluence scripts.

Modules:
    exceptions: Custom exception classes
    auth: SSL context, credentials loading, authentication
    api: Confluence REST API client
    converters: Content conversion utilities
"""

from .exceptions import (
    ConfluenceError,
    CredentialsError,
    PageNotFoundError,
    APIError,
    ContentConversionError,
)
from .auth import (
    create_ssl_context,
    load_credentials,
    get_auth_header,
)
from .api import ConfluenceAPI
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
    # Auth
    "create_ssl_context",
    "load_credentials",
    "get_auth_header",
    # API
    "ConfluenceAPI",
    # Converters
    "markdown_to_storage",
    "create_code_macro",
    "fix_code_blocks",
    "convert_inline",
]
