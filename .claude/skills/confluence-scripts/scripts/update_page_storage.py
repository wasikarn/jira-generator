#!/usr/bin/env python3
"""
Update Confluence Page with raw storage format

This script updates a Confluence page using raw storage format,
allowing for proper macro support (ToC, Children, etc.)

Example usage:
    python update_page_storage.py --page-id 156598299 --content-file content.html
    python update_page_storage.py --page-id 156598299 --content "<h1>Title</h1><p>Content</p>"
"""

import urllib.request
import urllib.error
import json
import base64
import ssl
import argparse
from pathlib import Path

# Create SSL context that doesn't verify certificates (for macOS)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Load credentials from .env file
def load_credentials():
    """Load Atlassian credentials from ~/.config/atlassian/.env"""
    env_path = Path.home() / ".config/atlassian/.env"
    creds = {}
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                creds[key] = value
    return creds

creds = load_credentials()
CONFLUENCE_URL = creds['CONFLUENCE_URL']
USERNAME = creds['CONFLUENCE_USERNAME']
API_TOKEN = creds['CONFLUENCE_API_TOKEN']

def get_auth_header():
    """Create Basic Auth header"""
    auth_string = f"{USERNAME}:{API_TOKEN}"
    auth_bytes = base64.b64encode(auth_string.encode()).decode()
    return f"Basic {auth_bytes}"

def get_page(page_id):
    """Get Confluence page content"""
    url = f"{CONFLUENCE_URL}/rest/api/content/{page_id}?expand=body.storage,version,space"

    req = urllib.request.Request(url)
    req.add_header("Authorization", get_auth_header())
    req.add_header("Content-Type", "application/json")

    with urllib.request.urlopen(req, context=ssl_context) as response:
        return json.loads(response.read().decode())

def update_page(page_id, title, content, version):
    """Update existing Confluence page with raw storage format"""
    url = f"{CONFLUENCE_URL}/rest/api/content/{page_id}"

    data = {
        "id": page_id,
        "type": "page",
        "title": title,
        "body": {
            "storage": {
                "value": content,
                "representation": "storage"
            }
        },
        "version": {
            "number": version + 1
        }
    }

    req = urllib.request.Request(url, method="PUT")
    req.add_header("Authorization", get_auth_header())
    req.add_header("Content-Type", "application/json")
    req.data = json.dumps(data).encode()

    with urllib.request.urlopen(req, context=ssl_context) as response:
        return json.loads(response.read().decode())

def main():
    parser = argparse.ArgumentParser(
        description='Update Confluence page with raw storage format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Update from file
  python update_page_storage.py --page-id 156598299 --content-file content.html

  # Update with inline content
  python update_page_storage.py --page-id 156598299 --content "<h1>Title</h1>"

  # Dry run (preview only)
  python update_page_storage.py --page-id 156598299 --content-file content.html --dry-run
        """
    )

    parser.add_argument('--page-id', required=True, help='Page ID to update')
    parser.add_argument('--content', help='Raw storage format content (inline)')
    parser.add_argument('--content-file', help='Path to file with storage format content')
    parser.add_argument('--title', help='New title (optional, keeps existing if not specified)')
    parser.add_argument('--dry-run', action='store_true', help='Preview without saving')

    args = parser.parse_args()

    # Get content
    if args.content_file:
        with open(args.content_file, 'r') as f:
            storage_content = f.read()
    elif args.content:
        storage_content = args.content
    else:
        print("Error: Specify --content or --content-file")
        return 1

    try:
        # Get current page info
        page = get_page(args.page_id)
        title = args.title or page['title']
        version = page['version']['number']

        print(f"📄 Page: {title}")
        print(f"   ID: {args.page_id}")
        print(f"   Current version: {version}")

        if args.dry_run:
            print(f"\n🔍 DRY RUN - Storage content preview:")
            print("=" * 60)
            print(storage_content[:500])
            if len(storage_content) > 500:
                print(f"... ({len(storage_content) - 500} more characters)")
            print("=" * 60)
            return 0

        # Update the page
        result = update_page(args.page_id, title, storage_content, version)
        print(f"✅ Updated to version {result['version']['number']}")
        print(f"   URL: {CONFLUENCE_URL}/pages/viewpage.action?pageId={args.page_id}")

        return 0

    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error: {e.code} - {e.reason}")
        error_body = e.read().decode()
        print(f"Details: {error_body[:500]}")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
