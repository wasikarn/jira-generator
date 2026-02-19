"""Authentication utilities for Confluence API.

This module provides authentication and credential management:
- SSL context creation (with certificate verification bypass for macOS)
- Credentials loading from environment file
- Basic Auth header generation

Usage:
    from lib.auth import create_ssl_context, load_credentials, get_auth_header

    ssl_ctx = create_ssl_context()
    creds = load_credentials()
    auth_header = get_auth_header(creds["CONFLUENCE_USERNAME"], creds["CONFLUENCE_API_TOKEN"])
"""

import base64
import logging
import ssl
from pathlib import Path
from typing import TypedDict

from .exceptions import CredentialsError

logger = logging.getLogger(__name__)

# Default credentials file location
DEFAULT_CREDENTIALS_PATH = Path.home() / ".config/atlassian/.env"

# Required credential keys
REQUIRED_KEYS = frozenset({"CONFLUENCE_URL", "CONFLUENCE_USERNAME", "CONFLUENCE_API_TOKEN"})


class Credentials(TypedDict):
    """Type definition for Confluence credentials."""

    CONFLUENCE_URL: str
    CONFLUENCE_USERNAME: str
    CONFLUENCE_API_TOKEN: str


def create_ssl_context() -> ssl.SSLContext:
    """Create SSL context with proper certificate verification.

    Attempts to use certifi for reliable cross-platform certificate handling.
    Falls back to system certificates, then to verification disabled as last resort.

    Returns:
        ssl.SSLContext: Configured SSL context.
    """
    # Try certifi first (most reliable cross-platform)
    try:
        import certifi
        ctx = ssl.create_default_context(cafile=certifi.where())
        logger.debug("Created SSL context with certifi certificates")
        return ctx
    except ImportError:
        pass

    # Try system certificates
    try:
        ctx = ssl.create_default_context()
        # Quick validation — if this doesn't raise, system certs are usable
        logger.debug("Created SSL context with system certificates")
        return ctx
    except ssl.SSLError:
        pass

    # Last resort: disable verification (macOS cert store issues)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    logger.warning("Created SSL context with verification DISABLED (install certifi for proper TLS)")
    return ctx


def load_credentials(path: Path | None = None) -> Credentials:
    """Load Atlassian credentials from environment file.

    Args:
        path: Path to credentials file. Defaults to ~/.config/atlassian/.env

    Returns:
        Credentials dictionary with URL, username, and API token.

    Raises:
        CredentialsError: If file not found, unreadable, or missing required keys.

    Example file format:
        CONFLUENCE_URL=https://example.atlassian.net/wiki
        CONFLUENCE_USERNAME=user@example.com
        CONFLUENCE_API_TOKEN=your-api-token
    """
    env_path = path or DEFAULT_CREDENTIALS_PATH

    if not env_path.exists():
        raise CredentialsError(f"Credentials file not found: {env_path}")

    logger.debug("Loading credentials from %s", env_path)
    creds: dict[str, str] = {}

    try:
        with open(env_path, encoding="utf-8") as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    logger.warning("Skipping malformed line %d: no '=' found", line_num)
                    continue
                key, value = line.split("=", 1)
                creds[key.strip()] = value.strip()
    except OSError as e:
        raise CredentialsError(f"Failed to read credentials file: {e}") from e

    # Validate required keys
    missing_keys = REQUIRED_KEYS - creds.keys()
    if missing_keys:
        raise CredentialsError(f"Missing required keys in credentials file: {', '.join(sorted(missing_keys))}")

    logger.debug("Loaded credentials for %s", creds.get("CONFLUENCE_USERNAME", "unknown"))

    return Credentials(
        CONFLUENCE_URL=creds["CONFLUENCE_URL"],
        CONFLUENCE_USERNAME=creds["CONFLUENCE_USERNAME"],
        CONFLUENCE_API_TOKEN=creds["CONFLUENCE_API_TOKEN"],
    )


def get_auth_header(username: str, api_token: str) -> str:
    """Create Basic Auth header value.

    Args:
        username: Atlassian username (email).
        api_token: Atlassian API token.

    Returns:
        Authorization header value in format "Basic <base64-encoded-credentials>"

    Example:
        >>> header = get_auth_header("user@example.com", "token123")
        >>> header
        'Basic dXNlckBleGFtcGxlLmNvbTp0b2tlbjEyMw=='
    """
    auth_string = f"{username}:{api_token}"
    auth_bytes = base64.b64encode(auth_string.encode("utf-8")).decode("ascii")
    return f"Basic {auth_bytes}"
